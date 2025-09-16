In [ ]:
```python
import opt_note.scsp as scsp
import pyscipopt
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# バイナリ定式化と比較

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = sum(len(s) for s in instance)

        scip: pyscipopt.Model = pyscipopt.Model()

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か
        sseq_valid = [scip.addVar(vtype="B") for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か
        sseq_char = [[scip.addVar(vtype="B") for _ in chars] for _ in sseq_valid]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か
        assign = [[[scip.addVar(vtype="B") for _ in sseq_valid] for c in s] for s in instance]

        for xs in sseq_char:
            scip.addCons(sum(xs) == 1)

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                scip.addCons(sum(assign[sidx][cidx]) == 1)
                for idx, _ in enumerate(assign[sidx][cidx]):
                    scip.addCons(assign[sidx][cidx][idx] <= sseq_valid[idx])
                    scip.addCons(assign[sidx][cidx][idx] <= sseq_char[idx][chars.index(c)])

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                scip.addCons(
                    sum(idx * assign[sidx][cidx - 1][idx] for idx, _ in enumerate(assign[sidx][cidx - 1])) + 1
                    <= sum(idx * assign[sidx][cidx][idx] for idx, _ in enumerate(assign[sidx][cidx]))
                )

        scip.setObjective(sum(sseq_valid), sense="minimize")

        self.instance = instance
        self.chars = chars
        self.scip = scip
        self.sseq_valid = sseq_valid
        self.sseq_char = sseq_char

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        if time_limit is not None:
            self.scip.setParam("limits/time", time_limit)
        if not log:
            self.scip.hideOutput()
        self.scip.optimize()

        return self

    def to_solution(self) -> str | None:
        if self.scip.getNLimSolsFound() == 0:
            return None

        solution = ""
        for valid, ssqc in zip(self.sseq_valid, self.sseq_char):
            if int(round(self.scip.getVal(valid))) == 1:
                for c, sqc in zip(self.chars, ssqc):
                    if int(round(self.scip.getVal(sqc))) == 1:
                        solution += c
                        break

        return solution
```

連続緩和モデルも作成.

In [ ]:
```python
class ModelContinuous:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = sum(len(s) for s in instance)

        scip: pyscipopt.Model = pyscipopt.Model()

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か
        sseq_valid = [scip.addVar(vtype="C", lb=0, ub=1) for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か
        sseq_char = [[scip.addVar(vtype="C", lb=0, ub=1) for _ in chars] for _ in sseq_valid]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か
        assign = [[[scip.addVar(vtype="C", lb=0, ub=1) for _ in sseq_valid] for c in s] for s in instance]

        for xs in sseq_char:
            scip.addCons(sum(xs) == 1)

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                scip.addCons(sum(assign[sidx][cidx]) == 1)
                for idx, _ in enumerate(assign[sidx][cidx]):
                    scip.addCons(assign[sidx][cidx][idx] <= sseq_valid[idx])
                    scip.addCons(assign[sidx][cidx][idx] <= sseq_char[idx][chars.index(c)])

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                scip.addCons(
                    sum(idx * assign[sidx][cidx - 1][idx] for idx, _ in enumerate(assign[sidx][cidx - 1])) + 1
                    <= sum(idx * assign[sidx][cidx][idx] for idx, _ in enumerate(assign[sidx][cidx]))
                )

        scip.setObjective(sum(sseq_valid), sense="minimize")

        self.instance = instance
        self.chars = chars
        self.scip = scip
        self.sseq_valid = sseq_valid
        self.sseq_char = sseq_char

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        if time_limit is not None:
            self.scip.setParam("limits/time", time_limit)
        if not log:
            self.scip.hideOutput()
        self.scip.optimize()

        return self
```

In [ ]:
```python
def bench1(instance: list[str]) -> None:
    model = scsp.model.linear_scip.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.scip.getStatus()}")
    print(f"best bound: {model.scip.getDualbound()}")
```

In [ ]:
```python
def bench2(instance: list[str]) -> None:
    model = Model(instance).solve(time_limit=60)
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.scip.getStatus()}")
    print(f"best bound: {model.scip.getDualbound()}")
```

以下のインスタンスは DIDP を使ってモデルによって最適値が 62 だとわかっている.

In [ ]:
```python
instance01 = scsp.example.load("uniform_q26n004k015-025.txt")
```

In [ ]:
```python
bench1(instance01)
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 70) ---
>  Sol: itkgojniqfeokulvahmcnzgpibxxrndycvhodstoqgubcvsoxzvqpzprvxininsgslpbxf
> str1: -tkg--n-----ku---hm----p--x--n----h---t-qg------xzv------xi---s-------
> str2: i---oj-iqf-o--l-----n----bxx----cv---s----u--------qp---v-i---s-s--bxf
> str3: -------------ul----c----i----n-yc--o-s-o-----v-o-z--p-p----------lp---
> str4: i--g------e----va----zg--b--r-d-----d------bc-s---v----rv--n-n-g-----f
> 
> solution is feasible: True
> solution status: timelimit
> best bound: 26.0
> ```

In [ ]:
```python
bench2(instance01)
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
> solution status: timelimit
> best bound: 2.0238481492365534
> ```

連続緩和して解くと...?

In [ ]:
```python
_model = ModelContinuous(instance01)
_model.solve()

print(f"solution status: {_model.scip.getStatus()}")
print(f"best bound: {_model.scip.getDualbound()}")
```

> ```
> solution status: optimal
> best bound: 1.3002346566164258
> ```

バイナリ定式化は筋が悪そう.
連続緩和した問題も解くのに 16 秒近くかかっており, 目的関数値はバウンドとして使えるレベルのものではない.
