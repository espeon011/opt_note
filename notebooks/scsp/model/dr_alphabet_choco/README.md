# アルファベットアルゴリズムで作成したものを削り出す (Choco)

## 概要

アルファベットアルゴリズムで求めた解から不要な文字を削除することで得られる解を探索する.
定式化については CP-SAT 版を参照.

## Python Code

```python
from dataclasses import dataclass

from pychoco.model import Model as ChocoModel
from pychoco.parallel_portfolio import ParallelPortfolio
from pychoco.variables.intvar import IntVar

from ..alphabet import Model as ModelAlphabet


def build_model(
    instance: list[str], template: str, name: str
) -> tuple[ChocoModel, list[IntVar]]:
    """テンプレートから削り出す定式化を組み立てる."""

    chocomodel = ChocoModel(name=name)

    # valids[idx]: テンプレートの idx 文字目を解に採用するか否か.
    valids = [chocomodel.intvar(0, 1) for _tc in template]
    one = chocomodel.intvar(1, 1)

    for s in instance:
        # 文字 c はテンプレート中で c が置かれている位置にしか対応づけられないので,
        # 定義域をその位置集合に限定した変数を作る.
        seq = [
            chocomodel.intvar([idx for idx, tc in enumerate(template) if tc == c])
            for c in s
        ]
        chocomodel.increasing(seq, 1).post()
        for cvar in seq:
            chocomodel.element(one, valids, cvar).post()

    objvar = chocomodel.intvar(0, len(template))
    chocomodel.sum(valids, "=", objvar).post()
    chocomodel.set_objective(objvar, maximize=False)

    return chocomodel, valids


@dataclass
class ModelReduction:
    instance: list[str]
    template: str
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        threads: int = 8,
        *args,
        **kwargs,
    ) -> str | None:
        # 同じモデルの複製を別々の探索戦略で並列に解かせる.
        portfolio = ParallelPortfolio()
        portfolio.steal_nogoods_on_restarts()

        workers: dict[str, list[IntVar]] = {}
        for widx in range(threads):
            name = f"worker{widx}"
            chocomodel, valids = build_model(self.instance, self.template, name)
            solver = chocomodel.get_solver()
            if log and widx == 0:
                solver.show_statistics()
            if time_limit is not None:
                solver.limit_time(f"{time_limit}s")
            portfolio.add_model(chocomodel)
            workers[name] = valids

        chocosolution = portfolio.find_best_solution()
        best_model = portfolio.get_best_model()

        # 最良解を見つけたモデルを名前で特定して変数の値を読む.
        best_name = best_model.name if best_model is not None else None
        if chocosolution is None or best_name not in workers:
            self.solution = None
            self.best_bound = 0.0
            return self.solution

        self.solution = "".join(
            tc
            for tc, valid in zip(self.template, workers[best_name])
            if chocosolution.get_int_val(valid) == 1
        )
        self.best_bound = (
            float(len(self.solution))
            if best_model.get_solver().is_objective_optimal()
            else 0.0
        )

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
```
