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
Model = scsp.model.wmm.Model
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
> --- Solution (of length 75) ---
>  Sol: iojiqtfgkegolnvakublzcghxbimxcnprdvxycdnsbhoucsqtovpqgviorxzvsnpsbxnpgfilps
> str1: -----t--k-g--n--ku-----h---m---p---x---n--h-----t---qg----xzv-----x----i--s
> str2: iojiq-f----oln----b-----x---xc----v-----s---u--q---p--vi-----s--sbx---f----
> str3: -----------------u-l-c----i---n-----yc-----o--s--ov-----o--z---p----p---lp-
> str4: i------g-e----va----z-g--b------rd----d--b---cs---v------r--v-n----n-gf----
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 75
> best bound: 0.0
> wall time: 0.001414s
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
> --- Solution (of length 128) ---
>  Sol: pioyjpbilrdeqtxfgknwzxubcevgolndcqkazbfpruvdghmpxjbrinqtvxcflcdgtdvyzscoebhmsrucdtqfzbrovpsviguimprvoxzpcqvxsdsbnnplbgiwxfdehops
> str1: -------------t---k---------g--n---k------u---hmpx----n--------------------h------tq----------g-------xz---vx----------i--------s
> str2: -io-j--i----q--f------------oln------b----------x--------xc-------v--s--------u---q------p-vi---------------s-sb--------xf------
> str3: ----------------------u------l--c-------------------in-------------y--co----s----------ov-----------o-zp----------pl----------p-
> str4: -i--------------g--------ev--------az-------g-----br----------d--d-------b-----c----------sv------rv------------nn---g---f------
> str5: p--y-p--lr----------zxu-c--------------p------m-------q-v------gtd-----------------f----------ui---v----c----dsb-------------o--
> str6: p-----b---de--------------v----dc---------vd---p-----------f--------zs-----ms--------bro-----------------qv----b----b-------h---
> str7: -----------e------n----bc-----------z-f----------j-----tvx--------------e----r------zbr-v---ig---p-----------------l-------e----
> str8: ---------r----x----w-x-----------qk-----r--d-------r--------lc--t------o--------dt--------------mpr----p---x-----------w--d-----
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 128
> best bound: 0.0
> wall time: 0.003027s
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
> --- Solution (of length 176) ---
>   Sol: iprxuskwxqklrojiqfaxcfigenbdyczpevfolrsazxudcpgahvtdqbjinvbxxqcekvwgnkuhmpscovqtvxfzklrdcgtdobfuiqwenhsmzpvcsbrdtizjavzqbgrvniesksmptzcfhkorbxjmgqpzvluxotbwvdahngbdmfikweghnpsy
> str01: --------------------------------------------------t-------------k--gnkuhmp-------x------------------nh----------t------q-g-------------------x-----zv--x--------------i-------s-
> str02: i------------ojiqf-----------------ol-------------------n-bxx-c--v--------s--------------------u-q-------pv------i-------------s-s----------bx-----------------------f----------
> str03: ----u------l--------c-i--n--yc-----o--s-------------------------------------ov--------------o-----------zp-------------------------p-----------------l-----------------------p--
> str04: i----------------------ge--------v-----az-----g------b--------------------------------rd---d-b-------------cs--------v----rvn-----------------------------------ng---f----------
> str05: -p--------------------------y--p----lr--zxu-cp--------------------------m-----q-v--------gtd--fui---------vc---d---------------s------------b-----------o-----------------------
> str06: -p------------------------bd----ev---------dc----v-d---------------------p--------fz------------------sm----sbr---------------------------o------q--v-----b-------b--------h----
> str07: ------------------------enb--cz---f-------------------j------------------------tvx-----------------e----------r---z-----b-rv-i------------------g-p--l-------------------e------
> str08: --rx---wxqk-r--------------d---------r-----------------------------------------------l--c-t-o------------------dt-----------------mp-------r------p----x---w-d------------------
> str09: ------k---k-----q-a--fig----------------------------q-j-----------w---------o-------k-------------------------------------------ks-------k-rb--------l-----------g--------------
> str10: -----------l-------x---------------------x---p-a-----b-i-vb------v-----------------zk-------o-----------z---------z--v---------------------------------------d------------------
> str11: ------k-----r--i-f--------------------sa---------v------n-----c------------------------d---------qw--h--z--c--------------------------------------------------------------------
> str12: ---------q--------ax----------------------ud--g-----q----v---qce--w--------------------------bf--------------------------g---i----------------j---------o--w------------w------y
> str13: --r--s--xq----j----------n--------f----------p-a---d---i--------------u---s---------------------iq-----------b----------------e------z--hko--------------------h----m-----g-----
> str14: i------w------------------------------s---------hv---------------------h---co--------------------------m---------i------------------------------------u-----vd-----dm-----------
> str15: ------------------------------------------------h-t--------xxq-----------------------------------------------------j--zqb-------------c------------------tb---a--------k----n---
> str16: ---xus-----------f--cf--------zpe------------------------------e-----------c-v--------------------w-----------------a-------n-------t--f-------mgq-z--u-------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 176
> best bound: 0.0
> wall time: 0.005835s
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
> --- Solution (of length 32) ---
>   Sol: bdcabcdebeaecdaebcdebdcdbeabdade
> str01: -dc-bc------cd--bc----c--e------
> str02: bd----d-be-e---e---ebd----------
> str03: --ca-cde-e--c--eb--e------------
> str04: ---a---e-----d----d--d-d-e-bd-d-
> str05: ---a-c--be-ec-a-bc-e------------
> str06: b---b-----a-----b--ebdc-b-a-----
> str07: b---b-----ae--aeb---------a-da--
> str08: -------e-e-e---e-c--bd--be-----e
> str09: --c--cde-e---da---d---cd--------
> str10: bd-ab-d-bea---a---d-------------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 32
> best bound: 0.0
> wall time: 0.000222s
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
> --- Solution (of length 37) ---
>   Sol: daecbdeacbedacebadecbadebacdebacdebbd
> str01: d--cb---c----c---d--b-----c----c-e---
> str02: ----bd-----d---b--e----e----e----eb-d
> str03: ---c---ac--d--e---ec---eb---e--------
> str04: -ae--d-----d-----d----deb--d----d----
> str05: -a-cb-e---e--c--a---b-----c-e--------
> str06: ----b----b--a--b--e-b-d---c--ba------
> str07: ----b----b--a-e-a-e-bad--a-----------
> str08: --e---e---e---e----cb-d-b---e----e---
> str09: ---c----c--d--e---e---d--a-d---cd----
> str10: ----bd-a-b-d---b--e--a---a-d---------
> str11: --e--de----da---a----a-e-a----a------
> str12: -a-----a--e-a---a---b--e----e-ac-----
> str13: --e----a----a--b---c-a----c----cd-b--
> str14: ----bde---e-a----de--ade-------------
> str15: ---c---a--eda----de----e----e---d----
> str16: --e-b---c---a----d--ba--b----b---e---
> str17: d----d--c-e---e-a---b-de-a-----------
> str18: da--b---c--d-----de--a-e--c----------
> str19: -a-----a---d-ce---e---d--a----a---b--
> str20: -ae---e-c----ce---e----e-a----a------
> str21: ----b----b-da-e----c-a---a-de--------
> str22: da-c--e----da-e--d---a--b------------
> str23: -a-----a--e-a--b----b---b----b-c-e---
> str24: d-e--d---b---c-b---c-a---a---b-------
> str25: d---bd-a----a-eb----b-----c--b-------
> str26: d-e-b-e----d---b--e-ba----c----------
> str27: ---c--e---e----b---c--d---c--b--de---
> str28: d---b-e----da---ad---a---a---b-------
> str29: ---c----c----c---d-cb--eb--d---c-----
> str30: -ae---eac--d---b---cb-d--------------
> str31: da-cb-eac----c-----c--d--------------
> str32: --ec--e--b---c-----c--d-b--d-b-------
> str33: d----d---b-----b---c---e---d--a---bb-
> str34: -a-----a--e-a--ba----a-eba-----------
> str35: --ecb----b---c--a----ad---cd---------
> str36: d-e-b---c----ce----c--d-b-c----------
> str37: da-----acb--a-e---e-b-----c----------
> str38: -a---d-a-be-a---a--c------c-e--------
> str39: daec-d---b--ac--a----a---------------
> str40: da-cb----b-d-ce--d-c-----------------
> str41: d-e--d---be---eb----b-de-------------
> str42: ---c-d-a---d-c---d-c--d--a----a------
> str43: ---c--e---ed-c-ba-e----e---d---------
> str44: ---c--ea--e--c--a----a---ac---a------
> str45: d--c----c----ceb----b---ba-d---------
> str46: ----b--a--e---e-a-e-b---b--de--------
> str47: d---bde--b--ac-----c--d-b------------
> str48: --e-b---cbe---e--d---a-e-a-----------
> str49: -ae---e---e----b----b-d-b-c---a------
> str50: d---bd-a-b---ce----cb---b------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 37
> best bound: 0.0
> wall time: 0.00071s
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
> --- Solution (of length 26) ---
>   Sol: TATCGACGTAAGACTAGTCATCGATC
> str01: -AT-G--G---GA-TA--C---G---
> str02: -AT--AC------CT--TC--C---C
> str03: ---C-ACG-AA---T--T----GA--
> str04: TA---A---AA---T---C-T-G-T-
> str05: -A--G--GTAA--C-A---A---A--
> str06: T-TC--C-TA-G----GT-A------
> str07: T-T-G---TA-GA-T---C-T-----
> str08: T---G--G---GA--AGT--TC----
> str09: T-TC--C--A---C-A---A-C--T-
> str10: T--C----TAA-AC--G--A---A--
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 26
> best bound: 0.0
> wall time: 0.000162s
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
> --- Solution (of length 146) ---
>   Sol: ATGACTGACTAGATCAGTCATACGTCATCATGCTAGACTAGCTAGCTACAGTCAGACTACGATCACTGACATGACTGACATAGCTACGTACTGCATGACTGCATGCATGACTGACTGACTGCACTGACAGATCGTAGTACAGTAGR
> str01: -T-A--G--TAG-T-AG--A--C-TC--C--G---GA--AG-T-G--ACA---A-AC--C---C--TGA-A--A---A----G--A---A-TG---GA-T--A---A--A-T-A-T-A----------------------------
> str02: --G---GA-TA-A--A--CA--C-TC--C---C--GA--A---A---A---T-A-A-T----T---TGAC-T---T-A-A-A-C-A---AC-GC--GAC---A-G--T---T--C--A----A--G--------------------
> str03: AT-AC---CT---TC---C-TA-G-------G-TA-AC-A---A---AC---CA-AC--C-A--ACT----T---T----T-G--A--T-CT-C-T---TG--T--A-GA-T--CTG-----------------------------
> str04: -T-A---A--A--T---T-ATA----ATC-T--TA---TA-CTAG-TA-A---A-A--A--AT-A--G----G---G---T-G-TA---AC--C--GA----A---A--AC-G---G--T-C------------------------
> str05: -T---T-A--A-A--A--CA---G-C--C-TG-T-G----G---G-T----T--G-C-AC---C-C--AC-T--C--ACA--G----G----GC----C--CA--C-TG---G---G-C-GCA---A--G----------------
> str06: ATGACT---T----C---CA-A--T------G---GA-T--C---C--CA---A--C--C--TCA---A---G-CT----T--C--C--AC--C----C--CA---ATG---G--T---T----T--CAG--C-------------
> str07: A--AC--A--A-A-C---CA-AC--CA--A--CT----T---T---T---G--A---T-C--TC--T----TG--T-A----G--A--T-CTG--T---T-C-T-C-T-A---A---AC-G-A---AC------------------
> str08: ATGA---A--A-A-C-G--A-A----A--AT--TA---T---TA--T-CA---AG-----G------G---T-A-TG-----G--A---A--G--TG---G-A---A-G-CTGAC-GA----A---A----T--------------
> str09: A---CT--C--G----G-C-T--G-CAT---GCT----TAG-T-GC-AC--TCA--C---G--CA--G---T-A-T-A-AT---TA---A-T--A--ACT--A---AT---T-A--------------------------------
> str10: -T---TG--TAGATC--T-----GT--TC-T-CTA-A--A-C--G--A-A--C----T----T---T-A-A--A---A--T--CT--GT---G--TG---GC-TG--T--C--ACT--C---------------------------
> str11: --G-C--A---GA---G-CAT---T--T--T-CTA-A-TA--T--C--CA--CA-A--A--AT----GA-A-G---G-CA-A--TA---A-T---TG--T--A--C-T-ACT--C-------------------------------
> str12: ATGA--G-C-----CA---A---G--ATC---C--GAC--G--A---A--G--AG-C--C---C-C--A-A-G---GA----G----G-A--G-A--A--G---G-A-G---G---GAC--C-C---C----C-------------
> str13: -T--CT--C-A---CAGT--T-C---A--A-G--A-AC---C---C-A-A---AG--TAC---C-C---C----C---CATAGC--C---CT-C-T---T--A---A--A--G-C---C---AC----------------------
> str14: A-G---G--T---T---T-ATAC--C-T--T-C----CTAG---G-TA-A--CA-A--AC---CA---AC----C--A-A---CT---T--T-C--GA-T-C-T-C-T---TG--T-A----------------------------
> str15: A-G---G--T---T---T-ATAC--C-T--T-C----C---C-AG-----GT-A-AC-A--A--AC---CA--AC---CA-A-CT---T--T-C--GA-T-C-T-C-T---TG--T-A----------------------------
> str16: -T-A---A--A-A-CA---A--C-TCA--AT---A--C-A---A-C-A---T-A-A----GA--A---A-AT--C--A-A---C---G--C---A--A----A---A--AC--ACT--C---AC--A-A-A---------------
> str17: ----C---C--G--C---C---C---AT--T--T-G----G---GC----G---G-CT-C--TC---GA---G-C-GA--TAGCT-CGT-C-G-A--A-T-C---C----CT--C-GAC--C--T---------------------
> str18: AT-AC---CT---TC---C---C---A----G---G--TA---A-C-A-A---A--C--C-A--AC---CA--ACT----T---T-CG-A-T-C-T--CT---TG--T-A--GA-T--CTG-------------------------
> str19: -T--CT--C-A---CAGT--T-C---A--A-G--A-AC---CT--C-A-AGTC----T-C---C-C---C----C--A--TAG----G--C--C-T--CT---T---T--C--A--G--T-CA--G--------------------
> str20: --GA-T--CT----C--TC-T-C---A-C---C--GA--A-C---CT---G---G-C--C---C-C-G----G---G-CA-A---A--T---GC----C--C-T--A--A-T--C---C---A--GA--G---GT-G---------
> str21: A-GA--G-C-A-ATCAGT-----G-CATCA-G--A-A--A--TA--TAC---C----TA---T---T-A--T-AC--AC-T---T---T---GC-T-A----A-G-A--A-T----------------------------------
> str22: A--A-T---TA-A--A---A--C---ATC-T-C-A-A-TA-C-A---ACA-T-A-A----GA--A---A-A--AC--A-A---C---G--C---A--A----A---A--AC--ACT--C---A-T---------------------
> str23: A--A---AC--GA--A--C-T---T--T-A----A-A--A--T--CT---GT--G--T--G------G-C-TG--T--CA---CT-CG----GC-TG-C---ATGC-T---T-A--G--TGC------------------------
> str24: AT-A---ACTA-AT---T-A--C-T------G-T---C--G-T---T---G--A--C-A-G------GACA---C-GA----G-TA---ACT-C--G--T-C-T--AT--CT---T--CTG-------------------------
> str25: ATGA--G--T-G-TCA--C----G--A--AT--T---C-A-C--G-TACA---A---T--GA--ACTG----GA-TG---T---T-C--AC-G--TG---G-A---AT-A---A--------------------------------
> str26: A---C---C--G-T--G------G-------GC--GA---GC--G-----GT--GAC--CG------G---TG--T--C-T---T-C---CT--A-G--TG---G---G--T--C---C--CAC-G-----T--T-G-A-A----R
> str27: A--A---A---G----GT--T---T-AT-A--C----CT---T--C--C---CAG-----G-T-A---ACA--A---AC----C-A---AC--CA--ACT---T---T--C-GA-T--CT-C--T------T-G------------
> str28: A-G--T-A---G-T---TC----G-C--C-TG-T-G--T-G--AGCT---G--A--C-A--A--ACT----T-A--G---TAG-T--GT--T---TG--TG-A-G---GA-T---T-A----------------------------
> str29: -T---T---TA--T-A--C---C-T--TC---CTAG----G-TA---ACA---A-AC--C-A--AC---CA--ACT----T---T-CG-A-T-C-T--CT---TG--T-A--GA-T------------------------------
> str30: ATG-C-G----G-TC-GTC-T-C-TC--C---C----C--G---GCT----T-----T----T---T----T---T--C----C--C---C-GC--G-C--C--GC--G--T---TG---GC---G-C----CG-A----------
> str31: --G--TGAC-A-A--A---A-AC---AT-A----A---T-G---G--AC--TC---C-A--A-CAC---CATG--T--CA-AGCT---T--T-CA-G---G--T--A-GAC-----------------------------------
> str32: --G--TG--TA-A---G--A-A----A-CA-G-TA-A---GC---C--C-G---GA--A-G-T----G----G--TG---T---T---T--TGC--GA-T---T---T--C-GA--G---GC-C-G---G----------------
> str33: --GA--GA--A--T--G--A---GTC-TCAT--TA--C---C--GC--C---C-G-----G-T-ACT----T-A--G-CA-AGCTA---A-T--A-G--T-CA--C--G---G-C-------------------------------
> str34: ATG--TG----G-TC-G--AT--G-C--CATG---GA---G---GC--C---CA--C--C-A-----G---T---T--CAT---TA---A--G---G-CT-C---C-TG---G-C--A-T----T---------------------
> str35: A---C-GA---G--C-GT--T---T--T-A----AG----G---GC--C---C-G-C---GA-C--TG-C--GAC-G-----GC--C--AC---ATG---GC---C----CTG--T-A-TG---T---------------------
> str36: --G---G--T---T---T-ATAC--C-T--T-C----C---C-AG-----GT-A-AC-A--A--AC---CA--AC---CA-A-CT---T--T-C--GA-T-C-T-C-T---TG--T-A--G-------------------------
> str37: -TG---G----GA--AGT--T-C--CA--A----A-A---G--A--T-CA--CA-A--A--A-CACT-AC----C--A----G-T-C--A----A---C--C-TG-A--A--G--T-AC---AC----------------------
> str38: --GA---A---G--C-GT--TA----A-C--G-T-G--T---T-G--A--G---GA--A--A--A--GACA-G-CT----TAG----G-A--G-A--AC---A---A-GA--G-CTG---G----G--------------------
> str39: A---C---C-AG--C-G-CA--C-T--TC--G---G-C-AGC--G-----G-CAG-C-AC---C--T--C--G---G-CA--GC-AC---CT-CA-G-C---A-GCA--AC-----------------------------------
> str40: ATG---G----GA-CA---A--C-T--T-AT--T---C---CTA--T-CA-T--G--T--G--C-C--A-A-GA--G-----G-T---T--T---T-AC--C---C--G---G--TGAC--CA-----------------------
> str41: -T---TG--TAGATC--T-----GT--TC-T-CTA-A--A-C--G--A-A--C----T----T---T-A-A--A---A--T--CT--GT---G--TG---G--T---TG--T--C--ACT-C------------------------
> str42: A--AC---C-A-A-C---CA-AC-T--T--T-C--GA-T--CT--CT----T--G--TA-GATC--TG---T---T--C-T--CTA---A----A---C-G-A---A---CT---T---T--A-----------------------
> str43: --G---G----G-T---TC-T--G-C--CA-G---G-C-A--TAG-T-C--T-----T----T---T----T---T----T--CT--G----GC--G---GC---C----CT---TG--TG---T-A-A-A-C------C--T-G-
> str44: --G---G-CT-G--CA-T-----G-C-T--T---AG--T-GC-A-CT-CA--C-G-C-A-G-T-A-T-A-AT---T-A-ATA---AC-TA----AT---T--A--C-TG--T----------------------------------
> str45: -TG-C--A-T-G--C--T--TA-GT------GC-A--CT--C-A-C----G-CAG--TA---T-A---A--T---T-A-ATA---AC-TA----AT---T--A--C-TG--T--C-G--T--------------------------
> str46: -T---T--C-----CA--CA-AC-T--T--T-C----C-A-C---C-A-AG-C----T-C--T----G-CA--A--GA--T--C--C---C---A-GA--G--T-CA-G---G---G---GC-CTG-----T--------------
> str47: -T--CT-A--A-A-C-G--A-AC-T--T--T---A-A--A---A--T-C--T--G--T--G-T----G----G-CTG---T--C-AC-T-C-G---G-CTGCATGC-T---T-A--G-----------------------------
> str48: A---C---C--G----G--AT--G-------GC----C--GC--G--A---T-----T----T---T----T--C-G-----G--A-GT-C--C-T---TG---G---G---G---GAC--CACT--CAGA----A-TA--G-A--
> str49: ----CT---T-G-T-AG--AT-C-T------G-T----T--CT--CTA-A---A--C---GA--ACT----T---T-A-A-A---A--T-CTG--TG--TG---GC-TG--T--C--ACT--------------------------
> str50: ATGA--G-C-A---C--T-A-A-G-C-----G--A-A---G--A---AC---CA-A--A--A--A--G-CA-GAC--A-ATA-C-A---AC--C----C-GC-T--AT---T-AC-------------------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 146
> best bound: 0.0
> wall time: 0.002805s
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
> --- Solution (of length 57) ---
>   Sol: MSFEAPLSYQEHVANFRKSFLNSDHALQNTVCPGFRAIRPVESGKGTALRNYHQDEG
> str01: M---A-LSY----------------------CP-----------KGT----------
> str02: M--------Q--------S---S---L-N-------AI-PV----------------
> str03: M----PLSYQ-H---FRK---------------------------------------
> str04: M--E------EHV-N--------------------------E------L---H-D--
> str05: MS------------NF-------D-A-----------IR--------AL--------
> str06: M-F-------------R----N-----QN-------------S------RN-----G
> str07: M-F-----Y----A----------HA--------F--------G-G-----Y-----
> str08: MS---------------K-F---------T-----R--RP-----------Y-Q---
> str09: MSF---------VA-------------------G------V-----TA-----Q---
> str10: M--E---S------------L---------V-PGF---------------N----E-
> 
> example file name: 'protein_n010k010.txt'
> best objective: 57
> best bound: 0.0
> wall time: 0.001127s
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
> --- Solution (of length 475) ---
>   Sol: MFAVFLESVLLPNRLVSSQPGFCVNEKTLHDAIRPLVQTRSLTAFSLPVYLQVRDSKETINLGIPVLSAFKRTQLPAVRNWSYTIDGEFLQMPALHIVEGDSNTKAFLRGVQIPNYKLSITEACDNVGSFTNKHQRGLPSYEDIVALTWAQSEKNVLDHMAREYTILAEKRGFPVQYTNDAQLPSIGVEDFTSPAKVRGTNYLEISVGRTHLPDEKGAFQSRHLWIKTVRDAGLYNSFTRGSDVLYEKPASQLRCIDFVGEKNSLYWADHPFTSILVQMIDRNAKLRSFETGAYLKPVRNSCLEIVSPDFWMAITHGVDSEAQKNGTLIPRADLGKFVIDESCRDYQHPGNLRSVITAKLTECLHNISRYDFVAGEKMICSQLTPVDRSWEHFVGNLDWVTSIYPARNIVQMGKETDLSTACIKSYGVLDNYGAEKMAVIGRKPVWKELASQGHRNSYCKDHIFVAGLMRTITVW
> str01: M------------R---------------H-----L------------------------N--I---------------------D----------I-E----T-----------Y--S---------S--N----------DI---------KN----------------G--V-Y------------------K-----Y---------------A------------DA--------------E---------DF--E-------------IL---------L--F---AY------S---I---D-------G--------G--------------E-------------V------ECL------D-----------LT---R---------------------------------------------------------------------------------------
> str02: M-----E------R-------------------R---------A---------------------------------------------------H------------R-----------T------------HQ-------------------N---------------------------------------------------------------------W-----DA------T--------KP----R------E--------------------R----R--------K--------------------------Q---T-------------------QH----R------LT---H-------------------P-D----------D---SIYP-R-I-----E--------K---------AE-----GRK----E------------DH----G--------
> str03: M-----E----P--------G----------A------------FS------------T---------A-----L-------------F-----------D----A-L---------------CD-----------------DI--L-----------H--R--------R-----------L-----E---S--------------------------Q---L-----R-------F--G------------------G----------------VQ-I----------------P----------P------------E----------------V---S--D---P---R-V--------------Y---AG----------------------------Y-A-----------L----------L----------------------------------------------
> str04: M-------------------G-----K-----------------F----Y--------------------------------Y------------------SN-----R--------------------------R-L-------A---------V----------------F-------AQ------------A------------------------QSRHL--------G-------GS---YE----Q--------------W--------L-------A-----------------C---VS---------G-DS-A--------------F------R-------------A---E----------V---K----------------------------AR--VQ--K--D----------------------------------------------------------
> str05: -F--F--------R-----------E----------------------------------NL------AF---Q----------------Q--------G----KA--R------------E-------F--------PS-E----------E-------AR-----A----------N-----S--------P-----T-----S--R-----E--------LW---VR---------RG------------------G--N-------P----L-----------S-E--A-----------------------G----A------------------E--R--------R---------------------G--------T-------------------------------------------------------------------------------------------
> str06: M-----------------------------D---P-----SLT--------QV---------------------------W------------A---VEG-S--------V------LS---A----------------------A---------V-D------T--AE--------TND-----------T-----------E--------PDE-G------L------------S------------A----------E-N--------------------------E-G-----------E----------T---------------R-------I----------------I------------R---------I----T----------G------S-------------------------------------------------------------------------
> str07: M-A-F-------------------------D-------------FS--V---------T---G----------------N---T--------------------K--L----------------D-----T--------S-------------------------------GF----T---Q----GV----S------------S------------------------------------------------------------------------M-----------T------V--------------A--------A---GTLI--ADL---V--------------------K-T------------A------S-------S---------------------Q------L-T----------N-----------------LA-Q----S------------------
> str08: M-AV----------------------------I--L-----------P-------S--T-----------------------YT-DG----------------T-A----------------AC------TN----G--S---------------------------------P-----D-------V--------V-GT-------G-T--------------------------------------------------------------------M-------------------------------W------V------N-T-I----L--------------PG--------------------DF--------------------F-----W-T---P-------------S-------G-------E---------------S-------------V----R---V-
> str09: M-----------N--------------T----------------------------------GI--------------------ID---L----------------F-----------------DN-------H----------V------------D--------------------------SI-------P-----T----I------LP---------H----------------------------QL--------------A----T--L----D------------YL--VR---------------T-------------I---------IDE---------N-RSV----L---L-------F-------------------H----------I--------MG-----S-------G------------------------------------------------
> str10: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR--T--------Q---------L--P----------PA-----YT------------------N---------------S----------FT----RG-------V------------------Y------------Y------P-----D-----KV---------------------F--R--------------S----S-VL------------------------H---S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M-----------------------------D---------S---------------KETI-L-I-----------------------E--------I---------------IP--K--I------------K------SY-----L---------LD------T-------------N------I------SP-K---------S----------------------------YN------D--------------F----------------I------------S----------RN-----------------------KN---I-------FVI-----------NL-----------------Y-------------------------N---V-S-------------T------I----------------------------------------------------
> str12: M----L---L------S---G-----K-----------------------------K-------------K--------------------M--L------------L----------------DN--------------YE-----T-A----------A------A--RG-------------------------RG--------G-----DE------R-------R---------RG-------------------------WA---F--------DR--------------P---------------AI---V--------T--------K-------RD-------------K--------S--D----------------R-----------------------M--------A--------------------------------H---------------------
> str13: M-----------N-------G----E-------------------------------E---------------------------D--------------D-N------------------E------------Q----------A---A----------A-E------------Q-----Q---------T---K-------------------K-A--------K--R----------------EKP------------K---------------Q-----A--R--------K-V----------------T----SEA-------------------------------------------------------------------WEHF----D-------A---------TD------------D--GAE-----------------------CK-H-------------
> str14: M-----ES-L-----V---PGF--NEKT-H------VQ---L---SLPV-LQVRD----------VL----------VR-------G-F----------GDS--------V----------E-------------------E--V-L----SE-------AR-------------Q----------------------------------HL---K--------------D-G-----T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M------------R-----------------------------------Y---------I-----V-S-------P--------------Q---L--V---------L---Q--------------VG----K---G-------------Q-E--V------E-------R---------A-L------------------YL------T--P---------------------Y-------D--Y---------ID---EK-S------P---I------------------Y---------------------------------------------------Y-------------------------F----------L----RS--H----L----------NI-Q------------------------------R-P-------------------------------
> str16: M----------P-R-V---P---V-------------------------Y----DS--------P--------Q---V---S----------P---------NT------V--P--------------------Q----------A---------------R----LA---------T-----PS-----F---A----T------------P--------------T---------F-RG--------A------D----------A--P------------A----F---------------------------------Q---------D-----------------------TA-------N---------------Q----------------------------Q---------A--------------------R---------Q-----------------------
> str17: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR--T--------Q---------L--P-L-A-------------YT------------------N---------------S----------FT----RG-------V------------------Y------------Y------P-----D-----KV---------------------F--R--------------S----S-VL------------------------H---S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: MF-VF----------------F-V----L------L-----------P--L-V--S-----------S-----Q-------------------------------------------------C--V----N-----L---------T----------------T-----R------T---QLP---------PA------Y-------T-------------------------NSFTRG--V-Y-------------------Y----P---------D---K------------V-----------F--------------------R----------S-----------SV----L----H--S-----------------------------------------------------------------------------------------------------------
> str19: M-----E------------------------AI--------------------------I-------S-F------A---------G---------I--G------------I-NYK---------------K----L------------QS-K--L------------------Q----------------------------------H--D----F-------------G------R---VL--K-A--L-------------------T---V-------------T-A-----R-------------A--------------L-P----G-----------Q-P---------K-----H-I------A----I--------R----------------------Q----------------------------------------------------------------
> str20: M-A----S--------S---G-------------P----------------------E-------------R----A----------E-------H---------------QI------I-----------------LP--E---------S------H-------L-----------------S-------SP--------L---V--------K------H---K------L----------LY-------------------YW-----------------KL----TG--L-P-----L----PD-----------E---------------------C-D--------------------------F--------------D----H----L-----I------------------------------------------------------------------------
> str21: M-----ES-L-----V---PGF--NEKT-H------VQ---L---SLPV-LQVRD----------VL----------VR-------G-F----------GDS--------V----------E-------------------E--V-L----SE--V-----R-------------Q----------------------------------HL---K--------------D-G-----T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L-------------------------A--P-----S------P------------N------S--K-------------I-----Q---L-----------F-------N----------N-----------------I----------N----------I-------------D-----I--------------NY-E------H----------------T-----LY--F-----------AS-------V----S---A---------Q----N----SF--------------------F--A---------Q------------------------------------------------------------------W---V-----V---Y--------------S-A--------D-----K-A-I-----------------------------------
> str23: M------S-----------------------AI-----T------------------ET-----------K----P-------TI--E-L--PAL----------A---------------E-----G-F----QR----Y-------------N--------------K-------T-----P--G---FT--------------------------------------------------------------C---V-----L---D------------R-----------Y--------------D------HGV----------I---------------------N-------------------D---------S--------------------------------K--------I----VL--Y-----------------------N-------------------
> str24: M-------------------------K---------------------------------N--I----A------------------EF---------------K-----------K-----A---------------P--E----L--A--EK--L---------L-E-----V---------------F-S-------N-L------------KG------------------NS--R-S--L-----------D-------------P-------M--R-A-------G---K-------------------H--D------------------V----------------V-----------------V-----I-----------E----------S-------------T-------K-----------K------------L--------------------------
> str25: M----------P------QP--------L---------------------------K----------------Q-------S-------L----------D----------Q------S-------------K---------------W-------L----RE----AEK----------------------------------------HL---------R---------A-L------------E---S-L-----V---------D----S--------N--L---E-------------E----------------E--K---L-------K------------P--------------------------------QL-----S----------------------MG-E-D----------V-----------------------Q----S------------------
> str26: MF-VFL--VLLP--LVSSQ---CVN---L---I-----TR--T--------Q---S--------------------------YT------------------N---------------S----------FT----RG-------V------------------Y------------Y------P-----D-----KV---------------------F--R--------------S----S-VL------------------------H---S----------------T-------------------------------Q---------D----------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-------------------------K-----------------F---------D----------VLS------L-------------F----A-------------------P----------------------------------WA---K-V-D----E------------Q------------E------------Y-----------D-----Q-------------------------------QL---------N-------------------N----------------N--LE--S------IT------A-------P-----KF--D----D----G-------A--TE----I--------E----S---------E---------------R-----G---D-----I----------------------------------------------------
> str28: MF-VFL--VLLP--LVSSQ---CVN-------------------F-------------T-N----------RTQLP-----S-----------A---------------------Y----T----N--SFT----RG-------V------------------Y------------Y------P-----D-----KV---------------------F--R--------------S----S-VL------------------------H---S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-------------------------------------------------------------------------------WS--I-----------IV---------L--------KL-I--------S--------------I------Q----------------------P--------L-------------------L--------L----------------V---------T--S--L---P---L------------Y----------------N-------------P--N-----------M------DS----------------------C-------------------CL--ISR---------I----TP-----E-----L--------A------GK---L-T-------------------------W----------------IF-------I---
> str30: M-----ES-L-----V---PGF--NEKT-H------VQ---L---SLPV-LQVRD----------VL----------VR-------G-F----------GDS--------V----------E-------------------E------------------------------F---------L-S---E-----A--R---------------------Q--HL--K---D-G-----T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: MF-VFL--VLLP--LVSSQ---CV-------------------------------------------------------------------MP-L-----------F-------N--L-IT---------T----------------T--QS-----------YT-------------N-----------FT-----RG-------V---------------------------Y----------Y--P-------D----K--------------V-----------F---------R-S-----S----------V---------L-------------------H---L---------------------------------------------------------------------------------------------------------------------------
> str32: M----------------------------H-------Q---------------------I------------T----V-------------------V---S-------G---P------TE----V-S-T---------------------------------------------------------------------------------------------------------------------------C--F-G---SL----HPF-----Q---------S------LKPV-------------MA-----------N------A-LG--V-------------L---------E------------G-KM--------------F----------------------------C--S--------------IG-----------G-R-S----------L-------
> str33: M-A------------------------TL------L---RSL-A--L----------------------FKR-------N------------------------K-------------------D-------K-----P----------------------------------P-----------I-----TS-----G------S-G--------GA-------I---R--G----------------------I-----K-------H----I----I------------------------IV-P-----I---------------P----G----D-S-----------S-IT---T-------R-----------S------R---------------------------------------------------------------------------------------
> str34: M-----ES-L-----V---PGF--NEKT-H------VQ---L---SLPV-LQVRD----------VL----------VR-------G-F----------GDS---------------------------------------------------------M--E-----E-----V-------L-S---E-----A--R---------------------Q--HL--K---D-G-----T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: MF-VFL--VLLP--LVSSQ---CVN---L---------T---T-------------------G---------TQLP----------------PA---------------------Y----T----N--SFT----RG-------V------------------Y------------Y------P-----D-----KV---------------------F--R--------------S----S-VL------------------------H---S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: M-A---------N-------------------I--------------------------INL------------------W---------------------N------G--I-------------V-----------P--------------------M--------------VQ---D-------V------------N-----V----------A--S----I-T---A-----F---------K--S---------------------------MID--------ET-------------------W-------D----K-----------K--I-E----------------A-------N-----------------T-------------------------------------CI-S----------------RK----------HRN-------------------
> str37: M----L------NR------------------I----QT--L-------------------------------------------------M------------K---------------T-A--N-----N--------YE-----T-----------------I--E----------------I----------------L-----R--------------------------N---------Y------LR----------LY--------I----I-----L------A-----RN---E----------------E----G----R---G---I------------L---I-------------YD---------------D--------N------I-------------D-S--------V-----------------------------------------------
> str38: M-A---------------------------D---P--------A------------------G---------T------N------GE----------EG---T-----G-------------C-N-G--------------------W-----------------------F---Y----------VE-----A-V---------V-------EK----------KT----G---------D------A-----I-------S----D-----------D--------E---------N---E--------------------N-------D--------S--D-----------T-----------------GE----------D---------L--V----------------D----------------------------------------------------------
> str39: MF-VFL--VLLP--LVSSQ---CVN---L----R----TR--T--------Q---------L--P----------P-----SYT------------------N---------------S----------FT----RG-------V------------------Y------------Y------P-----D-----KV---------------------F--R--------------S----S-VL------------------------H---S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L-----V---PGF--NEKT-H------VQ---L---SLPV-LQV----------------------------------------------------------------------CD-V----------L------V----------------R---------GF-------------G--D--S---V------E----------E-------------V----L--S---------E--A---R-----------------------Q-------------------------------------H-----------L-------K---D---------G------T----------------------------------------------------------------------------------------------------------------------
> str41: M-----------N-----------N------------Q-R----------------K-------------K-T---A-R-------------P--------S----F-------N--------------------------------------------M------L--KR---------A----------------R--N-------R-------------------V-------S-T----V------SQL--------------A----------------K-R-F-----------S----------------------K-G-L-----L-------S-------G-------------------------------Q------------G---------P------M-K---L---------V--------MA-------------------------F-----------
> str42: M------S----N--------F--------DAIR---------A--L-V-----D---T--------------------------D-------A---------------------YKL---------G-----H---------I--------------HM---Y---------P--------------E---------GT---E------------------------------Y--------VL-----S-----------N--------FT-------DR---------G--------S-----------------------------R-------I-E--------G----V-T-------H------------------T-V-----H-----------------------------------------------------------------------------------
> str43: M-------------------------------I------------------------E---L---------R-----------------------H--E-----------VQ---------------G--------------D---L--------V--------TI------------N--------V--------V------E-----T--P-E---------------D--L--------D----------------G-----------F---------R--------------------------DF---I----------------RA---------------H---L---I------CL---------A-----------VD-------------T-------------ET---T------G-LD---------I-----------------Y-----------------
> str44: MF-VFL--VLLP--LVSSQ---CV-------------------------------------------------------------------MP-L-----------F-------N--L-IT---------TN--Q----SY------T------N-----------------------------S-----FT-----RG-------V---------------------------Y----------Y--P-------D----K--------------V-----------F---------R-S-----S----------V---------L-------------------H-------------------------------------------------------------------------------------------------------------------------------
> str45: M------S------------------K---D----LV------A---------R-------------------Q--A------------L-M-----------T-A--R--------------------------------------------------M---------K----------A--------DF-----V---------------------F------------------F------L------------FV-----L-W-----------------K-------A-L-----S-L----P---------V-----------P--------------------------T-----------R----------C-Q--------------------I-------------D-------------------MA----K---K-L-S--------------AG--------
> str46: M-A----S-LL---------------K-------------SLT---L----------------------FKRT-----R------D----Q-P--------------------P---L----A-----S-------G--S-------------------------------G--------------G-------A---------I---R-------G--------IK------------------------------------------H------V--I------------------------IV---------------------LIP----G----D-S-----------S-I----------------V----------T---RS-----------------R--------------------------------------------------------------------
> str47: M------------R-V-----------------R----------------------------GI--L----R-------NW---------Q--------------------Q------------------------------------W---------------------------------------------------------------------------WI----------------------------------------W-----TS-L---------------G-----------------FWM------------------------F----------------------------------------MICS----V-------VGNL-WVT--------V---------------Y-----YG-----V----PVWKE-A---------K----------T-T--
> str48: M-AV--E----P---------F------------P----R-------------R----------P-------------------I------------------T----R----P-------------------H-----------A-----S-------------I--E-----V----D-----------TS-----G-----I--G--------G---S----------AG---S----S----EK----------V------------F-----------------------------CL-I-----------G-----Q--------A--------E--------G------------------------GE--------P----------N----T--------V-----------------------------------------------------------------
> str49: MF-----------------------------------------------Y------------------A--------------------------H---------AF--G-----------------G------------Y-D---------E-N-L-H-A-----------FP------------G-----------------IS--------------S------TV--A---N------DV---------R-------K---Y-------S--V--------------------V--S----V---------------------------------------Y----N-------K-----------------K--------------------------Y---NIV---K----------------N----K---------------------Y----------M-----W
> str50: M-A---------N------------------------------------Y-----SK-------P----F----L--------------L----------D-----------I-------------V--F-NK---------DI---------K----------------------------------------------------------------------------------------------------CI------N-----D----S---------------------------C----S--------H---S------------D---------CR-YQ------S-----------N-S-Y--V--E------L----R------------------RN--Q---------A-------L-N----K-------------------N-----------L-------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 475
> best bound: 0.0
> wall time: 0.028471s
> ```
