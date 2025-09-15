# 動的計画法[^1]

- 計算量: $O(k^n)$ らしいがこの実装では $O(k^n q n)$ かかる.
- 近似精度: $1$

**記法**

- 文字列 $s$ を $j$ 文字目までと $j+1$ 文字目以降に分けたうちの前半を $s[0..j]$ と書く.
- 文字列集合を $S = \lbrace s_1, \dots, s_n \rbrace$ とする.
- $t = (j_1, \dots, j_n) \ (i \in \lbrace 1, \dots, n \rbrace, \ j_i \in \lbrace 0, \dots, |s_i| \rbrace )$ を transversal と呼ぶ.
- $t = (j_1, \dots, j_n)$ に対して $S_t = \lbrace s_1[0..j_1], \dots, s_n[0..j_n] \rbrace$ と定める.
- $S_t$ に対する SCS の長さを $\lambda(t)$ と書く.
- $t = (j_1, \dots, j_n)$ に対し, $I = \lbrace 1, \dots, n \rbrace$ 上の同値関係として $S_t$ 内の文字列 $s_{i_1}$ と $s_{i_2}$ の最後の文字が等しいときかつその時に限り $i_1 \sim i_2$ とするものを考え, その商集合を $E_t$ と書く.
- 上記同値関係の同値類 $K \in E_t$ は特定の文字と対応する. それを $\beta_K$ と書く.
- $K \in E_t$ に対し, $S_t$ において最後の文字が $\beta_k$ である文字のインデックス $i$ に対して $j_i$ を $j_i - 1$ で更新した transversal を $t_K$ と書く.

**遷移**

- 最終的に求めたい SCS 長は right transversal $T = (|s_1|, \dots, |s_n|)$ に対する $\lambda(T)$.
- Base Case として left transversal $o = (0, \dots, 0)$ に対する $\lambda(o) = 0$ がある.
- 次の漸化式が成り立つ: $\lambda(t) = \min \lbrace \lambda(t_K) \ | \ K \in E_t \rbrace + 1$. ただし $t \ne o$.

[^1]: Timkovskii, V.G. Complexity of common subsequence and supersequence problems and related problems. Cybern Syst Anal 25, 565–580 (1989). https://doi.org/10.1007/BF01075212

## Python Code

```python
import itertools


def solve(instance: list[str]) -> str:
    dp: dict[tuple[int, ...], tuple[int, tuple[int, ...] | None]] = {
        (0,) * len(instance): (0, None)
    }
    for transversal in itertools.product(*[range(len(s) + 1) for s in instance]):
        if transversal in dp:
            continue

        end_chars = set(s[t - 1] for s, t in zip(instance, transversal) if t > 0)
        pretransversals = [
            tuple(
                t - 1 if t > 0 and s[t - 1] == c else t
                for s, t in zip(instance, transversal)
            )
            for c in end_chars
        ]

        min_transversal = pretransversals[0]
        min_length = dp[min_transversal][0]
        for pretransversal in pretransversals:
            if dp[pretransversal][0] < min_length:
                min_transversal = pretransversal
                min_length = dp[pretransversal][0]

        dp[transversal] = (min_length + 1, min_transversal)

    solution = ""
    left_transversal = (0,) * len(instance)
    right_transversal = tuple(len(s) for s in instance)
    current_transversal = right_transversal
    while current_transversal != left_transversal:
        pretransversal = dp[current_transversal][1]
        assert pretransversal is not None
        c = None
        for s, t1, t2 in zip(instance, current_transversal, pretransversal):
            if t1 == t2 + 1:
                c = s[t2]
                break
        assert c is not None
        solution += c
        current_transversal = pretransversal

    return solution[::-1]
```
