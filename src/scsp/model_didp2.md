In [ ]:
```python
import didppy
import util
import model_didp
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
def create_model(instance: list[str]) -> model_didp.Model:
    return model_didp.Model(instance, extra_bounds=[boundexpr_scs3len], disable_default_bound=True)
```

In [ ]:
```python
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    model = create_model(instance)
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
model_01 = create_model(instance_01)
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
>  Sol: ultcikgnycosjkuiqhoevmafozpxplnhtqgbrddxbxzcvsxuqpvirvsnnsbgxf
> str1: --t--kgn-----ku--h---m----px--nhtqg----x--z-v-x----i--s-------
> str2: ----i-----o-j--iq------fo----ln----b---x-x-cvs-uqpvi--s--sb-xf
> str3: ul-ci--nycos------o-v---ozp-pl-------------------p------------
> str4: ----i-g------------ev-a--z--------gbrdd-b--c-s----v-rv-nn--g-f
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 62
> ```

In [ ]:
```python
instance_02 = util.parse("uniform_q26n008k015-025.txt")
model_02 = create_model(instance_02)
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
>  Sol: iorjtipxwxypqkfolrbgdevazngbxkurlxdchpmqvgztdpfzsjutivbxnycodhtmsberoqvgoxzpbrvxissnngpbxlhfwpde
> str1: ----t--------k-----g-----n---ku-----h-m------p---------xn----ht------q-g-xz---vxis--------------
> str2: io-j-i------q-fol--------n-bx----x-c----v-------s-u------------------q-----p--v-iss----bx--f----
> str3: ------------------------------u-l--c----------------i---nyco----s---o-v-o-zp----------p--l---p--
> str4: i------------------g-evaz-gb---r--d---------d---------b---c-----s-----v------rv----nng-----f----
> str5: ------p---yp----lr------z---x-u----c-pmqvg-td-f---u-iv----c-d---sb--o---------------------------
> str6: ------p-----------b-dev-----------dc----v---dpfzs--------------msb-roqv-----b----------b--h-----
> str7: ---------------------e---n-b-------c------z---f--j-t-v-x----------er------z-brv-i----gp--l-----e
> str8: --r----xwx--qk---r--d----------rl--c-------t---------------od-tm-----------p-r--------p-x---w-d-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 67
> ```

In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
model_03 = create_model(instance_03)
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
> --- Solution (of length 151) ---
>   Sol: rxiwusxptypokqjgenkiqbdflcevarzoxflxupjadzhcgpiqnbrmtvdxpxgqlfeyecujvzsinhgewtoaudqrzvbenmcktsofmpbuvzkrgdijhsoqxzuvwcdskpxirgobnpabhznlvkwdmsgxfnycoep
> str01: --------t---k--g-nk-----------------u-----h--------m----px--------------nh---t----q---------------------g-------xz-v------xi-----------------s---------
> str02: --i--------o--j----iq--f-------o--l-------------nb-----x-x-------c--v-s---------u-q--------------p--v-----i--s---------s-------b---------------xf------
> str03: ----u-------------------lc--------------------i-n--------------y-c------------o--------------so-----v---------o--z-------p-------p-----l--------------p
> str04: --i------------ge----------va-z-------------g----br---d--------------------------d----b---c--s------v--r-----------v------------n-----n-------g-f------
> str05: -------p-yp-------------l----rz-x---u------c-p-----m-------q--------v-----g--t---d-------------f---u------i--------v-cds-------b--------------------o--
> str06: -------p-------------bd---ev------------d--c---------vd-p----f-------zs------------------m---s----b----r------oq---v-----------b---bh------------------
> str07: ----------------en---b---c----z--f----j-------------tv-x------e--------------------rz-b----------------r-----------v-------i-g---p-----l-------------e-
> str08: rx-w--x------q----k----------r----------d---------r---------l----c-----------to--d----------t---mp-----r-----------------px---------------wd-----------
> str09: ------------k-----k-q-------a----f------------i-----------gq-------j--------w-o------------k----------k------s----------k---r--b-------l------g--------
> str10: ------------------------l-------x--x-p-a---------b---------------------i-------------vb-------------vzk-------o--z-------------------z--v--d-----------
> str11: ------------k----------------r----------------i--------------f--------s--------a-----v--n-c--------------d-----q----w---------------hz-------------c---
> str12: -------------q--------------a---x---u---d---g--q-----v-----q-----c---------ew---------b--------f--------g-ij--o-----w---------------------w-------y----
> str13: r----sx------qj--n-----f-------------p-ad-----i-------------------u---si----------q---be-------------z------h-----------k-----o-----h-------m-g--------
> str14: --iw-s------------------------------------h----------v-------------------h----------------c---o-m---------i-------uv--d--------------------dm----------
> str15: ------------------------------------------h---------t--x-x-q-------j-z------------q---b---c-t-----b-------------------------------a------k-------n-----
> str16: -x--us-----------------f-c-------f-------z---p----------------e-ec--v-------w--a--------n---t--fm-------g------q-zu------------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 62
> ```

In [ ]:
```python
instance_04 = util.parse("uniform_q05n010k010-010.txt")
model_04 = create_model(instance_04)
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
>   Sol: bbaeddcbacdeeecbdbceabdcead
> str01: ----d-cb-c----c-dbc----ce--
> str02: b---dd-b---eee-----e-bd----
> str03: ------c-acdee-c----e-b--e--
> str04: --aedd----d-----d--e-bd---d
> str05: --a---cb---ee-c-----ab-ce--
> str06: bba----b---e---bd-c--b---a-
> str07: bbae----a--e---b----a-d--a-
> str08: ---e-------eeecbdb-e----e--
> str09: ------c--cdee---d---a-dc--d
> str10: b---d---a------bdb-ea----ad
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 27
> ```

In [ ]:
```python
instance_06 = util.parse("nucleotide_n010k010.txt")
model_06 = create_model(instance_06)
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
model_08 = create_model(instance_08)
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
>   Sol: MQESNKFDAPETRLSNYQAHVLNASICFRPGKVFNEGTALHDYQ
> str01: M-------A----LS-Y---------C--P-K----GT------
> str02: MQ-S----------S------LNA-I---P--V-----------
> str03: M--------P---LS-YQ-H-------FR--K------------
> str04: M-E-------E--------HV-N------------E---LHD--
> str05: M--SN-FDA----------------I--R---------AL----
> str06: M-----F-----R--N-Q----N-S---R-----N-G-------
> str07: M-----F---------Y-AH---A---F--G-----G-----Y-
> str08: M--S-KF----TR---------------RP------------YQ
> str09: M--S--F-------------V--A------G-V----TA----Q
> str10: M-ES---------L------V--------PG--FNE--------
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 34
> ```
