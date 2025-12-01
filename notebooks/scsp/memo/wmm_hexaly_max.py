# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.12.0",
#     "hexaly>=14.0.20251112",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==6.0.0",
# ]
# [[tool.uv.index]]
# name ="hexaly"
# url = "https://pip.hexaly.com"
# explict = true
# [tool.uv.sources]
# hexaly = { index = "hexaly" }
# ///

import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    from dataclasses import dataclass
    from functools import cached_property
    import hexaly.optimizer
    import opt_note.scsp as scsp


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # WMM_HEXALY モデルを max 演算で考えてみる
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    元の `WMM_HEXALY` モデルは `WMM` をパラメータ化しただけだったため,
    一部のパラメータを動かしただけでは解が更新されにくかった. Majority Merge の部分を「最も大きい Weight を持つ文字を採用する」にすれば Weight の変換に解が追従しやすくなるのではないか.
    """)
    return


@app.class_definition
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    @cached_property
    def chars(self) -> str:
        return "".join(sorted(list(set("".join(self.instance)))))

    @cached_property
    def indices_1d_to_2d(self) -> list[tuple[int, int]]:
        ans: list[tuple[int, int]] = []
        counter = 0
        for s in self.instance:
            ans.append((counter, counter + len(s)))
            counter += len(s)
        return ans

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [priorities1d[start:end] for start, end in self.indices_1d_to_2d]

    
    def wmm(self, priorities2d: list[list[int]]) -> str:
        max_len = len(self.instance) * max(len(s) for s in self.instance)
        indices = tuple(0 for _ in self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(max_len):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                max(
                    [0]
                    + [
                        priorities2d[sidx][idx]
                        for sidx, (idx, s) in enumerate(zip(indices, self.instance))
                        if idx < len(s) and s[idx] == c
                    ]
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

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d[i] for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        initial_weights: list[list[int]] | None = None,
        *args,
        **kwargs
    ) -> str | None:
        # 重みの最大値は初期重みが与えられた場合は初期重みの最大値の 2 倍,
        # 初期重みが与えられなかった場合は文字種数とする.
        max_weight = (
            max(max(w, len(s)) for s, ws in zip(self.instance, initial_weights) for w in ws)
            if initial_weights
            else len(self.chars)
        )

        with hexaly.optimizer.HexalyOptimizer() as hxoptimizer:
            hxmodel = hxoptimizer.model
            hxparam = hxoptimizer.param

            priorities1d = [
                hxmodel.int(1, max_weight) for s in self.instance for cidx, _ in enumerate(s)
            ]
            
            func = hxmodel.create_int_external_function(self.objective)
            func.external_context.lower_bound = 0
            func.external_context.upper_bound = sum(len(s) for s in self.instance)
    
            indices_1d_to_2d: list[tuple[int, int]] = []
            counter = 0
            for s in self.instance:
                indices_1d_to_2d.append((counter, counter + len(s)))
                counter += len(s)
                
            hxmodel.minimize(func(*priorities1d))
            hxmodel.close()
    
            if initial_weights:
                priorities2d = self.priorities_1d_to_2d(priorities1d)
                for ps, ws in zip(priorities2d, initial_weights):
                    for p, w in zip(ps, ws):
                        p.set_value(w)
                        
            if time_limit is not None:
                hxparam.time_limit = time_limit
            hxparam.verbosity = 1 if log else 0
            hxoptimizer.solve()
    
            solution = hxoptimizer.solution
            status = solution.status
            if status in {
                hexaly.optimizer.HxSolutionStatus.OPTIMAL,
                hexaly.optimizer.HxSolutionStatus.FEASIBLE,
            }:
                priorities1d_value: list[int] = [p.value for p in priorities1d]
                priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
                self.solution = self.wmm(priorities2d_value)
    
        return self.solution


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="protein_n010k010.txt")
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="protein_n050k050.txt")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    元の `WMM_HEXALY` よりもだいぶ悪い結果となった.
    """)
    return


if __name__ == "__main__":
    app.run()
