In [ ]:
```python
import random
import string
import pathlib
import functools
import util
```


In [ ]:
```python
import marimo as mo
import nbformat
```


# データ生成用

## 一様ランダム文字列

与えられた文字列集合の中から一様ランダムに文字を抽出して並べることで文字列を生成する.

- $q$: 使用文字種類数.
- $n$: 文字列数.
- $k_{\min}, k_{\max}$: 文字列超上下限. 実際の文字列超はこの範囲から一様ランダムに決める.

低確率で全く同じ文字列が生成される可能性があることに注意.

In [ ]:
```python
def gen_uniform_instance(
    q: int,
    n: int,
    k_min: int,
    k_max: int,
    seed: int = 0,
) -> None:
    assert q >= 1 and q <= 94
    assert n >= 1
    assert k_min >= 1 and k_max >=1
    assert k_min <= k_max

    characters = string.ascii_letters + string.digits + string.punctuation
    random.seed(seed)

    instance: list[str] = []
    for i in range(n):
        k = random.randint(k_min, k_max)
        s = "".join(random.choices(characters[:q], k=k))
        instance.append(s)

    return instance
```


In [ ]:
```python
def write_uniform_instance(
    q: int,
    n: int,
    k_min: int,
    k_max: int,
    seed: int = 0,
) -> None:
    instance = gen_uniform_instance(q, n, k_min, k_max, seed)
    filename = f"uniform_q{q:0>2}n{n:0>3}k{k_min:0>3}-{k_max:0>3}.txt"
    util.save(instance, filename)
```


In [ ]:
```python
write_uniform_instance(q=26, n=2, k_min=15, k_max=25)
write_uniform_instance(q=26, n=4, k_min=15, k_max=25)
write_uniform_instance(q=26, n=8, k_min=15, k_max=25)
write_uniform_instance(q=26, n=16, k_min=15, k_max=25)
write_uniform_instance(q=26, n=32, k_min=15, k_max=25)
write_uniform_instance(q=26, n=64, k_min=15, k_max=25)

write_uniform_instance(q=5, n=10, k_min=10, k_max=10)
write_uniform_instance(q=5, n=50, k_min=10, k_max=10)
write_uniform_instance(q=5, n=100, k_min=10, k_max=10)
write_uniform_instance(q=5, n=500, k_min=10, k_max=10)

write_uniform_instance(q=5, n=10, k_min=20, k_max=20)
write_uniform_instance(q=5, n=50, k_min=20, k_max=20)
write_uniform_instance(q=5, n=100, k_min=20, k_max=20)
write_uniform_instance(q=5, n=500, k_min=20, k_max=20)
```


## ヌクレオチド配列

実際の DNA 配列のデータから適当に切り出して作成する.

[NCBI Virus のページ](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus)から Nucleotide を選択して Download All Results をクリックし,
ランダムサンプル 1000 件をダウンロードしたデータセットに対して文字列長と文字列数を指定して配列の後ろをカットし,
サンプル数を制限する.

また, NCBI ではデータセットのフィルターで下記を指定した.

- Sequence Length: Min 500
- Nucleotide Completeness: complete
- Ambiguous Characters: Max 0

---
上記検索条件を保存した URL: https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&Completeness_s=complete&QualNum_i=0&SLen_i=500%20TO%203000000

アクセス日付: 2025-08-25

In [ ]:
```python
@functools.cache
def read_nucleotide_festa() -> list[str]:
    data_dir = pathlib.Path(__file__).parent / "file" / "ncbi"
    file_path = data_dir / "nucleotide_sequences_20250824_7758219.fasta"

    instance = []
    with open(file_path, mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    started = False
    instance = []
    seq = ""
    for line in lines:
        if line[0] == "\n":
            started = False
            instance.append(seq)
            seq = ""
            continue
        elif line[0] == ">":
            started = True
            continue

        if started:
            seq += line.strip()

    return instance
```


In [ ]:
```python
def gen_nucleotide_instance(n: int, k: int) -> list[str]:
    assert n >= 1 and n <= 1000
    assert k >= 1

    all_instance = list({s[:k] for s in read_nucleotide_festa()})
    assert n <= len(all_instance)

    instance = []
    for seq in all_instance[:n]:
        instance.append(seq.replace("N", "")[:k])

    return instance
```


