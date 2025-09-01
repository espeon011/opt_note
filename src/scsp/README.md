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

- `DP` 動的計画法[^5] ([model_dp.ipynb](./__marimo__/model_dp.ipynb))
- `ALPHABET` アルファベットアルゴリズム[^3] ([model_alphabet.ipynb](./__marimo__/model_alphabet.ipynb))
- `MM` Majority Merge アルゴリズム[^1] ([model_mm.ipynb](./__marimo__/model_mm.ipynb))
- `WMM` Weighted Majority Merge アルゴリズム[^4] ([model_wmm.ipynb](./__marimo__/model_wmm.ipynb))
- `IBS_SCS` IBS_SCS アルゴリズム[^2] ([model_ibs_scs.ipynb](./__marimo__/model_ibs_scs.ipynb))
- `DESCENDING` 2 つの文字列の SCS を DP で求める方法を用いて長い方から 2 個ずつマージする方法 ([model_descending.ipynb](./__marimo__/model_descending.ipynb))
- `LINEAR_SCIP` 整数線形計画モデル(SCIP) ([model_linear_scip.ipynb](./__marimo__/model_linear_scip.ipynb))
- `LINEAR_HIGHS` 整数線形計画モデル(HiGHS) ([model_linear_highs.ipynb](./__marimo__/model_linear_highs.ipynb))
- `LINEAR_CPSAT` 整数線形計画モデル(CP-SAT) ([model_linear_cpsat.ipynb](./__marimo__/model_linear_cpsat.ipynb))
- `AUTOMATON_CPSAT` オートマトン制約を用いた数理計画モデル(CP-SAT) ([model_automaton_cpsat.ipynb](./__marimo__/model_automaton_cpsat.ipynb))
- `WMM_HEXALY` Weighted Majority Merge アルゴリズムの重みの部分を Hexaly の決定変数で置き換えたもの ([model_wmm_hexaly.ipynb](./__marimo__/model_wmm_hexaly.ipynb))
- `WMM_HEXALY_INIT` 上記モデルにおいて初期重みを `WMM` と同じになるよう設定したもの ([model_wmm_hexaly_init.ipynb](./__marimo__/model_wmm_hexaly_init.ipynb))

## ベンチマーク

数理最適化ソルバーは時間制限を 1 分に設定して実行. (最適化ソルバー側が有利すぎるか...? )

| モデル名 | UNIFORM <br> $q=26$ <br> $15 \leq k \leq 25$ <br> $n=4$ | UNIFORM <br> $q=26$ <br> $15 \leq k \leq 25$ <br> $n=8$ | UNIFORM <br> $q=26$ <br> $15 \leq k \leq 25$ <br> $n=16$ | UNIFORM <br> $q=5$ <br> $k=10$ <br> $n=10$ | UNIFORM <br> $q=5$ <br> $k=10$ <br> $n=50$ | NUCLEOTIDE <br> $k=10$ <br> $n=10$ | NUCLEOTIDE <br> $k=50$ <br> $n=50$ | PROTEIN <br> $k=10$ <br> $n=10$ | PROTEIN <br> $k=50$ <br> $n=50$ |
| :---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DP`              | **62** 🥇 | - | - | - | - | - | - | - | - |
| `ALPHABET`        | 79 | 155 | 256 | 45 | 50 | 39 | 201 | 71 | 782 |
| `MM`              | 74 | 148 | 198 | 32 | 36 | 27 | 150 | 62 | 536 |
| `WMM`             | 75 | 128 | 176 | 32 | 37 | 26 | 146 | 57 | 475 |
| `IBS_SCS`         | 73 | 117 | 163 | 28 | **34** 🥇 | **24** 🥇 | 141 | 51 | 893 |
| `DESCENDING`      | 64 | 108 | 157 | 37 | 71 | 35 | 185 | 53 | 458 |
| `LINEAR_SCIP`     | 70 | 175 | - | 45 | - | 42 | - | 70 | - |
| `LINEAR_HIGHS`    | 75 | 148 | - | 52 | - | 32 | - | 66 | - |
| `LINEAR_CPSAT`    | 66 | 128 | 304 | 28 | 463 | **24** 🥇 | - | 49 | - |
| `AUTOMATON_CPSAT` | 65 | 138 | 245 | 30 | 42 | 25 | - | 45 | - |
| `WMM_HEXALY`      | **62** 🥇 | **102** 🥇 | 155 | **27** 🥇 | **34** 🥇 | **24** 🥇 | **136** 🥇 | **44** 🥇 | 498 |
| `WMM_HEXALY_INIT` | 64 | 105 | **150** 🥇 | **27** 🥇 | **34** 🥇 | **24** 🥇 | 138 | 45 | **454** 🥇 |
| | | | | | | | | | |

TODO: ベンチマーク用インスタンスを増やしてカテゴリ分けする. 

[^1]: Tao Jiang and Ming Li. 1995. On the Approximation of Shortest Common Supersequences and Longest Common Subsequences. SIAM J. Comput. 24, 5 (Oct. 1995), 1122–1139. https://doi.org/10.1137/S009753979223842X. 
[^2]: Sayyed Rasoul Mousavi, Fateme Bahri, Farzaneh Sadat Tabataba, An enhanced beam search algorithm for the Shortest Common Supersequence Problem, Engineering Applications of Artificial Intelligence, Volume 25, Issue 3, 2012, Pages 457-467, ISSN 0952-1976, https://doi.org/10.1016/j.engappai.2011.08.006.
[^3]: Paolo Barone, Paola Bonizzoni, Gianluca Delta Vedova, and Giancarlo Mauri. 2001. An approximation algorithm for the shortest common supersequence problem: an experimental analysis. In Proceedings of the 2001 ACM symposium on Applied computing (SAC '01). Association for Computing Machinery, New York, NY, USA, 56–60. https://doi.org/10.1145/372202.372275
[^4]: Branke, J., Middendorf, M. & Schneider, F. Improved heuristics and a genetic algorithm for finding short supersequences. OR Spektrum 20, 39–45 (1998). https://doi.org/10.1007/BF01545528
[^5]: Timkovskii, V.G. Complexity of common subsequence and supersequence problems and related problems. Cybern Syst Anal 25, 565–580 (1989). https://doi.org/10.1007/BF01075212
