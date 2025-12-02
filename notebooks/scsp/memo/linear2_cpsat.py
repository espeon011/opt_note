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
    # バイナリ変数のみで線形計画問題として定式化 (CP-SAT)
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

        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か.
        sseq_valid = [cpmodel.new_bool_var("") for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か.
        sseq_char = [[cpmodel.new_bool_var("") for _ in chars] for _ in sseq_valid]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か.
        assign = [
            [[cpmodel.new_bool_var("") for _ in sseq_valid] for c in s]
            for s in self.instance
        ]

        # 共通超配列の i 番目にはどれか 1 文字だけが置かれる.
        # 共通超配列の i 番目に文字が置かれるかどうか.
        for xs, xv in zip(sseq_char, sseq_valid):
            cpmodel.add_at_most_one(xs)
            cpmodel.add_max_equality(xv, xs)

        # s 番目の文字列の c 番目の文字は共通超配列のどこか一か所にのみ置かれる.
        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                cpmodel.add_exactly_one(assign[sidx][cidx])

        # 共通超配列に置くときは同じ文字である必要がある.
        for idx, xs in enumerate(sseq_char):
            for j, _ in enumerate(chars):
                cpmodel.add_max_equality(
                    xs[j],
                    [
                        assign[sidx][cidx][idx]
                        for sidx, s in enumerate(self.instance)
                        for cidx, c in enumerate(s)
                        if c == chars[j]
                    ],
                )

        # s 番目の文字列の共通超配列への埋め込み順序固定.
        for sidx, s in enumerate(self.instance):
            order = [cpmodel.new_int_var(0, max_len - 1, "") for _ in s]
            for cidx, o in enumerate(order):
                cpmodel.add_map_domain(o, assign[sidx][cidx])
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                # cpmodel.add(
                #     sum(
                #         idx * assign[sidx][cidx - 1][idx]
                #         for idx, _ in enumerate(assign[sidx][cidx - 1])
                #     )
                #     + 1
                #     <= sum(
                #         idx * assign[sidx][cidx][idx]
                #         for idx, _ in enumerate(assign[sidx][cidx])
                #     )
                # )
                cpmodel.add(order[cidx - 1] < order[cidx])

        cpmodel.minimize(sum(sseq_valid))

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
            for v, cs in zip(sseq_valid, sseq_char):
                if not cpsolver.boolean_value(v):
                    continue
                for cv, c in zip(cs, chars):
                    if cpsolver.boolean_value(cv):
                        solution += c
                        break
            self.solution = solution
        else:
            self.solution = None

        return self.solution


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    割と良くなったかもしれない.
    """)
    return


if __name__ == "__main__":
    app.run()
