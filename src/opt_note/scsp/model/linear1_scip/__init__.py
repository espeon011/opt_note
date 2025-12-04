"""
.. include:: ./README.md
"""

from dataclasses import dataclass
import pyscipopt


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        scip: pyscipopt.Model = pyscipopt.Model()

        max_len = sum(len(s) for s in self.instance)
        seqs = [
            [scip.addVar(vtype="I", lb=0, ub=max_len - 1) for _ in s]
            for s in self.instance
        ]

        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                scip.addCons(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(self.instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(self.instance, seqs)):
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

        if time_limit is not None:
            scip.setParam("limits/time", time_limit)
        if not log:
            scip.hideOutput()
        scip.optimize()

        self.best_bound = scip.getDualbound()

        if scip.getNLimSolsFound() > 0:
            objval = int(round(scip.getObjVal()))
            sol_char_idx = 0
            solution = ""
            while sol_char_idx <= objval:
                found = False
                for idx, (s, seq) in enumerate(zip(self.instance, seqs)):
                    for c_idx, cvar in enumerate(seq):
                        if int(round(scip.getVal(cvar))) == sol_char_idx:
                            solution += s[c_idx]
                            found = True
                            sol_char_idx += 1
                    if found:
                        break
                if not found:
                    sol_char_idx += 1
                self.solution = solution

        return self.solution
