In [ ]:
```python
import marimo as mo
import nbformat
```

In [ ]:
```python
from ortools.sat.python import cp_model
from ortools.math_opt.python import mathopt
import random
import datetime
```

# 忘年会席決め計算

## 問題

$n$ 人を $n$ 個の座席に配置する.
このとき以下のように配置する.

- 同一プロジェクトに配属されている人はできるだけ違うテーブルに配置
- 同一グループに所属している人はできるだけ違うテーブルに配置
- 同年代はできるだけ違うテーブルに配置(社員の年齢が確認できる場合)
- その他同属性の社員はできるだけ違うテーブルに配置

## 定式化

座席ごとではなくテーブル単位で割り当てる

### パラメータ

- $S_t$: テーブル $t$ の座席集合
- $E_p$: プロジェクト $p$ に配属されているメンバー
- $E_g$: グループ $g$ に配属されているメンバー
- $E_a$: 年代 $a$ に属しているメンバー

### 変数

- $x_{it}$: 人 $i$ をテーブル $t$ に配置するとき $1$, そうでないとき $0$

### 制約

- $\sum_i x_{it} \leq |S_t|$ (for all $t$): 1 つのテーブルに座れるのはテーブルのキャパシティ以下だけ
- $\sum_t x_{it} = 1$ (for all $i$): 1 人の人は 1 つのテーブルにだけ割り当てられる

### 目的関数

以下のコスト関数を重み付けして足す.

- 同一プロジェクト同一テーブル配置ペナルティ
  - $\sum_p \sum_t \left( \sum_{i \in E_p} x_{i t} \right)^2$
- 同一グループ同一テーブル配置ペナルティ
  - $\sum_g \sum_t \left( \sum_{i \in E_g} x_{i t} \right)^2$
- 同一世代同一テーブル配置ペナルティ
  - $\sum_a \sum_t \left( \sum_{i \in E_a} x_{i t} \right)^2$

2 乗になっている部分を展開して 0-1 変数の席の部分を線形制約で表現すれば線形目的関数にすることができる.
また, 近い位置にあるテーブルに同属性の社員を配置したくない場合は 2 乗の部分を単一テーブルではなく複数のテーブルも対象にすればよい.

## テスト実装

### データ生成

In [ ]:
```python
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
```

In [ ]:
```python
class Project:
    def __init__(self, id, name=""):
        self.id = id
        self.members = []
        self.name = name
```

In [ ]:
```python
class Group:
    def __init__(self, id, name=""):
        self.id = id
        self.members = []
        self.name = name
```

In [ ]:
```python
class Age:
    def __init__(self, id, name=""):
        self.id = id
        self.members = []
        self.name = name
```

In [ ]:
```python
class Sheet:
    def __init__(self, id, table, name=""):
        self.id = id
        self.table = table.id
        self.name = name
        table.sheets.append(self.id)
```

In [ ]:
```python
class Table:
    def __init__(self, id, name=""):
        self.id = id
        self.sheets = []
        self.name = name

    @property
    def capacity(self):
        return len(self.sheets)
```

In [ ]:
```python
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
```

In [ ]:
```python
for _e in employees:
    print(f"Employee {_e.id}", end=": ")
    print(f"group={_e.group}", end=" ")
    print(f"projects={_e.projects}", end=" ")
    print(f"age={_e.age}({ages[_e.age].name})")
```

