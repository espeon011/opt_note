"""
.. include:: ./README.md
"""

from dataclasses import dataclass

import didppy

from ..didp import Model as ModelDidp
from ..didp import TypeBoundExprFunc


def boundtable_charcount(
    instance: list[str], chars: list[str]
) -> list[list[list[int]]]:
    """
    `table[idc][idx][i]` = `instance[idx][i:]` に含まれる `chars[idc]` の個数.

    添字 `i` の範囲は文字列によらず共通でなければならないため最大文字列長に合わせて 0 で埋める.
    """

    maxlen = max(len(s) for s in instance)

    table = []
    for char in chars:
        rows = []
        for s in instance:
            counts = [0] * (maxlen + 1)
            for i in range(len(s) - 1, -1, -1):
                counts[i] = counts[i + 1] + (1 if s[i] == char else 0)
            rows.append(counts)
        table.append(rows)

    return table


def make_boundexpr_charcount(max_strs_per_char: int | None) -> TypeBoundExprFunc:
    """
    文字ごとの残出現数による dual bound を作る関数を返す.

    Args:
        max_strs_per_char(int | None):
            1 文字あたり max を取る文字列の本数の上限.
            `None` の場合は全ての文字列を使う.
    """

    def boundexpr_charcount(
        instance: list[str],
        dpmodel: didppy.Model,  # pyrefly: ignore # ty:ignore
        index_vars: list[didppy.ElementVar],  # pyrefly: ignore # ty:ignore
    ) -> didppy.IntExpr:  # pyrefly: ignore # ty: ignore
        chars = sorted(set("".join(instance)))
        table = dpmodel.add_int_table(boundtable_charcount(instance, chars))

        bound = didppy.IntExpr(0)  # pyrefly: ignore # ty: ignore
        for idc, char in enumerate(chars):
            # 残出現数が最大になる文字列は元々 char を多く含む文字列である事が多いため,
            # 出現数の多い順に上位 max_strs_per_char 本だけを候補にして式を小さく保つ.
            candidates = [idx for idx, s in enumerate(instance) if char in s]
            candidates.sort(key=lambda idx: -instance[idx].count(char))
            if max_strs_per_char is not None:
                candidates = candidates[:max_strs_per_char]

            count = didppy.IntExpr(0)  # pyrefly: ignore # ty: ignore
            for idx in candidates:
                count = didppy.max(  # pyrefly: ignore # ty: ignore
                    count, table[idc, idx, index_vars[idx]]
                )
            bound += count

        return bound

    return boundexpr_charcount


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        max_strs_per_char: int | None = None,
        *args,
        **kwargs,
    ) -> str | None:
        model = ModelDidp(self.instance)
        model.solve(
            time_limit,
            log,
            extra_bounds=[make_boundexpr_charcount(max_strs_per_char)],
            disable_default_bound=True,
        )
        self.best_bound = model.best_bound
        self.solution = model.solution
        return self.solution
