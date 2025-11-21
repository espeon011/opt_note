# Deposition and Reduction アルゴリズム[^1]

- 計算量: Deposition プロセス, Reduction プロセスに採用したアルゴリズムに依存. 
- 近似精度: Deposition プロセスに採用したアルゴリズムに近似精度があればそれがこのアルゴリズムの近似精度となる. 

Deposition and Reduction アルゴリズムでは Deposition プロセスでテンプレートを生成した後,
Reduction プロセスでテンプレートの部分配列を求めることでより短い共通超配列を求める. 

## Deposition プロセス

Deposition プロセスでは何かしらのアルゴリズムで共通超配列を 1 つ以上与える. 

元論文ではアルファベットアルゴリズムと Look-Ahead Sum-Height アルゴリズムの 2 つによって 2 つのテンプレートを作成していた. 
しかしこれは近似精度をアルファベットアルゴリズムの $q$ で上から抑えるためであり,
実質的には Deposition プロセスに採用するアルゴリズムを変更して 2 回実行していたにすぎない. 
この実装では Deposition プロセスに採用できるアルゴリズムは 1 つであるとし,
デフォルトは $(3, 1)$-LA-SH とする. 

## Reduction プロセス

Reduction プロセスでは Deposition プロセスで作成した共通超配列を以下のように削減する. 

- $\mathrm{sol}$ を Deposition プロセスで作成した解, $m$ をその長さとする. 
- $i = 1, \dots, m$ に対して下記を調べる. 
  - 解を $\mathrm{sol}_l = \mathrm{sol}[0 .. i]$, $\mathrm{sol}_r = \mathrm{sol}[i .. m]$ の 2 つに分割する. 
  - インスタンス内の各文字列 $s \in S$ に対して $s[j_s .. |s|]$ が $\mathrm{sol}_r$ の部分配列となる最小の $j_s$ を求める. 
  - Reduction プロセスに採用したアルゴリズムで $\lbrace s_1[j_1 .. |s_1|], \dots, s_n[j_n .. |s_n|] \rbrace$ に対する共通超配列 $\mathrm{sol}_l'$ を求め,
    $\mathrm{sol}$ を $\mathrm{sol}_l'$ と $\mathrm{sol}_r$ を結合したもので置き換える. 
- 上記を更新が無くなるまで繰り返す. 

この実装ではタイムリミットが設定できるようにし,
タイムリミットを超えている場合は更新があった場合でも Reduction プロセスを終了する. 

[^1]: Ning, K., Leong, H.W. Towards a better solution to the shortest common supersequence problem: the deposition and reduction algorithm. BMC Bioinformatics 7 (Suppl 4), S12 (2006). https://doi.org/10.1186/1471-2105-7-S4-S12

## Python Code

```python
from collections.abc import Callable
from typing import Protocol
import datetime
from .. import la_sh


def longest_suffix_index(s1: str, s2: str) -> int:
    """
    `s1[idx:]` が `s2` の部分配列となるもののうち最小の idx を返す.
    (つまり `s1[idx:]` が最長となるようにする. )
    """

    next = len(s1) - 1
    for c in reversed(s2):
        if next == -1:
            break
        if s1[next] == c:
            next -= 1

    return next + 1


def original_reduction(
    instance: list[str],
    template: str,
    time_limit: int | None = 60,
    solve_func: Callable[[list[str]], str | None] = la_sh.solve,
) -> str | None:
    start = datetime.datetime.now()
    if time_limit is not None:
        limit = start + datetime.timedelta(seconds=time_limit)
    else:
        limit = None

    update = True
    while update:
        update = False
        for i in range(len(template)):
            now = datetime.datetime.now()
            if limit is not None and now >= limit:
                break

            right = template[i + 1 :]

            remaining_prefixes = list(
                filter(
                    lambda s: len(s) > 0,
                    [s[: longest_suffix_index(s, right)] for s in instance],
                )
            )
            if len(remaining_prefixes) == 0:
                left = ""
            else:
                left = solve_func(remaining_prefixes)

            if left is None:
                break

            if len(left) < i + 1:
                update = True
                template = left + right
                break

        if not update:
            break

    return template


class DepositionFuncType(Protocol):
    def __call__(self, instance: list[str]) -> str | None: ...


class ReductionFuncType(Protocol):
    def __call__(
        self,
        instance: list[str],
        template: str,
        time_limit: int | None = 60,
    ) -> str | None: ...


def solve(
    instance: list[str],
    time_limit: int | None = 60,
    deposition: DepositionFuncType = la_sh.solve,
    reduction: ReductionFuncType = original_reduction,
) -> str | None:
    template = deposition(instance)
    if template is None:
        return None

    return reduction(instance, template, time_limit)
```
