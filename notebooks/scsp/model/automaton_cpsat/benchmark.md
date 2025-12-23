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
Model = scsp.model.automaton_cpsat.Model
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
> --- Solution (of length 69) ---
>  Sol: tiojukiqfolcignbxyxcovskuqpoviozhmppsxsnhtqgexzvazgbxrddbcisvrvlnngpf
> str1: t----k-------gn--------ku-------hmp--x-nhtqg-xzv----x-----is---------
> str2: -ioj--iqfol---nbx-xc-vs-uqp-vi------s-s------------bx---------------f
> str3: ----u-----lci-n--y-co-s----ov-oz--pp---------------------------l---p-
> str4: -i-----------g------------------------------e--vazgb-rddbc-svrv-nng-f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 69
> best bound: 10.0
> wall time: 60.240514s
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
> --- Solution (of length 134) ---
>  Sol: tkgnkuhmpxnhtqgiojiqfolnbxxcvsuqpvginyecosovazgbrdopdblcsvbrzxucpmqvnngtdfuievdcvdpfnzsmsbcroqvbzfjtvxerzbrvigpxhwxqkrdrlctodtmprpxwde
> str1: tkgnkuhmpxnhtqg----------x-------------------z-----------v---x-------------i----------s-----------------------------------------------
> str2: ---------------iojiqfolnbxxcvsuqpv-i-----s--------------s-b--x-----------f------------------------------------------------------------
> str3: -----u----------------l----c-------iny-cosov------o---------z---p-----------------p-------------------------------------l------p------
> str4: ---------------i------------------g---e----vazgbrd--db-csv-r-------vnng--f------------------------------------------------------------
> str5: --------p----------------------------y-------------p--l----rzxucpmqv--gtdfui-v-c-d----s--b--o-----------------------------------------
> str6: --------p---------------b------------------------d--------------------------evdcvdpf-zsmsb-roqvb---------b------h---------------------
> str7: --------------------------------------e-----------------------------n--------------------bc-----zfjtvxerzbrvigp---------l------------e
> str8: ------------------------------------------------r------------x---------------------------------------------------wxqkrdrlctodtmprpxwd-
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 134
> best bound: 6.0
> wall time: 60.286527s
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
> --- Solution (of length 243) ---
>   Sol: tkgnkuhmpxnhiojiqfolnbxxulcinycosgoevoazgbrddbcsvpyplrzxucpmqvgtdfupbdevdcvdpfzsmsnbczfjtvxerzbrvigxwxqkrdrlctodtmkpqafigqjwokkskrblxxpabivbvzkozrifsavnqaxudgqvqcewbfgijowwyrsxqjnfpadiusiqbezhkiwshvhcomiuvddhtxxqjzqbctbakxusfcfzpeecvwantfmgqzu
> str01: tkgnkuhmpxnh---------------------------------------------------t--------------------------------------q-----------------g-----------x--------z--------v---x------------i------s--------------------------------------------------------------------
> str02: ------------iojiqfolnbxx--c---------v----------s--------u---q------p---v-------------------------i-----------------------------s--------------------s---------------b----------x---f---------------------------------------------------------------
> str03: -----u-------------l------cinycos-o-vo-z---------p-pl-----p----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: ------------i--------------------g-ev-azgbrddbcsv----r-------v--------------------n--------------------------------------------------------------------n-----g-------f-----------------------------------------------------------------------------
> str05: --------p--------------------y-------------------p--lrzxucpmqvgtdfu------------------------------i----------------------------------------v----------------------c--------------------d--s--b-----------o------------------------------------------
> str06: --------p------------b---------------------d--------------------------evdcvdpfzsms-b--------r-----------------o-----q---------------------vb------------------------b--------------------------h---------------------------------------------------
> str07: -----------------------------------e----------------------------------------------nbczfjtvxerzbrvig----------------p---------------l------------------------------e--------------------------------------------------------------------------------
> str08: ------------------------------------------r------------x--------------------------------------------wxqkrdrlctodtm-p-------------r----p-------------------x--------w------------------d------------------------------------------------------------
> str09: -k--k-----------q---------------------a--------------------------f-------------------------------ig---q-------------------jwokkskrbl-------------------------g-------------------------------------------------------------------------------------
> str10: -------------------l--xx-------------------------p-------------------------------------------------------------------a------------b------ivbvzkoz---------------------------------------------z------v-------d-------------------------------------
> str11: -k----------------------------------------r------------------------------------------------------i--------------------f--------s-------a--v------------n---------c--------------------d----q------w-h----------------z--c--------------------------
> str12: ----------------q---------------------a----------------xu-------d---------------------------------g---q-----------------------------------v-------------q--------cewbfgijowwy----------------------------------------------------------------------
> str13: ------------------------------------------r----s-------x----q--------------------------j---------------------------------------------------------------n-------------f--------------padiusiqbezhk-------o------h------------------------------mg---
> str14: ------------i---------------------------------------------------------------------------------------w--------------------------s---------------------------------------------------------------h-----vhcomiuvdd-------------------------------m----
> str15: ------h--------------------------------------------------------t--------------------------x--------x--q-------------------j------------------z----------q-----------b----------------------------------c--------t------b---ak--------------n-------
> str16: ---------x--------------u-------s--------------------------------f-------c---fz------------------------------------p----------------------------------------------e--------------------------e---------c----v----------------------------wantfmgqzu
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 243
> best bound: 2.0
> wall time: 61.868441s
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
>   Sol: cbbaedacdbeeecbdcdbceabdcaed
> str01: -----d-c-b---c--cdbc----c-e-
> str02: -b---d--dbeee-------e-bd----
> str03: c--a---cd-ee-c------e-b---e-
> str04: ---aed--d------d-d--e-bd---d
> str05: ---a---c-bee-c-------ab-c-e-
> str06: -bba-----be---bdc-b--a------
> str07: -bbae-a---e---b------a-d-a--
> str08: ----e-----eeecbd--b-e-----e-
> str09: c------cd-ee---d-----a-dc--d
> str10: -b---da--b-----d--b-ea---a-d
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 28
> best bound: 8.0
> wall time: 60.088276s
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
> --- Solution (of length 39) ---
>   Sol: dacebaedacebabcdbaedcbaedbacdaeabdceabd
> str01: d-c-b----c----cdb---c------c--e--------
> str02: ----b--d-------db-e----e------e----e-bd
> str03: --c--a---c-----d--e----e---c--e-b--e---
> str04: -a-e---d-------d---d----d-----e-bd----d
> str05: -ac-b-e---e---c--a---b-----c--e--------
> str06: ----b------bab----e--b--d--c----b---a--
> str07: ----b------ba-----e---ae-ba-da---------
> str08: ---e--e---e-------e-cb--db----e----e---
> str09: --c------c-----d--e----ed-a-d-----c---d
> str10: ----b--da--b---db-e---a---a-d----------
> str11: ---e---d--e----d-a----a---a---ea----a--
> str12: -a---ae-a---ab----e----e--ac-----------
> str13: ---e-a--a--b--c--a--c------cd---b------
> str14: ----b--d--e-------e---a-d-----ea-d-e---
> str15: --c--aeda------d--e----e------e--d-----
> str16: ---eb----c--a--dba---b---b----e--------
> str17: d------d-ce-------e---a--b--d-ea-------
> str18: da--b----c-----d---d---e--a---e---c----
> str19: -a---a-d-ce-------ed--a---a-----b------
> str20: -a-e--e--c----c---e----e------ea----a--
> str21: ----b------b---d-ae-c-a---a-d-e--------
> str22: dace---da-e----d-a---b-----------------
> str23: -a---ae-a--b-b--b----b-----c--e--------
> str24: d--e---d---b--c-b---c-a---a-----b------
> str25: d---b--da---a-----e--b---b-c----b------
> str26: d--eb-ed---b------e--ba----c-----------
> str27: --ce--e----b--cd----cb--d-----e--------
> str28: d---b-eda---a--d-a----a--b-------------
> str29: --c------c----cd----cb-e-b--d-----c----
> str30: -a-e--e-ac-----db---cb--d--------------
> str31: dac-b-e-ac----c-----c---d--------------
> str32: ---e-----ceb--c-----c---db--d---b------
> str33: d------d---b-bc---ed--a--b------b------
> str34: -a---ae-a--ba----ae--ba----------------
> str35: ---e-----c-b-bc--a----a-d--cd----------
> str36: d--eb----c----c---e-c---db-c-----------
> str37: da---a---c-ba-----e----e-b-c-----------
> str38: -a-----da--b------e---a---ac------ce---
> str39: da-e-----c-----dba--c-a---a------------
> str40: dac-b------b---d----c--ed--c-----------
> str41: d--e---d---b------e----e-b------bd-e---
> str42: --c----da------d----c---d--cda-a-------
> str43: --ce--ed-c-ba-----e----ed--------------
> str44: --ce-ae--c--a----a----a----c-a---------
> str45: d-c------c----c---e--b---b------b---a-d
> str46: ----bae---e-a-----e--b---b--d-e--------
> str47: d---b--d--eba-c-----c---db-------------
> str48: ---eb----c-b------e----ed-a---ea-------
> str49: -a-e--e---eb-b-db---c-a----------------
> str50: d---b--da--b--c---e-cb---b-------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 39
> best bound: 2.0
> wall time: 62.170697s
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
>   Sol: TCATACGCGTAATCGATACGTTAC
> str01: --AT--G-G-----GATACG----
> str02: --ATAC-C-T--TC----C----C
> str03: -CA--CG---AAT---T--G--A-
> str04: T-A-A-----AATC--T--GT---
> str05: --A---G-GTAA-C-A-A----A-
> str06: T--T-C-C-TA---G----GT-A-
> str07: T--T--G--TA---GAT-C-T---
> str08: T-----G-G-----GA-A-GTT-C
> str09: T--T-C-C--A--C-A-AC-T---
> str10: TC-TA-----AA-CGA-A------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 3.0
> wall time: 60.180942s
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
> --- Solution not found ---
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: None
> best bound: 0.0
> wall time: 90.817662s
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
> --- Solution (of length 48) ---
>   Sol: MEQSFLVRPENKQAFNTSLSGYDRNQAHICPVAFGNRKGTAPELYHQD
> str01: M------------A----LS-Y-------CP------KGT--------
> str02: M-QS-------------SL-----N-A-I-PV----------------
> str03: M-------P---------LS-Y---Q-H-----F--RK----------
> str04: ME-------E-----------------H---V---N------EL-H-D
> str05: M--S------N---F-------D---A-I-------R---A--L----
> str06: M---F--R--N-Q--N-S-----RN---------G-------------
> str07: M---F----------------Y----AH----AFG---G-----Y---
> str08: M--S-------K--F-T------R------------R----P--Y-Q-
> str09: M--SF-V------A------G----------V-------TA-----Q-
> str10: ME-S-LV-P-----------G------------F-N------E-----
> 
> example file name: 'protein_n010k010.txt'
> best objective: 48
> best bound: 9.0
> wall time: 60.220852s
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
> --- Solution not found ---
> 
> example file name: 'protein_n050k050.txt'
> best objective: None
> best bound: 0.0
> wall time: 86.21094s
> ```
