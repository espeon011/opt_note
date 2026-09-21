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
Model = scsp.model.dr_alphabet_choco.Model
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
>  Sol: iotjkginqefkouvhlmpxacinyzghtbqgrxddxbcosovosuzpqrpvxisnsblnpxgf
> str1: --t-kg-n---k-u-h-mpx---n---ht-qg-x------------z----vxis---------
> str2: io-j--i-q-f-o---l------n-----b---x--x-c---v-su--q-pv-is-sb---x-f
> str3: -------------u--l----ciny-------------cosovo--zp--p-------l-p---
> str4: i----g---e----v-----a----zg--b--r-dd-bc-s-v------r-v---n---n--gf
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 64
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 60.10s
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
> --- Solution (of length 109) ---
>  Sol: ioprxejnwxbdiqtyckzfgjoptevalnrzdgkxberulchimpvxdmnpxdfhtyzbcoqsvdgmostuvxbdmopqrzfopquvxbinsvwncdgpsblxefhop
> str1: --------------t--k--g--------n----k----u--h-mp-x--n----ht-----q---g------x-------z-----vx-i-s----------------
> str2: io----j-----iq-----f--o-----ln------b----------x----x-------c---v----s-u-------q----p--v--i-s-------sb-x-f---
> str3: ---------------------------------------ulc-i------n------y--co-s----o---v----o---z--p--------------p--l-----p
> str4: i-------------------g----eva---z-g--b-r---------d----d-----bc--sv---------------r------v---n---n--g------f---
> str5: --p------------y-------p----l-rz---x---u-c---p---m------------q-v-g---t----d------f---u---i--v--cd--sb-----o-
> str6: --p-------bd-------------ev-----d--------c----v-d--p--f---z----s---m-s----b-----r--o-q-v-b-----------b----h--
> str7: -----e-n--b-----c-zf-j--t-v--------x-er-------------------zb--------------------r------v--i-------gp--l-e----
> str8: ---rx---wx---q---k------------r-d-----r-lc--------------t----o---d----t-----m-p-r---p---x-----w--d-----------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 109
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 60.20s
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
> --- Solution (of length 152) ---
>   Sol: hiloqrtxejkuwxaginpqsxybkprudfghlmceoqrvzafijptvxzglnpquybcehrdecfpsvwxadtvmnoxbcdipqvgjtudfmsuwgioqzbekpuvxzdhjkorvwxzachinpszdgkmprsblnprxegoqvwbfybdh
> str01: ------t---k----g-n------k--u---h-m-----------p--x---n-------h------------t----------q-g--------------------xz------v-x----i--s--------------------------
> str02: -i-o-----j------i--q---------f------o--------------ln----b------------x-------x-c----v-------su----q----p-v---------------i--s-------sb----x-------f----
> str03: -----------u--------------------l-c--------i--------n---y-c------------------o---------------s----o-------v------o----z-----p------p---l-p--------------
> str04: -i-------------g-------------------e---v-a-------zg------b---rd---------d------bc------------s------------v-------rv-------n------------n----g-----f----
> str05: ------------------p---y--p------l-----r-z-------x------u--c-------p--------m--------qvg-t-df--u--i--------v-------------c------d-----sb-------o---------
> str06: ------------------p----b----d------e---v----------------------d-c---v---d----------p-------f--------z------------------------s----m--sb---r---oqv-b--b-h
> str07: --------e--------n-----b----------c-----z-f-j-tvx----------e-r--------------------------------------zb------------rv------i-----g--p---l----e-----------
> str08: -----r-x----wx-----q----k-r-d---------r------------l------c--------------t---o---d------t---m-----------p---------r---------p--------------x-----w----d-
> str09: ----------k-------------k------------q---afi------g---q--------------------------------j-------w--o----k--------k------------s---k--r-bl-----g----------
> str10: --l----x-----x----p----------------------a---------------b------------------------i--v---------------b----v-z---ko----z-------z-----------------v-----d-
> str11: ----------k---------------r----------------i---------------------f-s---a--v-n---cd--q----------w--------------h-------z-c-------------------------------
> str12: ----q---------a------x-----ud-g------q-v--------------q---ce---------w---------b-----------f----gi-------------j-o--w----------------------------w--y---
> str13: -----r--------------sx---------------q------j-------n------------fp----ad---------i------u---s---i-q-be-----z-h-ko-------h--------m----------g----------
> str14: -i----------w-------s----------h-------v--------------------h---c------------o--------------m----i-------uv--d-----------------d--m---------------------
> str15: h-----tx-----x-----q------------------------j----z----q--bc--------------t-----b---------------------------------------a---------k------n---------------
> str16: -------x---u--------s--------f----c-------f------z---p-----e---ec---vw-a----n-----------t--fm---g--qz----u----------------------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 152
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 60.47s
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
> --- Solution (of length 29) ---
>   Sol: aebdbcdabcdeeaebcdeabcdbeacde
> str01: ---d-c--bc------cd--bc----c-e
> str02: --bd--d-b--ee-e---e-b-d------
> str03: -----c-a-cdee---c-e-b---e----
> str04: ae-d--d---d------de-b-d----d-
> str05: a----c--b--ee---c--abc--e----
> str06: --b-b--ab--e---b-d---c-b-a---
> str07: --b-b--a---e-aeb---a--d--a---
> str08: -e---------ee-e-c---b-dbe---e
> str09: -----c---cdee----d-a--d---cd-
> str10: --bd---ab-d----b--ea-----a-d-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 29
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 60.01s
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
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 60.20s
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
>   Sol: TATCGGTACGACTATCGTACGTAC
> str01: -AT-GG---GA-TA-CG-------
> str02: -AT----AC--CT-TC---C---C
> str03: ---C---ACGA--AT--T--G-A-
> str04: TA-----A--A--ATC-T--GT--
> str05: -A--GGTA--AC-A----A---A-
> str06: T-TC----C---TA--G---GTA-
> str07: T-T-G-TA-GA-T--C-T------
> str08: T---GG---GA--A--GT---T-C
> str09: T-TC----C-AC-A----AC-T--
> str10: T--C--TA--A--A-CG-A---A-
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 19.41s
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
>   Sol: ATGTACGTACGTACGAGTCGTACGTACTACTACGCGTACAGTACGTACGTCTATGACGATACGTACGACCGTACACGTACGTACGTAGTACGACGTACGTACGACTCTAGACTCGACGTACGTACGTACACRTGTACG
> str01: -T--A-GTA-GTA-GA--C-T-C---C------G-G-A-AGT--G-AC----A--A--A--C---C--C--T----G-A---A---A--A-GA---A--T--G------GA-T--A---A---A--TA----T--A--
> str02: --G---G-A--TA--A-----AC--ACT-C--C-CG-A-A--A---A--T--A--A---T---T-------T----G-AC-T---TA--A--AC--A---ACG-C----GAC---A-GT---T-C--A-A---G----
> str03: AT--AC---C-T-----TC---C-TA-------G-GTA-A---C--A-----A--AC----C--A--ACC--A-AC-T---T---T--T--GA--T-C-T-C---T-T-G--T--A-G-A--T-C-T------G----
> str04: -T--A---A---A----T--TA--TA--A-T-C---T----TA--TAC-T--A-G----TA---A--A----A-A---A--TA-G--G---G---T--GTA--AC-C--GA----A---A---ACG-------GT-C-
> str05: -T-TA---A---A--A--C--A-G--C--CT--G--T---G---G---GT-T--G-C-A--C---C--C---AC---T-C--AC--AG---G--G--C---C--C---A--CT-G--G---G--CG--CA-----A-G
> str06: ATG-AC-T---T-C----C--A---A-T-----G-G-A---T-C---C--C-A--AC----C-T-C-A----A---G--C-T---T----C--C--AC---C--C-C-A-A-T-G--GT---T---T-CA---G--C-
> str07: A---AC--A---A--A--C---C--A--AC--C----A-A---C-T---T-T-TGA---T-C-T-C-----T-----T--GTA-G-A-T-C----T--GT-----TCT---CT--A---A---ACG-A-AC-------
> str08: ATG-A---A---A--A--CG-A---A--A--A----T----TA--T---T--AT--C-A-A-G---G---GTA----T--G---G-A--A-G---T--G---GA----AG-CT-GACG-A---A---A----T-----
> str09: A----C-T-CG---G---C-T--G--C-A-T--GC-T----TA-GT--G-C-A---C--T-C--ACG-C---A---GTA--TA---A-T------TA---A----T--A-ACT--A---A--T---TA----------
> str10: -T-T--GTA-G-A----TC-T--GT--T-CT-C---TA-A--ACG-A-----A---C--T---T-------TA-A---A---A--T----C----T--GT--G--T---G----G-C-T--GT-C--AC---T---C-
> str11: --G--C--A-G-A-G---C--A--T--T--T-----T-C--TA---A--T--AT--C----C--AC-A----A-A---A--T--G-A--A-G--G--C--A--A-T--A-A-T-----T--GTAC-TAC---T---C-
> str12: ATG-A-G--C---C-A-----A-G-A-T-C--CG---AC-G-A---A-G---A-G-C----C---C--C---A-A-G---G-A-G--G-A-GA---A-G---GA-----G----G--G-AC---C---C-C-----C-
> str13: -T---C-T-C--AC-AGT--T-C--A--A----G---A-A---C---C--C-A--A--A---GTAC--CC---C-C---C--A--TAG--C--C---C-T-C---T-TA-A----A-G--C---C--AC---------
> str14: A-G---GT---T-----T---A--TAC--CT-----T-C----C-TA-G-----G----TA---AC-A----A-AC---C--A---A---C--C--A---AC---T-T----TCGA--T-C-T-C-T-----TGTA--
> str15: A-G---GT---T-----T---A--TAC--CT-----T-C----C---C----A-G--G-TA---AC-A----A-AC---C--A---A---C--C--A---AC---T-T----TCGA--T-C-T-C-T-----TGTA--
> str16: -T--A---A---A--A--C--A---ACT-C-A-----A---TAC--A-----A---C-ATA---A-GA----A-A---A--T-C--A--ACG-C--A---A--A----A-AC---AC-T-C--AC--A-A-----A--
> str17: -----C---CG--C----C---C--A-T--T-----T---G---G---G-C---G--G---C-T-C-----T-C--G-A-G--CG-A-TA-G-C-T-CGT-CGA----A---TC--C---C-T-CG-AC-C-T-----
> str18: AT--AC---C-T-----TC---C---C-A----G-GTA-A---C--A-----A--AC----C--A--ACC--A-AC-T---T---T----CGA--T-C-T-C---T-T-G--T--A-G-A--T-C-T------G----
> str19: -T---C-T-C--AC-AGT--T-C--A--A----G---A-A---C---C-TC-A--A-G-T-C-T-C--CC---C-C--A--TA-G--G--C--C-T-C-T-----T-T---C---A-GT-C--A-G------------
> str20: --G-A--T-C-T-C---TC-T-C--AC--C---G---A-A---C---C-T----G--G---C---C--CCG-----G---G--C--A--A--A--T--G--C--C-CTA-A-TC--C--A-G-A-G-------GT--G
> str21: A-G-A-G--C--A--A-TC--A-GT--------GC--A---T-C--A-G---A--A--ATA--TAC--C--TA----T---TA--TA---C-AC-T---T-----T---G-CT--A---A-G-A---A----T-----
> str22: A---A--T---TA--A-----A---AC-A-T-C---T-CA--A--TAC----A--AC-ATA---A-GA----A-A---A---AC--A--ACG-C--A---A--A----A-AC---AC-T-C--A--T-----------
> str23: A---A---ACG-A--A--C-T---T--TA--A-----A-A-T-C-T--GT----G----T--G---G-C--T----GT-C--AC-T----CG--G--C-T--G-C---A---T-G-C-T---TA-GT------G--C-
> str24: AT--A---AC-TA--A-T--TAC-T--------G--T-C-GT---T--G---A---C-A---G---GAC---AC--G-A-GTA---A---C----T-CGT-C---T--A---TC----T---T-C-T------G----
> str25: ATG-A-GT--GT-C-A--CG-A---A-T--T-C----AC-GTAC--A-----ATGA--A--C-T--G---G-A----T--GT---T----C-ACGT--G---GA----A---T--A---A------------------
> str26: A----C---CGT--G-G--G--CG-A-------GCG----GT--G-AC--C---G--G-T--GT-C-----T-----T-C---C-TAGT--G--G---GT-C--C-C-A--C--G---T---T--G-A-A-R------
> str27: A---A---A-G---G--T--T---TA-TAC--C---T----T-C---C--C-A-G--G-TA---AC-A----A-AC---C--A---A---C--C--A---AC---T-T----TCGA--T-C-T-C-T-----TG----
> str28: A-GTA-GT---T-CG---C---C-T--------G--T---GT--G-A-G-CT--GAC-A-A---AC-----T-----TA-GTA-GT-GT------T---T--G--T---GA---G--G-A--T---TA----------
> str29: -T-T---TA--TAC----C-T---T-C--CTA-G-GTA-A---C--A-----A--AC----C--A--ACC--A-AC-T---T---T----CGA--T-C-T-C---T-T-G--T--A-G-A--T---------------
> str30: ATG--CG---GT-CG--TC-T-C-T-C--C--C-CG----G--C-T---T-T-T-----T---T-------T-C-C---C---CG-----CG-C---CG--CG--T-T-G----G-CG--C---CG-A----------
> str31: --GT--G-AC--A--A-----A---A--AC-A----TA-A-T--G---G---A---C--T-C---C-A----ACAC---C--A--T-GT-C-A---A-G--C---T-T----TC-A-G---GTA-G-AC---------
> str32: --GT--GTA---A-GA-----A---AC-A----G--TA-AG--C---C--C---G--GA-A-GT--G---GT----GT---T---T--T--G-CG-A--T-----T-T---C--GA-G---G--C---C----G---G
> str33: --G-A-G-A---A----T-G-A-GT-CT-C-A----T----TAC---CG-C-----C----CG---G----TAC---T---TA-G-----C-A---A-G--C---T--A-A-T--A-GT-C--ACG-------G--C-
> str34: ATGT--G---GT-CGA-T-G--C---C-A-T--G-G-A--G---G--C--C-----C-A--C---C-A--GT-----T-C--A--T--TA--A-G---G--C---TC----CT-G--G--C--A--T-----T-----
> str35: A----CG-A-G--CG--T--T---T--TA--A-G-G----G--C---C--C---G-CGA--C-T--G-C-G-AC--G---G--C------C-AC--A--T--G------G-C-C--C-T--GTA--T------GT---
> str36: --G---GT---T-----T---A--TAC--CT-----T-C----C---C----A-G--G-TA---AC-A----A-AC---C--A---A---C--C--A---AC---T-T----TCGA--T-C-T-C-T-----TGTA-G
> str37: -TG---G---G-A--AGT--T-C---C-A--A-----A-AG-A--T-C----A---C-A-A---A--AC---AC---TAC---C--AGT-C-A---AC---C---T---GA----A-GTAC--AC-------------
> str38: --G-A---A-G--CG--T--TA---AC------G--T---GT---T--G---A-G--GA-A---A--A--G-ACA-G--C-T---TAG---GA-G-A---AC-A----AGA---G-C-T--G---G-------G----
> str39: A----C---C--A-G---CG--C--ACT--T-CG-G--CAG--CG---G-C-A-G-C-A--C---C-----T-C--G---G--C--AG--C-AC---C-T-C-A-----G-C---A-G--C--A---AC---------
> str40: ATG---G---G-AC-A-----AC-T--TA-T-----T-C----C-TA--TC-ATG----T--G--C--C---A-A-G-A-G---GT--T------T---TAC--C-C--G----G---T--G-AC---CA--------
> str41: -T-T--GTA-G-A----TC-T--GT--T-CT-C---TA-A--ACG-A-----A---C--T---T-------TA-A---A---A--T----C----T--GT--G--T---G----G---T---T--GT-CAC-T---C-
> str42: A---AC---C--A--A--C---C--A--ACT-----T----T-CG-A--TCT----C--T---T--G----TA---G-A--T-C-T-GT------T-C-T-C---T--A-A----ACG-A---AC-T-----T-TA--
> str43: --G---G---GT-----TC-T--G--C--C-A-G-G--CA-TA-GT-C-T-T-T-----T---T-------T-----T-C-T--G--G--CG--G--C---C--CT-T-G--T-G---TA---A---AC-C-TG----
> str44: --G---G--C-T--G---C--A--T--------GC-T----TA-GT--G-C-A---C--T-C--ACG-C---A---GTA--TA---A-T------TA---A----T--A-ACT--A---A--T---TAC---TGT---
> str45: -TG--C--A--T--G---C-T---TA-------G--T---G--C--AC-TC-A---CG---C--A-G----TA----TA---A--T--TA--A--TA---AC---T--A-A-T-----TAC-T--GT-C----GT---
> str46: -T-T-C---C--AC-A-----AC-T--T--T-C-C--AC----C--A-----A-G-C--T-C-T--G-C---A-A-G-A--T-C------C--C--A-G-A-G--TC-AG----G--G---G--C---C---TGT---
> str47: -T---C-TA---A--A--CG-A---ACT--T-----TA-A--A---A--TCT--G----T--GT--G---G--C---T--GT-C--A---C----T-CG---G-CT---G-C---A--T--G--C-T-----T--A-G
> str48: A----C---CG---GA-T-G---G--C--C---GCG-A---T---T---T-T-T--CG----G-A-G----T-C-C-T---T--G--G---G--G---G-AC--C---A--CTC-A-G-A---A--TA-----G-A--
> str49: -----C-T---T--G--T---A-G-A-T-CT--G--T----T-C-T-C-T--A--A--A--CG-A--AC--T-----T---TA---A--A--A--T-C-T--G--T---G--T-G--G--C-T--GT-CAC-T-----
> str50: ATG-A-G--C--AC---T---A---A-------GCG-A-AG-A---AC--C-A--A--A-A---A-G-C---A---G-AC--A---A-TAC-A---AC---C--C----G-CT--A--T---TAC-------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 138
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 62.48s
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
> --- Solution (of length 47) ---
>   Sol: MPEQSAEFHLRSVYACNPQEGKLNVFHSTDRAFGINRGKPVYAELQT
> str01: M----A---L-S-Y-C-P---K-----------G------------T
> str02: M--QS------S----------LN-------A--I----PV------
> str03: MP-------L-S-Y----Q-------H-----F---R-K--------
> str04: M-E---E-H---V---N--E--L---H--D-----------------
> str05: M---S-----------N--------F---D-A--I-R-----A-L--
> str06: M------F--R-----N-Q----N---S--R----N-G---------
> str07: M------F-----YA-----------H----AFG---G---Y-----
> str08: M---S----------------K---F--T-R-----R--P-Y---Q-
> str09: M---S--F----V-A-----G---V---T--A-------------Q-
> str10: M-E-S----L--V----P--G----F---------N-------E---
> 
> example file name: 'protein_n010k010.txt'
> best objective: 47
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 60.03s
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
> --- Solution (of length 457) ---
>   Sol: MNRSWAFHKLNQVYADEFGHILPQSTVAEGIKLPRTVYADEFGIKLNPQSTVADGIKLMPRSTADEHKLNPRTWYADEHILNPQSADEGILNVYADEFHLNPQSTVACEFGKMPQRSWYADGILNQRAEKLPRTVACDEFGHIKLNPQRSVWADEFGHIKLNQRSTVWYAFGIKLNPRSTVACDEGHIKLMPQSTVAHKLMRTFGLNQRSVYADEHLRTACEFGHIKLNPQRSTWYAFGIKLMNSVADGPSTVEGHKLPRSTVYAEFGIKLMNPQRSVYADEFGIKLNSVWACDEHKLPRSTVYFGIKNRSTVWAEFGILPQTVYCDGKNPRSVADFGIKLQRSTWYADFGHILVYDMNSYGPQRTAEINWAELNPSVDGKYEGTVEFLPRSCDILQRTYAEGNVAEHPRSVWYLADGKLQSTWYEFHIKLMRTAIKLRVDTFGHLQRSGKDINRTY
> str01: M-R----H-LN---------I------------------D---I---------------------E------T-Y---------S------------------S--------------------N------------D----IK-N----------G---------V-Y----K-------------------------------------YAD-----A-E-------------------------D------------------F--------------E--I-L----------L------F---------A---------Y-------S-----I---------D-G----------G-----E---------V----E---------C--L--------------------D--L--T---------R------------------------
> str02: M---------------E-----------------R-------------------------R--A--H----RT-----H----Q-------N-------------------------W--D------A-----T---------K--P-R-----E--------R-------------R----------K---Q-T------------Q-------H-R---------L-----T---------------------H--P---------------------D------------D------S-----I-----------------Y-----PR------I----------------------------E------------K-------------------AEG------R--------K------E--------------D---H----G-------
> str03: M---------------E-----P------G--------A--F-------ST-A----L---------------------------------------F----------------------D------A--L-----CD---------------D----I-L-------------------------H--------------R------R-------L----E----------S-----------------------------------------Q-----------L------------R----FG-----------G-----V-----------------Q----------I---------P------------P------E--V-----S-D--------------PR-V-Y-A-G------Y---------A--L-------L-----------
> str04: M-----------------G------------K---------F--------------------------------Y------------------Y---------S--------------------N-R-----R-----------L-------A-------------V---F----------A----------Q---A----------Q-S-------R------H--L----------G---------G-S------------Y-E--------Q---------------W------L----------------A----------C-------V---------S------G-----D--S------A--------------------F--R---------AE--V-------------K---------------A---RV------Q---KD-----
> str05: ------F----------F----------------R-----E-----N----------L-----A---------------------------------F----Q-----------Q------G-------K-----A------------R-----EF--------------------P-S-----E-----------------------------E----A-----------R----A------NS----P-T--------S--------------R-----E----L---W-----------V------R---------------------R-----G------------G-------N---P----------L--S-----E-----------------A-G--AE--R----------------------R----------G-----------T-
> str06: M--------------D------P-S-------L--T------------Q--V---------------------W-A----------------V---E-------------G-----S-----------------V---------L----S--A----------------A----------V--D----------T-A-----------------E---T---------N------------------D---T-E----P---------------------DE-G--L-S--A--E-------------N------E-G-------------------------------------------------E----------------T-----R---I---------------------------------I---R--I-----T-G----S--------
> str07: M----AF--------D-F------S-V--------T------G---N---T-----KL------D-------T-----------S---G--------F------T---------Q------G------------V--------------S--------------S-------------------------M---TVA---------------A----------G---------T-------L--------------------------I----------AD-----L--V------K----T------------A-----------------S----------S-------------------Q---------L----------T------------------N----------LA----QS-----------------------------------
> str08: M----A------V-------ILP-ST-----------Y------------T--DG-------TA-----------A-------------------------------C-------------------------T-----------N----------G-------S-----------P------D-----------V--------------V------------G---------T----G------------T-------------------M------------------W-----------V-----N--T------ILP------G-------DF------------F--------------------W-------------T----P-S----------G---E---SV--------------------R------V-----------------
> str09: MN-----------------------T---GI------------I---------D---L---------------------------------------F----------------------D---N----------------H--------V--D----------S-------I---P--T-------I-L-P-----H---------Q--------L--A-------------T-------L-----D---------------Y------L------V---------------------R-T----I-----------I-------D----------------------------------------E-N--------------------RS------------V---------L----L------FHI--M-----------G----SG-------
> str10: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V----------N------------L--R-T---------------------RT----Q--------L------------P-------------------P--------------A-------------Y----------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--------------------S--------
> str11: M--------------D--------S------K--------E---------T----I-L---------------------I-------E-I--------------------------------I--------P-----------K--------------IK----S---Y-----L--------------L-----------------------D----T---------N----------I----S----P------K---S--Y--------N-------D-F-I---S----------R--------N-------------------KN--------I----------F----V-------------IN---L-------Y---------------------NV-----S-----------T-----I----------------------------
> str12: M--------L-----------L--S----G-K------------K-----------K-M---------L-----------L-----D----N-Y--E-------T-A------------A-------A----R-------G-------R-------G--------------G-----------DE----------------R------R--------R-----G----------W-AF---------D-----------R-------------P-----A----I----V-----------T-----K-R----------------D-K---S--D------R--------------M--------A----------------------------------------H-------------------------------------------------
> str13: MN----------------G---------E-----------E------------D----------D----N-------E-----Q-A--------A-----------A-E-----Q----------Q-------T---------K---------------K---------A---K---R------E---K--P------K--------Q----A----R--------K------------------V-----T--------S----E-------------A----------W---EH--------F---------------------D-------A---------T---D-------D----G----AE------------------------C-------------------------K--------H-----------------------------
> str14: M---------------E-------S-------L---V----------P------G------------------------------------------F--N-------E--K---------------------T-------H--------V-----------Q-----------L---S----------L-P---V---L-------Q--V------R-----------------------------D----V----L----V------------R-------G--------------------FG--------------------D-----SV---------------------------------E----E----V----------L--S---------E---A---R----------Q------H--L-----K---D--G-----------T-
> str15: M-R----------Y------I-----V----------------------S---------P-----------------------Q------L-V------L--Q--V----GK---------G---Q--E-----V---E---------R---A-------L-------Y-----L----T-----------P-------------------Y-D---------------------Y---I-------D-----E--K---S------------P----------I------------------Y--------------------Y-----------F---L-RS-------H-L----N---------I---------------------------QR----------P------------------------------------------------
> str16: M---------------------P-----------R-V----------P---V----------------------Y-D-------S----------------PQ--V----------S--------------P-------------N-------------------TV---------P---------------Q---A----R---L------A-----T----------P--S----F--------A----T------P--T----F--------R-------G-------A-D--------------------A-----P-------------A-F----Q------D----------------TA--N--------------------------Q-----------------------Q-------------A---R-------Q----------
> str17: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V----------N------------L--R-T---------------------RT----Q--------L------------P-----------L----A----------------Y-------------------------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--------------------S--------
> str18: M-----F-----V----F-----------------------F---------V-----L----------L-P---------L-----------V----------S------------S--------Q----------C-------------V----------N------------L----T--------------T------RT----Q--------L------------P-------------------P--------------A-------------Y----------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--------------------S--------
> str19: M---------------E----------A--I------------I-----S-----------------------------------------------F--------A---G-----------I-----------------G-I--N----------------------Y----K--------------KL--QS----KL-------Q-------H-------------------------------D------------------FG-------R-V--------L---------K-----------------A----L--TV--------------------T--A----------------R-A------L-P---G----------------Q-----------P---------K--------HI-----AI--R-------Q----------
> str20: M----A------------------S------------------------S----G----P-----E-----R---A-EH----Q-----I--------------------------------IL-------P------E----------S-------H--L---S-------------S------------P-------L----------V---------------K----------------------------HKL------------L-------Y------------------------Y---------W--------------K-----------L---T-----G--L--------P----------L-P--D---E---------CD--------------------------------F-------------D---HL------I----
> str21: M---------------E-------S-------L---V----------P------G------------------------------------------F--N-------E--K---------------------T-------H--------V-----------Q-----------L---S----------L-P---V---L-------Q--V------R-----------------------------D----V----L----V------------R-------G--------------------FG--------------------D-----SV---------------------------------E----E----V----------L--S---------E--V----R----------Q------H--L-----K---D--G-----------T-
> str22: M--------L----A-------P-S--------P------------N--S------K----------------------I---Q------L------F--N-----------------------N-----------------I--N------------I------------------------D---I------------------N----Y--EH--T--------L-------Y-F--------A---S-V-------S---A---------Q------------NS---------------F-----------F-----------------A------Q---W--------V----------------------V---Y---------S--------A---------------D-K---------------AI---------------------
> str23: M--S-A--------------I----T--E------T--------K--P--T----I---------E--L-P----A----L----A-EG--------F----Q------------R--Y-----N----K---T------------P---------G-------------F--------T--C------------V---L-------------D---R-----------------Y-----------D-------H-----------G---------V------I--N-----D------S------K----------I----V----------------L-----Y-----------N--------------------------------------------------------------------------------------------------
> str24: M-------K-N---------I------AE------------F--K-----------K------A------P------E--L----A-E-----------------------K-----------L------L-------E-----------V----F--------S----------N-------------L--------K-----G-N--S-------R--------------S--------L-----D-P---------------------M---R---A---G-K---------H------------------------------D------V--------------------V----------------------V----------------I------E--------S-----------T------K------KL-------------------
> str25: M---------------------PQ---------P-----------L----------K--------------------------QS-----L----D------QS-------K-----W-----L--R-E------A--E----K-------------H--L--R-----A----L---------E--------S-----L----------V--D------------------S----------N-------------L-------E---------------E------------E-KL---------K------------PQ------------------L--S-------------M---G-----E----------D------V----------Q-------------S----------------------------------------------
> str26: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V----------N------------L------------I------T------RT----Q-S-Y------T---------N---S----F-------------T-------R-------G---------VY------------------------Y----------------P-----D-K----V--F-----RS---------------S-----------------V----------L------------------H--S-----------T-----------------------Q----D-----
> str27: M-------K--------F---------------------D-----------V-----L---S------L----------------------------F--------A------P---W-A---------K----V--DE--------Q------E-------------Y--------------D--------Q--------------Q--------L-----------N--------------N----------------------------N-------------L-------E-----S-----I----T--A-----P-------K-------F-----------D-------D----G----A-----------------T-E-------I------E--------S--------------E------R----------G-------DI----
> str28: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V----------N--------F--------T--------------------------N-R---------T-----------Q----------L-------PS-------------A-------------Y----------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--------------------S--------
> str29: M---W-------------------S-----I------------I-------V-----L---------KL----------I----S----I------------Q----------P---------L------L-------------L-----V--------------T------------S----------L-P-------L-----------Y----------------NP-------------N---------------------------M--------D-------S---C--------------------------------C--------------L-----------I------S----R---I---------------T----P-----------E------------LA-GKL--TW----I-------------F---------I----
> str30: M---------------E-------S-------L---V----------P------G------------------------------------------F--N-------E--K---------------------T-------H--------V-----------Q-----------L---S----------L-P---V---L-------Q--V------R-----------------------------D----V----L----V------------R-------G--------------------FG--------------------D-----SV---------------------------------E----E--------------FL--S---------E---A---R----------Q------H--L-----K---D--G-----------T-
> str31: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V---------------------------------------MP-------L---F--N---------L--------I-------T-----------------T---------T------------Q-S-Y----------------------T------N-------F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--L--------------------------
> str32: M------H---Q--------I----TV---------V------------S----G----P--T--E--------------------------V----------ST--C-FG-----S------L-----------------H----P--------F------Q-S---------L-------------K--P---V----M-----------A---------------N-------A----L------G---V----L-------E-G-K-M----------F---------C-------S-----I----------G---------G---RS-------L--------------------------------------------------------------------------------------------------------------------
> str33: M----A-------------------T------L------------L--------------RS------L------A----L----------------F-------------K---R--------N----K-------D-----K--P-----------------------------P----------I------T--------------S-------------G--------S-----G---------G---------------A---I------R-------GIK---------H----------I-----------I-------------------I---------------V-------P-----I------P---G-------------D----------------S----------S------I----T-------T-----RS-----R--
> str34: M---------------E-------S-------L---V----------P------G------------------------------------------F--N-------E--K---------------------T-------H--------V-----------Q-----------L---S----------L-P---V---L-------Q--V------R-----------------------------D----V----L----V------------R-------G--------------------FG--------------------D-----S------------------------M---------E----E----V----------L--S---------E---A---R----------Q------H--L-----K---D--G-----------T-
> str35: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V----------N------------L----T--------------T---------G-------------T-----------Q----------L-------P--------P-----A-------------Y----------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--------------------S--------
> str36: M----A----N---------I---------I---------------N----------L---------------W-------N------GI--V--------P----------M---------------------V------------Q-----D------------V--------N----VA-----------S-------------------------------I-------T--AF--K---S--------------------------M------------I--------DE------T-----------W------------D-K----------K------------I--------------E---A--N---------T-------C-I---------------S---------------------R---K-------H--R-----N---
> str37: M--------LN-----------------------R--------I----Q-T------LM--------K----T--A-----N---------N-Y--E-------T-----------------I-----E-------------I-L---R------------N------Y-----L--R-----------L---------------------Y-------------I-------------I-L----A------------R------------N--------E------------E----------G---R-------GIL------------------I-------Y-D-------D-N---------I---------D------------S------------V----------------------------------------------------
> str38: M----A---------D------P----A-G-----T----------N-------G----------E-----------E----------G---------------T-----G-------------------------C--------N----------G----------W--F----------------------------------------Y---------------------------------V-------E----------A------------V-----------V----E-K----------K---T-----G--------D-------A---I----S----D-------D----------E-N--E-N---D------------S-D----T---G---E---------D--L-------------------VD----------------
> str39: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V----------N------------L--R-T---------------------RT----Q--------L------------P-------------------PS------------Y-------------------------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H--------------------S--------
> str40: M---------------E-------S-------L---V----------P------G------------------------------------------F--N-------E--K---------------------T-------H--------V-----------Q-----------L---S----------L-P---V---L-------Q--V---------C--------------------------D----V----L----V------------R-------G--------------------FG--------------------D-----SV---------------------------------E----E----V----------L--S---------E---A---R----------Q------H--L-----K---D--G-----------T-
> str41: MN--------NQ----------------------R---------K-----------K-----TA-------R----------P-S------------F--N-----------M----------L-----K--R--A------------R------------N-R--V-----------STV------------S-------------Q--------L--A------K----R-----F------S-----------K----------G--L---------------L-S----------------G---------------Q-----G--P--------------------------M----------------------K-------L---------------V--------------------------M--A-------F--------------
> str42: M--S------N------F---------------------D------------A--I----R--A----L-----------------------V--D--------T---------------D------A----------------------------------------Y----KL----------GHI---------H--M----------Y-----------------P-----------------------EG------T---E------------Y----------V-------L--S-------N-------F-----T---D----R-----G-----S--------------------R---I---E------G-----V------------T--------H--------------T----------------V----H------------
> str43: M-------------------I-------E---L-R-------------------------------H----------E--------------V---------Q-------G---------D--L----------V------------------------------T------I--N----V--------------V------------------E---T----------P-----------------------E--------------------------D-----L------D-----------G----------F--------------R---DF-I---R----A---H-L--------------I-----------------------C--L----A---V-----------D-----T--E-------T-------T-G-L-----DI---Y
> str44: M-----F-----V----F---L----V-----L------------L-P---------L----------------------------------V----------S------------S--------Q----------C-------------V---------------------------------------MP-------L---F--N---------L--------I-------T-----------------T--------------------N-Q-S-Y----------------------T------N-S-----F-----T--------R-----G----------------VY----Y-P---------------D-K----V-F--RS------------------SV--L------------H-----------------------------
> str45: M--S----K------D-----L----VA------R-------------Q---A----LM---TA-------R----------------------------------------M----------------K-----A-D-F----------V----F--------------F---L----------------------------F------V-----L-----------------W-----K-----A----------L--S---------L--P---V--------------------P--T-------R---------------C---------------Q----------I---DM--------A-------------K-------------------------------------KL-S------------A--------G-------------
> str46: M----A------------------S-------L------------L----------K----S------L---T-------L----------------F-------------K---R-----------------T--------------R----D--------Q-------------P--------------P-------L------------A-------------------S-----G-----S---G-----G---------A---I------R-------GIK---------H------V---I-----------I----V----------------L-----------I---------P----------------G-------------D----------------S----------S------I----------V-T-----RS-----R--
> str47: M-R---------V---------------------R-------GI-L--------------R--------N---W---------Q------------------Q--------------W---------------------------------W------I--------W-----------T-------------S-----L----G-----------------F-----------W-------M-----------------------F----M------------I-------C-------S-V---------V----G-----------N----------L----W--------V----------T-----------V---Y-----------------Y--G-V---P--VW-----K------E--------A-K----T-------------T-
> str48: M----A------V---E-----P------------------F-----P------------R----------R----------P------I--------------T----------R---------------P---------H----------A-----------S-------I-----------E----------V-----------------D----T-------------S-----GI--------G-----G-----S---A--G--------S-----------S-----E-K-----V-F--------------------C--------------L-----------I--------G-Q--AE-----------G---G--E--P-------------N------------------T----------------V-----------------
> str49: M-----F------YA----H-------A-------------FG-----------G-------------------Y-DE---N--------L-------H-------A--F---P-------GI--------------------------S--------------STV--A-----N-------D-----------V-----R------------------------K--------Y--------SV------V-------S-VY--------N------------K----------K------Y----N---------I----V----KN---------K------Y----------M------------W--------------------------------------------------------------------------------------
> str50: M----A----N--Y----------S------K-P-------F---L-----------L------D--------------I------------V----F--N----------K--------D-I------K------C-----I--N-------D----------S-----------------C----------S---H-----------S---D------C----------R---Y--------------------------------------Q-S----------NS--------------Y--------V--E---L-----------R----------R---------------N----Q--A------LN-----K----------------------N----------L------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 457
> best bound: 0.0
> best submodel bound: 0.0
> wall time: 68.25s
> ```
