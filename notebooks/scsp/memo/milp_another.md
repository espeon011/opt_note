In [ ]:
```python
from dataclasses import dataclass
import pyscipopt
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# バイナリ定式化と元の MILP の定式化と比較

In [ ]:
```python
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0
    relax: bool = False

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)
        vtype = "C" if self.relax else "B"

        scip: pyscipopt.Model = pyscipopt.Model()

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か
        sseq_valid = [scip.addVar(vtype=vtype) for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か
        sseq_char = [[scip.addVar(vtype=vtype) for _ in chars] for _ in sseq_valid]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か
        assign = [
            [[scip.addVar(vtype=vtype) for _ in sseq_valid] for c in s]
            for s in self.instance
        ]

        for xs in sseq_char:
            scip.addCons(sum(xs) == 1)

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                scip.addCons(sum(assign[sidx][cidx]) == 1)
                for idx, _ in enumerate(assign[sidx][cidx]):
                    scip.addCons(assign[sidx][cidx][idx] <= sseq_valid[idx])
                    scip.addCons(
                        assign[sidx][cidx][idx] <= sseq_char[idx][chars.index(c)]
                    )

        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                scip.addCons(
                    sum(
                        idx * assign[sidx][cidx - 1][idx]
                        for idx, _ in enumerate(assign[sidx][cidx - 1])
                    )
                    + 1
                    <= sum(
                        idx * assign[sidx][cidx][idx]
                        for idx, _ in enumerate(assign[sidx][cidx])
                    )
                )

        scip.setObjective(sum(sseq_valid), sense="minimize")

        if time_limit is not None:
            scip.setParam("limits/time", time_limit)
        if not log:
            scip.hideOutput()
        scip.optimize()

        self.best_bound = scip.getDualbound()

        if not self.relax and scip.getNLimSolsFound() > 0:
            solution = ""
            for valid, ssqc in zip(sseq_valid, sseq_char):
                if int(round(scip.getVal(valid))) == 1:
                    for c, sqc in zip(chars, ssqc):
                        if int(round(scip.getVal(sqc))) == 1:
                            solution += c
                            break
            self.solution = solution

        return self.solution
```

以下のインスタンスは DIDP を使ってモデルによって最適値が 62 だとわかっている.

In [ ]:
```python
scsp.util.bench(
    scsp.model.linear_scip.Model, example_filename="uniform_q26n004k015-025.txt"
)
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 72) ---
>  Sol: itgevazojgbrdkignkqfuhomlcpnibxnxyhctvqgdxobsucqovozpsviprvssxbinsnglxfp
> str1: -t-----------k-gnk--uh-m--p---xn--h-t-qg-x---------z--v------x-i-s------
> str2: i------oj-----i---qf--o-l--n-bx-x--c-v------su-q----p-vi---ss-b------xf-
> str3: --------------------u---lc--i--n-y-c------o-s---ovozp---p-----------l--p
> str4: i-gevaz--gbrd---------------------------d--b--c------sv--rv-----n-ng--f-
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 72
> best bound: 26.0
> wall time: 60.172458s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution not found ---
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: None
> best bound: 2.3850583312421074
> wall time: 60.256086s
> ```

バイナリ定式化は解なし. dual bound も非常に悪い.

# 連続緩和問題を利用して dual bound を得る

元の MILP 定式化の連続緩和モデルと今回作成したバイナリ定式化の連続緩和モデルを比較する.

In [ ]:
```python
instance01 = scsp.example.load("uniform_q26n004k015-025.txt")
```

## バイナリ定式化の連続緩和モデルの実行結果

In [ ]:
```python
Model(instance01, relax=True).solve(log=True)
```

> ```
> presolving:
> (round 1, fast)       0 del vars, 0 del conss, 0 add conss, 9156 chg bounds, 0 chg sides, 0 chg coeffs, 0 upgd conss, 0 impls, 0 clqs, 0 implints
> (round 2, fast)       0 del vars, 0 del conss, 0 add conss, 9240 chg bounds, 0 chg sides, 0 chg coeffs, 0 upgd conss, 0 impls, 0 clqs, 0 implints
>    (0.1s) symmetry computation started: requiring (bin +, int +, cont +), (fixed: bin -, int -, cont -)
>    (0.1s) no symmetry present (symcode time: 0.00)
> presolving (3 rounds: 3 fast, 1 medium, 1 exhaustive):
>  0 deleted vars, 0 deleted constraints, 0 added constraints, 9240 tightened bounds, 0 added holes, 0 changed sides, 0 changed coefficients
>  0 implications, 0 cliques, 0 implied integral variables (0 bin, 0 int, 0 cont)
> presolved problem has 9240 variables (0 bin, 0 int, 9240 cont) and 14360 constraints
>   14360 constraints of type <linear>
> Presolving Time: 0.12
> 
>  time | node  | left  |LP iter|LP it/n|mem/heur|mdpt |vars |cons |rows |cuts |sepa|confs|strbr|  dualbound   | primalbound  |  gap   | compl. 
> *17.0s|     1 |     0 | 28155 |     - |    LP  |   0 |9240 |  14k|  14k|   0 |  0 |   0 |   0 | 1.300235e+00 | 1.300235e+00 |   0.00%| unknown
>  17.0s|     1 |     0 | 28155 |     - |    98M |   0 |9240 |  14k|  14k|   0 |  0 |   0 |   0 | 1.300235e+00 | 1.300235e+00 |   0.00%| unknown
> 
> SCIP Status        : problem is solved [optimal solution found]
> Solving Time (sec) : 16.95
> Solving Nodes      : 1
> Primal Bound       : +1.30023465661643e+00 (1 solutions)
> Dual Bound         : +1.30023465661643e+00
> Gap                : 0.00 %
> ```

## MILP モデルの連続緩和モデル

In [ ]:
```python
@dataclass
class ModelMILPContinuous:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        scip: pyscipopt.Model = pyscipopt.Model()

        max_len = sum(len(s) for s in self.instance)
        seqs = [
            [scip.addVar(vtype="C", lb=0, ub=max_len - 1) for _ in s]
            for s in self.instance
        ]

        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                scip.addCons(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(self.instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(self.instance, seqs)):
                if idx1 >= idx2:
                    continue

                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            big_m = max_len
                            lt = scip.addVar(vtype="C", lb=0, ub=1)
                            gt = scip.addVar(vtype="C", lb=0, ub=1)
                            scip.addCons(lt + gt == 1)
                            scip.addCons(cvar1 + 1 <= cvar2 + max_len * (1 - lt))
                            scip.addCons(cvar1 + max_len * (1 - gt) >= cvar2 + 1)

        obj = scip.addVar(vtype="C", lb=0, ub=max_len)
        for seq in seqs:
            scip.addCons(obj >= seq[-1])
        scip.setObjective(obj + 1, sense="minimize")

        if time_limit is not None:
            scip.setParam("limits/time", time_limit)
        if not log:
            scip.hideOutput()
        scip.optimize()

        self.best_bound = scip.getDualbound()

        return self.solution
```

In [ ]:
```python
ModelMILPContinuous(instance01).solve(log=True)
```

> ```
> presolving:
> (round 1, fast)       2527 del vars, 2527 del conss, 0 add conss, 82 chg bounds, 0 chg sides, 0 chg coeffs, 0 upgd conss, 0 impls, 0 clqs, 0 implints
> (round 2, fast)       2527 del vars, 2527 del conss, 0 add conss, 4391 chg bounds, 0 chg sides, 0 chg coeffs, 0 upgd conss, 0 impls, 0 clqs, 0 implints
> (round 3, fast)       2527 del vars, 2527 del conss, 0 add conss, 4494 chg bounds, 0 chg sides, 0 chg coeffs, 0 upgd conss, 0 impls, 0 clqs, 0 implints
> (round 4, exhaustive) 2527 del vars, 5054 del conss, 0 add conss, 4494 chg bounds, 0 chg sides, 0 chg coeffs, 0 upgd conss, 0 impls, 0 clqs, 0 implints
>    (0.0s) symmetry computation started: requiring (bin +, int +, cont +), (fixed: bin -, int -, cont -)
>    (0.1s) no symmetry present (symcode time: 0.00)
> presolving (5 rounds: 5 fast, 2 medium, 2 exhaustive):
>  2527 deleted vars, 5054 deleted constraints, 0 added constraints, 4494 tightened bounds, 0 added holes, 0 changed sides, 0 changed coefficients
>  0 implications, 0 cliques, 0 implied integral variables (0 bin, 0 int, 0 cont)
> presolved problem has 2612 variables (0 bin, 0 int, 2612 cont) and 2611 constraints
>    2611 constraints of type <linear>
> Presolving Time: 0.05
> 
>  time | node  | left  |LP iter|LP it/n|mem/heur|mdpt |vars |cons |rows |cuts |sepa|confs|strbr|  dualbound   | primalbound  |  gap   | compl. 
> * 0.1s|     1 |     0 |    83 |     - |    LP  |   0 |2612 |2611 |2611 |   0 |  0 |   0 |   0 | 2.500000e+01 | 2.500000e+01 |   0.00%| unknown
>   0.1s|     1 |     0 |    83 |     - |    47M |   0 |2612 |2611 |2611 |   0 |  0 |   0 |   0 | 2.500000e+01 | 2.500000e+01 |   0.00%| unknown
> 
> SCIP Status        : problem is solved [optimal solution found]
> Solving Time (sec) : 0.06
> Solving Nodes      : 1
> Primal Bound       : +2.50000000000000e+01 (1 solutions)
> Dual Bound         : +2.50000000000000e+01
> Gap                : 0.00 %
> ```

バイナリ定式化は筋が悪そう.
連続緩和した問題も解くのに 16 秒近くかかっており, 目的関数値はバウンドとして使えるレベルのものではない.

元の MILP 定式化の連続緩和はすぐ解けてバウンド値もバイナリ定式化のものより良いが,
元々も MILP モデルのバウンドと同じくらいの値なのでわざわざ連続緩和する必要がない.
