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

__generated_with = "0.16.0"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    import opt_note.scsp as scsp


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# ベンチマーク""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 注意点""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Dual bound を表示しているが, これはアルファベットアルゴリズムで構築した解の部分配列の中で最短のものを求める問題の dual bound であり, 与えられた SCSP に対する dual bound ではない事に注意. 

    最適性に関しても同様で, `OPTIMAL` と出ている場合はアルファベットアルゴリズムで構築した解の部分列の中では最短であるというだけであり, 実際に最短とは限らない. 
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    実際に簡単なケースで実験をする. 
    `ba`, `cb` の最短共通超配列は `cba` である: 
    """
    )
    return


@app.cell
def _():
    _instance = ["ba", "cb"]
    _model = scsp.model.didp.Model(_instance).solve()
    _solution = _model.to_solution()
    scsp.util.show(_instance)
    scsp.util.show(_instance, _solution)

    print(f"solution is optimal: {_model.solution.is_optimal}")
    print(f"bset bound: {_model.solution.best_bound}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""一方, この方法では長さが 4 の共通超配列が最適となってしまう: """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 本題""")
    return


@app.cell
def _():
    _instance = ["ba", "cb"]
    _model = scsp.model.alphabet_reduction_cpsat.Model(_instance).solve()
    _solution = _model.to_solution()
    scsp.util.show(_instance)
    scsp.util.show(_instance, _solution)

    print(f"solution status: {_model.cpsolver.status_name()}")
    print(f"best bound: {_model.cpsolver.best_objective_bound}")
    return


@app.function
def bench(instance: list[str]) -> None:
    model = scsp.model.alphabet_reduction_cpsat.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"best bound: {model.cpsolver.best_objective_bound}")


@app.cell
def _():
    bench(scsp.example.load("uniform_q26n004k015-025.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("uniform_q26n008k015-025.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("uniform_q26n016k015-025.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("uniform_q05n010k010-010.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("uniform_q05n050k010-010.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("nucleotide_n010k010.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("nucleotide_n050k050.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("protein_n010k010.txt"))
    return


@app.cell
def _():
    bench(scsp.example.load("protein_n050k050.txt"))
    return


if __name__ == "__main__":
    app.run()
