# Majority Merge アルゴリズム

## 概要

- 計算量: $O(qkn)$. この実装ではもっとかかる.
- 近似精度: なし

与えられた文字列たちの先頭を調べ, 最も出現頻度が高い文字を採用し,
文字列たちの先頭から削除する操作を全ての文字列が空になるまで繰り返す.

- 解 $\mathrm{sol}$ を空文字列で初期化する.
- 各文字列の先頭の文字 $s_1[0], s_2[0], \dots, s_n[0]$ を調べ, 最も多い文字を $c$ とする.
- $\mathrm{sol}$ の後ろに $c$ を追加する.
- 各文字列 $s_1, s_2, \dots, s_n$ に対し, 先頭の文字が $c$ である場合は先頭 1 文字を削除する.
- $s_1, s_2, \dots, s_n$ が全て空文字列になれば終了.

## 参考

1. Tao Jiang and Ming Li. 1995. On the Approximation of Shortest Common Supersequences and Longest Common Subsequences. SIAM J. Comput. 24, 5 (Oct. 1995), 1122–1139. https://doi.org/10.1137/S009753979223842X. 

## Python Code

```python
from dataclasses import dataclass


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, *args, **kwargs) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        indices = [0 for _ in self.instance]
        solution = ""

        while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
            fronts = [s[idx] for idx, s in zip(indices, self.instance) if idx < len(s)]
            counts = [fronts.count(c) for c in chars]
            next_char = chars[counts.index(max(counts))]

            solution += next_char
            for jdx in range(len(self.instance)):
                s = self.instance[jdx]
                idx = indices[jdx]
                if idx < len(s) and s[idx] == next_char:
                    indices[jdx] += 1

        self.solution = solution
        return self.solution
```
