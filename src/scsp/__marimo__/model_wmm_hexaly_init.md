In [ ]:
```python
import model_wmm_hexaly
import util
```


In [ ]:
```python
import marimo as mo
import nbformat
```


# Hexaly を用いたヒューリスティックに初期重みを追加

`WMM_HEXALY` モデルにおいて重み決定変数の初期値を `WMM` と等しくなるように設定する.

巨大なインスタンスにおいて常に `WMM` 以上の質の解が出る反面, 小さ目のインスタンスでは `WMM_HEXALY` と比較して悪化することがある.

In [ ]:
```python
def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str:
    return (
        model_wmm_hexaly.Model(instance, initial=True)
        .solve(time_limit, log)
        .to_solution()
    )
```


In [ ]:
```python
instance_01 = util.parse("uniform_q26n004k015-025.txt")
solution_01 = solve(instance_01, log=True)
```


> ```
> 
> Model:  expressions = 88, decisions = 84, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:           75
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,     458 itr]:           67
> 
> ```

> ```
> [  2 sec,     909 itr]:           65
> 
> ```

> ```
> [  3 sec,    1343 itr]:           65
> 
> ```

> ```
> [  4 sec,    1839 itr]:           65
> 
> ```

> ```
> [  5 sec,    2374 itr]:           65
> 
> ```

> ```
> [  6 sec,    3127 itr]:           65
> 
> ```

> ```
> [  7 sec,    3837 itr]:           65
> 
> ```

> ```
> [  8 sec,    4581 itr]:           64
> 
> ```

> ```
> [  9 sec,    5327 itr]:           64
> 
> ```

> ```
> [ 10 sec,    6029 itr]:           64
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,    6790 itr]:           64
> 
> ```

> ```
> [ 12 sec,    7490 itr]:           64
> 
> ```

> ```
> [ 13 sec,    8198 itr]:           64
> 
> ```

> ```
> [ 14 sec,    8921 itr]:           64
> 
> ```

> ```
> [ 15 sec,    9649 itr]:           64
> 
> ```

> ```
> [ 16 sec,   10421 itr]:           64
> 
> ```

> ```
> [ 17 sec,   11180 itr]:           64
> 
> ```

> ```
> [ 18 sec,   11916 itr]:           64
> 
> ```

> ```
> [ 19 sec,   12675 itr]:           64
> 
> ```

> ```
> [ 20 sec,   13401 itr]:           64
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,   14143 itr]:           64
> 
> ```

> ```
> [ 22 sec,   14892 itr]:           64
> 
> ```

> ```
> [ 23 sec,   15660 itr]:           64
> 
> ```

> ```
> [ 24 sec,   16411 itr]:           64
> 
> ```

> ```
> [ 25 sec,   17082 itr]:           64
> 
> ```

> ```
> [ 26 sec,   17821 itr]:           64
> 
> ```

> ```
> [ 27 sec,   18542 itr]:           64
> 
> ```

> ```
> [ 28 sec,   19303 itr]:           64
> 
> ```

> ```
> [ 29 sec,   20010 itr]:           64
> 
> ```

> ```
> [ 30 sec,   20734 itr]:           64
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,   21450 itr]:           64
> 
> ```

> ```
> [ 32 sec,   22148 itr]:           64
> 
> ```

> ```
> [ 33 sec,   22883 itr]:           64
> 
> ```

> ```
> [ 34 sec,   23634 itr]:           64
> 
> ```

> ```
> [ 35 sec,   24386 itr]:           64
> 
> ```

> ```
> [ 36 sec,   25125 itr]:           64
> 
> ```

> ```
> [ 37 sec,   25885 itr]:           64
> 
> ```

> ```
> [ 38 sec,   26617 itr]:           64
> 
> ```

> ```
> [ 39 sec,   27370 itr]:           64
> 
> ```

> ```
> [ 40 sec,   28163 itr]:           64
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,   28886 itr]:           64
> 
> ```

> ```
> [ 42 sec,   29647 itr]:           64
> 
> ```

> ```
> [ 43 sec,   30405 itr]:           64
> 
> ```

> ```
> [ 44 sec,   31144 itr]:           64
> 
> ```

> ```
> [ 45 sec,   31929 itr]:           64
> 
> ```

> ```
> [ 46 sec,   32725 itr]:           64
> 
> ```

> ```
> [ 47 sec,   33492 itr]:           64
> 
> ```

> ```
> [ 48 sec,   34294 itr]:           64
> 
> ```

> ```
> [ 49 sec,   35074 itr]:           64
> 
> ```

> ```
> [ 50 sec,   35805 itr]:           64
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,   36536 itr]:           64
> 
> ```

> ```
> [ 52 sec,   37289 itr]:           64
> 
> ```

> ```
> [ 53 sec,   38045 itr]:           64
> 
> ```

> ```
> [ 54 sec,   38790 itr]:           64
> 
> ```

> ```
> [ 55 sec,   39530 itr]:           64
> 
> ```

> ```
> [ 56 sec,   40270 itr]:           64
> 
> ```

> ```
> [ 57 sec,   41026 itr]:           64
> 
> ```

> ```
> [ 58 sec,   41796 itr]:           64
> 
> ```

> ```
> [ 59 sec,   42592 itr]:           64
> 
> ```

> ```
> [ 60 sec,   43381 itr]:           64
> [ optimality gap     ]:      100.00%
> [ 60 sec,   43381 itr]:           64
> [ optimality gap     ]:      100.00%
> 
> 43381 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           64
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_01
_solution = solution_01

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 64) ---
>  Sol: iojtkgnkulcihmpxenyhtqvazgxbrddbcosovrfozpplvnnbxxcvsuqpvissbgxf
> str1: ---tkgnku---hmpx-n-htq---gx-------------z---v---x--------is-----
> str2: ioj--------i---------q----------------fo---l-n-bxxcvsuqpvissb-xf
> str3: --------ulci-----ny-------------cosov--ozppl-----------p--------
> str4: i----g----------e-----vazg-brddbc-s-vr------vnn--------------g-f
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_02 = util.parse("uniform_q26n008k015-025.txt")
solution_02 = solve(instance_02, log=True)
```


> ```
> 
> Model:  expressions = 179, decisions = 175, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:          128
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,       6 itr]:          124
> 
> ```

> ```
> [  2 sec,     238 itr]:          115
> 
> ```

> ```
> [  3 sec,     529 itr]:          113
> 
> ```

> ```
> [  4 sec,     804 itr]:          109
> 
> ```

> ```
> [  5 sec,    1101 itr]:          108
> 
> ```

> ```
> [  6 sec,    1377 itr]:          106
> 
> ```

> ```
> [  7 sec,    1680 itr]:          106
> 
> ```

> ```
> [  8 sec,    1993 itr]:          106
> 
> ```

> ```
> [  9 sec,    2298 itr]:          106
> 
> ```

> ```
> [ 10 sec,    2610 itr]:          106
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,    2924 itr]:          106
> 
> ```

> ```
> [ 12 sec,    3217 itr]:          106
> 
> ```

> ```
> [ 13 sec,    3531 itr]:          106
> 
> ```

> ```
> [ 14 sec,    3851 itr]:          106
> 
> ```

> ```
> [ 15 sec,    4170 itr]:          106
> 
> ```

> ```
> [ 16 sec,    4488 itr]:          106
> 
> ```

> ```
> [ 17 sec,    4805 itr]:          106
> 
> ```

> ```
> [ 18 sec,    5108 itr]:          106
> 
> ```

> ```
> [ 19 sec,    5409 itr]:          105
> 
> ```

> ```
> [ 20 sec,    5718 itr]:          105
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,    6048 itr]:          105
> 
> ```

> ```
> [ 22 sec,    6343 itr]:          105
> 
> ```

> ```
> [ 23 sec,    6647 itr]:          105
> 
> ```

> ```
> [ 24 sec,    6966 itr]:          105
> 
> ```

> ```
> [ 25 sec,    7261 itr]:          105
> 
> ```

> ```
> [ 26 sec,    7572 itr]:          105
> 
> ```

> ```
> [ 27 sec,    7880 itr]:          105
> 
> ```

> ```
> [ 28 sec,    8212 itr]:          105
> 
> ```

> ```
> [ 29 sec,    8533 itr]:          105
> 
> ```

> ```
> [ 30 sec,    8858 itr]:          105
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,    9167 itr]:          105
> 
> ```

> ```
> [ 32 sec,    9483 itr]:          105
> 
> ```

> ```
> [ 33 sec,    9814 itr]:          105
> 
> ```

> ```
> [ 34 sec,   10137 itr]:          105
> 
> ```

> ```
> [ 35 sec,   10451 itr]:          105
> 
> ```

> ```
> [ 36 sec,   10759 itr]:          105
> 
> ```

> ```
> [ 37 sec,   11079 itr]:          105
> 
> ```

> ```
> [ 38 sec,   11387 itr]:          105
> 
> ```

> ```
> [ 39 sec,   11697 itr]:          105
> 
> ```

> ```
> [ 40 sec,   12033 itr]:          105
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,   12337 itr]:          105
> 
> ```

> ```
> [ 42 sec,   12640 itr]:          105
> 
> ```

> ```
> [ 43 sec,   12957 itr]:          105
> 
> ```

> ```
> [ 44 sec,   13269 itr]:          105
> 
> ```

> ```
> [ 45 sec,   13563 itr]:          105
> 
> ```

> ```
> [ 46 sec,   13887 itr]:          105
> 
> ```

> ```
> [ 47 sec,   14186 itr]:          105
> 
> ```

> ```
> [ 48 sec,   14496 itr]:          105
> 
> ```

> ```
> [ 49 sec,   14798 itr]:          105
> 
> ```

> ```
> [ 50 sec,   15130 itr]:          105
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,   15416 itr]:          105
> 
> ```

> ```
> [ 52 sec,   15724 itr]:          105
> 
> ```

> ```
> [ 53 sec,   16010 itr]:          105
> 
> ```

> ```
> [ 54 sec,   16317 itr]:          105
> 
> ```

> ```
> [ 55 sec,   16603 itr]:          105
> 
> ```

