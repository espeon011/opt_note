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
Model = scsp.model.linear1_cpsat.Model
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
>  Sol: tiokgnekuhmplcxjinhytvaqzgfolnbrxddzbxcovsxovrozpuqpvisnsnlpbxgf
> str1: t--kgn-kuhmp--x--nh-t--q-g------x--z----v-x----------is---------
> str2: -io------------ji------q--folnb-x----xc-vs-------uqpvis-s---bx-f
> str3: --------u---lc--in-y------------------co-s-ov-ozp--p------lp----
> str4: -i--g-e--------------va-zg----br-dd-b-c--s--vr------v--n-n----gf
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 64
> best bound: 30.0
> wall time: 60.055832s
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
> --- Solution (of length 130) ---
>  Sol: igenvazgbrxwxqkrdrlctodtmpyrpxwzfjtvxerzbrvidgplevdcvdpfzsmslbrzxoqulcpmqvgtdfuivbnycodsklognbxxcvrkozsuqpvihmpxnhtqlssngbxpzvxisf
> str1: --------------------t-------------------------------------------------------------------k--gn------k---u----hmpxnhtq----g-x-zvxis-
> str2: i--------------------o-----------j---------i----------------------q----------f-------o---l--nbxxcv----suqpvi---------ss--bx------f
> str3: -------------------------------------------------------------------ulc---------i--nyco-s--o------v--oz---p----p-----l------p------
> str4: ige-vazgbr------d-----d-----------------b----------c-----s---------------v------------------------r-------v-----n------ng--------f
> str5: -------------------------py-p------------------l--------------rzx--u-cpmqvgtdfuiv---c-ds-----b------o-----------------------------
> str6: -------------------------p--------------b---d---evdcvdpfzsms-br--oq------v-------b-----------b--------------h---------------------
> str7: --en----b----------c-----------zfjtvxerzbrvi-gple---------------------------------------------------------------------------------
> str8: ---------rxwxqkrdrlctodtmp-rpxw-------------d-------------------------------------------------------------------------------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 130
> best bound: 32.0
> wall time: 60.261813s
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
>   Sol: ulcinycoxusfcfzpeecvwantfmgqzhtxxqjzqbctbawshvhcomiuvdrsxqjnfpadiusiqbezhkohmaxudgqvqcewbfgijowwrifsavncdqwhzclxxpabivbvzkozzvkkqafigqjwokkskrblxwxqkrdrlctodtmprpenbczfjtvxwerzbrvigpbdevdcvdpfzsmsbroqvbbyplrzxucpmqvgtdfuivcdsbgevoazgbrddbcsvrvtjkiqfppgolnbnxxcvsgkuhqmpvissbxnhtfqgxzvxis
> str01: -----------------------t-------------------------------------------------k-------g--------------------n------------------k---------------------------------------------------------------------------------------u-------------------------------------------------------h-mp-----xnht-qgxzvxis
> str02: ---i---o--------------------------j---------------i------q--f-------------o-----------------------------------l----------------------------------------------------nb------x------------------------------------x-c---v---------s---------------------------------------u-q-pvissbx---f--------
> str03: ulcinyco--s-------------------------------------o---v---------------------o---------------------------------z----p---------------------------------------------p---------------------------------------------l-----p---------------------------------------------------------------------------
> str04: ---i----------------------g-------------------------------------------e------------v----------------a-------z-----------------------g---------b------rd-----d-------bc---------------------------s------v-----r-------v---------------------------------------n-n-----g---------------f--------
> str05: ---------------p-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------yplrzxucpmqvgtdfuivcdsb---o---------------------------------------------------------
> str06: ---------------p---------------------b---------------d----------------e------------v--------------------d----c-------v--------------------------------d--------p-------f-------z-----------------smsbroqvbb--------------------------------------------------------------h---------------------
> str07: ----------------e-----n--------------bc--------------------------------z-----------------f--j-------------------------------------------------------------t---------------vx-erzbrvigp-----------------------l---------------------e-----------------------------------------------------------
> str08: ------------------------------------------------------r-x------------------------------w-----------------------x----------------q--------k---r--------drlctodtmprp---------xw----------d-------------------------------------------------------------------------------------------------------
> str09: -------------------------------------------------------------------------k-----------------------------------------------k------qafigqjwokkskrbl------------------------------------g----------------------------------------------------------------------------------------------------------
> str10: -l------x----------------------x-----------------------------pa------b---------------------i---------v-------------b-v--zkozzv------------------------d----------------------------------------------------------------------------------------------------------------------------------------
> str11: -------------------------------------------------------------------------k----------------------rifsavncdqwhzc---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: ---------------------------q-------------a--------------x--------u--------------dgqvqcewbfgijoww-----------------------------------------------------------------------------------------------------------y-----------------------------------------------------------------------------------
> str13: ------------------------------------------------------rsxqjnfpadiusiqbezhkohm----g-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str14: ---i----------------w----------------------shvhcomiuvd---------d------------m------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: -----------------------------htxxqjzqbctba-------------------------------k----------------------------n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: --------xusfcfzpeecvwantfmgqz----------------------u-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 287
> best bound: 26.0
> wall time: 60.642233s
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
>   Sol: bbaedcadbcdebedecbaedbecaced
> str01: ----dc--bc------c---db-c-ce-
> str02: b---d--db--e-e-e---e-b-----d
> str03: -----ca--cde-e--c--e-be-----
> str04: --aed--d--d---de-b--d------d
> str05: --a--c--b--e-e--c-a--b-c--e-
> str06: bba-----b--eb-d-cba---------
> str07: bbae--a----eb-----a-d---a---
> str08: ---e-------e-e-ecb--dbe---e-
> str09: -----c---cde-ed---a-d--c---d
> str10: b---d-a-b-d-be----a-----a--d
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 28
> best bound: 16.0
> wall time: 60.117246s
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
> --- Solution (of length 240) ---
>   Sol: adacedaedabccdbccedbeeeebdbcaeeaccdbaeacbebdcbbacdcacabbdeaaceebcdcbdedebedbebacdbdaaebbcbbdaecaadecceeeaaceedaabbcddeaecceeabdeabcadbabbeaadeeedbdeeadeadebcaccdbbeeacaaeaabdabdbeaadcdeedadcdeecbdbeebadabbbebdcbaeceddebdddeecebedbdabcecbbaa
> str01: -d-c------bccdbcce------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str02: ----------b--d----dbeeeebd----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str03: ---c--a----c-d---e--e------c-e-----b-e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: a---ed--d----d----d-e---bd--------d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str05: a--c------b------e--e------ca------b---c-e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: ----------b---b-------------a------b-e--b--dcb-a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str07: ----------b---b-------------ae-a-----e--b------a-d-a--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: ----e--e---------e--e------c-------b-------d-b-----------e---e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str09: ---c-------c-d---e--e----d--a-----d----c---d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: ----------b--d--------------a------b-------d-b-----------eaa-----d------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: ----ed-eda------------------a--a-----ea--------a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: a-a-e-a--ab------e--e-------a---c---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str13: ----e-a--abc----------------a---ccdb------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str14: ----------b--d---e--e-------a-----d--ea----d-------------e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: ---c--aeda---d---e--ee---d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: ----e-----bc----------------a-----dba---b-b--------------e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: -d---d-----c-----e--e-------a------b-------d-------------ea-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: -da-------bc-d----d-e-------ae--c---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: a-a--d-----c-----e--e----d--a--a---b------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: a---e--e---cc----e--ee------a--a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str21: ----------b---b---d---------ae--c---a-a----d-------------e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: -dacedaedab-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str23: a-a-e-a---b---b----b----b--c-e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str24: -d--ed----bc--bc------------a--a---b------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: -d--------b--d--------------a--a-----e--b-b-cb--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: -d--e-----b------edbe---b---a---c---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: ---ce--e--bc-d-c---b-----d---e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str28: -d--------b------ed---------a--a--d-a-a-b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: ---c-------ccd-c---be---bd-c--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str30: a---e--e-a-c-dbc---b-----d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: -dac------b------e----------a---cc-----c---d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: ----e------c-----e-b-------c----c-db-------d-b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: -d---d----b---bc-ed---------a------b----b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: a-a-e-a---b-----------------a--a-----e--b------a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: ----e------c--b----b-------ca--a--d----c---d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: -d--e-----bcc----e---------c------db---c--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str37: -da---a----c--b-------------aee----b---c--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str38: ada-------b------e----------a--acc---e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str39: -da-e------c-db-------------a---c---a-a---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: -dac------b---b---d--------c-e----d----c--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: -d--ed----b------e--e---b-b-------d--e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: ---c-da-d--c-d-c--d---------a--a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: ---ce--ed--c--b-------------aee---d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: ---ce-ae---c----------------a--a----a--c-------a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: -d-c-------cc----e-b----b-b-a-----d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str46: ----------b-----------------aeea-----e--b-bd-------------e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: -d--------b--d---e-b--------a---ccdb------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str48: ----e-----bc--b--e--e----d--ae-a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: a---e--e---------e-b----bdbca-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str50: -d--------b--d--------------a------b---c-e--cbb-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 240
> best bound: 15.0
> wall time: 61.263532s
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
>   Sol: ATGGTACACGTAAGTCATCGACTA
> str01: ATGG-----G-A--T-A-CG----
> str02: AT---AC-C-T---TC--C--C--
> str03: ------CACG-AA-T--T-GA---
> str04: -T---A-A---AA-TC-T-G--T-
> str05: A-GGTA-AC--AA---A-------
> str06: -T--T-C-C-TA-G-----G--TA
> str07: -T--T----GTA-G--ATC---T-
> str08: -TGG-----G-AAGT--TC-----
> str09: -T--T-C-C--A---CA---ACT-
> str10: -T----C---TAA---A-CGA--A
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 16.0
> wall time: 60.095103s
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
> wall time: 86.142682s
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
>   Sol: MEQSSLKFVETRRPYAHAFGGNFQVTNEDAILSYQHDFRNALCPVKGT
> str01: M--------------A---------------LSY--------CP-KGT
> str02: M-QSSL---------------N-------AI------------PV---
> str03: M------------P-----------------LSYQH-FR------K--
> str04: ME-------E------H-------V-NE---L---HD-----------
> str05: M--S-----------------NF-----DAI-------R-AL------
> str06: M------F---R---------N-Q--N-----S-----RN------G-
> str07: M------F------YAHAFGG------------Y--------------
> str08: M--S--KF--TRRPY--------Q------------------------
> str09: M--S---FV------A---G----VT---A----Q-------------
> str10: ME-S-L--V----P-----G--F---NE--------------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 48
> best bound: 24.0
> wall time: 60.096598s
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
> wall time: 92.921109s
> ```
