In [ ]:
```python
from ortools.sat.python import cp_model
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# 方程式が成立するかどうかを表す Bool 変数

$x$ を 0-1 決定変数, $a, b$ を整数決定変数として

$$
x = 1 \iff a = b
$$

を実現する制約条件を考えたい.
まずは不等式の場合から考える.

## 不等式の場合

$x$ を 0-1 決定変数, $a, b$ を整数決定変数として

$$
x = 1 \iff a \leq b
$$

を実現する制約は big-M 法を使えば次のように線形に書ける.

- $a \leq b + M (1 - x)$
- $a - 1 \geq b - M x$

In [ ]:
```python
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count = self.__solution_count + 1
        for v in self.__variables:
            print(f'{v}={self.value(v)}', end=' ')
        print()

    @property
    def solution_count(self):
        return self.__solution_count
```

In [ ]:
```python
_lb_a, _ub_a = (1, 5)
_lb_b, _ub_b = (1, 5)
_model = cp_model.CpModel()
x = _model.new_bool_var('(a<=b)')
a = _model.new_int_var(_lb_a, _ub_a, 'a')
b = _model.new_int_var(_lb_b, _ub_b, 'b')
_big_m = _ub_b - _lb_a + 1
_model.add(a <= b + _big_m * (1 - x))
_model.add(a - 1 >= b - _big_m * x)

_solver = cp_model.CpSolver()
_solution_printer = VarArraySolutionPrinter([x, a, b])
_solver.parameters.enumerate_all_solutions = True
_status = _solver.solve(_model, _solution_printer)
```

> ```
> (a<=b)=0 a=2 b=1 
> (a<=b)=0 a=3 b=1 
> (a<=b)=0 a=4 b=1 
> (a<=b)=0 a=4 b=2 
> (a<=b)=0 a=3 b=2 
> (a<=b)=0 a=5 b=2 
> (a<=b)=0 a=5 b=1 
> (a<=b)=0 a=5 b=3 
> (a<=b)=0 a=4 b=3 
> (a<=b)=0 a=5 b=4 
> (a<=b)=1 a=5 b=5 
> (a<=b)=1 a=4 b=4 
> (a<=b)=1 a=3 b=4 
> (a<=b)=1 a=3 b=3 
> (a<=b)=1 a=3 b=5 
> (a<=b)=1 a=4 b=5 
> (a<=b)=1 a=1 b=5 
> (a<=b)=1 a=1 b=4 
> (a<=b)=1 a=1 b=3 
> (a<=b)=1 a=1 b=2 
> (a<=b)=1 a=2 b=2 
> (a<=b)=1 a=2 b=3 
> (a<=b)=1 a=2 b=4 
> (a<=b)=1 a=2 b=5 
> (a<=b)=1 a=1 b=1
> ```

## 方程式の場合

big-M 法を用いれば方程式の場合も線形に表すことができる.

- $x = 1 \iff a \leq b$ を表す制約
    - $a \leq b + M (1 - x)$
    - $a - 1 \geq b - M x$
- $y = 1 \iff a \geq b$ を表す制約
    - $b \leq a + M (1 - y)$
    - $b - 1 \geq a - M y$
- $z = x \land y$ を表す制約
    - $z + 1 \geq x + y$
    - $2 z \leq x + y$

これで
$z = 1 \iff a = b$
となる.

In [ ]:
```python
_lb_a, _ub_a = (1, 5)
_lb_b, _ub_b = (1, 5)
_model = cp_model.CpModel()
_x = _model.new_bool_var('(a<=b)')
_y = _model.new_bool_var('(a>=b)')
_z = _model.new_bool_var('(a==b)')
_a = _model.new_int_var(_lb_a, _ub_a, 'a')
_b = _model.new_int_var(_lb_b, _ub_b, 'b')
_big_m = max(_ub_a - _lb_b + 1, _ub_b - _lb_a + 1)
_model.add(_a <= _b + _big_m * (1 - _x))
_model.add(_a - 1 >= _b - _big_m * _x)
_model.add(_b <= _a + _big_m * (1 - _y))
_model.add(_b - 1 >= _a - _big_m * _y)
_model.add(_z + 1 >= _x + _y)
_model.add(2 * _z <= _x + _y)

