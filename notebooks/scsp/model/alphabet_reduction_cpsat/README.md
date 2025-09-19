# アルファベットアルゴリズムで作成したものを削り出す

- 計算量: ?
- 近似精度: $q$

アルファベットアルゴリズムで求めた解を $\mathrm{sol} = c_1 c_2 \dots, c_{kq}$ とする. 
この解の部分配列のなかで問題インスタンスの文字列全ての共通超配列であるものの中で最短のものを求める. 

ただしアルファベットアルゴリズムで求めた解の部分列には本当の最短共通超配列は存在しない場合がある. 
たとえば `ba`, `cb` の最短共通超配列は `cba` だが,
アルファベットアルゴリズムで構築した解 `abcabc` の部分配列の中で最短な共通超配列は例えば `bcab` である. 

**表記**

- $\Sigma = \lbrace \sigma_1, \dots, \sigma_q \rbrace$: 文字集合
- $S = \lbrace s_1, \dots, s_n \rbrace$: 問題インスタンス
- $s_i = c^{(i)}_0 \dots c^{(i)}_{|s_i|}$: 各文字列
- $k = \max_{i=1, \dots, n} |s_i|$: 文字列長の最大値

**決定変数**

- $x^{(i)}_j \in mathbb{Z}$: 文字列 $s_i$ の $j$ 番目の文字 $c^{(i)}_j$ が解 $\mathrm{sol}$ において何番目に位置するか
- $u_l \in \lbrace 0, 1 \rbrace \ (l = 1, \dots, kq)$: $\mathrm{sol}$ の $l$ 番目の文字 $c_l$ が使われたか否か

**制約条件**

- $x^{(i)}_{j} < x^{(i)}_{j + 1} \ (j = 1, \dots, |s_i| - 1)$
- $u_{x^{(i)}_{j}} = 1$

**目的関数**

- minimize $\sum_{l = 1}^{kq} u_l$

## Python Code

```python
from ortools.sat.python import cp_model


class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        valids = [cpmodel.new_bool_var("") for _ in range(max_len)]
        cvars = [
            [cpmodel.new_int_var(0, max(len(s) for s in instance) - 1, "") for c in s]
            for s in instance
        ]

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(
                    len(chars) * cvars[sidx][cidx - 1] + chars.index(s[cidx - 1])
                    < len(chars) * cvars[sidx][cidx] + chars.index(s[cidx])
                )

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                cpmodel.add_element(
                    len(chars) * cvars[sidx][cidx] + chars.index(c),
                    valids,
                    1,
                )

        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.valids = valids
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
        for idx, valid in enumerate(self.valids):
            if self.cpsolver.boolean_value(valid):
                solution += self.chars[idx % len(self.chars)]

        return solution
```
