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
    - 計算量: $O(k^2 \log_2 q + L^* (n \kappa \beta q + \beta q \log_2 \left( \beta q \right)))$
        - (補足) $L^*$: このアルゴリズムによって返される解の長さ. $O(nk)$ で上からバウンドできる. 
        - (補足) $\beta$, $\kappa$: ビームサーチのパラメータ. 
    - 近似精度: ?
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    `IBS_SCS` は基本的には残された文字列の先頭の文字の中から 1 つを採用して解を拡張していく手続きである. 
    1 つだけを選択して次の状態とする貪欲法と比較してビームサーチは以下のようにする: 

    - 状態は複数保持しておき, その状態たちから残された文字列の先頭に現れる文字の 1 つを選択して解を拡張する操作で得られる状態を全て集める.
    - 保持している状態に対して適切な評価を実施して評価が低いものを保持数が基準値を下回るよう切り捨てる.
    - 保持している状態の中に残された文字列が全て空になったものがあれば終了する. 

    この `IBS_SCS` アルゴリズムは以下の 4 ステップからなる. 

    1. 現在保持している状態から 1 手進めて得られる状態を集める. 
    2. 残された文字列の SCS 長の推定値を計算し, 各状態に対し評価用のヒューリスティック関数値を計算する.
    3. 今回のループで得られた状態の中で無駄な状態を削除する. (2 つの状態の間に支配という関係が定義される. 支配の関係にある 2 つの状態があったとき, うち片方はもう片方の完全劣化のため保持しない) 
    4. ヒューリスティック関数値を基準にビーム幅 $\beta$ 分の個数だけ状態を取り出して次のループへ.

    より具体的な内容は元論文か実装を参照. 
    ヒューリスティック関数値の計算には一様ランダムに生成された文字列に対する性質が用いられるため, 
    規則性のある文字列に対する SCS を計算する場合は性能が悪くなるかもしれない. 
    """
    )
    return


@app.function
def make_prob_table(num_chars: int, max_len: int) -> list[list[float]]:
    """
    以下の値が入っている 2 次元配列 p を返す: 
    p[q][k] = 一様ランダムに生成された長さ q の文字列 w と長さ k の文字列 y に対して, w が y の subsequence になる確率
    """

    nrow = max_len + 1
    ncol = math.ceil(max_len * math.log2(num_chars)) + 1

    ret = [[0.0 for k in range(ncol)] for q in range(nrow)]
    for q in range(nrow):
        for k in range(ncol):
            if q == 0:
                ret[q][k] = 1.0
            elif q > k:
                ret[q][k] = 0.0
            else:
                tmp1 = 1.0 / num_chars * ret[q-1][k-1]
                tmp2 = (num_chars - 1) / num_chars * ret[q][k-1]
                ret[q][k] = tmp1 + tmp2

    return ret


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

    def use(self, char: str) -> "State":
        new_state = copy.deepcopy(self)
        new_state.solution += char
        for idx, (s, pos) in enumerate(zip(self.instance, new_state.positions)):
            if pos < len(s) and s[pos] == char:
                new_state.positions[idx] += 1
        return new_state

    def dominate(self, other: "State") -> bool:
        geq = all(pos1 >= pos2 for pos1, pos2 in zip(self.positions, other.positions))
        neq = any(pos1 != pos2 for pos1, pos2 in zip(self.positions, other.positions))
        return geq and neq

    def heuristic(self, prob_table: list[list[float]], k: int) -> float:
        ret = 1.0
        for s, pos in zip(self.instance, self.positions):
            ret *= prob_table[len(s) - pos][k]
        return ret


@app.function
def solve(instance: list[str], beta: int = 100, kappa: int = 7) -> str:
    chars = sorted(list(set("".join(instance))))
    prob_table = make_prob_table(len(chars), max(len(s) for s in instance))
    states: list[State] = [State(instance)]

    while True:
        # Step 1: Extension
        new_states: list[State] = []
        for state in states:
            for char in chars:
                if state.is_usable(char):
                    new_state = state.use(char)
                    if new_state.is_feasible():
                        return new_state.solution
                    else:
                        new_states.append(new_state)

        # Step 2: Evaluation of candidate solutions
        k = math.ceil(
            math.log2(len(chars))
            * max(
                len(s) - pos
                for state in new_states
                for s, pos in zip(instance, state.positions)
            )
        )
        # k は残りの部分の SCS 長さの推定値を表している. 
        # k をどのような値にセットするのがよいのかは Open Problem とされている. 

        # 元論文ではこの辺りに評価用ヒューリスティック関数値の計算があった. 

        # Step 3: Dominance pruning
        new_states.sort(
            key=lambda state: state.heuristic(prob_table, k), reverse=True
        )
        kappa_best_list = new_states[:kappa]
        new_states = [
            new_state
            for new_state in new_states
            if all(not better.dominate(new_state) for better in kappa_best_list)
        ]

        # Step 4: Selection
        states = new_states[:beta]


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
