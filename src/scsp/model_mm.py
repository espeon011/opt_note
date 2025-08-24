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
    mo.md(r"""# Majority Merge アルゴリズム""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - 計算量: $O(qkn)$. この実装ではもっとかかる.
    - 近似精度: なし
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    与えられた文字列たちの先頭を調べ, 最も出現頻度が高い文字を採用し, 
    文字列たちの先頭から削除する操作を全ての文字列が空になるまで繰り返す. 

    - 解 $\mathrm{sol}$ を空文字列で初期化する.
    - 各文字列の先頭の文字 $s_1[0], s_2[0], \dots, s_n[0]$ を調べ, 最も多い文字を $c$ とする.
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
        fronts = [s[idx] for idx, s in zip(indices, instance) if idx < len(s)]
        counts = [fronts.count(c) for c in chars]
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


@app.cell
def _(util):
    _instance = util.parse("nucleotide_n010k010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("nucleotide_n050k050.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("protein_n010k010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _(util):
    _instance = util.parse("protein_n050k050.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


if __name__ == "__main__":
    app.run()
