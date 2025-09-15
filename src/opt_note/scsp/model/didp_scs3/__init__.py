"""
.. include:: ./README.md
"""

import didppy
from ..didp import Model


def boundtable_scs3(s1: str, s2: str, s3: str) -> list[list[list[int]]]:
    len1, len2, len3 = len(s1), len(s2), len(s3)

    # dp[i1][i2][i3]: s1[i1..] と s2[i2..] と s3[i3..] の SCS 長さ
    dp = [
        [[len1 + len2 + len3 + 1 for _ in range(len3 + 1)] for _ in range(len2 + 1)]
        for _ in range(len1 + 1)
    ]

    for i1 in range(len1 + 1):
        dp[i1][len2][len3] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2][len3] = len2 - i2
    for i3 in range(len3 + 1):
        dp[len1][len2][i3] = len3 - i3

    for i1 in range(len1, -1, -1):
        for i2 in range(len2, -1, -1):
            for i3 in range(len3, -1, -1):
                if [i1 == len1, i2 == len2, i3 == len3].count(True) >= 2:
                    continue

                front_chars = ""
                if i1 < len1:
                    front_chars += s1[i1]
                if i2 < len2:
                    front_chars += s2[i2]
                if i3 < len3:
                    front_chars += s3[i3]
                front_chars = set(front_chars)

                pretransversals = [
                    (
                        i1 + 1 if i1 < len1 and s1[i1] == c else i1,
                        i2 + 1 if i2 < len2 and s2[i2] == c else i2,
                        i3 + 1 if i3 < len3 and s3[i3] == c else i3,
                    )
                    for c in front_chars
                ]
                min_i1, min_i2, min_i3 = pretransversals[0]
                min_length = dp[min_i1][min_i2][min_i3]
                for pre_i1, pre_i2, pre_i3 in pretransversals:
                    if dp[pre_i1][pre_i2][pre_i3] < min_length:
                        min_i1 = pre_i1
                        min_i2 = pre_i2
                        min_i3 = pre_i3
                        min_length = dp[pre_i1][pre_i2][pre_i3]

                dp[i1][i2][i3] = min_length + 1

    return dp


def boundexpr_scs3len(
    instance: list[str], dpmodel: didppy.Model, index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    exprs = []
    for idx1 in range(len(instance)):
        for idx2 in range(idx1 + 1, len(instance)):
            for idx3 in range(idx2 + 1, len(instance)):
                s1 = instance[idx1]
                s2 = instance[idx2]
                s3 = instance[idx3]
                index_var1 = index_vars[idx1]
                index_var2 = index_vars[idx2]
                index_var3 = index_vars[idx3]
                table_s1s2s3 = dpmodel.add_int_table(boundtable_scs3(s1, s2, s3))
                exprs.append(table_s1s2s3[index_var1, index_var2, index_var3])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound


def create_model(instance: list[str]) -> Model:
    return Model(instance, extra_bounds=[boundexpr_scs3len], disable_default_bound=True)


def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    model = create_model(instance)
    model.solve(time_limit, log)
    return model.to_solution()
