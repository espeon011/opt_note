# MILP 定式化 (HiGHS)

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
        highs = highspy.Highs()

        max_len = sum(len(s) for s in self.instance)
        seqs = [
            [highs.addIntegral(lb=0, ub=max_len - 1) for idx, _ in enumerate(s)]
            for s in self.instance
        ]

        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                highs.addConstr(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(self.instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(self.instance, seqs)):
                if idx1 >= idx2:
                    continue

                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            lt = highs.addBinary()
                            gt = highs.addBinary()
                            highs.addConstr(lt + gt == 1)
                            big_m = max_len
                            highs.addConstr(cvar1 + 1 <= cvar2 + big_m * (1 - lt))
                            highs.addConstr(cvar1 + big_m * (1 - gt) >= cvar2 + 1)

        obj = highs.addVariable(lb=0, ub=max_len)
        for seq in seqs:
            highs.addConstr(obj >= seq[-1])
        highs.setObjective(obj=obj, sense=highspy.ObjSense.kMinimize)

        highs.setOptionValue("output_flag", log)
        if time_limit is not None:
            highs.setOptionValue("time_limit", time_limit)
        highs.solve()

        info = highs.getInfo()
        self.best_bound = info.mip_dual_bound
        primal_status = info.primal_solution_status
        if primal_status == highspy.SolutionStatus.kSolutionStatusFeasible:
            highssolution = highs.getSolution()
            objval = int(highs.getObjectiveValue())
            sol_char_idx = 0
            solution = ""
            while sol_char_idx <= objval:
                found = False
                for idx, (s, seq) in enumerate(zip(self.instance, seqs)):
                    for c_idx, cvar in enumerate(seq):
                        if math.isclose(
                            highssolution.col_value[cvar.index], sol_char_idx
                        ):
                            solution += s[c_idx]
                            found = True
                            sol_char_idx += 1
                    if found:
                        break
                if not found:
                    sol_char_idx += 1

            self.solution = solution
        else:
            self.solution = None

        return self.solution
```
