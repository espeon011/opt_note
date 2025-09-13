In [ ]:
```python
import model_didp2
import util
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# 計算時間は度外視して最適値が知りたい

In [ ]:
```python
instance = [
    "aehdmmqrstuwv",
    "afiknllppaavxusqszab",
    "bgglopqsssv",
    "cabhiknaampawqryssuv",
    "dbhciknddmpdqryssuwc",
    "cajhiknapasqrssuvv",
    "dacngoaiatsimawxltsc",
    "zbndjkozfrizsyctviw",
]
model = model_didp2.Model(instance)
solution = model.solve(time_limit=1800, log=True).to_solution()
```

> ```
> Solver: CABS from DIDPPy v0.10.0
> Searched with beam size: 1, threads: 12, kept: 450, sent: 0
> Searched with beam size: 1, expanded: 80, elapsed time: 0.001608304
> New primal bound: 80, expanded: 80, elapsed time: 0.001610638
> Searched with beam size: 2, threads: 12, kept: 375, sent: 393
> Searched with beam size: 2, expanded: 221, elapsed time: 0.002939492
> New dual bound: 46, expanded: 221, elapsed time: 0.002940253
> Searched with beam size: 4, threads: 12, kept: 372, sent: 1218
> Searched with beam size: 4, expanded: 512, elapsed time: 0.004728549
> New primal bound: 75, expanded: 512, elapsed time: 0.004830523
> Searched with beam size: 8, threads: 12, kept: 368, sent: 2824
> Searched with beam size: 8, expanded: 1074, elapsed time: 0.088721171
> New primal bound: 74, expanded: 1074, elapsed time: 0.088813396
> Searched with beam size: 16, threads: 12, kept: 483, sent: 5356
> Searched with beam size: 16, expanded: 2062, elapsed time: 0.158398627
> Searched with beam size: 32, threads: 12, kept: 918, sent: 10987
> Searched with beam size: 32, expanded: 4203, elapsed time: 0.22616828
> New dual bound: 47, expanded: 4203, elapsed time: 0.226170053
> New primal bound: 69, expanded: 4203, elapsed time: 0.226260996
> Searched with beam size: 64, threads: 12, kept: 1847, sent: 20988
> Searched with beam size: 64, expanded: 8268, elapsed time: 0.235997397
> New primal bound: 66, expanded: 8268, elapsed time: 0.236141771
> Searched with beam size: 128, threads: 12, kept: 3133, sent: 35274
> Searched with beam size: 128, expanded: 14741, elapsed time: 0.250773439
> New dual bound: 48, expanded: 14741, elapsed time: 0.250774421
> Searched with beam size: 256, threads: 12, kept: 6898, sent: 77330
> Searched with beam size: 256, expanded: 29649, elapsed time: 0.282091556
> New dual bound: 49, expanded: 29649, elapsed time: 0.282092588
> New primal bound: 64, expanded: 29649, elapsed time: 0.282164755
> Searched with beam size: 512, threads: 12, kept: 12959, sent: 143435
> Searched with beam size: 512, expanded: 57506, elapsed time: 0.339744615
> New dual bound: 50, expanded: 57506, elapsed time: 0.339745647
> New primal bound: 62, expanded: 57506, elapsed time: 0.33981536
> Searched with beam size: 1024, threads: 12, kept: 21659, sent: 239001
> Searched with beam size: 1024, expanded: 102264, elapsed time: 0.434250423
> Searched with beam size: 2048, threads: 12, kept: 42137, sent: 467335
> Searched with beam size: 2048, expanded: 188672, elapsed time: 0.61596504
> New dual bound: 51, expanded: 188672, elapsed time: 0.615966303
> Searched with beam size: 4096, threads: 12, kept: 82256, sent: 908332
> Searched with beam size: 4096, expanded: 356154, elapsed time: 0.983001025
> Searched with beam size: 8192, threads: 12, kept: 159990, sent: 1767672
> Searched with beam size: 8192, expanded: 679814, elapsed time: 1.6689851500000001
> New dual bound: 52, expanded: 679814, elapsed time: 1.6689868030000001
> Searched with beam size: 16384, threads: 12, kept: 309945, sent: 3415054
> Searched with beam size: 16384, expanded: 1303116, elapsed time: 3.038070554
> New dual bound: 53, expanded: 1303116, elapsed time: 3.038073329
> Searched with beam size: 32768, threads: 12, kept: 595796, sent: 6569149
> Searched with beam size: 32768, expanded: 2497248, elapsed time: 5.758296379
> Searched with beam size: 65536, threads: 12, kept: 1138104, sent: 12535716
> Searched with beam size: 65536, expanded: 4770268, elapsed time: 11.19765398
> New dual bound: 54, expanded: 4770268, elapsed time: 11.197656545
> Searched with beam size: 131072, threads: 12, kept: 2155524, sent: 23739899
> Searched with beam size: 131072, expanded: 9063125, elapsed time: 21.743439098
> New dual bound: 55, expanded: 9063125, elapsed time: 21.743440992
> Searched with beam size: 262144, threads: 12, kept: 4053953, sent: 44599277
> Searched with beam size: 262144, expanded: 17101987, elapsed time: 41.978211971
> New dual bound: 56, expanded: 17101987, elapsed time: 41.978214827
> Searched with beam size: 524288, threads: 12, kept: 7498746, sent: 82443237
> Searched with beam size: 524288, expanded: 31991682, elapsed time: 80.545532599
> New dual bound: 57, expanded: 31991682, elapsed time: 80.545534903
> Searched with beam size: 1048576, threads: 12, kept: 13618221, sent: 149704037
> Searched with beam size: 1048576, expanded: 59214685, elapsed time: 153.4048695
> New dual bound: 58, expanded: 59214685, elapsed time: 153.404871675
> Searched with beam size: 2097152, threads: 12, kept: 23885940, sent: 262634307
> Searched with beam size: 2097152, expanded: 107392634, elapsed time: 286.450816385
> New dual bound: 59, expanded: 107392634, elapsed time: 286.450818799
> Searched with beam size: 4194304, threads: 12, kept: 39595249, sent: 435508298
> Searched with beam size: 4194304, expanded: 189866744, elapsed time: 518.833821321
> New dual bound: 60, expanded: 189866744, elapsed time: 518.833823575
> Searched with beam size: 8388608, threads: 12, kept: 51965294, sent: 571625351
> Searched with beam size: 8388608, expanded: 318541616, elapsed time: 869.394033316
> New dual bound: 61, expanded: 318541616, elapsed time: 869.39403548
> Searched with beam size: 16777216, threads: 12, kept: 53795141, sent: 591728481
> Searched with beam size: 16777216, expanded: 458450774, elapsed time: 1245.773937496
> ```

In [ ]:
```python
util.show(instance)
if solution is not None:
    util.show(instance, solution)
    print(f"solution is feasible: {util.is_feasible(instance, solution)}")
    print(f"solution is optimal: {model.solution.is_optimal}")
    print(f"best bound: {model.solution.best_bound}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 26 chars) ---
> str1: aehdmmqrstuwv
> str2: afiknllppaavxusqszab
> str3: bgglopqsssv
> str4: cabhiknaampawqryssuv
> str5: dbhciknddmpdqryssuwc
> str6: cajhiknapasqrssuvv
> str7: dacngoaiatsimawxltsc
> str8: zbndjkozfrizsyctviw
> 
> --- Solution (of length 62) ---
>  Sol: dzcaejbhfciknlggdljkpopaizatfvsdimpdawxumsqryiszsycltuviwascbv
> str1: ---ae--h--------d----------------m------m-qr--s-----tu--w----v
> str2: ---a----f-iknl---l--p-pa--a--v--------xu-sq---sz---------a--b-
> str3: ------b-------gg-l---op-------------------q---s-s---------s--v
> str4: --ca--bh--ikn----------a--a------mp-aw----qry-s-s----uv-------
> str5: d-----bh-cikn---d--------------d-mpd------qry-s-s----u--w--c--
> str6: --ca-j-h--ikn----------a----------p-a----sqr--s-s----uv------v
> str7: d--a-----c--n-g------o-ai-at--s-im--awx------------lt-----sc--
> str8: -z----b-----n---d-jk-o---z--f--------------r-i-zsyc-t-viw-----
> 
> solution is feasible: True
> solution is optimal: True
> best bound: 62
> ```

計算時間は 20 分 46 秒だった.
