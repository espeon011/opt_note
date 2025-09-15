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
def bench(instance: list[str]) -> None:
    model = scsp.model.linear_cpsat.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")
```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n004k015-025.txt"))
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 66) ---
>  Sol: iguevazgbrdldbtcsvrkignycojisoqvfozkpuhmplnbxxcvsunhtqpgxzvxissbxf
> str1: --------------t----k-gn------------k-uhmp---x-----nhtq-gxzvxis----
> str2: i------------------------oji--q-fo-------lnbxxcvsu---qp---v-issbxf
> str3: --u--------l---c----i-nyco--so-v-oz-p---pl------------p-----------
> str4: ig-evazgbrd-db-csvr------------v----------n-------n----g---------f
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 30.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n008k015-025.txt"))
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
> --- Solution (of length 135) ---
>  Sol: irxgwexqknrvazdgbrlctodtmprbpxwczfjtvxerzbrvdiegvpdycvdpfzsmsbroqvbplerzxkucpmqvgtdfuoivlcdinsbycosovrvknxoxcvsuhzpmpxnhtqglpxzvxissbxf
> str1: --------------------t----------------------------------------------------k------g-----------n----------k-------uh--mpxnhtqg--xzvxis----
> str2: i--------------------o------------j----------i------------------q------------------f-o--l---n-b----------x-xcvsu---------q--p--v-issbxf
> str3: --------------------------------------------------------------------------u-------------lc-in--ycosov-----o------zp-p------lp----------
> str4: i--g-e-----vaz-gbr----d---------------------d----------------b-------------c-----------------s------vrv-n-------------n---g-----------f
> str5: -------------------------p-------------------------y---p------------l-rzx-ucpmqvgtdfu-iv-cd--sb--o-------------------------------------
> str6: -------------------------p-b----------------d-e-v-d-cvdpfzsmsbroqvb---------------------------b-----------------h----------------------
> str7: -----e---n------b--c------------zfjtvxerzbrv-i-g-p------------------le-----------------------------------------------------------------
> str8: -rx-w-xqk-r---d--rlctodtmpr-pxw-------------d------------------------------------------------------------------------------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 32.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n016k015-025.txt"))
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
> --- Solution (of length 293) ---
>   Sol: lxxpabivusfcfzpeecvwanhtfmgqzxxqjzqbctbaiwshvhcomiuvddrsxqjnfpadiusiqbezhkohqaxudgqvqcewbfgijowwkrifsavncdqwhvzkozzkkqafigqjwokkskrbrxwxqkrdrlctodtmprpxwenbczfjtvxerzbrvigplpbdevdcvdpfzsmsbroqvbbpyplrzxucpmqvgtdfuivcdsgevazgbrddbcsvrvnulcinycosovozjiqfolpnpltbxxcvksgnkuqpvisshmbpxnhtqgfxzvxis
> str01: -----------------------t-------------------------------------------------k-------g---------------------n-------k------------------------------------------------------------------------------------------u-------------------------------------------------------------------------hm-pxnhtqg-xzvxis
> str02: ------i----------------------------------------o----------j-----i---q--------------------f---o-----------------------------------------------l------------nb------x--------------------------------------x-c---v---------s-----------------u--------------q---p--------v---------iss--b-x-----f------
> str03: --------u------------------------------------------------------------------------------------------------------------------------------------lc--------------------------i----------------------------------------------------------------n-----ycosovoz------p-pl-------------p---------------------
> str04: ------i-------------------g-------------------------------------------e------------v-----------------a--------z----------g---------br------d-----d---------bc----------------------------s------v------r-------v--------------------------n----n--------------------------g-------------------f------
> str05: ---p------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------yplrzxucpmqvgtdfuivcds------b-----------------o--------------------------------------------------
> str06: ---p-b----------------------------------------------d-----------------e------------v---------------------d------------------------------------c------------------v-------------d------pfzsmsbroqvbb---------------------------------------------------------------------------------h----------------
> str07: ---------------e-----n-------------bc----------------------------------z-----------------f--j--------------------------------------------------t-----------------vxerzbrvigpl---e--------------------------------------------------------------------------------------------------------------------
> str08: ------------------------------------------------------r-x------------------------------w---------------------------------------------x--qkrdrlctodtmprpxw----------------------d---------------------------------------------------------------------------------------------------------------------
> str09: -------------------------------------------------------------------------k----------------------k---------q-----------afigqjwokkskrb---------l----------------------------g--------------------------------------------------------------------------------------------------------------------------
> str10: lxxpabiv---------------------------b--------v--------------------------z-ko-----------------------------------z--z-----------------------------------------------v-------------d---------------------------------------------------------------------------------------------------------------------
> str11: -------------------------------------------------------------------------k-----------------------rifsavncdqwh-z-------------------------------c------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: ---------------------------q-----------a----------------x--------u--------------dgqvqcewbfgijoww----------------------------------------------------------------------------------------------------y------------------------------------------------------------------------------------------------
> str13: ------------------------------------------------------rsxqjnfpadiusiqbezhkoh-----------------------------------------------------------------------m----------------------g--------------------------------------------------------------------------------------------------------------------------
> str14: ------i------------w----------------------shvhcomiuvdd---------------------------------------------------------------------------------------------m-------------------------------------------------------------------------------------------------------------------------------------------------
> str15: ----------------------ht-----xxqjzqbctba---------------------------------k-----------------------------n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: -x------usfcfzpeecvwan-tfmgqz---------------------u--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 26.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q05n010k010-010.txt"))
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
>   Sol: bbaedcabcecdbdeaecbdaebedcbde
> str01: ----dc-bc-cdb----c-------c--e
> str02: b---d------db-e-e----e-e--bd-
> str03: -----ca-c--d--e-ec---ebe-----
> str04: --aed------d-d-----d-eb-d--d-
> str05: --a--c-b-e----e--c--a-b--c--e
> str06: bba----b-e--bd---cb-a--------
> str07: bbae--a--e--b--a---da--------
> str08: ---e-----e----e-ecbd--be----e
> str09: -----c--c--d--e-e--da---dc-d-
> str10: b---d-ab---db-ea----a---d----
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 16.0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q05n050k010-010.txt"))
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
> --- Solution (of length 226) ---
>   Sol: dbdabcecbbaeeebbdbcaebcbeedaeadbdebaeedcdadcdbceebdabcddeaecddceeabdeaebcadbabbecaedadeeedbdeeadeadeaabcaccdbaaeaabeeacededaaaeaabdabdbeaadccdeedadcdeeeecbdbeebbaeaebadabbabebdcbacbeecabceaeddddebddcacdeecebebddbeeeebcbccdbcce
> str01: d----c--b---------c---c---d----b-------c---c---e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str02: -bd-------------db--e---ee--e--bd-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str03: -----c----a-------c-------d-e----e-----c-------e-b------e-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: ---a--e---------d---------d---d-deb---d-d-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str05: ---a-c--b--ee-----ca-bc-e---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: -b--b-----a---b-----eb----d------------c-----b-----a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str07: -b--b-----ae-------aeb-----a--d----a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: ------e----eee----c--b----d----b-e--e---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str09: -----c-c--------d---e---e-da--d--------cd-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: -bdab-----------db--e------a-ad---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: ------e---------d---e-----da-a-----ae----a---------a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: ---a------ae-------a-------a---b-e--e----a-c--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str13: ------e---a--------a-bc----a-----------c---cdb------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str14: -bd---e----e-------a------d-ead--e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: -----c----ae----d--a------d-e----e--e-d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: ------e-b---------ca------d----b---a---------b---b------e-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: d-d--ce----e-------a-b----d-ea----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: d--abc----------d---------d-ea---e-----c------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: ---a------a-----d-c-e---e-da-a-b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: ---a--e----e------c---c-ee--ea-----a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str21: -b--b-----------d--ae-c----a-ad--e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: d--a-ce---------d--ae-----da---b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str23: ---a------ae-------a-b-b-------b--b----c-------e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str24: d-----e---------dbc--bc----a-a-b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: dbda------ae--bb--c--b------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: d-----e-b--e----db--eb-----a-----------c------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: -----ce----e--b---c-------d------------c-----b----d-----e-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str28: db----e---------d--a-------a--d----a-----a---b------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: -----c-c----------c-------d------------c-----b-e-bd--c----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str30: ---a--e----e-------a--c---d----b-------c-----b----d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: d--a-c--b--e-------a--c----------------c---cd-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: ------ec---e--b---c---c---d----bd-b-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: d-d-b---b---------c-e-----da---b--b-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: ---a------ae-------a-b-----a-a---eba----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: ------ecbb--------ca-------a--d--------cd-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: d-----e-b---------c---c-e--------------cd----bc-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str37: d--a------a-------c--b-----ae----eb----c------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str38: ---a------------d--a-b--e--a-a---------c---c---e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str39: d--a--ec--------db-a--c----a-a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: d--a-c--bb------d-c-e-----d------------c------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: d-----e---------db--e---e------b--b---d--------e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: -----c----------d--a------d------------cd--cd------a-----a------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: -----ce----e----d-c--b-----ae----e----d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: -----ce---ae------ca-------a-a---------c-a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: d----c-c----------c-eb-b-------b---a--d-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str46: -b-a--e----e-------aeb-b--d-e-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: dbd---e-b-a-------c---c---d----b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str48: ------e-b---------c--b--eedaea----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: ---a--e----ee-bbdbca--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str50: dbdabcecbb------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 15.0
> ```

