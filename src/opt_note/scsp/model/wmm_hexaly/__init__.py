"""
.. include:: ./README.md
"""

import hexaly.optimizer


class Model:
    def __init__(
        self, instance: list[str], initial_weights: list[list[int]] | None = None
    ):
        chars = "".join(sorted(list(set("".join(instance)))))

        hxoptimizer = hexaly.optimizer.HexalyOptimizer()
        hxmodel = hxoptimizer.model
        assert isinstance(hxoptimizer, hexaly.optimizer.HexalyOptimizer)
        assert isinstance(hxmodel, hexaly.optimizer.HxModel)

        # 重みの最大値は初期重みが与えられた場合は初期重みの最大値の 2 倍,
        # 初期重みが与えられなかった場合は文字種数とする.
        max_weight = (
            max(2 * w for ws in initial_weights for w in ws)
            if initial_weights
            else len(chars)
        )
        priorities1d = [
            hxmodel.int(1, max_weight) for s in instance for cidx, _ in enumerate(s)
        ]

        func = hxmodel.create_int_external_function(self.objective)
        func.external_context.lower_bound = 0
        func.external_context.upper_bound = sum(len(s) for s in instance)

        indices_1d_to_2d: list[tuple[int, int]] = []
        counter = 0
        for s in instance:
            indices_1d_to_2d.append((counter, counter + len(s)))
            counter += len(s)

        self.instance = instance
        self.chars = chars
        self.hxoptimizer = hxoptimizer
        self.hxmodel = hxmodel
        self.priorities1d = priorities1d
        self.indices_1d_to_2d = indices_1d_to_2d

        # これらが実行される時点で self.* が必要になるため初期化の最後に移動

        hxmodel.minimize(func(*priorities1d))
        hxmodel.close()

        if initial_weights:
            priorities2d = self.priorities_1d_to_2d(priorities1d)
            for ps, ws in zip(priorities2d, initial_weights):
                for p, w in zip(ps, ws):
                    p.set_value(w)

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        assert isinstance(self.hxoptimizer.param, hexaly.optimizer.HxParam)
        if time_limit is not None:
            self.hxoptimizer.param.time_limit = time_limit
        self.hxoptimizer.param.verbosity = 1 if log else 0
        self.hxoptimizer.solve()
        return self

    def to_solution(self) -> str | None:
        assert isinstance(self.hxoptimizer.solution, hexaly.optimizer.HxSolution)
        status = self.hxoptimizer.solution.status
        if status not in {
            hexaly.optimizer.HxSolutionStatus.OPTIMAL,
            hexaly.optimizer.HxSolutionStatus.FEASIBLE,
        }:
            return None

        priorities1d_value: list[int] = [p.value for p in self.priorities1d]
        priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
        return self.wmm(priorities2d_value)

    def wmm(self, priorities2d: list[list[int]]) -> str:
        indices = tuple(0 for _ in self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(len(self.instance) * max(len(s) for s in self.instance)):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                sum(
                    priorities2d[sidx][idx]
                    for sidx, (idx, s) in enumerate(zip(indices, self.instance))
                    if idx < len(s) and s[idx] == c
                )
                for c in self.chars
            ]
            next_char = self.chars[counts.index(max(counts))]

            solution += next_char
            indices = tuple(
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(indices, self.instance)
            )

        return solution

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [priorities1d[start:end] for start, end in self.indices_1d_to_2d]

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d[i] for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)


def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