In [ ]:
```python
def write_nucleotide_instance(n: int, k: int) -> None:
    instance = gen_nucleotide_instance(n, k)
    filename = f"nucleotide_n{n:0>3}k{k:0>3}.txt"
    util.save(instance, filename)
```


### データの重複チェック

In [ ]:
```python
_all_instance = list(set(read_nucleotide_festa()))

print(f"number of unique nucleotide instance: {len(_all_instance)}")
for _k in [10, 50, 100, 500]:
    _instance = list(set([_s[:_k] for _s in _all_instance]))
    print(f"number of unique ncleotide instance (cut to length {_k}): {len(_instance)}")
```


> ```
> number of unique nucleotide instance: 995
> number of unique ncleotide instance (cut to length 10): 239
> number of unique ncleotide instance (cut to length 50): 278
> number of unique ncleotide instance (cut to length 100): 292
> number of unique ncleotide instance (cut to length 500): 401
> 
> ```



### 生成

In [ ]:
```python
write_nucleotide_instance(n=5, k=10)
write_nucleotide_instance(n=10, k=10)
write_nucleotide_instance(n=50, k=10)
write_nucleotide_instance(n=10, k=50)
write_nucleotide_instance(n=50, k=50)
write_nucleotide_instance(n=100, k=50)
write_nucleotide_instance(n=50, k=100)
write_nucleotide_instance(n=100, k=100)
#write_nucleotide_instance(n=500, k=100)
write_nucleotide_instance(n=100, k=500)
#write_nucleotide_instance(n=500, k=500)
```


## プロテイン配列

実際のプロテイン配列からデータを適当に切り出して作成する.

[NCBI Virus のページ](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus)から Nucleotide を選択して Download All Results をクリックし,
ランダムサンプル 1000 件をダウンロードしたデータセットに対して文字列長と文字列数を指定して配列の後ろをカットし,
サンプル数を制限する.

また, NCBI ではデータセットのフィルターで下記を指定した.

- Sequence Length: Min 500
- Nucleotide Completeness: complete
- Ambiguous Characters: Max 0

---

上記検索条件を保存した URL: https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Protein&SLen_i=500%20TO%203000000&Completeness_s=complete&QualNum_i=0

アクセス日付: 2025-08-25

In [ ]:
```python
@functools.cache
def read_protein_festa() -> list[str]:
    data_dir = pathlib.Path(__file__).parent / "file" / "ncbi"
    file_path = data_dir / "protein_sequences_20250824_5673972.fasta"

    instance = []
    with open(file_path, mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    started = False
    instance = []
    seq = ""
    for line in lines:
        if line[0] == "\n":
            started = False
            instance.append(seq)
            seq = ""
            continue
        elif line[0] == ">":
            started = True
            continue

        if started:
            seq += line.strip()

    return instance
```


In [ ]:
```python
def gen_protein_instance(n: int, k: int) -> list[str]:
    assert n >= 1 and n <= 1000
    assert k >= 1

    all_instance = list({s[:k] for s in read_protein_festa()})
    assert n <= len(all_instance)

    instance = []
    for seq in all_instance[:n]:
        instance.append(seq.replace("X", "")[:k])

    return instance
```


In [ ]:
```python
def write_protein_instance(n: int, k: int) -> None:
    instance = gen_protein_instance(n, k)
    filename = f"protein_n{n:0>3}k{k:0>3}.txt"
    util.save(instance, filename)
```


### データの重複チェック

In [ ]:
```python
_all_instance = list(set(read_protein_festa()))

print(f"number of unique protein instance: {len(_all_instance)}")
for k in [10, 50, 100, 500]:
    _instance = list(set([s[:k] for s in _all_instance]))
    print(f"number of unique protein instance (cut to length {k}): {len(_instance)}")
```


> ```
> number of unique protein instance: 701
> number of unique protein instance (cut to length 10): 140
> number of unique protein instance (cut to length 50): 167
> number of unique protein instance (cut to length 100): 198
> number of unique protein instance (cut to length 500): 327
> 
> ```



### 生成

In [ ]:
```python
write_protein_instance(n=5, k=10)
write_protein_instance(n=10, k=10)
write_protein_instance(n=50, k=10)
write_protein_instance(n=10, k=50)
write_protein_instance(n=50, k=50)
write_protein_instance(n=100, k=50)
write_protein_instance(n=50, k=100)
write_protein_instance(n=100, k=100)
#write_protein_instance(n=500, k=100)
write_protein_instance(n=100, k=500)
#write_protein_instance(n=500, k=500)
```

