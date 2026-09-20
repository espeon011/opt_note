# DIDP with char count bound

## 概要

`DIDP` モデルの dual bound に文字ごとの残出現数から決まる下界で置き換えてみる.

共通超配列は各文字 $c$ について,
どの文字列の残り部分に含まれる $c$ の個数よりも多くの $c$ を含んでいなければならない.
したがって状態 $(i_1, \dots, i_n)$ における

$$
\sum_{c \in \Sigma} \max_{j} \\#\\{ l \geq i_j \mid s_j[l] = c \\}
$$

は残りの長さの下界になる.
