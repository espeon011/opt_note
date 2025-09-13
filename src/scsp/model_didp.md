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
        disable_default_bound: bool = False, 
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
        if not disable_default_bound:
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
>  Sol: ultkcignyckuhojsimoqfevoazpplngbrddxxbcsvrvnnhstuqgpxzvxissbxf
> str1: --tk--gn--kuh----m--------p--------x-------n-h-t-qg-xzvxis----
> str2: -----i-------oj-i--qf--o----ln-b---xx-c-v-----s-uq-p--v-issbxf
> str3: ul--ci-nyc---o-s--o---vo-zppl----------------------p----------
> str4: -----ig--------------ev-az----gbrdd--bcsvrvnn-----g----------f
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
>  Sol: iojiqfotkpbyplrgdenbxvawczxqgkbrufdrlchpmqvjgtdpfuivxnerzbycsodhutmsbopvroqgxzpvxinnsbsgwpdblhxfpe
> str1: -------tk------g--n----------k--u-----h-m------p----xn---------h-t--------qgxz-vxi--s-------------
> str2: iojiqfo------l----nbx-----x----------c----v-----------------s---u---------q---pv-i--s-s----b--xf--
> str3: --------------------------------u---lc------------i--n----yc-o-----s-o-v-o---zp----------p--l---p-
> str4: i--------------g-e---va--z--g-br--d-----------d----------b-cs----------vr------v--nn---g-------f--
> str5: ---------p-yplr----------zx-----u----c-pmqv-gtd-fuiv-------c--d----sbo----------------------------
> str6: ---------pb-----de---v------------d--c----v---dpf-------z---s-----msb---roq----v-----b-----b-h----
> str7: -----------------enb----cz-------f---------j-t-----vx-erzb--------------r------v-i-----g-p--l----e
> str8: --------------r-----x--w--xq-k-r--drlc-------t---------------od--tm---p-r-----p-x-------w-d-------
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
>   Sol: pyplrsxiutkoqjageiwnsbdzxqkefovudlchqnpazfgzbvxrdijmtqpvxerenlfygxqcvujzsheitodwauqbvmnctfeusompgvkbkzrhdivskjozxiqzupcgnwvdsrbbxhpaknwldizmgfoecsyp
> str01: ---------tk----g---n------k----u---h---------------m--p-x---n------------h--t-----q-------------g---------------x--z------v-----x--------i-------s--
> str02: -------i---o-j---i-------q--fo---l---n------b-x---------x----------cv---s--------uq------------p-v-------i-s----------------s-b-x------------f------
> str03: --------u------------------------lc--------------i----------n--y---c---------o--------------so---v------------oz-----p------------p----l-----------p
> str04: -------i-------ge-------------v--------az-g-b--rd-----------------------------d----b---c----s----v----r---v-------------n------------n------gf------
> str05: pyplr------------------zx------u--c---p------------m-q-v--------g-----------t-d----------f-u-------------iv-----------c----ds-b---------------o-----
> str06: p--------------------bd----e--v-d-c----------v--d-----p-------f--------zs------------m------s------b--r-------o---q-------v---bb-h------------------
> str07: ----------------e--n-b------------c-----zf--------j-t--vxer------------z-----------b------------------r---v------i-----g----------p----l-------e----
> str08: ----r-x-----------w-----xqk--------------------rd---------r--l-----c--------tod---------t-----mp------r--------------p----------x-----w-d-----------
> str09: ----------k---------------k---------q--a-f-------i--------------g-q---j--------w-------------o----k-k------sk----------------rb--------l----g-------
> str10: ---l--x-----------------x-------------pa----b----i-----v---------------------------bv----------------z------k-oz---z------vd------------------------
> str11: ----------k------------------------------------r-i------------f---------s-------a---v-nc----------------d---------q------w-------h--------z-----c---
> str12: ------------q-a---------x------ud---------g----------q-v----------qc------e----w---b-----f------g--------i---jo----------w------------w-----------y-
> str13: ----rsx-----qj-----n--------f---------pa--------di-------------------u--s--i------qb------e----------z-h----k-o------------------h---------mg-------
> str14: -------i----------w-s--------------h---------v---------------------------h-------------c-----om----------i----------u-----vd------------d--m--------
> str15: -----------------------------------h----------------t---x--------xq---jz----------qb---ct----------b-------------------------------akn--------------
> str16: ------x-u-----------s-------f-----c------f-z----------p--e-e-------cv----------wa-----n-tf----m-g-----------------qzu-------------------------------
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
>   Sol: bbaeddcbeacdeecbdbeacbdcead
> str01: ----d-cb--c---c-db--c--ce--
> str02: b---dd-be---ee----e--bd----
> str03: ------c--acdeec---e--b--e--
> str04: --aedd-----d----d-e--bd---d
> str05: --a---cbe---e-c----a-b-ce--
> str06: bba----be------bd---cb---a-
> str07: bbae-----a--e--b---a--d--a-
> str08: ---e----e---eecbdbe-----e--
> str09: ------c---cdee--d--a--dc--d
> str10: b---d----a-----bdbea-----ad
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
>   Sol: dcaebdaecbdeabcedacbedabceabdacebd
> str01: dc--b---c-----c-d--b----c-----ce--
> str02: ----bd----d--b-e----e----e-----ebd
> str03: -ca-----c-de---e--c-e--b-e--------
> str04: --ae-d----d-----d----d---e-bd----d
> str05: --a-----cb-e---e--c---abce--------
> str06: ----b----b--ab-e---b-d--c--b-a----
> str07: ----b----b--a--e-a--e--b--a-da----
> str08: ---e---e---e---e--cb-d-b-e-----e--
> str09: -c------c-de---eda---d--c---d-----
> str10: ----bda--bd--b-e-a----a-----d-----
> str11: ---e-d-e--d-a----a----a--ea--a----
> str12: --a---ae----a----a-be----ea---c---
> str13: ---e--a-----abc--ac-----c---d---b-
> str14: ----bd-e---ea---d---e-a-----d--e--
> str15: -cae-da---de---e----ed------------
> str16: ---eb---c---a---d--b--ab---b---e--
> str17: d----d--c--e---e-a-b-d---ea-------
> str18: d-a-b---c-d-----d---e-a--e----c---
> str19: --a---a---d---ce----eda---ab------
> str20: --ae---ec-----ce----e----ea--a----
> str21: ----b----bd-a--e--c---a---a-d--e--
> str22: d-a-----c--e----da--edab----------
> str23: --a---ae----ab-----b---b---b--ce--
> str24: d--e-d---b----c----b----c-a--a--b-
> str25: d---bda-----a--e---b---bc--b------
> str26: d--eb--e--d--b-e---b--a-c---------
> str27: -c-e---e-b----c-d-cb-d---e--------
> str28: d---b--e--d-a----a---da---ab------
> str29: -c------c-----c-d-cbe--b----d-c---
> str30: --ae---e----a-c-d--b----c--bd-----
> str31: d-a-----cb-ea-c---c-----c---d-----
> str32: ---e----c--e-bc---c--d-b----d---b-
> str33: d----d---b---bceda-b---b----------
> str34: --a---ae----ab---a----a--e-b-a----
> str35: ---e----cb---bc--a----a-----d-c--d
> str36: d--eb---c-----ce--c--d-bc---------
> str37: d-a---a-cb--a--e----e--bc---------
> str38: --a--da--b-ea----ac-----ce--------
> str39: d-ae----c-d--b---ac---a---a-------
> str40: d-a-----cb---b--d-c-ed--c---------
> str41: d--e-d---b-e---e---b---b----d--e--
> str42: -c---da---d---c-d-c--da---a-------
> str43: -c-e---e--d---c----b--a--e-----e-d
> str44: -c-e--aec---a----a----a-c-a-------
> str45: dc------c-----ce---b---b---b-a---d
> str46: ----b-ae---ea--e---b---b----d--e--
> str47: d---bd-e-b--a-c---c--d-b----------
> str48: ---eb---cb-e---eda--e-a-----------
> str49: --ae---e---e-b-----b-d-bc-a-------
> str50: d---bda--b----ce--cb---b----------
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
>   Sol: TACTACGCGTAGATCAGATCGTAC
> str01: -A-T--G-G--GAT-A---CG---
> str02: -A-TAC-C-T---TC----C---C
> str03: --C-ACG---A-AT----T-G-A-
> str04: TA--A-----A-ATC---T-GT--
> str05: -A----G-GTA-A-CA-A----A-
> str06: T--T-C-C-TAG----G-T---A-
> str07: T--T--G--TAGATC---T-----
> str08: T-----G-G--GA--AG-T--T-C
> str09: T--T-C-C--A---CA-A-C-T--
> str10: T-CTA-----A-A-C-GA----A-
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
>   Sol: ATGCACGTAGTAACGTACTAGCATGTCAATCGTACGACTGATCAGCATGCTAGCGTAACGTACGTACTAGTCATCAGACTTGCAGCATGCTATGCAGACTGCTAGCATGCTACGTAAGCATGCTACGTCAGCR
> str01: -T--A-GTAGTA--G-ACT--C----C----G---GA---A---G--TG--A-C--AA---AC---C----C-T--GA-----A--A----A-G-A-A-TG---G-AT---A---AA---T---A--T-A---
> str02: --G---G-A-TAA---AC-A-C-T--C---C---CGA---A--A--AT---A----A---T---T--T-G--A-C----TT--A--A----A--CA-AC-GC--G-A--C-A-GT-----T-C-A----AG--
> str03: AT--AC-------C-T--T--C----C--T---A-G---G-T-A--A--C-A----AAC---C--A--A--C--CA-ACTT------T--T--G-A---T-CT--C-T--T--GTA-G-AT-CT--G------
> str04: -T--A---A--A---T--TA---T---AATC-T-----T-AT-A-C-T---AG--TAA---A---A--A---AT-AG----G--G--TG-TA---A--C--C--G-A----A---AA-C--G----GTC----
> str05: -T-----TA--AA---AC-AGC----C--T-GT--G---G----G--T--T-GC--A-C---C---C-A--C-TCA--C----AG---G----GC---C--C-A-C-TG----G---GC--GC-A----AG--
> str06: ATG-AC-T--T--C---C-A--ATG------G-A----T---C--C---C-A----A-C---C-T-C-A---A---G-CTT-C--CA--C----C---C--C-A--ATG----GT-----T--T-C---AGC-
> str07: A---AC--A--AAC---C-A--A---C---C--A--ACT--T-----T--T-G---A---T-C-T-CT--T-----G--T---AG-AT-CT--G-----T--T--C-T-CTA---AA-C--G--A----A-C-
> str08: ATG-A---A--AACG-A--A--A----A-T--TA----T--T-A---T-C-A----A--G---G-----GT-AT--G----G-A--A-G-T--G--GA-----AGC-TG--ACG-AA--AT------------
> str09: A--C---T-----CG-----GC-TG-CA-T-G--C---T--T-AG--TGC-A-C-T--C--ACG--C-AGT-AT-A-A-TT--A--AT---A---A--CT---A--AT--TA---------------------
> str10: -T-----T-GTA--G-A-T--C-TGT---TC-T-C---T-A--A--A--C--G---AAC-T---T--TA---A--A-A-T--C----TG-T--G-----TG---GC-TG-T-C--A--C-T-C----------
> str11: --GCA-G-AG---C--A-T----T-T---TC-TA--A-T-ATC--CA--C-A----AA---A--T----G--A--AG----GCA--AT---A---A---T--T-G--T---AC-TA--C-T-C----------
> str12: ATG-A-G------C---C-A--A-G--A-TC---CGAC-GA--AG-A-GC---C----C---C--A--AG------GA---G--G-A-G--A---AG---G--AG---G----G-A--C---C--C--C--C-
> str13: -T-C---T-----C--AC-AG--T-TCAA--G-A--AC----C--CA----A----A--GTAC---C----C--C---C---CA---T---A-GC---C--CT--C-T--TA---AAGC---C-AC-------
> str14: A-G---GT--T----TA-TA-C----C--T--T-C--CT-A---G---G-TA----A-C--A---A--A--C--CA-AC---CA--A--CT-T------T-C--G-AT-CT-C-T-----TG-TA--------
> str15: A-G---GT--T----TA-TA-C----C--T--T-C--C----CAG---G-TA----A-C--A---A--A--C--CA-AC---CA--A--CT-T------T-C--G-AT-CT-C-T-----TG-TA--------
> str16: -T--A---A--AAC--A--A-C-T--CAAT---AC-A---A-CA---T---A----A--G-A---A--A---ATCA-AC--GCA--A----A---A-AC----A-C-T-C-AC--AA--A-------------
> str17: ---C-CG------C---C---CAT-T---T-G---G---G--C-G---GCT--C-T--CG-A-G--C--G--AT-AG-CT--C-G--T-C---G-A-A-T-C---C---CT-CG-A--C---CT---------
> str18: AT--AC-------C-T--T--C----C---C--A-G---G-T-A--A--C-A----AAC---C--A--A--C--CA-ACTT------T-C---G-A---T-CT--C-T--T--GTA-G-AT-CT--G------
> str19: -T-C---T-----C--AC-AG--T-TCAA--G-A--AC----C----T-C-A----A--GT-C-T-C----C--C---C---CA---T---A-G--G-C--CT--C-T--T---T---CA-G-T-C---AG--
> str20: --G-A--T-----C-T-CT--C-T--CA--C---CGA---A-C--C-TG---GC----C---C---C--G------G----GCA--A----ATGC---C--CTA--AT-C--C--A-G-A-G----GT--G--
> str21: A-G-A-G------C--A--A---T--CA---GT--G-C--ATCAG-A----A----A---TA--TAC----C-T-A---TT--A---T---A--CA--CT--T----TGCTA---A-G-A----A--T-----
> str22: A---A--T--TAA---A--A-CAT--C--TC--A--A-T-A-CA--A--C-A---TAA-G-A---A--A---A--A--C----A--A--C---GCA-A-----A--A----AC--A--C-T-C-A--T-----
> str23: A---A---A----CG-A--A-C-T-T---T---A--A---A--A---T-CT-G--T---GT--G-----G-C-T--G--T--CA-C-T-C---G--G-CTGC-A---TGCT---TA-G--TGC----------
> str24: AT--A---A----C-TA--A---T-T-A--C-T--G--T---C-G--T--T-G---A-C--A-G-----G--A-CA--C--G-AG--T---A---A--CT-C--G--T-CTA--T---C-T--T-C-T--G--
> str25: ATG-A-GT-GT--C--AC--G-A----A-T--T-C-AC-G-T-A-CA----A---T---G-A---ACT-G------GA-T-G-----T--T---CA--C-G-T-G---G--A---A----T---A----A---
> str26: A--C-CGT-G----G-----GC--G--A---G--CG---G-T--G-A--C---CG----GT--GT-CT--TC--C----T---AG--TG----G--G--T-C---C---C-ACGT-----TG--A----A--R
> str27: A---A---AG----GT--T----T---A-T---AC--CT--TC--C---C-AG-GTAAC--A---A--A--C--CA-AC---CA--A--CT-T------T-C--G-AT-CT-C-T-----TG-----------
> str28: A-G----TAGT----T-C--GC----C--T-GT--G--TGA---GC-TG--A-C--AA---AC-T--TAGT-A---G--T-G-----T--T-TG-----TG--AG---G--A--T-----T---A--------
> str29: -T-----T--TA---TAC---C-T-TC---C-TA-G---G-T-A--A--C-A----AAC---C--A--A--C--CA-ACTT------T-C---G-A---T-CT--C-T--T--GTA-G-AT------------
> str30: ATGC--G--GT--CGT-CT--C-T--C---C---C--C-G----GC-T--T----T----T---T--T--TC--C---C---C-GC--GC----C-G-C-G-T----TG----G----C--GC--CG--A---
> str31: --G----T-G-A-C--A--A--A----AA-C--A----T-A--A---TG---G---A-C-T-C---C-A---A-CA--C---CA---TG-T---CA-A--GCT----T--T-C--A-G---G-TA-G--A-C-
> str32: --G----T-GTAA-G-A--A--A---CA---GTA--A--G--C--C---C--G-G-AA-GT--G-----GT-----G--TT------T--T--GC-GA-T--T----T-C---G-A-G---GC--CG---G--
> str33: --G-A-G-A--A---T----G-A-GTC--TC--A----T--T-A-C---C--GC----C---CG-----GT-A-C----TT--AGCA----A-GC----T---A--AT---A-GT---CA--C---G---GC-
> str34: ATG----T-G----GT-C--G-ATG-C---C--A----TG----G-A-G---GC----C---C--AC----CA---G--TT-CA---T--TA---AG---GCT--C---CT--G---GCAT--T---------
> str35: A--C--G-AG---CGT--T----T-T-AA--G---G---G--C--C---C--GCG-A-C-T--G--C--G--A-C-G----GC--CA--C-ATG--G-C--C---C-TG-TA--T--G--T------------
> str36: --G---GT--T----TA-TA-C----C--T--T-C--C----CAG---G-TA----A-C--A---A--A--C--CA-AC---CA--A--CT-T------T-C--G-AT-CT-C-T-----TG-TA-G------
> str37: -TG---G--G-AA-GT--T--C----CAA----A--A--GATCA-CA----A----AAC--AC-TAC----CA---G--T--CA--A--C----C----TG--A--A-G-TAC--A--C--------------
> str38: --G-A---AG---CGT--TA--A---C----GT--G--T--T--G-A-G---G---AA---A---A---G--A-CAG-CTT--AG---G--A-G-A-AC----A--A-G--A-G----C-TG----G---G--
> str39: A--C-C--AG---CG--C-A-C-T-TC----G---G-C--A---GC--G---GC--A--G--C--AC----C-TC-G----GCAGCA--C----C----T-C-AGCA-GC-A---A--C--------------
> str40: ATG---G--G-A-C--A--A-C-T-T-A-T--T-C--CT-ATCA---TG-T-GC----C--A---A---G--A---G----G-----T--T-T------T---A-C---C--CG---G--TG--AC--CA---
> str41: -T-----T-GTA--G-A-T--C-TGT---TC-T-C---T-A--A--A--C--G---AAC-T---T--TA---A--A-A-T--C----TG-T--G-----TG---G--T--T--GT---CA--CT-C-------
> str42: A---AC-------C--A--A-C----CAA-C-T-----T--TC-G-AT-CT--C-T----T--GTA---G--ATC----T-G-----T--T---C----T-CTA--A----ACG-AA-C-T--T---T-A---
> str43: --G---G--GT----T-CT-GC----CA---G---G-C--AT-AG--T-CT----T----T---T--T--T--TC----T-G--GC--G----GC---C--CT----TG-T--GTAA--A--C--C-T--G--
> str44: --G---G------C-T----GCATG-C--T--TA-G--TG--CA-C-T-C-A-CG---C--A-GTA-TA---AT-----T---A--AT---A---A--CT---A--AT--TAC-T--G--T------------
> str45: -TGCA--T-G---C-T--TAG--TG-CA--C-T-C-AC-G--CAG--T---A---TAA--T---TA--A-T-A--A--CT---A--AT--TA--C----TG-T--C--G-T----------------------
> str46: -T-----T-----C---C-A-CA----A--C-T-----T--TC--CA--C---C--AA-G--C-T-CT-G-CA--AGA-T--C--C---C-A-G-AG--T-C-AG---G----G---GC---CT--GT-----
> str47: -T-C---TA--AACG-A--A-C-T-T---T---A--A---A--A---T-CT-G--T---GT--G-----G-C-T--G--T--CA-C-T-C---G--G-CTGC-A---TGCT---TA-G---------------
> str48: A--C-CG--G-A---T----G---G-C---CG--CGA-T--T-----T--T----T--CG---G-A---GTC--C----TTG--G---G----G--GAC--C-A-C-T-C-A-G-AA---T---A-G--A---
> str49: ---C---T--T---GTA---G-AT--C--T-GT-----T---C----T-CTA----AACG-A---ACT--T--T-A-A-----A--AT-CT--G-----TG-T-G---GCT--GT---CA--CT---------
> str50: ATG-A-G------C--ACTA--A-G-C----G-A--A--GA--A-C---C-A----AA---A---A---G-CA---GAC----A--AT---A--CA-AC--C---C--GCTA--T-----T---AC-------
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
>   Sol: MAEQSKPFTLRSLENYAQHVFDAICNSRPGFVKGTNEGALHDYQ
> str01: MA-------L-S---Y--------C---P---KGT---------
> str02: M--QS------SL-N-A------I----P--V------------
> str03: M-----P--L-S---Y-QH-F------R----K-----------
> str04: M-E----------E----HV-----N----------E--LHD--
> str05: M---S---------N-----FDAI---R----------AL----
> str06: M------F--R---N--Q-------NSR-------N-G------
> str07: M------F-------YA-H---A-------F--G---G----Y-
> str08: M---SK-FT-R----------------RP-------------YQ
> str09: M---S--F-----------V--A------G-V--T---A----Q
> str10: M-E-S----L---------V--------PGF----NE-------
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
> --- Solution (of length 494) ---
>   Sol: MNARGFKEAHVIPWRSDFLEFAQKLNSRTAGDVYPSTKIELADFGTQIHEVRNTDPLAKEYQRDKWFLSNVGIMSFNVGKETPEARIHLQFANQPYLDVGRLFAIKMWEADATNQALGIDVHSPRWQSDNAFQTNKVYAMCGEDILWKRTKNVPHASGELFWTMSYCAAIPRVDQENKLGAQFITSPYHLVREPWLNEDRIGKLYPASHFTVSQLNFRMGETAHQIPSRFCNYLTDVGAKNACTDQESHKNVFPMREGKDIVFCATWLYEACPNKRQSFLRTVLPEADIWIGKVGTSCRFHYNALGWVIMTSDAEHPFCGALKNVTMAIDQHSLFYWRTDIRVNAKMEISPIFGVLDNYTEAPGCDNEKSHYLAFVRGITDEAPRVSKGCTLFADPQNMSERVWDKIALNSDRTDYNVFGMCEPLIVCSAQGYDMFKHNRSVADTGESLQNIKGHSGQATQDPVHELRMNQCIYKMGSDRAHKGQTNVFSIPWL
> str01: M--R-----H--------L------N------------I---D----I-E---T------Y-------S-----S-N--------------------D------IK-------N---G--V----------------Y---------K-----------------Y-A-----D------A-----------E-----D----------F----------E----I-------L---------------------------------L----------F-------A--------------Y---------S----------------ID-----------------------G---------G---E-------V-----E-------C-L--D-------------L----T-------------------------R------------------------------------------------------
> str02: M------E------R------------R-A------------------H--R-T---------------------------------H-Q--N--------------W--DAT----------------------K-----------------P-----------------R---E---------------R-------R--K----------Q-------T--Q-----------------------H------R-----------L-------------T------------------H---------------P------------D---------D---------S-I------Y---P-------------R-I--E-----K-----A------E------------------G-------------------R------------K------------E------------D--H-G----------
> str03: M------E----P-----------------G----------A-F------------------------S------------T--A---L-F------D-----A------------L-----------------------C--D-----------------------------D---------I-----L------------------H--------R----------R----L------------ES----------------------------Q--LR------------------F-----G-------------G----V-----Q---------I---------P-----------P----E-------V----------S-------DP-----RV------------Y-------------A-GY---------A-----L-----------------L---------------------------
> str04: M---G-K----------F---------------Y--------------------------Y-------SN---------------R--------------RL-A----------------V----------F------A-----------------------------------Q-----AQ---S-----R----------------H-----L----G-----------------G---------S--------------------YE------Q------------W--------------L--------A----C-----V-------S--------------------G--D------------S---AF-R-----A-----------------E-V--K-A----R----V------------Q-----K------D--------------------------------------------------
> str05: -----F-----------F---------R-----------E------------N---LA--------F----------------------Q---Q-----G-----K---A--------------R-----------------E-----------------F---------P--------------S------E----E--------A----------R----A--------N---------------S-----P-----------T-----------S--R----E------------------L-WV-----------------------------R---R-----------G---------G--N----------------P-------L-------SE------A-----------G---------A----------------E--------------------R-----------R---G-T--------
> str06: M---------------D-----------------PS----L----TQ---V--------------W------------------A-------------V---------E--------G----S-------------V--------L----------S----------AA---VD----------T---------------------A-------------ET---------N---D-------T--E------P-----D---------E---------------------G------------L------S-AE--------N-----------------------E-----G------E------------------T----R---------------------I------------------I-------------R-----------I-------T----------------GS----------------
> str07: M-A--F----------DF--------S-----V---T-------G-------NT----K--------L-----------------------------D--------------T---------S------------------G------------------F-T-----------Q----G----------V----------------S----S-----M--T--------------V-A--A---------------G-------T-L--------------------I--------------A--------D--------L--V--------------------K-------------T-A-------S----------------S---------Q-----------L----T--N-------L----AQ---------S-----------------------------------------------------
> str08: M-A-------VI------L---------------PST-----------------------Y--------------------T---------------D-G------------T--A--------------A---------C--------T-N-----G------S-----P--D----------------V--------------------V-------G-T---------------G-----T----------M-----------W---------------V-------------------N-------T-----------------I----L----------------P--G--D-----------------F-----------------F----------W---------T---------P----S--G--------------ES---------------V---R-------------------V------
> str09: MN--------------------------T-G-------I--------I------D-L---------F------------------------------D---------------N-------H--------------V------D------------S------------IP-------------T---------------I--L-P--H----QL-------A-----------T--------------------------------L-------------------D-------------Y--L--V-----------------------------RT-I-------I-------D---E-----N---------R---------S---------------V-----L---------------L----------F-H-------------I----------------M-------GS-----G----------
> str10: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-L------------R------------------T------R---T--Q--------L-------------------P------------------P-------------A--------------Y--------T------------N--------S-F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-------S----
> str11: M---------------D---------S----------K-E-----T-I--------L---------------I-------E-----I-----------------I------------------P-----------K--------I--K--------S--------Y------------L----------L--------D-----------T----N---------I-S-------------------------P----K------------------S-----------------------YN---------D----F----------I---S----R-----N-K-----------N--------------------I-------------F---------V---I--N--------------L-------Y-----N--V-----S-----------T------------I---------------------
> str12: M-----------------L-----L-S---G------K--------------------K-----K--------M--------------L-------LD---------------N-----------------------Y----E------T-----A-----------AA--R-------G-----------R---------G-----------------G---------------D----------E--------R-------------------R----R----------G--------------W------A---F-----------D-------R------------P----------A----------------I------V----T--------------K------R-D---------------------K---S--D-----------------------RM-----------AH------------
> str13: MN--G--E-----------E-----------D----------D---------N------E-Q----------------------A------A-----------A----E-----Q-----------Q------T-K-----------K-------A---------------------K-------------RE---------K--P---------------------------------K-----Q------------------A----------R----------------KV-TS-----------------E-----A---------------W----------E----------------------H---F-----D-A-------T---D---------D--------------G---------A----------------E------------------------C--K------H------------
> str14: M------E-------S--L-------------V-P---------G---------------------F--N----------E------------------------K------T--------H--------------V-------------------------------------Q---L------S---L---P-----------------V--L---------Q-----------V------------------R---D-V-----L--------------V---------------R------G-----------F-G---------D--S---------V----E------------E--------------V---------------L-------SE------A----R-----------------Q------H----------L---K--------D--------------G--------T--------
> str15: M--R-----------------------------Y----I-----------V-----------------S-------------P------Q------L-V--L------------Q-----V--------------------G-----K---------G----------------QE--------------V-E------R------A-------L-----------------YLT------------------P--------------Y------------------D-------------Y------I---D-E-------K---------S-----------------PI------Y------------Y--F----------------L---------R--------S--------------------------H----------L-NI-----Q---------R-----------------------P--
> str16: M-----------P-R-----------------V-P---------------V---------Y--D----S-------------P------Q--------V-----------------------SP-----N---T--V----------------P--------------------Q-----A----------R---L----------A---T---------------PS-F--------A----T---------P-----------T------------F-R----------G-----------A--------DA--P---A-------------F-------------------------------------------------------------Q-------D--------T---------------A--------N----------Q-------QA--------R--Q-----------------------
> str17: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-L------------R------------------T------R---T--Q--------L-------------------P-------------L--A------------------------------Y--------T------------N--------S-F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-------S----
> str18: M----F----V------F--F-----------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-L-----T-------------------------T------R---T--Q--------L-------------------P------------------P-------------A--------------Y--------T------------N--------S-F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-------S----
> str19: M------EA--I--------------------------I-----------------------------S------F--------A--------------G----I------------GI----------N-------Y---------K--K--------L--------------Q----------S----------------KL---------Q---------H-----------D----------------F----G-----------------R------VL--------K----------AL-----T-------------VT-A---------R------A----------L------PG--------------------------------Q--------------------------P------------KH-------------I------A-------------I------R----Q---------
> str20: M-A------------S----------S---G---P----E-----------R-----A-E---------------------------H-Q--------------I-------------I--------------------------L-------P----E-----S-----------------------HL-----------------S----S-------------P------L--V--K--------HK-----------------L-----------L---------------------Y---------------------------------YW--------K---------L---T---G--------L----------P-------L---P--------D-----------------E----C-----D-F-------D----------H-----------L-----I---------------------
> str21: M------E-------S--L-------------V-P---------G---------------------F--N----------E------------------------K------T--------H--------------V-------------------------------------Q---L------S---L---P-----------------V--L---------Q-----------V------------------R---D-V-----L--------------V---------------R------G-----------F-G---------D--S---------V----E------------E--------------V---------------L-------SE-V---------R-----------------Q------H----------L---K--------D--------------G--------T--------
> str22: M-----------------L--A------------PS-------------------P-------------N----S----K------I--Q------L-----F----------N---------------N--------------I------N-----------------I---D---------I------------N-------Y---------------E--H----------T--------------------------------LY---------F-------A---------S----------V---S-A----------------Q------------N-----S--F---------------------F-------A-------------Q------W-------------V--------V-----Y-------S-AD--------K-----A-------------I---------------------
> str23: M--------------S-----A----------------I------T---E---T----K-----------------------P-----------------------------T-----I-----------------------E--L-------P-A---L-------A-------E---G--F------------------------------Q---R--------------Y-------N--------K---------------T------P------------------G-------F----------T-------C-----V--------L-----D-R----------------Y------D----H------G-------V--------------------I--N-D----------------S-------K--------------I-----------V--L------Y------------N-------
> str24: M-----K------------------N------------I--A-------E----------------F------------K-------------------------K---A-------------P------------------E--L---------A--E------------------KL----------L--E------------------V----F----------S---N-L-----K-----------------G---------------N---S--R---------------S-------L-------D---P---------M----------R------A--------G--------------K-H---------D----V----------------V--------------V-------I--------------------ES-----------T--------------K-------K----------L
> str25: M-----------P---------Q-----------P-----L-----------------K--Q------S-------------------L--------D----------------Q-------S------------K----------W------------L-----------R---E----A-----------E---------K-----H-----L--R----A----------L------------ES-------------------L--------------V----D--------S-----N-L---------E--------------------------------E------------E-------K---L--------------K-------PQ-----------L-S---------M----------G--------------E--------------D-V------Q------S----------------
> str26: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-L----IT------R------------------T--Q-------------S----Y-T-----N------S----F------------T---------R---------------G-V-------Y---------------------------------Y--------------P-----D-----------K------V----------------F--------R--------S-----------------S------------V------L-----HS---TQD--------------------------------
> str27: M-----K----------F-------------DV-------L---------------------------S-------------------L-FA--P------------W-A-------------------------KV------D--------------E---------------QE-----------Y----------D--------------Q----------Q--------L------N---------N----------------------N-----L-----E----------S-----------I-T--A--P-----K-----------F----D----------------D------G---------A-----T-E------------------------I---------------E-----S-----------------E--------------------R--------G-D-----------I---
> str28: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-----F-T-----------N--R----------T--QL-----------PS----------A-----------------------------Y------------T--------------------N--------S-----F-------T-----------R---------------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-------S----
> str29: M------------W-S----------------------I--------I--V-----L-K--------L----I-S-----------I--Q----P-L----L--------------L---V------------T----------------------S--L----------P-------L--------Y--------N--------P---------N--M----------------D-----------S---------------C-------C-------L--------I-------S-R---------I-T-----P------------------------------E-------L-----A-G----K---L------T-----------------------W--I-----------F------I--------------------------------------------------------------------
> str30: M------E-------S--L-------------V-P---------G---------------------F--N----------E------------------------K------T--------H--------------V-------------------------------------Q---L------S---L---P-----------------V--L---------Q-----------V------------------R---D-V-----L--------------V---------------R------G-----------F-G---------D--S---------V----E------------E-------------F----------------L-------SE------A----R-----------------Q------H----------L---K--------D--------------G--------T--------
> str31: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V----------M------P-------L---F-------------N------L---------------------I--------T--------T---------------------T----------QS-----------------------Y--------T------------N----------F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-----------L
> str32: M--------H------------Q---------------I------T----V-------------------V---S---G---P-----------------------------T-----------------------------E---------V---S-----T---C---------------F------------------G-----S------L--------H--P--F---------------Q-S-------------------L------K---------P--------V---------------M---A---------N---A-----L-------------------GVL----E--G----K-----------------------------M-------------------F--C------S----------------------I-G--G----------R---------S---------------L
> str33: M-A-------------------------T-----------L---------------L-----R-----S-------------------L--A----L-----F--K------------------R----N-----K-------D---K-----P----------------P------------ITS---------------G-----S-----------G-----------------GA---------------------I--------------R---------------G----------------I-------------K--------H--------I-------I--I--V-------P---------------I----P----G-----D----S----------S--------------I------------------T--------------T-------R---------S-R--------------
> str34: M------E-------S--L-------------V-P---------G---------------------F--N----------E------------------------K------T--------H--------------V-------------------------------------Q---L------S---L---P-----------------V--L---------Q-----------V------------------R---D-V-----L--------------V---------------R------G-----------F-G---------D--S-------------ME------------E--------------V---------------L-------SE------A----R-----------------Q------H----------L---K--------D--------------G--------T--------
> str35: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-L-----T-------------------------T--------G-T--Q--------L-------------------P------------------P-------------A--------------Y--------T------------N--------S-F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-------S----
> str36: M-A----------------------N------------I--------I----N---L--------W---N-GI----V----P-----------------------M-------------V-----Q-D-------V--------------NV--AS------------I--------------T---------------------A--F-----------------------------K-------S------M-----I--------------------------D--------------------------E----------T----------W--D-----K----------------------K---------I--EA--------------N---------------T-------C---I--S----------R------------K-H------------R-N------------------------
> str37: M-----------------L------N-R----------I-------Q------T--L----------------M-----K-T--A-------N--------------------N-----------------------Y----E------T-------------------I-----E-------I-----L-R----N-------Y---------L--R---------------L----------------------------------Y-------------------I-I-------------L--------A-----------------------R-----N---E------------E--G------------RGI------------L--------------I--------Y-----------------D---------D------NI---------D---------------S---------V------
> str38: M-A-------------D-----------------P------A--GT------N------------------G--------E--E---------------G------------T----G----------------------C----------N-----G---W--------------------F----Y--V-E-------------A----V------------------------V---------E--K--------K------T-------------------------G--------------------DA--------------I---S------D----------------D---E-----NE-----------------------------N------D-----SD-T-----G--E----------D--------------L--------------V--------------D---------------
> str39: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V-----------------------N-L------------R------------------T------R---T--Q--------L-------------------P------------------P----S-----------------------Y--------T------------N--------S-F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H-------S----
> str40: M------E-------S--L-------------V-P---------G---------------------F--N----------E------------------------K------T--------H--------------V-------------------------------------Q---L------S---L---P-----------------V--L---------Q-----------V-----C-D------V---------------L--------------V---------------R------G-----------F-G---------D--S---------V----E------------E--------------V---------------L-------SE------A----R-----------------Q------H----------L---K--------D--------------G--------T--------
> str41: MN-----------------------N--------------------Q----R------K-----K----------------T--AR--------P---------------------------S--------F--N----M-----L-KR------A---------------R----N--------------R-------------------VS--------T--------------V----------S----------------------------Q--L------A-----K-----RF-----------S----------K------------------------------G-L----------------L-------------S-G-------Q----------------------G---P----------M-K-----------L--------------V----M-----------A-------F-----
> str42: M--------------S---------N-----------------F----------D--A--------------I------------R-----A----L-V-----------D-T------D----------A------Y---------K-----------L-------------------G--------H-----------I-------H---------M-------------Y--------------------P--EG-------T---E-------------------------------Y-----V-------------L----------S----------N--------F------T-----D----------RG--------S--------------R----I---------------E--------G---------V--T---------H----T---VH-----------------------------
> str43: M----------I-------E----L--R--------------------HEV----------Q---------G-------------------------D---L------------------V------------T----------I------NV-------------------V--E--------T-P-----E-----D----L-------------------------------D-G--------------F--R---D--F-------------------------I---------R----A-----------H-----L------I-----------------------------------C-------LA-V----D---------T---------E------------T------------------------------TG--L------------D----------IY--------------------
> str44: M----F----V------FL-------------V-------L---------------L-------------------------P-----L---------V-----------------------S----S----Q-------C-----------V----------M------P-------L---F-------------N------L---------------------I--------T--------T------N-------------------------QS-----------------------Y--------T------------N--------S-F---T--R-----------GV---Y------------Y-----------P----------D----------K-----------VF--------------------RS------S---------------V--L--------------H------------
> str45: M--------------S-------K-------D--------L---------V------A----R--------------------------Q-A----L---------M-----T--A--------R--------------M-------K-------A-----------------D--------F-------V------------------F------F----------------L------------------F--------V-----L---------------------W--K----------AL------S---------L----------------------------P---V-------P----------------T----R----C------Q---------I----D--------M--------A------K---------------K-------------L----------S--A--G----------
> str46: M-A------------S--L-----L------------K------------------------------S-------------------L-----------------------T---L--------------F---K------------RT---------------------R-DQ-----------P------P-L----------AS-----------G-------S---------G-------------------G------A-----------------------I---------R------G--I-------------K--------H----------V-----I--I--VL----------------------I----P----G-----D----S----------S--------------IV-----------------T----------------------R---------S-R--------------
> str47: M--R------V---R---------------G-------I-L----------RN------------W-----------------------Q---Q-------------W-----------------W------------------I-W--T------S--L-------------------G--F-----------W-----------------------M----------F------------------------M-----I--C-------------S----V----------VG-------N-L-WV--T-------------V----------Y----------------------Y----G-----------V-------P-V-----------------W-K----------------E------A------K-------T--------------T----------------------------------
> str48: M-A-------V--------E--------------P--------F-----------P------R----------------------R--------P---------I-------T-----------R----------------------------PHAS------------I-----E--------------V-------D-----------T-S------G-----I-----------G-------------------G-------------------S--------A----G----S--------------S--E-------K-V---------F-----------------------------C-------L-----I---------G-------Q----------A--------------E--------G-------------GE---------------P------N---------------T-V------
> str49: M----F---------------------------Y-------A------H--------A--------F----G------G----------------Y-D----------E----N--L----H--------AF---------------------P---G-----------I---------------S---------------------S--TV----------A--------N---DV------------------R--K---------Y--------S----V----------V--S----------V---------------------------Y-------N-K----------------------K--Y-------------------------N--------I----------V------------------K-N-------------K--------------------Y-M----------------W-
> str50: M-A----------------------N-------Y-S-K-----------------P----------FL--------------------L--------D------I---------------V----------F--NK-------DI--K------------------C--I------N---------------------D--------S----------------------C----------------SH----------------------------S---------D---------CR--Y----------------------------Q-S----------N-----S--------Y----------------V-----E---------L---------R----------R---N-------------Q-----------A-----L-N-K----------------N-----------------------L
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 93
> ```
