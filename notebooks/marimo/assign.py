# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy==2.2.0",
#     "ortools==9.11.4210",
#     "scipy==1.14.1",
# ]
# ///

import marimo

__generated_with = "0.9.33"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""# 割当問題""")
    return


@app.cell
def __():
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    from ortools.math_opt.python import mathopt
    import time
    return linear_sum_assignment, mathopt, np, time


@app.cell
def __(np):
    n = 1000
    np.random.seed(seed=0)
    cost = np.random.randint(100, 1000, size=(n, n))
    v = list(range(n))
    return cost, n, v


@app.cell
def __(cost, linear_sum_assignment, time):
    _start = time.time()
    row_ind, col_ind = linear_sum_assignment(cost)
    _end = time.time()
    _elapsed = _end - _start
    print(cost[row_ind, col_ind].sum())
    print(f"Wall time: {_elapsed} s")
    return col_ind, row_ind


@app.cell
def __(cost, mathopt, v):
    model = mathopt.Model(name="assign")

    x = {}
    for i in v:
        for j in v:
            # x[i, j] = model.add_binary_variable(name=f"x[{i},{j}]")
            x[i, j] = model.add_variable(lb=0, ub=1, name=f"x[{j},{i}]") # 割り当て問題は連続変数でも解が 0 か 1 になる

    for j in v:
        model.add_linear_constraint(sum(x[i, j] for i in v) == 1)
    for i in v:
        model.add_linear_constraint(sum(x[i, j] for j in v) == 1)

    model.minimize(sum(cost[i, j] * x[i, j] for i in v for j in v))
    return i, j, model, x


@app.cell
def __(mathopt, model):
    _params = mathopt.SolveParameters(enable_output=True)
    _result = mathopt.solve(model, mathopt.SolverType.GSCIP, params=_params)
    if _result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f'model failed to solve: {_result.termination}')
    return


@app.cell
def __(mathopt, model):
    _params = mathopt.SolveParameters(enable_output=True)
    _result = mathopt.solve(model, mathopt.SolverType.HIGHS, params=_params)
    if _result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f'model failed to solve: {_result.termination}')
    return


@app.cell
def __(mathopt, model):
    _params = mathopt.SolveParameters(enable_output=True)
    _result = mathopt.solve(model, mathopt.SolverType.GLOP, params=_params)
    if _result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f'model failed to solve: {_result.termination}')
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
