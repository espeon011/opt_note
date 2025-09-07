In [ ]:
```python
import datetime
from ortools.sat.python import cp_model
import util
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# 実行可能解を見つける問題を解きながら探索

`AUTOMATON_CPSAT` モデルでは解文字列を有効な文字と無効な文字が混ざった文字列とし, 有効な文字数を最小化するという定式化をしていた.

ここでは解文字列の長さを固定し, 実行可能解が存在するかどうかを CP-SAT ソルバーに解かせ,
その結果をもとに二分探索を行うことで最適値の範囲を狭めていく.

計算開始時には SCSP 長の下限は問題文字列たちの長さの最大値,
SCSP 長の上限 (これは計算開始前の最良解でもある) としてアルファベットアルゴリズムによって構築された解の長さを採用する.

In [ ]:
```python
class ModelSat:
    def __init__(self, instance: list[str], sol_len: int):
        chars = sorted(list(set("".join(instance))))

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars) - 1, name="")
            for _ in range(sol_len)
        ]

        for s in instance:
            transition_triples = (
                [
                    (idx, jdx, (idx + 1 if c == next_char else idx))
                    for idx, next_char in enumerate(s)
                    for jdx, c in enumerate(chars)
                ]
                + [(len(s), jdx, len(s)) for jdx, _ in enumerate(chars)]
            )
            cpmodel.add_automaton(
                transition_expressions=cvars,
                starting_state=0,
                final_states=[len(s)],
                transition_triples=transition_triples,
            )

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars
        self.status = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def is_feasible(self) -> bool:
        return self.status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }

    def is_proved_infeasible(self) -> bool:
        return self.status == cp_model.cp_model_pb2.INFEASIBLE

    def to_solution(self) -> str | None:
        if not self.is_feasible():
            return None

        solution = ""
        for cvar in self.cvars:
            cidx = self.cpsolver.value(cvar)
            solution += self.chars[cidx]

        return solution
```

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        chars = sorted(list(set("".join(instance))))
        len_lb = max(len(s) for s in instance)
        best_sol = chars * max(len(s) for s in instance)
        len_ub = len(best_sol)

        self.instance = instance
        self.len_lb = len_lb
        self.len_ub = len_ub
        self.best_sol = best_sol

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=time_limit)

        next_len = self.len_lb + (self.len_ub - self.len_lb) // 2
        if log:
            print(
                "Best Sol: {}, Range: [{},{}], Next: {}".format(
                    self.len_ub, self.len_lb, self.len_ub, next_len
                )
            )

        now = datetime.datetime.now()
        while self.len_lb < self.len_ub and now <= end_time:
            model_sat = ModelSat(self.instance, next_len)
            model_sat.solve((end_time - now).seconds)
            if model_sat.is_feasible():
                self.len_ub = next_len
                self.best_sol = model_sat.to_solution()
            elif model_sat.is_proved_infeasible():
                self.len_lb = next_len + 1
            else:
                break

            next_len = self.len_lb + (self.len_ub - self.len_lb) // 2
            if log:
                print(
                    "Best Sol: {}, Range: [{},{}], Next: {}".format(
                        self.len_ub, self.len_lb, self.len_ub, next_len
                    )
                )

            now = datetime.datetime.now()

        return self

    def best_bound(self) -> int:
        return self.len_lb

    def best_solution(self) -> str:
        return self.best_sol
```

In [ ]:
```python
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    return Model(instance).solve(time_limit, log).best_solution()
```

In [ ]:
```python
instance_01 = util.parse("uniform_q26n004k015-025.txt")
model_01 = Model(instance_01).solve(log=True)
```

> ```
> Best Sol: 625, Range: [25,625], Next: 325
> Best Sol: 325, Range: [25,325], Next: 175
> Best Sol: 175, Range: [25,175], Next: 100
> Best Sol: 100, Range: [25,100], Next: 62
> ```

