# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
#     "hexaly>=14.0.20250828",
# ]
# [[tool.uv.index]]
# url = "https://pip.hexaly.com/"
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")

with app.setup:
    import model_wmm_hexaly
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Hexaly を用いたヒューリスティックに初期重みを追加""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    `WMM_HEXALY` モデルにおいて重み決定変数の初期値を `WMM` と等しくなるように設定する. 

    巨大なインスタンスにおいて常に `WMM` 以上の質の解が出る反面, 小さ目のインスタンスでは `WMM_HEXALY` と比較して悪化することがある.
    """
    )
    return


@app.function
def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str:
    return (
        model_wmm_hexaly.Model(instance, initial=True)
        .solve(time_limit, log)
        .to_solution()
    )


@app.cell
def _():
    instance_01 = util.parse("uniform_q26n004k015-025.txt")
    solution_01 = solve(instance_01, log=True)
    return instance_01, solution_01


@app.cell
def _(instance_01, solution_01):
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
def _():
    instance_02 = util.parse("uniform_q26n008k015-025.txt")
    solution_02 = solve(instance_02, log=True)
    return instance_02, solution_02


@app.cell
def _(instance_02, solution_02):
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
def _():
    instance_03 = util.parse("uniform_q26n016k015-025.txt")
    solution_03 = solve(instance_03, log=True)
    return instance_03, solution_03


@app.cell
def _(instance_03, solution_03):
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
def _():
    instance_04 = util.parse("uniform_q05n010k010-010.txt")
    solution_04 = solve(instance_04, log=True)
    return instance_04, solution_04


@app.cell
def _(instance_04, solution_04):
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
def _():
    instance_05 = util.parse("uniform_q05n050k010-010.txt")
    solution_05 = solve(instance_05, log=True)
    return instance_05, solution_05


@app.cell
def _(instance_05, solution_05):
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
def _():
    instance_06 = util.parse("nucleotide_n010k010.txt")
    solution_06 = solve(instance_06, log=True)
    return instance_06, solution_06


@app.cell
def _(instance_06, solution_06):
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
def _():
    instance_07 = util.parse("nucleotide_n050k050.txt")
    solution_07 = solve(instance_07, log=True)
    return instance_07, solution_07


@app.cell
def _(instance_07, solution_07):
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
def _():
    instance_08 = util.parse("protein_n010k010.txt")
    solution_08 = solve(instance_08, log=True)
    return instance_08, solution_08


@app.cell
def _(instance_08, solution_08):
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
def _():
    instance_09 = util.parse("protein_n050k050.txt")
    solution_09 = solve(instance_09, log=True)
    return instance_09, solution_09


@app.cell
def _(instance_09, solution_09):
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
