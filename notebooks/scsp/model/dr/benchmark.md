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
    solution = scsp.model.dr.solve(instance)
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
> --- Solution (of length 68) ---
>  Sol: itkgnekojiqfouhlcimpnbvaxnhtqgxycozgbrddbcsovxiorsuqzpplpvinngfssbxf
> str1: -tkgn-k------uh---mp----xnhtqgx---z---------vxi--s------------------
> str2: i------ojiqfo--l----nb--x-----x-c-----------v----suq-p---vi----ssbxf
> str3: -------------u-lci--n----------yco--------sov--o----zpplp-----------
> str4: i--g-e----------------va----------zgbrddbcs-v---r--------v-nngf-----
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
> --- Solution (of length 127) ---
>  Sol: eingojipbdevaqdcrtkzfgjtbnkuhlcimpvxdnerddbycopflrhnzbrsmosbvigpleowtxqgxckrdrlctodtmzprplpucpmqvxbbghinngfstdfuiqpvcdissbowdxf
> str1: -----------------tk--g---nkuh---mp-x-n------------h-----------------t-qgx------------z----------vx----i----s-------------------
> str2: -i--oji------q------f------------------------o--l--n-b---------------x--xc----------------------v----------s---u-qpv--issb---xf
> str3: ---------------------------u-lci-----n-----yco---------s-o--v-----o------------------zp-plp------------------------------------
> str4: -i-g------eva------z-g--b--------------rddb-c----------s----v--------------r--------------------v------nngf--------------------
> str5: -------p-----------------------------------y--p-lr--z----------------x---------------------ucpmqv---g-------tdfui--vcd-s-bo----
> str6: -------pbdev--dc------------------v-d---------pf----z--sm-sb---------------r-----o-------------qv-bb-h-------------------------
> str7: e-n-----b------c---zf-jt----------vx--er------------zbr-----vigple-------------------------------------------------------------
> str8: ----------------r------------------x-------------------------------w-xq---krdrlctodtm-prp--------x-------------------------wd--
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
> --- Solution (of length 168) ---
>   Sol: kriflshtkqagenkvxuwsfhxmpabcqdfijzgnfpeqbcjtvdqcevwbahcokrdxerlcnvpfzksgjmiudbcrsvihtjodqbgkderwxzavntfmoybplngqrbpzvxucbbhefikoshmgopmqvgtowdfuivxcdvsbouqyzpplpvissbxf
> str01: -------tk--g-nk--u---h-mp----------------------------------x----n------------------ht---q-g-----xz-v-----------------x-------i--s---------------------------------------
> str02: --i----------------------------------------------------o----------------j-i-------------q-------------f-o---ln---b---x----------------------------xc-vs--uq--p---vissbxf
> str03: -----------------u--------------------------------------------lc----------i-------------------------n----y-------------c-------os---o---v--o----------------zpplp-------
> str04: --i--------ge--v---------a-------zg-----b----------------rd-----------------dbc-sv------------r----vn--------ng-------------f-------------------------------------------
> str05: ------------------------p--------------------------------------------------------------------------------y-pl---r--z-xuc-------------pmqvgt--dfuiv-cd-sbo---------------
> str06: ------------------------p-b--d--------e-----vd-c-v--------d-------pfz-s--m------s--------b----r---------o------q----v---bbh---------------------------------------------
> str07: ------------en------------bc-----z--f-----jtv--------------xer------z--------b-r-vi-------g----------------pl--------------e--------------------------------------------
> str08: -r--------------x-w---x-----q---------------------------krd--rlc--------------------t-od-------------t-m---p----r-p--x----------------------wd--------------------------
> str09: k-------kqa---------f----------i--g----q--j-------w----ok------------ks--------------------k--r-----------b-l-g---------------------------------------------------------
> str10: ----l-----------x-----x-pab----i------------v------b-------------v--zk----------------o----------z-----------------zv------------------------d--------------------------
> str11: krif-s----a----v-------------------n-----c---dq---w--h--------------z---------c-----------------------------------------------------------------------------------------
> str12: ---------qa-----xu-----------d----g----q----v-qce-wb---------------f---g--i----------jo--------w--------------------------------------------w--------------y------------
> str13: -r---s----------x-----------q---j--nfp--------------a-----d---------------iu----s-i-----qb---e---z------------------------h---ko-hmg------------------------------------
> str14: --i---------------ws-h----------------------v--------hco-----------------miu-----v-----d----d----------m----------------------------------------------------------------
> str15: ------ht--------x-----x-----q---jz-----qbc-t-------ba---k-------n-------------------------------------------------------------------------------------------------------
> str16: ----------------xu-sf------c--f--z---pe---------e-----c----------v-----------------------------w--a-ntfm------gq---z--u-------------------------------------------------
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
> --- Solution (of length 30) ---
>   Sol: bdcbacdbeecdaebdecbadabcdebdde
> str01: -dcb-c----cd--b--c-----c-e----
> str02: bd----dbee---e--e-b-d---------
> str03: --c-acd-eec--eb-e-------------
> str04: ----a---e--d---d----d---debdd-
> str05: ----ac-beec-a-b--c-------e----
> str06: b--ba--be-----bd-cba----------
> str07: b--ba---e---aeb----ada--------
> str08: --------ee---e--ecb-d-b--e---e
> str09: --c--cd-ee-da--d-c--d---------
> str10: bd--a--b---d--b-e--a-a--d-----
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
>   Sol: dacbedabceadbceadebcdabcdbeeabdcdeaa
> str01: d-cb----c----c--d-bc---c--e---------
> str02: ---b-d-----db-e--e--------ee-bd-----
> str03: --c---a-c--d--e--e-c------e--b---e--
> str04: -a--ed-----d----d---d-----e--bd-d---
> str05: -acbe----e---c-a--bc------e---------
> str06: ---b---b--a-b-e---b-d--c-b--a-------
> str07: ---b---b--a---ea-eb--a--d---a-------
> str08: ----e----e----e--e-c--b-dbee--------
> str09: --c-----c--d--e--e--da--d------cd---
> str10: ---b-dab---db-ea-----a--d-----------
> str11: ----ed---e-d---a-----a------a----eaa
> str12: -a----a--ea----a--b-------eea--c----
> str13: ----e-a---a-bc-a---c---cdb----------
> str14: ---b-d---e----eade---a--d-e---------
> str15: --c---a--e-d---ade--------ee--d-----
> str16: ----e--bc-adb--a--b---b---e---------
> str17: d----d--ce----ea--b-d-----e-a-------
> str18: da-b----c--d----de---a----e----c----
> str19: -a----a----d-ce--e--da------ab------
> str20: -a--e----e---c-----c------ee-----eaa
> str21: ---b---b---d---a-e-c-a------a-d--e--
> str22: dac-eda--e-d---a--b-----------------
> str23: -a----a--ea-b-----b---b--b-----c-e--
> str24: d---ed-bc---bc-a-----ab-------------
> str25: d--b-da---a---e---b---bc-b----------
> str26: d---e--b-e-db-e---b--a-c------------
> str27: --c-e----e--bc--d--c--b-d-e---------
> str28: d--beda---ad---a-----ab-------------
> str29: --c-----c----c--d--c--b---e--bdc----
> str30: -a--e----ea--c--d-bc--b-d-----------
> str31: dacbe-a-c----c-----cd---------------
> str32: ----e---ce--bc-----cd-b-db----------
> str33: d----d-b----bce-d----ab--b----------
> str34: -a----a--ea-b--a-----a----e--b----a-
> str35: ----e---c---b-----bc-a------a-dcd---
> str36: d---e--bc----ce----cd-bc------------
> str37: da----a-c---b--a-e--------e--b-c----
> str38: -a---dab-ea----a---c---c--e---------
> str39: da--e---c--db--a---c-a------a-------
> str40: dacb---b---d-ce-d--c----------------
> str41: d---ed-b-e----e---b---b-d-e---------
> str42: --c--da----d-c--d--cda------a-------
> str43: --c-e----e-d-c----b--a----ee--d-----
> str44: --c-e-a--e---c-a-----a------a--c--a-
> str45: d-c-----c----ce---b---b--b--a-d-----
> str46: ---b--a--e----ea-eb---b-d-e---------
> str47: d--b-d---e--b--a---c---cdb----------
> str48: ----e--bc---b-e--e--da----e-a-------
> str49: -a--e----e----e---b---b-db-----c--a-
> str50: d--b-dabce---c----b---b-------------
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
>   Sol: TATACACGGGATAGATCAACTGTCAGA
> str01: -AT----GGGATA---C----G-----
> str02: -ATAC-C----T---TC--C---C---
> str03: ----CACG--A-A--T----TG--A--
> str04: TA-A-A----AT----C---TGT----
> str05: -A-----GG--TA-A-CAA-----A--
> str06: T-T-C-C----TAG-------GT-A--
> str07: T-T----G---TAGATC---T------
> str08: T------GGGA-AG-T----T--C---
> str09: T-T-C-C---A-----CAACT------
> str10: T---C------TA-A--A-C-G--A-A
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
> --- Solution (of length 141) ---
>   Sol: ATGAGCTCAGCTAGATCGATAGCATCATGTCGATCTAGCTAGCGTAGTACGTACGTACAGTAGCTCAAGCTGATATCGATGCATGACTAGCATGCTAGCATGCACTGCTACAGTGCTACGATCAGCTAGTCAACGTARGTG
> str01: -T-AG-T-AG-TAGA-C--T--C--C--G--GA---AG-T-G---A---C--A---A-A----C-C---CTGA-A---A---A-GA--A---TG---G-AT--A-----A-A-T---A---T-A-----------------
> str02: --G-G---A--TA-A---A---CA-C-T--C---C---C--G---A--A---A---A---TA----A---T--T-T-GA--C-T---TA--A----A-CA---AC-GC----G----AC-A---G-T--TCAA-G------
> str03: AT-A-C-C---T---TC-----C-T-A-G--G-T--A---A-C--A--A---AC---CA--A-C-CAA-CT--T-T---TG-AT--CT--C-T--T-G--T--A--G--A---T-CT--G---------------------
> str04: -T-A----A---A--T---TA---T-A-----ATCT---TA---TA---C-TA-GTA-A--A----AA----ATA--G--G---G--T-G--T---A--A--C-C-G--A-A-----A--A-C-G---GTC----------
> str05: -T----T-A---A-A---A---CA----G-C---CT-G-T-G-G--GT---T--G--CA----C-C---C--A---C--T-CA---C-AG---G---GC---C-C----AC--TG----G----GC--G-CAA-G------
> str06: ATGA-CT----T----C-----CA--ATG--GATC---C---C--A--AC---C-T-CA--AGCT-----T-----C----CA---C---C---C---CA---A-TG-----GT--T----TCAGC---------------
> str07: A--A-C--A---A-A-C-----CA--A---C---C-A---A-C-T--T---T---T---G-A--TC----T-----C--T---TG--TAG-AT-CT-G--T----T-CT-C--T---A--A--A-C--G--AAC-------
> str08: ATGA----A---A-A-CGA-A--A--AT-T--AT-TA--T--C--A--A-G---G----GTA--T---G--GA-A--G-TG---GA--AGC-TG--A-C--G-A-----A-A-T---------------------------
> str09: A----CTC-G---G--C--T-GCAT---G-C--T-TAG-T-GC--A---C-T-C--AC-G---C--A-G-T-ATA---AT---T-A--A---T---A--A--C--T---A-A-T--TA-----------------------
> str10: -T----T--G-TAGATC--T-G--T--T--C--TCTA---A----A---CG-A---AC--T---T-----T-A-A---A---AT--CT-G--TG-T-G---GC--TG-T-CA---CT-C----------------------
> str11: --G--C--AG--AG--C-AT----T--T-TC--T--A---A---TA-T-C---C--ACA--A----AA--TGA-A--G--GCA--A-TA--AT--T-G--T--ACT---AC--T-C-------------------------
> str12: ATGAGC-CA---AGATC-----C-----G---A-C--G--A----AG-A-G--C---C-----C-CAAG--GA----G--G-A-GA--AG---G--AG---G----G--AC----C--C---C--C---------------
> str13: -T---CTCA-C-AG-T---T--CA--A-G---A---A-C---C------C--A---A-AGTA-C-C---C------C----C----C-A---T---AGC---C-CT-CT----T---A--A--AGC----CA-C-------
> str14: A-G-G-T----T---T--ATA-C--C-T-TC---CTAG---G--TA--AC--A---A-A----C-CAA-C------C-A---A---CT----T--T--C--G-A-T-CT-C--T--T--G-T-A-----------------
> str15: A-G-G-T----T---T--ATA-C--C-T-TC---C---C-AG-GTA--AC--A---A-A----C-CAA-C------C-A---A---CT----T--T--C--G-A-T-CT-C--T--T--G-T-A-----------------
> str16: -T-A----A---A-A-C-A-A-C-TCA-----AT--A-C-A----A---C--A--TA-AG-A----AA----AT--C-A---A---C--GCA----A--A---A-----ACA---CT-C-A-CA---A---A---------
> str17: -----C-C-GC-----C-----CAT--T-T-G-----G---GCG--G--C-T-C-T-C-G-AGC----G---ATA--G---C-T--C--G--T-C--G-A---A-T-C--C----CT-CGA-C--CT--------------
> str18: AT-A-C-C---T---TC-----C--CA-G--G-T--A---A-C--A--A---AC---CA--A-C-CAA-CT--T-TCGAT-C-T--CT----TG-TAG-AT-C--TG----------------------------------
> str19: -T---CTCA-C-AG-T---T--CA--A-G---A---A-C---C-T----C--A---A--GT--CTC---C------C----C----C-A---T---AG---GC-CT-CT----T--T-C-A---G-T---CA--G------
> str20: --GA--TC---T----C--T--C-TCA---C---C--G--A----A---C---C-T---G--GC-C---C------CG--G---G-C-A--A----A---TGC-C--CTA-A-T-C--C-A---G--AG-----GT--G--
> str21: A-GAGC--A---A--TC-A--G--T---G-C-ATC-AG--A----A--A--TA--TAC-----CT-A---T--TAT--A--CA---CT----T--T-GC-T--A-----A--G----A--AT-------------------
> str22: A--A--T----TA-A---A-A-CATC-T--C-A---A--TA-C--A--AC--A--TA-AG-A----AA----A-A-C-A---A---C--GCA----A--A---A-----ACA---CT-C-AT-------------------
> str23: A--A----A-C--GA---A---C-T--T-T--A---A---A----A-T-C-T--GT---GT-G-----GCTG-T--C-A--C-T--C--G---GCT-GCATGC--T--TA--GTGC-------------------------
> str24: AT-A----A-CTA-AT---TA-C-T---GTCG-T-T-G--A-C--AG---G-AC--AC-G-AG-T-AA-CT-----CG-T-C-T-A-T--C-T--T--C-TG---------------------------------------
> str25: ATGAG-T--G-T----C-A---C-----G---A---A--T----T----C--ACGTACA--A--T---G---A-A-C--TG---GA-T-G--T--T--CA--C---G-T---G-G--A--AT-A---A-------------
> str26: A----C-C-G-T-G---G---GC-----G---A----GC--G-GT-G-AC---CG----GT-G-TC----T--T--C----C-T-A---G--TG---G---G---T-C--C----C-ACG-T----T-G--AA----R---
> str27: A--A----AG---G-T---T----T-AT----A-C---CT----T----C---C---CAG--G-T-AA-C--A-A---A--C----C-A--A--C---CA---ACT--T----T-C---GATC---T---C----T---TG
> str28: A-G---T-AG-T---TCG----C--C-TGT-G-T---G--AGC-T-G-AC--A---A-A----CT-----T-A----G-T--A-G--T-G--T--T----TG---TG--A--G-G--A---T----TA-------------
> str29: -T----T----TA--T--A---C--C-T-TC---CTAG---G--TA--AC--A---A-A----C-CAA-C------C-A---A---CT----T--T--C--G-A-T-CT-C--T--T--G-T-AG--A-T-----------
> str30: ATG--C---G---G-TCG-T--C-TC-T--C---C---C---CG--G--C-T---T----T---T-----T--T-TC----C----C---C--GC--GC---C---GC----GT--T--G----GC--G-C--CG-A----
> str31: --G---T--G--A---C-A-A--A--A-----A-C-A--TA----A-T--G---G-AC--T--C-CAA-C--A---C----CATG--T--CA----AGC-T----T--T-CAG-G-TA-GA-C------------------
> str32: --G---T--G-TA-A--GA-A--A-CA-GT--A---AGC---C------CG---G-A-AGT-G-----G-TG-T-T---T---TG-C--G-AT--T----T-C---G--A--G-GC--CG----G----------------
> str33: --GAG---A---A--T-GA--G--TC-T--C-AT-TA-C---CG-----C---C---C-G--G-T-A--CT--TA--G---CA--A---GC-T---A--AT--A--G-T-CA---C---G----GC---------------
> str34: ATG---T--G---G-TCGAT-GC--CATG--GA----G---GC------C---C--AC-----C--A-G-T--T--C-AT---T-A--AG---GCT--C---C--TG-----G--C-A---T----T--------------
> str35: A----C---G--AG--CG-T----T--T-T--A---AG---G-G-----C---C---C-G---C----G---A---C--TGC--GAC--G---GC---CA--CA-TG-----G--C--C---C---T-GT-A---T--GT-
> str36: --G-G-T----T---T--ATA-C--C-T-TC---C---C-AG-GTA--AC--A---A-A----C-CAA-C------C-A---A---CT----T--T--C--G-A-T-CT-C--T--T--G-T-AG----------------
> str37: -TG-G----G--A-A--G-T----TC----C-A---A---A----AG-A--T-C--ACA--A----AA-C--A---C--T--A---C---CA-G-T--CA---AC--CT---G----A--A---G-TA--CA-C-------
> str38: --GA----AGC--G-T---TA--A-C--GT-G-T-T-G--AG-G-A--A---A---A--G-A-C--A-GCT--TA--G--G-A-GA--A-CA----AG-A-GC--TG-----G-G--------------------------
> str39: A----C-CAGC--G--C-A---C-T--T--CG-----GC-AGCG--G--C--A-G--CA----C-C----T-----CG--GCA-G-C-A-C---CT--CA-GCA--GC-A-A---C-------------------------
> str40: ATG-G----G--A---C-A-A-C-T--T----AT-T--C---C-TA-T-C--A--T---GT-GC-CAAG---A----G--G--T---T----T--TA-C---C-C-G-----GTG--AC---CA-----------------
> str41: -T----T--G-TAGATC--T-G--T--T--C--TCTA---A----A---CG-A---AC--T---T-----T-A-A---A---AT--CT-G--TG-T-G---G---T--T---GT-C-AC--TC------------------
> str42: A--A-C-CA---A---C-----CA--A---C--T-T---T--CG-A-T-C-T-C-T----T-G-T-A-G---AT--C--TG--T---T--C-T-CTA--A---AC-G--A-A---CT----T----TA-------------
> str43: --G-G----G-T---TC--T-GC--CA-G--G--C-A--TAG--T----C-T---T----T---T-----T--T-TC--TG---G-C--G---GC---C---C--T--T---GTG-TA--A--A-C----C----T--G--
> str44: --G-GCT--GC-A--T-G----C-T--T----A----G-T-GC--A---C-T-C--AC-G---C--A-G-T-ATA---AT---T-A--A---T---A--A--C--T---A-A-T--TAC--T--G-T--------------
> str45: -TG--C--A--T-G--C--T----T-A-GT-G--C-A-CT--C--A---CG--C--A--GTA--T-AA--T--TA---AT--A--ACTA--AT--TA-C-TG---T-C----GT---------------------------
> str46: -T----TC--C-A---C-A-A-C-T--T-TC---C-A-C---C--A--A-G--C-T-C--T-GC--AAG---AT--C----C----C-AG-A-G-T--CA-G----G-----G-GC--C--T--G-T--------------
> str47: -T---CT-A---A-A-CGA-A-C-T--T-T--A---A---A----A-T-C-T--GT---GT-G-----GCTG-T--C-A--C-T--C--G---GCT-GCATGC--T--TA--G----------------------------
> str48: A----C-C-G---GAT-G---GC--C--G-CGAT-T---T----T--T-CG---G-A--GT--C-C----T--T---G--G---G----G---G--A-C---CACT-C-A--G----A--AT-AG--A-------------
> str49: -----CT----T-G-T--A--G-ATC-TGT---TCT--CTA----A--ACG-A---AC--T---T-----T-A-A---A---AT--CT-G--TG-T-G---GC--TG-T-CA---CT------------------------
> str50: ATGAGC--A-CTA-A--G----C-----G---A---AG--A----A---C---C--A-A--A----AAGC--A----GA--CA--A-TA-CA----A-C---C-C-GCTA---T--TAC----------------------
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
> --- Solution (of length 50) ---
>   Sol: MEQSKAFPLSVEYACHPGFLRVNEQTAHFDAIGRAKRLHDNPSRNGTVYQ
> str01: M----A--LS--Y-C-P------------------K---------GT---
> str02: M-QS-----S---------L--N---A----I---------P-----V--
> str03: M------PLS--Y-----------Q--HF----R-K--------------
> str04: ME---------E---H-----VNE-------------LHD----------
> str05: M--S------------------N-----FDAI-RA--L------------
> str06: M-----F-------------R-N-Q---------------N-SRNG----
> str07: M-----F-----YA-H----------A-F---G------------G--Y-
> str08: M--SK-F------------------T-------R--R----P------YQ
> str09: M--S--F---V--A---G---V---TA----------------------Q
> str10: ME-S----L-V-----PGF---NE--------------------------
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
> --- Solution (of length 491) ---
>   Sol: MAFVEFSLVLLPGFLNREKTHVDINQLAFSILPRSQCDTVLAEGKRPQTVSYIVNRGSLFKPTQAGIDERLMPSYTNVELSFHATERDGNKMQTVLWAPSICEDANYKTEFVNLYGPDIKSVFEATRQGHLSNQSKVDLIAHSGIPYEFNTIKLQRNSGVYPDCTILENGKSAVFRAHEQLSWDYALSTPRGEFVLDHAMSTYVESQLYFPADKSVRFEGTNIRGSSVAHILKDGTEYNPHRVALEGIKSNADLEVKTFARYCDNSGLEQHITSAMDFERGPWVLKAICNSFDRPGTAFIYQDLEGVAESGMTNEKLQHRAGPNVDKSILPGQYDTFRVEHCLDIRNPDSMWKIVLTGDRSEYNQADCHLFIRAGVWDTYEPQSTRNVIEADSTKAGKEGILQRPDEANLHSVFQCKDAEFRTDDCHGIAECKLHIMAKKLSSAGRKHRVLHSTWYMNFMICFISVKVGNKLYMWVTVYYGVPVWKEAKTT
> str01: M---------------R---H-----L---------------------------N-----------ID--------------------------------I-E-----T-----Y-----S----------SN----D-I------------K---N-GVY---------K-------------YA----------D-A-----E-------D----FE---I--------L------------L-------------FA-Y---S-----I----D---G--------------G--------E-V-E--------------------------------CLD-----------LT--R-----------------------------------------------------------------------------------------------------------------------------------
> str02: M---E-----------R----------------R-------A----------------------------------------H---R------T-----------------------------------H---Q---------------N--------------------------------WD-A--T------------------------K-------------------------P-R---E--------------R------------------R-----K---------------Q----------T----QHR---------L-----T----H------PD---------D-S----------I-------Y-P---R--IE----KA--EG---R------------K--E---D--HG---------------------------------------------------------------
> str03: M---E------PG--------------AFS--------T--A----------------LF-------D---------------A-----------L-----C-D-------------DI-----------L----------H-------------R-------------------R----L-----------E-------S-----QL--------RF-G----G--V-----------------------------------------Q-I---------P------------P---------E-V--S---------------D----P------RV-----------------------Y--A--------G----Y----------A----------L-------L---------------------------------------------------------------------------------
> str04: M-----------G-----K---------F----------------------Y----------------------Y-----S--------N------------------------------------R----------------------------R----------L-----AVF-A--Q-----A--------------------Q-------S-R------------H-L--G-----------G--S-----------Y------EQ------------W-L-A-C-----------------V--SG--------------D-S-------------------------------------A----F-RA------E------V------KA-------R--------V-Q-KD-------------------------------------------------------------------------
> str05: --F--F----------RE------N-LAF------Q-----------Q--------G---K---A----R--------E--F----------------PS--E------E--------------A-R-------------A--------N-------S---P--T------S---R--E-L-W-----------V---------------------R------RG---------G---NP----L----S----E----A------G-------A---ER-------------R-GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: M---------------------D---------P-S-----L-------T--------------Q-------------V------------------WA-------------V-----------E----G--S----V-L---S-----------------------------A---A-----------------V-D----T---------A------E-TN-----------D-TE--P------------D-E-----------GL-----SA---E----------N--------------EG--E---T------R--------I---------------IR-------I--TG--S----------------------------------------------------------------------------------------------------------------------------------
> str07: MAF-------------------D-----FS---------V--------T-------G-------------------N-------T-----K----L-------D----T-----------S-------G-------------------F-T---Q---GV-----------S---------S-----------------M-T-V-------A----------------A-----GT--------L--I---ADL-VKT-A-----S-------S---------------------------Q-L--------TN--L---A-----------Q----------------S---------------------------------------------------------------------------------------------------------------------------------------------
> str08: MA-V-------------------I--L-----P-S---T------------Y----------T----D--------------------G----T---A------A----------------------------------------------------------CT---NG-S-----------------P------D------V-----------V---GT---G----------T---------------------------------------M------WV-----N------T--I---L------------------P--------G--D-F---------------------------------F-----W-T--P-S------------G-E------------SV--------R---------------------------V-----------------------------------------
> str09: M--------------N---T-----------------------G--------I-------------ID--L----------F-----D-N---------------------------------------H------VD----S-IP----TI-L-------P---------------H-QL----A--T------LD-----Y----L-------VR---T-I-------I--D--E-N--R-------S-----V-----------L----------------L------F--------------------------H---------I---------------------M------G--S-------------G--------------------------------------------------------------------------------------------------------------------
> str10: M-FV-F-LVLLP--L------V-------S----SQC--V--------------N---L----------R-----T----------R------T---------------------------------Q--L--------------P---------------P----------A-----------Y---T--------------------------------N---S--------------------------------F-------------T------RG--V----------------Y--------------------------------Y-------------PD---K-V---------------F-R----------S--------S-------------------V--------------------LH------S-------------------------------------------------
> str11: M---------------------D------S--------------K-----------------------E------T------------------------I------------L----I----E---------------I----IP------K------------I----KS------------Y-L--------LD----T-------------------NI--S-------------P--------KS-----------Y--N-----------DF---------I--S--R-------------------N-K-------N----I-------F-V-----I-N--------L------YN-----------V-------ST---I------------------------------------------------------------------------------------------------------
> str12: M------L-L-------------------S-------------GK---------------K-----------------------------KM---L-----------------L---D--------------N-------------YE--T---------------------A---A--------A----RG------------------------R--G----G--------D--E----R------------------R------------------RG-W---A----FDRP--A-I------V-----T--K---R-----DKS------D--R------------M--------------A--H--------------------------------------------------------------------------------------------------------------------------
> str13: M--------------N---------------------------G------------------------E---------E--------D---------------D-N---E-----------------Q------------A-------------------------------A---A-EQ--------------------------Q-------------T-----------K---------------K--A----K---R-------E----------------K--------P--------------------K-Q--A----------------R--------------K-V-T---SE---A----------W---E-----------------------------H--F---DA---TDD--G-AECK-H--------------------------------------------------------
> str14: M---E-SLV--PGF-N-EKTHV---QL--S-LP------VL------Q-V-----R-----------D---------V-L--------------V-------------------------------R-G-------------------F---------G---D--------S-V----E-------------E-VL----S---E------A----R----------------------------------------------------QH-------------LK------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M---------------R----------------------------------YIV---S---P-Q------L------V-L------------Q-V--------------------G---K--------G----Q-------------E-----------V-------E-------RA---L---Y-L-TP------------Y---------D------------------------Y---------I----D-E-K--------S---------------P-----I------------Y--------------------------------Y--F-----L--R---S------------------HL----------------N-I-------------QRP--------------------------------------------------------------------------------------
> str16: M----------P----R----V----------P------V-----------Y---------------D-----S------------------------P----------------------------Q--------V-----S--P---NT--------V-P-----------------Q-----A----R----L--A--T--------P---S--F----------A------T---P-----------------TF-R-----G-------A-D---------A-------P--AF--QD---------T-------A--N--------Q-------------------------------QA------R---------Q------------------------------------------------------------------------------------------------------------
> str17: M-FV-F-LVLLP--L------V-------S----SQC--V--------------N---L----------R-----T----------R------T---------------------------------Q--L--------------P-------L------------------A-----------Y---T--------------------------------N---S--------------------------------F-------------T------RG--V----------------Y--------------------------------Y-------------PD---K-V---------------F-R----------S--------S-------------------V--------------------LH------S-------------------------------------------------
> str18: M-FV-F-------F-------V----L----LP-------L--------VS------S-----Q-------------------------------------C---------VNL-----------T------------------------T----R--------T--------------QL--------P--------------------PA-------------------------Y-------------------T------NS-----------F------------------T----------------------R-G--V--------Y----------------------------Y------------------P---------D--K-----------------VF-------R-------------------SS------VLHS--------------------------------------
> str19: M---E----------------------A--I---------------------I----S-F----AGI---------------------G-----------I----NYK-----------K----------L--QSK--L---------------Q----------------------H-----D---------F-------------------------G---R---V---LK----------AL------------T-------------------------V------------TA---------------------RA--------LPGQ--------------P----K---------------H--I-A--------------I--------------R----------Q----------------------------------------------------------------------------
> str20: MA----S----------------------S-------------G--P---------------------ER-------------A-E-------------------------------------------H---Q-----I----I--------L-------P-----E---S-----H--LS-----S-P-----L-------V---------K---------------H--K-----------L--------L-------Y--------------------------------------Y--------------------------------------------------WK--LTG-----------L-----------P-------------------L--PDE--------C-D--F--D--H------L-I-------------------------------------------------------
> str21: M---E-SLV--PGF-N-EKTHV---QL--S-LP------VL------Q-V-----R-----------D---------V-L--------------V-------------------------------R-G-------------------F---------G---D--------S-V----E-------------E-VL----S---E----------VR----------------------------------------------------QH-------------LK------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L-------------------A----P-S-----------P-------N--S--K-----I-------------------------Q--L--------------F-N-------------------N------I---------N-I----------D--I--N---------------Y-------E----H---T-----LYF-A--SV---------S--A----------------------------------------Q-------------------NSF------F--------A---------Q---------------------------------W--V--------------------V---Y---S------AD--KA----I------------------------------------------------------------------------------------------
> str23: M-----S--------------------A--I-------T---E-----T-----------KPT---I-E-L-P----------A-----------L-A----E------------G------F----Q---------------------------R----Y-------N-K-----------------TP-G-F-------T------------------------------------------------------------C--------------------VL-------DR------Y-D---------------H--G--V---I-----------------N-DS--KIVL------YN-------------------------------------------------------------------------------------------------------------------------------
> str24: M-----------------K-----N-----I----------AE----------------FK-----------------------------K------AP---E----------L----------A----------------------E----KL------------LE-----VF------S---------------------------------------N---------LK-G---N----------S----------R----S-L--------D----P-----------------------------M-------RAG----K-------------H--D----------V--------------------V-----------VIE--STK--K---L-----------------------------------------------------------------------------------------
> str25: M----------P-------------Q------P-------L---K--Q--S-------L--------D------------------------Q------S-------K--------------------------------------------------------------------------W---L---R-E-----A-----E--------K---------------H-L---------R-ALE---S---L-V-------D-S-----------------------N-------------LE---E-----EKL---------K---P-Q---------L------SM------G---E----D--------V------QS-----------------------------------------------------------------------------------------------------------
> str26: M-FV-F-LVLLP--L------V-------S----SQC--V--------------N---L-------I--------T----------R------T---------------------------------Q---S--------------Y---T-----NS----------------F-------------T-RG--V-------Y-----Y-P-DK-V-F-----R-SSV---L--------H--------S-------T-----------Q------D----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-----------------K---------F--------D-VL---------S-------LF----A-------P-----------------------WA---------K---V-----D-----E---Q-------------------E------------Y-D----------------Q--------------------------QL-------------N----------------N-----------N--LE----------S-----IT-A------P---K-----FD---------D--G-A----T-E-------------I----------E---------S-----------E----------R-G--D----------I------------------------------------------------------------------------------------------------------
> str28: M-FV-F-LVLLP--L------V-------S----SQC--V--------------N----F--T-------------N---------R------T---------------------------------Q--L--------------P-----------S--------------A-----------Y---T--------------------------------N---S--------------------------------F-------------T------RG--V----------------Y--------------------------------Y-------------PD---K-V---------------F-R----------S--------S-------------------V--------------------LH------S-------------------------------------------------
> str29: M-----------------------------------------------------------------------------------------------W--SI-----------------I--V--------L----K--LI--S-I---------Q------P----L-------------L-----L-------V------T---S-L--P--------------------L-----YNP----------N------------------------MD-------------S--------------------------------------------------C-------------------------C-L-I-----------S-R--I----T----------P-E--L--------A--------G----KL-------------------TW-----I-FI---------------------------
> str30: M---E-SLV--PGF-N-EKTHV---QL--S-LP------VL------Q-V-----R-----------D---------V-L--------------V-------------------------------R-G-------------------F---------G---D--------S-V----E-------------EF-L----S---E------A----R----------------------------------------------------QH-------------LK------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FV-F-LVLLP--L------V-------S----SQC--V-------------------------------MP------L-F-------N-----L----I-------T----------------T------------------------T---Q--S--Y---T---N-----F-------------T-RG--V-------Y-----Y-P-DK-V-F-----R-SSV---L--------H---L------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M-------------------H----Q----I-------TV---------VS-----G----PT-----E--------V--S---T----------------C--------F----G----S---------L----------H---P--F-----Q--S--------L---K------------------P----V----M-----------A---------N------A--L--G-------V-LEG-K--------------------------M-F----------C-S--------I-----G----G--------R-------S-L-----------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: MA-----------------T------L----L-RS-----LA----------------LFK--------R------N-------------K------------D---K--------P----------------------------P-----I------------T------S-------------------G--------S------------------G----G---A-I----------R----GIK---------------------HI---------------I-----------I------V---------------P-----I-PG--D--------------S----------S----------I------T-----TR------S----------R---------------------------------------------------------------------------------------
> str34: M---E-SLV--PGF-N-EKTHV---QL--S-LP------VL------Q-V-----R-----------D---------V-L--------------V-------------------------------R-G-------------------F---------G---D--------S---------------------------M----E-------------E--------V---L-----------------S----E----AR--------QH-------------LK------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FV-F-LVLLP--L------V-------S----SQC--V--------------N---L---T------------T------------G----T---------------------------------Q--L--------------P---------------P----------A-----------Y---T--------------------------------N---S--------------------------------F-------------T------RG--V----------------Y--------------------------------Y-------------PD---K-V---------------F-R----------S--------S-------------------V--------------------LH------S-------------------------------------------------
> str36: MA-------------N-------I------I-----------------------N---L-------------------------------------W--------N---------G--I--V-----------------------P-----------------------------------------------------M---V--Q-----D--V-----N-----VA--------------------S---------------------IT-A--F-------K----S--------------------M----------------I-----D----E----------------T-------------------WD----------------K--K--I-----EAN-------------T--C--I------------S---RKHR--------N---------------------------------
> str37: M------L-------NR------I-Q------------T-L------------------------------M------------------K--T---A-------N------N-Y--------E-T-------------I-------E---I-L-RN---Y-----L--------R----L---Y-------------------------------------I-------IL-----------A----------------R---N---E---------E-G------------R-G---I---L------------------------I----YD--------D--N------I----D-S--------------V-------------------------------------------------------------------------------------------------------------------
> str38: MA--------------------D---------P--------A-G----T-----N-G-----------E---------E---------G----T---------------------G-----------------------------------------------C----NG------------W----------F--------YVE------A---V-----------V--------E-----------K-------KT--------G---------D---------AI--S-D---------D-E--------NE--------N-D-S------DT---------------------G---E----D--L-----V-D-----------------------------------------------------------------------------------------------------------------
> str39: M-FV-F-LVLLP--L------V-------S----SQC--V--------------N---L----------R-----T----------R------T---------------------------------Q--L--------------P---------------P---------S------------Y---T--------------------------------N---S--------------------------------F-------------T------RG--V----------------Y--------------------------------Y-------------PD---K-V---------------F-R----------S--------S-------------------V--------------------LH------S-------------------------------------------------
> str40: M---E-SLV--PGF-N-EKTHV---QL--S-LP------VL------Q-V---------------------------------------------------C-D-------V-L-------V----R-G-------------------F---------G---D--------S-V----E-------------E-VL----S---E------A----R----------------------------------------------------QH-------------LK------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M--------------N--------NQ-------R----------K---------------K-T-A----R--PS-------F-------N-M---L-----------K------------------R-------------A--------------RN------------------R------------------V-----ST-V-SQL---A-K--RF-------S------K-G---------L--------L-----------SG--Q----------GP-----------------------------M---KL-------V-------------------------M--------------A----F------------------------------------------------------------------------------------------------------------------------
> str42: M-----S--------N------------F--------D---A----------I--R--------A-----L------V---------D-----T---------DA-YK-----L-G-------------H---------I-H---------------------------------------------------------M--Y-------P-------EGT---------------EY----V-L----SN-------F-------------T---D--RG---------S--R-----I----EGV-----T-----H----------------T--V-H------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: M----------------------I------------------E---------------L----------R------------H--E--------V--------------------------------QG--------DL--------------------V----TI--N----V--------------------V---------E---------------T------------------P-----E------DL---------D--G----------F-R------------D-----FI-------------------RA-------------------H-L-I----------------------C-L---A-V-DT-E---T--------T--G----L---D----------------------I--------------------------Y-----------------------------------
> str44: M-FV-F-LVLLP--L------V-------S----SQC--V-------------------------------MP------L-F-------N-----L----I-------T----------------T------NQS-----------Y---T-----NS----------------F-------------T-RG--V-------Y-----Y-P-DK-V-F-----R-SSV---L--------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-----S-----------K---D---L------------V-A---R-Q----------------A-----LM---T-------A--R----M---------------K----------------A------------D----------F----------V--------------F------------------F-L-------------F-----V---------------L--------------------------------------------------W--KA----------------L-----S------L-----P-V-----P----T-R---C----------------------Q------I-----D----------------------------------------------------------MAKKLS-AG----------------------------------------------
> str46: MA----SL-L--------K----------S-L------T-L------------------FK--------R-----T----------RD----Q-----P-----------------P-------------L---------A-SG-------------SG----------G--A-------------------------------------------------IRG-----I-K-------H-V----I-----------------------I-----------VL--I------PG------D------S-----------------SI---------V-----------------T--RS-----------R----------------------------------------------------------------------------------------------------------------------
> str47: M---------------R----V-----------R---------G--------I-----L----------R------N-------------------W------------------------------Q-----Q------------------------------------------------W---------------------------------------------------------------------------------------------------W----I---------------------------------------------------------------W----T---S--------L----G--------------------------------------F----------------------------------------W-M-FMIC--SV-VGN-L--WVTVYYGVPVWKEAKTT
> str48: MA-VE------P-F------------------PR-----------RP-----I---------T------R--P---------HA---------------SI-E--------V-----D-------T-----S-----------GI-------------G----------G-SA------------------G--------S----S------------E-------------K---------V---------------F---C----L---I--------G--------------------Q-----AE-G----------G-----------------E-------P---------------N--------------T--------V-------------------------------------------------------------------------------------------------------
> str49: M-F------------------------------------------------Y------------A-----------------HA--------------------------F----G------------G-----------------Y---------------D----EN-----------L----------------HA----------FP--------G--I--SS--------T------VA------N-D--V----R------------------------K--------------Y--------S--------------V-------------V----------S----V-------YN------------------------------K--K---------------------------------------------------------Y-N--I----VK--NK-YMW----------------
> str50: MA-------------N-----------------------------------Y-----S--KP-------------------F-------------L-----------------L---DI--VF---------N--K-D-I------------K----------C-I--N--------------D---S--------------------------------------------------------------------------C--S----H--S--D-----------C----R------YQ-------S---N-------------S-----Y----VE--L--R-------------R---NQA---L----------------N-------K-------------NL---------------------------------------------------------------------------------
> 
> solution is feasible: True
> ```
