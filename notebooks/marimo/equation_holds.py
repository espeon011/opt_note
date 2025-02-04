# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "ortools==9.11.4210",
# ]
# ///

import marimo

__generated_with = "0.11.0"
app = marimo.App(layout_file="layouts/equation_holds.slides.json")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 方程式が成立するかどうかを表す Bool 変数""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        $x$ を 0-1 決定変数, $a, b$ を整数決定変数として

        $$
        x = 1 \iff a = b
        $$

        を実現する制約条件を考えたい. 
        まずは不等式の場合から考える.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 不等式の場合""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        $x$ を 0-1 決定変数, $a, b$ を整数決定変数として

        $$
        x = 1 \iff a \leq b
        $$

        を実現する制約は big-M 法を使えば次のように線形に書ける. 

        \begin{align*}
        a &\leq b + M (1 - x) \\
        a - 1 &\geq b - M x
        \end{align*}
        """
    )
    return


@app.cell
def _():
    from ortools.sat.python import cp_model
    return (cp_model,)


@app.cell
def _(cp_model):
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):

        def __init__(self, variables):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0

        def on_solution_callback(self):
            self.__solution_count = self.__solution_count + 1
            for v in self.__variables:
                print(f'{v}={self.value(v)}', end=' ')
            print()

        @property
        def solution_count(self):
            return self.__solution_count
    return (VarArraySolutionPrinter,)


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    lb_a, ub_a = (1, 5)
    lb_b, ub_b = (1, 5)
    model = cp_model.CpModel()
    x = model.new_bool_var('(a<=b)')
    a = model.new_int_var(lb_a, ub_a, 'a')
    b = model.new_int_var(lb_b, ub_b, 'b')
    _m = ub_b - lb_a + 1
    model.add(a <= b + _m * (1 - x))
    model.add(a - 1 >= b - _m * x)
    model

    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([x, a, b])
    solver.parameters.enumerate_all_solutions = True
    status = solver.solve(model, solution_printer)
    return (
        a,
        b,
        lb_a,
        lb_b,
        model,
        solution_printer,
        solver,
        status,
        ub_a,
        ub_b,
        x,
    )


@app.cell
def _(cp_model, solution_printer, solver, status):
    print(f'Number of solutions found: {solution_printer.solution_count}\n')
    _statuses = {cp_model.OPTIMAL: 'OPTIMAL', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.MODEL_INVALID: 'MODEL_INVALID', cp_model.UNKNOWN: 'UNKNOWN'}
    print(f'status = {_statuses[status]}')
    print(f'time = {solver.wall_time}')
    print(f'objective value = {solver.objective_value}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 方程式の場合""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        big-M 法を用いれば方程式の場合も線形に表すことができる. 

        - $x = 1 \iff a \leq b$ を表す制約
          - $a \leq b + M (1 - x)$
          - $a - 1 \geq b - M x$
        - $y = 1 \iff a \geq b$ を表す制約
          - $b \leq a + M (1 - y)$
          - $b - 1 \geq a - M y$
        - $z = x \land y$ を表す制約
          - $z + 1 \geq x + y$
          - $2 z \leq x + y$

        これで
        $z = 1 \iff a = b$
        となる.
        """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    lb_a_1, ub_a_1 = (1, 5)
    lb_b_1, ub_b_1 = (1, 5)
    model_1 = cp_model.CpModel()
    x_1 = model_1.new_bool_var('(a<=b)')
    y = model_1.new_bool_var('(a>=b)')
    z = model_1.new_bool_var('(a==b)')
    a_1 = model_1.new_int_var(lb_a_1, ub_a_1, 'a')
    b_1 = model_1.new_int_var(lb_b_1, ub_b_1, 'b')
    _m = max(ub_a_1 - lb_b_1 + 1, ub_b_1 - lb_a_1 + 1)
    model_1.add(a_1 <= b_1 + _m * (1 - x_1))
    model_1.add(a_1 - 1 >= b_1 - _m * x_1)
    model_1.add(b_1 <= a_1 + _m * (1 - y))
    model_1.add(b_1 - 1 >= a_1 - _m * y)
    model_1.add(z + 1 >= x_1 + y)
    model_1.add(2 * z <= x_1 + y)
    model_1

    solver_1 = cp_model.CpSolver()
    solution_printer_1 = VarArraySolutionPrinter([z, x_1, y, a_1, b_1])
    solver_1.parameters.enumerate_all_solutions = True
    status_1 = solver_1.solve(model_1, solution_printer_1)
    return (
        a_1,
        b_1,
        lb_a_1,
        lb_b_1,
        model_1,
        solution_printer_1,
        solver_1,
        status_1,
        ub_a_1,
        ub_b_1,
        x_1,
        y,
        z,
    )


