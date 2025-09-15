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
    model = scsp.model.automaton_cpsat.Model(instance).solve()
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
> --- Solution (of length 67) ---
>  Sol: utiojiqfkolcginybxxcovskuqhmopxnhetqvaiogsxzgsbrppddbcsvrvxnlngispf
> str1: -t------k---g-n--------ku-hm-pxnh-tq----g-xz-----------v--x----is--
> str2: --iojiqf-ol---n-bxxc-vs-uq---p------v-i--s---sb-----------x-------f
> str3: u---------lc-iny---co-s-----o-------v--o---z----pp----------l----p-
> str4: --i---------g--------------------e--va-----zg-br--ddbcsvrv-n-ng---f
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 10.0
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
>  Sol: tkgnkuhmpxnhtiojiqfolngbxxcvsuqpvlcinyscosogevoazgbrddbpycspvlrzxucpmqvnngbtdefuivdcvdpfzsmsnbroqczfjtvxebrzbhwxqkrvigpdrlctodtmprpxwed
> str1: tkgnkuhmpxnht----q----g-x-----------------------z-----------v---x---------------i--------s---------------------------------------------
> str2: -------------iojiqfoln-bxxcvsuqpv--i--s--s--------b-------------x-------------f--------------------------------------------------------
> str3: -----u--------------l-----c--------iny-coso--vo-z------p---p-l-----p-------------------------------------------------------------------
> str4: -------------i--------g---------------------ev-azgbrddb--cs-v-r-------vnng----f--------------------------------------------------------
> str5: --------p----------------------------y-----------------p-----lrzxucpmqv--g-td-fuiv-c-d---s---b-o---------------------------------------
> str6: --------p--------------b----------------------------d------------------------e---vdcvdpfzsms-broq-----v--b--bh-------------------------
> str7: --------------------------------------------e--------------------------n--b--------c----z----------fjtvxe-rzb-----rvigp--l-----------e-
> str8: ---------------------------------------------------r------------x---------------------------------------------wxqkr----drlctodtmprpxw-d
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 6.0
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
> --- Solution (of length 242) ---
>   Sol: tkgnkuhmpxnhiojiqfolnbxxulcinycosovoigevazgbrddbcsvpyplrzxucpmqvgtdfupbdevdcvdpfzsmsenbczfjtvxerzbrvigxwxqkrdrlctodtmpkqafigqjwokkskrblxxpabivbvzkozfsavnqaxudgqvqcewbfgirsxqjowwnfpadiuysiqbezhkwshvhcomiuvddhtxxqjzqbctbakxusfcfzpeecvwantfmgqzu
> str01: tkgnkuhmpxnh-----------------------------------------------------t---------------------------------------q-----------------g-----------x--------z------v---x------------i-s-----------------------------------------------------------------------
> str02: ------------iojiqfolnbxx--c-------v--------------s--------u---q------p---v--------------------------i-----------------------------s------------------s---------------b-----x------f---------------------------------------------------------------
> str03: -----u-------------l------cinycosovo-----z---------p-pl-----p-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: ------------i------------------------gevazgbrddbcsv----r-------v---------------------n------------------------------------------------------------------n-----g-------f---------------------------------------------------------------------------
> str05: --------p--------------------y---------------------p--lrzxucpmqvgtdfu-------------------------------i----------------------------------------v--------------------c------------------d---s--b----------o------------------------------------------
> str06: --------p------------b-----------------------d--------------------------evdcvdpfzsms--b--------r-----------------o-----q---------------------vb----------------------b-------------------------h--------------------------------------------------
> str07: --------------------------------------e----------------------------------------------nbczfjtvxerzbrvig---------------p----------------l----------------------------e------------------------------------------------------------------------------
> str08: --------------------------------------------r------------x---------------------------------------------wxqkrdrlctodtmp--------------r----p-----------------x--------w----------------d------------------------------------------------------------
> str09: -k--k-----------q-----------------------a--------------------------f--------------------------------ig---q-------------------jwokkskrbl-----------------------g-----------------------------------------------------------------------------------
> str10: -------------------l--xx---------------------------p--------------------------------------------------------------------a------------b------ivbvzkoz------------------------------------------z-----v-------d-------------------------------------
> str11: -k------------------------------------------r-------------------------------------------------------i--------------------f--------s-------a--v----------n---------c------------------d-----q-----w-h----------------z--c--------------------------
> str12: ----------------q-----------------------a----------------xu-------d----------------------------------g---q-----------------------------------v-----------q--------cewbfgi----joww-------y---------------------------------------------------------
> str13: --------------------------------------------r----s-------x----q---------------------------j-------------------------------------------------------------n-------------f------------padiu-siqbezhk------o------h------------------------------mg---
> str14: ------------i------------------------------------------------------------------------------------------w--------------------------s------------------------------------------------------------h----vhcomiuvdd-------------------------------m----
> str15: ------h----------------------------------------------------------t---------------------------x--------x--q-------------------j------------------z--------q-----------b--------------------------------c--------t------b---ak--------------n-------
> str16: ---------x--------------u-------s----------------------------------f-------c---fz------------------------------------p---------------------------------------------e-------------------------e--------c----v----------------------------wantfmgqzu
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 2.0
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
>   Sol: baebdcadbecdebecdaebadcbeadce
> str01: ----dc--b-c----cd--b--c----ce
> str02: b---d--dbe--e-e---eb-d-------
> str03: -----ca---cde-ec--eb----e----
> str04: -ae-d--d---d----d-eb-d----d--
> str05: -a---c--be--e--c-a-b--c-e----
> str06: b--b--a-be---b--d-----cb-a---
> str07: b--b--a--e-------aebad---a---
> str08: --e------e--e-ec---b-d-be---e
> str09: -----c----cde-e-da---dc---d--
> str10: b---d-a-b--d-be--a--ad-------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 9.0
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
> --- Solution (of length 40) ---
>   Sol: dacebaedacebabcdbaedcbbcaedbacdeebaadcde
> str01: d-c-b----c----cdb---c--c-e--------------
> str02: ----b--d-------db-e------e-----eeb--d---
> str03: --c--a---c-----d--e------e---c-e-b-----e
> str04: -a-e---d-------d---d------d----e-b--d-d-
> str05: -ac-b-e---e---c--a---b-c-e--------------
> str06: ----b------bab----e--b----d--c---ba-----
> str07: ----b------ba-----e-----ae-ba-d---a-----
> str08: ---e--e---e-------e-cb----db---ee-------
> str09: --c------c-----d--e------ed-a-d------cd-
> str10: ----b--da--b---db-e-----a---a-d---------
> str11: ---e---d--e----d-a------a---a--e--aa----
> str12: -a---ae-a---ab----e------e--ac----------
> str13: ---e-a--a--b--c--a--c--c--db------------
> str14: ----b--d--e-------e-----a-d----e--a-d--e
> str15: --c--aeda------d--e------e-----e----d---
> str16: ---eb----c--a--dba---bb--e--------------
> str17: d------d-ce-------e-----a--b--de--a-----
> str18: da--b----c-----d---d-----e--a--e-----c--
> str19: -a---a-d-ce-------ed----a---a----b------
> str20: -a-e--e--c----c---e------e-----e--aa----
> str21: ----b------b---d-ae-c---a---a-de--------
> str22: dace---da-e----d-a---b------------------
> str23: -a---ae-a--b-b--b----b-c-e--------------
> str24: d--e---d---b--c-b---c---a---a----b------
> str25: d---b--da---a-----e--bbc---b------------
> str26: d--eb-ed---b------e--b--a----c----------
> str27: --ce--e----b--cd----cb----d----e--------
> str28: d---b-eda---a--d-a------a--b------------
> str29: --c------c----cd----cb---e-b--d------c--
> str30: -a-e--e-ac-----db---cb----d-------------
> str31: dac-b-e-ac----c-----c-----d-------------
> str32: ---e-----ceb--c-----c-----db--d--b------
> str33: d------d---b-bc---ed----a--b-----b------
> str34: -a---ae-a--ba----ae--b--a---------------
> str35: ---e-----c-b-bc--a------a-d--cd---------
> str36: d--eb----c----c---e-c-----db-c----------
> str37: da---a---c-ba-----e------e-b-c----------
> str38: -a-----da--b------e-----a---ac-------c-e
> str39: da-e-----c-----dba--c---a---a-----------
> str40: dac-b------b---d----c----ed--c----------
> str41: d--e---d---b------e------e-b-----b--d--e
> str42: --c----da------d----c-----d--cd---aa----
> str43: --ce--ed-c-ba-----e------ed-------------
> str44: --ce-ae--c--a----a------a----c----a-----
> str45: d-c------c----c---e--bb----ba-d---------
> str46: ----bae---e-a-----e--bb---d----e--------
> str47: d---b--d--eba-c-----c-----db------------
> str48: ---eb----c-b------e------ed-a--e--a-----
> str49: -a-e--e---eb-b-db---c---a---------------
> str50: d---b--da--b--c---e-cbb-----------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 2.0
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
> --- Solution (of length 25) ---
>   Sol: TATAGGGCACTAGAATCTAGACTCA
> str01: -AT-GGG-A-TA----C--G-----
> str02: -ATA---C-CT----TC----C-C-
> str03: -------CAC--GAAT-T-GA----
> str04: TA-A----A--A---TCT-G--T--
> str05: -A--GG----TA-A--C-A-A---A
> str06: T-T----C-CTAG------G--T-A
> str07: T-T-G-----TAGA-TCT-------
> str08: T---GGG-A--AG--T-T---C---
> str09: T-T----C-C-A----C-A-ACT--
> str10: T------C--TA-AA-C--GA---A
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 8.0
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
> --- Solution (of length 46) ---
>   Sol: MQSESAKFRNPLQNSYVPEFDAQHGICPVTRAFNERLGKGTPYHDQ
> str01: M----A-----L--SY----------CP----------KGT-----
> str02: MQS-S------L-N-------A---I-PV-----------------
> str03: M---------PL--SY------QH--------F--R--K-------
> str04: M--E--------------E----H----V----NE-L------HD-
> str05: M-S------N---------FDA---I----RA----L---------
> str06: M------FRN--QNS---------------R--N---G--------
> str07: M------F-------Y-----A-H-------AF----G-G--Y---
> str08: M-S---KF---------------------TR----R-----PY--Q
> str09: M-S----F--------V----A--G---VT-A-------------Q
> str10: M--ES------L----VP------G-------FNE-----------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 8.0
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
