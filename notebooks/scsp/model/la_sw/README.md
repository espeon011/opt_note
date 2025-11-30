# Look-Ahead Sum-Weight

## 概要

LA-SH と WMM を組み合わせたもの. 

- 計算量: $O(n^2 k q^{m+1} / l)$. 多分...
- 近似精度: ?

LA-SH では $m$ 手進めたときに最も良い選択の前から $l$ 文字を採用するプロセスを繰り返す. 
しかし $m$ が小さい状況では近視眼的になってしまう.
MM に対して WMM が有効であったように残りの長さが長ければ長いほど優先度を高くすることで効率化を図る. 

### 記法

文字列 $s_i$ の $j$ 文字目の重みを $w_{ij} = |s_i| - j + 1$ とする. 

### 手続

整数パラメータ $m, l \ (l \leq m)$ を与えたうえで下記のようにする.
この手法を $(m, l)$-LA-SW と書く.

- 解 $\mathrm{sol}$ を空文字列で初期化する.
- 下記を $m$ 回繰り返すことで削除できた文字に対する重みの和 (Sum-Weight) が最大になる文字の取り方を探索する.
    - 各文字列 $s_1, \dots, s_n$ の先頭の文字の中から 1 つ選び, 選んだ文字を文字列たちの先頭から削除する.
- 上記の取り方に対して先頭の $l$ 文字を $sol$ の後ろに加え, 各文字列 $s_1, \dots, s_n$ の先頭から順に削除する.
- $s_1, \dots, s_n$ が全て空文字列になれば終了.

$m = l = 1$ としたとき, つまり $(1, 1)$-LA-SW は Weighted Majority Merge と同じ方法である.
LA-SH に倣ってデフォルトは $m = 3$, $l = 1$ とする.

## Python Code

```python
from dataclasses import dataclass


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
    weights = {
        char: sum(
            len(s) - idx
            for idx, s in zip(state, instance)
            if idx < len(s) and s[idx] == char
        )
        for char in chars
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
        if sum_ahead + weights[char] > max_sum_weight:
            max_sum_weight = sum_ahead + weights[char]
            max_str_front = char + str_ahead
    return (max_str_front, max_sum_weight)


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
```
