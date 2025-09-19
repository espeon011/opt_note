# 長い方から 2 つの SCS を順次求めていく方法

- 計算量: $O(nk^2)$
- 近似精度: ?

2 つの文字列の shortest common supersequence は動的計画法で計算することができる.
ここでは与えられた文字列を長さが長い順にソートし,
最初の 2 つを shortest common supersequence で置き換える操作を文字列が 1 つになるまで繰り返す.

文字列の集合 $S = \lbrace s_1, s_2, \dots, s_n \rbrace$ はソート済みで $|s_1| \geq |s_2| \geq \dots \geq |s_n|$ を満たしているとする.

- $n_0 = n$ とする.
- $l$ ステップ目において文字列集合が $\lbrace s_1, s_2, \dots, s_{n_l} \rbrace$ であるとする.
- $s_1$ と $s_2$ の shortest common supersequence を求め, $s_1$ をそれで置き換える.
  $s_2$ は削除し, $s_3$ 以降は番号を前に 1 つずらして更新し, $\lbrace s_1, s_2, \dots, s_{n_l - 1}\rbrace$ とする.
- 文字列集合が 1 元集合 $\lbrace s_1 \rbrace$ になったら終了.

この方法が common supersequence を与えるのは $s'$ が $s$ の supersequence であるという 2 項関係 $s \preceq s'$ が推移的 (さらにいえば半順序) であることからいえる.
一方でこの順序関係によって順序集合となった文字配列全体の集合には圏論的な余積 (最小上界) は存在しない.
したがって 2 つずつ shortest common supersequence を取るこの方法では基本的には最適解は得られない.

## Python Code

```python
def scs2(s1: str, s2: str) -> str:
    """
    2 つの文字列の shortest common supersequence の 1 つを返す.

    Args:
        s1(str): 文字列 1
        s2(str): 文字列 2
    """

    len1, len2 = len(s1), len(s2)

    dp = [["" for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for idx1 in range(len1 + 1):
        for idx2 in range(len2 + 1):
            if idx1 == 0:
                dp[idx1][idx2] = s2[:idx2]
            elif idx2 == 0:
                dp[idx1][idx2] = s1[:idx1]
            elif s1[idx1 - 1] == s2[idx2 - 1]:
                dp[idx1][idx2] = dp[idx1 - 1][idx2 - 1] + s1[idx1 - 1]
            else:
                if len(dp[idx1 - 1][idx2]) <= len(dp[idx1][idx2 - 2]):
                    dp[idx1][idx2] = dp[idx1 - 1][idx2] + s1[idx1 - 1]
                else:
                    dp[idx1][idx2] = dp[idx1][idx2 - 1] + s2[idx2 - 1]

    return dp[-1][-1]


def solve(instance: list[str]) -> str:
    instance_sorted = sorted(instance, key=lambda s: len(s), reverse=True)

    solution = instance_sorted[0]
    for s in instance_sorted[1:]:
        solution = scs2(solution, s)

    return solution
```
