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
Model = scsp.model.didp_charcount.Model
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
>  Sol: ulctkignycojiqesovfkaozuhmpxplnhtqgbxrddxbcvsuqpzvxissbrvnngxf
> str1: ---tk-gn-----------k---uhmpx--nhtqg-x-----------zvxis---------
> str2: -----i----ojiq----f--o-------ln----bx---x-cvsuqp-v-issb-----xf
> str3: ulc--i-nyco----sov---oz---p-pl-----------------p--------------
> str4: -----ig-------e--v--a-z-----------gb-rdd-bc-s----v-----rvnng-f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 0.74s
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
> --- Solution (of length 101) ---
>  Sol: ulcigenpybczfojtrivaxwxqksrdeovfozplgnbrkzxulctodthmdpbxcvsmqvrvnnghtdfuqilgxpfzvxciwsdmsbroqvbbhlxef
> str1: ---------------t--------k-----------gn--k--u------hm-p-x--------n--ht---q--gx--zvx-i-s---------------
> str2: ---i---------oj--i-----q-------fo--l-nb---x------------xcvs------------uq----p--v--i-s--sb--------x-f
> str3: ulci--n-y-c--o-----------s---ov-ozp------------------p--------------------l--p-----------------------
> str4: ---ige------------va-------------z--g-br--------d---d-b-c-s--vrvnng---f------------------------------
> str5: -------py-------------------------pl---r-zxu-c-------p-----mqv----g-tdfu-i------v-c---d-sb-o---------
> str6: -------p-b-----------------de-v-----------------d-------cv-----------d-------pfz-----s-msbroqvbbh----
> str7: -----en--bczf-jt--v-x-------e----------r-z------------b-------rv---------i-g-p-------------------l-e-
> str8: ----------------r---xwxqk-rd-----------r----lctodt-m-p--------r--------------p---x--w-d--------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 101
> best bound: 70.0
> wall time: 60.28s
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
> --- Solution (of length 162) ---
>   Sol: krexulpkqbsfigowcexqkrjidnqfycosovozpadfirhlctrzxudkgxqvhqncejwokdktmpabivbcvzfgijkoztvwxuehrmpxcvsqwddybcsvgitdqbarvnhtezphkfnuivcdzsmsbrgoqgxzpvxisbsbhmlgplxeuf
> str01: ---------------------------------------------t-----kg-----n-----k------------------------u-h-mpx---------------------nht--------------------qgxz-vxis-------------
> str02: ------------i-o-------ji--qf--o------------l--------------n------------b----------------x------xcvs----------------------------u------------q---pv-is-sb------x--f
> str03: ----ul----------c------i-n--ycosovozp--------------------------------p------------------------------------------------------------------------------------l-p-----
> str04: ------------ig---e---------------v---a---------z----g------------------b--------------------r--------dd-bcsv-------rvn--------n-----------g----------------------f
> str05: ------p---------------------y-------p------l--rzxu---------c---------p-----------------------m-----q-------vg-td-------------f-uivcd-s--b--o----------------------
> str06: ------p--b--------------d-----------------------------------e------------v---------------------------d---c-v---d----------p--f------zsmsbr-oq----v---b-bh---------
> str07: --e----------------------n---------------------------------------------b---c-zf--j---tv-x-e-r----------------------------z--------------br-------v-i-------gpl-e--
> str08: -r-x-----------w--xqkr--d----------------r-lct-----------------o-d-tmp----------------------r-px----wd------------------------------------------------------------
> str09: k------kq----------------------------a-fi-----------g-q------jwok-k-------------------------------s-------------------------k------------r-----------b----lg------
> str10: -----l------------x-----------------------------x--------------------pabivb-vz----koz------------------------------------z-------v-d------------------------------
> str11: kr----------i--------------f---s-----a-----------------v--nc-----d---------------------------------qw-----------------h--z--------c-------------------------------
> str12: --------q----------------------------a----------xud-g-qv-q-ce-w--------b------fgij-o---w------------w--y----------------------------------------------------------
> str13: -r--------s-------xq--j--n-f--------pad-i--------u------------------------------------------------s----------i--qb------ez-hk--------------o------------hm-g------
> str14: ------------i--w---------------s----------h------------vh--c---o----m---i----------------u-------v---dd-------------------------------m---------------------------
> str15: ------------------------------------------h--t--x----xq------j---------------z---------------------q----bc----t--ba---------k-n-----------------------------------
> str16: ---xu-----sf----c----------f-------zp-----------------------e-----------------------------e-----cv--w-------------a--n-t-----f--------m---g-q--z----------------u-
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 162
> best bound: 72.0
> wall time: 61.06s
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
>   Sol: bbaedcdabcedeecbdbecabdcade
> str01: ----dc--bc----c-db-c---c--e
> str02: b---d-d-b-e-ee----e--bd----
> str03: -----c-a-c-deec---e--b----e
> str04: --aed-d----d----d-e--bd--d-
> str05: --a--c--b-e-e-c-----ab-c--e
> str06: bba-----b-e----bd--c-b--a--
> str07: bbae---a--e----b----a-d-a--
> str08: ---e------e-eecbdbe-------e
> str09: -----c---c-dee--d---a-dc-d-
> str10: b---d--ab--d---b--e-a---ad-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 27.0
> wall time: 0.29s
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
>   Sol: aedcaebcdaedbcaebdacebdceabdceabde
> str01: --dc--bc-----c---d---b-c----ce----
> str02: ------b-d--db--e----e---e----e-bd-
> str03: ---ca--cd-e----e---ceb--e---------
> str04: aed-----d--d-----d--ebd----d------
> str05: a--c--b---e----e---c-----ab-ce----
> str06: ------b-----b-a-b---ebdc--b---a---
> str07: ------b-----b-ae--a-eb---a-d--a---
> str08: -e---e----e----e---c-bd---b--e---e
> str09: ---c---cd-e----e-da---dc---d------
> str10: ------b-da--b----d---b--ea----a-d-
> str11: -ed--e--da----a---a-e----a----a---
> str12: a---ae---a----a-b---e---ea--c-----
> str13: -e--a----a--bca----c---c---d---b--
> str14: ------b-d-e----e--a---d-ea-d-e----
> str15: ---cae--da-d---e----e---e--d------
> str16: -e----bc-a-db-a-b----b--e---------
> str17: --d-----d----c-e----e----abd-ea---
> str18: --d-a-bcd--d---e--a-e--c----------
> str19: a---a---d----c-e----e-d--a----ab--
> str20: ae---e-c-----c-e----e---ea----a---
> str21: ------b-----b----da-e--c-a----a-de
> str22: --d-a--c--ed--ae-da--b------------
> str23: a---ae---a--b---b----b----b-ce----
> str24: --d--e--d---bc--b--c-----a----ab--
> str25: --d---b-da----aeb----b-c--b-------
> str26: --d--eb---edb--eb-ac--------------
> str27: ---c-e----e-bc---d-c-bd-e---------
> str28: --d---b---ed--a---a---d--a----ab--
> str29: ---c---c-----c---d-c-b--e-bdc-----
> str30: ae---e---a---c---d---b-c--bd------
> str31: --d-a--c----b--e--ac---c----c---d-
> str32: -e-c-ebc-----c---d---bd---b-------
> str33: --d-----d---b---b--ce-d--ab----b--
> str34: a---ae---a--b-a---a-eb---a--------
> str35: -e-c--b-----bca---a---dc---d------
> str36: --d--ebc-----c-e---c--d---b-c-----
> str37: --d-a----a---c--b-a-e---e-b-c-----
> str38: a-d-a-b---e---a---ac---ce---------
> str39: --d-ae-cd---b-a----c-----a----a---
> str40: --d-a--c----b---bd-ce-dc----------
> str41: --d--e--d---b--e----eb----bd-e----
> str42: ---c----da-d-c---d-c--d--a----a---
> str43: ---c-e----ed-c--b-a-e---e--d------
> str44: ---c-e---ae--ca---a------a--c-a---
> str45: --dc---c-----c-eb----b----b---a-d-
> str46: ------b--ae----e--a-eb----bd-e----
> str47: --d---b-d-e-b-a----c---c---d---b--
> str48: -e----bc----b--e----e-d--a---ea---
> str49: ae---e----e-b---bd---b-c-a--------
> str50: --d---b-da--bc-e---c-b----b-------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 31.0
> wall time: 62.27s
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
>   Sol: TCATACCGGTAGATCAGACTGTCA
> str01: --AT---GG--GAT-A--C-G---
> str02: --ATACC--T---TC---C---C-
> str03: -CA--C-G--A-AT-----TG--A
> str04: T-A-A-----A-ATC----TGT--
> str05: --A----GGTA-A-CA-A-----A
> str06: T--T-CC--TAG----G--T---A
> str07: T--T---G-TAGATC----T----
> str08: T------GG--GA--AG--T-TC-
> str09: T--T-CC---A---CA-ACT----
> str10: TC-TA-----A-A-C-GA-----A
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 24.0
> wall time: 0.04s
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
> --- Solution (of length 140) ---
>   Sol: TAACTGCGTAAGTCAAGCTCATACGTCACAGTAGCATCGAGCTAGCTACAGTAGTACTCAAGCTGCATCGAGCATGTCACTTAGCGATCGAGTCGAACTGCTAACGTCTAGATGCGTACCAGCTACGTGCACTGATCARG
> str01: TA---G--TA-GT-A-G---A--C-TC-C-G--G-A---AG-T-G--ACA--A--AC-C---CTG-A---A--A----A----G--A---A-T-G----G--A---T--A-A-----A-----TA--T--A---------
> str02: -----G-G-A--T-AA----A--C---AC--T--C--C---C--G--A-A--A--A-T-AA--T---T------TG--ACTTA---A---A--C-AAC-GC----G---A----C--A---G-T---T-CA---A----G
> str03: -A--T----A---C---CT--T-C--C----TAG----G---TA---ACA--A--AC-CAA-C--CA---A-C-T-T---TT-G--ATC---TC----T--T---GT--AGAT-C-T----G------------------
> str04: TAA------A--T-----T-ATA----A---T--C-T-----TA--TAC--TAGTA---AA-----A---A--AT---A----G-G---G--T-G---T---AAC--C--GA-----A--A---ACG-G---T---C---
> str05: T---T----AA---AA-C--A---G-C-C--T-G--T-G-G---G-T----T-G--C--A--C--C--C-A-C-T--CAC--AG-G---G---C---C--C-A-C-T---G--G-G--C--GC-A-----A--G------
> str06: -A--TG---A---C----T--T-C--CA-A-T-G----GA--T--C--C-------C--AA-C--C-TC-A--A-G-C--TT--C---C-A--C---C--C---C----A-ATG-GT------T---T-CA--G--C---
> str07: -AAC-----AA---A--C-CA-AC--CA-A----C-T-----T---T----T-G-A-TC----T-C-T------TGT-A----G--ATC---T-G---T--T--C-TCTA-A-----AC--G--A-----AC--------
> str08: -A--TG---AA---AA-C------G--A-A--A--AT-----TA--T----TA-T-C--AAG--G----G----T---A-T--G-GA---AGT-G----G--AA-G-CT-GA--CG-A--A---A--T------------
> str09: -A-CT-CG---G-C----T-----G-CA---T-GC-T-----TAG-T---G-----C--A--CT-CA-CG--CA-GT-A-T-A---AT----T--AA-T---AAC-T--A-AT---TA----------------------
> str10: T---TG--TA-G--A---TC-T--GT-----T--C-TC----TA---A-A------C----G----A---A-C-T-T---T-A---A---A----A--T-CT---GT---G-TG-G--C----T--GT-CACT---C---
> str11: -----GC--A-G--A-GC--AT---T-----T----TC----TA---A---TA-T-C-CA--C---A---A--A----A-T--G--A---AG--G--C----AA--T--A-AT---T----G-TAC-T--ACT---C---
> str12: -A--TG---A-G-C---C--A-A-G--A---T--C--CGA-C--G--A-AG-AG--C-C---C--CA---AG---G--A----G-GA--GA----A---G-----G---AG--G-G-ACC--C--C---C----------
> str13: T--CT-C--A---CA-G-T--T-C---A-AG-A--A-C---C---C-A-A--AGTAC-C---C--C--C---CAT---A----GC---C----C----T-CT----T--A-A-----A---GC--C----AC--------
> str14: -A---G-GT---T-----T-ATAC--C----T----TC---CTAG-----GTA--AC--AA-----A-C---CA----AC----C-A---A--C----T--T----TC--GAT-C-T-C----T---TG---T-A-----
> str15: -A---G-GT---T-----T-ATAC--C----T----TC---C---C-A--G--GTA---A--C---A---A--A---C-C--A---A-C----C-AACT--T----TC--GAT-C-T-C----T---TG---T-A-----
> str16: TAA------AA--CAA-CTCA-A--T-ACA--A-CAT--A---AG--A-A--A--A-TCAA-C-GCA---A--A----A---A-C-A-C---TC-A-C----AA-----A------------------------------
> str17: ---C--CG-----C---C-CAT---T-----T-G----G-GC--G-----G-----CTC----T-C---GAGC--G--A-T-AGC--TCG--TCGAA-T-C---C--CT-----CG-ACC---T----------------
> str18: -A--T----A---C---CT--T-C--C-CAG--G--T--A---A-C-A-A--A---C-CAA-C--CA---A-C-T-T---T---CGATC---TC----T--T---GT--AGAT-C-T----G------------------
> str19: T--CT-C--A---CA-G-T--T-C---A-AG-A--A-C---CT--C-A-AGT----CTC---C--C--C---CAT---A----G-G--C----C----T-CT----T-T-----C--A---G-T-C----A--G------
> str20: -----G---A--TC----TC-T-C-TCAC-----C---GA---A-C--C--T-G-------GC--C--C---C--G-------G-G--C-A----AA-TGC---C--CTA-AT-C---C-AG--A-G-G---TG------
> str21: -A---G---A-G-CAA--TCA---GT----G---CATC-AG--A---A-A-TA-TAC-C----T--AT------T---A-T-A-C-A-C---T-----T--T---G-CTA-A-G---A--A--T----------------
> str22: -AA-T---TAA---AA-C--AT-C-TCA-A-TA-CA---A-C-A--TA-AG-A--A---AA-----A-C-A--A---C-----GC-A---A----AA-----A-C----A----C-T-C-A--T----------------
> str23: -AA------A---C--G---A-AC-T-----T----T--A---A---A-A-T----CT---G-TG--T-G-GC-TGTCACT---CG---G---C----TGC-A---T---G---C-T------TA-GTGC----------
> str24: -A--T----AA--C----T-A-A--T-----TA-C-T-G---T--C----GT--T------G----A-C-AG---G--AC--A-CGA--G--T--AACT-C----GTCTA--T-C-T------T-C-TG-----------
> str25: -A--TG---A-GT---G-TCA--CG--A-A-T----TC-A-C--G-TACA--A-T------G----A---A-C-TG-------G--AT-G--T-----T-C-A-CGT---G--G---A--A--TA-----A---------
> str26: -A-C--CGT--G----G-------G-C---G-AGC---G-G-T-G--AC-------C----G--G--T-G----T--C--TT--C---C---T--A---G-T---G----G--G--T-CC--C-ACGT----TGA--AR-
> str27: -AA------A-G----G-T--T---T-A---TA-C--C----T---T-C-------C-CA-G--G--T--A--A---CA---A---A-C----C-AAC--C-AAC-T-T---T-CG-A-----T-C-T-C--T--T---G
> str28: -A---G--TA-GT-----TC----G-C-C--T-G--T-G---T-G--A--G-----CT---G----A-C-A--A----ACTTAG---T--AGT-G---T--T----T---G-TG---A---G----G---A-T--T-A--
> str29: T---T---TA--T-A--C-C-T---TC-C--TAG----G---TA---ACA--A--AC-CAA-C--CA---A-C-T-T---T---CGATC---TC----T--T---GT--AGAT---------------------------
> str30: -A--TGCG---GTC--G-TC-T-C-TC-C-----C--CG-GCT---T----T--T--T-----T---TC---C----C-C---GCG--C----CG--C-G-T----T---G--GCG--CC-G--A---------------
> str31: -----G--T--G--A--C--A-A----A-A--A-CAT--A---A--T---G--G-ACTC---C---A---A-CA---C-C--A----T-G--TC-AA--GCT----T-T-----C--A---G----GT--A--GA-C---
> str32: -----G--T--GT-AAG---A-A----ACAGTA--A--G--C---C--C-G--G-A---A-G-TG----G----TGT---TT-----T-G---CGA--T--T----TC--GA-G-G--CC-G----G-------------
> str33: -----G---A-G--AA--T-----G--A--GT--C-TC-A--T---TAC-------C----GC--C--CG-G--T---ACTTAGC-A---AG-C----T---AA--T--AG-T-C--AC--G----G--C----------
> str34: -A--TG--T--G----G-TC----G--A---T-GC--C-A--T-G-----G-AG-------GC--C--C-A-C----CA----G---T----TC-A--T--TAA-G----G---C-T-CC---T--G-GCA-T--T----
> str35: -A-C-G---A-G-C--G-T--T---T-----TA--A--G-G---GC--C-------C----GC-G-A-C-----TG-C-----G--A-CG-G-C---C----A-C----A--TG-G--CC--CT--GT--A-TG-T----
> str36: -----G-GT---T-----T-ATAC--C----T----TC---C---C-A--G--GTA---A--C---A---A--A---C-C--A---A-C----C-AACT--T----TC--GAT-C-T-C----T---TG---T-A----G
> str37: T----G-G---G--AAG-T--T-C--CA-A--A--A--GA--T--C-ACA--A--A---A--C---A-C-----T---AC----C-A--G--TC-AAC--CT---G---A-A-G--TAC-A-C-----------------
> str38: -----G---AAG-C--G-T--TA----AC-GT-G--T-----T-G--A--G--G-A---AA-----A--GA-CA-G-C--TTAG-GA--GA----A-C----AA-G---AG---C-T----G----G-G-----------
> str39: -A-C--C--A-G-C--GC--A--C-T-----T--C---G-GC-AGC----G--G--C--A-GC---A-C---C-T--C-----G-G--C-AG-C-A-C--CT--C----AG---C--A---GC-A-----AC--------
> str40: -A--TG-G---G--A--C--A-AC-T-----TA---T-----T--C--C--TA-T-C--A---TG--T-G--C----CA---AG--A--G-GT-----T--T----T--A----C---CC-G----GTG-AC----CA--
> str41: T---TG--TA-G--A---TC-T--GT-----T--C-TC----TA---A-A------C----G----A---A-C-T-T---T-A---A---A----A--T-CT---GT---G-TG-GT------T--GT-CACT---C---
> str42: -AAC--C--AA--C---C--A-AC-T-----T----TCGA--T--CT-C--T--T------G-T--A--GA---T--C--T--G---T----TC----T-CTAA-----A----CG-A--A-CT---T----T-A-----
> str43: -----G-G---GT-----TC-T--G-C-CAG--GCAT--AG-T--CT----T--T--T-----T---T------T--C--T--G-G--CG-G-C---C--CT----T---G-TG--TA--A---AC---C--TG------
> str44: -----G-G-----C----T-----G-CA---T-GC-T-----TAG-T---G-----C--A--CT-CA-CG--CA-GT-A-T-A---AT----T--AA-T---AAC-T--A-AT---TAC----T--GT------------
> str45: T----GC--A--T---GCT--TA-GT----G---CA-C----T--C-AC-G-----C--A-G-T--AT--A--AT-T-A---A----T--A----A-CT---AA--T-TA----C-T----G-T-CGT------------
> str46: T---T-C------CA--C--A-AC-T-----T----TC---C-A-C--CA--AG--CTC----TGCA---AG-AT--C-C----C-A--GAGTC-A---G-----G----G--GC---C----T--GT------------
> str47: T--CT----AA---A--C------G--A-A----C-T-----T---TA-A--A--A-TC----TG--T-G----TG-------GC--T-G--TC-A-CT-C----G----G---C-T----GC-A--TGC--T--T-A-G
> str48: -A-C--CG---G--A---T-----G-----G---C--CG--C--G--A---T--T--T-----T---TCG-G-A-GTC-CTT-G-G---G-G--GA-C--C-A-C-TC-AGA-----A-----TA-G---A---------
> str49: ---CT---T--GT-A-G---AT-C-T----GT----TC----T--CTA-A--A---C----G----A---A-C-T-T---T-A---A---A----A--T-CT---GT---G-TG-G--C----T--GT-CACT-------
> str50: -A--TG---A-G-CA--CT-A-A-G-C---G-A--A--GA---A-C--CA--A--A---AAGC---A--GA-CA----A-T-A-C-A---A--C---C--C----G-CTA--T---TAC---------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 140
> best bound: 93.0
> wall time: 60.12s
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
>   Sol: MFRNQAESSPLNSEYCFDVAIPKGHFVTRANELQHFRKGGPYDQ
> str01: M----A----L-S-YC-----PKG---T----------------
> str02: M---Q--SS-LN-------AIP----V-----------------
> str03: M--------PL-S-Y------------------QHFRK------
> str04: M-----E------E----------H-V---NEL-H-------D-
> str05: M------S---N----FD-AI-------RA--L-----------
> str06: MFRNQ------NS---------------R-N-------G-----
> str07: MF------------Y----A----H----A-----F--GG-Y--
> str08: M------S--------------K--F-TR-------R---PY-Q
> str09: M------S--------F-VA---G--VT-A---Q----------
> str10: M-----ES--L-------V--P-G-F----NE------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 39.0
> wall time: 61.50s
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
> --- Solution (of length 550) ---
>   Sol: MAFNGEDPRYSKLVEPTIRAHLIFGKIEVFIPSVTYDSPLQRNWQQWWVSGPNTIWIVLKPEQLDGTKTHVPRLVSLGSFWNQEQAIAAMCEQDFQTKKLSLPVGANKHPMQIILWLREQKATPGVAESHLAKYSSLPLEIDTFNARSCRLAKDIKCAYLCDRIEDSTAAARPSVKFASYNMKDKPPTIHKLGPVSAHCRMADVDTKSADLFEYEKSLGGHSDQAQDWTGKARGAIEVKDACTSGIGPAFQFLNMLWDAKLYTPDVSEEARLNQAPSGYLYKQDTQHLAISRNDVSTVAMNDVRKPYSVTCSRGGAINLELWVRDSVYPRNEGTFKHILKTGDLYFPAISFDREDQIVCSLHVIKWGLSADYCVEQIPYFANENDGKFSRFNAPMECTDGEDIEFIGRGIATVGEKDHDVATFIRVLIYDGHNSTLADVTARALPGQRVMYIHCAFLDGGEKNALGVLEGFRSDTWDKCKYMFCSIVALERANHISMGQGPMKLATWHERCIQTSRIEGVTHDRMAKKLYSANTFIRVQDKAHDIYRPGN
> str01: M-------R-----------HL--------------------N-----------I---------D---------------------I----E----T------------------------------------YSS--------N--------DIK------------------------N-----------G-V------------------Y-K---------------------------------------------Y-------A-------------D----A------------------------------E----D---------F------------------E--I---L------L-----------FA-----------------------------------------------Y----S-----------------I-----DGGE-----V-E---------C---------L---------------------------------D-----L----T--R-------------
> str02: M----E--R---------RAH--------------------R-----------T---------------H------------Q-----------------------N--------W-------------------------D---A---------------------T-------K---------P-------------R------------E-------------------R-------------------------------------R----------KQ-TQH----R--------------------------L--------------T--H---------P----D--D----S---I-------Y-----P-----------R------------IE-----------K----A---------------------------------------E----G-----R-----K-----------E--------------------------------D-------------------H-----G-
> str03: M----E-P----------------G------------------------------------------------------------A--------F-----S---------------------T---A---L------------F---------D---A-LCD---D----------------------I--L-----H-R--------------------------------R-------------------L--------------E--------S-----Q----L---R------------------------------------------F------G------------------------G------V-QIP---------------P-E----------------V--------------------S---D------P--RV-Y---A---G---------------------Y------AL--------------L----------------------------------------------
> str04: M---G------K-----------F-----------Y-------------------------------------------------------------------------------------------------YS---------N-R--RLA----------------------V-FA---------------------------------------------QAQ-----------------S--------------------------R---------------HL-------------------------GG----------S-Y---E-----------------------Q---------W-L-A--CV--------------S----------G-D-------------------------------S--A------------------F---------------R---------------A-E-----------------------------V------K----A----RVQ-K--D------
> str05: --F--------------------F-----------------R-------------------E-------------------N-----------------L-----A-------------------------------------F-------------------------------------------------------------------------------Q-Q---GKAR---E------------F-------------P--SEEAR---A-----------------N--S---------P---T-SR------ELWVR-----R--G--------G---------------------------------------N-----------P--------------------------------L------S--------------------------E--A-G---------------------A-ER------------------R--------G-T-----------------------------
> str06: M-----DP--S-L---T-----------------------Q-------V------W-----------------------------A-----------------V--------------E-----G---S---------------------------------------------V----------------L---SA----A-VDT--A---E---------------T------------------------N---D----T----E-------P-------D-----------------------------------E------------G-----L----------S-------------------A----E------NE--G---------E-T---------R-I-------------IR--I------T----------G--------------------------S-----------------------------------------------------------------------------
> str07: MAF---D----------------F--------SVT---------------G-NT-----K---LD-T--------S-G-F----------------T--------------Q------------GV--S-----S----------------------------------------------M-----T------V-A----A----------------G---------T-----------------------L------------------------------------I--------A--D----------------L---V------------K----T------A-S---------S---------------Q--------------------------------------------------L-------T---------------------------N-L----------------------A----------Q---------------S-----------------------------------
> str08: MA-----------V---I---L---------PS-TY-----------------T----------DGT------------------A-A--C-----T---------N-----------------G---S--------P---D--------------------------------V-------------------V-----------------------G---------TG------------T-----------M-W--------V------N-----------T----I----------------------------L---------P---G---------D--F----F--------------W-------------------------------T----------------------------------------------P---------------------------S------------------------G----------E-----S----V---R-------------V------------
> str09: M--N------------T-------G-I---I-----D--L---------------------------------------F-------------D------------N-H----------------V---------------D-----S------I-----------------P--------------TI--L-P---H-------------------------Q----------------------------L-----A---T--------L-----------D----------------------Y-----------L---VR---------T---I----------I--D-E---------------------------N-------R-------------------------------------------S----V----L------------L-------------F----------------------HI-MG----------------S---G-------------------------------
> str10: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V--N-------L--R----T-----------------------R--------------------T-------------------------------------------------------Q----------------------------L----------P-----------P------------A-----------------Y--T-------N-------S--------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S------------------------------------------------------
> str11: M-----D---SK--E-TI---LI----E--I-----------------------I-----P------K------------------I----------K--S--------------------------------Y--L-L--DT-N---------I-----------S-----P--K--SYN--D---------------------------F-----------------------I-------S--------------------------R-N--------K----------N-----------------------I-----------------F----------------------V-----I-----------------N--------------------------------------------L-Y---N-----V---------------------------------S-T----------I----------------------------------------------------------------
> str12: M-----------L--------L----------S-----------------G--------K-------K-----------------------------K------------M---L-L------------------------D--N-------------Y-----E--TAAAR--------------------G------R------------------GG--D-------------E---------------------------------R--------------------R-----------R---------G-------W-------------------------A--FDR------------------------P--A---------------------I---------V--------T---------------------------------------K---------R-D---K------S-------------------------------------DRMA----------------H-------
> str13: M--NGE--------E---------------------D---------------------------D----------------N-EQA-AA--EQ--QTKK------A-K---------RE-K--P--------K------------------------------------------------------------------------------------------QA-------R-----K--------------------------V------------------T-----S----------------------------E---------------------------A-----------------W--------E------------------------------------------H----F------D------A--T-----------------D---------------D-----------------------G------A---E-C---------------K---------------H-------
> str14: M----E----S-LV-P--------G----F------------N------------------E-----KTHV-----------Q----------------LSLPV----------L----Q-----V--------------------R------D--------------------V----------------L--V----R------------------G------------------------------F---------------------------G-----D------S---V------------------------E-----------E-------------------------V--L-------S-----E-----A--------R--------------------------------------------------------Q-----H---L----K-----------D-----------------------G-------T--------------------------------------------
> str15: M-------RY-------I----------V---S-----P-Q-----------------L-----------V--L--------Q--------------------VG--K----------------G--------------------------------------------------------------------------------------------------Q------------EV-----------------------------E--R---A----LY------L--------T--------PY-----------------D--Y---------I----D----------E----------K---S--------P------------------------I-------------------------Y---------------------Y----FL--------------RS--------------------H---------L----------------------------N--I--Q-------RP--
> str16: M------PR----V-P------------V------YDSP-Q-------VS-PNT---V--P-Q----------------------A-------------------------------R------------LA----------T-----------------------------PS--FA---------T-----P-----------T-----F--------------------RGA----DA------PAFQ------D----T------A--NQ--------Q-----A--R---------------------------------------------------------------Q--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V--N-------L--R----T-----------------------R--------------------T-------------------------------------------------------Q----------------------------L----------P-------L--A---Y-----T-------N--S--------------------------------------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S------------------------------------------------------
> str18: M-F----------V---------F-----F---V-----L------------------L-P--L------V----S--S---Q-------C------------V--N-------L-------T-------------------T---R--------------------T-------------------------------------------------------Q----------------------------L----------P-----------P------------A-----------------Y--T-------N-------S--------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S------------------------------------------------------
> str19: M----E-------------A--I---I-----S----------------------------------------------F-----A------------------G-------I-----------G---------------I---N-------------Y----------------K------K--------L-------------------------------Q-------------------S---------------KL------------Q------------H------D----------------------------------------F------G----------R----V--L---K----A--------------------------------------------------------L-------T---VTARALPGQ-----------------------------------------------------P-K----H---I-------------A---------IR-Q-----------
> str20: MA--------S---------------------S-----------------GP---------E----------R------------A-----E----------------H--QIIL--------P---ESHL---SS-PL-----------------------------------VK-------------HKL------------------L--Y-----------------------------------------------Y-----------------------------------------------------------W-------------K--L-TG-L--P-------------L----------------P------D----------EC-D-----F-----------DH--------LI--------------------------------------------------------------------------------------------------------------------------
> str21: M----E----S-LV-P--------G----F------------N------------------E-----KTHV-----------Q----------------LSLPV----------L----Q-----V--------------------R------D--------------------V----------------L--V----R------------------G------------------------------F---------------------------G-----D------S---V------------------------E-----------E-------------------------V--L-------S-----E-------------------------------------V-----------R---------------------Q-----H---L----K-----------D-----------------------G-------T--------------------------------------------
> str22: M-----------L------A-----------PS-----P---N------S---------K--------------------------I-----Q------L-------------------------------------------FN-----------------------------------N-------I----------------------------------------------------------------N-----------------------------------I---D----------------------IN---------Y---E----H---T--LYF-A-S-------V-S---------A-----Q-----N------S-F-------------F-----A-----------------------------------Q----------------------------W----------V--------------------------------V---------YSA-------DKA--I-----
> str23: M---------S--------A--I-----------T--------------------------E----TK---P------------------------T---------------I-----E-----------L------P-------A----LA------------E---------------------------G------------------F-----------Q--------R----------------------------Y----------N--------K--T--------------------P-------G--------------------F-----T-----------------C---V----L--D------------------R--------------------------------------YD-H-------------G--V--I----------N----------D----------S-----------------K--------I-------V--------LY--N-----------------
> str24: M----------K------------------------------N-----------I------------------------------A-----E--F--KK------A---P--------E-----------LA-------E------------K------L-------------------------------L--------------------E------------------------V-----------F----------------S-----N------L-K-------------------------------G---N-------S---R-------------------S----------L---------D------P----------------M------------R--A--G-K-HDV-----V------------V------------I--------E-----------S-T--K-K--------L-------------------------------------------------------------
> str25: M------P--------------------------------Q----------P------LK--Q------------SL----------------D-Q----S------K-------WLRE--A-----E----K--------------------------------------------------------H-L-------R-A--------L-E---SL-------------------V-D---S---------N-L-----------EE--------------------------------------------------E---------------K--LK------P--------Q----L-------S-------------------------M----GED----------V---------------------------------Q-------------------------S-----------------------------------------------------------------------------
> str26: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V--N-------L-------------------------I-T---R--------------------T-------------------------------------------------------Q-------------------S-----------------YT---------N---S---------------------------------------------------------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S---------T------Q---------D---------------------------
> str27: M----------K-----------F------------D-----------V---------L----------------SL--F-----A----------------P------------W-----A----------K-----------------------------------------V--------D----------------------------E----------Q------------E------------------------Y--D--------Q--------Q----L----N-------N----------------NLE-----S-----------I--T------A-----------------------------P--------KF----------D--D----G---AT--E--------I------------------------------------E-----------S----------------ER------G------------------------D------------I--------------
> str28: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V--N------------------------------------F-----------------------T------------N------------------R-----T-----------------Q----------------------------L----------P--S--A--------Y-----T-------N--S--------------------------------------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S------------------------------------------------------
> str29: M------------------------------------------W-----S----I-IVLK---L----------------------I-------------S-----------I------Q---P------L-----L-L-----------------------------------V------------T-------S--------------L------------------------------------P----L--------Y----------N--P----------------N------M-D-----S--C-----------------------------------------------C-L--I----S--------------------R------------I--------T--------------------------------P---------------E---L----------------------A---------G----KL-TW----I----------------------FI--------------
> str30: M----E----S-LV-P--------G----F------------N------------------E-----KTHV-----------Q----------------LSLPV----------L----Q-----V--------------------R------D--------------------V----------------L--V----R------------------G------------------------------F---------------------------G-----D------S---V------------------------E-----------E--F---L----------S---E---------------A-------------------R--------------------------------------------------------Q-----H---L----K-----------D-----------------------G-------T--------------------------------------------
> str31: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V------M------------P------L------------FN-----L---I------------T-------------------T-----------------T-----------------Q-------------------S-----------------YT---------N-------------------------------------------------------------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H---------L----------------------------------------------
> str32: M-------------------H-------------------Q-------------I-----------T---V---VS-G------------------------P-------------------T----E----------------------------------------------V---S--------T----------C------------F------G--S------------------------------L---------------------------------H------------------P----------------------------F--------------------Q---SL---K------------P----------------------------------V------------------------------------M----A-------NALGVLEG-------K---MFCSI-----------G-G---------R----S-------------L---------------------
> str33: MA--------------T----L-----------------L-R-------S--------L--------------------------A-------------L-------------------------------------------F--------K---------R-----------------N-KDKPP-I----------------T-S----------G--S-------G---GAI----------------------------------R------G-----------I--------------K-------------------------------HI----------I-------IV-------------------P------------------------I-----------------------------------------PG-----------D--------------S-----------SI-------------------T-------T-R--------------S-----R-------------
> str34: M----E----S-LV-P--------G----F------------N------------------E-----KTHV-----------Q----------------LSLPV----------L----Q-----V--------------------R------D--------------------V----------------L--V----R------------------G------------------------------F---------------------------G-----D------S--------M-------------------E-----------E-------------------------V--L-------S-----E-----A--------R--------------------------------------------------------Q-----H---L----K-----------D-----------------------G-------T--------------------------------------------
> str35: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V--N-------L-------T-------------------T-------------------------------------------------G------------T-----------------Q----------------------------L----------P-----------P------------A-----------------Y--T-------N-------S--------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S------------------------------------------------------
> str36: MA-N-------------I----I-------------------N---------------L---------------------WN----------------------G-------I------------V-----------P-------------------------------------------M------------V----------------------------Q--D----------V---------------N-----------V---A------S------------I------T-A-----------------------------------FK-------------S--------------------------------------------M-------I-------------D-------------------------------------------E-------------TWDK-K-----I---E-AN------------T----CI--SR----------K---------------H---R--N
> str37: M-----------L-----------------------------N-----------------------------R-------------I-----Q---T--L----------M---------K-T---A-----------------N-----------------------------------N--------------------------------YE-------------T------IE--------I------L-----------------R-N-----YL-----------R--------------------------L--------Y---------I----------I-----------L--------A-------------------R-N---E----E-----GRGI----------------LIYD-------D------------------------N----------------------I------------------------------------D-------S------V------------
> str38: MA----DP-----------A----G---------T-------N-------G----------E---------------------E--------------------G-----------------T-G-----------------------C-------------------------------N-----------G----------------------------------W---------------------F-----------Y---V-E-A------------------------V--V---------------------E---------------K---KTGD----AIS-D--D-------------------E------NEND---S---------D------------T-GE-D---------L-----------V------------------D--------------------------------------------------------------------------------------------
> str39: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V--N-------L--R----T-----------------------R--------------------T-------------------------------------------------------Q----------------------------L----------P-----------PS-Y-----T-------N--S--------------------------------------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H-S------------------------------------------------------
> str40: M----E----S-LV-P--------G----F------------N------------------E-----KTHV-----------Q----------------LSLPV----------L----Q-----V----------------------C----D--------------------V----------------L--V----R------------------G------------------------------F---------------------------G-----D------S---V------------------------E-----------E-------------------------V--L-------S-----E-----A--------R--------------------------------------------------------Q-----H---L----K-----------D-----------------------G-------T--------------------------------------------
> str41: M--N--------------------------------------N-Q---------------------------R------------------------KK-----------------------T---A-------------------R-------------------------PS--F---NM---------L--------------K-------------------------R-A-----------------------------------R-N------------------R--VSTV---------S-----------------------------------------------Q----L--------A----------------K--RF------------------------------------------S---------------------------K---G-L--------------------L------S-GQGPMKL---------------V----MA--------F---------------
> str42: M---------S-------------------------------N------------------------------------F-------------D-----------A------I----R---A--------L-------------------------------------------V--------D---T--------------D-----A----Y-K-LG-H--------------I--------------------------------------------------H------------M------Y---------------------P--EGT-------------------E-----------------Y-V----------------------------------------------------L------S----------------------------N-------F---T-D-------------R------G----------------SRIEGVTH-----------T---V----H-------
> str43: M----------------I---------E-----------L-R---------------------------H-------------E-------------------V-------Q------------G----------------D--------L-----------------------V------------TI----------------------------------------------------------------N-----------V----------------------------V------------------------E-------------T------------P------ED-----L---------D--------------G-F-R--------D-----FI-R--A------H--------LI-------------------------C--L------A--V------DT--------------E---------------T-------T----G---------L----------D----IY----
> str44: M-F----------V---------F---------------L--------V---------L----L-------P-LVS--S---Q-------C------------V------M------------P------L------------FN-----L---I------------T-------------------T-----------------------------------------------------------------N-------------------Q--S-Y-----T-------N--S--------------------------------------F-----T-----------R-------------G------V----Y-------------------------------------------------Y---------------P------------D---K----V---FRS-----------S-V-L----H--------------------------------------------------------
> str45: M---------SK------------------------D--L--------V------------------------------------A-------------------------------R-Q-A--------L--------------------------------------------------M-----T--------A--RM-----K-AD-F-------------------------V-----------F-FL---------------------------------------------------------------------------------F----------------------V--L----W--------------------K-----A---------------------------------L------S-L--------P---V---------------------------------------------------P----T---RC-Q---I-----D-MAKKL-SA----------------G-
> str46: MA--------S-L--------L---K------S------L-------------T----L--------------------F-----------------K-------------------R----T-----------------------R------D---------------------------------------------------------------------Q-----------------------P---------------P-------L--A-SG------------S----------------------GGAI------R--------G----I-K---------------------HVI------------I-----------------------------------V-------------LI----------------PG-----------D--------------S-----------SIV------------------T---R----SR----------------------------------
> str47: M-------R----V----R-----G-I------------L-RNWQQWW------IW----------T--------SLG-FW--------M----F---------------M-I-----------------------------------C-----------------S-------V-------------------V-----------------------G----------------------------------N-LW--------V------------------T---------V-----------Y--------------------Y----G------------------------V-------------------P----------------------------------V--------------------------------------------------------------W-K-----------E-A----------K--T-------T------------------------------------
> str48: MA-----------VEP-------F-------P---------R------------------------------R-----------------------------P---------I---------T-----------------------R-------------------------P----------------H------A----------S---------------------------IEV-D--TSGIG------------------------------G------------S-------A--------------G-----------S-----------------------S---E----------K--------V-----F----------------C-----------------------------LI--G---------------Q-------A-----E----G---G-------------------E----------P-------------------------------NT---V------------
> str49: M-F------Y---------AH----------------------------------------------------------------A--------F---------G-------------------G--------Y-------D----------------------E---------------N----------L-----H---A---------F-----------------------------------P-----------------------------G-----------IS----STVA-NDVRK-YSV-------------V--SVY--N----K---K----Y------------------------------------N--------------------I---------V--K----------------N----------------------------K------------------YM------------------------W-------------------------------------------
> str50: MA-N-----YSK---P-------F---------------L------------------L-----D---------------------I----------------V---------------------------------------FN-------KDIKC------I----------------N--D-----------S--C--------S------------HSD------------------C----------------------------R-------Y---Q-------S-N--S----------Y-V----------EL--R-----RN------------------------Q-------------A--------------------------------------------------------L-----N----------------------------KN-L-------------------------------------------------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 550
> best bound: 145.0
> wall time: 60.44s
> ```
