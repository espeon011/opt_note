In [ ]:
```python
import hexaly.optimizer
import util
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# Hexaly を使ったヒューリスティック

Hexaly の外部関数最適化機能を用いた定式化を紹介する.
Weighted Majority Merge アルゴリズムにおいて次の文字を選択する基準は各文字列に対する残長の和であった.
その残長の部分を Hexaly の決定変数で置き換える.

**決定変数**

- $w_{ij} \in \mathbb{N}$: 文字列 $s_i$ の $j$ 文字目の重み. $(i \in \{ 1, \dots, n \}, \ j \in \{ 1, \dots, |s_i| \})$
    - $w_i = \{ w_{i,1} \dots, w_{i,|s_i|} \}$ とおく.


**目的関数**

下記のアルゴリズムに従って構築した共通超配列の長さを目的関数とする.

- 解 $\mathrm{sol}$ を空文字列で初期化する.
- 各文字 $c$ に対して重み $\sum_{i=1, \ s_i[0] = c}^n w_{i,1}$ を計算し, 重みが最大である $c$ を求める.
- $\mathrm{sol}$ の後ろに $c$ を追加する.
- 各文字列 $s_i \ (i \in \{ 1, \dots, n \})$ に対し, 先頭の文字が $c$ である場合は
    - $s_i$ の先頭の文字を削除する.
    - $w_i$ の先頭の重みを削除し, インデックスを前に詰める.
- $s_1, \dots, s_n$ 全てが空文字列になれば終了. $\mathrm{sol}$ が解.

In [ ]:
```python
class Model:
    def __init__(self, instance, initial: bool = False):
        chars = sorted(list(set("".join(instance))))

        hxoptimizer = hexaly.optimizer.HexalyOptimizer()
        hxmodel = hxoptimizer.model

        max_weight = max(len(s) for s in instance) if initial else len(chars)
        priorities1d = [
            hxmodel.int(1, max_weight) for s in instance for cidx, _ in enumerate(s)
        ]

        func = hxmodel.create_int_external_function(self.objective)
        func.external_context.lower_bound = 0
        func.external_context.upper_bound = sum(len(s) for s in instance)

        indices_1d_to_2d = []
        counter = 0
        for s in instance:
            indices_1d_to_2d.append((counter, counter + len(s)))
            counter += len(s)

        self.instance = instance
        self.chars = chars
        self.hxoptimizer = hxoptimizer
        self.hxmodel = hxmodel
        self.priorities1d = priorities1d
        self.indices_1d_to_2d = indices_1d_to_2d

        # これらが実行される時点で self.* が必要になるため初期化の最後に移動

        hxmodel.minimize(func(*priorities1d))
        hxmodel.close()

        if initial:
            priorities2d = self.priorities_1d_to_2d(priorities1d)
            for sidx, s in enumerate(instance):
                for cidx, c in enumerate(s):
                    priorities2d[sidx][cidx].set_value(len(s) - cidx)

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        if time_limit is not None:
            self.hxoptimizer.param.time_limit = time_limit
        self.hxoptimizer.param.verbosity = 1 if log else 0
        self.hxoptimizer.solve()
        return self

    def to_solution(self) -> str | None:
        status = self.hxoptimizer.solution.status
        if status not in {
            hexaly.optimizer.HxSolutionStatus.OPTIMAL,
            hexaly.optimizer.HxSolutionStatus.FEASIBLE,
        }:
            return None

        priorities1d_value = [priority.value for priority in self.priorities1d]
        priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
        return self.wmm(priorities2d_value)

    def wmm(self, priorities2d: list[list[int]]) -> str:
        indices = [0] * len(self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(len(self.instance) * max(len(s) for s in self.instance)):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                sum(
                    priorities2d[sidx][idx]
                    for sidx, (idx, s) in enumerate(zip(indices, self.instance))
                    if idx < len(s) and s[idx] == c
                )
                for c in self.chars
            ]
            next_char = self.chars[counts.index(max(counts))]

            solution += next_char
            indices = [
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(indices, self.instance)
            ]

        return solution

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [priorities1d[start:end] for start, end in self.indices_1d_to_2d]

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d.get(i) for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)
```

In [ ]:
```python
def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
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
> [  0 sec,       0 itr]:           74
> [ optimality gap     ]:      100.00%
> [  1 sec,     306 itr]:           69
> [  2 sec,    1059 itr]:           64
> [  3 sec,    1882 itr]:           63
> [  4 sec,    2686 itr]:           62
> [  5 sec,    3530 itr]:           62
> [  6 sec,    4379 itr]:           62
> [  7 sec,    5188 itr]:           62
> [  8 sec,    6023 itr]:           62
> [  9 sec,    6825 itr]:           62
> [ 10 sec,    7611 itr]:           62
> [ optimality gap     ]:      100.00%
> [ 11 sec,    8413 itr]:           62
> [ 12 sec,    9207 itr]:           62
> [ 13 sec,   10025 itr]:           62
> [ 14 sec,   10879 itr]:           62
> [ 15 sec,   11725 itr]:           62
> [ 16 sec,   12576 itr]:           62
> [ 17 sec,   13367 itr]:           62
> [ 18 sec,   14160 itr]:           62
> [ 19 sec,   14989 itr]:           62
> [ 20 sec,   15783 itr]:           62
> [ optimality gap     ]:      100.00%
> [ 21 sec,   16533 itr]:           62
> [ 22 sec,   17359 itr]:           62
> [ 23 sec,   18154 itr]:           62
> [ 24 sec,   18964 itr]:           62
> [ 25 sec,   19776 itr]:           62
> [ 26 sec,   20568 itr]:           62
> [ 27 sec,   21407 itr]:           62
> [ 28 sec,   22249 itr]:           62
> [ 29 sec,   23083 itr]:           62
> [ 30 sec,   23895 itr]:           62
> [ optimality gap     ]:      100.00%
> [ 31 sec,   24694 itr]:           62
> [ 32 sec,   25528 itr]:           62
> [ 33 sec,   26368 itr]:           62
> [ 34 sec,   27206 itr]:           62
> [ 35 sec,   28012 itr]:           62
> [ 36 sec,   28846 itr]:           62
> [ 37 sec,   29640 itr]:           62
> [ 38 sec,   30451 itr]:           62
> [ 39 sec,   31268 itr]:           62
> [ 40 sec,   32088 itr]:           62
> [ optimality gap     ]:      100.00%
> [ 41 sec,   32895 itr]:           62
> [ 42 sec,   33723 itr]:           62
> [ 43 sec,   34548 itr]:           62
> [ 44 sec,   35336 itr]:           62
> [ 45 sec,   36138 itr]:           62
> [ 46 sec,   36945 itr]:           62
> [ 47 sec,   37732 itr]:           62
> [ 48 sec,   38540 itr]:           62
> [ 49 sec,   39367 itr]:           62
> [ 50 sec,   40177 itr]:           62
> [ optimality gap     ]:      100.00%
> [ 51 sec,   40989 itr]:           62
> [ 52 sec,   41826 itr]:           62
> [ 53 sec,   42665 itr]:           62
> [ 54 sec,   43469 itr]:           62
> [ 55 sec,   44258 itr]:           62
> [ 56 sec,   45064 itr]:           62
> [ 57 sec,   45868 itr]:           62
> [ 58 sec,   46646 itr]:           62
> [ 59 sec,   47438 itr]:           62
> [ 60 sec,   48234 itr]:           62
> [ optimality gap     ]:      100.00%
> [ 60 sec,   48234 itr]:           62
> [ optimality gap     ]:      100.00%
> 
> 48234 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           62
>   gap    =      100.00%
>   bounds =            0
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
> --- Solution (of length 62) ---
>  Sol: tkulcigneycojiqfsovoazpkuhmplxnhtqgbxzrddbxcvsxuqpvissbxrvnngf
> str1: tk----gn---------------kuhmp-xnhtqg-xz------v-x----is---------
> str2: -----i-----ojiqf-o----------l-n----bx-----xcvs-uqpvissbx-----f
> str3: --ulci-n-yco----sovo-zp----pl--------------------p------------
> str4: -----ig-e---------v-az------------gb--rddb-c-s----v-----rvnngf
> 
> solution is feasible: True
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
> [  0 sec,       0 itr]:          148
> [ optimality gap     ]:      100.00%
> [  1 sec,     236 itr]:          115
> [  2 sec,     561 itr]:          113
> [  3 sec,     889 itr]:          111
> [  4 sec,    1212 itr]:          108
> [  5 sec,    1542 itr]:          107
> [  6 sec,    1894 itr]:          106
> [  7 sec,    2234 itr]:          106
> [  8 sec,    2559 itr]:          106
> [  9 sec,    2907 itr]:          105
> [ 10 sec,    3274 itr]:          105
> [ optimality gap     ]:      100.00%
> [ 11 sec,    3636 itr]:          104
> [ 12 sec,    3967 itr]:          104
> [ 13 sec,    4312 itr]:          103
> [ 14 sec,    4658 itr]:          103
> [ 15 sec,    4995 itr]:          103
> [ 16 sec,    5294 itr]:          102
> [ 17 sec,    5669 itr]:          102
> [ 18 sec,    6025 itr]:          102
> [ 19 sec,    6368 itr]:          102
> [ 20 sec,    6710 itr]:          102
> [ optimality gap     ]:      100.00%
> [ 21 sec,    7065 itr]:          102
> [ 22 sec,    7427 itr]:          102
> [ 23 sec,    7773 itr]:          102
> [ 24 sec,    8105 itr]:          102
> [ 25 sec,    8405 itr]:          102
> [ 26 sec,    8763 itr]:          102
> [ 27 sec,    9123 itr]:          102
> [ 28 sec,    9467 itr]:          102
> [ 29 sec,    9820 itr]:          102
> [ 30 sec,   10161 itr]:          102
> [ optimality gap     ]:      100.00%
> [ 31 sec,   10527 itr]:          102
> [ 32 sec,   10872 itr]:          102
> [ 33 sec,   11233 itr]:          102
> [ 34 sec,   11589 itr]:          102
> [ 35 sec,   11949 itr]:          102
> [ 36 sec,   12284 itr]:          102
> [ 37 sec,   12620 itr]:          102
> [ 38 sec,   12963 itr]:          102
> [ 39 sec,   13306 itr]:          102
> [ 40 sec,   13677 itr]:          102
> [ optimality gap     ]:      100.00%
> [ 41 sec,   14013 itr]:          102
> [ 42 sec,   14316 itr]:          102
> [ 43 sec,   14644 itr]:          102
> [ 44 sec,   15004 itr]:          102
> [ 45 sec,   15358 itr]:          102
> [ 46 sec,   15708 itr]:          102
> [ 47 sec,   16014 itr]:          102
> [ 48 sec,   16363 itr]:          102
> [ 49 sec,   16684 itr]:          102
> [ 50 sec,   17028 itr]:          102
> [ optimality gap     ]:      100.00%
> [ 51 sec,   17368 itr]:          102
> [ 52 sec,   17719 itr]:          102
> [ 53 sec,   18069 itr]:          102
> [ 54 sec,   18394 itr]:          102
> [ 55 sec,   18727 itr]:          102
> [ 56 sec,   19075 itr]:          102
> [ 57 sec,   19435 itr]:          102
> [ 58 sec,   19782 itr]:          102
> [ 59 sec,   20114 itr]:          102
> [ 60 sec,   20467 itr]:          102
> [ optimality gap     ]:      100.00%
> [ 60 sec,   20467 itr]:          102
> [ optimality gap     ]:      100.00%
> 
> 20467 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          102
>   gap    =      100.00%
>   bounds =            0
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
> --- Solution (of length 102) ---
>  Sol: ipuyplrogenbdcevadzfxwgbjtinyucvxerdpmqfozkrdbrlcsovgtondfkuibhtmpxrvnhntqgxzpcvxwdsubroqpvisslbxfbhep
> str1: -------------------------t----------------k---------g--n--ku--h-mpx--nh-tqgxz--vx----------is---------
> str2: i------o----------------j-i-----------qfo------l-------n-----b----x--------x--cv---su---qpviss-bxf----
> str3: --u--l-------c------------iny-c---------o--------sov--o---------------------zp-----------p----l------p
> str4: i-------ge-----va-z---gb----------rd--------db--cs-v---------------rvn-n--g----------------------f----
> str5: -p-yplr-----------z-x--------uc-----pmq------------vgt--df-ui-------v---------c---ds-b-o--------------
> str6: -p---------bd-ev-d------------cv---dp--f-z-------s--------------m------------------s-broq-v----b--bh--
> str7: ---------enb-c----zf----jt-----vxer------z---br----v--------i-------------g--p----------------l-----e-
> str8: ------r-------------xw----------x-----q---krd-rlc----to-d------tmp-r---------p--xwd-------------------
> 
> solution is feasible: True
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
> [  0 sec,       0 itr]:          198
> [ optimality gap     ]:      100.00%
> [  1 sec,     143 itr]:          172
> [  2 sec,     312 itr]:          170
> [  3 sec,     478 itr]:          169
> [  4 sec,     658 itr]:          169
> [  5 sec,     798 itr]:          168
> [  6 sec,     952 itr]:          168
> [  7 sec,    1109 itr]:          168
> [  8 sec,    1257 itr]:          168
> [  9 sec,    1408 itr]:          165
> [ 10 sec,    1567 itr]:          165
> [ optimality gap     ]:      100.00%
> [ 11 sec,    1721 itr]:          165
> [ 12 sec,    1883 itr]:          164
> [ 13 sec,    2036 itr]:          164
> [ 14 sec,    2182 itr]:          164
> [ 15 sec,    2327 itr]:          163
> [ 16 sec,    2482 itr]:          163
> [ 17 sec,    2634 itr]:          163
> [ 18 sec,    2765 itr]:          163
> [ 19 sec,    2928 itr]:          163
> [ 20 sec,    3077 itr]:          163
> [ optimality gap     ]:      100.00%
> [ 21 sec,    3226 itr]:          163
> [ 22 sec,    3380 itr]:          163
> [ 23 sec,    3528 itr]:          163
> [ 24 sec,    3687 itr]:          163
> [ 25 sec,    3842 itr]:          163
> [ 26 sec,    3976 itr]:          162
> [ 27 sec,    4102 itr]:          162
> [ 28 sec,    4248 itr]:          161
> [ 29 sec,    4394 itr]:          161
> [ 30 sec,    4543 itr]:          161
> [ optimality gap     ]:      100.00%
> [ 31 sec,    4698 itr]:          161
> [ 32 sec,    4835 itr]:          161
> [ 33 sec,    4987 itr]:          161
> [ 34 sec,    5136 itr]:          161
> [ 35 sec,    5298 itr]:          161
> [ 36 sec,    5452 itr]:          161
> [ 37 sec,    5597 itr]:          161
> [ 38 sec,    5741 itr]:          161
> [ 39 sec,    5874 itr]:          161
> [ 40 sec,    6020 itr]:          161
> [ optimality gap     ]:      100.00%
> [ 41 sec,    6183 itr]:          161
> [ 42 sec,    6329 itr]:          160
> [ 43 sec,    6490 itr]:          160
> [ 44 sec,    6634 itr]:          160
> [ 45 sec,    6762 itr]:          158
> [ 46 sec,    6894 itr]:          158
> [ 47 sec,    7053 itr]:          158
> [ 48 sec,    7187 itr]:          158
> [ 49 sec,    7339 itr]:          157
> [ 50 sec,    7472 itr]:          157
> [ optimality gap     ]:      100.00%
> [ 51 sec,    7628 itr]:          157
> [ 52 sec,    7773 itr]:          157
> [ 53 sec,    7927 itr]:          157
> [ 54 sec,    8085 itr]:          156
> [ 55 sec,    8226 itr]:          156
> [ 56 sec,    8365 itr]:          156
> [ 57 sec,    8510 itr]:          156
> [ 58 sec,    8659 itr]:          156
> [ 59 sec,    8814 itr]:          156
> [ 60 sec,    8961 itr]:          155
> [ optimality gap     ]:      100.00%
> [ 60 sec,    8961 itr]:          155
> [ optimality gap     ]:      100.00%
> 
> 8961 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          155
>   gap    =      100.00%
>   bounds =            0
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
> --- Solution (of length 155) ---
>   Sol: irkxuplcwsexqakrdinyfshtxpabcojivbnucdgevzqfkaolrzgpnkbxqujtvxerzqcedcvdwbhcsvrvantfigpmlcqvgtdijfuowqpvoiszsbxpaknhmiuvdcdtqgxfbezhksbkroqvbbhmprlgpxwydis
> str01: -----------------------t--------------------k-----g-nk---u----------------h------------m--------------p-------x---nh-------tqgx---z--------v---------x---is
> str02: i----------------------------oji----------qf--ol----n-bx-----x----c---v-----s---------------------u--qpv-is-sbx----------------f---------------------------
> str03: ----u-lc---------iny--------co----------------------------------------------s----------------------o---vo--z---p--------------------------------p-l-p------
> str04: i-------------------------------------gev----a---zg---b--------r----d--d-b-csvrv-n--------------------------------n----------g-f---------------------------
> str05: -----p-------------y-----p---------------------lrz-----x-u--------c-------------------pm--qvgtd--fu------i-------------v-cd----------sb--o-----------------
> str06: -----p---------------------b---------d-ev---------------------------dcvd--------------p----------f---------zs-------m----------------sb-roqvbbh------------
> str07: ----------e-------n--------bc------------z-f--------------jtvxerz--------b----rv----igp-l----------------------------------------e-------------------------
> str08: -r-x----w--xq-krd-------------------------------r---------------------------------------lc---t-----o--------------------d--t-------------------mpr--pxw-d--
> str09: --k-----------k---------------------------q--a-------------------------------------fig----q-----j---w---o--------k------------------ks-kr---b-----lg-------
> str10: ------l----x------------xpab---ivb------vz--k-o--z--------------z-----vd-----------------------------------------------------------------------------------
> str11: --k------------r-i--fs----a-----v-n-cd----q-----------------------------w-h--------------------------------z-------------c---------------------------------
> str12: ------------qa----------x----------u-dg---q-----------------v----qce----wb---------f-g---------ij--ow-------------------------------------------------wy---
> str13: -r-------s-xq-----------------j---n--------f-------p----------------------------a-------------di--u-------s----------i------q---bezhk----o----hm---g-------
> str14: i-------ws------------h---------v-----------------------------------------hc-----------------------o----------------miuvd-d--------------------m-----------
> str15: ----------------------htx------------------------------xq-j-----zq-------b-c------t--------------------------b--akn----------------------------------------
> str16: ---xu----s----------f-------c--------------f-----z-p----------e----e-cv-w-------antf---m----g--------q-----z----------u------------------------------------
> 
> solution is feasible: True
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
> [  1 sec,    3172 itr]:           29
> [  2 sec,    6390 itr]:           29
> [  3 sec,    9590 itr]:           29
> [  4 sec,   12739 itr]:           29
> [  5 sec,   15842 itr]:           29
> [  6 sec,   18940 itr]:           29
> [  7 sec,   22131 itr]:           29
> [  8 sec,   25303 itr]:           29
> [  9 sec,   28478 itr]:           28
> [ 10 sec,   31685 itr]:           28
> [ optimality gap     ]:      100.00%
> [ 11 sec,   34959 itr]:           28
> [ 12 sec,   38206 itr]:           28
> [ 13 sec,   41452 itr]:           28
> [ 14 sec,   44674 itr]:           28
> [ 15 sec,   47819 itr]:           28
> [ 16 sec,   51052 itr]:           28
> [ 17 sec,   54315 itr]:           28
> [ 18 sec,   57497 itr]:           27
> [ 19 sec,   60808 itr]:           27
> [ 20 sec,   64041 itr]:           27
> [ optimality gap     ]:      100.00%
> [ 21 sec,   67273 itr]:           27
> [ 22 sec,   70530 itr]:           27
> [ 23 sec,   73730 itr]:           27
> [ 24 sec,   77043 itr]:           27
> [ 25 sec,   80338 itr]:           27
> [ 26 sec,   83668 itr]:           27
> [ 27 sec,   86997 itr]:           27
> [ 28 sec,   90317 itr]:           27
> [ 29 sec,   93494 itr]:           27
> [ 30 sec,   96728 itr]:           27
> [ optimality gap     ]:      100.00%
> [ 31 sec,  100035 itr]:           27
> [ 32 sec,  103347 itr]:           27
> [ 33 sec,  106583 itr]:           27
> [ 34 sec,  109811 itr]:           27
> [ 35 sec,  112946 itr]:           27
> [ 36 sec,  116148 itr]:           27
> [ 37 sec,  119474 itr]:           27
> [ 38 sec,  122738 itr]:           27
> [ 39 sec,  126017 itr]:           27
> [ 40 sec,  129258 itr]:           27
> [ optimality gap     ]:      100.00%
> [ 41 sec,  132469 itr]:           27
> [ 42 sec,  135804 itr]:           27
> [ 43 sec,  139140 itr]:           27
> [ 44 sec,  142513 itr]:           27
> [ 45 sec,  145924 itr]:           27
> [ 46 sec,  149357 itr]:           27
> [ 47 sec,  152633 itr]:           27
> [ 48 sec,  155954 itr]:           27
> [ 49 sec,  159243 itr]:           27
> [ 50 sec,  162497 itr]:           27
> [ optimality gap     ]:      100.00%
> [ 51 sec,  165793 itr]:           27
> [ 52 sec,  169114 itr]:           27
> [ 53 sec,  172452 itr]:           27
> [ 54 sec,  175797 itr]:           27
> [ 55 sec,  179147 itr]:           27
> [ 56 sec,  182532 itr]:           27
> [ 57 sec,  185931 itr]:           27
> [ 58 sec,  189244 itr]:           27
> [ 59 sec,  192583 itr]:           27
> [ 60 sec,  195905 itr]:           27
> [ optimality gap     ]:      100.00%
> [ 60 sec,  195905 itr]:           27
> [ optimality gap     ]:      100.00%
> 
> 195905 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           27
>   gap    =      100.00%
>   bounds =            0
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
> [  0 sec,       0 itr]:           36
> [ optimality gap     ]:      100.00%
> [  1 sec,     876 itr]:           35
> [  2 sec,    1745 itr]:           34
> [  3 sec,    2606 itr]:           34
> [  4 sec,    3476 itr]:           34
> [  5 sec,    4326 itr]:           34
> [  6 sec,    5185 itr]:           34
> [  7 sec,    6053 itr]:           34
> [  8 sec,    6937 itr]:           34
> [  9 sec,    7776 itr]:           34
> [ 10 sec,    8637 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 11 sec,    9466 itr]:           34
> [ 12 sec,   10305 itr]:           34
> [ 13 sec,   11126 itr]:           34
> [ 14 sec,   11990 itr]:           34
> [ 15 sec,   12821 itr]:           34
> [ 16 sec,   13679 itr]:           34
> [ 17 sec,   14515 itr]:           34
> [ 18 sec,   15295 itr]:           34
> [ 19 sec,   16135 itr]:           34
> [ 20 sec,   17007 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 21 sec,   17873 itr]:           34
> [ 22 sec,   18696 itr]:           34
> [ 23 sec,   19499 itr]:           34
> [ 24 sec,   20336 itr]:           34
> [ 25 sec,   21169 itr]:           34
> [ 26 sec,   22025 itr]:           34
> [ 27 sec,   22855 itr]:           34
> [ 28 sec,   23663 itr]:           34
> [ 29 sec,   24536 itr]:           34
> [ 30 sec,   25379 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 31 sec,   26207 itr]:           34
> [ 32 sec,   27070 itr]:           34
> [ 33 sec,   27901 itr]:           34
> [ 34 sec,   28694 itr]:           34
> [ 35 sec,   29553 itr]:           34
> [ 36 sec,   30344 itr]:           34
> [ 37 sec,   31169 itr]:           34
> [ 38 sec,   32031 itr]:           34
> [ 39 sec,   32870 itr]:           34
> [ 40 sec,   33730 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 41 sec,   34571 itr]:           34
> [ 42 sec,   35412 itr]:           34
> [ 43 sec,   36227 itr]:           34
> [ 44 sec,   37043 itr]:           34
> [ 45 sec,   37867 itr]:           34
> [ 46 sec,   38692 itr]:           34
> [ 47 sec,   39530 itr]:           34
> [ 48 sec,   40404 itr]:           34
> [ 49 sec,   41251 itr]:           34
> [ 50 sec,   42104 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 51 sec,   42944 itr]:           34
> [ 52 sec,   43796 itr]:           34
> [ 53 sec,   44627 itr]:           34
> [ 54 sec,   45493 itr]:           34
> [ 55 sec,   46300 itr]:           34
> [ 56 sec,   47129 itr]:           34
> [ 57 sec,   47940 itr]:           34
> [ 58 sec,   48778 itr]:           34
> [ 59 sec,   49624 itr]:           34
> [ 60 sec,   50486 itr]:           34
> [ optimality gap     ]:      100.00%
> [ 60 sec,   50486 itr]:           34
> [ optimality gap     ]:      100.00%
> 
> 50486 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           34
>   gap    =      100.00%
>   bounds =            0
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
>   Sol: daecbdeabecdabcedaecbdaebcdeabacde
> str01: d--cb-----c---c-d---b----c-----c-e
> str02: ----bd-----d-b-e--e----e---e-b--d-
> str03: ---c---a--cd---e--ec---eb--e------
> str04: -ae--d-----d----d----d-eb-d-----d-
> str05: -a-cb-e--ec-abce------------------
> str06: ----b---b---ab-e----bd---c---ba---
> str07: ----b---b---a--e-ae-b-a---d-a-----
> str08: --e---e--e-----e---cbd--b--e-----e
> str09: ---c------cd---e--e--da---d----cd-
> str10: ----bd-ab--d-b-e-a----a---d-------
> str11: --e--de----da----a----ae----a-a---
> str12: -a-----a-e--a----a--b--e---ea--c--
> str13: --e----a----abc--a-c-----cd--b----
> str14: ----bde--e--a---d-e---a---de------
> str15: ---c---a-e-da---d-e----e---e----d-
> str16: --e-b-----c-a---d---b-a-b----b---e
> str17: d----d----c----e--e---a-b-dea-----
> str18: da--b-----cd----d-e---ae-c--------
> str19: -a-----a---d--ce--e--da-----ab----
> str20: -ae---e---c---ce--e----e----a-a---
> str21: ----b---b--da--e---c--a-----a---de
> str22: da-c--e----da--eda--b-------------
> str23: -a-----a-e--ab------b---b----b-c-e
> str24: d-e--d--b-c--bc--a----a-b---------
> str25: d---bd-a----a--e----b---bc---b----
> str26: d-e-b-e----d-b-e----b-a--c--------
> str27: ---c--e--e---bc-d--cbd-e----------
> str28: d---b-e----da----a---da-----ab----
> str29: ---c------c---c-d--cb--eb-d----c--
> str30: -ae---ea--cd-bc-----bd------------
> str31: da-cb-ea--c---c----c-d------------
> str32: --ec--e-b-c---c-d---bd--b---------
> str33: d----d--b----bceda--b---b---------
> str34: -a-----a-e--ab---a----aeb---a-----
> str35: --ecb---b-c-a----a---d---cd-------
> str36: d-e-b-----c---ce---c-d--bc--------
> str37: da-----a--c--b---ae----ebc--------
> str38: -a---d-abe--a----a-c-----c-e------
> str39: daec-d--b---a-c--a----a-----------
> str40: da-cb---b--d--ced--c--------------
> str41: d-e--d--be-----e----b---b-de------
> str42: ---c-d-a---d--c-d--c-da-----a-----
> str43: ---c--e--e-d--c-----b-ae---e----d-
> str44: ---c--ea-ec-a----a----a--c--a-----
> str45: d--c------c---ce----b---b----ba-d-
> str46: ----b--a-e-----e-ae-b---b-de------
> str47: d---bde-b---a-c----c-d--b---------
> str48: --e-b-----c--b-e--e--dae----a-----
> str49: -ae---e--e---b------bd--bc--a-----
> str50: d---bd-ab-c----e---cb---b---------
> 
> solution is feasible: True
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
> [  0 sec,       0 itr]:           27
> [ optimality gap     ]:      100.00%
> [  1 sec,    4220 itr]:           24
> [  2 sec,    8437 itr]:           24
> [  3 sec,   12578 itr]:           24
> [  4 sec,   16588 itr]:           24
> [  5 sec,   20565 itr]:           24
> [  6 sec,   24635 itr]:           24
> [  7 sec,   28705 itr]:           24
> [  8 sec,   32649 itr]:           24
> [  9 sec,   36627 itr]:           24
> [ 10 sec,   40829 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 11 sec,   44923 itr]:           24
> [ 12 sec,   49048 itr]:           24
> [ 13 sec,   53126 itr]:           24
> [ 14 sec,   57118 itr]:           24
> [ 15 sec,   61175 itr]:           24
> [ 16 sec,   65258 itr]:           24
> [ 17 sec,   69413 itr]:           24
> [ 18 sec,   73467 itr]:           24
> [ 19 sec,   77539 itr]:           24
> [ 20 sec,   81511 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 21 sec,   85578 itr]:           24
> [ 22 sec,   89584 itr]:           24
> [ 23 sec,   93650 itr]:           24
> [ 24 sec,   97507 itr]:           24
> [ 25 sec,  101307 itr]:           24
> [ 26 sec,  105043 itr]:           24
> [ 27 sec,  108730 itr]:           24
> [ 28 sec,  112720 itr]:           24
> [ 29 sec,  116874 itr]:           24
> [ 30 sec,  121009 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 31 sec,  125137 itr]:           24
> [ 32 sec,  129182 itr]:           24
> [ 33 sec,  133288 itr]:           24
> [ 34 sec,  137374 itr]:           24
> [ 35 sec,  141435 itr]:           24
> [ 36 sec,  145444 itr]:           24
> [ 37 sec,  149486 itr]:           24
> [ 38 sec,  153561 itr]:           24
> [ 39 sec,  157571 itr]:           24
> [ 40 sec,  161655 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 41 sec,  165779 itr]:           24
> [ 42 sec,  169879 itr]:           24
> [ 43 sec,  174008 itr]:           24
> [ 44 sec,  178113 itr]:           24
> [ 45 sec,  182132 itr]:           24
> [ 46 sec,  186250 itr]:           24
> [ 47 sec,  190476 itr]:           24
> [ 48 sec,  194509 itr]:           24
> [ 49 sec,  198625 itr]:           24
> [ 50 sec,  202698 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 51 sec,  206763 itr]:           24
> [ 52 sec,  210818 itr]:           24
> [ 53 sec,  214827 itr]:           24
> [ 54 sec,  219000 itr]:           24
> [ 55 sec,  223082 itr]:           24
> [ 56 sec,  227412 itr]:           24
> [ 57 sec,  231847 itr]:           24
> [ 58 sec,  236234 itr]:           24
> [ 59 sec,  240622 itr]:           24
> [ 60 sec,  245038 itr]:           24
> [ optimality gap     ]:      100.00%
> [ 60 sec,  245038 itr]:           24
> [ optimality gap     ]:      100.00%
> 
> 245038 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           24
>   gap    =      100.00%
>   bounds =            0
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
>   Sol: TCATGACCGTAGATCAGTACGATC
> str01: --ATG---G--GAT-A---CG---
> str02: --AT-ACC-T---TC----C---C
> str03: -CA---C-G-A-AT---T--GA--
> str04: T-A--A----A-ATC--T--G-T-
> str05: --A-G---GTA-A-CA--A--A--
> str06: T--T--CC-TAG----GTA-----
> str07: T--TG----TAGATC--T------
> str08: T---G---G--GA--AGT----TC
> str09: T--T--CC--A---CA--AC--T-
> str10: TC-T-A----A-A-C-G-A--A--
> 
> solution is feasible: True
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
> [  0 sec,       0 itr]:          150
> [ optimality gap     ]:      100.00%
> [  1 sec,     259 itr]:          141
> [  2 sec,     526 itr]:          141
> [  3 sec,     759 itr]:          138
> [  4 sec,     993 itr]:          138
> [  5 sec,    1245 itr]:          138
> [  6 sec,    1463 itr]:          138
> [  7 sec,    1682 itr]:          138
> [  8 sec,    1909 itr]:          138
> [  9 sec,    2119 itr]:          138
> [ 10 sec,    2287 itr]:          138
> [ optimality gap     ]:      100.00%
> [ 11 sec,    2486 itr]:          138
> [ 12 sec,    2638 itr]:          138
> [ 13 sec,    2805 itr]:          138
> [ 14 sec,    2995 itr]:          138
> [ 15 sec,    3153 itr]:          138
> [ 16 sec,    3333 itr]:          138
> [ 17 sec,    3488 itr]:          138
> [ 18 sec,    3653 itr]:          138
> [ 19 sec,    3819 itr]:          138
> [ 20 sec,    4009 itr]:          138
> [ optimality gap     ]:      100.00%
> [ 21 sec,    4200 itr]:          138
> [ 22 sec,    4401 itr]:          138
> [ 23 sec,    4590 itr]:          138
> [ 24 sec,    4789 itr]:          138
> [ 25 sec,    4982 itr]:          138
> [ 26 sec,    5144 itr]:          138
> [ 27 sec,    5315 itr]:          138
> [ 28 sec,    5479 itr]:          138
> [ 29 sec,    5615 itr]:          138
> [ 30 sec,    5743 itr]:          138
> [ optimality gap     ]:      100.00%
> [ 31 sec,    5865 itr]:          138
> [ 32 sec,    6021 itr]:          138
> [ 33 sec,    6174 itr]:          138
> [ 34 sec,    6343 itr]:          138
> [ 35 sec,    6506 itr]:          138
> [ 36 sec,    6666 itr]:          138
> [ 37 sec,    6828 itr]:          138
> [ 38 sec,    6990 itr]:          138
> [ 39 sec,    7167 itr]:          138
> [ 40 sec,    7357 itr]:          138
> [ optimality gap     ]:      100.00%
> [ 41 sec,    7525 itr]:          138
> [ 42 sec,    7688 itr]:          138
> [ 43 sec,    7856 itr]:          138
> [ 44 sec,    8002 itr]:          138
> [ 45 sec,    8187 itr]:          137
> [ 46 sec,    8353 itr]:          137
> [ 47 sec,    8498 itr]:          137
> [ 48 sec,    8673 itr]:          137
> [ 49 sec,    8846 itr]:          136
> [ 50 sec,    9024 itr]:          136
> [ optimality gap     ]:      100.00%
> [ 51 sec,    9168 itr]:          136
> [ 52 sec,    9313 itr]:          136
> [ 53 sec,    9456 itr]:          136
> [ 54 sec,    9589 itr]:          136
> [ 55 sec,    9751 itr]:          136
> [ 56 sec,    9916 itr]:          136
> [ 57 sec,   10055 itr]:          136
> [ 58 sec,   10183 itr]:          136
> [ 59 sec,   10319 itr]:          136
> [ 60 sec,   10463 itr]:          136
> [ optimality gap     ]:      100.00%
> [ 60 sec,   10463 itr]:          136
> [ optimality gap     ]:      100.00%
> 
> 10463 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          136
>   gap    =      100.00%
>   bounds =            0
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
> --- Solution (of length 136) ---
>   Sol: ATGACTGACGTAACGTACATGCATCATGCATCGATCGATCAGTCATCGATGCAGCTACAGATCAGCTAGTCATCGATCAGTACGCATAGCTGATCAGTCGATCTGATCGATCAGTCAGTCATCGACCTGATGCTAR
> str01: -T-A--G---TA--GTA---G-A-C-T-C--CG---GA--AGT----GA--CA---A-A---C--C----C-T-GA--A--A---A--G---A--A-T-G----GAT--A--A---A-T-AT--A-----------
> str02: --G---GA--TAA---ACA--C-TC---C--CGA---A--A---AT--A---A--T-----T----T-G--A-C--T---TA---A-A-C--A--A--CG--C-GA-C-A---GT---TCA---A---G-------
> str03: AT-AC---C-T----T-C---C-T-A-G----G-T--A--A--CA---A---A-C--CA-A-C--C-A---A-C--T---T-----T---TGATC--TC--T-TG-T--A---G--A-TC-T-G------------
> str04: -T-A---A---A---T---T--AT-A---ATC--T---T-A-T-A-C--T--AG-TA-A-A--A---A---AT--A---G---G----G-TG-T-A----A-C----CGA--A---A---A-CG----G-T-C---
> str05: -T---T-A---AA---ACA-GC--C-TG--T-G---G----GT--T-G---CA-C--C----CA-CT---CA-C-A---G---G----GC----C---C-A-CTG---G----G-C-G-CA---A---G-------
> str06: ATGACT----T--C---CA---AT---G----GATC---C---CA---A--C--CT-CA-A---GCT--TC--C-A-C----C-C----C--A--A-T-G----G-T---T---TCAG-C----------------
> str07: A--AC--A---AAC---CA---A-C---CA---A-C--T---T--T---TG-A--T-C---TC---T--T----G-T-AG-A----T--CTG-T---TC--TCT-A---A--A--C-G--A---AC----------
> str08: ATGA---A---AACG-A-A---A--AT---T--AT---T-A-TCA---A-G--G-----G-T-A--T-G-----GA--AGT--G----G---A--AG-C--T--GA-CGA--A---A-T-----------------
> str09: A---CT--CG----G--C-TGCAT---GC-T---T--A---GT----G---CA-CT-CA---C-GC-AGT-AT--A--A-T-----TA----AT-A----A-CT-A---AT---T-A-------------------
> str10: -T---TG---TA--G-A--T-C-T---G--T---TC--TC--T-A---A---A-C----GA--A-CT--T--T--A--A--A---AT--CTG-T--GT-G----G--C--T--GTCA--C-TC-------------
> str11: --G-C--A-G-A--G--CAT---T--T---TC--T--A--A-T-ATC----CA-C-A-A-A--A--T-G--A---A---G---GCA-A--T-A--A-T---T--G-T--A-C--T-A--C-TC-------------
> str12: ATGA--G-C----C--A-A-G-ATC---C---GA-CGA--AG--A--G---C--C--C----CA---AG-----GA---G---G-A--G---A--AG--GA---G---G----G--A--C--C--CC-----C---
> str13: -T--CT--C--A-C--A---G--T--T-CA---A--GA--A--C--C----CA---A-AG-T-A-C----C--C---C----C-CATAGC----C---C--TCT--T--A--A---AG-C--C-AC----------
> str14: A-G---G---T----T---T--AT-A--C--C--T---TC---C-T--A-G--G-TA-A---CA---A---A-C---CA--AC-CA-A-CT--T---TCGATCT---C--T---T--GT-A---------------
> str15: A-G---G---T----T---T--AT-A--C--C--T---TC---C--C-A-G--G-TA-A---CA---A---A-C---CA--AC-CA-A-CT--T---TCGATCT---C--T---T--GT-A---------------
> str16: -T-A---A---AAC--A-A--C-TCA---AT--A-C-A--A--CAT--A---AG--A-A-A--A--T---CA---A-C-G--C--A-A----A--A----A-C--A-C--TCA--CA---A---A-----------
> str17: ----C---CG---C---C---CAT--T---T-G---G----G-C---G--GC---T-C---TC-G--AG-C---GAT-AG--C---T--C-G-TC-G---A----ATC---C---C--TC---GACCT--------
> str18: AT-AC---C-T----T-C---C--CA-G----G-T--A--A--CA---A---A-C--CA-A-C--C-A---A-C--T---T-----T--C-GATC--TC--T-TG-T--A---G--A-TC-T-G------------
> str19: -T--CT--C--A-C--A---G--T--T-CA---A--GA--A--C--C--T-CA---A--G-TC---T---C--C---C----C-CATAG--G--C---C--TCT--T---TCAGTCAG------------------
> str20: --GA-T--C-T--C-T-C-T-CA-C---C---GA---A-C---C-T-G--GC--C--C----C-G---G-----G--CA--A---AT-GC----C---C--T---A---ATC---CAG--A--G----G-TG----
> str21: A-GA--G-C--AA--T-CA-G--T---GCATC-A--GA--A---AT--AT--A-C--C---T-A--T--T-AT--A-CA---C---T---T--T--G-C--T---A---A---G--A---AT--------------
> str22: A--A-T----TAA---A-A--CATC-T-CA---AT--A-CA---A-C-AT--A---A--GA--A---A---A---A-CA--ACGCA-A----A--A----A-C--A-C--TCA-T---------------------
> str23: A--A---ACG-AAC-T---T---T-A---A---A---ATC--T----G-TG----T---G----GCT-GTCA-C--TC-G---GC-T-GC--AT--G-C--T-T-A--G-T--G-C--------------------
> str24: AT-A---AC-TAA--T---T--A-C-TG--TCG-T---T--G--A-C-A-G--G--ACA---C-G--AGT-A---A-C--T-CG--T--CT-ATC--T---TCTG-------------------------------
> str25: ATGA--G---T---GT-CA--C-----G-A---AT---TCA--C---G-T--A-C-A-A--T--G--A---A-C--T--G---G-AT-G-T--TCA--CG-T--G---GA--A-T-A---A---------------
> str26: A---C---CGT---G-----G------GC---GA--G--C-G-----G-TG-A-C--C-G----G-T-GTC-T---TC----C---TAG-TG----G--G-TC----C---CA--C-GT--T-GA----A-----R
> str27: A--A---A-G----GT---T---T-AT--A-C---C--T---TC--C----CAG-----G-T-A---A--CA---A--A---C-CA-A-C----CA----A-CT--T---TC-G--A-TC-TC----T--TG----
> str28: A-G--T-A-GT----T-C--GC--C-TG--T-G-T-GA---G-C-T-GA--CA---A-A---C---T--T-A--G-T-AGT--G--T---T--T--GT-GA---G---GAT---T-A-------------------
> str29: -T---T----TA---TAC---C-T--T-C--C--T--A---G-----G-T--A---ACA-A--A-C----CA---A-C----C--A-A-CT--T---TCGATCT---C--T---T--GT-A--GA--T--------
> str30: ATG-C-G--GT--CGT-C-T-C-TC---C--C---CG----G-C-T---T-----T-----T----T--T--TC---C----C-C---GC-G--C---CG--C-G-T---T--G---G-C---G-CC-GA------
> str31: --G--TGAC--AA---A-A---A-CAT--A---AT-G----G--A-C--T-C--C-A-A---CA-C----CAT-G-TCA--A-GC-T---T--TCAG--G-T---A--GA-C------------------------
> str32: --G--TG---TAA-G-A-A---A-CA-G--T--A---A---G-C--C----C-G-----GA--AG-T-G-----G-T--GT-----T---T--T--G-CGAT-T--TCGA---G---G-C--CG----G-------
> str33: --GA--GA---A---T----G-A----G--TC--TC-AT---T-A-C----C-GC--C----C-G---GT-A-C--T---TA-GCA-AGCT-A--A-T--A---G-TC-A-C-G---G-C----------------
> str34: ATG--TG--GT--CG-A--TGC--CATG----GA--G----G-C--C----CA-C--CAG-T----T---CAT---T-A--A-G----GCT---C---C--T--G---G--CA-T---T-----------------
> str35: A---C-GA-G---CGT---T---T--T--A---A--G----G-----G---C--C--C-G--C-G--A--C-T-G--C-G-ACG----GC----CA--C-AT--G---G--C---C---C-T-G---T-ATG-T--
> str36: --G---G---T----T---T--AT-A--C--C--T---TC---C--C-A-G--G-TA-A---CA---A---A-C---CA--AC-CA-A-CT--T---TCGATCT---C--T---T--GT-A--G------------
> str37: -TG---G--G-AA-GT---T-C--CA---A---A---A---G--ATC-A--CA---A-A-A-CA-CTA--C--C-A---GT-C--A-A-C----C--T-GA----A--G-T-A--CA--C----------------
> str38: --GA---A-G---CGT---T--A--A--C---G-T-G-T---T----GA-G--G--A-A-A--AG--A--CA--G--C--T-----TAG--GA---G---A----A-C-A--AG--AG-C-T-G----G--G----
> str39: A---C---C--A--G--C--GCA-C-T---TCG---G--CAG-C---G--GCAGC-AC----C---T---C---G----G--C--A--GC--A-C---C--TC--A--G--CAG-CA---A-C-------------
> str40: ATG---G--G-A-C--A-A--C-T--T--AT---TC---C--T-ATC-ATG----T---G--C--C-A---A--GA---G---G--T---T--T---T--A-C----C---C-G---GT----GACC--A------
> str41: -T---TG---TA--G-A--T-C-T---G--T---TC--TC--T-A---A---A-C----GA--A-CT--T--T--A--A--A---AT--CTG-T--GT-G----G-T---T--GTCA--C-TC-------------
> str42: A--AC---C--AAC---CA---A-C-T---T---TCGATC--TC-T---TG----TA--GATC---T-GT--TC--TC--TA---A-A-C-GA--A--C--T-T--T--A--------------------------
> str43: --G---G--GT----T-C-TGC--CA-G----G--C-AT-AGTC-T---T-----T-----T----T--T--TC--T--G---GC---G--G--C---C---CT--T-G-T--GT-A---A---ACCTG-------
> str44: --G---G-C-T---G--CATGC-T--T--A--G-T-G--CA--C-TC-A--C-GC-A--G-T-A--TA---AT---T-A--A----TA----A-C--T--A----AT---T-A--C--T----G---T--------
> str45: -TG-C--A--T---G--C-T---T-A-G--T-G--C-A-C--TCA-CG---CAG-TA----T-A---A-T--T--A--A-TA---A---CT-A--A-T---T---A-C--T--GTC-GT-----------------
> str46: -T---T--C----C--ACA---A-C-T---T---TC---CA--C--C-A---AGCT-C---T--GC-A---A--GATC----C-CA--G---A---GTC-A---G---G----G---G-C--C----TG-T-----
> str47: -T--CT-A---AACG-A-A--C-T--T---T--A---A--A---ATC--TG----T---G-T--G---G-C-T-G-TCA---C---T--C-G----G-C--T--G--C-AT--G-C--T--T--A---G-------
> str48: A---C---CG----G-A--TG------GC--CG--CGAT---T--T---T-----T-C-G----G--AGTC--C--T---T--G----G--G----G--GA-C----C-A-C--TCAG--A---A--T-A-G--A-
> str49: ----CT----T---GTA---G-ATC-TG--T---TC--TC--T-A---A---A-C----GA--A-CT--T--T--A--A--A---AT--CTG-T--GT-G----G--C--T--GTCA--C-T--------------
> str50: ATGA--G-C--A-C-TA-A-GC-----G-A---A--GA--A--C--C-A---A---A-A-A---GC-AG--A-C-A--A-TAC--A-A-C----C---CG--CT-AT---T-A--C--------------------
> 
> solution is feasible: True
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
> [  0 sec,       0 itr]:           62
> [ optimality gap     ]:      100.00%
> [  1 sec,     757 itr]:           48
> [  2 sec,    1607 itr]:           48
> [  3 sec,    2431 itr]:           47
> [  4 sec,    3157 itr]:           47
> [  5 sec,    3924 itr]:           47
> [  6 sec,    4684 itr]:           47
> [  7 sec,    5477 itr]:           46
> [  8 sec,    6311 itr]:           46
> [  9 sec,    7065 itr]:           46
> [ 10 sec,    7963 itr]:           46
> [ optimality gap     ]:      100.00%
> [ 11 sec,    8905 itr]:           46
> [ 12 sec,    9847 itr]:           46
> [ 13 sec,   10762 itr]:           46
> [ 14 sec,   11681 itr]:           46
> [ 15 sec,   12477 itr]:           46
> [ 16 sec,   13308 itr]:           46
> [ 17 sec,   14122 itr]:           46
> [ 18 sec,   14968 itr]:           46
> [ 19 sec,   15843 itr]:           46
> [ 20 sec,   16666 itr]:           45
> [ optimality gap     ]:      100.00%
> [ 21 sec,   17566 itr]:           45
> [ 22 sec,   18414 itr]:           45
> [ 23 sec,   19348 itr]:           45
> [ 24 sec,   20245 itr]:           45
> [ 25 sec,   21179 itr]:           45
> [ 26 sec,   22119 itr]:           45
> [ 27 sec,   23049 itr]:           45
> [ 28 sec,   23996 itr]:           45
> [ 29 sec,   24974 itr]:           45
> [ 30 sec,   25785 itr]:           45
> [ optimality gap     ]:      100.00%
> [ 31 sec,   26598 itr]:           45
> [ 32 sec,   27455 itr]:           45
> [ 33 sec,   28336 itr]:           45
> [ 34 sec,   29209 itr]:           45
> [ 35 sec,   30082 itr]:           44
> [ 36 sec,   30982 itr]:           44
> [ 37 sec,   31885 itr]:           44
> [ 38 sec,   32808 itr]:           44
> [ 39 sec,   33737 itr]:           44
> [ 40 sec,   34716 itr]:           44
> [ optimality gap     ]:      100.00%
> [ 41 sec,   35656 itr]:           44
> [ 42 sec,   36590 itr]:           44
> [ 43 sec,   37526 itr]:           44
> [ 44 sec,   38450 itr]:           44
> [ 45 sec,   39380 itr]:           44
> [ 46 sec,   40256 itr]:           44
> [ 47 sec,   41180 itr]:           44
> [ 48 sec,   42129 itr]:           44
> [ 49 sec,   43046 itr]:           44
> [ 50 sec,   43966 itr]:           44
> [ optimality gap     ]:      100.00%
> [ 51 sec,   44894 itr]:           44
> [ 52 sec,   45841 itr]:           44
> [ 53 sec,   46766 itr]:           44
> [ 54 sec,   47686 itr]:           44
> [ 55 sec,   48578 itr]:           44
> [ 56 sec,   49459 itr]:           44
> [ 57 sec,   50328 itr]:           44
> [ 58 sec,   51215 itr]:           44
> [ 59 sec,   52076 itr]:           44
> [ 60 sec,   52954 itr]:           44
> [ optimality gap     ]:      100.00%
> [ 60 sec,   52954 itr]:           44
> [ optimality gap     ]:      100.00%
> 
> 52954 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =           44
>   gap    =      100.00%
>   bounds =            0
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
> --- Solution (of length 44) ---
>   Sol: MEQPSLSKFTRYAEHVNQELNSYCHFDAIRPGFKGVTANEGYQL
> str01: M-----------A------L-SYC------P--KG-T-------
> str02: M-Q-S-S------------LN------AI-P----V--------
> str03: M--P-LS----Y-----Q------HF---R---K----------
> str04: ME-----------EHVN-EL----H-D-----------------
> str05: M---S-----------N--------FDAIR-------A-----L
> str06: M-------F-R-----NQ--NS-------R--------N-G---
> str07: M-------F--YA-H------------A----F-G-----GY--
> str08: M---S--KFTR------------------RP----------YQ-
> str09: M---S---F------V-----------A---G---VTA----Q-
> str10: ME--SL---------V--------------PGF-----NE----
> 
> solution is feasible: True
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
> [  0 sec,       0 itr]:          536
> [ optimality gap     ]:      100.00%
> [  1 sec,      24 itr]:          524
> [  2 sec,      63 itr]:          508
> [  3 sec,      95 itr]:          508
> [  4 sec,     130 itr]:          507
> [  5 sec,     190 itr]:          507
> [  6 sec,     227 itr]:          507
> [  7 sec,     265 itr]:          507
> [  8 sec,     310 itr]:          507
> [  9 sec,     343 itr]:          507
> [ 10 sec,     396 itr]:          507
> [ optimality gap     ]:      100.00%
> [ 11 sec,     432 itr]:          507
> [ 12 sec,     474 itr]:          507
> [ 13 sec,     518 itr]:          507
> [ 14 sec,     557 itr]:          507
> [ 15 sec,     606 itr]:          503
> [ 16 sec,     647 itr]:          503
> [ 17 sec,     690 itr]:          503
> [ 18 sec,     725 itr]:          503
> [ 19 sec,     763 itr]:          503
> [ 20 sec,     822 itr]:          503
> [ optimality gap     ]:      100.00%
> [ 21 sec,     855 itr]:          502
> [ 22 sec,     901 itr]:          501
> [ 23 sec,     948 itr]:          501
> [ 24 sec,     990 itr]:          501
> [ 25 sec,    1025 itr]:          501
> [ 26 sec,    1070 itr]:          501
> [ 27 sec,    1112 itr]:          501
> [ 28 sec,    1158 itr]:          501
> [ 29 sec,    1192 itr]:          501
> [ 30 sec,    1217 itr]:          501
> [ optimality gap     ]:      100.00%
> [ 31 sec,    1255 itr]:          501
> [ 32 sec,    1289 itr]:          501
> [ 33 sec,    1314 itr]:          501
> [ 34 sec,    1346 itr]:          501
> [ 35 sec,    1394 itr]:          501
> [ 36 sec,    1430 itr]:          500
> [ 37 sec,    1483 itr]:          500
> [ 38 sec,    1499 itr]:          500
> [ 39 sec,    1537 itr]:          500
> [ 40 sec,    1576 itr]:          500
> [ optimality gap     ]:      100.00%
> [ 41 sec,    1623 itr]:          500
> [ 42 sec,    1643 itr]:          499
> [ 43 sec,    1683 itr]:          499
> [ 44 sec,    1715 itr]:          499
> [ 45 sec,    1746 itr]:          499
> [ 46 sec,    1790 itr]:          499
> [ 47 sec,    1823 itr]:          499
> [ 48 sec,    1840 itr]:          499
> [ 49 sec,    1884 itr]:          499
> [ 50 sec,    1900 itr]:          499
> [ optimality gap     ]:      100.00%
> [ 51 sec,    1916 itr]:          499
> [ 52 sec,    1948 itr]:          498
> [ 53 sec,    1966 itr]:          498
> [ 54 sec,    2011 itr]:          498
> [ 55 sec,    2046 itr]:          498
> [ 56 sec,    2091 itr]:          498
> [ 57 sec,    2121 itr]:          498
> [ 58 sec,    2164 itr]:          498
> [ 59 sec,    2204 itr]:          498
> [ 60 sec,    2244 itr]:          498
> [ optimality gap     ]:      100.00%
> [ 60 sec,    2244 itr]:          498
> [ optimality gap     ]:      100.00%
> 
> 2244 iterations performed in 60 seconds
> 
> Feasible solution: 
>   obj    =          498
>   gap    =      100.00%
>   bounds =            0
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
> --- Solution (of length 498) ---
>   Sol: MAFVFLESVLLPLVSSQCVNRPGFKNEDLKTHVQLSLPRAITRVLFQVSTGYALEIRDVLSPQLTKVRNGFMPLAGDSPTIEFLNDAYTVKLEQWNSFTRGIVDHAETYQPCGKIVLNRTAPSEAFNYLQGSAEKDHLMRTIEQLAVFPDKSEVILTRQHAGYPFSENDRTLKNSFAVRGQLTRGVYSDILPNVKTASGINLHPYPDKVFRSETSQLGVYLHSADFKRINPLCTNGSMRADEGKHVLWDAFSIPYTNVLEADGSVRIKGVELFTAIKPQGRDSWACSHITVLESDGKAFTRYEILNDRKVQGPADMSRIKLVTYFACSELIGQAHRYWLEGVSTNPDKHTVAILPDGEQSNDSFRISTPECLGFAVDSEGKILHIYNDSATVDERCLQWTMPRGIDFIRANEKHSGVKAECRLTNPDQYAGLNIVQKDSNRKIYMAKECDFHVIDLRICSVVGNLYWADKAHLINVTSAGQSTIVYYGVPVWKEAKTT
> str01: M-------------------R----------H--L---------------------------------N-----------I----D---------------I----ETY-------------S--------S-----------------------------------ND--------------------I----K-----N----------------GVY------K---------------------------Y-----AD------------A-----------------E-D---F---EIL---------------L---FA----------Y-----S---------I--DG---------------G-----E------------V-E-CL--------D----------------LT----------------R---------------------------------------------------------
> str02: M-----E-------------R-----------------RA----------------------------------------------------------------H-------------RT----------------H------Q-----------------------N-------------------------------------------------------------------------------WDA-----T-----------K---------P--R-----------E-------R------RK-Q-----------T---------Q-HR--L----T----H-----PD-----DS--I-------------------Y---------------PR-I------EK-----AE----------G---------RK-----E-D-H----------G-----------------------------------
> str03: M-----E----P----------G----------------A-----F--ST--AL----------------F-----D---------A----L-------------------C-----------------------D-------------D----IL---H---------R--------R--L------------------------------E-SQL----------R----------------------F-----------G-----GV--------Q---------I-----------------------P--------------------------------P-----------E-----------------V-S---------D-------------PR-------------V-----------YAG------------Y-A---------L--------L---------------------------------
> str04: M---------------------G-K--------------------F-----Y-----------------------------------Y--------S--------------------NR--------------------R----LAVF------------A-------------------Q---------------A------------------Q------S----R----------------H-L---------------G-----G-------------S------------------YE-------Q--------------------------WL------------A------------------C----V-S-G-------DSA----------------F-RA-E----VKA--R------------VQKD------------------------------------------------------------
> str05: --F-F---------------R-----E-----------------------------------------N----LA-------F----------Q---------------Q--GK------A------------------R--E----FP--SE-------------E---------A-R-----------------A---N----------S------------------P--T--S-R--E----LW---------V-------R--------------R--------------G---------------G--------------------------------NP-------L-----S---------E----A----G---------A---ER-------RG-------------------T--------------------------------------------------------------------------
> str06: M--------------------------D---------P----------S----L----------T----------------------------Q--------V------------------------------------------------------------------------------------------------------------------------------------------------W-A-------V-E--GSV------L----------S-A------------A-----------V----D-------T--A--E--------------TN-D--T-------E----------P-------D-EG--L-----SA---E----------------NE---G---E---T----------------R-I----------I--RI------------------T--G-S----------------
> str07: MAF------------------------D-----------------F--S---------V-----T----G--------------N---T-KL-----------D---T--------------S-------G----------------F--------T-Q--G---------------V---------S---------S---------------------------------------M-----------------T-V--A-------------A----G---------T-L-----------I---------AD-----LV-------------------------K-T-A-------S--S----------------------------------Q------------------------LTN------L-------------A----------------------------------QS----------------
> str08: MA-V------------------------------------I---L----------------P---------------S-T-------YT--------------D--------G------TA---A-----------------------------------------------------------------------------------------------------------CTNGS----------------P-------D--V----V---------G---------T-----G---T---------------M---------------------W---V--N----T--ILP-G----D-F---------F------------------------WT-P------------SG---E------------------S-------------V---R---V-------------------------------------
> str09: M------------------N----------T-------------------G----I------------------------I----D-----L-----F-----D-------------N------------------H---------V--D-S--I--------P------T------------------ILP----------H------------QL------A---------T------------L-D-----Y---L-----VR-------T-I------------I-----D-------E--N-R--------S----V-------L--------L------------------------F-------------------HI---------------M--G----------SG----------------------------------------------------------------------------------
> str10: M-FVFL--VLLPLVSSQCVN--------L---------R--TR------T------------QL--------P-----P-------AYT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M--------------------------D-------S-----------------------------K---------------E------T------------I--------------L------------------------IE-----------I----------------------------------I-P--K----I-------K---S-------YL----------L--------D--------------TN---------I---------------S-----------------------------P------K-------S--------Y-------N-D----------------F-IS---------------------------R---------------N-K-----------N--------I----------------F-VI---------NLY--------NV-S----TI--------------
> str12: M----L---L----S-------G-K----K-----------------------------------K-----M-L---------L-D---------N------------Y--------------E----------------T----A--------------A---------------A-RG---RG-------------G-------D-----E--------------R----------R--------------------------R--G--------------WA-------------F-------DR----PA----I--VT------------------------K----------------R-----------D---K-------S---D-R-----M--------A---H------------------------------------------------------------------------------------
> str13: M------------------N--G---E---------------------------E--D------------------D-------N-------EQ-----------A--------------A---A--------E---------Q--------------Q-----------T-K---------------------K-A----------K--R-E-------------K---P------------K----------------------------------Q-----A---------------R-------KV------------T----SE----A---W-E--------H--------------F------------D------------AT-D------------D---------G--AEC---------------K--------------H----------------------------------------------
> str14: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-----------V--E-------------E--------VL-----SEA--------------R---Q---------------H-----------LK---------------D---------G--------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-------------------R------------------------------Y---I--V-SPQL--V------L-------------------Q--------V---------GK----------------G------------Q--------EV------------E--R------A----L----Y---L----T-------PY-D------------Y--------I-----------DE-K-------S-P------------I----------------------------------Y---------------------YF----L-----R------S-----H----L------N----I-------------------------------Q----R----------------------P------------------------------------------------------------------------
> str16: M----------P--------R-----------V----P-----V-------Y-----D--SPQ---V----------SP-----N---TV--------------------P------------------Q--A------R----LA----------T------P-S---------FA-----T--------P---T-------------FR------G-----AD--------------A-------------P------A-----------F-----Q--D-------T-------A-------N----Q---------------------QA-R----------------------Q-------------------------------------------------------------------------------------------------------------------------------------------
> str17: M-FVFL--VLLPLVSSQCVN--------L---------R--TR------T------------QL--------PLA------------YT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FVF------------------F--------V-L-LP------L--VS-----------S-Q------------------------------------------------C---V-N----------L-----------T---------------TR------------T---------QL---------P-----------P-------------------A------------------------------YTN------S--------FT------R--------------G-------------V-------------Y------------Y--------PDK--V------------FR-S----------S-------------V----L----------------HS-----------------------------------------------------------------------------------
> str19: M-----E--------------------------------AI--------------I----S---------F---AG----I-------------------GI---------------N---------Y------K---------------K----L--Q------S------K--------L---------------------------------Q-----H--DF---------G--R------VL--------------------K------A----------------L-------T---------V------------T--A---------R---------------A-LP-G-Q---------P-----------K--HI----A--------------I---R------------------Q----------------------------------------------------------------------
> str20: MA-----S------S-------G--------------P----------------E-R-----------------A------E----------------------H----Q----I--------------------------I--L---P---E------------S------------------------------------H-------------L-----S-------------S----------------P----L-----V--K-------------------H--------K-------L---------------L--Y------------YW---------K-----L-------------T----G---------L------------------P--------------------L--PD--------------------ECDF---D----------------HLI------------------------
> str21: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-----------V--E-------------E--------VL-----SE----------------------V----------RQH-----------LK---------------D---------G--------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L---------------------------------A---------------------P---------------SP-----N-----------S----------------KI--------------Q-------L---------F-------------------N-----N---------------I--N------I------D---------------------IN------------------------Y----E---------------------------H-T-L---------Y----------------------FA-S-------------VS--------A------Q-N-SF---------FA----------------------QW-----------------V-----------------V--------Y---------------S-------ADKA--I------------------------
> str23: M------S-------------------------------AIT------------E---------TK------P------TIE-L--------------------------P---------A-------L---AE---------------------------G--F---------------Q--R--Y-----N-KT-------P-------------G-------F-------T---------------------------------------------------C----VL--D-----RY----D---------------------------H-----GV----------I-------NDS-----------------KI---------V----L-------------------------------Y---N-----------------------------------------------------------------
> str24: M-----------------------KN--------------I-----------A-E---------------F-------------------K----------------------K------AP-E----L---AEK--L------L-------EV----------FS-N---LK------G------------N----S------------RS----L-------D-----P------MRA--GKH---D--------V------V----V-----I----------------ES-----T--------K----------KL---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: M----------P----Q----P------LK---Q-SL--------------------D----Q--------------S------------K---W---------------------L-R----EA--------EK-HL-R-----A---------L----------E-------S------L---V--D--------S--NL----------E----------------------------E-----------------E-------K---L----KPQ------------L-S---------------------M---------------G-------E------D---V-------QS------------------------------------------------------------------------------------------------------------------------------------------
> str26: M-FVFL--VLLPLVSSQCVN--------L-----------ITR------T------------Q--------------S---------YT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S-T-Q--------D---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-----------------------K--------------------F-----------DVLS--L------F---A---P---------------W----------A-------K-V-------------------D------EQ--------E---------Y-----D-----------Q----------------------------------QL------------N----N---------------------N-LE---S--I------TA--P------------------K-F-------D-------D----------------G-A---------T-------------E-------I---E-------SE---------------R--------G-D-I------------------------------------------------------------------------------------------
> str28: M-FVFL--VLLPLVSSQCVN---F------T-------------------------------------N------------------------------R-------T-Q------L----PS-A--Y------------T--------------------------N------SF------TRGVY-----------------YPDKVFRS--S---V-LHS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M---------------------------------------------------------------------------------------------W-S----I------------IVL-----------------K--L---I---------S--I---Q----P-------L---------L--------L--V-T-S---L-P------------L--Y---------NP---N--M--D----------S---------------------------------C----------------------------------------C--LI-----------S---------------------RI-TPE-L--A----GK-L-------T-------W-----I-FI------------------------------------------------------------------------------------------
> str30: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-----------V--E-------------E------------------F--L--S-E-----------A-----------RQH-----------LK---------------D---------G--------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FVFL--VLLPLVSSQCV----------------------------------------------------MPL--------F-N------L---------I-----T-----------T--------------------T--Q-------S----------Y-------T--N-F------TRGVY-----------------YPDKVFRS--S---V-LH---------L--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M------------------------------H-Q------IT-V---VS-G----------P--T----------------E-------V------S-T------------C-------------F----GS-----L---------------------H---PF---------------Q------S--L---K--------P----V----------------------------M-A----------------N---A----------L-------G----------VLE--GK------------------M--------F-CS--IG--------G-----------------------R-S----L------------------------------------------------------------------------------------------------------------------------------
> str33: MA----------------------------T---L-L-R---------S----L--------------------A--------L-------------F---------------K----R-------N-------KD--------------K------------P---------------------------P-------I-------------TS--G----S------------G------G------A--I------------R--G------IK----------HI--------------I--------------I--V-----------------------P------I-P-G----DS---S--------------I--------T--------T--R-----------S------R----------------------------------------------------------------------------
> str34: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS------------------------------------------------------------M---E---------EV-L---------SE---------A-R-Q---------------------H-------------L---------K-------------D-G------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FVFL--VLLPLVSSQCVN--------L-T----------T--------G-------------T----------------------------Q----------------------L----P--------------------------P-----------A-Y-------T--NSF------TRGVY-----------------YPDKVFRS--S---V-LHS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA-----------------N--------------------I--------------I------------N----L--------------------WN----GIV-------P---------------------------M-------V-----------Q---------D--------V--------------NV--AS-I-------------T---------A-FK---------SM--------------I--------D--------E--T---------W----------D-K-----------K---------I---------E----A----------N----T--------------------C----------I------S-----R-----------------KH-------R--N-------------------------------------------------------------------------
> str37: M----L-------------NR-------------------I-----Q--T---L-----------------M------------------K-------T------A-----------N--------NY-----E------TIE-----------IL-R---------N------------------Y---L-------------------R-----L--Y--------I-----------------------I-----L-A----R---------------------------------------N----------------------E----------EG-----------------------R-------G--------IL-IY-D----D-----------------N----------------------I---DS-------------V---------------------------------------------
> str38: MA-------------------------D---------P-A----------G-------------T---NG-----------E----------E-------G------T----G-----------------------------------------------------------------------------------------------------------------------C-NG-----------W--F---Y--V-EA---V----VE-----K-------------------K--T-----------G--D----------A----I-----------S---D--------D-E--N--------E----------------NDS---D------T---G-------E--------------D----L--V--D------------------------------------------------------------
> str39: M-FVFL--VLLPLVSSQCVN--------L---------R--TR------T------------QL--------P-----P-----------------S-----------Y----------T------N----S---------------F--------TR---G---------------V--------Y-----------------YPDKVFRS--S---V-LHS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV---------------------------------------------------------------C-----------------------D----------V--------L---------------------VRG-----------------------------F-------G------D-----------S--------V-------------E----------E-------------------VL-S--------E----------A---R--------------Q-H---L--------K-------DG----------T----------------------------------------------------------------------------------------------------------------------------------
> str41: M------------------N-----N-------Q----R--------------------------K------------------------K-------T------A------------R--PS--FN-----------M-----L-----K------R--A--------R---N----R------V-S-------T------------V--S---QL------A--KR----------------------FS---------------KG--L-------------------L-S-G--------------QGP--M---KLV------------------------------------------------------------------------------M--------A----------------------------------------F-----------------------------------------------
> str42: M------S-----------N---F---D-----------AI-R---------AL----V-----------------D--T-----DAY--KL--------G---H---------I---------------------H-M-----------------------YP--E------------G--T-----------------------------E------Y-------------------------VL----S----N---------------FT-------D------------------R----------G----SRI---------E--G---------V-T----HTV--------------------------------H------------------------------------------------------------------------------------------------------------------
> str43: M---------------------------------------I-------------E----L-------R------------------------------------H-E--------V-------------QG----D-L--------V---------T--------------------------------I--NV--------------V---ET----------------P----------E------D---------L--DG---------F-------RD----------------F----I---R-----A--------------------H---L-------------I-----------------CL--AVD-------------T--E-----T-----------------------T------GL-----D----IY------------------------------------------------------
> str44: M-FVFL--VLLPLVSSQCV----------------------------------------------------MPL--------F-N------L---------I-----T-----------T------N--Q-S------------------------------Y-------T--NSF------TRGVY-----------------YPDKVFRS--S---V-LH------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M------S----------------K--DL---V------A--R---Q-----AL-----------------M-------T------A------------R--------------------------------------M-----------K---------A-------D------F-V-------------------------------F---------------F-----L------------------F------VL------------------------W------------KA------L-----------S---L------------------------P----V---P------------T--------------------------RC-Q------ID--------------------------------------MAK----------------------K--L----SAG------------------
> str46: MA-----S-LL-------------K----------SL----T--LF-------------------K-R-----------T-------------------R---D-----QP----------P------L---A------------------S---------G---S-------------G----G-----------A--I----------R------G----------I--------------KHV------I-------------I--V-L---I-P-G-DS---S-I-V--------TR---------------SR------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M-------------------R-----------V-----R-----------G----I---L-------RN-------------------------W--------------Q-------------------Q---------------------------------------------------------------------------------------------------------------------W-----------------------------------W----I------------------------------------------------W-----T---------------S-----------LGF------------------------W-M-----F-------------------------------------M--------I----CSVVGNL-W--------VT-------VYYGVPVWKEAKTT
> str48: MA-V--E----P-----------F-------------PR---R------------------P------------------I-------T----------R----------P-------------------------H--------A-----S--I-----------E----------V----------D------T-SGI-----------------G-----------------GS--A--G--------S-----------S------E-----K-------------V-------F---------------------------C--LIGQA-----EG---------------GE----------P-----------------N---TV----------------------------------------------------------------------------------------------------------
> str49: M-F------------------------------------------------YA---------------------------------------------------HA-------------------F----G------------------------------GY-----D-------------------------------------------E----------------N-L------------H----AF--P--------G---I---------------S---S--TV------A-------ND--V-------R-K---Y---S-------------V--------V--------S---------------V---------YN-------------------------K----K----------Y---NIV-K--N-K-YM---------------------W-------------------------------
> str50: MA-----------------N-------------------------------Y--------S----K------P---------FL-------L-----------D----------IV---------FN-------KD-----I--------K---------------------------------------------------------------------------------C-------------------I---N----D-S---------------------CSH-----SD-------------------------------C--------RY---------------------QSN-S----------------------Y-----V-E--L-----R-----R-N----------------Q-A-LN---K--N---------------L------------------------------------------
> 
> solution is feasible: True
> ```
