In [ ]:
```python
import numpy
import didppy
import util
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# DIDP with other bounds

DIDP ソルバーを使用した定式化において dual bound を計算する方法をインスタンス内の任意の 2 つの 文字列の SCS 長の最大値からインスタンス内の任意の 3 つの文字列の SCS 長の最大値に変更してみる.

これによって dual bound 自体はタイトになるものの,
事前計算のオーダーが $n^2 k^2$ から $n^3 k^3$ になり,
小さくないインスタンスに対してはそもそも DIDP による計算を開始できるようになるまでにかなり時間がかかるようになる.
例えば長さが一律で 10 の文字列が 50 個あるようなインスタンスでは 1 分近く事前計算をしたうえで Python カーネルが死んでしまった(`The Python kernel for file ...(略)... died unexpectedly.` と出力されていた)(もしかしたら Marimo の方の問題かもしれない).


小さいインスタンスに対しては確かに dual bound が改善した...
が今まで最適性を証明できていなかったインスタンスに対して最適性を証明できたりしたわけではなかった.
また, primal bound はあまり改善しなかった.

In [ ]:
```python
def boundtable_scs3(s1: str, s2: str, s3: str) -> list[list[list[int]]]:
    len1, len2, len3 = len(s1), len(s2), len(s3)

    # dp[i1][i2][i3]: s1[i1..] と s2[i2..] と s3[i3..] の SCS 長さ
    dp = [
        [
            [
                len1 + len2 + len3 + 1
                for _ in range(len3 + 1)
            ]
            for _ in range(len2 + 1)
        ]
        for _ in range(len1 + 1)
    ]

    for i1 in range(len1 + 1):
        dp[i1][len2][len3] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2][len3] = len2 - i2
    for i3 in range(len3 + 1):
        dp[len1][len2][i3] = len3 - i3

    for i1 in range(len1, -1, -1):
        for i2 in range(len2, -1, -1):
            for i3 in range(len3 , -1, -1):
                if [i1 == len1, i2 == len2, i3 == len3].count(True) >=2:
                    continue

                front_chars = ""
                if i1 < len1:
                    front_chars += s1[i1]
                if i2 < len2:
                    front_chars += s2[i2]
                if i3 < len3:
                    front_chars += s3[i3]
                front_chars = set(front_chars)

                pretransversals = [
                    (
                        i1 + 1 if i1 < len1 and s1[i1] == c else i1,
                        i2 + 1 if i2 < len2 and s2[i2] == c else i2,
                        i3 + 1 if i3 < len3 and s3[i3] == c else i3,
                    )
                    for c in front_chars
                ]
                min_i1, min_i2, min_i3 = pretransversals[0]
                min_length = dp[min_i1][min_i2][min_i3]
                for pre_i1, pre_i2, pre_i3 in pretransversals:
                    if dp[pre_i1][pre_i2][pre_i3] < min_length:
                        min_i1 = pre_i1
                        min_i2 = pre_i2
                        min_i3 = pre_i3
                        min_length = dp[pre_i1][pre_i2][pre_i3]

                dp[i1][i2][i3] = min_length + 1

    return dp
