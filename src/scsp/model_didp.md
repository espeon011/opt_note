In [ ]:
```python
import enum
from collections.abc import Callable
import didppy
import util

# Dual Bound を追加で設定する関数の型
type TypeBoundExprFunc = Callable[
    [list[str], didppy.Model, list[didppy.ElementVar]],
    didppy.IntExpr
]
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# DIDP を用いたモデル

考案者の解説記事: [動的計画法ベースの数理最適化ソルバDIDPPyで最短共通超配列問題を解く](https://zenn.dev/okaduki/articles/7f9a3f3c54bc98)

In [ ]:
```python
def boundtable_scs2(s1: str, s2: str) -> list[list[int]]:
    len1, len2 = len(s1), len(s2)

    dp = [[len1 + len2 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i1 in range(len1 + 1):
        dp[i1][len2] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2] = len2 - i2

    for i1 in range(len1 - 1, -1, -1):
        for i2 in range(len2 - 1, -1, -1):
            if s1[i1] == s2[i2]:
                dp[i1][i2] = dp[i1 + 1][i2 + 1] + 1
            else:
                dp[i1][i2] = min(dp[i1 + 1][i2], dp[i1][i2 + 1]) + 1

    return dp
```

In [ ]:
```python
def boundexpr_scs2len(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    exprs = []
    for idx1, (s1, index_var1) in enumerate(zip(instance, index_vars)):
        for idx2, (s2, index_var2) in enumerate(zip(instance, index_vars)):
            if idx2 >= idx1:
                continue
            table_idx1_idx2 = dpmodel.add_int_table(boundtable_scs2(s1, s2))
            exprs.append(table_idx1_idx2[index_var1, index_var2])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound
```

In [ ]:
```python
class Model:
    def __init__(
        self,
        instance: list[str],
        extra_bounds: list[TypeBoundExprFunc] | None = None,
    ):
        chars = sorted(list(set("".join(instance))))

        dpmodel = didppy.Model(maximize=False, float_cost=False)

        index_types = [dpmodel.add_object_type(number=len(s) + 1) for s in instance]
        index_vars = [
            dpmodel.add_element_var(object_type=index_type, target=0)
            for index_type in index_types
        ]

        instance_table = dpmodel.add_element_table(
            [
                [
                    chars.index(c) for c in s
                ] + [len(chars)]
                for s in instance
            ]
        )

        dpmodel.add_base_case(
            [
                index_var == len(s)
                for s, index_var in zip(instance, index_vars)
            ]
        )

        # 文字 char に従って進む
        for id_char, char in enumerate(chars):
            condition = didppy.Condition(False)
            for sidx, index_var in enumerate(index_vars):
                condition |= (instance_table[sidx, index_var] == id_char)
            trans = didppy.Transition(
                name=f"{char}",
                cost=1 + didppy.IntExpr.state_cost(),
                effects=[
                    (
                        index_var,
                        (
                            instance_table[sidx, index_var] == id_char
                        ).if_then_else(index_var + 1, index_var),
                    )
                    for sidx, index_var in enumerate(index_vars)
                ],
                preconditions=[condition],
            )
            dpmodel.add_transition(trans)

        # 残っている文字列から 2 つを選んで SCS を取って長さが最大のものを Dual Bound とする. 
        dpmodel.add_dual_bound(boundexpr_scs2len(instance, dpmodel, index_vars))

        # 追加の Dual Bound があれば. 
        if extra_bounds:
            for bound_func in extra_bounds:
                dpmodel.add_dual_bound(bound_func(instance, dpmodel, index_vars))

        self.instance = instance
        self.dpmodel = dpmodel
        self.dpsolver = None
        self.solution = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.dpsolver = didppy.CABS(self.dpmodel, threads=12, time_limit=time_limit, quiet=(not log))
        self.solution = self.dpsolver.search()
        return self

    def to_solution(self) -> str:
        return "".join([trans.name for trans in self.solution.transitions])
```

In [ ]:
```python
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    model = Model(instance)
    model.solve(time_limit, log)
    return model.to_solution()
```

In [ ]:
```python
instance_01 = util.parse("uniform_q26n004k015-025.txt")
model_01 = Model(instance_01)
solution_01 = model_01.solve().to_solution()
```

In [ ]:
```python
_instance = instance_01
_model = model_01
_solution = solution_01

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 62) ---
>  Sol: ultckignkycosoevjuaiqfozhgmpplnbrxddbxcsvrvsnhntuqgpxzvxissbxf
> str1: --t-k-gnk--------u------h-mp-----x----------nh-t-qg-xzvxis----
> str2: -----i-----o----j--iqfo------lnb-x---xc-v--s----uq-p--v-issbxf
> str3: ul-c-i-n-ycoso-v------oz---ppl---------------------p----------
> str4: -----ig-------ev--a----z-g-----br-ddb-csvrv-n-n---g----------f
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 62
> ```

In [ ]:
```python
instance_02 = util.parse("uniform_q26n008k015-025.txt")
model_02 = Model(instance_02)
solution_02 = model_02.solve().to_solution()
```

In [ ]:
```python
_instance = instance_02
_model = model_02
_solution = solution_02

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 26 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> str5: pyplrzxucpmqvgtdfuivcdsbo
> str6: pbdevdcvdpfzsmsbroqvbbh
> str7: enbczfjtvxerzbrvigple
> str8: rxwxqkrdrlctodtmprpxwd
> 
> --- Solution (of length 98) ---
>  Sol: tikojiqgfpobydeplnbrxvcazwxqgkbrfdrulhcpmqvjgtdpfuivxerbnyczodsohtvmpsubroqgxzpvnxnigplewpssbbhxdf
> str1: t-k----g---------n-----------k-----u-h--m------p----x---n-------ht--------qgxz-v-x-i------s-------
> str2: -i-ojiq-f-o-----lnb-x-----x-----------c---v-------------------s-------u---q---pv---i------ssb--x-f
> str3: -----------------------------------ul-c-----------i-----nyc-o-so--v------o---zp------pl--p--------
> str4: -i-----g------e------v-az---g-br-d------------d--------b--c---s---v-----r------vn-n-g------------f
> str5: ---------p--y--pl--r----z-x--------u--cpmqv-gtd-fuiv------c--ds--------b-o------------------------
> str6: ---------p-b-de------v-----------d----c---v---dpf----------z--s----m-s-broq----v------------bbh---
> str7: --------------e--nb---c-z-------f----------j-t-----vxer----z-----------br------v---igple----------
> str8: -------------------rx----wxq-k-r-dr-l-c------t--------------od---t-mp---r-----p--x------w-------d-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 56
> ```

In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
model_03 = Model(instance_03)
solution_03 = model_03.solve().to_solution()
```

In [ ]:
```python
_instance = instance_03
_model = model_03
_solution = solution_03

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 26 chars) ---
> str01: tkgnkuhmpxnhtqgxzvxis
> str02: iojiqfolnbxxcvsuqpvissbxf
> str03: ulcinycosovozpplp
> str04: igevazgbrddbcsvrvnngf
> str05: pyplrzxucpmqvgtdfuivcdsbo
> str06: pbdevdcvdpfzsmsbroqvbbh
> str07: enbczfjtvxerzbrvigple
> str08: rxwxqkrdrlctodtmprpxwd
> str09: kkqafigqjwokkskrblg
> str10: lxxpabivbvzkozzvd
> str11: krifsavncdqwhzc
> str12: qaxudgqvqcewbfgijowwy
> str13: rsxqjnfpadiusiqbezhkohmg
> str14: iwshvhcomiuvddm
> str15: htxxqjzqbctbakn
> str16: xusfcfzpeecvwantfmgqzu
> 
> --- Solution (of length 148) ---
>   Sol: pyplrsxiboqjdgtuswevaizkgxqnfokulnpbrdcfzgpqahfjtmvdpxiuserlxgqefbnychvjeziwsgtuhaqomdkvsbncptfeomurvzdgihkoxsgzpkuqvcrnjbdsbowphzxlavknwdimgfpeysuc
> str01: --------------t--------kg--n--ku-------------h---m--px------------n--h--------t---q--------------------g----x--z----v-------------x-------i------s--
> str02: -------i-o-j---------i----q-fo--ln-b-----------------x------x-------c-v-----s--u--q---------p-------v---i----s-------------sb-----x----------f------
> str03: ---------------u----------------l-----c---------------i-----------nyc--------------o----s-------o---v------o---zp--------------p---l----------p-----
> str04: -------i-----g----eva-z-g----------brd-------------d-------------b--c-------s----------v-----------rv------------------n---------------n----gf------
> str05: pyplr-----------------z--x-----u------c---p------m------------q-------v------gt------d--------f---u-----i-----------vc----dsbo----------------------
> str06: p-------b---d-----ev-----------------dc-----------vdp-----------f--------z--s-------m---sb---------r-------o-------qv----b--b---h-------------------
> str07: ------------------e--------n-------b--c-z-----fjt-v--x---er--------------z---------------b---------rv---i-----g-p------------------l-----------e----
> str08: ----r-x----------w-------xq---k-----rd--------------------rl--------c---------t----o-d-------t---m--------------p-----r--------p--x-----wd----------
> str09: -----------------------k------k------------qa-f-------i------gq--------j---w-------o--k-------------------k--s---k----r--b---------l--------g-------
> str10: ---l--x------------------x--------p---------a--------------------b--------i------------v-b----------vz----ko---z-----------------z---v---d----------
> str11: -----------------------k------------r-----------------i---------f-----------s----a-----v--nc----------d------------q----------w-hz-----------------c
> str12: ----------q---------a----x-----u-----d---g-q------v-----------q-----c---e--w-------------b----f--------gi---------------j----ow---------w-------y---
> str13: ----rsx---qj---------------nf-----p---------a------d--ius-----------------i-------q------b-----e-----z---hko--------------------h----------mg-------
> str14: -------i---------w--------------------------------------s------------hv---------h----------c----om------i---------u-v-----d--------------d-m--------
> str15: ---------------------------------------------h--t----x------x-q--------j-z--------q------b-c-t---------------------------b----------a-kn------------
> str16: ------x--------us-----------f---------cfz-p--------------e-----e----c-v----w-----a--------n--tf--m-----g-----------q-------------z----------------u-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 49
> ```

In [ ]:
```python
instance_04 = util.parse("uniform_q05n010k010-010.txt")
model_04 = Model(instance_04)
solution_04 = model_04.solve().to_solution()
```

In [ ]:
```python
_instance = instance_04
_model = model_04
_solution = solution_04

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 5 chars) ---
> str01: dcbccdbcce
> str02: bddbeeeebd
> str03: cacdeecebe
> str04: aeddddebdd
> str05: acbeecabce
> str06: bbabebdcba
> str07: bbaeaebada
> str08: eeeecbdbee
> str09: ccdeedadcd
> str10: bdabdbeaad
> 
> --- Solution (of length 27) ---
>   Sol: bbaeddcbeacdeecbdbecabdcead
> str01: ----d-cb--c---c-db-c---ce--
> str02: b---dd-be---ee----e--bd----
> str03: ------c--acdeec---e--b--e--
> str04: --aedd-----d----d-e--bd---d
> str05: --a---cbe---e-c-----ab-ce--
> str06: bba----be------bd--c-b---a-
> str07: bbae-----a--e--b----a-d--a-
> str08: ---e----e---eecbdbe-----e--
> str09: ------c---cdee--d---a-dc--d
> str10: b---d----a-----bdbe-a----ad
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 27
> ```

In [ ]:
```python
instance_05 = util.parse("uniform_q05n050k010-010.txt")
model_05 = Model(instance_05)
solution_05 = model_05.solve().to_solution()
```

In [ ]:
```python
_instance = instance_05
_model = model_05
_solution = solution_05

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 5 chars) ---
> str01: dcbccdbcce
> str02: bddbeeeebd
> str03: cacdeecebe
> str04: aeddddebdd
> str05: acbeecabce
> str06: bbabebdcba
> str07: bbaeaebada
> str08: eeeecbdbee
> str09: ccdeedadcd
> str10: bdabdbeaad
> str11: ededaaaeaa
> str12: aaeaabeeac
> str13: eaabcaccdb
> str14: bdeeadeade
> str15: caedadeeed
> str16: ebcadbabbe
> str17: ddceeabdea
> str18: dabcddeaec
> str19: aadceedaab
> str20: aeecceeeaa
> str21: bbdaecaade
> str22: dacedaedab
> str23: aaeabbbbce
> str24: dedbcbcaab
> str25: dbdaaebbcb
> str26: debedbebac
> str27: ceebcdcbde
> str28: dbedaadaab
> str29: cccdcbebdc
> str30: aeeacdbcbd
> str31: dacbeacccd
> str32: ecebccdbdb
> str33: ddbbcedabb
> str34: aaeabaaeba
> str35: ecbbcaadcd
> str36: debccecdbc
> str37: daacbaeebc
> str38: adabeaacce
> str39: daecdbacaa
> str40: dacbbdcedc
> str41: dedbeebbde
> str42: cdadcdcdaa
> str43: ceedcbaeed
> str44: ceaecaaaca
> str45: dcccebbbad
> str46: baeeaebbde
> str47: dbdebaccdb
> str48: ebcbeedaea
> str49: aeeebbdbca
> str50: dbdabcecbb
> 
> --- Solution (of length 34) ---
>   Sol: dabecedbaecdabcdeaecbdeabceadbcead
> str01: d---c--b--c---cd----b----c----ce--
> str02: --b---d----d-b--e-e---e---e--b---d
> str03: ----c---a-cd----e-ec--e-b-e-------
> str04: -a-e--d----d---d-----de-b---d----d
> str05: -a--c--b-e------e--c---abce-------
> str06: --b----ba----b--e---bd---c---b--a-
> str07: --b----bae--a---e---b--a----d---a-
> str08: ---e-e---e------e--cbd--b-e----e--
> str09: ----c-----cd----e-e--d-a----d-c--d
> str10: --b---d-a----b-d----b-ea---ad-----
> str11: ---e--d--e-da----a-----a--ea----a-
> str12: -a------ae--a----a--b-e---ea--c---
> str13: ---e----a---abc--a-c-----c--db----
> str14: --b---d--e------ea---dea----d--e--
> str15: ----c---ae-da--de-e---e-----d-----
> str16: ---e---b--c-a--d----b--ab----b-e--
> str17: d-----d---c-----e-e----ab---d--ea-
> str18: dab-c-d----d----eaec--------------
> str19: -a------a--d--c-e-e--d-a---a-b----
> str20: -a-e-e----c---c-e-e---ea---a------
> str21: --b----b---da---e--c---a---ad--e--
> str22: da--ced-ae-dab--------------------
> str23: -a------ae--ab------b---b----bce--
> str24: d--e--db--c--bc--a-----ab---------
> str25: d-b---d-a---a---e---b---bc---b----
> str26: d--e---b-e-d-b--e---b--a-c--------
> str27: ----ce---e---bcd---cbde-----------
> str28: d-be--d-a---a--d-a-----ab---------
> str29: ----c-----c---cd---cb-e-b---d-c---
> str30: -a-e-e--a-cd-bc-----bd------------
> str31: da--c--b-e--a-c----c-----c--d-----
> str32: ---ece-b--c---cd----bd--b---------
> str33: d-----db-----bc-e----d-ab----b----
> str34: -a------ae--ab---a-----a--e--b--a-
> str35: ---ec--b-----bc--a-----a----d-c--d
> str36: d--e---b--c---c-e--c-d--bc--------
> str37: da------a-c--b---ae---e-bc--------
> str38: -a----d-a----b--ea-----a-c----ce--
> str39: da-ec-dba-c-a----a----------------
> str40: da--c--b-----b-d---c--e-----d-c---
> str41: d--e--db-e------e---b---b---d--e--
> str42: ----c-d-a--d--cd---c-d-a---a------
> str43: ----ce---e-d--c-----b--a--e----e-d
> str44: ----ce--aec-a----a-----a-c-a------
> str45: d---c-----c---c-e---b---b----b--ad
> str46: --b-----ae------eae-b---b---d--e--
> str47: d-b---d--e---b---a-c-----c--db----
> str48: ---e---b--c--b--e-e--d-a--ea------
> str49: -a-e-e---e---b------bd--bc-a------
> str50: d-b---d-a----bc-e--cb---b---------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 24
> ```

In [ ]:
```python
instance_06 = util.parse("nucleotide_n010k010.txt")
model_06 = Model(instance_06)
solution_06 = model_06.solve().to_solution()
```

In [ ]:
```python
_instance = instance_06
_model = model_06
_solution = solution_06

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 4 chars) ---
> str01: ATGGGATACG
> str02: ATACCTTCCC
> str03: CACGAATTGA
> str04: TAAAATCTGT
> str05: AGGTAACAAA
> str06: TTCCTAGGTA
> str07: TTGTAGATCT
> str08: TGGGAAGTTC
> str09: TTCCACAACT
> str10: TCTAAACGAA
> 
> --- Solution (of length 24) ---
>   Sol: TACTACGCGGTAATCGAATCGTAC
> str01: -A-T--G-GG-A-T--A--CG---
> str02: -A-TAC-C--T--TC----C---C
> str03: --C-ACG----AAT----T-G-A-
> str04: TA--A------AATC---T-GT--
> str05: -A----G-G-TAA-C-AA----A-
> str06: T--T-C-C--TA---G----GTA-
> str07: T--T--G---TA---GA-TC-T--
> str08: T-----G-GG-AA--G--T--T-C
> str09: T--T-C-C---A--C-AA-C-T--
> str10: T-CTA------AA-CGAA------
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 24
> ```

In [ ]:
```python
instance_07 = util.parse("nucleotide_n050k050.txt")
model_07 = Model(instance_07)
solution_07 = model_07.solve().to_solution()
```

In [ ]:
```python
_instance = instance_07
_model = model_07
_solution = solution_07

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 5 chars) ---
> str01: TAGTAGTAGACTCCGGAAGTGACAAACCCTGAAAAGAATGGATAAATATA
> str02: GGATAAACACTCCCGAAAATAATTTGACTTAAACAACGCGACAGTTCAAG
> str03: ATACCTTCCTAGGTAACAAACCAACCAACTTTTGATCTCTTGTAGATCTG
> str04: TAAATTATAATCTTATACTAGTAAAAAATAGGGTGTAACCGAAAACGGTC
> str05: TTAAAACAGCCTGTGGGTTGCACCCACTCACAGGGCCCACTGGGCGCAAG
> str06: ATGACTTCCAATGGATCCCAACCTCAAGCTTCCACCCCAATGGTTTCAGC
> str07: AACAAACCAACCAACTTTTGATCTCTTGTAGATCTGTTCTCTAAACGAAC
> str08: ATGAAAACGAAAATTATTATCAAGGGTATGGAAGTGGAAGCTGACGAAAT
> str09: ACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTA
> str10: TTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTC
> str11: GCAGAGCATTTTCTAATATCCACAAAATGAAGGCAATAATTGTACTACTC
> str12: ATGAGCCAAGATCCGACGAAGAGCCCCAAGGAGGAGAAGGAGGGACCCCC
> str13: TCTCACAGTTCAAGAACCCAAAGTACCCCCCATAGCCCTCTTAAAGCCAC
> str14: AGGTTTATACCTTCCTAGGTAACAAACCAACCAACTTTCGATCTCTTGTA
> str15: AGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTA
> str16: TAAAACAACTCAATACAACATAAGAAAATCAACGCAAAAACACTCACAAA
> str17: CCGCCCATTTGGGCGGCTCTCGAGCGATAGCTCGTCGAATCCCTCGACCT
> str18: ATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTG
> str19: TCTCACAGTTCAAGAACCTCAAGTCTCCCCCATAGGCCTCTTTCAGTCAG
> str20: GATCTCTCTCACCGAACCTGGCCCCGGGCAAATGCCCTAATCCAGAGGTG
> str21: AGAGCAATCAGTGCATCAGAAATATACCTATTATACACTTTGCTAAGAAT
> str22: AATTAAAACATCTCAATACAACATAAGAAAAACAACGCAAAAACACTCAT
> str23: AAACGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGC
> str24: ATAACTAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTG
> str25: ATGAGTGTCACGAATTCACGTACAATGAACTGGATGTTCACGTGGAATAA
> str26: ACCGTGGGCGAGCGGTGACCGGTGTCTTCCTAGTGGGTCCCACGTTGAAR
> str27: AAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTG
> str28: AGTAGTTCGCCTGTGTGAGCTGACAAACTTAGTAGTGTTTGTGAGGATTA
> str29: TTTATACCTTCCTAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGAT
> str30: ATGCGGTCGTCTCTCCCCGGCTTTTTTTCCCCGCGCCGCGTTGGCGCCGA
> str31: GTGACAAAAACATAATGGACTCCAACACCATGTCAAGCTTTCAGGTAGAC
> str32: GTGTAAGAAACAGTAAGCCCGGAAGTGGTGTTTTGCGATTTCGAGGCCGG
> str33: GAGAATGAGTCTCATTACCGCCCGGTACTTAGCAAGCTAATAGTCACGGC
> str34: ATGTGGTCGATGCCATGGAGGCCCACCAGTTCATTAAGGCTCCTGGCATT
> str35: ACGAGCGTTTTAAGGGCCCGCGACTGCGACGGCCACATGGCCCTGTATGT
> str36: GGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAG
> str37: TGGGAAGTTCCAAAAGATCACAAAACACTACCAGTCAACCTGAAGTACAC
> str38: GAAGCGTTAACGTGTTGAGGAAAAGACAGCTTAGGAGAACAAGAGCTGGG
> str39: ACCAGCGCACTTCGGCAGCGGCAGCACCTCGGCAGCACCTCAGCAGCAAC
> str40: ATGGGACAACTTATTCCTATCATGTGCCAAGAGGTTTTACCCGGTGACCA
> str41: TTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGTTGTCACTC
> str42: AACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAACGAACTTTA
> str43: GGGTTCTGCCAGGCATAGTCTTTTTTTCTGGCGGCCCTTGTGTAAACCTG
> str44: GGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTACTGT
> str45: TGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTACTGTCGT
> str46: TTCCACAACTTTCCACCAAGCTCTGCAAGATCCCAGAGTCAGGGGCCTGT
> str47: TCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAG
> str48: ACCGGATGGCCGCGATTTTTCGGAGTCCTTGGGGGACCACTCAGAATAGA
> str49: CTTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACT
> str50: ATGAGCACTAAGCGAAGAACCAAAAAGCAGACAATACAACCCGCTATTAC
> 
> --- Solution (of length 133) ---
>   Sol: ATGACCGTAGTAACGTCAATGCATGCTACAGTCAGTCAGTAGCTAGCTACGTGCATCAGAGTCACGTACATGCTAGACTCGAGTACGATCATGCAGACTCGTATCGATCCGTACGTAGCTAGTCACGTAGCTR
> str01: -T-A--GTAGTA--G--A---C-T-C--C-G---G--A--AG-T-G--AC----A--A-A--C-C---C-TG--A-A----A--A-GA--ATG--GA-T---A---A-----A--TA--TA------------
> str02: --G---G-A-TAA----A---CA--CT-C---C---C-G-A---A---A-----AT-A-A-T----T---TG--A--CT----TA--A--A--CA-AC--G---CGA-C---A-GT---T---CA---AG---
> str03: AT-ACC-T--T--C--C--T--A-G-----GT-A---A----C-A---A-----A-C-----CA---AC---C-A-ACT----T----T--TG-A---TC-T--C--T---T--GTAG--A-TC---T-G---
> str04: -T-A----A--A---T---T--AT---A-A-TC--T---TA--TA-CTA-GT--A--A-A---A---A-AT---AG----G-GT--G-T-A---A--C-CG-A---A-----A---A-C--G----GT--C--
> str05: -T-----TA--AA----A---CA-GC--C--T--GT--G--G---G-T---TGCA-C-----C-C--AC-T-C-A--C---AG---G-----GC---C-C--A-C--T--G---G--GC--G-CA---AG---
> str06: ATGAC--T--T--C--CAATG---G--A---TC---C-----C-A---AC---C-TCA-AG-C---T---T-C----C---A---C---C---C---C----A---AT--G---GT---T--TCA-G---C--
> str07: A--AC---A--AAC--CAA--C---C-A-A--C--T---T---T---T--G---ATC----TC---T---TG-TAGA-TC---T--G-T--T-C----TC-TA---A-----ACG-A---A--C---------
> str08: ATGA----A--AACG--AA---A----A---T---T-A-T---TA--T-C----A--AG-G----GTA--TG---GA----AGT--G-----G-A-A---G---C--T--G-ACG-A---A---A--T-----
> str09: A---C--T-----CG-----GC-TGC-A---T--G-C--T---TAG-T--G--CA-C----TCACG--CA-G-TA---T--A--A---T--T--A-A-T---A---A-C--TA---A--T--T-A--------
> str10: -T-----T-GTA--G--A-T-C-TG-T----TC--TC--TA---A---ACG---A--A----C---T---T--TA-A----A--A---TC-TG-----T-GT---G----G--C-T-G-T---CAC-T--C--
> str11: --G-C---AG-A--G-CA-T---T--T----TC--T-A--A--TA--T-C---CA-CA-A---A---A--TG--A-A---G-G--C-A--AT--A-A-T--T---G-T----AC-TA-CT---C---------
> str12: ATGA--G------C--CAA-G-AT-C--C-G--A--C-G-A---AG--A-G--C--C-----C-C--A-A-G---GA---G-G-A-GA--A-G--GA---G----G----G-AC----C----C-C----C--
> str13: -T--C--T-----C---A---CA-G-T----TCA---AG-A---A-C--C---CA--A-AGT-AC---C---C----C-C-----C-AT-A-GC---C-C-T--C--T---TA---A---AG-C-C--A-C--
> str14: A-G---GT--T----T-A-T--A--C--C--T---TC-----CTAG----GT--A--A----CA---A-A--C----C---A--AC---CA---A--CT--T-TCGATC--T-C-T---T-GT-A--------
> str15: A-G---GT--T----T-A-T--A--C--C--T---TC-----C---C-A-G-G--T-A-A--CA---A-A--C----C---A--AC---CA---A--CT--T-TCGATC--T-C-T---T-GT-A--------
> str16: -T-A----A--AAC---AA--C-T-C-A-A-T-A--CA--A-C-A--TA-----A---GA---A---A-AT-C-A-AC--G----C-A--A---A-A-----A-C-A-C--T-C--A-C-A---A---A----
> str17: ----CCG------C--C----CAT--T----T--G---G--GC--G----G--C-TC----TC--G-A---GC--GA-T--AG--C--TC--G-----TCG-A---ATCC---C-T--C--G--AC----CT-
> str18: AT-ACC-T--T--C--C----CA-G-----GT-A---A----C-A---A-----A-C-----CA---AC---C-A-ACT----T----TC--G-A---TC-T--C--T---T--GTAG--A-TC---T-G---
> str19: -T--C--T-----C---A---CA-G-T----TCA---AG-A---A-C--C-T-CA--AG--TC---T-C---C----C-C-----C-AT-A-G--G-C-C-T--C--T---T---T--C-AGTCA-G------
> str20: --GA---T-----C-TC--T-C-T-C-AC---C-G--A--A-C---CT--G-GC--C-----C-CG-----G---G-C---A--A--AT---GC---C-C-TA---ATCC--A-G-AG---GT---G------
> str21: A-GA--G------C---AAT-CA-G-T---G-CA-TCAG-A---A---A--T--AT-A----C-C-TA--T--TA---T--A---C-A-C-T------T--T---G--C--TA---AG--A---A--T-----
> str22: A--A---T--TAA----AA--CAT-CT-CA---A-T-A----C-A---AC----AT-A-AG--A---A-A----A-AC---A--ACG--CA---A-A-----A---A-C---AC-T--C-A-T----------
> str23: A--A----A----CG--AA--C-T--T----T-A---A--A---A--T-C-TG--T--G--T---G-----GCT-G--TC-A---C--TC--G--G-CT-G---C-AT--G--C-T---TAGT---G---C--
> str24: AT-A----A----C-T-AAT---T---AC--T--GTC-GT---T-G--AC----A---G-G--AC--AC--G--AG--T--A--AC--TC--G-----TC-TATC--T---T-C-T-G---------------
> str25: ATGA--GT-GT--C---A---C--G--A-A-T---TCA----C--G-TAC----A--A---T---G-A-A--CT-G----GA-T--G-T--T-CA--C--GT---G----G-A---A--TA---A--------
> str26: A---CCGT-G----G-----GC--G--A--G-C-G---GT-G--A-C--CG-G--T--G--TC---T---T-C----CT--AGT--G-----G--G--TC----C---C---ACGT---T-G--A---A---R
> str27: A--A----AG----GT---T---T---A---T-A--C-----CT---T-C---C--CAG-GT-A---ACA----A-AC-C-A--AC---CA---A--CT--T-TCGATC--T-C-T---T-G-----------
> str28: A-G----TAGT----TC---GC---CT---GT--GT--G-AGCT-G--AC----A--A-A--C---T---T---AG--T--AGT--G-T--T------T-GT---GA---G---G-A--T--T-A--------
> str29: -T-----T--TA---T-A---C---CT----TC---C--TAG---G-TA-----A-CA-A---AC---CA----A--C-C-A--AC--T--T------TCG-ATC--TC--T---T-G-TAG--A--T-----
> str30: ATG-C-G--GT--CGTC--T-C-T-C--C---C---C-G--GCT---T---T---T-----T----T---T-C----C-C-----CG--C--GC---C--G---CG-T---T--G--GC--G-C-CG-A----
> str31: --G----T-G-A-C---AA---A----A-A--CA-T-A--A--T-G----G---A-C----TC-C--A-A--C-A--C-C-A-T--G-TCA---AG-CT--T-TC-A---G---GTAG--A--C---------
> str32: --G----T-GTAA-G--AA---A--C-A--GT-A---AG---C---C--CG-G-A--AG--T---G-----G-T-G--T----T----T--TGC-GA-T--T-TCGA---G---G---C----C--G--G---
> str33: --GA--G-A--A---T----G-A-G-T-C--TCA-T---TA-C---C---G--C--C-----C--G-----G-TA--CT----TA-G--CA---AG-CT---A---AT----A-GT--C-A--C--G--GC--
> str34: ATG----T-G----GTC---G-ATGC--CA-T--G---G-AG---GC--C---CA-C-----CA-GT---T-C-A---T----TA--A----G--G-CTC----C--T--G---G---C-A-T----T-----
> str35: A---C-G-AG---CGT---T---T--TA-AG---G---G---C---C--CG--C----GA--C---T----GC--GAC--G-G--C---CA--CA---T-G----G--CC---C-T-G-TA-T---GT-----
> str36: --G---GT--T----T-A-T--A--C--C--T---TC-----C---C-A-G-G--T-A-A--CA---A-A--C----C---A--AC---CA---A--CT--T-TCGATC--T-C-T---T-GT-A-G------
> str37: -TG---G--G-AA-GT---T-C---C-A-A---A---AG-A--T--C-AC----A--A-A---AC--AC-T---A--C-C-AGT-C-A--A--C---CT-G-A---A---GTAC--A-C--------------
> str38: --GA----AG---CGT---T--A----AC-GT--GT---T-G--AG----G---A--A-A---A-G-ACA-GCT----T--AG---GA----G-A-AC----A---A---G-A-G---CT-G----G--G---
> str39: A---CC--AG---CG-CA---C-T--T-C-G---G-CAG---C--G----G--CA---G---CAC---C-T-C--G----G----C-A----GCA--C-C-T--C-A---G--C--AGC-A---AC-------
> str40: ATG---G--G-A-C---AA--C-T--TA---T---TC-----CTA--T-C----AT--G--T---G--C---C-A-A---GAG---G-T--T------T--TA-C---CCG---GT-G--A--C-C--A----
> str41: -T-----T-GTA--G--A-T-C-TG-T----TC--TC--TA---A---ACG---A--A----C---T---T--TA-A----A--A---TC-TG-----T-GT---G----GT---T-G-T---CAC-T--C--
> str42: A--ACC--A--A-C--CAA--C-T--T----TC-G--A-T--CT--CT---TG--T-AGA-TC---T----G-T----TC---T-C--T-A---A-AC--G-A---A-C--T---T---TA------------
> str43: --G---G--GT----TC--TGC---C-A--G---G-CA-TAG-T--CT---T---T-----T----T---T--T---CT-G-G--CG-----GC---C-C-T-T-G-T--GTA---A---A--C-C-T-G---
> str44: --G---G------C-T----GCATGCT----T-AGT--G---C-A-CT-C----A-C-G---CA-GTA--T---A-A-T----TA--AT-A---A--CT---A---AT---TAC-T-G-T-------------
> str45: -TG-C---A-T---G-C--T---T---A--GT--G-CA----CT--C-ACG--CA---G--T-A--TA-AT--TA-A-T--A--AC--T-A---A---T--TA-C--T--GT-CGT-----------------
> str46: -T-----T-----C--CA---CA----AC--T---T---T--C---C-AC---CA--AG---C---T-C-TGC-A-A---GA-T-C---C---CAGA---GT--C-A---G---G--G---G-C-C-T-G-T-
> str47: -T--C--TA--AACG--AA--C-T--T----T-A---A--A---A--T-C-TG--T--G--T---G-----GCT-G--TC-A---C--TC--G--G-CT-G---C-AT--G--C-T---TAG-----------
> str48: A---CCG--G-A---T----G---GC--C-G-C-G--A-T---T---T---T---TC-G-G--A-GT-C---CT----T-G-G---G-----G--GAC-C--A-C--TC---A-G-A---A-T-A-G-A----
> str49: ----C--T--T---GT-A--G-AT-CT---GT---TC--T--CTA---A-----A-C-GA---AC-T---T--TA-A----A--A---TC-TG-----T-GT---G----G--C-T-G-T---CAC-T-----
> str50: ATGA--G------C---A---C-T---A-AG-C-G--A--AG--A---AC---CA--A-A---A---A---GC-AGAC---A--A---T-A--CA-AC-C----CG--C--TA--T---TA--C---------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 84
> ```

In [ ]:
```python
instance_08 = util.parse("protein_n010k010.txt")
model_08 = Model(instance_08)
solution_08 = model_08.solve().to_solution()
```

In [ ]:
```python
_instance = instance_08
_model = model_08
_solution = solution_08

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 19 chars) ---
> str01: MALSYCPKGT
> str02: MQSSLNAIPV
> str03: MPLSYQHFRK
> str04: MEEHVNELHD
> str05: MSNFDAIRAL
> str06: MFRNQNSRNG
> str07: MFYAHAFGGY
> str08: MSKFTRRPYQ
> str09: MSFVAGVTAQ
> str10: MESLVPGFNE
> 
> --- Solution (of length 44) ---
>   Sol: MAPLEQSKFYTSRLNEQAHFDVAINCSFRPGVFNEKGTALHDYQ
> str01: MA-L--S--Y---------------C---P-----KGT------
> str02: M----QS----S-LN--A-----I-----P-V------------
> str03: M-PL--S--Y------Q-HF--------R------K--------
> str04: M---E----------E--H--V--N---------E----LHD--
> str05: M-----S-------N----FD-AI----R---------AL----
> str06: M-------F---R-N-Q-------N-S-R----N--G-------
> str07: M-------FY-------AH---A----F--G-----G-----Y-
> str08: M-----SKF-T-R---------------RP------------YQ
> str09: M-----S-F------------VA-------GV-----TA----Q
> str10: M---E-S------L-------V-------PG-FNE---------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 29
> ```

In [ ]:
```python
instance_09 = util.parse("protein_n050k050.txt")
model_09 = Model(instance_09)
solution_09 = model_09.solve().to_solution()
```

In [ ]:
```python
_instance = instance_09
_model = model_09
_solution = solution_09

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 20 chars) ---
> str01: MRHLNIDIETYSSNDIKNGVYKYADAEDFEILLFAYSIDGGEVECLDLTR
> str02: MERRAHRTHQNWDATKPRERRKQTQHRLTHPDDSIYPRIEKAEGRKEDHG
> str03: MEPGAFSTALFDALCDDILHRRLESQLRFGGVQIPPEVSDPRVYAGYALL
> str04: MGKFYYSNRRLAVFAQAQSRHLGGSYEQWLACVSGDSAFRAEVKARVQKD
> str05: FFRENLAFQQGKAREFPSEEARANSPTSRELWVRRGGNPLSEAGAERRGT
> str06: MDPSLTQVWAVEGSVLSAAVDTAETNDTEPDEGLSAENEGETRIIRITGS
> str07: MAFDFSVTGNTKLDTSGFTQGVSSMTVAAGTLIADLVKTASSQLTNLAQS
> str08: MAVILPSTYTDGTAACTNGSPDVVGTGTMWVNTILPGDFFWTPSGESVRV
> str09: MNTGIIDLFDNHVDSIPTILPHQLATLDYLVRTIIDENRSVLLFHIMGSG
> str10: MFVFLVLLPLVSSQCVNLRTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS
> str11: MDSKETILIEIIPKIKSYLLDTNISPKSYNDFISRNKNIFVINLYNVSTI
> str12: MLLSGKKKMLLDNYETAAARGRGGDERRRGWAFDRPAIVTKRDKSDRMAH
> str13: MNGEEDDNEQAAAEQQTKKAKREKPKQARKVTSEAWEHFDATDDGAECKH
> str14: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEVLSEARQHLKDGT
> str15: MRYIVSPQLVLQVGKGQEVERALYLTPYDYIDEKSPIYYFLRSHLNIQRP
> str16: MPRVPVYDSPQVSPNTVPQARLATPSFATPTFRGADAPAFQDTANQQARQ
> str17: MFVFLVLLPLVSSQCVNLRTRTQLPLAYTNSFTRGVYYPDKVFRSSVLHS
> str18: MFVFFVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS
> str19: MEAIISFAGIGINYKKLQSKLQHDFGRVLKALTVTARALPGQPKHIAIRQ
> str20: MASSGPERAEHQIILPESHLSSPLVKHKLLYYWKLTGLPLPDECDFDHLI
> str21: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEVLSEVRQHLKDGT
> str22: MLAPSPNSKIQLFNNINIDINYEHTLYFASVSAQNSFFAQWVVYSADKAI
> str23: MSAITETKPTIELPALAEGFQRYNKTPGFTCVLDRYDHGVINDSKIVLYN
> str24: MKNIAEFKKAPELAEKLLEVFSNLKGNSRSLDPMRAGKHDVVVIESTKKL
> str25: MPQPLKQSLDQSKWLREAEKHLRALESLVDSNLEEEKLKPQLSMGEDVQS
> str26: MFVFLVLLPLVSSQCVNLITRTQSYTNSFTRGVYYPDKVFRSSVLHSTQD
> str27: MKFDVLSLFAPWAKVDEQEYDQQLNNNLESITAPKFDDGATEIESERGDI
> str28: MFVFLVLLPLVSSQCVNFTNRTQLPSAYTNSFTRGVYYPDKVFRSSVLHS
> str29: MWSIIVLKLISIQPLLLVTSLPLYNPNMDSCCLISRITPELAGKLTWIFI
> str30: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEFLSEARQHLKDGT
> str31: MFVFLVLLPLVSSQCVMPLFNLITTTQSYTNFTRGVYYPDKVFRSSVLHL
> str32: MHQITVVSGPTEVSTCFGSLHPFQSLKPVMANALGVLEGKMFCSIGGRSL
> str33: MATLLRSLALFKRNKDKPPITSGSGGAIRGIKHIIIVPIPGDSSITTRSR
> str34: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSMEEVLSEARQHLKDGT
> str35: MFVFLVLLPLVSSQCVNLTTGTQLPPAYTNSFTRGVYYPDKVFRSSVLHS
> str36: MANIINLWNGIVPMVQDVNVASITAFKSMIDETWDKKIEANTCISRKHRN
> str37: MLNRIQTLMKTANNYETIEILRNYLRLYIILARNEEGRGILIYDDNIDSV
> str38: MADPAGTNGEEGTGCNGWFYVEAVVEKKTGDAISDDENENDSDTGEDLVD
> str39: MFVFLVLLPLVSSQCVNLRTRTQLPPSYTNSFTRGVYYPDKVFRSSVLHS
> str40: MESLVPGFNEKTHVQLSLPVLQVCDVLVRGFGDSVEEVLSEARQHLKDGT
> str41: MNNQRKKTARPSFNMLKRARNRVSTVSQLAKRFSKGLLSGQGPMKLVMAF
> str42: MSNFDAIRALVDTDAYKLGHIHMYPEGTEYVLSNFTDRGSRIEGVTHTVH
> str43: MIELRHEVQGDLVTINVVETPEDLDGFRDFIRAHLICLAVDTETTGLDIY
> str44: MFVFLVLLPLVSSQCVMPLFNLITTNQSYTNSFTRGVYYPDKVFRSSVLH
> str45: MSKDLVARQALMTARMKADFVFFLFVLWKALSLPVPTRCQIDMAKKLSAG
> str46: MASLLKSLTLFKRTRDQPPLASGSGGAIRGIKHVIIVLIPGDSSIVTRSR
> str47: MRVRGILRNWQQWWIWTSLGFWMFMICSVVGNLWVTVYYGVPVWKEAKTT
> str48: MAVEPFPRRPITRPHASIEVDTSGIGGSAGSSEKVFCLIGQAEGGEPNTV
> str49: MFYAHAFGGYDENLHAFPGISSTVANDVRKYSVVSVYNKKYNIVKNKYMW
> str50: MANYSKPFLLDIVFNKDIKCINDSCSHSDCRYQSNSYVELRRNQALNKNL
> 
> --- Solution (of length 499) ---
>   Sol: MEINWAGRFDSVNPKELVFLDVNRIQAVHGQYIPESTNLDVFAGPHADEIKVEPFGLRYSNEKITKWMQDAESLRAAEPIFQHVLDGTKSCIFYNARTLDPQGANEWVKSAILQDATCMFVHAIKTVNYELWDSGARCLPIFQMCANTLHSVKAWNAMFQSRIDAPTRVNEGILQSKPCRAHLQTEGPFADINGYVSTEKRFFDWLHRTGVALSDKQYHIRCHEKTGLMNPQALYAISFGDVTNHKMEFQGARISHPGTEDYLPKCNMGPVQYAASTVAGDYFNRILWNHDSKAEPRFLCGSIAVTYDLWNACGMKLAYVSFGPINDRQGAEHLWSDTIKRNVYSEMFCTRIEGPLAIRANPTVYKDEIGYLPVDNHREAFKGIFPVHTACRLSKDFRAIEQAPSYMRGNWDTIVDACFHLQVREWCPQLSDGIMKYAVIEGFSYHLAKITNAGDEPDRHKVWLIGTMVSGCADNTYQHRGKMSILFYNVDRGHIPQWT
> str01: M------R--------------------H---------L---------------------N--I-----D---------I-------------------------E----------T-----------Y----S----------------S----N-------D--------I---K---------------NG-V---------------------Y------K---------YA----D----------A-------ED---------------------F-----------E-------I-----L-------L----F--------A------------YS------I--------------D--G------------G-----------------E-------------V---------E-C--L-D--------------L---T-------R----------------------------------------
> str02: ME-----R---------------R--A-H----------------------------R------T-----------------H------------------Q--N-W-------DAT-------K--------------P---------------------R--------E--------R--------------------R--------------KQ--------T-----Q------------H-------R---------L-------------T------------H-----P-----------D------------------D--------S--I----Y----------P---R---------I---------E--K-------A----------E-------G--------------R-----------K----E-------------D----H-----G---------------------------------
> str03: ME-----------P---------------G------------A-----------F----S----T-----A--L------F----D---------A--L------------------C--------------D------------------------------D--------IL-------H------------------R------R----L----------E-------------S-----------Q------------L---------------------R------------F--G------------G-----V--------Q---------I---------------P------P-----E-----V-------------------S-D-------P---R------V---------------------YA---G--Y--A---------------L---------------------L-------------
> str04: M-----G-------K---F------------Y--------------------------YSN-------------R---------------------R-L----A---V-----------F--A-------------------Q--A-------------QSR-------------------HL---G------G--S--------------------Y-----E-------Q-------------------------------------------------------W----------L----A--------C------VS-G---D--------S--------------------A-----------------------F----------R------A-E-------------V--------------------K-A--------------------R--V---------------Q---K--------D--------
> str05: --------F---------F----R----------E--NL---A-----------F-------------Q------------Q----G-K------AR--------E-------------F-------------------P----------S-------------------E--------------E---A----------R----------A-----------------N-------S------------------P-T----------------S--------R---------E---L----------W---------V-------R------------R------------G---------------G-----N---------P------LS------E-A-----G-------A-------E---------------------------------R--------------------RG-----------------T
> str06: M--------D---P---------------------S--L-------------------------T---Q--------------V----------------------W---A---------V--------E----G---------------SV---------------------L-S----A--------A-----V-------D----T--A-----------E-T---N----------D-T----E--------P---D---------------------------------E-----G-------L-----------S---------AE---------N---E-------G-------------E--------------------T--R-------I-------------I---------R---------I----------------T--G---------------S-----------------------------
> str07: M----A--FD--------F----------------S----V-----------------------T---------------------G-------N--T----------K---L-D-T----------------SG------F-----T-----------Q-----------G-----------------------VS----------------S--------------M-------------T---------------------------V--AA----G-------------------------T--L---------------I-----A-----D------------------L-------V-K----------------------TA---S----------S----------------Q-------L--------------------TN-----------L--------A----Q-----S---------------
> str08: M----A-----V------------I-------------L-----P--------------S----T----------------------------Y---T-D--G-------------T-----A------------A-C---------T-------N---------------G---S-P------------D----V--------------V---------------G---------------T-------G-------T--------M-------------------W----------------V-----N--------------------------TI----------------L-----P-------G----D-----F---F-------------------------W-T--------------P--S-G-------E--S-----------------V-----------------R---------V---------
> str09: M--N--------------------------------T------G-----I-------------I-----D---L------F----D--------N--------------------------H----V-----DS------I------------------------PT-----IL---P---H-Q---------------------L-----A-------------T-L------------D--------------------YL-------V-------------R--------------------T------------------I-------------I---------------------------DE-------N-R---------------S--------------------V-----L--------L------------F--H---I-----------------M--G------------S--------G------
> str10: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V---N-----------------L-----R----T---------------R-------T-------Q----------L--P-------------------------P----------------A-------Y-----------------------T----N---------SF---------------T--R------------G---------VY-----Y-P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----------------------------
> str11: M--------DS---KE--------------------T------------I------L------I-------E-------I-----------I--------P-------K--I------------K--------S------------------------------------------------------------Y----------L------L-D----------T---N------IS------------------P-------K----------S-----Y-N------D------F----I-----------------S------R-------------N-----------------------K---------N-------IF-V------------I---------N----------L---------------Y--------------N---------V-------S-----T--------I--------------
> str12: M---------------L--L---------------S-------G------K-----------K--K-M-----L----------LD--------N---------------------------------YE-----------------T-----A--A-------A--R---G-------R------G------G---------D-------------------E----------------------------R-------------------------------R-----------R---G--------W-A---------F----DR--------------------------P-AI-----V------------------------T-----K--R-------------D-----------------------K-------S----------D---R--------M----A-----H--------------------
> str13: M--N--G--------E------------------E----D-------D------------NE------Q-A----AAE---Q-------------------Q--------------T-------K---------------------------KA----------------------K--R-----E-------------K------------------------------P--------------K---Q-AR-----------K-----V-----T--------------S--E--------A-----W---------------------EH--------------F------------------D------------A--------T------D---------------D--------------------G----A--E------------------------------C---------K-----------H-----
> str14: ME--------S-----LV---------------P---------G----------F-----NEK-T-----------------HV-----------------Q----------L--------------------S----LP-----------V---------------------LQ--------------------V----R--D------V-L----------------------------V----------R----G------------------------F-----------------G------D------------S---------------------V--E------E----------V-------L---------------------S------E-A----R-------------Q-----------------------HL-K-----D----------GT--------------------------------
> str15: M------R-----------------------YI-------V------------------S------------------P--Q--L----------------------V----LQ------V-------------G-----------------K------------------G--Q----------E---------V--E-R----------AL----Y---------L--------------T-------------P----Y------------------DY---I----D---E--------------------K----S--PI------------------Y--------------------Y---------------F-----------L----R------S--------------HL------------------------------N------------I------------Q-R---------------P---
> str16: M------------P---------R---V-----P------V-----------------Y----------D--S-----P--Q-V-----S----------P---N-----------T---V------------------P--Q--A---------------R-----------L------A---T--P--------S----F---------A-------------T----P-----------T-----F---R----G---------------A------D------------A-P-------A-----------------F------Q-------DT------------------A---N----------------------------------------Q-------------------Q---------------A--------------------R------------------Q---------------------
> str17: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V---N-----------------L-----R----T---------------R-------T-------Q----------L--P--L-A-------------------------Y--------------T------N-------S-----F-------T---------------------R-G------------VY--------------------Y-------P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----------------------------
> str18: M-------F--V------F----------------------F---------V----L----------------L----P-----L----------------------V-S-----------------------S--------Q-C------V---N-----------------L----------T------------T--R-------T-------Q----------L--P-------------------------P----------------A-------Y-----------------------T----N---------SF---------------T--R------------G---------VY-----Y-P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----------------------------
> str19: ME---A------------------I-------I--S-----FAG-----I-----G-------I------------------------------N---------------------------------Y-----------------------K-----------------------K-----LQ------------S--K-----L----------Q-H---------------------D-------F-G-R-----------------V---------------L-----KA----L------T-------------V-----------------T------------------A-RA-----------LP---------G------------------Q-P-------------------------------K---------H---I--A-----------I--------------R----------------Q--
> str20: M----A----S------------------------S-------GP---E--------R------------AE----------H------------------Q---------I-----------I------L--------P------------------------------E----S-----HL-------------S----------------S----------------P--L-------V---K---------H--------K---------------------L-----------L-------Y-----------Y---------------W----K---------------L------T------G-LP-------------------L----------P-------D------------E-C----D----------F-----------D----H---LI----------------------------------
> str21: ME--------S-----LV---------------P---------G----------F-----NEK-T-----------------HV-----------------Q----------L--------------------S----LP-----------V---------------------LQ--------------------V----R--D------V-L----------------------------V----------R----G------------------------F-----------------G------D------------S---------------------V--E------E----------V-------L---------------------S------E-------------V--------R----Q----------------HL-K-----D----------GT--------------------------------
> str22: M---------------L---------A------P-S--------P---------------N-----------S---------------K--I---------Q----------L------F-------N------------------N---------------I------N--I-----------------DIN-Y---E-------H-T---L----Y--------------------F------------A--S---------------V----S--A-------------------------------------------------Q------------N--S--F--------------------------------F--------A-----------Q--------W---V-------V-------------Y------S---A------D-----K-----------A-----------I--------------
> str23: M---------S---------------A-----I---T-----------E---------------TK------------P--------T---I-------------E------L--------------------------P-----A--L----A----------------EG----------------F---------------------------Q---R-------------Y--------N-K------------T----P----G-------------F----------------------T------C------V-------------L--D---R--Y----------------------D---------H-----G---V------------I---------N-D------------------S----K---I---------------------V-L------------Y-----------N----------
> str24: M-------------K-------N-I-A-------E------F--------K-----------K-------A-------P--------------------------E------L--A-------------E----------------------K--------------------L--------L--E---------V-----F-----------S---------------N---L-----------K----G---------------N--------S--------R------S------L--------D---------------P----------------------M---R-----A------------G-----------K-----H-------D------------------V-------V---------------VIE--S------T---------K--------------------K---L-------------
> str25: M------------P-----------Q-------P----L-----------K-----------------Q---SL-----------D---------------Q-------S--------------K------W------L----------------------R--------E---------A----E-------------K------H-----L-------R-----------AL-------------E------S-------L-------V---------D----------S------------------N-----L--------------E-------------E------E------------K-----L---------K---P---------------Q------------------L---------S---M------G-------------E-D---V---------------Q-----S---------------
> str26: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V---N-----------------L-----------------I-----T--R-------T-------Q--------------------S-----------------------Y--------------T------N-------S-----F-------T---------------------R-G------------VY--------------------Y-------P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----T-Q------------D--------
> str27: M-------------K---F-DV----------------L--------------------S-------------L------F--------------A----P-----W---A-------------K-V-----D-------------------------------------E---Q----------E--------Y--------D------------Q--------------Q-L---------N----------------------N----------------N--L-------E------SI--T-----A-----------P---------------K-------F------------------D-------D-------G------A----------------------T-----------E--------I------E--S-----------E--R------G-------D----------I--------------
> str28: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V---N--F-------T--N---------R----T-------------------------------Q----------L--P------S-------------A---------Y--------------T------N-------S-----F-------T---------------------R-G------------VY--------------------Y-------P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----------------------------
> str29: M---W-----S-------------I-------I-------V---------------L-----K----------L-----I---------S-I---------Q-------------------------------------P--------L------------------------L--------L------------V-T---------------S-------------L--P--LY--------N------------P---------NM------------D----------S-------C------------C---L-------I----------S----R----------I----------T---------P-----E-------------L-----A---------G--------------------------K----------L---T-----------W-I---------------------F-------I----
> str30: ME--------S-----LV---------------P---------G----------F-----NEK-T-----------------HV-----------------Q----------L--------------------S----LP-----------V---------------------LQ--------------------V----R--D------V-L----------------------------V----------R----G------------------------F-----------------G------D------------S---------------------V--E------E---------------------------F-----------LS------E-A----R-------------Q-----------------------HL-K-----D----------GT--------------------------------
> str31: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V-----M-------P-------L--------------F---N------------L-------------I-----T----------------T---------------T------------Q---S-----Y-----------------------T----N----------F---------------T--R------------G---------VY-----Y-P-D------K----V---------FR------S-------------------------S-------V-------L------------H---L-----------------------------------
> str32: M---------------------------H-Q-I---T---V----------V-------S--------------------------G-------------P---------------T------------E---------------------V--------S-----T-----------C---------F----G--S--------LH-----------------------P-------F----------Q----S-------L-K----PV-------------------------------------------M--A-------N----A--L-------------------G---------V-------L------E---G-----------K-----------M-----------F-------C---S--I-------G-----------G----R----------S---------------L-------------
> str33: M----A------------------------------T-L-----------------LR-S-------------L-A--------L-------F---------------K---------------------------R---------N-----K----------D------------KP---------P---I-----T---------------S------------G----------S-G----------GA-I------------------------------R---------------G-I------------K----------------H-----I------------I-----I-----V--------P----------I-P----------------------G--D------------------S------------S-----IT---------------T------------R---S-------R-------
> str34: ME--------S-----LV---------------P---------G----------F-----NEK-T-----------------HV-----------------Q----------L--------------------S----LP-----------V---------------------LQ--------------------V----R--D------V-L----------------------------V----------R----G------------------------F-----------------G------D------------S-------------------------M-----E--------------E-----V------------------LS------E-A----R-------------Q-----------------------HL-K-----D----------GT--------------------------------
> str35: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V---N-----------------L----------T------------T-----------G---------------T-----Q-L----------------------P------P---------A-------Y-----------------------T----N---------SF---------------T--R------------G---------VY-----Y-P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----------------------------
> str36: M----A------N-----------I-------I----NL---------------------------W---------------------------N-------G--------I--------V------------------P---M-------V-------Q---D----VN-------------------------V---------------A-S-----I-----T------A-----F------K--------S------------M-----------------I----D---E----------T---W----------------D------------K-------------------------K--I---------EA-----------------------------N--T----C---------------I---------S--------------R-K-----------------HR--------N----------
> str37: M---------------L-----NRIQ----------T-L----------------------------M--------------------K--------T-----AN----------------------NYE-----------------T--------------I-------E-IL-----R------------N-Y----------L-R----L----Y-I----------------I-------------------------L----------A----------R---N-----E------------------------------------E---------------------G----R----------G-------------I--------L------I-----Y-----D---D-----------------------------------N------------I--------D---------S-----V---------
> str38: M----A---D---P------------A--G------TN-----G----E---E--G--------T---------------------G---C---N-------G---W------------F--------Y----------------------V------------------E---------A--------------V--------------V------------EK--------------------K------------T---------G-----------D------------A--------I-----------------S-----D---------D--------E--------------N------E-------N-------------------D--------S------DT-------------------G-------E-------------D--------L----V----D-------------------------
> str39: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V---N-----------------L-----R----T---------------R-------T-------Q----------L--P-------------------------P------------------S-----Y-----------------------T----N---------SF---------------T--R------------G---------VY-----Y-P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------S-----------------------------
> str40: ME--------S-----LV---------------P---------G----------F-----NEK-T-----------------HV-----------------Q----------L--------------------S----LP-----------V---------------------LQ--------------------V-------------------------C------------------DV--------------------L-------V-------------R---------------G--------------------FG---D--------S------V--E------E----------V-------L---------------------S------E-A----R-------------Q-----------------------HL-K-----D----------GT--------------------------------
> str41: M--N--------N------------Q-------------------------------R----K--K---------------------T-------AR---P--------S---------F-------N---------------M----L---K--------R--A--R-N---------R---------------VST------------V--S--Q----------L----A------------K------R-----------------------------F--------SK-------G-------L-------L---S-G-----QG------------------------P---------------------------------------------------M----------------------------K----------L--------------V-----M----A-------------F------------
> str42: M---------S-N-----F-D-----A-----I------------------------R------------A--L---------V-D-T-----------D---A------------------------Y-----------------------K--------------------L------------G-------------------H------------I--H-----M-----Y---------------------P--E--------G-------T-----------------E-----------Y------------V-------------L-S-----N-----F-T----------------D----------R----G----------S---R-IE-------G-----V-----------------------------------T--------H------T-V---------H--------------------
> str43: M-I------------EL------R----H-----E-----V---------------------------Q-----------------G------------D------------L-------V----T--------------I-----N----V----------------V-E-------------T--P----------E----D-L--------D-----------G-----------F-------------R-------D---------------------F--I----------R------A----------------------------HL----I---------C------LA------V--D---------------------T-----------E-----------T-------------------------------------T--G---------L---------D----------I--Y-----------
> str44: M-------F--V------FL-V----------------L-----------------L---------------------P-----L----------------------V-S-----------------------S--------Q-C------V-----M-------P-------L--------------F---N------------L-------------I-----T----------------TN-----Q----S------Y--------------T------N-------S-----F-------T---------------------R-G------------VY--------------------Y-------P-D------K----V---------FR------S-------------------------S-------V-------L------------H---------------------------------------
> str45: M---------S---K-----D-----------------L-V-A--------------R----------Q-A--L--------------------------------------------M------T---------AR------M--------KA---------D------------------------F------V-----FF--L--------------------------------F--V--------------------L------------------------W----KA----L--S------L--------------P------------------V-----------P-------T--------------R------------C----------Q-----------I-D------------------M--A----------K-----------K--L-----S--A-------G------------------
> str46: M----A----S-----L--L------------------------------K--------S-------------L-------------T----------L--------------------F----K-----------R----------T-------------R-D----------Q--P---------P-----------------L-----A-S------------G----------S-G----------GA-I------------------------------R---------------G-I------------K----------------H---------V--------I-----I-----V-------L-----------I-P----------------------G--D------------------S------------S-----I-----------V----T------------R---S-------R-------
> str47: M------R---V-----------R-----G--I-----L------------------R--N-----W-Q------------Q------------------------W------------------------W--------I-------------W-----------T--------S------L---G-F---------------W-----------------------M---------F-------M------I-----------C---------S-V--------------------------V--------G-----------N-------LW-------V------T-------------VY-----Y-----------G---V----------------P----------V----------W---------K----E------AK-T---------------T--------------------------------
> str48: M----A-----V---E-----------------P-------F--P------------R----------------R---PI-------T--------R---P--------------------HA----------S------I-----------------------------E------------------------V-------D----T----S------------G---------I--G----------G---S------------------A-----G-----------S---------S-----------------------------E-------K--V----FC------L-I-----------G-------------------------------QA---------------------E-------G--------G-------------EP-----------------NT-------------V---------
> str49: M-------F----------------------Y----------A--HA-------FG------------------------------G------Y-----D-----E---------------------N--L------------------H---A----F------P-----GI--S--------------------ST------------VA-----------------N----------DV----------R-----------K-------Y--S-V--------------------------V---------------S---------------------VY----------------N----K---------------K-----------------------Y---N---IV--------------------K---------------N--------K---------------Y-----M--------------W-
> str50: M----A------N------------------Y---S--------------K--PF-L----------------L-----------D-----I---------------V-----------F-------N------------------------K----------D--------I---K-C------------IN----------D---------S-------C---------------S------H---------S-----D----C------------------R---------------------Y---------------------Q------S-----N--S-------------------Y--------V----E-------------L----R---------R-N-----------Q---------------A--------L----N--------K-------------N----------L-------------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 93
> ```