In [ ]:
```python
_model = model_01
_instance = _model.instance
_solution = _model.best_solution()
_bound = _model.best_bound()

util.show(_model.instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
print(f"solution is optimal: {_model.len_lb == _model.len_ub}")
print(f"best bound: {_model.best_bound()}")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 100) ---
>  Sol: zitogujeklvagnikuhmqpxmgfcminiyopbfcholttnpbxnxqgxmzpyddgnbchtrqvsguqxpovipsvosdzdbppctlqgxsvrvnngpf
> str1: --t-----k---gn-kuhm-px------n-------h--t-------qgx-z------------v----x---i-s------------------------
> str2: -i-o--j-------i----q----f------o------l--n-bx-x------------c----vs-uq-p-vi-s--s---b-------x--------f
> str3: -----u---l---------------c-in-y----c-o---------------------------s-----ov----o--z--pp--l----------p-
> str4: -i--g--e--va---------------------------------------z----g-b---r----------------d-db--c-----svrvnng-f
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 25
> ```

In [ ]:
```python
instance_02 = util.parse("uniform_q26n008k015-025.txt")
model_02 = Model(instance_02).solve(log=True)
```

> ```
> Best Sol: 650, Range: [25,650], Next: 337
> Best Sol: 337, Range: [25,337], Next: 181
> Best Sol: 181, Range: [25,181], Next: 103
> ```

In [ ]:
```python
_model = model_02
_instance = _model.instance
_solution = _model.best_solution()
_bound = _model.best_bound()

util.show(_model.instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
print(f"solution is optimal: {_model.len_lb == _model.len_ub}")
print(f"best bound: {_model.best_bound()}")
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
> --- Solution (of length 181) ---
>  Sol: etkgnkuhmpxnhtqgzzzzzzzzzzzzzzzzzzzzzzzzzzzziojiqfolnbxxcvsuqpvisulcinycosovoigevazgbrddbcsvrvnnpyplrzxucpmqvgtdfuipbdevdcvdpfzsmsbroqvbbhenbczfjtvxerzbrvigprxwxqkrdrlctodtmprpxwedd
> str1: -tkgnkuhmpxnhtqg--------------------------------------x---------------------------z--------v----------x-----------i------------s-----------------------------------------------------
> str2: --------------------------------------------iojiqfolnbxxcvsuqpvis--------s----------b-----------------x---------f--------------------------------------------------------------------
> str3: ------u--------------------------------------------l----c------i-----nycosovo-----z-------------p-pl-----p---------------------------------------------------------------------------
> str4: --------------------------------------------i---------------------------------gevazgbrddbcsvrvnn-------------g--f--------------------------------------------------------------------
> str5: ---------p------------------------------------------------------------y-------------------------p--lrzxucpmqvgtdfui----v-c-d---s--b-o------------------------------------------------
> str6: ---------p-------------------------------------------b--------------------------------d-------------------------------evdcvdpfzsmsbroqvbbh-------------------------------------------
> str7: e---n------------------------------------------------b--c-------------------------z-----------------------------f-------------------------------jtvxerzbrvigp---------l-----------e--
> str8: -------------------------------------------------------------------------------------r----------------x--------------------------------------------------------wxqkrdrlctodtmprpxw-d-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 25
> ```

In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
model_03 = Model(instance_03).solve(log=True)
```

> ```
> Best Sol: 650, Range: [25,650], Next: 337
> Best Sol: 337, Range: [25,337], Next: 181
> ```

In [ ]:
```python
_model = model_03
_instance = _model.instance
_solution = _model.best_solution()
_bound = _model.best_bound()