> ```
> Employee 0: group=3 projects=[0, 2] age=2(60 代以上)
> Employee 1: group=3 projects=[2, 3] age=1(40~50 代)
> Employee 2: group=1 projects=[2] age=0(20~30 代)
> Employee 3: group=0 projects=[4, 1] age=1(40~50 代)
> Employee 4: group=0 projects=[2] age=1(40~50 代)
> Employee 5: group=0 projects=[3, 2] age=2(60 代以上)
> Employee 6: group=1 projects=[3, 2] age=0(20~30 代)
> Employee 7: group=0 projects=[3] age=2(60 代以上)
> Employee 8: group=0 projects=[2, 1] age=2(60 代以上)
> Employee 9: group=2 projects=[1] age=2(60 代以上)
> Employee 10: group=1 projects=[1] age=2(60 代以上)
> Employee 11: group=3 projects=[0] age=1(40~50 代)
> Employee 12: group=3 projects=[2] age=2(60 代以上)
> Employee 13: group=2 projects=[4] age=1(40~50 代)
> Employee 14: group=1 projects=[3, 0] age=2(60 代以上)
> Employee 15: group=3 projects=[4, 1] age=1(40~50 代)
> Employee 16: group=1 projects=[1] age=0(20~30 代)
> Employee 17: group=2 projects=[0, 4] age=2(60 代以上)
> Employee 18: group=1 projects=[0] age=0(20~30 代)
> Employee 19: group=3 projects=[4, 1] age=0(20~30 代)
> Employee 20: group=3 projects=[3, 4] age=2(60 代以上)
> Employee 21: group=2 projects=[2] age=2(60 代以上)
> Employee 22: group=0 projects=[4, 2] age=0(20~30 代)
> Employee 23: group=1 projects=[2] age=0(20~30 代)
> Employee 24: group=1 projects=[1, 2] age=1(40~50 代)
> Employee 25: group=0 projects=[1] age=2(60 代以上)
> Employee 26: group=1 projects=[4] age=2(60 代以上)
> Employee 27: group=0 projects=[0] age=2(60 代以上)
> Employee 28: group=1 projects=[3] age=0(20~30 代)
> Employee 29: group=2 projects=[0] age=2(60 代以上)
> Employee 30: group=0 projects=[1] age=2(60 代以上)
> Employee 31: group=0 projects=[1, 0] age=2(60 代以上)
> Employee 32: group=0 projects=[4, 0] age=1(40~50 代)
> Employee 33: group=0 projects=[0] age=2(60 代以上)
> Employee 34: group=2 projects=[3, 1] age=0(20~30 代)
> Employee 35: group=3 projects=[4] age=0(20~30 代)
> Employee 36: group=3 projects=[2] age=1(40~50 代)
> Employee 37: group=3 projects=[1] age=0(20~30 代)
> Employee 38: group=1 projects=[2] age=2(60 代以上)
> Employee 39: group=2 projects=[4] age=1(40~50 代)
> Employee 40: group=1 projects=[3] age=2(60 代以上)
> Employee 41: group=3 projects=[2, 3] age=2(60 代以上)
> Employee 42: group=2 projects=[4] age=2(60 代以上)
> Employee 43: group=0 projects=[0, 2] age=2(60 代以上)
> Employee 44: group=0 projects=[1, 4] age=1(40~50 代)
> Employee 45: group=2 projects=[2, 1] age=2(60 代以上)
> Employee 46: group=2 projects=[3, 0] age=0(20~30 代)
> Employee 47: group=1 projects=[1, 4] age=0(20~30 代)
> Employee 48: group=3 projects=[4, 3] age=0(20~30 代)
> Employee 49: group=3 projects=[0, 1] age=1(40~50 代)
> Employee 50: group=0 projects=[1, 3] age=2(60 代以上)
> Employee 51: group=3 projects=[0] age=1(40~50 代)
> Employee 52: group=2 projects=[3, 0] age=1(40~50 代)
> Employee 53: group=1 projects=[1] age=0(20~30 代)
> Employee 54: group=3 projects=[2, 0] age=0(20~30 代)
> Employee 55: group=0 projects=[4] age=2(60 代以上)
> Employee 56: group=0 projects=[0] age=2(60 代以上)
> Employee 57: group=1 projects=[2, 1] age=0(20~30 代)
> Employee 58: group=3 projects=[0, 4] age=1(40~50 代)
> Employee 59: group=3 projects=[2] age=0(20~30 代)
> Employee 60: group=2 projects=[1] age=1(40~50 代)
> Employee 61: group=0 projects=[0] age=0(20~30 代)
> Employee 62: group=2 projects=[2, 0] age=2(60 代以上)
> Employee 63: group=3 projects=[3, 2] age=2(60 代以上)
> Employee 64: group=1 projects=[3] age=2(60 代以上)
> ```

