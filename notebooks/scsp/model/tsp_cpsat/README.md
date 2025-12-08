# 順序制約付き巡回セールスマン問題として定式化 (CP-SAT)

## 概要

- 計算量: ?
- 近似精度: $n$

各文字列の各文字を頂点とした TSP に頂点を訪れる順序を定める制約を課して定式化する. 

### 決定変数

- $x_{(i_1, j_1),(i_2, j_2)} \in \lbrace 0, 1 \rbrace$: $i_1$ 番目の文字列の $j_1$ 番目の文字に対応する頂点と $i_2$ 番目の文字列の $j_2$ 番目の文字に対応する頂点を結ぶ辺を使用するかどうかを表す 0-1 変数. 
- $y_{(i, j)} \in \mathbb{Z}$: $i$ 番目の文字列の $j$ 番目の文字は巡回において何番目に訪れるか. 

### 制約条件

- ダミーの頂点を入れたうえで circuit 制約を課す. 
- ダミーの頂点を訪れる順番を $0$ に固定し, $y_{(i, j)}$ たちに「$x_{(i_1, j_1),(i_2, j_2)} = 1$ ならば $y_{(i_2, j_2)} = y_{(i_1, j_1)} + 1$」を課す. 
- $y_{(i, j)} < y_{(i, j+1)} \ (\forall i = 1, \dots, n, \ \forall j = 1, \dots, |s_i| - 1)$

### 目的関数

頂点間の遷移コストは次のように定義する. 

- 同じ文字列に対応する頂点間の遷移は次のように定義する:
  頂点 $(i, j_1)$ から頂点 $(i, j_2)$ へは $j_2 = j_1 + 1$ のときに限りコスト $1$ で遷移できる. 
  そうでないときは遷移できない. 
- 異なる文字列に対応する頂点間の遷移は次のように定義する:
  $i_1 \neq i_2$ として頂点 $(i_1, j_1)$ から頂点 $(i_2, j_2)$ へは $i_1 < i_2$ かつ対応する文字が等しい時のみコスト $0$ で遷移できる. 
  そうでないときはコスト $1$ で遷移できる. 
- ダミーノードから各頂点へはコスト $1$ で遷移でき, 各頂点からダミーノードへはコスト $0$ で遷移できる. 

上記のコストのもと, 巡回路を形成する全ての辺のコストの和を最小化する. 

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
        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        nodes = [
            (sidx, cidx)
            for sidx, s in enumerate(self.instance)
            for cidx, _ in enumerate(s)
        ]
        order = [cpmodel.new_int_var(1, len(nodes), "") for _ in nodes]

        dummy_idx = len(nodes)
        order.append(cpmodel.new_constant(0))

        arcs = []
        costs = dict()

        for nidx, (sidx, cidx) in enumerate(nodes):
            if cidx == 0:
                arcs.append((dummy_idx, nidx, cpmodel.new_bool_var("")))
                costs[(dummy_idx, nidx)] = 1
            if cidx == len(self.instance[sidx]) - 1:
                arcs.append((nidx, dummy_idx, cpmodel.new_bool_var("")))
                costs[(nidx, dummy_idx)] = 0

        for nidx1, (sidx1, cidx1) in enumerate(nodes):
            for nidx2, (sidx2, cidx2) in enumerate(nodes):
                if sidx1 == sidx2 and cidx1 + 1 != cidx2:
                    continue
                s1 = self.instance[sidx1]
                s2 = self.instance[sidx2]
                arcs.append((nidx1, nidx2, cpmodel.new_bool_var("")))
                costs[(nidx1, nidx2)] = (
                    0 if sidx1 < sidx2 and s1[cidx1] == s2[cidx2] else 1
                )

        cpmodel.add_circuit(arcs)

        for nidx1, nidx2, v in arcs:
            if nidx2 == dummy_idx:
                continue
            cpmodel.add(order[nidx2] == order[nidx1] + 1).only_enforce_if(v)

        nidx = -1
        for s in self.instance:
            for cidx, _ in enumerate(s):
                nidx += 1
                if cidx == 0:
                    continue
                cpmodel.add(order[nidx - 1] < order[nidx])

        cpmodel.minimize(sum(costs[(nidx1, nidx2)] * v for (nidx1, nidx2, v) in arcs))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
            solution = ""
            current_node = dummy_idx
            current_char: str | None = None
            current_sidxs: set[int] = set()
            complete = False
            while True:
                for nidx1, nidx2, v in arcs:
                    if nidx1 == current_node and cpsolver.boolean_value(v):
                        if nidx2 == dummy_idx:
                            complete = True
                            break
                        sidx, cidx = nodes[nidx2]

                        if (
                            self.instance[sidx][cidx] != current_char
                            or sidx in current_sidxs
                        ):
                            solution += self.instance[sidx][cidx]
                            current_sidxs.clear()

                        current_node = nidx2
                        current_char = self.instance[sidx][cidx]
                        current_sidxs.add(sidx)
                if complete:
                    break
            self.solution = solution
        else:
            self.solution = None

        return self.solution
```
