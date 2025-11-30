# WMM + Hexaly モデルに初期重みを追加

## 概要

`WMM_HEXALY` モデルにおいて重み決定変数の初期値を `WMM` と等しくなるよう全て同じ値で設定する. 

巨大なインスタンスにおいて常に `WMM` 以上の質の解が出る反面, 小さ目のインスタンスでは `WMM_HEXALY` と比較して悪化することがある.

## Python Code

```python
from dataclasses import dataclass
from .. import wmm_hexaly


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        initial_weights = [
            [len(s) - cidx for cidx, _ in enumerate(s)] for s in self.instance
        ]
        model = wmm_hexaly.Model(self.instance)
        self.solution = model.solve(time_limit, log, initial_weights)
        return self.solution
```
