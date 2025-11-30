# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.12.0",
#     "hexaly>=14.0.20251112",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==6.0.0",
# ]
# [[tool.uv.index]]
# name ="hexaly"
# url = "https://pip.hexaly.com"
# explict = true
# [tool.uv.sources]
# hexaly = { index = "hexaly" }
# ///

import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    from dataclasses import dataclass
    import opt_note.scsp as scsp


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # LA-SH モデルと WMM を組み合わせる
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    LA-SH では $m$ 手進んだときに最も良い選択をするが,
    より先を見て判断するため, 進んだ手数の代わりに Weight の和を採用する.

    $m = 1$, $l = 1$ のときは WMM と同じである.
    """)
    return


@app.function
def find_next_strategy(
    instance: list[str],
    chars: str,
    state: tuple[int, ...],
    m: int,
) -> tuple[str, int]:
    """
    現在の状態を受け取り, m 手進めたときに weight の和が最大になる文字の選び方 (長さ m の文字列として表される) と sum-weight の値を組みにして返す
    """

    if m == 0 or all(idx == len(s) for idx, s in zip(state, instance)):
        return ("", 0)

    fronts = [s[idx] for idx, s in zip(state, instance) if idx < len(s)]
    counts = {char: fronts.count(char) for char in chars}
    weights = {
        char: sum(
            len(s) - idx for idx, s in zip(state, instance) if idx < len(s) and s[idx] == char
        ) for char in chars
    }
    max_sum_weight = 0
    max_str_front = ""
    explores = set()
    for char in chars:
        if char not in fronts or char in explores:
            continue
        explores.add(char)
        ahead_state = tuple(
            idx + 1 if idx < len(s) and s[idx] == char else idx
            for idx, s in zip(state, instance)
        )
        str_ahead, sum_ahead = find_next_strategy(instance, chars, ahead_state, m - 1)
        # if sum_ahead + counts[char] > max_sum_weight:
        #     max_sum_weight = sum_ahead + counts[char]
        #     max_str_front = char + str_ahead
        if sum_ahead + weights[char] > max_sum_weight:
            max_sum_weight = sum_ahead + weights[char]
            max_str_front = char + str_ahead
    return (max_str_front, max_sum_weight)


@app.class_definition
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, m: int = 3, ll: int = 1, *args, **kwargs) -> str:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        state = tuple(0 for _ in self.instance)
        solution = ""

        while not all(idx == len(s) for idx, s in zip(state, self.instance)):
            next_str, _ = find_next_strategy(self.instance, chars, state, m)
            solution += next_str[:ll]
            for next_char in next_str[:ll]:
                state = tuple(
                    idx + 1 if idx < len(s) and s[idx] == next_char else idx
                    for idx, s in zip(state, self.instance)
                )

        self.solution = solution
        return self.solution


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q05n010k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q05n050k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="protein_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="protein_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="protein_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="protein_n050k050.txt")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
