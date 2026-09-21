# MILP 定式化 (Choco)

## 概要

数理最適化モデルを用いて SCSP を解く.
定式化については SCIP 版を参照.

## Python Code

```python
from dataclasses import dataclass

from pychoco.model import Model as ChocoModel
from pychoco.parallel_portfolio import ParallelPortfolio
from pychoco.variables.intvar import IntVar


def build_model(
    instance: list[str], name: str
) -> tuple[ChocoModel, list[list[IntVar]]]:
    """位置変数による定式化を組み立てる."""

    max_len = sum(len(s) for s in instance)

    chocomodel = ChocoModel(name=name)
    seqs = [[chocomodel.intvar(0, max_len - 1) for _c in s] for s in instance]

    # 各文字列の中では文字の位置は狭義単調増加.
    for seq in seqs:
        chocomodel.increasing(seq, 1).post()

    # 異なる文字が解の同じ位置に来てはならない.
    for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
        for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
            if idx1 >= idx2:
                continue
            for c1, cvar1 in zip(s1, seq1):
                for c2, cvar2 in zip(s2, seq2):
                    if c1 != c2:
                        chocomodel.arithm(cvar1, "!=", cvar2).post()

    objvar = chocomodel.intvar(0, max_len - 1)
    chocomodel.max(objvar, [seq[-1] for seq in seqs]).post()
    chocomodel.set_objective(objvar, maximize=False)

    return chocomodel, seqs


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        # モデルの複製 1 つごとにメモリを消費する.
        # 最大のインスタンスでは 1 複製あたり 1.7GB 程度になるため 4 に抑えている.
        threads: int = 4,
        *args,
        **kwargs,
    ) -> str | None:
        # 同じモデルの複製を別々の探索戦略で並列に解かせる.
        portfolio = ParallelPortfolio()
        portfolio.steal_nogoods_on_restarts()

        workers: dict[str, list[list[IntVar]]] = {}
        for widx in range(threads):
            name = f"worker{widx}"
            chocomodel, seqs = build_model(self.instance, name)
            solver = chocomodel.get_solver()
            if log and widx == 0:
                solver.show_statistics()
            if time_limit is not None:
                solver.limit_time(f"{time_limit}s")
            portfolio.add_model(chocomodel)
            workers[name] = seqs

        chocosolution = portfolio.find_best_solution()
        best_model = portfolio.get_best_model()

        # 最良解を見つけたモデルを名前で特定して変数の値を読む.
        best_name = best_model.name if best_model is not None else None
        if chocosolution is None or best_name not in workers:
            self.solution = None
            self.best_bound = 0.0
            return self.solution

        placements = {
            chocosolution.get_int_val(cvar): c
            for s, seq in zip(self.instance, workers[best_name])
            for c, cvar in zip(s, seq)
        }
        self.solution = "".join(placements[pos] for pos in sorted(placements))
        # choco は探索途中の双対限界を公開していないため,
        # 最適性が証明されたときのみ設定する.
        self.best_bound = (
            float(len(self.solution))
            if best_model.get_solver().is_objective_optimal()
            else 0.0
        )

        return self.solution
```
