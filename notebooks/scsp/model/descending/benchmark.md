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
Model = scsp.model.descending.Model
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
>  Sol: ulctkginycosjiqfolnkuhmpbxnhtqgevoaxzpplgbrddbcsvrxsuqpvnngissbxf
> str1: ---tkg-n-----------kuhmp-xnhtqg----xz-----------v-x--------is----
> str2: ------i---o-jiqfoln-----bx---------x----------c-v--suqpv---issbxf
> str3: ulc---inycos----o---------------vo--zppl--------------p----------
> str4: ------i-----------------------gev-a-z---gbrddbcsvr-----vnng-----f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 65
> best bound: 0.0
> wall time: 0.00s
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
> --- Solution (of length 105) ---
>  Sol: utrxwxpypiojiqkgevafolrzgnkbcizfjrdrlevdbxuhmpxnyhtcosopmqvgxertozdtmpfzvsmsbrvouigqplpexwvnngbcdissbhoxf
> str1: -t------------kg---------nk---------------uhmpxn-ht------q-gx----z------v---------------x--------is------
> str2: ---------iojiq-----fol---n-b-------------x----x----c------v--------------s------u--qp-----v------issb--xf
> str3: u--------------------l------ci-----------------ny--coso---v-----oz---p--------------plp------------------
> str4: ---------i-----geva----zg--b-----rd----db----------c-s----v---r---------v------------------nng----------f
> str5: ------pyp------------lrz-----------------xu--------c---pmqvg---t--d---f---------ui--------v----cd-s-b-o--
> str6: ------p--------------------b------d--evd-----------c------v-------d--pfz-smsbr-o---q------v---b-----bh---
> str7: ----------------e--------n-bc-zfj-----------------t-------v-xer--z----------brv--ig-pl-e-----------------
> str8: --rxwx-------qk-------r-----------drl--------------c-----------to-dtmp-------r------p---xw------d--------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 105
> best bound: 0.0
> wall time: 0.00s
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
> --- Solution (of length 148) ---
>   Sol: hikltrxusfcwxqpypiojiqkgfolrshavzpenkqabdrlectzfivbwadxudghmpxcpmqjwtnyhvgtqcokkdtmiupfzsovkmgxesbrddozuiqzvpxwavbfgcdijusvrvnnigplpqsbezhkowwyhmgxf
> str01: ----t-----------------kg-----------nk------------------u--hmpx-------n-h--tq-----------------gx-------z----v-x--------i--s--------------------------
> str02: -i----------------ojiq--fol--------n---b--------------x------xc---------v---------------s--------------u-q--p---v-----i--s-----------sb-----------xf
> str03: -------u------------------l-----------------c---i--------------------ny-----co----------sov----------oz-----p--------------------plp----------------
> str04: -i---------------------g----------e--------------v--a----------------------------------z-----g---brdd------------b--c----svrvnn-g------------------f
> str05: --------------pyp---------lr----z---------------------xu------cpmq------vgt-----d-----f----------------ui--v--------cd---s------------b----o--------
> str06: --------------p------------------------bd--e-----v---d--------c---------v-------d----pfzs---m---sbr--o---q-v-----b--------------------b--h----------
> str07: ----------------------------------en---b----c-zf------------------j-t---v---------------------xe--r---z----------b---------rv--igpl----e------------
> str08: -----rx----wxq--------k----r------------drl-ct-------------------------------o--dtm--p------------r---------pxw------d------------------------------
> str09: --k-------------------k--------------qa--------fi--------g-------qjw---------okk--------s--k------r--------------b----------------l--------------g--
> str10: ---l--x-----x-p---------------a--------b--------ivb---------------------v--------------z---k---------oz---zv---------d------------------------------
> str11: --k--r-----------i------f---s-av---n--------c--------d-----------q-w---h---------------z----------------------------c-------------------------------
> str12: -------------q----------------a-----------------------xudg-------q------v--qc------------------e--------------w--bfg--ij-------------------owwy-----
> str13: -----r--s---xq-----j---------------n-----------f------------p--------------------------------------------------a-----di-us-----i----q-bezhko---hmg--
> str14: -i---------w----------------sh-v--------------------------h---c--------------o----miu-----v--------dd-------------------------------------------m---
> str15: h---t-x-----xq-----j------------z----q-b----ct----b-a-------------------------k----------------------------------------------n----------------------
> str16: ------xusfc-------------f-------zpe--------ec----v-wa----------------n----t-----------f-----mg-----------qz-------------u---------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 148
> best bound: 0.0
> wall time: 0.01s
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
> --- Solution (of length 35) ---
>   Sol: eebbaeabeddbdcabccdbeaedecadbcebded
> str01: ---------d---c-bccdb-----c---ce----
> str02: --b------ddb--------e-e-e-----ebd--
> str03: -------------ca-c-d-e-e--c----eb-e-
> str04: ----ae---dd-d-----d-e-------b---d-d
> str05: ----a--------c-b----e-e--ca-bce----
> str06: --bba--be--bdc-b-----a-------------
> str07: --bbaea-e--b--a---d--a-------------
> str08: ee---e--e----c-b--dbe-e------------
> str09: -------------c--c-d-e-ed--ad-c--d--
> str10: --b------d----ab--dbea----ad-------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 35
> best bound: 0.0
> wall time: 0.00s
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
> --- Solution (of length 49) ---
>   Sol: cdebacbaeadecdcbbaeabceddbdcabccdbeaedecadbcebded
> str01: -d---cb-----c-c--------d-b-c--c---e--------------
> str02: ---b------d--d-b--e---e-----------e-e-----b---d--
> str03: c---ac----de------e--ce--b--------e--------------
> str04: ----a---e-d--d---------dd---------e-------b---d-d
> str05: ----acb-e--ec----a--bce--------------------------
> str06: ---b--ba-------b--e-b--d---c-b-----a-------------
> str07: ---b--baea-e---b-a-----d----a--------------------
> str08: --e-----e--e------e--c---bd--b----e-e------------
> str09: c----c----de------e----d----a---d------c-d-------
> str10: ---b------d------a--b--d-b--------ea----ad-------
> str11: --e-------de-d---a-a--------a-----ea----a--------
> str12: ----a--aea-------a--b-e-----------ea---c---------
> str13: --e-a--a-------b-----c------a-ccdb---------------
> str14: ---b------de------ea---d----------ea-de----------
> str15: c---a---e-d------a-----d----------e-e-e--d-------
> str16: --eb-c-a--d----b-a--b----b--------e--------------
> str17: -d--------d-c-----e---e-----ab--d-ea-------------
> str18: -d--a-b-----cd---------d----------eae--c---------
> str19: ----a--a--d-c-----e---ed----a------a------b------
> str20: ----a---e--ec-c---e---e-----------ea----a--------
> str21: ---b--b---d------ae--c------a------a-de----------
> str22: -d--ac--e-d------ae----d----ab-------------------
> str23: ----a--aea-----bb---b----b-c------e--------------
> str24: -de-------d----b-----c---b-ca------a------b------
> str25: -d-b------d------a-a--e--b---bc--b---------------
> str26: -deb----e-d----b--e-b-------a-c------------------
> str27: c-e-----e------b-----c-d---c-b--d-e--------------
> str28: -d-b----e-d------a-a---d----a------a------b------
> str29: c----c------cdcb--e-b--d---c---------------------
> str30: ----a---e--e-----a---c-d-b-c-b--d----------------
> str31: -d--acb-ea--c-c------c-d-------------------------
> str32: --e--c--e------b-----c-----c----db---d----b------
> str33: -d--------d----bb----ced----ab---b---------------
> str34: ----a--aea-----b-a-a--e--b--a--------------------
> str35: --e--cb--------b-----c------a------a-d-c-d-------
> str36: -deb-c------c-----e--c-d-b-c---------------------
> str37: -d--a--a----c--b-ae---e--b-c---------------------
> str38: ----a-----d------a--b-e-----a------a---c---ce----
> str39: -d--a---e---cd-b-a---c------a------a-------------
> str40: -d--acb--------b-------d---c------e--d-c---------
> str41: -de-------d----b--e---e--b---b--d-e--------------
> str42: cd--a-----d-cdc--------d----a------a-------------
> str43: c-e-----e-d-c--b-ae---ed-------------------------
> str44: c-e-a---e---c----a-a--------a-c----a-------------
> str45: -d---c------c-c---e-b----b---b-----a-d-----------
> str46: ---ba---e--e-----ae-b----bd-------e--------------
> str47: -d-b------de---b-a---c-----c----db---------------
> str48: --eb-cb-e--e-d---aea-----------------------------
> str49: ----a---e--e------e-b----bd--bc----a-------------
> str50: -d-b------d------a--bce----c-b---b---------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 49
> best bound: 0.0
> wall time: 0.00s
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
> --- Solution (of length 31) ---
>   Sol: TCGTCAGGTACACTGAGGATCCTGTGCCACG
> str01: -----A--T-----G-GGAT--------ACG
> str02: -----A--TAC-CT-----TCC----C----
> str03: -C---A----C---GA--AT--TG----A--
> str04: T----A---A-A---A---TC-TGT------
> str05: -----AGGTA-AC--A--A---------A--
> str06: T--TC-----C--T-AGG-T--------A--
> str07: T--T--G-TA----GA---TC-T--------
> str08: T-G---GG-A-A--G----T--T---C----
> str09: T--TC-----CAC--A--A-C-T--------
> str10: TC-T-A---A-AC-GA--A------------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 31
> best bound: 0.0
> wall time: 0.00s
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
> --- Solution (of length 165) ---
>   Sol: ACTCGAGTAAACTGCAGACCAGTGACTTCACCGTCAGTCTACGACTATCAGCCTGATGCTGGTAAGATCGCACGATAACTTCGACTAGCCTGCACGTAGACTTCGCTTAATACGATACGGCCCAATGGCTGTCGCTAATGCTCGTAGCGTTAAACGGTCATARCG
> str01: --T--AGTA----G--------T-A-------G--A--CT-C--C-----G---GA-------A-G-T-G-AC-A-AAC--C--CT-G-----A---A-A--------A----GA-A--------TGG--------A-T------A-----AA----T-ATA---
> str02: ----G-G-A---T--A-A--A----C---AC--TC---C--CGA--A--A-----AT------AA--T-------T---T--GACT----T--A---A-AC-------AA--CG---CG----A----C-------A--G-T--T--C---AA--G---------
> str03: A-T--A-----C--C-------T---T-C-C--T-AG-----G--TA--A-C---A-------AA---C-CA--A---C--C-A--A-C-T-----T----TT-G---A-T-C--T-C-------T---TGT----A--G-----A---T----C--T------G
> str04: --T--A--AA--T---------T-A-T--A-----A-TCT-----TAT-A-C-T-A-G-T---AA-A----A--A-A--T---A---G---G---GT-G--T------AA--C----CG----AA-----------AA--C--G--G--T----C----------
> str05: --T----TAAA----A--C-AG---C--C----T--GT----G-------G---G-T--TG-------C--AC-----C--C-ACT--C----AC--AG-----G--------G---C--CC-A----CTG--G-----GC--G---C---AA--G---------
> str06: A-T-GA-----CT---------T--C--CA-----A-T----G-------G----AT-C---------C-CA--A---C--C---T--C----A---AG-CTTC-C--A---C----C--CC-AATGG-T-T---T----C----AGC-----------------
> str07: A----A-----C---A-A--A----C--CA-----A--C--C-A--A-C----T--T--T--T--GATC------T--CTT-G--TAG-----A--T---CT--G-TT----C--T-C-------T----------AA-------A-CG--AA-C----------
> str08: A-T-GA--AAAC-G-A-A--A---A-TT-A---T---T--A----T--CA-----A-G--GGTA---T-G---GA-A-----G--T-G---G-A---AG-CT--G---A---CGA-A------A-T---------------------------------------
> str09: ACTCG-G----CTGCA------TG-CTT-A--GT--G-C-AC---T--CA-C--G---C----A-G-T---A---TAA-TT--A--A---T--A---A--CT------AAT----TA------------------------------------------------
> str10: --T----T-----G--------T-A-------G--A-TCT--G--T-TC----T----CT---AA-A-CG-A--A---CTT----TA------A---A-A-T-C--T------G-T--G------TGGCTGTC---A---CTC----------------------
> str11: ----G------C---AGA---G---C---A---T---T-T-----T--C----T-A-------A---T---A---T--C--C-AC-A------A---A-A-T--G---AA---G----G-C--AAT----------AAT--T-GTA-C-T-A--C--TC------
> str12: A-T-GAG----C--CA-A---G--A-T-C-C-G--A--C---GA--A---G----A-GC---------C-C-C-A-A-----G----G-----A-G--GA----G---AA---G----G----A--GG--G-----A---C-C----C------C---C------
> str13: --TC---T---C---A--C-AGT---T-CA-----AG---A--AC---C--C---A-------AAG-T---AC-----C--C--C---CC---A--TAG-C--C-CT-----C--T---------T----------AA-------AGC------C----A---C-
> str14: A---G-GT----T---------T-A-T--ACC-T---TC--C---TA---G---G-T------AA---C--A--A-A-C--C-A--A-CC---A---A--CTT---T-----CGAT-C-------T--CT-T-G-TA----------------------------
> str15: A---G-GT----T---------T-A-T--ACC-T---TC--C--C-A---G---G-T------AA---C--A--A-A-C--C-A--A-CC---A---A--CTT---T-----CGAT-C-------T--CT-T-G-TA----------------------------
> str16: --T--A--AAAC---A-AC---T--C---A-----A-T--AC-A--A-CA---T-A-------A-GA----A--A-A--T-C-A--A-C--GCA---A-A--------AA--C-A--C-------T--C-------A---C----A-----AA------------
> str17: -C-CG------C--C---C-A-T---TT----G---G-----G-C-----G---G---CT--------C------T--C---GA---GC--G-A--TAG-CT-CG-T-----CGA-A--------T--C---C-CT----C--G-A-C------C--T-------
> str18: A-T--A-----C--C-------T---T-C-CC---AG-----G--TA--A-C---A-------AA---C-CA--A---C--C-A--A-C-T-----T----T-CG---A-T-C--T-C-------T---TGT----A--G-----A---T----C--T------G
> str19: --TC---T---C---A--C-AGT---T-CA-----AG---A--AC---C----T----C----AAG-TC------T--C--C--C---CC---A--TAG-----GC------C--T-C-------T---T-TC---A--G-TC--AG------------------
> str20: ----GA-T---CT-C-------T--CT-CACCG--A----AC--CT----G---G---C---------C-C-CG--------G----GC----A---A-A-T--GC------C----C-------T----------AAT-C-C--AG----A---GGT------G
> str21: A---GAG----C---A-A----T--C---A--GT--G-C-A----T--CAG----A-------AA--T---A---TA-C--C---TA---T-----TA---T------A---C-A--C-------T---T-T-GCTAA-G-----A-----A-----T-------
> str22: A----A-T----T--A-A--A---AC---A---TC--TC-A--A-TA-CA-----A--C----A---T---A--A-------GA--A------A---A-AC-------AA--CG---C-----AA-----------AA-------A-C---A--C--TCAT----
> str23: A----A--A--C-G-A-AC---T---TT-A-----A----A--A-T--C----TG-TG-TGG------C------T------G--T--C----AC-T---C---G--------G---C-------TG-C-------A-TGCT--TAG--T-----G--C------
> str24: A-T--A--A--CT--A-A----T---T--AC--T--GTC---G--T-T--G----A--C----A-G---G-AC-A---C---GA---G--T--A---A--CT-CG-T-----C--TA--------T--CT-TC--T---G-------------------------
> str25: A-T-GAGT-----G--------T--C---AC-G--A----A----T-TCA-C--G-T------A----C--A--AT------GA--A-C-TG---G-A---T--G-TT----C-A--CG------TGG--------AAT------A-----A-------------
> str26: AC-CG--T-----G--G----G---C------G--AG-C---G-------G--TGA--C---------CG---G-T------G--T--C-T-----T---C--C--T-A----G-T--GG------G--T--C-C-----C----A-CGTT----G---A-AR--
> str27: A----A--A----G--G-----T---TT-A---T-A--C--C---T-TC--CC--A-G--G-TAA---C--A--A-A-C--C-A--A-CC---A---A--CTT---T-----CGAT-C-------T--CT-T-G-------------------------------
> str28: A---G--TA----G--------T---T-C---G-C---CT--G--T----G--TGA-GCTG--A----C--A--A-A-CTT--A---G--T--A-GT-G--TT---T------G-T--G----A--GG--------A-T--T---A-------------------
> str29: --T----T----T--A------T-AC--C----T---TC--C---TA---G---G-T------AA---C--A--A-A-C--C-A--A-CC---A---A--CTT---T-----CGAT-C-------T--CT-T-G-TA--G-----A---T---------------
> str30: A-T-G------C-G--G-----T--C------GTC--TCT-C--C---C--C--G--GCT--T----T-------T---TT----T--CC--C-CG----C---GC------CG---CG------T---TG--GC----GC-CG-A-------------------
> str31: ----G--T-----G-A--C-A---A----A-----A----AC-A-TA--A---TG--G-----A----C------T--C--C-A--A-C----AC-----C-------A-T--G-T-C-----AA-G-CT-T---T----C----AG-GT-A---G---A---C-
> str32: ----G--T-----G--------T-A----A--G--A----A--AC-A---G--T-A-------A-G--C-C-CG--------GA--AG--TG---GT-G--TT---TT-----G---CG----A-T---T-TCG--A--G---G---C------CGG--------
> str33: ----GAG-AA--TG-AG-----T--CT-CA---T---T--AC--C-----GCC-----C-GGTA----C------T---T---A---GC----A---AG-CT------AATA-G-T-C-----A----C-G--GC------------------------------
> str34: A-T-G--T-----G--G-----T--C------G--A-T----G-C---CA---TG--G-----A-G---GC-C-----C----AC---C----A-GT----T-C----A-T----TA------A--GGCT--C-CT---G---G---C---A-----T--T----
> str35: AC--GAG----C-G--------T---TT-----T-A----A-G-------G---G---C---------C-C--G----C---GACT-GC--G-ACG--G-C--C----A---C-AT--GGCCC--TG--T------A-TG-T-----------------------
> str36: ----G-GT----T---------T-A-T--ACC-T---TC--C--C-A---G---G-T------AA---C--A--A-A-C--C-A--A-CC---A---A--CTT---T-----CGAT-C-------T--CT-T-G-TA--G-------------------------
> str37: --T-G-G------G-A-A---GT---T-C-C----A----A--A--A---G----AT-C----A----C--A--A-AAC----ACTA-CC---A-GT---C-------AA--C----C-------TG---------AA-G-T---A-C---A--C----------
> str38: ----GA--A----GC-G-----T---T--A-----A--C---G--T----G--T--TG-----A-G---G-A--A-AA----GAC-AGC-T-----TAG-----G---A----GA-AC-----AA-G---------A--GCT-G--G-G----------------
> str39: AC-C-AG----C-GCA--C---T---T-C---G---G-C-A-G-C-----G---G---C----A-G--C--AC-----CT-CG----GC----A-G----C-------A---C----C-------T--C-------A--GC----AGC---AA-C----------
> str40: A-T-G-G------G-A--C-A---ACTT-A---T---TC--C---TATCA---TG-TGC---------C--A--A-------GA---G---G----T----TT---T-A---C----C--C-----GG-TG-----A---C-C--A-------------------
> str41: --T----T-----G--------T-A-------G--A-TCT--G--T-TC----T----CT---AA-A-CG-A--A---CTT----TA------A---A-A-T-C--T------G-T--G------TGG-T-T-G-T----C----A-C-T----C----------
> str42: A----A-----C--CA-ACCA---ACTT-----TC-G---A----T--C----T----CT--T--G-T---A-GAT--CT--G--T----T-C---T---CT------AA-ACGA-AC-------T---T-T----A----------------------------
> str43: ----G-G------G--------T---T-C----T--G-C--C-A------G---G---C----A---T---A-G-T--CTT----T----T-----T----TTC--T------G----G-C-----GGC---C-CT--TG-T-GTA-----AA-C---C-T---G
> str44: ----G-G----CTGCA------TG-CTT-A--GT--G-C-AC---T--CA-C--G---C----A-G-T---A---TAA-TT--A--A---T--A---A--CT------AAT----TAC-------TG--T-----------------------------------
> str45: --T-G------C---A------TG-CTT-A--GT--G-C-AC---T--CA-C--G---C----A-G-T---A---TAA-TT--A--A---T--A---A--CT------AAT----TAC-------TG--T--CG-T-----------------------------
> str46: --T----T---C--CA--C-A---ACTT-----TC---C-AC--C-A--AGC-T----CTG-------C--A--A-------GA-T--CC--CA-G-AG--T-C----A----G----GG------G-C---C--T---G-T-----------------------
> str47: --TC---TAAAC-G-A-AC---T---TT-A-----A----A--A-T--C----TG-TG-TGG------C------T------G--T--C----AC-T---C---G--------G---C-------TG-C-------A-TGCT--TAG------------------
> str48: AC-CG-G-A---TG--G-CC-G---C------G--A-T-T-----T-T-----T----C-GG-A-G-TC-C----T---T--G----G---G---G--GAC--C----A---C--T-C-----A--G---------AAT------AG----A-------------
> str49: -CT----T-----G--------T-A-------G--A-TCT--G--T-TC----T----CT---AA-A-CG-A--A---CTT----TA------A---A-A-T-C--T------G-T--G------TGGCTGTC---A---CT-----------------------
> str50: A-T-GAG----C---A--C---T-A----A--G-C-G---A--A------G----A-------A----C-CA--A-AA-----A---GC----A-G-A--C-------AATAC-A-AC--CC----G-CT------A-T--T---A-C-----------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 165
> best bound: 0.0
> wall time: 0.07s
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
> --- Solution (of length 50) ---
>   Sol: MESLFVPYAGFRNEEHVPQSKSLNFTDEAIRALSYQHDFGRNCPVKGYQT
> str01: M-------A-------------L----------SY-------CP-KG--T
> str02: M-----------------QS-SLN----AI-------------PV-----
> str03: M-----P---------------L----------SYQH-F-R----K----
> str04: ME-----------E-HV------N---E----L---HD------------
> str05: M-S---------N-----------F-D-AIRAL-----------------
> str06: M---F------RN-----Q----N---------S------RN----G---
> str07: M---F--YA------H------------A---------FG------GY--
> str08: M-S-----------------K---FT----R---------R--P---YQ-
> str09: M-S-FV--AG------V--------T--A------Q--------------
> str10: MESL-VP--GF-NE------------------------------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 50
> best bound: 0.0
> wall time: 0.00s
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
> --- Solution (of length 456) ---
>   Sol: MFHLATPQISKDPRYNFLVLDSGPAHIERQALKKKMEFDNTVGIQSLAEVPITDLFNGYFRKMKDNWQETAHQWWINSLHIDPKWINGKFYYSNRRLAVFFLLPTWEFSHRTLYGAKHQVLSFNETKWIDKAVELQGDHITHSPMFVLRESTAQCAAVMIPLNFCDDTKNYLIGWSKAKPNTDVVRILQHEKPRTNRLESGFTKQARLPNNYNSVIPLWERKFPAGVSTVPGSFEYEAVTCQWEILSDPMTHQVRLANDGIVSFGKIMPCTESRVGHPDELKFIWVARRGWSAKGDDGYLSAFSENDHIVIKTNIVFCRGTPVTAIYQPDYLESRAENMVIDETWDKSCCYVAGQDLPAETRGILYIGYFRVDLSTQPKMDFFWENRSHITPELANDTQASVSQGLKECDLYTWNISLFHARQYSIMDKHGSGEVECLIKDGLTRNPMAFHVQDSL
> str01: M------------R-----------H-----L-------N---I---------D---------------------I------------------------------E----T-Y-------S--------------------S-------------------N--D------I---K---N-------------------G-------------V--------------------Y-----------------------------K--------------------------------Y--A----D-----------------A-------E--------D---------------------------F--------------E----I---L-----------L------------F-A--YSI-D--G-GEVECL--D-LTR-----------
> str02: M--------------------------ER-------------------------------R---------AH----------------------R---------T----H--------Q----N---W-D-A--------T---------------------------K----------P-----R----E--R--R------KQ-----------------------T------------Q---------H--RL--------------T-----HPD----------------D----S-------I-----------------Y-P-----R-----I-E---K-----A------E--G-------R-------K-----E-----------D----------------------H----------G-------------------------
> str03: M--------------------------E----------------------P------G------------A------------------F--S-----------T----------A----L-F------D-A--L-------------------C----------DD-----I--------------L-H---R--RLES----Q--L------------R-F--G-----G------V--Q--I---P-------------------P--E--V----------------S---D-------------------------P------------R----V----------Y-AG-----------Y----------------------------A----------L----L---------------------------------------------
> str04: M---------------------G---------K----F--------------------Y-------------------------------Y-SNRRLAVF---------------A--Q------------A---Q------S-----R----------------------------------------H-------L--G------------------------G-S-------YE----QW--L----------A------------C----V----------------S--GD----SAF---------------R-----A-------E------V------K-----A--------R---------V----Q-K-D---------------------------------------------------------------------------
> str05: -F--------------F-----------R-------E--N------LA-------F-----------Q----Q--------------GK--------A------------R-------------E--------------------F--------------P--------------S--------------E-------E------AR-----------------A--------------------------------N----S-----P-T-SR-----EL---WV-RRG----G----------N---------------P---------L-S--E---------------AG----AE-R--------R---------------------------------G-------T-------------------------------------------
> str06: M----------DP--------S---------L--------T---Q----V----------------W---A---------------------------V-------E-------G------S----------V-L-------S---------A--A-V-------D-T---------A------------E---TN---------------------------------------------------D--T--------------------E-----PDE---------G---------LSA--EN--------------------------E--------------------G-----ETR-I--I---R------------------IT-------------G-----------S---------------------------------------
> str07: M---A-----------F---D----------------F-------S---V--T----G-------N---T-------------K------------L--------------------------------D----------T-S------------------------------G---------------------------FT-Q--------------------GVS----S----------------MT--V--A-----------------------------A--G----------------------T------------------L--------I-----------A--DL--------------V------K-----------T---A-----S-SQ-L------T-N--L--A-Q-S-------------------------------
> str08: M---A-------------V-------I----L------------------P--------------------------S--------------------------T--------Y-----------T---D------G---T-----------A--A--------C--T-N---G-S---P--DVV---------------G-T----------------------G--T--------------------M----------------------------------WV-------------------N------T-I----------------L-------------------------P----G---------D--------FFW------TP--------S---G--E--------S-----------------V---------R------V----
> str09: M--------------N------------------------T-GI-------I-DLF--------DN-----H--------------------------V------------------------------D------------S----------------IP------T----I--------------L----P----------------------------------------------------------HQ--LA-------------T---------L--------------D--YL---------V--------R-T----I--------------IDE------------------------------------------NRS-------------V---L----L-------FH-----IM---GSG-----------------------
> str10: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--V----N--------L-------------R--------T-R-----T-Q--LP-------P-------A----------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S-------------------------------
> str11: M----------D---------S----------K---E---T--I--L----I----------------E------I----I-PK-I--K---S--------------------Y------L-------------L--D--T---------------------N---------I--S---P-----------K-------S-----------YN----------------------------------D---------------F--I-----SR-------------------------------N-----K-NI-F-----V--I-----------N------------------L--------Y-------------------N---------------VS---------T--I----------------------------------------
> str12: M--L-------------L---SG---------KKKM----------L-------L---------DN------------------------Y---------------E----T---A---------------A--------------------A--------------------------------R--------------G-----R------------------G-----G---------------D-----------------------E-R-------------RRGW-A---------F---D-----------R--P--AI-------------V---T--K--------------R----------D-----K--------S--------D------------------------R----M---------------------A-H-----
> str13: M--------------N------G----E--------E-D--------------D--N-----------E---Q------------------------A-----------------A---------------A-E-Q-----------------Q-------------TK-------KAK------R----EKP----------KQAR--------------K----V-T---S-E--A----WE-------H-----------F--------------D-------A-------------------------T----------------D-----------D-----------G----AE------------------------------------------------C-------------------KH--------------------------
> str14: M--------------------------E-----------------SL--VP------G-F-----N--E--------------K--------------------T----H---------V---------------Q-----------L--S----------L-----------------P---V---LQ-------------------------V-----R--------------------------D-----V-L-----V-----------R-G------F------G-----D----S--------V----------------------E---E--V----------------L-----------------S---------E---------A--------------------------RQ------H-------L-KDG-T------------
> str15: M------------RY-----------I--------------V---S----P----------------Q----------L-------------------V--L----------------QV----------------G-------------------------------K----G--------------Q-E-----------------------V----ER---A--------------------L----------------------------------------------------YL------------T--------P----Y--DY---------IDE---KS---------P-----I-Y--YF---L------------RSH----L-N-------------------I------Q---------------------R-P---------
> str16: M-----P------R----V----P-----------------V----------------Y-----D------------S----P-----------------------------------QV-S---------------------P------------------N----T---------------V--------P-----------QARL----------------A---T-P-SF---A-T--------P-T------------F---------R-G----------A--------D-----A-------------------P--A--------------------------------------------F------Q---D---------T---AN--Q----Q----------------ARQ---------------------------------
> str17: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--V----N--------L-------------R--------T-R-----T-Q--LP--------L------A----------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S-------------------------------
> str18: MF----------------V------------------F-----------------F------------------------------------------V--LLP--------L------V-S--------------------S----------QC--V----N--------L---------T------------T-R-----T-Q--LP-------P-------A----------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S-------------------------------
> str19: M--------------------------E--A------------I-------I-------------------------S-----------F-------A----------------G-------------I-------G--I----------------------N-------Y-----K-K--------LQ----------S---K---L---------------------------------Q---------H------D----FG--------RV-----LK----A------------L------------T--V----T---A---------RA--------------------LP----G-------------QPK---------HI----A--------------------I-----RQ---------------------------------
> str20: M---A----S-----------SGP---ER-A-----E----------------------------------HQ--I----I---------------L------P--E-SH--L--------S--------------------SP---L---------V----------K--------------------H-K-----L---------L---Y-----------------------Y------W----------------------K--------------L-------------------------------T------G-----------L-------------------------P------L------------P--D---E-----------------------CD--------F--------D-H-------LI-----------------
> str21: M--------------------------E-----------------SL--VP------G-F-----N--E--------------K--------------------T----H---------V---------------Q-----------L--S----------L-----------------P---V---LQ-------------------------V-----R--------------------------D-----V-L-----V-----------R-G------F------G-----D----S--------V----------------------E---E--V----------------L-----------------S---------E----------------V-------------------RQ------H-------L-KDG-T------------
> str22: M--LA-P--S--P--N-----S----------K----------IQ-L--------FN--------N---------IN---ID---IN---Y---------------E--H-TLY--------F--------A----------S---V---S-AQ--------N------------S-------------------------F--------------------F-A----------------QW----------V-------V------------------------------------Y-SA----D----K------------AI----------------------------------------------------------------------------------------------------------------------------------
> str23: M--------S--------------A-I-------------T-------E---T--------K--------------------P---------------------T-----------------------I----EL--------P--------A--------L---------------A------------E---------GF--Q-R----YN--------K------T-PG-F-----TC------------V-L--D--------------R------------------------Y-------DH-----------G--V--I-----------N---D-----S------------------------------K----------I-----------V---L-----Y--N-----------------------------------------
> str24: M---------K----N----------I---A-----EF-----------------------K-K------A-----------P-----------------------E-----L--A--------E-K-------L------------L-E-------V-----F-----------S----N------L---K--------G--------N---S------R------S-----------------L-DPM----R-A--G-----K----------H-D------V-----------------------V-----V---------I------ES---------T--K-------------------------------K--------------L--------------------------------------------------------------
> str25: M-----PQ----P----L--------------K-----------QSL------D-------------Q---------S-----KW-----------L-------------R-------------E------A-E----------------------------------K--------------------H-------L--------R-----------------A--------------------L-------------------------ES-------L----V---------D----S----N-------------------------LE---E-----E---K---------L---------------------K------------P------Q------L----------S---------M---G--E------D----------VQ-S-
> str26: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--V----N--------LI--------T---R--------T---------Q--------S---------------------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S------------------T--------QD--
> str27: M---------K-----F---D--------------------V----L------------------------------SL----------F-------A-----P-W---------AK--V---------D---E-Q-------------E--------------------Y-----------D-----Q---------------Q--L-NN-N----L-E-------S----------------I-----T-----A-----------P------------KF------------DDG---A----------T-------------------E-------I-E----S-----------E-RG---------D----------------I------------------------------------------------------------------
> str28: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--V----NF---T-N---------------R--------T---------Q--LP----S----------A----------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S-------------------------------
> str29: M-----------------------------------------------------------------W----------S--I----I------------V--L--------------K---L-------I-------------S----------------I----------------------------Q---P----L---------L---------L--------V-T---S------------L--P------L------------------------------------------Y------N---------------P---------------NM--D-----SCC------L------I----------S-----------R--ITPELA---------G-K---L-TW-I--F------I------------------------------
> str30: M--------------------------E-----------------SL--VP------G-F-----N--E--------------K--------------------T----H---------V---------------Q-----------L--S----------L-----------------P---V---LQ-------------------------V-----R--------------------------D-----V-L-----V-----------R-G------F------G-----D----S--------V----------------------E---E--------------------------------F---LS---------E---------A--------------------------RQ------H-------L-KDG-T------------
> str31: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--VM-PL-F-----N-LI--------T------------T-------T-Q--------S---------------------Y---T-----------------N-----F------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H-----------------L------------------
> str32: M-H----QI-------------------------------TV-------V---------------------------S---------G---------------PT-E------------V-S---T----------------------------C--------F---------G-S-----------L-H--P--------F--Q--------S---L---K-P--V----------------------M------AN----------------------------A------------L-------------------G--V--------LE--------------------G------------------------KM-F--------------------------C-------S--------I----G-G-----------R---------SL
> str33: M---AT-----------L-L--------R----------------SLA------LF-----K--------------------------------R----------------------------N--K--DK------------P----------------P-----------I--------T-----------------SG------------S-----------G-----G-----A------I---------R----GI----K----------H------I------------------------I-I----V-----P---I--P------------------------G-D------------------S------------S-IT------T-----------------------R--S-------------------R-----------
> str34: M--------------------------E-----------------SL--VP------G-F-----N--E--------------K--------------------T----H---------V---------------Q-----------L--S----------L-----------------P---V---LQ-------------------------V-----R--------------------------D-----V-L-----V-----------R-G------F------G-----D----S-------------------------------------M---E----------------E-----------V-LS---------E---------A--------------------------RQ------H-------L-KDG-T------------
> str35: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--V----N--------L---------T------------T-----G-T-Q--LP-------P-------A----------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S-------------------------------
> str36: M---A----------N----------I----------------I------------N---------------------L-----W-NG----------------------------------------I---V----------PM-V------Q-----------D-----------------V-----------N------------------V---------A--S----------------I-----T-----A------F-K------S-----------------------------------------------------------------M-IDETWDK-------------------------------K----------I--E-AN-T----------C------IS----R------KH--------------RN----------
> str37: M--L-----------N------------R--------------IQ-------T-L-------MK-----TA-----N---------N---Y---------------E----T----------------I----E-----I-------LR-------------N-------YL-------------R-L-----------------------Y---I----------------------------IL----------A----------------R-------------------------------N--------------------------E---E----------------G-------RGIL-I-Y---D-------D----N---I------D---SV------------------------------------------------------
> str38: M---A------DP-----------A-----------------G---------T---NG----------E-------------------------------------E-------G----------T----------G-----------------C-------N----------GW--------------------------F---------Y--V----E----A-V--V----E------------------------------K---------------K------------------------------T------G---------D-----A----I------S-------D----------------D-----------EN------E--ND---S--------D--T-----------------G--E------D-L--------V-D--
> str39: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--V----N--------L-------------R--------T-R-----T-Q--LP-------P----------S-------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H----S-------------------------------
> str40: M--------------------------E-----------------SL--VP------G-F-----N--E--------------K--------------------T----H---------V---------------Q-----------L--S----------L-----------------P---V---LQ-------------------------V-------------------------C------D-----V-L-----V-----------R-G------F------G-----D----S--------V----------------------E---E--V----------------L-----------------S---------E---------A--------------------------RQ------H-------L-KDG-T------------
> str41: M--------------N-----------------------N----Q---------------RK-K-----TA-----------------------R--------P----S-------------FN--------------------M--L--------------------K----------------R-------------------AR--N----------R-----VSTV--S--------Q---L----------A--------K-------R--------F--------S-KG----L-------------------------------L-S-------------------GQ-------G--------------P-M--------------------------K---L-----------------------V------------MAF------
> str42: M--------S-----NF---D---A-I-R-AL---------V-----------D---------------T-----------D---------------A---------------Y--K---L---------------G-HI-H--M-------------------------Y--------P----------E---------G-T----------------E---------------Y--V------LS----------N-----F------T-------D--------R-G-S--------------------------R------I------E--------------------G-----------------V---T------------H-T----------V-----------------H------------------------------------
> str43: M-------I------------------E---L----------------------------R----------H----------------------------------E------------V---------------QGD---------L---------V---------T----I-------N--VV-----E---T-------------P----------E---------------------------D-------L--DG---F---------R----D---FI---R----A--------------H-----------------------L--------I-------C-------L-A------------VD--T--------E-----T------T------GL---D-----I-------Y--------------------------------
> str44: MF----------------V------------------F--------L--V----L-----------------------L---P-------------L-V---------S------------S-------------Q------------------C--VM-PL-F-----N-LI--------T------------TN--------Q--------S---------------------Y---T-----------------N----SF------T--R-G---------V------------Y---------------------------Y-PD----------------K----V-----------------FR---S------------S-------------V---L-------------H------------------------------------
> str45: M--------SKD-----LV-----A---RQAL---M----T------A------------R-MK------A----------D-------F--------VFFL-----F-----------VL------W--KA--L-------S----L------------P----------------------V--------P-T-R-------------------------------------------CQ--I--D-M------A--------K---------------K-----------------LSA-----------------G----------------------------------------------------------------------------------------------------------------------------------------
> str46: M---A----S-------L-L------------K------------SL-----T-LF-----K--------------------------------R---------T-----R------------------D-----Q-------P----------------PL---------------A---------------------SG------------S-----------G-----G-----A------I---------R----GI----K----------H--------V----------------------I-I----V---------------L--------I----------------P----G---------D-S------------S-I-----------V----------T--------R--S-------------------R-----------
> str47: M------------R----V---------R-------------GI--L-------------R----NWQ----QWWI--------W-------------------T---S---L-G-------F----W----------------MF------------MI----C----------S-------VV---------------G--------N-------LW-------V-TV-----Y--------------------------------------------------------------Y--------------------G--V-----P----------V----W-K------------E----------------------------------A-----------K-----T------------------------------T------------
> str48: M---A-------------V--------E----------------------P----F--------------------------P-----------RR-------P------------------------I-----------T-------R-----------P----------------------------H---------------A-------S-I---E------V--------------------D--T-----------S-G-I--------G-------------G-SA-G-----S--SE------K---VFC-------------L--------I------------GQ---AE--G----G----------------E------P---N-T---V------------------------------------------------------
> str49: MF------------Y---------AH----A------F----G--------------GY-----D---E-------N-LH-----------------A-F---P----------G-------------I-------------S-------ST-----V-------------------A--N-DV-R-----K-------------------Y-SV-----------VS-V-----Y---------------------N-------K---------------K----------------Y------N--IV-K-N--------------------------------K---Y----------------------------M---W------------------------------------------------------------------------
> str50: M---A----------N------------------------------------------Y------------------S-----K-------------------P---F----L-------L--------D---------I------V----------------F-----N------K-----D---I----K------------------------------------------------C---I------------ND---S------C--S---H--------------S---D---------------------CR-------YQ-----S---N---------S--YV-------E----L-----R---------------R--------N--QA-----L--------N-------------K----------------N---------L
> 
> example file name: 'protein_n050k050.txt'
> best objective: 456
> best bound: 0.0
> wall time: 0.24s
> ```
