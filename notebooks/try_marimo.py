# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "ortools==9.11.4210",
# ]
# ///

import marimo

__generated_with = "0.9.33"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


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


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
