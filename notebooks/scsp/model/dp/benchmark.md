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
def bench(instance: list[str]) -> None:
    solution = scsp.model.dp.solve(instance)
    scsp.util.show(instance)
    scsp.util.show(instance, solution)
    print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
```

**現実的な時間内に解を求められないため, 小さいインスタンスに対してのみ実行する**.

In [ ]:
```python
bench(scsp.example.load("uniform_q26n004k015-025.txt"))
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
bench(scsp.example.load("nucleotide_n005k010.txt"))
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
bench(scsp.example.load("protein_n005k010.txt"))
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