> ```
> [ 56 sec,   16882 itr]:          105
> 
> ```

> ```
> [ 57 sec,   17170 itr]:          105
> 
> ```

> ```
> [ 58 sec,   17482 itr]:          105
> 
> ```

> ```
> [ 59 sec,   17796 itr]:          105
> 
> ```

> ```
> [ 60 sec,   18097 itr]:          105
> [ optimality gap     ]:      100.00%
> [ 60 sec,   18097 itr]:          105
> [ optimality gap     ]:      100.00%
> 
> 18097 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          105
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_02
_solution = solution_02

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 105) ---
>  Sol: pietokgnbdcevayplrzxwxqkrudchvdpmqfjtvgpxebrlcitdonhdbtqfuycosovozslnmpsbrvinngxzvplxwcdvsuboqpvissbxbhef
> str1: ---t-kgn---------------k-u--h---m------px---------nh--tq----------------------gxzv--x-----------is-------
> str2: -i--o------------------------------j----------i--------qf---o------ln---b------x----x-c-vsu--qpvissbx---f
> str3: -------------------------u------------------lci---n-------ycosovoz----p-----------pl----------p----------
> str4: -i----g----eva----z-------------------g---br----d---db-----c-s-v---------rv-nng-------------------------f
> str5: p-------------yplrzx-----u-c---pmq---vg--------td-------fu-----------------i-----v----cd-s-bo------------
> str6: p-------bd-ev-------------dc-vdp--f------------------------------zs--m-sbr------------------oq-
> ```

> ```
> v---b-bh--
> str7: --e----nb-c-------z---------------fjtv--xe-r---------------------z------brvi--g---pl-------------------e-
> str8: -----------------r-xwxqkr-d----------------rlc-t-o--d-t--------------mp--r--------p-xw-d-----------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
solution_03 = solve(instance_03, log=True)
```


> ```
> 
> Model:  expressions = 327, decisions = 323, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:          176
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,      54 itr]:          163
> 
> ```

> ```
> [  2 sec,     180 itr]:          161
> 
> ```

> ```
> [  3 sec,     319 itr]:          160
> 
> ```

> ```
> [  4 sec,     476 itr]:          160
> 
> ```

> ```
> [  5 sec,     609 itr]:          159
> 
> ```

> ```
> [  6 sec,     750 itr]:          159
> 
> ```

> ```
> [  7 sec,     886 itr]:          158
> 
> ```

> ```
> [  8 sec,    1026 itr]:          158
> 
> ```

> ```
> [  9 sec,    1158 itr]:          157
> 
> ```

> ```
> [ 10 sec,    1302 itr]:          157
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,    1437 itr]:          157
> 
> ```

> ```
> [ 12 sec,    1593 itr]:          157
> 
> ```

> ```
> [ 13 sec,    1747 itr]:          157
> 
> ```

> ```
> [ 14 sec,    1896 itr]:          157
> 
> ```

> ```
> [ 15 sec,    2031 itr]:          155
> 
> ```

> ```
> [ 16 sec,    2163 itr]:          155
> 
> ```

> ```
> [ 17 sec,    2300 itr]:          155
> 
> ```

> ```
> [ 18 sec,    2437 itr]:          155
> 
> ```

> ```
> [ 19 sec,    2584 itr]:          155
> 
> ```

> ```
> [ 20 sec,    2727 itr]:          155
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,    2868 itr]:          155
> 
> ```

> ```
> [ 22 sec,    2998 itr]:          155
> 
> ```

> ```
> [ 23 sec,    3129 itr]:          154
> 
> ```

> ```
> [ 24 sec,    3286 itr]:          154
> 
> ```

> ```
> [ 25 sec,    3444 itr]:          154
> 
> ```

> ```
> [ 26 sec,    3580 itr]:          153
> 
> ```

> ```
> [ 27 sec,    3739 itr]:          153
> 
> ```

> ```
> [ 28 sec,    3872 itr]:          153
> 
> ```

> ```
> [ 29 sec,    4023 itr]:          153
> 
> ```

> ```
> [ 30 sec,    4174 itr]:          153
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,    4331 itr]:          153
> 
> ```

> ```
> [ 32 sec,    4477 itr]:          152
> 
> ```

> ```
> [ 33 sec,    4636 itr]:          152
> 
> ```

> ```
> [ 34 sec,    4791 itr]:          152
> 
> ```

> ```
> [ 35 sec,    4931 itr]:          152
> 
> ```

> ```
> [ 36 sec,    5063 itr]:          151
> 
> ```

> ```
> [ 37 sec,    5201 itr]:          151
> 
> ```

> ```
> [ 38 sec,    5349 itr]:          151
> 
> ```

> ```
> [ 39 sec,    5493 itr]:          151
> 
> ```

> ```
> [ 40 sec,    5654 itr]:          151
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,    5787 itr]:          151
> 
> ```

> ```
> [ 42 sec,    5939 itr]:          150
> 
> ```

> ```
> [ 43 sec,    6102 itr]:          150
> 
> ```

> ```
> [ 44 sec,    6250 itr]:          150
> 
> ```

> ```
> [ 45 sec,    6395 itr]:          150
> 
> ```

> ```
> [ 46 sec,    6553 itr]:          150
> 
> ```

> ```
> [ 47 sec,    6683 itr]:          150
> 
> ```

> ```
> [ 48 sec,    6837 itr]:          150
> 
> ```

> ```
> [ 49 sec,    6993 itr]:          150
> 
> ```

> ```
> [ 50 sec,    7140 itr]:          150
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,    7288 itr]:          150
> 
> ```

> ```
> [ 52 sec,    7429 itr]:          150
> 
> ```

> ```
> [ 53 sec,    7583 itr]:          150
> 
> ```

> ```
> [ 54 sec,    7737 itr]:          150
> 
> ```

> ```
> [ 55 sec,    7899 itr]:          150
> 
> ```

> ```
> [ 56 sec,    8066 itr]:          150
> 
> ```

> ```
> [ 57 sec,    8219 itr]:          150
> 
> ```

> ```
> [ 58 sec,    8371 itr]:          150
> 
> ```

> ```
> [ 59 sec,    8531 itr]:          150
> 
> ```

> ```
> [ 60 sec,    8686 itr]:          150
> [ optimality gap     ]:      100.00%
> [ 60 sec,    8686 itr]:          150
> [ optimality gap     ]:      100.00%
> 
> 8686 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          150
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_03
_solution = solution_03

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
>   Sol: irpkxwsxqkhtojgenbvyplrdiqfaxxusfczpafdigbrqjzdevdolncitvbxucspevrkgnkuhmqcewbodpfxcvgtzksnmiuycosbroqpvdfwauibezhkntskrjoqgxzvppxwcdisblhxfmgeqopzuwy
> str01: -----------t------------------------------------------------------kgnkuhm-------p-x-------n----------------------h--t-----qgxzv--x---is---------------
> str02: i-----------oj----------iqf-----------------------oln----bx-----------------------xcv----s---u-------qpv-----i-------s----------------sb--xf----------
> str03: ------------------------------u--------------------l-ci-------------n-------------------------ycos--o--v-----------------o---z-pp-------l--------p----
> str04: i-------------ge--v--------a------z-----gbr---d--d-------b--cs--vr------------------v-----n------------------------n-------g---------------f----------
> str05: --p----------------yplr-----------z-----------------------xuc-p---------mq----------vgt-----------------df--ui----------------v----cd-sb--------o-----
> str06: --p--------------b-----d-----------------------evd---c--v----------------------dpf-----z-s-m-----sbroq-v------b------------------------b-h------------
> str07: ---------------enb---------------cz--f------j----------tv-x----e-r---------------------z----------br---v-----i-------------g---p--------l-----e-------
> str08: -r--xw-xqk------------rd------------------r--------l-c-t----------------------od------t----m----------p----------------r-------p-xw-d-----------------
> str09: ---k-----k---------------q-a----f------ig--qj-------------------------------w-o---------k-------------------------k--skr---------------bl----g--------
> str10: ---------------------l------xx-----pa----b------------i-vb------v----------------------zk-------o---------------z------------zv-----d-----------------
> str11: ---k------------------r-i-f----s----a-----------v---nc-------------------------d---------------------q----w------h-----------z-----c------------------
> str12: --------q------------------ax-u-------d-g--q----v------------------------qcewb---f---g------i---------------------------jo--------w-----------------wy
> str13: -r----sxq----j--n---------f--------pa-di-------------------u-s------------------------------i--------q--------bezhk------o---------------h--mg--------
> str14: i----ws---h-------v----------------------------------------------------h--c---o------------miu---------vd---------------------------d-------m---------
> str15: ----------ht----------------xx-------------qjz---------------------------q---b-----c--t-----------b--------a------kn----------------------------------
> str16: ----x-------------------------usfc---f-------z----------------pe-----------e-------cv---------------------wa-------nt----------------------fmg-q--zu--
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_04 = util.parse("uniform_q05n010k010-010.txt")
solution_04 = solve(instance_04, log=True)
```


> ```
> 
> Model:  expressions = 104, decisions = 100, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:           32
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,    1259 itr]:           29
> 
> ```

> ```
> [  2 sec,    4447 itr]:           29
> 
> ```

> ```
> [  3 sec,    7469 itr]:           29
> 
> ```

> ```
> [  4 sec,   10499 itr]:           29
> 
> ```

> ```
> [  5 sec,   13648 itr]:           29
> 
> ```

> ```
> [  6 sec,   16703 itr]:           28
> 
> ```

> ```
> [  7 sec,   19761 itr]:           28
> 
> ```

> ```
> [  8 sec,   22854 itr]:           28
> 
> ```

> ```
> [  9 sec,   25843 itr]:           28
> 
> ```

> ```
> [ 10 sec,   28873 itr]:           28
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,   31920 itr]:           28
> 
> ```

> ```
> [ 12 sec,   34964 itr]:           28
> 
> ```

> ```
> [ 13 sec,   38035 itr]:           28
> 
> ```

> ```
> [ 14 sec,   41059 itr]:           28
> 
> ```

> ```
> [ 15 sec,   43988 itr]:           28
> 
> ```

> ```
> [ 16 sec,   46789 itr]:           28
> 
> ```