_solver = cp_model.CpSolver()
_solution_printer = VarArraySolutionPrinter([_z, _x, _y, _a, _b])
_solver.parameters.enumerate_all_solutions = True
_status = _solver.solve(_model, _solution_printer)
```

> ```
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=1 b=2 
> (a==b)=1 (a<=b)=1 (a>=b)=1 a=1 b=1 
> (a==b)=1 (a<=b)=1 (a>=b)=1 a=2 b=2 
> (a==b)=1 (a<=b)=1 (a>=b)=1 a=3 b=3 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=2 b=3 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=1 b=3 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=1 b=4 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=1 b=5 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=2 b=5 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=2 b=4 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=3 b=4 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=3 b=5 
> (a==b)=0 (a<=b)=1 (a>=b)=0 a=4 b=5 
> (a==b)=1 (a<=b)=1 (a>=b)=1 a=5 b=5 
> (a==b)=1 (a<=b)=1 (a>=b)=1 a=4 b=4 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=5 b=4 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=4 b=3 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=5 b=3 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=5 b=1 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=5 b=2 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=4 b=2 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=4 b=1 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=3 b=1 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=3 b=2 
> (a==b)=0 (a<=b)=0 (a>=b)=1 a=2 b=1
> ```

## `only_enforce_if()` の利用

Google OR-Tools には `only_enforce_if()` 関数があり,
特定の Bool 変数が `True` のときのみ制約を ON にすることができる.

### 同値でなくてもよい場合

下記を直接制約に加える.

$$
x = 1 \Longrightarrow a = b
$$

In [ ]:
```python
_lb_a, _ub_a = (1, 5)
_lb_b, _ub_b = (1, 5)
_model = cp_model.CpModel()
_x = _model.new_bool_var('(a==b)')
_a = _model.new_int_var(_lb_a, _ub_a, 'a')
_b = _model.new_int_var(_lb_b, _ub_b, 'b')
_model.add(_a == _b).only_enforce_if(_x)

_solver = cp_model.CpSolver()
_solution_printer = VarArraySolutionPrinter([_x, _a, _b])
_solver.parameters.enumerate_all_solutions = True
_status = _solver.solve(_model, _solution_printer)
```

> ```
> (a==b)=0 a=1 b=1 
> (a==b)=0 a=2 b=1 
> (a==b)=0 a=2 b=2 
> (a==b)=0 a=1 b=2 
> (a==b)=0 a=3 b=2 
> (a==b)=0 a=3 b=1 
> (a==b)=0 a=3 b=3 
> (a==b)=0 a=2 b=3 
> (a==b)=0 a=1 b=3 
> (a==b)=0 a=4 b=3 
> (a==b)=0 a=4 b=2 
> (a==b)=0 a=4 b=1 
> (a==b)=0 a=4 b=4 
> (a==b)=0 a=3 b=4 
> (a==b)=0 a=2 b=4 
> (a==b)=0 a=1 b=4 
> (a==b)=0 a=5 b=4 
> (a==b)=0 a=5 b=3 
> (a==b)=0 a=5 b=2 
> (a==b)=0 a=5 b=1 
> (a==b)=0 a=5 b=5 
> (a==b)=0 a=4 b=5 
> (a==b)=0 a=3 b=5 
> (a==b)=0 a=2 b=5 
> (a==b)=0 a=1 b=5 
> (a==b)=1 a=1 b=1 
> (a==b)=1 a=2 b=2 
> (a==b)=1 a=3 b=3 
> (a==b)=1 a=4 b=4 
> (a==b)=1 a=5 b=5
> ```

### 同値にしたい場合

上記の

$$
x = 1 \Longrightarrow a = b
$$

に加えてその裏を制約に入れることで同値にできる:

$$
x = 0 \Longrightarrow a \ne b
$$

In [ ]:
```python
_lb_a, _ub_a = (1, 5)
_lb_b, _ub_b = (1, 5)
_model = cp_model.CpModel()
_x = _model.new_bool_var('(a==b)')
_a = _model.new_int_var(_lb_a, _ub_a, 'a')
_b = _model.new_int_var(_lb_b, _ub_b, 'b')
_model.add(_a == _b).only_enforce_if(_x)
_model.add(_a != _b).only_enforce_if(_x.negated())