In [ ]:
```python
for _p in projects:
    print(f"Project {_p.id}: members={_p.members}")
```

> ```
> Project 0: members=[0, 11, 14, 17, 18, 27, 29, 31, 32, 33, 43, 46, 49, 51, 52, 54, 56, 58, 61, 62]
> Project 1: members=[3, 8, 9, 10, 15, 16, 19, 24, 25, 30, 31, 34, 37, 44, 45, 47, 49, 50, 53, 57, 60]
> Project 2: members=[0, 1, 2, 4, 5, 6, 8, 12, 21, 22, 23, 24, 36, 38, 41, 43, 45, 54, 57, 59, 62, 63]
> Project 3: members=[1, 5, 6, 7, 14, 20, 28, 34, 40, 41, 46, 48, 50, 52, 63, 64]
> Project 4: members=[3, 13, 15, 17, 19, 20, 22, 26, 32, 35, 39, 42, 44, 47, 48, 55, 58]
> ```

In [ ]:
```python
for _g in groups:
    print(f"Group {_g.id}: members={_g.members}")
```

> ```
> Group 0: members=[3, 4, 5, 7, 8, 22, 25, 27, 30, 31, 32, 33, 43, 44, 50, 55, 56, 61]
> Group 1: members=[2, 6, 10, 14, 16, 18, 23, 24, 26, 28, 38, 40, 47, 53, 57, 64]
> Group 2: members=[9, 13, 17, 21, 29, 34, 39, 42, 45, 46, 52, 60, 62]
> Group 3: members=[0, 1, 11, 12, 15, 19, 20, 35, 36, 37, 41, 48, 49, 51, 54, 58, 59, 63]
> ```

In [ ]:
```python
for _a in ages:
    print(f"Age {_a.id}: members={_a.members}")
```

> ```
> Age 0: members=[2, 6, 16, 18, 19, 22, 23, 28, 34, 35, 37, 46, 47, 48, 53, 54, 57, 59, 61]
> Age 1: members=[1, 3, 4, 11, 13, 15, 24, 32, 36, 39, 44, 49, 51, 52, 58, 60]
> Age 2: members=[0, 5, 7, 8, 9, 10, 12, 14, 17, 20, 21, 25, 26, 27, 29, 30, 31, 33, 38, 40, 41, 42, 43, 45, 50, 55, 56, 62, 63, 64]
> ```

In [ ]:
```python
for _t in tables:
    print(f"Table {_t.id}: sheets={_t.sheets}")
```

> ```
> Table 0: sheets=[0, 1, 2, 3, 4]
> Table 1: sheets=[5, 6, 7, 8, 9]
> Table 2: sheets=[10, 11, 12, 13, 14]
> Table 3: sheets=[15, 16, 17, 18, 19]
> Table 4: sheets=[20, 21, 22, 23, 24]
> Table 5: sheets=[25, 26, 27, 28, 29]
> Table 6: sheets=[30, 31, 32, 33, 34]
> Table 7: sheets=[35, 36, 37, 38, 39]
> Table 8: sheets=[40, 41, 42, 43, 44]
> Table 9: sheets=[45, 46, 47, 48, 49]
> Table 10: sheets=[50, 51, 52, 53, 54]
> Table 11: sheets=[55, 56, 57, 58, 59]
> Table 12: sheets=[60, 61, 62, 63, 64]
> ```

### モデル化(CP-SAT)

In [ ]:
```python
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
```

In [ ]:
```python
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
```

> ```
> status = OPTIMAL
> time = 0.8570429380000001
> objective value = 374.0
> ```

In [ ]:
```python
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for _t in tables:
        print(f"Table {_t.id}:")
        for _e in employees:
            if not solver.value(x[_e.id][_t.id]) == 1:
                continue
            print(
                f"  employee {_e.id}: projects={_e.projects} group={_e.group} age={_e.age}"
            )
```

