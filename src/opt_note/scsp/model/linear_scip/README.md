# MILP 定式化 (SCIP)

数理最適化モデルを用いて SCSP を解く. 以下のように定義する.

**決定変数**

- $x_{i,j} \in \mathbb{N} \ (\forall i \in \lbrace 1, \dots, n \rbrace, \ \forall j \in \lbrace 1, \dots, |s_i| \rbrace)$: $i$ 番目の文字列の $j$ 番目の文字が解において何番目に対応するか.

**制約条件**

- $x_{i,j} < x_{i,j+1} \ (\forall i \in \lbrace 1, \dots, n \rbrace, \ \forall j \in \lbrace 1, \dots, |s_i| - 1 \rbrace)$
- $i_1, i_2 \in \lbrace 1, \dots, n \rbrace \ (i_1 \ne i_2)$ と $j_1 \in \lbrace 1, \dots, |s_{i_1}| \rbrace, \ j_2 \in \lbrace 1, \dots, |s_{i_2}| \rbrace$ に対し,
  $s_{i_1}[j_1] \ne s_{i_2}[j_2]$ ならば $x_{i_1, j_1} \ne x_{i_2, j_2}$.

**目的関数**

- minimize $\max_{i = 1, \dots, n} x_{i, |s_i|}$
