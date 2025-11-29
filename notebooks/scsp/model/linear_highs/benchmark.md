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
Model = scsp.model.linear_highs.Model
```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 75) ---
>  Sol: tkgnkuihmpxnhtqgxozjvxisqfolcinbycxxcovsuoqpvozipspsblxpevazgbrddbcsvrvnngf
> str1: tkgnku-hmpxnhtqgx-z-vxis---------------------------------------------------
> str2: ------i----------o-j--i-qfol--nb--xxc-vsu-qpv--i-s-sb-x-------------------f
> str3: -----u---------------------lcin-yc---o-s-o--voz-p-p--l-p-------------------
> str4: ------i--------g----------------------------------------evazgbrddbcsvrvnngf
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 75
> best bound: 25.0
> wall time: 60.571671s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
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
>  Sol: ulcinygevacosovozpplrxwtknbczfjxqkrdrlctodtmprpxwgnkuhmpxnhvxerzbrvigpledcvdpfzsmsbroqvbbhtcsvrvnngyfqgxzplrzxucpmqvgtdfuxisolnbxxcvsuqpvissbxfcdsbo
> str1: -----------------------tk------------------------gnkuhmpxnh-------------------------------t----------qgxz----------v-----xis------------------------
> str2: ---i-------o------------------j------------------------------------i-----------------q--------------f-----------------------olnbxxcvsuqpvissbxf-----
> str3: ulciny----cosovozppl------------------------p-------------------------------------------------------------------------------------------------------
> str4: ---i--geva------z--------------------------------g--------------br------d--d------b--------csvrvnng-f-----------------------------------------------
> str5: -----------------p---------------------------------------------------------------------------------y-----plrzxucpmqvgtdfu-i--------v-----------cdsbo
> str6: -----------------p--------b--------d-------------------------e----v-----dcvdpfzsmsbroqvbbh----------------------------------------------------------
> str7: -------e-----------------nbczfj--------t-------------------vxerzbrvigple----------------------------------------------------------------------------
> str8: --------------------rxw--------xqkrdrlctodtmprpxw-----------------------d---------------------------------------------------------------------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 148
> best bound: 25.0
> wall time: 73.195941s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
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
> --- Solution not found ---
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: None
> best bound: 25.0
> wall time: 68.290904s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q05n010k010-010.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
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
> --- Solution (of length 49) ---
>   Sol: bdcbdacbeecaeddcdadebcadabdbccdeedbadcbdeadcbcead
> str01: -dcb--c---c--d------bc------c--e-----------------
> str02: bd--d--bee--e------eb--d-------------------------
> str03: --c--ac------d-----e-----------e-----c--e---b-e--
> str04: -----a--e----dd-d-deb--d--d----------------------
> str05: -----acbeeca--------bc---------e-----------------
> str06: b--b-a-be-----------b--d----c-----ba-------------
> str07: b--b-a--e--ae-------b-ada------------------------
> str08: --------ee--e------e-c---bdb---ee----------------
> str09: --c---c------d-----e-----------e-d-adc-d---------
> str10: bd---a-b-----d------b----------e---a-----ad------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 49
> best bound: 11.0
> wall time: 60.780899s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
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
> --- Solution not found ---
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: None
> best bound: 10.0
> wall time: 76.894007s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="nucleotide_n010k010.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
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
> --- Solution (of length 30) ---
>   Sol: ATGGGATACGCTTCCCACGGATATCTGATA
> str01: ATGGGATACG--------------------
> str02: AT---A--C-CTTCCC--------------
> str03: --------C-------ACG-A-AT-TGA--
> str04: -T---A-A--------A---AT--CTG-T-
> str05: A-GG--TA--------AC--A-A----A--
> str06: -T----T-C-CT----A-GG-TA-------
> str07: -T----T--G-T----A-G-AT--CT----
> str08: -TGGGA-A-G-TTC----------------
> str09: -T----T-C-C-----AC--A-A-CT----
> str10: -T------C--T----A---A-A-C-GA-A
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 30
> best bound: 11.0
> wall time: 60.649339s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
```

In [ ]:
```python
scsp.util.bench(Model, example_filename="protein_n010k010.txt")
```

> ```
> Running HiGHS 1.12.0 (git hash: 755a8e0): Copyright (c) 2025 HiGHS under MIT licence terms
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
> --- Solution (of length 63) ---
>   Sol: MALSYCNFQSSDLNAIEEHVNPKGTELHDSYFRAGVTNLQHFRALKNSVPARGFNRNGGPYQE
> str01: MALSYC---------------PKGT--------------------------------------
> str02: M-------QSS-LNAI-----P-------------V---------------------------
> str03: M--------------------P----L--SY--------QHFR--K-----------------
> str04: M---------------EEHVN----ELHD----------------------------------
> str05: M--S--NF---D--AI----------------RA----L------------------------
> str06: M------F------------------------R----N-Q------NS---R--N--G-----
> str07: M------F----------------------Y--A------H--A---------F---GG-Y--
> str08: M--S------------------K--------F----T-----R--------R-------PYQ-
> str09: M--S---F-----------V-------------AGVT------A-----------------Q-
> str10: M---------------E------------S--------L---------VP--GFN-------E
> 
> example file name: 'protein_n010k010.txt'
> best objective: 63
> best bound: 11.0
> wall time: 60.985743s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
