# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nbformat==5.10.4",
#     "pyscipopt==5.5.0",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    import pyscipopt


@app.cell
def _():
    import marimo as mo
    import nbformat
    import util
    return mo, util


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# MILP 定式化 (SCIP)""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    数理最適化モデルを用いて SCSP を解く. 以下のように定式化する. 

    **決定変数**

    - $x_{i,j} \in \mathbb{N} \ (\forall i \in \{ 1, \dots, n \}, \ \forall j \in \{ 1, \dots, |s_i| \})$: $i$ 番目の文字列の $j$ 番目の文字が解において何番目に対応するか. 

    **制約条件**

    - $x_{i,j} < x_{i,j+1} \ (\forall i \in \{ 1, \dots, n \}, \ \forall j \in \{ 1, \dots, |s_i| - 1 \})$
    - $i_1, i_2 \in \{ 1, \dots, n\} \ (i_1 \ne i_2)$ と $j_1 \in \{ 1, \dots, |s_{i_1}| \}, \ j_2 \in \{ 1, \dots, |s_{i_2}| \}$ に対し,
      $s_1[j_1] \ne s_2[j_2]$ ならば $x_{i_1, j_1} \ne x_{i_2, j_2}$. 

    **目的関数**

    - minimize $\max_{i = 1, \dots, n} x_{i, |s_i|}$
    """
    )
    return


@app.class_definition
class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)

        scip: pyscipopt.Model = pyscipopt.Model()
    
        seqs = [
            [
                scip.addVar(vtype="I", lb=0, ub=max_len - 1)
                for _ in s
            ]
            for s in instance
        ]
        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                scip.addCons(seq[idx - 1] + 1 <= seq[idx])
    
        for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
                if idx1 >= idx2:
                    continue
    
                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            lt = scip.addVar(vtype="B")
                            gt = scip.addVar(vtype="B")
                            scip.addCons(lt + gt == 1)
                            scip.addConsIndicator(cvar1 + 1 <= cvar2, binvar=lt)
                            scip.addConsIndicator(cvar1 >= cvar2 + 1, binvar=gt)
                            
        obj = scip.addVar(vtype="C", lb=0, ub=max_len)
        for seq in seqs:
            scip.addCons(obj >= seq[-1])
        scip.setObjective(obj + 1, sense="minimize")

        self.instance = instance
        self.scip = scip
        self.seqs = seqs

    def solve(self, time_limit: int | None = 60) -> "Model":
        if time_limit is not None:
            self.scip.setParam("limits/time", time_limit)
        self.scip.optimize()

        return self

    def to_solution(self) -> str | None:
        if self.scip.getNLimSolsFound() == 0:
            return None

        objval = int(round(self.scip.getObjVal()))
        sol_char_idx = 0
        solution = ""
        while sol_char_idx <= objval:
            found = False
            for idx, (s, seq) in enumerate(zip(self.instance, self.seqs)):
                for c_idx, cvar in enumerate(seq):
                    if int(round(self.scip.getVal(cvar))) == sol_char_idx:
                        solution += s[c_idx]
                        found = True
                        sol_char_idx += 1
                if found:
                    break
            if not found:
                sol_char_idx += 1
    
        return solution


@app.function
def solve(instance: list[str], time_limit: int | None = 60) -> str | None:
    return Model(instance).solve(time_limit).to_solution()


@app.cell
def _(util):
    instance_01 = util.parse("uniform_q26n004k015-025.txt")
    solution_01 = solve(instance_01)
    return instance_01, solution_01


@app.cell
def _(instance_01, solution_01, util):
    _instance = instance_01
    _solution = solution_01

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _(util):
    instance_02 = util.parse("uniform_q26n008k015-025.txt")
    solution_02 = solve(instance_02)
    return instance_02, solution_02


@app.cell
def _(instance_02, solution_02, util):
    _instance = instance_02
    _solution = solution_02

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _(util):
    instance_03 = util.parse("uniform_q26n016k015-025.txt")
    solution_03 = solve(instance_03)
    return instance_03, solution_03


@app.cell
def _(instance_03, solution_03, util):
    _instance = instance_03
    _solution = solution_03

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _(util):
    instance_04 = util.parse("uniform_q05n010k010-010.txt")
    solution_04 = solve(instance_04)
    return instance_04, solution_04


@app.cell
def _(instance_04, solution_04, util):
    _instance = instance_04
    _solution = solution_04

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


@app.cell
def _(util):
    instance_05 = util.parse("uniform_q05n050k010-010.txt")
    solution_05 = solve(instance_05)
    return instance_05, solution_05


@app.cell
def _(instance_05, solution_05, util):
    _instance = instance_05
    _solution = solution_05

    util.show(_instance)
    if _solution is not None:
        util.show(_instance, _solution)
        print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
    else:
        print("--- Solution not found ---")
    return


if __name__ == "__main__":
    app.run()
