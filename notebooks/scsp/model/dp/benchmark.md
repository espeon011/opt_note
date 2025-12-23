In [ ]:
```python
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# ベンチマーク

In [ ]:
```python
Model = scsp.model.dp.Model
```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
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
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 1.151772s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="protein_n010k010.txt")
```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
