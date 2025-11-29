# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.12.0",
#     "hexaly>=14.0.20251112",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==5.7.1",
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
    import pyscipopt
    import opt_note.scsp as scsp


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # バイナリ定式化と元の MILP の定式化と比較
    """)
    return


@app.class_definition
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0
    relax: bool = False

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)
        vtype = "C" if self.relax else "B"

        scip: pyscipopt.Model = pyscipopt.Model()

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か
        sseq_valid = [scip.addVar(vtype=vtype) for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か
        sseq_char = [[scip.addVar(vtype=vtype) for _ in chars] for _ in sseq_valid]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か
        assign = [
            [[scip.addVar(vtype=vtype) for _ in sseq_valid] for c in s]
            for s in self.instance
        ]

        for xs in sseq_char:
            scip.addCons(sum(xs) == 1)

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                scip.addCons(sum(assign[sidx][cidx]) == 1)
                for idx, _ in enumerate(assign[sidx][cidx]):
                    scip.addCons(assign[sidx][cidx][idx] <= sseq_valid[idx])
                    scip.addCons(
                        assign[sidx][cidx][idx] <= sseq_char[idx][chars.index(c)]
                    )

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                scip.addCons(
                    sum(
                        idx * assign[sidx][cidx - 1][idx]
                        for idx, _ in enumerate(assign[sidx][cidx - 1])
                    )
                    + 1
                    <= sum(
                        idx * assign[sidx][cidx][idx]
                        for idx, _ in enumerate(assign[sidx][cidx])
                    )
                )

        scip.setObjective(sum(sseq_valid), sense="minimize")

        if time_limit is not None:
            scip.setParam("limits/time", time_limit)
        if not log:
            scip.hideOutput()
        scip.optimize()

        self.best_bound = scip.getDualbound()

        if not self.relax and scip.getNLimSolsFound() > 0:
            solution = ""
            for valid, ssqc in zip(sseq_valid, sseq_char):
                if int(round(scip.getVal(valid))) == 1:
                    for c, sqc in zip(chars, ssqc):
                        if int(round(scip.getVal(sqc))) == 1:
                            solution += c
                            break
            self.solution = solution

        return self.solution


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    以下のインスタンスは DIDP を使ってモデルによって最適値が 62 だとわかっている.
    """)
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.linear_scip.Model,
        example_filename="uniform_q26n004k015-025.txt"
    )
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    バイナリ定式化は解なし. dual bound も非常に悪い.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 連続緩和問題を利用して dual bound を得る
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    元の MILP 定式化の連続緩和モデルと今回作成したバイナリ定式化の連続緩和モデルを比較する.
    """)
    return


@app.cell
def _():
    instance01 = scsp.example.load("uniform_q26n004k015-025.txt")
    return (instance01,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## バイナリ定式化の連続緩和モデルの実行結果
    """)
    return


@app.cell
def _(instance01):
    Model(instance01, relax=True).solve(log=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## MILP モデルの連続緩和モデル
    """)
    return


@app.class_definition
@dataclass
class ModelMILPContinuous:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        scip: pyscipopt.Model = pyscipopt.Model()

        max_len = sum(len(s) for s in self.instance)
        seqs = [
            [scip.addVar(vtype="C", lb=0, ub=max_len - 1) for _ in s]
            for s in self.instance
        ]

        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                scip.addCons(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(self.instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(self.instance, seqs)):
                if idx1 >= idx2:
                    continue

                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            big_m = max_len
                            lt = scip.addVar(vtype="C", lb=0, ub=1)
                            gt = scip.addVar(vtype="C", lb=0, ub=1)
                            scip.addCons(lt + gt == 1)
                            scip.addCons(cvar1 + 1 <= cvar2 + max_len * (1 - lt))
                            scip.addCons(cvar1 + max_len * (1 - gt) >= cvar2 + 1)

        obj = scip.addVar(vtype="C", lb=0, ub=max_len)
        for seq in seqs:
            scip.addCons(obj >= seq[-1])
        scip.setObjective(obj + 1, sense="minimize")

        if time_limit is not None:
            scip.setParam("limits/time", time_limit)
        if not log:
            scip.hideOutput()
        scip.optimize()

        self.best_bound = scip.getDualbound()

        return self.solution


@app.cell
def _(instance01):
    ModelMILPContinuous(instance01).solve(log=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    バイナリ定式化は筋が悪そう.
    連続緩和した問題も解くのに 16 秒近くかかっており, 目的関数値はバウンドとして使えるレベルのものではない.

    元の MILP 定式化の連続緩和はすぐ解けてバウンド値もバイナリ定式化のものより良いが,
    元々も MILP モデルのバウンドと同じくらいの値なのでわざわざ連続緩和する必要がない.
    """)
    return


if __name__ == "__main__":
    app.run()
