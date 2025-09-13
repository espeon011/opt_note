In [ ]:
```python
import itertools
import util
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# 動的計画法

- 計算量: $O(k^n)$ らしいがこの実装では $O(k^n q n )$ かかる.
- 近似精度: $1$

**記法**

- 文字列 $s$ を $j$ 文字目までと $j+1$ 文字目以降に分けたうちの前半を $s[0..j]$ と書く.
- 文字列集合を $S = \lbrace s_1, \dots, s_n \rbrace$ とする.
- $t = (j_1, \dots, j_n) \ (i \in \lbrace 1, \dots, n \rbrace, \ j_i \in \lbrace 0, \dots, |s_i| \rbrace )$ を transversal と呼ぶ.
- $t = (j_1, \dots, j_n)$ に対して $S_t = \lbrace s_1[0..j_1], \dots, s_n[0..j_n] \rbrace$ と定める.
- $S_t$ に対する SCS の長さを $\lambda(t)$ と書く.
- $t = (j_1, \dots, j_n)$ に対し, $I = \lbrace 1, \dots, n \rbrace$ 上の同値関係として $S_t$ 内の文字列 $s_{i_1}$ と $s_{i_2}$ の最後の文字が等しいときかつその時に限り $i_1 \sim i_2$ とするものを考え, その商集合を $E_t$ と書く.
- 上記同値関係の同値類 $K \in E_t$ は特定の文字と対応する. それを $\beta_K$ と書く.
- $K \in E_t$ に対し, $S_t$ において最後の文字が $\beta_k$ である文字のインデックス $i$ に対して $j_i$ を $j_i - 1$ で更新した transversal を $t_K$ と書く.

**遷移**

- 最終的に求めたい SCS 長は right transversal $T = (|s_1|, \dots, |s_n|)$ に対する $\lambda(T)$.
- Base Case として left transversal $o = (0, \dots, 0)$ に対する $\lambda(o) = 0$ がある.
- 次の漸化式が成り立つ: $\lambda(t) = \min \lbrace \lambda(t_K) \ | \ K \in E_t \rbrace + 1$. ただし $t \ne o$.

In [ ]:
```python
def solve(instance: list[str]) -> str:
    chars = sorted(list(set("".join(instance))))

    dp = {(0,) * len(instance): (0, None)}
    for transversal in itertools.product(*[range(len(s) + 1) for s in instance]):
        if transversal in dp:
            continue

        end_chars = set(
            s[t - 1] for s, t in zip(instance, transversal) if t > 0
        )
        pretransversals = [
            tuple(
                t - 1 if t > 0 and s[t - 1] == c else t
                for s, t in zip(instance, transversal)
            )
            for c in end_chars
        ]

        min_transversal = pretransversals[0]
        min_length = dp[min_transversal][0]
        for pretransversal in pretransversals:
            if dp[pretransversal][0] < min_length:
                min_transversal = pretransversal
                min_length = dp[pretransversal][0]

        dp[transversal] = (min_length + 1, min_transversal)

    solution = ""
    left_transversal = (0,) * len(instance)
    right_transversal = tuple(len(s) for s in instance)
    current_transversal = right_transversal
    while current_transversal != left_transversal:
        pretransversal = dp[current_transversal][1]
        c = None
        for s, t1, t2 in zip(instance, current_transversal, pretransversal):
            if t1 == t2 + 1:
                c = s[t2]
                break

        solution += c
        current_transversal = pretransversal

    return solution[::-1]
```

**現実的な時間内に解を求められないため,
小さいインスタンスに対してのみ実行する.**

In [ ]:
```python
_instance = util.parse("uniform_q26n004k015-025.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 62) ---
>  Sol: ulcitkgnycojisoevqfoazkuhmpplxnhtqgbrxzddbxcvsuqpvxirvsnnsbgxf
> str1: ----tkgn--------------kuhmp--xnhtqg--xz-----v-----xi--s-------
> str2: ---i------oji----qfo--------l-n----b-x----xcvsuqpv-i--s--sb-xf
> str3: ulci---nyco--so-v--o-z----ppl-------------------p-------------
> str4: ---i--g--------ev---az------------gbr--ddb-c-s---v--rv-nn--g-f
> 
> solution is feasible: True
> ```

In [ ]:
```python
_instance = util.parse("nucleotide_n005k010.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
```

> ```
> --- Condition (with 4 chars) ---
> str1: ATGGGATACG
> str2: ATACCTTCCC
> str3: CACGAATTGA
> str4: TAAAATCTGT
> str5: AGGTAACAAA
> 
> --- Solution (of length 21) ---
>  Sol: ATGGTACACGATATCTGTACC
> str1: ATGG-----GATA-C-G----
> str2: AT---AC-C--T-TC----CC
> str3: ------CACGA-AT-TG-A--
> str4: -T---A-A--A-ATCTGT---
> str5: A-GGTA-AC-A-A-----A--
> 
> solution is feasible: True
> ```

In [ ]:
```python
_instance = util.parse("protein_n005k010.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
```

> ```
> --- Condition (with 19 chars) ---
> str1: MALSYCPKGT
> str2: MQSSLNAIPV
> str3: MPLSYQHFRK
> str4: MEEHVNELHD
> str5: MSNFDAIRAL
> 
> --- Solution (of length 31) ---
>  Sol: MAPLSYQEEHSSVLNFELHDAICRPKGTVAL
> str1: MA-LSY----------------C-PKGT---
> str2: M-----Q---SS-LN-----AI--P---V--
> str3: M-PLSYQ--H-----F-------R-K-----
> str4: M------EEH--V-N-ELHD-----------
> str5: M---S---------NF---DAI-R-----AL
> 
> solution is feasible: True
> ```
