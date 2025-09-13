# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "nbformat==5.10.4",
#     "numpy==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")

with app.setup:
    # import numpy
    import didppy
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# DIDP with other bounds""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    DIDP ソルバーを使用した定式化において dual bound を計算する方法をインスタンス内の任意の 2 つの 文字列の SCS 長の最大値からインスタンス内の任意の 3 つの文字列の SCS 長の最大値に変更してみる. 

    これによって dual bound 自体はタイトになるものの, 
    事前計算のオーダーが $n^2 k^2$ から $n^3 k^3$ になり, 
    小さくないインスタンスに対してはそもそも DIDP による計算を開始できるようになるまでにかなり時間がかかるようになる. 
    例えば長さが一律で 10 の文字列が 50 個あるようなインスタンスでは 1 分近く事前計算をしたうえで Python カーネルが死んでしまった(`The Python kernel for file ...(略)... died unexpectedly.` と出力されていた)(もしかしたら Marimo の方の問題かもしれない). 


    小さいインスタンスに対しては確かに dual bound が改善した... 
    が今まで最適性を証明できていなかったインスタンスに対して最適性を証明できたりしたわけではなかった. 
    また, primal bound はあまり改善しなかった.
    """
    )
    return


@app.function
def boundtable_scs3(s1: str, s2: str, s3: str) -> list[list[list[int]]]:
    len1, len2, len3 = len(s1), len(s2), len(s3)

    # dp[i1][i2][i3]: s1[i1..] と s2[i2..] と s3[i3..] の SCS 長さ
    dp = [
        [
            [
                len1 + len2 + len3 + 1
                for _ in range(len3 + 1)
            ]
            for _ in range(len2 + 1)
        ]
        for _ in range(len1 + 1)
    ]

    for i1 in range(len1 + 1):
        dp[i1][len2][len3] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2][len3] = len2 - i2
    for i3 in range(len3 + 1):
        dp[len1][len2][i3] = len3 - i3

    for i1 in range(len1, -1, -1):
        for i2 in range(len2, -1, -1):
            for i3 in range(len3 , -1, -1):
                if [i1 == len1, i2 == len2, i3 == len3].count(True) >=2:
                    continue

                front_chars = ""
                if i1 < len1:
                    front_chars += s1[i1]
                if i2 < len2:
                    front_chars += s2[i2]
                if i3 < len3:
                    front_chars += s3[i3]
                front_chars = set(front_chars)

                pretransversals = [
                    (
                        i1 + 1 if i1 < len1 and s1[i1] == c else i1,
                        i2 + 1 if i2 < len2 and s2[i2] == c else i2,
                        i3 + 1 if i3 < len3 and s3[i3] == c else i3,
                    )
                    for c in front_chars
                ]
                min_i1, min_i2, min_i3 = pretransversals[0]
                min_length = dp[min_i1][min_i2][min_i3]
                for pre_i1, pre_i2, pre_i3 in pretransversals:
                    if dp[pre_i1][pre_i2][pre_i3] < min_length:
                        min_i1 = pre_i1
                        min_i2 = pre_i2
                        min_i3 = pre_i3
                        min_length = dp[pre_i1][pre_i2][pre_i3]

                dp[i1][i2][i3] = min_length + 1

    return dp


@app.function
def boundexpr_scs3len(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    exprs = []
    for idx1 in range(len(instance)):
        for idx2 in range(idx1 + 1, len(instance)):
            for idx3 in range(idx2 + 1, len(instance)):
                s1 = instance[idx1]
                s2 = instance[idx2]
                s3 = instance[idx3]
                index_var1 = index_vars[idx1]
                index_var2 = index_vars[idx2]
                index_var3 = index_vars[idx3]
                table_s1s2s3 = dpmodel.add_int_table(boundtable_scs3(s1, s2, s3))
                exprs.append(table_s1s2s3[index_var1, index_var2, index_var3])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound


@app.class_definition
class Model:
    def __init__(self, instance: list[str]):
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
                    chars.index(c)
                    for c in s
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

        # dual bound
        if True:
            dpmodel.add_dual_bound(boundexpr_scs3len(instance, dpmodel, index_vars))

        self.instance = instance
        self.dpmodel = dpmodel
        self.dpsolver = None
        self.solution = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.dpsolver = didppy.CABS(
            self.dpmodel,
            threads=12,
            time_limit=time_limit,
            quiet=(not log),
        )
        self.solution = self.dpsolver.search()
        return self

    def to_solution(self) -> str:
        return "".join([trans.name for trans in self.solution.transitions])


@app.function
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    model = Model(instance)
    model.solve(time_limit, log)
    return model.to_solution()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    大きいインスタンスでは正常に動作しないため, 一部のインスタンスに対して実験する. 
    具体的に, 以下のインスタンスはスキップ. 

    - `uniform_q05n050k010-010.txt`
    - `nucleotide_n050k050.txt`
    - `protein_n050k050.txt`
    """
    )
    return


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


if __name__ == "__main__":
    app.run()
