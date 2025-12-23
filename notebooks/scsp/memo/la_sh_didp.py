# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
#     "opt-note",
# ]
#
# [tool.uv.sources]
# opt-note = { git = "https://github.com/espeon011/opt_note" }
# ///

import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    from dataclasses import dataclass
    import opt_note.scsp as scsp
    import datetime
    import didppy


@app.cell
def _():
    import marimo as mo
    import nbformat

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # `LA_SH` アルゴリズムのサブルーチンを DIDP で置き換えてみる
    """)
    return


@app.function
def find_next_strategy(
    instance: list[str],
    chars: str,
    m: int,
) -> str:
    """
    現在の状態を受け取り, m 手進めたときに sum height が最大になる文字の選び方 (長さ m 以下の文字列として表される) を返す
    """

    dpmodel = didppy.Model(maximize=True, float_cost=False)

    instance_table = dpmodel.add_element_table(
        [[chars.index(c) for c in s] + [len(chars)] for s in instance]
    )

    index_types = [dpmodel.add_object_type(number=len(s) + 1) for s in instance]
    index_vars = [
        dpmodel.add_element_var(object_type=index_type, target=0)
        for index_type in index_types
    ]
    sol_len = dpmodel.add_int_var(target=0)

    dpmodel.add_base_case([sol_len == m])

    # 文字 char に従って進む
    for id_char, char in enumerate(chars):
        sum_height = sum(
            (instance_table[sidx, index_var] == id_char).if_then_else(1, 0)
            for sidx, index_var in enumerate(index_vars)
        )
        trans = didppy.Transition(
            name=f"{char}",
            cost=sum_height + didppy.IntExpr.state_cost(),
            effects=[
                (
                    index_var,
                    (instance_table[sidx, index_var] == id_char).if_then_else(
                        index_var + 1, index_var
                    ),
                )
                for sidx, index_var in enumerate(index_vars)
            ]
            + [(sol_len, sol_len + 1)],
            preconditions=[sum_height > 0],
        )
        dpmodel.add_transition(trans)

    # Force transition
    end = didppy.Transition(
        name="",
        cost=didppy.IntExpr.state_cost(),
        effects=[(sol_len, m)],
        preconditions=[
            index_var == len(s) for s, index_var in zip(instance, index_vars)
        ],
    )
    dpmodel.add_transition(end, forced=True)

    # Dual bound
    dual_bound_table = dpmodel.add_int_table(
        [[min(m, len(s) - idx) for idx in range(len(s) + 1)] for s in instance]
    )
    bound = didppy.IntExpr(0)
    for sidx, index_var in enumerate(index_vars):
        bound += dual_bound_table[sidx, index_var]
    dpmodel.add_dual_bound(bound)

    dpsolver = didppy.CABS(dpmodel, threads=8, quiet=True)
    solution = dpsolver.search()

    return "".join([trans.name for trans in solution.transitions])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 計算時間の比較
    """)
    return


@app.class_definition
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, m: int = 3, ll: int = 1, *args, **kwargs) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        state = tuple(0 for _ in self.instance)
        solution = ""

        count = 0
        while not all(idx == len(s) for idx, s in zip(state, self.instance)):
            next_str = find_next_strategy(
                [s[idx:] for idx, s in zip(state, self.instance)], chars, m
            )
            if len(next_str) == 0:
                break
            count += 1
            # print(f"{count=}, {next_str=}")
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
    scsp.util.bench(
        scsp.model.la_sh.Model, example_filename="uniform_q26n004k015-025.txt"
    )
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.la_sh.Model, example_filename="uniform_q26n008k015-025.txt"
    )
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.la_sh.Model, example_filename="uniform_q26n016k015-025.txt"
    )
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.la_sh.Model, example_filename="uniform_q05n010k010-010.txt"
    )
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.la_sh.Model, example_filename="uniform_q05n050k010-010.txt"
    )
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="protein_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="protein_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(scsp.model.la_sh.Model, example_filename="protein_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="protein_n050k050.txt")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    DIDP を使うと時間が長くなる.
    小さな問題であれば直接プログラミングした方がよい.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 先読みの手数を増やせないか
    """)
    return


@app.class_definition
@dataclass
class Model2:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, m: int = 5, ll: int = 1, *args, **kwargs) -> str | None:
        model = Model(self.instance)
        self.solution = model.solve(m=m, ll=ll)
        self.best_bound = model.best_bound
        return self.solution


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="uniform_q05n010k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="uniform_q05n050k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model2, example_filename="protein_n010k010.txt")
    return


@app.cell
def _():
    # 5 分以内に計算が終わらなかったのでスキップ

    # scsp.util.bench(Model2, example_filename="protein_n050k050.txt")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    改善はしたが, 計算時間の増加に見合うほどではなかった.
    """)
    return


if __name__ == "__main__":
    app.run()