> ```
> Table 0:
>   employee 10: projects=[1] group=1 age=2
>   employee 28: projects=[3] group=1 age=0
>   employee 32: projects=[4, 0] group=0 age=1
>   employee 45: projects=[2, 1] group=2 age=2
>   employee 59: projects=[2] group=3 age=0
> Table 1:
>   employee 7: projects=[3] group=0 age=2
>   employee 8: projects=[2, 1] group=0 age=2
>   employee 11: projects=[0] group=3 age=1
>   employee 23: projects=[2] group=1 age=0
>   employee 39: projects=[4] group=2 age=1
> Table 2:
>   employee 29: projects=[0] group=2 age=2
>   employee 41: projects=[2, 3] group=3 age=2
>   employee 44: projects=[1, 4] group=0 age=1
>   employee 47: projects=[1, 4] group=1 age=0
>   employee 54: projects=[2, 0] group=3 age=0
> Table 3:
>   employee 17: projects=[0, 4] group=2 age=2
>   employee 36: projects=[2] group=3 age=1
>   employee 37: projects=[1] group=3 age=0
>   employee 40: projects=[3] group=1 age=2
>   employee 61: projects=[0] group=0 age=0
> Table 4:
>   employee 5: projects=[3, 2] group=0 age=2
>   employee 19: projects=[4, 1] group=3 age=0
>   employee 43: projects=[0, 2] group=0 age=2
>   employee 60: projects=[1] group=2 age=1
>   employee 64: projects=[3] group=1 age=2
> Table 5:
>   employee 3: projects=[4, 1] group=0 age=1
>   employee 12: projects=[2] group=3 age=2
>   employee 27: projects=[0] group=0 age=2
>   employee 46: projects=[3, 0] group=2 age=0
>   employee 57: projects=[2, 1] group=1 age=0
> Table 6:
>   employee 14: projects=[3, 0] group=1 age=2
>   employee 15: projects=[4, 1] group=3 age=1
>   employee 22: projects=[4, 2] group=0 age=0
>   employee 38: projects=[2] group=1 age=2
>   employee 52: projects=[3, 0] group=2 age=1
> Table 7:
>   employee 2: projects=[2] group=1 age=0
>   employee 20: projects=[3, 4] group=3 age=2
>   employee 21: projects=[2] group=2 age=2
>   employee 25: projects=[1] group=0 age=2
>   employee 49: projects=[0, 1] group=3 age=1
> Table 8:
>   employee 18: projects=[0] group=1 age=0
>   employee 24: projects=[1, 2] group=1 age=1
>   employee 35: projects=[4] group=3 age=0
>   employee 50: projects=[1, 3] group=0 age=2
>   employee 62: projects=[2, 0] group=2 age=2
> Table 9:
>   employee 0: projects=[0, 2] group=3 age=2
>   employee 13: projects=[4] group=2 age=1
>   employee 48: projects=[4, 3] group=3 age=0
>   employee 53: projects=[1] group=1 age=0
>   employee 56: projects=[0] group=0 age=2
> Table 10:
>   employee 1: projects=[2, 3] group=3 age=1
>   employee 16: projects=[1] group=1 age=0
>   employee 33: projects=[0] group=0 age=2
>   employee 42: projects=[4] group=2 age=2
>   employee 58: projects=[0, 4] group=3 age=1
> Table 11:
>   employee 6: projects=[3, 2] group=1 age=0
>   employee 9: projects=[1] group=2 age=2
>   employee 30: projects=[1] group=0 age=2
>   employee 51: projects=[0] group=3 age=1
>   employee 55: projects=[4] group=0 age=2
> Table 12:
>   employee 4: projects=[2] group=0 age=1
>   employee 26: projects=[4] group=1 age=2
>   employee 31: projects=[1, 0] group=0 age=2
>   employee 34: projects=[3, 1] group=2 age=0
>   employee 63: projects=[3, 2] group=3 age=2
> ```

### モデル化(SCIP)

In [ ]:
```python
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
```

In [ ]:
```python
_params = mathopt.SolveParameters(enable_output=True)
result = mathopt.solve(model_scip, mathopt.SolverType.GSCIP, params=_params)
```

