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
> --- Solution (of length 64) ---
>  Sol: tuikogljcinyecqosovfaozlgnkbxrdxdbcsvrvsuhmpnpxnhltqgpxzvxissbxf
> str1: t--k-g----n---------------k-------------uhmp--xnh-tqg-xzvxis----
> str2: --i-o--j-i----q----f-o-l-n-bx--x--c-v--su----------q-p--v-issbxf
> str3: -u----l-ciny-c-osov--oz--------------------p-p---l---p----------
> str4: --i--g------e-----v-a-z-g--b-rd-dbcsvrv-----n--n----g----------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 64
> best bound: 55.0
> wall time: 60.279375s
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
> --- Solution (of length 143) ---
>  Sol: tkgnkuhmpxnhtulcinyicosovozppblgenbczfqjtvazgbrdedbgcsvdcvdpzxucxfzspmevrsbroiqvbxwzfovlnbrbxxcvsuqpvigqssbpvngxqkrpdrlctodtmprpxwdfuivcdihesbo
> str1: tkgnkuhmpxnht-------------------------q-----g----------------x----z----v---------x-------------------i--s--------------------------------------
> str2: ----------------i----o-----------------j-------------------------------------iq-----fo-lnb--xxcvsuqpvi--ssb----x-------------------f-----------
> str3: -----u--------lciny-cosovozpp-l----------------------------p-----------------------------------------------------------------------------------
> str4: ----------------i--------------ge--------vazgbrd-db-csv-----------------r------v--------n--------------------ng--------------------f-----------
> str5: --------p---------y--------p--l---------------r-------------zxuc----pm--------qv----------------------g-----------------t-d--------fuivcd---sbo
> str6: --------p--------------------b-----------------de-----vdcvdp-----fzs-m---sbro-qvb--------b------------------------------------------------h----
> str7: --------------------------------enbczf-jtv-------------------x--------e-r----------z-----br----v-----ig----p----------l--------------------e---
> str8: ----------------------------------------------r--------------x--------------------w---------x-----q--------------kr-drlctodtmprpxwd------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 143
> best bound: 62.0
> wall time: 60.743952s
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
> wall time: 62.764959s
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
> --- Solution (of length 47) ---
>   Sol: bdacbbabebdecabaccdedbeecaedeacedddecbdbeadcade
> str01: -d-cb-------c---c-d--b--c-----ce---------------
> str02: bd--------d---b----e--ee--e----------bd--------
> str03: ---c--a-----c-----de--e-c-e----------b--e------
> str04: --a-----e-d-------d-d------de--------bd---d----
> str05: --acb---e--ecab-c--e---------------------------
> str06: b---b-abebd-c-ba-------------------------------
> str07: b---b-a-e----a-----e-b---a-d-a-----------------
> str08: --------e--e-------e--e-c------------bdbe-----e
> str09: ---c--------c-----de--e----d-a--d---c-d--------
> str10: bda-b-----d---b----e-----a---a--d--------------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 47
> best bound: 26.0
> wall time: 60.436837s
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
> wall time: 66.872798s
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
> --- Solution (of length 40) ---
>   Sol: ATGGGATCCTTCTACGAATTGGGATATGACTAACGTAACA
> str01: ATGGGAT------ACG------------------------
> str02: AT---A-CCTTC--C--------------C----------
> str03: -------C-----ACGAATTG--A----------------
> str04: -T---A-------A--AAT----------CT---GT----
> str05: A-GG--T------A--A------------C-AA---A---
> str06: -T----TCCT---A-G----G---TA--------------
> str07: -T----T--------G--T----A---GA-T--C-T----
> str08: -TGGGA-------A-G--TT---------C----------
> str09: -T----TCC----AC-AA-----------CT---------
> str10: -T-----C-T---A--AA-----------C----G-AA--
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 40
> best bound: 20.0
> wall time: 60.646441s
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
> --- Solution (of length 58) ---
>   Sol: MESQFYAPEHVAFGVGSLSNEKFYQLTRHRHNTDAIQNPFSYCDVRQALVPGFKNEGT
> str01: M-----A----------LS----Y------------------C-------P--K--GT
> str02: M--Q------------S-S------L-----N--AI--P-----V-------------
> str03: M------P---------LS----YQ---H----------F-----R-------K----
> str04: ME------EHV--------NE----L--H----D------------------------
> str05: M-S----------------N--F----------DAI---------R-AL---------
> str06: M---F----------------------R---N----QN--S----R--------N-G-
> str07: M---FYA--H-AFG-G-------Y----------------------------------
> str08: M-S------------------KF---TR-R--------P--Y----Q-----------
> str09: M-S-F-----VA-GV-----------T-------A-Q---------------------
> str10: MES--------------L--------------------------V-----PGF-NE--
> 
> example file name: 'protein_n010k010.txt'
> best objective: 58
> best bound: 35.0
> wall time: 60.266714s
> ```

In [ ]:
```python
# 問題が大きすぎるのでスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
