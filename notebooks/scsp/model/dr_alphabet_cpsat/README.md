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

- $x^{(i)}_j \in \mathbb{Z}$: 文字列 $s_i$ の $j$ 番目の文字 $c^{(i)}_j$ が解 $\mathrm{sol}$ において何番目に位置するか
- $u_l \in \lbrace 0, 1 \rbrace \ (l = 1, \dots, kq)$: $\mathrm{sol}$ の $l$ 番目の文字 $c_l$ が使われたか否か

**制約条件**

- $x^{(i)}_{j} < x^{(i)}_{j + 1} \ (j = 1, \dots, |s_i| - 1)$
- $u_{x^{(i)}_{j}} = 1$

**目的関数**

- minimize $\sum_{l = 1}^{kq} u_l$

## Python Code

```python
from dataclasses import dataclass
from ortools.sat.python import cp_model
from ..alphabet import Model as ModelAlphabet


@dataclass
class ModelReduction:
    instance: list[str]
    template: str
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, time_limit: int | None = 60, log: bool = False) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance + [self.template])))))

        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        valids = [cpmodel.new_bool_var("") for _ in self.template]
        cvars = [
            [
                cpmodel.new_int_var_from_domain(
                    cp_model.Domain.from_values(
                        [idx for idx, solc in enumerate(self.template) if c == solc]
                    ),
                    "",
                )
                for c in s
            ]
            for s in self.instance
        ]

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(cvars[sidx][cidx - 1] < cvars[sidx][cidx])

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                cpmodel.add_element(cvars[sidx][cidx], valids, 1)

        cpmodel.minimize(sum(valids))
        # cpmodel.minimize(cp_model.LinearExpr.sum(valids))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit

        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            solution = ""
            for idx, valid in enumerate(valids):
                if cpsolver.boolean_value(valid):
                    solution += chars[idx % len(chars)]
            self.solution = solution
        else:
            self.solution = None

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