```

In [ ]:
```python
def boundexpr_scs3len(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    exprs = []
    for idx1 in range(len(instance)):
        for idx2 in range(idx1 + 1, len(instance)):
            for idx3 in range(idx2 + 1, len(instance)):
                s1 = instance[idx1]
                s2 = instance[idx2]
                s3 = instance[idx3]
                index_var1 = index_vars[idx1]
                index_var2 = index_vars[idx2]
                index_var3 = index_vars[idx3]
                table_s1s2s3 = dpmodel.add_int_table(boundtable_scs3(s1, s2, s3))
                exprs.append(table_s1s2s3[index_var1, index_var2, index_var3])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound
```

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
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
                    chars.index(c)
                    for c in s
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

        # dual bound
        if True:
            dpmodel.add_dual_bound(boundexpr_scs3len(instance, dpmodel, index_vars))

        self.instance = instance
        self.dpmodel = dpmodel
        self.dpsolver = None
        self.solution = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.dpsolver = didppy.CABS(
            self.dpmodel,
            threads=12,
            time_limit=time_limit,
            quiet=(not log),
        )
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

大きいインスタンスでは正常に動作しないため, 一部のインスタンスに対して実験する.
具体的に, 以下のインスタンスはスキップ.

- `uniform_q05n050k010-010.txt`
- `nucleotide_n050k050.txt`
- `protein_n050k050.txt`

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
>  Sol: utlkcignycosokuevjiahqfozpmplxnhtqgbrddxzxbcvsuqxpvirsvnnsbxgf
> str1: -t-k--gn-----ku-----h-----mp-xnhtqg----xz---v---x--i-s--------
> str2: -----i----o------ji--qfo----l-n----b---x-x-cvsuq-pvi-s---sbx-f
> str3: u-l-ci-nycoso---v------ozp-pl--------------------p------------
> str4: -----ig--------ev--a----z---------gbrdd---bc-s----v-r-vnn---gf
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
> --- Solution (of length 96) ---
>  Sol: rxwiojxiqfopypltkrbdgevanzgbxkruxdlcphmqvgztdpfjztsuivxnybcodhtmsebroqvogxzpbrvxissbhnngplexpwdf
> str1: ---------------tk---g---n----k-u-----hm------p--------xn-----ht------q--gxz---vxis--------------
> str2: ---ioj-iqfo---l---------n--bx---x--c----v---------su-----------------q-----p--v-issb-------x---f
> str3: -------------------------------u--lc----------------i--ny-co----s---o-vo--zp------------pl--p---
> str4: ---i----------------geva-zgb--r--d----------d------------bc-----s-----v------rv------nng-------f
> str5: -----------pypl--r-------z--x--u---cp-mqvg-td-f----uiv----c-d---s-b-o---------------------------
> str6: -----------p------bd-ev----------d-c----v---dpf-z-s------------ms-broqv-----b------bh-----------
> str7: ---------------------e--n--b-------c------z---fj-t---vx----------e-r------z-brv-i------gple-----
> str8: rxw---x-q-------kr-d----------r---lc-------t---------------od-tm-----------p-r----------p--x-wd-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 67
> ```

In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
model_03 = Model(instance_03)
solution_03 = model_03.solve().to_solution()
```

> ```
>
> ```

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
> --- Solution (of length 150) ---
>   Sol: rxwusxipqtyoekgkjnibqfdpklecvazorfzxudilngcbqjhtxprvdmepxqlyecfvewouzsganhtjrdbizuqvhncodftmspbrkevguijokxzspchkqtrugvcnodsbzpxwhlzaibwvdmknghocufeyps
> str01: ---------t---kg--n------k-----------u---------h------m-px---------------nht-------q----------------g-----xz----------v--------x-----i----------------s
> str02: ------i----o----j-i-qf---------o-------ln--b----x-------x----c-v-----s-----------uq----------p----v--i-----s--------------sb--x------------------f----
> str03: ---u---------------------l-c----------i-n------------------y-c----o--s-----------------o----------v----o--z-p----------------p---l------------------p-
> str04: ------i-------g-----------e-vaz----------g-b------r-d------------------------db-------c-----s-----v---------------r--v-n-------------------ng----f----
> str05: -------p--y------------p-l------r-zxu-----c------p---m---q-----v------g---t--d-----------f----------ui---------------vc--dsb------------------o-------
> str06: -------p-----------b--d---e-v--------d----c--------vd--p------f-----zs---------------------ms-br-------o--------q----v-----b---------b-------h--------
> str07: ------------e----n-b-------c--z--f-----------j-t---v----x---e---------------r---z-------------br--v--i--------------g--------p---l----------------e---
> str08: rxw--x--q----k------------------r----d------------r-------l--c------------t------------od-tm-p-r------------p-----------------xw--------d-------------
> str09: -------------k-k----q--------a---f----i--g--qj-------------------wo-----------------------------k-------k--s---k--r--------b-----l----------g---------
> str10: -------------------------l---------x------------xp---------------------a------bi---v----------b---v-------z----k--------o---z-----z----vd-------------
> str11: -------------k------------------r-----i-----------------------f------s-a-----------v-nc-d-----------------------q--------------wh-z------------c------
> str12: --------q--------------------a-----xud---g--q------v-----q---c--ew------------b----------f---------g-ijo-----------------------w------w------------y--
> str13: r---sx--q-------jn---f-p-----a-------di----------------------------u-s---------i--q-----------b--e--------z---hk--------o-------h--------m--g---------
> str14: ------i----------------------------------------------------------w---s---h---------vh-co---m---------i-------------u-v---d--------------dm------------
> str15: ----------------------------------------------htx-------xq-----------------j----z-q-----------b--------------c---t---------b-------a------kn----------
> str16: -x-us----------------f-----c-----fz--------------p----e-----ec-v-w-----an-t--------------f-m-------g------------q-----------z-------------------u-----
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 62
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
>   Sol: bbaeddcbeacdeecbdbceabdcead
> str01: ----d-cb--c---c-dbc----ce--
> str02: b---dd-be---ee-----e-bd----
> str03: ------c--acdeec----e-b--e--
> str04: --aedd-----d----d--e-bd---d
> str05: --a---cbe---e-c-----ab-ce--
> str06: bba----be------bd-c--b---a-
> str07: bbae-----a--e--b----a-d--a-
> str08: ---e----e---eecbdb-e----e--
> str09: ------c---cdee--d---a-dc--d
> str10: b---d----a-----bdb-ea----ad
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 27
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
>   Sol: TACTGACGCGTAATCAGATCGTAC
> str01: -A-TG--G-G-A-T-A---CG---
> str02: -A-T-AC-C-T--TC----C---C
> str03: --C--ACG---AAT----T-G-A-
> str04: TA---A-----AATC---T-GT--
> str05: -A--G--G--TAA-CA-A----A-
> str06: T--T--C-C-TA----G---GTA-
> str07: T--TG-----TA----GATC-T--
> str08: T---G--G-G-AA---G-T--T-C
> str09: T--T--C-C--A--CA-A-C-T--
> str10: T-CT-A-----AA-C-GA----A-
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 24
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
>   Sol: MAPQESKLFTERSYCANQHVFLNDAIFSRPGKVFNGTEYAQLHD
> str01: MA-----L----SYC--------------P-K---GT-------
> str02: M--Q-S------S--------LN-AI---P--V-----------
> str03: M-P----L----SY---QH-F-------R--K------------
> str04: M---E-----E-------HV--N--------------E---LHD
> str05: M----S----------N---F--DAI--R----------A-L--
> str06: M-------F--R----NQ----N----SR-----NG--------
> str07: M-------F----Y-A--H-----A-F---G----G--Y-----
> str08: M----SK-FT-R----------------RP--------Y-Q---
> str09: M----S--F----------V----A-----G-V---T--AQ---
> str10: M---ES-L-----------V---------PG--FN--E------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 34
> ```

In [ ]:
```python
_instance = [
    "aehdmmqrstuwv",
    "afiknllppaavxusqszab",
    "bgglopqsssv",
    "cabhiknaampawqryssuv",
    "dbhciknddmpdqryssuwc",
    "cajhiknapasqrssuvv",
    "dacngoaiatsimawxltsc",
    "zbndjkozfrizsyctviw",
]
_model = Model(_instance)
_solution = _model.solve(time_limit=600).to_solution()

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"best bound: {_model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```
