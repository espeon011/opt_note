# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "highspy==1.11.0",
#     "hexaly>=14.0.20250915",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
#     "pyscipopt==5.6.0",
# ]
# [[tool.uv.index]]
# name ="hexaly"
# url = "https://pip.hexaly.com"
# explict = true
# [tool.uv.sources]
# hexaly = { index = "hexaly" }
# ///

import marimo

__generated_with = "0.15.3"
app = marimo.App(width="medium")

with app.setup:
    import opt_note.scsp as scsp
    from ortools.sat.python import cp_model


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# `AUTOMATON_CPSAT` モデルの改良""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    `Alphabet` アルゴリズムで求めた巨大な共通超配列の部分列の中から最短な共通超配列を見つける方針. 

    ただし `Alphabet` アルゴリズムの部分列には本当の最短共通超配列は存在しない場合がある. 
    例えば `ba`, `cb` の最短共通超配列は `cba` だが `Alphabet` アルゴリズムで構築した解は `abcabc` であり, この中から最短な共通超配列を探すと `bcab` のようになってしまう. 
    これは `Alphabet` アルゴリズムにおいてアルファベットを並べる順序が固定されているからであり, アルファベットの並びをブロックごとに可変にしたら改善するんじゃないかと考えた. 

    ただしアルファベットの並びを可変にすれば最適解を実行可能領域に含むようになるかは証明していない. 
    従って改良モデルにおける dual bound は (あくまで最初に用意した大きな配列の部分配列の中での dual bound なため) 実際には最適解より大きくなってしまう可能性がある. 
    """
    )
    return


@app.class_definition
class Model:
    def __init__(self, instance: list[str], perm: bool = False):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars) - 1, name="") for _ in range(max_len)
        ]
        valids = [cpmodel.new_bool_var("") for _ in cvars]
        transition_expressions = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="") for _ in range(max_len)
        ]

        # 初期解としてアルファベットアルゴリズムを設定
        for valid in valids:
            cpmodel.add_hint(valid, 1)
        for idx, cvar in enumerate(cvars):
            cpmodel.add_hint(cvar, idx % len(chars))
        for texp in transition_expressions:
            cpmodel.add_hint(texp, idx % len(chars) + 1)

        if perm:
            for t in range(max(len(s) for s in instance)):
                cpmodel.add_all_different(cvars[t * len(chars) : (t + 1) * len(chars)])
        else:
            for idx, cvar in enumerate(cvars):
                cpmodel.add(cvar == idx % len(chars))

        for cvar, valid, texp in zip(cvars, valids, transition_expressions):
            cpmodel.add(texp == 0).only_enforce_if(~valid)
            cpmodel.add(texp == cvar + 1).only_enforce_if(valid)

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
                transition_expressions=transition_expressions,
                starting_state=0,
                final_states=[len(s)],
                transition_triples=transition_triples,
            )

        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars
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
        for cvar, valid in zip(self.cvars, self.valids):
            if self.cpsolver.boolean_value(valid):
                cidx = self.cpsolver.value(cvar)
                solution += self.chars[cidx]

        return solution


@app.function
def bench1(instance: list[str]) -> None:
    model = scsp.model.automaton_cpsat.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")


@app.function
def bench2(instance: list[str], perm: bool) -> None:
    model = Model(instance, perm).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    最初に示した例で計算してみよう. 
    `ba`, `cb` に対する最短共通超配列を `AUTOMATON_CPSAT` モデルで求めると最適解 (の 1 つ) は `cba` だとわかる. 
    """
    )
    return


@app.cell
def _():
    bench1(["ba", "cb"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""一方順番を固定した改良法だとこの最適解は出ない. """)
    return


@app.cell
def _():
    bench2(["ba", "cb"], perm=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""アルファベットの順番を可変にすると元の最適解が出るようになる. """)
    return


@app.cell
def _():
    bench2(["ba", "cb"], perm=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## ベンチマーク""")
    return


@app.cell
def _():
    instance01 = scsp.example.load("uniform_q26n004k015-025.txt")
    return (instance01,)


@app.cell
def _(instance01):
    bench1(instance01)
    return


@app.cell
def _(instance01):
    bench2(instance01, perm=False)
    return


@app.cell
def _(instance01):
    bench2(instance01, perm=True)
    return


@app.cell
def _():
    instance02 = scsp.example.load("uniform_q26n008k015-025.txt")
    return (instance02,)


@app.cell
def _(instance02):
    bench1(instance02)
    return


@app.cell
def _(instance02):
    bench2(instance02, perm=False)
    return


@app.cell
def _(instance02):
    bench2(instance02, perm=True)
    return


@app.cell
def _():
    instance03 = scsp.example.load("uniform_q26n016k015-025.txt")
    return (instance03,)


@app.cell
def _(instance03):
    bench1(instance03)
    return


@app.cell
def _(instance03):
    bench2(instance03, perm=False)
    return


@app.cell
def _(instance03):
    bench2(instance03, perm=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""アルファベットの順番を可変にすると解が悪化した. """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## ログを見よう""")
    return


@app.cell
def _(instance01):
    _model = Model(instance01)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance02):
    _model = Model(instance02)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _(instance03):
    _model = Model(instance03)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _():
    instance04 = scsp.example.load("uniform_q05n010k010-010.txt")
    return (instance04,)


@app.cell
def _(instance04):
    _model = Model(instance04)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _():
    instance05 = scsp.example.load("uniform_q05n050k010-010.txt")
    return (instance05,)


@app.cell
def _(instance05):
    _model = Model(instance05)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _():
    instance06 = scsp.example.load("nucleotide_n010k010.txt")
    return (instance06,)


@app.cell
def _(instance06):
    _model = Model(instance06)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _():
    instance07 = scsp.example.load("nucleotide_n050k050.txt")
    return (instance07,)


@app.cell
def _(instance07):
    _model = Model(instance07)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _():
    instance08 = scsp.example.load("protein_n010k010.txt")
    return (instance08,)


@app.cell
def _(instance08):
    _model = Model(instance08)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell
def _():
    instance09 = scsp.example.load("protein_n050k050.txt")
    return (instance09,)


@app.cell
def _(instance09):
    _model = Model(instance09)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    性能自体は悪くないかも. 
    例えば `protein_n050k050.txt` で 497 は `WMM_HEXALY` を 1 だけ上回っている. 

    一方で巨大なインスタンスでは presolve に時間がかかりすぎていて初期解をちょっと改善して終わりみたいになったりする. 
    DNA 配列の長さ 100 を 100 個用意して計算してみると... 
    """
    )
    return


@app.cell
def _():
    instance_large1 = scsp.example.load("nucleotide_n100k100.txt")
    return (instance_large1,)


@app.cell
def _(instance_large1):
    _model = Model(instance_large1)
    _model.solve(time_limit=120, log=True)
    _model.to_solution()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""presolve が終わらなかった... """)
    return


if __name__ == "__main__":
    app.run()