> ```
> presolving:
> (round 1, exhaustive) 0 del vars, 0 del conss, 0 add conss, 1 chg bounds, 0 chg sides, 0 chg coeffs, 78 upgd conss, 0 impls, 65 clqs
>    (0.2s) probing cycle finished: starting next cycle
>    Deactivated symmetry handling methods, since SCIP was built without symmetry detector (SYM=none).
>    Deactivated symmetry handling methods, since SCIP was built without symmetry detector (SYM=none).
> presolving (2 rounds: 2 fast, 2 medium, 2 exhaustive):
>  0 deleted vars, 0 deleted constraints, 0 added constraints, 1 tightened bounds, 0 added holes, 0 changed sides, 0 changed coefficients
>  3783 implications, 65 cliques
> presolved problem has 1002 variables (845 bin, 156 int, 0 impl, 1 cont) and 235 constraints
>      13 constraints of type <knapsack>
>      65 constraints of type <setppc>
>     156 constraints of type <linear>
>       1 constraints of type <nonlinear>
> Presolving Time: 0.15
> 
>  time | node  | left  |LP iter|LP it/n|mem/heur|mdpt |vars |cons |rows |cuts |sepa|confs|strbr|  dualbound   | primalbound  |  gap   | compl. 
> p 0.2s|     1 |     0 |     0 |     - |  clique|   0 |1159 | 235 | 703 |   0 |  0 |   0 |   0 |-1.000000e-09 | 4.860000e+02 |    Inf | unknown
> p 0.2s|     1 |     0 |     0 |     - |   locks|   0 |1159 | 235 | 703 |   0 |  0 |   0 |   0 |-1.000000e-09 | 4.700000e+02 |    Inf | unknown
>   0.6s|     1 |     0 | 10564 |     - |    12M |   0 |1159 | 246 | 703 |   0 |  0 |  13 |   0 | 2.860000e+02 | 4.700000e+02 |  64.34%| unknown
>   0.6s|     1 |     0 | 10564 |     - |    12M |   0 |1159 | 249 | 703 |   0 |  0 |  16 |   0 | 2.860000e+02 | 4.700000e+02 |  64.34%| unknown
>   1.1s|     1 |     0 | 19794 |     - |    22M |   0 |1159 | 249 | 823 | 120 |  1 |  16 |   0 | 3.550000e+02 | 4.700000e+02 |  32.39%| unknown
>   1.1s|     1 |     0 | 19794 |     - |    22M |   0 |1159 | 251 | 823 | 120 |  1 |  18 |   0 | 3.550000e+02 | 4.700000e+02 |  32.39%| unknown
>   1.5s|     1 |     0 | 25781 |     - |    43M |   0 |1159 | 251 | 851 | 148 |  2 |  18 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   1.5s|     1 |     0 | 25781 |     - |    43M |   0 |1159 | 253 | 851 | 148 |  2 |  20 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   1.6s|     1 |     0 | 26343 |     - |    65M |   0 |1159 | 253 | 855 | 152 |  3 |  20 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   1.7s|     1 |     0 | 26391 |     - |    85M |   0 |1159 | 255 | 860 | 157 |  4 |  22 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   1.8s|     1 |     0 | 26590 |     - |   112M |   0 |1159 | 255 | 862 | 159 |  5 |  22 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   2.0s|     1 |     0 | 26831 |     - |   136M |   0 |1159 | 255 | 868 | 165 |  6 |  22 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   2.1s|     1 |     0 | 26957 |     - |   159M |   0 |1159 | 255 | 873 | 170 |  7 |  22 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   2.4s|     1 |     0 | 27251 |     - |   178M |   0 |1159 | 256 | 878 | 175 |  8 |  23 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   2.6s|     1 |     0 | 27370 |     - |   190M |   0 |1159 | 257 | 883 | 180 |  9 |  24 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>  time | node  | left  |LP iter|LP it/n|mem/heur|mdpt |vars |cons |rows |cuts |sepa|confs|strbr|  dualbound   | primalbound  |  gap   | compl. 
>   2.8s|     1 |     0 | 27506 |     - |   216M |   0 |1159 | 258 | 888 | 185 | 10 |  25 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   3.0s|     1 |     0 | 27546 |     - |   216M |   0 |1159 | 259 | 618 | 188 | 11 |  26 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
>   3.2s|     1 |     0 | 27546 |     - |   216M |   0 |1159 | 260 | 618 | 188 | 12 |  27 |   0 | 3.740000e+02 | 4.700000e+02 |  25.67%| unknown
> o 3.5s|     1 |     0 | 29103 |     - |feaspump|   0 |1159 | 260 | 618 | 188 | 13 |  27 |   0 | 3.740000e+02 | 3.880000e+02 |   3.74%| unknown
>   4.1s|     1 |     0 | 41477 |     - |   216M |   0 |1159 | 260 | 618 | 188 | 13 |  30 |   0 | 3.740000e+02 | 3.880000e+02 |   3.74%| unknown
>   4.6s|     1 |     2 | 41477 |     - |   216M |   0 |1159 | 260 | 618 | 188 | 14 |  30 |  23 | 3.740000e+02 | 3.880000e+02 |   3.74%| unknown
> d 5.9s|     8 |     0 | 72647 |6443.0 |pscostdi|   7 |1159 | 260 | 597 |   0 |  2 |  30 |  23 | 3.740000e+02 | 3.740000e+02 |   0.00%| 100.00%
> 
> SCIP Status        : problem is solved [optimal solution found]
> Solving Time (sec) : 5.91
> Solving Nodes      : 8
> Primal Bound       : +3.74000000000000e+02 (5 solutions)
> Dual Bound         : +3.74000000000000e+02
> Gap                : 0.00 %
> ```