In [ ]:
```python
bench(scsp.example.load("nucleotide_n010k010.txt"))
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
>   Sol: TCATGGACGCTAATCGATACGTCA
> str01: --ATGG--G--A-T--A--CG---
> str02: --AT--AC-CT--TC----C--C-
> str03: -CA----CG--AAT---T--G--A
> str04: T-A---A----AATC--T--GT--
> str05: --A-GG----TAA-C-A-A----A
> str06: T--T---C-CTA---G----GT-A
> str07: T--TG-----TA---GAT-C-T--
> str08: T---GG--G--AA--G-T---TC-
> str09: T--T---C-C-A--C-A-AC-T--
> str10: TC-T--A----AA-CGA-A-----
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 16.0
> ```

In [ ]:
```python
bench(scsp.example.load("nucleotide_n050k050.txt"))
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
> solution status: UNKNOWN
> bset bound: 0.0
> ```

In [ ]:
```python
bench(scsp.example.load("protein_n010k010.txt"))
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
> --- Solution (of length 51) ---
>   Sol: MEQSLFNEVPAGVLSKFTRRPYAHDANQIVNELSHDFGGRNALIYCPVKGT
> str01: M---------A--LS------Y-----------------------CP-KGT
> str02: M-QS----------S-----------------L-------NA-I--PV---
> str03: M--------P---LS------Y-----Q------H-F--R--------K--
> str04: ME-----E---------------H-----VNEL-HD---------------
> str05: M--S--N---------F-------DA--I----------R-AL--------
> str06: M----F------------R-------NQ--N--S-----RN--------G-
> str07: M----F---------------YAH-A----------FGG-----Y------
> str08: M--S-----------KFTRRPY-----Q-----------------------
> str09: M--S-F--V-AGV----T----A----Q-----------------------
> str10: ME-SL---VP-G----F---------N----E-------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 24.0
> ```

In [ ]:
```python
bench(scsp.example.load("protein_n050k050.txt"))
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
> solution status: UNKNOWN
> bset bound: 0.0
> ```
