"""
.. include:: ./README.md
"""

import pyscipopt


class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)

        scip: pyscipopt.Model = pyscipopt.Model()

        seqs = [
            [scip.addVar(vtype="I", lb=0, ub=max_len - 1) for _ in s] for s in instance
        ]
        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                scip.addCons(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
                if idx1 >= idx2:
                    continue

                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            lt = scip.addVar(vtype="B")
                            gt = scip.addVar(vtype="B")
                            scip.addCons(lt + gt == 1)
                            scip.addConsIndicator(cvar1 + 1 <= cvar2, binvar=lt)
                            scip.addConsIndicator(cvar1 >= cvar2 + 1, binvar=gt)

        obj = scip.addVar(vtype="C", lb=0, ub=max_len)
        for seq in seqs:
            scip.addCons(obj >= seq[-1])
        scip.setObjective(obj + 1, sense="minimize")

        self.instance = instance
        self.scip = scip
        self.seqs = seqs

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        if time_limit is not None:
            self.scip.setParam("limits/time", time_limit)
        if not log:
            self.scip.hideOutput()
        self.scip.optimize()

        return self

    def to_solution(self) -> str | None:
        if self.scip.getNLimSolsFound() == 0:
            return None

        objval = int(round(self.scip.getObjVal()))
        sol_char_idx = 0
        solution = ""
        while sol_char_idx <= objval:
            found = False
            for idx, (s, seq) in enumerate(zip(self.instance, self.seqs)):
                for c_idx, cvar in enumerate(seq):
                    if int(round(self.scip.getVal(cvar))) == sol_char_idx:
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
