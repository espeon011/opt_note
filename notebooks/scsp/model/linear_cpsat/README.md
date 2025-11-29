# MILP 定式化 (CP-SAT)

数理最適化モデルを用いて SCSP を解く.
定式化については SCIP 版を参照.

## Python Code

```python
from dataclasses import dataclass
from ortools.sat.python import cp_model


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        max_len = sum(len(s) for s in self.instance)
        seqs = [
            [cpmodel.new_int_var(0, max_len - 1, "") for c in s] for s in self.instance
        ]

        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                cpmodel.add(seq[idx - 1] < seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(self.instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(self.instance, seqs)):
                if idx1 >= idx2:
                    continue
                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            cpmodel.add(cvar1 != cvar2)

        obj = cpmodel.new_int_var(0, max_len, "")
        cpmodel.add_max_equality(obj, [seq[-1] for seq in seqs])
        cpmodel.minimize(obj)

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            objval = int(cpsolver.objective_value)
            sol_char_idx = 0
            solution = ""
            while sol_char_idx <= objval:
                found = False
                for idx, (s, seq) in enumerate(zip(self.instance, seqs)):
                    for c_idx, cvar in enumerate(seq):
                        if cpsolver.value(cvar) == sol_char_idx:
                            solution += s[c_idx]
                            found = True
                            sol_char_idx += 1
                    if found:
                        break
                if not found:
                    sol_char_idx += 1
            self.solution = solution

        return self.solution
```
