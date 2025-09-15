# 決定問題を解きながら探索

`AUTOMATON_CPSAT` モデルでは解文字列を有効な文字と無効な文字が混ざった文字列とし, 有効な文字数を最小化するという定式化をしていた.

ここでは解文字列の長さを固定し, 実行可能解が存在するかどうかを CP-SAT ソルバーに解かせ,
その結果をもとに二分探索を行うことで最適値の範囲を狭めていく.

計算開始時には SCSP 長の下限は問題文字列たちの長さの最大値,
SCSP 長の上限 (これは計算開始前の最良解でもある) としてアルファベットアルゴリズムによって構築された解の長さを採用する.


## Python Code

```python
import datetime
from ortools.sat.python import cp_model


class ModelSat:
    def __init__(self, instance: list[str], sol_len: int):
        chars = sorted(list(set("".join(instance))))

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars) - 1, name="")
            for _ in range(sol_len)
        ]

        for s in instance:
            transition_triples = [
                (idx, jdx, (idx + 1 if c == next_char else idx))
                for idx, next_char in enumerate(s)
                for jdx, c in enumerate(chars)
            ] + [(len(s), jdx, len(s)) for jdx, _ in enumerate(chars)]
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
        self.status: cp_model.cp_model_pb2.CpSolverStatus | None = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "ModelSat":
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


class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        len_lb = max(len(s) for s in instance)
        best_sol = chars * max(len(s) for s in instance)
        len_ub = len(best_sol)

        self.instance = instance
        self.len_lb = len_lb
        self.len_ub = len_ub
        self.best_sol = best_sol

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        start_time = datetime.datetime.now()
        end_time = None
        if time_limit is not None:
            end_time = start_time + datetime.timedelta(seconds=time_limit)

        next_len = self.len_lb + (self.len_ub - self.len_lb) // 2
        if log:
            print(
                "Best Sol: {}, Range: [{},{}], Next: {}".format(
                    self.len_ub, self.len_lb, self.len_ub, next_len
                )
            )

        now = datetime.datetime.now()
        while self.len_lb < self.len_ub and (end_time is None or now <= end_time):
            model_sat = ModelSat(self.instance, next_len)
            model_sat.solve((end_time - now).seconds if end_time is not None else None)
            if model_sat.is_feasible():
                self.len_ub = next_len
                best_sol = model_sat.to_solution()
                assert best_sol is not None
                self.best_sol = best_sol
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

    def to_solution(self) -> str:
        return self.best_sol


def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    return Model(instance).solve(time_limit, log).to_solution()
```
