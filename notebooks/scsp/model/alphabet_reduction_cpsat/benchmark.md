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

## 注意点

Dual bound を表示しているが, これはアルファベットアルゴリズムで構築した解の部分配列の中で最短のものを求める問題の dual bound であり, 与えられた SCSP に対する dual bound ではない事に注意.

最適性に関しても同様で, `OPTIMAL` と出ている場合はアルファベットアルゴリズムで構築した解の部分列の中では最短であるというだけであり, 実際に最短とは限らない.

実際に簡単なケースで実験をする.
`ba`, `cb` の最短共通超配列は `cba` である:

In [ ]:
```python
_instance = ["ba", "cb"]
_model = scsp.model.didp.Model(_instance).solve()
_solution = _model.to_solution()
scsp.util.show(_instance)
scsp.util.show(_instance, _solution)

print(f"solution is optimal: {_model.solution.is_optimal}")
print(f"bset bound: {_model.solution.best_bound}")
```

> ```
> --- Condition (with 3 chars) ---
> str1: ba
> str2: cb
> 
> --- Solution (of length 3) ---
>  Sol: cba
> str1: -ba
> str2: cb-
> 
> solution is optimal: True
> bset bound: 3
> ```

一方, この方法では長さが 4 の共通超配列が最適となってしまう:

## 本題

In [ ]:
```python
_instance = ["ba", "cb"]
_model = scsp.model.alphabet_reduction_cpsat.Model(_instance).solve()
_solution = _model.to_solution()
scsp.util.show(_instance)
scsp.util.show(_instance, _solution)

print(f"solution status: {_model.cpsolver.status_name()}")
print(f"best bound: {_model.cpsolver.best_objective_bound}")
```

> ```
> --- Condition (with 3 chars) ---
> str1: ba
> str2: cb
> 
> --- Solution (of length 4) ---
>  Sol: bcab
> str1: b-a-
> str2: -c-b
> 
> solution status: OPTIMAL
> best bound: 4.0
> ```