> ```
> [ 17 sec,   49583 itr]:           28
> 
> ```

> ```
> [ 18 sec,   52634 itr]:           28
> 
> ```

> ```
> [ 19 sec,   55712 itr]:           28
> 
> ```

> ```
> [ 20 sec,   58768 itr]:           28
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,   61764 itr]:           28
> 
> ```

> ```
> [ 22 sec,   64851 itr]:           28
> 
> ```

> ```
> [ 23 sec,   67797 itr]:           28
> 
> ```

> ```
> [ 24 sec,   70896 itr]:           28
> 
> ```

> ```
> [ 25 sec,   73947 itr]:           28
> 
> ```

> ```
> [ 26 sec,   76895 itr]:           28
> 
> ```

> ```
> [ 27 sec,   79962 itr]:           28
> 
> ```

> ```
> [ 28 sec,   82970 itr]:           28
> 
> ```

> ```
> [ 29 sec,   85960 itr]:           28
> 
> ```

> ```
> [ 30 sec,   89061 itr]:           28
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,   92079 itr]:           28
> 
> ```

> ```
> [ 32 sec,   95115 itr]:           28
> 
> ```

> ```
> [ 33 sec,   98109 itr]:           28
> 
> ```

> ```
> [ 34 sec,  101119 itr]:           28
> 
> ```

> ```
> [ 35 sec,  104141 itr]:           28
> 
> ```

> ```
> [ 36 sec,  107196 itr]:           28
> 
> ```

> ```
> [ 37 sec,  110218 itr]:           28
> 
> ```

> ```
> [ 38 sec,  113234 itr]:           28
> 
> ```

> ```
> [ 39 sec,  116342 itr]:           28
> 
> ```

> ```
> [ 40 sec,  119451 itr]:           27
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,  122540 itr]:           27
> 
> ```

> ```
> [ 42 sec,  125704 itr]:           27
> 
> ```

> ```
> [ 43 sec,  128847 itr]:           27
> 
> ```

> ```
> [ 44 sec,  131923 itr]:           27
> 
> ```

> ```
> [ 45 sec,  135175 itr]:           27
> 
> ```

> ```
> [ 46 sec,  138420 itr]:           27
> 
> ```

> ```
> [ 47 sec,  141582 itr]:           27
> 
> ```

> ```
> [ 48 sec,  144778 itr]:           27
> 
> ```

> ```
> [ 49 sec,  148041 itr]:           27
> 
> ```

> ```
> [ 50 sec,  151261 itr]:           27
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,  154478 itr]:           27
> 
> ```

> ```
> [ 52 sec,  157687 itr]:           27
> 
> ```

> ```
> [ 53 sec,  160866 itr]:           27
> 
> ```

> ```
> [ 54 sec,  164087 itr]:           27
> 
> ```

> ```
> [ 55 sec,  167284 itr]:           27
> 
> ```

> ```
> [ 56 sec,  170479 itr]:           27
> 
> ```

> ```
> [ 57 sec,  173679 itr]:           27
> 
> ```

> ```
> [ 58 sec,  176908 itr]:           27
> 
> ```

> ```
> [ 59 sec,  180094 itr]:           27
> 
> ```

> ```
> [ 60 sec,  183283 itr]:           27
> [ optimality gap     ]:      100.00%
> [ 60 sec,  183283 itr]:           27
> [ optimality gap     ]:      100.00%
> 
> 183283 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           27
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_04
_solution = solution_04

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
>   Sol: bbaedcdbeacdeecbdbeacbdacde
> str01: ----dc-b--c---c-db--c---c-e
> str02: b---d-dbe---ee----e--bd----
> str03: -----c---acdeec---e--b----e
> str04: --aed-d----d----d-e--bd--d-
> str05: --a--c-be---e-c----a-b--c-e
> str06: bba----be------bd---cb-a---
> str07: bbae-----a--e--b---a--da---
> str08: ---e----e---eecbdbe-------e
> str09: -----c----cdee--d--a--d-cd-
> str10: b---d----a-----bdbea---a-d-
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_05 = util.parse("uniform_q05n050k010-010.txt")
solution_05 = solve(instance_05, log=True)
```


> ```
> 
> Model:  expressions = 504, decisions = 500, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:           37
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,      41 itr]:           35
> 
> ```

> ```
> [  2 sec,     761 itr]:           35
> 
> ```

> ```
> [  3 sec,    1298 itr]:           35
> 
> ```

> ```
> [  4 sec,    1716 itr]:           35
> 
> ```

> ```
> [  5 sec,    2203 itr]:           35
> 
> ```

> ```
> [  6 sec,    2673 itr]:           35
> 
> ```

> ```
> [  7 sec,    3258 itr]:           34
> 
> ```

> ```
> [  8 sec,    3896 itr]:           34
> 
> ```

> ```
> [  9 sec,    4504 itr]:           34
> 
> ```

> ```
> [ 10 sec,    5089 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,    5737 itr]:           34
> 
> ```

> ```
> [ 12 sec,    6403 itr]:           34
> 
> ```

> ```
> [ 13 sec,    7074 itr]:           34
> 
> ```

> ```
> [ 14 sec,    7768 itr]:           34
> 
> ```

> ```
> [ 15 sec,    8340 itr]:           34
> 
> ```

> ```
> [ 16 sec,    8860 itr]:           34
> 
> ```

> ```
> [ 17 sec,    9402 itr]:           34
> 
> ```

> ```
> [ 18 sec,   10047 itr]:           34
> 
> ```

> ```
> [ 19 sec,   10626 itr]:           34
> 
> ```

> ```
> [ 20 sec,   11250 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,   11840 itr]:           34
> 
> ```

> ```
> [ 22 sec,   12437 itr]:           34
> 
> ```

> ```
> [ 23 sec,   13051 itr]:           34
> 
> ```

> ```
> [ 24 sec,   13672 itr]:           34
> 
> ```

> ```
> [ 25 sec,   14237 itr]:           34
> 
> ```

> ```
> [ 26 sec,   14839 itr]:           34
> 
> ```

> ```
> [ 27 sec,   15478 itr]:           34
> 
> ```

> ```
> [ 28 sec,   16047 itr]:           34
> 
> ```

> ```
> [ 29 sec,   16650 itr]:           34
> 
> ```

> ```
> [ 30 sec,   17213 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,   17797 itr]:           34
> 
> ```

> ```
> [ 32 sec,   18399 itr]:           34
> 
> ```

> ```
> [ 33 sec,   18976 itr]:           34
> 
> ```

> ```
> [ 34 sec,   19541 itr]:           34
> 
> ```

> ```
> [ 35 sec,   20185 itr]:           34
> 
> ```

> ```
> [ 36 sec,   20719 itr]:           34
> 
> ```

> ```
> [ 37 sec,   21319 itr]:           34
> 
> ```

> ```
> [ 38 sec,   21877 itr]:           34
> 
> ```

> ```
> [ 39 sec,   22498 itr]:           34
> 
> ```

> ```
> [ 40 sec,   23064 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,   23655 itr]:           34
> 
> ```

> ```
> [ 42 sec,   24205 itr]:           34
> 
> ```

> ```
> [ 43 sec,   24798 itr]:           34
> 
> ```

> ```
> [ 44 sec,   25435 itr]:           34
> 
> ```

> ```
> [ 45 sec,   25995 itr]:           34
> 
> ```

> ```
> [ 46 sec,   26589 itr]:           34
> 
> ```

> ```
> [ 47 sec,   27138 itr]:           34
> 
> ```

> ```
> [ 48 sec,   27730 itr]:           34
> 
> ```

> ```
> [ 49 sec,   28293 itr]:           34
> 
> ```

> ```
> [ 50 sec,   28867 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,   29496 itr]:           34
> 
> ```

> ```
> [ 52 sec,   30075 itr]:           34
> 
> ```

> ```
> [ 53 sec,   30670 itr]:           34
> 
> ```

> ```
> [ 54 sec,   31266 itr]:           34
> 
> ```

> ```
> [ 55 sec,   31855 itr]:           34
> 
> ```

> ```
> [ 56 sec,   32440 itr]:           34
> 
> ```

> ```
> [ 57 sec,   33093 itr]:           34
> 
> ```

> ```
> [ 58 sec,   33657 itr]:           34
> 
> ```

> ```
> [ 59 sec,   34212 itr]:           34
> 
> ```

> ```
> [ 60 sec,   34842 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 60 sec,   34842 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> 34842 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           34
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_05
_solution = solution_05

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
>   Sol: dacebdaecdbaecdbecabdebacedabacdeb
> str01: d-c-b---c----cdb-c------ce--------
> str02: ----bd---db-e---e----e---e--b--d--
> str03: --c---a-cd--e---ec---eb--e--------
> str04: -a-e-d---d----d-----deb---d----d--
> str05: -ac-b--e----ec----ab----ce--------
> str06: ----b-----ba---be
> ```

