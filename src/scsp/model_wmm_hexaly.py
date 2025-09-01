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
    import hexaly.optimizer
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Hexaly を使ったヒューリスティック""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Hexaly の外部関数最適化機能を用いた定式化を紹介する. 
    Weighted Majority Merge アルゴリズムにおいて次の文字を選択する基準は各文字列に対する残長の和であった. 
    その残長の部分を Hexaly の決定変数で置き換える. 

    **決定変数**

    - $w_{ij} \in \mathbb{N}$: 文字列 $s_i$ の $j$ 文字目の重み. $(i \in \{ 1, \dots, n \}, \ j \in \{ 1, \dots, |s_i| \})$
        - $w_i = \{ w_{i,1} \dots, w_{i,|s_i|} \}$ とおく. 


    **目的関数**

    下記のアルゴリズムに従って構築した共通超配列の長さを目的関数とする. 

    - 解 $\mathrm{sol}$ を空文字列で初期化する. 
    - 各文字 $c$ に対して重み $\sum_{i=1, \ s_i[0] = c}^n w_{i,1}$ を計算し, 重みが最大である $c$ を求める.
    - $\mathrm{sol}$ の後ろに $c$ を追加する. 
    - 各文字列 $s_i \ (i \in \{ 1, \dots, n \})$ に対し, 先頭の文字が $c$ である場合は
        - $s_i$ の先頭の文字を削除する.
        - $w_i$ の先頭の重みを削除し, インデックスを前に詰める. 
    - $s_1, \dots, s_n$ 全てが空文字列になれば終了. $\mathrm{sol}$ が解.
    """
    )
    return


@app.class_definition
class Model:
    def __init__(self, instance, initial: bool = False):
        chars = sorted(list(set("".join(instance))))

        hxoptimizer = hexaly.optimizer.HexalyOptimizer()
        hxmodel = hxoptimizer.model

        max_weight = max(len(s) for s in instance) if initial else len(chars)
        priorities1d = [
            hxmodel.int(1, max_weight)
            for s in instance
            for cidx, _ in enumerate(s)
        ]

        func = hxmodel.create_int_external_function(self.objective)
        func.external_context.lower_bound = 0
        func.external_context.upper_bound = sum(len(s) for s in instance)

        indices_1d_to_2d = []
        counter = 0
        for s in instance:
            indices_1d_to_2d.append((counter, counter + len(s)))
            counter += len(s)

        self.instance = instance
        self.chars = chars
        self.hxoptimizer = hxoptimizer
        self.hxmodel = hxmodel
        self.priorities1d = priorities1d
        self.indices_1d_to_2d = indices_1d_to_2d

        # これらが実行される時点で self.* が必要になるため初期化の最後に移動

        hxmodel.minimize(func(*priorities1d))
        hxmodel.close()

        if initial:
            priorities2d = self.priorities_1d_to_2d(priorities1d)
            for sidx, s in enumerate(instance):
                for cidx, c in enumerate(s):
                    priorities2d[sidx][cidx].set_value(len(s) - cidx)

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        if time_limit is not None:
            self.hxoptimizer.param.time_limit = time_limit
        self.hxoptimizer.param.verbosity = 1 if log else 0
        self.hxoptimizer.solve()
        return self

    def to_solution(self) -> str | None:
        status = self.hxoptimizer.solution.status
        if status not in {
            hexaly.optimizer.HxSolutionStatus.OPTIMAL,
            hexaly.optimizer.HxSolutionStatus.FEASIBLE,
        }:
            return None

        priorities1d_value = [priority.value for priority in self.priorities1d]
        priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
        return self.wmm(priorities2d_value)

    def wmm(self, priorities2d: list[list[int]]) -> str:
        indices = [0] * len(self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(
            len(self.instance) * max(len(s) for s in self.instance)
        ):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                sum(
                    priorities2d[sidx][idx]
                    for sidx, (idx, s) in enumerate(
                        zip(indices, self.instance)
                    )
                    if idx < len(s) and s[idx] == c
                )
                for c in self.chars
            ]
            next_char = self.chars[counts.index(max(counts))]

            solution += next_char
            indices = [
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(indices, self.instance)
            ]

        return solution

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [
            priorities1d[start:end] for start, end in self.indices_1d_to_2d
        ]

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d.get(i) for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)


@app.function
def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()


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
