"""
.. include:: ./README.md
"""

from ortools.sat.python import cp_model


class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        valids = [cpmodel.new_bool_var("") for _ in range(max_len)]
        cvars = [
            [cpmodel.new_int_var(0, max(len(s) for s in instance) - 1, "") for c in s]
            for s in instance
        ]

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(
                    len(chars) * cvars[sidx][cidx - 1] + chars.index(s[cidx - 1])
                    < len(chars) * cvars[sidx][cidx] + chars.index(s[cidx])
                )

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                cpmodel.add_element(
                    len(chars) * cvars[sidx][cidx] + chars.index(c),
                    valids,
                    1,
                )

        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.valids = valids
        self.status: cp_model.cp_model_pb2.CpSolverStatus | None = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            return None

        solution = ""
        for idx, valid in enumerate(self.valids):
            if self.cpsolver.boolean_value(valid):
                solution += self.chars[idx % len(self.chars)]

        return solution
