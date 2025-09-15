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
    solution = scsp.model.mm.solve(instance)
    scsp.util.show(instance)
    scsp.util.show(instance, solution)
    print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
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
> --- Solution (of length 74) ---
>  Sol: igeojiqfolnbtkgnkuhlcimnpxnhtqgxcvazgbrddbcsvruqpvinngfssbxfisycosovozpplp
> str1: ------------tkgnkuh---m-pxnhtqgx---z--------v-------------x-is------------
> str2: i--ojiqfolnb-------------x-----xcv---------s--uqpvi----ssbxf--------------
> str3: -----------------u-lci-n--------------------------------------ycosovozpplp
> str4: ige------------------------------vazgbrddbcsvr---v-nngf-------------------
> 
> solution is feasible: True
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
> --- Solution (of length 148) ---
>  Sol: ipbdegevadcnbczfgbrddbcjtvxdekgnkuhlcimpfnycosjiovrzboplrvzxnhigplengfplpqfolnbsmsbroqtqgxucpmqvbbghtdfuivcdsbowxcqkrdrlctodtmprpvsuqpvissbxfwdzvxis
> str1: ------------------------t----kgnkuh---mp-------------------xnh------------------------tqgx-----------------------------------------------------zvxis
> str2: i-------------------------------------------o-ji-------------------------qfolnb----------x----------------------xc---------------vsuqpvissbxf-------
> str3: ---------------------------------u-lci---nycos--ov---o----z-----p-----plp---------------------------------------------------------------------------
> str4: i----geva-----z-gbrddbc----------------------s---vr------v--n------ngf------------------------------------------------------------------------------
> str5: -p----------------------------------------y-----------plr-zx------------------------------ucpmqv--g-tdfuivcdsbo-------------------------------------
> str6: -pbde--v-dc--------------v-d-----------pf----------z---------------------------smsbroq---------vbb-h------------------------------------------------
> str7: ----e------nbczf-------jtvx-e---------------------rzb---rv----igple---------------------------------------------------------------------------------
> str8: ------------------r-------x------------------------------------------------------------------------------------wx-qkrdrlctodtmprp----------x-wd-----
> 
> solution is feasible: True
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
> --- Solution (of length 198) ---
>   Sol: ikrpxulswxqkaxbcifshtavncdeqypafbigvbcojnbczfpevadiqjuswhzcokgvdozpfzbrddbcsmivrlctodvnksuxerzbrvxqbcddeghmplnbxgfigpjzqvbctbaknhkoqcewabfghmgijlentfmgqgxzucvprbbhlgmopxwdisquqpvgissbtdfuivcdsbowxfy
> str01: --------------------t---------------------------------------kg------------------------nk-u---------------hmp---x---------------nh------------------t---qgxz--v----------x--is-------------------------
> str02: i-------------------------------------oj----------iq---------------f---------------o------------------------lnbx-----------------------------------------x--cv--------------s-uqpv-issb------------xf-
> str03: -----ul--------ci------n----y--------co---------------s----o--v-ozp----------------------------------------pl-------p---------------------------------------------------------------------------------
> str04: i---------------------------------g-----------eva--------z---g-------brddbcs--vr-----vn----------------------n--gf------------------------------------------------------------------------------------
> str05: ---p------------------------yp--------------------------------------------------l-----------rz---x---------------------------------------------------------uc-p------m-------q---vg----tdfuivcdsbo----
> str06: ---p----------b----------de--------v-------------d--------c---vd--pfz------sm-----------s-----br----------------------------------oq-------------------------v--bbh-----------------------------------
> str07: --------------------------e-------------nbczf-------j-----------------------------t--v----xerzbrv-----------------igp---------------------------le----------------------------------------------------
> str08: --r-x---wxqk----------------------------------------------------------rd-------rlctod--------------------------------------t----------------m-----------------pr-------pxwd---------------------------
> str09: -k---------k---------------q--af-ig----------------qj--w---ok--------------------------ks-------------------------------------k--------------------------------rb--lg---------------------------------
> str10: ------l--x---x---------------pa-bi-vb----------v---------z--k---oz--z---------v-----d-----------------------------------------------------------------------------------------------------------------
> str11: -kr-------------ifs--avncd-q---------------------------whzc-------------------------------------------------------------------------------------------------------------------------------------------
> str12: ----------q-ax---------------------------------------u---------d----------------------------------------g--------------qv----------qcew-bfg---ij----------------------o--w------------------------w--y
> str13: --r----s-xq----------------------------jn---fp--adi--us----------------------i--------------------qb---e--------------z---------hko--------hmg--------------------------------------------------------
> str14: i-------w---------sh--v---------------------------------h-co----------------mi-----------u------v----dd---m-------------------------------------------------------------------------------------------
> str15: -------------------ht---------------------------------------------------------------------x------xq------------------jzq-bctbakn----------------------------------------------------------------------
> str16: ----xu-s---------f------c------f-----------z-pe--------------------------------------------e--------c-------------------v-------------wa----------ntfmgq--zu------------------------------------------
> 
> solution is feasible: True
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
> --- Solution (of length 32) ---
>   Sol: bdacbaecdebecaebdadcbdeabebdcced
> str01: -d-cb--c----c---d---b-------cce-
> str02: bd------d-be--e-------e--ebd----
> str03: ---c-a-cde-ec-eb------e---------
> str04: --a---e-d-------d-d--de-b--d---d
> str05: --acb-e--e--ca-b---c--e---------
> str06: b---ba----be---bd--cb--a--------
> str07: b---bae------aeb-ad----a--------
> str08: ------e--e-e--e----cbd--be----e-
> str09: ---c---cde-e----dadc-d----------
> str10: bda-b---d-be-a---ad-------------
> 
> solution is feasible: True
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
> --- Solution (of length 36) ---
>   Sol: daecbdeabcedacbeadcbedabeacbdeacdbed
> str01: d--cb----c---c---d-b------c----c--e-
> str02: ----bd-----d--be----e---e----e---b-d
> str03: ---c---a-c-d---e----e-----c--e---be-
> str04: -ae--d-----d-----d---d--e--bd---d---
> str05: -a-cb-e---e--c--a--b------c--e------
> str06: ----b---b---a-be---b-d----cb--a-----
> str07: ----b---b---a--ea---e--b-a--d-a-----
> str08: --e---e---e----e--cb-d-be----e------
> str09: ---c-----c-d---e----eda-----d--cd---
> str10: ----bd-ab--d--bea-----a-----d-------
> str11: --e--de----da---a-----a-ea----a-----
> str12: -a-----a--e-a---a--be---eac---------
> str13: --e----a----a-b---c---a---c----cdb--
> str14: ----bde---e-a----d--e-a-----de------
> str15: ---c---a--eda----d--e---e----e--d---
> str16: --e-b----c--a----d-b--ab---b-e------
> str17: d----d---ce----ea--b-d--ea----------
> str18: da--b----c-d-----d--e-a-e-c---------
> str19: -a-----a---d-c-e----eda--a-b--------
> str20: -ae---e--c---c-e----e---ea----a-----
> str21: ----b---b--da--e--c---a--a--de------
> str22: da-c--e----da--e-d----ab------------
> str23: -a-----a--e-a-b----b---b---b---c--e-
> str24: d-e--d--bc----b---c---a--a-b--------
> str25: d---bd-a----a--e---b---b--cb--------
> str26: d-e-b-e----d--be---b--a---c---------
> str27: ---c--e---e---b---c--d----cbde------
> str28: d---b-e----da---ad----a--a-b--------
> str29: ---c-----c---c---dcbe--b----d--c----
> str30: -ae---ea-c-d--b---cb-d--------------
> str31: da-cb-ea-c---c----c--d--------------
> str32: --ec--e-bc---c---d-b-d-b------------
> str33: d----d--b-----b---c-edab---b--------
> str34: -a-----a--e-a-b-a-----a-e--b--a-----
> str35: --ecb---bc--a---adc--d--------------
> str36: d-e-b----c---c-e--c--d-b--c---------
> str37: da-----a-c----b-a---e---e--b---c----
> str38: -a---d-ab-e-a---a-c-------c--e------
> str39: daec-d--b---ac--a-----a-------------
> str40: da-cb---b--d-c-e-dc-----------------
> str41: d-e--d--b-e----e---b---b----de------
> str42: ---c-d-a---d-c---dc--da--a----------
> str43: ---c--e---ed-cb-a---e---e---d-------
> str44: ---c--ea--e--c--a-----a--ac---a-----
> str45: d--c-----c---c-e---b---b---b--a-d---
> str46: ----b--a--e----ea---e--b---bde------
> str47: d---bde-b---ac----c--d-b------------
> str48: --e-b----c----be----eda-ea----------
> str49: -ae---e---e---b----b-d-b--c---a-----
> str50: d---bd-abce--cb----b----------------
> 
> solution is feasible: True
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
> --- Solution (of length 27) ---
>   Sol: TATCGACGTAAGACTACGTAACGTCAC
> str01: -AT-G--G---GA-TACG---------
> str02: -AT--AC------CT---T--C--C-C
> str03: ---C-ACG-AA---T---T---G--A-
> str04: TA---A---AA---T-C-T---GT---
> str05: -A--G--GTAA--C-A---AA------
> str06: T-TC--C-TA-G-----GTA-------
> str07: T-T-G---TA-GA-T-C-T--------
> str08: T---G--G---GA--A-GT----TC--
> str09: T-TC--C--A---C-A---A-C-T---
> str10: T--C----TAA-AC---G-AA------
> 
> solution is feasible: True
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
> --- Solution (of length 150) ---
>   Sol: ATGACTGACTAGATCAGTACTACGATCTCATGACTAGCATGCAGTCAGTCAAGCATCACAGTCAGTACATGACTAGCATACGTACTGACTCGATCTGACTGATCGATCGATGACTACGTAGCATGCATCGATCGAGATATGAACCGARTG
> str01: -T-A--G--TAG-T-AG-ACT-C---C----G----G-A---AGT--G--A--CA--A-A--C----C----CT-G-A-A---A---A---GA----A-TG---GAT--A--A--A--TA---T--A-----------------------
> str02: --G---GA-TA-A--A---C-AC--TC-C----C--G-A---A---A---A----T-A-A-T---T---TGACT----TA---A---AC---A----AC-G--CGA-C-A-G--T---T--CA---A--G--------------------
> str03: AT-AC---CT---TC----CTA-G-------G--TA--A--CA---A---A--C--CA-A--C----CA--ACT----T---T--TGA-TC--TCT---TG-T--A--GAT--CT--G--------------------------------
> str04: -T-A---A--A--T---TA-TA--ATCT--T-A-TA-C-T--AGT-A---AA--A--A-A-T-AG-----G----G--T--GTA---AC-CGA----A---A---A-CG--G--T-C---------------------------------
> str05: -T---T-A--A-A--A---C-A-G--C-C-TG--T-G---G--GT---T---GCA-C-C---CA---C-T--C-A-CA---G----G----G--C---C----C-A-C--TG-----G--GC--GCA---A--G----------------
> str06: ATGACT---T----C----C-A--AT-----G----G-AT-C---C---CAA-C--C----TCA--A---G-CT----T-C---C--AC-C---C---C--A---AT-G--G--T---T----T-CA--G--C-----------------
> str07: A--AC--A--A-A-C----C-A--A-C-CA--ACT----T----T---T---G-ATC----TC--T---TG--TAG-AT-C-T---G--T---TCT--CT-A---A---A---C---G-A--A--C------------------------
> str08: ATGA---A--A-A-C-G-A--A--A----AT---TA---T----T-A-TCAAG-------G---GTA--TG----G-A-A-GT---G----GA----A--G--C--T-GA---C---G-A--A---AT----------------------
> str09: A---CT--C--G----G--CT--G--C--ATG-CT----T--AGT--G-CA--C-TCAC-G-CAGTA--T-A--A---T---TA---A-T--A----ACT-A---AT---T-A-------------------------------------
> str10: -T---TG--TAGATC--T-----G-T-TC-T--CTA--A---A--C-G--AA-C-T-----T---TA-A--A--A---T-C-T---G--T-G-T--G---G--C--T-G-T--C-AC-T--C----------------------------
> str11: --G-C--A---GA---G--C-A---T-T--T---T--C-T--A---A-T-A----TC-CA--CA--A-A--A-T-G-A-A-G----G-C---A----A-T-A---AT---TG--TAC-TA-C-T-C------------------------
> str12: ATGA--G-C-----CA--A----GATC-C--GAC--G-A---AG--AG-C---C--C-CA---AG-----GA---G-----G-A--GA----A---G---GA--G---G--GAC--C----C---C--C---------------------
> str13: -T--CT--C-A---CAGT--T-C-A----A-GA--A-C---C---CA---AAG--T-AC---C----C----C---C---C--A-T-A---G--C---C----C--TC--T---TA---A--A-GC--C-A-C-----------------
> str14: A-G---G--T---T---TA-TAC---CT--T--C---C-T--AG---GT-AA-CA--A-A--C----CA--AC---CA-AC-T--T---TCGATCT--CT--T-G-T--A----------------------------------------
> str15: A-G---G--T---T---TA-TAC---CT--T--C---C---CAG---GT-AA-CA--A-A--C----CA--AC---CA-AC-T--T---TCGATCT--CT--T-G-T--A----------------------------------------
> str16: -T-A---A--A-A-CA--ACT-C-A----AT-AC-A--A--CA-T-A---A-G-A--A-A---A-T-CA--AC--GCA-A---A---A----A-C--ACT---C-A-C-A--A--A----------------------------------
> str17: ----C---C--G--C----C--C-AT-T--TG----G---GC-G---G-C-----TC----TC-G-A---G-C--G-ATA-G--CT--C--G-TC-GA---ATC---C-----CT-CG-A-C---C-T----------------------
> str18: AT-AC---CT---TC----C--C-A------G----G--T--A---A--CAA--A-C-CA---A---C----C-A--A--C-T--T---TCGATCT--CT--T-G-T--A-GA-T-C-T-G-----------------------------
> str19: -T--CT--C-A---CAGT--T-C-A----A-GA--A-C---C--TCA---A-G--TC----TC----C----C---C---C--A-T-A---G----G-C----C--TC--T---T---T--CA-G--TC-A--G----------------
> str20: --GA-T--CT----C--T-CT-C-A-C-C--GA--A-C---C--T--G----GC--C-C---C-G-----G----GCA-A---A-TG-C-C---CT-A---ATC---C-A-GA----G--G--TG-------------------------
> str21: A-GA--G-C-A-ATCAGT-----G--C--AT--C-AG-A---A---A-T-A----T-AC---C--TA--T---TA---TAC--ACT---T---T--G-CT-A---A--GA--A-T-----------------------------------
> str22: A--A-T---TA-A--A--AC-A---TCTCA--A-TA-CA---A--CA-T-AAG-A--A-A---A--ACA--AC--GCA-A---A---A----A-C--ACT---C-AT-------------------------------------------
> str23: A--A---AC--GA--A---CT----T-T-A--A--A--AT-C--T--GT---G--T----G---G--C-TG--T--CA--C-T-C-G----G--CTG-C--AT-G--C--T---TA-GT-GC----------------------------
> str24: AT-A---ACTA-AT---TACT--G-TC----G--T----TG-A--CAG----G-A-CAC-G--AGTA-A---CT--C----GT-CT-A-TC--T-T--CTG-------------------------------------------------
> str25: ATGA--G--T-G-TCA---C---GA----AT---T--CA--C-GT-A--CAA---T----G--A--AC-TG----G-AT--GT--T--C---A-C-G--TG---GA---AT-A--A----------------------------------
> str26: A---C---C--G-T--G------G-------G-C--G-A-GC-G---GT---G-A-C-C-G---GT----G--T--C-T---T-C---CT--A---G--TG---G---G-T--C--C----CA--C---G-T-----T--GAA----R--
> str27: A--A---A---G----GT--T----T---AT-AC---C-T----TC---C---CA-----G---GTA-A---C-A--A-AC---C--A----A-C---C--A---A-C--T---T---T--C--G-ATC--TC----T-TG---------
> str28: A-G--T-A---G-T---T-C---G--C-C-TG--T-G--TG-AG-C--T---G-A-CA-A---A---C-T---TAG--TA-GT---G--T---T-TG--TGA--G---GAT---TA----------------------------------
> str29: -T---T---TA--T-A---C--C--T-TC----CTAG---G---T-A---A--CA--A-A--C----CA--AC---CA-AC-T--T---TCGATCT--CT--T-G-T--A-GA-T-----------------------------------
> str30: ATG-C-G----G-TC-GT-CT-C--TC-C----C---C--G--G-C--T------T-----T---T---T---T----T-C---C---C-CG--C-G-C----CG--CG-T---T--G--GC--GC--CGA-------------------
> str31: --G--TGAC-A-A--A--A--AC-AT---A--A-T-G---G-A--C--TC---CA--ACA--C----CATG--T--CA-A-G--CT---T---TC--A--G---G-T--A-GAC------------------------------------
> str32: --G--TG--TA-A---G-A--A--A-C--A-G--TA--A-GC---C---C--G-------G--A--A---G--T-G-----GT---G--T---T-T---TG--CGAT---T---T-CG-AG---GC--CG---G----------------
> str33: --GA--GA--A--T--G-A----G-TCTCAT---TA-C---C-G-C---C---C------G---GTAC-T---TAGCA-A-G--CT-A----AT---A--G-TC-A-CG--G-C------------------------------------
> str34: ATG--TG----G-TC-G-A-T--G--C-CATG----G-A-G--G-C---C---CA-C-CAGT---T-CAT---TA--A---G----G-CTC---CTG---G--C-AT---T---------------------------------------
> str35: A---C-GA---G--C-GT--T----T-T-A--A---G---G--G-C---C---C------G-C-G-AC-TG-C--G-A--CG----G-C-C-A-C--A-TG---G--C-----C--C-T-G--T--AT-G-T------------------
> str36: --G---G--T---T---TA-TAC---CT--T--C---C---CAG---GT-AA-CA--A-A--C----CA--AC---CA-AC-T--T---TCGATCT--CT--T-G-T--A-G--------------------------------------
> str37: -TG---G----GA--AGT--T-C---C--A--A--A--A-G-A-TCA--CAA--A--ACA--C--TAC----C-AG--T-C--A---AC-C--T--GA---A--G-T--A---C-AC---------------------------------
> str38: --GA---A---G--C-GT--TA--A-C----G--T-G--T----T--G--A-G-------G--A--A-A--A---G-A--C--A--G-CT---T---A--G---GA--GA--AC-A---AG-A-GC-T-G---G-G--------------
> str39: A---C---C-AG--C-G--C-AC--T-TC--G----GCA-GC-G---G-CA-GCA-C-C--TC-G-----G-C-AGCA--C---CT--C---A---G-C--A--G--C-A--AC------------------------------------
> str40: ATG---G----GA-CA--ACT----T---AT---T--C---C--T-A-TCA----T----GT--G--C----C-A--A---G-A--G----G-T-T---T--T--A-C-----C--CG--G--TG-A-C---C-A---------------
> str41: -T---TG--TAGATC--T-----G-T-TC-T--CTA--A---A--C-G--AA-C-T-----T---TA-A--A--A---T-C-T---G--T-G-T--G---G-T---T-G-T--C-AC-T--C----------------------------
> str42: A--AC---C-A-A-C----C-A--A-CT--T---T--C--G-A-TC--TC-----T-----T--GTA---GA-T--C-T--GT--T--CTC--T---A---A---A-CGA--ACT---T----T--A-----------------------
> str43: --G---G----G-T---T-CT--G--C-CA-G----GCAT--AGTC--T------T-----T---T---T---T----T-C-T---G----G--C-G---G--C---C-----CT---T-G--TG--T--A---A-A------CC---TG
> str44: --G---G-CT-G--CA-T-----G--CT--T-A---G--TGCA--C--TCA--C------G-CAGTA--T-A--A---T---TA---A-T--A----ACT-A---AT---T-ACT--GT-------------------------------
> str45: -TG-C--A-T-G--C--T--TA-G-T-----G-C-A-C-T-CA--C-G-CA-G--T-A---T-A--A--T---TA--ATA---ACT-A----AT-T-ACTG-TCG-T-------------------------------------------
> str46: -T---T--C-----CA---C-A--A-CT--T---T--C---CA--C---CAAGC-TC----T--G--CA--A---G-AT-C---C---C---A---GA--G-TC-A--G--G-----G--GC---C-T-G-T------------------
> str47: -T--CT-A--A-A-C-G-A--AC--T-T--T-A--A--A---A-TC--T---G--T----GT--G-----G-CT-G--T-C--ACT--C--G----G-CTG--C-AT-G----CT---TAG-----------------------------
> str48: A---C---C--G----G-A-T--G-------G-C---C--GC-G--A-T------T-----T---T---T--C--G-----G-A--G--TC---CT---TG---G---G--G-----G-A-C---CA-C--TC-AGA-AT-A---GA---
> str49: ----CT---T-G-T-AG-A-T-C--T-----G--T----T-C--TC--T-AA--A-C---G--A--AC-T---T----TA---A---A----ATCTG--TG-T-G---G----CT--GT--CA--C-T----------------------
> str50: ATGA--G-C-A---C--TA--A-G--C----GA--AG-A---A--C---CAA--A--A-AG-CAG-ACA--A-TA-CA-AC---C---C--G--CT-A-T--T--A-C------------------------------------------
> 
> solution is feasible: True
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
> --- Solution (of length 62) ---
>   Sol: MSFEAEHVNAELSYAHAFDGACPKGLVTAQSYFIRALNQHFNSRKLNAGIPGFNETRRPVYQ
> str01: M---A------LSY-------CPKG--T----------------------------------
> str02: M----------------------------QS-----------S--LNA-IP--------V--
> str03: M---------------------P--L----SY------QHF--RK-----------------
> str04: M--E-EHVN-EL---H--D-------------------------------------------
> str05: MS------N--------FD-A------------IRAL-------------------------
> str06: M-F-------------------------------R--NQ--NSR--N-G-------------
> str07: M-F----------YAHAF-G----G------Y------------------------------
> str08: MS---------------------K--------F----------------------TRRP-YQ
> str09: MSF----V-A---------G------VTAQ--------------------------------
> str10: M--E--------S------------LV-----------------------PGFNE-------
> 
> solution is feasible: True
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
> --- Solution (of length 536) ---
>   Sol: MFAVFLESVLLPLVSSQCVNRPGFKNEDLKTHVQLSLPRAITRVLQVFSTGYALEIRDVLSPQTKLVRNGFMPLAGDSPTIEFNLDAYTKLVEQWNSFTRGIVDHAETYQPCGKIVLNRTAPSEAFNYLQGSAEKDHLMRTIEQLAVFPDKSEIVLTRQAGYFHPSENRTDLKNSFVARQLGTRGVYSDILNVPKTASGITYPDKVFRSEGSLHQLANSVLHYDSFTPLCGVKRINYEDLSFGAMTIDRGVENLWAKFYAHLSPGTVRDEKLIASGNEWISTAVLYPKDFQDRAIPREGVLSAHIDVGKQTAVENPGKRILSETMDSVIAGEQCLFARCSKYWTNSVLDIFGHPQAETRSIDKLMGRSGEHITVAKLQCFHRNISDYAGTDEPDNEGLIDQSVARKNSIYTECLPGDSAFLVHKLTRNWEGIFMAEFPDTVKARIVQKDSIYNLRIECDFDHGEDLVDIKMICSADKAINKYMWTPRNVSGESVGIEKAEGRKEDHGNLQALNKNLTIVWVTVYYGVPVWKEAKTT
> str01: M-------------------R----------H--L---------------------------------N-----------I----D---------------I----ETY-------------S--------S-----------------------------------N--D------------------I----K----------------------N------------GV----Y-------------------K-YA--------D----A---E----------DF-------E------I---------------L-------------LFA----Y---S---I-----------D---G--GE---V-----------------E--------------------CL--D---L----TR-------------------------------------------------------------------------------------------------------------
> str02: M-----E-------------R-----------------RA----------------------------------------------------------------H-------------RT----------------H------Q-----------------------N--------------------------------------------------------------------------------------W-------------D----A-------T-----K-------PRE--------------------R------------------R--K-------------Q--T-------------------Q--HR---------------L------------T-----------H--------------PD---------DSIY---------------------------------PR--------IEKAEGRKEDHG-----------------------------
> str03: M-----E----P----------G----------------A-------FST--AL----------------F-----D---------A---L--------------------C-----------------------D-------------D---I-L-------H----R---------R-L----------------------------E-S--QL-----------------R-------FG------GV---------------------------------------Q---IP-------------------P------E----V-----------S--------D----P----R--------------V------------YAG--------------------Y--------A-L---L---------------------------------------------------------------------------------------------------------------
> str04: M---------------------G-K----------------------F---Y-----------------------------------Y--------S--------------------NR--------------------R----LAVF-----------A-------------------Q----------------A-----------------Q---S--------------R--------------------------HL--G----------G----S----Y-----------E-----------Q--------------------------------W----L-------A----------------------C-----------------------V----S-------GDSAF------R-------AE----VKAR-VQKD---------------------------------------------------------------------------------------
> str05: -F--F---------------R-----E-----------------------------------------N----LA-------F----------Q---------------Q--GK------A------------------R--E----FP--SE-------------E----------AR-----------------A--------------------NS--------P-----------------T----------------S----R-E-L------W----V--------R---R-G--------G------NP----LSE------AG-----A-------------------E-R-------R-G---T-------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: M--------------------------D---------P----------S----L---------T-----------------------------Q--------V-------------------------------------------------------------------------------------------------------------------------------------------------------WA----------V--E-----G----S--VL----------------SA--------AV------------D-----------------T-----------AET------------------------N--D---T-EPD-EGL---S-A-------E---------------N-EG----E---T---RI-----I---RI----------------------------T-----G-S-------------------------------------------
> str07: M-A-F----------------------D-------------------FS---------V----T-----G-------------N----TKL------------D---T--------------S-------G----------------F--------T-Q-G---------------V----------S---------S----------------------------------------------MT----V----A---A----GT-----LIA--------------D-----------L-----V-K-TA---------S----S-----Q-L--------TN--L-------A---------------------Q------S-------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: M-AV------------------------------------I---L----------------P---------------S-T-------YT--------------D--------G------TA---A--------------------------------------------------------------------------------------------------------C---------------T------N-----------G---------S-----------P-D----------V------VG--T-----G------TM-----------------W---V-----------------------------------N------T--------I--------------LPGD--F------------F--------------------------------------------------WTP---SGESV-------R----------------V-----------------
> str09: M------------------N----------T-------------------G----I------------------------I----D----L------F-----D-------------N------------------H---------V--D-S-I----------P----T-------------------IL--P-------------------HQLA---------T-L---------D-------------------Y--L----VR-------------T------------I---------ID-------EN---R--S-----V------L------------L--F-H-------I---MG-SG-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: MF-VFL--VLLPLVSSQCVN--------L---------R--TR------T------------Q--L------P-----P-------AYT------NSFTRG-V-----Y------------------Y--------------------PDK---V-------F-----R-----S------------S----V-------------------LH----S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M--------------------------D-------S----------------------------K----------------E------T------------I--------------L------------------------IE----------I-----------------------------------I---PK----I----K---S-------------Y-----L----------L-------D-----------------T----------N--IS-----PK-------------S---------------------------------------Y--N---D-F---------I------S-------------RN----------------------KN-I----------F-V---------I--------------------NL---------------------------Y-----NVS--------------------------TI------------------
> str12: M----L---L----S-------G-K----K----------------------------------K------M-L----------LD---------N------------Y--------------E----------------T----A-------------A-----------------AR--G-RG-------------G----D-----E-----------------------R--------------R------------------R-------G--W---A------F-DR--P------A-I-V---T------KR------D--------------K----S--D---------R-----M---------A-----H-----------------------------------------------------------------------------------------------------------------------------------------------------------
> str13: M------------------N--G---E---------------------------E--D------------------D------N--------EQ-----------A--------------A---A--------E---------Q--------------Q----------T--K---------------------K-A-------K--R-E----------------------K------------------------------P------K-------------------Q--A--R-----------K---V----------T--S----E----A-----W-------------E-------------H--------F-----D-A-TD--D--G------A-------EC----------K-------------------------------------H--------------------------------------------------------------------------
> str14: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VLQV---------RDVL------VR-GF----GDS-------------VE-------------E--------VL-----SEA--------------R---Q-------------------H-------LK---------------D---------G-T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-------------------R------------------------------Y---I--V-SPQ--LV------L-------------------Q--------V---------GK----------------G------------Q--------E-V-----------E-R--------A--L-----Y---L----T------P-------------------YD------------Y---------ID---E----K-----SP--------I------------Y-------------------------------------------------------Y--------F------------L--RS--H-----L-----NI----------------Q---R---------P-------------------------------------------------------------------------------------------------------------------------
> str16: M----------P--------R-----------V----P-----V-------Y-----D--SPQ---V----------SP----N----T--V------------------P------------------Q--A------R----LA----------T-------PS---------F-A----T----------P-T----------FR--G-----A------D-------------------A-------------------P---------A---------------FQD------------------TA--N-----------------Q---------------------QA--R------------------Q--------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: MF-VFL--VLLPLVSSQCVN--------L---------R--TR------T------------Q--L------PLA------------YT------NSFTRG-V-----Y------------------Y--------------------PDK---V-------F-----R-----S------------S----V-------------------LH----S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: MF-VF------------------F--------V-L-LP------L-V-S-----------S-Q------------------------------------------------C---V-N----------L-----------T---------------TR-----------T---------QL------------P--------P-------------A-----Y---T--------N----SF---T--RGV-------Y--------------------------YP-D-------------------K---V----------------------F-R-S-----SVL----H------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: M-----E--------------------------------AI--------------I----S---------F---AG----I-------------------GI---------------N---------Y------K---------------K----L--Q------S------K-------L---------------------------------Q------H-D-F----G--R----------------V--L--K--A-L---TV--------------TA---------RA------L--------------PG---------------Q--------------------P--------K-------HI--A--------I--------------------R-----------------------------------------Q-----------------------------------------------------------------------------------------
> str20: M-A----S------S-------G--------------P----------------E-R-----------------A------E----------------------H----Q----I--------------------------I--L---P---E------------S-----------------------------------------------H-L--S-----S--PL--VK---------------------------H---------KL------------LY-------------------------------------------------------YW-------------------KL--------T---------------G--------L----------------P-----L----------------PD-----------------ECDFDH---L--I-------------------------------------------------------------------
> str21: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VLQV---------RDVL------VR-GF----GDS-------------VE-------------E--------VL-----SE----------------------V----------RQ----H-------LK---------------D---------G-T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L---------------------------------A---------------------P---------------SP----N------------S----------------KI--------------Q-------L---------F-------------------N-----N---------------I-N-------I---D------------------------------INYE----------------------H----T-----L-------------Y---F---A-------S----V--------------S-------A--Q-----------NS----F----------------------------F-------A------------Q---------------------------W-----------V----V-----Y---------------------SADKAI---------------------------------------------------------
> str23: M------S-------------------------------AIT------------E--------TK-------P------TIE--L-------------------------P---------A-------L---AE--------------------------G-F----------------Q---R--Y----N--KT------P-------G--------------FT--C-V-------L-------DR---------Y---------D----------------------------------H---G----V------I------------------------N---D----------S--K--------I-V--L---------Y-------N---------------------------------------------------------------------------------------------------------------------------------------------
> str24: M-----------------------KN--------------I-----------A-E---------------F------------------K-----------------------K------AP-E----L---AEK--L------L-------E-V-------F--S-N---LK--------G---------N-----S---------RS---L----------D---P----------------M---R------A--------G-----K--------------------------------H-DV-----V--------------VI--E-------S---T------------------K------------KL---------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: M----------P----Q----P------LK---Q-SL--------------------D----Q--------------S-----------K----W---------------------L-R----EA--------EK-HL-R-----A---------L----------E-------S-----L----V--D--------S-------------------N--L----------------E-------------E-----------------EKL---------------K-------P-------------Q----------LS--M-----GE----------------D------------------------V---Q------S-------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: MF-VFL--VLLPLVSSQCVN--------L-----------ITR------T------------Q--------------S---------YT------NSFTRG-V-----Y------------------Y--------------------PDK---V-------F-----R-----S------------S----V-------------------LH----S-------T---------------------------------------------------------------QD----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-----------------------K----------------------F---------DVLS----L----F---A---P---------------W----------A-------K-V-------------------D------EQ--------E--------Y--------D--------Q----------------------------------QL-N-----------------N----------------NL---------------E----S----I-TA---PK-F-D-------------D-G---A-----------T-------E-----------------I------E--S---------E-----------R------G-D-------I-----------------------------------------------------------------------------------------------------------------------------------------
> str28: MF-VFL--VLLPLVSSQCVN---F------T-------------------------------------N------------------------------R-------T-Q------L----PS-A--Y------------T--------------------------N------SF------TRGVY--------------YPDKVFRS--S-------VLH--S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M---------------------------------------------------------------------------------------------W-S----I------------IVL-----------------K--L---I---------S-I----Q-----P------L--------L---------L-V--T-S--------------L--------------PL-------Y---------------N----------P------------N-----------------------------------------------MDS------C----C--------L-I---------S------R----IT-------------------P--E-L-----A-----------G-------KLT--W--IF-----------I-------------------------------------------------------------------------------------------
> str30: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VLQV---------RDVL------VR-GF----GDS-------------VE-------------E------------------F--L--S-E-----------A-----------RQ----H-------LK---------------D---------G-T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: MF-VFL--VLLPLVSSQCV----------------------------------------------------MPL--------FNL----------------I-----T-----------T--------------------T--Q-------S---------Y-------T---N-F------TRGVY--------------YPDKVFRS--S-------VLH------L-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M------------------------------H-Q------IT-V--V-S-G----------P-T-----------------E---------V----S-T------------C-------------F----GS-----L-------------------------HP----------F---Q-------S--L---K-------P--V--------------------------------------M----------A--------------------N-----A-L-------------GVL------------E--GK------M----------F--CS---------I-G-------------GRS--------L---------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: M-A---------------------------T---L-L-R---------S----L--------------------A---------L------------F---------------K----R-------N-------KD--------------K-------------P----------------------------P-----IT-------S-GS------------------G-----------GA--I-RG----------------------I--------------K---------------HI--------------I--------I-----------------V------P------I-------------------------------P---G--D-S-----SI-T--------------TR----------------------S----R---------------------------------------------------------------------------------
> str34: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VLQV---------RDVL------VR-GF----GDS------------------------------------------------------------M---E---------E-VL---------SE----------ARQ---------------------------------H-L----------------K-----D---G--T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: MF-VFL--VLLPLVSSQCVN--------L-T----------T--------G------------T-----------------------------Q----------------------L----P--------------------------P----------A-Y-------T---NSF------TRGVY--------------YPDKVFRS--S-------VLH--S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: M-A----------------N--------------------I--------------I------------N----L--------------------WN----GIV-------P---------------------------M-------V-----------Q-----------D-----V--------------NV---AS-IT---------------A--------F------K-------S---M-ID---E-------------T------------W---------D-------------------K--------K-I--E------A--------------N------------T--------------------C----IS-------------------RK----------------H---RN------------------------------------------------------------------------------------------------------------
> str37: M----L-------------NR-------------------I----Q---T---L-----------------M-----------------K--------T------A-----------N--------NY-----E------TIE----------I-L-R---------N------------------Y---L----------------R----L---------Y-----------I-----------I------L-A-----------R--------NE-------------------EG-------------------R-----------G------------------I-------------L-------I--------------Y---D--DN---ID-SV-------------------------------------------------------------------------------------------------------------------------------------
> str38: M-A------------------------D---------P-A----------G------------T----NG-----------E----------E-------G------T----G--------------------------------------------------------------------------------------------------------------------C-----N------G-----------W--FY-------V--E---A---------V---------------V-------------E---K----------------------K--T-------G---------D------------A--------ISD----DE--NE----------N---------DS--------------------DT----------------------GEDLVD--------------------------------------------------------------------
> str39: MF-VFL--VLLPLVSSQCVN--------L---------R--TR------T------------Q--L------P-----P-----------------S-----------Y----------T------N----S---------------F--------TR--G---------------V---------Y--------------YPDKVFRS--S-------VLH--S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VLQV----------------------------------------------------------------C-----------------------D----------V--------L--------------------V-R--G------------------------F---G------------DS------V-----E-------------E--------------V----L--S--E----A---------R----------------Q------------------------------------------H----------L-----------K---------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M------------------N-----N-------Q----R-------------------------K------------------------K--------T------A------------R--PS--FN-----------M-----L-----K------R-A--------R----N----R------V-S-------T---------V--S-----QLA---------------KR-------F--------------------S-------K----G--------L---------------LS-----G-Q------G------------------------------------P----------M----------KL-------------------------V------------------------------MA-F---------------------------------------------------------------------------------------------------
> str42: M------S-----------N---F---D-----------AI-R---------AL----V-----------------D--T-----DAY-KL---------G---H---------I---------------------H-M----------------------Y--P-E--------------GT--------------------------E------------Y--------V-------LS-----------N----F-------T--D-----------------------R-----G--S----------------RI--E-------G---------------V----------T------------H-TV------H-----------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: M---------------------------------------I-------------E----L-------R------------------------------------H-E--------V-------------QG----D-L--------V---------T--------------------------------I-NV------------V---E----------------TP---------EDL-------D-G-------F---------RD--------------------F----I-R-----AH----------------L-------I----CL-A---------V-D--------T-----------E--T----------------T------GL-D--------IY------------------------------------------------------------------------------------------------------------------------------
> str44: MF-VFL--VLLPLVSSQCV----------------------------------------------------MPL--------FNL----------------I-----T-----------T------N--Q-S-----------------------------Y-------T---NSF------TRGVY--------------YPDKVFRS--S-------VLH--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M------S----------------K--DL---V------A--R--Q------AL-----------------M-------T------A------------R--------------------------------------M-----------K--------A----------D----FV-----------------------------F------------------F--L------------F--------V--LW-K--A-LS--------L--------------P------------V---------------P-------T-------------RC---------------Q-----ID--M---------AK-----------------------------K-------L---SA-----------G---------------------------------------------------------------------------------------------------------
> str46: M-A----S-LL-------------K----------SL----T--L--F----------------K--R-----------T-------------------R---D-----QP----------P------L---A------------------S--------G----S---------------G--G-----------A--I-------R--G-----------------------I---------------------K---H-----V-----I------I---VL---------IP--G------D---------------S----S-I-----------------V----------TRS------R-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M-------------------R-----------V-----R-----------G----I---L-------RN-------------------------W--------------Q-------------------Q----------------------------------------------------------------------------------------------------------------------------W-----------------------WI--------------------------------------------------------------WT-S-L---G---------------------------F------------------------------------------------W----M--F---------------------------------MICS--------------V----VG------------NL----------WVTVYYGVPVWKEAKTT
> str48: M-AV--E----P-----------F-------------PR---R------------------P------------------I-------T----------R----------P-------------------------H--------A-----S-I------------E---------V-----------D------T-SGI----------G-------------------G---------S--A-----G------------S-----------S--E---------K-----------V-----------------------------------F--C--------L-I-G--QAE--------G--GE----------------------P-N---------------T----------V------------------------------------------------------------------------------------------------------------------
> str49: MF-------------------------------------------------YA---------------------------------------------------HA-------------------F----G-----------------------------GY--------D--------------------------------------E-------N--LH---------------------A-------------F-----PG-------I-S-----ST-V---------A--------------------N----------D-V---------R--KY---SV--------------------------V----------S-----------------V------Y-----------------N-------------K-----K---YN--I----------V--K---------NKYMW----------------------------------------------------
> str50: M-A----------------N-------------------------------Y--------S---K-------P---------F-L-----L------------D----------IV---------FN-------KD-----I--------K------------------------------------------------------------------------------C----IN--D-S--------------------------------------------------------------------------------------------C-----S------------H------S-D----------------C--R----Y-------------QS----NS-Y-----------V-------E-----------------------LR-------------------------------RN---------------------QALNKNL--------------------
> 
> solution is feasible: True
> ```
