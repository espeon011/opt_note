# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "nbformat==5.10.4",
#     "ortools==9.14.6206",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import nbformat
    return (mo,)


@app.cell
def _():
    from ortools.sat.python import cp_model
    from ortools.math_opt.python import mathopt
    import random
    import datetime
    return cp_model, datetime, mathopt, random


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 忘年会席決め計算""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 問題""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    $n$ 人を $n$ 個の座席に配置する. 
    このとき以下のように配置する. 

    - 同一プロジェクトに配属されている人はできるだけ違うテーブルに配置
    - 同一グループに所属している人はできるだけ違うテーブルに配置
    - 同年代はできるだけ違うテーブルに配置(社員の年齢が確認できる場合)
    - その他同属性の社員はできるだけ違うテーブルに配置
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 定式化""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""座席ごとではなくテーブル単位で割り当てる""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### パラメータ""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - $S_t$: テーブル $t$ の座席集合
    - $E_p$: プロジェクト $p$ に配属されているメンバー
    - $E_g$: グループ $g$ に配属されているメンバー
    - $E_a$: 年代 $a$ に属しているメンバー
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 変数""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- $x_{it}$: 人 $i$ をテーブル $t$ に配置するとき $1$, そうでないとき $0$""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 制約""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - $\sum_i x_{it} \leq |S_t|$ (for all $t$): 1 つのテーブルに座れるのはテーブルのキャパシティ以下だけ
    - $\sum_t x_{it} = 1$ (for all $i$): 1 人の人は 1 つのテーブルにだけ割り当てられる
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 目的関数""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    以下のコスト関数を重み付けして足す. 

    - 同一プロジェクト同一テーブル配置ペナルティ
      - $\sum_p \sum_t \left( \sum_{i \in E_p} x_{i t} \right)^2$
    - 同一グループ同一テーブル配置ペナルティ
      - $\sum_g \sum_t \left( \sum_{i \in E_g} x_{i t} \right)^2$
    - 同一世代同一テーブル配置ペナルティ
      - $\sum_a \sum_t \left( \sum_{i \in E_a} x_{i t} \right)^2$

    2 乗になっている部分を展開して 0-1 変数の席の部分を線形制約で表現すれば線形目的関数にすることができる. 
    また, 近い位置にあるテーブルに同属性の社員を配置したくない場合は 2 乗の部分を単一テーブルではなく複数のテーブルも対象にすればよい.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## テスト実装""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### データ生成""")
    return


@app.class_definition
class Employee:
    def __init__(self, id, projects, group, age, name=""):
        self.id = id
        self.group = group.id
        self.projects = [_p.id for _p in projects]
        self.age = age.id
        self.name = name
        for _p in projects:
            _p.members.append(self.id)
        group.members.append(self.id)
        age.members.append(self.id)


@app.class_definition
class Project:
    def __init__(self, id, name=""):
        self.id = id
        self.members = []
        self.name = name


@app.class_definition
class Group:
    def __init__(self, id, name=""):
        self.id = id
        self.members = []
        self.name = name


@app.class_definition
class Age:
    def __init__(self, id, name=""):
        self.id = id
        self.members = []
        self.name = name


@app.class_definition
class Sheet:
    def __init__(self, id, table, name=""):
        self.id = id
        self.table = table.id
        self.name = name
        table.sheets.append(self.id)


@app.class_definition
class Table:
    def __init__(self, id, name=""):
        self.id = id
        self.sheets = []
        self.name = name

    @property
    def capacity(self):
        return len(self.sheets)


