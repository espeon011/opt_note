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
    from ortools.sat.python import cp_model
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# オートマトン制約を用いた数理計画モデル""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    CP-SAT 固有のオートマトン制約を用いて定式化してみる. 

    **定数**

    - $\Sigma = \lbrace \sigma_1, \dots, \sigma_q \rbrace$: 文字の集合

    **決定変数**

    - $x_i \in \mathbb{Z}$: 解において $i$ 番目の文字が $\sigma_j$ であれば $j$ となる.
      どの文字も対応しないとき $0$. 
      このとき解は $\sigma_{x_0} \sigma_{x_1} \dots$ となる.
      ただし $\sigma_0$ は空文字列とする. 
    - $v_i \in \lbrace 0, 1 \rbrace$: 解の $i$ 番目が空でないとき $1$. 空のとき $0$.

    **制約条件**

    - $x_i > 0 \Rightarrow v_i = 1$
    - 与えられた文字列 $s \in S$ の各文字を $\Sigma$ を基準にインデックスの配列としたものを $\mathrm{index}_s$ とする.
      $\mathrm{index}_s$ を部分配列にもつすべての配列を受理するオートマトンを文字列の数だけ作成し, 
      $\lbrace x_i \rbrace_i$ が受理されるという制約を課す. 

    **目的関数**

    - minimize $\sum_{i} v_i$
    """
    )
    return


@app.class_definition
class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)
        chars = sorted(list(set("".join(instance))))

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="")
            for _ in range(max_len)
        ]

        for s in instance:
            transition_triples = (
                [
                    (idx, jdx + 1, (idx + 1 if c == next_char else idx))
                    for idx, next_char in enumerate(s)
                    for jdx, c in enumerate(chars)
                ]
                + [(idx, 0, idx) for idx, _ in enumerate(s)]
                + [(len(s), 0, len(s))]
                + [(len(s), jdx + 1, len(s)) for jdx, _ in enumerate(chars)]
            )
            cpmodel.add_automaton(
                transition_expressions=cvars,
                starting_state=0,
                final_states=[len(s)],
                transition_triples=transition_triples,
            )

        valids = [cpmodel.new_bool_var("") for _ in cvars]
        for cvar, valid in zip(cvars, valids):
            cpmodel.add(cvar == 0).only_enforce_if(~valid)
        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {cp_model.cp_model_pb2.OPTIMAL, cp_model.cp_model_pb2.FEASIBLE}:
            return None

        solution = ""
        for cvar in self.cvars:
            cidx = self.cpsolver.value(cvar) - 1
            if cidx >= 0:
                solution += self.chars[cidx]

        return solution


@app.function
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()


@app.cell
def _():
    instance_01 = util.parse("uniform_q26n004k015-025.txt")
    solution_01 = solve(instance_01)
    return instance_01, solution_01


@app.cell
def _(instance_01, solution_01):
    _instance = instance_01
    _solution = solution_01

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_02 = util.parse("uniform_q26n008k015-025.txt")
    solution_02 = solve(instance_02)
    return instance_02, solution_02


@app.cell
def _(instance_02, solution_02):
    _instance = instance_02
    _solution = solution_02

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_03 = util.parse("uniform_q26n016k015-025.txt")
    solution_03 = solve(instance_03)
    return instance_03, solution_03


@app.cell
def _(instance_03, solution_03):
    _instance = instance_03
    _solution = solution_03

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_04 = util.parse("uniform_q05n010k010-010.txt")
    solution_04 = solve(instance_04)
    return instance_04, solution_04


@app.cell
def _(instance_04, solution_04):
    _instance = instance_04
    _solution = solution_04

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_05 = util.parse("uniform_q05n050k010-010.txt")
    solution_05 = solve(instance_05)
    return instance_05, solution_05


@app.cell
def _(instance_05, solution_05):
    _instance = instance_05
    _solution = solution_05

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_06 = util.parse("nucleotide_n010k010.txt")
    solution_06 = solve(instance_06)
    return instance_06, solution_06


@app.cell
def _(instance_06, solution_06):
    _instance = instance_06
    _solution = solution_06

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_07 = util.parse("nucleotide_n050k050.txt")
    solution_07 = solve(instance_07)
    return instance_07, solution_07


@app.cell
def _(instance_07, solution_07):
    _instance = instance_07
    _solution = solution_07

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_08 = util.parse("protein_n010k010.txt")
    solution_08 = solve(instance_08)
    return instance_08, solution_08


@app.cell
def _(instance_08, solution_08):
    _instance = instance_08
    _solution = solution_08

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_09 = util.parse("protein_n050k050.txt")
    solution_09 = solve(instance_09)    
    return instance_09, solution_09


@app.cell
def _(instance_09, solution_09):
    _instance = instance_09
    _solution = solution_09

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


if __name__ == "__main__":
    app.run()
