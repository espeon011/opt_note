In [ ]:
```python
import enum
import didppy
import util
```


In [ ]:
```python
import marimo as mo
import nbformat
```


# DIDP を用いたモデル

`DP` モデルの定式化を DIDP[^1] 用に書き直したもの.
基本的な遷移規則は `DP` と同様.

探索効率のため dual bound を何種類か用意した.

[^1]: https://didp.ai/

In [ ]:
```python
class BoundOption(enum.IntFlag):
    MAX_LEN = 0b1
    SCS2LEN = 0b10
    CHAR_COUNT = 0b100

    ALL = 0b111
```


In [ ]:
```python
def boundexpr_maxlen(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    min_to = dpmodel.add_int_table(
        [
            [
                len(s) - j for j in range(len(s) + 1)
            ]
            for s in instance
        ]
    )

    bound = didppy.IntExpr(0)
    for sidx, index_var in enumerate(index_vars):
        bound = didppy.max(bound, min_to[sidx, index_var])

    return bound
```


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
def boundexpr_charcount(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    chars = sorted(list(set("".join(instance))))

    # alpha_counts[char][s_i][idx]
    alpha_counts: list[list[list[int]]] = [
        [
            [0] * (len(s) + 1)
            for s in instance
        ]
        for char in chars
    ]

    for cidx, c in enumerate(chars):
        for sidx, s in enumerate(instance):
            alpha_counts[cidx][sidx][len(s)] = 0
            for i in range(len(s) - 1, -1, -1):
                alpha_counts[cidx][sidx][i] = alpha_counts[cidx][sidx][
                    i + 1
                ] + (1 if s[i] == c else 0)

    bound = didppy.IntExpr(0)
    for cidx, _ in enumerate(chars):
        expr = didppy.IntExpr(0)
        for sidx, _ in enumerate(instance):
            table_i = dpmodel.add_int_table(alpha_counts[cidx][sidx])
            expr = didppy.max(expr, table_i[index_vars[sidx]])
        bound += expr

    return bound
```


In [ ]:
```python
class Model:
    def __init__(
        self, instance: list[str], bound_option: BoundOption = BoundOption.SCS2LEN
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

        # Dual Bound
        if bound_option & BoundOption.MAX_LEN:
            # 残っている文字数が最長のものが下限
            dpmodel.add_dual_bound(boundexpr_maxlen(instance, dpmodel, index_vars))
        if bound_option & BoundOption.SCS2LEN:
            # 残っている文字列から 2 つを選んで SCS を取って長さが最大の物が下限
            # primal solution は 3 つの中で一番良いけど best bound は弱い
            dpmodel.add_dual_bound(boundexpr_scs2len(instance, dpmodel, index_vars))
        if bound_option & BoundOption.CHAR_COUNT:
            # 文字列とアルファベットごとに残数をカウントし, その最大値をアルファベット全体にわたって足したものが下限
            # best bound は良くなるけど primal solution はそんなに良くない
            dpmodel.add_dual_bound(boundexpr_charcount(instance, dpmodel, index_vars))

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
>  Sol: ultkcignkyuhcosjoemviqfaozgpplnbrxdxdbcsvrvnnshtuqgpxzvxissbxf
> str1: --tk--gnk-uh------m--------p-----x---------n--ht-qg-xzvxis----
> str2: -----i-------o-j----iqf-o----lnb-x-x--c-v----s--uq-p--v-issbxf
> str3: ul--ci-n-y--cos-o--v----oz-ppl---------------------p----------
> str4: -----ig----------e-v---a-zg----br-d-dbcsvrvnn-----g----------f
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 62
> 
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
> --- Solution (of length 99) ---
>  Sol: iojiqfopyplrtkgbdenbxvazwxqkrdurlcphmqvzfgjtdbpfuivxernzdsychodutmsbopcsvroqgxzpvnxnigplesswbpbxhdf
> str1: ------------tkg---n--------k--u----hm---------p----x--n-----h---t----------qgxz-v-x-i----s---------
> str2: iojiqfo---l-------nbx----x-------c----v------------------s-----u-----------q---pv---i----ss-b--x--f
> str3: ------------------------------u-lc---------------i----n---yc-o----s-o---v-o---zp------pl-----p-----
> str4: i-------------g--e---vaz-----------------g---b-------r--d-----d----b--csvr------vn-n-g------------f
> str5: -------pyplr-----------z-x----u--cp-mqv--g-td--fuiv--------c--d---sbo------------------------------
> str6: -------p-------bde---v-------d---c----v-----d-pf-------z-s-------msb-----roq----v-----------b-b-h--
> str7: -----------------enb-------------c-----zf-jt------vxer-z-----------b-----r------v---igple----------
> str8: -----------r--------x---wxqkrd-rlc---------t-----------------od-tm---p---r-----p--x--------w-----d-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 56
> 
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
> --- Solution (of length 149) ---
>   Sol: pyplrsxutiqobdzkjwaisgexqfolnbvckurdafzcpgqafjhtvdbmpxierfngxlequycdvjzseghtiwaoduqmbkvncestfzompbuvhdgikskrjvozqxizucpwvdsbngphxbaknghzlwidcompyfsge
> str01: --------t------k-----g------n---ku------------h----mpx----n---------------ht------q-------------------g----------x-z----v-------x---------i-------s--
> str02: ---------i-o----j--i----qfolnb-----------------------x------x-----c-v--s---------uq-------------p--v---i-s----------------sb----x----------------f---
> str03: -------u-------------------l---c----------------------i---n------yc------------o----------s---o----v----------oz------p-------p---------l------p-----
> str04: ---------i-----------ge-------v-----a-z--g--------b-----r----------d------------d---b---c-s--------v-------r-v--------------n-------ng-----------f---
> str05: pyplr---------z--------x---------u-----cp----------m-----------q----v----g-t----d-----------f-----u----i-----v-------c---dsb-----------------o-------
> str06: p-----------bd--------e-------v----d---c--------vd--p----f------------zs-----------m------s------b---------r--o-q-------v--b-----b----h--------------
> str07: ----------------------e-----nb-c------z-----fj-tv----x-er-------------z-------------b----------------------r-v----i----------gp---------l-----------e
> str08: ----r-x----------w-----xq-------k-rd--------------------r----l----c--------t---od----------t---mp----------r----------p---------x--------w-d---------
> str09: ---------------k----------------k---------qaf---------i----g---q-----j-------w-o-----k------------------kskr---------------b------------l----------g-
> str10: ---l--x----------------x----------------p--a------b---i-------------v---------------b-v------z----------k-----oz---z----vd---------------------------
> str11: ---------------k------------------r-------------------i--f-------------s------a-------vnc------------d----------q------w-------h-------z----c--------
> str12: ----------q-------a----x---------u-d-----gq-----v--------------q--c-----e----w------b-------f---------gi----j-o--------w-----------------w------y----
> str13: ----rsx---q-----j-----------n--------f--p--a-----d----i---------u------s----i-----q-b----e---z------h---k-----o----------------h--------------m----g-
> str14: ---------i-------w--s-------------------------h-v-------------------------h-------------c-----om-------i------------u---vd-----------------d--m------
> str15: ----------------------------------------------ht-----x------x--q-----jz-----------q-b---c--t-----b--------------------------------akn----------------
> str16: ------xu------------s----f-----c-----fz-p--------------e------e---c-v--------wa--------n---tf--m------g---------q--zu--------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 49
> 
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
>   Sol: bbaedcdbeacdeecbdbeacbdcade
> str01: ----dc-b--c---c-db--c--c--e
> str02: b---d-dbe---ee----e--bd----
> str03: -----c---acdeec---e--b----e
> str04: --aed-d----d----d-e--bd--d-
> str05: --a--c-be---e-c----a-b-c--e
> str06: bba----be------bd---cb--a--
> str07: bbae-----a--e--b---a--d-a--
> str08: ---e----e---eecbdbe-------e
> str09: -----c----cdee--d--a--dc-d-
> str10: b---d----a-----bdbea----ad-
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 27
> 
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
>   Sol: dbaecdeabecdabceadecbdeabeacdbcead
> str01: d---c---b-c---c--d--b------c--ce--
> str02: -b---d-----d-b-e--e---e--e---b---d
> str03: ----c--a--cd---e--ec--e-be--------
> str04: --ae-d-----d-----d---de-b---d----d
> str05: --a-c---be-----e---c---ab--c---e--
> str06: -b------b---ab-e----bd-----c-b--a-
> str07: -b------b---a--ea-e-b--a----d---a-
> str08: ---e--e--e-----e---cbd--be-----e--
> str09: ----c-----cd---e--e--d-a----d-c--d
> str10: -b---d-ab--d-b-ea------a----d-----
> str11: ---e-de----da---a------a-ea-----a-
> str12: --a----a-e--a---a---b-e--eac------
> str13: ---e---a----abc-a--c-------cdb----
> str14: -b---de--e--a----de----a----d--e--
> str15: ----c--a-e-da----de---e--e--d-----
> str16: ---e----b-c-a----d--b--ab----b-e--
> str17: d----d----c----e--e----ab---d--ea-
> str18: d-a-----b-cd-----de----a-e-c------
> str19: --a----a---d--ce--e--d-a--a--b----
> str20: --ae--e---c---ce--e---ea--a-------
> str21: -b------b--da--e---c---a--a-d--e--
> str22: d-a-c-e----da--e-d-----ab---------
> str23: --a----a-e--ab------b---b----bce--
> str24: d--e-d--b-c--bc-a------ab---------
> str25: db---d-a----a--e----b---b--c-b----
> str26: d--e----be-d-b-e----b--a---c------
> str27: ----c-e--e---bc--d-cbde-----------
> str28: db-e-d-a----a----d-----a--a--b----
> str29: ----c-----c---c--d-cb-e-b---d-c---
> str30: --ae--ea--cd-bc-----bd------------
> str31: d-a-c---be--a-c----c-------cd-----
> str32: ---ec-e-b-c---c--d--bd--b---------
> str33: d----d--b----bce-d-----ab----b----
> str34: --a----a-e--ab--a------a-e---b--a-
> str35: ---ec---b----bc-a------a----d-c--d
> str36: d--e----b-c---ce---c-d--b--c------
> str37: d-a----a--c--b--a-e---e-b--c------
> str38: --a--d-abe--a---a--c-------c---e--
> str39: d-aecd--b---a-c-a------a----------
> str40: d-a-c---b----b---d-c--e-----d-c---
> str41: d--e-d--be-----e----b---b---d--e--
> str42: ----cd-a---d--c--d-c-d-a--a-------
> str43: ----c-e--e-d--c-----b--a-e-----e-d
> str44: ----c-ea-ec-a---a------a---c----a-
> str45: d---c-----c---ce----b---b----b--ad
> str46: -bae--ea-e---b------bde-----------
> str47: db---de-b---a-c----c-d--b---------
> str48: ---e----b-c--b-e--e--d-a-ea-------
> str49: --ae--e--e---b------bd--b--c----a-
> str50: db---d-ab-c----e---cb---b---------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 24
> 
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
>   Sol: TACTACGCGTAGATCAGACTGTAC
> str01: -A-T--G-G--GAT-A--C-G---
> str02: -A-TAC-C-T---TC---C----C
> str03: --C-ACG---A-AT-----TG-A-
> str04: TA--A-----A-ATC----TGT--
> str05: -A----G-GTA-A-CA-A----A-
> str06: T--T-C-C-TAG----G--T--A-
> str07: T--T--G--TAGATC----T----
> str08: T-----G-G--GA--AG--T-T-C
> str09: T--T-C-C--A---CA-ACT----
> str10: T-CTA-----A-A-C-GA----A-
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 24
> 
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
>   Sol: ACTGACGTAGTAACGTACATGCATCAGACTCAGTCAGTAGCTGATCATGCGATCAGTACAGCTAACTGCAAGTACCTGCATAGCATGCAGTCGATGCACTGCAGTACTCGTACGTAGACTGCATCCGTAGTCR
> str01: --T-A-GTAGTA--G-AC-T-C--C-G-----G--A--AG-TGA-CA----A--A---C--C---CTG-AA--A-----A--G-A---A-T-G--G-A-T--A--A-----A--TA---T--A----------
> str02: ---G--G-A-TAA---ACA--C-TC---C-C-G--A--A----A--AT---A--A-T-----T---TG-A----C-T---TA--A---A--C-A---AC-GC-G-AC----A-GT----T-CA-----AG---
> str03: A-T-AC-------C-T---T-C--C----T-AG---GTA----A-CA----A--A---C--C-AAC--CAA---C-T---T----T----T-GAT-C--T-C--T--T-GTA-G-A---T-C-T--G------
> str04: --T-A---A--A---T---T--AT-A-A-TC--T---TA--T-A-C-T---A---GTA-A---AA----AA-TA---G----G---G---T-G-T--A----A---C-CG-A---A-A----A-C-G--GTC-
> str05: --T----TA--AA---ACA-GC--C----T--GT--G--G--G-T--TGC-A-C----C--C-A-CT-CA----C----A--G---G--G-C----C-C---A---CT-G---G--G-C-GCA-----AG---
> str06: A-TGAC-T--T--C---CA---AT--G-----G--A-T--C----C---C-A--A---C--CT--C---AAG--C-T---T--C---CA--C----C-C--CA--A-T-G---GT----T---TC---AG-C-
> str07: A---AC--A--AAC---CA---A-C---C--A---A----CT--T--T----T--G-A----T--CT-C---T---TG--TAG-AT-C--T-G-T----T-C--T-CT---A---A-AC-G-A-----A--C-
> str08: A-TGA---A--AACG-A-A---A--A---T---T-A-T---T-ATCA----A---G----G------G----TA--TG----G-A---AGT-G--G-A----AG--CT-G-ACG-A-A----AT---------
> str09: ACT--CG--G---C-T----GCAT--G-CT---T-AGT-GC--A-C-T-C-A-C-G--CAG-TA--T--AA-T---T--A-A---T--A----A--C--T--A--A-T--TA---------------------
> str10: --T----T-GTA--G-A--T-C-T--G--T---TC--T--CT-A--A----A-C-G-A-A-CT---T-----TA-----A-A--AT-C--T-G-TG---TG--G--CT-GT-C--A--CT-C-----------
> str11: ---G-C--AG-A--G--CAT---T-----T---TC--TA----AT-AT-C---CA---CA---AA----A--T----G-A-AG---GCA----AT--A----A-T--T-GTAC-TA--CT-C-----------
> str12: A-TGA-G------C---CA---A---GA-TC---C-G-A-C-GA--A-G--A---G--C--C---C--CAAG-----G-A--G---G-AG---A---A--G--G-A---G---G--GAC--C--CC-----C-
> str13: --T--C-T-----C--ACA-G--T-----TCA---AG-A----A-C---C---CA--A-AG-TA-C--C-----CC--C----CAT--AG-C----C-CT-C--T--T---A---A-A--GC--C---A--C-
> str14: A--G--GT--T----TA--T--A-C---CT---TC-----CT-A----G-G-T-A--ACA---AAC--CAA---CC---A-A-C-T----T---T-C---G-A-T-CTC-T---T-G--T--A----------
> str15: A--G--GT--T----TA--T--A-C---CT---TC-----C----CA-G-G-T-A--ACA---AAC--CAA---CC---A-A-C-T----T---T-C---G-A-T-CTC-T---T-G--T--A----------
> str16: --T-A---A--AAC--A-A--C-TCA-A-T-A--CA--A-C--AT-A----A---G-A-A---AA-T-CAA---C--GCA-A--A---A----A--CACT-CA---C----A---A-A---------------
> str17: -C---CG------C---C---CAT-----T---T--G--G--G--C--G-G--C--T-C---T--C-G-A-G--C--G-ATAGC-T-C-GTCGA---A-T-C----C-C-T-CG-A--C--C-T---------
> str18: A-T-AC-------C-T---T-C--C---C--AG---GTA----A-CA----A--A---C--C-AAC--CAA---C-T---T----T-C-G---AT-C--T-C--T--T-GTA-G-A---T-C-T--G------
> str19: --T--C-T-----C--ACA-G--T-----TCA---AG-A----A-C---C--TCA--A--G-T--CT-C-----CC--C----CAT--AG--G---C-CT-C--T--T--T-C--AG--T-CA---G------
> str20: ---GA--T-----C-T-C-T-C-TCA--C-C-G--A--A-C----C-TG-G--C----C--C---C-G---G-----GCA-A--ATGC---C----C--T--A--A-TC---C--AGA--G-----GT-G---
> str21: A--GA-G------C--A-AT-CA---G--T--G-CA-T--C--A----G--A--A--A----TA--T--A----CCT--AT----T--A-T--A--CACT----T--T-G--C-TA-A--G-A-----A-T--
> str22: A---A--T--TAA---A
> ```

> ```
> -A--CATC----TCA---A-TA-C--A--A--C-AT-A--A--G--AA----AA--AC----A-A-C--GCA----A---A----A--AC----AC-T---C---AT---------
> str23: A---A---A----CG-A-A--C-T-----T---T-A--A----A--AT-C--T--GT---G-T----G---G--C-TG--T--CA--C--TCG--GC--TGCA-T----G--C-T----T--A---GT-G-C-
> str24: A-T-A---A----C-TA-AT---T-A--CT--GTC-GT---TGA-CA-G-GA-CA---C-G--A---G----TA-----A---C-T-C-GTC--T--A-T-C--T--TC-T--G-------------------
> str25: A-TGA-GT-GT--C--AC--G-A--A---T---TCA----C-G-T-A--C-A--A-T---G--AACTG---G-A--TG--T----T-CA--CG-TG----G-A--A-T---A---A-----------------
> str26: AC---CGT-G----G-----GC----GA----G-C-G--G-TGA-C---CG----GT---G-T--CT-----T-CCT--A--G--TG--G--G-T-C-C--CA---C--GT---T-GA----A---------R
> str27: A---A---AG----GT---T---T-A---T-A--C-----CT--TC---C---CAG----G-TAAC---AA--ACC---A-A-C---CA----A--C--T----T--TCG-A--T---CT-C-T---T-G---
> str28: A--G---TAGT----T-C--GC--C----T--GT--GT-G---A----GC--T--G-ACA---AACT-----TA---G--TAG--TG---T---T----TG---T----G-A-G--GA-T---T----A----
> str29: --T----T--TA---TAC---C-T-----TC---C--TAG--G-T-A----A-CA--A-A-C---C---AA---CC---A-A-C-T----T---T-C---G-A-T-CTC-T---T-G--T--A---G-A-T--
> str30: A-TG-CG--GT--CGT-C-T-C-TC---C-C---C-G--GCT--T--T----T---T-----T---T-C-----CC--C---GC--GC---CG---C---G---T--T-G---G----C-GC--C-G-A----
> str31: ---G---T-G-A-C--A-A---A--A-AC--A-T-A--A--TG-----G--A-C--T-C--C-AAC---A----CC---AT-G--T-CA----A-GC--T----T--TC--A-G--G--T--A---G-A--C-
> str32: ---G---T-GTAA-G-A-A---A-CAG--T-A---AG---C----C---CG----G-A-AG-T----G---GT----G--T----T----T---TGC---G-A-T--T--T-CG-AG---GC--C-G--G---
> str33: ---GA-G-A--A---T----G-A---G--TC--TCA-T---T-A-C---CG--C----C--C-----G---GTAC-T---TAGCA---AG-C--T--A----A-TA---GT-C--A--C-G-----G----C-
> str34: A-TG---T-G----GT-C--G-AT--G-C-CA-T--G--G---A----G-G--C----C--C-A-C--CA-GT---T-CAT----T--A----A-G----GC--T-C-C-T--G--G-C---AT---T-----
> str35: AC-GA-G------CGT---T---T-----T-A---AG--G--G--C---C---C-G--C-G--A-CTGC--G-AC--G----GC---CA--C-ATG----GC----C-C-T--GTA---TG--T---------
> str36: ---G--GT--T----TA--T--A-C---CT---TC-----C----CA-G-G-T-A--ACA---AAC--CAA---CC---A-A-C-T----T---T-C---G-A-T-CTC-T---T-G--T--A---G------
> str37: --TG--G--G-AA-GT---T-C--CA-A---A---AG-A--T---CA--C-A--A--A-A-C-A-CT--A----CC---A--G--T-CA----A--C-CTG-A--A---GTAC--A--C--------------
> str38: ---GA---AG---CGT---T--A--A--C---GT--GT---TGA----G-GA--A--A-AG--A-C---A-G--C-T---TAG---G-AG---A---AC---A--A---G-A-G----CTG-----G--G---
> str39: AC---C--AG---CG--CA--C-T-----TC-G---G---C--A----GCG----G--CAGC-A-C--C---T-C--G----GCA-GCA--C----C--T-CAG--C----A-G----C---A-----A--C-
> str40: A-TG--G--G-A-C--A-A--C-T-----T-A-T---T--C----C-T---ATCA-T---G-T----GC-----C----A-AG-A-G--GT---T----T----TAC-C---CG--G--TG-A-CC--A----
> str41: --T----T-GTA--G-A--T-C-T--G--T---TC--T--CT-A--A----A-C-G-A-A-CT---T-----TA-----A-A--AT-C--T-G-TG---TG--GT--T-GT-C--A--CT-C-----------
> str42: A---AC-------C--A-A--C--CA-ACT---T---T--C-GATC-T-C--T---T---G-TA---G-A--T-C-TG--T----T-C--TC--T--A----A--AC--G-A---A--CT---T---TA----
> str43: ---G--G--GT----T-C-TGC--CAG-----G-CA-TAG-T---C-T----T---T-----T---T-----T---T-C-T-G---GC-G--G---C-C--C--T--T-GT--GTA-A----A-CC-T-G---
> str44: ---G--G------C-T----GCAT--G-CT---T-AGT-GC--A-C-T-C-A-C-G--CAG-TA--T--AA-T---T--A-A---T--A----A--C--T--A--A-T--TAC-T-G--T-------------
> str45: --TG-C--A-T---G--C-T---T-AG--T--G-CA----CT---CA--CG--CAGTA----TAA-T-----TA-----ATA--A--C--T--A---A-T----TACT-GT-CGT------------------
> str46: --T----T-----C---CA--CA--A--CT---T---T--C----CA--C---CA--A--GCT--CTGCAAG-A--T-C----C---CAG---A-G---T-CAG-----G---G--G-C--C-T--GT-----
> str47: --T--C-TA--AACG-A-A--C-T-----T---T-A--A----A--AT-C--T--GT---G-T----G---G--C-TG--T--CA--C--TCG--GC--TGCA-T----G--C-T----T--A---G------
> str48: AC---CG--G-A---T----G-----G-C-C-G-C-G-A--T--T--T----T---T-C-G------G-A-GT-CCT---T-G---G--G--G--G-AC--CA---CTC--A-G-A-A-T--A---G-A----
> str49: -CT----T-GTA--G-A--T-C-T--G--T---TC--T--CT-A--A----A-C-G-A-A-CT---T-----TA-----A-A--AT-C--T-G-TG---TG--G--CT-GT-C--A--CT-------------
> str50: A-TGA-G------C--AC-T--A--AG-C---G--A--AG---A--A--C---CA--A-A---AA--GCA-G-AC----A-A---T--A--C-A---AC--C----C--G--C-TA---T---T----A--C-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 84
> 
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
>   Sol: MQPSKFTRAESLNESYAQHFVDANISRCPGVKFGTNEALHDGYQ
> str01: M-------A--L--SY-----------CP--K-GT---------
> str02: MQ-S------SLN---A-------I---P-V-------------
> str03: M-P--------L--SY-QHF------R----K------------
> str04: M--------E---E----H-V--N------------E-LHD---
> str05: M--S--------N------F-DA-I-R----------AL-----
> str06: M----F-R----N----Q-----N-SR--------N-----G--
> str07: M----F---------YA-H---A---------FG-------GY-
> str08: M--SKFTR------------------R-P-------------YQ
> str09: M--S-F--------------V-A------GV---T--A-----Q
> str10: M--------ESL--------V-------PG--F--NE-------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 29
> 
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
> --- Solution (of length 500) ---
>   Sol: MEWFNGPAKDELRYSIVFDAHREPSNGADLIKSDTYQLREHIGSANIFTKGVPLYERQSFKVIDNLVWASGANEKAIQTMEGRLDMNASFHQAPKYRLTDYIEVADIFQNTWGLIDEPSAHKVLDGNSMYWRQATIHVFWNECKPAADHLNTFAQSRVCDLMGIAWLAEKPRGIFYVDLASQTNGEAHFDLIDPFERVTKGNSCRPQLETWKDAMGYSHGEQRKIVTLMPFNAQLHDRYFSATGGNSDCVLNFKMPEADGHIVKTGCRYEPARDNTFAHQKSLEQMVVYIATNGLSFADWRGKESTICAYLRFAKWPVCIDANTRAKHYLWSGVDKFQSNIELVDFYCLRAEPIGIEMAIKTYEFVMDSLNHPARYIAGKDEHKLFTNRFASYVIGDPLCGEQFCADLSAVRWEKTPGNDCEIVSEVAPRDMYGACDKFWHQDNSKLIYTHMAGEVDQLNSHTMLQAIYRWSHPKVIADGQMTSNRQFGLADTIKYVHPL
> str01: M-----------R-------H--------L---------------NI----------------D------------I---E-----------------T-Y-----------------S--------S------------N------D---------------I-----K-------------NG------------V------------------Y------K--------------Y--A-----D---------A-----------E---D--F------E-----I----L---------------L-FA--------------Y--S--------I---D---------G-----------------------G--E-----------V-------E--C--L-----------D--------------------------L--T-------------------R------------------------------
> str02: ME----------R--------R-----A------------H---------------R---------------------T-----------HQ-----------------N-W---D---A--------------T--------KP-----------R-----------E--R------------------------R--K------Q--T-----------Q-------------H-R------------L-------------T-------------H-------------------------------------P---D-------------D---S-I-----Y-----P---------------------R-I----E-K------A----------E---------------G-----------R-------K----------------E-D----H-----------------G--------------------
> str03: ME----P-------------------GA-------------------F----------S-------------------T--------A---------L---------F-------D---A---L------------------C----D-----------D---I--L--------------------H--------R-------R--LE--------S---Q-----L---------R-F---GG----V-----------------------------Q---------I--------------------------P-----------------------------------P---E--------V--S-----------D----------------P-------------R-----------V--------Y-A------------------G--------------Y--------A-----------L---------L
> str04: M----G--K--------F-----------------Y------------------Y---S-----N-----------------R-------------RL------A-----------------V---------------F------A--------Q---------A----------------Q--------------------S-R-------------H--------L---------------GG-S---------------------YE---------Q-------------------W----------L--A----C--------------V----S---------------G------------DS----A-----------F--R-A----------E--------V---K------------A-R-------------------------V-Q----------------K---D---------------------
> str05: ---F-------------F---RE--N---L--------------A--F---------Q-------------------Q---G------------K---------A--------------------------R---------E----------F-----------------P---------S----E---------E-----------------A--------R---------A------------NS--------P--------T----------------S------------------R--E------L----W-V------R------------------------R----G-----------------------G--------N---------PL---------S----E-------------A-----GA-------------------E--------------R---------------R--G---T-------
> str06: M--------D-------------PS----L----T-Q--------------V---------------WA----------------------------------V------------E--------G-S---------V-----------L-----S--------A--A--------VD----T---A--------E--T--N----------D-------------T-----------------------------E-------------P--D---------E---------GLS-A-----E------------------N------------------E-
> ```

> ```
> -----------G-E----T------------R-I-----------------I----------------R----------I--------------------------T---G------S---------------------------------------
> str07: M------A---------FD----------------------------F----------S--V----------------T--G----N-----------T----------------------K-LD---------T--------------------S------G-----------F-------T-----------------------Q--------G---------V--------------S-----S-------M---------T---------------------V---A------A---G---T----L--------I-A------------D-------LV----------------KT-----------A-----------------S----------------S--------------------------------Q----L--T---------N----L-A-------------Q--S----------------
> str08: M------A--------V-------------I------L--------------P-----S-------------------T----------------Y--TD------------G---------------------T----------AA-----------C-----------------------TNG-----------------S--P------D------------V-----------------------V---------G----TG---------T---------M-------------W-----------------V----NT----------------I-L---------P-G------------D-----------------F---F----------------------W--TP-------S--------G--------------------E-----S--------------V---------R----------V---
> str09: M---N-----------------------------T-------G---I---------------ID-L-----------------------F---------D---------N----------H-V-D--S-------I--------P------T-----------I--L---P----------------H------------------QL-----A------------TL--------D-Y-----------L-----------V----R-------T-------------I----------------I-------------D--------------------E----------------------------N---R----------------S-V----L--------L------------------------------F-H------I---M-G------S------------------G--------------------
> str10: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N------L-----R-T-----R----T-----------Q-----L-P-------------------------P-A----------Y------T----------------N--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------------------------
> str11: M--------D----S----------------K-------E--------T-------------I--L----------I---E--------------------I----I----------P---K-------------I-------K-----------S-------------------Y--L-----------L-D-----T--N----------------------I---------------S--------------P-------K-----------------S------Y---N-----D-------------F------I-----------S-----------------R--------------------N--------K-------N------I--------F------V-----------I--------------------N--L-Y----------N---------------V-------S--------TI------
> str12: M----------L-----------------L--S---------G------K----------K-------------K----M---L-------------L-D---------N-------------------Y-----------E---------T-A----------A--A---RG-----------------------R---G--------------G--------------------D-------------------E----------R----R---------------------------RG-------------W-----A--------------F-------D----R--P-----AI-----V--------------------T---------------------------K--------------RD------K------S-----------D------------R-----------M--------A------H--
> str13: M---NG----E-----------E-----D----D-----------N---------E-Q----------A--A---A----E----------Q----------------Q-T----------K---------------------K-A-----------------------K-R-------------E-------------K-----P-----K---------Q----------A----R---------------K--------V-T----------------S-E------A--------W---E-----------------------H--------F-------D-----A----------T-----D------------D--------------G---------A-------E------C----------------K--H-----------------------------------------------------------
> str14: ME------------S--------------L---------------------VP-----------------G------------------F-------------------N------E----K------------T-HV----------------Q-----L-------------------S---------L--P---V---------L-------------Q---V-----------R---------D-VL-----------V----R-------------------------G--F----G------------------D----------S-V-------E---------E-------------V---L---------------------S---------E---A-----R-----------------------------Q--------H-------L---------------K---DG--T-----------------
> str15: M-----------RY-IV-------S---------------------------P----Q-------LV----------------L-------Q-----------V--------G--------K---G------Q--------E---------------V----------E--R-------A----------L-------------------------Y----------L--------------T------------P------------Y----D--------------YI--------D----E----------K----------------S--------------------PI--------Y------------Y---------F------------L------------R------------S---------------H-----L------------N-------I------------Q----R------------P-
> str16: M-----P-----R---V------P---------------------------V--Y--------D-----S-----------------------P--------------Q-------------V----S----------------P-----NT-----V------------P----------Q----A---------R----------L-----A------------T--P----------S-----------F----A------T-----P----TF-------------
> ```

> ```
> ----------RG------A-----------DA------------------------------P-----A-----F-------------------------------------Q---D--------T-----------A---------------N-------------Q-------QA--R----------Q-------------------
> str17: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N------L-----R-T-----R----T-----------Q-----L-P----L------A--------------------------Y------T----------------N--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------------------------
> str18: M--F------------VF-----------------------------F---V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N------L-------T----------T------------R---T------QL--------------------P--------------PA----------------Y--TN--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------------------------
> str19: ME-----A-------I--------------I-S--------------F--------------------A-G-----I----G-------------------I-------N-------------------Y-------------K-------------------------K--------L--Q--------------------S--------K---------------L-----Q-HD--F---G-----------------------R------------------V-------L-------K-----A-L------------T---------V---------------------------T-----------AR--A------L------------P--G-Q-------------P--------------------K--H------I----A--------------I-R----------Q-------------------
> str20: M------A------S---------S-G-------------------------P--ER-----------A----E----------------HQ---------I----I------L---P-----------------------E-------------S-------------------------------H--L-----------S--------------S-----------P----L--------------V---K------H--K------------------L-----------L--------------Y------------------Y-W----K------L------------------T----------------G-----L------------PL-----------------P--D-E-------------CD-F---D-------H-------L--------I--------------------------------
> str21: ME------------S--------------L---------------------VP-----------------G------------------F-------------------N------E----K------------T-HV----------------Q-----L-------------------S---------L--P---V---------L-------------Q---V-----------R---------D-VL-----------V----R-------------------------G--F----G------------------D----------S-V-------E---------E-------------V---L---------------------S---------E--------VR-----------------------------Q--------H-------L---------------K---DG--T-----------------
> str22: M----------L-------A---PS---------------------------P-----------N----S----K-IQ-----L-----F-------------------N----------------N--------I----N----------------------I-------------D-------------I---------N--------------Y---E--------------H------T-------L-----------------Y-------FA---S----V--------S-A---------------------------------------Q-N----------------------------S----------------F---FA-----------Q---------W----------V--V-----Y-----------S-------A---D-----------------K--A---------------I------
> str23: M-------------S----A----------I---T----E--------TK--P-------------------------T----------------------IE----------L---P-A---L---------A-------E--------------------G-----------F------Q--------------R-------------------Y--------------N---------------------K----------T-----P----------------------G--F--------T-C---------V-----------L----D--------------R------------Y----D---H------G--------------VI-----------------------ND----S------------K---------I-------V--L---------Y---------------N---------------
> str24: M-------K----------------N----I-------------A----------E---FK-------------KA-----------------P--------E----------L-----A---------------------E-K-----L----------L-------E-------V-----------F-------------S----------------------------N--L------------------K-----G--------------N------S------------------R---S-----L---------D-------------------------------P----M----------------R--AGK--H-------------D-------------V------------V--V--------------------I------E-----S-T-----------K-------------------K----L
> str25: M-----P-----------------------------Q---------------PL------K----------------Q----------S--------L-D--------Q---------S--K--------W------------------L------R-----------E----------A-----E-------------K------------------H--------L---------R---A--------L-----E------------------------SL---V-----------D-----S-----------------N------L-----------E---------E----E---K--------L---------K-----------------P----Q----LS----------------------M-G--------------------E-D------------------V----Q--S----------------
> str26: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N------LI------T-----R----T-----------Q----------------
> ```

> ```
> --S---------------------------Y------T----------------N--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------T---Q----D--------
> str27: M-------K--------FD--------------------------------V-L----S------L-----------------------F--AP-----------------W-------A-KV-D----------------E------------Q-------------E------Y-D---Q------------------------QL-----------------------N-------------N-----N------------------------------LE-----------S----------I----------------T-A--------------------------P-------K---F--D------------D--------------G---------A---------T-----EI--E------------------S---------E--------------R---------G-----------D-I------
> str28: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N----F---------T--N--R----T-----------Q-----L-P----------SA--------------------------Y------T----------------N--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------------------------
> str29: M-W-----------SI--------------I--------------------V-L------K----L----------I-----------S------------I------Q--------P-----L-------------------------L----------L---------------V-----T-------------------S----L---------------------P----L---Y------N---------P------------------N----------M------------D-----S--C----------C----------L----------I---------------------------S-----R-I---------T----------P---E-----L-A-------G-------------------K--------L--T--------------------W-----I----------F-----I------
> str30: ME------------S--------------L---------------------VP-----------------G------------------F-------------------N------E----K------------T-HV----------------Q-----L-------------------S---------L--P---V---------L-------------Q---V-----------R---------D-VL-----------V----R-------------------------G--F----G------------------D----------S-V-------E---------E------------F----L---------------------S---------E---A-----R-----------------------------Q--------H-------L---------------K---DG--T-----------------
> str31: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V---M--------P-------L---------F------------N-----L----------------I-T---------------T---------------------T--------------Q-S------Y--TN---F--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H--L-----------------------------------
> str32: M-------------------H---------------Q----I------T--V---------V-------SG----------------------P----T---EV--------------S---------------T-------C---------F---------G-----------------S---------L---------------------------H-----
> ```

> ```
> -----PF--Q------S---------L--K-P------V----------------------M----A-N----A------------L---------------------GV--------L--------E--G-----K-----M------------------F-------------C--------S-------------I----------G-------------------G---------------R-S-----------------L----------
> str33: M------A--------------------------T--L---------------L--R-S------L--A--------------L-----F----K-R------------N-----------K--D------------------KP-------------------------P--I--------T-------------------S------------G-S-G-----------------------G-------------A---I-----R-------------------------G------------I-------K------------H------------I------------I-I---------V------P---I--------------------P--G-----D-S---------------S----------------------I-T------------T------R-S-------------R--------------
> str34: ME------------S--------------L---------------------VP-----------------G------------------F-------------------N------E----K------------T-HV----------------Q-----L-------------------S---------L--P---V---------L-------------Q---V-----------R---------D-VL-----------V----R-------------------------G--F----G------------------D----------S-------------------------M-----E-----------------E-----------V----L---------S----E-------------A-R-----------Q--------H-------L---------------K---DG--T-----------------
> str35: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N------L-------T----------T-----G----------T------QL--------------------P--------------PA----------------Y--TN--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------------------------
> str36: M------A-----------------N----I----------I---N-------L-------------W----N--------G-------------------I-V-------------P----------M--------V----------------Q----D----------------V------N-------------V---------------A---S------I-T-----A------F-------------K---------------------------S---M---I--------D----E-T---------W----D-----K--------K----IE--------A-------------------N---------------T------------C----------------------I-S----R-------K--H----------------------------R--------------N---------------
> str37: M----------L-------------N------------R--I---------------Q--------------------T----L-M--------K---T-----A----N----------------N--Y-----------E---------T-----------I----E----I----L-----------------R----N--------------Y----------L---------R------------L-----------------Y--------------------I----------------I---L--A----------R--------------N-E---------E--G-------------------R---G---------------I---L-----------------------I---------Y---D-----DN---I--------D---S--------------V------------------------
> str38: M------A-D-------------P---A--------------G-----T---------------N-----G--E------EG----------------T-------------G-----------------------------C-------N-----------G--W--------FYV--------EA
> ```

> ```
> ----------V---------------------------V------------------------------E------K----------------K----------T-G----D---------A----------I-----------S--D---------D------E------------------N----------E-----N--------D-----------S----------D-----------------------------T---GE-D-L----------------V--D---------------------
> str39: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V-------------------------N------L-----R-T-----R----T-----------Q-----L-P-------------------------P-------------------------S------Y--TN--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H---------S----------------------------
> str40: ME------------S--------------L---------------------VP-----------------G------------------F-------------------N------E----K------------T-HV----------------Q-----L-------------------S---------L--P---V---------L-------------Q---V----------------------C---------D---V-------------------L---V-------------RG----------F-------------------G-D---S----V-------E----E--------V---L---------------------S---------E---A-----R-----------------------------Q--------H-------L---------------K---DG--T-----------------
> str41: M---N--------------------N----------Q-R----------K----------K-----------------T--------A--------R--------------------PS-------------------F-N--------------------M----L--K-R-------A----------------R----N--R--------------------V--------------S-T------V-------------------------------S--Q---------L--A----K--------RF------------------S---K------------------G--------------L--------------L------S---G------Q--------------G----------P--M-----K--------L--------V-------M--A--------------------F------------
> str42: M-------------S----------N---------------------F---------------D----A-------I-----R----A---------L-----V-D----T----D---A---------Y-------------K-----L------------G------------------------H---I--------------------------H---------M---------Y----------------PE--G----T----E------------------Y----------------------------V-----------L-S-------N-----F---------------T-----D------R---G------------S-------------------R----------I--E-------G---------------------V------T---------H---------T-------------VH--
> str43: M--------------I------E------L--------R-H--------------E-----V---------------Q---G--D------------L-----V------T---I-----------N----------V-------------------V----------E-------------T----------P-E----------------D--------------L--------D------G--------F--------------R-----D--F------------I----------R-------A------------------H-L----------I------CL-A--------------V-D------------------T--------------E-------------T---------------------------------T---G----L-------------------D--------------I-Y----
> str44: M--F------------VF-----------L---------------------V-L-----------L---------------------------P---L-----V--------------S--------S----Q---------C--------------V---M--------P-------L---------F------------N-----L----------------I-T---------------T--N---------------------------------Q-S------Y--TN--SF--------T-----R--------------------GV------------Y---------------Y---------P-------D--K---------V---------F-------R------------S-------------------S----------V--L--H--------------------------------------
> str45: M-------------S----------------K-D---L-------------V----------------A-------------R--------QA----L------------------------------M-----T----------A----------R----M-------K---------A---------D----F--V--------------------------------F--------F----------L-F---------V-------------------L----------------W--K-----A-L--------------------S----------L---------P------------V------P-------------T-R----------C--Q-------------------I-------DM--A--K-------KL-------------S-----A------------G--------------------
> str46: M------A------S--------------L-------L-----------K--------S------L------------T----L-----F----K-R-T--------------------------------R---------------D--
> ```

> ```
> ----Q---------------P----------------------P-------------L-----A---S-G--------------------S--GG------------A---I-----R-------------------------G------------I-------K------------H-----V------I------------I-----------V---L------I--------------------P--G-----D-S---------------S----------------------I-------V------T------R-S-------------R--------------
> str47: M-----------R---V----R----G---I------LR------N---------------------W---------Q-------------Q-------------------W------------------W----I---W-----------T---S----L-G-----------F-----------------------------------W---M---------------F-----------------------M------I----C--------------S----VV-----G----------------------------N------LW--V---------------------------T---V---------Y----------------Y--G--------------V-----P------V---------------W-----K--------E-----------A-------K-------T---------T-------
> str48: M------A--------V-----EP-----------------------F----P---R-------------------------R----------P-------I--------T--------------------R------------P---H----A-S-------I----E-------VD----T-------------------S------------G--------I------------------GG-S----------A-G---------------------S-------------S-------E----------K--V------------------F----------CL----IG-----------------------------------------------Q--A-------E---G---------------G--------------------E------------------P----------N-------T---V---
> str49: M--F---------Y-----AH------A-------------------F--G-------------------G------------------------Y---D--E------N---L------H------------A----F-----P-----------------GI----------------S---------------------S------T---------------V------A------------N-D-V-----------------R------------K-------Y------S---------------------V---------------V----S----V--Y-----------------------N--------K---K--------Y-------------------------N---IV-------------K-----N-K--Y--M------------------W-----------------------------
> str50: M------A-----------------N---------Y-------S-----K--P------F-----L-----------------LD----------------I-V---F-N-----------K--D----------I-------K--------------C----I-------------------N-----D------------SC-------------SH---------------------S------DC------------------RY----------Q-S----------N--S-------------Y-------V-----------------------EL------R------------------------R------------N--------------Q--A-L----------N------------------K-----N--L-----------------------------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 93
> 
> ```


