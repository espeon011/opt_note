# Weighted Majority Merge をパラメータ化し, Hexaly で探索

## 概要

Hexaly の外部関数最適化機能を用いた定式化を紹介する.
Weighted Majority Merge アルゴリズムにおいて次の文字を選択する基準は各文字列に対する残長の和であった.
その残長の部分を Hexaly の決定変数で置き換える.

### 決定変数

- $w_{ij} \in \mathbb{N}$: 文字列 $s_i$ の $j$ 文字目の重み. $(i \in \lbrace 1, \dots, n \rbrace, \ j \in \lbrace 1, \dots, |s_i| \rbrace)$
    - $w_i = \lbrace w_{i,1} \dots, w_{i,|s_i|} \rbrace$ とおく.

### 目的関数

下記のアルゴリズムに従って構築した共通超配列の長さを目的関数とする.

- 解 $\mathrm{sol}$ を空文字列で初期化する.
- 各文字 $c$ に対して重み $\sum_{i=1, \ s_i[0] = c}^n w_{i,1}$ を計算し, 重みが最大である $c$ を求める.
- $\mathrm{sol}$ の後ろに $c$ を追加する.
- 各文字列 $s_i \ (i \in \lbrace 1, \dots, n \rbrace)$ に対し, 先頭の文字が $c$ である場合は
    - $s_i$ の先頭の文字を削除する.
    - $w_i$ の先頭の重みを削除し, インデックスを前に詰める.
- $s_1, \dots, s_n$ 全てが空文字列になれば終了. $\mathrm{sol}$ が解.