_solver = cp_model.CpSolver()
_solution_printer = VarArraySolutionPrinter([_x, _a, _b])
_solver.parameters.enumerate_all_solutions = True
_status = _solver.solve(_model, _solution_printer)
```

> ```
> (a==b)=0 a=1 b=2 
> (a==b)=0 a=2 b=1 
> (a==b)=0 a=3 b=1 
> (a==b)=0 a=4 b=1 
> (a==b)=0 a=4 b=2 
> (a==b)=0 a=3 b=2 
> (a==b)=0 a=5 b=2 
> (a==b)=0 a=5 b=1 
> (a==b)=0 a=5 b=3 
> (a==b)=0 a=4 b=3 
> (a==b)=0 a=5 b=4 
> (a==b)=0 a=4 b=5 
> (a==b)=0 a=3 b=4 
> (a==b)=0 a=3 b=5 
> (a==b)=0 a=2 b=5 
> (a==b)=0 a=2 b=4 
> (a==b)=0 a=2 b=3 
> (a==b)=0 a=1 b=3 
> (a==b)=0 a=1 b=4 
> (a==b)=0 a=1 b=5 
> (a==b)=1 a=4 b=4 
> (a==b)=1 a=3 b=3 
> (a==b)=1 a=5 b=5 
> (a==b)=1 a=2 b=2 
> (a==b)=1 a=1 b=1
> ```

## 応用

X のポスト([https://x.com/mrsolyu/status/1846512850879275074](https://x.com/mrsolyu/status/1846512850879275074))でこういった問題があったので定式化して犯人を求める.

> お前達の誰かが、あの祠を壊したんか！？
>
> A「俺がやりました」
>
> B「犯人は2人いる」
>
> C「Dが犯人でないなら僕が犯人」
>
> D「4人の中で嘘つきは奇数人」
>
> 犯人はこの中にいるはずじゃ。そして呪いで嘘しかつけなくなっておるわい。
> 誰が祠を壊したかのう？

総当たりで探索しても一瞬で終わる程度の規模ではあるが, 練習のために定式化と実装を行う.

### 定式化

#### 変数

- $x_A, x_B, x_C, x_D$: A ~ D が嘘つきのとき $1$, 正直もののとき $0$
- $y_A, y_B, y_C, y_D$: A ~ D が犯人のとき $1$, そうでないとき $0$

#### 制約

- 祠を壊したものは呪いで嘘しかつけなくなっている
    - $y_* <= x_*$
- A「俺がやりました」
    - $x_A = 0 \Longrightarrow y_A = 1$
    - $x_A = 1 \Longrightarrow y_A = 0$
    - 上記 2 つをまとめて $x_A = 1 - y_A$ と書ける
- B「犯人は2人いる」
    - $x_B = 0 \Longrightarrow y_A + y_B + y_C + y_D = 2$
    - $x_B = 1 \Longrightarrow y_A + y_B + y_C + y_D \ne 2$
- C「Dが犯人でないなら僕が犯人」
    - $x_C = 0 \Longrightarrow$ 「$y_D = 0 \Longrightarrow y_C = 1$」だがこれは $1 - x_C \leq y_C + y_D$ と同値
    - $x_C = 1 \Longrightarrow$ 「$y_D = 0 \land y_C = 0$」だがこれは $2 (1 - x_C) \geq y_C + y_D$ と同値
- D「4人の中で嘘つきは奇数人」
    - $x_D = 0 \Longrightarrow x_A + x_B + x_C + x_D \equiv 1 \mod 2$
    - $x_D = 1 \Longrightarrow x_A + x_B + x_C + x_D \equiv 0 \mod 2$
    - 上記をまとめて $x_A + x_B + x_C + x_D \equiv 1 - x_D \mod 2$ として実装する
    - この条件は線形にすることができる.
    $e, o$ を 0-1 決定変数とし, 嘘つきの数が偶数人か奇数人かに対応させるとする.
    この条件は次のように書ける. $s_e, z$ を整数決定変数として,

        - $e + o = 1$
        - $x_D = e$
        - $s_e = 2 * z$
        - $x_A + x_B + x_C + x_D = s_e + o$

    とすればよい.
    こうして A から D までの全ての条件は線形制約で記述できる.

### 実装

In [ ]:
```python
suspects = ['A', 'B', 'C', 'D']
```

In [ ]:
```python
_model = cp_model.CpModel()
_liar = {_s: _model.new_bool_var(f'{_s}_is_liar') for _s in suspects}
_culprit = {_s: _model.new_bool_var(f'{_s}_is_culprit') for _s in suspects}
for _s in suspects:
    _model.add_implication(_culprit[_s], _liar[_s])
_model.add_bool_xor(_liar['A'], _culprit['A'])
_model.add(sum((_culprit[_s] for _s in suspects)) == 2).only_enforce_if(_liar['B'].negated())
_model.add(sum((_culprit[_s] for _s in suspects)) != 2).only_enforce_if(_liar['B'])
_model.add_implication(_culprit['D'].negated(), _culprit['C']).only_enforce_if(_liar['C'].negated())
_model.add(_culprit['C'] == 0).only_enforce_if(_liar['C'])
_model.add(_culprit['D'] == 0).only_enforce_if(_liar['C'])
_n_liar = _model.new_int_var(0, len(suspects), 'num_of_liars')
_model.add(_n_liar == sum((_liar[_s] for _s in suspects)))
_model.add_modulo_equality(_liar['D'].negated(), _n_liar, 2)
_model.add(sum((_culprit[_s] for _s in suspects)) >= 1)

