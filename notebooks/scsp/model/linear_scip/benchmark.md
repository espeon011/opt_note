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
Model = scsp.model.linear_scip.Model
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
> --- Solution (of length 72) ---
>  Sol: itgevazojgbrdkignkqfuhomlcpnibxnxyhctvqgdxobsucqovozpsviprvssxbinsnglxfp
> str1: -t-----------k-gnk--uh-m--p---xn--h-t-qg-x---------z--v------x-i-s------
> str2: i------oj-----i---qf--o-l--n-bx-x--c-v------su-q----p-vi---ss-b------xf-
> str3: --------------------u---lc--i--n-y-c------o-s---ovozp---p-----------l--p
> str4: i-gevaz--gbrd---------------------------d--b--c------sv--rv-----n-ng--f-
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 72
> best bound: 26.0
> wall time: 60.192853s
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
> --- Solution (of length 175) ---
>  Sol: rxwxqkrdrlctodtmprpxwdenbczfjtvxerzbrvigplepbdevdcvdpfzsmsbroqvbbhpyplrzxucpmqvgtdfuivcdsboigevazgbrddbcsvrvnngfulcinycosovozpplpiojiqfolnbxxcvsuqpvissbxftkgnkuhmpxnhtqgxzvxis
> str1: -----------t-----------------------------------------------------------------------------------------------------------------------------------------------kgnkuhmpxnhtqgxzvxis
> str2: --------------------------------------i---------------------o----------------------------------------------------------------------jiqfolnbxxcvsuqpvissbxf---------------------
> str3: -------------------------------------------------------------------------u---------------------------------------lcinycosovozpplp----------------------------------------------
> str4: --------------------------------------ig--e----v-----------------------------------------------azgbrddbcsvrvnngf---------------------------------------------------------------
> str5: ----------------p--------------------------------------------------yplrzxucpmqvgtdfuivcdsbo------------------------------------------------------------------------------------
> str6: ----------------p-------b--------------------devdcvdpfzsmsbroqvbbh-------------------------------------------------------------------------------------------------------------
> str7: ----------------------enbczfjtvxerzbrvigple------------------------------------------------------------------------------------------------------------------------------------
> str8: rxwxqkrdrlctodtmprpxwd---------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 175
> best bound: 26.0
> wall time: 61.036027s
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
> best bound: 25.0
> wall time: 62.559053s
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
> --- Solution (of length 52) ---
>   Sol: bbaeacacdeedaebdeceabdcedbedcebdabecebaacebcdcadbede
> str01: --------d--------c--b-c-----c--d-b-c----ce----------
> str02: b-------d--d--b-e-e----e--e---bd--------------------
> str03: -----cacdee------ce-b--e----------------------------
> str04: --ae----d--d---d-----d-e-b-d---d--------------------
> str05: --a--c--------b-e-e---c---------ab-ce---------------
> str06: bba-----------b-e---bdc--b------a-------------------
> str07: bbaea----e----b----a-d----------a-------------------
> str08: ---e-----ee--e---c--bd---be--e----------------------
> str09: -----c-cdeeda--d-c---d------------------------------
> str10: b-------d---a-bd----b--e--------a-----a-----d-------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 52
> best bound: 12.0
> wall time: 60.225939s
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
> best bound: -1e+20
> wall time: 65.374171s
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
> --- Solution (of length 42) ---
>   Sol: TATCTGCACGATGCTACGACGTACTACGTAGCTCATGCACTA
> str01: -AT--G---G--G--A-----TAC---G--------------
> str02: -AT----AC----CT------T-C--C----C----------
> str03: ---C---ACGA----A-----T--T--G-A------------
> str04: TA-----A--A----A-----T-CT--GT-------------
> str05: -A---G---G-T---A--AC--A--A---A------------
> str06: T-TC--C----T---A-G--GTA-------------------
> str07: T-T--G-----T---A-GA--T-CT-----------------
> str08: T----G---G--G--A--A-GT--T-C---------------
> str09: T-TC--CAC-A----AC----T--------------------
> str10: T--CT--A--A----ACGA---A-------------------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 42
> best bound: 11.0
> wall time: 60.213393s
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
> --- Solution (of length 70) ---
>   Sol: MFALSESYCPSQLRNFESKFDASNHFSVPYLQTNGAIEAQRFNHGIRVSGTPRFNAELRGHNYDQAKQVG
> str01: M-ALS--YCP--------K---------------G---------------T-------------------
> str02: M----------Q-----S----S-------L--N-AI--------------P----------------V-
> str03: M--------P--L----S-----------Y-Q-----------H---------F----R-------K---
> str04: M----E----------E-------H--V-----N---E-------------------L--H--D------
> str05: M---S---------NF----DA--------------I---R--------------A-L------------
> str06: MF-----------RN----------------Q-N--------------S---R-N----G----------
> str07: MF-----Y-------------A--H----------A-----F--G----G------------Y-------
> str08: M---S-------------KF------------T-------R-----R----P----------Y-Q-----
> str09: M---S----------F-----------V-------A--------G--V--T----A--------Q-----
> str10: M----ES-----L--------------VP-----G------FN-------------E-------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 70
> best bound: 12.0
> wall time: 60.292798s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
