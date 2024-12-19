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

        - A「AとDは食べてない」
        - B「Eは食べてない」
        - C「CとEは食べてない」
        - D「AとCは食べてない」
        - E「DとEは食べてない」
        - 探偵「嘘つきは1人」「私は食べてない」
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
            detective_is_not_liar: bool = False,
            detective_is_liar: bool = False,
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

            # B「Eは食べてない」
            self.model.add(self.culprits["E"] == 0).only_enforce_if(
                self.liars["B"].negated()
            )
            self.model.add(self.culprits["E"] == 1).only_enforce_if(
                self.liars["B"]
            )

            # C「CとEは食べてない」
            self.model.add(
                self.culprits["C"] + self.culprits["E"] == 0
            ).only_enforce_if(self.liars["C"].negated())
            self.model.add(
                self.culprits["C"] + self.culprits["E"] > 0
            ).only_enforce_if(self.liars["C"])

            # D「AとCは食べてない」
            self.model.add(
                self.culprits["A"] + self.culprits["C"] == 0
            ).only_enforce_if(self.liars["D"].negated())
            self.model.add(
                self.culprits["A"] + self.culprits["C"] > 0
            ).only_enforce_if(self.liars["D"])

            # E「DとEは食べてない」
            self.model.add(
                self.culprits["D"] + self.culprits["E"] == 0
            ).only_enforce_if(self.liars["E"].negated())
            self.model.add(
                self.culprits["D"] + self.culprits["E"] > 0
            ).only_enforce_if(self.liars["E"])

            # 探偵「嘘つきは1人」「私は食べてない」
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
            # 追加: 探偵は正直者
            if detective_is_not_liar:
                self.model.add(self.liars["探偵"] == 0)
            # 追加: 探偵は嘘つき
            if detective_is_liar:
                self.model.add(self.liars["探偵"] == 1)

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
                _result_string = ""
                _result_string += f"{"正直者" if self.value(self.__liars[_s]) == 0 else "嘘つき"}"
                _result_string += "/"
                _result_string += (
                    f"{"無罪" if self.value(self.__culprits[_s]) == 0 else "有罪"}"
                )
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
    switch_c_one = mo.ui.switch(label="犯人は 1 人とする")
    switch_exciting_bokuwata = mo.ui.switch(
        label="ぼくわたチャンネルは面白い(=主人公は正直者)"
    )
    switch_not_exciting_bokuwata = mo.ui.switch(
        label="ぼくわたチャンネルは面白くない(=主人公は嘘つき)"
    )
    switch_detective_is_not_liar = mo.ui.switch(label="探偵は正直者")
    switch_detective_is_liar = mo.ui.switch(label="探偵は嘘つき")

    mo.vstack(
        [
            mo.md("## 追加条件"),
            switch_c_one,
            switch_exciting_bokuwata,
            switch_not_exciting_bokuwata,
            switch_detective_is_not_liar,
            switch_detective_is_liar,
        ]
    )
    return (
        switch_c_one,
        switch_detective_is_liar,
        switch_detective_is_not_liar,
        switch_exciting_bokuwata,
        switch_not_exciting_bokuwata,
    )


@app.cell
def _(
    Model,
    mo,
    statuses,
    switch_c_one,
    switch_detective_is_liar,
    switch_detective_is_not_liar,
    switch_exciting_bokuwata,
    switch_not_exciting_bokuwata,
):
    model2 = Model(
        switch_c_one.value,
        switch_exciting_bokuwata.value,
        switch_not_exciting_bokuwata.value,
        switch_detective_is_not_liar.value,
        switch_detective_is_liar.value,
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


if __name__ == "__main__":
    app.run()
