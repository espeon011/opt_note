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
>  Sol: itkgnkuojiqfolevanbzcghxbimxcnprdvxycdnsbhoucstqovpgvoxzrvisnpsbxnpgfilps
> str1: -tkgnku---------------h---m---p---x---n--h----tq---g--xz-v------x----i--s
> str2: i------ojiqfol---nb----x---xc----v-----s---u---q--p-v-----is--sbx---f----
> str3: ------u------l------c----i---n-----yc-----o--s--ov---o-z-----p----p---lp-
> str4: i--g----------eva--z-g--b------rd----d--b---cs---v------rv--n----n-gf----
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 73
> best bound: 0.0
> wall time: 0.52s
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
> --- Solution (of length 114) ---
>  Sol: pigenboyplrczxujiqfolcdevjtdcvwxqkgnerdpazgbrkuhmqvigpxnlyctodfzshtmxcvsudbqprovicsvgoxzrvpxcqdsvbnnpgxfbilwdehops
> str1: --------------------------t------kgn---------kuhm----pxn---------ht--------q--------g-xz-v-x-------------i-------s
> str2: -i----o--------jiqfol--------------n-------b----------x-------------xcvsu--qp--vi-s------------s-b----xf----------
> str3: --------------u-----lc-----------------------------i---n-yc-o---s-------------ov-----o-z--p---------p-----l-----p-
> str4: -ige--------------------v---------------azgbr----------------d-----------db------csv----rv--------nn-g-f----------
> str5: p------yplr-zxu------c-----------------p--------mqv-g------t-df---------u-------i--v--------c-ds-b-------------o--
> str6: p----b----------------dev--dcv--------dp----------------------fzs--m---s--b--ro--------------q--vb------b-----h---
> str7: ---enb-----cz-----f------jt--v-x----er---z-br-----vigp--l----------------------------------------------------e----
> str8: ----------r--x----------------wxqk---rd-----r-----------l-ctod----tm--------pr------------px---------------wd-----
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 114
> best bound: 0.0
> wall time: 1.73s
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
> --- Solution (of length 171) ---
>   Sol: krixuwslxqpkfchtxojiqafnypxlrzbdevkgnxudcfpevabdigqovjzqcewbscvzfkuhmpoglnbrxjtvxcoqvsifzlcgtdsmdbakneuqcspvbrezhkodtqivnsbwangfuivcdmprsbxtfvimgqpzjowhlkvxwrdmblgizcepsuy
> str01: ---------------t------------------kgn----------------------------kuhmp------x-----------------------n-----------h---tq--------g-----------x--------z------vx-------i----s--
> str02: --i--------------ojiq-f----------------------------o--------------------lnb-x---xc--vs----------------uq--pv----------i--s--------------sbx-f------------------------------
> str03: ----u--l-----c-----i---ny---------------c----------o--------s---------o--------v--o-----z-----------------p---------------------------p-----------------l--------------p---
> str04: --i--------------------------------g-------eva--------z----------------g--br-----------------d--db------cs-v-r---------vn----ngf-------------------------------------------
> str05: ----------p-------------yp-lrz-------xu-c-p-------------------------m--------------qv------gtd---------------------------------fuivcd---sb-----------o---------------------
> str06: ----------p-------------------bdev-----dc---v--d---------------------p-----------------fz-----sm---------s--br----o--q-v--b--------------b-------------h-------------------
> str07: --------------------------------e---n---------b---------c------zf------------jtvx--------------------e-------r-z----------b------------r-----vi-g-p-----l-------------e----
> str08: -r-x-w--xq-k----------------r--d-------------------------------------------r-------------lc-t---------------------odt----------------mpr----------p--------xw-d------------
> str09: k----------k--------qaf-------------------------igq--j----w-----------o----------------------------k-------------k-------s-------------------------------k---r--blg--------
> str10: -------lx-------x--------p-------------------ab-i---v------b--vz-k----o-----------------z----------------------z-------v------------d--------------------------------------
> str11: kri---------f-----------------------------------------------s-------------------------------------a--------v------------n----------cd------------q----wh------------zc-----
> str12: ---------q-----------a----x-----------ud---------gq-v--qcewb----f------g--------------i-------------------------------------------------------------jow-----w-------------y
> str13: -r----s-xq--------j----n-----------------fp--a-di-----------------u------------------si----------------q----b-ezhko------------------------------------h-------m--g--------
> str14: --i--ws-------h------------------v---------------------------------h-------------co------------m----------------------i---------u-v-d-------------------------dm-----------
> str15: --------------htx---------x-----------------------q--jzq---b-c----------------t------------------bakn----------------------------------------------------------------------
> str16: ---xu-s-----fc--------f------z------------pe-------------e---cv------------------------------------------------------------wan-------------tf--mgq-z---------------------u-
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 171
> best bound: 0.0
> wall time: 5.77s
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
> wall time: 0.20s
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
> wall time: 0.56s
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
> wall time: 0.15s
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
> --- Solution (of length 132) ---
>   Sol: ATGACGTCAGATCAGTCATGACATGCTATCGATCGTACAGCTAGCTAGACTCATGCAGTACGTCAGTACTGACTAGACTCAGATCAGTCGAGTCACTGCGATTGACTACGACGTGCATGACATGCAGCTGAR
> str01: -T-A-GT-AG-T-AG--A---C-T-C---CG---G-A-AG-T-G--A--C--A---A--AC--C----CTGA--A-A---AGA--A-T-G-G--A-T---A---A--A-----T--AT-A------------
> str02: --G--G--A--T-A---A--ACA--CT--C---C---C-G--A---A-A---AT--A--A--T---T--TGACT----T-A-A--A--C-A---AC-GCGA----C-A-G---T---T--CA---AG-----
> str03: AT-AC--C---T---TC----C-T---A--G---GTA-A-C-A---A-AC-CA---A---C--CA--ACT---T----T----T--G---A-TC--T-C--TTG--TA-GA--T-C-TG-------------
> str04: -T-A----A-AT---T-AT-A-AT-CT-T--AT---AC---TAG-TA-A---A---A--A----A-TA--G----G-----G-T--GT--A---AC--CGA---A--A--ACG-G--T--C-----------
> str05: -T----T-A-A--A---A---CA-GC---C--T-GT---G---G---G--T--TGCA---C--C----C--ACT---C--A---CAG--G-G-C-C--C-A----CT--G--G-GC--G-CA---AG-----
> str06: ATGAC-T----TC---CA--A--TG-----GATC---C--C-A---A--C-C-T-CA--A-G-C--T--T--C----C--A---C---C----C-C----A---A-T--G--GT---T----T-CAGC----
> str07: A--AC---A-A--A--C----CA----A-C---C--A-A-CT---T----T--TG-A-T-C-TC--T--TG--TAGA-TC---T--GT----TC--T-C--T--A--A--ACG---A--AC-----------
> str08: ATGA----A-A--A--C--GA-A----A---AT--TA----T---TA---TCA---AG---G---GTA-TG----GA---AG-T--G--GA---A--GC--T-GAC---GA-----A--A--T---------
> str09: A---C-TC-G----G-C-TG-CATGCT-T--A--GT---GC-A-CT---C--A--C-G--C---AGTA-T-A--A---T----T-A----A-T-A-----A----CTA--A--T---T-A------------
> str10: -T----T--G-T-AG--AT--C-TG-T-TC--TC-TA-A---A-C--GA---A--C--T---T---TA---A--A-A-TC---T--GT-G--T----G-G-----CT--G---T-CA---C-T-C-------
> str11: --G-C---AGA---G-CAT----T--T-TC--T---A-A--TA--T---C-CA--CA--A----A--A-TGA--AG-----G--CA----A-T-A-----ATTG--TAC----T--A---C-T-C-------
> str12: ATGA-G-C----CA---A-GA--T-C---CGA-CG-A-AG--AGC----C-C---CA--A-G---G-A--G----GA----GA--AG--GAG-----G-GA----C--C--C---C----C-----------
> str13: -T--C-TCA---CAGT--T--CA----A--GA----AC--C---C-A-A---A-G---TAC--C----C---C----C-CA--T-AG-C----C-CT-C--TT-A--A--A-G--C----CA--C-------
> str14: A-G--GT----T---T-AT-AC---CT-TC---C-TA--G---G-TA-AC--A---A--AC--CA--AC---C-A-ACT----T---TCGA-TC--T-C--TTG--TA------------------------
> str15: A-G--GT----T---T-AT-AC---CT-TC---C---CAG---G-TA-AC--A---A--AC--CA--AC---C-A-ACT----T---TCGA-TC--T-C--TTG--TA------------------------
> str16: -T-A----A-A--A--CA--AC-T-C-A---AT---ACA---A-C-A---T-A---AG-A----A--A---A-T---C--A-A-C-G-C-A---A-----A---A--AC-AC-T-CA---CA---A----A-
> str17: ----C--C-G--C---C----CAT--T-T-G---G----GC--G---G-CTC-T-C-G-A-G-C-G-A-T-A---G-CTC-G-TC-G---A---A-T-C------C--C----T-C--GAC---C---T---
> str18: AT-AC--C---T---TC----C---C-A--G---GTA-A-C-A---A-AC-CA---A---C--CA--ACT---T----TC-GATC--TC---T---TG---T--A----GA--T-C-TG-------------
> str19: -T--C-TCA---CAGT--T--CA----A--GA----AC--CT--C-A-A-----G---T-C-TC----C---C----C-CA--T-AG--G---C-CT-C--TT---T-C-A-GT-CA-G-------------
> str20: --GA--TC---TC--TC-T--CA--C---CGA----AC--CT-G---G-C-C---C----CG---G----G-C-A-A---A--T--G-C----C-CT---A---A-T-C--C----A-GA---G--G-TG--
> str21: A-GA-G-CA-ATCAGT---G-CAT-C-A--GA----A-A--TA--TA--C-C-T--A-T---T-A-TAC--ACT----T----T--G-C---T-A-----A--GA--A-----T------------------
> str22: A--A--T----T-A---A--A-A--C-ATC--TC--A-A--TA-C-A-AC--AT--A--A-G--A--A---A--A-AC--A-A-C-G-C-A---A-----A---A--AC-AC-T-CAT--------------
> str23: A--A----A---C-G--A--AC-T--T-T--A----A-A---A--T---CT---G---T--GT--G----G-CT-G--TCA---C--TCG-G-C--TGC-AT-G-CT------T--A-G---TGC-------
> str24: AT-A----A---C--T-A--A--T--TA-C--T-GT-C-G-T---T-GAC--A-G--G-AC---A---C-GA---G--T-A-A-C--TCG--TC--T---AT---CT------T-C-TG-------------
> str25: ATGA-GT--G-TCA--C--GA-AT--T--C-A-CGTACA---A--T-GA---A--C--T--G---G-A-TG--T----TCA---C-GT-G-G--A-----AT--A--A------------------------
> str26: A---C--C-G-T--G----G----GC----GA--G--C-G---G-T-GAC-C--G--GT--GTC--T--T--C----CT-AG-T--G--G-GTC-C--C-A----C---G---T---TGA-A---------R
> str27: A--A----AG----GT--T----T---AT--A-C---C---T---T---C-C---CAG---GT-A--AC--A--A-AC-CA-A-C---C-A---ACT----TT--C---GA--T-C-T--C-T-----TG--
> str28: A-G---T-AG-T---TC--G-C---CT---G-T-GT---G--AGCT-GAC--A---A--AC-T---TA--G--TAG--T--G-T---T----T----G---T-GA----G--G---AT----T--A------
> str29: -T----T----T-A-T-A---C---CT-TC---C-TA--G---G-TA-AC--A---A--AC--CA--AC---C-A-ACT----T---TCGA-TC--T-C--TTG--TA-GA--T------------------
> str30: ATG-CG---G-TC-GTC-T--C-T-C---C---C---C-G---GCT----T--T----T---T---T--T--C----C-C----C-G-CG---C-C-GCG-TTG-----G-CG--C----C--G-A------
> str31: --G---T--GA-CA---A--A-A----A-C-AT---A-A--T-G---GACTC---CA--AC---A---C---C-A---T--G-TCA----AG-C--T----TT--C-A-G--GT--A-GAC-----------
> str32: --G---T--G-T-A---A-GA-A----A-C-A--GTA-AGC---C----C----G--G-A----AGT---G----G--T--G-T---T----T---TGCGATT---T-CGA-G-GC----C--G--G-----
> str33: --GA-G--A-AT--G--A-G---T-CT--C-AT--TAC--C--GC----C-C--G--GTAC-T---TA--G-C-A-A----G--C--T--A---A-T---A--G--T-C-ACG-GC----------------
> str34: ATG---T--G----GTC--GA--TGC---C-AT-G----G--AG---G-C-C---CA---C--CAGT--T--C-A---T----T-A----AG-----GC--T---C--C----TG---G-CAT-----T---
> str35: A---CG--AG--C-GT--T----T--TA---A--G----G---GC----C-C--GC-G-AC-T--G--C-GAC--G-----G--C---C-A--CA-TG-G-----C--C--C-TG--T-A--TG----T---
> str36: --G--GT----T---T-AT-AC---CT-TC---C---CAG---G-TA-AC--A---A--AC--CA--AC---C-A-ACT----T---TCGA-TC--T-C--TTG--TA-G----------------------
> str37: -TG--G---GA--AGT--T--C---C-A---A----A-AG--A--T---C--A--CA--A----A--AC--ACTA--C-CAG-TCA----A--C-CTG--A---A----G---T--A---CA--C-------
> str38: --GA----AG--C-GT--T-A-A--C----G-T-GT-----T-G--AG------G-A--A----A--A--GAC-AG-CT----T-AG--GAG--A-----A----C-A--A-G---A-G-C-TG--G--G--
> str39: A---C--CAG--C-G-CA---C-T--T--CG---G--CAGC--G---G-C--A-GCA---C--C--T-C-G----G-C--AG--CA--C----C--T-C-A--G-C-A-G-C----A--AC-----------
> str40: ATG--G---GA-CA---A---C-T--TAT---TC---C---TA--T---C--ATG---T--G-C----C--A--AGA----G----GT----T---T----T--AC--C--CG-G--TGAC---CA------
> str41: -T----T--G-T-AG--AT--C-TG-T-TC--TC-TA-A---A-C--GA---A--C--T---T---TA---A--A-A-TC---T--GT-G--T----G-G-TTG--T-C-AC-T-C----------------
> str42: A--AC--CA-A-C---CA--AC-T--T-TCGATC-T-C---T---T-G--T-A-G-A-T-C-T--GT--T--CT---CT-A-A--A--CGA---ACT----TT-A---------------------------
> str43: --G--G---G-T---TC-TG-C---C-A--G---G--CA--TAG-T---CT--T----T---T---T--T---T---CT--G----G-CG-G-C-C--C--TTG--T--G---T--A--A-A--C--CTG--
> str44: --G--G-C---T--G-CATG-C-T--TA--G-T-G--CA-CT--C-A--C----GCAGTA--T-A--A-T---TA-A-T-A-A-C--T--A---A-T----T--ACT--G---T------------------
> str45: -TG-C---A--T--G-C-T----T---A--G-T-G--CA-CT--C-A--C----GCAGTA--T-A--A-T---TA-A-T-A-A-C--T--A---A-T----T--ACT--G---T-C--G---T---------
> str46: -T----TC----CA--CA--AC-T--T-TC---C--AC--C-A---AG-CTC-TGCA--A-G--A-T-C---C----C--AGA---GTC-AG-----G-G---G-C--C----TG--T--------------
> str47: -T--C-T-A-A--A--C--GA-A--CT-T---T---A-A---A---A---TC-TG---T--GT--G----G-CT-G--TCA---C--TCG-G-C--TGC-AT-G-CT------T--A-G-------------
> str48: A---C--C-G----G--ATG----GC---CG--CG-A----T---T----T--T----T-CG---G-A--G--T---C-C---T---T-G-G-----G-G---GAC--C-AC-T-CA-GA-AT--AG---A-
> str49: ----C-T----T--GT-A-GA--T-CT---G-T--T-C---T--CTA-A---A--C-G-A----A---CT---T----T-A-A--A----A-TC--TG---T-G--T--G--G--C-TG---T-CA-CT---
> str50: ATGA-G-CA---C--T-A--A---GC----GA----A--G--A---A--C-CA---A--A----A--A--G-C-AGAC--A-AT-A--C-A---AC--C------C---G-C-T--AT----T--A-C----
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 132
> best bound: 0.0
> wall time: 2.02s
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
> --- Solution (of length 50) ---
>   Sol: MEQSKFPLSYVALRNQEHAFPGVNSTRDAIRYCPKGEYFNLQAHDEGLTV
> str01: M----------AL-----------S------YCPKG------------T-
> str02: M-QS----S---L-N---A----------I---P---------------V
> str03: M-----PLSY-----Q-H-F------R-------K---------------
> str04: ME--------------EH----VN------------E---L--HD-----
> str05: M--S----------N----F-------DAIR-----------A----L--
> str06: M----F-------RNQ-------NS-R------------N------G---
> str07: M----F---Y-A-----HAF-G-------------G-Y------------
> str08: M--SKF-------------------TR---R--P---Y---Q--------
> str09: M--S-F----VA---------GV--T--A------------Q--------
> str10: ME-S---L--V---------PG----------------FN-----E----
> 
> example file name: 'protein_n010k010.txt'
> best objective: 50
> best bound: 0.0
> wall time: 0.80s
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
> --- Solution (of length 462) ---
>   Sol: MAFVESFLVLLPLNRVSGKFDSQCVNPLAIEKRTHVQALSLRPEFTYIVSLQVKTAPGNLRDMTPHQILWAFSKVLRDNIEVQLPAGYTSIDVGPLAYTENSFTRQGIVKASFNYDEGTQPNLIKHACDSVENIKLQGRYTNVPDSKLFEVTARGFSPILNMVYLKRGAHWQDLSETVNARYPEFAQDTISLKPVRAEHNLSTPGDESFCITGLARVYNFSRKQLTPDSMARNKFGWIAYDEVLWISTFVRGQHLARKDYVLTAEGRPAGSVLENIVSWTKHLPIDFSLGVYEQPIDSKAMRTNKIYECSPDGLAFWEHSLDCRYIVDTGEKNQSFDACLISNRSFVTDPIEGMFRMICSVGDSAQYVEGNLWVTPRIEVYKLGDSHANDVSFRKPMAEVKLGYDTGVIEHNQARLSVTKMLITCPVWKYAGEDLQRVSAKDNMGYALTIFKHRQSNLGIPT
> str01: M-------------R-------------------H---L-------------------N--------I---------D-IE-------T--------Y---S---------S-N-D-------IK-------N----G----V--------------------Y-K---------------Y---A-D--------AE-------D--F--------------------------------E---I--------L------L------------------------F------------A------Y--S---------------I-D-G----------------------G---------------E----V----E---------------------------------------------C---------L------D-----LT----R--------
> str02: M---E---------R-----------------R----A---------------------------H----------R-----------T------------------------------------H----------Q----N----------------------------W-D------A--------T---KP-R-E-----------------R-----RKQ-T--------------------------QH--R----LT------------------H-P-D----------DS-------IY---P------------R-I----EK-----A-------------EG--R-------------------------K----------------E-----D-----H--------------------G------------------------------
> str03: M---E------P-----G----------A---------------F----S----TA---L-----------F-----D-------A---------L-------------------------------CD---------------D-------------IL---------H----------R--------------R----L-----ES---------------QL------R--FG---------------G--------V--------------------------------Q-I--------------P--------------------------------------P-E--------V--S--------------------D----------P------------------R--V-----------YAG-------------YAL---------L----
> str04: M----------------GKF--------------------------Y----------------------------------------Y-S----------N---R---------------------------------R--------L----A---------V---------------------FAQ---------A--------------------------Q----S--R---------------------HL----------G---GS--------------------YEQ----------------------W---L----------------AC-------V------------S-GDSA---------------------------FR---AEVK------------AR--V-----------------Q----KD--------------------
> str05: --F---F-------R---------------E---------------------------NL----------AF----------Q----------------------QG--KA---------------------------R----------E-----F-P----------------SE-------E-A---------RA--N-S-P-------T--------SR-------------------E-LW----VR-----R--------G---G----N--------P----L--------S---------E------A--------------G-------A-------------E---R--------------------R------G---------------------T--------------------------------------------------------
> str06: M-------------------D-----P------------SL----T-----QV----------------WA---V-----E-----G--S--V--L-----S--------A---------------A---V-------------D------TA----------------------ET-N--------DT--------E-----P-DE-----GL------S---------A----------E--------------------------------N-----------------E-------------------G----E----------T--------------R------I------I------------------RI---------------------------TG---------S---------------------------------------------
> str07: MAF-----------------D-----------------------F----S--V-T--GN----T---------K-L-D----------TS---G--------FT-QG-V--S-----------------S-------------------------------M--------------TV-A-----A------------------G------T-L-----------------------IA-D--L-----V-------K----TA------S------S---------------Q-------------------L--------------T---N------L------------------------AQ-------------------S----------------------------------------------------------------------------
> str08: MA-V-------------------------I--------L---P------S----T--------------------------------YT--D-G----T-----------A---------------AC------------TN------------G-SP--------------D----V----------------V---------G------TG------------T---M------W-----V-------------------------------N----T----I---L-----P-----------------G--------D-------------F---------F--------------------------W-TP---------S----------------G------E------SV------------------RV------------------------
> str09: M------------N-------------------T-----------------------G---------I-----------I-----------D---L------F------------D-----N---H----V-------------DS------------I-----------------------P-----TI-L-P----H------------------------QL-----A----------------T------L---DY-L---------V-----------------------------RT--I-------------------I-D--E-N----------RS-V------------------------L----------L---------F-----------------H-----------I--------------------MG----------S--G---
> str10: M-FV--FLVLLPL--VS----SQCVN-L----RT-------R---T-----Q-------L----P-------------------PA-YT-----------NSFTR-G-V-----Y------------------------Y---PD-K---V----F----------R-------S---------------S---V-----L----------------------------------------------------H----------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M-------------------DS---------K-----------E-T-I--L----------------I------------E---------I----------------I------------P---K--------IK----------S-----------------YL--------L-------------DT----------N----------I---------S-----P------K------------S------------Y--------------N----------DF--------I-S---R-NK---------------------------N-------I----FV---I-------------------NL--------Y-------N-VS-------------T--I-----------------------------------------------------
> str12: M------L-L------SGK------------K---------------------K--------M-----L------L-DN--------Y-----------E---T------A---------------A-------------------------ARG-----------RG------------------------------------GDE--------R-----R---------R---GW-A---------F---------D-------RPA------IV--TK--------------------R---------D-------------------K--S-D------R---------M----------A---------------------H---------------------------------------------------------------------------
> str13: M------------N---G------------E------------E-----------------D---------------DN-E-Q--A----------A-------------A-----E--Q----------------Q---T-----K------------------K--A-----------------------K--R-E------------------------K---P------K------------------Q--ARK--V-T-------S--E-------------------------A----------------WEH----------------FDA---------TD-------------D------G-----------------A----------E-------------------------C---K-----------------------H---------
> str14: M---ES-LV--P-----G-F-----N----EK-THVQ-LSL-P-----V-LQV-------RD------------VL-----V----------------------R-G-----F----G----------DSVE-----------------EV--------L--------------SE---AR-----Q-----------H-L---------------------K----D-------G-----------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-------------R-------------------------------YIVS------P---------Q-L-----VL------Q---------VG---------------K-------G-Q-----------E----------V------E---R--------------A----L-------Y---------L----------TP-------------Y---------D-----------Y-----I------------D-----E---------------K------S------PI----------Y-----------------Y----------F---L---RS-----------------------------------------H--------------L---------N----------I------------QR-----------------------P-
> str16: M----------P--RV----------P--------V----------Y--------------D----------S-----------P--------------------Q--V--S--------PN------------------T-VP---------------------------Q-------AR----------L----A-----TP---SF-----A----------TP--------------------TF-RG---A--D----A---PA-----------------F------Q--D-----T-----------A-----------------NQ-------------------------------Q---------------------A-----R------------------Q-------------------------------------------------
> str17: M-FV--FLVLLPL--VS----SQCVN-L----RT-------R---T-----Q-------L----P---L-A----------------YT-----------NSFTR-G-V-----Y------------------------Y---PD-K---V----F----------R-------S---------------S---V-----L----------------------------------------------------H----------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FV--F------------F----V--L----------L---P-------L-V-------------------S----------------S---------------Q---------------------C--V-N--L----T----------T-R----------------------T---------Q----L-P---------P----------A--Y-------T------N-------------S-F-------------T---R--G-V-------------------Y--------------Y---PD-------------------K--------------V-------FR---S---S---V---L--------------H----S----------------------------------------------------------------------
> str19: M---E-----------------------AI-----------------I-S---------------------F-------------AG---I--G-------------I-----NY---------K---------KLQ--------SKL-----------------------Q--------------------------H------D--F---G--RV-------L--------K----A----L---T-V------------TA--R-A---L----------P-----G---QP---K-------------------H------I-----------A--I--R---------------------Q------------------------------------------------------------------------------------------------
> str20: MA---S----------SG--------P---E-R----A-----E---------------------HQI-----------I---LP--------------E-S-----------------------H---------L---------S----------SP-L--V--K---H----------------------K-------L------------L---Y---------------------Y----W------------K---LT--G------L----------P----L-----P-D----------EC--D---F-----D----------------------------------------------------------------H--------------L------I-----------------------------------------------------
> str21: M---ES-LV--P-----G-F-----N----EK-THVQ-LSL-P-----V-LQV-------RD------------VL-----V----------------------R-G-----F----G----------DSVE-----------------EV--------L--------------SE-V--R-----Q-----------H-L---------------------K----D-------G-----------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L--------------------A-------------P------S------P-N-------------SK-----I--QL------------------F----------N-------N-I--------NI----------D-------------I-N--Y-----------E----------------------H---T----------L---Y-F----------A---------------S--V--------------------S----------------------------A---------------------------------Q--------N-SF--------F---------AQ------WV-----VY----S-A-D----K--A----------I-----------------------------------------------------
> str23: M----S----------------------AI---T---------E-T-------K--P------T---I------------E--LPA---------LA--E------G-----F------Q------------------RY-N----K----T-----P---------G----------------F---T--------------------C------V-------L--D---R-------YD------------H-----------G-----V---I---------------------------N-------D-------S-----------K--------I-----V------------------------L--------Y-------N-------------------------------------------------------------------------
> str24: M-----------------K------N---I-------A-----EF--------K-------------------K-----------A--------P----E----------------------L---A----E--KL-----------L-EV----FS---N---LK-G----------N-----------S----R-----S-----------L-------------D---------------------------------------P--------------------------------MR------------A--------------G-K------------------------------------------------------H--DV--------V-------VIE------S-TK--------K-----L---------------------------
> str25: M----------P----------Q---PL---K----Q--SL--------------------D----Q-----SK------------------------------------------------------------------------------------------------W--L------R--E-A-----------E------------------------K------------------------------HL-R------A--------LE---S----L-------V-----DS-----N---------L---E------------E--------------------E-----------------------------KL-----------KP----------------Q--LS---M----------GED---V----------------QS------
> str26: M-FV--FLVLLPL--VS----SQCVN-L-I---T-------R---T-----Q--------------------S--------------YT-----------NSFTR-G-V-----Y------------------------Y---PD-K---V----F----------R-------S---------------S---V-----L----------------------------------------------------H----------------S--------T-------------Q--D---------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-----------------KFD---V--L-----------SL---F----------AP------------WA--KV--D--E-Q----------------E--------------YD---Q----------------Q----------L------------N-----------------N--------------------NL-----ES--IT--A-----------P------KF-----D-----------------D------G--A----------T------------E--I-----------E-S-------E-----R-----G------D---I-------------------------------------------------------------------------------------------------------------------------
> str28: M-FV--FLVLLPL--VS----SQCVN------------------FT------------N-R--T--Q-L---------------P----S------AYT-NSFTR-G-V-----Y------------------------Y---PD-K---V----F----------R-------S---------------S---V-----L----------------------------------------------------H----------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M--------------------------------------------------------------------W--S------I----------I-V--L-------------K------------LI-----S---I--Q------P---L-----------L----L------------V----------T-SL-P------L----------------YN-------P-----N-------------------------------------------------------------------M----------D-------S--C---------------CLIS-R------I-----------------------TP--E---L----A--------------G----------------K-L-T---W---------------------IF--------I--
> str30: M---ES-LV--P-----G-F-----N----EK-THVQ-LSL-P-----V-LQV-------RD------------VL-----V----------------------R-G-----F----G----------DSVE-----------------E-----F---L--------------SE---AR-----Q-----------H-L---------------------K----D-------G-----------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FV--FLVLLPL--VS----SQCV-------------------------------------M-P---L--F------N----L------I-------T----T--------------TQ---------S---------YTN------F--T-RG-------VY-----------------YP----D----K-V-------------F------R----S-------S-------------VL---------HL---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M---------------------------------H-Q----------I------T-------------------V------V-------S---GP---TE--------V--S------T--------C--------------------F-----G-S--L---------H------------P-F-Q---SLKPV----------------------------------MA-N-----A----L-------G--------VL--EG--------------K-------------------M--------------F------C-----------S-----I-----------G--------G--------------R--------S---------------L------------------------------------------------------------
> str33: MA-------------------------------T----L-LR-------SL----A---L-----------F-K--R-N------------------------------K-----D--------K------------------P-------------PI-----------------T-------------S-------------G--S----G----------------------G--A------I----RG-----------------------I----KH--I----------I---------I--------------------V----------------------PI------------------------P-------GDS-----S----------------I---------T----T------------R-S--------------R--------
> str34: M---ES-LV--P-----G-F-----N----EK-THVQ-LSL-P-----V-LQV-------RD------------VL-----V----------------------R-G-----F----G----------DS-------------------------------M-------------E-------E----------V-----LS----E-------AR-------Q-----------------------------HL--KD------G-------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FV--FLVLLPL--VS----SQCVN-L-----T-----------T-----------G-----T--Q-L---------------P---------P-AYT-NSFTR-G-V-----Y------------------------Y---PD-K---V----F----------R-------S---------------S---V-----L----------------------------------------------------H----------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA-----------N---------------I-----------------I----------NL---------W--------N-------G---I-V-P------------------------------------------------------------------MV--------QD----VN---------------V-A----S--------IT--A----F--K-----SM-------I--DE-----T------------------------------W------D------------K-----KI-E------A-----------------N--------------T----------C------------------I-------S-------RK---------------H---R---------------------------N-------------------
> str37: M------L-----NR--------------I------Q--------T----L-----------M----------K--------------T-------A---N------------NY-E-T----I-------E-I-L--R--N---------------------YL-R------L-------Y-------I--------------------I--LAR--N----------------------E----------------------EGR--G-----I------L-I------Y----D--------------D--------------------N-------I-------D----------SV-----------------------------------------------------------------------------------------------------
> str38: MA------------------D-----P-A----------------------------G-----T--------------N-------G------------E----------------EGT------------------G-----------------------------------------------------------------------C--------N----------------GW-----------F----------YV---E---A--V----V---------------E-----K-----K-----------------------TG------DA--IS------D-------------D-----E-N-------E---------ND-S------------DTG--E-----------------------DL--V---D--------------------
> str39: M-FV--FLVLLPL--VS----SQCVN-L----RT-------R---T-----Q-------L----P-------------------P----S-------YT-NSFTR-G-V-----Y------------------------Y---PD-K---V----F----------R-------S---------------S---V-----L----------------------------------------------------H----------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M---ES-LV--P-----G-F-----N----EK-THVQ-LSL-P-----V-LQV--------------------------------------------------------------------------CD-V----L------V----------RGF-----------G----D-S--V-----E-------------E------------------V-------L---S------------E-------------AR------------------------------------Q------------------------H-L----------K----D---------------G---------------------T---------------------------------------------------------------------------------------
> str41: M------------N-----------N----------Q----R-----------K-------------------K--------------T-------A-------R---------------P--------S------------------F-----------NM--LKR-A-----------R------------------N---------------RV---S----T----------------V---S-----Q-LA-K--------R-------------------FS----------K-------------GL------L-------------S-----------------G------------Q---G-----P--------------------M---KL-----V------------M---------A-------------------F-----------
> str42: M----S-------N-----FD-------AI--R----AL---------V------------D-T-------------D-------A-Y---------------------K------------L--------------G-------------------------------H-------------------I--------H------------------------------M---------Y---------------------------P-----E---------------G------------T----E----------------Y-V------------L-SN--F-TD------R-----G-S------------RIE----G------V--------------T----H-------T-------V-------------------------H---------
> str43: M----------------------------IE-------L--R-----------------------H--------------EVQ---G----D---L------------V---------T----I--------N---------V-------V------------------------ET-----PE---D---L-------------D------G------F-R-----D------F--I------------R----A-------------------------HL-I-----------------------C----LA-----------VDT-E----------------T--------------------------T--------G-----------------L--D---I--------------------Y--------------------------------
> str44: M-FV--FLVLLPL--VS----SQCV-------------------------------------M-P---L--F------N----L------I-------T----T---------N-----Q---------S---------YTN---S--F--T-RG-------VY-----------------YP----D----K-V-------------F------R----S-------S-------------VL---------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M----S------------K-D------L-------V-A---R---------Q---A---L--MT------A-----R------------------------------------------------------------------------------------M---K--A---D-----------F---------V-------------F----------F----L---------F-------VLW------------K-----A--------L----S----LP------V---P-------T--------------------R--------------C--------------------------Q-----------I------D-----------MA--K------------------K-L----------------SA----G-----------------
> str46: MA---S-L-L--------K--S-----L-----T----L-----F--------K------R--T------------RD----Q-P---------PLA----S----G----S-----G-------------------G--------------A-----I-------RG---------------------I--K-----H-----------------V--------------------I-------I---V----L--------------------I-------P-----G------DS-----------S---------------IV-T--------------RS----------R----------------------------------------------------------------------------------------------------------
> str47: M-------------RV----------------R------------------------G---------IL-------R-N-------------------------------------------------------------------------------------------WQ--------------Q-------------------------------------------------W-------WI--------------------------------WT-------SLG-------------------------FW------------------------------------MF-MICSV------V-GNLWVT----VY----------------------Y--GV-----------------PVWK---E------AK-------T------------T
> str48: MA-VE------P-------F------P-----R--------RP----I------T-----R---PH----A-S------IEV---------D------T--S----GI---------G-------------------G-------S------A-G-S-----------------SE----------------K-V-------------FC---L-----------------------I-------------GQ--A--------EG---G---E---------P-------------------N------------------------T-----------------V-------------------------------------------------------------------------------------------------------------------
> str49: M-F-------------------------------------------Y--------A---------H----AF--------------G------G---Y-----------------DE----NL--HA---------------------F--------P---------G---------------------IS----------ST-------------V-------------A-N-------D-V-------R------K-Y----------SV----VS------------VY-----------NK--------------------------K----------------------------------Y---N------I-V-K------N-----K--------Y----------------M------W----------------------------------
> str50: MA-----------N--------------------------------Y--S---K--P--------------F---L-------L-------D---------------IV---FN----------K---D----IK--------------------------------------------------------------------------CI-------N--------DS-------------------------------------------------------------------------------CS--------HS-DCRY--------QS-------N-S---------------------YVE--L----R----------------R-----------------NQA-L--------------------------N--------K----NL----
> 
> example file name: 'protein_n050k050.txt'
> best objective: 462
> best bound: 0.0
> wall time: 32.57s
> ```
