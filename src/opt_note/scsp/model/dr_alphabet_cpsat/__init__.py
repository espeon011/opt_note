"""
.. include:: ./README.md
"""

from dataclasses import dataclass
from ortools.sat.python import cp_model
from ..alphabet import Model as ModelAlphabet


@dataclass
class ModelReduction:
    instance: list[str]
    template: str
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, time_limit: int | None = 60, log: bool = False) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance + [self.template])))))

        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        valids = [cpmodel.new_bool_var("") for _ in self.template]
        cvars = [
            [
                cpmodel.new_int_var_from_domain(
                    cp_model.Domain.from_values(
                        [idx for idx, solc in enumerate(self.template) if c == solc]
                    ),
                    "",
                )
                for c in s
            ]
            for s in self.instance
        ]

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(cvars[sidx][cidx - 1] < cvars[sidx][cidx])

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                cpmodel.add_element(cvars[sidx][cidx], valids, 1)

        cpmodel.minimize(sum(valids))
        # cpmodel.minimize(cp_model.LinearExpr.sum(valids))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit

        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            solution = ""
            for idx, valid in enumerate(valids):
                if cpsolver.boolean_value(valid):
                    solution += chars[idx % len(chars)]
            self.solution = solution
        else:
            self.solution = None

        return self.solution


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0
    inner_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        template = ModelAlphabet(self.instance).solve()
        if template is None:
            return None
        inner_model = ModelReduction(self.instance, template)
        inner_model.solve(time_limit, log)
        self.solution = inner_model.solution
        self.inner_bound = inner_model.best_bound
        return self.solution
