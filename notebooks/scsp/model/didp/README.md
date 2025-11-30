# DIDP を用いたモデル

## 概要

DIDP を用いて DP モデルを強化する.
Dual bound には 2 文字の文字列の最短共通超配列の長さを全ての組合せに対して取ったものの最大値を採用する. 

## 参考

1. 考案者の解説記事: [動的計画法ベースの数理最適化ソルバDIDPPyで最短共通超配列問題を解く](https://zenn.dev/okaduki/articles/7f9a3f3c54bc98)

## Python Code

```python
from dataclasses import dataclass
from collections.abc import Callable
import didppy


type TypeBoundExprFunc = Callable[
    # pyrefly: ignore
    [list[str], didppy.Model, list[didppy.ElementVar]], didppy.IntExpr
]


def boundtable_scs2(s1: str, s2: str) -> list[list[int]]:
    len1, len2 = len(s1), len(s2)

    dp = [[len1 + len2 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i1 in range(len1 + 1):
        dp[i1][len2] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2] = len2 - i2

    for i1 in range(len1 - 1, -1, -1):
        for i2 in range(len2 - 1, -1, -1):
            if s1[i1] == s2[i2]:
                dp[i1][i2] = dp[i1 + 1][i2 + 1] + 1
            else:
                dp[i1][i2] = min(dp[i1 + 1][i2], dp[i1][i2 + 1]) + 1

    return dp


def boundexpr_scs2len(
    instance: list[str],
    dpmodel: didppy.Model,  # pyrefly: ignore
    index_vars: list[didppy.ElementVar],  # pyrefly: ignore
) -> didppy.IntExpr:  # pyrefly: ignore
    exprs = []
    for idx1, (s1, index_var1) in enumerate(zip(instance, index_vars)):
        for idx2, (s2, index_var2) in enumerate(zip(instance, index_vars)):
            if idx2 >= idx1:
                continue
            table_idx1_idx2 = dpmodel.add_int_table(boundtable_scs2(s1, s2))
            exprs.append(table_idx1_idx2[index_var1, index_var2])

    bound = didppy.IntExpr(0)  # pyrefly: ignore
    for expr in exprs:
        bound = didppy.max(bound, expr)  # pyrefly: ignore

    return bound


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        extra_bounds: list[TypeBoundExprFunc] | None = None,
        disable_default_bound: bool = False,
        *args,
        **kwargs,
    ) -> str | None:
        chars = sorted(list(set("".join(self.instance))))

        # pyrefly: ignore
        dpmodel = didppy.Model(maximize=False, float_cost=False)

        index_types = [
            dpmodel.add_object_type(number=len(s) + 1) for s in self.instance
        ]
        index_vars = [
            dpmodel.add_element_var(object_type=index_type, target=0)
            for index_type in index_types
        ]

        instance_table = dpmodel.add_element_table(
            [[chars.index(c) for c in s] + [len(chars)] for s in self.instance]
        )

        dpmodel.add_base_case(
            [index_var == len(s) for s, index_var in zip(self.instance, index_vars)]
        )

        # 文字 char に従って進む
        for id_char, char in enumerate(chars):
            condition = didppy.Condition(False)  # pyrefly: ignore
            for sidx, index_var in enumerate(index_vars):
                condition |= instance_table[sidx, index_var] == id_char
            trans = didppy.Transition(  # pyrefly: ignore
                name=f"{char}",
                cost=1 + didppy.IntExpr.state_cost(),  # pyrefly: ignore
                effects=[
                    (
                        index_var,
                        # pyrefly: ignore
                        (instance_table[sidx, index_var] == id_char).if_then_else(
                            index_var + 1, index_var
                        ),
                    )
                    for sidx, index_var in enumerate(index_vars)
                ],
                preconditions=[condition],
            )
            dpmodel.add_transition(trans)

        # 残っている文字列から 2 つを選んで SCS を取って長さが最大のものを Dual Bound とする.
        if not disable_default_bound:
            dpmodel.add_dual_bound(
                boundexpr_scs2len(self.instance, dpmodel, index_vars)
            )

        # 追加の Dual Bound があれば.
        if extra_bounds:
            for bound_func in extra_bounds:
                dpmodel.add_dual_bound(bound_func(self.instance, dpmodel, index_vars))

        dpsolver = didppy.CABS(  # pyrefly: ignore
            dpmodel, threads=12, time_limit=time_limit, quiet=(not log)
        )
        didpsolution = dpsolver.search()

        if not didpsolution.is_infeasible and len(didpsolution.transitions) > 0:
            self.solution = "".join([trans.name for trans in didpsolution.transitions])
        else:
            self.solution = None

        if didpsolution.best_bound is not None:
            self.best_bound = float(didpsolution.best_bound)
        else:
            self.best_bound = 0.0

        return self.solution
```