In [ ]:
```python
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
```

> ```
> Table 0:
>   employee 34: projects=[3, 1] group=2 age=0
>   employee 51: projects=[0] group=3 age=1
>   employee 55: projects=[4] group=0 age=2
>   employee 56: projects=[0] group=0 age=2
>   employee 57: projects=[2, 1] group=1 age=0
> Table 1:
>   employee 12: projects=[2] group=3 age=2
>   employee 18: projects=[0] group=1 age=0
>   employee 25: projects=[1] group=0 age=2
>   employee 39: projects=[4] group=2 age=1
>   employee 40: projects=[3] group=1 age=2
> Table 2:
>   employee 14: projects=[3, 0] group=1 age=2
>   employee 15: projects=[4, 1] group=3 age=1
>   employee 21: projects=[2] group=2 age=2
>   employee 22: projects=[4, 2] group=0 age=0
>   employee 53: projects=[1] group=1 age=0
> Table 3:
>   employee 6: projects=[3, 2] group=1 age=0
>   employee 9: projects=[1] group=2 age=2
>   employee 30: projects=[1] group=0 age=2
>   employee 32: projects=[4, 0] group=0 age=1
>   employee 54: projects=[2, 0] group=3 age=0
> Table 4:
>   employee 10: projects=[1] group=1 age=2
>   employee 26: projects=[4] group=1 age=2
>   employee 44: projects=[1, 4] group=0 age=1
>   employee 52: projects=[3, 0] group=2 age=1
>   employee 59: projects=[2] group=3 age=0
> Table 5:
>   employee 20: projects=[3, 4] group=3 age=2
>   employee 24: projects=[1, 2] group=1 age=1
>   employee 37: projects=[1] group=3 age=0
>   employee 61: projects=[0] group=0 age=0
>   employee 62: projects=[2, 0] group=2 age=2
> Table 6:
>   employee 1: projects=[2, 3] group=3 age=1
>   employee 17: projects=[0, 4] group=2 age=2
>   employee 23: projects=[2] group=1 age=0
>   employee 31: projects=[1, 0] group=0 age=2
>   employee 35: projects=[4] group=3 age=0
> Table 7:
>   employee 27: projects=[0] group=0 age=2
>   employee 43: projects=[0, 2] group=0 age=2
>   employee 47: projects=[1, 4] group=1 age=0
>   employee 60: projects=[1] group=2 age=1
>   employee 63: projects=[3, 2] group=3 age=2
> Table 8:
>   employee 0: projects=[0, 2] group=3 age=2
>   employee 2: projects=[2] group=1 age=0
>   employee 11: projects=[0] group=3 age=1
>   employee 42: projects=[4] group=2 age=2
>   employee 50: projects=[1, 3] group=0 age=2
> Table 9:
>   employee 4: projects=[2] group=0 age=1
>   employee 19: projects=[4, 1] group=3 age=0
>   employee 28: projects=[3] group=1 age=0
>   employee 29: projects=[0] group=2 age=2
>   employee 41: projects=[2, 3] group=3 age=2
> Table 10:
>   employee 7: projects=[3] group=0 age=2
>   employee 38: projects=[2] group=1 age=2
>   employee 45: projects=[2, 1] group=2 age=2
>   employee 48: projects=[4, 3] group=3 age=0
>   employee 49: projects=[0, 1] group=3 age=1
> Table 11:
>   employee 5: projects=[3, 2] group=0 age=2
>   employee 13: projects=[4] group=2 age=1
>   employee 16: projects=[1] group=1 age=0
>   employee 33: projects=[0] group=0 age=2
>   employee 36: projects=[2] group=3 age=1
> Table 12:
>   employee 3: projects=[4, 1] group=0 age=1
>   employee 8: projects=[2, 1] group=0 age=2
>   employee 46: projects=[3, 0] group=2 age=0
>   employee 58: projects=[0, 4] group=3 age=1
>   employee 64: projects=[3] group=1 age=2
> ```