@app.cell
def _(cp_model, solution_printer_1, solver_1, status_1):
    print(f'Number of solutions found: {solution_printer_1.solution_count}\n')
    _statuses = {cp_model.OPTIMAL: 'OPTIMAL', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.MODEL_INVALID: 'MODEL_INVALID', cp_model.UNKNOWN: 'UNKNOWN'}
    print(f'status = {_statuses[status_1]}')
    print(f'time = {solver_1.wall_time}')
    print(f'objective value = {solver_1.objective_value}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## `only_enforce_if()` の利用""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Google OR-Tools には `only_enforce_if()` 関数があり, 
        特定の Bool 変数が `True` のときのみ制約を ON にすることができる.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 同値でなくてもよい場合""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        下記を直接制約に加える. 

        $$
        x = 1 \Longrightarrow a = b
        $$
        """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    lb_a_2, ub_a_2 = (1, 5)
    lb_b_2, ub_b_2 = (1, 5)
    model_2 = cp_model.CpModel()
    x_2 = model_2.new_bool_var('(a==b)')
    a_2 = model_2.new_int_var(lb_a_2, ub_a_2, 'a')
    b_2 = model_2.new_int_var(lb_b_2, ub_b_2, 'b')
    model_2.add(a_2 == b_2).only_enforce_if(x_2)
    model_2

    solver_2 = cp_model.CpSolver()
    solution_printer_2 = VarArraySolutionPrinter([x_2, a_2, b_2])
    solver_2.parameters.enumerate_all_solutions = True
    status_2 = solver_2.solve(model_2, solution_printer_2)
    return (
        a_2,
        b_2,
        lb_a_2,
        lb_b_2,
        model_2,
        solution_printer_2,
        solver_2,
        status_2,
        ub_a_2,
        ub_b_2,
        x_2,
    )


@app.cell
def _(cp_model, solution_printer_2, solver_2, status_2):
    print(f'Number of solutions found: {solution_printer_2.solution_count}\n')
    _statuses = {cp_model.OPTIMAL: 'OPTIMAL', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.MODEL_INVALID: 'MODEL_INVALID', cp_model.UNKNOWN: 'UNKNOWN'}
    print(f'status = {_statuses[status_2]}')
    print(f'time = {solver_2.wall_time}')
    print(f'objective value = {solver_2.objective_value}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 同値にしたい場合""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        上記の

        $$
        x = 1 \Longrightarrow a = b
        $$

        に加えてその裏を制約に入れることで同値にできる: 

        $$
        x = 0 \Longrightarrow a \ne b
        $$
        """
    )
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    lb_a_3, ub_a_3 = (1, 5)
    lb_b_3, ub_b_3 = (1, 5)
    model_3 = cp_model.CpModel()
    x_3 = model_3.new_bool_var('(a==b)')
    a_3 = model_3.new_int_var(lb_a_3, ub_a_3, 'a')
    b_3 = model_3.new_int_var(lb_b_3, ub_b_3, 'b')
    model_3.add(a_3 == b_3).only_enforce_if(x_3)
    model_3.add(a_3 != b_3).only_enforce_if(x_3.negated())
    model_3

    solver_3 = cp_model.CpSolver()
    solution_printer_3 = VarArraySolutionPrinter([x_3, a_3, b_3])
    solver_3.parameters.enumerate_all_solutions = True
    status_3 = solver_3.solve(model_3, solution_printer_3)
    return (
        a_3,
        b_3,
        lb_a_3,
        lb_b_3,
        model_3,
        solution_printer_3,
        solver_3,
        status_3,
        ub_a_3,
        ub_b_3,
        x_3,
    )