_solver = cp_model.CpSolver()
_solution_printer = VarArraySolutionPrinter(list(_liar.values()) + list(_culprit.values()))
_solver.parameters.enumerate_all_solutions = True
_status = _solver.solve(_model, _solution_printer)
```

> ```
> A_is_liar=1 B_is_liar=1 C_is_liar=1 D_is_liar=0 A_is_culprit=0 B_is_culprit=1 C_is_culprit=0 D_is_culprit=0 
> A_is_liar=1 B_is_liar=1 C_is_liar=1 D_is_liar=1 A_is_culprit=0 B_is_culprit=1 C_is_culprit=0 D_is_culprit=0
> ```

### 実装(線形版)

In [ ]:
```python
_model = cp_model.CpModel()
_liar = {_s: _model.new_bool_var(f'{_s}_is_liar') for _s in suspects}
_culprit = {_s: _model.new_bool_var(f'{_s}_is_culprit') for _s in suspects}
for _s in suspects:
    _model.add(_culprit[_s] <= _liar[_s])
_model.add(1 - _liar['A'] == _culprit['A'])
_y = _model.new_bool_var('(culprits<=2)')
_z = _model.new_bool_var('(culprits>=2)')
_m = 10
_model.add(sum((_culprit[_s] for _s in suspects)) <= 2 + _m * (1 - _y))
_model.add(sum((_culprit[_s] for _s in suspects)) - 1 >= 2 - _m * _y)
_model.add(2 <= sum((_culprit[_s] for _s in suspects)) + _m * (1 - _z))
_model.add(2 - 1 >= sum((_culprit[_s] for _s in suspects)) - _m * _z)
_model.add(1 - _liar['B'] + 1 >= _y + _z)
_model.add(2 * (1 - _liar['B']) <= _y + _z)
_model.add(1 - _liar['C'] <= _culprit['C'] + _culprit['D'])
_model.add(2 * (1 - _liar['C']) >= _culprit['C'] + _culprit['D'])
_e = _model.new_bool_var('n_liar_is_even')
_o = _model.new_bool_var('n_liar_is_odd')
_model.add(_e + _o == 1)
_model.add(_liar['D'] == _e)
_se = _model.new_int_var(0, len(_liar) // 2, 'n_liar//2')
_model.add(sum((_liar[_s] for _s in suspects)) == 2 * _se + _o)
_model.add(sum((_culprit[_s] for _s in suspects)) >= 1)

_solver = cp_model.CpSolver()
_solution_printer = VarArraySolutionPrinter(list(_liar.values()) + list(_culprit.values()))
_solver.parameters.enumerate_all_solutions = True
_status = _solver.solve(_model, _solution_printer)
```

> ```
> A_is_liar=1 B_is_liar=1 C_is_liar=1 D_is_liar=0 A_is_culprit=0 B_is_culprit=1 C_is_culprit=0 D_is_culprit=0 
> A_is_liar=1 B_is_liar=1 C_is_liar=1 D_is_liar=1 A_is_culprit=0 B_is_culprit=1 C_is_culprit=0 D_is_culprit=0
> ```

### 補足

犯人が 1 人以上いると仮定すると犯人は B でそれ以外は無実.
全員が犯人でないケースもあり得たが今回は除外.
嘘つきかどうかに関しては D 以外は全員嘘つきで確定していて, D は嘘つきでも正直ものでもどちらでも整合する.

`add_modulo_equality()` の引数に式をそのまま入れてしまうと `MODEL_INVALID` になってしまった.
他の関数, 例えば `add_multiplication_equality()` でも同様のことが起こったため,
線形でない制約を追加する際は式を新しい変数に格納してから渡すと安全そう.

また, `add_modulo_equality()` の返り値に `only_enforce_if()` を繋げたら `MODEL_INVALID` となってしまった.
ドキュメントには書かれていなかったが `only_enforce_if()` が使える制約と使えない制約があるようで,
例えば `add_bool_xor()` は明確に

> In contrast to add_bool_or and add_bool_and, it does not support .only_enforce_if().

と書かれている.
(`model.add(a != b)` には `only_enforce_if()` をつなげることができたのでなぜこうなっているかは謎)
