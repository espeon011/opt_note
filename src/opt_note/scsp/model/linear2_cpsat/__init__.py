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

        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か.
        sseq_valid = [cpmodel.new_bool_var("") for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か.
        sseq_char = [[cpmodel.new_bool_var("") for _ in chars] for _ in range(max_len)]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か.
        assign = [
            [[cpmodel.new_bool_var("") for _ in range(max_len)] for c in s]
            for s in self.instance
        ]

        # 共通超配列の i 番目にはどれか 1 文字だけが置かれる.
        # 共通超配列の i 番目に文字が置かれるかどうか.
        for idx in range(max_len):
            cpmodel.add_at_most_one(sseq_char[idx])
            cpmodel.add_max_equality(sseq_valid[idx], sseq_char[idx])

        # s 番目の文字列の c 番目の文字は共通超配列のどこか一か所にのみ置かれる.
        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                cpmodel.add_exactly_one(assign[sidx][cidx])

        # 共通超配列に置くときは同じ文字である必要がある.
        for idx in range(max_len):
            for j, char in enumerate(chars):
                cpmodel.add_max_equality(
                    sseq_char[idx][j],
                    [
                        assign[sidx][cidx][idx]
                        for sidx, s in enumerate(self.instance)
                        for cidx, c in enumerate(s)
                        if c == char
                    ],
                )

        # s 番目の文字列の共通超配列への埋め込み順序固定.
        for sidx, s in enumerate(self.instance):
            order = [cpmodel.new_int_var(0, max_len - 1, "") for _ in s]
            for cidx, o in enumerate(order):
                cpmodel.add_map_domain(o, assign[sidx][cidx])
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(order[cidx - 1] < order[cidx])

        cpmodel.minimize(sum(sseq_valid))

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
            for v, cs in zip(sseq_valid, sseq_char):
                if not cpsolver.boolean_value(v):
                    continue
                for cv, c in zip(cs, chars):
                    if cpsolver.boolean_value(cv):
                        solution += c
                        break
            self.solution = solution
        else:
            self.solution = None

        return self.solution
