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
>  Sol: utlcikgnycosjiqefovkuaohmzppglnbxrddxbcsvrvnnhstuqgxzpvxissbxf
> str1: -t---kgn-----------ku--hm-p-----x----------n-h-t-qgxz-vxis----
> str2: ----i-----o-jiq-fo-----------lnbx---x-c-v-----s-uq---pv-issbxf
> str3: u-lci--nycos-----ov---o--zpp-l-----------------------p--------
> str4: ----i-g--------e--v--a---z--g--b-rdd-bcsvrvnn-----g----------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 1.361842s
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
>  Sol: tiojikqfpegypolrnbdxzwxqevkrdurlchpmqazvgtdpfjuitvbxnyerczohdsdbtmcosbvrouqgxzpvxissbnrngplxwfbhdep
> str1: t----k----g-----n---------k--u---h-m-------p-------xn------h----t---------qgxz-vxis----------------
> str2: -ioji-qf-----ol-nb-x--x---------c------v---------------------s-----------uq---pv-issb------x-f-----
> str3: -----------------------------u-lc--------------i----ny--c-o--s-----o--v-o----zp----------pl-------p
> str4: -i--------g-------------ev-----------az-g---------b----r----d-db--c-s-vr-------v-----n-ng----f-----
> str5: --------p--yp-lr----z-x------u--c-pmq--vgtd-f-ui-v------c---ds-b---o-------------------------------
> str6: --------p--------bd-----ev--d---c------v--dpf------------z---s---m--sb-ro-q----v----b---------bh---
> str7: ---------e------nb--------------c-----z-----fj--tv-x--er-z-----b-------r-------v-i------gpl------e-
> str8: ---------------r---x-wxq--krd-rlc--------t----------------o-d---tm------------p-------r--p-xw---d--
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 99
> best bound: 56.0
> wall time: 60.841571s
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
>   Sol: pyplriosxtkqjgeuniwazsbdxqkuefvodlcqnpafzgbhrvfjmdiptxqvgrxlqneeycvjfuzsehtiwurodqkzabvmnctesfozmbpukrvgiadrhskjvoqxzcupgwvdspnrhznbbcxvliwdhepsmgfoy
> str01: ---------tk--g--n---------ku---------------h----m--p-x-------n-----------ht------q---------------------g-----------xz-----v-----------x--i-----s-----
> str02: -----io-----j----i-------q---f-o-l--n-----b----------x----x------cv----s-----u---q----------------p---v-i----s--------------s------b--x-----------f--
> str03: ---------------u-----------------lc---------------i----------n--yc-------------o------------s-o-------v----------o--z--p-----p----------l-----p------
> str04: -----i-------ge---------------v-------a-zgb-r----d------------------------------d----b---c--s---------v----r----v-------------n---n--------------gf--
> str05: pyplr---------------z---x--u------c--p----------m-----qvg-----------------t-----d------------f-----u----i-------v----c-----ds------b---------------o-
> str06: p---------------------bd----e-v-d-c----------v---d-p----------------f-zs---------------m----s----b---r-----------oq-------v--------bb-------h--------
> str07: --------------e-n-----b-----------c-----z-----fj----t--v--x---e---------------r----z-b---------------rv-i---------------g----p----------l----e-------
> str08: ----r---x---------w-----xqk-----------------r----d-------r-l-----c--------t----od---------t-----m-p--r-----------------p--------------x---wd---------
> str09: ----------k---------------k--------q--af----------i-----g---q------j--------w--o--k-----------------k--------sk----------------r---b----l--------g---
> str10: ---l----x---------------x------------pa---b-------i----v-----------------------------bv--------z----k------------o--z------------z-----v---d---------
> str11: ----------k---------------------------------r-----i-----------------f--s------------a-v-nc----------------d-------q------w------hz---c---------------
> str12: -----------q-------a----x--u----d--------g------------qv----q----c------e---w--------b-------f---------gi------j-o-------w----------------w---------y
> str13: ----r--sx--qj---n------------f-------pa----------di------------------u-s---i-----q---b-----e---z------------h-k--o--------------h---------------mg---
> str14: -----i------------w--s---------------------h-v---------------------------h---------------c----o-m-------i-------------u---vd---------------d----m----
> str15: -------------------------------------------h--------tx----x-q------j--z----------q---b---ct------b-------a----k---------------n----------------------
> str16: --------x------u-----s-------f----c----fz----------p----------ee-cv---------w-------a---n-t--f--m------g----------q-z-u------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 149
> best bound: 49.0
> wall time: 60.856061s
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
>   Sol: bbaeddcbeacdeecbdbeacbdcaed
> str01: ----d-cb--c---c-db--c--c-e-
> str02: b---dd-be---ee----e--bd----
> str03: ------c--acdeec---e--b---e-
> str04: --aedd-----d----d-e--bd---d
> str05: --a---cbe---e-c----a-b-c-e-
> str06: bba----be------bd---cb--a--
> str07: bbae-----a--e--b---a--d-a--
> str08: ---e----e---eecbdbe------e-
> str09: ------c---cdee--d--a--dc--d
> str10: b---d----a-----bdbea----a-d
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 27.0
> wall time: 5.195178s
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
>   Sol: dacebdaecbdeabcedacbeadbceabdacebd
> str01: d-c-b---c-----c-d--b----c-----ce--
> str02: ----bd----d--b-e----e----e-----ebd
> str03: --c---a-c-de---e--c-e--b-e--------
> str04: -a-e-d----d-----d-----d--e-bd----d
> str05: -ac-b--e---e--c--a-b----ce--------
> str06: ----b----b--ab-e---b--d-c--b-a----
> str07: ----b----b--a--e-a--e--b--a-da----
> str08: ---e---e---e---e--cb--db-e-----e--
> str09: --c-----c-de---eda----d-c---d-----
> str10: ----bda--bd--b-e-a---ad-----------
> str11: ---e-d-e--d-a----a---a---ea--a----
> str12: -a----ae----a----a-be----ea---c---
> str13: ---e--a-----abc--ac-----c---d---b-
> str14: ----bd-e---ea---d---ead--e--------
> str15: --c---ae--d-a---d---e----e-----e-d
> str16: ---eb---c---a---d--b-a-b---b---e--
> str17: d----d--c--e---e-a-b--d--ea-------
> str18: da--b---c-d-----d---ea---e----c---
> str19: -a----a---d---ce----e-d---a--a--b-
> str20: -a-e---ec-----ce----e----ea--a----
> str21: ----b----bd-a--e--c--a----a-d--e--
> str22: dace-dae--d-ab--------------------
> str23: -a----ae----ab-----b---b---b--ce--
> str24: d--e-d---b----c----b----c-a--a--b-
> str25: d---bda-----a--e---b---bc--b------
> str26: d--eb--e--d--b-e---b-a--c---------
> str27: --ce---e-b----c-d-cb--d--e--------
> str28: d---b--e--d-a----a----d---a--a--b-
> str29: --c-----c-----c-d-cbe--b----d-c---
> str30: -a-e---e----a-c-d--b----c--bd-----
> str31: dac-b--e----a-c---c-----c---d-----
> str32: ---e----c--e-bc---c---db----d---b-
> str33: d----d---b---bceda-b---b----------
> str34: -a----ae----ab---a---a---e-b-a----
> str35: ---e----cb---bc--a---ad-c---d-----
> str36: d--eb---c-----ce--c---dbc---------
> str37: da----a-cb--a--e----e--bc---------
> str38: -a---da--b-ea----ac-----ce--------
> str39: da-e----c-d--b---ac--a----a-------
> str40: dac-b----bd---ced-c---------------
> str41: d--e-d---b-e---e---b---b----d--e--
> str42: --c--da---d---c-d-c---d---a--a----
> str43: --ce---e--d---c----b-a---e-----e-d
> str44: --ce--aec---a----a---a--c-a-------
> str45: d-c-----c-----ce---b---b---b-a---d
> str46: ----b-ae---ea--e---b---b----d--e--
> str47: d---bd-e-b--a-c---c---db----------
> str48: ---eb---cb-e---eda--ea------------
> str49: -a-e---e---e-b-----b--dbc-a-------
> str50: d---bda--b----ce--cb---b----------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 24.0
> wall time: 62.094253s
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
>   Sol: TACTAGCCGTAGATCAGATCGTAC
> str01: -A-T-G--G--GAT-A---CG---
> str02: -A-TA-CC-T---TC----C---C
> str03: --C-A-C-G-A-AT----T-G-A-
> str04: TA--A-----A-ATC---T-GT--
> str05: -A---G--GTA-A-CA-A----A-
> str06: T--T--CC-TAG----G-T---A-
> str07: T--T-G---TAGATC---T-----
> str08: T----G--G--GA--AG-T--T-C
> str09: T--T--CC--A---CA-A-C-T--
> str10: T-CTA-----A-A-C-GA----A-
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 24.0
> wall time: 0.476453s
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
>   Sol: ATCGACGTAGTAACGATCATGCATGCTATCAGCTGACGTATGCAGTCACTAGCGTAACTGCTAACGTACAGTCACTACGATGCAGCTATGCATGCTAGACTGCTACGATGCTAGCTAGCATCGACTCGATGCR
> str01: -T--A-GTAGTA--GA-C-T-C---C-----G--GA---A-G---T-----G---A-C----AA---AC---C-CT--GA---A---A---A-G--A-A-TG----GAT---A---A--AT--A-T--A----
> str02: ---G--G-A-TAA--A-CA--C-T-C---C--C-GA---A---A---A-TA----A--T--T----T---G--ACT----T--A---A---A--C-A-AC-GC---GA--C-AG-T----TC-A----A-G--
> str03: AT--AC-------C--T--T-C---CTA---G--G---TA---A--CA--A----A-C--C-AAC---CA---ACT----T-----T-TG-AT-CT---CT--T--G-T---AG--A---TC---T-G-----
> str04: -T--A---A--A----T--T--AT---A--A--T--C-T-T--A-T-ACTAG--TAA-----AA---A-A-T-A----G--G--G-T--G--T---A-AC--C---GA----A---A--A-CG----G-T-C-
> str05: -T-----TA--AA--A-CA-GC---CT----G-TG--G---G---T---T-GC--A-C--C---C--AC--TCAC-A-G--G--GC----C---C-A--CTG----G--GC--GC-A--A--G----------
> str06: AT-GAC-T--T--C---CA---ATG------G---A--T---C---C-C-A----A-C--CT--C--A-AG-C--T----T-C--C-A--C---C----C--C-A--ATG---G-T----T----TC-A-GC-
> str07: A---AC--A--AAC---CA---A--C---CA----AC-T-T----T---T-G---A--T-CT--C-T----T------G-T--AG--AT-C-TG-T----T-CT-C--T---A---A--A-CGA----A--C-
> str08: AT-GA---A--AACGA--A---A----AT----T-A--T-T--A-TCA--AG-G-----G-TA---T---G-------GA---AG-T--G---G--A-A--GCT--GA--C--G--A--A---A-T-------
> str09: A-C----T-----CG-----GC-TGC-AT--GCT----TA-G---T-----GC--A-CT-C-A-CG--CAGT-A-TA--AT-----TA---AT---A-ACT---A--AT--TA--------------------
> str10: -T-----T-GTA--GATC-TG--T--T--C---T--C-TA---A---AC--G---AACT--T----TA-A---A--A---T-C---T--G--TG-T-G---GCT--G-T-C-A-CT--C--------------
> str11: ---G-C--AG-A--G--CAT---T--T-TC---T-A---AT--A-TC-C-A-C--AA-----AA--T---G--A--A-G--GCA---AT--A----A---T--T--G-T---A-CTA-C-TC-----------
> str12: AT-GA-G------C---CA---A-G--ATC--C-GACG-A---AG--A---GC----C--C---C--A-AG-------GA-G--G--A-G-A----AG---G--A-G--G---G--A-C--C--C-C----C-
> str13: -TC----T-----C-A-CA-G--T--T--CA----A-G-A---A--C-C---C--AA-----A--GTAC---C-C--C----C--C-AT--A-GC----C--CT-C--T--TA---A--A--G-C-C-A--C-
> str14: A--G--GT--T-----T-AT--A--C---C---T----T---C---C--TAG-GTAAC----AA---AC---CA--AC----CA---A--C-T--T----T-C---GAT-CT--CT----T-G--T--A----
> str15: A--G--GT--T-----T-AT--A--C---C---T----T---C---C-C-AG-GTAAC----AA---AC---CA--AC----CA---A--C-T--T----T-C---GAT-CT--CT----T-G--T--A----
> str16: -T--A---A--AAC-A--A--C-T-C-A--A--T-AC--A---A--CA-TA----A---G--AA---A-A-TCA--ACG---CA---A---A----A-AC----AC--T-C-A-C-A--A---A---------
> str17: --C--CG------C---C---CAT--T-T--G--G--G----C-G------GC-T--CT-C----G-A--G-C-----GAT--AGCT---C--G-T---C-G--A--AT-C---C---C-TCGAC-C--T---
> str18: AT--AC-------C--T--T-C---C---CAG--G---TA---A--CA--A----A-C--C-AAC---CA---ACT----T-----T---C--G--A---T-CT-C--T--T-G-TAG-ATC---T-G-----
> str19: -TC----T-----C-A-CA-G--T--T--CA----A-G-A---A--C-CT--C--AA--G-T--C-T-C---C-C--C----CA--TA-G---GC----CT-CT----T--T--C-AG--TC-A---G-----
> str20: ---GA--T-----C--TC-T-C-T-C-A-C--C-GA---A--C---C--T-G-G---C--C---C---C-G-------G--GCA---A---ATGC----C--CTA--AT-C---C-AG-A--G----G-TG--
> str21: A--GA-G------C-A--AT-CA-G-T----GC--A--T---CAG--A--A----A--T---A---TAC---C--TA---T-----TAT--A--C-A--CT--T----TGCTA---AG-A---A-T-------
> str22: A---A--T--TAA--A--A--CAT-CT--CA----A--TA--CA---AC-A---TAA--G--AA---A-A---AC-A--A--C-GC-A---A----A-A-----AC-A--CT--C-A---T------------
> str23: A---A---A----CGA--A--C-T--T-T-A----A---A---A-TC--T-G--T----G-T---G----G-C--T--G-T-CA-CT---C--G---G-CTGC-A---TGCT---TAG--T-G-C--------
> str24: AT--A---A----C--T-A---AT--TA-C---TG---T---C-GT---T-G---A-C----A--G----G--AC-ACGA-G----TA---A--CT---C-G-T-C--T---A--T--C-T----TC--TG--
> str25: AT-GA-GT-GT--C-A-C--G-A----AT----T--C--A--C-GT-AC-A----A--TG--AAC-T---G-------GATG----T-T-CA--C--G--TG----GA----A--TA--A-------------
> str26: A-C--CGT-G----G-----GC--G--A---GC-G--GT--G-A--C-C--G-GT----G-T--C-T----TC-CTA-G-TG--G----G--T-C----C--C-ACG-T--T-G--A--A------------R
> str27: A---A---AG----G-T--T---T---AT-A-C---C-T-T-C---C-C-AG-GTAAC----AA---AC---CA--AC----CA---A--C-T--T----T-C---GAT-CT--CT----T-G----------
> str28: A--G---TAGT-----TC--GC---CT----G-TG---T--G-AG-C--T-G---A-C----AA---AC--T---TA-G-T--AG-T--G--T--T----TG-T--GA-G---G--A---T----T--A----
> str29: -T-----T--TA----T-A--C---CT-TC--CT-A-G---G---T-A--A-C--AA-----A-C---CA---AC--C-A---A-CT-T---T-C--GA-T-CT-C--T--T-G-TAG-AT------------
> str30: AT-G-CG--GT--CG-TC-T-C-T-C---C--C---CG---GC--T---T----T---T--T----T----TC-C--C----C-GC---GC---C--G-C-G-T----TG---GC--GC--CGA---------
> str31: ---G---T-G-A-C-A--A---A----A--A-C--A--TA---A-T-----G-G-A-CT-C---C--A-A--CAC--C-ATG----T---CA----AG-CT--T----T-C-AG---G--T--A---GA--C-
> str32: ---G---T-GTAA-GA--A---A--C-A---G-T-A---A-GC---C-C--G-G-AA--G-T---G----GT------G-T-----T-T---TGC--GA-T--T----T-C--G--AG----G-C-CG--G--
> str33: ---GA-G-A--A----T---G-A-G-T--C---T--C--AT----T-AC---CG---C--C---CG----GT-ACT----T--AGC-A---A-GCTA-A-T---A-G-T-C-A-C--G----G-C--------
> str34: AT-G---T-G----G-TC--G-ATGC---CA--TG--G-A-G--G-C-C---C--A-C--C-A--GT----TCA-T----T--A---A-G---GCT---C--CT--G--GC-A--T----T------------
> str35: A-CGA-G------CG-T--T---T--TA--AG--G--G----C---C-C--GCG-A-CTGC----G-AC-G-------G---C--C-A--CATG---G-C--C--C--TG-TA--T-G--T------------
> str36: ---G--GT--T-----T-AT--A--C---C---T----T---C---C-C-AG-GTAAC----AA---AC---CA--AC----CA---A--C-T--T----T-C---GAT-CT--CT----T-G--T--A-G--
> str37: -T-G--G--G-AA-G-T--T-C---C-A--A----A---A-G-A-TCAC-A----AA-----A-C--AC--T-AC--C-A-G----T---CA----A--C--CT--GA----AG-TA-CA-C-----------
> str38: ---GA---AG---CG-T--T--A----A-C-G-TG---T-TG-AG------G---AA-----AA-G-ACAG-C--T----T--AG----G-A-G--A-AC----A--A-G--AGCT-G----G----G-----
> str39: A-C--C--AG---CG--CA--C-T--T--C-G--G-C--A-GC-G------GC--A---GC-A-C---C--TC-----G--GCAGC-A--C---CT---C----A-G---C-AGC-A--A-C-----------
> str40: AT-G--G--G-A-C-A--A--C-T--TAT----T--C-----C--T-A-T--C--A--TG-T---G--C---CA--A-GA-G--G-T-T---T--TA--C--C--CG--G-T-G--A-C--C-A---------
> str41: -T-----T-GTA--GATC-TG--T--T--C---T--C-TA---A---AC--G---AACT--T----TA-A---A--A---T-C---T--G--TG-T-G---G-T----TG-T--C-A-C-TC-----------
> str42: A---AC-------C-A--A--C---C-A--A-CT----T-T-C-G--A-T--C-T--CT--T---GTA--G--A-T-C--TG----T-T-C-T-CTA-A-----ACGA----A-CT----T----T--A----
> str43: ---G--G--GT-----TC-TGC---C-A---G--G-C--AT--AGTC--T----T---T--T----T----T---T-C--TG--GC---G---GC----C--CT----TG-T-G-TA--A---AC-C--TG--
> str44: ---G--G------C--T---GCATGCT-T-AG-TG-C--A--C--TCAC--GC--A---G-TA---TA-A-T---TA--AT--A---A--C-T---A-A-T--TAC--TG-T---------------------
> str45: -T-G-C--A-T---G--C-T---T---A---G-TG-C--A--C--TCAC--GC--A---G-TA---TA-A-T---TA--AT--A---A--C-T---A-A-T--TAC--TG-T--C--G--T------------
> str46: -T-----T-----C---CA--CA----A-C---T----T-T-C---CAC---C--AA--GCT--C-T---G-CA--A-GAT-C--C----CA-G--AG--T-C-A-G--G---G---GC--C---T-G-T---
> str47: -TC----TA--AACGA--A--C-T--T-T-A----A---A---A-TC--T-G--T----G-T---G----G-C--T--G-T-CA-CT---C--G---G-CTGC-A---TGCT---TAG---------------
> str48: A-C--CG--G-A----T---G---GC---C-GC-GA--T-T----T---T----T--C-G-----G-A--GTC-CT----TG--G----G---G---GAC--C-AC--T-C-AG--A--AT--A---GA----
> str49: --C----T--T---G-T-A-G-AT-CT----G-T----T---C--TC--TA----AAC-G--AAC-T----T---TA--A---A---AT-C-TG-T-G--TG----G---CT-G-T--CA-C---T-------
> str50: AT-GA-G------C-A-C-T--A----A---GC-GA---A-G-A---AC---C--AA-----AA---A--G-CA----GA--CA---AT--A--C-A-AC--C--CG---CTA--T----T--AC--------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 133
> best bound: 84.0
> wall time: 61.153306s
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
>   Sol: MPQAESLKFTRSLENYQAHFDVAINSRCPGVFKGTANEGLHDYQ
> str01: M--A--L----S---Y-----------CP---KGT---------
> str02: M-Q--S-----SL-N--A-----I----P-V-------------
> str03: MP----L----S---YQ-HF------R-----K-----------
> str04: M---E--------E----H--V--N------------E-LHD--
> str05: M----S--------N----FD-AI--R--------A---L----
> str06: M-------F-R---N-Q-------NSR---------N-G-----
> str07: M-------F------Y-AH---A--------F-G----G---Y-
> str08: M----S-KFTR---------------R-P-------------YQ
> str09: M----S--F------------VA------GV---TA-------Q
> str10: M---ESL--------------V------PG-F----NE------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 29.0
> wall time: 60.985707s
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
> --- Solution (of length 489) ---
>   Sol: MLFWNGPKAIERSDVFPFRLEYSGKADNIHLIVDTGYALQDPNELFRIDSKGKTVLIPNHEFAWPMQRIGYLVDTNRSLQGDAWEIKGAFTNPAHDSAELTEQIVNSKEMDWGYIWCHFALDQENKTSAAGPRLSCMVKITNDLEAEFKQMSDGEWRPIKGHDYQAICLETKPSVINHFALPDEVTIRSLEPKNGFTLIYAQHRSADGVCWYMITPLEFSGAKNDHSMYEQAHLWADIGVTTDCFPKRAVNDSLAYCPQTAKEFGKSNDVARTMLNWKYPIGHARTLDVEFRGSKCNATDAMVISGHLCFEARPQEITFYWNVKGLSHDARISLVNFRKDICFAEGPMHEWGSYKFITVRPDNLAYGSPLDCREKYIHPDGVLFSATREDNGKVYMQWIPDAGNVRTQRYFECMLSGDLIVSATKEPWYDAMNFHRGCVKESQIQTLSVANFPRDHGILYRSTKMADGNQHRVTLDKVIQSFPLWYTGR
> str01: M----------R-----------------HL-----------N----ID-------I---E-------------T--------------------------------------Y-------------S------S------ND---------------IK----------------N-----------------G-------------V--Y----------K-----Y--A----D-----------A-------------E-----D---------------------F-------------------E-----I--------L-------L--F------A---------Y-------------S--------I--DG----------G-------------------E--------V----E-----------C--------L-------D---L---T--------R-----------------
> str02: M---------ER------R------A---H----------------R------T-----H------Q--------N-------W-----------D-A--T------K-----------------------PR-----------E-----------R------------------------------R----K--------Q------------T---------------Q-H--------------R-----L-----T----------------------H------------------------------P--------------D----------D------------S---I--------Y--P---R---I-----------E---K--------A---------E----G------------------R---KE-------------DHG--------------------------------
> str03: M---------E-----P------G-A-------------------F---S---T--------A--------L-----------------F-----D-A-L----------------C----D--------------------D---------------I---------L--------H---------R---------------R------------LE-S----------Q--L-------------R---------------FG----------------G------V-------------------------Q-I-----------------------------P-------------P------------E-------V--S----D---------P-----R--------------V-------Y-A-----G----------------------Y-----A--------L--------L-----
> str04: M----G-K-------F-----Y--------------Y------------S--------N--------R--------R-L---A---------------------V-------------FA--Q-----A--------------------Q-S----R----H------L-------------------------G------------G-----------S--------YEQ---W------------------LA-C------------V-----------------------S-----------G----------------------D---S----------A-----------F---R----A--------E-------V----------K--------A---R--------------V---------------------Q--------------------K--D----------------------
> str05: --F------------F--R-E------N--L------A-------F--------------------Q------------QG-----K-A-------------------------------------------R-----------E--F---------P---------------S---------E------E---------A--R-A-----------------N--S------------------P-------------T------S----R-----------------E-----------------L------------W-V-------R------R-------G-----G----------N-----PL--------------S---E------------AG-------------------A--E---------R-----------------R--G-----T--------------------------
> str06: M------------D--P-----S-------L---T----Q--------------V--------W------------------A---------------------V---E---G--------------S---------V-----L-------S-------------A-------------A----V---------------------D-------T------A-------E----------T---------ND-------T--E----------------P-------D-E--G--------------L------------------S--A--------------E-----------------N----------E------G-------E-----------------T-R----------I-----------------------I---------R---I----T----G------------S--------
> str07: M-------A------F----------D------------------F---S----V-------------------T-----G----------N--------T------K------------LD----TS--G----------------F----------------------T------------------------------Q-----GV----------S------SM------------T--------V----A-----A---G-------T-L-----I--A---D-------------------L--------------VK---------------------------------T------A--S----------------S-----------Q-----------------L--------T--------N-------------L--A-------------------Q----------S--------
> str08: M-------A-----V-------------I-L----------P-------S---T----------------Y---T------D-----G--T--A---A------------------C---------T--------------N-----------G-------------------S-------PD-V-----------------------V-----------G-------------------T-----------------------G-------TM--W-----------V-------N-T----I---L-----P----------G---D-------F-----F-------W------T--P------S------------G-------E--------------------------S----V--------------R--V--------------------------------------------------
> str09: M---N-----------------------------TG-----------I--------I----------------D----L----------F-----D---------N-----------H-------------------V----D--------S------I-------------P------------TI--L-P----------H---------------------------Q--L-A----T------------L--------------D---------Y-------L-V--R------T----I------------I-----------D---------------E-----------------N---------R-----------S--------V--------------------L---L--------------FH--------I--------------------M--G------------S------G-
> str10: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-L------------R-------------T----------------R--------T----Q--------------L----------------------------P-----------P--A-----------------Y------T----------N-------S----F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---------S--------
> str11: M------------D--------S-K------------------E---------T--I--------------L-------------I------------E----I----------I----------------P------KI--------K--S-----------Y----L-----------L-D--T-------N----I-----S----------P------K---S-Y---------------------ND-----------F----------------I------------S------------------R--------N-K-----------N----I-F---------------V-----------------I-------------N-----------------------L-------------Y---N-----V--S---T-----------I-------------------------------
> str12: ML-----------------L--SGK-------------------------K-K------------M-----L------L--D---------N---------------------Y---------E--T-AA---------------A----------R---G--------------------------R------G------------G----------------D----E-----------------R-----------------------R------------R-------G---------------------------W--------A------F--D-------------------RP---A-----------I----V----T-----K------------R-----------D------K----------------S------------D-----R---MA----H------------------
> str13: M---NG----E---------E-----D------D--------NE----------------------Q---------------A-----A----A----E---Q-------------------Q---T-----------K---------K----------------A-----K---------------R--E-K----------------------P------K-------QA---------------R-------------K-------V--T--------------------S----------------EA--------W-----------------------E---H------F-----D--A---------------------T--D----------D-G-------------------A--E-----------C-K---------------H---------------------------------
> str14: M---------E-S------L------------V--------P---------G---------F-------------N--------E-K---T---H---------V-----------------Q----------LS--------L-------------P----------------V-----L--------------------Q------V--------------------------------------R---D-----------------V----L-------------V--RG----------------F--------------G---D---S-V---------E----E--------V----L---S-----E-----------A-R--------Q-------------------------------------H-----------L----------------K--DG-----T---------------
> str15: M----------R---------Y------I---V----------------S-------P--------Q----LV-----LQ------------------------V-------G------------K----G------------------Q----E-------------------V--------E---R------------A---------------L-----------Y----L------T----P---------Y------------D---------Y-I------D-E----K---------S--------P--I--Y---------------------------------Y-F-------L--------R-----------S-------------------------------------------------H-----------L---N------I-----------Q-R----------P------
> str16: M-----P----R--V-P---------------V---Y---D--------S-------P--------Q-----V----S--------------P------------N--------------------T----------V-------------------P------QA---------------------R-L----------A-------------TP---S------------------------F---A----------T-------------------P-----T----FRG----A-DA------------P---------------A------F-----------------------------------------------------------Q---D-----T---------------A---------N---------Q-Q----A---R---------------Q-------------------
> str17: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-L------------R-------------T----------------R--------T----Q--------------L----------------------------P-------LAY---T-------N-------------------------S---------------F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---------S--------
> str18: M-F-----------VF-F--------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-L--------------------------T--------------T-R--------T----Q--------------L----------------------------P-----------P--A-----------------Y------T----------N-------S----F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---------S--------
> str19: M---------E--------------A--I--I-----------------S-----------FA------G---------------I-G---------------I-N-------Y-----------K------------K----L-----Q-S-------K--------L--------------------------------QH---D-----------F-G--------------------------R-V---L-------K--------A---L----------T--V---------T-A-----------R----------------A---L------------P----G--------------------------------------------Q--P------------------------K---------H--------I-----A-------I--R--------Q-------------------
> str20: M-------A---S---------SG-----------------P-E--R---------------A---------------------E---------H-------QI----------I-----L----------P------------E------S---------H------L----S--------------S--P-----L----------V-------------K--H--------------------K------L--------------------L---Y----------------------------------------YW--K-L-------------------------------T--------G--L--------P---L----------------PD----------EC----D---------------F--------------------DH--L-------------------I----------
> str21: M---------E-S------L------------V--------P---------G---------F-------------N--------E-K---T---H---------V-----------------Q----------LS--------L-------------P----------------V-----L--------------------Q------V--------------------------------------R---D-----------------V----L-------------V--RG----------------F--------------G---D---S-V---------E----E--------V----L---S-----E-------V-----R--------Q-------------------------------------H-----------L----------------K--DG-----T---------------
> str22: ML------A-------P-----S------------------PN------SK-----I---------Q----L-----------------F-N-------------N--------I---------N--------------I--D---------------I-----------------N----------------------Y-----------------E-------H--------------T------------L-Y-------F------A----------------------S--------V-S------A--Q------N----S---------F-----FA----------------------------------------------------QW------V---------------V-------Y------------S-------A----D--------K-A------------I----------
> str23: M-----------S------------A--I-----T--------E---------T--------------------------------K-----P-------T--I----E-----------L----------P-------------A----------------------L----------A---E----------GF-----Q-R-------Y-----------N----------------------K------------T-------------------P-G--------F-------T---------C-------------V--L--D-R----------------------Y-------D---------------H--GV----------------I----N-------------D---S--K------------------I----V---------LY--------N--------------------
> str24: M------K-------------------NI--------A-----E-F----K-K---------A-P-------------------E--------------L-------------------A---E-K-------L---------LE-----------------------------V---F---------S----N---L------------------------K---------------G-----------N-S------------------R---------------------S-------------L--------------------D-----------------PM-----------R----A-G-------K--H-D-V-----------V----------V--------------I-----E---------------S---T-----------------K------------K------L-----
> str25: M-----P--------------------------------Q-P--L-----K---------------Q----------SL--D--------------------Q---SK---W--------L-----------R-----------EAE-K------------H------L------------------R------------A---------------LE-S-------------L-----V--D---------S--------------N------L--------------E--------------------E----E-------K-L------------K-------P-------------------------------------------------Q-----------------LS---------------M----G---E-------------D-----------------V------QS--------
> str26: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-L--------------I-----------T----------------R--------T----Q--S------Y--T--------N--S-----------------F--------------T-----------R---------G------V------------------------------Y---------------------------------Y------PD------------K------V-F---R---------------------------S-----S----------------V-------L--------H-----ST------Q-----D-------------
> str27: M------K-------F----------D-----V-----L----------S-----L-----FA-P------------------W----A------------------K-----------------------------V----D-E----Q----E--------Y------------------D------------------Q----------------------------Q--L----------------N----------------N-------N----------L--E---S---------I-------------T-----------A----------------P-------KF-----D--------D---------G----AT-E---------I------------E---S---------E---------RG-----------------D--I-------------------------------
> str28: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-----F----------------------T-----N----------R--------T----Q--------------L----------------------------P------S-AY---T-------N-------------------------S---------------F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---------S--------
> str29: M--W--------S---------------I--IV-----L-----------K----LI--------------------S-------I----------------Q----------------------------P-L---------L------------------------L-----V----------T--SL-P-----L-Y-----------------------N---------------------P----N----------------------M-------------D-----S-C------------C----------------L-----IS----R--I----------------T--P------------E--------L--A-----GK---------------------L--------T---W---------------I-------F-----I-------------------------------
> str30: M---------E-S------L------------V--------P---------G---------F-------------N--------E-K---T---H---------V-----------------Q----------LS--------L-------------P----------------V-----L--------------------Q------V--------------------------------------R---D-----------------V----L-------------V--RG----------------F--------------G---D---S-V---------E----E-----F-------L---S-----E-----------A-R--------Q-------------------------------------H-----------L----------------K--DG-----T---------------
> str31: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V------------M------P----------L---------F--------------N---LI---------------T-------------------------TT----------------Q-------S-----------Y------T----------N------------F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---L--------------
> str32: M----------------------------H---------Q-------I-----TV-----------------V----S--G-----------P-------TE--V-S-------------------T--------C-----------F-----G-------------------S------L---------------------H------------P--F-----------Q---------------------SL-------K-----------------P--------V------------M---------A---------N-------A---L-----------G------------V----L---------E------G-----------K--M--------------F-C--S---I----------------G-------------------G---RS------------L--------------
> str33: M-------A-------------------------T---L-----L-R--S-----L------A--------L-----------------F-----------------K------------------------R--------N------K---D------K------------P--------P----I---------T-------S--G-----------SG-----------------G---------A-------------------------------I---R-------G----------I-------------------K---H---I--------I---------------I-V-P---------------I-P-G--------D-------------------------S-----S---------------------I-T----------------T--------R--------S-------R
> str34: M---------E-S------L------------V--------P---------G---------F-------------N--------E-K---T---H---------V-----------------Q----------LS--------L-------------P----------------V-----L--------------------Q------V--------------------------------------R---D-----------------V----L-------------V--RG----------------F--------------G---D---S--------------M-E-----------------------E-------VL-S---E------------A---R-Q--------------------------H-----------L----------------K--DG-----T---------------
> str35: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-L--------------------------T--------------T--------G-T----Q--------------L----------------------------P-----------P--A-----------------Y------T----------N-------S----F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---------S--------
> str36: M-------A------------------NI--I----------N-L------------------W-----------N----G----I------------------V--------------------------P----MV-----------Q--D---------------------V-N-------V---------------A---S--------IT------A----------------------F-K-----S--------------------M------I------D-E--------T---------------------W-------D---------K---------------K-I----------------E-----------A----N---------------T-----C------I-S-------------R---K---------------H----R-------N--------------------
> str37: ML--N------R----------------I----------Q-------------T-L---------M--------------------K---T--A-----------N------------------N--------------------------------------Y-----ET----I-------E--I--L-------------R-------------------N----Y----L-------------R-----L-Y------------------------I----------------------I---L---AR--------N----------------------E----E-G-------R------G---------I-----L---------------I----------Y-------D-----------D--N----------I----------D------S----------V----------------
> str38: M-------A----D--P--------A---------G-----------------T----N----------G--------------E-------------E-------------G-------------T---G----C-----N-----------G-W----------------------F--------------------Y--------V--------E---A-----------------V---------V------------E--K-----------K-------T------G------DA--IS-----------------------D----------D----E-----------------N----------E----------------N---------D--------------S-D-----T------------G---E-------------D---L-------------V--D-------------
> str39: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V---N-L------------R-------------T----------------R--------T----Q--------------L----------------------------P-----------P--------S-----------Y------T----------N-------S----F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H---------S--------
> str40: M---------E-S------L------------V--------P---------G---------F-------------N--------E-K---T---H---------V-----------------Q----------LS--------L-------------P----------------V-----L--------------------Q------VC--------------D--------------V-------------L---------------V-R---------G--------F-G------D----S-----------------V---------------------E----E--------V----L---S-----E-----------A-R--------Q-------------------------------------H-----------L----------------K--DG-----T---------------
> str41: M---N----------------------N-----------Q------R---K-KT--------A----R------------------------P---S---------------------F-----N-----------M------L----K-------R--------A---------------------R-----N---------R----V----------S--------------------T--------V--S-----Q---------------L--------A----------K-----------------R-----F-------S-----------K------G-----------------L-----L--------------S------G----Q-----G-----------------------P----M-------K------L-V---------------MA---------------F-------
> str42: M-----------S--------------N-----------------F--D-------------A-----I-------R-----A----------------L----V-----D---------------T---------------D--A-----------------Y-------K--------L-------------G-------H----------I-----------H-MY----------------P----------------E-G-------T----------------E-----------------------------Y--V--LS--------NF--------------------T---D----------R-------G---S--R----------I------------E----G---V--T----------H----------T--V------H---------------------------------
> str43: M--------IE--------L--------------------------R------------HE-----------V------QGD-----------------L----V---------------------T------------I-N--------------------------------V---------V-----E-----T------------------P-E------D--------L--D-G-----F--R---D-----------F----------------I---R------------A--------HL--------I------------------------C---------------------LA----------------V-------D----------------T----E-----------T---------------------T----------G-L-------D-----------I------Y---
> str44: M-F-----------VF---L------------V-----L-----L------------P-------------LV----S------------------S-----Q-------------C--------------------V------------M------P----------L---------F--------------N---LI---------------T-------------------------T---------N-------Q-------S-----------Y------T----------N-------S----F-------T------------R--------------G------------V------Y---------Y--PD------------KV----------------F------------------------R-----S-----SV---------L-----------H------------------
> str45: M-----------S-----------K-D---L-V----A--------R-------------------Q---------------A----------------L---------M----------------T-A---R---M-K------A------D-------------------------F-----V----------F----------------------F--------------L----------F----V---L----------------------WK-----A--L------S-------------L-----P--------V-----------------------P----------T-R-----------C------------------------Q-I-D------------M--------A-K--------------K------LS-A------G--------------------------------
> str46: M-------A---S------L----------L-------------------K--------------------------SL-----------T--------L------------------F------K------R-------T---------------R-----D-Q-------P--------P-------L----------A---S--G-----------SG-----------------G---------A-------------------------------I---R-------G----------I-------------------K---H------V-----I---------------I-V----L------------I-P-G--------D-------------------------S-----S---------------------I----V-------------T--------R--------S-------R
> str47: M----------R--V---R----G----I-L---------------R-----------N----W--Q------------Q---W---------------------------W--IW----------TS-----L-------------------G------------------------F-------------------------------W-M-----F--------M---------I-----C--------S----------------V------------------V---G---N----------L------------W-V----------------------------------TV------Y---------Y----GV-----------------P----V----------------------W-----------KE--------A-------------K---------T------------T--
> str48: M-------A-----V-----E--------------------P---F-----------P---------R--------R---------------P----------I----------------------T-----R------------------------P---H---A-------S-I-------EV---------------------D-------T----SG----------------IG-------------------------G-S---A----------G-----------S----------S-----E------------K----------V-F----C---------------------L------------I---G---------------Q----A---------E----G-------------------G---E-----------P---------------N----T---V-----------
> str49: M-F------------------Y---A---H-------A-------F-----G-----------------GY--D----------E------N-------L-----------------H-A---------------------------F---------P--G-----I------S--------------S-------T-----------V------------A-ND--------------V-------R-------------K----------------Y--------------S--------V-------------------V---S-------V------------------Y--------N-----------K-----------------K-Y--------N---------------IV---K-------N------K-------------------Y----M-------------------W----
> str50: M-------A------------------N--------Y------------SK------P---F---------L------L--D---I------------------V-------------F-----NK----------------D---------------IK-------C-------IN-----D-----S--------------------C---------S-----HS---------D------C---R-------Y--Q-------SN-------------------------S-------------------------Y--V---------------------E------------------L--------R--------------R--N-----Q----A------------L-----------------N------K----------N-------L------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 489
> best bound: 93.0
> wall time: 60.959994s
> ```
