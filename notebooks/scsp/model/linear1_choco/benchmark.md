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
Model = scsp.model.linear1_choco.Model
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
> --- Solution (of length 67) ---
>  Sol: iojiqftokglnkguhempvazgbrlddbcsvrxxvinycosohvozppltsuqngxzpvxissbxf
> str1: ------t-kg-nk-uh-mp--------------x---n-----h------t--q-gxz-vxis----
> str2: iojiqf-o--ln-----------b---------xx----c----v------suq----pv-issbxf
> str3: --------------u----------l---c------inycoso-vozppl--------p--------
> str4: i--------g------e--vazgbr-ddbcsvr--v-n----------------ng----------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 67
> best bound: 0.0
> wall time: 60.02s
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
> --- Solution (of length 116) ---
>  Sol: iojiqfogevapyplrzxucplmgqnbxxvrdgtdfkuczfjtvxerzbrvignycosvrwvnkuhpmpxnqkrdrlcohtqgxevodpzvxfzppltismsbpropqvxwdfbbh
> str1: ---------------------------------t--k---------------gn---------kuh-mpxn--------htqgx-----zvx------is----------------
> str2: iojiqfo-------l----------nbxx---------c----v-------------s------u------q----------------p-v-------is-sb------x--f---
> str3: ------------------u--l----------------c------------i-nycos--------------------o------vo--z----ppl------p------------
> str4: i------geva-----z------g--b---rd--d-------------b------c-svr-vn-------n-----------g---------f-----------------------
> str5: -----------pyplrzxucp-m-q----v--gtdf-u-------------i------v------------------c---------d-----------s--b--o----------
> str6: -----------p--------------b----d-------------e----v-----------------------d--c-------v-dp---fz-----smsb-ro-qv----bbh
> str7: --------e----------------nb-----------czfjtvxerzbrvig-------------p---------l-------e-------------------------------
> str8: ---------------r-x------------------------------------------w--------x-qkrdrlc--t-----od---------t--m--pr-p--xwd----
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 116
> best bound: 0.0
> wall time: 60.14s
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
> --- Solution (of length 170) ---
>   Sol: iojiqfolnkxpyplrzxucpmhlgtwshebkxibxqjnfpadiuszqeabczfjtvbaszgnkuhmpxnhtqidcfruezvdgrxplnaqvqcewbfgiyhvcztorddbcsvrvnxmkoiezuwantfmgqjwhowskkszpbkvruozpplqpvblbxwefhdydmg
> str01: -------------------------t-----k-----------------------------gnkuhmpxnhtq----------g-x------------------z--------v---x---i----------------s-------------------------------
> str02: iojiqfoln---------------------b-x--x---------------c----v--s----u-------q-------------p----v-------i------------s-------------------------s-----b---------------x--f------
> str03: ------------------u----l---------------------------c---------------------i--------------n-----------y--c--o-----s-------o-------------------------v--ozppl-p--------------
> str04: i-----------------------g----e--------------------------v-a-zg----------------------------------b----------rddbcsvrvn----------n---g-------------------------------f------
> str05: -----------pyplrzxucpm--------------q-------------------v----g---------t--d-f-u--------------------i--vc----d---s-------------------------------b----o--------------------
> str06: -----------p------------------b-----------d-----e-------v-----------------dc-----vd---p----------f------z-------s-----m-------------------s-----b--r-o----q-vb-b----h-----
> str07: -----------------------------e--------n-----------bczfjtv-----------x----------e----r-------------------z-----b---rv-----i---------g-----------p---------l--------e-------
> str08: ---------------r-x--------w-----x---q--------------------------k-------------r----d-r--l-----c-----------to-d-------------------t-m------------p---r---p--------xw---d----
> str09: ---------k---------------------k----q----a-----------f-------------------i---------g------q------------------------------------------jw-o--kks---k-r---------bl----------g
> str10: -------l--x------x--p--------------------a--------b----------------------i-------v--------------b-----v-z--------------ko--z------------------z---v------------------d----
> str11: ---------k-----r-----------------i-----f-----s---a------v-----n------------c------d-------q----w-----h--z------c----------------------------------------------------------
> str12: ----q------------------------------------a--------------------------x---------u---dg------qvqcewbfgi---------------------------------j--ow-----------------------w----y---
> str13: ---------------r-----------s----x---qjnfpadius---------------------------i----------------q-----b-------------------------ez-----------h---k---------o--------------h---mg
> str14: i-------------------------wsh---------------------------v--------h---------c------------------------------o-----------m--i--u---------------------v------------------d-dm-
> str15: ----------------------h--t------x--xqj--------zq--bc---t-ba----k-----n----------------------------------------------------------------------------------------------------
> str16: ----------x-------u--------s-----------f-----------c-f------z------p-----------e--------------e--------c---------v-----------wantfmgq---------z-----u---------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 170
> best bound: 0.0
> wall time: 60.73s
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
> --- Solution (of length 27) ---
>   Sol: bbaeddcbeacdeecbdbeacbdcade
> str01: ----d-cb--c---c-db--c--c--e
> str02: b---dd-be---ee----e--bd----
> str03: ------c--acdeec---e--b----e
> str04: --aedd-----d----d-e--bd--d-
> str05: --a---cbe---e-c----a-b-c--e
> str06: bba----be------bd---cb--a--
> str07: bbae-----a--e--b---a--d-a--
> str08: ---e----e---eecbdbe-------e
> str09: ------c---cdee--d--a--dc-d-
> str10: b---d----a-----bdbea----ad-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 0.0
> wall time: 60.02s
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
> --- Solution (of length 37) ---
>   Sol: daecdbacdcebedabecabecdebcadeeabcbade
> str01: d--c-b-c-c---d-b-c---c-e-------------
> str02: -----b--d----d-be---e--e----e--b---d-
> str03: ---c--acd-e-e----c--e---b---e--------
> str04: -ae-d---d----d--------deb--d-------d-
> str05: -a-c-b----e-e----cab-c-e-------------
> str06: -----b-----b--abe--b--d--c-----b--a--
> str07: -----b-----b--a-e-a-e---b-ad--a------
> str08: --e-------e-e---ec-b--d-b---ee-------
> str09: ---c---cd-e-eda-------d--c-d---------
> str10: -----b--d-----ab------d-b---e-a---ad-
> str11: --e-d-----e--da---a-------a-e-a---a--
> str12: -a----a---e---a---abe--e--a-----c----
> str13: --e---a-------ab-ca--c---c-d---b-----
> str14: -----b--d-e-e-a-------de--ade--------
> str15: ---c--a---e--da-------de----ee-----d-
> str16: --e--b-c------a-------d-b-a----b-b--e
> str17: d---d--c--e-e-ab------de--a----------
> str18: da---b-cd----d--e-a-ec---------------
> str19: -a----a-dce-eda---ab-----------------
> str20: -ae-------e------c---c-e----eea---a--
> str21: -----b-----b-da-eca-------ade--------
> str22: da-c------e--da-e-----d---a----b-----
> str23: -a----a---e---ab---b----b------bc---e
> str24: d-e-db-c---b-----ca-------a----b-----
> str25: d----b--d-----a---a-e---b------bcb---
> str26: d-e--b----e--d-be--b------a-----c----
> str27: ---c------e-e--b-c----d--c-----b---de
> str28: d----b----e--da---a---d---a---ab-----
> str29: ---c---c-c---d---c-be---b--d----c----
> str30: -ae-------e---a--c----d-bc-----b---d-
> str31: da-c-b----e---a--c---c---c-d---------
> str32: --ec------eb-----c---cd-b--d---b-----
> str33: d---db-----b-----c--e-d---a----b-b---
> str34: -a----a---e---ab--a-------a-e--b--a--
> str35: --ec-b-----b-----ca-------ad----c--d-
> str36: d-e--b-c-ce------c----d-bc-----------
> str37: da----ac---b--a-e---e---bc-----------
> str38: -a--d-a----be-a---a--c---c--e--------
> str39: daecdbac------a---a------------------
> str40: da-c-b-----b-d---c--e-d--c-----------
> str41: d-e-db----e-e--b---b--de-------------
> str42: ---cd-a-dc---d---c----d---a---a------
> str43: ---c------e-ed---c-b------a-ee-----d-
> str44: ---c------e---a-eca-------a---a-c-a--
> str45: d--c---c-ceb---b---b------ad---------
> str46: -----ba---e-e-a-e--b----b--de--------
> str47: d----b--d-eb--a--c---cd-b------------
> str48: --e--b-c---be---e-----d---a-e-a------
> str49: -ae-------e-e--b---b--d-bca----------
> str50: d----b--d-----ab-c--ec--b------b-----
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 37
> best bound: 0.0
> wall time: 62.47s
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
> --- Solution (of length 25) ---
>   Sol: ATAGCTACCGGTAATCGATACGTAC
> str01: AT-G-----GG-A-T--A--CG---
> str02: ATA-C--C---T--TC----C---C
> str03: ----C-AC-G--AAT---T--G-A-
> str04: -TA---A-----AATC--T--GT--
> str05: A--G-----G-TAA-C-A-A---A-
> str06: -T---T-CC--TA---G----GTA-
> str07: -T---T---G-TA---GAT-C-T--
> str08: -T-G-----GG-AA--G-T---T-C
> str09: -T---T-CC---A--C-A-AC-T--
> str10: -T--CTA-----AA-CGA-A-----
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 25
> best bound: 0.0
> wall time: 60.04s
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
> --- Solution (of length 176) ---
>   Sol: ACTAGTCGGACAAGCAGTTGTCAGACTTAAGCTAGCGTCGCAGCTTGGACCCTGACAGCGTTGATACCTGAACTCTGGGTACTACATCGATGGCTGCACACATAGGCCTGAGCCTGTAGACTCGCTAAGCCTGGACATTAGACGATCTGCGTACTCTTAGAGGTAGCTCACAGRTG
> str01: --TAGT---A---G---T----AGACT----C---CG--G-A------A----G------T-GA--C---AA--------AC--C--C--TG-----A-A-A-AG-----A------A---T-G----G-----A--T-A-A--AT------A-T---A-----------------
> str02: ----G--G-A-------T----A-A---A--C-A-C-TC-C--C--G-A-----A-A------ATA----A--T-T---T--------GA---CT-------TA------A------A--C-----AA-C--G--C----GAC-A---G--T--TC--A-AG--------------
> str03: A-TA--C---C------TT--C---CT-A-G---G--T---A------AC----A-A------A--CC--AAC-C-----A--AC-T---T---T-------T-G-----A---T-----CTC--T-----TG----T-AGA---TCTG---------------------------
> str04: --TA-----A-A-----TT---A---T-AA--T--C-T------T---A---T-AC----T--A-----G---T------A--A-A---A-------A-A--TAGG---G----TGTA-AC-CG--AA------A-A-----CG----G--T-C----------------------
> str05: --T--T---A-AA--A-----CAG-C-----CT-G--T-G--G---G-----T-------T-G---C---A-C-C------C-AC-TC-A---C---A------GG---G--CC------C-----A--C-TGG------G-CG--C-----A-----AG----------------
> str06: A-T-G----AC------TT--C---C--AA--T-G-G----A--T----CCC--A-A-C-------C-T---C-------A--A----G----CT-------T---CC--A-CC------C-C---AA---TGG---TT------TC-----A------G------C---------
> str07: A--A--C--A-AA-C------CA-AC-----C-A-------A-CTT------T-------T-GAT-C-T---CT-TG--TA-------GAT--CTG------T-----T---C-T-----CT----AA------AC----GA--A-C-----------------------------
> str08: A-T-G----A-AA--A-----C-GA---AA---A---T------T---A---T-------T--AT-C---AA----GGGTA-T-----G--G-----A-A----G---TG-G-----A-A---GCT--G-----AC----GA--A-------A-T---------------------
> str09: ACT---CGG-C------T-G-CA---T---GCT----T---AG-T-G--C----AC----T-----C---A-C---G----C-A----G-T------A----TA------A---T-TA-A-T----AA-C-T--A-ATTA------------------------------------
> str10: --T--T-G---------T----AGA-T----CT-G--T------T----C--T--C----T--A-A----A-C---G---A--AC-T---T---T--A-A-A-A----T---C-TGT-G--T-G----GC-TG----T----C-A-CT-C--------------------------
> str11: ----G-C--A---G-AG----CA---TT----T----TC-----T---A-----A-----T--AT-CC--A-C-------A--A-A---ATG-----A-A----GGC---A------A---T----AA---T-----T--G----T------ACT---A-------CTC-------
> str12: A-T-G----A---GC------CA-A-----G--A---TC-C-G-----AC---GA-AG-----A-----G--C-C------C--CA---A-GG----A------GG----AG-----A-A---G----G-----A-----G--G----G---AC-C----------C-C-C-----
> str13: --T---C----------T---CA--C--A-G-T----TC--A------A----GA-A-C-------CC--AA--------A-------G-T------AC-C-----CC----CC---A---T----A-GCC----C-T----C--T-T----A-----A-AG----C-CAC-----
> str14: A---G--G---------TT-T-A---T-A--C---C-T------T----CC-T-A--G-GT--A-AC---AA--------AC--CA---A---C--CA-AC-T-----T-----T-----C--G--A----T---C-T----C--T-TG--TA-----------------------
> str15: A---G--G---------TT-T-A---T-A--C---C-T------T----CCC--A--G-GT--A-AC---AA--------AC--CA---A---C--CA-AC-T-----T-----T-----C--G--A----T---C-T----C--T-TG--TA-----------------------
> str16: --TA-----A-AA-CA------A--CT----C-A-------A--T---AC----A-A-C----ATA----A-----G---A--A-A---AT--C---A-AC---G-C---A------A-A------AA-C----AC-T----C-A-C-----A-----A-A---------------
> str17: -C----CG--C---C------CA---TT----T-G-G--GC-G---G--C--T--C----T-----C--GA-----G----C------GAT------A------G-C-T---C--GT---C--G--AA---T---C------C---CT-CG-AC-CT-------------------
> str18: A-TA--C---C------TT--C---C-----C-AG-GT---A------AC----A-A------A--CC--AAC-C-----A--AC-T---T---T-C-------G-----A---T-----CTC--T-----TG----T-AGA---TCTG---------------------------
> str19: --T---C----------T---CA--C--A-G-T----TC--A------A----GA-A-C-------C-T---C-------A--A----G-T--CT-C-C-C-----CC--A---T--AG----GC----C-T---C-TT------TC-----A------G---T--C--A--G---
> str20: ----G----A-------T---C----T----CT--C-TC--A-C-----C---GA-A-C-------C-TG------G----C--C--C-----C-G--------GGC---A------A-A-T-GC----CCT--A-AT----C---C-----A------GAGGT-G----------
> str21: A---G----A---GCA------A---T----C-AG--T-GCA--T----C----A--G-----A-A----A--T------A-TAC--C--T------A----T-----T-A---T--A--C-----A--C-T-----TT-G-C--T------A-----AGA---A--T--------
> str22: A--A-T-----------T----A-A---AA-C-A---TC-----T----C----A-A---T--A--C---AAC-------A-TA-A--GA-------A-A-A-A--C---A------A--C--GC-AA------A-A--A--C-A-CT-C--A-T---------------------
> str23: A--A-----AC--G-A------A--CTT----TA-------A------A-----A-----T-----C-TG---T--G--T--------G--G-CTG------T---C---A-C-T-----C--G----GC-TG--CAT--G-C--T-T----A------G---T-GC---------
> str24: A-TA-----AC------T----A-A-TTA--CT-G--TCG----TTG-AC----A--G-G---A--C---A-C---G---A-------G-T------A-AC-T---C--G----T-----CT----A----T---C-TT---C--T--G---------------------------
> str25: A-T-G----A---G---T-GTCA--C----G--A-------A--TT---C----AC-G--T--A--C---AA-T--G---A--AC-T-G--G-----A----T-G---T-----T-----C-----A--C--G----T--G--GA-------A-T---A-A---------------
> str26: AC----CG---------T-G---G------GC--G------AGC--GG----TGAC--CG--G-T----G---TCT---T-C--C-T--A-G--TG--------GG--T---CC------C-----A--C--G----TT-GA--A----------------------------R--
> str27: A--A-----A---G--GTT-T-A---T-A--C---C-T------T----CCC--A--G-GT--A-AC---AA--------AC--CA---A---C--CA-AC-T-----T-----T-----C--G--A----T---C-T----C--T-TG---------------------------
> str28: A---GT---A---G---TT--C-G-C-----CT-G--T-G----T-G-A----G-C----T-GA--C---AA--------ACT---T--A-G--T--A------G---TG----T-T----T-G-T--G-----A-----G--GAT-T----A-----------------------
> str29: --T--T-----------T----A---T-A--C---C-T------T----CC-T-A--G-GT--A-AC---AA--------AC--CA---A---C--CA-AC-T-----T-----T-----C--G--A----T---C-T----C--T-TG--TA------GA--T------------
> str30: A-T-G-CGG--------T---C-G--T----CT--C-TC-C--C-----C---G---GC-TT--T---T----T-T---T-C--C--C-----C-GC-------G-CC-G--C--GT----T-G----GC--G--C------CGA-------------------------------
> str31: ----GT-G-ACAA--A------A-AC--A---TA-------A--T-GGAC--T--C--C----A-AC---A-C-C-----A-T-----G-T--C---A-A----G-C-T-----T-T---C-----A-G---G----T-AGAC---------------------------------
> str32: ----GT-G---------T----A-A-----G--A-------A------AC----A--G--T--A-A---G--C-C------C------G--G-----A-A----G---TG-G--TGT----T---T-----TG--C----GA---T-T---T-C-----GAGG---C-C---G--G
> str33: ----G----A---G-A------A---T---G--AG--TC-----T----C----A-----TT-A--CC-G--C-C------C------G--G--T--AC---T-----T-AGC----A-A---GCTAA---T--A-----G----TC-----AC-----G-G----C---------
> str34: A-T-GT-GG--------T---C-GA-T---GC---C-----A--T-GGA----G---GC-------CC--A-C-C-----A-------G-T---T-CA----T-----T-A------AG----GCT---CCTGG-CATT-------------------------------------
> str35: AC--G----A---GC-GTT-T-----T-AAG---G-G-C-C--C--G--C---GAC----T-G---C--GA-C---GG---C--CA-C-ATGGC--C-C---T-G---T-A---TGT-----------------------------------------------------------
> str36: ----G--G---------TT-T-A---T-A--C---C-T------T----CCC--A--G-GT--A-AC---AA--------AC--CA---A---C--CA-AC-T-----T-----T-----C--G--A----T---C-T----C--T-TG--TA------G----------------
> str37: --T-G--GGA-A-G---TT--C---C--AA---A-------AG-----A---T--CA-C----A-A----AAC-------ACTAC--C-A-G--T-CA-AC-----C-TGA------AG--T----A--C----AC----------------------------------------
> str38: ----G----A-A-GC-GTT---A-AC----G-T-G--T------T-G-A----G---G-----A-A----AA----G---AC-A----G----CT-------TAGG----AG-----A-AC-----AAG-----A-----G-C--T--G-G--------G----------------
> str39: AC----C--A---GC-G----CA--CTT---C--G-G-C--AGC--GG-C----A--GC----A--CCT---C---GG---C-A----G----C---AC-C-T---C---AGC----AG-C-----AA-C----------------------------------------------
> str40: A-T-G--GGACAA-C--TT---A---TT---C---C-T---A--T----C----A-----T-G-T----G--C-C-----A--A----GA-GG-T-------T-----T-----T--A--C-C-C---G---G----T--GAC---C-----A-----------------------
> str41: --T--T-G---------T----AGA-T----CT-G--T------T----C--T--C----T--A-A----A-C---G---A--AC-T---T---T--A-A-A-A----T---C-TGT-G--T-G----G--T-----T--G----TC-----ACTC--------------------
> str42: A--A--C---CAA-C------CA-ACTT----T--CG----A--T----C--T--C----TTG-TA---GA--TCTG--T--T-C-TC--T------A-A-A----C--GA------A--CT---T-----T--A-----------------------------------------
> str43: ----G--GG--------TT--C----T---GC---C-----AG---G--C----A-----T--A-----G---TCT---T--T---T---T---T-------T---C-TG-GC--G--G-C-C-CT-----TG----T--G----T------A-----A-A-----C-C-----TG
> str44: ----G--G--C------T-G-CA---T---GCT----T---AG-T-G--C----AC----T-----C---A-C---G----C-A----G-T------A----TA------A---T-TA-A-T----AA-C-T--A-ATTA--C--T--G--T------------------------
> str45: --T-G-C--A-------T-G-C----TTA-G-T-GC-----A-CT----C----AC-GC----A-----G---T------A-TA-AT---T------A-A--TA------A-C-T--A-A-T---TA--C-TG----T----CG-T------------------------------
> str46: --T--TC---CA--CA------A--CTT----T--C--C--A-C-----C----A-AGC-T-----C-TG--C-------A--A----GAT--C--C-CA----G-----AG--T-----C-----A-G---GG------G-C---CTG--T------------------------
> str47: --T---C----------T----A-A---A--C--G------A------AC--T-------TT-A-A----AA-TCTG--T--------G-TGGCTG------T---C---A-C-T-----C--G----GC-TG--CAT--G-C--T-T----A------G----------------
> str48: AC----CGGA-------T-G---G-C-----C--GCG----A--TT------T-------TT----C--G------G---A-------G-T--C--C-----T-----TG-G---G--G----G--A--CC---AC-T----C-A---G---A-----A----TAG---A------
> str49: -CT--T-G---------T----AGA-T----CT-G--T------T----C--T--C----T--A-A----A-C---G---A--AC-T---T---T--A-A-A-A----T---C-TGT-G--T-G----GC-TG----T----C-A-CT----------------------------
> str50: A-T-G----A---GCA-----C----T-AAGC--G------A------A----GA-A-C-------C---AA--------A--A-A--G----C---A------G-----A-C----A-A-T----A--C----A-A-----C---C--CG--CT---A----T---T-AC-----
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 176
> best bound: 0.0
> wall time: 119.97s
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
> --- Solution (of length 46) ---
>   Sol: MQSKFESTRRLVPALSNGYFQECNSAHDAFGIPRVKNGTEYALQHD
> str01: M------------ALS--Y---C---------P--K-GT-------
> str02: MQS---S---L-----N--------A-----IP-V-----------
> str03: M-----------P-LS--Y-Q-----H--F---R-K----------
> str04: M----E---------------E----H-------V-N--E--L-HD
> str05: M-S-------------N--F-------DA--I-R-------AL---
> str06: M---F---R-------N---Q--NS--------R--NG--------
> str07: M---F-------------Y------AH-AFG------G--Y-----
> str08: M-SKF--TRR--P-----Y-Q-------------------------
> str09: M-S-F------V-A---G----------------V---T--A-Q--
> str10: M----ES---LVP----G-F---N---------------E------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 46
> best bound: 0.0
> wall time: 60.03s
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
> --- Solution (of length 678) ---
>   Sol: MANYSKPFLLDIVFNKDIKCINDSCSHSLPSTYTDGTAACTNGSPDVVGTGTMWVNTILPGDFFWTPSGRYIVSPQLVLQVGKGQEVERALYLTPYDYISLVPGFNEKTHLNIDIETYSSNDIKNRAHRTHQNWDATKPRERRKQTQHRLTHPYSNRRLAVFASTALFDALCDDILHRGFEVSGPTEVSTCFGSLHPFQSLKPVMANALGVLEGKMFCSQGKAREFPSEEARANSPTLRELWVSQGMNPYDENLHAFPGISGINYKKLQSKLQHDFGRVLKALTVWWIWTSLGFWMFMICSVVGNLWVTVYYDAYKLGHIHMYPETAAARGRGGDERRRGWAFLLLVTSLPLYNPNMDSCCLISRITPELAGKLTHLSSPLVKHILRNYLRLYIILARQVRDILCDGFFLFVLWKALSLPVPTRCQIDMAKKLSAEHTLYFASVSAGGAIRGITNSFTRGLVDPKKTGDAISDDENENDSQLAKRFSKGLLSGQGPMKLVYLVRTIIDCVSGDSAFRAEVKARVWKLHIGADAPAFQDTANQQAYEEKLKPQLSMGIIVPIPGDSCLAVDTETFNHFDATDDGKVFRSSIGQAEPLPSEARQHLKDGTFVINYWVVYSLLFHIMGSGTCISRKHRNECDIVKNKYMWQHLKADNIDSVGLFDHPVSTNTKAIGLIVSR
> str01: M--------------------------------------------------------------------R---------------------------------------HLNIDIETYSSNDIKN-----------------------------------------------------G--V-------------------------------------------------------------------Y---------------K--------------------------------------------Y--A--------------------D------A--------------------------E--------------------------------D-----F---------------------------E-------------I----------L--------------------L---F----------------------------A-----------------------------Y--------S--I------D------------------G-------G--E---------------V--------------------------EC-----------L--D------L------T----------R
> str02: M------------------------------------------------------------------------------------E--R------------------------------------RAHRTHQNWDATKPRERRKQTQHRLTHP---------------D---D---------S----------------------------------------------------------------------------I----Y----------------------------------------------------------P-----R--------------------------------I-----E---K-----------------------A--------------------------------------E----------G---R-------------K---------E---D------------------------------------------------H-G----------------------------------------------------------------------------------------------------------------------------------------------------
> str03: M------------------------------------------------------------------------------------E--------P--------G----------------------A----------------------------------F-STALFDALCDDILHR---------------------------------------------R-------------L-E---SQ--------L-----------------------R---------------F---------G-------------G----------------------------V---------------------------------------------------Q---I----------------P-P-------------E-------VS-----------------DP--------------------R--------------VY-------------A--------------G--------------Y----------------------A---------------------------L-------L--------------------------------------------------------------------------
> str04: M----------------------------------G----------------------------------------------K---------------------F------------Y-----------------------------------YSNRRLAVFA-----------------------------------Q------A-------------Q-------S---R----------------------H------------L--------G---------------G-------S---------Y-------------E-------------------------------------------------------------------------Q--------------W--L------------A------------------------------------------------------------------------------CVSGDSAFRAEVKARV------------Q----------K---------------D------------------------------------------------------------------------------------------------------------------
> str05: -------F-----F-------------------------------------------------------R---------------E-------------------N----L---------------A----------------------------------F------------------------------------Q--------------------QGKAREFPSEEARANSPT------S---------------------------------R----------------------------------------------E------------------L---------------------------------------------------------------------W------V--R--------------------------RG-------G---------------N-------------------P--L-----------S-------E--A-------GA--------------E----------------------------------------R-------------R-----GT----------------------------------------------------------------------
> str06: M---------D------------------PS---------------------------L------T---------Q-V-------------------------------------------------------W-A------------------------V-------------------E--G----S--------------V----L---------S---A-------A-----------V-------D--------------------------------T-----------------------------A----------ET---------------------------N---D--------T-E----------P---------------------D---------------------------------E----------G-------------L----------S----------A-----------------------------------E---------------------N----E---------G---------------ET-------------R--I--------------------I--------------------R-------I--------------------------T-----G---S-
> str07: MA-----F--D--F---------S----------------------V--TG----NT-------------------------K-------L-----D-----------T---------S-----------------------------------------------------------GF-----T------------Q----------GV-------S--------S------------------M------------------------------------TV----------------------------A------------A---G----------------T-L------------I-------A------------------------------D-L-------V--K-------T------A---S--------S-------------------------------------QL----------------------T-----------------------------------N-------L------------------A-----------------------Q-----S--------------------------------------------------------------------------------
> str08: MA----------V----I----------LPSTYTDGTAACTNGSPDVVGTGTMWVNTILPGDFFWTPSG----------------E-------------S-V-----------------------R----------------------------------V-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str09: M-N----------------------------T---G---------------------I-------------I------------------------D---L---F--------D------N------H--------------------------------V-------D-------------S----------------------------------------------------------------------------I---------------------------------------------------------------P-T------------------------------------I------L---------P---H--------------Q----L-----------A------T---------L-----------------------------D-------------------------------------YLVRTIID----------E---------------------N---------------------------------------------RS---------------------V--------LLFHIMGSG---------------------------------------------------
> str10: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N-L--------------R------------T-R--------------------------------------------T------------------------------------------------------------------------------------------------------------------Q----L---------------P-P-------A---------Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S----------------------------------------------------
> str11: M---------D------------S----------------------------------------------------------K--E-------T----I-L-----------I--E------I---------------------------------------------------I---------P----------------K---------------------------------------------------------I-----K---S----------------------------------------Y-----L--------------------------L-------------D--------T--------------------N-----I-----------------------S-P----------K--S-----Y--------------N-------D----------------------F-------------------I----S-----R-----------------------N------K--------------------------N--------------I------------------FVIN------L-------------------------Y--------N---V-------ST----I------
> str12: M-------LL-------------S-----------G----------------------------------------------K------------------------K---------------K--------------------------------------------------------------------------------M---L--L--------------------------------------D-N-----------Y-----------------------------------------------------------ETAAARGRGGDERRRGWAF--------------D------R--P--A-------------I--------------V----------------------T-------K-------------------R-----------D-K------SD-----------R-----------M-----------------A------------H------------------------------------------------------------------------------------------------------------------------------------------------------
> str13: M-N--------------------------------G-------------------------------------------------E-E--------D----------------D------N-------------------E---Q--------------A--A--A--------------E-----------------Q--------------------Q----------------T----------------------------KK--------------A---------------------------------K-------------R-----E------------------------------------K------P--K---------------Q----------------A-------R------K------------V---------T-S------------------E-------A-----------------------------------------W--------------------E-----------------------------HFDATDDG---------AE----------------------------------C---KH--------------------------------------------
> str14: M------------------------------------------------------------------------------------E-------------SLVPGFNEKTH--------------------------------------------------V-------------------------------------Q-L-----------------S------------------L----------P-----------------------------VL----------------------------------------------------------------------------------------------------------------------QVRD---------VL-------V--R----------------------G---------F--G--D--------S---------------------------V------------------E--------------------------E------------V-------L--------------------S-----E-----ARQHLKDGT----------------------------------------------------------------------
> str15: M--------------------------------------------------------------------RYIVSPQLVLQVGKGQEVERALYLTPYDYI--------------D-E-------K------------------------------S-----------------------------P--------------------------------------------------------------------------I----Y---------------------------------------------Y-------------------------------FL--------------------R------------S-----H-L-N-----I----Q-R------------------P------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: M-----P--------------------------------------------------------------R--V-P--V-------------Y----D--S--P----------------------------Q----------------------------V--S--------------------P---------------------N-----------------------------T-----V-----P-------------------Q------------A-----------------------------------------------R-------------L--------------------------A---T----P-------------------------------------S----------------------FA-----------T---------P--T------------------F-----------------R-------G--A----------------DAPAFQDTANQQA------------------------------------------R----Q--------------------------------------------------------------------------------------
> str17: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N-L--------------R------------T-R--------------------------------------------T------------------------------------------------------------------------------------------------------------------Q----L---------------P------------L-A----Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S----------------------------------------------------
> str18: M------F----VF------------------------------------------------F---------V---L-L---------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N-L---------------------------T----------------------------------------------T---------------------------------------------R-----------------T--------------------------------------------------Q----L---------------P-P-------A---------Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S----------------------------------------------------
> str19: M------------------------------------------------------------------------------------E---A--------I-------------I-----S------------------------------------------FA---------------G--------------------------------------------------------------------------------I-GINYKKLQSKLQHDFGRVLKALTV----T-----------------------A---------------R-----------A-L------P--------------------G--------------------------Q--------------------P----------K-----H------------I-------------------AI-------------R--------Q----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: MA--S------------------S-----------G--------P----------------------------------------E--RA----------------E--H---------------------Q------------------------------------------I------------------------------------------------------------------------------------I-------L-------------------------------------------------------PE-----------------------S--------------------------HLSSPLVKH------------------------------K-L-L--------------------Y------------------------------------------------------------Y-----------------------WKL-----------T----------------G----------L---------------------------PLP--------D------------------------------ECD---------------------FDH----------LI---
> str21: M------------------------------------------------------------------------------------E-------------SLVPGFNEKTH--------------------------------------------------V-------------------------------------Q-L-----------------S------------------L----------P-----------------------------VL----------------------------------------------------------------------------------------------------------------------QVRD---------VL-------V--R----------------------G---------F--G--D--------S---------------------------V------------------E--------------------------E------------V-------L--------------------S-----E---------------V---------------------R---------------QHLK-D-----G-------T-----------
> str22: M-------L----------------------------A------P----------------------S------P------------------------------N------------S----K--------------------------------------------------I-----------------------Q-L---------------F----------------N-------------N-----------I---N-----------------------I------------------------D------I---------------------------------N----------------------------------Y----------------------------------------------EHTLYFASVSA----------------------------------Q-----------------------------------------------------------N------------S-------------------F--F-A------------Q---------------------WVVYS---------------------------------AD----------------KAI------
> str23: M---S--------------------------------A-------------------I-------T-------------------E-------T-------------K------------------------------P------T----------------------------I-----E-------------L-P--------A--L-------------A-E--------------------G----------F-----------Q--------R--------------------------------Y------------------------------------------N------------------K-T----P--------------------------GF--------------T-C------------------V----------------L-D---------------------R---------------Y------D-------------------H-G----------------------------V-I-------------N--D---------S----------------K-----I---V---L-------------------------Y--------N------------------------
> str24: M----K--------N--I-------------------A-----------------------------------------------E------------------F--K---------------K--A-----------P-E--------L---------A--------------------E--------------------K------L--LE-----------------------------V-------------F---S--N---L--K-----G---------------------------N-------------------------------------------S---------------R------------S--L--------------------D-----------------P--------M---------------------R------------------A------------------G--------K-----------------------------H---D--------------------------V---------V---------------V----I---E---S---------T------------------------K--------K-------L----------------------------
> str25: M-----P--------------------------------------------------------------------Q------------------P-----L------K-----------------------Q----------------------S---L---------D-----------------------------QS-K---------------------------------------W-----------L-----------------------R----------------------------------------------E-A--------E------------------------------------K--HL---------R---------A------L-------------------------------E------S-----------------LVD--------S---N-----L------------------------------------E--------------------------EEKLKPQLSMG---------------E-----D------V------Q-----S--------------------------------------------------------------------------------
> str26: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N-L--------------------------------------------------I-----------------------T---------------------------------------------R-----------------T--------------------------------------------------Q------------------S---------------------Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S-T-------------------Q----D-------------------------
> str27: M----K-F--D-V---------------L-S---------------------------L---F--------------------------A----P--------------------------------------W-A-K----------------------V-------D-----------E-----------------Q-------------E------------------------------------YD-----------------Q---Q------L------------------------N------------------------------------------------N-N-----L------E--------S------I-------------------------------------T------A---------------------------------PK--------------------F---------------------D----D----------------GA-------T------E----------I--------------E---------------S-----E------R-----G-------------------------------DI--------------------------------------
> str28: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N---------F-------------------T----------N-----------------------------R-----T------------------------------------------------------------------------------------------------------------------Q----L---------------P-------------SA----Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S----------------------------------------------------
> str29: M----------------------------------------------------W-------------S---I--------------------------I--V--------L------------K-------------------------L------------------------I-------S----------------------------------------------------------------------------I--------Q------------------------------------------------------P-------------------LLLVTSLPLYNPNMDSCCLISRITPELAGKLT--------------------------------------W------------I-------------F--------I------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str30: M------------------------------------------------------------------------------------E-------------SLVPGFNEKTH--------------------------------------------------V-------------------------------------Q-L-----------------S------------------L----------P-----------------------------VL----------------------------------------------------------------------------------------------------------------------QVRD---------VL-------V--R----------------------G---------F--G--D--------S---------------------------V------------------E--------------------------E---------------------------F---------------------L-SEARQHLKDGT----------------------------------------------------------------------
> str31: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V----------------------M---------------------P----------L------------------F------N---L-------------------I-T------------------T----------------T------------------------------------------------------------------------Q------------------S---------------------Y-------------TN-FTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---------------------------L----------------------------
> str32: M-------------------------H------------------------------------------------Q----------------------I---------T---------------------------------------------------V--------------------VSGPTEVSTCFGSLHPFQSLKPVMANALGVLEGKMFCS----------------------------------------I-G--------------GR------------SL--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: MA-----------------------------T--------------------------L-----------------L-----------R----------SL-------------------------A----------------------L-----------F---------------------------------------K---------------------R---------N-------------------------------K--------D-----K------------------------------------------P--------------------------P-----------I---T----------S----------------------------G----------S----------------------------GGAIRGI-----------K--------------------------------------------------------------HI---------------------------IIVPIPGDS----------------------S-I-----------------T-------------------T---R------------------------S--------------------R
> str34: M------------------------------------------------------------------------------------E-------------SLVPGFNEKTH--------------------------------------------------V-------------------------------------Q-L-----------------S------------------L----------P-----------------------------VL----------------------------------------------------------------------------------------------------------------------QVRD---------VL-------V--R----------------------G---------F--G--D--------S------------------------M---------------------E--------------------------E------------V-------L--------------------S-----E-----ARQHLKDGT----------------------------------------------------------------------
> str35: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N-L---------------------------T----------------------------------------------T--------G---------------T-----------------------------------------------------------------------------------------Q----L---------------P-P-------A---------Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S----------------------------------------------------
> str36: MAN--------I-----I---N------L------------------------W-N----G----------IV-P---------------------------------------------------------------------------------------------------------------------------------M-----V--------Q------------------------------D---------------------------V-------------------------N--V-----A----------------------------------S-------------I---T---A------------------------------------F------K--S----------M--------------------I------------D-----------E-----------------------------T-------------------W------D---------------K-K------I--------------E------A--------------------------------N---------------TCISRKHRN------------------------------------------
> str37: M-------L-----N------------------------------------------------------R-I---Q-----------------T------L-------------------------------------------------------------------------------------------------------M---------K---------------------T------------------A-------N----------------------------------------N-----Y-------------ET------------------------------------I-----E---------------ILRNYLRLYIILAR--------------------------------------------------------N-------------------E-E-----------G--------------R-------G----------------I-------------------L-------I-------------------------------------------------------Y-------------------------D-------------DNIDSV--------------------
> str38: MA--------D------------------P-------A----G------T-----N----G------------------------E-E---------------G----T---------------------------------------------------------------------G-----------C---------------N--G-------------------------------W--------------F-------Y-------------V---------------------------------------------E-A-------------------V----------------------------------V-----------------------------------------------------E----------------------------KKTGDAISDDENENDS---------------------------D------------------------------T----------------G---------------E-----D-----------------L-------------V----------------------------D---------------------------------------
> str39: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V------------------------N-L--------------R------------T-R--------------------------------------------T------------------------------------------------------------------------------------------------------------------Q----L---------------P-P-----------S-----Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H---S----------------------------------------------------
> str40: M------------------------------------------------------------------------------------E-------------SLVPGFNEKTH--------------------------------------------------V-------------------------------------Q-L-----------------S------------------L----------P-----------------------------VL----------------------------------------------------------------------------------------------------------------------QV----CD-----VL-------V--R----------------------G---------F--G--D--------S---------------------------V------------------E--------------------------E------------V-------L--------------------S-----E-----ARQHLKDGT----------------------------------------------------------------------
> str41: M-N-----------N------------------------------------------------------------Q------------R------------------K---------------K-----T-----A---R------------P-S------F--------------------------------------------N--------M---------------------L---------------------------K-----------R---A-----------------------------------------------R-----------------------N----------R----------------V-----------------------------------S----T--------------------VS-----------------------------------QLAKRFSKGLLSGQGPMKLV------------------------------------------------------M------------A-----F--------------------------------------------------------------------------------------------------------
> str42: M---S---------N-----------------------------------------------F---------------------------------D-----------------------------A-----------------------------------------------I--R---------------------------A--L-V---------------------------------------D--------------------------------T----------------------------DAYKLGHIHMYPE-----G----------------T--------------------E-------------------Y----------V---L-------------S------------------------------------N-FT----D---------------------R---G--S-----------R-I------------E----------G----------------------------V-----------T----H---T----V-----------------H---------------------------------------------------------------------------
> str43: M----------I-------------------------------------------------------------------------E----L----------------------------------R-H------------E-------------------V-------------------------------------Q----------G----------------------------------------D--L------------------------V----T---I----------------N--V-V--------------ET------------------------P-----------------E--------------------------------D-L-DGF---------------R---D------------F--------IR------------------A---------------------------------------------------------H--------------------L-------I--------CLAVDTET------T--G------------L---------D----I-Y-----------------------------------------------------------------
> str44: M------F----VF--------------L-----------------V-----------L-----------------L-----------------P-----LV----------------SS-----------Q---------------------------------------C---------V----------------------M---------------------P----------L------------------F------N---L-------------------I-T------------------T--------------------------------------------N--------------------------------------------Q------------------S---------------------Y-------------TNSFTRG-V--------------------------------------Y-------------------------------------------Y-----P------------D-------------------KVFRSS--------------------V--------L--H--------------------------------------------------------
> str45: M---SK----D-----------------L-----------------V------------------------------------------A-----------------------------------R-----Q---A-------------L------------------------------------------------------M-------------------------------T------------------A---------------------R-----------------M-------------------K----------A-------D-------F---V------------------------------------------------------------FFLFVLWKALSLPVPTRCQIDMAKKLSA-----------G---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str46: MA--S---LL-----K-------S----L--T--------------------------L---F-------------------K-----R----T-------------------------------R--------D---------Q-------P-------------------------------P---------L----------A------------S-G------S-----------------G------------G----------------------A-----I-----------------------------------------RG-------------------------------I---------K--H-----V--I--------I-----V---L----------------------I------------------------------------P---GD--S-------S-------------------------I---V----------------------------T-----------------------------------------------RS------------R-----------------------------------------------------------------------------
> str47: M--------------------------------------------------------------------R--V---------------R--------------G--------I------------------------------------L------R-------------------------------------------------N----------------------------------W--Q-----------------------Q----------------WWIWTSLGFWMFMICSVVGNLWVTVYY-----G----------------------------V---P------------------------------V-------------------------------WK--------------------E-----A----------------------K-T-------------------------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str48: MA----------V------------------------------------------------------------------------E--------P---------F---------------------------------PR-R----------P---------------------I----------T-------------------------------------R--P---------------------------HA----S-I-------------------------------------------------------------E---------------------V----------D--------T----------S----------------------------G-------------------I-------------------GG-------S-------------A------------------G--S------------------S-------E-K--V-----------F-----------------------------CL----------------------IGQAE------------G-----------------G-----------E--------------------------P---NT------V--
> str49: M------F------------------------Y----A-----------------------------------------------------------------------H----------------A----------------------------------F----------------G----G-----------------------------------------------------------------YDENLHAFPGIS--------S-------------TV----------------------------A---------------------------------------N---D-----------------------V----R---------------------------K------------------------Y--SV-----------------V---------S---------------------------VY---------------------------------------N------K-K--------------------------------------------------------------Y----------------------N---IVKNKYMW-------------------------------
> str50: MANYSKPFLLDIVFNKDIKCINDSCSHS------D----C-----------------------------RY----Q-----------------------S-----N------------S----------------------------------Y------V-------------------E-------------L----------------------------R-------R-N----------Q----------A-----------L------------------------------------N----------K-------------------------------------N-------L----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 678
> best bound: 0.0
> wall time: 146.70s
> ```
