# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")

with app.setup:
    import util
    import copy


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Look-Ahead Sum-Height アルゴリズム""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - 計算量: この実装では $O(n^2 k q m)$. 多分...
    - 近似精度: なし
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Sum-Height アルゴリズムという手法がある. 
    これは Majority Merge と完全に同じものだが, 
    この Sum-Height 法に「数手先まで見て最も良い選択をする」という拡張を加える. 

    このアルゴリズムは整数パラメータ $m, l \ (l \leq m)$ を与えたうえで下記のようにする. 
    この手法を $(m, l)$-LA-SH と書く. 

    - 解 $\mathrm{sol}$ を空文字列で初期化する. 
    - 下記を $m$ 回繰り返すことで文字列たちの先頭の文字を削除できた数 (Sum-Height) が最大になる文字の取り方を探索する.
        - 各文字列 $s_1, \dots, s_n$ の先頭の文字の中から 1 つ選び, 選んだ文字を文字列たちの先頭から削除する. 
    - Sum-Height が最大になる文字の取り方に対して先頭の $l$ 文字を解の後ろに加え, 各文字列 $s_1, \dots, s_n$ の先頭から削除する. 
    - $s_1, \dots, s_n$ が全て空文字列になれば終了. 

    $l = m = 1$ としたとき, つまり $(1, 1)$-LA-SH は Majority Merge と同じ方法である. 
    元論文では $(3, 1)$-LA-SH がちょうど良いとされていたのでデフォルトは $l = 1$, $m = 3$ とする. 
    """
    )
    return


@app.function
def find_next_strategy(
    instance: list[str],
    chars: str,
    state: list[int],
    m: int,
) -> (str, int):
    """
    現在の状態を受け取り, m 手進めたときに sum height が最大になる文字の選び方 (長さ m の文字列として表される) と sum-height の値を組みにして返す
    """

    if m == 0 or all(idx == len(s) for idx, s in zip(state, instance)):
        return ("", 0)

    fronts = [s[idx] for idx, s in zip(state, instance) if idx < len(s)]
    counts = {char: fronts.count(char) for char in chars}
    max_sum_height = 0
    max_str_front: str | None = None
    explores = set()
    for char in chars:
        if char not in fronts or char in explores:
            continue
        explores.add(char)
        ahead_state = [
            idx + 1 if idx < len(s) and s[idx] == char else idx
            for idx, s in zip(state, instance)
        ]
        str_ahead, sum_ahead = find_next_strategy(instance, chars, ahead_state, m - 1)
        if sum_ahead + counts[char] > max_sum_height:
            max_sum_height = sum_ahead + counts[char]
            max_str_front = char + str_ahead
    return (max_str_front, max_sum_height)


@app.function
def solve(instance: list[str], m: int = 3, l: int = 1) -> str:
    chars = sorted(list(set("".join(instance))))
    state = [0] * len(instance)
    solution = ""

    while not all(idx == len(s) for idx, s in zip(state, instance)):
        next_str, _ = find_next_strategy(instance, chars, state, m)
        solution += next_str[:l]
        for next_char in next_str[:l]:
            for jdx, (idx, s) in enumerate(zip(state, instance)):
                if idx < len(s) and s[idx] == next_char:
                    state[jdx] += 1

    return solution


@app.cell
def _():
    _instance = util.parse("uniform_q26n004k015-025.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("uniform_q26n008k015-025.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("uniform_q26n016k015-025.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("uniform_q05n010k010-010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("uniform_q05n050k010-010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("nucleotide_n010k010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("nucleotide_n050k050.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("protein_n010k010.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


@app.cell
def _():
    _instance = util.parse("protein_n050k050.txt")
    util.show(_instance)
    _solution = solve(_instance)
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    return


if __name__ == "__main__":
    app.run()