> ```
> --bd---c---ba----
> str07: ----b-----bae-----a--eba--da------
> str08: ---e---e----e---ec-bd-b--e------e-
> str09: --c-----cd--e---e---d--a--d---cd--
> str10: ----bda---b---dbe-a----a--d-------
> str11: ---e-d-e-d-a------a----a-e-a-a----
> str12: -a----ae---a------ab-e---e-a--c---
> str13: ---e--a----a---b-ca-----c-----cd-b
> str14: ----bd-e----e-----a-de-a--d-----e-
> str15: --c---ae-d-a--d-e----e---ed-------
> str16: ---eb---c--a--db--ab--b--e--------
> str17: d----d--c---e---e-abde-a----------
> str18: da--b---cd----d-e-a--e--c---------
> str19: -a----a--d---c--e----e----da-a---b
> str20: -a-e---ec----c--e----e---e-a-a----
> str21: ----b-----b---d---a--e--c--a-a-de-
> str22: dace-dae-d-a---b------------------
> str23: -a----ae---a---b---b--b-----b-c-e-
> str24: d--e-d----b--c-b-ca----a----b-----
> str25: d---bda----ae--b---b----c---b-----
> str26: d--eb--e-db-e--b--a-----c---------
> str27: --ce---e--b--cd--c-bde------------
> str28: d---b--e-d-a------a-d--a---ab-----
> str29: --c-----c----cd--c-b-eb---d---c---
> str30: -a-e---e---a-cdb-c-bd-------------
> str31: dac-b--e---a-c---c------c-d-------
> str32: ---e----c---e--b-c------c-d-b--d-b
> str33: d----d----b----b-c---e----dab----b
> str34: -a----ae---a---b--a----a-e--ba----
> str35: ---e----c-b----b-ca----a--d---cd--
> str36: d--eb---c----c--ec--d-b-c---------
> str37: da----a-c-bae---e--b----c---------
> str38: -a---da---b-e-----a----ac-----c-e-
> str39: da-e----cdba-c----a----a----------
> str40: dac-b-----b---d--c---e----d---c---
> str41: d--e-d----b-e---e--b--b---d-----e-
> str42: --c--da--d---cd--c--d--a---a------
> str43: --ce---e-d---c-b--a--e---ed-------
> str44: --ce--aec--a------a----ac--a------
> str45: d-c-----c----c--e--b--b-----ba-d--
> str46: ----b-ae----e-----a--eb-----b--de-
> str47: d---bd-e--ba-c---c--d-b-----------
> str48: ---eb---c-b-e---e---d--a-e-a------
> str49: -a-e---e----e--b---bd-b-c--a------
> str50: d---bda---b--c--ec-b--b-----------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_06 = util.parse("nucleotide_n010k010.txt")
solution_06 = solve(instance_06, log=True)
```


> ```
> 
> Model:  expressions = 104, decisions = 100, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:           26
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,     687 itr]:           25
> 
> ```

> ```
> [  2 sec,    4523 itr]:           24
> 
> ```

> ```
> [  3 sec,    8295 itr]:           24
> 
> ```

> ```
> [  4 sec,   12133 itr]:           24
> 
> ```

> ```
> [  5 sec,   15938 itr]:           24
> 
> ```

> ```
> [  6 sec,   19639 itr]:           24
> 
> ```

> ```
> [  7 sec,   23468 itr]:           24
> 
> ```

> ```
> [  8 sec,   27357 itr]:           24
> 
> ```

> ```
> [  9 sec,   31171 itr]:           24
> 
> ```

> ```
> [ 10 sec,   34956 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,   38627 itr]:           24
> 
> ```

> ```
> [ 12 sec,   42392 itr]:           24
> 
> ```

> ```
> [ 13 sec,   46329 itr]:           24
> 
> ```

> ```
> [ 14 sec,   50147 itr]:           24
> 
> ```

> ```
> [ 15 sec,   53986 itr]:           24
> 
> ```

> ```
> [ 16 sec,   57899 itr]:           24
> 
> ```

> ```
> [ 17 sec,   61808 itr]:           24
> 
> ```

> ```
> [ 18 sec,   65702 itr]:           24
> 
> ```

> ```
> [ 19 sec,   69573 itr]:           24
> 
> ```

> ```
> [ 20 sec,   73470 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,   77385 itr]:           24
> 
> ```

> ```
> [ 22 sec,   81250 itr]:           24
> 
> ```

> ```
> [ 23 sec,   85127 itr]:           24
> 
> ```

> ```
> [ 24 sec,   89023 itr]:           24
> 
> ```

> ```
> [ 25 sec,   92882 itr]:           24
> 
> ```

> ```
> [ 26 sec,   96692 itr]:           24
> 
> ```

> ```
> [ 27 sec,  100698 itr]:           24
> 
> ```

> ```
> [ 28 sec,  104546 itr]:           24
> 
> ```

> ```
> [ 29 sec,  108335 itr]:           24
> 
> ```

> ```
> [ 30 sec,  112185 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,  116053 itr]:           24
> 
> ```

> ```
> [ 32 sec,  119941 itr]:           24
> 
> ```

> ```
> [ 33 sec,  123762 itr]:           24
> 
> ```

> ```
> [ 34 sec,  127542 itr]:           24
> 
> ```

> ```
> [ 35 sec,  131368 itr]:           24
> 
> ```

> ```
> [ 36 sec,  135169 itr]:           24
> 
> ```

> ```
> [ 37 sec,  139035 itr]:           24
> 
> ```

> ```
> [ 38 sec,  142883 itr]:           24
> 
> ```

> ```
> [ 39 sec,  146782 itr]:           24
> 
> ```

> ```
> [ 40 sec,  150612 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,  154314 itr]:           24
> 
> ```

> ```
> [ 42 sec,  158042 itr]:           24
> 
> ```

> ```
> [ 43 sec,  161888 itr]:           24
> 
> ```

> ```
> [ 44 sec,  165719 itr]:           24
> 
> ```

> ```
> [ 45 sec,  169520 itr]:           24
> 
> ```

> ```
> [ 46 sec,  173314 itr]:           24
> 
> ```

> ```
> [ 47 sec,  177210 itr]:           24
> 
> ```

> ```
> [ 48 sec,  181020 itr]:           24
> 
> ```

> ```
> [ 49 sec,  184794 itr]:           24
> 
> ```

> ```
> [ 50 sec,  188495 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,  192302 itr]:           24
> 
> ```

> ```
> [ 52 sec,  196058 itr]:           24
> 
> ```

> ```
> [ 53 sec,  199806 itr]:           24
> 
> ```

> ```
> [ 54 sec,  203478 itr]:           24
> 
> ```

> ```
> [ 55 sec,  207233 itr]:           24
> 
> ```

> ```
> [ 56 sec,  210301 itr]:           24
> 
> ```

> ```
> [ 57 sec,  212942 itr]:           24
> 
> ```

> ```
> [ 58 sec,  215503 itr]:           24
> 
> ```

> ```
> [ 59 sec,  217900 itr]:           24
> 
> ```

> ```
> [ 60 sec,  220267 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 60 sec,  220267 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> 220267 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           24
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_06
_solution = solution_06

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
>   Sol: TATGCGTACGACTATCGTACGTAC
> str01: -ATG-G---GA-TA-CG-------
> str02: -AT----AC--CT-TC---C---C
> str03: ----C--ACGA--AT--T--G-A-
> str04: TA-----A--A--ATC-T--GT--
> str05: -A-G-GTA--AC-A----A---A-
> str06: T-T-C---C---TA--G---GTA-
> str07: T-TG--TA-GA-T--C-T------
> str08: T--G-G---GA--A--GT---T-C
> str09: T-T-C---C-AC-A----AC-T--
> str10: T---C-TA--A--A-CG-A---A-
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_07 = util.parse("nucleotide_n050k050.txt")
solution_07 = solve(instance_07, log=True)
```


> ```
> 
> Model:  expressions = 2504, decisions = 2500, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:          146
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,      92 itr]:          139
> 
> ```

> ```
> [  2 sec,     268 itr]:          139
> 
> ```

> ```
> [  3 sec,     453 itr]:          139
> 
> ```

> ```
> [  4 sec,     619 itr]:          139
> 
> ```

> ```
> [  5 sec,     790 itr]:          139
> 
> ```

> ```
> [  6 sec,     958 itr]:          139
> 
> ```

> ```
> [  7 sec,    1145 itr]:          139
> 
> ```

> ```
> [  8 sec,    1290 itr]:          139
> 
> ```

> ```
> [  9 sec,    1458 itr]:          139
> 
> ```

> ```
> [ 10 sec,    1629 itr]:          139
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,    1814 itr]:          139
> 
> ```

> ```
> [ 12 sec,    1999 itr]:          139
> 
> ```

> ```
> [ 13 sec,    2161 itr]:          139
> 
> ```

> ```
> [ 14 sec,    2316 itr]:          139
> 
> ```

> ```
> [ 15 sec,    2478 itr]:          139
> 
> ```

> ```
> [ 16 sec,    2656 itr]:          139
> 
> ```

> ```
> [ 17 sec,    2834 itr]:          139
> 
> ```

> ```
> [ 18 sec,    3016 itr]:          139
> 
> ```

> ```
> [ 19 sec,    3178 itr]:          139
> 
> ```

> ```
> [ 20 sec,    3348 itr]:          139
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,    3519 itr]:          139
> 
> ```

> ```
> [ 22 sec,    3688 itr]:          139
> 
> ```

> ```
> [ 23 sec,    3866 itr]:          139
> 
> ```

> ```
> [ 24 sec,    4028 itr]:          138
> 
> ```

> ```
> [ 25 sec,    4208 itr]:          138
> 
> ```

> ```
> [ 26 sec,    4370 itr]:          138
> 
> ```

> ```
> [ 27 sec,    4553 itr]:          138
> 
> ```

> ```
> [ 28 sec,    4733 itr]:          138
> 
> ```

> ```
> [ 29 sec,    4913 itr]:          138
> 
> ```

> ```
> [ 30 sec,    5087 itr]:          138
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,    5264 itr]:          138
> 
> ```

> ```
> [ 32 sec,    5450 itr]:          138
> 
> ```

> ```
> [ 33 sec,    5630 itr]:          138
> 
> ```

> ```
> [ 34 sec,    5800 itr]:          138
> 
> ```

> ```
> [ 35 sec,    5974 itr]:          138
> 
> ```

> ```
> [ 36 sec,    6142 itr]:          138
> 
> ```

> ```
> [ 37 sec,    6316 itr]:          138
> 
> ```

> ```
> [ 38 sec,    6496 itr]:          138
> 
> ```

> ```
> [ 39 sec,    6676 itr]:          138
> 
> ```

> ```
> [ 40 sec,    6856 itr]:          138
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,    7030 itr]:          138
> 
> ```

> ```
> [ 42 sec,    7203 itr]:          138
> 
> ```

> ```
> [ 43 sec,    7380 itr]:          138
> 
> ```

> ```
> [ 44 sec,    7535 itr]:          138
> 
> ```

> ```
> [ 45 sec,    7722 itr]:          138
> 
> ```

> ```
> [ 46 sec,    7897 itr]:          138
> 
> ```

> ```
> [ 47 sec,    8064 itr]:          138
> 
> ```

> ```
> [ 48 sec,    8228 itr]:          138
> 
> ```

