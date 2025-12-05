"""
.. include:: ./README.md
"""

from dataclasses import dataclass
from functools import cached_property
import hexaly.optimizer


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: int = 0

    @cached_property
    def nodes(self) -> list[tuple[int, int]]:
        return [
            (sidx, cidx)
            for sidx, s in enumerate(self.instance)
            for cidx, _ in enumerate(s)
        ]

    def makesol(self, seq: list[int]) -> str:
        max_sidx = -1
        current_char: str | None = None
        solution = ""
        for nidx in seq:
            sidx, cidx = self.nodes[nidx]
            next_char = self.instance[sidx][cidx]
            if current_char is None or next_char != current_char or sidx <= max_sidx:
                solution += next_char
                current_char = next_char
                max_sidx = -1
            max_sidx = sidx
        return solution

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        cost_table = [
            [
                0 if c1 == c2 and sidx1 < sidx2 else 1
                for sidx2, s2 in enumerate(self.instance)
                for c2 in s2
            ]
            for sidx1, s1 in enumerate(self.instance)
            for c1 in s1
        ]

        with hexaly.optimizer.HexalyOptimizer() as hxoptimizer:
            assert isinstance(hxoptimizer.model, hexaly.optimizer.HxModel)
            assert isinstance(hxoptimizer.param, hexaly.optimizer.HxParam)
            hxmodel: hexaly.optimizer.HxModel = hxoptimizer.model
            hxparam: hexaly.optimizer.HxParam = hxoptimizer.param

            seq = hxmodel.list(len(self.nodes))
            hxmodel.constraint(hxmodel.count(seq) == len(self.nodes))

            for sidx, s in enumerate(self.instance):
                nidx_per_s = sorted(
                    [nidx for nidx, node in enumerate(self.nodes) if node[0] == sidx]
                )
                for cidx, _ in enumerate(nidx_per_s):
                    if cidx == 0:
                        continue
                    hxmodel.constraint(
                        hxmodel.index(seq, nidx_per_s[cidx - 1])
                        < hxmodel.index(seq, nidx_per_s[cidx])
                    )

            cost_table_array = hxmodel.array(cost_table)
            cost_lambda = hxmodel.lambda_function(
                lambda i: hxmodel.at(cost_table_array, seq[i - 1], seq[i])
            )
            objective = 1 + hxmodel.sum(hxmodel.range(1, len(self.nodes)), cost_lambda)
            hxmodel.minimize(objective)

            hxmodel.close()

            if time_limit is not None:
                hxparam.time_limit = time_limit
            hxparam.verbosity = 1 if log else 0

            hxoptimizer.solve()

            assert isinstance(hxoptimizer.solution, hexaly.optimizer.HxSolution)
            hxsolution: hexaly.optimizer.HxSolution = hxoptimizer.solution

            self.best_bound = hxsolution.get_objective_bound(0)
            if hxsolution.status in {
                hexaly.optimizer.HxSolutionStatus.OPTIMAL,
                hexaly.optimizer.HxSolutionStatus.FEASIBLE,
            }:
                self.solution = self.makesol([x for x in seq.value])
            else:
                self.solution = None

            return self.solution
