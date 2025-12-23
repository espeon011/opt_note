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
Model = scsp.model.ibs_scs.Model
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
> --- Solution (of length 73) ---
>  Sol: itkgnkuojiqfolevnabzcghxbimxnrcpdvyxcdnsbhoucstqovpgvorxzvisnpsbxnpgfilps
> str1: -tkgnku---------------h---m----p---x--n--h----tq---g---xzv------x----i--s
> str2: i------ojiqfol--n-b----x---x--c--v-----s---u---q--p-v-----is--sbx---f----
> str3: ------u------l------c----i--n-----y-c-----o--s--ov---o--z----p----p---lp-
> str4: i--g----------ev-a-z-g--b----r--d----d--b---cs---v----r--v--n----n-gf----
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 73
> best bound: 0.0
> wall time: 0.585041s
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
> --- Solution (of length 119) ---
>  Sol: pigenboyjpilrdqtxevwzxucfkolgnqkdcazfrvdpgbrujmhxiqtvxlcgtodtmpxnferzvsudbychmsotqpvrvisgovxbrozqvpcdsbxplnngfbiwdehops
> str1: ---------------t---------k--gn-k------------u--h-------------mpxn-----------h---tq------g--x---z-v-----x-------i------s
> str2: -i----o-j-i---q---------f-ol-n------------b-----x----x-c-------------vsu---------qpv--is-------------sbx-----f---------
> str3: ----------------------u----l-----c---------------i--------------n---------yc---o-------s-ov---oz--p-----pl-----------p-
> str4: -ige--------------v---------------az-----gbr---------------d------------db-c--s----vrv--------------------nngf---------
> str5: p------y-p-lr-------zxuc----------------p-----m---q-v---gt-d-----f-----u--------------i---v--------cdsb-------------o--
> str6: p----b-------d---ev-------------dc----vdp------------------------f--z-s------ms-------------bro-qv----b-------b----h---
> str7: ---enb-----------------c-----------zf--------j-----tvx------------erz----b----------rvi-g---------p------l--------e----
> str8: ------------r---x--w-x--------qk-----r-d---r----------lc-todtmp----r--------------p--------x--------------------wd-----
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 119
> best bound: 0.0
> wall time: 2.015542s
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
> --- Solution (of length 163) ---
>   Sol: krixuwslxqpkfchtxojiqfanypfxlrzpeabdigevudcosvaqjzgbrlnbxcdqvzkwognkuhcpmfqvdbctozsmipxqjbewtvanhtzcvsbuqgxfrpvdtmgideksrzfburvihkoqvprbnlgpxcjdsbowhmnglxfiwzdesuy
> str01: ---------------t----------------------------------------------k--gnkuh--m------------px--------nht------qgx--------------z----v-------------x--------------i----s--
> str02: --i--------------ojiqf---------------------o---------lnbx-----------------------------x------------cvs-uq----pv----i---s------------------------sb-------xf--------
> str03: ----u--l-----c-----i---ny-----------------cos-------------------o----------v----oz---p-----------------------p---------------------------l-p-----------------------
> str04: --i----------------------------------gev------a--zgbr-----d-----------------dbc---s----------v--------------r-v-------------------------n-------------ng--f--------
> str05: ----------p-------------yp--lrz-------------------------x-----------u-cpm-qv-----------------------------g------t---d-----f-u--i----v--------c-dsbo----------------
> str06: ----------p-----------------------bd--ev-dc--v------------d------------p-f-------zsm-----------------sb-----r---------------------oqv--b---------b--h--------------
> str07: --------------------------------e---------------------nb-c---z-----------f--------------j---tv------------x----------e--rz-b-rvi----------gp------------l------e---
> str08: -r-x-w--xq-k-----------------r-----d----------------rl---c---------------------to------------------------------dtm-------------------pr----px------w----------d----
> str09: k----------k--------q-a---f---------ig---------qj--------------wo--k--------------------------------------------------ks---------k----rb-lg------------------------
> str10: -------lx-------x--------p-------ab-i--v-----------b--------vzk-o----------------z----------------z-v----------d---------------------------------------------------
> str11: kri---------f-------------------------------s-a-------------v-----n---c-----d----------q---w----h-zc---------------------------------------------------------------
> str12: ---------q------------a----x------------ud--------g--------qv-------------q---c-----------ew----------b----f------gi--------------------------j---ow--------w-----y
> str13: -r----s-xq--------j----n--f----p-a-di---u---s---------------------------------------i--q-be-------z-----------------------------hko-----------------hm-g-----------
> str14: --i--ws-------h------------------------v-----------------------------hc---------o--mi------------------u------vd----d--------------------------------m-------------
> str15: --------------htx----------x-------------------qjz---------q-----------------bct---------b----a-----------------------k-----------------n--------------------------
> str16: ---xu-s-----fc-------f--------zpe-----e---c--v-----------------w------------------------------an-t---------f-----mg----------------q-------------------------z---u-
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 163
> best bound: 0.0
> wall time: 6.06334s
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
> --- Solution (of length 28) ---
>   Sol: bdcbacedbeeecdabddecbadceade
> str01: -dcb-c------cd-b---c---ce---
> str02: bd-----dbeee------e-b-d-----
> str03: --c-ac-d-ee-c-----e-b---e---
> str04: ----a-ed-----d--dde-b-d---d-
> str05: ----ac--bee-c-ab---c----e---
> str06: b--ba---be-----bd--cba------
> str07: b--ba-e-------a---e-bad--a--
> str08: ------e--eeec--bd---b---e--e
> str09: --c--c-d-ee--da-d--c--d-----
> str10: bd--a---b----d-b--e--a---ad-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 28
> best bound: 0.0
> wall time: 0.226905s
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
>   Sol: daebcdabecdaebceadcbaedbcebadceabd
> str01: d---c--b-c----c--d-b----c----ce---
> str02: ---b-d----d--b-e-----e---e----e-bd
> str03: ----c-a--cd-e--e--c--e-b-e--------
> str04: -ae--d----d------d----d--eb-d----d
> str05: -a--c--be---e-c-a--b----ce--------
> str06: ---b---b---a-b-e---b--d-c-ba------
> str07: ---b---b---ae---a----e-b---ad--a--
> str08: --e-----e---e--e--cb--db-e----e---
> str09: ----c----cd-e--e-d--a-d-c---d-----
> str10: ---b-dab--d--b-ea---a-d-----------
> str11: --e--d--e-da----a---ae-----a---a--
> str12: -a----a-e--a----a--b-e---e-a-c----
> str13: --e---a----a-bc-a-c-----c---d---b-
> str14: ---b-d--e---e---ad---e-----ad-e---
> str15: ----c-a-e-da-----d---e---e----e--d
> str16: --ebc-a---d--b--a--b---b-e--------
> str17: d----d---c--e--ea--b--d--e-a------
> str18: da-bcd----d-e---a----e--c---------
> str19: -a----a---d---ce-----ed----a---ab-
> str20: -ae-----ec----ce-----e---e-a---a--
> str21: ---b---b--dae-c-a---a-d--e--------
> str22: da--c---e-dae----d--a--b----------
> str23: -a----a-e--a-b-----b---b--b--ce---
> str24: d-e--d-b-c---bc-a---a--b----------
> str25: d--b-da----aeb-----b----c-b-------
> str26: d-eb----e-d--b-e---ba---c---------
> str27: ----c---e---ebc--dcb--d--e--------
> str28: d--b----e-da----ad--a------a----b-
> str29: ----c----c----c--dcb-e-b----dc----
> str30: -ae-----e--a--c--d-b----c-b-d-----
> str31: da--c--be--a--c---c-----c---d-----
> str32: --e-c---e----bc---c---db----d---b-
> str33: d----d-b-----bce-d--a--b--b-------
> str34: -a----a-e--a-b--a---ae-b---a------
> str35: --e-c--b-----bc-a---a-d-c---d-----
> str36: d-ebc----c--e-c--d-b----c---------
> str37: da----a--c---b--a----e---eb--c----
> str38: -a---dabe--a----a-c-----ce--------
> str39: dae-cd-b---a--c-a---a-------------
> str40: da--c--b-----b---dc--ed-c---------
> str41: d-e--d-be---eb-----b--d--e--------
> str42: ----cda---d---c--dc---d----a---a--
> str43: ----c---e---e----dcbae---e--d-----
> str44: ----c---e--ae-c-a---a------a-c-a--
> str45: d---c----c----ce---b---b--bad-----
> str46: ---b--a-e---e---a----e-b--b-d-e---
> str47: d--b-d--e----b--a-c-----c---d---b-
> str48: --ebc--be---e----d--ae-----a------
> str49: -ae-----e---eb-----b--dbc--a------
> str50: d--b-dab-c--e-c----b---b----------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 34
> best bound: 0.0
> wall time: 0.655461s
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
>   Sol: TATCGGTACGACTAGTCTGACTAC
> str01: -AT-GG---GA-TA--C-G-----
> str02: -AT----AC--CT--TC---C--C
> str03: ---C---ACGA--A-T-TGA----
> str04: TA-----A--A--A-TCTG--T--
> str05: -A--GGTA--AC-A-----A--A-
> str06: T-TC----C---TAG---G--TA-
> str07: T-T-G-TA-GA-T---CT------
> str08: T---GG---GA--AGT-T--C---
> str09: T-TC----C-AC-A-----ACT--
> str10: T--C--TA--A--A--C-GA--A-
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 0.0
> wall time: 0.15998s
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
> --- Solution (of length 135) ---
>   Sol: AAACCTGTAGCTAGATCAGTCATGACTCATCAGTCGTACAGCTACGATCAGCTAGACTAAACGTCAGTACTGACTAGTCAGCTCATGATGCATGACGCTCATGACTGCATGCTAGCTAGACTGACCGTAGCACRT
> str01: -----T--AG-TAG-T-AG--A---CTC--C-G--G-A-AG-T--GA-CA---A-AC----C--C--T---GA--A---A----A-GA---ATG--G---AT-A----A----A--TA---T-A-----------
> str02: ------G--G--A--T-A---A--AC--A-C--TC---C--C---GA--A---A-A-TAA---T---T--TGACT--T-A----A--A--CA--ACGC----GAC---A-G-T---T---C--A----AG-----
> str03: A----T--A-C-----C--T--T--C-C-T-AG--GTA-A-C-A--A--A-C----C-AA-C--CA--ACT---T--T----T---GAT-C-T--C--T--TG--T--A-G--A--T---CTG------------
> str04: -----T--A---A-AT---T-AT-A---ATC--T--TA----TAC--T-AG-TA-A--AAA----A-TA--G----G---G-T---G-T--A--AC-C----GA----A----A---A--C-G---GT--C----
> str05: -----T-TA---A-A--A--CA-G-C-C-T--GT-G----G----G-T----T-G-C-A--C--C----C--ACT---CA-C--A-G--G---G-C-C-CA---CTG---G---GC--G-C--A----AG-----
> str06: A----TG-A-CT---TC---CA--A-T-----G--G-A----T-C---C--C-A-AC----C-TCA--A--G-CT--TC--C--A-----C----C-C-CA--A-TG---G-T---T----T--C---AGC----
> str07: AA-C----A---A-A-C---CA--AC-CA--A--C-T-----T----T----T-GA-T---C-TC--T--TG--TAG--A--TC-TG-T---T--C--TC-T-A----A----A-C--GA---AC----------
> str08: A----TG-A---A-A--A--C--GA---A--A-----A----T----T-A--T----TA----TCA--A--G----G---G-T-ATG--G-A--A-G-T---G---G-A----AGCT-GAC-GA----A--A--T
> str09: A--C-T----C--G----G-C-TG-C--AT--G-C-T-----TA-G-T--GC-A--CT---C---A---C-G-C-AGT-A--T-A--AT---T-A-----AT-A----A--CTA---A---T-----TA------
> str10: -----T-T-G-TAGATC--T---G--T--TC--TC-TA-A---ACGA--A-CT----T-----T-A--A---A--A-TC---T---G-TG--TG--GCT---G--T-CA--CT--C-------------------
> str11: ------G---C-AGA---G-CAT---T--T---TC-TA-A--TA---TC--C-A--C-AAA----A-T---GA--AG---GC--A--AT--A--A---T--TG--T--A--CTA-CT---C--------------
> str12: A----TG-AGC-----CA---A-GA-TC--C-G----AC-G--A--A---G--AG-C----C--C----C--A--AG---G---A-G--G-A-GA-----A-G---G-A-G---G---GAC---CC----C-C--
> str13: -----T----CT----CA--CA-G--T--TCA-----A--G--A--A-C--C----C-AAA-GT-A---C---C----C--C-C------CAT-A-GC-C----CT-C-T--TA---A-A--G-CC--A-C----
> str14: A-----G--G-T---T---T-AT-AC-C-T---TC---C---TA-G----G-TA-AC-AAAC--CA--AC---C-A---A-CT--T--T-C--GA---TC-T--CT---TG-TA---------------------
> str15: A-----G--G-T---T---T-AT-AC-C-T---TC---C--C-A-G----G-TA-AC-AAAC--CA--AC---C-A---A-CT--T--T-C--GA---TC-T--CT---TG-TA---------------------
> str16: -----T--A---A-A--A--CA--ACTCA--A-T---ACA---AC-AT-A---AGA--AAA--TCA--AC-G-C-A---A----A--A---A---C----A---CT-CA--C-A---A-A---------------
> str17: ---CC-G---C-----C---CAT---T--T--G--G----GC---G----GCT---CT---CG--AG--C-GA-TAG-C---TC--G-T-C--GA-----AT--C--C---CT--C--GAC---C--T-------
> str18: A----T--A-C-----C--T--T--C-C--CAG--GTA-A-C-A--A--A-C----C-AA-C--CA--ACT---T--TC-G---AT----C-T--C--T--TG--T--A-G--A--T---CTG------------
> str19: -----T----CT----CA--CA-G--T--TCA-----A--G--A--A-C--CT---C-AA--GTC--T-C---C----C--C-CAT-A-G---G-C-CTC-T---T---T-C-AG-T---C--A--G--------
> str20: ------G-A--T----C--TC-T--CTCA-C---CG-A-A-C--C--T--G---G-C----C--C----C-G----G---GC--A--A---ATG-C-C-C-T-A----AT-C---C-AGA--G---GT-G-----
> str21: A-----G-AGC-A-ATCAGT---G-C--ATCAG----A-A---A---T-A--TA--C----C-T-A-T--T-A-TA--CA-CT--T--TGC-T-A-----A-GA----AT-------------------------
> str22: AA---T-TA---A-A--A--CAT--CTCA--A-T---ACA---AC-AT-A---AGA--AAA----A---C--A--A--C-GC--A--A---A--A-----A---C---A--CT--C-A---T-------------
> str23: AAAC--G-A---A---C--T--T---T-A--A-----A-A--T-C--T--G-T-G--T----G---G--CTG--T---CA-CTC--G--GC-TG-C----ATG-CT---T---AG-T-G-C--------------
> str24: A----T--A---A---C--T-A--A-T--T-A--C-T---G-T-CG-T----T-GAC-A---G---G-AC--AC--G--AG-T-A--A--C-T--CG-TC-T-A-T-C-T--T--CT-G----------------
> str25: A----TG-AG-T-G-TCA--C--GA---AT---TC--AC-G-TAC-A--A--T-GA--A--C-T--G----GA-T-GT----TCA-----C--G----T---G---G-A----A--TA-A---------------
> str26: A--CC-GT-G---G----G-C--GA-------G-CG----G-T--GA-C--C--G-------GT--GT-CT---T---C--CT-A-G-TG---G--G-TC----C--CA--C--G-T----TGA----A----R-
> str27: AAA---G--G-T---T---T-AT-AC-C-T---TC---C--C-A-G----G-TA-AC-AAAC--CA--AC---C-A---A-CT--T--T-C--GA---TC-T--CT---TG------------------------
> str28: A-----GTAG-T---TC-G-C----CT-----GT-GT---G--A-G--C---T-GAC-AAAC-T---TA--G--TAGT--G-T--T--TG--TGA-G-----GA-T---T---A---------------------
> str29: -----T-T---TA--T-A--C----CT--TC---C-TA--G----G-T-A---A--C-AAAC--CA--AC---C-A---A-CT--T--T-C--GA---TC-T--CT---TG-TAG--A---T-------------
> str30: A----TG---C--G----GTC--G--TC-TC--TC---C--C--CG----GCT----T-----T---T--T---T--TC--C-C------C--G-CGC-C--G-C-G--T--T-G---G-C-G-CCG-A------
> str31: ------GT-G--A---CA---A--A---A--A--C--A----TA--AT--G---GACT---C--CA--AC--AC----CA--T---G-T-CA--A-GCT--T---T-CA-G---G-TAGAC--------------
> str32: ------GT-G-TA-A---G--A--A---A-CAGT---A-AGC--C---C-G---GA--A---GT--G----G--T-GT----T--T--TGC--GA---T--T---T-C--G--AG---G-C---C-G--G-----
> str33: ------G-AG--A-AT--G--A-G--TC-TCA-T--TAC--C---G--C--C----C-----G---GTACT---TAG-CA----A-G---C-T-A-----AT-A--G--T-C-A-C--G---G-C----------
> str34: A----TGT-G---G-TC-G--ATG-C-CAT--G--G-A--G----G--C--C----C-A--C--CAGT--T--C-A-T----T-A--A-G---G-C--TC----CTG---GC-A--T----T-------------
> str35: A--C--G-AGC--G-T---T--T---T-A--AG--G----GC--C---C-GC--GACT----G-C-G-AC-G----G-C--C--A-----CATG--GC-C----CTG--T---A--T-G--T-------------
> str36: ------G--G-T---T---T-AT-AC-C-T---TC---C--C-A-G----G-TA-AC-AAAC--CA--AC---C-A---A-CT--T--T-C--GA---TC-T--CT---TG-TAG--------------------
> str37: -----TG--G---GA--AGT--T--C-CA--A-----A-AG--A---TCA-C-A-A--AA-C---A---CT-AC----CAG-TCA--A--C----C--T---GA----A-G-TA-C-A--C--------------
> str38: ------G-A---AG--C-GT--T-A---A-C-GT-GT-----T--GA---G---GA--AAA-G--A---C--A---G-C---T--T-A-G---GA-G---A--AC---A----AG--AG-CTG---G--G-----
> str39: A--CC---AGC--G--CA--C-T---TC----G--G--CAGC---G----GC-AG-C-A--C--C--T-C-G----G-CAGC--A-----C----C--TCA-G-C---A-GC-A---A--C--------------
> str40: A----TG--G---GA-CA---A---CT--T-A-T--T-C--CTA---TCA--T-G--T----G-C----C--A--AG--AG-----G-T---T-----T--T-AC--C---C--G---G--TGACC--A------
> str41: -----T-T-G-TAGATC--T---G--T--TC--TC-TA-A---ACGA--A-CT----T-----T-A--A---A--A-TC---T---G-TG--TG--G-T--TG--T-CA--CT--C-------------------
> str42: AA-CC---A---A---C---CA--ACT--T---TCG-A----T-C--TC---T----T----GT-AG-A-T--CT-GT----TC-T----C-T-A-----A--AC-G-A----A-CT----T-----TA------
> str43: ------G--G---G-T---TC-TG-C-CA---G--G--CA--TA-G-TC---T----T-----T---T--T---T--TC---T---G--GC--G--GC-C----CT---TG-T-G-TA-A---ACC-T-G-----
> str44: ------G--GCT-G--CA-T---G-CT--T-AGT-G--CA-CT-C-A-C-GC-AG--TA----T-A--A-T---TA---A--T-A--A--C-T-A-----AT---T--A--CT-G-T------------------
> str45: -----TG---C-A--T--G-C-T---T-A---GT-G--CA-CT-C-A-C-GC-AG--TA----T-A--A-T---TA---A--T-A--A--C-T-A-----AT---T--A--CT-G-T---C-G----T-------
> str46: -----T-T--C-----CA--CA--ACT--T---TC---CA-C--C-A--AGCT---CT----G-CA--A--GA-T---C--C-CA-GA-G--T--C----A-G---G---G---GC----CTG----T-------
> str47: -----T----CTA-A--A--C--GA---A-C--T--T-----TA--A--A---A---T---C-T--GT---G--T-G---GCT---G-T-CA---C--TC--G---GC-TGC-A--T-G-CT-----TAG-----
> str48: A--CC-G--G--A--T--G----G-C-C----G-CG-A----T----T----T----T-----TC-G----GA---GTC--CT--TG--G---G--G-----GAC--CA--CT--C-AGA---A---TAG-A---
> str49: ---C-T-T-G-TAGATC--T---G--T--TC--TC-TA-A---ACGA--A-CT----T-----T-A--A---A--A-TC---T---G-TG--TG--GCT---G--T-CA--CT----------------------
> str50: A----TG-AGC-A---C--T-A--A-------G-CG-A-AG--A--A-C--C-A-A--AAA-G-CAG-AC--A--A-T-A-C--A--A--C----C-C----G-CT--AT--TA-C-------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 135
> best bound: 0.0
> wall time: 2.588287s
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
> --- Solution (of length 49) ---
>   Sol: MESFAPLSYRNQEHVKFDANSCPGVTRSLNHAFIRKGPNEALGYQHDTV
> str01: M---A-LSY------------CP------------KG----------T-
> str02: M----------Q--------S------SLN-A-I---P----------V
> str03: M----PLSY--Q-H--F---------R--------K-------------
> str04: ME----------EHV----N-------------------E-L---HD--
> str05: M-S-------N-----FDA--------------IR-----AL-------
> str06: M--F-----RNQ-------NS-----R--N------G------------
> str07: M--F----Y---------A-----------HAF---G-----GY-----
> str08: M-S------------KF--------TR-------R--P-----YQ----
> str09: M-SF----------V---A----GVT-----A------------Q----
> str10: MES---L-------V-------PG--------F-----NE---------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 49
> best bound: 0.0
> wall time: 0.876143s
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
> --- Solution (of length 876) ---
>   Sol: FFMADEAFDFGHIEIKFDLALNGEEDDIAEFIKKANELPAEGAFLAEKLLEQAAAEIPLKQQREHEIKKLNIDIELAFQQGKARAEFHPRSAEEAFAGIGIKDEKKLDLKMLLDNFDAIPNQRALNSGKILPEQLFNNINIDINRAEHQIILPESHLSSPLTAEGHIIDKKAKLFDAIEIIKLCDDILHMKNGEEGHPKIKQNREKPKQARKLESFLALFKNMLKQLRAEFGGLNKDKPPIRNRTAGCKNGNPRDQPPLASGSGGAIRGIKHIIIVADEFFIIKHKLLPFGFINEKPGDQGDILPPERGILQALMRNPITADAGHIELNPALAEGFQRMKADFPHASEAIELFANLKGNPSIRSLDPMRAGKHDTIKLDPHQLATLDRSGFRTQGVDFFLFILPGDLSDGPQLAKRFSIKGLLMPSGQGPMKLTEINSGIGGSAGSSEKVAAFCGLIGMAFQAEGGEPNSSQCVCDEIEMNFLIPLFNLIRDSTCFGKKLIADLNPEDLDGFRDFIRAHLICLASLHPFQRSLKPTGNQLPLAPARSAWYTNDSAVKLVREGFHTIRGAVDSPQYVLESYPFANDIKTVLPQARNGVEYGKLRDISVFTLYANKDSEITGQPLNRKQLHMACVFTLDRQNGSAVYPEDVFEINLGVRATSLEYPDSLVITFRGAWDSNLEKSTHGVALTNFRIQWYSAENPGIWTDAVRKSLGFMWYDTQSRHPVNMDLGIEKFDCSGAIVYSTILPDEKRCGATDHSPIYEQWLDCKARYFLISMICVSRGDNIFVSQVGESNTPGLWVTERKISYVEANLYQPKHARFRNYGKLTVDSMAYNIVQKAEPVKWLNKCISRAGERSVAKHRTQNYKFIMDGLPTVW
> str01: --M-----------------------------------------------------------R-H----LNIDIE--------------------------------------------------------------------------------------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y---S-----------------S-----------NDIK-------NGV-Y-K---------YA--D---------------A---------------ED-FEI-L------L---------F--A---------------------YS-----I--D------G----------------G-E--------V-------E--C------------LD------L---------------------T-------R-------------------------------------------------------------------------
> str02: --M--E--------------------------------------------------------R--------------------RA--H-R-----------------------------------------------------------------------T---H-----------------------------------QN---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W---D-A---------T---------------------K---P--R---E----R---------------------RKQ-------T---Q--------------------------------------------H-------R-------------------L------T---HP---D------D-S--I-Y----P---R--------I-E-----KA----------------------E----G-----RK----E-------------------D------------------------------H----------G-----
> str03: --M--E--------------------------------P--GAF----------------------------------------------S----------------------------------------------------------------------TA----------LFDA-----LCDDILH--------------R------R-LES----------QLR--FGG------------------------------------------V-----------------------Q--I-PPE----------------------------------------------------------------------------------------V-----------SD-P----R---------------------------------V---------------------------------------------------------------------------------------------------Y----A------G------------Y-------A------L-----------L----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: --M-------G----KF----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y------------------------Y---S----N---------R--------R------L-A--------------------VF--------A--------------------------------------------------Q---A---------------------QSRH-----LG-------G----S-----------------YEQWL---A--------CVS-GD----S---------------------A---------FR----------A-------E-VK--------A--R-V-----Q--K---D------
> str05: FF------------------------------------------------------------RE------N----LAFQQGKAR-EF-P-S-EEA---------------------------RA-NS----P-----------------------------T----------------------------------------------------S------------R-E---L--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W------V---R------RG---------------------------G----------------N--------PL------------------S----E----------A--------------GA-----E-----------R----------------R---G-----T-------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: --M-D---------------------------------P---------------------------------------------------S---------------L------------------------------------------------------T---------------------------------------Q-------------------------------------------------------------------------V--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-----AV----EG---------S---VL-S---A---------A---V------D----T--A----E-T----N------------D---------------------T--E-PD--------------E----G--L--------SAEN-------------------------------E-----G----------E-----T--------------R---I--I---R---I---------T-G--------S----------------------------------------------------------------------
> str07: --MA---FDF--------------------------------------------------------------------------------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V-------------------------------------------T---G----N---------------------------------------------T-KLD-----T---SGF-TQGV-----------S---------S-----M---------T---------------VAA--G--------------------------------------T-----LIADL---------------------------------------------------VK-------T---A--S------S------------Q---------L------T---N---------L-------A-------Q--S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: --MA-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V-----I----L-P---------------------------------------------------------S---------------------------T------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YT-D--------G--T---A-------------A------------------------------------------------C--T----NGS---P-DV------V----------------G---------T-G---T-------------------------MW--------VN-----------------TILP-----G--D---------------F-------------F------------W-T-------------P--------------S----------------------GE-SV---R-------------V-
> str09: --M------------------N-------------------------------------------------------------------------------------------------------------------------------------------T--G-IID----LFD---------------N----H------------------------------------------------------------------------------V-D--------------------------------------------------------------------S--I---------P--------------TI-L-PHQLATLD------------------------------------------------------------------------------------------------------------------------------------------------------------------Y-------LVR----TI-------------------I-----------------D------------E------NR----------------S-V---------L------L---------F------------H--------I---------------------M--------------G------SG------------------------------------------------------------------------------------------------------------------------------------------
> str10: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------N-L-------R--T------------------R----------------------T--QLP--PA----YTN-S--------F-T-RG-V----Y----YP---D-K-V------------------F----------------R----------------S-----------------S-------V----------L----H------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: --M-D-------------------------------------------------------------------------------------S----------K-E---------------------------------------------------------T----I------L---IEII----------------PKIK-------------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y-------L------------------L-------D--T------N---------IS---------------P---K---------------S--Y-------N-----------D-----F---------------------I---S-----------R----------------N------K--------------------------------------------------NIFV-----------------I-----NLY--------N-----V-S-------------------------------T-----I--------
> str12: --M---------------L-L---------------------------------------------------------------------S------G---K--KK----MLLDN--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y----------E---T---A-------------A---------AR-G------R----------------G--------------------G------D--E-----R--------------R-------------------R---------G-W--A------F---D---R-P--------------AIV--T-----KR----D-----------K------S-------D-------------------R---------------------------MA---------------------------H----------------
> str13: --M------------------NGEEDD--------NE--------------QAAAE----QQ---------------------------------------------------------------------------------------------------T-------KKAK------------------------------REKPKQARK---------------------------------------------------------------V-------------------------------------------T--------------------------SEA-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-----------E--H-----------------F--D-------A---------------T-----D---------------------D---G-A---E----------------------------------------------------------------------------------------C-------------K------H-----------------------------------------------------------------------------------------------------------------------
> str14: --M--E------------------------------------------------------------------------------------S---------------L------------------------------------------------------------------------------------------------------------------------------------------------------------------------V------------P-GF-NEK-----------------------T----H----------------------------------------------------------------------V---------------QL----S---L--P------------------------V-----L-----Q-----------V----------------RD---------------------------------------------------------------V-LVR-GF----G--DS---V-E-------------------E--------V--L-----SE-------------A------RQ--------------------------------------------H---L---------------------K-------D-----------G-------------T------------------------------------------------------------------------------------------------------------------------------------
> str15: --M-----------------------------------------------------------R------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y---------------I---V-SPQ--L-----------VL-Q----V--GK------------------GQ-------------------------E-V-E-----RA--L-Y---L--T------------------------------P---------------YD-----------------------Y--I--DEK-------SPIY---------YFL-------R------S----------------------------H--------L-------NI-Q-------------R---------------------P---
> str16: --M-----------------------------------P-----------------------R--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V------------P----------------------------------------------------------------------------------------------------------V---------------------------------------------------------------------------------------------------------------------------------------------------------Y--DS------------------PQ-V--S-P--N---TV-PQAR-------L---------A------T--P-------------------S-------F-------AT----P-----TFRGA-D----------A-------------P-----A------F-----Q-------D---------------T---------A-----------------------------N----Q------------------------Q---AR-----------------Q---------------------------------------
> str17: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------N-L-------R--T------------------R----------------------T--QLPLA------YTN-S--------F-T-RG-V----Y----YP---D-K-V------------------F----------------R----------------S-----------------S-------V----------L----H------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---FF------------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------N-L----------T-----------------------------------------T---------R----T----------------------Q--L---P---------P-A-----Y---------T---N--S-----------------FT--R--G--VY-----------------YPD---------------K----V----FR----S-------------S-------------V---L---------------------------HS----------------------------------------------------------------------------------------------------------------------
> str19: --M--EA-----I-I---------------------------------------------------------------------------S----FAGIGI-------------N--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y------K-----------------------------K--L-Q-------------S-------K--------L---Q-H-------D------------F----G-R----------V----------L-K-----ALT------------------V----------T-------------------A-----------R--A----------L------------------------------PG----------------QPKH-----------------I---A---------I-R-----------Q-------------
> str20: --MA--------------------------------------------------------------------------------------S-----------------------------------SG---PE-----------RAEHQIILPESHLSSPL------------------------------------------------------------------------------------------------------------------V-------KHKLL---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y------------------------Y---------------------------------------------------------------------------------------------------W-----K------LT------------G---------L-----------P----L-----------------PDE--C---D---------------F----------D---------------------------------H--------L--------I-----------------------------------------
> str21: --M--E------------------------------------------------------------------------------------S---------------L------------------------------------------------------------------------------------------------------------------------------------------------------------------------V------------P-GF-NEK-----------------------T----H----------------------------------------------------------------------V---------------QL----S---L--P------------------------V-----L-----Q-----------V----------------RD---------------------------------------------------------------V-LVR-GF----G--DS---V-E-------------------E--------V--L-----SE---------------V----RQ--------------------------------------------H---L---------------------K-------D-----------G-------------T------------------------------------------------------------------------------------------------------------------------------------
> str22: --M---------------LA------------------P---------------------------------------------------S----------------------------PN-----S-KI---QLFNNINIDIN---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y----------E--HT-----------L--Y-FA----------------------SV--------S--------------A-------QN-S-------F--------------------F--A-------------------QW------------V----------------V----------------YS----------A-D-----------KA----I------------------------------------------------------------------------------------------------------
> str23: --M---------------------------------------------------------------------------------------SA------I--------------------------------------------------------------T-E--------------------------------------------------------------------------------T---K---P------------------------------------------------------------------T-----IEL-PALAEGFQR-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y-N----K-------T-------P----------------------G-----------FT----------------------CV--LDR------Y--D-----------------------------------HGV------I------N-----D----S---------------------K------IV----L--------------Y----------------------N--------------------------------------------------------------------------------------------
> str24: --M------------K-----N-----IAEF-KKA---P-E---LAEKLLE--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------------------------------------------------------------------S-------NLKGN-S-RSLDPMRAGKHD---------------------V-----------------------------------------------------V-----------------------V---IE-------------ST---KKL----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: --M-----------------------------------P------------Q-----PLKQ-----------------------------S---------------LD-------------Q----S-K-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W--------L-RE-------A--------E--------K-----------------------------------------H------L-R----A----------L-------E---SLV-------DSNLE------------------E--------------------------------EK------------L---K--------P---Q-L---------SM-----G---------E------------------------------------D------VQ------------S--------------------------
> str26: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------N-LI---------T------------------R----------------------T--Q-------S--YTN-S--------F-T-RG-V----Y----YP---D-K-V------------------F----------------R----------------S-----------------S-------V----------L----H------------S-------T--------------Q-------D----------------------------------------------------------------------------------------------------------------------------------------------------
> str27: --M------------KFD-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V----------L-----------------------------------------------------------S----LFA-----P--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-----A-K-V-----------D------E-------------Q-----EY----D----------------Q-----QL-----------N------------N------------------------NLE-S----------I-----------T-A----------------P--------KFD------------D----GAT------E-----------I-----------------ES--------ER--------------------G----D-----I-----------------------------------------
> str28: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------NF-----------T----------N-------R----------------------T--QLP-----SA-YTN-S--------F-T-RG-V----Y----YP---D-K-V------------------F----------------R----------------S-----------------S-------V----------L----H------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: --M-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W----S-----------I-------------------I--VL----------KL--IS-----------I--QPL----L-------L-------V--------------TSL--P--L----------------------------Y---NP------------------------NMD--------S--------------C--------------C-----LIS-----R---I---------TP-----E---------L-----A-----GKLT----------------W----I-----------------FI--------
> str30: --M--E------------------------------------------------------------------------------------S---------------L------------------------------------------------------------------------------------------------------------------------------------------------------------------------V------------P-GF-NEK-----------------------T----H----------------------------------------------------------------------V---------------QL----S---L--P------------------------V-----L-----Q-----------V----------------RD---------------------------------------------------------------V-LVR-GF----G--DS---V-E-------------------E---------F-L-----SE-------------A------RQ--------------------------------------------H---L---------------------K-------D-----------G-------------T------------------------------------------------------------------------------------------------------------------------------------
> str31: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV-----M----PLFNLI---T-----------------------------------------T--------------T----------------------Q----SY-------T------N------------FT---------------R---------------G--VY-----------------YPD---------------K----V----FR----S-------------S-------------V---L---------------------------H-------L---------------------------------------------------------------------------------------------------------------
> str32: --M--------H---------------------------------------Q----I--------------------------------------------------------------------------------------------------------T-----------------------------------------------------------------------------------------------------------------V-----------------------------------------------------------------------------------------------------------------------V-----------S-GP----------------------TE--------------V-------------------S-----------------------TCFG---------------------------SLHPFQ-SLKP--------------------V-------------------------------------------------------------------------MA--------N--A----------LGV----LE----------G-------K---------------------------------M------------------F-CS--I------------G----------------------------G--------------------R--S-----L----------------------------------------------------------------
> str33: --MA-------------------------------------------------------------------------------------------------------------------------------------------------------------T-----------L--------L--------------------R----------S-LALFK------R------NKDKPPI---T---------------SGSGGAIRGIKHIIIV------------P---I---PGD-----------------------------------------------S-------------SI------------T---------T--RS--R----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: --M--E------------------------------------------------------------------------------------S---------------L------------------------------------------------------------------------------------------------------------------------------------------------------------------------V------------P-GF-NEK-----------------------T----H----------------------------------------------------------------------V---------------QL----S---L--P------------------------V-----L-----Q-----------V----------------RD---------------------------------------------------------------V-LVR-GF----G--DS---------------------------------------------------------M----------------E---E----V----L----S-------------E------A----R-Q----------------------------H-----L---K-D--G-----T------------------------------------------------------------------------------------------------------------------------------------
> str35: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------N-L----------T-----------------------------------------TG-------------T----------------------Q--L---P---------P-A-----Y---------T---N--S-----------------FT--R--G--VY-----------------YPD---------------K----V----FR----S-------------S-------------V---L---------------------------HS----------------------------------------------------------------------------------------------------------------------
> str36: --MA-----------------N-----I---I---N-L------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W--N---------G---I---V--P--------------------------------------------------------M--V-----Q--------DV---N--V-A-S--------IT---A----------------F------------------KS---M---------------I---D-------------E-----T--------W-D-K-----------------------------------KI---EAN---------------T--------------------CISR-------KHR--N------------
> str37: --M---------------L--N----------------------------------------R---I-----------Q----------------------------------------------------------------------------------T-----------L---------------MK-----------------------------------------------------TA---N-N---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y----------E---TI-----------E-------I---L---RN---Y--LR------LY------I---------------------------------I-L---A-------------R-----N-E------------------E--G------R---G-----------------I--------------L-------------IY----D----------------DNI-------------------------------------------DS-----V----------------------------------------
> str38: --MAD---------------------------------PA-G-----------------------------------------------------------------------------------------------------------------------T-----------------------------NGEEG------------------------------------------------T-GC-NG---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-------------F-----------YV-E----A-----V-------VE--K------------K----TG----------------D-----A--------I-------S----D----------D---E---------N--------EN-----D----S------DT----------G-E--D----------L--------------------------------V---D---------------------------------------------------------------------------------------------
> str39: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV------N-L-------R--T------------------R----------------------T--QLP--P--S--YTN-S--------F-T-RG-V----Y----YP---D-K-V------------------F----------------R----------------S-----------------S-------V----------L----H------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: --M--E------------------------------------------------------------------------------------S---------------L------------------------------------------------------------------------------------------------------------------------------------------------------------------------V------------P-GF-NEK-----------------------T----H----------------------------------------------------------------------V---------------QL----S---L--P------------------------V-----L-----Q-----------VCD-------------------------------------------------------------------------------V-LVR-GF----G--DS---V-E-------------------E--------V--L-----SE-------------A------RQ--------------------------------------------H---L---------------------K-------D-----------G-------------T------------------------------------------------------------------------------------------------------------------------------------
> str41: --M------------------N-------------N---------------Q----------R----KK--------------------------------------------------------------------------------------------TA----------------------------------------R--P-------SF-----NMLK--RA------------RNR-------------------------------V----------------------------------------------------------------------S---------------------------T--------------------V-----------S---QLAKRFS-KGLL--SGQGPMKL----------------V--------MAF-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: --M---------------------------------------------------------------------------------------S-----------------------NFDAI---RAL------------------------------------------------------------------------------------------------------------------------------------------------------V-D-----------------------------------------T-DA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y------KL---G-H-I--------------------------------------------------------------HM--------------YPE-------G---T--EY----V----------L--S-------NF-------------TD--R---G-------SR--------IE-----G--V--T------------H-------------------------------------T----V----------------H-----------------------------------------------------------
> str43: --M---------IE----L-------------------------------------------R-HE-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V-----------------------QGD-L-------------------------------------------------------------------------------------------V-------------------------------------T-IN------------V-----------------------V--E----------------T-----------PEDLDGFRDFIRAHLICLA-------------------------------V--------------D----------------T---------E----------T---------TG--L-------------D--------------I----------Y---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: --M----F---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V---F------L------------------------------------------------------------------------------------------------------------V---L--LP--L------------------------------------------V-------------------SSQCV-----M----PLFNLI---T-----------------------------------------T-NQ-------S--YTN-S--------F-T-RG-V----Y----YP---D-K-V------------------F----------------R----------------S-----------------S-------V----------L----H------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: --M---------------------------------------------------------------------------------------S----------KD---L------------------------------------------------------------------------------------------------------------------------------------------------------------------------VA------------------------------R---QALM----TA----------------RMKADF----------------------------------------------------V-FFLF------------------------------------------------V-----L--------------------------------------------------------------------------------------------W-------K-----------A-------L-S----------LP-----V------------------------P------------T--R-------------------------------------------------------------------------------------------------C--------------------------Q----------I--------D-----------------------------------------------MA-----K----K-L----S-AG-----------------------
> str46: --MA--------------------------------------------------------------------------------------S---------------L-LK----------------S---L------------------------------T-----------LF------K---------------------R----------------------------------------T--------RDQPPLASGSGGAIRGIKH---V-----II----------------------------------------------------------------------------------------------------------------V---L-I-PGD-S---------SI------------------------------V-------------------------------------------T------------------R-----------S-----R---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: --M-----------------------------------------------------------R--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V-------------------------------RGIL----RN---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W------------------------Q-----------------Q----------------------------------------------------------------------------------W-------------------W-------IWT-----SLGF-W----------M------F-----------------------------------------MIC-S------V--VG--N---LWVT------V----Y---------YG---V------------PV-W--K------E---AK--T-----------T--
> str48: --MA-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------V--E---------PF------P----------R-------R-PIT-----------------R-----PHAS--IE--------------------------------------------VD------------------------------------T---SGIGGSAGSSEKV--FC-LIG---QAEGGEPN------------------------T-------------------------------------------------------------V--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: --M----F-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y----A--------H----A------------F-------------G---G----------Y---D-E------N---LH-A--F-----------P--------G-------------I-------S----ST--VA--N---------------D-VRK------Y---S---V---------------V-S-----------------------------------V---------------------------Y---N----K--------K-------YNIV-K-------NK-----------------Y---M------W
> str50: --MA-----------------N-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y---S--K---------------P--------F-------L-----------L-DI-VF----NKD--I-------K-----C-------------------IN-----------DS---------------------------------------------------------------------CS-------------------HS-------DC--RY-----------------Q---SN-----------SYVE--L------R-RN--------------Q-A-----LNK----------------N-------L----
> 
> example file name: 'protein_n050k050.txt'
> best objective: 876
> best bound: 0.0
> wall time: 55.273526s
> ```