> ```
> [ 49 sec,    8410 itr]:          138
> 
> ```

> ```
> [ 50 sec,    8572 itr]:          138
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,    8741 itr]:          138
> 
> ```

> ```
> [ 52 sec,    8904 itr]:          138
> 
> ```

> ```
> [ 53 sec,    9057 itr]:          138
> 
> ```

> ```
> [ 54 sec,    9229 itr]:          138
> 
> ```

> ```
> [ 55 sec,    9414 itr]:          138
> 
> ```

> ```
> [ 56 sec,    9602 itr]:          138
> 
> ```

> ```
> [ 57 sec,    9761 itr]:          138
> 
> ```

> ```
> [ 58 sec,    9932 itr]:          138
> 
> ```

> ```
> [ 59 sec,   10101 itr]:          138
> 
> ```

> ```
> [ 60 sec,   10273 itr]:          138
> [ optimality gap     ]:      100.00%
> [ 60 sec,   10273 itr]:          138
> [ optimality gap     ]:      100.00%
> 
> 10273 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          138
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_07
_solution = solution_07

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 138) ---
>   Sol: ATGACGTACGTACAGTCATCAGCTACTGATCGTCATGACGATCAGTCAGACTACGTACAGCATCAGTACTGATCAGTCAGTCATGCATCGACTGCATGATCGTACTGACTACTGACTCAGTACGACTAGTCGACRTGT
> str01: -T-A-GTA-GTA--G--A-C---T-C----CG----GA--A---GT--GAC-A---A-A-C--C----CTGA--A---A---A-G-A---A-TG---GAT---A---A--A-T-A-T-A-------------------
> str02: --G--G-A--TA-A---A-CA-CT-C----C--C--GA--A--A---A---TA---A-----T---T--TGA-C--T---T-A---A---AC---A--A-CG--C-GAC-A--G--T---T-C-A--AG---------
> str03: AT-AC---C-T----TC--C---TA--G---GT-A--AC-A--A---A--C--C--A-A-C--CA--ACT--T---T---T---G-ATC---T-C-T--T-GTA--GA-T-CTG------------------------
> str04: -T-A---A---A---T--T-A--TA---ATC-T--T-A---T-A--C----TA-GTA-A--A--A--A---AT-AG---G----G--T-G--T--A--A-C---C-GA--A---A---A---CG----GTC-------
> str05: -T----TA---A-A---A-CAGC--CTG-T-G----G--G-T---T--G-C-AC---C--CA-C--T-C--A-CAG---G----GC--C--C---A----C-T---G------G-----G--CG-C-A----A---G-
> str06: ATGAC-T---T-C---CA--A--T---G---G--AT--C---C---CA-AC--C-T-CA--A---G--CT--TC---CA--C---C--C--C---A--AT-G----G--T--T---TCAG--C---------------
> str07: A--AC--A---A-A--C--CA---AC----C---A--AC--T---T-----T---T---G-ATC--T-CT--T--GT-AG--AT-C-T-G--T---T---C-T-CT-A--A---AC---G-A--AC------------
> str08: ATGA---A---A-A--C----G--A---A-----A--A---T---T-A---T---TA-----TCA--A--G----G---GT-ATG----GA----A-G-T-G----GA--A--G-CT--G-ACGA--A----A--T--
> str09: A---C-T-CG----G-C-T--GC-A-TG--C-T--T-A-G-T--G-CA--CT-C--AC-GCA---GTA-T-A--A-T---T-A---AT--A----A----C-TA---A-T--T-A-----------------------
> str10: -T----T--GTA--G--ATC---T---G-T--TC-T--C--T-A---A-AC---G-A-A-C-T---T--T-A--A---A---AT-C-T-G--TG--TG---G--CTG--T-C--ACTC--------------------
> str11: --G-C--A-G-A--G-CAT--
> ```

> ```
> --T--T--TC-T-A--A---T-A-TC---C-AC--A-A--A--A-T---GA--AG---G-CA---AT--A----AT--T-GTACT-ACT-C--------------------------
> str12: ATGA-G--C---CA---A---G--A-T---C--C--GACGA--AG--AG-C--C---C--CA--AG----GA---G---G--A-G-A---A--G---GA--G----G------GAC-C----C--C----C-------
> str13: -T--C-T-C--ACAGT--TCA---A--GA-----A---C---C---CA-A--A-GTAC--C--C----C----C---CA-T-A-GC--C--CT-C-T--T---A---A--A--G-C-CA---C---------------
> str14: A-G--GT---T----T-AT-A-C--CT--TC--C-T-A-G----GT-A-AC-A---A-A-C--CA--AC----CA---A--C-T---T----T-C--GATC-T-CT---T---G--T-A-------------------
> str15: A-G--GT---T----T-AT-A-C--CT--TC--C----C-A---G---G--TA---ACA--A--A---C----CA---A--C---CA---ACT---T--TCG-A-T--CT-CT---T--GTA----------------
> str16: -T-A---A---A-A--CA--A-CT-C--A-----AT-AC-A--A--CA---TA---A--G-A--A--A---ATCA---A--C--GCA---A----A--A----AC--ACT-C--AC--A--A--A-------------
> str17: ----C---CG--C---C--CA--T--T--T-G----G--G--C-G---G-CT-C-T-C-G-A---G--C-GAT-AG-C--TC--G--TCGA----AT---C---C---CT-C-GAC-C--T-----------------
> str18: AT-AC---C-T----TC--C--C-A--G---GT-A--AC-A--A---A--C--C--A-A-C--CA--ACT--T---TC-G--AT-C-TC---T---TG-T---A--GA-T-CTG------------------------
> str19: -T--C-T-C--ACAGT--TCA---A--GA-----A---C---C--TCA-A----GT-C----TC----C----C---C---CAT--A--G---GC-----C-T-CT---T--T--C--AGT-C-A---G---------
> str20: --GA--T-C-T-C--TC-TCA-C--C-GA-----A---C---C--T--G-----G--C--C--C----C-G----G---G-CA---A---A-TGC-----C---CT-A--A-T--C-CAG-A-G----GT-G------
> str21: A-GA-G--C--A-A-TCA---G-T---G--C---AT--C-A---G--A-A--A--TA-----T-A---C----C--T-A-T--T--AT--AC---A----C-T--T---T---G-CT-A--A-GA--A-T--------
> str22: A--A--T---TA-A---A--A-C-A-T---C-TCA--A---T-A--CA-AC-A--TA-AG-A--A--A---A--A--CA---A--C---G-C---A--A----A---A--AC--ACTCA-T-----------------
> str23: A--A---ACG-A-A--C-T----T--T-A-----A--A--ATC--T--G--T--GT---G-----G--CTG-TCA--C--TC--G----G-CTGCATG--C-T--T-A-----G--T--G--C---------------
> str24: AT-A---AC-TA-A-T--T-A-CT---G-TCGT--TGAC-A---G---GAC-ACG-A--G--T-A--ACT---C-GTC--T-AT-C-T----T-C-TG----------------------------------------
> str25: ATGA-GT--GT-CA--C----G--A---AT--TCA---CG-T-A--CA-A-T--G-A-A-C-T--G----GAT--GT---TCA--C---G--TG---GA----A-T-A--A---------------------------
> str26: A---C---CGT---G------G-----G--CG--A-G-CG----GT--GAC--CG----G--T--GT-CT--TC---C--T-A-G--T-G---G---G-TC---C---C-AC-G--T---T--GA--A------R---
> str27: A--A---A-G----GT--T----TA-T-A-C--C-T-----TC---C---C-A-G----G--T-A--AC--A--A---A--C---CA---AC--CA--A-C-T--T---T-C-GA-TC--T-C---T--T-G------
> str28: A-G---TA-GT----TC----GC--CTG-T-GT---GA-G--C--T--GAC-A---A-A-C-T---TA--G-T-AGT--GT--T---T-G--TG-A-G---G-A-T---TA---------------------------
> str29: -T----T---TA---T-A-C--CT--T---C--C-T-A-G----GT-A-AC-A---A-A-C--CA--AC----CA---A--C-T---T----T-C--GATC-T-CT---T---G--T-AG-A----T-----------
> str30: ATG-CG---GT-C-GTC-TC---T-C----C--C----CG----G-C----T---T------T---T--T--T---TC---C---C--CG-C-GC-----CG--C-G--T--TG-----G--CG-C----CGA-----
> str31: --G---T--G-ACA---A--A---A---A-C---AT-A--AT--G---GACT-C---CA--A-CA---C----CA-T--GTCA---A--G-CT---T--TC--A--G------G--T-AG-AC---------------
> str32: --G---T--GTA-AG--A--A---AC--A--GT-A--A-G--C---C---C---G----G-A--AGT---G----GT--GT--T---T----TGC--GAT--T--T--C----GA----G---G-C----CG----G-
> str33: --GA-G-A---A---T-----G--A--G-TC-TCAT-----T-A--C---C---G--C--C--C-G----G-T-A--C--T--T--A--G-C---A--A--G--CT-A--A-T-A----GT-C-AC--G--G-C----
> str34: ATG---T--G----GTC----G--A-TG--C--CATG--GA---G---G-C--C---CA-C--CAGT--T---CA-T---T-A---A--G---GC-T---C---CTG------G-C--A-T-----T-----------
> str35: A---CG-A-G--C-GT--T----T--T-A-----A-G--G----G-C---C--CG--C-G-A-C--T---G--C-G--A--C--G----G-C--CA----C--A-TG------G-C-C----C---T-GT--A--TGT
> str36: --G--GT---T----T-AT-A-C--CT--TC--C----C-A---G---G--TA---ACA--A--A---C----CA---A--C---CA---ACT---T--TCG-A-T--CT-CT---T--GTA-G--------------
> str37: -TG--G---G-A-AGT--TC--C-A---A-----A--A-GATCA--CA-A--A---ACA-C-T-A---C----CAGTCA---A--C--C---TG-A--A--GTAC--AC-----------------------------
> str38: --GA---A-G--C-GT--T-A---AC-G-T-GT--TGA-G----G--A-A--A---A--G-A-CAG--CT--T-AG---G--A-G-A---AC---A--A--G-A--G-CT---G-----G---G--------------
> str39: A---C---C--A--G-C----GC-ACT--TCG----G-C-A---G-C-G-----G--CAGCA-C----CT---C-G---G-CA-GCA-C--CT-CA-G--C--A--G-C-A---AC----------------------
> str40: ATG--G---G-ACA---A-C---T--T-AT--TC----C--T-A-TCA---T--GT---GC--CA--A--GA---G---GT--T---T----T--A----C---C---C----G-----GT--GAC----C-A-----
> str41: -T----T--GTA--G--ATC---T---G-T--TC-T--C--T-A---A-AC---G-A-A-C-T---T--T-A--A---A---AT-C-T-G--TG--TG---GT--TG--T-C--ACTC--------------------
> str42: A--AC---C--A-A--C--CA---ACT--T--TC--GA---TC--TC----T---T---G--T-AG-A-T---C--T--GT--T-C-TC---T--A--A----AC-GA--ACT---T---TA----------------
> str43: --G--G---GT----TC-T--GC--C--A--G----G-C-AT-AGTC----T---T------T---T--T--T---TC--T---G----G-C-G---G--C---C---CT--TG--T--GTA--A--A--C--C-TG-
> str44: --G--G--C-T---G-CAT--GCT--T-A--GT---G-C-A-C--TCA--C---G--CAG--T-A-TA---AT---T-A---AT--A---ACT--A--AT--TACTG--T----------------------------
> str45: -TG-C--A--T---G-C-T----TA--G-T-G-CA---C--TCA--C-G-C-A-GTA-----T-A--A-T--T-A---A-T-A---A-C---T--A--AT--TACTG--T-C-G--T---------------------
> str46: -T----T-C---CA--CA--A-CT--T--TC--CA---C---CA---AG-CT-C-T---GCA--AG-A-T---C---C---CA-G-A--G--T-CA-G---G----G------G-C-C--T--G--T-----------
> str47: -T--C-TA---A-A--C----G--A---A-C-T--T-----T-A---A-A--A--T-C----T--GT---G-T--G---G-C-TG--TC-ACT-C--G---G--CTG-C-A-TG-CT---TA-G--------------
> str48: A---C---CG----G--AT--G-----G--C--C--G-CGAT---T-----T---T------TC-G----GA---GTC---C-T---T-G---G---G---G----GAC--C--ACTCAG-A--A-TAG---A-----
> str49: ----C-T---T---GT-A---G--A-T---C-T---G----T---TC----T-C-TA-A--A-C-G-A---A-C--T---T--T--A---A----A--ATC-T---G--T---G--T--G---G-CT-GTC-AC-T--
> str50: ATGA-G--C--AC--T-A--AGC----GA-----A-GA--A-C---CA-A--A---A-AGCA---G-AC--A--A-T-A--CA---A-C--C--C--G--C-TA-T---TAC--------------------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_08 = util.parse("protein_n010k010.txt")
solution_08 = solve(instance_08, log=True)
```


