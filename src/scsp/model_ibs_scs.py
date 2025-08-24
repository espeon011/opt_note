# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    import copy
    import math
    import functools


@app.cell
def _():
    import marimo as mo
    import nbformat
    import util
    return mo, util


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# `IBS_SCS` アルゴリズム""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    参考: Sayyed Rasoul Mousavi, Fateme Bahri, Farzaneh Sadat Tabataba, 2012, An enhanced beam search algorithm for the Shortest Common Supersequence Problem,
    Engineering Applications of Artificial Intelligence,
    Volume 25, Issue 3, Pages 457-467, https://www.sciencedirect.com/science/article/pii/S0952197611001497
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - 計算量: $O(k^2 \log_2 q + L^* (n \kappa \beta q + \beta q \log_2 \left( \beta q \right)))$
        - (補足) $L^*$: このアルゴリズムによって返される解の長さ. $O(nk)$
        - (補足) $\kappa$, $\beta$: ビームサーチのパラメータ. 
    - 近似精度: ?
    """
    )
    return


@app.function
@functools.cache
def probability(len_sub: int, len_super: int, num_alphabet: int) -> float:
    """
    一様ランダムに生成された文字列 w (長さ len_sub) と y (長さ len_super) について, 
    y が w の supersequence である確率を返す. 
    """

    if len_sub == 0:
        return 1.0
    elif len_sub > len_super:
        return 0.0
    else:
        tmp1 = 1.0 / num_alphabet * probability(len_sub - 1, len_super - 1, num_alphabet)
        tmp2 = (num_alphabet - 1) / num_alphabet * probability(len_sub, len_super - 1, num_alphabet)

    return tmp1 + tmp2


@app.class_definition
class State:
    def __init__(self, instance: list[str]):
        self.instance = instance
        self.positions = [0 for _ in instance]
        self.solution = ""

    def is_feasible(self) -> bool:
        return all(pos == len(s) for s, pos in zip(self.instance, self.positions))

    def is_usable(self, c: str) -> bool:
        for pos, s in zip(self.positions, self.instance):
            if pos < len(s) and s[pos] == c:
                return True

        return False

    def dominate(self, other: "State") -> bool:
        geq = all(pos1 >= pos2 for pos1, pos2 in zip(self.positions, other.positions))
        neq = any(pos1 != pos2 for pos1, pos2 in zip(self.positions, other.positions))
        return geq and neq


@app.function
def solve(instance: list[str], beta: int = 100, kappa: int = 7) -> str:
    chars = sorted(list(set("".join(instance))))
    initial_state = State(instance)
    b: list[State] = [initial_state]

    while True:
        # Step 1: Extension
        c: list[State] = []
        for state in b:
            for char in chars:
                if not state.is_usable(char):
                    continue

                new_state = copy.deepcopy(state)
                new_state.solution += char
                for idx, (s, pos) in enumerate(zip(instance, new_state.positions)):
                    if pos < len(s) and s[pos] == char:
                        new_state.positions[idx] += 1

                if new_state.is_feasible():
                    return new_state.solution
                else:
                    c.append(new_state)

        # Step 2: Evaluation of candidate solutions
        k = round(
            math.log2(len(chars))
            * max(
                len(s) - pos
                for state in c
                for s, pos in zip(instance, state.positions)
            )
        )

        heuristics = []
        for state in c:
            tmp_h = 1.0
            for s, pos in zip(instance, state.positions):
                tmp_h *= probability(len(s) - pos, k, len(chars))
            heuristics.append(tmp_h)

        # Step 3: Dominance pruning
        sorted_c = [
            state for (idx, state) in sorted(
                list(enumerate(c)),
                key=lambda tmp: heuristics[tmp[0]],
                reverse=True,
            )
        ]
        kappa_best_list = sorted_c[:kappa]
        for idx in range(len(sorted_c) - 1, len(kappa_best_list) - 1, -1):
            if any(better.dominate(sorted_c[idx]) for better in kappa_best_list):
                sorted_c.pop(idx)

        # Step 4: Selection
        b = sorted_c[:beta]


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