## 線形計画モデルとてしての定式化

### パラメータ

- $S_t$: テーブル $t$ の座席集合
- $E_p$: プロジェクト $p$ に配属されているメンバー
- $E_g$: グループ $g$ に配属されているメンバー
- $E_a$: 年代 $a$ に属しているメンバー

### 変数

- $x_{it}$: 人 $i$ をテーブル $t$ に配置するとき $1$, そうでないとき $0$

### 制約

- $\sum_i x_{it} \leq |S_t|$ (for all $t$): 1 つのテーブルに座れるのはテーブルのキャパシティ以下だけ
- $\sum_t x_{it} = 1$ (for all $i$): 1 人の人は 1 つのテーブルにだけ割り当てられる
- 下記目的関数を表現するための制約

### 目的関数

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

## テスト実装(線形)

Google OR-Tools の MathOpt を用いてモデリングし,
計算時に呼び出すソルバーを切り替えて比較する.

In [ ]:
```python
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
```

### ソルバー比較

どのソルバーも終わりそうになかったのでとりあえずリミット 1 分で計算.

#### 実行: CP-SAT

In [ ]:
```python
_params = mathopt.SolveParameters(
    time_limit=datetime.timedelta(minutes=1), enable_output=False
)
_result = mathopt.solve(
    model_linear, mathopt.SolverType.CP_SAT, params=_params
)

print(f"primal bound: {_result.primal_bound()}")
print(f"dual bound: {_result.dual_bound()}")
```

> ```
> primal bound: 380.0
> dual bound: 226.0
> ```

#### 実行: SCIP

In [ ]:
```python
_params = mathopt.SolveParameters(
    time_limit=datetime.timedelta(minutes=1), enable_output=False
)
_result = mathopt.solve(
    model_linear, mathopt.SolverType.GSCIP, params=_params
)

print(f"primal bound: {_result.primal_bound()}")
print(f"dual bound: {_result.dual_bound()}")
```

> ```
> primal bound: 410.0
> dual bound: 226.0
> ```

#### 実行: Highs

In [ ]:
```python
_params = mathopt.SolveParameters(
    time_limit=datetime.timedelta(minutes=1), enable_output=False
)
_result = mathopt.solve(
    model_linear, mathopt.SolverType.HIGHS, params=_params
)

print(f"primal bound: {_result.primal_bound()}")
print(f"dual bound: {_result.dual_bound()}")
```

> ```
> primal bound: 384.0000000000428
> dual bound: 226.00000000000153
> ```
