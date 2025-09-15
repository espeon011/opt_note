# オートマトン制約を用いた数理計画モデル

CP-SAT 固有のオートマトン制約を用いて定式化してみる.

**定数**

- $\Sigma = \lbrace \sigma_1, \dots, \sigma_q \rbrace$: 文字の集合

**決定変数**

- $x_i \in \mathbb{Z}$: 解において $i$ 番目の文字が $\sigma_j$ であれば $j$ となる.
  どの文字も対応しないとき $0$.
  このとき解は $\sigma_{x_0} \sigma_{x_1} \dots$ となる.
  ただし $\sigma_0$ は空文字列とする.
- $v_i \in \lbrace 0, 1 \rbrace$: 解の $i$ 番目が空でないとき $1$. 空のとき $0$.

**制約条件**

- $x_i > 0 \Rightarrow v_i = 1$
- 与えられた文字列 $s \in S$ の各文字を $\Sigma$ を基準にインデックスの配列としたものを $\mathrm{index}_s$ とする.
  $\mathrm{index}_s$ を部分配列にもつすべての配列を受理するオートマトンを文字列の数だけ作成し,
  $\lbrace x_i \rbrace_i$ が受理されるという制約を課す.

**目的関数**

- minimize $\sum_{i} v_i$

## Python Code

```python
from ortools.sat.python import cp_model


class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)
        chars = "".join(sorted(list(set("".join(instance)))))

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="") for _ in range(max_len)
        ]

        for s in instance:
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

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars
        self.status: cp_model.cp_model_pb2.CpSolverStatus | None = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            return None

        solution = ""
        for cvar in self.cvars:
            cidx = self.cpsolver.value(cvar) - 1
            if cidx >= 0:
                solution += self.chars[cidx]

        return solution


def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
```
