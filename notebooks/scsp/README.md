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

- `DP` 動的計画法[^5] ([概要](./model/dp))
- `ALPHABET` アルファベットアルゴリズム[^3] ([概要](./model/alphabet))
- `MM` Majority Merge アルゴリズム[^1] ([概要](./model/mm))
- `WMM` Weighted Majority Merge アルゴリズム[^4] ([概要](./model/wmm))
- `LA_SH` Look-Ahead Sum-Height アルゴリズム[^7] ([概要](./model/la_sh))
- `IBS_SCS` IBS_SCS アルゴリズム[^2] ([概要](./model/ibs_scs))
- `DESCENDING` 2 つの文字列の SCS を DP で求める方法を用いて長い方から 2 個ずつマージする方法 ([概要](./model/descending))
- `LINEAR_SCIP` 整数線形計画モデル(SCIP) ([概要](./model/linear_scip))
- `LINEAR_HIGHS` 整数線形計画モデル(HiGHS) ([概要](./model/linear_highs))
- `LINEAR_CPSAT` 整数線形計画モデル(CP-SAT) ([概要](./model/linear_cpsat))
- `AUTOMATON_CPSAT` オートマトン制約を用いた数理計画モデル(CP-SAT) ([概要](./model/automaton_cpsat))
- `WMM_HEXALY` Weighted Majority Merge アルゴリズムの重みの部分を Hexaly の決定変数で置き換えたもの ([概要](./model/wmm_hexaly))
- `WMM_HEXALY_INIT` 上記モデルにおいて初期重みを `WMM` と同じになるよう設定したもの ([概要](./model/wmm_hexaly_init))
- `DIDP` DIDP ソルバーを用いた定式化[^8][^6] ([概要](./model/didp))

## ベンチマーク

数理最適化ソルバーは時間制限を 1 分に設定して実行. (最適化ソルバー側が有利すぎるか...? )

