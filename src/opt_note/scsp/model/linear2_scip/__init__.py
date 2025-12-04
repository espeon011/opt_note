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
        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)

        scip: pyscipopt.Model = pyscipopt.Model()

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か
        assign: list[list[list[pyscipopt.Variable]]] = [
            [[scip.addVar(vtype="B") for _ in range(max_len)] for c in s]
            for s in self.instance
        ]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か
        sseq_char: list[list[pyscipopt.Variable]] = [
            [scip.addVar(vtype="B") for _ in chars] for _ in range(max_len)
        ]

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か
        sseq_valid: list[pyscipopt.Variable] = [
            scip.addVar(vtype="B") for _ in range(max_len)
        ]

        # 超配列の i 番目に何かの文字が割り当てられたか否か.
        # (+ 異なる文字を同じ場所に割り当てられない)
        for idx in range(max_len):
            scip.addCons(sum(sseq_char[idx]) == sseq_valid[idx])

        # s 番目の文字列の c 番目の文字が共通超配列の i 番目に配置されたかどうか.
        # (+ 異なる文字列の同じ文字は同じ場所に配置することができる)
        for sidx, s in enumerate(self.instance):
            for idx in range(max_len):
                for j, char in enumerate(chars):
                    scip.addCons(
                        sum(
                            assign[sidx][cidx][idx]
                            for cidx, c in enumerate(s)
                            if c == char
                        )
                        <= sseq_char[idx][j]
                    )

        # 各文字列は必ず超配列に埋め込まれる & 埋め込み順序.
        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                scip.addCons(sum(assign[sidx][cidx]) == 1)
                if cidx == 0:
                    continue
                scip.addCons(
                    sum(
                        idx * assign[sidx][cidx - 1][idx]
                        for idx, _ in enumerate(assign[sidx][cidx - 1])
                    )
                    + 1
                    <= sum(
                        idx * assign[sidx][cidx][idx]
                        for idx, _ in enumerate(assign[sidx][cidx])
                    )
                )

        scip.setObjective(sum(sseq_valid), sense="minimize")

        if time_limit is not None:
            scip.setParam("limits/time", time_limit)
        if not log:
            scip.hideOutput()
        scip.optimize()

        self.best_bound = scip.getDualbound()

        if scip.getNLimSolsFound() > 0:
            solution = ""
            for valid, ssqc in zip(sseq_valid, sseq_char):
                if int(round(scip.getVal(valid))) == 1:
                    for c, sqc in zip(chars, ssqc):
                        if int(round(scip.getVal(sqc))) == 1:
                            solution += c
                            break
            self.solution = solution
        else:
            self.solution = None

        return self.solution
