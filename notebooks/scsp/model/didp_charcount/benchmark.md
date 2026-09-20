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
>  Sol: ulctkigneykcojisovaqfozguhbpmprdlndbxxcsvrvnsnuhtqpgxzvxissbxf
> str1: ---tk-gn--k-------------uh--mp------x------n---htq-gxzvxis----
> str2: -----i------oji----qfo----------ln-bxxc-v---s-u--qp---v-issbxf
> str3: ulc--i-n-y-co--sov---oz----p-p--l-----------------p-----------
> str4: -----ig-e--------va---zg--b---rd--db--csvrvn-n-----g---------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 1.06s
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
>  Sol: ulcigenpbyrcozfxjtivwxqkrfdesovoazplgnbrdkzlxuctohdtmpbxcvsvrmqvnnghtdpfuiqgxzpvwxicsmdlsbroqvbxbhefp
> str1: -----------------t-----k------------gn---k---u---h--mp-x--------n--ht-----qgxz-v-xi-s----------------
> str2: ---i--------o---j-i---q--f---o-----l-nb-----x----------xcvs-------------u-q---pv--i-s---sb-----x---f-
> str3: ulci--n--y-co---------------sovo-zp------------------p---------------------------------l------------p
> str4: ---ige-------------v------------az--g-brd---------d---b-c-svr--vnng----f-----------------------------
> str5: -------p-y------------------------pl---r--z-xuc------p-------mqv--g-td-fui-----v---c--d-sb-o---------
> str6: -------pb-----------------de--v---------d-----c----------v-----------dpf-----z------sm--sbroqvb-bh---
> str7: -----en-b--c-zf-jt-v-x-----e-----------r--z-----------b-----r--v---------i-g--p--------l----------e--
> str8: ----------r----x----wxqkr-d------------r---l--cto-dtmp------r---------p-----x---w-----d--------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 101
> best bound: 70.0
> wall time: 60.34s
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
> --- Solution (of length 155) ---
>   Sol: krixwxqkergpbdusrlxfhvhctomjiqnfycosoevxpablivbvrzxujnckozfpadigqjwotkvkmqpcxewbvgrtdlpfgixjozwwynskuhdmpbxcvsuiqvberzcvnhotqpvbwadkinsgsbxotfphmlgqzvxiuse
> str01: ------------------------t------------------------------k-------g---------------------------------n-kuh-mp-x-------------nh-tq----------g--x---------zvxi-s-
> str02: --i----------------------o-jiq-f--o--------l---------n-------------------------b----------x---------------xcvsu-q------------pv-----i-s-sbx--f-------------
> str03: --------------u--l-----c----i-n-ycoso-v-----------------oz-p--------------p----------lp--------------------------------------------------------------------
> str04: --i-------g--------------------------ev--a-------z-------------g---------------b--r-d-----------------d--b-c-s---v--r--vn------------n-g-----f-------------
> str05: -----------p--------------------y-------p--l----rzxu--c----p------------mq------vg-td--f------------u----------i-v----c-----------d---s--b-o---------------
> str06: -----------pbd-----------------------ev----------------------d-------------c----v---d-pf-----z----s----m-----s----b-r-----o-q-vb---------b-----h-----------
> str07: --------e---------------------n-----------b-----------c--zf------j--t-v-----xe----r----------z-----------b----------r--v------------i--g------p--l--------e
> str08: -r-xwxqk-r---d--rl-----cto-----------------------------------d------t---m-p-------r---p---x---w-------d----------------------------------------------------
> str09: k------k---------------------q-----------a----------------f---igqjwo-k-k--------------------------sk----------------r----------b-----------------lg--------
> str10: -----------------lx--------------------xpab-ivbv-z-----koz-----------------------------------z--------------v---------------------d------------------------
> str11: kri----------------f---------------s-----a---v-------nc------d--q-w----------------------------------h---------------zc------------------------------------
> str12: ------q----------------------------------a--------xu---------d-gq-----v--q-c-ewb-------fgi-jo-wwy----------------------------------------------------------
> str13: -r-------------s--x----------q----------------------jn----fpadi-------------------------------------u--------s-iq-be-z---h---------k-------o---hm-g--------
> str14: --i-w----------s----hvhc-om-i----------------------u------------------v-------------d-----------------dm---------------------------------------------------
> str15: --------------------h---t--------------x----------x-------------qj---------------------------z------------------q-b---c----t---b-a-k-n---------------------
> str16: ---x----------us---f---c-------f-----------------z---------p-----------------e-------------------------------------e--cv--------wa---n------tf--m-gqz---u--
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 155
> best bound: 72.0
> wall time: 60.31s
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
>   Sol: bbaedcdabcdeeecbdbceabdcade
> str01: ----dc--bc----c-dbc----c--e
> str02: b---d-d-b--eee-----e-bd----
> str03: -----c-a-cdee-c----e-b----e
> str04: --aed-d---d-----d--e-bd--d-
> str05: --a--c--b--ee-c-----ab-c--e
> str06: bba-----b--e---bd-c--b--a--
> str07: bbae---a---e---b----a-d-a--
> str08: ---e-------eeecbdb-e------e
> str09: -----c---cdee---d---a-dc-d-
> str10: b---d--ab-d----b---ea---ad-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 27.0
> wall time: 0.04s
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
>   Sol: dacebdaecdacbdeabecabdecbadecabdeb
> str01: d-c-b---c--c-d--b-c----c---e------
> str02: ----bd---d--b-e--e----e----e--bd--
> str03: --c---a-cd----e--ec---e-b--e------
> str04: -a-e-d---d---d-------de-b-d----d--
> str05: -ac-b--e------e---cab--c---e------
> str06: ----b-------b--abe--bd-cba--------
> str07: ----b-------b--a-e-a--e-bad--a----
> str08: ---e---e------e--ec-bd--b--e----e-
> str09: --c-----cd----e--e---d---ad-c--d--
> str10: ----bda-----bd--be-a-----ad-------
> str11: ---e-d-e-da----a---a--e--a---a----
> str12: -a----ae--a----abe----e--a--c-----
> str13: ---e--a---a-b-----ca---c----c--d-b
> str14: ----bd-e------ea-----de--ade------
> str15: --c---ae-da--de--e----e---d-------
> str16: ---eb---c-a--d--b--ab---b--e------
> str17: d----d--c-----e--e-abde--a--------
> str18: da--b---cd---dea-ec---------------
> str19: -a----a--d-c--e--e---d---a---ab---
> str20: -a-e---ec--c--e--e----e--a---a----
> str21: ----b-------bd-a-eca-----ade------
> str22: dace-dae-da-b---------------------
> str23: -a----ae--a-b---b---b---b---c---e-
> str24: d--e-d------b-----c-b--c-a---ab---
> str25: d---bda---a---e-b---b--cb---------
> str26: d--eb--e-d--b-e-b--a---c----------
> str27: --ce---e----b-----c--d-cb-de------
> str28: d---b--e-da----a-----d---a---ab---
> str29: --c-----c--c-d----c-b-e-b-d-c-----
> str30: -a-e---e--ac-d--b-c-bd------------
> str31: dac-b--e--ac------c----c--d-------
> str32: ---e----c-----e-b-c----c--d---bd-b
> str33: d----d------b---b-c---e---d--ab--b
> str34: -a----ae--a-b--a---a--e-ba--------
> str35: ---e----c---b---b-ca-----ad-c--d--
> str36: d--eb---c--c--e---c--d--b---c-----
> str37: da----a-c---b--a-e----e-b---c-----
> str38: -a---da-----b-ea---a---c----c---e-
> str39: da-e----cd--b--a--ca-----a--------
> str40: dac-b-------bd----c---e---d-c-----
> str41: d--e-d------b-e--e--b---b-de------
> str42: --c--da--d-c-d----c--d---a---a----
> str43: --ce---e-d-cb--a-e----e---d-------
> str44: --ce--aec-a----a---a---c-a--------
> str45: d-c-----c--c--e-b---b---bad-------
> str46: ----b-ae------ea-e--b---b-de------
> str47: d---bd-e----b--a--c----c--d---b---
> str48: ---eb---c---b-e--e---d---a-e-a----
> str49: -a-e---e------e-b---bd--b---ca----
> str50: d---bda-----b-----c---ecb-----b---
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 30.0
> wall time: 61.84s
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
>   Sol: TCATAGGCCTGAATCGAATCGTCA
> str01: --AT-GG---GA-T--A--CG---
> str02: --ATA--CCT---TC----C--C-
> str03: -CA----C--GAAT----T-G--A
> str04: T-A-A------AATC---T-GT--
> str05: --A--GG--T-AA-C-AA-----A
> str06: T--T---CCT-A---G----GT-A
> str07: T--T-G---T-A---GA-TC-T--
> str08: T----GG---GAA--G--T--TC-
> str09: T--T---CC--A--C-AA-C-T--
> str10: TC-TA------AA-CGAA------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 24.0
> wall time: 0.05s
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
> --- Solution (of length 137) ---
>   Sol: TACTGCGATAGTACAGTACTACATCAGATCACAGTAGCATACAGTGACGATGTCACGTCAGTCACGTCTGTAAGACTGCATCAGACTCTGAGCATGCTAGCAGATCTACGATGCTACGACTGACTGCATCGATGCAR
> str01: TA--G---TAGTA--G-ACT-C--C-G------G-A--A----GTGAC-A----A----A--C-C--CTG-AA-A----A---GA-----A---TG---G-A--T--A--A----A----T-A-T--A---------
> str02: ----G-GATA--A-A---C-AC-TC----C-C-G-A--A-A-A-T-A--AT-T----T--G--AC-T-T--AA-AC---A--A--C---G--C--G--A-CAG-T-T-C-A----A-G-------------------
> str03: -A-T---A-----C----CT---TC----C----TAG------GT-A--A---CA----A---AC--C---AA--C--CA--A--CT-T-----T--T-G-A--TCT-C--T--T--G--T-A--G-ATC--TG---
> str04: TA-----A-A-T----TA-TA-ATC---T-----TA---TAC--T-A-G-T---A----A---A-------AA-A-T--A---G-----G-G--TG-TA--A---C--CGA----A--A---AC-G----G-T-C--
> str05: T--T---A-A--A-A---C-A-----G--C-C--T-G--T---G-G--G-T-T---G-CA--C-C--C---A---CT-CA-CAG-----G-GC---C---CA---CT--G--G----G-C-G-C---A---A-G---
> str06: -A-TG--A-----C--T--T-C--CA-AT----G--G-AT-C-----C-----CA----A--C-C-TC---AAG-CT---TC---C----A-C---C---C----C-A--ATG----G--T---T---TC-A-GC--
> str07: -A-----A-----CA--A--AC--CA-A-C-CA--A-C-T----T-----T-T---G--A-TC---TCT-T--G--T--A---GA-TCTG----T--T--C---TCTA--A----ACGA---AC-------------
> str08: -A-TG--A-A--A-A---C-------GA--A-A--A---T----T-A---T-T-A--TCA---A-G---G---G--T--AT--G-----GA--A-G-T-G--GA---A-G---CT--GAC-GA----A---AT----
> str09: -ACT-CG---G--C--T---------G--CA---T-GC-T----T-A-G-TG-CAC-TCA--C--G-C---A-G--T--AT-A-A-T-T-A--AT---A--A---CTA--AT--TA---------------------
> str10: T--TG---TAG-A---T-CT------G-T-----T--C-T-C--T-A--A----ACG--A---AC-T-T-TAA-A----ATC----T--G----TG-T-G--G--CT--G-T-C-AC---T--C-------------
> str11: ----GC-A--G-A--G--C-A--T----T-----T----T-C--T-A--AT---A--TC---CAC------AA-A----AT--GA-----AG---GC-A--A--T--A--AT--T--G--T-ACT--A-C--T-C--
> str12: -A-TG--A--G--C----C-A-A---GATC-C-G-A-C-----G--A--A-G--A-G-C---C-C--C---AAG---G-A---G-----GAG-A----AG--GA-----G--G----GAC---C--C--C----C--
> str13: T-CT-C-A-----CAGT--T-CA--AGA--AC-----C---CA---A--A-GT-AC--C---C-C--C-------C---AT-AG-C-C----C-T-CT------T--A--A----A-G-C---C---A-C-------
> str14: -A--G-G-T--T----TA-TAC--C---T-----T--C---C--T-A-G--GT-A----A--CA-------AA--C--CA--A--C-C--A--A--CT------T-T-CGAT-CT-C---T---TG--T--A-----
> str15: -A--G-G-T--T----TA-TAC--C---T-----T--C---C-----C-A-G----GT-A---AC------AA-AC--CA--A--C-C--A--A--CT------T-T-CGAT-CT-C---T---TG--T--A-----
> str16: TA-----A-A--ACA--ACT-CA--A--T-ACA--A-CATA-AG--A--A----A----A-TCA-------A---C-GCA--A-A-----A--A--C-A-C---TC-AC-A----A--A------------------
> str17: --C--CG------C----C--CAT----T-----T-G------G-G-CG--G-C---TC--TC--G-----A-G-C-G-AT-AG-CTC-G----T-C--G-A-ATC--C----CT-CGAC---CT------------
> str18: -A-T---A-----C----CT---TC----C-CAG--G--TA-A----C-A----A----A--C-C------AA--C--CA--A--CT-T-----T-C--G-A--TCT-C--T--T--G--T-A--G-ATC--TG---
> str19: T-CT-C-A-----CAGT--T-CA--AGA--AC-----C-T-CA---A-G-T--C---TC---C-C--C-------C---AT-AG-----G--C---CT--C---T-T----T-C-A-G--T--C---A--G------
> str20: ----G--AT----C--T-CT-C-TCA---C-C-G-A--A--C-----C--TG----G-C---C-C--C-G---G---GCA--A-A-T--G--C---C---C---T--A--AT-C--C-A--GA--G----G-TG---
> str21: -A--G--A--G--CA--A-T-CA---G-T----G---CAT-CAG--A--A----A--T-A-T-AC--CT--A----T---T-A---T---A-CA--CT------T-T--G---CTA--A--GA----AT--------
> str22: -A-----AT--TA-A--A--ACATC---TCA-A-TA-CA-ACA-T-A--A-G--A----A---A-------AA--C---A--A--C---G--CA----A--A-A---AC-A--CT-C-A-T----------------
> str23: -A-----A-A---C-G-A--AC-T----T-----TA--A-A-A-T--C--TGT---GT--G----G-CTGT----C---A-C----TC-G-GC-TGC-A-----T----G---CT-----T-A--G--T-G---C--
> str24: -A-T---A-A---C--TA--A--T----T-AC--T-G--T-C-GT-----TG--AC---AG----G-----A---C---A-C-GA----G----T---A--A---CT-CG-T-CTA----T--CT---TC--TG---
> str25: -A-TG--A--GT---GT-C-AC----GA--A---T----T-CA----CG-T---AC---A---A--T--G-AA--CTG-----GA-T--G----T--T--CA---C---G-TG----GA---A-T--A---A-----
> str26: -AC--CG-T-G----G----------G--C---G-AGC-----G-G----TG--AC--C-G----GT--GT----CT---TC---CT---AG--TG---G--G-TC--C----C-ACG--T---TG-A---A----R
> str27: -A-----A-AG----GT--T---T-A--T-AC-----C-T----T--C-----C-C---AG----GT----AA--C---A--A-AC-C--A--A--C---CA-A-CT----T--T-CGA-T--CT-C-T---TG---
> str28: -A--G---TAGT----T-C-------G--C-C--T-G--T---GTGA-G----C---T--G--AC------AA-ACT---T-AG--T---AG--TG-T------T-T--G-TG--A-G---GA-T---T--A-----
> str29: T--T----TA-TAC----CT---TC----C----TAG------GT-A--A---CA----A---AC--C---AA--C--CA--A--CT-T-----T-C--G-A--TCT-C--T--T--G--T-A--G-AT--------
> str30: -A-TGCG---GT-C-GT-CT-C-TC----C-C-----C-----G-G-C--T-T----T---T----T-T-T----C--C--C---C---G--C--GC---C-G--C---G-T--T--G---G-C-GC--CGA-----
> str31: ----G---T-G-ACA--A--A-A--A---CA---TA--AT---G-GAC--T--C-C---A---AC------A---C--CAT--G--TC--A--A-GCT------T-T-C-A-G----G--T-A--G-A-C-------
> str32: ----G---T-GTA-AG-A--A-A-CAG-T-A-AG---C---C-----CG--G--A----AGT---G---GT--G--T---T-----T-TG--C--G--A-----T-T----T-C---GA--G---GC--CG--G---
> str33: ----G--A--G-A-A-T---------GA-----GT--C-T-CA-T-----T---AC--C-G-C-C--C-G---G--T--A-C----T-T-AGCA----AGC---T--A--AT---A-G--T--C---A-CG--GC--
> str34: -A-TG---T-G----GT-C-------GAT----G---C---CA-TG--GA-G----G-C---C-C------A---C--CA---G--T-T---CAT--TA--AG------G---CT-C--CTG---GCAT---T----
> str35: -AC-G--A--G--C-GT--T---T----T-A-AG--G------G---C-----C-CG-C-G--AC-T--G-----C-G-A-C-G-----G--C---C-A-CA--T----G--GC--C--CTG--T--AT-G-T----
> str36: ----G-G-T--T----TA-TAC--C---T-----T--C---C-----C-A-G----GT-A---AC------AA-AC--CA--A--C-C--A--A--CT------T-T-CGAT-CT-C---T---TG--T--A-G---
> str37: T---G-G---G-A-AGT--T-C--CA-A--A-AG-A---T-CA----C-A----A----A---AC------A---CT--A-C---C----AG--T-C-A--A---C--C--TG--A--A--G--T--A-C-A--C--
> str38: ----G--A-AG--C-GT--TA-A-C-G-T----GT----T---G--A-G--G--A----A---A-------A-GAC---A---G-CT-T-AG---G--AG-A-A-C-A--A-G--A-G-CTG---G----G------
> str39: -AC--C-A--G--C-G--C-AC-T----TC---G--GCA----G---CG--G-CA-G-CA--C-C-TC-G---G-C---A---G-C----A-C---CT--CAG--C-A-G---C-A--AC-----------------
> str40: -A-TG-G---G-ACA--ACT---T-A--T-----T--C---C--T-A---T--CA--T--GT---G-C-------C---A--AGA----G-G--T--T------T-TAC----C--CG---G--TG-A-C----CA-
> str41: T--TG---TAG-A---T-CT------G-T-----T--C-T-C--T-A--A----ACG--A---AC-T-T-TAA-A----ATC----T--G----TG-T-G--G-T-T--G-T-C-AC---T--C-------------
> str42: -A-----A-----C----C-A-A-C----CA-A----C-T----T-----T--C--G--A-TC---TCT-T--G--T--A---GA-TCTG----T--T--C---TCTA--A----ACGA---ACT---T---T--A-
> str43: ----G-G---GT----T-CT------G--C-CAG--GCATA--GT--C--T-T----T---T----T-T-T----CTG-----G-C---G-GC---C---C---T-T--G-TG-TA--A---AC--C-T-G------
> str44: ----G-G------C--T---------G--CA---T-GC-T----T-A-G-TG-CAC-TCA--C--G-C---A-G--T--AT-A-A-T-T-A--AT---A--A---CTA--AT--TAC---TG--T------------
> str45: T---GC-AT-G--C--T--TA-----G-T----G---CA--C--T--C-A---C--G-CAGT-A--T----AA---T---T-A-A-T---A--A--CTA--A--T-TAC--TG-T-CG--T----------------
> str46: T--T-C-------CA---C-A-A-C---T-----T----T-C-----C-A---C-C---A---A-G-CT------CTGCA--AGA-TC----C---C-AG-AG-TC-A-G--G----G---G-C--C-T-G-T----
> str47: T-CT---A-A--AC-G-A--AC-T----T-----TA--A-A-A-T--C--TGT---GT--G----G-CTGT----C---A-C----TC-G-GC-TGC-A-----T----G---CT-----T-A--G-----------
> str48: -AC--CG---G-A---T---------G------G---C---C-G---CGAT-T----T---T----TC-G---GA--G--TC---CT-TG-G---G---G--GA-C--C-A--CT-C-A--GA----AT--A-G-A-
> str49: --CT----T-GTA--G-A-T-C-T--G-T-----T--C-T-C--T-A--A----ACG--A---AC-T-T-TAA-A----ATC----T--G----TG-T-G--G--CT--G-T-C-AC---T----------------
> str50: -A-TG--A--G--CA---CTA-A---G--C---G-A--A----G--A--A---C-C---A---A-------AA-A--GCA---GAC----A--AT---A-CA-A-C--C----C---G-CT-A-T---T--A--C--
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 137
> best bound: 93.0
> wall time: 60.67s
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
>   Sol: MAPQESKEHLFSYVCTRNQELHNFDASIRPKHGVTAFGLNGYEQ
> str01: MA-------L-SY-C--------------PK-G-T---------
> str02: M--Q-S-----S--------L-N--A-I-P---V----------
> str03: M-P------L-SY-----Q--H-F----R-K-------------
> str04: M---E--EH----V---N-ELH--D-------------------
> str05: M----S-----------N-----FDA-IR------A--L-----
> str06: M---------F-----RNQ---N---S-R----------NG---
> str07: M---------F-Y------------A-----H---AFG--GY--
> str08: M----SK---F----TR-----------RP-----------Y-Q
> str09: M----S----F--V-----------A------GVTA-------Q
> str10: M---ES---L---V---------------P--G---F--N--E-
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 38.0
> wall time: 61.30s
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
> --- Solution (of length 575) ---
>   Sol: MFANKDPGERSYLVFKPDETILIRAHVAFYEDSPQVSTYGPNTVPQIKGLDGTRNWEQASQWPWIWEIVLPALVSKCQSIYNVHLAFQEQQTKNDEKPTHVRRLAKTFCENDHIQIILSLPVLQVGFWSFARDVALMCDVLDNELAEKPLFSFNMTLEWAALREVDTAEKRPPIQPHLESADSPLNTIKMFNVCRGAYKLGHKVLTSLFDTNQLKPSEPSGMTGAAARCYGRTNSFGVGAAIGTYDEARSGVWIKCALPYAFQKSCIYNPDKVFDESEVMNLEGTYANQGPLWITSRHSEECASVMAKNDSCICLFWEVRKYGEDTASGLSQAIGSGHRLAKPYIRLIEQTPQHAQELSQDWAFDQRNDLAECDMQERKGTSELGADVRGEIYQHLAMFSNCKSDEFIWTAPKGSDAEDVLFSEKMANGVYAETLRTQGFAWIHDPPYVITNLDACSKDEKIPRNCYFVATWLIDGHRAREFNSCAGVDPTKGQAWLNDGRPMKITSSDEVDLFCNQMVEYASIGDESCHVTRKGEHKLNTGIMADPYRKAVLFDNIYQTGSHADRQIMLNGPVW
> str01: M--------R---------------H-----------------------L----N---------I-----------------------------D------------------I-----------------------------E-----------T-----------------------------------------Y--------S---------S----------------N-----------D-------IK-------------N--------------G--------------------V----------------Y-------------------K-Y----------A-----D-A--------E-D------------------------F------E-I------------L-------------L----FA------Y--------S----I------------DG----------G----------------------EV--------E--------C---------L------D------L------T-----R---------
> str02: M-------ER-------------RAH---------------------------R-------------------------------------T-------H--------------Q---------------------------N---------------W------D-A------------------T-K--------------------------P-----------R------------------E-R-----------------------------------------------R----------K-----------------------Q------------------T-QH------------R--L----------T-------------H----------------P---D--D---S-------------------I----Y--------------PR---------I------E----------K--A--------------E--------------G-------RK-E---------D----------------H--------G---
> str03: M-------E-------P----------------------G------------------A---------------------------F-------------------------------S------------------------------------T---A-L----------------------------F------------------D--------------A--------------------------------L-------C----D---D------------------I--------------------L----------------------HR------RL-E---------SQ---------L-------R--------------------F--------------G--------------GV-------Q----I--PP------------E--------V--------------S----DP----------R---------V---------YA--G----------------------Y--A-L----------------L-----
> str04: M------G-------K------------FY--------Y--------------------S---------------------N-------------------RRLA----------------V----F---A-------------------------------------------Q-----A-------------------------------Q---S----------R---------------------------------------------------------------------H----------------L-------G-----G-S------------Y----EQ-----------W-------LA-C--------------V-----------S-------------G-D------S---A------------F-----------------------R-----A----------E------V---K--A-----R---------V-----Q----------------K-----------D-----------------------------
> str05: -F------------F--------R------E----------N-------L--------A---------------------------FQ-Q-----------------------------------G---------------------K-----------A--RE--------------------------F------------------------PSE----------------------------EAR-------A-----------N-------S-------------P---TSR--E--------------L-W-VR------------------R----------------------------------------G----G---------------N----------P--------L-SE--A-G--AE--R---------------------------R-----------G--------------T------------------------------------------------------------------------------------
> str06: M----DP---S-L------T--------------QV-------------------W--A---------V-------------------E------------------------------------G--S----V-L---------------S-------AA---VDTAE-----------------T----N-----------------DT------EP--------------------------DE---G------L------S---------------------A------------E--------N--------E----GE-T------------R-----I--I------------------R------------------------I-----------------T---GS----------------------------------------------------------------------------------------------------------------------------------------------------------------
> str07: M-A-----------F--D----------F---S--V-T-G-NT----K-LD-T------S-----------------------------------------------------------------GF----------------------------T------------------Q--------------------G-------V--S---------S----MT--------------V-AA-GT-------------L--------I-------------------A----------------------D----L---V-K----TAS--SQ-------L----------T----------------N-LA----Q-----S-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: M-A----------V------IL-----------P--STY---T-------DGT-----A------------A----C--------------T-N-------------------------------G--S-------------------P----------------D--------------------------V----------V----------------G-TG--------T----------------------------------------------M------------W-----------V---N----------------T-------I-----L--P------------------------------------G------D-----------F-------F-WT-P--S-------------G---E-----------------------S-----------V--------R---------V---------------------------------------------------------------------------------------
> str09: M--N---------------T-------------------G------I-----------------I-----------------------------D--------L---F---D------------------------------N---------------------------------H---------------V----------------D------S------------------------I----------------P-------------------------T--------I--------------------L---------------------------P----------H-Q-L----A-----------------T--L--D-----Y--L-----------------------V---------------RT-----I------I---D-----E----N------------R-----S---V--------L---------------LF---------------H------------IM----------------GS---------G---
> str10: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-L-----------------R---T---R---------------T-------------------------QL-P--P-----A----Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H--------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M----D----S----K--ETILI-------E---------------I-----------------I-----P----K---I------------K-------------------------S------------------------------------------------------------------------------Y-L----L----DTN-----------------------------I-------S--------P----KS--YN-D--F-------------------I-SR-----------N-----------K----------------------------------------------N-----------------------I------F--------------------V----------------------I--------NL-------------Y---------------N----V------------------S------------------------T----------I--------------------------------
> str12: M-----------L--------L----------S------G-------K---------------------------K----------------K-------------------------------------------M---L---L--------------------D-------------------N-----------Y-------------------E----T-AAAR--GR----G-G------DE-R-----------------------------------------------R----------------------R--G--------------------------------------WAFD-R--------------------------------------------P----A-------------------------I-----V-T------K-----R----------D----------------K--------------S-D-----------------------R----------MA-----------------H------------
> str13: M--N---GE---------E------------D------------------D---N-EQA------------A-------------A--EQQTK---K-------AK-------------------------R-----------E---KP--------------------K----Q-----A-------------R---K----V-TS----------E------A---------------------------W----------------------E---------------------H-----------------F--------D-A-----------------------T---------D---D--------------G-----A----E----------CK----------------------------------------H-----------------------------------------------------------------------------------------------------------------------------------
> str14: M-------E-S-LV--P----------------------G----------------------------------------------F------N-EK-THV-------------Q--LSLPVLQV------RDV-L---V----------------------R--------------------------------G------------F-----------G------------------------D---S-V-----------------------E-EV--L-------------S---E--A----------------R-----------Q-----H-L-K------------------D------------------GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M--------R-Y--------I-----V-----SPQ--------------L------------------VL-------Q----V------------------------------------------G---------------------K-----------------------------------------------G----------------Q----E-------------------V--------E-R-------AL-Y---------------------L--T-----P------------------------------Y--D------------------YI---------------D----------E------K--S-----------------------------P------------------------------I----Y------------------YF----L----R-----S---------------------------------------------H--------LN--I---------------Q------R------P--
> str16: M-----P--R---V--P---------V--Y-DSPQVS---PNTVPQ------------A------------------------------------------R-LA-T-------------P-------SFA------------------------T---------------P--------------T---F---RGA------------D--------------A---------------------------------P-AFQ-------D-------------T-ANQ------------------------------------------QA-----R----------Q---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-L-----------------R---T---R---------------T-------------------------QL-P-----------------------------------------L--A------Y----------------T--N-------S-------------------F---------T------------R----------------------------------------G-------V----Y-------------------------------------Y--------------P-------D---K----------V------------F------------------R-----SS--V-L----------------H-------------------------------S-------------
> str18: MF-----------VF-------------F------V-------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-L----------T----------T---R---------------T-------------------------QL-P--P-----A----Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H--------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: M-------E---------------A---------------------I-----------------I---------S-----------F-----------------A--------------------G-----------------------------------------------I---------------------G---------------------------------------------I--------------------------N----------------Y---------------------K------------K--------L-Q---S-----K----L--Q---H------D--F---------------G--------R------------------------------VL---K-A-------L-T-----------V-T---A--------R-----A--L----------------P--GQ-------P-K-------------------------H------------I-A-----------I--------RQ--------
> str20: M-A-------S---------------------S------GP---------------E--------------------------------------------R--A----E--H-QIIL--P----------------------E-------S------------------------HL-S--SPL-------V-----K--HK-L--L---------------------Y--------------Y-------W-K--L--------------------------T----G-L--------------------------------------------------P---L----P--------D----------ECD------------------------F-----D--------------------------------------H--------L--------I-----------------------------------------------------------------------------------------------------------------
> str21: M-------E-S-LV--P----------------------G----------------------------------------------F------N-EK-THV-------------Q--LSLPVLQV------RDV-L---V----------------------R--------------------------------G------------F-----------G------------------------D---S-V-----------------------E-EV--L-------------S---E----V--------------R-----------Q-----H-L-K------------------D------------------GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M-----------L-----------A--------P--S---PN-----------------S---------------K---I-------Q---------------L---F--N-------------------------------N------------------------------I-----------N-I---------------------D-------------------------------I--------------------------N----------------Y-------------E-------------------------------------H------------T------L----------------------------------Y-----F-----------A---S----V--S---A----------Q-------------N----S----------F-------------F---A-------Q-W--------------V-------V-Y-S---------------------AD---KA-----I------------------
> str23: M---------S-------------A---------------------I-----T---E----------------------------------TK----PT--------------I-----------------------------EL---P----------A-L-----AE--------------------------G------------F---Q--------------R-Y---N--------------------K-----------------------------T-----P-------------------------------G----------------------------------------F----------------T--------------------C-----------------VL-----------------------D------------------R--Y-------D-H---------GV----------------I----------N---------D-S-----K--------I--------VL----Y------------N----
> str24: M---K------------------------------------N----I-----------A-------E-------------------F-----K---K-------A---------------P----------------------ELAEK-L------LE------V-------------------------F---------------S----N-LK-----G------------NS-------------RS-------L------------D-------------------P--------------M-------------R------A-G------------K-----------H------D--------------------------V-------------------------------V---------V------------I----------------E-----------------------S------TK-----------K--------L--------------------------------------------------------------
> str25: M-----P---------------------------Q-----P--------L-------------------------K-QS-----L---------D-------------------Q---S----------------------------K----------W--LRE---AEK------HL----------------R-A--L-----------------E-S-------------------------------------L--------------V-D-S---NLE----------------EE------K------L-----K---------------------P------Q-------LS---------------M----G--E---DV-----Q-----S-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-L----------------------------I------------T-------R----------T------Q---S------------Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H--------------------S---------------------T------------Q----------D--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M---K---------F--D--------V----------------------L---------S---------L----------------F-----------------A---------------P------W--A----------------K----------------VD--E-----Q---E------------------Y-----------D--Q-------------------------------------------------Q------------------L-----N--------------------N----------------------------------------------------------N-L-E---------S---------I-----------------TAPK--------F----------------------D--------D---------------------G--A-----------T------------------E-------------I--ES-------E------------R-----------G---D--I-------
> str28: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-------F----T-----------------------------N--------R----------T------QL-PS-------A----Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H--------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M------------------------------------------------------W---S----I--IVL-----K--------L----------------------------I----S------------------------------------------------------IQP-L------L--------------L---V-TSL-------P-----------------------------------------L-Y--------NP----------N------------------------M---DSC-CL------------------I-S--R-----I-----TP----EL----A----------------G----------------------K-----------------L------------T-------WI------------------------F-----I-----------------------------------------------------------------------------------------------------
> str30: M-------E-S-LV--P----------------------G----------------------------------------------F------N-EK-THV-------------Q--LSLPVLQV------RDV-L---V----------------------R--------------------------------G------------F-----------G------------------------D---S-V-----------------------E-E-------------------------------------F-------------LS-----------------E-----A-----------R--------Q------------------HL------K-D--------G-------------------T---------------------------------------------------------------------------------------------------------------------------------------------
> str31: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------M-----------PLF--N--L----------------I------------T------------------T----T-Q---S------------Y--TN-F-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H-L-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M------------------------H--------Q-----------I-----T---------------V----VS--------------------------------------------------G----------------------P------T-E------V--------------S------T------C--------------F-----------G-------------S----------------------L---------------------------------------H--------------------------------------------P--------------------F-Q---------------S-L------------------K--------P-------V-----MAN---A--L---G---------V---L------E---------------G---------------K----------M----------FC-------SIG---------G-------------R------------S-------L-----
> str33: M-A----------------T-L---------------------------L---R-----S---------L-AL-------------F-----K--------R--------N------------------------------------K-----------------D---K-PPI------------T-------------------S-------------G-------------S-G-GA-I------R-G--IK------------------------------------------H--------------I--------------------I----------I------------------------------------------V-----------------------P------------------------------I--P-----------------------------G------------D-----------------SS---------------I-------T--------T-------R------------S---R---------
> str34: M-------E-S-LV--P----------------------G----------------------------------------------F------N-EK-THV-------------Q--LSLPVLQV------RDV-L---V----------------------R--------------------------------G------------F-----------G------------------------D---S-----------------------------M--E----------------E----V---------L------------S--------------------E-----A-----------R--------Q------------------HL------K-D--------G-------------------T---------------------------------------------------------------------------------------------------------------------------------------------
> str35: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-L----------T----------T----------------------------G---------T------QL-P--P-----A----Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H--------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: M-AN----------------I-I------------------N-------L-----W-------------------------N-------------------------------------------G-----------------------------------------------I------------------V----------------------P-----M---------------V------------------------Q-------D-V-------N-----------------------V-A---S-I------------TA------------------------------------F--------------K--S---------------M---------I-------D-E---------------T-------W--D------------K--KI------------------E----A-----------N-------T--------C--------I---S----RK--H-----------R------N-------------------
> str37: M-----------L----------------------------N-----------R----------I------------Q-------------T-----------L--------------------------------M----------K-------T---A-------------------------N-----N-----Y-------------------E----T------------------I----E------I---L--------------------------------------R-----------N------------Y-------L--------RL---YI--I---------L----A---RN---E----E--G--------RG-I---L-----------I----------------------Y-------------D--------D----------N--------ID--------S---V---------------------------------------------------------------------------------------
> str38: M-A--DP-----------------A--------------G--T-----------N----------------------------------------------------------------------G-----------------E--E------------------------------------------------G---------T--------------G-------C----N--G---------------W--------F-----Y----V--E----------A-----------------V-------------V----E-----------------K------------------------------------K-T---G-D---------A----------I------SD--D----E---N----E------------------N-D--S-D-----------T----G----E-------D-------L-------------VD---------------------------------------------------------------
> str39: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------------N-L-----------------R---T---R---------------T-------------------------QL-P--PS---------Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H--------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-------E-S-LV--P----------------------G----------------------------------------------F------N-EK-THV-------------Q--LSLPVLQV------------CDVL-----------------------V-----R------------------------G------------F-----------G------------------------D---S-V-----------------------E-EV--L-------------S---E--A----------------R-----------Q-----H-L-K------------------D------------------GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M--N-------------------------------------N---Q-------R---------------------K----------------K-----T-----A--------------------------R----------------P--SFNM-L------------KR---------A-------------R----------------N---------------R---------V-----------S----------------------------------T-------------------V-----S--------------------Q-------LAK---R-----------------F-----------------S--------------------K----------G------L-------------L---------------------S------------------G-----------------Q-----G-PMK--------L-----V------------------------MA--------F---------------------
> str42: M---------S------------------------------N--------------------------------------------F-------D---------A--------I-----------------R--AL---V-D-------------T---------D-A-----------------------------YKLGH---------------------------------------I-------------------------------------------------------H-------M---------------Y--------------------P-----E------------------------------GT-E---------Y--------------------------VL-S----N-----------F----------T--D---------R-----------G-------S----------------R---I----E--------------G-----VT----H---T----------V----------H------------
> str43: M-------------------I---------E------------------L---R-----------------------------H----E-----------V-------------Q----------G------D--L---V---------------T-----------------I-----------N------V----------V-------------E----T-----------------------------------P----------------E---------------------------------D----L---------D---G----------------------------------F--R-D-----------------------------F--------I---------------------------R----A--H--------L--------I---C------L-----A--------VD-T------------------E---------------------T--------TG----------L-D-IY-----------------
> str44: MF-----------VF------L----V----------------------L-------------------LP-LVS---S--------Q--------------------C------------V--------------M-----------PLF--N--L----------------I------------T------------------T-----NQ---S------------Y--TNSF-------T----R-GV-------Y-------Y-PDKVF----------------------R-S----SV---------L----------------------H---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M---------S----K-D---L----VA-------------------------R---QA----------L------------------------------------------------------------------M------------------T---A--R--------------------------M--------K-------------------------A--------------------D---------------F----------VF-----------------------------------------F-------------L---------------------------------F-----------------------V-------L------------W---K---A---L-S-----------L----------P--V-------------P-------T------R------C--------Q----------I---D--------M---A-----------K---KL----------------------S-A-------G---
> str46: M-A-------S-L--------L-------------------------K-----------S---------L---------------------T-----------L---F---------------------------------------K--------------R---T---R----------D------------------------------Q--P--P--------------------------------------L--A---S------------------G-----------S--------------------------G-----G---AI----R----------------------------------------G-----------I----------K----------------------------------------H----VI-----------I------V---LI---------------P--G-----D-------SS---------------I------VTR----------------------------S---R---------
> str47: M--------R---V---------R---------------G------I--L---RNW-Q--QW-WIW-------------------------T--------------------------SL-----GFW--------M-------------F---M------------------I-------------------C------------S------------------------------V-------------V-------------------------------G---N---LW-----------V--------------------T-------------------------------------------------------------V----Y-------------------------------------Y-------G---------V-------------P-----V--W-------------------K-----------------E-----------A-----------K------T------------------T---------------
> str48: M-A----------V----E--------------P----------------------------------------------------F----------P---RR-----------------P----------------------------------------------------I------------T-------R--------------------P---------------------------------------------------------------------------------H----AS--------I----EV-----DT-SG----IG-G---------------------S---A----------------G-S-----------------S-----E------K------V-F---------------------------------C----------------LI-G-----------------QA--------------E--------------G---------GE----------P--------N---T-------------V-
> str49: MF---------Y------------AH-AF----------G--------G-------------------------------Y-------------DE--------------N------L----------------------------------------------------------H---A---------F------------------------P----G--------------------I-------S--------------S-------------------T-------------------V-A-ND--------VRKY-----S-----------------------------------------------------------V-------------------------------V--S------VY--------------------N-----K--K-----Y---------------N---------------------I-----V----------------------K-----N---------K-------Y----------M-----W
> str50: M-AN-------Y--------------------S--------------K--------------P-----------------------F----------------L-------------L--------------D----------------------------------------I------------------V---------------F--N--K------------------------------D-------IKC----------I-N-D-----S------------------------C-S---------------------------------H--------------------S-D-----------C----R--------------YQ-----SN--S--------------------------Y-----------------V----------E------------L----R-R--N----------QA-LN-----K-----------N----------------------L------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 575
> best bound: 145.0
> wall time: 61.00s
> ```