> ```
> 
> Model:  expressions = 104, decisions = 100, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:           57
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,     455 itr]:           51
> 
> ```

> ```
> [  2 sec,    1157 itr]:           48
> 
> ```

> ```
> [  3 sec,    1716 itr]:           47
> 
> ```

> ```
> [  4 sec,    2323 itr]:           47
> 
> ```

> ```
> [  5 sec,    2921 itr]:           46
> 
> ```

> ```
> [  6 sec,    3568 itr]:           46
> 
> ```

> ```
> [  7 sec,    4260 itr]:           46
> 
> ```

> ```
> [  8 sec,    4916 itr]:           46
> 
> ```

> ```
> [  9 sec,    5660 itr]:           46
> 
> ```

> ```
> [ 10 sec,    6446 itr]:           46
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,    7249 itr]:           46
> 
> ```

> ```
> [ 12 sec,    8110 itr]:           46
> 
> ```

> ```
> [ 13 sec,    8971 itr]:           46
> 
> ```

> ```
> [ 14 sec,    9730 itr]:           46
> 
> ```

> ```
> [ 15 sec,   10523 itr]:           46
> 
> ```

> ```
> [ 16 sec,   11366 itr]:           46
> 
> ```

> ```
> [ 17 sec,   12172 itr]:           46
> 
> ```

> ```
> [ 18 sec,   12980 itr]:           46
> 
> ```

> ```
> [ 19 sec,   13743 itr]:           46
> 
> ```

> ```
> [ 20 sec,   14530 itr]:           46
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,   15295 itr]:           46
> 
> ```

> ```
> [ 22 sec,   16058 itr]:           46
> 
> ```

> ```
> [ 23 sec,   16854 itr]:           46
> 
> ```

> ```
> [ 24 sec,   17620 itr]:           46
> 
> ```

> ```
> [ 25 sec,   18379 itr]:           46
> 
> ```

> ```
> [ 26 sec,   19203 itr]:           45
> 
> ```

> ```
> [ 27 sec,   20027 itr]:           45
> 
> ```

> ```
> [ 28 sec,   20815 itr]:           45
> 
> ```

> ```
> [ 29 sec,   21644 itr]:           45
> 
> ```

> ```
> [ 30 sec,   22493 itr]:           45
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,   23339 itr]:           45
> 
> ```

> ```
> [ 32 sec,   24125 itr]:           45
> 
> ```

> ```
> [ 33 sec,   24958 itr]:           45
> 
> ```

> ```
> [ 34 sec,   25790 itr]:           45
> 
> ```

> ```
> [ 35 sec,   26618 itr]:           45
> 
> ```

> ```
> [ 36 sec,   27439 itr]:           45
> 
> ```

> ```
> [ 37 sec,   28299 itr]:           45
> 
> ```

> ```
> [ 38 sec,   29102 itr]:           45
> 
> ```

> ```
> [ 39 sec,   29887 itr]:           45
> 
> ```

> ```
> [ 40 sec,   30690 itr]:           45
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,   31407 itr]:           45
> 
> ```

> ```
> [ 42 sec,   32186 itr]:           45
> 
> ```

> ```
> [ 43 sec,   32969 itr]:           45
> 
> ```

> ```
> [ 44 sec,   33775 itr]:           45
> 
> ```

> ```
> [ 45 sec,   34518 itr]:           45
> 
> ```

> ```
> [ 46 sec,   35299 itr]:           45
> 
> ```

> ```
> [ 47 sec,   36057 itr]:           45
> 
> ```

> ```
> [ 48 sec,   36797 itr]:           45
> 
> ```

> ```
> [ 49 sec,   37561 itr]:           45
> 
> ```

> ```
> [ 50 sec,   38340 itr]:           45
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,   39096 itr]:           45
> 
> ```

> ```
> [ 52 sec,   39823 itr]:           45
> 
> ```

> ```
> [ 53 sec,   40600 itr]:           45
> 
> ```

> ```
> [ 54 sec,   41359 itr]:           45
> 
> ```

> ```
> [ 55 sec,   42084 itr]:           45
> 
> ```

> ```
> [ 56 sec,   42874 itr]:           45
> 
> ```

> ```
> [ 57 sec,   43682 itr]:           45
> 
> ```

> ```
> [ 58 sec,   44515 itr]:           45
> 
> ```

> ```
> [ 59 sec,   45264 itr]:           45
> 
> ```

> ```
> [ 60 sec,   46027 itr]:           45
> [ optimality gap     ]:      100.00%
> [ 60 sec,   46027 itr]:           45
> [ optimality gap     ]:      100.00%
> 
> 46027 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           45
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_08
_solution = solution_08

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 45) ---
>   Sol: MESFYPQALSERNYQHVAFCPKGFTNESLRHDNGAIRPVTYALKQ
> str01: M------ALS---Y-----CPKG-T--------------------
> str02: M-----Q--S-----------------SL---N-AI-PV------
> str03: M----P--LS---YQH--F----------R-------------K-
> str04: ME--------E----HV--------NE-L-HD-------------
> str05: M-S---------N-----F------------D--AIR----AL--
> str06: M--F-------RN-Q----------N-S-R--NG-----------
> str07: M--FY--A-------H-AF---G----------G------Y----
> str08: M-S------------------K-FT----R------RP--Y---Q
> str09: M-SF------------VA----G---------------VT-A--Q
> str10: MES-----L-------V---P-GF-NE------------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_09 = util.parse("protein_n050k050.txt")
solution_09 = solve(instance_09, log=True)
```


> ```
> 
> Model:  expressions = 2504, decisions = 2500, constraints = 0, objectives = 1
> Param:  time limit = 60 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]:          475
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [  1 sec,      17 itr]:          475
> 
> ```

> ```
> [  2 sec,      27 itr]:          473
> 
> ```

> ```
> [  3 sec,      36 itr]:          462
> 
> ```

> ```
> [  4 sec,      55 itr]:          462
> 
> ```

> ```
> [  5 sec,      70 itr]:          457
> 
> ```

> ```
> [  6 sec,      91 itr]:          457
> 
> ```

> ```
> [  7 sec,     120 itr]:          457
> 
> ```

> ```
> [  8 sec,     150 itr]:          457
> 
> ```

> ```
> [  9 sec,     176 itr]:          457
> 
> ```

> ```
> [ 10 sec,     193 itr]:          456
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 11 sec,     221 itr]:          456
> 
> ```

> ```
> [ 12 sec,     241 itr]:          456
> 
> ```

> ```
> [ 13 sec,     259 itr]:          454
> 
> ```

> ```
> [ 14 sec,     289 itr]:          454
> 
> ```

> ```
> [ 15 sec,     317 itr]:          454
> 
> ```

> ```
> [ 16 sec,     346 itr]:          454
> 
> ```

> ```
> [ 17 sec,     376 itr]:          454
> 
> ```

> ```
> [ 18 sec,     405 itr]:          454
> 
> ```

> ```
> [ 19 sec,     434 itr]:          454
> 
> ```

> ```
> [ 20 sec,     464 itr]:          454
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 21 sec,     482 itr]:          454
> 
> ```

> ```
> [ 22 sec,     511 itr]:          454
> 
> ```

> ```
> [ 23 sec,     540 itr]:          454
> 
> ```