@app.cell
def _(cp_model, solution_printer_3, solver_3, status_3):
    print(f'Number of solutions found: {solution_printer_3.solution_count}\n')
    _statuses = {cp_model.OPTIMAL: 'OPTIMAL', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.MODEL_INVALID: 'MODEL_INVALID', cp_model.UNKNOWN: 'UNKNOWN'}
    print(f'status = {_statuses[status_3]}')
    print(f'time = {solver_3.wall_time}')
    print(f'objective value = {solver_3.objective_value}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 応用: 誰が祠を""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        X のポスト([https://x.com/mrsolyu/status/1846512850879275074](https://x.com/mrsolyu/status/1846512850879275074))でこういった問題があったので定式化して犯人を求める. 

        > お前達の誰かが、あの祠を壊したんか！？
        > 
        > A「俺がやりました」\
        > B「犯人は2人いる」\
        > C「Dが犯人でないなら僕が犯人」\
        > D「4人の中で嘘つきは奇数人」
        > 
        > 犯人はこの中にいるはずじゃ。そして呪いで嘘しかつけなくなっておるわい。
        > 誰が祠を壊したかのう？

        総当たりで探索しても一瞬で終わる程度の規模ではあるが, 練習のために定式化と実装を行う.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 定式化""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### 変数

        - $x_A, x_B, x_C, x_D$: A ~ D が嘘つきのとき $1$, 正直もののとき $0$
        - $y_A, y_B, y_C, y_D$: A ~ D が犯人のとき $1$, そうでないとき $0$

        #### 制約

        - 祠を壊したものは呪いで嘘しかつけなくなっている
          - $y_* <= x_*$
        - A「俺がやりました」
          - $x_A = 0 \Longrightarrow y_A = 1$
          - $x_A = 1 \Longrightarrow y_A = 0$
          - 上記 2 つをまとめて $x_A = 1 - y_A$ と書ける
        - B「犯人は2人いる」
            - $x_B = 0 \Longrightarrow y_A + y_B + y_C + y_D = 2$
            - $x_B = 1 \Longrightarrow y_A + y_B + y_C + y_D \ne 2$
        - C「Dが犯人でないなら僕が犯人」
          - $x_C = 0 \Longrightarrow$ 「$y_D = 0 \Longrightarrow y_C = 1$」だがこれは $1 - x_C \leq y_C + y_D$ と同値
          - $x_C = 1 \Longrightarrow$ 「$y_D = 0 \land y_C = 0$」だがこれは $2 (1 - x_C) \geq y_C + y_D$ と同値
        - D「4人の中で嘘つきは奇数人」
          - $x_D = 0 \Longrightarrow x_A + x_B + x_C + x_D \equiv 1 \mod 2$
          - $x_D = 1 \Longrightarrow x_A + x_B + x_C + x_D \equiv 0 \mod 2$
          - 上記をまとめて $x_A + x_B + x_C + x_D \equiv 1 - x_D \mod 2$ として実装する
          - この条件は線形にすることができる.
            $e, o$ を 0-1 決定変数とし, 嘘つきの数が偶数人か奇数人かに対応させるとする.
            この条件は次のように書ける. $s_e, z$ を整数決定変数として,

            - $e + o = 1$
            - $x_D = e$
            - $s_e = 2 * z$
            - $x_A + x_B + x_C + x_D = s_e + o$

            とすればよい.
            こうして A から D までの全ての条件は線形制約で記述できる.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 実装""")
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    model_4 = cp_model.CpModel()
    suspects = ['A', 'B', 'C', 'D']
    liar = {s: model_4.new_bool_var(f'{s}_is_liar') for s in suspects}
    culprit = {s: model_4.new_bool_var(f'{s}_is_culprit') for s in suspects}
    for _s in suspects:
        model_4.add_implication(culprit[_s], liar[_s])
    model_4.add_bool_xor(liar['A'], culprit['A'])
    model_4.add(sum((culprit[_s] for _s in suspects)) == 2).only_enforce_if(liar['B'].negated())
    model_4.add(sum((culprit[_s] for _s in suspects)) != 2).only_enforce_if(liar['B'])
    model_4.add_implication(culprit['D'].negated(), culprit['C']).only_enforce_if(liar['C'].negated())
    model_4.add(culprit['C'] == 0).only_enforce_if(liar['C'])
    model_4.add(culprit['D'] == 0).only_enforce_if(liar['C'])
    n_liar = model_4.new_int_var(0, len(suspects), 'num_of_liars')
    model_4.add(n_liar == sum((liar[_s] for _s in suspects)))
    model_4.add_modulo_equality(liar['D'].negated(), n_liar, 2)
    model_4.add(sum((culprit[_s] for _s in suspects)) >= 1)

    solver_4 = cp_model.CpSolver()
    solution_printer_4 = VarArraySolutionPrinter(list(liar.values()) + list(culprit.values()))
    solver_4.parameters.enumerate_all_solutions = True
    status_4 = solver_4.solve(model_4, solution_printer_4)
    return (
        culprit,
        liar,
        model_4,
        n_liar,
        solution_printer_4,
        solver_4,
        status_4,
        suspects,
    )


@app.cell
def _(cp_model, solution_printer_4, solver_4, status_4):
    print(f'Number of solutions found: {solution_printer_4.solution_count}\n')
    _statuses = {cp_model.OPTIMAL: 'OPTIMAL', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.MODEL_INVALID: 'MODEL_INVALID', cp_model.UNKNOWN: 'UNKNOWN'}
    print(f'status = {_statuses[status_4]}')
    print(f'time = {solver_4.wall_time}')
    print(f'objective value = {solver_4.objective_value}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 実装(線形版)""")
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model, culprit, liar, model_4, suspects):
    for _s in suspects:
        model_4.add(culprit[_s] <= liar[_s])
    model_4.add(1 - liar['A'] == culprit['A'])
    y_1 = model_4.new_bool_var('(culprits<=2)')
    z_1 = model_4.new_bool_var('(culprits>=2)')
    _m = 10
    model_4.add(sum((culprit[_s] for _s in suspects)) <= 2 + _m * (1 - y_1))
    model_4.add(sum((culprit[_s] for _s in suspects)) - 1 >= 2 - _m * y_1)
    model_4.add(2 <= sum((culprit[_s] for _s in suspects)) + _m * (1 - z_1))
    model_4.add(2 - 1 >= sum((culprit[_s] for _s in suspects)) - _m * z_1)
    model_4.add(1 - liar['B'] + 1 >= y_1 + z_1)
    model_4.add(2 * (1 - liar['B']) <= y_1 + z_1)
    model_4.add(1 - liar['C'] <= culprit['C'] + culprit['D'])
    model_4.add(2 * (1 - liar['C']) >= culprit['C'] + culprit['D'])
    e = model_4.new_bool_var('n_liar_is_even')
    o = model_4.new_bool_var('n_liar_is_odd')
    model_4.add(e + o == 1)
    model_4.add(liar['D'] == e)
    se = model_4.new_int_var(0, len(liar) // 2, 'n_liar//2')
    model_4.add(sum((liar[_s] for _s in suspects)) == 2 * se + o)
    model_4.add(sum((culprit[_s] for _s in suspects)) >= 1)
    model_4

    solver_5 = cp_model.CpSolver()
    solution_printer_5 = VarArraySolutionPrinter(list(liar.values()) + list(culprit.values()))
    solver_5.parameters.enumerate_all_solutions = True
    status_5 = solver_5.solve(model_4, solution_printer_5)
    return e, o, se, solution_printer_5, solver_5, status_5, y_1, z_1


@app.cell
def _(cp_model, solution_printer_5, solver_5, status_5):
    print(f'Number of solutions found: {solution_printer_5.solution_count}\n')
    _statuses = {cp_model.OPTIMAL: 'OPTIMAL', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.MODEL_INVALID: 'MODEL_INVALID', cp_model.UNKNOWN: 'UNKNOWN'}
    print(f'status = {_statuses[status_5]}')
    print(f'time = {solver_5.wall_time}')
    print(f'objective value = {solver_5.objective_value}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 補足

        犯人が 1 人以上いると仮定すると犯人は B でそれ以外は無実だった. 
        全員が犯人でないケースもあり得たが今回は除外. 
        嘘つきかどうかに関しては D 以外は全員嘘つきで確定していて, D は嘘つきでも正直ものでもどちらでも整合する. 

        `add_modulo_equality()` の引数に式をそのまま入れてしまうと `MODEL_INVALID` になってしまった. 
        他の関数, 例えば `add_multiplication_equality()` でも同様のことが起こったため, 
        線形でない制約を追加する際は式を新しい変数に格納してから渡すと安全そう. 

        また, `add_modulo_equality()` の返り値に `only_enforce_if()` を繋げたら `MODEL_INVALID` となってしまった. 
        ドキュメントには書かれていなかったが `only_enforce_if()` が使える制約と使えない制約があるようで, 
        例えば `add_bool_xor()` は明確に

        > In contrast to add_bool_or and add_bool_and, it does not support .only_enforce_if().

        と書かれている. 
        (`model.add(a != b)` には `only_enforce_if()` をつなげることができたのでなぜこうなっているかは謎)
        """
    )
    return


if __name__ == "__main__":
    app.run()
