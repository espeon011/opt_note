# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import nbformat
    import util
    return mo, util


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Weighted Majority Merge アルゴリズム""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - 計算量: ?
    - 近似精度: なし
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    与えられた文字列たちの先頭の文字列を調べ, 優先度の高い順に採用していく流れは Majority Merge と同じ. 
    Weighted Majority Merge では出現するか否かの代わりに残された文字列長を考えた重み付き出現回数を採用する. 

    - 解 $\mathrm{sol}$ を空文字列で初期化する.
    - 各文字 $c$ に対し重要度 $\sum_{i=1, \ s_i[0] = c}^n |s_i|$ を計算し, 重要度が最大である $c$ を求める.
    - $\mathrm{sol}$ の後ろに $c$ を追加する.
    - 各文字列 $s_1, s_2, \dots, s_n$ に対し, 先頭の文字が $c$ である場合は先頭 1 文字を削除する.
    - $s_1, s_2, \dots, s_n$ が全て空文字列になれば終了.
    """
    )
    return


@app.function
def solve(instance: list[str]) -> str:
    chars = sorted(list(set("".join(instance))))
    indices = [0 for _ in instance]
    solution = ""

    while not all(idx == len(s) for idx, s in zip(indices, instance)):
        counts = [
            sum(
                len(s) - idx
                for idx, s in zip(indices, instance)
                if idx < len(s) and s[idx] == c
            )
            for c in chars
        ]
        next_char = chars[counts.index(max(counts))]

        solution += next_char
        for jdx in range(len(instance)):
            s = instance[jdx]
            idx = indices[jdx]
            if idx < len(s) and s[idx] == next_char:
                indices[jdx] += 1

    return solution


@app.cell
def _(util):
    _instance = util.parse("uniform_q26n004k015-025.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("uniform_q26n008k015-025.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("uniform_q26n016k015-025.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("uniform_q05n010k010-010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("uniform_q05n050k010-010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


if __name__ == "__main__":
    app.run()
