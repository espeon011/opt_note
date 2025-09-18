# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.11.0",
#     "hexaly>=14.0.20250915",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==5.6.0",
# ]
# [[tool.uv.index]]
# name ="hexaly"
# url = "https://pip.hexaly.com"
# explict = true
# [tool.uv.sources]
# hexaly = { index = "hexaly" }
# ///

import marimo

__generated_with = "0.15.5"
app = marimo.App(width="medium")

with app.setup:
    import opt_note.scsp as scsp
    from ortools.sat.python import cp_model
    import automaton_cpsat_test


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# ALPHABET から削り出すやつを整数線形計画でやる""")
    return


@app.class_definition
class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        valids = [cpmodel.new_bool_var("") for _ in range(max_len)]
        cvars = [
            [
                cpmodel.new_int_var(0, max(len(s) for s in instance) - 1, "")
                for c in s
            ]
            for s in instance
        ]

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(
                    len(chars) * cvars[sidx][cidx - 1] + chars.index(s[cidx - 1])
                    < len(chars) * cvars[sidx][cidx] + chars.index(s[cidx])
                )

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                cpmodel.add_element(
                    len(chars) * cvars[sidx][cidx] + chars.index(c),
                    valids,
                    1,
                )

        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.valids = valids
        self.status: cp_model.cp_model_pb2.CpSolverStatus | None = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            return None

        solution = ""
        for idx, valid in enumerate(self.valids):
            if self.cpsolver.boolean_value(valid):
                solution += self.chars[idx % len(self.chars)]

        return solution


@app.function
def bench1(instance: list[str]) -> None:
    model = automaton_cpsat_test.Model(instance, False).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")


@app.function
def bench2(instance: list[str]) -> None:
    model = Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")


@app.cell
def _():
    instance01 = scsp.example.load("uniform_q26n004k015-025.txt")
    return (instance01,)


@app.cell
def _(instance01):
    bench1(instance01)
    return


@app.cell
def _(instance01):
    bench2(instance01)
    return


@app.cell
def _():
    instance02 = scsp.example.load("uniform_q26n008k015-025.txt")
    return (instance02,)


@app.cell
def _(instance02):
    bench1(instance02)
    return


@app.cell
def _(instance02):
    bench2(instance02)
    return


@app.cell
def _():
    instance03 = scsp.example.load("uniform_q26n016k015-025.txt")
    return (instance03,)


@app.cell
def _(instance03):
    bench1(instance03)
    return


@app.cell
def _(instance03):
    bench2(instance03)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""オートマトン制約を使うよりも線形制約で定式化した方が良さげ""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## ログを見よう""")
    return


@app.cell
def _():
    instance04 = scsp.example.load("uniform_q05n010k010-010.txt")
    instance05 = scsp.example.load("uniform_q05n050k010-010.txt")
    instance06 = scsp.example.load("nucleotide_n010k010.txt")
    instance07 = scsp.example.load("nucleotide_n050k050.txt")
    instance08 = scsp.example.load("protein_n010k010.txt")
    instance09 = scsp.example.load("protein_n050k050.txt")
    return (
        instance04,
        instance05,
        instance06,
        instance07,
        instance08,
        instance09,
    )


@app.cell
def _(instance01):
    _model = Model(instance01)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance02):
    _model = Model(instance02)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance03):
    _model = Model(instance03)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance04):
    _model = Model(instance04)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance05):
    _model = Model(instance05)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance06):
    _model = Model(instance06)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance07):
    _model = Model(instance07)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance08):
    _model = Model(instance08)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance09):
    _model = Model(instance09)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""巨大なインスタンスで試してみよう""")
    return


@app.cell
def _():
    instance_large1 = scsp.example.load("nucleotide_n100k100.txt")
    instance_large2 = scsp.example.load("protein_n100k100.txt")
    return instance_large1, instance_large2


@app.cell
def _(instance_large1):
    _model = Model(instance_large1)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance_large2):
    _model = Model(instance_large2)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    大きなインスタンスに対しても実行可能解がきちんと出る. 
    Dual Bound はカスだけど... 
    """
    )
    return


if __name__ == "__main__":
    app.run()
