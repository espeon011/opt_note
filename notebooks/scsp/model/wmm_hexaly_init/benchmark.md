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
Model = scsp.model.wmm_hexaly_init.Model
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
> --- Solution (of length 64) ---
>  Sol: iojtkgnkulcihmpxenyhtqvazgxbrddbcosovrfozpplvnnbxxcvsuqpvissbgxf
> str1: ---tkgnku---hmpx-n-htq---gx-------------z---v---x--------is-----
> str2: ioj--------i---------q----------------fo---l-n-bxxcvsuqpvissb-xf
> str3: --------ulci-----ny-------------cosov--ozppl-----------p--------
> str4: i----g----------e-----vazg-brddbc-s-vr------vnn--------------g-f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 64
> best bound: 0.0
> wall time: 59.587764s
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
> --- Solution (of length 105) ---
>  Sol: pietokgnbdcevayplrzxwxqkrudchvdpmqfjtvgpxebrlcitdonhdbtqfuycosovozslnmpsbrvinngxzvplxwcdvsuboqpvissbxbhef
> str1: ---t-kgn---------------k-u--h---m------px---------nh--tq----------------------gxzv--x-----------is-------
> str2: -i--o------------------------------j----------i--------qf---o------ln---b------x----x-c-vsu--qpvissbx---f
> str3: -------------------------u------------------lci---n-------ycosovoz----p-----------pl----------p----------
> str4: -i----g----eva----z-------------------g---br----d---db-----c-s-v---------rv-nng-------------------------f
> str5: p-------------yplrzx-----u-c---pmq---vg--------td-------fu-----------------i-----v----cd-s-bo------------
> str6: p-------bd-ev-------------dc-vdp--f------------------------------zs--m-sbr------------------oq-v---b-bh--
> str7: --e----nb-c-------z---------------fjtv--xe-r---------------------z------brvi--g---pl-------------------e-
> str8: -----------------r-xwxqkr-d----------------rlc-t-o--d-t--------------mp--r--------p-xw-d-----------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 105
> best bound: 0.0
> wall time: 59.99322s
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
> --- Solution (of length 150) ---
>   Sol: irpkxwsxqkhtojgenbvyplrdiqfaxxusfczpafdigbrqjzdevdolncitvbxucspevrkgnkuhmqcewbodpfxcvgtzksnmiuycosbroqpvdfwauibezhkntskrjoqgxzvppxwcdisblhxfmgeqopzuwy
> str01: -----------t------------------------------------------------------kgnkuhm-------p-x-------n----------------------h--t-----qgxzv--x---is---------------
> str02: i-----------oj----------iqf-----------------------oln----bx-----------------------xcv----s---u-------qpv-----i-------s----------------sb--xf----------
> str03: ------------------------------u--------------------l-ci-------------n-------------------------ycos--o--v-----------------o---z-pp-------l--------p----
> str04: i-------------ge--v--------a------z-----gbr---d--d-------b--cs--vr------------------v-----n------------------------n-------g---------------f----------
> str05: --p----------------yplr-----------z-----------------------xuc-p---------mq----------vgt-----------------df--ui----------------v----cd-sb--------o-----
> str06: --p--------------b-----d-----------------------evd---c--v----------------------dpf-----z-s-m-----sbroq-v------b------------------------b-h------------
> str07: ---------------enb---------------cz--f------j----------tv-x----e-r---------------------z----------br---v-----i-------------g---p--------l-----e-------
> str08: -r--xw-xqk------------rd------------------r--------l-c-t----------------------od------t----m----------p----------------r-------p-xw-d-----------------
> str09: ---k-----k---------------q-a----f------ig--qj-------------------------------w-o---------k-------------------------k--skr---------------bl----g--------
> str10: ---------------------l------xx-----pa----b------------i-vb------v----------------------zk-------o---------------z------------zv-----d-----------------
> str11: ---k------------------r-i-f----s----a-----------v---nc-------------------------d---------------------q----w------h-----------z-----c------------------
> str12: --------q------------------ax-u-------d-g--q----v------------------------qcewb---f---g------i---------------------------jo--------w-----------------wy
> str13: -r----sxq----j--n---------f--------pa-di-------------------u-s------------------------------i--------q--------bezhk------o---------------h--mg--------
> str14: i----ws---h-------v----------------------------------------------------h--c---o------------miu---------vd---------------------------d-------m---------
> str15: ----------ht----------------xx-------------qjz---------------------------q---b-----c--t-----------b--------a------kn----------------------------------
> str16: ----x-------------------------usfc---f-------z----------------pe-----------e-------cv---------------------wa-------nt----------------------fmg-q--zu--
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 150
> best bound: 0.0
> wall time: 59.992121s
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
>   Sol: bbaedcdbeacdeecbdbeacbdacde
> str01: ----dc-b--c---c-db--c---c-e
> str02: b---d-dbe---ee----e--bd----
> str03: -----c---acdeec---e--b----e
> str04: --aed-d----d----d-e--bd--d-
> str05: --a--c-be---e-c----a-b--c-e
> str06: bba----be------bd---cb-a---
> str07: bbae-----a--e--b---a--da---
> str08: ---e----e---eecbdbe-------e
> str09: -----c----cdee--d--a--d-cd-
> str10: b---d----a-----bdbea---a-d-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 0.0
> wall time: 59.959859s
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
>   Sol: dacebdaecdbaecdbecabdebacedabacdeb
> str01: d-c-b---c----cdb-c------ce--------
> str02: ----bd---db-e---e----e---e--b--d--
> str03: --c---a-cd--e---ec---eb--e--------
> str04: -a-e-d---d----d-----deb---d----d--
> str05: -ac-b--e----ec----ab----ce--------
> str06: ----b-----ba---be--bd---c---ba----
> str07: ----b-----bae-----a--eba--da------
> str08: ---e---e----e---ec-bd-b--e------e-
> str09: --c-----cd--e---e---d--a--d---cd--
> str10: ----bda---b---dbe-a----a--d-------
> str11: ---e-d-e-d-a------a----a-e-a-a----
> str12: -a----ae---a------ab-e---e-a--c---
> str13: ---e--a----a---b-ca-----c-----cd-b
> str14: ----bd-e----e-----a-de-a--d-----e-
> str15: --c---ae-d-a--d-e----e---ed-------
> str16: ---eb---c--a--db--ab--b--e--------
> str17: d----d--c---e---e-abde-a----------
> str18: da--b---cd----d-e-a--e--c---------
> str19: -a----a--d---c--e----e----da-a---b
> str20: -a-e---ec----c--e----e---e-a-a----
> str21: ----b-----b---d---a--e--c--a-a-de-
> str22: dace-dae-d-a---b------------------
> str23: -a----ae---a---b---b--b-----b-c-e-
> str24: d--e-d----b--c-b-ca----a----b-----
> str25: d---bda----ae--b---b----c---b-----
> str26: d--eb--e-db-e--b--a-----c---------
> str27: --ce---e--b--cd--c-bde------------
> str28: d---b--e-d-a------a-d--a---ab-----
> str29: --c-----c----cd--c-b-eb---d---c---
> str30: -a-e---e---a-cdb-c-bd-------------
> str31: dac-b--e---a-c---c------c-d-------
> str32: ---e----c---e--b-c------c-d-b--d-b
> str33: d----d----b----b-c---e----dab----b
> str34: -a----ae---a---b--a----a-e--ba----
> str35: ---e----c-b----b-ca----a--d---cd--
> str36: d--eb---c----c--ec--d-b-c---------
> str37: da----a-c-bae---e--b----c---------
> str38: -a---da---b-e-----a----ac-----c-e-
> str39: da-e----cdba-c----a----a----------
> str40: dac-b-----b---d--c---e----d---c---
> str41: d--e-d----b-e---e--b--b---d-----e-
> str42: --c--da--d---cd--c--d--a---a------
> str43: --ce---e-d---c-b--a--e---ed-------
> str44: --ce--aec--a------a----ac--a------
> str45: d-c-----c----c--e--b--b-----ba-d--
> str46: ----b-ae----e-----a--eb-----b--de-
> str47: d---bd-e--ba-c---c--d-b-----------
> str48: ---eb---c-b-e---e---d--a-e-a------
> str49: -a-e---e----e--b---bd-b-c--a------
> str50: d---bda---b--c--ec-b--b-----------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 0.0
> wall time: 59.991101s
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
>   Sol: TATGCGTACGACTATCGTACGTAC
> str01: -ATG-G---GA-TA-CG-------
> str02: -AT----AC--CT-TC---C---C
> str03: ----C--ACGA--AT--T--G-A-
> str04: TA-----A--A--ATC-T--GT--
> str05: -A-G-GTA--AC-A----A---A-
> str06: T-T-C---C---TA--G---GTA-
> str07: T-TG--TA-GA-T--C-T------
> str08: T--G-G---GA--A--GT---T-C
> str09: T-T-C---C-AC-A----AC-T--
> str10: T---C-TA--A--A-CG-A---A-
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 0.0
> wall time: 59.977838s
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
> --- Solution (of length 138) ---
>   Sol: ATGACGTACGTACAGTCATCAGCTACTGATCGTCATGACGATCAGTCAGACTACGTACAGCATCAGTACTGATCAGTCAGTCATGCATCGACTGCATGATCGTACTGACTACTGACTCAGTACGACTAGTCGACRTGT
> str01: -T-A-GTA-GTA--G--A-C---T-C----CG----GA--A---GT--GAC-A---A-A-C--C----CTGA--A---A---A-G-A---A-TG---GAT---A---A--A-T-A-T-A-------------------
> str02: --G--G-A--TA-A---A-CA-CT-C----C--C--GA--A--A---A---TA---A-----T---T--TGA-C--T---T-A---A---AC---A--A-CG--C-GAC-A--G--T---T-C-A--AG---------
> str03: AT-AC---C-T----TC--C---TA--G---GT-A--AC-A--A---A--C--C--A-A-C--CA--ACT--T---T---T---G-ATC---T-C-T--T-GTA--GA-T-CTG------------------------
> str04: -T-A---A---A---T--T-A--TA---ATC-T--T-A---T-A--C----TA-GTA-A--A--A--A---AT-AG---G----G--T-G--T--A--A-C---C-GA--A---A---A---CG----GTC-------
> str05: -T----TA---A-A---A-CAGC--CTG-T-G----G--G-T---T--G-C-AC---C--CA-C--T-C--A-CAG---G----GC--C--C---A----C-T---G------G-----G--CG-C-A----A---G-
> str06: ATGAC-T---T-C---CA--A--T---G---G--AT--C---C---CA-AC--C-T-CA--A---G--CT--TC---CA--C---C--C--C---A--AT-G----G--T--T---TCAG--C---------------
> str07: A--AC--A---A-A--C--CA---AC----C---A--AC--T---T-----T---T---G-ATC--T-CT--T--GT-AG--AT-C-T-G--T---T---C-T-CT-A--A---AC---G-A--AC------------
> str08: ATGA---A---A-A--C----G--A---A-----A--A---T---T-A---T---TA-----TCA--A--G----G---GT-ATG----GA----A-G-T-G----GA--A--G-CT--G-ACGA--A----A--T--
> str09: A---C-T-CG----G-C-T--GC-A-TG--C-T--T-A-G-T--G-CA--CT-C--AC-GCA---GTA-T-A--A-T---T-A---AT--A----A----C-TA---A-T--T-A-----------------------
> str10: -T----T--GTA--G--ATC---T---G-T--TC-T--C--T-A---A-AC---G-A-A-C-T---T--T-A--A---A---AT-C-T-G--TG--TG---G--CTG--T-C--ACTC--------------------
> str11: --G-C--A-G-A--G-CAT----T--T--TC-T-A--A---T-A-TC---C-AC--A-A--A--A-T---GA--AG---G-CA---AT--A----AT--T-GTACT-ACT-C--------------------------
> str12: ATGA-G--C---CA---A---G--A-T---C--C--GACGA--AG--AG-C--C---C--CA--AG----GA---G---G--A-G-A---A--G---GA--G----G------GAC-C----C--C----C-------
> str13: -T--C-T-C--ACAGT--TCA---A--GA-----A---C---C---CA-A--A-GTAC--C--C----C----C---CA-T-A-GC--C--CT-C-T--T---A---A--A--G-C-CA---C---------------
> str14: A-G--GT---T----T-AT-A-C--CT--TC--C-T-A-G----GT-A-AC-A---A-A-C--CA--AC----CA---A--C-T---T----T-C--GATC-T-CT---T---G--T-A-------------------
> str15: A-G--GT---T----T-AT-A-C--CT--TC--C----C-A---G---G--TA---ACA--A--A---C----CA---A--C---CA---ACT---T--TCG-A-T--CT-CT---T--GTA----------------
> str16: -T-A---A---A-A--CA--A-CT-C--A-----AT-AC-A--A--CA---TA---A--G-A--A--A---ATCA---A--C--GCA---A----A--A----AC--ACT-C--AC--A--A--A-------------
> str17: ----C---CG--C---C--CA--T--T--T-G----G--G--C-G---G-CT-C-T-C-G-A---G--C-GAT-AG-C--TC--G--TCGA----AT---C---C---CT-C-GAC-C--T-----------------
> str18: AT-AC---C-T----TC--C--C-A--G---GT-A--AC-A--A---A--C--C--A-A-C--CA--ACT--T---TC-G--AT-C-TC---T---TG-T---A--GA-T-CTG------------------------
> str19: -T--C-T-C--ACAGT--TCA---A--GA-----A---C---C--TCA-A----GT-C----TC----C----C---C---CAT--A--G---GC-----C-T-CT---T--T--C--AGT-C-A---G---------
> str20: --GA--T-C-T-C--TC-TCA-C--C-GA-----A---C---C--T--G-----G--C--C--C----C-G----G---G-CA---A---A-TGC-----C---CT-A--A-T--C-CAG-A-G----GT-G------
> str21: A-GA-G--C--A-A-TCA---G-T---G--C---AT--C-A---G--A-A--A--TA-----T-A---C----C--T-A-T--T--AT--AC---A----C-T--T---T---G-CT-A--A-GA--A-T--------
> str22: A--A--T---TA-A---A--A-C-A-T---C-TCA--A---T-A--CA-AC-A--TA-AG-A--A--A---A--A--CA---A--C---G-C---A--A----A---A--AC--ACTCA-T-----------------
> str23: A--A---ACG-A-A--C-T----T--T-A-----A--A--ATC--T--G--T--GT---G-----G--CTG-TCA--C--TC--G----G-CTGCATG--C-T--T-A-----G--T--G--C---------------
> str24: AT-A---AC-TA-A-T--T-A-CT---G-TCGT--TGAC-A---G---GAC-ACG-A--G--T-A--ACT---C-GTC--T-AT-C-T----T-C-TG----------------------------------------
> str25: ATGA-GT--GT-CA--C----G--A---AT--TCA---CG-T-A--CA-A-T--G-A-A-C-T--G----GAT--GT---TCA--C---G--TG---GA----A-T-A--A---------------------------
> str26: A---C---CGT---G------G-----G--CG--A-G-CG----GT--GAC--CG----G--T--GT-CT--TC---C--T-A-G--T-G---G---G-TC---C---C-AC-G--T---T--GA--A------R---
> str27: A--A---A-G----GT--T----TA-T-A-C--C-T-----TC---C---C-A-G----G--T-A--AC--A--A---A--C---CA---AC--CA--A-C-T--T---T-C-GA-TC--T-C---T--T-G------
> str28: A-G---TA-GT----TC----GC--CTG-T-GT---GA-G--C--T--GAC-A---A-A-C-T---TA--G-T-AGT--GT--T---T-G--TG-A-G---G-A-T---TA---------------------------
> str29: -T----T---TA---T-A-C--CT--T---C--C-T-A-G----GT-A-AC-A---A-A-C--CA--AC----CA---A--C-T---T----T-C--GATC-T-CT---T---G--T-AG-A----T-----------
> str30: ATG-CG---GT-C-GTC-TC---T-C----C--C----CG----G-C----T---T------T---T--T--T---TC---C---C--CG-C-GC-----CG--C-G--T--TG-----G--CG-C----CGA-----
> str31: --G---T--G-ACA---A--A---A---A-C---AT-A--AT--G---GACT-C---CA--A-CA---C----CA-T--GTCA---A--G-CT---T--TC--A--G------G--T-AG-AC---------------
> str32: --G---T--GTA-AG--A--A---AC--A--GT-A--A-G--C---C---C---G----G-A--AGT---G----GT--GT--T---T----TGC--GAT--T--T--C----GA----G---G-C----CG----G-
> str33: --GA-G-A---A---T-----G--A--G-TC-TCAT-----T-A--C---C---G--C--C--C-G----G-T-A--C--T--T--A--G-C---A--A--G--CT-A--A-T-A----GT-C-AC--G--G-C----
> str34: ATG---T--G----GTC----G--A-TG--C--CATG--GA---G---G-C--C---CA-C--CAGT--T---CA-T---T-A---A--G---GC-T---C---CTG------G-C--A-T-----T-----------
> str35: A---CG-A-G--C-GT--T----T--T-A-----A-G--G----G-C---C--CG--C-G-A-C--T---G--C-G--A--C--G----G-C--CA----C--A-TG------G-C-C----C---T-GT--A--TGT
> str36: --G--GT---T----T-AT-A-C--CT--TC--C----C-A---G---G--TA---ACA--A--A---C----CA---A--C---CA---ACT---T--TCG-A-T--CT-CT---T--GTA-G--------------
> str37: -TG--G---G-A-AGT--TC--C-A---A-----A--A-GATCA--CA-A--A---ACA-C-T-A---C----CAGTCA---A--C--C---TG-A--A--GTAC--AC-----------------------------
> str38: --GA---A-G--C-GT--T-A---AC-G-T-GT--TGA-G----G--A-A--A---A--G-A-CAG--CT--T-AG---G--A-G-A---AC---A--A--G-A--G-CT---G-----G---G--------------
> str39: A---C---C--A--G-C----GC-ACT--TCG----G-C-A---G-C-G-----G--CAGCA-C----CT---C-G---G-CA-GCA-C--CT-CA-G--C--A--G-C-A---AC----------------------
> str40: ATG--G---G-ACA---A-C---T--T-AT--TC----C--T-A-TCA---T--GT---GC--CA--A--GA---G---GT--T---T----T--A----C---C---C----G-----GT--GAC----C-A-----
> str41: -T----T--GTA--G--ATC---T---G-T--TC-T--C--T-A---A-AC---G-A-A-C-T---T--T-A--A---A---AT-C-T-G--TG--TG---GT--TG--T-C--ACTC--------------------
> str42: A--AC---C--A-A--C--CA---ACT--T--TC--GA---TC--TC----T---T---G--T-AG-A-T---C--T--GT--T-C-TC---T--A--A----AC-GA--ACT---T---TA----------------
> str43: --G--G---GT----TC-T--GC--C--A--G----G-C-AT-AGTC----T---T------T---T--T--T---TC--T---G----G-C-G---G--C---C---CT--TG--T--GTA--A--A--C--C-TG-
> str44: --G--G--C-T---G-CAT--GCT--T-A--GT---G-C-A-C--TCA--C---G--CAG--T-A-TA---AT---T-A---AT--A---ACT--A--AT--TACTG--T----------------------------
> str45: -TG-C--A--T---G-C-T----TA--G-T-G-CA---C--TCA--C-G-C-A-GTA-----T-A--A-T--T-A---A-T-A---A-C---T--A--AT--TACTG--T-C-G--T---------------------
> str46: -T----T-C---CA--CA--A-CT--T--TC--CA---C---CA---AG-CT-C-T---GCA--AG-A-T---C---C---CA-G-A--G--T-CA-G---G----G------G-C-C--T--G--T-----------
> str47: -T--C-TA---A-A--C----G--A---A-C-T--T-----T-A---A-A--A--T-C----T--GT---G-T--G---G-C-TG--TC-ACT-C--G---G--CTG-C-A-TG-CT---TA-G--------------
> str48: A---C---CG----G--AT--G-----G--C--C--G-CGAT---T-----T---T------TC-G----GA---GTC---C-T---T-G---G---G---G----GAC--C--ACTCAG-A--A-TAG---A-----
> str49: ----C-T---T---GT-A---G--A-T---C-T---G----T---TC----T-C-TA-A--A-C-G-A---A-C--T---T--T--A---A----A--ATC-T---G--T---G--T--G---G-CT-GTC-AC-T--
> str50: ATGA-G--C--AC--T-A--AGC----GA-----A-GA--A-C---CA-A--A---A-AGCA---G-AC--A--A-T-A--CA---A-C--C--C--G--C-TA-T---TAC--------------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 138
> best bound: 0.0
> wall time: 60.002989s
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
> --- Solution (of length 45) ---
>   Sol: MESFYPQALSERNYQHVAFCPKGFTNESLRHDNGAIRPVTYALKQ
> str01: M------ALS---Y-----CPKG-T--------------------
> str02: M-----Q--S-----------------SL---N-AI-PV------
> str03: M----P--LS---YQH--F----------R-------------K-
> str04: ME--------E----HV--------NE-L-HD-------------
> str05: M-S---------N-----F------------D--AIR----AL--
> str06: M--F-------RN-Q----------N-S-R--NG-----------
> str07: M--FY--A-------H-AF---G----------G------Y----
> str08: M-S------------------K-FT----R------RP--Y---Q
> str09: M-SF------------VA----G---------------VT-A--Q
> str10: MES-----L-------V---P-GF-NE------------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 45
> best bound: 0.0
> wall time: 59.93691s
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
> --- Solution (of length 454) ---
>   Sol: MFAVFLESVLLPNRLVSSQPGFCVNEKTLDHAIRPLVQTRLSLPTAFYINSLVKETGILQVRDASLPFKVLITDNQALEMRPSTYHQALFGKWNLITAVRGDENSIPFTNYEGTVDSAQPKIEVLQKSAPELARGCNDVYLHTNSGIFEKLTRGVQANWDTSILAEGVFYPKSDMVLKRAQHTNDEVRGFAILYSPKRSTGVENQLPDSRVEKLTPASIYTNDVFRKHSQLAGEFTCLDRKSVFGMILSYWADETVQLNRIWTSLGAFPDERVKALYNSGIPQHRLTKPGINFQDLESIAYWMFDLVKPTSCIVRAHLSGEDNPMICKHSFDTVAGLIQDRGSIVPYNALTEIVGPRDIECNLFRSKWVTDPELAGRVYESGKMDQSNASYVKELRRDNISTHVKDRTGLFVCSIARNKYMGEDHPVWQALIKEGNRSAKFNLQRTVDGHIPTY
> str01: M------------R----------------H----L-------------N-------I----D--------I------E----TY-------------------S-----------S-------------------ND--------I--K-------N--------GV-Y-K---------------------Y----------------------A-----D--------A-E----D----F---------E------I---L----------L----------------F------AY---------S-I--------D-------------G-----G---------E-V-----EC-L-------D--L---------------------------T----R-----------------------------------------------
> str02: M-----E------R-------------------R-----------A---------------------------------------H-------------R--------T--------------------------------H-------------Q-NWD----A-----------------T-------------K---------P--R-E-------------R-------------RK---------------Q-----T-------------------QHRLT-----------------------------H------P-------D-------D--SI--Y--------PR-IE------K-------A----E-G-------------R--------K-----------------EDH---------G-------------------
> str03: M-----E----P--------G----------A--------------F---S----T-------A-L-F-----D--AL---------------------------------------------------------C-D---------------------D--IL-----------------H-----R---------R-------L-----E-----S-----------QL--------R---FG--------------------G------V---------Q-------I-----------------P--------------P---------------------------E-V-----------S----DP----RVY---------A-------------------G----------Y---------AL-----------L-----------
> str04: M-------------------G-----K-------------------FY------------------------------------Y-------------------S----N-----------------------R------------------R----------LA--VF----------AQ---------A-------------Q---SR-----------------H--L-G-----------G---SY---E--Q----W--L-A--------------------------------------------C-V----SG-D-------S----A----------------------------FR---------A----E-----------VK----------------------AR---------V-Q---K--------------D------
> str05: -F--F--------R-----------E-----------------------N-L-----------A---F-------Q----------Q---GK-----A-R--E----F-----------P-------S--E-----------------E-------A---------------------RA---N----------SP---T--------SR-E-L------------------------------------W----V---R-----------R-------G---------G-N----------------P--------LS-E-------------AG------------A--E----R-------R----------G-------------------------T----------------------------------------------------
> str06: M----------------------------D----P------SL-T--------------QV-------------------------------W----AV---E---------G---S------VL--SA---A-----V--------------------DT---AE----------------TND--------------T--E---PD---E--------------------G----L---S---------A-E----N-----------E--------G----------------E------------T----R----------I-----------I--R--I------T---G----------S----------------------------------------------------------------------------------------
> str07: M-A-F------------------------D----------------F---S-V--TG-----------------N--------T-------K--L------D------T-------S-----------------G------------F---T---Q----------GV----S---------------------S--------------------------------------------------M--------TV----------A-------A----G------T--------L--IA----DLVK-T-----A--S----------S--------Q----------LT----------NL-----------A----------QS-------------------------------------------------------------------
> str08: M-AV----------------------------I--L-------P------S----T----------------------------Y-----------T----D----------GT---A----------A------C------TN-G---------------S--------P--D-V----------V-G----------TG-------------T------------------------------M----W----V--N---T-----------------I----L--PG----D--------F--------------------------F------------------------------------W-T-P--------SG-----------E------S--V--R----V------------------------------------------
> str09: M-----------N--------------T----------------------------GI-------------I-D---L-----------F-----------D-N-------------------------------------H------------V----D-SI-------P-----------T--------IL--P-------------------------------H-QLA---T-LD----------Y-------L--------------V-----------R-T---I-------I-----D---------------E-N-----------------R-S-V----L------------LF--------------------------------------H-----------I-----MG---------------S----------G-----
> str10: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR----T--------------Q-----LP--------------P-----A----------------------Y--T----------------------N-------S--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-------------S------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M----------------------------D-----------S-----------KET-IL------------I------E----------------I---------IP-------------KI----KS-----------YL---------L--------DT----------------------N-------I--SPK-S--------------------Y-ND-F---------------------I-S----------R-----------------N---------K---N------I----F--V-----I---------N-------------L---------YN-----V-----------S---T-----------------------------I------------------------------------------------------
> str12: M----L---L------S---G-----K--------------------------K--------------K----------M--------L-----L------D-N------YE-T---A----------A---ARG-----------------RG------------G------D-----------E-R---------R-----------R----------------------G-----------------WA---------------F-D-R---------P-----------------A------------IV------------------T---------------------------------K---------R-------D-------K-------S----DR-------------M--------A-------------------H----
> str13: M-----------N-------G----E----------------------------E-------D----------DN---E-------QA---------A-------------------A----E--Q-----------------------------Q----T----------K-----K-A----------------KR----E---------K--P----------K--Q-A-------RK-V-----------T--------S------E---A--------------------------W------------------E-------H-FD--A---------------T------D------------D----G------------A----E------------------C-----K-----H-----------------------------
> str14: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS------V------E-----------------E-----V--------L--------S------------E----A------R------Q----------------------H--L---------K-----------D------------G--------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M------------R---------------------------------YI---V-----------S-P--------Q-L--------------------V-------------------------LQ------------V------G---K---G-Q---------E-V-----------------E-R--A-LY-----------L--------TP---Y--D--------------------------Y----------I--------DE--K----S--P--------I---------Y---------------------------------------------Y----------------F---------L--R---S---------------------H------L-------N-------------I-----------QR------P--
> str16: M----------P-R-V---P---V-----------------------Y--------------D-S-P--------Q----------------------V-----S-P--N---TV----P-----Q--A----R------L---------------A---T---------P-S----------------FA--------T------P-------T---------FR------G------------------AD-------------A-P-----A-----------------FQD--------------T-----A------N---------------Q----------------------------------------------Q--A------R--------------------------------Q-------------------------
> str17: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR----T--------------Q-----LP---L-----A-------Y-----------T------NS--FT------------------------RG---VY-----------------------------YP--D---K--------V--F-------RS---------S-V--L-------------HS---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: MF-VF----------------F-V----L------L-------P-------LV-----------S-----------------S---Q------------------------------------------------C--V----N------LT--------T-----------------R---T---------------------QLP--------PA--YTN------S-----FT---R----G----------V--------------------Y-----------------------Y-------P------------D-----K-----V-----------------------------FRS--------------S----------V--L-------H----------S----------------------------------------
> str19: M-----E------------------------AI---------------I-S----------------F--------A-------------G----I----G----I---NY---------K-----K----L-----------------------Q-----S---------K----L---QH--D----F----------G--------RV--L------------K----A-----L----------------TV------T---A----R--AL-----P-------G---Q--------------P------------------KH--------I----------A---I---R----------------------------Q--------------------------------------------------------------------
> str20: M-A----S--------S---G-------------P-------------------E------R-A--------------E------HQ--------I---------I------------------L----PE-------------S------------------------------------H----------L-S---S-------P------L---------V--KH------------K------L---------L------------------Y-----------------------YW-----K---------L--------------T--GL--------P---L-----P-D-EC---------D---------------------------------------F------------DH-----LI----------------------
> str21: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS------V------E-----------------E-----V--------L--------S------------EVR----------------Q----------------------H--L---------K-----------D------------G--------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L-------------------------A--P------S-P-----NS--K---I-Q-----L-F------N------------------N-I-------N-I---------D-----I--------------N--Y--------E--------------------------------HT---------LY------------------------------F------A---------SV-----S--A----Q-N----S---F------------------------F------A--------------------------------------Q----------------------------WV--------VY-S-------A--------D------K----------A---------------I----------------------
> str23: M------S-----------------------AI-----T---------------ET------------K------------P-T-----------I------E---------------------L----P--A-------L---------------A--------EG-F-----------Q------R-----Y---------N--------K-TP----------------G-FTC-----V----L----D------R----------------Y-----------------D---------------------H--G-------------V---I---------N---------D-------SK--------------------------------I---V-----L---------Y---------------N------------------
> str24: M-------------------------K----------------------N-------I-----A--------------E----------F-K----------------------------K-------APELA---------------EKL------------L-E-VF---S----------N--------L---K---G--N----SR-------S------------L-------D-----------------------------P---------------------------------M-----------RA---G-------KH--D-V----------V--------V----IE-----S---T------------K---------K-L-----------------------------------------------------------
> str25: M----------P------QP--------L------------------------K-----Q----SL-------D-Q------S--------KW-L----R--E--------------A----E---K--------------H--------L-R---A------L-E------S---L---------V--------------------DS------------N--------L--E-------------------E----------------E--K-L-----------KP----Q-L-S----M----------------GED-----------V----Q---S---------------------------------------------------------------------------------------------------------------
> str26: MF-VFL--VLLP--LVSSQ---CVN---L---I-----TR----T--------------Q----S-------------------Y-----------T------NS--FT------------------------RG---VY-----------------------------YP--D---K--------V--F-------RS---------S-V--L-------------HS------T--------------------Q------------D----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-------------------------K-------------------F---------------D------VL-----------S-----LF-------A--------P---------------------------------------------------W-----A------K---V--------DE------------------Q------E-------Y--D------Q--------------------------QLN------------------N-------------N---LESI----------T-----A-------P---K--FD-------D-G------A-TEI------E-----S------E---R----G--D--------------I------------------------------------------------------
> str28: MF-VFL--VLLP--LVSSQ---CVN---------------------F--------T------------------N-----R--T--Q-L-----------------P---------SA---------------------Y--TNS--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-------------S------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-------------------------------------------------------------------------------------------W-----------SI---------------I-VL-K----L--------------I--------------SI-----------------Q--------------P---------L-------L----------------L-----------V-----------T--------SL---P------LYN---P---------N----------M-D-----SC--------------C---------LI----S-------------R-I----------T-PELAG------K-----------L------T-------------------------W---I--------F---------I---
> str30: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS------V------E-----------------E-------------------F-------L-----------------S-------E-------------A--------R---Q-----------------------------------------------------H-L-K------D------------------------G------------T-------------------------------------------------------------------------------------------------------------------------
> str31: MF-VFL--VLLP--LVSSQ---CV-------------------------------------------------------M-P------LF---NLIT-----------T----T----Q--------S-----------Y--TN---F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-L------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M-----------------------------H------Q----------I------T----V--------V------------S-------G---------------P-T--E--V-S-------------------------T---------------------------------------------------------------------------------------------C------FG---S--------L-------------------------H----P---FQ---S-------L-KP----V----------M---------A------------NAL----G-------------V----L-----E-GKM--------------------------F-CSI------G------------G-RS----L-----------
> str33: M-A------------------------TL------L---R-SL--A-----L---------------FK-----------R------------N--------------------------K----------------D-----------K--------------------P------------------------P----------------------I-T-------S---G--------S--G--------------------GA-------------I---R----GI----------------K--------H--------I-----------I-----IVP------I--P-------------------G--------D-S--S---------I-T-----T--------R--------------------S------R---------
> str34: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQVRD------VL---------------------------VRG------F----G--DS---------------------------------------------------------M----------E----------------E-------V--L---S---------------E-----------------A-------R----------------------QH-L-K------D------------------------G------------T-------------------------------------------------------------------------------------------------------------------------
> str35: MF-VFL--VLLP--LVSSQ---CVN---L---------T-----T-----------G---------------T--Q-L---P------------------------P----------A---------------------Y--TNS--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H-------------S------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: M-A---------N-------------------I---------------IN-L----------------------------------------WN------G----I--------V----P------------------------------------------------------MV----Q---D-V----------------N------V-----ASI-T----------A--F-----KS---MI-----DET------W-------D---K-------------K--I-----E--A----------------------N---------T---------------------------C--------------------------------------IS-----R-----------K-----H-----------R----N------------
> str37: M----L------NR------------------I----QT-L--------------------------------------M-----------K----TA-----N-----NYE-T-------IE-----------------------I---L-R----N-----------Y------L-R-------------LY------------------------I---------------------------IL---A-------R-----------------N------------------E-----------------------E--------------G----RG-I-----L--I-------------------------Y-----D------------DNI-----D-------S------------V---------------------------
> str38: M-A--------------------------D----P----------A----------G---------------T-N---------------G-----------E--------EGT--------------------GCN--------G------------W---------FY-----V---------E----A----------V--------VEK-------------K--------T--------G-------D-------------A-------------I----------------S------D----------------D-----------------------------E---------N----------E--------------N---------D--S----D-TG-------------ED------L---------------VD------
> str39: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR----T--------------Q-----LP--------------PS-Y-----------T------NS--FT------------------------RG---VY-----------------------------YP--D---K--------V--F-------RS---------S-V--L-------------HS---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L-----V---PGF--NEKT--H-----VQ--LSLP--------V-----LQV--------------------------------------------------------------------------C-DV-L-------------V-----------------------R---------GF----------G------DS-VE---------------------E--------V----LS----E------------A----R----------QH-L-K------D------------------------G------------T-------------------------------------------------------------------------------------------------------------------------
> str41: M-----------N-----------N------------Q-R-------------K--------------K---T---A---RPS------F---N--------------------------------------------------------------------------------M-LKRA-------R---------------N-----RV------S--T--V----SQLA--------K------------------R-------F----------S--------K-G-----L---------L----S--------G------------------Q--G---P-------------------------------------M--------K-L--------V----------------M--------A----------F-------------
> str42: M------S----N--------F-------D-AIR-----------A-----LV---------D---------TD--A-------Y------K--L-----G----------------------------------------H----I----------------------------------H---------------------------------------------------------------M---Y------------------P-E--------G------T---------E---Y-----V----------LS---N-------F-T------DRGS-------------R-IE---------------G-V-----------------------TH----T---V------------H-----------------------------
> str43: M-------------------------------I---------------------E---L--R-----------------------H----------------E-----------V---Q---------------G--D--L-------------V-----T-I--------------------N--V--------------VE-----------TP-----------------E----D--------L----D------------G-F---R----------------------D--------F--------I-RAHL-------IC---------L-----------A----V---D-----------T--E----------------------------T-----TGL-------------D-------I---------------------Y
> str44: MF-VFL--VLLP--LVSSQ---CV-------------------------------------------------------M-P------LF---NLIT-----------TN--------Q--------S-----------Y--TNS--F---TRGV--------------Y-----------------------Y-P-----------D----K----------VFR--S------------SV----L-----------------------------------H--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M------S------------------K--D-----LV--------A---------------R-------------QAL-M---T---A-----------R--------------------------------------------------------------------------M--K-A----D----F-----------V----------------------F---------F--L-----F-----------V-L---W-----------KAL--S------L--P-----------------V-PT----R-----------C-----------Q----I-------------D-------------------------M----A---K-----------K----L---S-A-----G--------------------------------
> str46: M-A----S-LL---------------K--------------SL-T------L---------------FK-----------R--T---------------R-D----------------QP---------P-LA-----------SG---------------S----G---------------------G-AI-----R--G-----------------I-------KH--------------V---I-------------I-----------V--L----IP-------G----D--S------------S-IV------------------T-------R-S-------------R-------------------------------------------------------------------------------------------------
> str47: M------------R-V-----------------R----------------------GIL--R------------N-----------------W-------------------------Q------Q--------------------------------W-------------------------------------------------------------------------------------------W---------IWTSLG-F---------------------------------WMF--------------------MIC--S---V----------V---------G------NL----WVT-------VY-----------Y-----------------G--V-------------PVW----KE----AK-----T------T-
> str48: M-AV--E----P---------F------------P----R---------------------R----P----IT-------RP---H-A----------------SI-----E--VD--------------------------T-SGI------G------------G-----S------A--------G-----S---S---E---------K----------VF-----------CL--------I------------------G----------------Q----------------A--------------------E--------------G-----G---------E---P-----N-------T-------V----------------------------------------------------------------------------
> str49: MF---------------------------------------------Y---------------A---------------------H-A-FG---------G---------Y----D------E-------------N---LH--------------A-----------F-P-----------------G--I--S---ST-V--------------A----NDV-RK----------------------Y-------------S--------V---------------------------------V---S--V--------------------------------YN------------------K---------------K-------Y-------NI---VK------------NKYM------W--------------------------
> str50: M-A---------N----------------------------------Y--S--K------------PF--L------L-----------------------D---I--------V--------------------------------F---------N-------------K-D-----------------I----K---------------------------------------C---------I-----------N----------D--------S--------------------------------C------S---------HS-D----------------------------C---R-------------Y------QSN-SYV-ELRR-N-----------------------------QAL----N---K-NL-----------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 454
> best bound: 0.0
> wall time: 60.071189s
> ```
