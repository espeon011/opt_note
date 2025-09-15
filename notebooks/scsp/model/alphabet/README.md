# アルファベットアルゴリズム

- 計算量: $O(qk)$
- 近似精度: $q$

文字種全体を $\Sigma = \lbrace c_1, \dots, c_q \rbrace$ とする. 
与えられた文字列の中で最大の長さ $k$ に対して下記は与えられた文字列全ての supersequence になる: 

$$
(c_1 c_2 \dots c_q)^k
$$

これを解とすることで長さ $qk$ の common supersequence を出力する. 
この長さは文字列の数に直接は依存しない. 

各文字列 $s_i$ の $j$ 番目の文字は上記 $(c_1 c_2 \dots c_q)^k$ の中の $j$ 番目のブロックに対応するが, 
$j$ 番目のブロックの中にはどの文字列でも使用しない文字があるかもしれない. 
そのような文字は捨てることで解を少し改善する. 
これによって解が少し改善するが, 文字列の数が増えると削れる文字が少なくなり, 長さ $qk$ に近づく.

## Python Code

```python
def solve(instance: list[str]) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
    solution = ""

    for i in range(max([len(s) for s in instance])):
        used = [False for _ in chars]
        for s in instance:
            if i >= len(s):
                continue
            used[chars.index(s[i])] = True

        for c, u in zip(chars, used):
            if u:
                solution += c

    return solution
```