> ```
> [ 24 sec,     566 itr]:          454
> 
> ```

> ```
> [ 25 sec,     591 itr]:          454
> 
> ```

> ```
> [ 26 sec,     618 itr]:          454
> 
> ```

> ```
> [ 27 sec,     641 itr]:          454
> 
> ```

> ```
> [ 28 sec,     663 itr]:          454
> 
> ```

> ```
> [ 29 sec,     692 itr]:          454
> 
> ```

> ```
> [ 30 sec,     720 itr]:          454
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 31 sec,     743 itr]:          454
> 
> ```

> ```
> [ 32 sec,     764 itr]:          454
> 
> ```

> ```
> [ 33 sec,     793 itr]:          454
> 
> ```

> ```
> [ 34 sec,     822 itr]:          454
> 
> ```

> ```
> [ 35 sec,     843 itr]:          454
> 
> ```

> ```
> [ 36 sec,     872 itr]:          454
> 
> ```

> ```
> [ 37 sec,     896 itr]:          454
> 
> ```

> ```
> [ 38 sec,     922 itr]:          454
> 
> ```

> ```
> [ 39 sec,     944 itr]:          454
> 
> ```

> ```
> [ 40 sec,     973 itr]:          454
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 41 sec,    1002 itr]:          454
> 
> ```

> ```
> [ 42 sec,    1031 itr]:          454
> 
> ```

> ```
> [ 43 sec,    1048 itr]:          454
> 
> ```

> ```
> [ 44 sec,    1073 itr]:          454
> 
> ```

> ```
> [ 45 sec,    1093 itr]:          454
> 
> ```

> ```
> [ 46 sec,    1119 itr]:          454
> 
> ```

> ```
> [ 47 sec,    1135 itr]:          454
> 
> ```

> ```
> [ 48 sec,    1156 itr]:          454
> 
> ```

> ```
> [ 49 sec,    1169 itr]:          454
> 
> ```

> ```
> [ 50 sec,    1181 itr]:          454
> [ optimality gap     ]:      100.00%
> 
> ```

> ```
> [ 51 sec,    1211 itr]:          454
> 
> ```

> ```
> [ 52 sec,    1232 itr]:          454
> 
> ```

> ```
> [ 53 sec,    1261 itr]:          454
> 
> ```

> ```
> [ 54 sec,    1274 itr]:          454
> 
> ```

> ```
> [ 55 sec,    1287 itr]:          454
> 
> ```

> ```
> [ 56 sec,    1308 itr]:          454
> 
> ```

> ```
> [ 57 sec,    1321 itr]:          454
> 
> ```

> ```
> [ 58 sec,    1342 itr]:          454
> 
> ```

> ```
> [ 59 sec,    1365 itr]:          454
> 
> ```

> ```
> [ 60 sec,    1385 itr]:          454
> [ optimality gap     ]:      100.00%
> [ 60 sec,    1385 itr]:          454
> [ optimality gap     ]:      100.00%
> 
> 1385 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          454
>   gap    =      100.00%
>   bounds =            0
> 
> ```



In [ ]:
```python
_instance = instance_09
_solution = solution_09

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 454) ---
>   Sol: MFAVFLESVLLPNRLVSSQPGFCVNEKTLDHAIRPLVQTRLSLPTAFYINSLVKETGILQVRDASLPFKVLITDNQALEMRPSTYHQALFGKWNLITAVRGDENSIPFTNYEGTVDSAQPKIEVLQKSAPELARGCNDVYLHTNSGIFEKLTRGVQANWDTSILAEGVFYPKSDMVLKRAQHTNDEVRGFAILYSPKRSTGVENQLPDSRVEKLTPASIYTNDVFRKHSQLAGEFTCLDRKSVFGMILSYWADETVQLNRIWTSLGAFPDERVKALYNSGIPQHRLTKPGINFQDLESIAYWMFDLVKPTSCIVRAHLSGEDNPMICKHSFDTVAGLIQDRGSIVPYNALTEIVGPRDIECNLFRSKWVTDPELAGRVYESGKMDQSNASYVKELRRDNISTHVKDRTGLFVCSIARNKYMGEDHPVWQALIKEGNRSAKFNLQRTVDGHIPTY
> str01: M------------R----------------H----L-------------N-------I----D--------I------E----TY-------------------S-----------S-------------------ND--------I--K-------N--------GV-Y-K---------------------Y----------------------A-----D--------A-E----D----F---------E------I---L----------L----------------F------AY---------S-I--------D-------------G-----G---------E-V-----EC-L-------D--L---------------------------T----R-----------------------------------------------
> str02: M-----E------R-------------------R-----------A---------------------------------------H-------------R--------T--------------------------------H-------------Q-NWD----A-----------------T-------------K---------P--R-E-------------R-------------RK---------------Q-----T-------------------QHRLT-----------------------------H------P-------D-------D--SI--Y--------PR-IE------K-------A----E-G-------------R--------K-----------------EDH---------G-------------------
> str03: M-----E----P--------G----------A--------------F---S----T-------A-L-F-----D--AL---------------------------------------------------------C-D---------------------D--IL-----------------H-----R---------R-------L-----E-----S-----------QL--------R---FG--------------------G------V---------Q-------I-----------------P--------------P---------------------------E-V-----------S----DP----RVY---------A-------------------G----------Y---------AL-----------L-----------
> str04: M-------------------G-----K-------------------FY------------------------------------Y-------------------S----N-----------------------R------------------R----------LA--VF----------AQ---------A-------------Q---SR-----------------H--L-G-----------G---SY---E--Q----W--L-A--------------------------------------------C-V----SG-D-------S----A----------------------------FR---------A----E-----------VK----------------------AR---------V-Q---K--------------D------
> str05: -F--F--------R-----------E-----------------------N-L-----------A---F-------Q----------Q---GK-----A-R--E----F-----------P-------S--E-----------------E-------A---------------------RA---N----------SP---T--------SR-E-L------------------------------------W----V---R-----------R-------G---------G-N----------------P--------LS-E-------------AG------------A--E----R-------R----------G-------------------------T----------------------------------------------------
> str06: M----------------------------D----P------SL-T--------------QV-------------------------------W----AV---E---------G---S------VL--SA---A-----V--------------------DT---AE----------------TND--------------T--E---PD---E--------------------G----L---S---------A-E----N-----------E--------G----------------E------------T----R----------I-----------I--R--I------T---G----------S----------------------------------------------------------------------------------------
> str07: M-A-F------------------------D----------------F---S-V--TG-----------------N--------T-------K--L------D------T-------S-----------------G------------F---T---Q----------GV----S---------------------S--------------------------------------------------M--------TV----------A-------A----G------T--------L--IA----DLVK-T-----A--S----------S--------Q----------LT----------NL-----------A----------QS-------------------------------------------------------------------
> str08: M-AV----------------------
> ```

