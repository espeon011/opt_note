# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")

with app.setup:
    import datetime
    from ortools.sat.python import cp_model
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 実行可能解を見つける問題を解きながら探索""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    `AUTOMATON_CPSAT` モデルでは解文字列を有効な文字と無効な文字が混ざった文字列とし, 有効な文字数を最小化するという定式化をしていた. 

    ここでは解文字列の長さを固定し, 実行可能解が存在するかどうかを CP-SAT ソルバーに解かせ, 
    その結果をもとに二分探索を行うことで最適値の範囲を狭めていく. 

    計算開始時には SCSP 長の下限は問題文字列たちの長さの最大値, 
    SCSP 長の上限 (これは計算開始前の最良解でもある) としてアルファベットアルゴリズムによって構築された解の長さを採用する. 
    """
    )
    return


@app.class_definition
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


@app.class_definition
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


@app.function
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    return Model(instance).solve(time_limit, log).best_solution()


@app.cell
def _():
    instance_01 = util.parse("uniform_q26n004k015-025.txt")
    model_01 = Model(instance_01).solve(log=True)
    return (model_01,)


@app.cell
def _(model_01):
    _model = model_01
    _instance = _model.instance
    _solution = _model.best_solution()
    _bound = _model.best_bound()

    util.show(_model.instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.len_lb == _model.len_ub}")
    print(f"best bound: {_model.best_bound()}")
    return


@app.cell
def _():
    instance_02 = util.parse("uniform_q26n008k015-025.txt")
    model_02 = Model(instance_02).solve(log=True)
    return (model_02,)


@app.cell
def _(model_02):
    _model = model_02
    _instance = _model.instance
    _solution = _model.best_solution()
    _bound = _model.best_bound()

    util.show(_model.instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.len_lb == _model.len_ub}")
    print(f"best bound: {_model.best_bound()}")
    return


@app.cell
def _():
    instance_03 = util.parse("uniform_q26n016k015-025.txt")
    model_03 = Model(instance_03).solve(log=True)
    return (model_03,)


@app.cell
def _(model_03):
    _model = model_03
    _instance = _model.instance
    _solution = _model.best_solution()
    _bound = _model.best_bound()

    util.show(_model.instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    print(f"solution is optimal: {_model.len_lb == _model.len_ub}")
    print(f"best bound: {_model.best_bound()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    この定式化も制限時間内ではあまり良い結果が得られなかった...

    元々の `AUTOMATON_CPSAT` の定式化において無効な文字と有効な文字に関する制約がなくなれば性能が良くなるんじゃないかと思っていたけど, 
    有効無効に関する制約をなくしたこのモデルでも 1 回の最適化計算時間が長く, 
    反復回数が稼げなかった. 
    この結果を見る限りオートマトン制約部分の定式化がそんなに良くなさそう. 
    """
    )
    return


if __name__ == "__main__":
    app.run()
