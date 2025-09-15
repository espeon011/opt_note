# DIDP を用いたモデル

考案者の解説記事: [動的計画法ベースの数理最適化ソルバDIDPPyで最短共通超配列問題を解く](https://zenn.dev/okaduki/articles/7f9a3f3c54bc98)

## Python Code

```python
from collections.abc import Callable
import didppy


type TypeBoundExprFunc = Callable[
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
    instance: list[str], dpmodel: didppy.Model, index_vars: list[didppy.ElementVar]
) -> didppy.IntExpr:
    exprs = []
    for idx1, (s1, index_var1) in enumerate(zip(instance, index_vars)):
        for idx2, (s2, index_var2) in enumerate(zip(instance, index_vars)):
            if idx2 >= idx1:
                continue
            table_idx1_idx2 = dpmodel.add_int_table(boundtable_scs2(s1, s2))
            exprs.append(table_idx1_idx2[index_var1, index_var2])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound


class Model:
    def __init__(
        self,
        instance: list[str],
        extra_bounds: list[TypeBoundExprFunc] | None = None,
        disable_default_bound: bool = False,
    ):
        chars = sorted(list(set("".join(instance))))

        dpmodel = didppy.Model(maximize=False, float_cost=False)

        index_types = [dpmodel.add_object_type(number=len(s) + 1) for s in instance]
        index_vars = [
            dpmodel.add_element_var(object_type=index_type, target=0)
            for index_type in index_types
        ]

        instance_table = dpmodel.add_element_table(
            [[chars.index(c) for c in s] + [len(chars)] for s in instance]
        )

        dpmodel.add_base_case(
            [index_var == len(s) for s, index_var in zip(instance, index_vars)]
        )

        # 文字 char に従って進む
        for id_char, char in enumerate(chars):
            condition = didppy.Condition(False)
            for sidx, index_var in enumerate(index_vars):
                condition |= instance_table[sidx, index_var] == id_char
            trans = didppy.Transition(
                name=f"{char}",
                cost=1 + didppy.IntExpr.state_cost(),
                effects=[
                    (
                        index_var,
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
            dpmodel.add_dual_bound(boundexpr_scs2len(instance, dpmodel, index_vars))

        # 追加の Dual Bound があれば.
        if extra_bounds:
            for bound_func in extra_bounds:
                dpmodel.add_dual_bound(bound_func(instance, dpmodel, index_vars))

        self.instance = instance
        self.dpmodel = dpmodel
        self.dpsolver = None
        self.solution = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.dpsolver = didppy.CABS(
            self.dpmodel, threads=12, time_limit=time_limit, quiet=(not log)
        )
        self.solution = self.dpsolver.search()
        return self

    def to_solution(self) -> str:
        return "".join([trans.name for trans in self.solution.transitions])


def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str:
    model = Model(instance)
    model.solve(time_limit, log)
    return model.to_solution()
```
