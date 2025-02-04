# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "ortools==9.11.4210",
# ]
# ///

import marimo

__generated_with = "0.11.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 極大ナップサック問題""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 問題""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        正整数の配列 $a = [ a_1, \dots, a_n]$ と整数 $\tau$ が与えられる. 
        このとき $a$ の部分配列でその**総積**が $\tau$ 以下になるもので極大なものを全て列挙せよ.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 定式化""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        $x = [x_1, \dots, x_n]$ を 0-1 決定変数とする. 
        $x_i$ が $1$ のとき $a_i$ を採用し, $0$ のとき採用しない. 
        また, 決定変数 $y = [y_1, \dots, y_n]$ を用意し $y_i = (a_i - 1) x_i + 1$ を課す. 
        こうすると $y_i$ は $x_i$ が $1$ のとき $a_i$ を値に取り, $0$ のとき $1$ を値にとる. 
        同様に $z_i = (a_i - 1) (1 - x_i) + 1$ とおく. 
        こちらは $y_i$ とは逆に採用されてない $a_i$ に対してだけ値 $a_i$ を取り, 採用されているものについては $1$ を取る. 

        Google OR-Tools は整数変数の積をそのまま扱えるため, 線形ではない定式化を行う. 

        - $\prod_{i=1}^n y_i \leq \tau$: 採用した $a_i$ の積が $\tau$ を超えない. 
        - $z_j \prod_{i=1}^n y_i > \tau (1 - x_j) \quad (\forall j = 1, \dots, n)$: 採用しなかった $a_j$ を掛けたら $\tau$ を超えてしまう. 

        また, Google OR-Tools の CP-SAT ソルバーは目的関数を設定しない場合, 
        実行可能解を全て求めるよう指示できるのでそれを使って全ての極大元を求める.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 実装""")
    return


@app.cell
def _():
    from ortools.sat.python import cp_model
    import math
    import time
    return cp_model, math, time


@app.cell
def _(cp_model, time):
    class SolutionPrinter(cp_model.CpSolverSolutionCallback):

        def __init__(self, a, solution: list[cp_model.IntVar]):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__solution = solution
            self.__a = a
            self.__solution_count = 0
            self.__all_solutions = []
            self.__start_time = time.time()

        @property
        def solution_count(self) -> int:
            return self.__solution_count

        @property
        def all_solutions(self):
            return self.__all_solutions

        def on_solution_callback(self):
            current_time = time.time()
            self.__solution_count = self.__solution_count + 1
            print(f'Solution {self.__solution_count}, time = {current_time - self.__start_time} s')
            print('  [', end=' ')
            for x in self.__solution:
                print(f'{self.value(x)}', end=' ')
            print(']')
            print('  [', end=' ')
            solution = []
            for i, x in enumerate(self.__solution):
                if self.value(x) == 1:
                    solution.append(self.__a[i])
                    print(f'{self.__a[i]}', end=' ')
            print(']')
            self.__all_solutions.append(solution)
    return (SolutionPrinter,)


@app.cell
def _(SolutionPrinter, cp_model):
    class Model:
        def __init__(self, a, tau):
            self.a = a
            self.tau = tau

            self.model = cp_model.CpModel()
            self.solver = cp_model.CpSolver()

            self.x = [self.model.new_bool_var(f"a{i} is used") for i in range(len(self.a))]
            y = [self.model.new_int_var(1, self.a[i], "") for i in range(len(self.a))]
            z = [self.model.new_int_var(1, self.a[i], "") for i in range(len(self.a))]

            for i in range(len(self.a)):
                self.model.add(y[i] == (self.a[i] - 1) * self.x[i] + 1)
                self.model.add(z[i] == (self.a[i] - 1) * (1 - self.x[i]) + 1)

            y_prod = self.model.new_int_var(1, tau, "")
            self.model.add_multiplication_equality(y_prod, y)
            for j in range(len(self.a)):
                y_prod_zj = self.model.new_int_var(1, tau * self.a[j], "")
                self.model.add_multiplication_equality(y_prod_zj, [z[j], y_prod])
                self.model.add(y_prod_zj >= self.tau * (1 - self.x[j]) + 1)

        def solve(self):
            self.solution_printer = SolutionPrinter(self.a, self.x)
            self.solver.parameters.enumerate_all_solutions = True
            #self.solver.parameters.log_search_progress = True
            self.solver.solve(self.model, self.solution_printer)
    return (Model,)


@app.cell
def _():
    # a = list(range(1, 5+1))
    # tau = 10

    # a = list(range(1, 10+1))
    # tau = 50

    a = list(range(1, 20+1))
    tau = 100

    # a = [2] * 20 # 終わらない
    # tau = 2 ** 10

    print(f"a = {a}")
    print(f"tau = {tau}")
    return a, tau


@app.cell
def _(Model, a, tau):
    model = Model(a, tau)
    model.solve()
    return (model,)


@app.cell
def _(model):
    model.solution_printer.all_solutions
    return


@app.cell
def _(model):
    print("Statistics")
    print(f"  conflicts      : {model.solver.num_conflicts}")
    print(f"  branches       : {model.solver.num_branches}")
    print(f"  wall time      : {model.solver.wall_time} s")
    print(f"  solutions found: {model.solution_printer.solution_count}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 結果

        掛け算を使った定式化は厳密ではあるものの数値が大きくなりすぎてしまう問題がある. 
        おとなしく $\log$ を使って線形計画問題にしよう.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 定式化(MILP)""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        $x = [x_1, \dots, x_n]$ を 0-1 決定変数とする. 
        $x_i$ が $1$ のとき $a_i$ を採用し, $0$ のとき採用しない. 

        $$
        w := \log(a_1) x_1 + \dots + \log(a_n) x_n
        $$

        とすると制約条件は以下のように書ける. 

        - $w \leq \log(\tau)$: 採用した $a_i$ の積が $\tau$ を超えない
        - $w + \log(a_i) (1 - x_i) > \log(\tau) (1 - x_i) \quad (\forall i = 1, \dots, n)$: 採用しなかった $a_j$ を掛けたら $\tau$ を超えてしまう. 

        CP-SAT ソルバーは整数しか扱えないので $\log(a_i)$ や $\log(\tau)$ は適当にスケールして小数点以下を切り捨てることにする.
        これによって誤差が出るかもしれない.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 実装(MILP)""")
    return


