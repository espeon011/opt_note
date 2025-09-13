# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "nbformat==5.10.4",
#     "numpy==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")

with app.setup:
    import model_didp2
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 計算時間は度外視して最適値が知りたい""")
    return


@app.cell
def _():
    instance = [
        "aehdmmqrstuwv",
        "afiknllppaavxusqszab",
        "bgglopqsssv",
        "cabhiknaampawqryssuv",
        "dbhciknddmpdqryssuwc",
        "cajhiknapasqrssuvv",
        "dacngoaiatsimawxltsc",
        "zbndjkozfrizsyctviw",
    ]
    model = model_didp2.Model(instance)
    solution = model.solve(time_limit=1800, log=True).to_solution()
    return instance, model, solution


@app.cell
def _(instance, model, solution):
    util.show(instance)
    if solution is not None:
        util.show(instance, solution)
        print(f"solution is feasible: {util.is_feasible(instance, solution)}")
        print(f"solution is optimal: {model.solution.is_optimal}")
        print(f"best bound: {model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""計算時間は 20 分 46 秒だった. """)
    return


if __name__ == "__main__":
    app.run()
