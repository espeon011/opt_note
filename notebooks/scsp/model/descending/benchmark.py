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


@app.function
def bench(instance: list[str]) -> None:
    solution = scsp.model.descending.solve(instance)
    scsp.util.show(instance)
    scsp.util.show(instance, solution)
    print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")


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
