# MILP バイナリ定式化 (SCIP)

## 概要

数理最適化モデルを用いて SCSP を解く. 以下のように定義する.

### 定数

- $m = \sum_{i=1}^n |s_i|$: 共通超配列の長さ上限. 

### 決定変数

- $x_{i,j,l} \in \lbrace 0, 1 \rbrace \ (\forall i \in \lbrace 1, \dots, n \rbrace, \ \forall j \in \lbrace 1, \dots, |s_i| \rbrace, \ \forall l \in \lbrace 1, \dots, m \rbrace)$: $i$ 番目の文字列の $j$ 番目の文字が解において $m$ 番目に対応するときかつそのときに限り $1$ を取る. 
- $y_{l,c} \in \lbrace 0, 1 \rbrace \ (\forall l \in \lbrace 1, \dots, m \rbrace, \ \forall c in \Sigma)$: 超配列の $l$ 番目の文字が $c$ であるときかつそのときに限り $1$ を取る. 
- $z_l \in \lbrace 0, 1, \rbrace \ (\forall l \in \lbrace 1, \dots, m \rbrace)$: 超配列の $l$ 番目が使われるときかつその時に限り $1$ を取る. 

### 制約条件

- $z_l = \sum_{c \in \Sigma} y_{l,c} \ (\forall l \in \lbrace 1, \dots, m \rbrace)$
- $y_{l,c} \geq \sum_{j \in \lbrace 1, \dots, |s_i| \rbrace, \ s_j = c} x_{i,j,l} \ (\forall i \in \lbrace 1, \dots, n \rbrace, \ \forall l \in \lbrace 1, \dots, m \rbrace, \ \forall c in \Sigma)$
- $\sum_{l \in \lbrace 1, \dots, m \rbrace} x_{i,j,l} = 1 \ (\forall i \in \lbrace 1, \dots, n \rbrace, \ \forall j \in \lbrace 1, \dots, |s_i| \rbrace)$
- $\sum_{l \in \lbrace 1, \dots, m \rbrace} l x_{i,j,l} + 1 \leq \sum_{l \in \lbrace 1, \dots, m \rbrace} l x_{i,j+1,l} \ (\forall i \in \lbrace 1, \dots, n \rbrace, \ \forall j \in \lbrace 1, \dots, |s_i| - 1 \rbrace)$

### 目的関数

- minimize $\sum_{l=1}^m z_l$