util.show(_model.instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
print(f"solution is optimal: {_model.len_lb == _model.len_ub}")
print(f"best bound: {_model.best_bound()}")
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
> --- Solution (of length 337) ---
>   Sol: etkgnkuhmpxnhzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzziojiqfolnbxxulcinycosovoigevazgbrddbcsvpyplrzxucpmqvgtdfupbdevdcvdpfzsmsenbczfjtvxerzbrvigrxwxqkrdrlctodtmpkkqafigqjwokkskrblxxpabivbvzkozkrifsavnqaxudgqvqcewbfgijowwyrsxqjnfpadiusiqbezhkiwshvhcomiuvddhtxxqjzqbctbakxusfcfzpeecvwantfmgqznuu
> str01: -tkgnkuhmpxnh------------------------------------------------------------------------------------------------------------------------------------------t----------------------------------------q------------------g-----------x--------z---------v---x------------i------s----------------------------------------------------------------------
> str02: --------------------------------------------------------------------------------------------------iojiqfolnbxx--c-------v--------------s--------u---q------p---v--------------------------i-------------------------------s---------------------s---------------b----------x---f-----------------------------------------------------------------
> str03: ------u--------------------------------------------------------------------------------------------------l------cinycosovo-----z---------p-pl-----p----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: --------------------------------------------------------------------------------------------------i------------------------gevazgbrddbcsv----r-------v---------------------n-----------------------------------------------------------------------n-----g-------f-------------------------------------------------------------------------------
> str05: ---------p---------------------------------------------------------------------------------------------------------y---------------------p--lrzxucpmqvgtdfu-------------------------------i------------------------------------------v-----------------------c--------------------d--s--b-----------o--------------------------------------------
> str06: ---------p-------------------------------------------------------------------------------------------------b-----------------------d--------------------------evdcvdpfzsms--b--------r------------------o------q---------------------vb-------------------------b--------------------------h-----------------------------------------------------
> str07: e---n------------------------------------------------------------------------------------------------------b----c--------------z-------------------------f----------------------jtvxerzbrvig----------------p-----------------l-------------------------------e----------------------------------------------------------------------------------
> str08: ----------------------------------------------------------------------------------------------------------------------------------r------------x----------------------------------------------wxqkrdrlctodtmp---------------r----p--------------------x--------w------------------d--------------------------------------------------------------
> str09: --k--k------------------------------------------------------------------------------------------------q-----------------------a--------------------------f--------------------------------ig----q--------------------jwokkskrbl--------------------------g---------------------------------------------------------------------------------------
> str10: ---------------------------------------------------------------------------------------------------------l--xx---------------------------p----------------------------------------------------------------------a------------b------ivbvzkoz----------------------------------------------z------v-------d---------------------------------------
> str11: --k-------------------------------------------------------------------------------------------------------------------------------r-------------------------------------------------------i----------------------f--------s-------a--v-------------n---------c--------------------d----q------w-h----------------z--c----------------------------
> str12: ------------------------------------------------------------------------------------------------------q-----------------------a----------------xu-------d----------------------------------g----q------------------------------------v--------------q--------cewbfgijowwy------------------------------------------------------------------------
> str13: ----------------------------------------------------------------------------------------------------------------------------------r----s-------x----q---------------------------j------------------------------------------------------------------n-------------f--------------padiusiqbezhk-------o------h------------------------------mg-----
> str14: --------------------------------------------------------------------------------------------------i-------------------------------------------------------------------------------------------w---------------------------s----------------------------------------------------------------h-----vhcomiuvdd-------------------------------m------
> str15: -------h-----------------------------------------------------------------------------------------------------------------------------------------------t---------------------------x---------x--q--------------------j------------------z-----------q-----------b----------------------------------c--------t------b---ak--------------n---------
> str16: ----------x---------------------------------------------------------------------------------------------------u-------s----------------------------------f-------c---fz-------------------------------------p-------------------------------------------------e--------------------------e---------c----v----------------------------wantfmgqz-u-
> 
> solution is feasible: True
> solution is optimal: False
> best bound: 25
> ```

この定式化も制限時間内ではあまり良い結果が得られなかった...

元々の `AUTOMATON_CPSAT` の定式化において無効な文字と有効な文字に関する制約がなくなれば性能が良くなるんじゃないかと思っていたけど,
有効無効に関する制約をなくしたこのモデルでも 1 回の最適化計算時間が長く,
反復回数が稼げなかった.
この結果を見る限りオートマトン制約部分の定式化がそんなに良くなさそう.
