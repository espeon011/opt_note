"""
.. include:: ./README.md
"""

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
