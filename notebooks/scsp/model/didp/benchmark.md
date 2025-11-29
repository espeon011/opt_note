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
Model = scsp.model.didp.Model
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
>  Sol: ulctikgnkycuhosjmiqfoevoazppgblrddnbxxcsvrvnnshtuqgxpzvxissbxf
> str1: ---t-kgnk--uh---m---------p---------x------n--ht-qgx-zvxis----
> str2: ----i--------o-j-iqfo---------l---nbxxc-v----s--uq--p-v-issbxf
> str3: ulc-i--n-yc--os-----o-vo-zpp--l---------------------p---------
> str4: ----i-g--------------ev-az--gb-rdd-b--csvrvnn-----g----------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 1.179607s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
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
>  Sol: iojiqfotkpbyplrgxdevanzgbwxqkulrdcphmzfjtqvdpxeirnlbycgtodfzhtsmvsboprvnuinoqgxzpvxwiscdsbxfbhplpeo
> str1: -------tk------g-----n------ku-----hm-------px---n----------ht--------------qgxz-vx-is-------------
> str2: iojiqfo------l-------n--b-x------------------x-------c----------vs------u---q---pv--is--sbxf-------
> str3: -----------------------------ul--c-------------i-n--yc--o-----s----o--v----o---zp-------------plp--
> str4: i--------------g--eva-zgb------rd----------d-------b-c--------s-v----rvn--n--g-------------f-------
> str5: ---------p-yplr-------z---x--u---cp-m----qv-----------gt-df-------------ui-------v----cdsb--------o
> str6: ---------pb------dev------------dc--------vdp-------------fz--sm-sb--r-----oq----v-------b--bh-----
> str7: ------------------e--n--b--------c---zfjt-v--xe-r----------z------b--rv--i---g--p--------------l-e-
> str8: --------------r-x--------wxqk--rd---------------r-l--c-tod---t-m----pr----------p-xw---d-----------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 99
> best bound: 56.0
> wall time: 60.559699s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
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
>   Sol: pypltrisxuqkojgwbdseinzaxqfolbkuvdncqparzfgbvhzmdipjqtxvxegrfnlqdyecvujzsiehtwoudqbavnmctkesfozumbpgdvihkrjovskixqzpgunwczvdrsbpxahknwiobldzmgfesphyc
> str01: ----t------k--g------n--------ku-------------h-m--p---x------n-------------ht----q-----------------g------------x-z-------v-----x-----i---------s----
> str02: ------i-----oj------i----qfol-----n--------b----------x-x----------cv---s------u-q----------------p--vi------s---------------sb-x-------------f------
> str03: ---------u------------------l------c-------------i-----------n---y-c----------o------------s-o-------v-----o------zp-----------p---------l-------p---
> str04: ------i-------g----e------------v-----a-z-gb---------------r----d---------------d-b----c---s---------v---r--v---------n-------------n--------gf------
> str05: pypl-r----------------z-x------u---c-p---------m----q--v--g-----------------t---d-----------f--u------i-----v-----------c--d-sb--------o-------------
> str06: p---------------bd-e------------vd-c--------v---d-p---------f----------zs-------------m----s-----b-------r-o-----q--------v---b---------b---------h--
> str07: -------------------e-n-------b-----c----zf---------j-t-vxe-r-----------z----------b----------------------r--v--i----g----------p---------l-----e-----
> str08: -----r--x------w--------xq----k--------r--------d----------r--l----c--------t-o-d-------t-------m-p------r---------p------------x----w----d----------
> str09: -----------k------------------k-----q-a--f-------i--------g----q------j------wo----------k--------------k----sk-------------r-b----------l---g-------
> str10: ---l----x---------------x------------pa----b-----i-----v--------------------------b-v---------z---------k--o------z------zvd-------------------------
> str11: -----------k---------------------------r---------i----------f-----------s----------avn-c------------d------------q-----w----------h--------z--------c
> str12: ----------q------------ax------u-d--------g---------q--v-------q---c------e--w----b---------f------g--i---jo-----------w-------------w-------------y-
> str13: -----r-sx-q--j-------n----f----------pa---------di-------------------u--si-------qb-------e---z--------hk--o----------------------h---------mg-------
> str14: ------i--------w--s--------------------------h---------v-------------------h-----------c-----o--m-----i--------------u----vd--------------d-m--------
> str15: ---------------------------------------------h-------tx-x------q------jz---------qb----ct--------b-------------------------------a-kn----------------
> str16: --------xu--------s-------f--------c-----f----z---p------e--------ecv--------w-----a-n--t---f---m--g-------------qz--u-------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 149
> best bound: 49.0
> wall time: 60.191138s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
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
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 27.0
> wall time: 4.657037s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
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
>   Sol: daecbdebaecdabcdeacbedabceabdcebad
> str01: d--cb-----c---cd---b----c----ce---
> str02: ----bd-----d-b--e---e----e----eb-d
> str03: ---c----a-cd----e---e---ce-b--e---
> str04: -ae--d-----d---d-----d---e-bd----d
> str05: -a-cb-e--ec-abc-e-----------------
> str06: ----b--ba----b--e--b-d--c--b----a-
> str07: ----b--bae--a---e--b--a-----d---a-
> str08: --e---e--e------e-cb-d-b-e----e---
> str09: ---c------cd----e---eda-----dc---d
> str10: ----bd--a----b-d---be-a---a-d-----
> str11: --e--de----da----a----a--ea-----a-
> str12: -a------ae--a----a-be----ea--c----
> str13: --e-----a---abc--ac-----c---d--b--
> str14: ----bde--e--a--dea---d---e--------
> str15: ---c----ae-da--de---e----e--d-----
> str16: --e-b-----c-a--d---b--ab---b--e---
> str17: d----d----c-----e---e-ab----d-e-a-
> str18: da--b-----cd---dea--e---c---------
> str19: -a------a--d--c-e---eda---ab------
> str20: -ae---e---c---c-e---e----ea-----a-
> str21: ----b--b---da---e-c---a---a-d-e---
> str22: da-c--e----da---e----dab----------
> str23: -a------ae--ab-----b---b---b-ce---
> str24: d-e--d-b--c--bc--a----ab----------
> str25: d---bd--a---a---e--b---bc--b------
> str26: d-e-b-e----d-b--e--b--a-c---------
> str27: ---c--e--e---bcd--cb-d---e--------
> str28: d---b-e----da----a---da---ab------
> str29: ---c------c---cd--cbe--b----dc----
> str30: -ae---e-a-cd-bc----b-d------------
> str31: da-cb-e-a-c---c---c--d------------
> str32: --ec--eb--c---cd---b-d-b----------
> str33: d----d-b-----bc-e----dab---b------
> str34: -a------ae--ab---a----a--e-b----a-
> str35: --ecb--b--c-a----a---d--c---d-----
> str36: d-e-b-----c---c-e-c--d-bc---------
> str37: da------a-c--b---a--e----e-b-c----
> str38: -a---d--a----b--ea----a-c----ce---
> str39: daec-d-ba-c-a----a----------------
> str40: da-cb--b---d--c-e----d--c---------
> str41: d-e--d-b-e------e--b---b----d-e---
> str42: ---c-d--a--d--cd--c--da---a-------
> str43: ---c--e--e-d--c----b--a--e----e--d
> str44: ---c--e-aec-a----a----a-c-a-------
> str45: d--c------c---c-e--b---b---b----ad
> str46: ----b---ae------ea--e--b---bd-e---
> str47: d---bdeba-c---cd---b--------------
> str48: --e-b-----c--b--e---eda--ea-------
> str49: -ae---e--e---b-----b-d-bc-a-------
> str50: d---bd--a----bc-e-cb---b----------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 24.0
> wall time: 61.804317s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
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
>   Sol: TACTACGGCTAGATCAGACTGATC
> str01: -A-T--GG---GAT-A--C-G---
> str02: -A-TAC--CT---TC---C----C
> str03: --C-ACG---A-AT-----TGA--
> str04: TA--A-----A-ATC----TG-T-
> str05: -A----GG-TA-A-CA-A---A--
> str06: T--T-C--CTAG----G--T-A--
> str07: T--T--G--TAGATC----T----
> str08: T-----GG---GA--AG--T--TC
> str09: T--T-C--C-A---CA-ACT----
> str10: T-CTA-----A-A-C-GA---A--
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 24.0
> wall time: 0.440073s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
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
>   Sol: ATGACCGTAGTAACGTACTAGCATGCAATCGTACGTACTGATGCAGTCTACGTCACGATCAGTACGATCATGCTAGACTGAGTCAACGATCTAGCGACTGCTGACATCGTACGTAGCATCGACTCATGATGCR
> str01: -T-A--GTAGTA--G-ACT--C---C----G---G-A---A-G---T----G--AC-A--A--AC---C---CT-GA---A---AA-GA---A-----TG--GA--T---A---A--AT--A-T-A-------
> str02: --G---G-A-TAA---AC-A-C-T-C---C---CG-A---A---A----A--T-A--AT---T----T---G--A--CT---T-AA--A-C-A---AC-GC-GACA--GT---T--CA---A-----G-----
> str03: AT-ACC-T--T--C---CTAG---G---T---A---AC--A---A----AC--CA--A-C----C-A--A--CT----T---T------T---G--A-T-CT--C-T--T--GTAG-ATC---T---G-----
> str04: -T-A----A--A---T--TA---T--AATC-T---TA-T-A--C--T--A-GT-A--A--A--A--A--AT---AG---G-GT----G-T--A---AC--C-GA-A----A---A-C---G------G-T-C-
> str05: -T-----TA--AA---AC-AGC---C--T-GT--G----G--G---T-T--G-CAC---C----C-A-C-T-C-A--C--AG-----G-----GC--C--C--AC-T-G---G--GC---G-C--A--A-G--
> str06: ATGAC--T--T--C---C-A--ATG-----G-A--T-C-----C---C-A----AC---C--T-C-A--A-GCT----T----C--C-A-C---C--C--C--A-AT-G---GT----T----TCA-G---C-
> str07: A--AC---A--AAC---C-A--A--C---C--A---ACT--T----T-T--G--A---TC--T-C--T--TG-TAGA-T----C-----T---G----T--T--C-TC-TA---A--A-CGA---A-----C-
> str08: ATGA----A--AACG-A--A--A---A-T--TA--T--T-AT-CA----A-G----G----GTA---T---G---GA---AGT----G-----G--A------A----G--C-T-G-A-CGA---A--AT---
> str09: A---C--T-----CG-----GC-TGCA-T-G--C-T--T-A-G---T----G-CAC--TCA---CG--CA-G-TA---T-A---A----T-TA---A-T----A-A-C-TA---A---T----T-A-------
> str10: -T-----T-GTA--G-A-T--C-TG---T--T-C-T-CT-A---A----ACG--A--A-C--T----T--T---A-A---A---A----TCT-G----TG-TG-----G--C-T-G--TC-ACTC--------
> str11: --G-C---AG-A--G--C-A---T----T--T---T-CT-A---A-T--A--TC-C-A-CA--A--A--ATG--A-A--G-G-CAA---T--A---A-T--TG---T---AC-TA-C-TC-------------
> str12: ATGA--G------C---C-A--A-G-A-TC---CG-AC-GA---AG---A-G-C-C---C----C-A--A-G---GA--G-G--A--GA---AG-GA--G--G-----G-AC----C--C--C-C--------
> str13: -T--C--T-----C--AC-AG--T----TC--A---A--GA---A--C--C--CA--A--AGTAC---C---C----C-----C--C-AT--AGC--C--CT--C-T--TA---A--A--G-C-CA-----C-
> str14: A-G---GT--T----TA-TA-C---C--T--T-C---CT-A-G--GT--A----AC-A--A--AC---CA----A--C-----CAAC--T-T------T-C-GA--TC-T-C-T----T-G--T-A-------
> str15: A-G---GT--T----TA-TA-C---C--T--T-C---C-----CAG-----GT-A--A-CA--A--A-C---C-A-AC-----CAAC--T-T------T-C-GA--TC-T-C-T----T-G--T-A-------
> str16: -T-A----A--AAC--A--A-C-T-CAAT---AC--A---A--CA-T--A----A-GA--A--A--ATCA----A--C-G---CAA--A---A---AC-----AC-TC--AC--A--A---A-----------
> str17: ----CCG------C---C---CAT----T--T--G----G--GC-G-----G-C----TC--T-CGA----GC--GA-T-AG-C-----TC--G----T-C-GA-ATC---C----C-TCGAC-C-T------
> str18: AT-ACC-T--T--C---C---CA-G-----GTA---AC--A---A----AC--CA--A-C----C-A--A--CT----T---TC---GATCT--C---T--TG---T---A-G-A---TC---T---G-----
> str19: -T--C--T-----C--AC-AG--T----TC--A---A--GA---A--C--C-TCA--A---GT-C--TC---C----C-----C--C-AT--AG-G-C--CT--C-T--T---T--CA--G--TCA-G-----
> str20: --GA---T-----C-T-CT--C-T-CA--C---CG-A---A--C---CT--G----G--C----C---C---C--G---G-G-CAA--AT---GC--C--CT-A-ATC---C--AG-A--G------G-TG--
> str21: A-GA--G------C--A--A---T-CA---GT--G--C--AT-CAG---A----A--AT-A-TAC---C-T---A---T---T-A----T--A-C-ACT--T----T-G--C-TA--A--GA---AT------
> str22: A--A---T--TAA---A--A-CAT-C--TC--A---A-T-A--CA----AC---A---T-A--A-GA--A----A-A---A--CAACG--C-A---A------A-A----AC--A-C-TC-A-T---------
> str23: A--A----A----CG-A--A-C-T----T--TA---A---A---A-TCT--GT---G-T--G---G--C-TG-T---C--A--C-----TC--G-G-CTGC--A--T-G--C-T----T--A-----G-TGC-
> str24: AT-A----A----C-TA--A---T----T---AC-T---G-T-C-GT-T--G--AC-A---G---GA-CA--C--GA--G--T-AAC--TC--G----T-CT-A--TC-T---T--C-T-G------------
> str25: ATGA--GT-GT--C--AC--G-A---A-T--T-C--AC-G-T--A--C-A----A---T--G-A--A-C-TG---GA-TG--T------TC-A-CG--TG--GA-AT---A---A------------------
> str26: A---CCGT-G----G-----GC--G-A---G--CG----G-TG-A--C--CG----G-T--GT-C--T--T-C----CT-AGT----G-----G-G--T-C---C--C--ACGT----T-GA---A------R
> str27: A--A----AG----GT--T----T--A-T---AC---CT--T-C---C--C---A-G----GTA--A-CA----A-AC-----CAAC---C-A---ACT--T----TCG-A--T--C-TC---T--TG-----
> str28: A-G----TAGT----T-C--GC---C--T-GT--GT---GA-GC--T----G--AC-A--A--AC--T--T---AG--T-AGT----G-T-T------TG-TGA----G---G-A---T----T-A-------
> str29: -T-----T--TA---TAC---C-T----TC---C-TA--G--G---T--A----AC-A--A--AC---CA----A--C-----CAAC--T-T------T-C-GA--TC-T-C-T----T-G--T-A-GAT---
> str30: ATG-C-G--GT--CGT-CT--C-T-C---C---C---C-G--GC--T-T---T-----T---T----T--T-C----C-----C--CG--C--GC--C-GC-G---T--T--G--GC---G-C-C--GA----
> str31: --G----T-G-A-C--A--A--A---AA-C--A--TA---ATG--G---AC-TC-C-A--A---C-A-C---C-A---TG--TCAA-G--CT------T--T--CA--G---GTAG-A-C-------------
> str32: --G----T-GTAA-G-A--A--A--CA---GTA---A--G---C---C--CG----GA--AGT--G-----G-T-G--T---T------T-T-GCGA-T--T----TCG-A-G--GC--CG------G-----
> str33: --GA--G-A--A---T----G-A-G---TC-T-C--A-T--T--A--C--CG-C-C---C-G---G-T-A--CT----T-AG-CAA-G--CTA---A-T----A----GT-C--A-C---G------G---C-
> str34: ATG----T-G----GT-C--G-ATGC---C--A--T---G--G-AG-----G-C-C---CA---C---CA-G-T----T----CA----T-TA---A--G--G-C-TC---C-T-G----G-C--AT--T---
> str35: A---C-G-AG---CGT--T----T----T---A---A--G--G--G-C--C--C--G--C-G-AC--T---GC--GAC-G-G-C--C-A-C-A-----TG--G-C--C---C-T-G--T--A-T---G-T---
> str36: --G---GT--T----TA-TA-C---C--T--T-C---C-----CAG-----GT-A--A-CA--A--A-C---C-A-AC-----CAAC--T-T------T-C-GA--TC-T-C-T----T-G--T-A-G-----
> str37: -TG---G--G-AA-GT--T--C---CAA----A---A--GAT-CA--C-A----A--A--A---C-A-C-T---A--C-----CA--G-TC-A---AC--CTGA-A--GTAC--A-C----------------
> str38: --GA----AG---CGT--TA--A--C----GT--GT--TGA-G--G---A----A--A--AG-AC-A----GCT----T-AG-----GA----G--A------ACA----A-G-AGC-T-G------G--G--
> str39: A---CC--AG---CG--C-A-C-T----TCG---G--C--A-GC-G-----G-CA-G--CA---C---C-T-C--G---G---CA--G--C-A-C--CT-C--A----G--C--AGCA---AC----------
> str40: ATG---G--G-A-C--A--A-C-T----T---A--T--T----C---CTA--TCA---T--GT--G--C---C-A-A--GAG-----G-T-T------T--T-AC--C---CG--G--T-GAC-CA-------
> str41: -T-----T-GTA--G-A-T--C-TG---T--T-C-T-CT-A---A----ACG--A--A-C--T----T--T---A-A---A---A----TCT-G----TG-TG-----GT---T-G--TC-ACTC--------
> str42: A--ACC--A--A-C---C-A--A--C--T--T---T-C-GAT-C--TCT---T---G-T-AG-A---TC-TG-T----T----C-----TCTA---A------AC---G-A---A-C-T----T--T-A----
> str43: --G---G--GT----T-CT-GC---CA---G---G--C--AT--AGTCT---T-----T---T----T--T--T---CTG-G-C---G-----GC--C--CT----T-GT--GTA--A---AC-C-TG-----
> str44: --G---G------C-T----GCATGC--T--TA-GT---G---CA--CT-C---ACG--CAGTA---T-A----A---T---T-AA---T--A---ACT----A-AT--TAC-T-G--T--------------
> str45: -TG-C---A-T---G--CT----T--A---GT--G--C--A--C--TC-ACG-CA-G-T-A-TA--AT--T---A-A-T-A---A-C--T--A---A-T--T-AC-T-GT-CGT-------------------
> str46: -T-----T-----C---C-A-CA---A--C-T---T--T----C---C-AC--CA--A---G--C--TC-TGC-A-A--GA-TC--C---C-AG--A--G-T--CA--G---G--G----G-C-C-TG-T---
> str47: -T--C--TA--AACG-A--A-C-T----T--TA---A---A---A-TCT--GT---G-T--G---G--C-TG-T---C--A--C-----TC--G-G-CTGC--A--T-G--C-T----T--A-----G-----
> str48: A---CCG--G-A---T----G---GC---CG--CG-A-T--T----T-T---TC--G----G-A-G-TC---CT----TG-G-----G-----G-GAC--C--AC-TC--A-G-A--AT--A-----GA----
> str49: ----C--T--T---GTA---G-AT-C--T-GT---T-CT----C--T--A----A--A-C-G-A--A-C-T--T----T-A---AA--ATCT-G----TG-TG-----G--C-T-G--TC-ACT---------
> str50: ATGA--G------C--ACTA--A-GC----G-A---A--GA---A--C--C---A--A--A--A--A----GC-AGAC--A---A----T--A-C-A------AC--C---CG---C-T--A-T--T-A--C-
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 133
> best bound: 84.0
> wall time: 61.256264s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="protein_n010k010.txt")
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
>   Sol: MQPASKLESFYTLRNEAQHFDVAINSRCPGFNEKVGTGALHDYQ
> str01: M--A--L-S-Y----------------CP----K-GT-------
> str02: MQ--S---S---L-N-A------I----P-----V---------
> str03: M-P---L-S-Y------QHF------R------K----------
> str04: M------E-------E--H--V--N-------E------LHD--
> str05: M---S---------N----FD-AI--R-----------AL----
> str06: M--------F---RN--Q------NSR----N---G--------
> str07: M--------FY-----A-H---A-------F----G-G----Y-
> str08: M---SK---F-T-R------------R-P-------------YQ
> str09: M---S----F-----------VA------G----V-T-A----Q
> str10: M------ES---L--------V------PGFNE-----------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 29.0
> wall time: 61.34941s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="protein_n050k050.txt")
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
> --- Solution (of length 497) ---
>   Sol: MNWGFPEADIERLRHSVFENVKIQYTIEPALFDVPRTSGHLNPIFDYLEKVAFQTIRPFGQENDKSYVLFWETSAIQFNGKMVHQLKPEEHILDVYNPADRQTWFAGSKHILDWQVNARSEGMFNTPYHDLAEISLGKVNDHQCPFAQWDCTIAEDRNSKAVMTLFDKGPWFEARIQYNACSPGLEDFILVRWAPVEQKHTNGLMSRADFSTEMIYRLGEHPKQHFTNVCLNRADEYSQAIMGSFYDTANVPHKNGLPDEHADFISFTKQPIRYAKMNVRWGEYLITDSKNRFCAYEWHKIGLLRSAMAYTDNCVWYNTFGLAQPDEVSIWRKTPREFDQTSDIAVNFLMEPKRIYTGGDSWPCQVLEADFFNRYLGDHKKAPIVYDPRFELSGQLEIHDVNTICARLGSWTKARPIQEDMNRVLFISDGVCEYCLKDHQRTASIEGKHDGAEFLNIDSKCWVAHLMQRYADTPGLQIMKNRSTVAKHRSFQDGIWL
> str01: M----------R--H---------------L----------N-I-D---------I-----E----------T----------------------Y-----------S-----------S----N----D---I---K-N----------------------------G---------------------V------------------------Y------K-------------Y--A------D-A----------E--DF------------------E--I----------------LL---------------F--A--------------------------------Y----S----------------------I--D------G--------------G---------E----V--------E-CL-D----------------L-----------------T--------R---------------
> str02: M-----E----R-R---------------A---------H----------------R---------------T----------HQ-----------N------W--------D----A-------T-----------K------P-----------R---------------E-R----------------R------K------------------------Q--T-----------Q-------------H-------------------R-----------L-T-----------H-------------------------PD------------D--S-I-----------Y------P----------R---------I------E---------------------KA----E----------G----------R------K----E----D------H---------G----------------------
> str03: M-----E---------------------P---------G------------AF------------S------T-A----------L------------------F-------D----A------------L------------C-----D-----D-------------------I--------L--------------H------R---------RL-E-----------------SQ-----------------L---------------R-------------------F--------G------------------G------V-----------Q---I-------P----------P----E----------------V-------S------D---------------P------RV---------Y--------A---G----------------------YA----L--------------------L
> str04: M--G-----------------K---------F--------------Y-------------------Y------S----N---------------------R-----------------R-----------LA------V------FAQ-----A----------------------Q----S---------R-------H---L--------------G-----------------------GS-Y-------------E---------Q----------W---L---------A------------------CV-------------S----------------------------G-DS-------A-F--R-------A--------E---------V-----------KAR--------V---------------Q-------K-D-----------------------------------------------
> str05: ----F------------F-----------------R------------E-------------N-----L-----A--F------Q----------------Q----G-K--------AR-E--F--P-------S-------------------E-----------------EAR----A---------------------N---S---------------P----T----------S----------------------------------R---------E-L------------W----------------V----------------R---R---------------------GG-------------N---------P--------LS---E--------A--G----A----E---R-----------------R-----G-------------------------T------------------------
> str06: M-------D-------------------P--------S--L-------------T-----Q------V--W---A-------V-----E-----------------GS-------V--------------L---S-----------A------A-------V----D---------------------------------T------A----E-------------TN------D------------T-----------E----------P----------------D--------E----GL--SA-------------------E-------------------N---E------G---------E----------------------------------T---R---------I---------I-------------R---I---------------------------T-G-------S--------------
> str07: M------A---------F--------------D-----------F--------------------S-V----T------G----------------N-----T-----K--LD------------T--------S-G--------F-----T------------------------Q------G------V--------------S----S--M------------T-V----A-----A--G----T--------L-------I---------A------------D--------------L-----------V-----------------KT----------A---------------S-------------------------------S-QL------T------------------N--L-----------------A------------------------Q--------------S--------------
> str08: M------A--------V-----I-------L---P--S----------------T-----------Y-----T--------------------D------------G------------------T-----A--------------A---CT-----N----------G------------SP---D---V----V------G--------T------G-------T--------------M--------------------------------------W---------------------------------V--NT----------I------------------L--P-----G-D----------FF--------------------------------------WT---P-----------S-G--E----------S------------------V-----R---------------V------------
> str09: MN-----------------------T------------G----I-----------I-------D----LF-----------------------D--N------------H-----V-------------D----S-----------------I----------------P------------------------------T-------------I--L---P--H-------------Q-----------------L----A-----T----------------L--D-------Y------L-----------V----------------R-T---------I----------I----D-------E----NR------------------S-------V------L----------------LF------------H-----I---------------------M-------G-------S----------G---
> str10: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N-----L------R--------T-----R----T-----------Q------L--------------------P-----P---A-----------Y------------T---N--------------S-------------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H-S-------
> str11: M-------D------S-----K-----E--------T------I---L-------I-----E-------------I---------------I-----P----------K-I--------------------------K--------------------S------------------Y------L----L------------------D--T---------------N------------I--S-------P-K-----------S-------Y---N---------D----F-------I----S-------------------------R--------------N-----K-------------------N----------I-----F----------V--I-----------------N--L--------Y---------------------N------V-------------------ST----------I--
> str12: M-----------L-----------------L------SG----------K--------------K---------------KM---L------LD--N------------------------------Y----E------------------T-A------A------------AR--------G-------R----------G---------------G---------------DE------------------------------------R------R-----------R---------G-------------W------A--------------FD--------------R--------P-----A--------------IV-----------------T---------K-R----D----------------K------S-----D------------------R---------M------A-H---------
> str13: MN-G--E---E---------------------D------------D----------------N--------E----Q---------------------A------A-----------A--E---------------------Q----Q---T-------K-------K-----A------------------------K-------R-----E---------K----------------------------P-K---------------Q----A----R---------K------------------------V---T---------S-------E-------A----------------W-----E----------H----------F---------D-----A-----T-------D--------DG------------A--E--------------C------------------K-------H---------
> str14: M-----E--------S--------------L--VP---G-----F-----------------N--------E--------K---------------------T------H-----V--------------------------Q---------------------L----------------S--L---------PV-------L-------------------Q----V---R-D---------------V-----L---------------------VR-G----------F--------G---------D----------------S----------------V----E----------------E----------------V------LS---E--------AR----------Q--------------------H---------------L----K-----------D--G--------T-------------
> str15: M----------R------------Y-I------V---S----P----------Q--------------L-------------V--L---------------Q-------------V-----G---------------K------------------------------G-------Q--------E----V-----E---------RA---------L------------------Y-------------------L----------T--P--Y-------------D-------Y----I----------D--------------E-----K--------S---------P--IY------------------Y--------------F-L--------------R--S----------------------------H---------------LNI----------QR----P-----------------------
> str16: M----P-----R----V-----------P----V------------Y----------------D-S---------------------P-------------Q-------------V---S------P------------N-----------T---------V-------P------Q--A-----------R-----------L---A---T---------P---------------S------F---A------------------T--P---------------T-----F-----------R---------------G-A--D------------------A------P----------------A-F-----------------------Q----D--T--A---------------N-----------------Q---------------------------Q--A----------R---------Q-----
> str17: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N-----L------R--------T-----R----T-----------Q------L--------------------P----L----A-----------Y------------T---N--------------S-------------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H-S-------
> str18: M---F-----------VF-------------F-V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N-----L---------------T----------T----R---------T-----------Q-----------------LP------------P---A--------Y--T---N--------------S-------------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H-S-------
> str19: M-----EA-I------------I--------------S------F------A-------G---------------I---G-----------I----N------------------------------Y---------K---------------------K----L-----------Q----S----------------K----L-------------------QH---------D---------F----------G----------------R-----V-----L----K----A-------L-------T---V---T---A--------R------------A---L--P-----G------Q-----------------P-----------------------------K-------------------------H-----I------A----I-----------R-------Q--------------------
> str20: M------A-------S---------------------SG---P-----E-------R-----------------A-------------E-H----------Q--------I----------------------I-L--------P---------E---S----------------------------------------H---L-S----S----------P--------L-------------------V--K------H-------K---------------L-----------------L------Y------Y-------------W-K---------------L-------TG--------L---------------P--------L-----------------------P---D------------E-C--D---------------F---D------HL-----------I-------------------
> str21: M-----E--------S--------------L--VP---G-----F-----------------N--------E--------K---------------------T------H-----V--------------------------Q---------------------L----------------S--L---------PV-------L-------------------Q----V---R-D---------------V-----L---------------------VR-G----------F--------G---------D----------------S----------------V----E----------------E----------------V------LS---E---V-----R----------Q--------------------H---------------L----K-----------D--G--------T-------------
> str22: M-----------L----------------A----P--S----P-------------------N--S--------------K----------I---------Q---------L-----------FN--------------N------------I----N-----------------I----------D-I------------N-------------Y---EH-----T---L-----Y-------F---A----------------S------------V---------S-----A----------------------------Q----------------------N-------------S---------FF---------A------------Q---------------W------------V------V--Y---------S-------A-----D-K---A-------------I-------------------
> str23: M--------------S-------------A-------------I----------T------E----------T-------K------P--------------T-------I---------E---------L-------------P-A-----------------L--------A-----------E----------------G------F-------------Q--------R---Y------------N---K-------------T--P----------G----------F-----------------T--CV------L---D-----R-----------------------Y---D------------------H--------------G------V--I-----------------N------D--------------S---K--------I-----V--L---Y----------N----------------
> str24: M--------------------K-------------------N-I-------A---------E-------F----------K-----K-----------A---------------------------P-----E--L----------A-------E----K----L-------------------LE----V------------------FS----------------N--L----------------------K-G---------------------N----------S--R-------------S---------------L---D--------P--------------M---R--------------A-------G--K------------------HDV----------------------V------V-------------IE------------S-------------T------K------K---------L
> str25: M----P-----------------Q----P-L------------------K---Q-----------S--L------------------------D-------Q-----SK----W----------------L-------------------------R---------------EA-----------E------------KH---L--RA---------L-E-----------------S------------------L---------------------V--------DS-N-----------L-----------------------E---------E-------------E-K-------------L------------K--P-----------QL-------------S----------M--------G--E----D------------------------V----Q--------------S--------------
> str26: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N-----L---I-----------T-----R----T-----------Q-------------S-------Y-T-N---------------SFT----R--------G--------------------------------V-Y--------------------------------------Y------P------D---------K----V----F----------------R--S-----------------S--V----L--H----S----------------------------T---Q---------------D----
> str27: M--------------------K---------FDV------L------------------------S--LF----A------------P---------------W-A--K------V-------------D--E---------Q-----------E----------------------Y--------D----------Q-------------------------Q------LN-----------------N----N-L--E-----S-----I--------------T-------A-----------------------------P-------K----FD---D--------------G----------A---------------------------------T---------------E-------I-----E----------S-E----------------------R-----G-----------------D-I--
> str28: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N--------F------------TN----R----T-----------Q------L--------------------P-------------S--------A--------Y--T---N--------------S-------------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H-S-------
> str29: M-W------------S------I---I------V------L--------K------------------L------I-------------------------------S--I---Q-----------P---L----L----------------------------L-------------------------V---------T----S-----------L---P--------L-----Y------------N-P--N---------------------M----------DS----C-------------------C-------L-------I-----------S-----------RI-T-----P----E-------L-----A-----------G------------------K-----------L----------------T-------------------W---------------I------------F---I--
> str30: M-----E--------S--------------L--VP---G-----F-----------------N--------E--------K---------------------T------H-----V--------------------------Q---------------------L----------------S--L---------PV-------L-------------------Q----V---R-D---------------V-----L---------------------VR-G----------F--------G---------D----------------S----------------V----E----------------E--F----L----------------S---E--------AR----------Q--------------------H---------------L----K-----------D--G--------T-------------
> str31: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------VM------P--------------L--F-------------N-L----------I-----------T--------------------T-------------------T-Q------------------S------Y--------------T-N------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H--------L
> str32: M-------------H--------Q--I---------T-------------V----------------V-----S-----G-------P--------------T-----------------E-----------------V-------------------S----T----------------C------F--------------G--S-----------L--HP---F------------Q----S------------L-----------K-P-------V----------------------------MA---N---------A-------------------------L--------G-------VLE--------G--K----------------------------------------M----F-----C-----------SI-G---G-----------------R-------------S-------------L
> str33: M------A-----------------T----L---------L---------------R--------S--L-----A----------L------------------F---K---------R-----N------------K--D------------------K---------P------------P-----I-----------T----S------------G------------------S----G------------G-----A--I-------R--------G---I---K--------H-I----------------------------I-------------I-V-----P--I-------P-------------GD--------------S----------------S------I------------------------T------------------------------T--------RS-----R--------
> str34: M-----E--------S--------------L--VP---G-----F-----------------N--------E--------K---------------------T------H-----V--------------------------Q---------------------L----------------S--L---------PV-------L-------------------Q----V---R-D---------------V-----L---------------------VR-G----------F--------G---------D----------------S--------------------ME----------------E----------------V------LS---E--------AR----------Q--------------------H---------------L----K-----------D--G--------T-------------
> str35: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N-----L---------------T----------T------G-------T-----------Q-----------------LP------------P---A--------Y--T---N--------------S-------------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H-S-------
> str36: M------A-----------N--I---I--------------N-----L----------------------W-------NG-----------I--V--P------------------------M---------------V---Q------D-----------V----------------N-----------V--A-----------S--------I-----------T------A----------F--------K-----------S----------M--------I-D--------E-------------T----W---------D------K-------------------K-I------------EA---N-----------------------------T-C-----------I----------S------------R------KH-------------------R-----------N----------------
> str37: M-----------L------N---------------R-------I---------QT-------------L------------M----K---------------T--A----------N-------N--Y----E------------------TI-E--------------------I--------L------R---------N-------------Y-L--------------R-----------------------L----------------Y-----------I--------------I-L---A------------------------R--------------N---E----------------E--------G-----------R----G---I---------L--------I----------------Y---D-----------D-----NIDS---V----------------------------------
> str38: M------AD-------------------PA--------G---------------T-------N----------------G--------EE----------------G------------------T----------G------C-------------N----------G-WF-----Y------------V-----E----------A--------------------V---------------------V--------E--------K------K----------T--------------G---------D----------A------I-----------SD----------------D-------E----N-----------------E----------N-----------------D-------SD------------T----G-----E----D-------L------------------V-------D----
> str39: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------V----------------N-----L------R--------T-----R----T-----------Q------L--------------------P-----P-------S-------Y------------T---N--------------S-------------F-------------T-R---------------------G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H-S-------
> str40: M-----E--------S--------------L--VP---G-----F-----------------N--------E--------K---------------------T------H-----V--------------------------Q---------------------L----------------S--L---------PV-------L-------------------Q----VC----D---------------V-----L---------------------VR-G----------F--------G---------D----------------S----------------V----E----------------E----------------V------LS---E--------AR----------Q--------------------H---------------L----K-----------D--G--------T-------------
> str41: MN-----------------N---Q-----------R-------------K--------------K-------T-A-------------------------R-------------------------P-------S----------F-----------N----M-L--K------R----A-----------R---------N----R---------------------V--------S---------T--V--------------S---Q--------------L---------A----K----R--------------F--------S---K------------------------G--------L--------L----------------SGQ-------------G------P----M---------------K-----------------L-------V---M---A-------------------F------
> str42: M--------------S---N-----------FD------------------A---IR-----------------A----------L--------V----D--T---------D----A---------Y---------K--------------------------L---G------------------------------H--------------I-----H--------------------M---Y-----P-------E---------------------G----T---------E------------Y----V------L------S-----------------NF--------T--D-------------R--G---------------S-------------R---------I-E----------GV----------T------H-----------------------T-----------V--H---------
> str43: M--------IE-LRH---E-V--Q--------------G------D-L--V---TI------N----V--------------V-----E-------------T-----------------------P-----E-------D-----------------------L-D-G--F--R-----------DFI--R-A-----H---L----------I--------------CL--A----------------V-------D--------T--------------E---T-----------------------T---------GL---D---I-------------------------Y---------------------------------------------------------------------------------------------------------------------------------------------
> str44: M---F-----------VF------------L--V------L------L---------P----------L-------------V------------------------S-----------S----------------------QC-----------------VM------P--------------L--F-------------N-L----------I-----------T--------------------T-N-------------------Q------------------S------Y--------------T-N---------------S--------F--T------------R---G-------V--------Y----------Y-P-----------D------------K----------V-F--------------R--S--------------S---V--L---------------------H---------
> str45: M--------------S-----K----------D-------L---------VA----R---Q-------------A----------L------------------------------------M--T-----A------------------------R-----M----K-----A------------DF--V------------------F---------------F----L-------------F-----V-----L-----------------------W--------K----A-------L--S---------------L--P--V------P-----T------------R---------CQ------------------I--D---------------------------------M---------------------A----K-----------K-----L----------------S--A-------G---
> str46: M------A-------S--------------L---------L--------K---------------S--L---T------------L------------------F---K---------R------T------------------------------R---------D---------Q-----P-----------P--------L---A--S-------G------------------S----G------------G-----A--I-------R--------G---I---K--------H---------------V--------------I-------------I-V--L-----I-------P-------------GD--------------S----------------S------I------V-----------------T--------------------------R-------------S-----R--------
> str47: M----------R----V------------------R--G----I---L--------R-----N-------W-----Q-------Q------------------W---------W-------------------I--------------W--T------S-----L---G--F--------------------W-----------M----F---MI--------------C-------S------------V---------------------------V--G--------N-----------L------------W-----------V-----T-----------V---------Y------------------Y-G-------V--P------------V---------W-K-----E-----------------------A----K------------------------T----------T-------------
> str48: M------A--------V-E---------P--F--PR--------------------RP-----------------I--------------------------T---------------R-------P-H--A--S-----------------I-E------V----D---------------------------------T----S------------G---------------------I-G------------G---------S--------A------G------S----------------S--------------------E-----K------------V-F---------------C--L----------------I---------GQ----------A------------E----------G----------------G-----E--------------------P------N--TV------------
> str49: M---F-------------------Y----A---------H-----------AF------G-------------------G---------------Y---D--------------------E---N-----L----------H----A------------------F---P-------------G----I----------------S----ST----------------V----A---------------N--------D-------------------VR---------K-----Y---------S--------V------------VS----------------V---------Y----------------N------KK----Y---------------N-I-------------------V------------K------------------N---K---------Y--------M----------------W-
> str50: M------A-----------N----Y------------S-----------K-------PF---------L----------------L-------D----------------I----V-------FN------------K--D-----------I------K--------------------C-------I------------N------D-S------------------C-------S--------------H------------S---------------------D-----C----------R----Y-------------Q----S-----------------N-------------S-------------Y---------V-----EL--------------R-------R------N-----------------Q--A-----------LN---K--------------------N---------------L
> 
> example file name: 'protein_n050k050.txt'
> best objective: 497
> best bound: 93.0
> wall time: 60.881371s
> ```