> ```
> ------I--L-------P------S----T----------------------------Y-----------T----D----------GT---A----------A------C------TN-G---------------S--------P--D-V----------V-G----------TG-------------T------------------------------M----W----V--N---T-----------------I----L--PG----D--------F--------------------------F------------------------------------W-T-P--------SG-----------E------S--V--R----V------------------------------------------
> str09: M-----------N--------------T----------------------------GI-------------I-D---L-----------F-----------D-N-------------------------------------H------------V----D-SI-------P-----------T--------IL--P-------------------------------H-QLA---T-LD----------Y-------L--------------V-----------R-T---I-------I-----D---------------E-N-----------------R-S-V----L------------LF--------------------------------------H-----------I-----MG---------------S----------G-----
> str10: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR----T--------------Q-----LP--------------P-----A----------------------Y--T----------------------N-------S--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-------------S------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M----------------------------D-----------S-----------KET-IL------------I------E----------------I---------IP-------------KI----KS-----------YL---------L--------DT----------------------N-------I--SPK-S--------------------Y-ND-F---------------------I-S----------R-----------------N---------K---N------I----F--V-----I---------N-------------L---------YN-----V-----------S---T-----------------------------I------------------------------------------------------
> str12: M----L---L------S---G-----K--------------------------K--------------K----------M--------L-----L------D-N------YE-T---A----------A---ARG-----------------RG------------G------D-----------E-R---------R-----------R----------------------G-----------------WA---------------F-D-R---------P-----------------A------------IV------------------T---------------------------------K---------R-------D-------K-------S----DR-------------M--------A-------------------H----
> str13: M-----------N-------G----E----------------------------E-------D----------DN---E-------QA---------A-------------------A----E--Q-----------------------------Q----T----------K-----K-A----------------KR----E---------K--P----------K--Q-A-------RK-V-----------T--------S------E---A--------------------------W------------------E-------H-FD--A---------------T------D------------D----G------------A----E------------------C-----K-----H-----------------------------
> str14: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS------V------E-----------------E-----V--------L--------S------------E----A------R------Q----------------------H--L---------K-----------D------------G--------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M------------R---------------------------------YI---V-----------S-P--------Q-L--------------------V-------------------------LQ------------V------G---K---G-Q---------E-V-----------------E-R--A-LY-----------L--------TP---Y--D--------------------------Y----------I--------DE--K----S--P--------I---------Y---------------------------------------------Y----------------F---------L--R---S---------------------H------L-------N-------------I-----------QR------P--
> str16: M----------P-R-V---P---V-----------------------Y--------------D-S-P--------Q----------------------V-----S-P--N---TV----P-----Q--A----R------L---------------A---T---------P-S----------------FA--------T------P-------T---------FR------G------------------AD-------------A-P-----A-----------------FQD--------------T-----A------N---------------Q----------------------------------------------Q--A------R--------------------------------Q-------------------------
> str17: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR----T--------------Q-----LP---L-----A-------Y-----------T------NS--FT------------------------RG---VY-----------------------------YP--D---K--------V--F-------RS---------S-V--L-------------HS---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: MF-VF----------------F-V----L------L-------P-------LV-----------S-----------------S---Q------------------------------------------------C--V----N------LT--------T-----------------R---T---------------------QLP--------PA--YTN------S-----FT---R----G----------V--------------------Y-----------------------Y-------P------------D-----K-----V-----------------------------FRS--------------S----------V--L-------H----------S----------------------------------------
> str19: M-----E------------------------AI---------------I-S----------------F--------A-------------G----I----G----I---NY---------K-----K----L-----------------------Q-----S---------K----L---QH--D----F----------G--------RV--L------------K----A-----L----------------TV------T---A----R--AL-----P-------G---Q--------------P------------------KH--------I----------A---I---R----------------------------Q--------------------------------------------------------------------
> str20: M-A----S--------S---G-------------P-------------------E------R-A--------------E------HQ--------I---------I------------------L----PE-------------S------------------------------------H----------L-S---S-------P------L---------V--KH------------K------L---------L------------------Y-----------------------YW-----K---------L--------------T--GL--------P---L-----P-D-EC---------D---------------------------------------F------------DH-----LI----------------------
> str21: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS------V------E-----------------E-----V--------L--------S------------EVR----------------Q----------------------H--L---------K-----------D------------G--------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L-------------------------A--P------S-P-----NS--K---I-Q-----L-F------N------------------N-I-------N-I---------D-----I--------------N--Y--------E--------------------------------HT---------LY------------------------------F------A---------SV-----S--A----Q-N----S---F------------------------F------A--------------------------------------Q----------------------------WV--------VY-S-------A--------D------K----------A---------------I----------------------
> str23: M------S-----------------------AI-----T---------------ET------------K------------P-T-----------I------E---------------------L----P--A-------L---------------A--------EG-F-----------Q------R-----Y---------N--------K-TP----------------G-FTC-----V----L----D------R----------------Y-----------------D---------------------H--G-------------V---I---------N---------D-------SK--------------------------------I---V-----L---------Y---------------N------------------
> str24: M-------------------------K----------------------N-------I-----A--------------E----------F-K----------------------------K-------APELA---------------EKL------------L-E-VF---S----------N--------L---K---G--N----SR-------S------------L-------D-----------------------------P---------------------------------M-----------RA---G-------KH--D-V----------V--------V----IE-----S---T------------K---------K-L-----------------------------------------------------------
> str25: M----------P------QP--------L------------------------K-----Q----SL-------D-Q------S--------KW-L----R--E--------------A----E---K--------------H--------L-R---A------L-E------S---L---------V--------------------DS------------N--------L--E-------------------E----------------E--K-L-----------KP----Q-L-S----M----------------GED-----------V----Q---S---------------------------------------------------------------------------------------------------------------
> str26: MF-VFL--VLLP--LVSSQ---CVN---L---I-----TR----T--------------Q----S-------------------Y-----------T------NS--FT------------------------RG---VY-----------------------------YP--D---K--------V--F-------RS---------S-V--L-------------HS------T--------------------Q------------D----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-------------------------K-------------------F---------------D------VL-----------S-----LF-------A--------P---------------------------------------------------W-----A------K---V--------DE------------------Q------E-------Y--D------Q--------------------------QLN------------------N-------------N---LESI----------T-----A-------P---K--FD-------D-G------A-TEI------E-----S------E---R----G--D--------------I------------------------------------------------------
> str28: MF-VFL--VLLP--LVSSQ---CVN---------------------F--------T------------------N-----R--T--Q-L-----------------P---------SA---------------------Y--TNS--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-------------S------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-------------------------------------------------------------------------------------------W-----------SI---------------I-VL-K----L--------------I--------------SI-----------------Q--------------P---------L-------L----------------L-----------V-----------T--------SL---P------LYN---P---------N----------M-D-----SC--------------C---------LI----S-------------R-I----------T-PELAG------K-----------L------T-------------------------W---I--------F---------I---
> str30: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS------V------E-----------------E-------------------F-------L-----------------S-------E-------------A--------R---Q-----------------------------------------------------H-L-K------D------------------------G------------T-------------------------------------------------------------------------------------------------------------------------
> str31: MF-VFL--VLLP--LVSSQ---CV-------------------------------------------------------M-P------LF---NLIT-----------T----T----Q--------S-----------Y--TN---F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-L------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M-----------------------------H------Q----------I------T----V--------V------------S-------G---------------P-T--E--V-S-------------------------T---------------------------------------------------------------------------------------------C------FG---S--------L-------------------------H----P---FQ---S-------L-KP----V----------M---------A------------NAL----G-------------V----L-----E-GKM--------------------------F-CSI------G------------G-RS----L-----------
> str33: M-A------------------------TL------L---R-SL--A-----L---------------FK-----------R------------N--------------------------K----------------D-----------K--------------------P------------------------P----------------------I-T-------S---G--------S--G--------------------GA-------------I---R----GI----------------K--------H--------I-----------I-----IVP------I--P-------------------G--------D-S--S---------I-T-----T--------R--------------------S------R---------
> str34: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS---------------------------------------------------------M----------E----------------E-------V--L---S---------------E-----------------A-------R----------------------QH-L-K------D------------------------G------------T-------------------------------------------------------------------------------------------------------------------------
> str35: MF-VFL--VLLP--LVSSQ---CVN---L---------T-----T-----------G---------------T--Q-L---P------------------------P----------A---------------------Y--TNS--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-------------S------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: M-A---------N-------------------I---------------IN-L----------------------------------------WN------G----I--------V----P------------------------------------------------------MV----Q---D-V----------------N------V-----ASI-T----------A--F-----KS---MI-----DET------W-------D---K-------------K--I-----E--A----------------------N---------T---------------------------C--------------------------------------IS-----R-----------K-----H-----------R----N------------
> str37: M----L------NR------------------I----QT-L--------------------------------------M-----------K----TA-----N-----NYE-T-------IE-----------------------I---L-R----N-----------Y------L-R-------------LY------------------------I---------------------------IL---A-------R-----------------N------------------E-----------------------E--------------G----RG-I-----L--I-------------------------Y-----D------------DNI-----D-------S------------V---------------------------
> str38: M-A--------------------------D----P----------A----------G---------------T-N---------------G-----------E--------EGT--------------------GCN--------G------------W---------FY-----V---------E----A----------V--------VEK-------------K--------T--------G-------D-------------A-------------I----------------S------D----------------D-----------------------------E---------N----------E--------------N---------D--S----D-TG-------------ED------L---------------VD------
> str39: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR----T--------------Q-----LP--------------PS-Y-----------T------NS--FT------------------------RG---VY-----------------------------YP--D---K--------V--F-------RS---------S-V--L-------------HS---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQV--------------------------------------------------------------------------C-DV-L-------------V-----------------------R---------GF----------G------DS-VE---------------------E--------V----LS----E------------A----R----------QH-L-K------D------------------------G------------T-------------------------------------------------------------------------------------------------------------------------
> str41: M-----------N-----------N------------Q-R-------------K--------------K---T---A---RPS------F---N--------------------------------------------------------------------------------M-LKRA-------R---------------N-----RV------S--T--V----SQLA--------K------------------R-------F----------S--------K-G-----L---------L----S--------G------------------Q--G---P-------------------------------------M--------K-L--------V----------------M--------A----------F-------------
> str42: M------S----N--------F-------D-AIR-----------A-----LV---------D---------TD--A-------Y------K--L-----G----------------------------------------H----I----------------------------------H---------------------------------------------------------------M---Y------------------P-E--------G------T---------E---Y-----V----------LS---N-------F-T------DRGS-------------R-IE---------------G-V-----------------------TH----T---V------------H-----------------------------
> str43: M-------------------------------I---------------------E---L--R------------------
> ```

> ```
> -----H----------------E-----------V---Q---------------G--D--L-------------V-----T-I--------------------N--V--------------VE-----------TP-----------------E----D--------L----D------------G-F---R----------------------D--------F--------I-RAHL-------IC---------L-----------A----V---D-----------T--E----------------------------T-----TGL-------------D-------I---------------------Y
> str44: MF-VFL--VLLP--LVSSQ---CV-------------------------------------------------------M-P------LF---NLIT-----------TN--------Q--------S-----------Y--TNS--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M------S------------------K--D-----LV--------A---------------R-------------QAL-M---T---A-----------R--------------------------------------------------------------------------M--K-A----D----F-----------V----------------------F---------F--L-----F-----------V-L---W-----------KAL--S------L--P-----------------V-PT----R-----------C-----------Q----I-------------D-------------------------M----A---K-----------K----L---S-A-----G--------------------------------
> str46: M-A----S-LL---------------K--------------SL-T------L---------------FK-----------R--T---------------R-D----------------QP---------P-LA-----------SG---------------S----G---------------------G-AI-----R--G-----------------I-------KH--------------V---I-------------I-----------V--L----IP-------G----D--S------------S-IV------------------T-------R-S-------------R-------------------------------------------------------------------------------------------------
> str47: M------------R-V-----------------R----------------------GIL--R------------N-----------------W-------------------------Q------Q--------------------------------W-------------------------------------------------------------------------------------------W---------IWTSLG-F---------------------------------WMF--------------------MIC--S---V----------V---------G------NL----WVT-------VY-----------Y-----------------G--V-------------PVW----KE----AK-----T------T-
> str48: M-AV--E----P---------F------------P----R---------------------R----P----IT-------RP---H-A----------------SI-----E--VD--------------------------T-SGI------G------------G-----S------A--------G-----S---S---E---------K----------VF-----------CL--------I------------------G----------------Q----------------A--------------------E--------------G-----G---------E---P-----N-------T-------V----------------------------------------------------------------------------
> str49: MF---------------------------------------------Y---------------A---------------------H-A-FG---------G---------Y----D------E-------------N---LH--------------A-----------F-P-----------------G--I--S---ST-V--------------A----NDV-RK----------------------Y-------------S--------V---------------------------------V---S--V--------------------------------YN------------------K---------------K-------Y-------NI---VK------------NKYM------W--------------------------
> str50: M-A---------N----------------------------------Y--S--K------------PF--L------L-----------------------D---I--------V--------------------------------F---------N-------------K-D-----------------I----K---------------------------------------C---------I-----------N----------D--------S--------------------------------C------S---------HS-D----------------------------C---R-------------Y------QSN-SYV-ELRR-N-----------------------------QAL----N---K-NL-----------
> 
> solution is feasible: True
> 
> ```


