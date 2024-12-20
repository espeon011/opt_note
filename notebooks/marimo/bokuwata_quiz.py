# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "ortools==9.11.4210",
#     "polars==1.17.1",
# ]
# ///

import marimo

__generated_with = "0.10.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# プリンを食べた嘘つきは誰？""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        <center>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/n8i0RpDbWMk" title="【論理クイズ】プリンを食べた嘘つきは誰？【激ムズ】" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </center>

        ## 証言

        - A「A と D は食べてない」
        - B「E は食べてない」
        - C「C と B は食べてない」
        - D「A と C は食べてない」
        - E「D と E は食べてない」
        - 探偵「嘘つきは 1 人」「私は食べてない」
        - 主人公「私は食べてない」「このチャンネルは面白い」

        ## 論理クイズのルール

        - このクイズの登場人物は「正直者」か「嘘つき」のどちらか
        - 正直者は本当のことしか言わない
        - 嘘つきは嘘のことしか言わない
        """
    )
    return


@app.cell
def _():
    from ortools.sat.python import cp_model
    import polars as pl

    _ = pl.Config.set_tbl_rows(16)
    return cp_model, pl


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    class Model:
        def __init__(
            self,
            c_one: bool = False,
            ex_bokuwata: bool = False,
            not_ex_bokuwata: bool = False,
        ):
            self.model = cp_model.CpModel()

            self.suspects = ["A", "B", "C", "D", "E", "探偵", "主人公"]
            self.liars = {
                _s: self.model.new_bool_var(f"{_s}_is_liar")
                for _s in self.suspects
            }
            self.culprits = {
                _s: self.model.new_bool_var(f"{_s}_is_culprit")
                for _s in self.suspects
            }

            # A「A と D は食べてない」
            self.model.add(
                self.culprits["A"] + self.culprits["D"] == 0
            ).only_enforce_if(self.liars["A"].negated())
            self.model.add(
                self.culprits["A"] + self.culprits["D"] > 0
            ).only_enforce_if(self.liars["A"])

            # B「E は食べてない」
            self.model.add(self.culprits["E"] == 0).only_enforce_if(
                self.liars["B"].negated()
            )
            self.model.add(self.culprits["E"] == 1).only_enforce_if(
                self.liars["B"]
            )

            # C「C と B は食べてない」
            self.model.add(
                self.culprits["C"] + self.culprits["B"] == 0
            ).only_enforce_if(self.liars["C"].negated())
            self.model.add(
                self.culprits["C"] + self.culprits["B"] > 0
            ).only_enforce_if(self.liars["C"])

            # D「A と C は食べてない」
            self.model.add(
                self.culprits["A"] + self.culprits["C"] == 0
            ).only_enforce_if(self.liars["D"].negated())
            self.model.add(
                self.culprits["A"] + self.culprits["C"] > 0
            ).only_enforce_if(self.liars["D"])

            # E「D と E は食べてない」
            self.model.add(
                self.culprits["D"] + self.culprits["E"] == 0
            ).only_enforce_if(self.liars["E"].negated())
            self.model.add(
                self.culprits["D"] + self.culprits["E"] > 0
            ).only_enforce_if(self.liars["E"])

            # 探偵「嘘つきは 1 人」「私は食べてない」
            self.model.add(self.culprits["探偵"] == 0).only_enforce_if(
                self.liars["探偵"].negated()
            )
            self.model.add(self.culprits["探偵"] == 1).only_enforce_if(
                self.liars["探偵"]
            )
            self.model.add(
                sum(self.liars[_s] for _s in self.suspects) == 1
            ).only_enforce_if(self.liars["探偵"].negated())
            self.model.add(
                sum(self.liars[_s] for _s in self.suspects) != 1
            ).only_enforce_if(self.liars["探偵"])

            # 主人公「私は食べてない」「このチャンネルは面白い」
            self.model.add(self.culprits["主人公"] == 0).only_enforce_if(
                self.liars["主人公"].negated()
            )
            self.model.add(self.culprits["主人公"] == 1).only_enforce_if(
                self.liars["主人公"]
            )

            # 追加: 犯人は 1 人
            if c_one:
                self.model.add_exactly_one(self.culprits.values())
            # 追加: ぼくわたチャンネルは面白い
            if ex_bokuwata:
                self.model.add(self.liars["主人公"] == 0)
            # 追加: ぼくわたチャンネルは面白い
            if not_ex_bokuwata:
                self.model.add(self.liars["主人公"] == 1)

        def solve(self):
            self.solver = cp_model.CpSolver()
            self.solution_printer = VarArraySolutionPrinter(
                self.suspects, self.liars, self.culprits
            )
            self.solver.parameters.enumerate_all_solutions = True
            return self.solver.solve(self.model, self.solution_printer)
    return (Model,)


@app.cell
def _(cp_model, pl):
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, suspects, liars, culprits):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__suspects = suspects
            self.__liars = liars
            self.__culprits = culprits
            self.__solution_count = 0
            # self.__dataframe = pl.DataFrame({_s: [] for _s in self.__suspects})
            self.__dataframe = pl.DataFrame()

        def on_solution_callback(self):
            self.__solution_count = self.__solution_count + 1
            _add = {_s: [] for _s in self.__suspects}
            for _s in self.__suspects:
                _result_string = "-"
                if (
                    self.value(self.__liars[_s]) + self.value(self.__culprits[_s])
                    > 0
                ):
                    _result_string = ""
                    _result_string += (
                        f"{"嘘つき" if self.value(self.__liars[_s]) == 1 else ""}"
                    )
                    _result_string += "/"
                    _result_string += (
                        f"{"有罪" if self.value(self.__culprits[_s]) == 1 else ""}"
                    )
                    _result_string = _result_string.strip("/")
                _add[_s].append(_result_string)
                # print(f"{_s}:{_result_string}", end=" ")
            # print()
            self.__dataframe = pl.concat([self.__dataframe, pl.DataFrame(_add)])

        @property
        def solution_count(self):
            return self.__solution_count

        @property
        def dataframe(self):
            return self.__dataframe
    return (VarArraySolutionPrinter,)


@app.cell
def _(cp_model):
    statuses = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
        cp_model.UNKNOWN: "UNKNOWN",
    }
    return (statuses,)


@app.cell
def _(Model, mo, statuses):
    model = Model()
    status = model.solve()

    mo.md(f"""
    ## 計算結果

    - Number of solutions found: {model.solution_printer.solution_count}
    - Status = {statuses[status]}
    - Time = {model.solver.wall_time}
    """)
    return model, status


@app.cell
def _(model):
    model.solution_printer.dataframe
    return


@app.cell(hide_code=True)
def _(mo):
    switch_c_one = mo.ui.switch(label="犯人は 1 人とする", value=True)
    switch_exciting_bokuwata = mo.ui.switch(
        label="ぼくわたチャンネルは面白い(=主人公は正直者)"
    )
    switch_not_exciting_bokuwata = mo.ui.switch(
        label="ぼくわたチャンネルは面白くない(=主人公は嘘つき)"
    )

    mo.vstack(
        [
            mo.md("## 追加条件"),
            switch_c_one,
            switch_exciting_bokuwata,
            switch_not_exciting_bokuwata,
        ]
    )
    return (
        switch_c_one,
        switch_exciting_bokuwata,
        switch_not_exciting_bokuwata,
    )


@app.cell
def _(
    Model,
    mo,
    statuses,
    switch_c_one,
    switch_exciting_bokuwata,
    switch_not_exciting_bokuwata,
):
    model2 = Model(
        switch_c_one.value,
        switch_exciting_bokuwata.value,
        switch_not_exciting_bokuwata.value,
    )
    status2 = model2.solve()

    mo.md(f"""
    ## 計算結果

    - Number of solutions found: {model2.solution_printer.solution_count}
    - Status = {statuses[status2]}
    - Time = {model2.solver.wall_time}
    """)
    return model2, status2


@app.cell
def _(model2):
    model2.solution_printer.dataframe
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 人力で解く方法

        犯人は 1 人だけとする. 

        B を嘘つきと仮定すると E はプリンを食べたことになる. 
        E は自分は食べてないと主張しているので嘘つきになる. 
        B も E も嘘つきであるため嘘つきは 1 人だけと主張する探偵も嘘つきになり, 探偵も犯人になる. 犯人は 1 人のため矛盾. 
        よって B は正直者. E は犯人ではない. 

        E を嘘つきとする. このとき D か E のどちらか一方はプリンを食べたことになる. 
        上の結果より E は食べていないので D が犯人となる. 
        A は A も D もプリンを食べていないと主張しているため嘘つきとなる. 
        E も A も嘘つきとなり, 探偵も嘘つきとなることから探偵も犯人となるが, D と探偵が犯人となるため矛盾. 
        よって E は正直者. 特に D は犯人ではない. 

        A を嘘つきとする. このとき A と D のどちらか一方はプリンを食べたことになる. 
        上の結果より D は食べていないので A が犯人となる. 
        このとき A も C もプリンを食べていないと主張する D も嘘つきとなる. 
        そして嘘つきが 1 人であると主張する探偵も嘘つきになり, 探偵も犯人となり矛盾する. 
        よって A は正直者. 特に A は犯人ではない. 

        D を嘘つきとする. このとき A と C のどちらか一方はプリンを食べたことになる. 
        上の結果より A は犯人ではないので C が犯人である. 
        C 自身も C が犯人でないと主張しているため, C も嘘つきとなる. 
        嘘つきが 2 人以上いるので探偵も嘘つきとなり, 探偵も犯人となり, 矛盾する. 
        よって D は正直者. 特に C は犯人ではない. 

        探偵を嘘つきとする. 
        このとき探偵が犯人であり, 嘘つきは 2 人以上存在する. 
        主人公が嘘つきだとすると 2 人目の犯人になってしまうため, 2 人目の嘘つきは C となる. 
        C が嘘つきのため C と B のどちらかは犯人であるが, 2 人目の犯人になってしまうため矛盾. 
        よって探偵は正直者. 特に探偵は犯人ではない. 

        ここまでで確定していないのは

        - C が嘘つきか正直者か
        - B が犯人かどうか
        - 主人公が嘘つきかどうか
        - 主人公が犯人かどうか

        で C と主人公以外は全員正直者で確定しており, 
        B と主人公以外は犯人でないことが確定している. 

        残りの問題については

        - 主人公が嘘つき ⇔ 主人公が犯人
        - C が嘘つき ⇔ B が犯人

        で, 探偵が正直者であり, 嘘つきが 1 人しかいないことから

        | ケース | 主人公 | B | C |
        | :--- | ---: | ---: | ---: |
        | ケース 1 | 嘘つき/犯人| - | - |
        | ケース 2 | - | 犯人 | 嘘つき |

        の 2 通りしかない.

        どちらになるかは, ぼくわたチャンネルが面白いかどうかに依存し, 

        - ぼくわたチャンネルが面白い場合, 主人公は正直者で無実のケース 2
        - ぼくわたチャンネルが面白くない場合, 主人公は嘘つきで犯人のケース 1

        となる.
        """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
