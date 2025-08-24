# Shortest Common Supersequence Problem

Shortest Common Supersequence Problem (SCSP) は与えられた複数の配列に対し,
その全てを部分配列に持つ配列 (共通超配列) の中で長さが最小のものを見つける問題. 

この問題は ($\mathrm{P} = \mathrm{NP}$ でなければ) 多項式時間線形近似アルゴリズムを持たない事が示されており[^1], 
本質的に難しい問題である. 

## 記号

- $\Sigma$: アルファベットの集合
- $S = \\{ s_1, \dots, s_n \\}$: 文字列の集合
- $q = |\Sigma|$: アルファベットの数
- $k = \max_{s \in S} |s|$: 最大文字列長
- $n = |S|$: 文字列の数

## モデル

- [アルファベットアルゴリズム](./__marimo__/model_alphabet.ipynb)
- [長い方から 2 個ずつマージする方法](./__marimo__/model_descending.ipynb)
- [Majority Merge](./__marimo__/model_mm.ipynb)
- [Weighted Majority Merge](./__marimo__/model_wmm.ipynb)
- [IBS_SCS](./__marimo__/model_ibs_scs.ipynb)[^2]
- [線形計画問題(SCIP)](./__marimo__/model_linear_scip.ipynb)

[^1]: Tao Jiang and Ming Li. 1995. On the Approximation of Shortest Common Supersequencesand Longest Common Subsequences. SIAM J. Comput. 24, 5 (Oct. 1995), 1122–1139. https://doi.org/10.1137/S009753979223842X. 
[^2]: Sayyed Rasoul Mousavi, Fateme Bahri, Farzaneh Sadat Tabataba, An enhanced beam search algorithm for the Shortest Common Supersequence Problem, Engineering Applications of Artificial Intelligence, Volume 25, Issue 3, 2012, Pages 457-467, ISSN 0952-1976, https://doi.org/10.1016/j.engappai.2011.08.006.
