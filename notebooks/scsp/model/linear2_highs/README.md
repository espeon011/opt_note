# MILP バイナリ定式化 (HiGHS)

## 概要

数理最適化モデルを用いて SCSP を解く.
定式化については SCIP 版を参照.

## Python Code

```python
from dataclasses import dataclass
import math
import highspy


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)

        highs = highspy.Highs()

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か
        assign = [[highs.addBinaries(max_len) for c in s] for s in self.instance]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か
        sseq_char = [highs.addBinaries(len(chars)) for _ in range(max_len)]

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か
        sseq_valid = highs.addBinaries(max_len)

        # 超配列の i 番目に何かの文字が割り当てられたか否か.
        # (+ 異なる文字を同じ場所に割り当てられない)
        for idx in range(max_len):
            highs.addConstr(sseq_char[idx].sum() == sseq_valid[idx])

        # s 番目の文字列の c 番目の文字が共通超配列の i 番目に配置されたかどうか.
        # (+ 異なる文字列の同じ文字は同じ場所に配置することができる)
        for sidx, s in enumerate(self.instance):
            for idx in range(max_len):
                for j, char in enumerate(chars):
                    highs.addConstr(
                        sum(
                            assign[sidx][cidx][idx]
                            for cidx, c in enumerate(s)
                            if c == char
                        )
                        <= sseq_char[idx][j]
                    )

        # 各文字列は必ず超配列に埋め込まれる & 埋め込み順序.
        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                highs.addConstr(assign[sidx][cidx].sum() == 1)
                if cidx == 0:
                    continue
                highs.addConstr(
                    (assign[sidx][cidx - 1] * list(range(max_len))).sum() + 1
                    <= (assign[sidx][cidx] * list(range(max_len))).sum()
                )

        highs.setObjective(obj=sseq_valid.sum(), sense=highspy.ObjSense.kMinimize)

        highs.setOptionValue("output_flag", log)
        if time_limit is not None:
            highs.setOptionValue("time_limit", time_limit)
        highs.solve()

        info = highs.getInfo()
        self.best_bound = info.mip_dual_bound
        primal_status = info.primal_solution_status
        if primal_status == highspy.SolutionStatus.kSolutionStatusFeasible:
            highssolution = highs.getSolution()
            solution = ""
            for valid, ssqc in zip(sseq_valid, sseq_char):
                if math.isclose(highssolution.col_value[valid.index], 1):
                    for c, sqc in zip(chars, ssqc):
                        if math.isclose(highssolution.col_value[sqc.index], 1):
                            solution += c
                            break
            self.solution = solution
        else:
            self.solution = None

        return self.solution
```
