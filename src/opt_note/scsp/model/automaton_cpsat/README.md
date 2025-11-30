# オートマトン制約を用いた数理計画モデル

## 概要

CP-SAT 固有のオートマトン制約を用いて定式化してみる.

### 定数

- $\Sigma = \lbrace \sigma_1, \dots, \sigma_q \rbrace$: 文字の集合

### 決定変数

- $x_i \in \mathbb{Z}$: 解において $i$ 番目の文字が $\sigma_j$ であれば $j$ となる.
  どの文字も対応しないとき $0$.
  このとき解は $\sigma_{x_0} \sigma_{x_1} \dots$ となる.
  ただし $\sigma_0$ は空文字列とする.
- $v_i \in \lbrace 0, 1 \rbrace$: 解の $i$ 番目が空でないとき $1$. 空のとき $0$.

### 制約条件

- $x_i > 0 \Rightarrow v_i = 1$
- 与えられた文字列 $s \in S$ の各文字を $\Sigma$ を基準にインデックスの配列としたものを $\mathrm{index}_s$ とする.
  $\mathrm{index}_s$ を部分配列にもつすべての配列を受理するオートマトンを文字列の数だけ作成し,
  $\lbrace x_i \rbrace_i$ が受理されるという制約を課す.

### 目的関数

- minimize $\sum_{i} v_i$