In [ ]:
```python
def bench(instance: list[str]) -> None:
    model = scsp.model.alphabet_reduction_cpsat.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"best bound: {model.cpsolver.best_objective_bound}")
```

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
>  Sol: tuklcignycoejsikoquvafozphmpxlnhtqgbrxdxdbcvzsuvqxprvinsnsbgxf
> str1: t-k---gn-------k--u------hmpx-nhtqg--x------z--v-x---i-s------
> str2: -----i----o-j-i--q---fo------ln----b-x-x--cv-su-q-p-vi-s-sb-xf
> str3: -u-lci-nyco--s--o--v--ozp--p-l--------------------p-----------
> str4: -----ig----e-------va--z----------gbr-d-dbc--s-v---rv-n-n--g-f
> 
> solution is feasible: True
> solution status: OPTIMAL
> best bound: 62.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n008k015-025.txt"))
```

> ```
> --- Condition (with 26 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> str5: pyplrzxucpmqvgtdfuivcdsbo
> str6: pbdevdcvdpfzsmsbroqvbbh
> str7: enbczfjtvxerzbrvigple
> str8: rxwxqkrdrlctodtmprpxwd
> 
> --- Solution (of length 103) ---
>  Sol: pypuilortxzjkwxceginqbdekrvdruyaclopszcfhjmopqtvxglnbeordhtpqxdfgxzbcsvmsuqbprvxinoqsvcdnsbgpxlpwbdefho
> str1: --------t---k----g-n----k----u----------h-m-p---x--n-----ht-q---gxz---v--------xi---s------------------
> str2: ----i-o----j------i-q------------------f---o------lnb--------x---x--c-v-suq-p-v-i---s----sb--x------f--
> str3: ---u-l---------c--in----------y-c-o-s------o---v------o-----------z---------p---------------p-lp-------
> str4: ----i------------g-----e--v----a-----z-----------g--b--rd-----d----bcsv------rv--n------n--g--------f--
> str5: pyp--l-r--z---x--------------u--c--p------m--q-v-g--------t---df---------u------i----vcd-sb-----------o
> str6: p--------------------bde--vd----c--------------v--------d--p---f--z--s-ms--b-r----oq-v----b------b---h-
> str7: ----------------e--n-b----------c----z-f-j----tvx----e-r----------zb---------rv-i----------gp-l----e---
> str8: -------r-x---wx-----q---kr-dr----l----c-------t-------o-d-t------------m----pr--------------px--w-d----
> 
> solution is feasible: True
> solution status: FEASIBLE
> best bound: 75.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n016k015-025.txt"))
```

> ```
> --- Condition (with 26 chars) ---
> str01: tkgnkuhmpxnhtqgxzvxis
> str02: iojiqfolnbxxcvsuqpvissbxf
> str03: ulcinycosovozpplp
> str04: igevazgbrddbcsvrvnngf
> str05: pyplrzxucpmqvgtdfuivcdsbo
> str06: pbdevdcvdpfzsmsbroqvbbh
> str07: enbczfjtvxerzbrvigple
> str08: rxwxqkrdrlctodtmprpxwd
> str09: kkqafigqjwokkskrblg
> str10: lxxpabivbvzkozzvd
> str11: krifsavncdqwhzc
> str12: qaxudgqvqcewbfgijowwy
> str13: rsxqjnfpadiusiqbezhkohmg
> str14: iwshvhcomiuvddm
> str15: htxxqjzqbctbakn
> str16: xusfcfzpeecvwantfmgqzu
> 
> --- Solution (of length 146) ---
>   Sol: rsxiuhoqtjklpwxcginqsxybdefkopquvalrzdghnbmpxcinrvhluzcfjostzdiopdegmqvbefgoqxzcersvwzabimrsuvbntcdfgijmnpqrwghkoqwzkpuvxzbiksvwacdkrsbhlmpxefgnoy
> str01: --------t-k-----g-n--------k---u-------h--mpx--n--h--------t---------q----g--xz----v------------------------------------x--i-s--------------------
> str02: ---i--o--j-------i-q------f-o-----l-----nb--x--------------------------------x-c---v-------su-------------q----------p-v---i-s-------sb----x-f----
> str03: ----u------l---c-in---y----------------------c-----------os----o------v----o--z--------------------------p-----------p------------------l-p-------
> str04: ---i------------g--------e------va--z-g--b------r------------d---d-----b-------c--sv------r--v-n--------n----g-------------------------------f----
> str05: ------------p---------y------p----lrz-------x-------u-c---------p---mqv---g---------------------t-df------------------u----i--v--cd--sb---------o-
> str06: ------------p----------bde------v----d-------c---v-----------d--p--------f----z---s------m-s--b------------r----oq-----v--b-----------bh----------
> str07: -------------------------e--------------nb---c-------z-fj--t----------v------x--er---z-b--r--v-------i-------g-------p------------------l---e-----
> str08: r-x----------wx----q-------k-------r-d----------r--l--c----t---o-d------------------------------t------m-p-r---------p--x------w--d---------------
> str09: ----------k----------------k--q--a---------------------f------i----g-q--------------------------------j-----w---o---k-------ks-----kr-b-l-----g---
> str10: -----------l--x------x-------p---a-------b----i--v---------------------b-----------v-z-------------------------ko--z-----z----v---d---------------
> str11: ----------k------------------------r----------i--------f--s---------------------------a------v-n-cd-------q-w-h----z-------------c----------------
> str12: -------q-------------------------a----------x-------u--------d-----g-qv-----q--ce---w--b-----------fgij---------o-w------------w-----------------y
> str13: rsx----q-j--------n-------f--p---a---d--------i-----u-----s---i------q-be-----z-------------------------------hko----------------------h-m----g---
> str14: ---i---------w------s------------------h---------vh---c--o----------m-------------------i---uv----d-------------------------------d------m--------
> str15: -----h--t-----x------x--------q-------------------------j---z--------q-b-------c----------------t-------------------------b-----a--k-----------n--
> str16: --x-u---------------s-----f------------------c---------f----z---p-e-----e------c---vw-a--------nt--f---m-----g---q-z--u---------------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> best bound: 82.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q05n010k010-010.txt"))
```

> ```
> --- Condition (with 5 chars) ---
> str01: dcbccdbcce
> str02: bddbeeeebd
> str03: cacdeecebe
> str04: aeddddebdd
> str05: acbeecabce
> str06: bbabebdcba
> str07: bbaeaebada
> str08: eeeecbdbee
> str09: ccdeedadcd
> str10: bdabdbeaad
> 
> --- Solution (of length 29) ---
>   Sol: abdecdbeabcdeaecdbdceabdeacde
> str01: --d-c-b---c----cdb-c------c-e
> str02: -bd--dbe----e-e-----e-bd-----
> str03: ----c---a-cde-ec----e-b-e----
> str04: a--e-d-----d----d-d-e-bd---d-
> str05: a---c-be----e--c-----ab---c-e
> str06: -b----b-ab--e----bdc--b--a---
> str07: -b----b-a---eae--b---a-d-a---
> str08: ---e---e----e-ec-bd---b-e---e
> str09: ----c-----cde-e-d----a-d--cd-
> str10: -bd-----ab-d-----b--ea---a-d-
> 
> solution is feasible: True
> solution status: OPTIMAL
> best bound: 29.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q05n050k010-010.txt"))
```

> ```
> --- Condition (with 5 chars) ---
> str01: dcbccdbcce
> str02: bddbeeeebd
> str03: cacdeecebe
> str04: aeddddebdd
> str05: acbeecabce
> str06: bbabebdcba
> str07: bbaeaebada
> str08: eeeecbdbee
> str09: ccdeedadcd
> str10: bdabdbeaad
> str11: ededaaaeaa
> str12: aaeaabeeac
> str13: eaabcaccdb
> str14: bdeeadeade
> str15: caedadeeed
> str16: ebcadbabbe
> str17: ddceeabdea
> str18: dabcddeaec
> str19: aadceedaab
> str20: aeecceeeaa
> str21: bbdaecaade
> str22: dacedaedab
> str23: aaeabbbbce
> str24: dedbcbcaab
> str25: dbdaaebbcb
> str26: debedbebac
> str27: ceebcdcbde
> str28: dbedaadaab
> str29: cccdcbebdc
> str30: aeeacdbcbd
> str31: dacbeacccd
> str32: ecebccdbdb
> str33: ddbbcedabb
> str34: aaeabaaeba
> str35: ecbbcaadcd
> str36: debccecdbc
> str37: daacbaeebc
> str38: adabeaacce
> str39: daecdbacaa
> str40: dacbbdcedc
> str41: dedbeebbde
> str42: cdadcdcdaa
> str43: ceedcbaeed
> str44: ceaecaaaca
> str45: dcccebbbad
> str46: baeeaebbde
> str47: dbdebaccdb
> str48: ebcbeedaea
> str49: aeeebbdbca
> str50: dbdabcecbb
> 
> --- Solution (of length 34) ---
>   Sol: adeabcdebdacebcdeacebdeabcdeabcead
> str01: -d---c--b--c--cd----b----c----ce--
> str02: ----b-d--d---b--e--e--e----e-b---d
> str03: -----c----ac---de--e-----c-e-b-e--
> str04: a-e---d--d-----d-----de-b-d------d
> str05: a----c--b---e---e-c----abc-e------
> str06: ----b---b-a--b--e---bd---c---b--a-
> str07: ----b---b-a-e----a-eb--a--d-a-----
> str08: --e----e----e---e-c-bd--b--e---e--
> str09: -----c-----c---de--e-d-a--d---c--d
> str10: ----b-d---a--b-d----b-ea----a----d
> str11: --e---de-da------a-----a---ea---a-
> str12: a--a---e--a------a--b-e----ea-c---
> str13: --ea------a--bc--ac------cd--b----
> str14: ----b-de----e----a---dea--de------
> str15: -----c----a-e--d-a---de----e---e-d
> str16: --e-bc----a----d----b--ab----b-e--
> str17: -d----d----ce---ea--bdea----------
> str18: -d-abcd--d--e----a-e-----c--------
> str19: a--a--d----ce---e----d-a----ab----
> str20: a-e----e---c--c-e--e--ea----a-----
> str21: ----b---bda-e-c--a-----a--de------
> str22: -d-a-c-e-da-e--d-a--b-------------
> str23: a--a---e--a--b------b---b----bce--
> str24: -de---d-b--c-bc--a-----ab---------
> str25: -d--b-d---a------a-eb---bc---b----
> str26: -de-b--e-d---b--e---b--a-c--------
> str27: -----c-e----ebcd--c-bde-----------
> str28: -d--b--e-da------a---d-a----ab----
> str29: -----c-----c--cd--c-b-e-b-d---c---
> str30: a-e----e--ac---d----b----c---b---d
> str31: -d-a-c--b---e----ac------c----c--d
> str32: --e--c-eb--c--cd----bd--b---------
> str33: -d----d-b----bc-e----d-ab----b----
> str34: a--a---e--a--b---a-----a---e-b--a-
> str35: --e--c--b----bc--a-----a--d---c--d
> str36: -de-bc-----ce-cd----b----c--------
> str37: -d-a------ac-b---a-e--e-bc--------
> str38: ad-ab--e--a------ac------c-e------
> str39: -d-a---e---c---d----b--a-c--a---a-
> str40: -d-a-c--b----b-d--ce-d---c--------
> str41: -de---d-b---e---e---b---b-de------
> str42: -----cd---a----d--c--d---cd-a---a-
> str43: -----c-e----e--d--c-b--a---e---e-d
> str44: -----c-e--a-e-c--a-----a----a-c-a-
> str45: -d---c-----c--c-e---b---b----b--ad
> str46: ----b-----a-e---ea-eb---b-de------
> str47: -d--b-deb-ac--cd----b-------------
> str48: --e-bc--b---e---e----d-a---ea-----
> str49: a-e----e----eb------bd--bc--a-----
> str50: -d--b-d---a--bc-e-c-b---b---------
> 
> solution is feasible: True
> solution status: OPTIMAL
> best bound: 34.0
> ```

In [ ]:
```python
bench(scsp.example.load("nucleotide_n010k010.txt"))
```

> ```
> --- Condition (with 4 chars) ---
> str01: ATGGGATACG
> str02: ATACCTTCCC
> str03: CACGAATTGA
> str04: TAAAATCTGT
> str05: AGGTAACAAA
> str06: TTCCTAGGTA
> str07: TTGTAGATCT
> str08: TGGGAAGTTC
> str09: TTCCACAACT
> str10: TCTAAACGAA
> 
> --- Solution (of length 24) ---
>   Sol: TACTACGCGTAGATCAGTACGTAC
> str01: -A-T--G-G--GAT-A---CG---
> str02: -A-TAC-C-T---TC----C---C
> str03: --C-ACG---A-AT---T--G-A-
> str04: TA--A-----A-ATC--T--GT--
> str05: -A----G-GTA-A-CA--A---A-
> str06: T--T-C-C-TAG----GTA-----
> str07: T--T--G--TAGATC--T------
> str08: T-----G-G--GA--AGT---T-C
> str09: T--T-C-C--A---CA--AC-T--
> str10: T-CTA-----A-A-C-G-A---A-
> 
> solution is feasible: True
> solution status: OPTIMAL
> best bound: 24.0
> ```

In [ ]:
```python
bench(scsp.example.load("nucleotide_n050k050.txt"))
```

> ```
> --- Condition (with 5 chars) ---
> str01: TAGTAGTAGACTCCGGAAGTGACAAACCCTGAAAAGAATGGATAAATATA
> str02: GGATAAACACTCCCGAAAATAATTTGACTTAAACAACGCGACAGTTCAAG
> str03: ATACCTTCCTAGGTAACAAACCAACCAACTTTTGATCTCTTGTAGATCTG
> str04: TAAATTATAATCTTATACTAGTAAAAAATAGGGTGTAACCGAAAACGGTC
> str05: TTAAAACAGCCTGTGGGTTGCACCCACTCACAGGGCCCACTGGGCGCAAG
> str06: ATGACTTCCAATGGATCCCAACCTCAAGCTTCCACCCCAATGGTTTCAGC
> str07: AACAAACCAACCAACTTTTGATCTCTTGTAGATCTGTTCTCTAAACGAAC
> str08: ATGAAAACGAAAATTATTATCAAGGGTATGGAAGTGGAAGCTGACGAAAT
> str09: ACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTA
> str10: TTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTC
> str11: GCAGAGCATTTTCTAATATCCACAAAATGAAGGCAATAATTGTACTACTC
> str12: ATGAGCCAAGATCCGACGAAGAGCCCCAAGGAGGAGAAGGAGGGACCCCC
> str13: TCTCACAGTTCAAGAACCCAAAGTACCCCCCATAGCCCTCTTAAAGCCAC
> str14: AGGTTTATACCTTCCTAGGTAACAAACCAACCAACTTTCGATCTCTTGTA
> str15: AGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTA
> str16: TAAAACAACTCAATACAACATAAGAAAATCAACGCAAAAACACTCACAAA
> str17: CCGCCCATTTGGGCGGCTCTCGAGCGATAGCTCGTCGAATCCCTCGACCT
> str18: ATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTG
> str19: TCTCACAGTTCAAGAACCTCAAGTCTCCCCCATAGGCCTCTTTCAGTCAG
> str20: GATCTCTCTCACCGAACCTGGCCCCGGGCAAATGCCCTAATCCAGAGGTG
> str21: AGAGCAATCAGTGCATCAGAAATATACCTATTATACACTTTGCTAAGAAT
> str22: AATTAAAACATCTCAATACAACATAAGAAAAACAACGCAAAAACACTCAT
> str23: AAACGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGC
> str24: ATAACTAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTG
> str25: ATGAGTGTCACGAATTCACGTACAATGAACTGGATGTTCACGTGGAATAA
> str26: ACCGTGGGCGAGCGGTGACCGGTGTCTTCCTAGTGGGTCCCACGTTGAAR
> str27: AAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTG
> str28: AGTAGTTCGCCTGTGTGAGCTGACAAACTTAGTAGTGTTTGTGAGGATTA
> str29: TTTATACCTTCCTAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGAT
> str30: ATGCGGTCGTCTCTCCCCGGCTTTTTTTCCCCGCGCCGCGTTGGCGCCGA
> str31: GTGACAAAAACATAATGGACTCCAACACCATGTCAAGCTTTCAGGTAGAC
> str32: GTGTAAGAAACAGTAAGCCCGGAAGTGGTGTTTTGCGATTTCGAGGCCGG
> str33: GAGAATGAGTCTCATTACCGCCCGGTACTTAGCAAGCTAATAGTCACGGC
> str34: ATGTGGTCGATGCCATGGAGGCCCACCAGTTCATTAAGGCTCCTGGCATT
> str35: ACGAGCGTTTTAAGGGCCCGCGACTGCGACGGCCACATGGCCCTGTATGT
> str36: GGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAG
> str37: TGGGAAGTTCCAAAAGATCACAAAACACTACCAGTCAACCTGAAGTACAC
> str38: GAAGCGTTAACGTGTTGAGGAAAAGACAGCTTAGGAGAACAAGAGCTGGG
> str39: ACCAGCGCACTTCGGCAGCGGCAGCACCTCGGCAGCACCTCAGCAGCAAC
> str40: ATGGGACAACTTATTCCTATCATGTGCCAAGAGGTTTTACCCGGTGACCA
> str41: TTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGTTGTCACTC
> str42: AACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAACGAACTTTA
> str43: GGGTTCTGCCAGGCATAGTCTTTTTTTCTGGCGGCCCTTGTGTAAACCTG
> str44: GGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTACTGT
> str45: TGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTACTGTCGT
> str46: TTCCACAACTTTCCACCAAGCTCTGCAAGATCCCAGAGTCAGGGGCCTGT
> str47: TCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAG
> str48: ACCGGATGGCCGCGATTTTTCGGAGTCCTTGGGGGACCACTCAGAATAGA
> str49: CTTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACT
> str50: ATGAGCACTAAGCGAAGAACCAAAAAGCAGACAATACAACCCGCTATTAC
> 
> --- Solution (of length 136) ---
>   Sol: ATGTACGTACGTACGTACTAGTACTACGTACGTACGTACGACTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGACGTCGACGTACTACGTACGTACGTACGTACGTACGTACGRT
> str01: -T--A-GTA-GTA-G-ACT----C--CG---G-A---A-G--T--G-AC--A---A---AC---C---C-T--G-A---A---A---A-G-A--A--T-G--G-A-TA---A---A--TA--TA------------
> str02: --G---G-A--TA---A--A---C-AC-T-C---C---CGA--A---A---A--TA---A--T---T---T--G-AC-T---TA---A---AC-A-----ACG--C---G-AC--A-GT---T-C--A---A-G--
> str03: AT--AC---C-T---T-C-----CTA-G---GTA---AC-A--A---AC---C--A---AC---C--A---AC-T---T---T---T--G-A-----TC----T-CT---T--GTA-G-A--T-C-T--G------
> str04: -T--A---A---A--T--TA-TA--A--T-C-T---TA----TAC-TA-GTA---A---A---A---A---A--TA-G---G---GT--GTA--AC--CGA---A--A---ACG---GT-C---------------
> str05: -T-TA---A---A---AC-AG--C--C-T--GT--G---G-----GT---T--G--C--AC---C---C--AC-T-C--AC--A-G---G---G-C--C--C--ACT--G---G---G--CG--C--A---A-G--
> str06: ATG-AC-T---T-C---C-A--A-T--G---G-A--T-C--C--C--A---AC---C-T-C--A---A-G--C-T---T-C---C--AC---C--C--C-A---A-T--G---GT---T---T-C--A-G--C---
> str07: A---AC--A---A---AC-----C-A---AC---C--A--ACT---T---T---T--G-A--T-C-T-C-T---T--GTA-G-A--T-C-T--G---T-----T-CT-C-TA---A---ACG-A---AC-------
> str08: ATG-A---A---A---AC--G-A--A---A---A--T-----TA--T---TA--T-C--A---A-G---G---GTA--T--G---G-A---A-G---T-G--G-A--A-G--C-T--G-ACG-A---A---A---T
> str09: A----C-T-CG---G--CT-G--C-A--T--G--C-T-----TA-GT--G--C--AC-T-C--ACG--C--A-GTA--TA---A--T---TA--A--T--A---ACTA---A--T---TA----------------
> str10: -T-T--GTA-G-A--T-CT-GT--T-C-T-C-TA---A--AC---G-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G--G-C----T-----GT-C--AC-T-C---------------
> str11: --G--C--A-G-A-G--C-A-T--T---T---T-C-TA--A-TA--T-C---C--AC--A---A---A---A--T--G-A---A-G---G--C-A-----A--TA--A--T---T--GTAC-TAC-T-C-------
> str12: ATG-A-G--C---C--A--AG-A-T-C---CG-ACG-A--A----G-A-G--C---C---C---C--A---A-G---G-A-G---G-A-G-A--A-G--GA-G------G---G-AC---C---C---C---C---
> str13: -T---C-T-C--AC--A---GT--T-C--A---A-G-A--AC--C---C--A---A---A-GTAC---C---C---C---C---C--A--TA-G-C--C--C-T-CT---TA---A---A-G--C---C--AC---
> str14: A-G---GT---T---TA-TA---C--C-T---T-C---C---TA-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC----T-----T--T-CG-A--T-C-T-C-T---T--GTA----
> str15: A-G---GT---T---TA-TA---C--C-T---T-C---C--C-A-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC----T-----T--T-CG-A--T-C-T-C-T---T--GTA----
> str16: -T--A---A---A---AC-A--ACT-C--A---A--TAC-A--AC--A--TA---A-G-A---A---A---A--T-C--A---ACG--C--A--A-----A---A--AC--AC-T-C--AC--A---A---A----
> str17: -----C---CG--C---C-----C-A--T---T---T--G-----G---G--CG---G--C-T-C-T-CG-A-G--CG-A--TA-G--C-T-CG---TCGA---A-T-C---C---C-T-CG-AC---C-T-----
> str18: AT--AC---C-T---T-C-----C--C--A-G---GTA--AC-A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A-----TC----T-CT---T--GTA-G-A--T-C-T--G------
> str19: -T---C-T-C--AC--A---GT--T-C--A---A-G-A--AC--C-T-C--A---A-GT-C-T-C---C---C---C---C--A--TA-G---G-C--C----T-CT---T---T-C--A-GT-C--A-G------
> str20: --G-A--T-C-T-C-T-CT----C-AC---CG-A---AC--CT--G---G--C---C---C---CG---G---G--C--A---A---A--T--G-C--C--C-TA--A--T-C---C--A-G-A-G---GT--G--
> str21: A-G-A-G--C--A---A-T----C-A-GT--G--C--A----T-C--A-G-A---A---A--TA--TAC---C-TA--T---TA--TAC--AC----T-----T--T--G--C-TA---A-G-A---A--T-----
> str22: A---A--T---TA---A--A--AC-A--T-C-T-C--A--A-TAC--A---AC--A--TA---A-G-A---A---A---A---AC--A---ACG-C----A---A--A---A---AC--AC-T-C--A--T-----
> str23: A---A---ACG-A---ACT--T--TA---A---A---A----T-C-T--GT--GT--G---G--C-T--GT-C--AC-T-CG---G--C-T--G-C----A--T-----G--C-T---TA-GT--G--C-------
> str24: AT--A---AC-TA---A-T--TACT--GT-CGT---T--GAC-A-G---G-AC--ACG-A-GTA---AC-T-CGT-C-TA--T-C-T---T-C----T-G------------------------------------
> str25: ATG-A-GT--GT-C--AC--G-A--A--T---T-C--ACG--TAC--A---A--T--G-A---AC-T--G---G-A--T--GT---T-C--ACG---T-G--G-A--A--TA---A--------------------
> str26: A----C---CGT--G-----G------G--CG-A-G--CG-----GT--G-AC---CG---GT--GT-C-T---T-C---C-TA-GT--G---G--GTC--C---C-ACGT---T--G-A---A----------R-
> str27: A---A---A-G---GT--T--TA-TAC---C-T---T-C--C--C--A-G---GTA---AC--A---A---AC---C--A---AC---C--A--AC-T-----T--T-CG-A--T-C-T-C-T---T--G------
> str28: A-GTA-GT---T-CG--C-----CT--GT--GT--G-A-G-CT--G-AC--A---A---AC-T---TA-GTA-GT--GT---T---T--GT--GA-G--GA--T--TA----------------------------
> str29: -T-T---TA--TAC---CT--T-C--C-TA-G---GTA--AC-A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A-----TC----T-CT---T--GTA-G-A--T-------------
> str30: ATG--CG---GT-CGT-CT----CT-C---C---C---CG-----G--C-T---T---T---T---T---T---T-C---C---C---CG--CG-C--CG-CGT--T--G---G--CG--C---CG-A--------
> str31: --GT--G-AC--A---A--A--A--AC--A--TA---A----T--G---G-AC-T-C---C--A---AC--AC---C--A--T--GT-C--A--A-G-C----T--T---T-C--A-G---GTA-G-AC-------
> str32: --GT--GTA---A-G-A--A--AC-A-GTA---A-G--C--C--CG---G-A---A-GT--G---GT--GT---T---T---T--G--CG-A-----T-----T--T-CG-A-G---G--C---CG---G------
> str33: --G-A-G-A---A--T----G-A----GT-C-T-C--A----T---TAC---CG--C---C---CG---GTAC-T---TA-G--C--A---A-G-C-T--A---A-TA-GT-C--ACG---G--C-----------
> str34: ATGT--G---GT-CG-A-T-G--C--C--A--T--G---GA----G---G--C---C---C--AC---C--A-GT---T-C--A--T---TA--A-G--G-C-T-C--C-T--G---G--C--A--T---T-----
> str35: A----CG-A-G--CGT--T--T--TA---A-G---G---G-C--C---CG--CG-AC-T--G--CG-ACG---G--C---C--AC--A--T--G--G-C--C---CT--GTA--T--GT-----------------
> str36: --G---GT---T---TA-TA---C--C-T---T-C---C--C-A-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC----T-----T--T-CG-A--T-C-T-C-T---T--GTA-G--
> str37: -TG---G---G-A---A---GT--T-C---C--A---A--A--A-G-A--T-C--AC--A---A---A---AC--AC-TAC---C--A-GT-C-A-----AC---CT--G-A---A-GTAC--AC-----------
> str38: --G-A---A-G--CGT--TA--AC---GT--GT---T--GA----G---G-A---A---A---A-G-AC--A-G--C-T---TA-G---G-A-GA-----AC--A--A-G-A-G--C-T--G---G---G------
> str39: A----C---C--A-G--C--G--C-AC-T---T-CG---G-C-A-G--CG---G--C--A-G--C--AC---C-T-CG---G--C--A-G--C-AC--C----T-C-A-G--C--A-G--C--A---AC-------
> str40: ATG---G---G-AC--A--A---CT---TA--T---T-C--CTA--T-C--A--T--GT--G--C---C--A---A-G-A-G---GT---T------T-----TAC--C---CG---GT--G-AC---C--A----
> str41: -T-T--GTA-G-A--T-CT-GT--T-C-T-C-TA---A--AC---G-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G--GT-----T-----GT-C--AC-T-C---------------
> str42: A---AC---C--A---AC-----C-A---AC-T---T-----T-CG-A--T-C-T-C-T---T--GTA-G-A--T-C-T--GT---T-C-T-C----T--A---A--ACG-A---AC-T---T---TA--------
> str43: --G---G---GT---T-CT-G--C--C--A-G---G--C-A-TA-GT-C-T---T---T---T---T---T---T-C-T--G---G--CG---G-C--C--C-T--T--GT--GTA---A---AC---C-T--G--
> str44: --G---G--C-T--G--C-A-T-----G--C-T---TA-G--T--G--C--AC-T-C--ACG--C--A-GTA--TA---A--T---TA---A-----T--A---ACTA---A--T---TAC-T--GT---------
> str45: -TG--C--A--T--G--CT--TA----GT--G--C--AC---T-C--ACG--C--A-GTA--TA---A--T---TA---A--TA---AC-TA--A--T-----TACT--GT-CGT---------------------
> str46: -T-T-C---C--AC--A--A---CT---T---T-C---C-AC--C--A---A-G--C-T-C-T--G--C--A---A-G-A--T-C---C---C-A-G---A-GT-C-A-G---G---G---G--C---C-T--G-T
> str47: -T---C-TA---A---AC--G-A--AC-T---T---TA--A--A---A--T-C-T--GT--GT--G---G--C-T--GT-C--AC-T-CG---G-C-T-G-C--A-T--G--C-T---TA-G--------------
> str48: A----C---CG---G-A-T-G------G--C---CG--CGA-T---T---T---T---T-CG---G-A-GT-C---C-T---T--G---G---G--G--GAC---C-AC-T-C--A-G-A---A--TA-G-A----
> str49: -----C-T---T--GTA---G-A-T-C-T--GT---T-C---T-C-TA---A---ACG-A---AC-T---T---TA---A---A---A--T-C----T-G---T-----GT--G---G--C-T--GT-C--AC--T
> str50: ATG-A-G--C--AC-TA--AG--C---G-A---A-G-A--AC--C--A---A---A---A---A-G--C--A-G-AC--A---A--TAC--A--AC--C--CG--CTA--T---TAC-------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> best bound: 38.0
> ```

In [ ]:
```python
bench(scsp.example.load("protein_n010k010.txt"))
```

> ```
> --- Condition (with 19 chars) ---
> str01: MALSYCPKGT
> str02: MQSSLNAIPV
> str03: MPLSYQHFRK
> str04: MEEHVNELHD
> str05: MSNFDAIRAL
> str06: MFRNQNSRNG
> str07: MFYAHAFGGY
> str08: MSKFTRRPYQ
> str09: MSFVAGVTAQ
> str10: MESLVPGFNE
> 
> --- Solution (of length 46) ---
>   Sol: MQSKNPAEFLRSYDLNQVACINPSTEGHRVAFNREGKLGHPTYADQ
> str01: M-----A--L-SY------C--P-------------K-G--T----
> str02: MQS--------S--LN--A-I-P------V----------------
> str03: M----P---L-SY---Q----------H---F-R--K---------
> str04: M------E-----------------E-H-V--N-E--L-H----D-
> str05: M-S-N---F----D----A-I-------R-A------L--------
> str06: M-------F-R----NQ----N-S----R---N--G----------
> str07: M-------F---Y-----A--------H--AF---G--G---Y---
> str08: M-SK----F---------------T---R----R------P-Y--Q
> str09: M-S-----F--------VA-------G--V-----------T-A-Q
> str10: M------E---S--L--V----P---G----FN-E-----------
> 
> solution is feasible: True
> solution status: OPTIMAL
> best bound: 46.0
> ```

In [ ]:
```python
bench(scsp.example.load("protein_n050k050.txt"))
```

> ```
> --- Condition (with 20 chars) ---
> str01: MRHLNIDIETYSSNDIKNGVYKYADAEDFEILLFAYSIDGGEVECLDLTR
> str02: MERRAHRTHQNWDATKPRERRKQTQHRLTHPDDSIYPRIEKAEGRKEDHG
> str03: MEPGAFSTALFDALCDDILHRRLESQLRFGGVQIPPEVSDPRVYAGYALL
> str04: MGKFYYSNRRLAVFAQAQSRHLGGSYEQWLACVSGDSAFRAEVKARVQKD
> str05: FFRENLAFQQGKAREFPSEEARANSPTSRELWVRRGGNPLSEAGAERRGT
> str06: MDPSLTQVWAVEGSVLSAAVDTAETNDTEPDEGLSAENEGETRIIRITGS
> str07: MAFDFSVTGNTKLDTSGFTQGVSSMTVAAGTLIADLVKTASSQLTNLAQS
> str08: MAVILPSTYTDGTAACTNGSPDVVGTGTMWVNTILPGDFFWTPSGESVRV
> str09: MNTGIIDLFDNHVDSIPTILPHQLATLDYLVRTIIDENRSVLLFHIMGSG
> str10: MFVFLVLLPLVSSQCVNLRTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS
> str11: MDSKETILIEIIPKIKSYLLDTNISPKSYNDFISRNKNIFVINLYNVSTI
> str12: MLLSGKKKMLLDNYETAAARGRGGDERRRGWAFDRPAIVTKRDKSDRMAH
> str13: MNGEEDDNEQAAAEQQTKKAKREKPKQARKVTSEAWEHFDATDDGAECKH
> str14: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEVLSEARQHLKDGT
> str15: MRYIVSPQLVLQVGKGQEVERALYLTPYDYIDEKSPIYYFLRSHLNIQRP
> str16: MPRVPVYDSPQVSPNTVPQARLATPSFATPTFRGADAPAFQDTANQQARQ
> str17: MFVFLVLLPLVSSQCVNLRTRTQLPLAYTNSFTRGVYYPDKVFRSSVLHS
> str18: MFVFFVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS
> str19: MEAIISFAGIGINYKKLQSKLQHDFGRVLKALTVTARALPGQPKHIAIRQ
> str20: MASSGPERAEHQIILPESHLSSPLVKHKLLYYWKLTGLPLPDECDFDHLI
> str21: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEVLSEVRQHLKDGT
> str22: MLAPSPNSKIQLFNNINIDINYEHTLYFASVSAQNSFFAQWVVYSADKAI
> str23: MSAITETKPTIELPALAEGFQRYNKTPGFTCVLDRYDHGVINDSKIVLYN
> str24: MKNIAEFKKAPELAEKLLEVFSNLKGNSRSLDPMRAGKHDVVVIESTKKL
> str25: MPQPLKQSLDQSKWLREAEKHLRALESLVDSNLEEEKLKPQLSMGEDVQS
> str26: MFVFLVLLPLVSSQCVNLITRTQSYTNSFTRGVYYPDKVFRSSVLHSTQD
> str27: MKFDVLSLFAPWAKVDEQEYDQQLNNNLESITAPKFDDGATEIESERGDI
> str28: MFVFLVLLPLVSSQCVNFTNRTQLPSAYTNSFTRGVYYPDKVFRSSVLHS
> str29: MWSIIVLKLISIQPLLLVTSLPLYNPNMDSCCLISRITPELAGKLTWIFI
> str30: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEFLSEARQHLKDGT
> str31: MFVFLVLLPLVSSQCVMPLFNLITTTQSYTNFTRGVYYPDKVFRSSVLHL
> str32: MHQITVVSGPTEVSTCFGSLHPFQSLKPVMANALGVLEGKMFCSIGGRSL
> str33: MATLLRSLALFKRNKDKPPITSGSGGAIRGIKHIIIVPIPGDSSITTRSR
> str34: MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSMEEVLSEARQHLKDGT
> str35: MFVFLVLLPLVSSQCVNLTTGTQLPPAYTNSFTRGVYYPDKVFRSSVLHS
> str36: MANIINLWNGIVPMVQDVNVASITAFKSMIDETWDKKIEANTCISRKHRN
> str37: MLNRIQTLMKTANNYETIEILRNYLRLYIILARNEEGRGILIYDDNIDSV
> str38: MADPAGTNGEEGTGCNGWFYVEAVVEKKTGDAISDDENENDSDTGEDLVD
> str39: MFVFLVLLPLVSSQCVNLRTRTQLPPSYTNSFTRGVYYPDKVFRSSVLHS
> str40: MESLVPGFNEKTHVQLSLPVLQVCDVLVRGFGDSVEEVLSEARQHLKDGT
> str41: MNNQRKKTARPSFNMLKRARNRVSTVSQLAKRFSKGLLSGQGPMKLVMAF
> str42: MSNFDAIRALVDTDAYKLGHIHMYPEGTEYVLSNFTDRGSRIEGVTHTVH
> str43: MIELRHEVQGDLVTINVVETPEDLDGFRDFIRAHLICLAVDTETTGLDIY
> str44: MFVFLVLLPLVSSQCVMPLFNLITTNQSYTNSFTRGVYYPDKVFRSSVLH
> str45: MSKDLVARQALMTARMKADFVFFLFVLWKALSLPVPTRCQIDMAKKLSAG
> str46: MASLLKSLTLFKRTRDQPPLASGSGGAIRGIKHVIIVLIPGDSSIVTRSR
> str47: MRVRGILRNWQQWWIWTSLGFWMFMICSVVGNLWVTVYYGVPVWKEAKTT
> str48: MAVEPFPRRPITRPHASIEVDTSGIGGSAGSSEKVFCLIGQAEGGEPNTV
> str49: MFYAHAFGGYDENLHAFPGISSTVANDVRKYSVVSVYNKKYNIVKNKYMW
> str50: MANYSKPFLLDIVFNKDIKCINDSCSHSDCRYQSNSYVELRRNQALNKNL
> 
> --- Solution (of length 447) ---
>   Sol: MRSAEFHKLNSTWYDFGLSVAEHIKPRTADEFGNQAIKLPRSTYAEFHKLQRTVYADEHKLMNPQSVWEFGKLNPQRTYADHILRSVEFGILNPQTWDELRSAHNPSTVWYADFGIKLPQSWACELRTVADEGHIMPQRCDNTVAEGILMPQRSTVWYAFHIKQRTCDEGHILMNPQRSTVYADGKLNPQSVYDFIKLNRTVWACEGIKLMPSTYDFGINRTYAEHIKLPQRSVWDFMNTAGIKLRTYACFGHQSVYAELMPRSTVWGIKNSVYADEFKLNPQRTVWGIKMSACDEFHIKLNPRSVACIKLPRTWYEFGHINSVDEFGKNPRYADEILNRTFHPSYACEGIKLPQRSVWCHIKLNQSTYADGKLMPQRSTVYADEFGNPSVYCIMQRSTAEIKSVWDGIKTCEHILPQRSADLNTVGIKLMRYAHKNQSTDFGILTY
> str01: MR----H-LN-------------I-----D------I--------E------T-Y----------S-------------------S------N----D-----------------IK------------------------N----G--------V-Y----K------------------YAD-------------------A-E---------DF-------E-I-L---------------L-----F------A---------------Y-----------------S------I-------------------------D--G---------------------G----------------------------------E-----V---------E----------C---L-----DL-T------R---------------
> str02: M---E---------------------R-------------R---A--H---RT-----H-----Q--------N----------------------WD----A----T--------K-P-------R----E------R-------------R---------KQ-T----------Q------------------------------------------------H-----R------------L-T-----H--------P-------------D------------------D---------S---I------Y--------------PR----I-----------E--K-----------------A--------------E-G---------R-----K---------E--------D------------H-------G----
> str03: M---E--------------------P------G--A----------F------------------S-----------T-A---L----F--------D----A--------------L-----C------D---------D------IL-----------H---R------------R--------L------------------E------S-----------------Q-------------LR----FG---------------G----V---------Q-----I-------------P--------P----E------V--------------------S-------------------------D----P-R--VYA---G----Y-------A---------------L------L------------------------
> str04: M---------------G-------K------F-----------Y----------Y----------S-------N--R-------R------L----------A-----V----F--------A--------------Q------A------Q-S----------R-----H-L-----------G---------------------G-----S-Y---------E-----Q---W---------L---AC-----V-------S---G-------D---------------SA---F------R--A---------E------V----K----A-----R-----------------V-------Q------K----------D---------------------------------------------------------------
> str05: -----F---------F----------R---E--N----L-----A-F---Q-------------Q-----GK-------A----R--EF----P-------S----------------------E------E------------A-------R-----A---------------N---S---------P-----------T-----------S-------R---E---L-----W--------------------V------R--------------------R---G------------------------------G--N--------P------L------S---E--------------------A-G----------A-E-----------R---------------------R-------G------------T-------
> str06: M-------------D----------P---------------S-------L--T-----------Q-VW-----------A------VE-G-----------S------V--------L--S-A------A-------------V-----------------------D-----------T--A----------------------E-------T-----N---------------D---T------------------E--P-------------DE----------G------------L---S-A---------E----N---E-G-------E----T--------------R-----I-------------------------------I--R----I--------T---------------G-----------S--------
> str07: M--A-F--------DF--SV-------T----GN--------T-----KL------D--------------------T-------S---G-----------------------F-------------T---------Q--------G--------V----------------------S-----------S-------------------M--T-------------------V------A-------A--G------------T--------------L--------I---A-D-----L----V---K---T-------------------A----------S-----------S--------Q-------L-----T-------N---------------------------L----A----------------QS--------
> str08: M--A---------------V---I--------------LP-STY--------T---D-------------G------T-A----------------------A--------------------C---T-------------N----G------S---------------------P-------D-------V---------V----G------T---G---T---------------M----------------------------W-----V-------N---T---I-----------L-P---------------G-----D-F--------------F----------------W--------T-------P--S-------G-------------E--SV-------------R------V---------------------
> str09: M--------N-T----G------I------------I-------------------D---L--------F----------D-----------N----------H----V---D-------S-------------I-P-----T----IL-P---------H--Q--------L---------A-----------------T--------L-----D------Y-----L----V-----------RT---------------------I-------------------I-----DE-----N-RSV----L--------------------------L---FH-------I-----------------------M-----------G--S-----------------G---------------------------------------
> str10: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N------L---R-T---------RT----------Q---------L-P----------------------P-----------A-----------------------Y----------------T-----NS-----F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---S--------
> str11: M-------------D---S-----K-----E-----------T---------------------------------------IL------I-------E----------------I------------------I-P-------------------------K--------I-------------K----S-Y----L-----------L-----D-----T----------------N---I-----------S------P-------K-S-Y------N-------------D-F-I-----S-------R--------N------KN------I----F---------------V---I--N--------L-------Y-----N--V------ST--I---------------------------------------------
> str12: M-------L--------LS-------------G----K----------K----------K-M----------L----------L-------------D------N-----Y-------------E--T-A--------------A-------------A-----R----G-------R------G---------------------G--------D--------E------R-------------R----------------R----G------------------W-----A---F---------------------------D------R-----------P--A---I------V---------T----K----R-----D------------------KS--D-----------R-----------M--AH------------
> str13: M--------N------G----E--------E-------------------------D-----------------------D-----------N-----E--------------------Q--A------A--------------AE-----Q-----------Q-T-------------------K----------K------A----K-----------R---E--K-P-------------K---------Q---A----R------K--V-----------T------S---E----------A-------W-E--H------F-------D-----------A--------------------T--D------------D--G------------AE----------C----------------K-----H------------
> str14: M---E-----S------L-V-----P------G-------------F---------------N-----E--K-----T---H----V-------Q----L-S---------------LP---------V-------------------L--Q---V--------R--D------------V-----L----V-------R------G---------FG-----------------D------------------SV--E-----------------E--------V--------------L---S-----------E----------------A-----R--------------Q-----H--L--------K----------D--G-----------T------------------------------------------------
> str15: MR-----------Y---------I-----------------------------V-----------S--------PQ-------L--V----L--Q-------------V-----G-K---------------G----Q-------E---------V------------E--------R----A---L-----Y----L--T----------P--YD------Y---I--------D----------------------E----------K-S---------P------I--------------------------Y----------------Y--------F----------L--RS---H--LN----------------------------I-QR-------------------P------------------------------
> str16: M------------------------PR--------------------------V---------P--V-----------Y-D----S-------PQ-------------V-----------S---------------P----NTV------PQ------A-----R-------L---------A-----------------T----------PS---F------A---------------T---------------------P--T------------F-----R---G----A-D-----------A----P---------------------A-------F------------Q---------------D--------T--A----N-------Q---------------------Q--A----------R-----Q---------
> str17: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N------L---R-T---------RT----------Q---------L-P--------L-----A----------Y------T----------------N---------------S----------------------F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---S--------
> str18: M----F-------------V-----------F--------------F------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N------L-----T----------T-----------R-T---------Q-------L-------------P-----------------P----------A------Y----------------T-----NS-----F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---S--------
> str19: M---E---------------A--I------------I----S----F--------A--------------G-----------I------GI-N-----------------Y-----K---------------------------------------------K---------L---Q-S------KL--Q-----------------------------------H---------DF----G---R---------V---L---------K----A----L----TV---------------------------T-------------------A-----R------A-----LP-----------------G----Q-----------P-------------K----------HI-----A------I---R-----Q---------
> str20: M--A------S-------S-------------G------P-----E-----R---A-EH-----Q-----------------I-------IL-P----E--S-H-------------L--S--------------------------------S---------------------P----------L----V----K----------------------------H-KL---------------L--Y--------Y---------W--K---------L----T--G------------L-P-------LP------------DE---------------------C----------------------D--------------F--------------------D------H-L-----------I-------------------
> str21: M---E-----S------L-V-----P------G-------------F---------------N-----E--K-----T---H----V-------Q----L-S---------------LP---------V-------------------L--Q---V--------R--D------------V-----L----V-------R------G---------FG-----------------D------------------SV--E-----------------E--------V--------------L---S-----------E------V-------R----------------------Q-----H--L--------K----------D--G-----------T------------------------------------------------
> str22: M-------L-----------A----P---------------S---------------------P---------N-----------S------------------------------K-----------------I--Q----------L----------F--------------N------------N-------I--N--------I-------D--IN--Y-EH-------------T----L--Y--F------A-----S-V-----S--A-------Q------------------N--S------------F--------F------A--------------------Q---W---------------------V---------VY-----S-A------D--K----------A------I-------------------
> str23: M-SA-------------------I---T--E-----------T-----K--------------P-------------T----I----E---L-P--------A--------------L----A-E-------G--------------------------F---QR----------------Y-----N--------K---T----------P-----G------------------F--T---------C-----V---L---------------D-------R-------------------------------Y--------D-----------------H------G-------V---I--N-----D-------S-----------------------K-----I----------------V---L--Y---N----------
> str24: M------K-N-------------I----A-EF-----K----------K------A-------P----E---L------A-------E----------------------------KL-------L-----E-----------V---------------F------------------S--------N---------L----------K--------G-N------------S------------R--------S----L---------------D-----P--------M------------R--A-----------G---------K-------------H---------------------------D---------V---------V-------------V---I---E------S----T---K------K--------L--
> str25: M------------------------P--------Q----P---------L---------K----QS------L-------D-------------Q------S--------------K----W---LR----E------------AE----------------K-------H-L----R----A---L------------------E------S---------------L----V-D------------------S---------------N--------L---------------E--------------------E--------E--K--------L-------------K-PQ--------L--S-------M-----------G-------------E-----D------------------V-----------QS--------
> str26: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N------L------------I---T-----------R-T---------QS-Y-------T------------------N------------S---F--T-----R-----G---VY----------------Y-------P------------D----K-----V-----------F-------------R------------S-----------SV-----L-------------------------------------------------H-----S----T------------Q--D------
> str27: M------K-------F-------------D-----------------------V------L----S------L---------------F-------------A--P---W-A----K-----------V-DE-----Q-------E-----------Y---------D--------Q------------Q-------LN--------------------N------------------N-----L-------------E----S----I---------------T-------A---------P------K-------F------D---------D--------------G-------------------A---------T----E--------I------E--S--------E-----R-------G-------------D--I---
> str28: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N-----------------F-----T--------N--R-T---------Q-------L-------------PS----------A-----------------------Y----------------T-----NS-----F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---S--------
> str29: M-----------W-----S----I------------I----------------V------L----------KL---------I--S----I---Q----------P-----------L-------L----------------------L------V---------T------------S-------L-P--------L----------------Y----N---------P--------N---------------------M--------------D---------------S-C-------------C--L---------I-S--------R----I---T--P----E---L----------------A-GKL-----T-------------------------W--I--------------------------------F-I---
> str30: M---E-----S------L-V-----P------G-------------F---------------N-----E--K-----T---H----V-------Q----L-S---------------LP---------V-------------------L--Q---V--------R--D------------V-----L----V-------R------G---------FG-----------------D------------------SV--E-----------------EF-L-----------S---E----------A-----R-----------------------------------------Q-----H--L--------K----------D--G-----------T------------------------------------------------
> str31: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------MP-----------L----------F--------------N-----------L--------I----T------------T-------T--------Q-S--------------Y----------------T-----N------F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---------L--
> str32: M-----H---------------------------Q-I-----T----------V------------V------------------S---G---P-T--E---------V-----------S------T-----------C-------------------F---------G--------S-------L--------------------------------------H---P------F----------------QS----L---------K-----------P---V----M-A--------N----A---L-------G----V-------------L----------EG-K----------------------M----------F------C----S---I-----G------------------G----R------S-----L--
> str33: M--A-------T-----L--------------------L-RS-------L-----A----L--------F-K----R---------------N-----------------------K-------------D-------------------------------K------------P------------P------I----T-----------S----G--------------S--------G---------G-----A----------I--------------R---GIK-------HI---------I-----------I--V------P-----I------P-----G--------------------D-------S----------S---I----T-----------T-------RS-----------R---------------
> str34: M---E-----S------L-V-----P------G-------------F---------------N-----E--K-----T---H----V-------Q----L-S---------------LP---------V-------------------L--Q---V--------R--D------------V-----L----V-------R------G---------FG-----------------D------------------S-----M---------------E------------------E---------V----L-----------S--E-------A-----R--------------Q-----H--L--------K----------D--G-----------T------------------------------------------------
> str35: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N------L-----T----------T---G---------T---------Q-------L-------------P-----------------P----------A------Y----------------T-----NS-----F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---S--------
> str36: M--A-----N-------------I------------I-------------------------N---------L-----------------------W-------N---------GI------------V-------P------------M-----V-------Q---D------------V------N---V-----------A--------S-----I--T-A------------F------K----------S-----M-------I------DE-------T-W-------D----K---------K----------I----E-------A----N-T------C--I-----S--------------------R------------------------K----------H----R----N-----------------------
> str37: M-------LN----------------R---------I-------------Q-T-------LM---------K-----T-A------------N-----------N-----Y-------------E--T------I----------E-IL---R---------------------N------Y----L------------R---------L----Y---I-------I-L-----------A----R------------------------N-----E------------------E----------------------G------------R-----------------GI-L--------I------Y-D------------D---N-----I------------D------------S-----V---------------------
> str38: M--A----------D----------P--A---G---------T-------------------N-------G----------------E----------E---------------G------------T----G------C-N----G---------W--F---------------------Y---------V-------------E-----------------A---------V---------------------V--E----------K--------K-----T--G------D-----------A-I-------------S-D---------DE--N---------E---------------N-----D-------S----D--------------T--------G----E--------DL--V--------------D------
> str39: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------------N------L---R-T---------RT----------Q---------L-P----------------------PS-Y------T----------------N---------------S----------------------F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H---S--------
> str40: M---E-----S------L-V-----P------G-------------F---------------N-----E--K-----T---H----V-------Q----L-S---------------LP---------V-------------------L--Q---V----------CD------------V-----L----V-------R------G---------FG-----------------D------------------SV--E-----------------E--------V--------------L---S-----------E----------------A-----R--------------Q-----H--L--------K----------D--G-----------T------------------------------------------------
> str41: M--------N-----------------------NQ-----R-------K----------K-----------------T-A----R--------P-------S-----------F---------------------------N-------M----------------------L------------K-------------R---A----------------R-----------------N------R---------V-------STV-----S----------Q-----------------L-----A--K--R----F----S-----K--------------------G--L----------L--S----G----Q---------G-P-----M-------K------------L---------V----M--A-------F-----
> str42: M-S------N-----F-------------D-----AI---R---A----L---V--D--------------------T--D---------------------A-------Y-----KL--------------GHI-------------------------H------------M-------Y------P----------------EG------T----------E----------------------Y-------V---L---S------N------F------T---------D--------R--------------G---S--------R----I-----------EG-------V---------T---------------------------------------------H----------TV--------H------------
> str43: M----------------------I------E-------L-R------H---------E--------V--------Q-------------G-------D-L--------V------------------T------I------N-V-----------V------------E----------T--------P----------------E---------D------------L------D-----G--------F-----------R------------D-F----------I--------------R--A------------H-----------------L------------I--------C---L-----A----------V--D--------------T-E---------T-------------T-G--L----------D--I--Y
> str44: M----F-------------V-----------F------L--------------V------L-----------L-P--------L--V--------------S----S------------Q---C----V------MP-----------L----------F--------------N-----------L--------I----T------------T-----N----------Q-S--------------Y----------------T-----NS-----F------T------------------R--------------G----V--------Y------------Y-------P----------------D-K-------V----F----------RS-----SV----------L------------------H------------
> str45: M-S----K------D--L-VA-----R-------QA--L----------------------M---------------T-A----R--------------------------------------------------M--------------------------K-------------------AD----------F------V--------------F-------------------F-------L-----F----V---L------W--K----A----L-----------S--------L-P--V-----P-T-----------------R---------------C------Q------I--------D---M-------A-------------------K------K-----L---SA-----G--------------------
> str46: M--A------S------L--------------------L---------K----------------S------L----T-----L----F---------------------------K---------RT----------R-D----------Q-----------------------P------------P--------L-----A--------S----G--------------S--------G---------G-----A----------I--------------R---GIK-------H-------V--I-----------I--V-------------L------------I--P-----------------G-----------D-----S-------S---I--V-----T-------RS-----------R---------------
> str47: MR-----------------V------R-----G---I-L-R---------------------N----W-------Q------------------Q-W------------W-----I-----W-----T-------------------------S------------------L-----------G---------F-------W-------M-----F--------------------M----I------C----SV---------V-G--N--------L------W------------------V-------T---------V--------Y------------Y---G-------V-----------------P----V------------------------W---K--E-------A-------K----------T-----T-
> str48: M--A---------------V-E---P-----F-------PR----------R-----------P------------------I------------T----R----P---------------------------H----------A--------S-------I------E-----------V--D----------------T-----------S----GI----------------------G---------G--S--A---------G---S-------------------S---E---K-----V-----------F-----------------------------C----L--------I---------G----Q-----A-E-G--------------------G----E---P------NTV---------------------
> str49: M----F-------Y------A-H-----A--FG-------------------------------------G-------Y-D------E----N------L---H-------A-F----P-------------G-I------------------S------------------------STV-A----N-----D-------V------------------R------K-------------------Y------SV---------V-----SVY------N--------K---------K---------------Y-----N--------------I--------------------V----K-N-------K--------Y------------M----------W-----------------------------------------
> str50: M--A-----N---Y----S-----KP-----F------L----------L------D-------------------------I---V-F---N-----------------------K-------------D---I---------------------------K---C----I--N--------D------S-------------C-------S------------H------S--D-------------C------------R----------Y--------Q--------S---------N--S----------Y-------V-E-----------L-R---------------R--------NQ---A---L-------------N--------------K--------------------N-----L-----------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> best bound: 26.0
> ```
