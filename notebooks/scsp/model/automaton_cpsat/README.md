# オートマトン制約を用いた数理計画モデル

## 概要

CP-SAT 固有のオートマトン制約を用いて定式化してみる.

### 定数

- $\Sigma = \lbrace \sigma_1, \dots, \sigma_q \rbrace$: 文字の集合

### 決定変数

- $x_i \in \mathbb{Z}$: 解において $i$ 番目の文字が $\sigma_j$ であれば $j$ となる.
  どの文字も対応しないとき $0$.
  このとき解は $\sigma_{x_0} \sigma_{x_1} \dots$ となる.
  ただし $\sigma_0$ は空文字列とする.
- $v_i \in \lbrace 0, 1 \rbrace$: 解の $i$ 番目が空でないとき $1$. 空のとき $0$.

### 制約条件

- $x_i > 0 \Rightarrow v_i = 1$
- 与えられた文字列 $s \in S$ の各文字を $\Sigma$ を基準にインデックスの配列としたものを $\mathrm{index}_s$ とする.
  $\mathrm{index}_s$ を部分配列にもつすべての配列を受理するオートマトンを文字列の数だけ作成し,
  $\lbrace x_i \rbrace_i$ が受理されるという制約を課す.

### 目的関数

- minimize $\sum_{i} v_i$

## Python Code

```python
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
        max_len = sum(len(s) for s in self.instance)
        chars = "".join(sorted(list(set("".join(self.instance)))))

        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="") for _ in range(max_len)
        ]

        for s in self.instance:
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

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)
        self.best_bound = cpsolver.best_objective_bound

        if status in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
            solution = ""
            for cvar in cvars:
                cidx = cpsolver.value(cvar) - 1
                if cidx >= 0:
                    solution += chars[cidx]
            self.solution = solution
        else:
            self.solution = None

        return self.solution
```
