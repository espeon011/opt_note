"""
.. include:: ./README.md
"""

from dataclasses import dataclass


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


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, *args, **kwargs) -> str | None:
        instance_sorted = sorted(self.instance, key=lambda s: len(s), reverse=True)

        solution = instance_sorted[0]
        for s in instance_sorted[1:]:
            solution = scs2(solution, s)

        self.solution = solution
        return self.solution
