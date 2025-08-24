# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    import random
    import string
    import util


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# データ生成用""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 一様ランダム文字列""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    与えられた文字列集合の中から一様ランダムに文字を抽出して並べることで文字列を生成する. 

    - $q$: 使用文字種類数. 
    - $n$: 文字列数. 
    - $k_{\min}, k_{\max}$: 文字列超上下限. 実際の文字列超はこの範囲から一様ランダムに決める.
    """
    )
    return


@app.function
def gen_uniform_instance(
    q: int,
    n: int,
    k_min: int,
    k_max: int,
    seed: int = 0,
) -> None:
    assert q >= 1 and q <= 94
    assert n >= 1
    assert k_min >= 1 and k_max >=1
    assert k_min <= k_max

    characters = string.ascii_letters + string.digits + string.punctuation
    random.seed(seed)

    instance: list[str] = []
    for i in range(n):
        k = random.randint(k_min, k_max)
        s = "".join(random.choices(characters[:q], k=k))
        instance.append(s)

    return instance


@app.function
def write_uniform_instance(
    q: int,
    n: int,
    k_min: int,
    k_max: int,
    seed: int = 0,
) -> None:
    instance = gen_uniform_instance(q, n, k_min, k_max, seed)
    filename = f"uniform_q{q:0>2}n{n:0>3}k{k_min:0>3}-{k_max:0>3}.txt"
    util.save(instance, filename)


@app.cell
def _():
    write_uniform_instance(q=26, n=2, k_min=15, k_max=25)
    write_uniform_instance(q=26, n=4, k_min=15, k_max=25)
    write_uniform_instance(q=26, n=8, k_min=15, k_max=25)
    write_uniform_instance(q=26, n=16, k_min=15, k_max=25)
    write_uniform_instance(q=26, n=32, k_min=15, k_max=25)
    write_uniform_instance(q=26, n=64, k_min=15, k_max=25)

    write_uniform_instance(q=5, n=10, k_min=10, k_max=10)
    write_uniform_instance(q=5, n=50, k_min=10, k_max=10)
    write_uniform_instance(q=5, n=100, k_min=10, k_max=10)
    write_uniform_instance(q=5, n=500, k_min=10, k_max=10)

    write_uniform_instance(q=5, n=10, k_min=20, k_max=20)
    write_uniform_instance(q=5, n=50, k_min=20, k_max=20)
    write_uniform_instance(q=5, n=100, k_min=20, k_max=20)
    write_uniform_instance(q=5, n=500, k_min=20, k_max=20)
    return


if __name__ == "__main__":
    app.run()