@app.cell
def _(random):
    # n_all: 人数
    # s_per_t: 1 テーブルあたりの席数
    n_all = 65
    s_per_t = 5

    s_all = n_all
    t_all = (s_all + s_per_t - 1) // s_per_t

    # テーブルは順番に番号付ける
    tables = [Table(t_id) for t_id in range(t_all)]
    sheets = [Sheet(s_id, tables[s_id // s_per_t]) for s_id in range(s_all)]

    # プロジェクト, グループ, 年代を適当に生成
    p_all = 5
    g_all = 4
    projects = [Project(p_id) for p_id in range(p_all)]
    groups = [Group(g_id) for g_id in range(g_all)]
    ages = [
        Age(id, name)
        for id, name in enumerate(["20~30 代", "40~50 代", "60 代以上"])
    ]

    random.seed(0)
    employees = []
    for e_id in range(n_all):
        e_group = random.choice(groups)
        e_projects = random.sample(
            projects, random.randint(1, len(projects) // 2)
        )  # プロジェクトをランダムに割り当て
        e_age = random.choice(ages)

        employees.append(Employee(e_id, e_projects, e_group, e_age))
    return ages, employees, groups, projects, tables


@app.cell
def _(ages, employees):
    for _e in employees:
        print(f"Employee {_e.id}", end=": ")
        print(f"group={_e.group}", end=" ")
        print(f"projects={_e.projects}", end=" ")
        print(f"age={_e.age}({ages[_e.age].name})")
    return


@app.cell
def _(projects):
    for _p in projects:
        print(f"Project {_p.id}: members={_p.members}")
    return


@app.cell
def _(groups):
    for _g in groups:
        print(f"Group {_g.id}: members={_g.members}")
    return


@app.cell
def _(ages):
    for _a in ages:
        print(f"Age {_a.id}: members={_a.members}")
    return


@app.cell
def _(tables):
    for _t in tables:
        print(f"Table {_t.id}: sheets={_t.sheets}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### モデル化(CP-SAT)""")
    return


@app.cell
def _(ages, cp_model, employees, groups, projects, tables):
    model = cp_model.CpModel()
    x = [
        [model.new_bool_var(f"e {_e.id} -> t {_t.id}") for _t in tables]
        for _e in employees
    ]
    for _e in employees:
        model.add_exactly_one([x[_e.id][_t.id] for _t in tables])
    for _t in tables:
        model.add(sum((x[_e.id][_t.id] for _e in employees)) <= _t.capacity)
    _obj_p = 0
    _obj_g = 0
    _obj_a = 0
    for _t in tables:
        for _p in projects:
            tp1 = model.new_int_var(
                0,
                min(_t.capacity, len(_p.members)),
                f"number_of_employee_in_project{_p.id}_in_table{_t.id}",
            )
            model.add(tp1 == sum((x[e_id][_t.id] for e_id in _p.members)))
            tp2 = model.new_int_var(0, min(_t.capacity, len(_p.members)) ** 2, "")
            model.add_multiplication_equality(tp2, [tp1, tp1])
            _obj_p = _obj_p + tp2
        for _g in groups:
            tp1 = model.new_int_var(
                0,
                min(_t.capacity, len(_g.members)),
                f"number_of_employee_in_group{_g.id}_in_table{_t.id}",
            )
            model.add(tp1 == sum((x[e_id][_t.id] for e_id in _g.members)))
            tp2 = model.new_int_var(0, min(_t.capacity, len(_g.members)) ** 2, "")
            model.add_multiplication_equality(tp2, [tp1, tp1])
            _obj_g = _obj_g + tp2
        for _a in ages:
            tp1 = model.new_int_var(
                0,
                min(_t.capacity, len(_a.members)),
                f"number_of_employee_in_age{_a.id}_in_table{_t.id}",
            )
            model.add(tp1 == sum((x[e_id][_t.id] for e_id in _a.members)))
            tp2 = model.new_int_var(0, min(_t.capacity, len(_a.members)) ** 2, "")
            model.add_multiplication_equality(tp2, [tp1, tp1])
            _obj_a = _obj_a + tp2
    model.minimize(_obj_p + _obj_g + _obj_a)
    return model, x


@app.cell
def _(cp_model, model):
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    statuses = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
        cp_model.UNKNOWN: "UNKNOWN",
    }

    print(f"status = {statuses[status]}")
    print(f"time = {solver.wall_time}")
    print(f"objective value = {solver.objective_value}")
    return solver, status


@app.cell
def _(cp_model, employees, solver, status, tables, x):
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for _t in tables:
            print(f"Table {_t.id}:")
            for _e in employees:
                if not solver.value(x[_e.id][_t.id]) == 1:
                    continue
                print(
                    f"  employee {_e.id}: projects={_e.projects} group={_e.group} age={_e.age}"
                )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### モデル化(SCIP)""")
    return


@app.cell
def _(ages, employees, groups, mathopt, projects, tables):
    model_scip = mathopt.Model(name="sheet")
    x_1 = [
        [
            model_scip.add_binary_variable(name=f"e {_e.id} -> t {_t.id}")
            for _t in tables
        ]
        for _e in employees
    ]
    for _e in employees:
        model_scip.add_linear_constraint(
            sum((x_1[_e.id][_t.id] for _t in tables)) == 1
        )
    for _t in tables:
        model_scip.add_linear_constraint(
            sum((x_1[_e.id][_t.id] for _e in employees)) <= _t.capacity
        )
    _obj_p = 0
    _obj_g = 0
    _obj_a = 0
    for _t in tables:
        for _p in projects:
            _tp = model_scip.add_integer_variable(
                lb=0,
                ub=min(_t.capacity, len(_p.members)),
                name=f"number_of_employee_in_project{_p.id}_in_table{_t.id}",
            )
            model_scip.add_linear_constraint(
                _tp == sum((x_1[e_id][_t.id] for e_id in _p.members))
            )
            _obj_p = _obj_p + _tp * _tp
        for _g in groups:
            _tp = model_scip.add_integer_variable(
                lb=0,
                ub=min(_t.capacity, len(_g.members)),
                name=f"number_of_employee_in_group{_g.id}_in_table{_t.id}",
            )
            model_scip.add_linear_constraint(
                _tp == sum((x_1[e_id][_t.id] for e_id in _g.members))
            )
            _obj_g = _obj_g + _tp * _tp
        for _a in ages:
            _tp = model_scip.add_integer_variable(
                lb=0,
                ub=min(_t.capacity, len(_a.members)),
                name=f"number_of_employee_in_age{_a.id}_in_table{_t.id}",
            )
            model_scip.add_linear_constraint(
                _tp == sum((x_1[e_id][_t.id] for e_id in _a.members))
            )
            _obj_a = _obj_a + _tp * _tp
    model_scip.minimize(_obj_p + _obj_g + _obj_a)
    return model_scip, x_1


@app.cell
def _(mathopt, model_scip):
    _params = mathopt.SolveParameters(enable_output=True)
    result = mathopt.solve(model_scip, mathopt.SolverType.GSCIP, params=_params)
    return (result,)


@app.cell
def _(employees, mathopt, result, tables, x_1):
    if (
        result.termination.reason == mathopt.TerminationReason.OPTIMAL
        or result.termination.reason == mathopt.TerminationReason.FEASIBLE
    ):
        for _t in tables:
            print(f"Table {_t.id}:")
            for _e in employees:
                if not round(result.variable_values()[x_1[_e.id][_t.id]]) == 1:
                    continue
                print(
                    f"  employee {_e.id}: projects={_e.projects} group={_e.group} age={_e.age}"
                )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 線形計画モデルとてしての定式化""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### パラメータ""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - $S_t$: テーブル $t$ の座席集合
    - $E_p$: プロジェクト $p$ に配属されているメンバー
    - $E_g$: グループ $g$ に配属されているメンバー
    - $E_a$: 年代 $a$ に属しているメンバー
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 変数""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- $x_{it}$: 人 $i$ をテーブル $t$ に配置するとき $1$, そうでないとき $0$""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 制約""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - $\sum_i x_{it} \leq |S_t|$ (for all $t$): 1 つのテーブルに座れるのはテーブルのキャパシティ以下だけ
    - $\sum_t x_{it} = 1$ (for all $i$): 1 人の人は 1 つのテーブルにだけ割り当てられる
    - 下記目的関数を表現するための制約
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 目的関数""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    以下のコスト関数を重み付けして足す. 

    - 同一プロジェクト同一テーブル配置ペナルティ
      - $\sum_p \sum_t \left( \sum_{i \in E_p} x_{i t} \right)^2$: これを下記制約により線形化する
          - $\sum_p \sum_t \sum_{i \in E_p} \sum_{j \in E_p} y_{i j t}^{(p)}$
          - $x_{i t} + x_{j t} \leq y_{i j t}^{(p)} + 1$
    - 同一グループ同一テーブル配置ペナルティ
      - $\sum_g \sum_t \left( \sum_{i \in E_g} x_{i t} \right)^2$: これを下記制約により線形化する
          - $\sum_p \sum_t \sum_{i \in E_g} \sum_{j \in E_g} y_{i j t}^{(g)}$
          - $x_{i t} + x_{j t} \leq y_{i j t}^{(g)} + 1$
    - 同一世代同一テーブル配置ペナルティ
      - $\sum_a \sum_t \left( \sum_{i \in E_a} x_{i t} \right)^2$: これを下記制約により線形化する
          - $\sum_p \sum_t \sum_{i \in E_a} \sum_{j \in E_a} y_{i j t}^{(a)}$
          - $x_{i t} + x_{j t} \leq y_{i j t}^{(a)} + 1$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## テスト実装(線形)""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Google OR-Tools の MathOpt を用いてモデリングし, 
    計算時に呼び出すソルバーを切り替えて比較する. 
    """
    )
    return


@app.cell
def _(ages, employees, groups, mathopt, projects, tables):
    model_linear = mathopt.Model(name="sheet")
    x_2 = [
        [
            model_linear.add_binary_variable(name=f"e {_e.id} -> t {_t.id}")
            for _t in tables
        ]
        for _e in employees
    ]
    for _e in employees:
        model_linear.add_linear_constraint(
            sum((x_2[_e.id][_t.id] for _t in tables)) == 1
        )
    for _t in tables:
        model_linear.add_linear_constraint(
            sum((x_2[_e.id][_t.id] for _e in employees)) <= _t.capacity
        )
    _obj_p = 0
    _obj_g = 0
    _obj_a = 0
    for _t in tables:
        for _p in projects:
            for e1_id in _p.members:
                for e2_id in _p.members:
                    _tp = model_linear.add_binary_variable()
                    model_linear.add_linear_constraint(
                        x_2[e1_id][_t.id] + x_2[e2_id][_t.id] <= _tp + 1
                    )
                    _obj_p = _obj_p + _tp
        for _g in groups:
            for e1_id in _g.members:
                for e2_id in _g.members:
                    _tp = model_linear.add_binary_variable()
                    model_linear.add_linear_constraint(
                        x_2[e1_id][_t.id] + x_2[e2_id][_t.id] <= _tp + 1
                    )
                    _obj_g = _obj_g + _tp
        for _a in ages:
            for e1_id in _a.members:
                for e2_id in _a.members:
                    _tp = model_linear.add_binary_variable()
                    model_linear.add_linear_constraint(
                        x_2[e1_id][_t.id] + x_2[e2_id][_t.id] <= _tp + 1
                    )
                    _obj_a = _obj_a + _tp
    model_linear.minimize(_obj_p + _obj_g + _obj_a)
    return (model_linear,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### ソルバー比較""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""どのソルバーも終わりそうになかったのでとりあえずリミット 1 分で計算. """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### 実行: CP-SAT""")
    return


@app.cell
def _(datetime, mathopt, model_linear):
    _params = mathopt.SolveParameters(
        time_limit=datetime.timedelta(minutes=1), enable_output=False
    )
    _result = mathopt.solve(
        model_linear, mathopt.SolverType.CP_SAT, params=_params
    )

    print(f"primal bound: {_result.primal_bound()}")
    print(f"dual bound: {_result.dual_bound()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### 実行: SCIP""")
    return


@app.cell
def _(datetime, mathopt, model_linear):
    _params = mathopt.SolveParameters(
        time_limit=datetime.timedelta(minutes=1), enable_output=False
    )
    _result = mathopt.solve(
        model_linear, mathopt.SolverType.GSCIP, params=_params
    )

    print(f"primal bound: {_result.primal_bound()}")
    print(f"dual bound: {_result.dual_bound()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### 実行: Highs""")
    return


@app.cell
def _(datetime, mathopt, model_linear):
    _params = mathopt.SolveParameters(
        time_limit=datetime.timedelta(minutes=1), enable_output=False
    )
    _result = mathopt.solve(
        model_linear, mathopt.SolverType.HIGHS, params=_params
    )

    print(f"primal bound: {_result.primal_bound()}")
    print(f"dual bound: {_result.dual_bound()}")
    return


if __name__ == "__main__":
    app.run()
