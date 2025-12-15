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
Model = scsp.model.wmm_hexaly.Model
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
>  Sol: tkulcigneycojiqfsovoazpkuhmplxnhtqgbxzrddbxcvsxuqpvissbxrvnngf
> str1: tk----gn---------------kuhmp-xnhtqg-xz------v-x----is---------
> str2: -----i-----ojiqf-o----------l-n----bx-----xcvs-uqpvissbx-----f
> str3: --ulci-n-yco----sovo-zp----pl--------------------p------------
> str4: -----ig-e---------v-az------------gb--rddb-c-s----v-----rvnngf
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 0.0
> wall time: 60.010912s
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
>  Sol: ipuyplrogenbdcevadzfxwgbjtinyucvxerdpmqfozkrdbrlcsovgtondfkuibhtmpxrvnhntqgxzpcvxwdsubroqpvisslbxfbhep
> str1: -------------------------t----------------k---------g--n--ku--h-mpx--nh-tqgxz--vx----------is---------
> str2: i------o----------------j-i-----------qfo------l-------n-----b----x--------x--cv---su---qpviss-bxf----
> str3: --u--l-------c------------iny-c---------o--------sov--o---------------------zp-----------p----l------p
> str4: i-------ge-----va-z---gb----------rd--------db--cs-v---------------rvn-n--g----------------------f----
> str5: -p-yplr-----------z-x--------uc-----pmq------------vgt--df-ui-------v---------c---ds-b-o--------------
> str6: -p---------bd-ev-d------------cv---dp--f-z-------s--------------m------------------s-broq-v----b--bh--
> str7: ---------enb-c----zf----jt-----vxer------z---br----v--------i-------------g--p----------------l-----e-
> str8: ------r-------------xw----------x-----q---krd-rlc----to-d------tmp-r---------p--xwd-------------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 102
> best bound: 0.0
> wall time: 59.992837s
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
> --- Solution (of length 158) ---
>   Sol: irkxuelpbscwxqkrinyfsdahtxpuabcojivncdqfbgevzfapkolrzgnbxkuqjtvxerdzqcvdewhbcsvrvwantfigpmqvglctdfijowuqpviokszspbxnahmiuvdcdtqbgxezhksbkroqnfvbbhmplgrpxwdyis
> str01: ------------------------t-----------------------k----gn--ku---------------h--------------m--------------p---------xn-h-------tq-gx-z----------v---------x---is
> str02: i------------------------------oji----qf---------ol---nbx------x-----cv------s------------------------uqpvi--s-s-bx--------------------------f----------------
> str03: ----u-l---c-----iny-----------co---------------------------------------------s----------------------o----v-o--z-p----------------------------------pl--p------
> str04: i----------------------------------------gev--a-----zg-b---------rd----d---bcsvrv--n-------------------------------n------------g------------f----------------
> str05: -------p----------y-------p-----------------------lrz---x-u----------c------------------pmqvg--tdf----u---i--------------v-cd---------sb--o-------------------
> str06: -------pb------------d--------------------ev----------------------d--cvd----------------p--------f------------zs------m---------------sb-roq--vbbh------------
> str07: -----e-----------n-----------bc-------------zf--------------jtvxer-z-------b---rv-----igp----l------------------------------------e---------------------------
> str08: -r-x-------wxqkr-----d-----------------------------r-----------------------------------------lct----o---------------------d--t--------------------mp--rpxwd---
> str09: --k-----------k-----------------------q-------a--------------------------------------fig--q--------j-w-----ok------------------------ks-kr-----b----lg--------
> str10: ------l-----x------------xp-ab---iv-----b--vz---ko--z--------------z--vd--------------------------------------------------------------------------------------
> str11: --k------------ri--fs-a-----------vncdq----------------------------------wh-----------------------------------z------------c----------------------------------
> str12: -------------q--------a--x-u---------d---g-----------------q--v-----qc--ew-b---------f-g----------ijow---------------------------------------------------w-y--
> str13: -r-------s--xq------------------j--n---f-------p----------------------------------a-------------d-i---u------s---------i------qb--ezhk----o------hm--g--------
> str14: i----------w--------s--h----------v---------------------------------------h-c-----------------------o-----------------miuvd-d---------------------m-----------
> str15: -----------------------htx------------------------------x--qj------zq------bc-------t----------------------------b--a----------------k------n-----------------
> str16: ---xu----s---------f----------c--------f----z--p----------------e-------e---c-v--wantf---m--g----------q------z---------u-------------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 158
> best bound: 0.0
> wall time: 59.613262s
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
> wall time: 59.964769s
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
>   Sol: daecbdeabecdabcedaecbdaebcdeabacde
> str01: d--cb-----c---c-d---b----c-----c-e
> str02: ----bd-----d-b-e--e----e---e-b--d-
> str03: ---c---a--cd---e--ec---eb--e------
> str04: -ae--d-----d----d----d-eb-d-----d-
> str05: -a-cb-e--ec-abce------------------
> str06: ----b---b---ab-e----bd---c---ba---
> str07: ----b---b---a--e-ae-b-a---d-a-----
> str08: --e---e--e-----e---cbd--b--e-----e
> str09: ---c------cd---e--e--da---d----cd-
> str10: ----bd-ab--d-b-e-a----a---d-------
> str11: --e--de----da----a----ae----a-a---
> str12: -a-----a-e--a----a--b--e---ea--c--
> str13: --e----a----abc--a-c-----cd--b----
> str14: ----bde--e--a---d-e---a---de------
> str15: ---c---a-e-da---d-e----e---e----d-
> str16: --e-b-----c-a---d---b-a-b----b---e
> str17: d----d----c----e--e---a-b-dea-----
> str18: da--b-----cd----d-e---ae-c--------
> str19: -a-----a---d--ce--e--da-----ab----
> str20: -ae---e---c---ce--e----e----a-a---
> str21: ----b---b--da--e---c--a-----a---de
> str22: da-c--e----da--eda--b-------------
> str23: -a-----a-e--ab------b---b----b-c-e
> str24: d-e--d--b-c--bc--a----a-b---------
> str25: d---bd-a----a--e----b---bc---b----
> str26: d-e-b-e----d-b-e----b-a--c--------
> str27: ---c--e--e---bc-d--cbd-e----------
> str28: d---b-e----da----a---da-----ab----
> str29: ---c------c---c-d--cb--eb-d----c--
> str30: -ae---ea--cd-bc-----bd------------
> str31: da-cb-ea--c---c----c-d------------
> str32: --ec--e-b-c---c-d---bd--b---------
> str33: d----d--b----bceda--b---b---------
> str34: -a-----a-e--ab---a----aeb---a-----
> str35: --ecb---b-c-a----a---d---cd-------
> str36: d-e-b-----c---ce---c-d--bc--------
> str37: da-----a--c--b---ae----ebc--------
> str38: -a---d-abe--a----a-c-----c-e------
> str39: daec-d--b---a-c--a----a-----------
> str40: da-cb---b--d--ced--c--------------
> str41: d-e--d--be-----e----b---b-de------
> str42: ---c-d-a---d--c-d--c-da-----a-----
> str43: ---c--e--e-d--c-----b-ae---e----d-
> str44: ---c--ea-ec-a----a----a--c--a-----
> str45: d--c------c---ce----b---b----ba-d-
> str46: ----b--a-e-----e-ae-b---b-de------
> str47: d---bde-b---a-c----c-d--b---------
> str48: --e-b-----c--b-e--e--dae----a-----
> str49: -ae---e--e---b------bd--bc--a-----
> str50: d---bd-ab-c----e---cb---b---------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 0.0
> wall time: 59.993184s
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
>   Sol: TCATGACCGTAGATCAGTACGATC
> str01: --ATG---G--GAT-A---CG---
> str02: --AT-ACC-T---TC----C---C
> str03: -CA---C-G-A-AT---T--GA--
> str04: T-A--A----A-ATC--T--G-T-
> str05: --A-G---GTA-A-CA--A--A--
> str06: T--T--CC-TAG----GTA-----
> str07: T--TG----TAGATC--T------
> str08: T---G---G--GA--AGT----TC
> str09: T--T--CC--A---CA--AC--T-
> str10: TC-T-A----A-A-C-G-A--A--
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 0.0
> wall time: 59.976992s
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
>   Sol: ATGACTGACGTAACGTACATGCATCATGCATCGATGCAGTCATCAGTCAGCATGCATAGCATACTGACAGTACTGATCAACTGCATGACTGCTAGCATGCATGCATCGTAGCATCGTAGCTACGACTACTGAGTCGAR
> str01: -T-A--G---TA--GTA---G-A-C-T-C--CG--G-A---A---GT--G-A--CA-A--A--C---C----CTGA--AA----A-GA-----A---TG---G-AT---A--A----A--TA----TA----------
> str02: --G---GA--TAA---ACA--C-TC---C--CGA---A---A--A-T-A--AT---T----T---GAC--T--T-A--AAC---A--AC-GC--G-A--CA-G--T--T--CA----AG-------------------
> str03: AT-AC---C-T----T-C---C-T-A-G----G-T--A---A-CA---A--A--C----CA-AC---CA--ACT--T----T---TGA-T-CT--C-T---TG--T---AG-ATC-T-G-------------------
> str04: -T-A---A---A---T---T--AT-A---ATC--T----T-AT-A--C----T--A--G--TA---A-A--A---A--A--T--A-G---G---G--TG--T--A----A-C--CG-A---A--A--AC-G-GTC---
> str05: -T---T-A---AA---ACA-GC--C-TG--T-G--G--GT--T--G-CA-C---C----CA--CT--CA---C--A------G---G---GC---C---CA--C-T-G--G----G---C---G-C-A---AG-----
> str06: ATGACT----T--C---CA---AT---G----GAT-C---C--CA---A-C---C-T--CA-A--G-C--T--T---C--C---A---C--C---C---CA---AT-G--G--T--T---T-C-A-----G---C---
> str07: A--AC--A---AAC---CA---A-C---CA---A--C--T--T---T-----TG-AT--C-T-CT-----T---G-T-A---G-AT--CTG-T----T-C-T-C-T---A--A----A-C---GA--AC---------
> str08: ATGA---A---AACG-A-A---A--AT---T--AT----T-ATCA---AG---G----G--TA-TG---G-A---A------G--TG---G--A--A-GC-TG-A-CG-A--A----A--T-----------------
> str09: A---CT--CG----G--C-TGCAT---GC-T---T--AGT-----G-CA-C-T-CA---C-----G-CAGTA-T-A--A--T---T-A-----A---T--A---A-C-TA--AT--TA--------------------
> str10: -T---TG---TA--G-A--T-C-T---G--T---T-C--TC-T-A---A--A--C---G-A-ACT-----T--T-A--AA----AT--CTG-T-G--TG---GC-T-GT--CA-C-T--C------------------
> str11: --G-C--A-G-A--G--CAT---T--T---TC--T--A---AT-A-TC--CA--CA-A--A-A-TGA-AG----G--CAA-T--A--A-T--T-G--T--A--C-T---A-C-TC-----------------------
> str12: ATGA--G-C----C--A-A-G-ATC---C---GA--C-G--A--AG--AGC---C----C---C--A-AG----GA------G---GA--G--A--A-G---G-A--G--G----G-A-C--C--C--C-----C---
> str13: -T--CT--C--A-C--A---G--T--T-CA---A-G-A---A-C---C--CA---A-AG--TAC---C----C----C--C--CAT-A--GC---C---C-T-C-T--TA--A----AGC--C-AC------------
> str14: A-G---G---T----T---T--AT-A--C--C--T----TC--C--T-AG---G--TA--A--C--A-A--AC----CAAC--CA--ACT--T----T-C--G-ATC-T--C-T--T-G-TA----------------
> str15: A-G---G---T----T---T--AT-A--C--C--T----TC--C---CAG---G--TA--A--C--A-A--AC----CAAC--CA--ACT--T----T-C--G-ATC-T--C-T--T-G-TA----------------
> str16: -T-A---A---AAC--A-A--C-TCA---AT--A--CA---A-CA-T-A--A-G-A-A--A-A-T--CA--AC-G--CAA----A--A-----A-CA--C-T-CA-C--A--A----A--------------------
> str17: ----C---CG---C---C---CAT--T---T-G--G--G-C----G---GC-T-C-T--C-----GA--G--C-GAT-A---GC-T--C-G-T--C--G-A---ATC----C--C-T--C---GAC--CT--------
> str18: AT-AC---C-T----T-C---C--CA-G----G-T--A---A-CA---A--A--C----CA-AC---CA--ACT--T----T-C--GA-T-CT--C-T---TG--T---AG-ATC-T-G-------------------
> str19: -T--CT--C--A-C--A---G--T--T-CA---A-G-A---A-C---C----T-CA-AG--T-CT--C----C----C--C--CAT-A--G---GC---C-T-C-T--T----TC--AG-T-C-A-----G-------
> str20: --GA-T--C-T--C-T-C-T-CA-C---C---GA---A--C--C--T--G---GC----C---C---C-G----G-------GCA--A-----A---TGC---C--C-TA--ATC----C-A-GA-----G-GT-G--
> str21: A-GA--G-C--AA--T-CA-G--T---GCATC-A-G-A---A--A-T-A---T--A---C---CT-A---T--T-AT-A-C---A---CT--T----TGC-T--A----AG-A----A--T-----------------
> str22: A--A-T----TAA---A-A--CATC-T-CA---AT--A--CA--A--CA---T--A-AG-A-A---A-A--AC--A--A-C-GCA--A-----A--A---A--CA-C-T--CAT------------------------
> str23: A--A---ACG-AAC-T---T---T-A---A---A---A-TC-T--GT--G--TG----GC-T---G----T-C--A-C---T-C--G---GCT-GCATGC-T---T---AG--T-G---C------------------
> str24: AT-A---AC-TAA--T---T--A-C-TG--TCG-T----T-----G--A-CA-G----G-A--C--AC-G-A--G-T-AACT-C--G--T-CTA---T-C-T---TC-T-G---------------------------
> str25: ATGA--G---T---GT-CA--C-----G-A---AT----TCA-C-GT-A-CA---AT-G-A-ACTG---G-A-TG-T----T-CA---C-G-T-G---G-A---AT---A--A-------------------------
> str26: A---C---CGT---G-----G------GC---GA-GC-G------GT--G-A--C----C-----G---GT---G-TC---T---T--C--CTAG--TG---G----GT--C--C----C-ACG--T--TGA----AR
> str27: A--A---A-G----GT---T---T-AT--A-C----C--T--TC---C--CA-G----G--TA---ACA--A---A-C--C---A--AC--C-A--A--C-T---T--T--C---G-A--T-C---T-CT---T-G--
> str28: A-G--T-A-GT----T-C--GC--C-TG--T-G-TG-AG-C-T--G--A-CA---A-A-C-T--T-A--GTA--G-T-----G--T---T--T-G--TG-A-G----G-A---T--TA--------------------
> str29: -T---T----TA---TAC---C-T--T-C--C--T--AG------GT-A--A--CA-A--A--C---CA--AC----CAACT---T---T-C--G-AT-C-T-C-T--T-G--T---AG--A----T-----------
> str30: ATG-C-G--GT--CGT-C-T-C-TC---C--C----C-G------G-C----T---T----T--T-----T--T--TC--C--C----C-GC--GC---C--GC---GT----T-G--GC---G-C--C-GA------
> str31: --G--TGAC--AA---A-A---A-CAT--A---ATG--G--A-C--TC--CA---A---CA--C---CA-T---G-TCAA--GC-T---T--T--CA-G---G--T---AG-A-C-----------------------
> str32: --G--TG---TAA-G-A-A---A-CA-G--T--A---AG-C--C---C-G---G-A-AG--T---G---GT---G-T----T---T---TGC--G-AT---T---TCG-AG----G---C--CG------G-------
> str33: --GA--GA---A---T----G-A----G--TC--T-CA-T--T-A--C--C--GC----C---C-G---GTACT--T-A---GCA--A--GCTA--AT--A-G--TC--A-C---G--GC------------------
> str34: ATG--TG--GT--CG-A--TGC--CATG----GA-G--G-C--C---CA-C---CA--G--T--T--CA-T--T-A--A---G---G-CT-C---C-TG---GCAT--T-----------------------------
> str35: A---C-GA-G---CGT---T---T--T--A---A-G--G------G-C--C---C---GC-----GAC--T---G--C----G-A---C-G---GC---CA--CAT-G--GC--C----CT--G--TA-TG--T----
> str36: --G---G---T----T---T--AT-A--C--C--T----TC--C---CAG---G--TA--A--C--A-A--AC----CAAC--CA--ACT--T----T-C--G-ATC-T--C-T--T-G-TA-G--------------
> str37: -TG---G--G-AA-GT---T-C--CA---A---A---AG--ATCA--CA--A---A-A-CA--CT-AC----C--A------G--T--C----A--A--C---C-T-G-A--A--GTA-C-AC---------------
> str38: --GA---A-G---CGT---T--A--A--C---G-TG---T--T--G--AG---G-A-A--A-A--GACAG--CT--T-A---G---GA--G--A--A--CA---A--G-AGC-T-G--G----G--------------
> str39: A---C---C--A--G--C--GCA-C-T---TCG--GCAG-C----G---GCA-GCA---C---CT--C-G----G--CA---GCA---C--CT--CA-GCA-GCA----A-C--------------------------
> str40: ATG---G--G-A-C--A-A--C-T--T--AT---T-C---C-T-A-TCA---TG--T-GC---C--A-AG-A--G-------G--T---T--T----T--A--C--C----C---G--G-T--GAC--C--A------
> str41: -T---TG---TA--G-A--T-C-T---G--T---T-C--TC-T-A---A--A--C---G-A-ACT-----T--T-A--AA----AT--CTG-T-G--TG---G--T--T-G--TC--A-CT-C---------------
> str42: A--AC---C--AAC---CA---A-C-T---T---T-C-G--ATC--TC----T---T-G--TA--GA---T-CTG-T----T-C-T--CT---A--A---A--C---G-A--A-C-T---T-----TA----------
> str43: --G---G--GT----T-C-TGC--CA-G----G---CA-T-A---GTC----T---T----T--T-----T--T--TC---TG---G-C-G---GC---C---C-T--T-G--T-GTA---A--AC--CTG-------
> str44: --G---G-C-T---G--CATGC-T--T--A--G-TGCA--C-TCA--C-GCA-G--TA---TA---A---T--T-A--A--T--A--ACT---A--AT---T--A-C-T-G--T------------------------
> str45: -TG-C--A--T---G--C-T---T-A-G--T-G---CA--C-TCA--C-GCA-G--TA---TA---A---T--T-A--A--T--A--ACT---A--AT---T--A-C-T-G--TCGT---------------------
> str46: -T---T--C----C--ACA---A-C-T---T---T-C---CA-C---CA--A-GC-T--C-T---G-CA--A--GATC--C--CA-GA--G-T--CA-G---G----G--GC--C-T-G-T-----------------
> str47: -T--CT-A---AACG-A-A--C-T--T---T--A---A---A--A-TC----TG--T-G--T---G---G--CTG-TCA-CT-C--G---GCT-GCATGC-T---T---AG---------------------------
> str48: A---C---CG----G-A--TG------GC--CG---C-G--AT---T-----T---T----T-C-G---G-A--G-TC--CT---TG---G---G---G---G-A-C----CA-C-T--C-A-GA--A-T-AG---A-
> str49: ----CT----T---GTA---G-ATC-TG--T---T-C--TC-T-A---A--A--C---G-A-ACT-----T--T-A--AA----AT--CTG-T-G--TG---GC-T-GT--CA-C-T---------------------
> str50: ATGA--G-C--A-C-TA-A-GC-----G-A---A-G-A---A-C---CA--A---A-A--A----G-CAG-AC--A--A--T--A---C----A--A--C---C--CG---C-T---A--T-----TAC---------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 138
> best bound: 0.0
> wall time: 59.824583s
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
>   Sol: MEQPSLSKFTRYAEHVNQELNSYCHFDAIRPGFKGVTANEGYQL
> str01: M-----------A------L-SYC------P--KG-T-------
> str02: M-Q-S-S------------LN------AI-P----V--------
> str03: M--P-LS----Y-----Q------HF---R---K----------
> str04: ME-----------EHVN-EL----H-D-----------------
> str05: M---S-----------N--------FDAIR-------A-----L
> str06: M-------F-R-----NQ--NS-------R--------N-G---
> str07: M-------F--YA-H------------A----F-G-----GY--
> str08: M---S--KFTR------------------RP----------YQ-
> str09: M---S---F------V-----------A---G---VTA----Q-
> str10: ME--SL---------V--------------PGF-----NE----
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 0.0
> wall time: 59.944306s
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
> --- Solution (of length 499) ---
>   Sol: MAFVFLESVLLPLVSSQCVNRPGFKNDLEKTHVQLSLPRAITRVLFQVSTGYALEIRDVLSPQLTKVRNGFMPLAGDSPTIEFNLDAYTKLVEQWNSFTRGIVDHAETYQPCGKIVLNRTAPSEAFNYLQGSAEKDHLMRTIEQLAVFPDKSEVILTRQAHGYPFSENDRTLKNSFAVRGQLTRGVYSDILPNVKTASGINLHPYPDKVFRSETSQLGVYLHSADFKRINPLCTNGSMRADEGKHVLWDAFSIPYTNVLEADGSVIKRGVELFTAIKPQGRDSWACSHITVLESDGKAFTRYEILNDRKVQGPADMSRIKLVTYFACSELIGQAHRYWEGLVSTNPDKHTVAILPDGEQSNDSFRISTPECLGFAVDSEGKILHIYNDSATVDERCLQWTMPRGIDFRANEKHISGVKAECRLTNPDSVQYKRIAGLNDIVFHKNMAKYRIKECDLSAVVGDFDHLINLYGKAIMWNVTGSQSTIVYYGVPVWKEAKTT
> str01: M-------------------R----------H--L---------------------------------N-----------I----D---------------I----ETY-------------S--------S-----------------------------------ND--------------------I----K-----N----------------GVY------K---------------------------Y-----AD------------A-----------------E-D---F---EIL---------------L---FA----------Y-----S---------I--DG---------------G-----E------------V-E-CL--------D----------------LT--------R------------------------------------------------------------------
> str02: M-----E-------------R-----------------RA----------------------------------------------------------------H-------------RT----------------H------Q-----------------------N-------------------------------------------------------------------------------WDA-----T----------K----------P--R-----------E-------R------RK-Q-----------T---------Q-HR----L--T----H-----PD-----DS--I-------------------Y---------------PR-I-----EK------AE---------------G-------------R-KE-D---------H-----G----------------------------
> str03: M-----E----P----------G----------------A-----F--ST--AL----------------F-----D---------A---L--------------------C-----------------------D-------------D----IL----H--------R--------R--L------------------------------E-SQL----------R----------------------F-----------G-----GV--------Q---------I-----------------------P--------------------------------P-----------E-----------------V-S---------D-------------PR-------------V-------------Y---AG------------Y--------A-------L--L------------------------------
> str04: M---------------------G-K--------------------F-----Y-----------------------------------Y--------S--------------------NR--------------------R----LAVF-----------A--------------------Q---------------A------------------Q------S----R----------------H-L---------------G-----G-------------S------------------YE-------Q--------------------------W--L----------A------------------C----V-S-G-------DSA----------------FRA-E-----VKA--R------VQ-K------D------------------------------------------------------------
> str05: --F-F---------------R-------E---------------------------------------N----LA-------F----------Q---------------Q--GK------A------------------R--E----FP--SE-------------E---------A-R-----------------A---N----------S------------------P--T--S-R--E----LW---------V---------R------------R--------------G---------------G--------------------------------NP-------L-----S---------E----A----G---------A---ER-------RG-------------------T---------------------------------------------------------------------------
> str06: M-------------------------D----------P----------S----L----------T----------------------------Q--------V------------------------------------------------------------------------------------------------------------------------------------------------W-A-------V-E--GSV------L----------S-A------------A-----------V----D-------T--A--E--------------TN-D--T-------E----------P-------D-EG--L-----SA---E---------------NE----G---E---T--------RI-----I---------RI---------------------------TGS------------------
> str07: MAF-----------------------D------------------F--S---------V-----T----G-------------N----TKL------------D---T--------------S-------G----------------F--------T-Q--G---------------V---------S---------S---------------------------------------M-----------------T-V--A-------------A----G---------T-L-----------I---------AD-----LV-------------------------K-T-A-------S--S----------------------------------Q------------------------LTN-----------L---------A----------------------------------QS----------------
> str08: MA-V------------------------------------I---L----------------P---------------S-T-------YT--------------D--------G------TA---A-----------------------------------------------------------------------------------------------------------CTNGS----------------P-------D--V----V---------G---------T-----G---T---------------M---------------------W---V--N----T--ILP-G----D-F---------F------------------------WT-P------------SG---E-------SV---R-------V----------------------------------------------------------
> str09: M------------------N----------T-------------------G----I------------------------I----D----L------F-----D-------------N------------------H---------V--D-S--I--------P------T------------------ILP----------H------------QL------A---------T------------L-D-----Y---L-----V--R-----T-I------------I-----D-------E--N-R--------S----V-------L----------L----------------------F-------------------HI---------------M--G----------SG-----------------------------------------------------------------------------------
> str10: M-FVFL--VLLPLVSSQCVN-------L----------R--TR------T------------QL--------P-----P-------AYT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M-------------------------D--------S-----------------------------K---------------E------T------------I--------------L------------------------IE-----------I----------------------------------I-P--K----I-------K---S-------YL----------L--------D--------------TN--------I----------------S-----------------------------P------K-------S--------Y-------N-D----------------F-IS---------------------------R--------------N-K------------N--------I-------F----------------V-------INLY------NV--S--TI--------------
> str12: M----L---L----S-------G-K----K-----------------------------------K-----M-L----------LD---------N------------Y--------------E----------------T----A-------------A----------------A-RG---RG-------------G-------D-----E--------------R----------R----------------------------RG--------------WA-------------F-------DR----PA----I--VT------------------------K----------------R-----------D---K-------S---D-R-----M-------A---H--------------------------------------------------------------------------------------
> str13: M------------------N--G-----E-------------------------E--D------------------D------N--------EQ-----------A--------------A---A--------E---------Q--------------Q-----------T-K---------------------K-A----------K--R-E-------------K---P------------K----------------------------------Q-----A---------------R-------KV------------T----SE----A---WE---------H--------------F------------D------------AT-D------------D---------G--AEC----------K----------H--------------------------------------------------------
> str14: M-----ES-L---V-------PGF-N--EKTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-------------VE-------------E--------VL-----SEA--------------R---Q----------------H----------LK---------------D---------G--------------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-------------------R------------------------------Y---I--V-SPQL--V------L-------------------Q--------V---------GK----------------G------------Q--------EV------------E--R------A----L----Y---L----T-------PY-D------------Y--------I-----------DE-K-------S-P-----------I-----------------------------------Y---------------------YF----L-----R------S-----H----L------N----I-------------------------------Q----R----------------------P-------------------------------------------------------------------------
> str16: M----------P--------R-----------V----P-----V-------Y-----D--SPQ---V----------SP----N----T--V------------------P------------------Q--A------R----LA----------T------P-S---------FA-----T--------P---T-------------FR------G-----AD--------------A-------------P------A-----------F-----Q--D-------T-------A-------N----Q---------------------QA-R----------------------Q--------------------------------------------------------------------------------------------------------------------------------------------
> str17: M-FVFL--VLLPLVSSQCVN-------L----------R--TR------T------------QL--------PLA------------YT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FVF------------------F--------V-L-LP------L--VS-----------S-Q------------------------------------------------C---V-N----------L-----------T---------------TR------------T---------QL---------P-----------P-------------------A------------------------------YTN------S--------FT------R--------------G-------------V-------------Y------------Y--------PDK--V------------FR-S----------S-------------V----L---------------H-S------------------------------------------------------------------------------------
> str19: M-----E--------------------------------AI--------------I----S---------F---AG----I-------------------GI---------------N---------Y------K---------------K----L--Q------S------K--------L---------------------------------Q-----H--DF---------G--R------VL-------------------K-------A----------------L-------T---------V------------T--A---------R---------------A-LP-G-Q---------P-----------K--HI----A--------------I--R---------------------Q---------------------------------------------------------------------
> str20: MA-----S------S-------G--------------P----------------E-R-----------------A------E----------------------H----Q----I--------------------------I--L---P---E------------S------------------------------------H-------------L-----S-------------S----------------P----L-----V-K--------------------H--------K-------L---------------L--Y------------YW---------K-----L-------------T----G---------L------------------P--------------------L--PD-------------------------ECD-------FDHLI--------------------------------
> str21: M-----ES-L---V-------PGF-N--EKTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-------------VE-------------E--------VL-----SE----------------------V----------RQ-H----------LK---------------D---------G--------------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L---------------------------------A---------------------P---------------SP----N------------S----------------KI--------------Q-------L---------F-------------------N-----N---------------I--N------I------D---------------------IN------------------------Y----E---------------------------H-T-L---------Y----------------------FA-S-------------VS--------A------Q-N-SF---------FA----------------------QW-----------------V-----------V-Y-------------------------SA---D---------KAI-------------------------
> str23: M------S-------------------------------AIT------------E---------TK------P------TIE--L-------------------------P---------A-------L---AE---------------------------G--F---------------Q--R--Y-----N-KT-------P-------------G-------F-------T---------------------------------------------------C----VL--D-----RY----D---------------------------H----G-V----------I-------NDS-----------------KI---------V----L---------------------------------Y------N-------------------------------------------------------------
> str24: M-----------------------KN--------------I-----------A-E---------------F------------------K-----------------------K------AP-E----L---AEK--L------L-------EV----------FS-N---LK------G------------N----S------------RS----L-------D-----P------MRA--GKH---D--------V------V----V-----I----------------ES-----T--------K----------KL----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: M----------P----Q----P-----L-K---Q-SL--------------------D----Q--------------S-----------K----W---------------------L-R----EA--------EK-HL-R-----A---------L----------E-------S------L---V--D--------S--NL----------E----------------------------E-----------------E------K----L----KPQ------------L-S---------------------M---------------G------E-------D---V-------QS-------------------------------------------------------------------------------------------------------------------------------------------
> str26: M-FVFL--VLLPLVSSQCVN-------L------------ITR------T------------Q--------------S---------YT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S-T-Q--------D----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-----------------------K--------------------F-----------DVLS--L------F---A---P---------------W----------A-------K-V-------------------D------EQ--------E---------Y-----D-----------Q----------------------------------QL------------N----N---------------------N-LE---S-I-------TA--P------------------K-F-------D-------D----------------G-A---------T-------------E-------I---E-------SE---------------R--------G-D-------I-------------------------------------------------------------------------------------
> str28: M-FVFL--VLLPLVSSQCVN---F------T-------------------------------------N------------------------------R-------T-Q------L----PS-A--Y------------T--------------------------N------SF------TRGVY-----------------YPDKVFRS--S---V-LHS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M---------------------------------------------------------------------------------------------W-S----I------------IVL-----------------K--L---I---------S--I---Q----P-------L---------L--------L--V-T-S---L-P------------L--Y---------NP---N--M--D----------S---------------------------------C----------------------------------------C--LI-----------S---------------------RI-TPE-L--A----GK-L-------T-------W-----I-F------I-------------------------------------------------------------------------------------
> str30: M-----ES-L---V-------PGF-N--EKTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-------------VE-------------E------------------F--L--S-E-----------A-----------RQ-H----------LK---------------D---------G--------------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FVFL--VLLPLVSSQCV----------------------------------------------------MPL--------FNL----------------I-----T-----------T--------------------T--Q-------S----------Y-------T--N-F------TRGVY-----------------YPDKVFRS--S---V-LH---------L---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M------------------------------H-Q------IT-V---VS-G----------P--T----------------E---------V----S-T------------C-------------F----GS-----L----------------------H--PF---------------Q------S--L---K--------P----V----------------------------M-A----------------N---A----------L-------G----------VLE--GK------------------M--------F-CS--IG-------G------------------------R-S----L-------------------------------------------------------------------------------------------------------------------------------
> str33: MA----------------------------T---L-L-R---------S----L--------------------A---------L------------F---------------K----R-------N-------KD--------------K------------P---------------------------P-------I-------------TS--G----S------------G------G------A--I--------------RG------IK----------HI--------------I--------------I--V-----------------------P------I-P-G----DS---S--------------I--------T--------T--R-----------S------R-----------------------------------------------------------------------------
> str34: M-----ES-L---V-------PGF-N--EKTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS------------------------------------------------------------M---E---------EV-L---------SE---------A-R-Q---------------------H-------------L---------K-------------D-G------------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FVFL--VLLPLVSSQCVN-------L--T----------T--------G-------------T----------------------------Q----------------------L----P--------------------------P----------A--Y-------T--NSF------TRGVY-----------------YPDKVFRS--S---V-LHS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA-----------------N--------------------I--------------I------------N----L--------------------WN----GIV-------P---------------------------M-------V-----------Q---------D--------V--------------NV--AS-I-------------T---------A-FK---------SM--------------I--------D--------E--T---------W----------D-K-----------K---------I---------E----A----------N----T--------------------C----------I------S-----R----------------KH--------R--N--------------------------------------------------------------------------
> str37: M----L-------------NR-------------------I-----Q--T---L-----------------M-----------------K--------T------A-----------N--------NY-----E------TIE-----------IL-R---------N------------------Y---L-------------------R-----L--Y--------I-----------------------I-----L-A------R-------------------------------------N----------------------E---------EG------------------------R-------G--------IL-IY-D----D----------------N---I------------DSV----------------------------------------------------------------------
> str38: MA------------------------D----------P-A----------G-------------T---NG-----------E----------E-------G------T----G-----------------------------------------------------------------------------------------------------------------------C-NG-----------W--F---Y--V-EA---V----VE-----K-------------------K--T-----------G--D----------A----I-----------S---D--------D-E--N--------E----------------NDS---D------T---G------E---------------D---------L---V-------------D--------------------------------------------
> str39: M-FVFL--VLLPLVSSQCVN-------L----------R--TR------T------------QL--------P-----P-----------------S-----------Y----------T------N----S---------------F--------TR---G---------------V--------Y-----------------YPDKVFRS--S---V-LHS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L---V-------PGF-N--EKTHVQLSLP-----VL-QV---------------------------------------------------------------C-----------------------D----------V--------L---------------------VRG-----------------------------F-------G------D-----------S--------V-------------E----------E-------------------VL-S--------E----------A---R--------------Q-H-----L------K-------DG----------T-----------------------------------------------------------------------------------------------------------------------------------
> str41: M------------------N-----N-------Q----R--------------------------K-----------------------K--------T------A------------R--PS--FN-----------M-----L-----K------R-A---------R---N----R------V-S-------T------------V--S---QL------A--KR----------------------FS--------------K-G--L-------------------L-S-G--------------QGP--M---KLV------------------------------------------------------------------------------M-------A--------------------------------F---------------------------------------------------------
> str42: M------S-----------N---F--D------------AI-R---------AL----V-----------------D--T-----DAY-KL---------G---H---------I---------------------H-M-----------------------YP--E------------G--T-----------------------------E------Y-------------------------VL----S----N---------------FT-------D------------------R----------G----SRI---------E--G---------V-T----HTV--------------------------------H-------------------------------------------------------------------------------------------------------------------
> str43: M---------------------------------------I-------------E----L-------R------------------------------------H-E--------V-------------QG----D-L--------V---------T--------------------------------I--NV--------------V---ET----------------P----------E------D---------L--DG---------F-------RD----------------F----I---R-----A--------------------H-----L-----------I-----------------CL--AVD-------------T--E-----T-----------------------T-----------GL-DI--------Y--------------------------------------------------
> str44: M-FVFL--VLLPLVSSQCV----------------------------------------------------MPL--------FNL----------------I-----T-----------T------N--Q-S------------------------------Y-------T--NSF------TRGVY-----------------YPDKVFRS--S---V-LH-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M------S----------------K-DL----V------A--R---Q-----AL-----------------M-------T------A------------R--------------------------------------M-----------K--------A--------D------F-V-------------------------------F---------------F-----L------------------F------VL------------------------W------------KA------L-----------S---L------------------------P----V---P------------T--------------------------RC-Q------ID---------------------------------------MAK---K---LSA--G--------------------------------------
> str46: MA-----S-LL-------------K----------SL----T--LF-------------------K-R-----------T-------------------R---D-----QP----------P------L---A------------------S---------G---S-------------G----G-----------A--I----------R------G----------I--------------KHV------I------------I---V-L---I-P-G-DS---S-I-V--------TR---------------SR-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M-------------------R-----------V-----R-----------G----I---L-------RN-------------------------W--------------Q-------------------Q---------------------------------------------------------------------------------------------------------------------W-----------------------------------W----I------------------------------------------------W-----T---------------S-----------LGF------------------------W-M-----F--------------------------------------M----I--C--S-VVG------NL------W-VT------VYYGVPVWKEAKTT
> str48: MA-V--E----P-----------F-------------PR---R------------------P------------------I-------T----------R----------P-------------------------H--------A-----S--I-----------E----------V----------D------T-SGI-----------------G-----------------GS--A--G--------S-----------S------E-----K-------------V-------F---------------------------C--LIGQA----EG----------------GE----------P-----------------N---TV-----------------------------------------------------------------------------------------------------------
> str49: M-F------------------------------------------------YA---------------------------------------------------HA-------------------F----G------------------------------GY-----D-------------------------------------------E----------------N-L------------H----AF--P--------G--I----------------S---S--TV------A-------ND--V-------R-K---Y---S-------------V--------V--------S---------------V---------YN------------------------K-----K------------Y------N-IV--KN--KY-------------------------MW-----------------------
> str50: MA-----------------N-------------------------------Y--------S----K------P---------F-L-----L------------D----------IV---------FN-------KD-----I--------K---------------------------------------------------------------------------------C-------------------I---N----D-S---------------------CSH-----SD-------------------------------C--------RY---------------------QSN-S----------------------Y-----V-E--L-----R----R-N-------------------Q----A-LN-----KN----------L-------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 499
> best bound: 0.0
> wall time: 59.99864s
> ```
