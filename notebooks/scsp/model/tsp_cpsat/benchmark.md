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
Model = scsp.model.tsp_cpsat.Model
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
>  Sol: tkignkouhjimpxnhtqfgolnbexxcinvyazgbrddbcosovozuqrppvxninslsbxgfp
> str1: tk-gnk-uh--mpxnhtq-g-----x-------z----------v--------x-i-s-------
> str2: --i---o--ji------qf-olnb-xxc--v-----------s----uq-p-v--i-s-sbx-f-
> str3: -------u-------------l-----cin-y--------cosovoz---pp------l-----p
> str4: --ig--------------------e-----v-azgbrddbc-s-v----r--v-n-n-----gf-
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 65
> best bound: 52.0
> wall time: 60.336082s
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
> --- Solution (of length 148) ---
>  Sol: igertivazkgbrxnkwuhxddojiqkrdrmpyplrfbxnhotqgxzxucsvrpmlnbqxvxcvsuqctpvinngtdfuivcdysbodcsfotmsovbozprpxlfwpbdenvdbcvdpfzsmsbroqvbzfjtvxerzbrvihgple
> str1: ----t----kg---nk-uh-----------mp------xnh-tqgxz----v-------x-----------i------------s---------------------------------------------------------------
> str2: i---------------------ojiq----------f----o-------------lnb-x-xcvsuq--pvi------------s----s-------b-----x-f------------------------------------------
> str3: -----------------u----------------l--------------c---------------------in----------y----c--o--sov-ozp-p-l--p----------------------------------------
> str4: ige---vaz-gbr-------dd---------------b-----------csvr-------v-----------nng--f----------------------------------------------------------------------
> str5: -------------------------------pyplr----------zxuc---pm---q-v-------------gtdfuivcd-sbo-------------------------------------------------------------
> str6: -------------------------------p-----b--------------------------------------d---------------------------------e-vd-cvdpfzsmsbroqvb---------b---h----
> str7: --e-----------n----------------------b-----------c-------------------------------------------------z-----f--------------------------jtvxerzbrvi-gple
> str8: ---r---------x--w--x-----qkrdr----l--------------c------------------t-----------------od----tm------prpx--w--d--------------------------------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 148
> best bound: 61.0
> wall time: 60.74474s
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
> best bound: 70.0
> wall time: 62.539455s
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
> --- Solution (of length 43) ---
>   Sol: cbaecdedddbdaeeecaebcdaebedabdcbdcbeaadbcce
> str01: -----d----------c--bc---------c-d-b-----cce
> str02: -b---d-d--b--eee--eb-d---------------------
> str03: c-a-cde------e--c-eb---e-------------------
> str04: --ae-d-ddd---e-----b-d----d----------------
> str05: --a-c-----b--ee-ca-bc--e-------------------
> str06: -b--------b-a------b---eb-d---cb----a------
> str07: -b--------b-ae---aeb--a---da---------------
> str08: ---e--e------ee-c--b-d--be---------e-------
> str09: c---cde------e-------da---d---c-d----------
> str10: -b---d------a------b-d--be-a--------a-d----
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 43
> best bound: 26.0
> wall time: 60.323193s
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
> best bound: 28.0
> wall time: 66.70791s
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
>   Sol: AGGTTAGACATAGGATACTTCCTAGGGAAGTGATAACGAACT
> str01: A--T--G-----GGATAC------G-----------------
> str02: A--T-A--C--------CTTCC--------------C-----
> str03: --------CA-------C------G--AA-T--T---GA---
> str04: ---T-A-A-A-A---T-CT-----G-----T-----------
> str05: AGGT-A-ACA-A--A---------------------------
> str06: ---TT---C--------CT----AGG----T-A---------
> str07: ---TT-G---TAG-AT-CT-----------------------
> str08: ---T--G-----GGA-A-------G-----T--T--C-----
> str09: ---TT---C--------C-----A------------C-AACT
> str10: ---T----C-TA--A-AC------G--AA-------------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 42
> best bound: 20.0
> wall time: 60.59658s
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
> --- Solution (of length 59) ---
>   Sol: MPFMLYQMSYSAEEHAKQFHVAGVLNTFDAIELHGRNAQDLGNSRNPYLVCPQKGFTNE
> str01: M----------A------------L------------------S---Y--CP-KG-T--
> str02: M-----Q-S-S-------------LN---AI---------------P--V---------
> str03: MP--L---SY-------Q-H-------F-------R-----------------K-----
> str04: M-----------EEH-----V----N-----ELH-----D-------------------
> str05: M-------S----------------N-FDAI----R-A--L------------------
> str06: M-F--------------------------------RN-Q---NSRN--------G----
> str07: M-F--Y-----A--HA--F---G-----------G------------Y-----------
> str08: M-------S-------K-F-------T--------R--------R-PY----Q------
> str09: M-------S---------F-VAGV--T--A--------Q--------------------
> str10: M-----------E------------------------------S----LV-P--GF-NE
> 
> example file name: 'protein_n010k010.txt'
> best objective: 59
> best bound: 34.0
> wall time: 60.256631s
> ```

In [ ]:
```python
# 問題が大きすぎるのでスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
