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
Model = scsp.model.linear1_hexaly.Model
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
>  Sol: ultcikgnycokesjioqvfuhoazlmpgbrpdndbxxcsvsrpvulnhtnqpgxzvxissbxf
> str1: --t--kgn---k--------uh----mp--------x----------nht-q-gxzvxis----
> str2: ----i-----o---ji-q-f--o--l-------n-bxxc-vs---u-----qp---v-issbxf
> str3: ul-ci--nyco--s--o-v---o-z--p---p--------------l-----p-----------
> str4: ----i-g-----e-----v----az---gbr-d-db--csv-r-v--n--n--g---------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 64
> best bound: 26.0
> wall time: 59.10s
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
> --- Solution (of length 154) ---
>  Sol: piypglulebrczdxucepmxwxeqivokvdrdrgljtkcvgvdifnpakuhuimpnqbfolfivzgytbrccddbcsvzrodfsjbtomtvvxnzsozpphvnlnntbmxsxcbrovsupqggxzqpwvibsxsbbxfiserzdhbrvigple
> str1: -------------------------------------tk--g----n--kuh--mp-------------------------------------xn------h-----t-------------qg-xz---v---x-----is-------------
> str2: -i-------------------------o--------j-------i------------q-fol--------------------------------n-------------b-x-xc---vsu-q-----p-vi-s-sb-xf---------------
> str3: ------ul---c-------------i--------------------n--------------------y---c---------o--s---o--v-----ozpp---l---------------p---------------------------------
> str4: -i--g---e-----------------v---------------------a----------------zg--br--ddbcsv-r----------v--n--------n------------------g---------------f---------------
> str5: p-yp-l----r-z-xuc-pm----q-v-------g--t-----d-f----u--i----------v------c-d---s--------b-o-----------------------------------------------------------------
> str6: p--------b---d---e--------v---d--------cv--d---p-----------f-----z-----------s-----------m------s-----------b------ro----q-------v-b---b---------h--------
> str7: --------e-------------------------------------n-----------b------------c-------z---f-j-t---v-x-----------------------------------------------erz--brvigple
> str8: ----------r---x------wx-q---k--rdr-l---c----------------------------t------------od----t-m---------p---------------r----p---x---w---------------d---------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 154
> best bound: 26.0
> wall time: 60.09s
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
> --- Solution (of length 280) ---
>   Sol: kprixullcigewpqnyvaxrinycixzfgbqiwrdojdbastpkisxkqrlfoplrdqbczsavnxrjasblnfngcbxuxdkqcvvwhinktusdpmqpafvgsosdtkrumhihptjfuhsiqambtvxeerzvdvfzhpxhupfxcfzpebeicvwaxzvisdsrpnomntikcdsczfnxghiohqcoxjuntwqumgkobkvqkddgsjzbozuqxzkrvigbzwcgqtdbpvvdqcewapblgkefgxplixpjowwnzfyismsbroqvbbh
> str01: ------------------------------------------t-k-------------------------------g--------------nk-u-------------------h------------m--------------px--------------------------n---------------h----------t-q--g------------------xz--v----------------------------x--i-----------s----------
> str02: ---i--------------------------------oj-------i---q--fo-l---------n-----b-------x-x---cv--------s----------------u------------q----------------p---------------v-----is-s-------------------------------------b---------------x------------------------------f---------------------------
> str03: -----ul-ci-----ny-------c-----------o----s-----------o----------v-----------------------------------------o----------------------------z------p---p-----------------------------------------------------------------------------------------------------l------p------------------------
> str04: ---i------ge-----va--------z-gb---rd--db--------------------c-s-v--r------------------v----n------------------------------------------------------------------------------n--------------g------------------------------------------------------------------f---------------------------
> str05: -p--------------y--------------------------p-------l----r----z----x-------------u----c-----------pmq---vg----t---------------------------d-f-----u----------i-v------------------cds-------------------------b-----------o--------------------------------------------------------------
> str06: -p----------------------------b----d------------------------------------------------------------------------------------------------e---vd-----------c--------v-------d--p------------f--------------------------------z-----------------------------------------------------smsbroqvbbh
> str07: -----------e---n--------------b-----------------------------cz------------f--------------------------------------------j---------tvxe-rz------------------b-------------r--------------------------------------v------------------ig---------p----------l--e----------------------------
> str08: --r-x-------w------x-----------q------------k-----r------d---------r----l----c---------------t------------o-dt---m---p----------------r-------px---------------w------d-----------------------------------------------------------------------------------------------------------------
> str09: k-------------------------------------------k----q-------------a----------f---------------i-------------g--------------------q--------------------------------------------------------------------j---w-----o-k--k---s---------kr---b-------------------lg------------------------------
> str10: ------l------------x------x----------------p-------------------a-------b------------------i------------v------------------------b-v----z----------------------------------------k-----------o--------------------------z--z------v---------d--------------------------------------------
> str11: k-ri------------------------f------------s---------------------avn-----------c----d-q---wh---------------------------------------------z-------------c----------------------------------------------------------------------------------------------------------------------------------
> str12: --------------q---ax------------------------------------------------------------u-d---------------------g--------------------q----v-----------------------------------------------------------qc---------------------------------------------------ew--b----fg---i--joww---y------------
> str13: --r--------------------------------------s-----x-q------------------j----nf----------------------p---a------d------i-----u-siq--b---e--z-----h----------------------------------k-----------oh-----------mg-----------------------------------------------------------------------------
> str14: ---i--------w----------------------------s-----------------------------------------------h-------------v----------h----------------------------------c---------------------om--i-------------------u-----------v--dd----------------------------------------------------------m---------
> str15: -----------------------------------------------------------------------------------------h---t-------------------------------------x-----------x----------------------------------------------q---j--------------------z----q-------b--c--t-b--------a----k-------------n---------------
> str16: ----xu-----------------------------------s----------f-------c-------------f------------------------------------------------------------z------p----------e-e-cvwa---------n---t-------f------------------mg-----q------z---u------------------------------------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 280
> best bound: 25.0
> wall time: 59.91s
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
> --- Solution (of length 34) ---
>   Sol: bdbaedcdabdbbcecdeeebdcbaadbacebed
> str01: -d----c--b---c-cd---b-c------ce---
> str02: bd---d---b----e--eeebd------------
> str03: ------c-a----c--dee---c-------ebe-
> str04: ---aed-d--d-----de--bd----d-------
> str05: ---a--c--b----e--e----c-a--b-ce---
> str06: b-ba-----b----e-----bdcba---------
> str07: b-bae---a-----e-----b---a-d-a-----
> str08: ----e---------e--ee---cb--db--e-e-
> str09: ------c------c--dee--d--a-d--c---d
> str10: bd-a-----bdb--e---------aad-------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 34
> best bound: 12.0
> wall time: 60.03s
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
> --- Solution (of length 358) ---
>   Sol: eddcdaabadedabcabbedccccbcaaccdacecdedbdeedbadcddeeedacaacdeabccddbbcaaedbdabcddcbeeaeceebbddceddbadddaeeaeedabdebbebcbbbaadccdeeabdaccaeeaacdaedaaaadcebecebdeaacdebcdadbabeaeebabeebbdedaeeeddcedaebccdaabbabaedadccecaabaabbecebaeeeccccdeedacbccabcbbddbedebebebbbdeecbddaaaabceebccaadeaabeaabedabdbcbddbddadbebadcedbbdddaaedbaeeebbcdcbecdbeacacaeaedceecadbaab
> str01: -d-c---b------c-----c---------d-------b-------c-------c----e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str02: -------b-d-d-b----e--------------e--e---e--b-d------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str03: ---c-a--------c----d-------------e--e---------c--e-----------b---------e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: -----a----ed-------d----------d----de-bd--d---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str05: -----a--------c-b-e--------------ec---------a----------------bc--------e----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: -------b-----b-ab-e-----b-----d-c-----b-----a-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str07: -------b-----b-a--e-------a------e----b-----ad-------a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: e---------e-------e--------------ec---bd---b-----ee-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str09: ---c----------c----d-------------e--ed------adcd----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: -------b-d--ab-----d----b--------e----------a--------a----d-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: ed--------eda--a----------a------e----------a--------a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: -----aa---e-a--ab-e--------------e----------a-c-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str13: e----aab------ca----cc--------d-------b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str14: -------b-de-------e-------a---d--e----------ad---e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: ---c-a----eda------d-------------e--e---e-d---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: e------b------ca---d----b-a-----------b----b-----e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: -ddc------e-------e-------a-----------bde---a-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: -d---a-b------c----d----------d--e----------a----e----c---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: -----aa--d----c---e--------------e-d--------a--------a-------b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: -----a----e-------e-cc-----------e--e---e---a--------a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str21: -------b-----b-----d------a------ec---------a--------a----de----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: -d---a--------c---ed------a------e-d--------a----------------b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str23: -----aa---e-ab--bb------bc-------e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str24: -d--------ed-bc-b---c-----aa----------b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: -d-----b-d--a--a--e-----b-------------b-------c--------------b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: -d--------e--b----ed----b--------e----b-----a-c-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: ---c------e-------e-----bc----d-c-----bde-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str28: -d-----b--eda--a---d------aa----------b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: ---c----------c-----c---------d-c-----b-e--b-dc-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str30: -----a----e-------e-------a-c-d-------b-------c--------------b--d-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: -d---a--------c-b-e-------a-cc--c--d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: e--c------e--bc-----c---------d-------bd---b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: -dd----b-----bc---ed------a-----------b----b--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: -----aa---e-ab-a----------a------e----b-----a-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: e--c---b-----bca----------a---d-c--d----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: -d--------e--bc-----c------------ecd--b-------c-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str37: -d---aa-------c-b---------a------e--e-b-------c-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str38: -----a---d--ab----e-------aacc---e------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str39: -d---a----e---c----d----b-a-c--a------------a-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: -d---a--------c-bb-dc------------e-d----------c-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: -d--------ed-b----e--------------e----b----b-d---e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: ---cda---d----c----dc---------da------------a-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: ---c------e-------edc---b-a------e--ed--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: ---c------e-a-----e-c-----aa---ac-----------a-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: -d-c----------c-----c------------e----b----b-----------------b-------a--d---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str46: -------ba-e-------e-------a------e----b----b-d---e--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: -d-----b-de--b-a----cc--------d-------b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str48: e------b------c-b-e--------------e-d--------a----e---a----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: -----a----e-------e--------------e----b----b-d---------------bc------a------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str50: -d-----b-d--abc---e-c---b-------------b-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 358
> best bound: 10.0
> wall time: 59.97s
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
> --- Solution (of length 29) ---
>   Sol: ATTAGACCACTAGGATAGATCCTGAAATC
> str01: AT--G-------GGATA---C--G-----
> str02: AT-A--CC--T----T----CC------C
> str03: ------C-AC--G-A-A--T--TGA----
> str04: -T-A-A--A--A---T----C-TG---T-
> str05: A---G-------G--TA-A-C---AAA--
> str06: -TT---CC--TAGG-TA------------
> str07: -TT-G-----TAG-AT----C-T------
> str08: -T--G-------GGA-AG-T--T-----C
> str09: -TT---CCAC-A--A-----C-T------
> str10: -T----C---TA--A-A---C--GAA---
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 29
> best bound: 12.0
> wall time: 59.87s
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
> best bound: 50.0
> wall time: 73.20s
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
> --- Solution (of length 52) ---
>   Sol: MMMEQSSKFTPARLSEYNQRHVYNNAFVSELHDACIPYGRKFNVGEGTALQY
> str01: M----------A-LS-Y-----------------C-P---K---G--T----
> str02: M---QSS------L---N-------A---------IP------V--------
> str03: M---------P--LS-Y-Q-H-----F------------RK-----------
> str04: M--E-----------E----HV-N-----ELHD-------------------
> str05: M----S-----------N--------F-----DA-I---R--------AL--
> str06: M-------F---R----NQ----N----S----------R--N-G-------
> str07: M-------F-------Y--------A-----H-A-------F--G-G----Y
> str08: M----S-KFT--R------R----------------PY------------Q-
> str09: M----S--F------------V---A------------G----V---TA-Q-
> str10: M--E-S-------L-------V--------------P-G--FN--E------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 52
> best bound: 12.0
> wall time: 59.82s
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
> best bound: 50.0
> wall time: 77.17s
> ```
