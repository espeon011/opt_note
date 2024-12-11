# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "matplotlib==3.9.3",
#     "ortools==9.11.4210",
#     "pandas==2.2.3",
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
    mo.md(r"""# Marimo お試しノート""")
    return


@app.cell
def __():
    from ortools.math_opt.python import mathopt
    return (mathopt,)


@app.cell
def __(mathopt):
    # Build the model.
    model = mathopt.Model(name="getting_started_lp")
    x = model.add_variable(lb=-1.0, ub=1.5, name="x")
    #y = model.add_variable(lb=0.0, ub=1.0, name="y")
    y = model.add_binary_variable(name="y")
    model.add_linear_constraint(x + y <= 1.5)
    #model.maximize(x + 2 * y)
    model.maximize(x + 2 * y * y)
    return model, x, y


@app.cell
def __(mathopt, model):
    # Solve and ensure an optimal solution was found with no errors.
    # (mathopt.solve may raise a RuntimeError on invalid input or internal solver
    # errors.)
    params = mathopt.SolveParameters(enable_output=True)
    #result = mathopt.solve(model, mathopt.SolverType.CP_SAT, params=params)
    result = mathopt.solve(model, mathopt.SolverType.GSCIP, params=params)
    #result = mathopt.solve(model, mathopt.SolverType.HIGHS, params=params)
    if result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f"model failed to solve: {result.termination}")
    return params, result


@app.cell
def __(result, x, y):
    # Print some information from the result.
    print("MathOpt solve succeeded")
    print("Objective value:", result.objective_value())
    print("x:", result.variable_values()[x])
    print("y:", result.variable_values()[y])
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ## LaTeX
        You can embed LaTeX in Markdown.

        For example,

        ```python3
        mo.md(r'$f : \mathbb{R} \to \mathbb{R}$')
        ```

        renders $f : \mathbb{R} \to \mathbb{R}$, while

        ```python3
        mo.md(
            r'''
            \[
            f: \mathbb{R} \to \mathbb{R}
            \]
            '''
        )
        ```

        renders the display math

        \[
        f: \mathbb{R} \to \mathbb{R}.
        \]
        """
    )
    return


@app.cell
def __(mo):
    leaves = mo.ui.slider(1, 32, label="🍃: ")

    mo.md(
        f"""
        ### UI elements

        A `marimo.ui` object:

        ```python3
        leaves = mo.ui.slider(1, 16, label="🍃: ")
        mo.md(f"{{leaves}}")
        ```

        yields

        {leaves}
        """
    )
    return (leaves,)


@app.cell
def __(leaves, mo):
    mo.md(f"Your leaves: {'🍃' * leaves.value}")
    return


@app.cell
def __():
    import matplotlib.pyplot as plt
    plt.plot([1, 2])
    return (plt,)


@app.cell
def __():
    import pandas as pd
    pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    return (pd,)


@app.cell
def __(pd):
    df_web = pd.read_csv(
        'https://raw.githubusercontent.com/nkmk/python-snippets/master/notebook/data/src/sample_header.csv'
    )

    print(df_web)
    return (df_web,)


@app.cell
def __(df_web):
    df_web
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
