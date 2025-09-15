"""
.. include:: ./README.md
"""

import math
import copy


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
                tmp1 = 1.0 / num_chars * ret[q - 1][k - 1]
                tmp2 = (num_chars - 1) / num_chars * ret[q][k - 1]
                ret[q][k] = tmp1 + tmp2

    return ret


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


def solve(instance: list[str], beta: int = 100, kappa: int = 7) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
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
        new_states.sort(key=lambda state: state.heuristic(prob_table, k), reverse=True)
        kappa_best_list = new_states[:kappa]
        new_states = [
            new_state
            for new_state in new_states
            if all(not better.dominate(new_state) for better in kappa_best_list)
        ]

        # Step 4: Selection
        states = new_states[:beta]
