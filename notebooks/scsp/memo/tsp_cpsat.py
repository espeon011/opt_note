# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.12.0",
#     "hexaly>=14.0.20251112",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==6.0.0",
# ]
# [[tool.uv.index]]
# name ="hexaly"
# url = "https://pip.hexaly.com"
# explict = true
# [tool.uv.sources]
# hexaly = { index = "hexaly" }
# ///

import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    from dataclasses import dataclass
    from ortools.sat.python import cp_model
    import opt_note.scsp as scsp


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 順序制約付き巡回セールスマン問題として定式化する
    """)
    return


@app.class_definition
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        nodes = [
            (sidx, cidx)
            for sidx, s in enumerate(self.instance)
            for cidx, _ in enumerate(s)
        ]
        order = [cpmodel.new_int_var(1, len(nodes), "") for _ in nodes]

        dummy_idx = len(nodes)
        order.append(cpmodel.new_constant(0))

        arcs = []
        costs = dict()

        for nidx, (sidx, cidx) in enumerate(nodes):
            if cidx == 0:
                arcs.append((dummy_idx, nidx, cpmodel.new_bool_var("")))
                costs[(dummy_idx, nidx)] = 1
            if cidx == len(self.instance[sidx]) - 1:
                arcs.append((nidx, dummy_idx, cpmodel.new_bool_var("")))
                costs[(nidx, dummy_idx)] = 0

        for nidx1, (sidx1, cidx1) in enumerate(nodes):
            for nidx2, (sidx2, cidx2) in enumerate(nodes):
                if sidx1 == sidx2 and cidx1 + 1 != cidx2:
                    continue
                s1 = self.instance[sidx1]
                s2 = self.instance[sidx2]
                arcs.append((nidx1, nidx2, cpmodel.new_bool_var("")))
                costs[(nidx1, nidx2)] = (
                    0 if sidx1 < sidx2 and s1[cidx1] == s2[cidx2] else 1
                )

        cpmodel.add_circuit(arcs)

        for nidx1, nidx2, v in arcs:
            if nidx2 == dummy_idx:
                continue
            cpmodel.add(order[nidx2] == order[nidx1] + 1).only_enforce_if(v)

        nidx = -1
        for s in self.instance:
            for cidx, _ in enumerate(s):
                nidx += 1
                if cidx == 0:
                    continue
                cpmodel.add(order[nidx - 1] < order[nidx])

        cpmodel.minimize(sum(costs[(nidx1, nidx2)] * v for (nidx1, nidx2, v) in arcs))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            solution = ""
            current_node = dummy_idx
            current_char: str | None = None
            current_sidxs: set[int] = set()
            complete = False
            while True:
                for nidx1, nidx2, v in arcs:
                    if nidx1 == current_node and cpsolver.boolean_value(v):
                        if nidx2 == dummy_idx:
                            complete = True
                            break
                        sidx, cidx = nodes[nidx2]

                        if self.instance[sidx][cidx] != current_char or sidx in current_sidxs:
                            solution += self.instance[sidx][cidx]
                            current_sidxs.clear()

                        current_node = nidx2
                        current_char = self.instance[sidx][cidx]
                        current_sidxs.add(sidx)
                if complete:
                    break
            self.solution = solution
        else:
            self.solution = None

        return self.solution


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt", log=True)
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt", log=True)
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt", log=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    う～ん非常に良くない.
    なんならただの線形計画問題としての定式化 `LINEAR_CPSAT` よりも悪い.
    """)
    return


if __name__ == "__main__":
    app.run()
