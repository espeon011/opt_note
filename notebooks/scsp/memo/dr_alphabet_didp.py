# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "didppy==0.10.0",
#     "nbformat==5.10.4",
#     "opt-note",
# ]
# [tool.uv.sources]
# opt-note = { git = "https://github.com/espeon011/opt_note" }
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    from dataclasses import dataclass
    import didppy
    import opt_note.scsp as scsp


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # アルファベットアルゴリズムで作成したものを削り出す (DIDP)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `DR_ALPHABET_CPSAT` の Reduction プロセスは DIDP 向きな気がする.
    """)
    return


@app.function
def boundtable_scs2(s1: str, s2: str) -> list[list[int]]:
    len1, len2 = len(s1), len(s2)

    dp = [[len1 + len2 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i1 in range(len1 + 1):
        dp[i1][len2] = len1 - i1
    for i2 in range(len2 + 1):
        dp[len1][i2] = len2 - i2

    for i1 in range(len1 - 1, -1, -1):
        for i2 in range(len2 - 1, -1, -1):
            if s1[i1] == s2[i2]:
                dp[i1][i2] = dp[i1 + 1][i2 + 1] + 1
            else:
                dp[i1][i2] = min(dp[i1 + 1][i2], dp[i1][i2 + 1]) + 1

    return dp


@app.function
def boundexpr_scs2len(
    instance: list[str],
    dpmodel: didppy.Model,
    index_vars: list[didppy.ElementVar],
) -> didppy.IntExpr:
    exprs = []
    for idx1, (s1, index_var1) in enumerate(zip(instance, index_vars)):
        for idx2, (s2, index_var2) in enumerate(zip(instance, index_vars)):
            if idx2 >= idx1:
                continue
            table_idx1_idx2 = dpmodel.add_int_table(boundtable_scs2(s1, s2))
            exprs.append(table_idx1_idx2[index_var1, index_var2])

    bound = didppy.IntExpr(0)
    for expr in exprs:
        bound = didppy.max(bound, expr)

    return bound


@app.class_definition
@dataclass
class ModelReduction:
    instance: list[str]
    template: str
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, time_limit: int | None = 60, log: bool = False) -> str | None:
        chars = sorted(list(set("".join(self.instance) + self.template)))

        dpmodel = didppy.Model(maximize=False, float_cost=False)

        instance_table = dpmodel.add_element_table(
            [[chars.index(c) for c in s] + [len(chars)] for s in self.instance]
        )
        template_table = dpmodel.add_element_table(
            [chars.index(c) for c in self.template] + [len(chars)]
        )

        index_types = [
            dpmodel.add_object_type(number=len(s) + 1) for s in self.instance
        ]
        index_vars = [
            dpmodel.add_element_resource_var(object_type=index_type, target=0)
            for index_type in index_types
        ]
        objtype_template = dpmodel.add_object_type(number=len(self.template) + 1)
        next = dpmodel.add_element_var(object_type=objtype_template, target=0)
        dpmodel.add_state_constr(next <= len(self.template))
        for s, index_var in zip(self.instance, index_vars):
            dpmodel.add_state_constr(len(self.template) - next >= len(s) - index_var)

        condition = didppy.Condition(False)
        for sidx, index_var in enumerate(index_vars):
            condition |= instance_table[sidx, index_var] == template_table[next]

        # テンプレート文字列の next 文字目を採用する
        use = didppy.Transition(
            name="1",
            cost=1 + didppy.IntExpr.state_cost(),
            effects=[
                (
                    index_var,
                    (
                        instance_table[sidx, index_var] == template_table[next]
                    ).if_then_else(index_var + 1, index_var),
                )
                for sidx, index_var in enumerate(index_vars)
            ]
            + [(next, next + 1)],
            preconditions=[condition],
        )

        # テンプレート文字列の next 文字目を採用しない
        disuse = didppy.Transition(
            name="0",
            cost=didppy.IntExpr.state_cost(),
            effects=[(next, next + 1)],
            preconditions=[condition],
        )

        # テンプレート文字列の next 文字目を使用しても意味がない場面
        disuse_forced = didppy.Transition(
            name="0",
            cost=didppy.IntExpr.state_cost(),
            effects=[(next, next + 1)],
            preconditions=[~condition],
        )

        dpmodel.add_transition(use)
        dpmodel.add_transition(disuse)
        dpmodel.add_transition(disuse_forced, forced=True)

        dpmodel.add_base_case(
            [index_var == len(s) for s, index_var in zip(self.instance, index_vars)]
        )

        # 残っている文字列から 2 つを選んで SCS を取って長さが最大のものを Dual Bound とする.
        dpmodel.add_dual_bound(boundexpr_scs2len(self.instance, dpmodel, index_vars))

        dpsolver = didppy.CABS(
            dpmodel, threads=12, time_limit=time_limit, quiet=(not log)
        )
        # dpsolver = didppy.ForwardRecursion(
        #     dpmodel, time_limit=time_limit, quiet=(not log)
        # )
        # dpsolver = didppy.CAASDy(
        #     dpmodel, time_limit=time_limit, quiet=(not log)
        # )
        # dpsolver = didppy.LNBS(
        #     dpmodel, time_limit=time_limit, quiet=(not log)
        # )
        # dpsolver = didppy.DFBB(
        #     dpmodel, time_limit=time_limit, quiet=(not log)
        # )
        didpsolution = dpsolver.search()

        if didpsolution.best_bound is not None:
            self.best_bound = float(didpsolution.best_bound)
        else:
            self.best_bound = 0.0

        if not didpsolution.is_infeasible and len(didpsolution.transitions) > 0:
            use_list = "".join([trans.name for trans in didpsolution.transitions])
            self.solution = "".join(
                [self.template[idx] for idx, flag in enumerate(use_list) if flag == "1"]
            )
        else:
            self.solution = None

        return self.solution


@app.class_definition
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0
    inner_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        template = scsp.model.alphabet.Model(self.instance).solve()
        if template is None:
            return None
        inner_model = ModelReduction(self.instance, template)
        inner_model.solve(time_limit, log)
        self.solution = inner_model.solution
        self.inner_bound = inner_model.best_bound
        return self.solution


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ベンチマーク
    """)
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n002k015-025.txt", log=False)
    return


@app.cell
def _():
    scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt", log=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    なんかダメだな... 定式化が間違っている?
    あるいは単純に相性が悪いだけ?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 参考: CP-SAT 版
    """)
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.dr_alphabet_cpsat.Model,
        example_filename="uniform_q26n002k015-025.txt",
    )
    return


@app.cell
def _():
    scsp.util.bench(
        scsp.model.dr_alphabet_cpsat.Model,
        example_filename="uniform_q26n004k015-025.txt",
    )
    return


if __name__ == "__main__":
    app.run()
