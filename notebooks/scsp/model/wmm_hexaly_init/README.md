# WMM + Hexaly モデルに初期重みを追加

`WMM_HEXALY` モデルにおいて重み決定変数の初期値を `WMM` と等しくなるよう全て同じ値で設定する. 

巨大なインスタンスにおいて常に `WMM` 以上の質の解が出る反面, 小さ目のインスタンスでは `WMM_HEXALY` と比較して悪化することがある.

## Python Code

```python
from ..wmm_hexaly import Model


def create_model(instance: list[str]) -> Model:
    initial_weights = [[len(s) - cidx for cidx, _ in enumerate(s)] for s in instance]
    return Model(instance, initial_weights)


def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    model = create_model(instance)
    model.solve(time_limit, log)
    return model.to_solution()
```
