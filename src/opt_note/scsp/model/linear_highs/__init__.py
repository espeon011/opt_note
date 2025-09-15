"""
.. include:: ./README.md
"""

import math
import highspy


class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)

        highs = highspy.Highs()

        seqs = [
            [highs.addIntegral(lb=0, ub=max_len - 1) for idx, _ in enumerate(s)]
            for s in instance
        ]
        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                highs.addConstr(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
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

        self.instance = instance
        self.highs = highs
        self.seqs = seqs

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.highs.setOptionValue("output_flag", log)
        if time_limit is not None:
            self.highs.setOptionValue("time_limit", time_limit)
        self.highs.solve()
        return self

    def to_solution(self) -> str | None:
        info = self.highs.getInfo()
        primal_status = info.primal_solution_status
        if primal_status != highspy.SolutionStatus.kSolutionStatusFeasible:
            return None

        highssolution = self.highs.getSolution()
        objval = int(self.highs.getObjectiveValue())
        sol_char_idx = 0
        solution = ""
        while sol_char_idx <= objval:
            found = False
            for idx, (s, seq) in enumerate(zip(self.instance, self.seqs)):
                for c_idx, cvar in enumerate(seq):
                    if math.isclose(highssolution.col_value[cvar.index], sol_char_idx):
                        solution += s[c_idx]
                        found = True
                        sol_char_idx += 1
                if found:
                    break
            if not found:
                sol_char_idx += 1

        return solution


def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