@app.cell
def _(SolutionPrinter, cp_model, math):
    class ModelLinear:
        def __init__(self, a, tau):
            self.a = a
            self.tau = tau
            base = 1000000
            self.log_a = [math.floor(math.log(ai) * base) for ai in a]
            self.log_tau = math.floor(math.log(self.tau) * base)
            print(f"log_a = {self.log_a}")
            print(f"log_tau = {self.log_tau}")
            self.model = cp_model.CpModel()
            self.solver = cp_model.CpSolver()
            self.x = [self.model.new_bool_var(f"a{i} is used") for i in range(len(self.a))]
            w = sum(a * x for a, x in zip(self.log_a, self.x))

            self.model.add(w <= self.log_tau)
            for a, x in zip(self.log_a, self.x):
                self.model.add(w + a * (1 - x) >= (self.log_tau + 1) * (1 - x))

        def solve(self):
            self.solution_printer = SolutionPrinter(self.a, self.x)
            self.solver.parameters.enumerate_all_solutions = True
            #self.solver.parameters.log_search_progress = True
            self.solver.solve(self.model, self.solution_printer)
    return (ModelLinear,)


@app.cell
def _(a, tau):
    print(f"a = {a}")
    print(f"tau = {tau}")
    return


@app.cell
def _(ModelLinear, a, tau):
    model_1 = ModelLinear(a, tau)
    model_1.solve()
    return (model_1,)


@app.cell
def _(model_1):
    model_1.solution_printer.all_solutions
    return


@app.cell
def _(model_1):
    print('Statistics')
    print(f' conflicts : {model_1.solver.num_conflicts}')
    print(f' branches : {model_1.solver.num_branches}')
    print(f' wall time : {model_1.solver.wall_time} s')
    print(f' solutions found: {model_1.solution_printer.solution_count}')
    return


if __name__ == "__main__":
    app.run()
