# MILP 定式化 (Hexaly)

## 概要

数理最適化モデルを用いて SCSP を解く.
定式化については SCIP 版を参照.

## Python Code

```python
from dataclasses import dataclass

import hexaly.optimizer


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *_args, **_kwargs
    ) -> str | None:
        with hexaly.optimizer.HexalyOptimizer() as hxoptimizer:
            assert isinstance(hxoptimizer.model, hexaly.optimizer.HxModel)
            assert isinstance(hxoptimizer.param, hexaly.optimizer.HxParam)
            hxmodel: hexaly.optimizer.HxModel = hxoptimizer.model
            hxparam: hexaly.optimizer.HxParam = hxoptimizer.param

            max_len = sum(len(s) for s in self.instance)

            seqs = [[hxmodel.int(0, max_len - 1) for _c in s] for s in self.instance]

            for seq in seqs:
                for cidx, cvar in enumerate(seq):
                    if cidx == 0:
                        continue
                    hxmodel.constraint(seq[cidx - 1] < cvar)

            for idx1, (s1, seq1) in enumerate(zip(self.instance, seqs)):
                for idx2, (s2, seq2) in enumerate(zip(self.instance, seqs)):
                    if idx1 >= idx2:
                        continue
                    for c1, cvar1 in zip(s1, seq1):
                        for c2, cvar2 in zip(s2, seq2):
                            if c1 != c2:
                                hxmodel.constraint(cvar1 != cvar2)

            hxmodel.minimize(hxmodel.max([seq[-1] for seq in seqs]))
            hxmodel.close()

            if time_limit is not None:
                hxparam.time_limit = time_limit
            hxparam.verbosity = 1 if log else 0

            hxoptimizer.solve()

            assert isinstance(hxoptimizer.solution, hexaly.optimizer.HxSolution)
            hxsolution: hexaly.optimizer.HxSolution = hxoptimizer.solution

            # 目的関数は最後の文字の位置なので, 解の長さの下界はそれに 1 を足したもの.
            self.best_bound = float(hxsolution.get_objective_bound(0)) + 1

            if hxsolution.status in {
                hexaly.optimizer.HxSolutionStatus.OPTIMAL,
                hexaly.optimizer.HxSolutionStatus.FEASIBLE,
            }:
                placements = {
                    # pyrefly: ignore # ty: ignore
                    int(cvar.value): c
                    for s, seq in zip(self.instance, seqs)
                    for c, cvar in zip(s, seq)
                }
                self.solution = "".join(placements[pos] for pos in sorted(placements))
            else:
                self.solution = None

        return self.solution
```
