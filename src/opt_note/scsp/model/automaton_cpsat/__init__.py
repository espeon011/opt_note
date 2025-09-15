"""
.. include:: ./README.md
"""

from ortools.sat.python import cp_model


class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)
        chars = "".join(sorted(list(set("".join(instance)))))

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="") for _ in range(max_len)
        ]

        for s in instance:
            transition_triples = (
                [
                    (idx, jdx + 1, (idx + 1 if c == next_char else idx))
                    for idx, next_char in enumerate(s)
                    for jdx, c in enumerate(chars)
                ]
                + [(idx, 0, idx) for idx, _ in enumerate(s)]
                + [(len(s), 0, len(s))]
                + [(len(s), jdx + 1, len(s)) for jdx, _ in enumerate(chars)]
            )
            cpmodel.add_automaton(
                transition_expressions=cvars,
                starting_state=0,
                final_states=[len(s)],
                transition_triples=transition_triples,
            )

        valids = [cpmodel.new_bool_var("") for _ in cvars]
        for cvar, valid in zip(cvars, valids):
            cpmodel.add(cvar == 0).only_enforce_if(~valid)
        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars
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
        for cvar in self.cvars:
            cidx = self.cpsolver.value(cvar) - 1
            if cidx >= 0:
                solution += self.chars[cidx]

        return solution


def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
