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
Model = scsp.model.linear_cpsat.Model
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
> --- Solution (of length 65) ---
>  Sol: uigtekvazgblrddbocjinkycoqfsovrvozpplnbxxcvsuhmqpxnhtqgxzvxissbxf
> str1: ---t-k---g----------nk----------------------uhm-pxnhtqgxzvxis----
> str2: -i--------------o-ji-----qf-o-------lnbxxcvsu--qp--------v-issbxf
> str3: u----------l-----c-in-yco--sov--ozppl-----------p----------------
> str4: -ig-e-vazgb-rddb-c---------s-vrv-----n------------n---g---------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 65
> best bound: 30.0
> wall time: 60.043455s
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
> --- Solution (of length 127) ---
>  Sol: irxtgevazgnbwxqkrdrlctodtmprpxwzfjytvxerzbrvigpldevdcvdpfzsmsbrozxucpmqvgtdfuivlbcinycodsovrlnkbxxcvozspuhmplxnnhtqpgxzvxissbxf
> str1: ---t-----------k-----------------------------g-------------------------------------n----------k---------uhmp-xn-htq-gxzvxis----
> str2: i---------------------o----------j----------i-------------------------q----f----------o-----ln-bxxcv--s-u---------qp---v-issbxf
> str3: ------------------------------------------------------------------u------------l-cinyco-sov---------oz-p---pl------p-----------
> str4: i---gevazg-b----rd-----d-----------------b----------c-----s------------v-------------------r-------v----------nn----g---------f
> str5: --------------------------p-------y-----------pl--------------r-zxucpmqvgtdfuiv--c-----ds------b----o--------------------------
> str6: --------------------------p--------------b------devdcvdpfzsmsbro------qv--------b--------------b---------h---------------------
> str7: -----e----nb--------c----------zfj-tvxerzbrvigpl-e-----------------------------------------------------------------------------
> str8: -rx---------wxqkrdrlctodtmprpxw-----------------d------------------------------------------------------------------------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 127
> best bound: 32.0
> wall time: 60.208848s
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
> --- Solution (of length 287) ---
>   Sol: qaxudgsfcfzpeecvwantfmhgqztxxqjzqbctbiwshuarvhcomiuvsxqjnfpadiusiqbezhkohvdqcewbfgijowwrifsavncdqwhelxxpazbivbvzkozkkqafigqjwokkskrxbnwxqkrdzrlctodtmprpbxwczfjtvxerzbrvigpyldevdcvdpmfzsmsbroqvbbpdlrzxucpmqvgtdfuivcdsgevazgbulrddbcsvrinyvnntckojsovgnkgiqfozpplnbxxcvsuqhmpxnhtqgxzvxissbxf
> str01: -------------------t--------------------------------------------------k----------g-----------n------------------k---------------------------------------------------------------------------------------u-------------------------------------------------------------------hmpxnhtqgxzvxis----
> str02: -------------------------------------i---------o-------j-----i---q--------------f---o---------------l--------------------------------n------------------bx-------x---------------cv-----s---------------u---q---------------------------------------------------p-------v----------------issbxf
> str03: ---u------------------------------------------------------------------------------------------------l------------------------------------------c------------------------i-----------------------------------------------------------------ny----c-o-sov-------ozppl-----------p----------------
> str04: -------------------------------------i-------------------------------------------g-----------------e--------v---------a---------------------z----------------------------g-----------------br------d------------d-------------b------csvr---vnn--------g-----f---------------------------------
> str05: -----------p---------------------------------------------------------------------------------------------------------------------------------------------------------------y--------p---------------lrzxucpmqvgtdfuivcds------b-------------------o--------------------------------------------
> str06: -----------p---------------------b--------------------------d------e-----vd-c---------------v--d-------p---------------f--------------------z-------------------------------------------smsbroqvbb--------------------------------------------------------------------------h------------------
> str07: ------------e-----n--------------bc---------------------------------z-----------f--j------------------------------------------------------------t---------------vxerzbrvigp-l-e----------------------------------------------------------------------------------------------------------------
> str08: -------------------------------------------r---------x------------------------w----------------------x---------------q--------k---r--------d-rlctodtmprp-xw------------------d-----------------------------------------------------------------------------------------------------------------
> str09: ----------------------------------------------------------------------k-----------------------------------------k----qafigqjwokkskr-b---------l--------------------------g---------------------------------------------------------------------------------------------------------------------
> str10: ----------------------------------------------------------------------------------------------------lxxpa-bivbvzkoz-------------------------z-------------------v------------d-----------------------------------------------------------------------------------------------------------------
> str11: ----------------------------------------------------------------------k----------------rifsavncdqwh------z-------------------------------------c-----------------------------------------------------------------------------------------------------------------------------------------------
> str12: qaxudg------------------q-------------------v---------q---------------------cewbfgijoww------------------------------------------------------------------------------------y-------------------------------------------------------------------------------------------------------------------
> str13: -------------------------------------------r--------sxqjnfpadiusiqbezhkoh---------------------------------------------------------------------------m--------------------g---------------------------------------------------------------------------------------------------------------------
> str14: -------------------------------------iwsh---vhcomiuv--------d-------------d-------------------------------------------------------------------------m------------------------------------------------------------------------------------------------------------------------------------------
> str15: ----------------------h---txxqjzqbctb-----a---------------------------k----------------------n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: --xu--sfcfzpeecvwantfm-gqz---------------u-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 287
> best bound: 26.0
> wall time: 60.521928s
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
>   Sol: bbaedabdbecbacdeecdebadcdbcee
> str01: ----d-----cb-c---cd-b--c--ce-
> str02: b---d--dbe-----ee--eb-d------
> str03: ----------c-acdeec-eb------e-
> str04: --aed--d------d---deb-d-d----
> str05: --a-------cb---eec---a---bce-
> str06: bba---b--e-b--d--c--ba-------
> str07: bbae-a---e-ba-d------a-------
> str08: ---e-----e-----eec--b-d--b-ee
> str09: ----------c--cdee-d--adcd----
> str10: b---dabdbe--a--------ad------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 29
> best bound: 16.0
> wall time: 60.126456s
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
> --- Solution (of length 87) ---
>   Sol: aeddddebddbcbcaabeecabdcbebadedadceebbacbedeabcdebdeadeecebebdcdbdbdeadcdcdaadaacadedba
> str01: --d--------cbc-----c--d-b--------c-----c-e---------------------------------------------
> str02: -------bddb------ee------e---e------b-----d--------------------------------------------
> str03: -----------c--a----c--d--e---e---ce-b----e---------------------------------------------
> str04: aeddddebdd-----------------------------------------------------------------------------
> str05: a----------cb----eecab-c-e-------------------------------------------------------------
> str06: -------b--b---a-be---bdcb--a-----------------------------------------------------------
> str07: -------b--b---a--e--a----ebad--a-------------------------------------------------------
> str08: -e----e----------eec-bd-be---e---------------------------------------------------------
> str09: -----------c-c--------d--e---edadc--------d--------------------------------------------
> str10: -------bd-----a-b-----d-be-a---ad------------------------------------------------------
> str11: -ed---e-d-----aa----a----e-a---a-------------------------------------------------------
> str12: a-------------a--e--a------a--------b----e-ea-c----------------------------------------
> str13: -e------------aab--ca--c---------c--------d--b-----------------------------------------
> str14: -------bd--------ee-a-d--e-ade---------------------------------------------------------
> str15: -----------c--a--e----d----ade----ee------d--------------------------------------------
> str16: -e-----b---c--a-------d-b--a--------bb---e---------------------------------------------
> str17: --dd-------c-----ee-abd--e-a-----------------------------------------------------------
> str18: --d-----------a-b--c--d-----de-a--e----c-----------------------------------------------
> str19: a-------------a-------dc-e---eda------a-b----------------------------------------------
> str20: ae----e----c-c---ee------e-a---a-------------------------------------------------------
> str21: -------b--b-----------d----a-e---c----a-----a--de--------------------------------------
> str22: --d-----------a----c-----e--d--a--e-------d-ab-----------------------------------------
> str23: a-------------a--e--ab--b-b---------b--c-e---------------------------------------------
> str24: --d---e-d-bcbcaab----------------------------------------------------------------------
> str25: --d----bd-----aa-e---b--b--------c--b--------------------------------------------------
> str26: --d---eb---------e----d-beba-----c-----------------------------------------------------
> str27: -----------c-----ee--b-c----d----c--b-----de-------------------------------------------
> str28: --d----b---------e----d----a---ad-----a-----ab-----------------------------------------
> str29: -----------c-c-----c--dcbeb-d----c-----------------------------------------------------
> str30: ae----e-------a----c--d-b--------c--b-----d--------------------------------------------
> str31: --d-----------a----c-b---e-a-----c-----c------cd---------------------------------------
> str32: -e---------c-----e---b-c---------c--------d--b-d-b-------------------------------------
> str33: --dd---b--bc-----e----d----a--------bb-------------------------------------------------
> str34: a-------------a--e--ab-----a---a--e-b-a------------------------------------------------
> str35: -e---------cb---b--ca------ad----c--------d--------------------------------------------
> str36: --d---eb---c-c---e-c--d-b--------c-----------------------------------------------------
> str37: --d-----------aa---c-b-----a-e----e-b--c-----------------------------------------------
> str38: a-d-----------a-be--a------a-----c-----c-e---------------------------------------------
> str39: --d-----------a--e-c--d-b--a-----c----a-----a------------------------------------------
> str40: --d-----------a----c-b--b---d----ce-------d---c----------------------------------------
> str41: --d---e-d-b------ee--b--b---de---------------------------------------------------------
> str42: -----------c----------d----ad----c--------d---cd----a----------------a-----------------
> str43: -----------c-----ee---dcb--a-e----e-------d--------------------------------------------
> str44: -----------c-----e--a----e-------c----a-----a-------a---c------------a-----------------
> str45: --d--------c-c-----c-----eb---------bba---d--------------------------------------------
> str46: -------b------a--ee-a----eb---------b-----de-------------------------------------------
> str47: --d----bd--------e---b-----a-----c-----c--d--b-----------------------------------------
> str48: -e-----b---cb----ee---d----a-e-a-------------------------------------------------------
> str49: ae----e----------e---b--b---d-------b--c----a------------------------------------------
> str50: --d----bd-----a-b--c-----e-------c--bb-------------------------------------------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 87
> best bound: 15.0
> wall time: 61.171645s
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
>   Sol: ATGGTGACCTACGAATCTGCATAC
> str01: ATGG-GA--TACG-----------
> str02: AT----ACCT-----TC--C---C
> str03: -------C--ACGAAT-TG-A---
> str04: -T----A---A--AATCTG--T--
> str05: A-GGT-A---AC-AA-----A---
> str06: -T--T--CCTA-G-----G--TA-
> str07: -T--TG---TA-GA-TCT------
> str08: -TGG-GA---A-G--T-T-C----
> str09: -T--T--CC-AC-AA-CT------
> str10: -T-----C-TA--AA-C-G-A-A-
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 16.0
> wall time: 60.084703s
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
> wall time: 85.40178s
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
>   Sol: MESLKFYVEAGVTHARNQFSGPVNESLGSRPYQHFNCDAIRPKEGTALV
> str01: M--------A----------------L-S--Y----C----PK-GT---
> str02: M----------------Q-S-----SL--------N--AI-P------V
> str03: M--------------------P----L-S--YQHF-----R-K------
> str04: ME------E----H--------VNE-L------H---D-----------
> str05: M-S-------------N-F------------------DAIR-----AL-
> str06: M----F---------RNQ-----N-S---R-----N--------G----
> str07: M----FY--A---HA---F-G------G---Y-----------------
> str08: M-S-KF------T--R-------------RPYQ----------------
> str09: M-S--F-V-AGVT-A--Q-------------------------------
> str10: MESL---V-------------P-----G------FN-------E-----
> 
> example file name: 'protein_n010k010.txt'
> best objective: 49
> best bound: 24.0
> wall time: 60.078664s
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
> wall time: 91.745744s
> ```
