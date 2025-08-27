# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    from ortools.sat.python import cp_model


@app.cell
def _():
    import marimo as mo
    import nbformat
    import util
    return mo, util


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# MILP 定式化 (CP-SAT)""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    数理最適化モデルを用いて SCSP を解く. 
    定式化については SCIP 版を参照. 
    """
    )
    return


@app.class_definition
class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        seqs = [
            [
                cpmodel.new_int_var(0, max_len - 1, "")
                for c in s
            ]
            for s in instance
        ]

        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                cpmodel.add(seq[idx - 1] < seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
                if idx1 >= idx2:
                    continue
                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            cpmodel.add(cvar1 != cvar2)

        obj = cpmodel.new_int_var(0, max_len, "")
        cpmodel.add_max_equality(obj, [seq[-1] for seq in seqs])
        cpmodel.minimize(obj)

        self.instance = instance
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.seqs = seqs
        self.status = None

    def solve(self, time_limit: int | None = 60) -> "Model":
        self.cpsolver.parameters.log_search_progress = True
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {cp_model.cp_model_pb2.OPTIMAL, cp_model.cp_model_pb2.FEASIBLE}:
            return None

        objval = int(self.cpsolver.objective_value)
        sol_char_idx = 0
        solution = ""
        while sol_char_idx <= objval:
            found = False
            for idx, (s, seq) in enumerate(zip(self.instance, self.seqs)):
                for c_idx, cvar in enumerate(seq):
                    if self.cpsolver.value(cvar) == sol_char_idx:
                        solution += s[c_idx]
                        found = True
                        sol_char_idx += 1
                if found:
                    break
            if not found:
                sol_char_idx += 1

        return solution


@app.function
def solve(instance: list[str], time_limit: int | None = 60) -> str | None:
    return Model(instance).solve(time_limit).to_solution()


@app.cell
def _(util):
    instance_01 = util.parse("uniform_q26n004k015-025.txt")
    solution_01 = solve(instance_01)
    return instance_01, solution_01


@app.cell
def _(instance_01, solution_01, util):
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
def _(util):
    instance_02 = util.parse("uniform_q26n008k015-025.txt")
    solution_02 = solve(instance_02)
    return instance_02, solution_02


@app.cell
def _(instance_02, solution_02, util):
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
def _(util):
    instance_03 = util.parse("uniform_q26n016k015-025.txt")
    solution_03 = solve(instance_03)
    return instance_03, solution_03


@app.cell
def _(instance_03, solution_03, util):
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
def _(util):
    instance_04 = util.parse("uniform_q05n010k010-010.txt")
    solution_04 = solve(instance_04)
    return instance_04, solution_04


@app.cell
def _(instance_04, solution_04, util):
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
def _(util):
    instance_05 = util.parse("uniform_q05n050k010-010.txt")
    solution_05 = solve(instance_05)
    return instance_05, solution_05


@app.cell
def _(instance_05, solution_05, util):
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
def _(util):
    instance_06 = util.parse("nucleotide_n010k010.txt")
    solution_06 = solve(instance_06)
    return instance_06, solution_06


@app.cell
def _(instance_06, solution_06, util):
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
def _(util):
    instance_07 = util.parse("nucleotide_n050k050.txt")
    solution_07 = solve(instance_07)
    return instance_07, solution_07


@app.cell
def _(instance_07, solution_07, util):
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
def _(util):
    instance_08 = util.parse("protein_n010k010.txt")
    solution_08 = solve(instance_08)
    return instance_08, solution_08


@app.cell
def _(instance_08, solution_08, util):
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
def _(util):
    instance_09 = util.parse("protein_n050k050.txt")
    solution_09 = solve(instance_09)    
    return instance_09, solution_09


@app.cell
def _(instance_09, solution_09, util):
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
