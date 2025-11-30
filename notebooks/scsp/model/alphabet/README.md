# アルファベットアルゴリズム

## 概要

- 計算量: $O(qk)$
- 近似精度: $q$

文字種全体を $\Sigma = \lbrace c_1, \dots, c_q \rbrace$ とする. 
与えられた文字列の中で最大の長さ $k$ に対して下記は与えられた文字列全ての supersequence になる: 

$$
(c_1 c_2 \dots c_q)^k
$$

これを解とすることで長さ $qk$ の common supersequence を出力する. 
この長さは文字列の数に直接は依存しない. 

## 参考

1. Paolo Barone, Paola Bonizzoni, Gianluca Delta Vedova, and Giancarlo Mauri. 2001. An approximation algorithm for the shortest common supersequence problem: an experimental analysis. In Proceedings of the 2001 ACM symposium on Applied computing (SAC '01). Association for Computing Machinery, New York, NY, USA, 56–60. https://doi.org/10.1145/372202.372275

## Python Code

```python
from dataclasses import dataclass


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, *args, **kwargs) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        self.solution = chars * max([len(s) for s in self.instance])
        return self.solution
```