| モデル名 | UNIFORM <br> $q=26$ <br> $15 \leq k \leq 25$ <br> $n=4$ | UNIFORM <br> $q=26$ <br> $15 \leq k \leq 25$ <br> $n=8$ | UNIFORM <br> $q=26$ <br> $15 \leq k \leq 25$ <br> $n=16$ | UNIFORM <br> $q=5$ <br> $k=10$ <br> $n=10$ | UNIFORM <br> $q=5$ <br> $k=10$ <br> $n=50$ | NUCLEOTIDE <br> $k=10$ <br> $n=10$ | NUCLEOTIDE <br> $k=50$ <br> $n=50$ | PROTEIN <br> $k=10$ <br> $n=10$ | PROTEIN <br> $k=50$ <br> $n=50$ |
| :---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ALPHABET`        | 79 | 155 | 256 | 45 | 50 | 39 | 201 | 71 | 782 |
| `MM`              | 74 | 148 | 198 | 32 | 36 | 27 | 150 | 62 | 536 |
| `WMM`             | 75 | 128 | 176 | 32 | 37 | 26 | 146 | 57 | 475 |
| `LA_SH`           | 70 | 132 | 170 | 31 | 38 | 28 | 144 | 51 | 497 |
| `IBS_SCS`         | 73 | 119 | 163 | 28 | **34** 🥇 | **24** 🥇 | 135 | 49 | 876 |
| `DESCENDING`      | 64 | 108 | 157 | 37 | 71 | 35 | 185 | 53 | 458 |
| `LINEAR_SCIP`     | 70 | 175 | - | 45 | - | 42 | - | 70 | - |
| `LINEAR_HIGHS`    | 75 | 148 | - | 52 | - | 32 | - | 66 | - |
| `LINEAR_CPSAT`    | 66 | 135 | 293 | 29 | 226 | **24** 🥇 | - | 51 | - |
| `AUTOMATON_CPSAT` | 67 | 135 | 242 | 29 | 40 | 25 | - | 46 | - |
| `WMM_HEXALY`      | **62** 🥇 | 102 | 156 | **27** 🥇 | **34** 🥇 | **24** 🥇 | 136 | **44** 🥇 | 498 |
| `WMM_HEXALY_INIT` | 64 | 105 | 150 | **27** 🥇 | **34** 🥇 | **24** 🥇 | 138 | 45 | **454** 🥇 |
| `DIDP`            | **62*** 🥇 | **99** 🥇 | **149** 🥇 | **27*** 🥇 | **34** 🥇 | **24*** 🥇 | **133** 🥇 | **44** 🥇 | 503 |
| | | | | | | | | | |

- Hexaly を使ったものはライセンスされた別の PC で実行. 
- 「*」 マークがついているものは最適性の証明ができたもの.
- パラメータを持つアルゴリズムについては下記の設定で実行
  - `IBS_SCS` $\beta = 100$, $\kappa = 7$. 
  - `LA_SH` $m = 3$, $l = 1$.
- 下記モデルは性能の問題により表から除外.
  - `DP`
- TODO: ベンチマーク用インスタンスを増やしてカテゴリ分けする. 

## 解法の分類

### 解の構成法

- 前から1文字ずつ取ってきて構成する ... `DP`, `MM`, `WMM`, `LA_SH`, `IBS_SCS`, `WMM_HEXALY`, `WMM_HEXALY_INIT`, `DIDP`
- その他 ... `ALPHABET`, `DESCENDING`, `LINEAR_SCIP`, `LINEAR_HIGHS`, `LINEAR_CPSAT`, `AUTOMATON_CPSAT`

### 探索法

- 貪欲 ... `ALPHABET`, `MM`, `WMM`, `LA_SH`, `DESCENDING`
- ビームサーチ ... `IBS_SCS`, `DIDP`
- 全探索 ... `DP`, `DIDP`, `LINEAR_SCIP`, `LINEAR_HIGHS`, `LINEAR_CPSAT`, `AUTOMATON_CPSAT`
- アニーリング? ... `WMM_HEXALY`, `WMM_HEXALY_INIT`

| 探索法\解の構築法 | 前から1文字ずつ取ってくる | その他 |
| --- | --- | --- |
| 貪欲 | `MM`, `WMM`, `LA_SH` | `ALPHABET`, `DESCENDING` |
| ビームサーチ | `IBS_SCS`, `DIDP` | |
| 全探索 | `DP`, `DIDP` | `LINEAR_SCIP`, `LINEAR_HIGHS`, `LINEAR_CPSAT`, `AUTOMATON_CPSAT` |
| アニーリング? | `WMM_HEXALY`, `WMM_HEXALY_INIT` | |

[^1]: Tao Jiang and Ming Li. 1995. On the Approximation of Shortest Common Supersequences and Longest Common Subsequences. SIAM J. Comput. 24, 5 (Oct. 1995), 1122–1139. https://doi.org/10.1137/S009753979223842X. 
[^2]: Sayyed Rasoul Mousavi, Fateme Bahri, Farzaneh Sadat Tabataba, An enhanced beam search algorithm for the Shortest Common Supersequence Problem, Engineering Applications of Artificial Intelligence, Volume 25, Issue 3, 2012, Pages 457-467, ISSN 0952-1976, https://doi.org/10.1016/j.engappai.2011.08.006.
[^3]: Paolo Barone, Paola Bonizzoni, Gianluca Delta Vedova, and Giancarlo Mauri. 2001. An approximation algorithm for the shortest common supersequence problem: an experimental analysis. In Proceedings of the 2001 ACM symposium on Applied computing (SAC '01). Association for Computing Machinery, New York, NY, USA, 56–60. https://doi.org/10.1145/372202.372275
[^4]: Branke, J., Middendorf, M. & Schneider, F. Improved heuristics and a genetic algorithm for finding short supersequences. OR Spektrum 20, 39–45 (1998). https://doi.org/10.1007/BF01545528
[^5]: Timkovskii, V.G. Complexity of common subsequence and supersequence problems and related problems. Cybern Syst Anal 25, 565–580 (1989). https://doi.org/10.1007/BF01075212
[^6]: https://github.com/okaduki/opt100, 2025-09-09 アクセス. 
[^7]: Ning, K., Choi, K. P., Leong, H. W., & Zhang, L. (2005). A post-processing method for optimizing synthesis strategy for oligonucleotide microarrays. Nucleic acids research, 33(17), e144. https://doi.org/10.1093/nar/gni147
[^8]: https://zenn.dev/okaduki/articles/7f9a3f3c54bc98, 2025-09-09 アクセス. 
