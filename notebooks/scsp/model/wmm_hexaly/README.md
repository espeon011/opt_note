# Weighted Majority Merge をパラメータ化し, Hexaly で探索

## 概要

Hexaly の外部関数最適化機能を用いた定式化を紹介する.
Weighted Majority Merge アルゴリズムにおいて次の文字を選択する基準は各文字列に対する残長の和であった.
その残長の部分を Hexaly の決定変数で置き換える.

### 決定変数

- $w_{ij} \in \mathbb{N}$: 文字列 $s_i$ の $j$ 文字目の重み. $(i \in \lbrace 1, \dots, n \rbrace, \ j \in \lbrace 1, \dots, |s_i| \rbrace)$
    - $w_i = \lbrace w_{i,1} \dots, w_{i,|s_i|} \rbrace$ とおく.

### 目的関数

下記のアルゴリズムに従って構築した共通超配列の長さを目的関数とする.

- 解 $\mathrm{sol}$ を空文字列で初期化する.
- 各文字 $c$ に対して重み $\sum_{i=1, \ s_i[0] = c}^n w_{i,1}$ を計算し, 重みが最大である $c$ を求める.
- $\mathrm{sol}$ の後ろに $c$ を追加する.
- 各文字列 $s_i \ (i \in \lbrace 1, \dots, n \rbrace)$ に対し, 先頭の文字が $c$ である場合は
    - $s_i$ の先頭の文字を削除する.
    - $w_i$ の先頭の重みを削除し, インデックスを前に詰める.
- $s_1, \dots, s_n$ 全てが空文字列になれば終了. $\mathrm{sol}$ が解.

## Python Code

```python
from dataclasses import dataclass
from functools import cached_property
import hexaly.optimizer


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    @cached_property
    def chars(self) -> str:
        return "".join(sorted(list(set("".join(self.instance)))))

    @cached_property
    def indices_1d_to_2d(self) -> list[tuple[int, int]]:
        ans: list[tuple[int, int]] = []
        counter = 0
        for s in self.instance:
            ans.append((counter, counter + len(s)))
            counter += len(s)
        return ans

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [priorities1d[start:end] for start, end in self.indices_1d_to_2d]

    def wmm(self, priorities2d: list[list[int]]) -> str:
        max_len = len(self.instance) * max(len(s) for s in self.instance)
        indices = tuple(0 for _ in self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(max_len):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                sum(
                    priorities2d[sidx][idx]
                    for sidx, (idx, s) in enumerate(zip(indices, self.instance))
                    if idx < len(s) and s[idx] == c
                )
                for c in self.chars
            ]
            next_char = self.chars[counts.index(max(counts))]

            solution += next_char
            indices = tuple(
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(indices, self.instance)
            )

        return solution

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d[i] for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        initial_weights: list[list[int]] | None = None,
        *args,
        **kwargs,
    ) -> str | None:
        with hexaly.optimizer.HexalyOptimizer() as hxoptimizer:
            assert isinstance(hxoptimizer.model, hexaly.optimizer.HxModel)
            assert isinstance(hxoptimizer.param, hexaly.optimizer.HxParam)
            hxmodel: hexaly.optimizer.HxModel = hxoptimizer.model
            hxparam: hexaly.optimizer.HxParam = hxoptimizer.param

            chars = "".join(sorted(list(set("".join(self.instance)))))

            # 重みの最大値は初期重みが与えられた場合は初期重みの最大値の 2 倍,
            # 初期重みが与えられなかった場合は文字種数とする.
            max_weight = (
                max(
                    max(w, len(s))
                    for s, ws in zip(self.instance, initial_weights)
                    for w in ws
                )
                if initial_weights
                else len(chars)
            )

            priorities1d = [
                hxmodel.int(1, max_weight)
                for s in self.instance
                for cidx, _ in enumerate(s)
            ]

            func = hxmodel.create_int_external_function(self.objective)
            func.external_context.lower_bound = 0
            func.external_context.upper_bound = sum(len(s) for s in self.instance)

            hxmodel.minimize(func(*priorities1d))
            hxmodel.close()

            if initial_weights is not None:
                priorities2d = self.priorities_1d_to_2d(priorities1d)
                for ps, ws in zip(priorities2d, initial_weights):
                    for p, w in zip(ps, ws):
                        p.set_value(w)

            if time_limit is not None:
                hxparam.time_limit = time_limit
            hxparam.verbosity = 1 if log else 0
            hxoptimizer.solve()

            assert isinstance(hxoptimizer.solution, hexaly.optimizer.HxSolution)
            solution: hexaly.optimizer.HxSolution = hxoptimizer.solution
            assert isinstance(solution.status, hexaly.optimizer.HxSolutionStatus)
            status = solution.status
            if status in {
                hexaly.optimizer.HxSolutionStatus.OPTIMAL,
                hexaly.optimizer.HxSolutionStatus.FEASIBLE,
            }:
                priorities1d_value: list[int] = [p.value for p in priorities1d]
                priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
                self.solution = self.wmm(priorities2d_value)

            return self.solution
```
