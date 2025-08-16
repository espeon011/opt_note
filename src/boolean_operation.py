# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
# ]
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from ortools.sat.python import cp_model
    return (cp_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# MIP における論理演算の扱い""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    $a, b$ を 0-1 決定変数とする. 
    このとき以下のような制約を持つ決定変数 $c$ の定め方を説明する.

    - AND: $c = a \land b$
    - OR: $c = a \lor b$
    - NAND: $c = a \uparrow b$
    - NOR: $c = a \downarrow b$
    - XOR: $c = a \veebar b$
    - XNOR: $c = (a \Leftrightarrow b)$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 定式化と実装""")
    return


@app.cell
def _(cp_model):
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, variables):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0

        def on_solution_callback(self):
            self.__solution_count += 1
            for v in self.__variables:
                print(f"{v}={self.value(v)}", end=" ")
            print()

        @property
        def solution_count(self):
            return self.__solution_count
    return (VarArraySolutionPrinter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### AND""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    $a \land b \Rightarrow c$ と $c \Rightarrow a \land b$ を表現すればよい. 

    - $a + b \leq 1 + c$
    - $2 c \leq a + b$ (あるいは $c \leq a \ \land \ c \leq b$)

    ---

    3 つ以上の変数の AND を考えたい場合, 
    $x_1, \dots, x_n$ を 0-1 決定変数とし,その AND を $r$ に入れたい場合を考える. 

    1. $2$ つの制約条件で定式化する場合
        - $\sum_{i=1}^n x_i + 1 \leq n + r$
        - $n r \leq \sum_{i=1}^n x_i$
    1. $n + 1$ 個の制約条件で定式化する場合
        - $\sum_{i=1}^n x_i + 1 \leq n + r$
        - $r \leq x_i \ (\forall i = 1, \dots, n)$

    どちらも同じ定式化だが, 問題を連続緩和した場合には下の定式化の方が強い定式化となり, 
    多面体の頂点が必ず格子点となる.
    """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _a = _model.new_bool_var("A")
    _b = _model.new_bool_var("B")
    _c = _model.new_bool_var(f"{_a}and{_b}")
    _model.add(_a + _b <= 1 + _c)
    _model.add(2 * _c <= _a + _b)
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter([_a, _b, _c])
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### OR""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    $a \lor b \Rightarrow c$ と $c \Rightarrow a \lor b$ を表現すればよい. 

    - $a + b \leq 2 c$ (あるいは $a \leq c \ \land \ b \leq c$)
    - $c \leq a + b$

    ---

    3 つ以上の変数の OR を考えたい場合, 
    $x_1, \dots, x_n$ を 0-1 決定変数とし,その OR を $r$ に入れたい場合を考える. 

    1. $2$ つの制約条件で定式化する場合
        - $\sum_{i=1}^n x_i \leq n r$
        - $r \leq \sum_{i=1}^n x_i$
    1. $n + 1$ 個の制約条件で定式化する場合
        - $x_i \leq r \ (\forall i = 1, \dots, n)$
        - $r \leq \sum_{i=1}^n x_i$

    どちらも同じ定式化だが, 問題を連続緩和した場合には下の定式化の方が強い定式化となり, 
    多面体の頂点が必ず格子点となる.
    """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _a = _model.new_bool_var("A")
    _b = _model.new_bool_var("B")
    _c = _model.new_bool_var(f"{_a}or{_b}")
    _model.add(_a + _b <= 2 * _c)
    _model.add(_c <= _a + _b)
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter([_a, _b, _c])
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### NAND""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    AND の定式化における $c$ を $1 - c$ に置き換えればよい. 

    - $a + b \leq 1 + (1 - c)$
    - $2 (1 - c) \leq a + b$

    あるいは AND で定式化した $c$ に対して $1 - c$ を用いる.
    """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _a = _model.new_bool_var("A")
    _b = _model.new_bool_var("B")
    _c = _model.new_bool_var(f"{_a}nand{_b}")
    _model.add(_a + _b <= 1 + (1 - _c))
    _model.add(2 * (1 - _c) <= _a + _b)
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter([_a, _b, _c])
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### NOR""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    OR の定式化における $c$ を $1 - c$ に置き換えれば良い. 

    - $a + b \leq 2 (1 - c)$
    - $1 - c \leq a + b$

    あるいは OR で定式化した $c$ に対して $1 - c$ を用いる.
    """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _a = _model.new_bool_var("A")
    _b = _model.new_bool_var("B")
    _c = _model.new_bool_var(f"{_a}nor{_b}")
    _model.add(_a + _b <= 2 * (1 - _c))
    _model.add(1 - _c <= _a + _b)
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter([_a, _b, _c])
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### XOR""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    $(a = 0 \land b = 0) \Rightarrow c = 0$, $(a = 1 \land b = 1) \Rightarrow c = 0$, $(a = 1 \land b = 0) \Rightarrow c = 1$, $(a = 0 \land b = 1) \Rightarrow c = 1$ を全て表現する. 

    - $(1 - a) + (1 - b) \leq 1 + (1 - c)$
    - $a + b \leq 1 + (1 - c)$
    - $a + (1 - b) \leq 1 + c$
    - $(1 - a) + b \leq 1 + c$
    """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _a = _model.new_bool_var("A")
    _b = _model.new_bool_var("B")
    _c = _model.new_bool_var(f"{_a}xor{_b}")
    _model.add(1 - _a + (1 - _b) <= 1 + (1 - _c))
    _model.add(_a + _b <= 1 + (1 - _c))
    _model.add(_a + (1 - _b) <= 1 + _c)
    _model.add(1 - _a + _b <= 1 + _c)
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter([_a, _b, _c])
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### XNOR""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    XOR の定式化における $c$ を $1 - c$ に置き換えれば良い. 

    - $(1 - a) + (1 - b) \leq 1 + c$
    - $a + b \leq 1 + c$
    - $a + (1 - b) \leq 1 + (1 - c)$
    - $(1 - a) + b \leq 1 + (1 - c)$

    あるいは XOR で定式化した $c$ に対して $1 - c$ を用いる.
    """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _a = _model.new_bool_var("A")
    _b = _model.new_bool_var("B")
    _c = _model.new_bool_var(f"{_a}xor{_b}")
    _model.add(1 - _a + (1 - _b) <= 1 + _c)
    _model.add(_a + _b <= 1 + _c)
    _model.add(_a + (1 - _b) <= 1 + (1 - _c))
    _model.add(1 - _a + _b <= 1 + (1 - _c))
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter([_a, _b, _c])
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


if __name__ == "__main__":
    app.run()
