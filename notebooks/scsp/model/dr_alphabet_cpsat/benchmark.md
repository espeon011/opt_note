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
Model = scsp.model.dr_alphabet_cpsat.Model
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
>  Sol: tuklcignycoejsikoquvafozphmpxlnhtqgbrxdxdbcvzsuvqxprvinsnsbgxf
> str1: t-k---gn-------k--u------hmpx-nhtqg--x------z--v-x---i-s------
> str2: -----i----o-j-i--q---fo------ln----b-x-x--cv-su-q-p-vi-s-sb-xf
> str3: -u-lci-nyco--s--o--v--ozp--p-l--------------------p-----------
> str4: -----ig----e-------va--z----------gbr-d-dbc--s-v---rv-n-n--g-f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 0.0
> best submodel bound: 62.0
> wall time: 14.197525s
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
> --- Solution (of length 102) ---
>  Sol: iorxjwxgipqyefoptvaklrzgnbdekruvxdhlmpuxcinvdhptfmqvyzbcgostdfjotvxemorszbpruoqipvxinbnswcdgpsblpxefho
> str1: ----------------t--k---gn---k-u---h-mp-x--n--h-t--q-----g---------x-----z--------vxi---s--------------
> str2: io--j---i-q--fo-----l---nb------x------xc--v--------------s-----------------u-q-pv-i---s-----sb--x-f--
> str3: ------------------------------u----l----cin---------y--c-os----o-v---o--z-p-----p--------------lp-----
> str4: i------g----e----va---zg-b---r---d----------d---------bc--s------v----r----------v--n-n----g-------f--
> str5: ---------p-y---p----lrz---------x-----u-c-----p--mqv----g--tdf--------------u--i-v-------cd--sb------o
> str6: ---------p---------------bde---v-d------c--vd-p-f----z----s---------m--s-b-r-oq--v---b--------b-----h-
> str7: ------------e-----------nb--------------c------------z-------fj-tvxe--r-zb-r-----v-i-------gp--l--e---
> str8: --rx-wx---q--------k-r----d--r-----l----c------t---------o--d---t---m-----pr----p-x-----w-d-----------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 102
> best bound: 0.0
> best submodel bound: 75.0
> wall time: 60.50907s
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
> --- Solution (of length 143) ---
>   Sol: iohjkrtikpqxaswxyfgopuelnqsvabcdjkrzeivxdgnuxbcfpradhlmqvbcfgijtuzdfpsuvxeiqwybcefhorsvzbcdoprvwaiknoshkmstzbfkmnpqrgijopqxzuvwbdbdhlmwxefgipsy
> str01: ------t-k---------g-----n--------k---------u--------h-m-------------p---x--------------------------n--h---t-------q-g-----xz-v---------x---i-s-
> str02: io-j---i--q------f-o---ln----b---------x----x-c---------v------------su----q----------------p-v--i---s---s--b-------------x--------------f-----
> str03: ---------------------u-l------c------i----n----------------------------------y-c---o-s-----o--v-----o------z-----p------p-----------l-------p--
> str04: i-----------------g---e----va------z-----g---b---r-d--------------d-----------bc-----sv------rv----n------------n---g--------------------f-----
> str05: ---------p------y---p--l----------rz---x---u--c-p-----mqv---g--t--df--u---i-----------v--cd----------s------b----------o-----------------------
> str06: ---------p-------------------b-d----e-v-d-----c---------v---------d-p------------f-----z-------------s--ms--b------r---o-q---v-b-b-h-----------
> str07: ----------------------e-n----bc----z-----------f--------------jt-------vxe----------r--zb----rv--i------------------g---p-----------l---e------
> str08: -----r-----x--wx---------q-------kr-----d--------r---l----c----t-------------------o------d---------------t----m-p-r----p-x---w-d--------------
> str09: ----k---k-q-a----f-------------------i---g-------------q------j-------------w------o--------------k----k-s----k----r-----------b----l-----g----
> str10: -----------------------l---------------x----x---p-a------b---i---------v------b-------vz----------k-o------z---------------z-v--d--------------
> str11: ----kr-i---------f--------s-a---------v---n---c----d---q--------------------w-----h----z-c-----------------------------------------------------
> str12: ----------q-a--x-----u---------d---------g-------------qv------------------q---ce--------------w------------bf------gijo------w-------w-------y
> str13: -----r-------s-x---------q------j---------n----fp-ad---------i--u----s----iq--b-e------z--------------hk---------------o-----------h-m----g----
> str14: i-------------w-----------s-------------------------h---v-------------------------h------c-o------------m------------i------uv--d-d--m---------
> str15: --h---t----x---x---------q------j--z-------------------q-bc----t--------------b-----------------a-kn-------------------------------------------
> str16: -----------x---------u----s--------------------f----------cf-----z--p----e------e--------c----vwa--n------t--f-m----g----q-zu------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 143
> best bound: 0.0
> best submodel bound: 82.0
> wall time: 60.791699s
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
>   Sol: abedcdebeacdeabcebdbceabdacde
> str01: ---dc--b--c----c--dbc-----c-e
> str02: -b-d-d-be---e---e----e-bd----
> str03: ----c----acde---e---ce-b----e
> str04: a-ed-d-----d------d--e-bd--d-
> str05: a---c--be---e--c------ab--c-e
> str06: -b-----b-a----b-ebd-c--b-a---
> str07: -b-----b-a--ea--eb----a-da---
> str08: --e---e-e---e--c-bdb-e------e
> str09: ----c-----cde---e-d---a-d-cd-
> str10: -b-d-----a----b---db-ea--a-d-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 29
> best bound: 0.0
> best submodel bound: 29.0
> wall time: 0.188104s
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
> best submodel bound: 34.0
> wall time: 1.043105s
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
>   Sol: TACGTACGCGTAATCGATACGTAC
> str01: -A--T--G-G-----GATACG---
> str02: -A--TAC-C-T--TC----C---C
> str03: --C--ACG---AAT---T--G-A-
> str04: TA---A-----AATC--T--GT--
> str05: -A-G---G--TAA-C-A-A---A-
> str06: T---T-C-C-TA---G----GTA-
> str07: T---T--G--TA---GAT-C-T--
> str08: T--G---G-G-AA--G-T---T-C
> str09: T---T-C-C--A--C-A-AC-T--
> str10: T-C-TA-----AA-CGA-A-----
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 0.0
> best submodel bound: 24.0
> wall time: 0.185407s
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
> example file name: 'nucleotide_n050k050.txt'
> best objective: 136
> best bound: 0.0
> best submodel bound: 38.0
> wall time: 62.585195s
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
> --- Solution (of length 46) ---
>   Sol: MQSENPSAFLRSVYCNPQADEGHKVAFGNSTEIRALNRGHKPVYDQ
> str01: M------A-L-S-YC-P------K---G--T---------------
> str02: MQS---S--L-----N--A-------------I--------PV---
> str03: M----P---L-S-Y---Q----H---F------R------K-----
> str04: M--E----------------E-H-V---N--E---L---H----D-
> str05: M-S-N---F----------D-----A------IRAL----------
> str06: M-------F-R----N-Q----------NS---R--N-G-------
> str07: M-------F----Y----A---H--AFG----------G----Y--
> str08: M-S--------------------K--F---T--R---R---P-Y-Q
> str09: M-S-----F---V-----A--G--V-----T---A----------Q
> str10: M--E--S--L--V---P----G----F-N--E--------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 46
> best bound: 0.0
> best submodel bound: 46.0
> wall time: 2.172262s
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
> --- Solution (of length 438) ---
>   Sol: MDEFLNPQRSWAGHIKPSVEFILNPSTVYGIKPQRYDEFLSVAGHIKLNPRTADEFGKLNRTVWYAFMNQSVIKLSFGHIPQRTACDILPTVWFGKLNRWYADEGIKNQSTVWYEGIKLNPRSTADEGHIMQTVACDFKLNPQRSVACEGIMNPRSTYDEHKLQSTVWYACDEFGHIKLPQRSTHMNVYAFKLNPQSVWYDEFGIKLMRSTVYADEFKNPQRVGLMNPTVWYCDEGIKLPSYAHIKMNQRTVACDEFGLRSVYACIKRSTVCDFGHLPQADEIKLNSTVADKLPRWDFSVYEKNSTYAEGKMNVWCEFHIKLQRYDFHIPRCDGLMSTVEGILNPQRSAEGIKLNPQVYADGHLSTWYDEGKMNSVAIKLPRTVWYCDFGHIKLMNQSVAEFGIRSYADEHRSTVGLCKMQTVWADGHKRSTILNPRY
> str01: M-------R----H--------LN------I-----D--------I--------E------T--Y-----S----S---------------------N----D--IKN-------G-----------------V-----------------------Y---K------YA-D-----------------A-----------E------------D-F-----------------E-I-L-------------------L--------------F-----A--------------------Y---S--------------I-----D-------G------G--------E-------V-----------E----------------C------L--------------D-------L----T-------R--------
> str02: M-E-----R-------------------------R-------A-H-----RT--------------------------H--Q---------------N-W--D---------------------A-------T-----K--P-R----E-----R--------------------------R---------K---Q--------------T---------Q----------------------H-----R--------L----------T-----H-P--D---------D-------S--------------------I----Y----PR----------I-------E--K------A---------EG----------R----------K-------E-------D-H----G----------------------
> str03: M-E---P-----G-----------------------------A------------F--------------S------------TA---L----F--------D---------------------A--------------L-------C----------D------------D----I-L-----H-----------------------R------------R--L---------E-----S-------Q---------LR-------------FG----------------------------------G---V--------Q-----IP--------------P----E-------V------S---D-----------PR-V-Y-------------A--G---YA--------L----------------L----
> str04: M-----------G--K----F-------Y------Y----S-------N-R---------R-------------L---------A------V-F-------A------Q---------------A------Q------------S---------R-----H-L-----------G----------------------------G-----S--Y--E----Q---------W-------L---A----------C-------V------S-----G-----D-----S--A-------F-------------------------R------------------------AE-------V-------------K----A----R-V------------Q---------------------K------D------------
> str05: ---F----------------F-------------R--E----------N---------L------AF--Q-----------Q------------GK-----A-------------------R----E----------F---P--S---E----------E---------A-----------R-------A---N--S----------------------P--------T-----------S--------R-----E--L------------------------------------W---V-----------------------R------R--G------G--NP--------L----------S----E------A------------G---------AE---R------R---G-----T----------------
> str06: MD----P--S------------L---T------Q-------V---------------------W-A-----V-------------------------------EG----S-V------L---S-A---------A----------V------------D------T---A--E----------T--N-------------D---------T----E---P-------------DEG--L-S-A------------E-----------------------------N---------------E-------G------E--------------------T--------R----I-------------------------I---R---------I---------------------T-G--------------S-------
> str07: M----------A--------F---------------D-F-SV---------T----G--N-T-----------KL-----------D---T------------------S-----G---------------------F------------------T------Q----------G------------V--------S------------S---------------M--TV------------A---------A----G-----------T------L-----I------AD-L------V--K--T-A----------------------------S----------S--------Q------L-T-------N-----L-------------------A--------------------Q---------S-------
> str08: M----------A------V--IL-PST-Y----------------------T-D--G----T---A------------------AC----T------N------G----S----------P----D-------V-----------V---G------T-----------------G--------T-M------------W------------V------N---------T-------I-LP-----------------G--------------DF-----------------------F----------------W----------------------T------P--S--G------------------E----SV-----R-V------------------------------------------------------
> str09: M----N--------------------T--GI--------------I-------D----L-------F-------------------D----------N------------------------------H----V--D-------S-----I--P--T-------------------I-LP----H----------Q----------L------A--------------T---------L---------------D-------Y-------------L-----------V-----R----------T-------------I--------I---D------E---N--RS---------V-----L---------------L--------F-HI--M-------G--S---------G----------------------
> str10: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V-----N--------------------L--R-T-------------------R------------T------Q--------------LP--------------P------------------A-----------------Y------------------T----------------------------------NS----------F-------T-----------------R---------G----V-------------------Y--------Y------------P------D----K-----V--F--RS------S-V-L----------H--S-------
> str11: MD-------S-----K---E------T---I--------L-----I--------E-----------------I------IP--------------K---------IK--S---Y----L--------------------L------------------D------T--------------------N-----------------I----S---------P-----------------K--SY-----N------D-F--------I--S-------------------------R--------N------K-N------I------F-----------V--I-N---------L----Y--------------N-V---------------------S---------------T------------------I-----
> str12: M---L-----------------L--S---G-K--------------K----------K---------M------L-------------L-------------D----N-----YE--------TA---------A-----------A-------R-------------------G------R---------------------G-------------------G---------DE--------------R---------R-------R------G--------------------W-----------A---------F-------D----R-------------P---A--I-----V-------T-----K---------R-----D----K----S----------D--R-------M----A--H----------
> str13: M----N------G------E-----------------E---------------D--------------------------------D----------N-----E----Q---------------A---------A-----------A-E--------------Q----------------Q--T-------K-------------K-------A---K---R------------E--K-P-----K--Q---A------R------K---V----------------T----------S--E-----A------W-E-H-------F-----D---------------A----------------T--D------------------D-G---------AE----------------CK--------H----------
> str14: M-E------S------------L----V----P----------G-----------F---N-------------------------------------------E--K---T-----------------H----V--------Q-------------------L-S-------------LP-------V----L--Q-V----------R-----D-------V-L----V-------------------R-------G---------------FG-----D-----S-V------------E------E----V-------L--------------S--E--------A--------------------------------R--------------Q-------------H-----L-K------DG----T------
> str15: M-------R-------------------Y-I----------V----------------------------S---------PQ------L--V----L-----------Q--V---G-K---------G---Q----------------E-----------------V-----E--------R-------A--L------Y------L---T--------P-----------Y-D-------Y--I---------DE----------K-S--------P----I-----------------Y-----Y----------F---L-R------------S-------------------------HL---------N---I------------------Q-------R------------------------------P--
> str16: M-----P-R---------V-----P--VY-------D---S--------P-------------------Q-V---S----P----------------N------------TV--------P----------Q--A--------R------------------L------A-------------T----------P-S-----F----------A--------------T----------P----------T-----F--R--------------G----AD--------A---P-------------A---------F----Q--D-----------T----------A-----N-Q---------------------------------------Q--A----R---------------Q-----------------
> str17: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V-----N--------------------L--R-T-------------------R------------T------Q--------------LP------------L--------------------A-----------------Y------------------T----------------------------------NS----------F-------T-----------------R---------G----V-------------------Y--------Y------------P------D----K-----V--F--RS------S-V-L----------H--S-------
> str18: M--F--------------V-F-----------------F--V-----L----------L---------------------P-------L--V-----------------S------------S--------Q---C---------V------N---------L--T-----------------T------------------------R-T---------Q---L--P-----------P--A-------------------Y------T---------------NS----------F-------T-----------------R---------G----V-------------------Y--------Y------------P------D----K-----V--F--RS------S-V-L----------H--S-------
> str19: M-E--------A--I------I---S------------F---AG-I----------G---------------I------------------------N--Y-----K----------KL------------Q------------S----------------KLQ-----------H------------------------D-FG----R--V------------L------------K----A---------------L----------TV----------------T-A----R------------A-------------L-------P---G-----------Q---------P---------------K------------------HI-------A---IR---------------Q-----------------
> str20: M----------A-----S-------S---G--P----E------------R-A-E-----------------------H--Q-----I-----------------I------------L-P-----E-----------------S---------------H-L-S-----------------S-----------P-----------L----V-----K-------------------------H-K------------L-----------------L-----------------------Y-----Y-------W-----KL---------------T--G-L-P--------L-P----D--------E----------------CDF-------------------D-H-----L---------------I-----
> str21: M-E------S------------L----V----P----------G-----------F---N-------------------------------------------E--K---T-----------------H----V--------Q-------------------L-S-------------LP-------V----L--Q-V----------R-----D-------V-L----V-------------------R-------G---------------FG-----D-----S-V------------E------E----V-------L--------------S--E-----------------V-----------------------R--------------Q-------------H-----L-K------DG----T------
> str22: M---L------A----PS------P-----------------------N---------------------S--K-----I-Q------L----F---N---------N--------I--N---------I------D-------------I-N----Y-EH----T------------L---------Y-F----------------------A--------------------------S----------V--------S--A--------------Q------NS----------F-------------------F------------------------------A-------Q---------W--------V-------V-Y-----------S-A--------D---------K-----A-------I-----
> str23: M--------S-A--I-----------T----------E-------------T-----K----------------------P--T---I---------------E--------------L-P---A--------------L------A-EG-----------------------F------QR------Y----N-----------K----T--------P---G--------------------------------F------------T-C----------------V---L---D--------------------------RYD-H-----G----V--I-N----------------D---S------K-----I-----V---------L------------Y---------------------------N---
> str24: M--------------K-------N------I-----------A-----------EF-K---------------K----------A----P-------------E--------------L-----A-E-----------KL----------------------L---------E--------------V--F-----S---------------------N-----L------------K-------------------G---------------------------NS-------R---S----------------------L---D---P-----M----------R-A-G-K---------H-----D------V-------V--------------V----I-----E--ST----K---------K----L----
> str25: M-----PQ--------P-----L--------K-Q------S------L-----D---------------QS--K------------------W---L-R----E--------------------A-E-----------K---------------------H-L------------------R-------A--L--------E-------S--------------L----V---D------S------N----------L----------------------E-------------------E------E-K----------L------------------------------K--PQ------LS-------M----------------G----------E-------D-----V-----Q---------S-------
> str26: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V-----N--------------------L----------I--T----------R------------T------QS---Y--------------T--N---------S-----F-------T----------R-G-----V-Y---------Y-----------------------------------P--D--K----V--------F-------------------------R------------S----------S---------V-----L--------------------------H------S---------------T------Q----D------------
> str27: M--------------K----F---------------D----V-----L----------------------S---L-F-------A----P--W--------A----K----V-------------DE----Q----------------E--------YD----Q----------------Q-----------LN------------------------N-------N-----------L----------------E----S----I---T---------A-------------P--------K--------------F-------D------DG--------------A----------------T---E-------I----------------------E----S---E-R---G---------D------I-----
> str28: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V-----N---------------------------------------F------------------T-----------------------------N---------------------R-T---------Q---L--P------------S-A-------------------Y------T---------------NS----------F-------T-----------------R---------G----V-------------------Y--------Y------------P------D----K-----V--F--RS------S-V-L----------H--S-------
> str29: M---------W------S---I--------I----------V-----L---------KL-------------I--S---I-Q-------P------L---------------------L--------------------L-----V----------T-------S-------------LP------------L------Y------------------NP------N-------------------M-------D-----S---C------C----L-----I---S-------R------------------------I-----------------T------P----E---L-----A-G---------K-------L--T-W------I---------F-I----------------------------------
> str30: M-E------S------------L----V----P----------G-----------F---N-------------------------------------------E--K---T-----------------H----V--------Q-------------------L-S-------------LP-------V----L--Q-V----------R-----D-------V-L----V-------------------R-------G---------------FG-----D-----S-V------------E------E--------F---L--------------S--E--------A--------------------------------R--------------Q-------------H-----L-K------DG----T------
> str31: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V--------------------------------------M----------P--------------------L----------F------------N-----L-----------I-----T-----------------T---------------------T---------------------------Q-------S-------------Y----T------N----F-------------------T--------R---G------VY--------Y------------P------D----K-----V--F--RS------S-V-L----------H-----L----
> str32: M------------H-------------------Q-----------I-----T----------V--------V---S-G--P--T-------------------E-------V----------ST-----------C-F-----------G-----S------L------------H---P----------F----QS---------L----------K-P--V--M----------------A----N----A-----L---------------G-------------V---L--------E-------GKM-----F-------------C----S----I--------G----------G-------------------R---------------S------------------L---------------------
> str33: M----------A--------------T------------L-------L--R-------------------S---L---------A---L----F-K--R--------N---------K-------D------------K--P-----------P----------------------I------T------------S------G-----S-------------G-----------G------A-I----R-------G-------IK--------H------I------------------------------------I--------I---------V-----P------I---P-----G------D-----S----------------------S-----I---------T-------T-------RS-----R-
> str34: M-E------S------------L----V----P----------G-----------F---N-------------------------------------------E--K---T-----------------H----V--------Q-------------------L-S-------------LP-------V----L--Q-V----------R-----D-------V-L----V-------------------R-------G---------------FG-----D-----S------------------------M----E----------------------E-----------------V-----LS----E------A----R--------------Q-------------H-----L-K------DG----T------
> str35: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V-----N--------------------L----T--------T----------------G------T------Q--------------LP--------------P------------------A-----------------Y------------------T----------------------------------NS----------F-------T-----------------R---------G----V-------------------Y--------Y------------P------D----K-----V--F--RS------S-V-L----------H--S-------
> str36: M----------A-----------N------I--------------I--N---------L----W----N--------G-I-----------V----------------------------P---------M--V--------Q---------------D-------V-------------------NV-A------S-------I-----T--A--FK----------------------S-----M------------------I------D--------E-----T-------WD-----K-------K--------I-------------------E--------A-----N----------T--------------------C----I-----S------R-------------K--------H-R----N---
> str37: M---LN--R-----I------------------Q-----------------T------L--------M-----K---------TA------------N---------N-----YE--------T-----I------------------E-I-----------L------------------R----N-Y---L---------------R---------------L------Y----I-------I-------------L----A---R-----------------N---------------E------EG-------------R---------G-------IL--------I------Y-D-------D----N---I---------D---------SV---------------------------------------
> str38: M----------A------------------------D------------P--A---G----T------N--------G-------------------------E----------EG-------T---G-------C----N--------G-----------------W-----F--------------Y--------V---E-----------A--------V------V----E--K-------K----T------G--------------D------A--I---S---D-----D----E-N----E---N------------D----------S-----------------------D----T----G-----------------------------E-------D-------L-----V--D------------
> str39: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V-----N--------------------L--R-T-------------------R------------T------Q--------------LP--------------P-S--Y----------T-------N---------------------S---------------F------------T------------------------R--------------G---V----------Y---------------------------------Y---------------------P------D----K-----V--F--RS------S-V-L----------H--S-------
> str40: M-E------S------------L----V----P----------G-----------F---N-------------------------------------------E--K---T-----------------H----V--------Q-------------------L-S-------------LP-------V----L--Q-V----------------------------------CD-----------------V------L--V-----R------G----------------------F-----------G---------------D----------S-VE---------E-------V-----LS----E------A----R--------------Q-------------H-----L-K------DG----T------
> str41: M----N-----------------N---------QR-----------K----------K---T---A----------------R------P-------------------S---------------------------F--N----------M----------L--------------K---R-------A------------------R---------N--RV-----------------S---------TV--------S-----------------Q-----L----A-K--R--FS---K------G-----------L------------L-S---G----Q----G----P----------------M-----KL---V----------M----A-F------------------------------------
> str42: M--------S-------------N--------------F--------------D-----------A------I---------R-A---L--V----------D-------T--------------D--------A----------------------Y---KL-----------GHI-------HM--Y-----P------E-G------T----E---------------Y-------------------V------L-S------------------------N-----------F-------T-------------------D----R--G--S---------R----I-----------------EG----V------T-------H----------------------TV------------H----------
> str43: M-------------I----E--L-----------R---------H---------E-------V------Q-------G--------D-L--V------------------T-----I--N-------------V-----------V--E-------T----------------------P---------------------E------------D---------L--------D-G--------------------F--R------------DF--------I-----------R------------A----------H--L------I--C--L-------------A--------V--D----T---E------------T------------------------------T-GL--------D------I----Y
> str44: M--F--------------V-F-L----V-----------L-------L-P--------L---V-------S----S-----Q---C-----V--------------------------------------M----------P--------------------L----------F------------N-----L-----------I-----T-----------------T------------------NQ-----------S-Y------T---------------NS----------F-------T-----------------R---------G----V-------------------Y--------Y------------P------D----K-----V--F--RS------S-V-L----------H----------
> str45: M--------S-----K--------------------D--L-VA-------R------------------Q--------------A---L-----------------------------------------M-T-A--------R-------M---------K-------A-D-F-------------V--F-----------F---L---------F-----V-L-----W------K----A---------------L-S---------------LP----------V----P-----------T-----------------R-------C-------------Q-----I--------D-----------M---A-K-------------KL---S-A--G-----------------------------------
> str46: M----------A-----S----L----------------L------K-----------------------S---L--------T----L----F-K--R-----------T----------R---D-----Q---------P-----------P--------L------A------------S--------------------G-----S-------------G-----------G------A-I----R-------G-------IK--------H------------V------------------------------I--------I---------V---L--------I---P-----G------D-----S----------------------S-----I----------V------T-------RS-----R-
> str47: M-------R---------V---------------R--------G-I-L--R--------N---W-----Q-----------Q----------W------W-----I------W----------T--------------------S-----------------L-----------G---------------F-------W--------M--------F--------M----------I----------------C------SV--------V---G----------N------L--W---V-----T-------V----------Y---------------------------------Y--G-------------V----P--VW-------K-------E------A----------K--T---------T------
> str48: M----------A------VE----P-------------F----------PR---------R-------------------P------I--T-------R---------------------P-------H-----A---------S-----I--------E------V----D-----------T------------S------GI------------------G-----------G----S-A--------------G--S-------S------------E-K----V--------F-----------------C-----L------I----G-----------Q--AEG----------G-------E----------P--------------N-----------------TV-----------------------
> str49: M--F------------------------Y-------------A-H-------A--FG--------------------G----------------------Y-DE---N----------L---------H-----A--F---P-------GI----S--------STV--A----------------N-------------D----------V---------R---------------K---Y------------------SV--------V---------------S-V-----------Y--N------K---------K---Y------------------N-------I-----V-------------K-N----K------Y--------M----------------------------W--------------
> str50: M----------A-----------N----Y-----------S-----K--P-----F--L---------------L-----------DI---V-F---N--------K------------------D---I--------K--------C--I-N-----D-----S-----C-----------S-H-----------S---D-------------------------------C----------------R------------Y---------------Q-------S----------------NS-Y------V--E----L-R------R------------N-Q--A----LN----------------K-N-----L----------------------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 438
> best bound: 0.0
> best submodel bound: 26.0
> wall time: 69.392739s
> ```
