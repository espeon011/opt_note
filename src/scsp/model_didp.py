# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "nbformat==5.10.4",
# ]
# ///

import marimo

__generated_with = "0.15.3"
app = marimo.App(width="medium")

with app.setup:
    import enum
    from collections.abc import Callable
    import didppy
    import util

    # Dual Bound を追加で設定する関数の型
    type TypeBoundExprFunc = Callable[
        [list[str], didppy.Model, list[didppy.ElementVar]],
        didppy.IntExpr
    ]


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# DIDP を用いたモデル""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""考案者の解説記事: [動的計画法ベースの数理最適化ソルバDIDPPyで最短共通超配列問題を解く](https://zenn.dev/okaduki/articles/7f9a3f3c54bc98)""")
    return


@app.function
def boundtable_scs2(s1: str, s2: str) -> list[list[int]]:
    len1, len2 = len(s1), len(s2)

    dp = [[len1 + len2 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i1 in range(len1 + 1):
        dp[i1][len2] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2] = len2 - i2

    for i1 in range(len1 - 1, -1, -1):
        for i2 in range(len2 - 1, -1, -1):
            if s1[i1] == s2[i2]:
                dp[i1][i2] = dp[i1 + 1][i2 + 1] + 1
            else:
                dp[i1][i2] = min(dp[i1 + 1][i2], dp[i1][i2 + 1]) + 1

    return dp


@app.function
def boundexpr_scs2len(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    exprs = []
    for idx1, (s1, index_var1) in enumerate(zip(instance, index_vars)):
        for idx2, (s2, index_var2) in enumerate(zip(instance, index_vars)):
            if idx2 >= idx1:
                continue
            table_idx1_idx2 = dpmodel.add_int_table(boundtable_scs2(s1, s2))
            exprs.append(table_idx1_idx2[index_var1, index_var2])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound


@app.class_definition
class Model:
    def __init__(
        self,
        instance: list[str],
        extra_bounds: list[TypeBoundExprFunc] | None = None,
    ):
        chars = sorted(list(set("".join(instance))))

        dpmodel = didppy.Model(maximize=False, float_cost=False)

        index_types = [dpmodel.add_object_type(number=len(s) + 1) for s in instance]
        index_vars = [
            dpmodel.add_element_var(object_type=index_type, target=0)
            for index_type in index_types
        ]

        instance_table = dpmodel.add_element_table(
            [
                [
                    chars.index(c) for c in s
                ] + [len(chars)]
                for s in instance
            ]
        )

        dpmodel.add_base_case(
            [
                index_var == len(s)
                for s, index_var in zip(instance, index_vars)
            ]
        )

        # 文字 char に従って進む
        for id_char, char in enumerate(chars):
            condition = didppy.Condition(False)
            for sidx, index_var in enumerate(index_vars):
                condition |= (instance_table[sidx, index_var] == id_char)
            trans = didppy.Transition(
                name=f"{char}",
                cost=1 + didppy.IntExpr.state_cost(),
                effects=[
                    (
                        index_var,
                        (
                            instance_table[sidx, index_var] == id_char
                        ).if_then_else(index_var + 1, index_var),
                    )
                    for sidx, index_var in enumerate(index_vars)
                ],
                preconditions=[condition],
            )
            dpmodel.add_transition(trans)

        # 残っている文字列から 2 つを選んで SCS を取って長さが最大のものを Dual Bound とする. 
        dpmodel.add_dual_bound(boundexpr_scs2len(instance, dpmodel, index_vars))

        # 追加の Dual Bound があれば. 
        if extra_bounds:
            for bound_func in extra_bounds:
                dpmodel.add_dual_bound(bound_func(instance, dpmodel, index_vars))

        self.instance = instance
        self.dpmodel = dpmodel
        self.dpsolver = None
        self.solution = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.dpsolver = didppy.CABS(self.dpmodel, threads=12, time_limit=time_limit, quiet=(not log))
        self.solution = self.dpsolver.search()
        return self

    def to_solution(self) -> str:
        return "".join([trans.name for trans in self.solution.transitions])


@app.function
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    model = Model(instance)
    model.solve(time_limit, log)
    return model.to_solution()


@app.cell
def _():
    instance_01 = util.parse("uniform_q26n004k015-025.txt")
    model_01 = Model(instance_01)
    solution_01 = model_01.solve().to_solution()
    return instance_01, model_01, solution_01


@app.cell
def _(instance_01, model_01, solution_01):
    _instance = instance_01
    _model = model_01
    _solution = solution_01

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_02 = util.parse("uniform_q26n008k015-025.txt")
    model_02 = Model(instance_02)
    solution_02 = model_02.solve().to_solution()
    return instance_02, model_02, solution_02


@app.cell
def _(instance_02, model_02, solution_02):
    _instance = instance_02
    _model = model_02
    _solution = solution_02

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_03 = util.parse("uniform_q26n016k015-025.txt")
    model_03 = Model(instance_03)
    solution_03 = model_03.solve().to_solution()
    return instance_03, model_03, solution_03


@app.cell
def _(instance_03, model_03, solution_03):
    _instance = instance_03
    _model = model_03
    _solution = solution_03

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_04 = util.parse("uniform_q05n010k010-010.txt")
    model_04 = Model(instance_04)
    solution_04 = model_04.solve().to_solution()
    return instance_04, model_04, solution_04


@app.cell
def _(instance_04, model_04, solution_04):
    _instance = instance_04
    _model = model_04
    _solution = solution_04

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_05 = util.parse("uniform_q05n050k010-010.txt")
    model_05 = Model(instance_05)
    solution_05 = model_05.solve().to_solution()
    return instance_05, model_05, solution_05


@app.cell
def _(instance_05, model_05, solution_05):
    _instance = instance_05
    _model = model_05
    _solution = solution_05

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_06 = util.parse("nucleotide_n010k010.txt")
    model_06 = Model(instance_06)
    solution_06 = model_06.solve().to_solution()
    return instance_06, model_06, solution_06


@app.cell
def _(instance_06, model_06, solution_06):
    _instance = instance_06
    _model = model_06
    _solution = solution_06

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_07 = util.parse("nucleotide_n050k050.txt")
    model_07 = Model(instance_07)
    solution_07 = model_07.solve().to_solution()
    return instance_07, model_07, solution_07


@app.cell
def _(instance_07, model_07, solution_07):
    _instance = instance_07
    _model = model_07
    _solution = solution_07

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_08 = util.parse("protein_n010k010.txt")
    model_08 = Model(instance_08)
    solution_08 = model_08.solve().to_solution()
    return instance_08, model_08, solution_08


@app.cell
def _(instance_08, model_08, solution_08):
    _instance = instance_08
    _model = model_08
    _solution = solution_08

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _():
    instance_09 = util.parse("protein_n050k050.txt")
    model_09 = Model(instance_09)
    solution_09 = model_09.solve().to_solution()
    return instance_09, model_09, solution_09


@app.cell
def _(instance_09, model_09, solution_09):
    _instance = instance_09
    _model = model_09
    _solution = solution_09

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
        print(f"solution is optimal: {_model.solution.is_optimal}")
        print(f"best bound: {_model.solution.best_bound}")
    else:
        print("--- Solution not found ---")
    return


if __name__ == "__main__":
    app.run()
