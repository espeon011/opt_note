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
    model = scsp.model.didp.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.solution.is_optimal}")
    print(f"bset bound: {model.solution.best_bound}")
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
>  Sol: ultcikgnycosjiqefovoazkuhpmplngbxrxddbcsvrvnnshtuqgpxzvxissbxf
> str1: --t--kgn--------------kuh-mp----x----------n--ht-qg-xzvxis----
> str2: ----i-----o-jiq-fo----------ln-bx-x---c-v----s--uq-p--v-issbxf
> str3: ul-ci--nycos-----ovo-z---p-pl----------------------p----------
> str4: ----i-g--------e--v-az--------gb-r-ddbcsvrvnn-----g----------f
> 
> solution is feasible: True
> solution status: True
> bset bound: 62
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
> --- Solution (of length 99) ---
>  Sol: tikojigqfpypolrenbxzwxqkrdrevuldcphmqavzgtdpfjuibtvxernycdozhsdtmbocsvbruoqgxzpvxningsrbpsbhxlfwped
> str1: t-k---g---------n------k-----u----hm-------p-------x--n-----h--t----------qgxz-vx-i--s-------------
> str2: -i-oji-qf---ol--nbx--x----------c-----v----------------------s----------u-q---pv--i--s---sb-x-f----
> str3: -----------------------------ul-c--------------i------nyc-o--s----o--v---o---zp---------p----l--p--
> str4: -i----g--------e------------v--------a-zg-------b----r---d----d--b-csv-r-------v-n-ng---------f----
> str5: ---------pyp-lr----z-x-------u--cp-mq-v-gtd-f-ui--v-----cd---s---bo--------------------------------
> str6: ---------p-------b-------d-ev--dc-----v---dpf--------------z-s--m---s-br-oq----v-------b--bh-------
> str7: ---------------enb--------------c------z----fj---tvxer-----z-----b-----r-------v--i-g---p----l---e-
> str8: --------------r---x-wxqkrdr---l-c--------t----------------o---dtm-------------p-------r-p---x--w--d
> 
> solution is feasible: True
> solution status: False
> bset bound: 56
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
> --- Solution (of length 149) ---
>   Sol: pyplirsbxtoqjukgwsdeizaxqfolnkvbudcrfpgqazfhjtvdxgimpgebrxlunqyecfjdvzshigteowaduvqbnctmfpsokekburvmgidxozshkruqvjncozdswngpbxphabwlzekfvydnmcugiosph
> str01: ---------t----kg------------nk--u----------h-------mp----x--n----------h--t-------q-----------------g--x-z------v------------x------------------i-s--
> str02: ----i-----o-j-------i---qfoln--b----------------x--------x------c---v-s---------u-q------p--------v--i----s------------s----bx---------f-------------
> str03: -------------u-------------l------c---------------i---------n-y-c-----------o-------------so------v-----oz-----------------p--p----l---------------p-
> str04: ----i----------g---e----------v---------az-------g-----br----------d-----------d---b-c----s-------v----------r--v-n------ng------------f-------------
> str05: pypl-r---------------z-x--------u-c--p-------------m---------q------v----gt----d--------f-------u----i----------v--c--ds----b--------------------o---
> str06: p------b----------de----------v--dc-----------vd----p------------f---zs----------------m--s----b-r------o------qv-----------b----b------------------h
> str07: -------------------e--------n--b--c------zf-jtv-x-----e-r------------z-------------b-------------rv--i--------------------gp-------l-e---------------
> str08: -----r--x-------w------xq----k-----r-----------d--------r-l-----c---------t-o--d------tm-p-------r-------------------------p-x----w-------d----------
> str09: --------------k--------------k---------qa-f-------i--g-------q----j----------w-------------ok-k-----------s-kr--------------b------l-----------g-----
> str10: ---l----x--------------x-------------p--a--------------b----------------i--------v-b--------------v------z--k-------oz--------------z---v-d----------
> str11: --------------k--------------------r--------------i--------------f----s-------a--v--nc----------------d--------q--------w------h----z--------c-------
> str12: -----------q----------ax--------ud----gq------v--------------q--c----------e-w-----b----f-----------gi-----------j--o---w---------w------y-----------
> str13: -----rs-x--qj---------------n-------fp--a------d--i--------u----------s-i---------qb---------e-----------z-hk-------o----------h------------m--g-----
> str14: ----i-----------ws-------------------------h--v------------------------h-------------c-----o-------m-i--------u-v-----d-------------------d-m--------
> str15: -------------------------------------------h-t--x--------x---q----j--z------------qb-ct--------b--------------------------------a-----k----n---------
> str16: --------x----u---s-------f--------c-f----z----------p-e--------ec---v--------wa-----n-t-f----------mg----------q-----z------------------------u------
> 
> solution is feasible: True
> solution status: False
> bset bound: 49
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
> --- Solution (of length 27) ---
>   Sol: bbaeddcbacdeeecbdbceabdcead
> str01: ----d-cb-c----c-dbc----ce--
> str02: b---dd-b---eee-----e-bd----
> str03: ------c-acdee-c----e-b--e--
> str04: --aedd----d-----d--e-bd---d
> str05: --a---cb---ee-c-----ab-ce--
> str06: bba----b---e---bd-c--b---a-
> str07: bbae----a--e---b----a-d--a-
> str08: ---e-------eeecbdb-e----e--
> str09: ------c--cdee---d---a-dc--d
> str10: b---d---a------bdb-ea----ad
> 
> solution is feasible: True
> solution status: True
> bset bound: 27
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
>   Sol: daebcdeabecdabcedacbedabceabdceabd
> str01: d---c---b-c---c-d--b----c----ce---
> str02: ---b-d-----d-b-e----e----e----e-bd
> str03: ----c--a--cd---e----e---ce-b--e---
> str04: -ae--d-----d----d----d---e-bd----d
> str05: -a--c---be-----e--c---abce--------
> str06: ---b----b---ab-e---b-d--c--b---a--
> str07: ---b----b---a--e-a--e--b--a-d--a--
> str08: --e---e--e-----e--cb-d-b-e----e---
> str09: ----c-----cd---e----eda-----dc---d
> str10: ---b-d-ab--d-b-e-a----a-----d-----
> str11: --e--de----da----a----a--ea----a--
> str12: -a-----a-e--a----a-be----ea--c----
> str13: --e----a----abc--ac-----c---d---b-
> str14: ---b-de--e--a---d---e-a-----d-e---
> str15: ----c--a-e-da---d---e----e----e--d
> str16: --ebc--a---d-b---a-b---b-e--------
> str17: d----d----c----e----e-ab----d-ea--
> str18: da-bcd-----d---e-a--e---c---------
> str19: -a-----a---d--ce----eda---ab------
> str20: -ae---e---c---ce----e----ea----a--
> str21: ---b----b--da--e--c---a---a-d-e---
> str22: da--c-e----da--eda-b--------------
> str23: -a-----a-e--ab-----b---b---b-ce---
> str24: d-e--d--b-c--bc--a----ab----------
> str25: d--b-d-a----a--e---b---bc--b------
> str26: d-eb--e----d-b-e---b--a-c---------
> str27: ----c-e--e---bc-d-cb-d---e--------
> str28: d--b--e----da----a---da---ab------
> str29: ----c-----c---c-d-cbe--b----dc----
> str30: -ae---ea--cd-bc----b-d------------
> str31: da--c---be--a-c---c-----c---d-----
> str32: --e-c-e-b-c---c-d--b-d-b----------
> str33: d----d--b----bceda-b---b----------
> str34: -a-----a-e--ab---a----a--e-b---a--
> str35: --e-c---b----bc--a----a-----dc---d
> str36: d-ebc-----c----e--c--d-bc---------
> str37: da-----a--c--b---a--e----e-b-c----
> str38: -a---d-abe--a----ac-----ce--------
> str39: dae-cd--b---a-c--a----a-----------
> str40: da--c---b----b--d-c-ed--c---------
> str41: d-e--d--be-----e---b---b----d-e---
> str42: ----cd-a---d--c-d-c--da---a-------
> str43: ----c-e--e-d--c----b--a--e----e--d
> str44: ----c-ea-ec-a----a----a-c-a-------
> str45: d---c-----c---ce---b---b---b---a-d
> str46: ---b---a-e-----e-a--e--b---bd-e---
> str47: d--b-de-b---a-c---c--d-b----------
> str48: --ebc---be-----eda--e-a-----------
> str49: -ae---e--e---b-----b-d-bc-a-------
> str50: d--b-d-ab-c----e--cb---b----------
> 
> solution is feasible: True
> solution status: False
> bset bound: 24
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
>   Sol: TACTGGACCTGAATCAGATCGTAC
> str01: -A-TGG----GA-T-A---CG---
> str02: -A-T--ACCT---TC----C---C
> str03: --C---AC--GAAT----T-G-A-
> str04: TA----A----AATC---T-GT--
> str05: -A--GG---T-AA-CA-A----A-
> str06: T--T---CCT-A----G---GTA-
> str07: T--TG----T-A----GATC-T--
> str08: T---GG----GAA---G-T--T-C
> str09: T--T---CC--A--CA-A-C-T--
> str10: T-CT--A----AA-C-GA----A-
> 
> solution is feasible: True
> solution status: True
> bset bound: 24
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
> --- Solution (of length 133) ---
>   Sol: ATGACCGTAGTAACGTACTAGCATGCTATCAGTACGTCATGCATGCACTGCATGAGTCATCGTAACGCTAAGTCACTGACTAGCATGCAGTGCATGACGACTCGTACGATCGACGTAGACTGCACTGCATGCR
> str01: -T-A--GTAGTA--G-ACT--C---C-----G---G--A---A-G---TG-A-----CA----AAC-C-----C--TGA--A--A---AG---A--A----T-G---GAT--A---A-A-T--A-T--A----
> str02: --G---G-A-TAA---AC-A-C-T-C---C----CG--A---A---A----AT-A---AT--T-----T--G--ACT---TA--A---A---CA--ACG-C--G-AC-A--G---T----T-CA----A-G--
> str03: AT-ACC-T--T--C---CTAG---G-TA--A---C---A---A---AC--CA--A--C--C--AAC--T---T---T---T-G-AT-C--T-C-T------T-GTA-GATC----T-G---------------
> str04: -T-A----A--A---T--TA---T---A--A-T-C-T--T--AT--ACT--A-G--T-A----AA----AA---A-T-A---G---G--GTG--T-A--AC-CG-A--A---A---A--C-G----G--T-C-
> str05: -T-----TA--AA---AC-AGC---CT----GT--G----G---G---T---TG---CA-C----C-C-A---C--T--C-A-CA-G--G-GC----C--C----AC--T-G--G--G-C-GCA----A-G--
> str06: ATGAC--T--T--C---C-A--ATG------G-A--TC---C---CA----A-----C--C-T--C---AAG-C--T---T--C---CA---C----C--C-C--A--AT-G--GT----T----T-CA-GC-
> str07: A--AC---A--AAC---C-A--A--C---CA--AC-T--T---T----TG-AT----C-TC-T-----T--GT-A--GA-T--C-TG---T---T--C---TC-TA--A---ACG-A-AC-------------
> str08: ATGA----A--AACG-A--A--A----AT---TA--T--T--AT-CA----A-G-G-----GTA----T--G-----GA--AG--TG--G---A--A-G-CT-G-ACGA---A---A---T------------
> str09: A---C--T-----CG-----GC-TGC-AT--G--C-T--T--A-G---TGCA-----C-TC--A-CGC-A-GT-A-T-A--A---T----T--A--A----T---A--A-C----TA-A-T----T--A----
> str10: -T-----T-GTA--G-A-T--C-TG-T-TC--T-C-T-A---A---AC-G-A--A--C-T--T-----TAA---A---A-T--C-TG---TG--TG--G-CT-GT-C-A-C----T---C-------------
> str11: --G-C---AG-A--G--C-A---T--T-T---T-C-T-A---AT--A-T-C------CA-C--AA----AA-T----GA--AG---GCA----AT-A--A-T--T--G-T--AC-TA--CT-C----------
> str12: ATGA--G------C---C-A--A-G--ATC----CG--A--C--G-A----A-GAG-C--C----C-C-AAG-----GA---G---G-AG---A--A-G----G-A-G---G--G-A--C--C-C--C---C-
> str13: -T--C--T-----C--AC-AG--T--T--CA--A-G--A---A--C-C--CA--A---A--GTA-C-C-----C-C---C---CAT--AG--C----C--CTC-T----T--A---A-A--GC-C---A--C-
> str14: A-G---GT--T----TA-TA-C---CT-TC----C-T-A-G---G---T--A--A--CA----AAC-C-AA--C-C--A--A-C-T----T---T--CGA-TC-T-C--T-----T-G--T--A---------
> str15: A-G---GT--T----TA-TA-C---CT-TC----C--CA-G---G---T--A--A--CA----AAC-C-AA--C-C--A--A-C-T----T---T--CGA-TC-T-C--T-----T-G--T--A---------
> str16: -T-A----A--AAC--A--A-C-T-C-A--A-TAC---A---A--CA-T--A--AG--A----AA----A--TCA---AC--GCA---A----A--A--AC----AC--TC-AC--A-A----A---------
> str17: ----CCG------C---C---CAT--T-T--G---G----GC--G----GC-T----C-TCG-A--GC---G--A-T-A---GC-T-C-GT-C--GA--A-TC---C---C----T---C-G-AC--C-T---
> str18: AT-ACC-T--T--C---C---CA-G------GTA----A--CA---A----A-----C--C--AAC-C-AA--C--T---T----T-C-G---AT--C---TC-T----T-G---TAGA-T-C--TG------
> str19: -T--C--T-----C--AC-AG--T--T--CA--A-G--A---A--C-CT-CA--AGTC-TC----C-C-----C-C--A-TAG---GC----C-T--C---T--T----TC-A-GT---C---A--G------
> str20: --GA---T-----C-T-CT--C-T-C-A-C----CG--A---A--C-CTG---G---C--C----C-C---G-----G----GCA---A----ATG-C--C-C-TA--ATC--C--AGA--G----G--TG--
> str21: A-GA--G------C--A--A---T-C-A---GT--G-CAT-CA-G-A----A--A-T-AT---A-C-CTA--T---T-A-TA-CA--C--T---T------T-G--C--T--A---AGA----A-T-------
> str22: A--A---T--TAA---A--A-CAT-CT--CA--A--T-A--CA---AC---AT-A---A--G-AA----AA---AC--A--A-C--GCA----A--A--A-----AC-A-C----T---C---A-T-------
> str23: A--A----A----CG-A--A-C-T--T-T-A--A----A---AT-C--TG--TG--T----G----GCT--GTCACT--C--G---GC--TGCATG-C---T--TA-G-T-G-C-------------------
> str24: AT-A----A----C-TA--A---T--TA-C--T--GTC--G--T----TG-A-----CA--G----G--A---CAC-GA---G--T--A----A---C---TCGT-C--T--A--T---CT----T-C-TG--
> str25: ATGA--GT-GT--C--AC--G-A----AT---T-C---A--C--G---T--A-----CA----A----T--G--A---ACT-G---G-A-TG--T------TC--ACG-T-G--G-A-A-T--A----A----
> str26: A---CCGT-G----G-----GC--G--A---G--CG----G--TG-AC--C--G-GT----GT--C--T---TC-CT-A---G--TG--G-G--T--C--C-C--ACG-T-----T-GA----A--------R
> str27: A--A----AG----GT--T----T---AT-A---C--C-T---T-C-C--CA-G-GT-A----A-C---AA---AC---C-A--A--C----CA--AC---T--T----TCGA--T---CT-C--T---TG--
> str28: A-G----TAGT----T-C--GC---CT----GT--GT---G-A-GC--TG-A-----CA----AAC--T---T-A--G--TAG--TG---T---T------T-GT--GA--G--G-A---T----T--A----
> str29: -T-----T--TA---TAC---C-T--T--C----C-T-A-G---G---T--A--A--CA----AAC-C-AA--C-C--A--A-C-T----T---T--CGA-TC-T-C--T-----T-G--T--A--G-AT---
> str30: ATG-C-G--GT--CGT-CT--C-T-C---C----C--C--G---GC--T---T---T--T--T-----T---TC-C---C---C--GC-G--C----CG-C--GT----T-G--G----C-GC-C-G-A----
> str31: --G----T-G-A-C--A--A--A----A--A---C---AT--A---A-TG---GA--C-TC----C---AA--CAC---C-A---TG---T-CA--A-G-CT--T----TC-A-G--G--T--A--G-A--C-
> str32: --G----T-GTAA-G-A--A--A--C-A---GTA----A-GC---C-C-G---GA---A--GT---G----GT----G--T----T----T---TG-CGA-T--T----TCGA-G--G-C--C---G---G--
> str33: --GA--G-A--A---T----G-A-G-T--C--T-C---AT---T--AC--C--G---C--C----CG----GT-ACT---TAGCA---AG--C-T-A--A-T---A-G-TC-ACG--G-C-------------
> str34: ATG----T-G----GT-C--G-ATGC---CA-T--G----G-A-G----GC------C--C--A-C-C-A-GT---T--C-A---T----T--A--A-G----G--C--TC--C-T-G---GCA-T---T---
> str35: A---C-G-AG---CGT--T----T--TA--AG---G----GC---C-C-GC--GA--C-T-G---CG--A---C---G----GC---CA---CATG--G-C-C---C--T-G---TA---TG---T-------
> str36: --G---GT--T----TA-TA-C---CT-TC----C--CA-G---G---T--A--A--CA----AAC-C-AA--C-C--A--A-C-T----T---T--CGA-TC-T-C--T-----T-G--T--A--G------
> str37: -TG---G--G-AA-GT--T--C---C-A--A--A----A-G-AT-CAC---A--A---A----A-C---A---C--T-AC---CA-G---T-CA--AC--CT-G-A--A--G---TA--C---AC--------
> str38: --GA----AG---CGT--TA--A--C-----GT--GT--TG-A-G----G-A--A---A----A--G--A---CA--G-CT----T--AG-G-A-GA--AC----A--A--GA-G----CTG----G---G--
> str39: A---CC--AG---CG--C-A-C-T--T--C-G---G-CA-GC--G----GCA-G---CA-C----C--T----C---G----GCA-GCA---C----C---TC--A-G--C-A-G----C---A----A--C-
> str40: ATG---G--G-A-C--A--A-C-T--TAT---T-C--C-T--AT-CA-TG--TG---C--C--AA-G--A-G-----G--T----T----T---T-AC--C-CG---G-T-GAC-----C---A---------
> str41: -T-----T-GTA--G-A-T--C-TG-T-TC--T-C-T-A---A---AC-G-A--A--C-T--T-----TAA---A---A-T--C-TG---TG--TG--G--T--T--G-TC-AC-T---C-------------
> str42: A--ACC--A--A-C---C-A--A--CT-T---T-CG--AT-C-T-C--T---TG--T-A--G-A----T----C--TG--T----T-C--T-C-T-A--A-----ACGA---AC-T----T----T--A----
> str43: --G---G--GT----T-CT-GC---C-A---G---G-CAT--A-G---T-C-T---T--T--T-----T---T---T--CT-G---GC-G-GC----C--CT--T--G-T-G---TA-A----AC--C-TG--
> str44: --G---G------C-T----GCATGCT-T-AGT--G-CA--C-T-CAC-GCA-G--T-AT---AA---T---T-A---A-TA--A--C--T--A--A----T--TAC--T-G---T-----------------
> str45: -TG-C---A-T---G--CT----T---A---GT--G-CA--C-T-CAC-GCA-G--T-AT---AA---T---T-A---A-TA--A--C--T--A--A----T--TAC--T-G---T---C-G---T-------
> str46: -T-----T-----C---C-A-CA----A-C--T---T--T-C---CAC--CA--AG-C-TC-T---GC-AAG--A-T--C---C---CAG---A-G-----TC--A-G---G--G--G-C--C--TG--T---
> str47: -T--C--TA--AACG-A--A-C-T--T-T-A--A----A---AT-C--TG--TG--T----G----GCT--GTCACT--C--G---GC--TGCATG-C---T--TA-G-------------------------
> str48: A---CCG--G-A---T----G---GC---C-G--CG--AT---T----T---T---TC---G----G--A-GTC-CT---T-G---G--G-G---GAC--C----AC--TC-A-G-A-A-T--A--G-A----
> str49: ----C--T--T---GTA---G-AT-CT----GT---TC-T-C-T--A----A--A--C---G-AAC--T---T---T-A--A--A---A-T-C-TG-----T-GT--G---G-C-T-G--T-CACT-------
> str50: ATGA--G------C--ACTA--A-GC-----G-A----A-G-A---AC--CA--A---A----AA-GC-A-G--AC--A--A---T--A---CA--AC--C-CG--C--T--A--T----T--AC--------
> 
> solution is feasible: True
> solution status: False
> bset bound: 84
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
> --- Solution (of length 44) ---
>   Sol: MQSKFTPEASLRENSYAQHVFDAINSRCPGVFNEKGTAGLHDYQ
> str01: M-------A-L---SY-----------CP-----KGT-------
> str02: MQS------SL--N--A------I----P-V-------------
> str03: M-----P---L---SY-QH-F-----R-------K---------
> str04: M------E----E-----HV----N--------E-----LHD--
> str05: M-S----------N------FDAI--R----------A-L----
> str06: M---F------R-N---Q------NSR-----N--G--------
> str07: M---F----------YA-H---A--------F---G--G---Y-
> str08: M-SKFT-----R--------------R-P-------------YQ
> str09: M-S-F--------------V--A------GV-----TA-----Q
> str10: M------E-SL--------V--------PG-FNE----------
> 
> solution is feasible: True
> solution status: False
> bset bound: 29
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
> --- Solution (of length 503) ---
>   Sol: MPSNWGFLLADIERVSKYPNFAREAIHGNYPAQDTILSAGKELFVARNDYATIHLPDFEKWPSLIVNGDKRQLPVTGLSDMFYAEQKRLHFIAEPIATGNWALDRVEKQLNTRLYPAEMWDGFSKLATEIHNSAQKVCWDNIGVPHQYFNRKLETGDASKVMCATILPFRQCEPFKANYGLITFSVDEWRNIFKEATNHSLIGAYCDPQHSRGVDTQENKMHVSAFTPILRADNYVLSFALGCKVDQMEFIGATCNPSVVLPRAFEAGSQLHKTNDEVRYSMRQAIDLPWKTESCRFAYNLIGDLTDCAEVIDMTWYAGCHFISELRNDAVKYLESHFGWKNIVDTHIAQRFTCSLRGPVYSAKDEENIHDRSMPETGFADVLPADEINFKYRVPKFQGIYALCSFADRGELTKQWPCINREGAEDVIDSGLTMFECRDTLFPQSVYMAKGEDHNSADIWALNGQKGRAHVYIQMTLSTHKCAHDRGKQDFSNLGVIHLWTPR
> str01: M------------R------------H---------L----------N----I---D-------I-------------------E------------T----------------Y--------S--------S-------N---------------D--------I---------K-N-G-----V------------------Y--------------K--------------Y----A-----D------A------------E---------D--------------------F------------E-I-------------L-------L---F----------A-----------YS------I-D------G--------------------G-----------E---------------V--------EC---L-----------D--------L-------------T---------R-----------------
> str02: M-----------ER--------R-A-H-------------------R----T-H-----------------Q---------------------------NW--D------------A----------T-------K--------P-----R--E---------------R-------------------R---K--------------Q------TQ----H--------R-----L----------------T-----------------H----------------P--------------D--D----------------S------------------I-----------------Y-------------P-----------------R------I----------E--K---------AE-----G------R-----------K-EDH---------G---------------------------------------
> str03: M-----------E-----P--------G---A-----------F------------------S------------T-------A----L-F------------D------------A--------L-----------C-D----------------D--------IL-------------------------------H------------R------------------R-----L-----------E--------S-----------QL-------R-----------------F-----G---------------G-----------V------------------Q------------------I-----P--------P--E------V----------S--D--------P---R-----V-------------------Y-A-G--------------------Y----------A----------L----L----
> str04: M----G----------K---F--------Y-------------------Y------------S---N---R----------------RL---A------------V----------------F---A-------Q----------------------A------------Q-------------S----R--------H-L-G---------G----------S----------Y-------------E--------------------Q-------------------W----------L-------A----------C----------V----S--G-----D---------S-------A---------------F-------------R--------A--------E---------------V----------------------K------A----------R--V--Q------K---D------------------
> str05: ------F-------------F-RE----N-------L-A----F---------------------------Q-------------Q------------G--------K--------A---------------------------------R--E--------------F----P----------S--E------EA---------------R------------A--------N---S------------------P----------------T------S-R---------E-------L--------------W--------------V-------------------R-----RG-------------------G----------N-----P-------L-S-----E------------A------G-----------------A--E---------------R-----------------RG-------------T--
> str06: M---------D-------P------------------S----L--------T-------------------Q--V-------------------------WA---VE--------------G-S------------V---------------L-----S----A------------A--------VD---------T------A-------------E--------T------N-----------D-------T-----------E----------------------P--------------D-----E--------G------L---------S------------A----------------E-N-------E-G--------E-------------------------T-------R------I------------------------------I--------R----I--T----------G----S-----------
> str07: M--------A----------F------------D---------F------------------S--V---------TG----------------------N-----------T------------KL-------------D--------------T---S--------------------G---F------------T-----------Q---GV---------S-------------S---------M-----T----V----A--AG-----T-------------L-------------I------A---D------------L----VK-------------T--A-----S------S-----------------------------------Q----L---------T------N-----------L----------------A---------------Q------------S-------------------------
> str08: M--------A----V----------I----------L------------------P------S------------T------Y--------------T-----D-----------------G-----T-----A-----------------------A----C-T------------N-G----S----------------------P------D-------V------------V-----G-----------T-------------G-----T-------M-------W--------------------V----------------N-----------------T-I-------L--P------------------G--D--------F------F------------------W----------------T---------P-S-----GE---S--------------V--------------R---------V-------
> str09: M--N------------------------------T----G------------I-----------I---D---L--------F---------------------D------N-------------------H-----V--D------------------S------I-P--------------T--------I--------L------P-H------Q------------L-A---------------------T------L--------------D---Y-------L----------------------V---------------R------------------T-I--------------------I-D----E------------N---R-----------S---------------------V----L--------LF-----------H----I---------------M-----------G----S--G--------
> str10: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N--L----------------R------------T------R------T-----------Q--------------------L--------------------------P----P-A---------------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------S-----------
> str11: M---------D----SK------E----------TIL---------------I-----E-----I--------------------------I--P------------K---------------------I-----K----------------------S-------------------Y-L-------------------L-----D--------T--N---------I--------S------------------P---------------K-------S-----------------YN---D-----------------FIS--RN---K---------NI--------F-------V--------I-------------------N-------------L-------------------------------------------Y-------N---------------V------ST-----------------I------
> str12: M------LL------S-----------G------------K------------------K---------K----------M-------L-------------LD------N---Y--E---------T-----A-----------------------A-----A-----R---------G---------R------------G---------G-D--E------------R-------------------------------R---------------R-----------------------G------------W-A---F------D---------------------R-------P---A-----I------------V------------------------------TK------R----D-----------------------K-----S-D---------R------M-------AH-------------------
> str13: M--N-G------E----------E---------D--------------D-----------------N-----------------EQ------A---A----A----E-Q-------------------------Q-------------------T----K---------------KA----------------K-----------------R-----E-K-------P---------------K--Q-----A---------R---------K----V-------------T-S---------------E-------A---------------------W-------------------------E---H--------F-D---A---------------------------T------------D--D-G-----------------A--E-----------------------------C-----K---------H-----
> str14: M-----------E--S--------------------L-------V----------P-----------G-------------F-----------------N------EK---T------------------H-----V---------Q-----L-----S-------LP-----------------V--------------L-------Q----V----------------R-D--VL-------V-----------------R----G----------------------------F-----GD-------------------S------V---E------------------------------E---------------VL---------------------S-----E------------A-------------R-----Q---------H-------L---K------------------D-G-------------T--
> str15: M------------R---Y-------I------------------V-----------------S----------P-----------Q--L----------------V---L------------------------Q-V-----G--------K---G--------------Q-E------------V-E-R-----A----L---Y------------------------L-----------------------T--P----------------------Y------D-----------Y--I-D-----E---------------------K---S----------------------P---------I----------------------Y--------Y----F-----L--------R--------S-----------------------H-------LN---------IQ-----------R---------------P-
> str16: MP-----------RV---P-------------------------V----Y------D-----S----------P-----------Q-------------------V-----------------S--------------------P----N----T-----V------P--Q-----A------------R----------L--A-----------T-----------P---------SFA-------------T--P----------------T----------------------F-----------------------------R-----------G---------A---------------D--------------A---PA----F-------Q---------D----T----------A------------------------------N---------Q--------Q--------A--R--Q--------------
> str17: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N--L----------------R------------T------R------T-----------Q--------------------L--------------------------P---L--A---------------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------S-----------
> str18: M-----F-------V-----F----------------------FV---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N--L-T---------T----R------------T-------------------------Q--------------------L--------------------------P----P-A---------------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------S-----------
> str19: M-----------E--------A---I---------I-S-----F-A---------------------G-----------------------I------G------------------------------I-N---------------Y---K-------K------L---Q-------------S--------K------L-------QH----D----------F---------------G--------------------R--------------V---------L--K------A--L----T----V---T--A--------R--A---L------------------------P------------------G-------------------Q------------------P--------------------------------K---H----I-A-----------I------------R--Q--------------
> str20: M--------A-----S---------------------S-G---------------P--E-----------R------------AE----H------------------Q--------------------I-----------I----------L--------------P----E-----------S-------------H-L---------S------------S---P-L-----V-------K---------------------------HK--------------L------------L---------------Y---------------Y------WK--------------L--------------------TG----LP------------------L-------------P--------D---------EC-D--F----------DH-------L----------I------------------------------
> str21: M-----------E--S--------------------L-------V----------P-----------G-------------F-----------------N------EK---T------------------H-----V---------Q-----L-----S-------LP-----------------V--------------L-------Q----V----------------R-D--VL-------V-----------------R----G----------------------------F-----GD-------------------S------V---E------------------------------E---------------VL---------------------S-----E---------------V----------R-----Q---------H-------L---K------------------D-G-------------T--
> str22: M------L-A--------P------------------S-----------------P----------N-----------S-------K----I----------------QL------------F--------N--------NI-------N---------------I--------------------D----I-----N------Y------------E---H----T--L----Y---FA-----------------SV---------S---------------A----------------------------------------------------------------Q-----------------N----S-----F----------F-----------A------------QW----------V------------------VY--------SAD-------K--A---I------------------------------
> str23: M-S------A-I----------------------T------E---------T-------K-P-------------T---------------I-E--------L------------PA--------LA-E-------------G-----F---------------------Q------------------R--------------Y-------------NK------TP-------------G-------F---TC---V-L--------------D--RY------D---------------------------------H-----------------G----V---I-------------------N--D-S-----------------K--------I--------------------------V----L--------------Y-------N------------------------------------------------
> str24: M---------------K--N-----I-----A---------E-F---------------K---------K-------------A----------P-----------E--L------AE------KL--------------------------LE------V-------F---------------S-----N---------L------------------K---------------------G-------------N-S----R-----S-L----D------------P------------------------M------------R--A--------G-K-----H-----------------D----------------V-----------V--------------------------------VI-------E--------S------------------------------T----K------K-----L---------
> str25: MP------------------------------Q----------------------P-------L-----K-Q------S---------L--------------D----Q--------------SK-------------W-------------L----------------R--E---A----------E-----K----H-L----------R------------A----L------------------E--------S--L----------------V--------D------S-----NL--------E--------------E---------E-----K--------------L-------K----------P----------------------Q----L-S----------------------------M----------------GED-----------------V--Q---S-------------------------
> str26: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N--L------------I----------------T------R------T-----------Q-S-----------------------Y------------------T-N-S------F--------T----R-----------------------G-------V-----Y---------------Y-------------------------P-----D-------------------------K--V--F-----------R--------------------S--------------SV---------------L-------H-------ST---------QD-------------
> str27: M---------------K---F------------D----------V---------L-------SL-----------------F-A----------P-----WA-----K----------------------------V--D-------------E----------------Q-E-----Y-------D---------------------Q-------Q------------L---N---------------------N------------------N------------L----ES-------I---T--A-------------------------------------------------P----K--------------F-D----D------------G--A----------T--------E-----I-------E--------S------E---------------R------------------G--D------I------
> str28: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N------------------F-------------T-------N--------------------R---TQ------------L--------------------------PS-----A---------------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------S-----------
> str29: M---W----------S---------I---------I--------V---------L----K---LI-------------S------------I----------------Q------P---------L--------------------------L-------------L------------------V----------T--SL------P---------------------L----Y--------------------NP-----------------N------M----D------SC------------C-----------------L----------------I-----------S-R-----------I-------T------P--E---------------L---A--G---K-----------------LT--------------------------W------------I-----------------F-----I------
> str30: M-----------E--S--------------------L-------V----------P-----------G-------------F-----------------N------EK---T------------------H-----V---------Q-----L-----S-------LP-----------------V--------------L-------Q----V----------------R-D--VL-------V-----------------R----G----------------------------F-----GD-------------------S------V---E------------------------------E------------F---L---------------------S-----E------------A-------------R-----Q---------H-------L---K------------------D-G-------------T--
> str31: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----------------M-----P------------L--F------N---------LI-------------T----------T--------------------------T---------------Q----------S-----------------Y------T---------------------N---------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-------------L---------
> str32: M-------------------------H-----Q--I---------------T-------------V--------V---S-------------------G----------------P-----------TE-------V---------------------S-----T------C--F----G----S---------------L--------H-----------------P----------F-------Q----------S--L-----------K---------------P---------------------V--M---A---------N-A---L----G----V-----------L---------E-----------G------------K------------------------------------------MF-C-------S-------------I----G--GR---------S---------------L---------
> str33: M--------A------------------------T-L-----L---R---------------SL-------------------A----L-F----------------K----R------------------N---K---D-----------K---------------P-----P-------IT-S-----------------G-------S-G----------------------------G----------A--------------------------------I---------R------G--------I-------------------K----H-----I----I--------------------I------------V-P---I------P---G--------D---------------------S--------------S-------------I----------------T--T------R-----S----------R
> str34: M-----------E--S--------------------L-------V----------P-----------G-------------F-----------------N------EK---T------------------H-----V---------Q-----L-----S-------LP-----------------V--------------L-------Q----V----------------R-D--VL-------V-----------------R----G----------------------------F-----GD-------------------S-------------------------------------------------M-E----------E------V--------L-S-----E------------A-------------R-----Q---------H-------L---K------------------D-G-------------T--
> str35: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N--L-T---------T--------------G--T-------------------------Q--------------------L--------------------------P----P-A---------------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------S-----------
> str36: M--------A---------N-----I---------I-----------N------L-----W-----NG-----------------------I-------------V---------P--M-----------------V---------Q---------D---V----------------N-------V---------A---S-I-------------T--------AF-----------------K-------------S-----------------------M---ID-----E------------T---------W------------D--K--------K-I----------------------E-------------A--------N-----------------------T----CI----------S-------R-----------K---H-------------R------------------------N----------
> str37: M------L-----------N--R--I------Q-T-L-------------------------------------------M-----K----------T---A--------N--------------------N---------------Y-----ET----------I------E--------I------------------L----------R------N---------------Y-L-------------------------R-------L--------Y-----I---------------I--L---A-----------------RN------E------------------------------E-----------G--------------R-----GI--L---------------I---------------------------Y-----D----D----N---------I-----------D------S---V-------
> str38: M--------AD-------P--A-----G------T------------N-------------------G----------------E--------E----G------------T---------G---------------C--N-G---------------------------------------------W---F-----------Y--------V---E------A----------V--------V---E-----------------------K-----------------KT----------GD----A--I-----------S----D---------------D--------------------E-N-------E------------N------------------D---------------------S--------DT----------GED--------L--------V-------------D------------------
> str39: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----N--L----------------R------------T------R------T-----------Q--------------------L--------------------------P----P------S----------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------S-----------
> str40: M-----------E--S--------------------L-------V----------P-----------G-------------F-----------------N------EK---T------------------H-----V---------Q-----L-----S-------LP-----------------V--------------L-------Q----V----------------------------C--D------------V-L----------------VR-----------------------G------------------F----------------G-----D---------S----V-----EE--------------VL---------------------S-----E------------A-------------R-----Q---------H-------L---K------------------D-G-------------T--
> str41: M--N---------------N------------Q-------------R------------K---------K-----T-------A---R------P----------------------------S------------------------FN-----------M----L--------K-------------R-----A---------------R------N-----------R----V-S---------------T----V---------SQL-------------A-----K----RF--------------------------S-------K------G----------------L--------------------------L---------------------S----G----Q-------G-------------------P----M-K-----------L--------V---M-------A-------F------------
> str42: M-SN--F---D----------A---I--------------------R---A---L----------V--D------T---D---A------------------------------Y---------KL----------------G--H-------------------I--------------------------------H---------------------M-------------Y---------------------P--------E-G-----T--E--Y------------------------------V--------------L---------S-----N---------FT-----------D------R-----G--------------------------S---R---------I--EG---V-----T--------------------H---------------------T-------------------V-H-----
> str43: M----------IE-----------------------L---------R------H----E------V-----Q----G--D--------L----------------V-----T-----------------I-N----V------V---------ET------------P----E-------------D-------------L-----D-----G------------F----R-D-----F-----------I-----------RA-------H---------------L-------------I-----C-----------------L---AV-------------DT-------------------E----------T-----------------------------------T---------G--------L------D-------------------I------------Y-------------------------------
> str44: M-----F-------V-----F---------------L-------V---------L--------L---------P---L---------------------------V-----------------S--------S-Q--C-----V-----------------M-----P------------L--F------N---------LI-------------T----------T------N------------Q----------S---------------------Y-----------T-------N-----------------------S-------------F-------T----R------G-VY------------------------------Y--P------------D-----K------------V-------F--R------S----------S--------------V-----L--H-----------------------
> str45: M-S-------------K----------------D--L-------VAR------------------------Q-----------A----L-----------------------------M--------T-----A----------------R----------M-------------KA---------D-----F--------------------V-----------F------------F-L--------F--------V-L----------------------------WK------A--L----------------------S-L--------------------------------PV--------------P-T---------------R----------C----------Q---I------D-------M--------------AK---------------K----------LS----A---G----------------
> str46: M--------A-----S--------------------L-----L----------------K--SL-----------T-L---F----KR---------T------R---------------D-------------Q---------P----------------------P------------L--------------A---S--G-------S-G----------------------------G----------A--------------------------------I---------R------G--------I-------------------K----H------V---I--------------------I------------VL----I------P---G--------D---------------------S--------------S-------------I-----------V----T---------R-----S----------R
> str47: M------------RV-------R----G-------IL---------RN------------W----------Q-------------Q--------------W------------------W---------I--------W---------------T---S-------L------------G---F----W-------------------------------M----F---------------------M--I---C--SVV-------G------N------------L-W--------------------V---T---------------V-Y---------------------------Y----------------G---V-P---------V---------------------W---------------------------------K-E----A--------K---------T--T------------------------
> str48: M--------A----V--------E------P------------F-----------P--------------R----------------R------PI-T------R----------P--------------H--A------------------------S------I------E------------VD---------T--S--G-------------------------I------------G---------G-----S-----A---GS-----------S-----------E--------------------------------------K-----------V-------F-C-L------------I--------G-------------------Q---A--------E-----------G-------G----E------P-----------N--------------------T-------------------V-------
> str49: M-----F----------Y---A----H----A-----------F-----------------------G--------G-----Y--------------------D--E---N--L----------------H--A--------------F------------------P-----------G-I--S--------------S---------------T------V-A--------N-----------D------------V---R---------K------YS-----------------------------V-------------------V----S-------V----------------Y------N----------------------K----K----Y------------------N-------I-----------------V---K----N----------K-----Y--M------------------------W---
> str50: M--------A---------N---------Y-------S--K--------------P-F-----L--------L------D-----------I-------------V----------------F--------N---K---D-I---------K----------C--I-----------N--------D------------S-----C----S----------H-S--------D---------C-------------------R----------------Y---Q---------S-----N-----------------------S--------Y----------V---------------------E----------------L---------R---------------R----------N-----------------------Q----A------------LN--K--------------------------NL---------
> 
> solution is feasible: True
> solution status: False
> bset bound: 93
> ```
