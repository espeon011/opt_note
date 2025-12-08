"""
.. include:: ./README.md
"""

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

        nodes = [
            (sidx, cidx)
            for sidx, s in enumerate(self.instance)
            for cidx, _ in enumerate(s)
        ]
        order = [cpmodel.new_int_var(1, len(nodes), "") for _ in nodes]

        dummy_idx = len(nodes)
        order.append(cpmodel.new_constant(0))

        arcs = []
        costs = dict()

        for nidx, (sidx, cidx) in enumerate(nodes):
            if cidx == 0:
                arcs.append((dummy_idx, nidx, cpmodel.new_bool_var("")))
                costs[(dummy_idx, nidx)] = 1
            if cidx == len(self.instance[sidx]) - 1:
                arcs.append((nidx, dummy_idx, cpmodel.new_bool_var("")))
                costs[(nidx, dummy_idx)] = 0

        for nidx1, (sidx1, cidx1) in enumerate(nodes):
            for nidx2, (sidx2, cidx2) in enumerate(nodes):
                if sidx1 == sidx2 and cidx1 + 1 != cidx2:
                    continue
                s1 = self.instance[sidx1]
                s2 = self.instance[sidx2]
                arcs.append((nidx1, nidx2, cpmodel.new_bool_var("")))
                costs[(nidx1, nidx2)] = (
                    0 if sidx1 < sidx2 and s1[cidx1] == s2[cidx2] else 1
                )

        cpmodel.add_circuit(arcs)

        for nidx1, nidx2, v in arcs:
            if nidx2 == dummy_idx:
                continue
            cpmodel.add(order[nidx2] == order[nidx1] + 1).only_enforce_if(v)

        nidx = -1
        for s in self.instance:
            for cidx, _ in enumerate(s):
                nidx += 1
                if cidx == 0:
                    continue
                cpmodel.add(order[nidx - 1] < order[nidx])

        cpmodel.minimize(sum(costs[(nidx1, nidx2)] * v for (nidx1, nidx2, v) in arcs))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
            solution = ""
            current_node = dummy_idx
            current_char: str | None = None
            current_sidxs: set[int] = set()
            complete = False
            while True:
                for nidx1, nidx2, v in arcs:
                    if nidx1 == current_node and cpsolver.boolean_value(v):
                        if nidx2 == dummy_idx:
                            complete = True
                            break
                        sidx, cidx = nodes[nidx2]

                        if (
                            self.instance[sidx][cidx] != current_char
                            or sidx in current_sidxs
                        ):
                            solution += self.instance[sidx][cidx]
                            current_sidxs.clear()

                        current_node = nidx2
                        current_char = self.instance[sidx][cidx]
                        current_sidxs.add(sidx)
                if complete:
                    break
            self.solution = solution
        else:
            self.solution = None

        return self.solution
