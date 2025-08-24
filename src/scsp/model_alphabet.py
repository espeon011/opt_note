# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo
    import nbformat
    import util
    return mo, util


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# アルファベットアルゴリズム""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - 計算量: $O(qk)$
    - 近侍制度: $q$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    文字種全体を $\Sigma = \{ c_1, \dots, c_q \}$ とする. 
    与えられた文字列の中で最大の長さ $k$ に対して下記は与えられた文字列全ての supersequence になる: 

    $$
    (c_1 c_2 \dots c_q)^k
    $$

    これを解とすることで長さ $qk$ の common supersequence を出力する. 
    この長さは文字列の数に直接は依存しない. 

    各文字列 $s_i$ の $j$ 番目の文字は上記 $(c_1 c_2 \dots c_q)^k$ の中の $j$ 番目のブロックに必ず含まれているが, 
    $j$ 番目のブロックの中にはどの文字列でも使用しない文字があるかもしれない. 
    そのような文字は捨てることで解を少し改善する. 
    これによって解が少し改善するが, 文字列の数が増えると削れる文字が少なくなり, 長さ $qk$ に近づく.
    """
    )
    return


@app.function
def solve(instance: list[str]) -> str:
    chars = sorted(list(set("".join(instance))))
    solution = ""

    for i in range(max([len(s) for s in instance])):
        used = [False for _ in chars]
        for s in instance:
            if i >= len(s):
                continue
            used[chars.index(s[i])] = True

        for c, u in zip(chars, used):
            if u:
                solution += c

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
