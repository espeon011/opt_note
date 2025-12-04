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
Model = scsp.model.linear2_scip.Model
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
> --- Solution (of length 76) ---
>  Sol: tkgnkuhmpxnhtqgxzvxiojiqfolnbxxcvsuqpvissbnycosovozpplgevazgbrddbxpcsvrvnngf
> str1: tkgnkuhmpxnhtqgxzvxi-------------s------------------------------------------
> str2: -------------------iojiqfolnbxxcvsuqpvissb-----------------------x---------f
> str3: -----u--------------------l----c------i---nycosovozppl------------p---------
> str4: -------------------i----------------------------------gevazgbrddb--csvrvnngf
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 76
> best bound: 50.38414212850001
> wall time: 60.216345s
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
>  Sol: tkgnkuhmpxnhtqgxzvxiojiqfolnbxxcvsuqpvissbxnycosovozpplgevazgbrddbcsvrvnngevdcvdpfzsmsbroqvbbczfjtvxerzbrvigplwxqrzxucpmqvgtdfuivcdsbsfhekrdrlctodtmprpxwd
> str1: tkgnkuhmpxnhtqgxzvxi-------------s------------------------------------------------------------------------------------------------------------------------
> str2: -------------------iojiqfolnbxxcvsuqpvissbx--------------------------------------f------------------------------------------------------------------------
> str3: -----u--------------------l----c------i----nycosovozppl-------------------------p-------------------------------------------------------------------------
> str4: -------------------i-----------------------------------gevazgbrddbcsvrvnng-------f------------------------------------------------------------------------
> str5: --------p-----------------------------------y-------p-l-------r-------------------z----------------x----------------ucpmqvgtdfuivcdsb-----------o---------
> str6: --------p-------------------b----------------------------------d----------evdcvdpfzsmsbroqvbb------------------------------------------h------------------
> str7: --------------------------------------------------------e--------------n--------------b------czfjtvxerzbrvigpl--------------------------e-----------------
> str8: --------------------------------------------------------------r------------------------------------x----------wxq------------------------krdrlctodtmprpxwd
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 154
> best bound: 0.0
> wall time: 60.880417s
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
> --- Solution not found ---
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: None
> best bound: 0.0
> wall time: 63.357299s
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
> --- Solution (of length 59) ---
>   Sol: dcbccdbccdbeeeebacdeecebddddebdecbaebadcdeabcedadcdabdbeaad
> str01: dcbccdbcc--e-----------------------------------------------
> str02: --b--d---dbeeeeb--d----------------------------------------
> str03: -c--------------acdeeceb----e------------------------------
> str04: ----------------a--e----ddddebd-------d--------------------
> str05: ----------------ac-----b----e--ec-a-b--c-e-----------------
> str06: --b---b---------a------b----ebd-cba------------------------
> str07: --b---b---------a--e--------------aebad---a----------------
> str08: -----------eeee--c-----bd----b-e---e-----------------------
> str09: -c-c-d-----ee-----d---------------a---dcd------------------
> str10: --b--d----------a------bd----b-e--a--ad--------------------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 59
> best bound: 26.000000000000004
> wall time: 60.218254s
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
> --- Solution not found ---
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: None
> best bound: 0.0
> wall time: 66.153779s
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
> --- Solution (of length 49) ---
>   Sol: ATGGGATACCTTCCACGAATTGCTAGATCCAGTTCCACAACTAAACGAA
> str01: ATGGGATAC-------G--------------------------------
> str02: AT---A--CCTTCC-C---------------------------------
> str03: --------C-----ACGAATTG--A------------------------
> str04: -T---A-A------A--A-T--CT-G-T---------------------
> str05: A-GG--TA------AC-AA-----A------------------------
> str06: -T----T-CCT---A-G----G-TA------------------------
> str07: -T----T---------G--T----AGATC---T----------------
> str08: -TGGGA-A--------G--TT-C--------------------------
> str09: -T----T-CC----AC-AA---CT-------------------------
> str10: -T------C-T---A--AA---C--GA---A------------------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 49
> best bound: 20.000000000000018
> wall time: 60.418628s
> ```

In [ ]:
```python
# 問題が大きすぎるのでスキップ

# scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
```

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
> --- Solution (of length 78) ---
>   Sol: MALSYCPKGQSSLNAIPSYQHFREEHVNELHDAIRAYAHAFGGTRRPYQMRNQNSRNKDYSFVAGVTAQESLVPGFNE
> str01: MALSYCPKG----------------------------------T----------------------------------
> str02: M--------QSSLNAIP---------V---------------------------------------------------
> str03: M-----P-----L----SYQHFR----------------------------------K--------------------
> str04: M----------------------EEHVNELHD----------------------------------------------
> str05: M--S---------N-------F---------DAIRA-----------------------------------L------
> str06: M--------------------FR----N--------------------Q--N--SRN-------G-------------
> str07: M--------------------F--------------YAHAFGG----Y------------------------------
> str08: M--S---K-------------F---------------------TRRPYQ-----------------------------
> str09: M--S-----------------F----V-----A--------G--------------------V---TAQ---------
> str10: M----------------------E------------------------------S----------------LVPGFNE
> 
> example file name: 'protein_n010k010.txt'
> best objective: 78
> best bound: 33.00000000000001
> wall time: 60.426677s
> ```

In [ ]:
```python
# 問題が大きすぎるのでスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
