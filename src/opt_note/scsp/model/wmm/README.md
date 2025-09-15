# Weighted Majority Merge アルゴリズム[^1]

- 計算量: ?
- 近似精度: なし

与えられた文字列たちの先頭の文字列を調べ, 優先度の高い順に採用していく流れは Majority Merge と同じ.
Weighted Majority Merge では出現するか否かの代わりに残された文字列長を考えた重み付き出現回数を採用する.

- 解 $\mathrm{sol}$ を空文字列で初期化する.
- 各文字 $c$ に対し重要度 $\sum_{i=1, \ s_i[0] = c}^n |s_i|$ を計算し, 重要度が最大である $c$ を求める.
- $\mathrm{sol}$ の後ろに $c$ を追加する.
- 各文字列 $s_1, s_2, \dots, s_n$ に対し, 先頭の文字が $c$ である場合は先頭 1 文字を削除する.
- $s_1, s_2, \dots, s_n$ が全て空文字列になれば終了.

[^1]: Branke, J., Middendorf, M. & Schneider, F. Improved heuristics and a genetic algorithm for finding short supersequences. OR Spektrum 20, 39–45 (1998). https://doi.org/10.1007/BF01545528
