# IBS_SCS アルゴリズム

## 概要

- 計算量: $O(k^2 \log_2 q + L^* (n \kappa \beta q + \beta q \log_2 \left( \beta q \right)))$
    - (補足) $L^*$: このアルゴリズムによって返される解の長さ. $O(nk)$ で上からバウンドできる.
    - (補足) $\beta$, $\kappa$: ビームサーチのパラメータ.
- 近似精度: ?

IBS_SCS は基本的には残された文字列の先頭の文字の中から 1 つを採用して解を拡張していく手続きである.
1 つだけを選択して次の状態とする貪欲法と比較してビームサーチは以下のようにする:

- 状態は複数保持しておき, その状態たちから残された文字列の先頭に現れる文字の 1 つを選択して解を拡張する操作で得られる状態を全て集める.
- 保持している状態に対して適切な評価を実施して評価が低いものを保持数が基準値を下回るよう切り捨てる.
- 保持している状態の中に残された文字列が全て空になったものがあれば終了する.

この IBS_SCS アルゴリズムは以下の 4 ステップからなる.

1. 現在保持している状態から 1 手進めて得られる状態を集める.
2. 残された文字列の SCS 長の推定値を計算し, 各状態に対し評価用のヒューリスティック関数値を計算する.
3. 今回のループで得られた状態の中で無駄な状態を削除する. (2 つの状態の間に支配という関係が定義される. 支配の関係にある 2 つの状態があったとき, うち片方はもう片方の完全劣化のため保持しない)
4. ヒューリスティック関数値を基準にビーム幅 $\beta$ 分の個数だけ状態を取り出して次のループへ.

より具体的な内容は元論文か実装を参照.
ヒューリスティック関数値の計算には一様ランダムに生成された文字列に対する性質が用いられるため,
規則性のある文字列に対する SCS を計算する場合は性能が悪くなるかもしれない.

## 参考

1. Sayyed Rasoul Mousavi, Fateme Bahri, Farzaneh Sadat Tabataba, An enhanced beam search algorithm for the Shortest Common Supersequence Problem, Engineering Applications of Artificial Intelligence, Volume 25, Issue 3, 2012, Pages 457-467, ISSN 0952-1976, https://doi.org/10.1016/j.engappai.2011.08.006.

## Python Code

```python
import math
import copy
from dataclasses import dataclass


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


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, beta: int = 100, kappa: int = 7, *args, **kwargs) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        prob_table = make_prob_table(len(chars), max(len(s) for s in self.instance))
        states: list[State] = [State(self.instance)]

        while True:
            # Step 1: Extension
            new_states: list[State] = []
            for state in states:
                for char in chars:
                    if state.is_usable(char):
                        new_state = state.use(char)
                        if new_state.is_feasible():
                            self.solution = new_state.solution
                            return self.solution
                        else:
                            new_states.append(new_state)

            # Step 2: Evaluation of candidate solutions
            k = math.ceil(
                math.log2(len(chars))
                * max(
                    len(s) - pos
                    for state in new_states
                    for s, pos in zip(self.instance, state.positions)
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
```
