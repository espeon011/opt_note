# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.11.0",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==5.6.0",
# ]
# ///

import marimo

__generated_with = "0.15.3"
app = marimo.App(width="medium")

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
    mo.md(
        r"""
    元々の `AUTOMATON_CPSAT` の定式化において無効な文字と有効な文字に関する制約がなくなれば性能が良くなるんじゃないかと思っていたけど, 
    有効無効に関する制約をなくしたこのモデルでも 1 回の最適化計算時間が長く, 反復回数が稼げなかった. 
    この結果を見る限りオートマトン制約部分の定式化がそんなに良くなさそう.
    """
    )
    return


@app.function
def bench(instance: list[str]) -> None:
    model = scsp.model.automaton_cpsat_sat.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
        print(f"solution is optimal: {model.len_lb == model.len_ub}")
        print(f"bset bound: {model.best_bound()}")
    else:
        print("--- Solution not found ---")


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
