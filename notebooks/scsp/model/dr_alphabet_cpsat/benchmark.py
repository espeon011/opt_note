# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
#     "opt-note",
# ]
#
# [tool.uv.sources]
# opt-note = { git = "https://github.com/espeon011/opt_note" }
# ///

import marimo

__generated_with = "0.18.4"
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
    mo.md(r"""
    # ベンチマーク
    """)
    return


@app.cell
def _():
    Model = scsp.model.dr_alphabet_cpsat.Model
    return (Model,)


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="protein_n010k010.txt")
    return


@app.cell
def _(Model):
    scsp.util.bench(Model, example_filename="protein_n050k050.txt")
    return


if __name__ == "__main__":
    app.run()
