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
Model = scsp.model.la_sw.Model
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
> --- Solution (of length 68) ---
>  Sol: itkgonjikqefoulcinbvahmpxxyczgobrddnbcsohvstuqpgoxrzvxinpnpsglsbpfxf
> str1: -tkg-n--k----u-------hmpx----------n----h--t-q-g-x-zvxi----s--------
> str2: i---o-ji-q-fo-l--nb-----xx-c-------------vs-uqp-----v-i----s--sb--xf
> str3: -------------ulcin--------yc--o-------so-v------o--z----p-p--l--p---
> str4: i--g------e--------va-------zg-brdd-bcs--v--------r-v--n-n--g----f--
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 68
> best bound: 0.0
> wall time: 0.028115s
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
> --- Solution (of length 111) ---
>  Sol: igenopbdevdaczfjtrvkgxdiypwxlqnfkrzoxulcinbdehprmpqlxxycodvgstnhodbftmuqipcsbvrogxqzbrpvxcdisgplnnbgsbwdehopfxf
> str1: ----------------t--kg---------n-k----u-------h--mp--x---------nh----t--q--------gx-z---vx--is------------------
> str2: i---o----------j-------i-----q-f---o--l--nb---------xx-c--v-s---------uq-p---v-------------is-------sb-------xf
> str3: -------------------------------------ulcin------------yco---s---o------------v-o---z--p-------pl-----------p---
> str4: ige------v-a-z------g---------------------b----r---------d-------db-------cs-vr--------v--------nn-g--------f--
> str5: -----p------------------yp--l----rz-xu-c------p-m-q-------vg-t---d-f--u-i----v-----------cd-s-----b-------o----
> str6: -----pbdevd-c-----v---d--p-----f--z-------------------------s--------m-----sb-ro--q----v----------b--b---h-----
> str7: --en--b-----czfjt-v--x----------------------e--r-----------------------------------zbr-v---i-gpl--------e------
> str8: -----------------r---x----wx-q--kr---------d---r---l---c-----t--od--tm---p----r-------p-x-------------wd-------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 111
> best bound: 0.0
> wall time: 0.229376s
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
> --- Solution (of length 153) ---
>   Sol: kprisxtkgenbqawxudsflcojignqfykzpehvalrdzxuhecoxpmqsabivglnbrtdpfxjulxctovdwozsiqbkxaenhtjmruzqpswbrfgvcihkdjosxqpmgzkvrstbvlnpahngqxbfiklmwwzceghnosuvdy
> str01: ------tkg-n-------------------k-----------uh-----m-------------p-x--------------------nht-----q------g---------x----z-v-------------x--i------------s----
> str02: ---i------------------oji--qf-----------------o----------lnb-----x---xc--v----s-------------u-qp------v-i-----s---------s-b---------x-f------------------
> str03: ----------------u---lc--i-n--y---------------co----s--------------------ov--oz-----------------p-----------------p----------l-p--------------------------
> str04: ---i----ge-------------------------va---z---------------g--br-d-----------d------b---------------------c------s-------vr---v-n---ng---f------------------
> str05: -p---------------------------y--p----lr-zxu--c--pmq----vg----td-f--u-----------i----------------------vc---d--s-----------b------------------------o-----
> str06: -p---------b-----d---------------e-v---d-----c---------v------dpf------------zs-----------m-----s-br---------o--q-----v---b----------b-----------h-------
> str07: ---------enb---------c---------z--------------------------------f-j----t-v---------x-e-----r-z----br--v-i----------g----------p----------l-----e---------
> str08: --r--x--------wx-----------q--k-------rd--------------------r-------l-cto-d-------------t-m----p---r-------------p------------------x------w-----------d-
> str09: k------k----qa-----f----ig-q--------------------------------------j--------wo-----k-----------------------k---s------k-r--b-l-----g----------------------
> str10: --------------------l--------------------x-----xp---abiv---b-------------v---z----k--------------------------o------z------------------------z--------vd-
> str11: k-ri---------------f-------------------------------sa--v--n-----------c---d-----q----------------w-------h----------z-------------------------c----------
> str12: ------------qa-xud-------g-q-------v--------------q-------------------c--------------e-----------wb-fg--i---jo-----------------------------ww-----------y
> str13: --r-sx------q----------j--n-f---p---a--d--------------i------------u----------siqb---e-------z-----------hk--o------------------h---------m-----g--------
> str14: ---i----------w---s---------------hv-------h-co--m----i------------u-----vd--------------------------------d------m--------------------------------------
> str15: ----------------------------------h--------------------------t---x---x----------q--------j---zq---b----c-----------------tb----a--------k---------n------
> str16: -----x----------u-sf-c------f--zpe----------ec---------v-------------------w--------a-n-t-----------f-------------mg---------------q---------z-------u---
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 153
> best bound: 0.0
> wall time: 1.519552s
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
> --- Solution (of length 31) ---
>   Sol: abdcbacdbeecdaebdecbaddacebddee
> str01: --dcb-c----cd--b--c-----ce-----
> str02: -bd----dbee---e--e-b-d---------
> str03: ---c-acd-eec--eb-e-------------
> str04: a--------e--d---d----dd--ebdd--
> str05: a--cb----eec-a-b--c------e-----
> str06: -b--ba--be-----bd-cba----------
> str07: -b--ba---e---aeb----ad-a-------
> str08: ---------ee---e--ecb-d----b--ee
> str09: ---c--cd-ee-da--d-c--d---------
> str10: -bd--a--b---d--b-e--a--a---d---
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 31
> best bound: 0.0
> wall time: 0.007011s
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
> --- Solution (of length 36) ---
>   Sol: dacebdacebdabceaedcbadeabcdebceaabcd
> str01: d-c-b--c-----c---d-b-----c---ce-----
> str02: ----bd----d-b-e-e-----e----eb------d
> str03: --c---ac--d---e-e-c---e-b--e--------
> str04: -a-e-d----d------d---de-b-d--------d
> str05: -ac-b---e-----e---c-a---bc-e--------
> str06: ----b----b-ab-e----b-d---c--b--a----
> str07: ----b----b-a--eae--bad-a------------
> str08: ---e----e-----e-e-cb-d--b--e--e-----
> str09: --c----c--d---e-ed--ad---cd---------
> str10: ----bda--bd-b-ea----ad--------------
> str11: ---e-d--e-da---a----a-ea-------a----
> str12: -a----a-e--a---a---b--e----e---a--c-
> str13: ---e--a----abc-a--c------cd-b-------
> str14: ----bd--e-----ea-d----ea--de--------
> str15: --c---a-e-da-----d----e----e--e----d
> str16: ---eb--c---a-----d-ba---b---b-e-----
> str17: d----d-ce-----ea---b-dea------------
> str18: da--b--c--d------d----ea---e-c------
> str19: -a----a---d--ce-ed--a--ab-----------
> str20: -a-e----e----c----c---e----e--eaa---
> str21: ----b----bda--e---c-a--a--de--------
> str22: dace-da-e-dab-----------------------
> str23: -a----a-e--ab------b----b---bce-----
> str24: d--e-d---b---c-----b-----c-----aab--
> str25: d---bda----a--e----b----bc--b-------
> str26: d--eb---e-d-b-e----ba----c----------
> str27: --ce----eb---c---dcb-de-------------
> str28: d---b---e-da---a-d--a--ab-----------
> str29: --c----c-----c---dcb--e-b-d--c------
> str30: -a-e----e--a-c---d-b-----c--b------d
> str31: dac-b---e--a-c----c------cd---------
> str32: ---e---ceb---c----c--d--b-d-b-------
> str33: d----d---b--bce--d--a---b---b-------
> str34: -a----a-e--ab--a----a-e-b------a----
> str35: ---e---c-b--bc-a----ad---cd---------
> str36: d--eb--c-----ce---c--d--bc----------
> str37: da----ac-b-a--e-e--b-----c----------
> str38: -a---da--b----ea----a----c---ce-----
> str39: da-e---c--d-b--a--c-a--a------------
> str40: dac-b----bd--ce--dc-----------------
> str41: d--e-d---b----e-e--b----b-de--------
> str42: --c--da---d--c---dc--d-a-------a----
> str43: --ce----e-d--c-----ba-e----e-------d
> str44: --ce--a-e----c-a----a--a-c-----a----
> str45: d-c----c-----ce----b----b---b--a---d
> str46: ----b-a-e-----eae--b----b-de--------
> str47: d---bd--eb-a-c----c--d--b-----------
> str48: ---eb--c-b----e-ed--a-ea------------
> str49: -a-e----e-----e----b----b-d-bc-a----
> str50: d---bda--b---ce---cb----b-----------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 36
> best bound: 0.0
> wall time: 0.048946s
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
> --- Solution (of length 26) ---
>   Sol: TCATACCGGGATATCGATCGTAAACT
> str01: --AT---GGGATA-CG----------
> str02: --ATACC----T-TC---C-----C-
> str03: -CA--C-G--A-AT---T-G-A----
> str04: T-A-A-----A-ATC--T-GT-----
> str05: --A----GG--TA---A-C--AAA--
> str06: T--T-CC----TA--G---GTA----
> str07: T--T---G---TA--GATC-T-----
> str08: T------GGGA-A--G-T--T---C-
> str09: T--T-CC---A---C-A----A--CT
> str10: TC-TA-----A-A-CGA----A----
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 26
> best bound: 0.0
> wall time: 0.003872s
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
> --- Solution (of length 139) ---
>   Sol: ATGAGCTCAGCTAGATCGATAGCATCATGTGCATCTACGTAGCGTAGATCATGACACTGTCAGTAGCTACAGATCTGAACTAGTCGAGTCATAGTCATGCACTGACTAGTTCGACGTCATCGATGACCTGAGACTCGAR
> str01: -T-AG-T-AG-TAGA-C--T--C--C--G-G-A---A-GT-G---A---CA--A-AC---C-----CT---GA----AA--AG---A---AT-G----G-A-T-A--A-----A--T-AT--A----------------
> str02: --G-G---A--TA-A---A---CA-C-T---C--C--CG-A----A-A--AT-A-A-T-T---T-G--AC---T-T-AA--A--C-A---A----C--GC---GAC-AGTTC-A----A--G-----------------
> str03: AT-A-C-C---T---TC-----C-T-A-G-G--T--A---A-C--A-A--A---C-C----A--A-C--CA-A-CT----T--T----T----G--AT-C--T--CT--T--G---T-A--GAT--C-TG---------
> str04: -T-A----A---A--T---TA---T-A-----ATCT---TA---TA---C-T-A----GT-A--A---A-A-A----A--TAG--G-GT----GT-A---AC---C--G----A----A---A--AC--G-G--TC---
> str05: -T----T-A---A-A---A---CA----G--C--CT--GT-G-G--G-T--TG-CAC---C-----C-AC---TC--A-C-AG--G-G-C-----C---CACTG----G---G-CG-CA---A-G--------------
> str06: ATGA-CT----T----C-----CA--ATG-G-ATC--C----C--A-A-C----C--T--CA--AGCT-----TC----C-A--C----C-----C---CA---A-T-G---G---T--T---T--C---AG-C-----
> str07: A--A-C--A---A-A-C-----CA--A----C--C-A---A-C-T---T--T-----TG--A-T--CT-C---T-TG---TAG---A-TC-T-GT--T-C--T--CTA-----A----A-CGA--AC------------
> str08: ATGA----A---A-A-CGA-A--A--AT-T--AT-TA--T--C--A-A----G-----G---GTA--T---G----GAA---GT-G-G--A-AG-C-TG-AC-GA--A-----A--T----------------------
> str09: A----CTC-G---G--C--T-GCAT---G--C-T-TA-GT-GC--A---C-T--CAC-G-CAGTA--TA-A--T-T-AA-TA----A--C-TA---AT----T-A----------------------------------
> str10: -T----T--G-TAGATC--T-G--T--T---C-TCTA---A----A---C--GA-ACT-T---TA---A-A-ATCTG---T-GT-G-G-C-T-GTCA--C--T--C---------------------------------
> str11: --G--C--AG--AG--C-AT----T--T-T-C-T--A---A---TA--TC----CAC----A--A---A-A--T--GAA---G--G---CA-A-T-A---A-T---T-GT---AC-T-A-C--T--C------------
> str12: ATGAGC-CA---AGATC-----C-----G---A-C---G-A----AGA----G-C-C---C-----C-A-AG----GA----G--GAG--A-AG----G-A--G----G---GAC--C--C-----CC-----------
> str13: -T---CTCA-C-AG-T---T--CA--A-G---A---AC----C------CA--A-A--GT-A----C--C----C----C----C----CATAG-C---C-CT--CT--T---A----A---A-G-CC--A--C-----
> str14: A-G-G-T----T---T--ATA-C--C-T-T-C--CTA-G--G--TA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TA-------------------------------
> str15: A-G-G-T----T---T--ATA-C--C-T-T-C--C--C--AG-GTA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TA-------------------------------
> str16: -T-A----A---A-A-C-A-A-C-TCA-----AT--AC--A----A---CAT-A-A--G--A--A---A-A--TC--AAC--G-C-A---A-A---A---AC--ACT----C-AC---A---A--A-------------
> str17: -----C-C-GC-----C-----CAT--T-TG-------G--GCG--G--C-T--C--T--C-G-AGC----GAT---A----G-C---TC---GTC--G-A---A-T----C--C--C-TCGA---CCT----------
> str18: AT-A-C-C---T---TC-----C--CA-G-G--T--A---A-C--A-A--A---C-C----A--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TAG----A--TC-T-G-----------------
> str19: -T---CTCA-C-AG-T---T--CA--A-G---A---AC----C-T----CA--A----GTC--T--C--C----C----C----C-A-T-A--G----GC-CT--CT--TTC-A-GTCA--G-----------------
> str20: --GA--TC---T----C--T--C-TCA----C--C---G-A----A---C----C--TG---G---C--C----C----C--G--G-G-CA-A---ATGC-C---CTA-----A--TC--C-A-GA---G-G--T-G--
> str21: A-GAGC--A---A--TC-A--G--T---G--CATC-A-G-A----A-AT-AT-AC-CT---A-T---TA----T---A-C-A--C---T--T--T---GC--T-A--AG----A----AT-------------------
> str22: A--A--T----TA-A---A-A-CATC-T---CA---A--TA-C--A-A-CAT-A-A--G--A--A---A-A-A-C--AAC--G-C-A---A-A---A---AC--ACT----C-A--T----------------------
> str23: A--A----A-C--GA---A---C-T--T-T--A---A---A----A--TC-TG----TGT--G--GCT---G-TC--A-CT---CG-G-C-T-G-CATGC--T---TAGT--G-C------------------------
> str24: AT-A----A-CTA-AT---TA-C-T---GT-C------GT----T-GA-CA-G-----G--A----C-AC-GA---G---TA----A--C-T---C--G---T--CTA-T-C----T--TC--TG--------------
> str25: ATGAG-T--G-T----C-A---C-----G---A---A--T----T----CA---C---GT-A----C-A-A--T--GAACT-G--GA-T----GT--T-CAC-G--T-G---GA----AT--A--A-------------
> str26: A----C-C-G-T-G---G---GC-----G---A-----G---CG--G-T---GAC-C-G---GT-G-T-C---T-T---C----C---T-A--GT---G----G----GT-C--C--CA-CG-T----TGA-A-----R
> str27: A--A----AG---G-T---T----T-AT----A-C--C-T----T----C----C-C----AG--G-TA-A---C--AA--A--C----CA-A--C---CA---ACT--TTCGA--TC-TC--T----TG---------
> str28: A-G---T-AG-T---TCG----C--C-TGTG--T----G-AGC-T-GA-CA--A-ACT-T-AGTAG-T---G-T-T----T-GT-GAG-----G--AT----T-A----------------------------------
> str29: -T----T----TA--T--A---C--C-T-T-C--CTA-G--G--TA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TAG----A--T----------------------
> str30: ATG--C---G---G-TCG-T--C-TC-T---C--C--C----CG--G--C-T-----T-T---T---T-----T-T---C----C----C-----C--GC---G-C-----CG-CGT--T-G--G-C--G---C-CGA-
> str31: --G---T--G--A---C-A-A--A--A-----A-C-A--TA----A--T---G-----G--A----CT-C----C--AAC-A--C----CAT-GTCA---A--G-CT--TTC-A-G-----G-T-A---GA--C-----
> str32: --G---T--G-TA-A--GA-A--A-CA-GT--A---A-G---C------C----C---G---G-A---A--G-T--G-----GT-G--T--T--T--TGC---GA-T--TTCGA-G-----G----CC-G-G-------
> str33: --GAG---A---A--T-GA--G--TC-T---CAT-TAC----CG-----C----C-C-G---GTA-CT-----T---A----G-C-A---A--G-C-T--A---A-TAGT-C-ACG-----G----C------------
> str34: ATG---T--G---G-TCGAT-GC--CATG-G-A-----G--GC------C----CAC---CAGT---T-CA--T-T-AA---G--G---C-T---C---C--TG----G--C-A--T--T-------------------
> str35: A----C---G--AG--CG-T----T--T-T--A---A-G--G-G-----C----C-C-G-C-G-A-CT---G--C-GA-C--G--G---C-----CA--CA-TG----G--C--C--C-T-G-T-A--TG----T----
> str36: --G-G-T----T---T--ATA-C--C-T-T-C--C--C--AG-GTA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TAG------------------------------
> str37: -TG-G----G--A-A--G-T----TC-----CA---A---A----AGATCA---CA-----A--A---ACA---CT-A-C----C-AGTCA-A--C---C--TGA--AGT---AC---A-C------------------
> str38: --GA----AGC--G-T---TA--A-C--GTG--T-T--G-AG-G-A-A--A--A----G--A----C-A--G--CT----TAG--GAG--A-A--CA---A--GA---G--C----T----G--G----G---------
> str39: A----C-CAGC--G--C-A---C-T--T---C------G--GC--AG--C--G-----G-CAG---C-AC----CT---C--G--G---CA--G-CA--C-CT--C-AG--C-A-G-CA---A---C------------
> str40: ATG-G----G--A---C-A-A-C-T--T----AT-T-C----C-TA--TCATG----TG-C-----C-A-AGA---G-----GT----T--T--T-A--C-C---C--G---G---T----GA---CC--A--------
> str41: -T----T--G-TAGATC--T-G--T--T---C-TCTA---A----A---C--GA-ACT-T---TA---A-A-ATCTG---T-GT-G-GT--T-GTCA--C--T--C---------------------------------
> str42: A--A-C-CA---A---C-----CA--A----C-T-T---T--CG-A--TC-T--C--T-T--GTAG--A----TCTG---T--TC---TC-TA---A---AC-GA--A---C----T--T---T-A-------------
> str43: --G-G----G-T---TC--T-GC--CA-G-GCAT--A-GT--C-T---T--T-----T-T---T---T-C---T--G-----G-CG-G-C-----C---C--T---T-GT--G---T-A---A--ACCTG---------
> str44: --G-GCT--GC-A--T-G----C-T--T----A-----GT-GC--A---C-T--CAC-G-CAGTA--TA-A--T-T-AA-TA----A--C-TA---AT----T-ACT-GT-----------------------------
> str45: -TG--C--A--T-G--C--T----T-A-GTGCA-CT-C--A-CG-----CA-G----T---A-TA---A----T-T-AA-TA----A--C-TA---AT----T-ACT-GT-CG---T----------------------
> str46: -T----TC--C-A---C-A-A-C-T--T-T-C--C-AC----C--A-A----G-C--T--C--T-GC-A-AGATC----C----C-AG--A--GTCA-G----G----G---G-C--C-T-G-T---------------
> str47: -T---CT-A---A-A-CGA-A-C-T--T-T--A---A---A----A--TC-TG----TGT--G--GCT---G-TC--A-CT---CG-G-C-T-G-CATGC--T---TAG------------------------------
> str48: A----C-C-G---GAT-G---GC--C--G--C------G-A---T---T--T-----T-TC-G--G--A--G-TC----CT--T-G-G-----G----G----GAC-----C-AC-TCA--GA--A--T-AGA------
> str49: -----CT----T-G-T--A--G-ATC-TGT---TCT-C-TA----A-A-C--GA-ACT-T---TA---A-A-ATCTG---T-GT-G-G-C-T-GTCA--C--T------------------------------------
> str50: ATGAGC--A-CTA-A--G----C-----G---A---A-G-A----A---C----CA-----A--A---A-AG--C--A----G---A--CA-A-T-A--CA---AC-----C--CG-C-T--AT----T-A--C-----
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 139
> best bound: 0.0
> wall time: 0.101224s
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
> --- Solution (of length 51) ---
>   Sol: MEQSKAFPLSVRNYAEQHAFGLVNDTAICPGERKFSLRNGAHPDELTVQYQ
> str01: M----A--LS---Y--------------CP---K-----G------T----
> str02: M-QS-----S-----------L-N--AI-P-----------------V---
> str03: M------PLS---Y--QH-F------------RK-----------------
> str04: ME-------------E-H----VN-------E----L----H-D-------
> str05: M--S--------N------F----D-AI----R-------A----L-----
> str06: M-----F----RN---Q------N-----------S-RNG-----------
> str07: M-----F------YA--HAFG---------G------------------Y-
> str08: M--SK-F------------------T------R----R----P------YQ
> str09: M--S--F---V---A-----G-V--TA---------------------Q--
> str10: ME-S----L-V------------------PG---F---N-----E------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 51
> best bound: 0.0
> wall time: 0.100373s
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
> --- Solution (of length 419) ---
>   Sol: MAFVEFSLVLLNPLVSGKFDNSQCREVKNPLAIRTHVEQLFRSTAQKLPYGITVLQVRDSMPLFDANLGHIERTWQAVLSFKPYTDNEGIVSFTAQNLRGCFVYDENTKLGDHQISAVYPMELDKTNSIWAGFLPTQREKGIVLARSNQDEHYKLVEAGRVFSTAIQNLKGVDSETMANYPGDIKTSVRHQLEFSAKITQLPRADFGYSLERVCKTNGSLPDVHKLYGQAFINRDGSWAEDFLTIKHVMRAYIDEGPNWTSLERQHGPAIFVLYWMDKSICRLFETASHCVLPSGNKYFDMICLPRDSNAIVGYQPTDLRSIEVAGKNSFLWVNTRAIPDEGVNCHKLFIYAPGERVQEDLSMFFRWTKYGCVPSNIVELRGDHNMQATWKELRYSANDIKGTLVQRHFSAIGNLPTVY
> str01: M-----------------------R----------H---L--------------------------N---I--------------D---I---------------E-T----------Y--------S------------------SN-D---------------I---K--------N--G-----V-------------------Y------K-----------Y--A----D---AEDF------------E--------------I--L---------LF--A----------Y---------S--I------D-------G---------------G------------E-V-E------------C-------L--D---------L---------T---R------------
> str02: M---E-------------------R--------R----------A------------------------H--RT--------------------------------------HQ------------N--W-------------------D-------A-----T-----K----------P-------R---E---------R--------R--K-------------Q--------------T--------------------QH---------------RL--T--H---P------D------DS--I--Y-P---R-IE---K---------A---EG-------------R------------K---------E---DH-----------------G-----------------
> str03: M---E-------P---G--------------A--------F-STA--L---------------FDA-L--------------------------------C---D------D--I-------L----------------------------H-------R----------------------------R--LE-S----QL-R--FG----------G----V-----Q--I------------------------P----------P----------------E-----V--S-----D----PR-----V-Y----------AG------------------------YA--------L------------------L---------------------------------------
> str04: M---------------GKF------------------------------Y---------------------------------Y-------S----N-R--------------------------------------R-----LA----------V-----F--A-Q----------A------------Q---S-------R--------------------H-L-G-------GS--------------Y--E---------Q---------W-------L---A--CV--SG----D-------S-A-------------------F-----RA---E-V---K----A---RVQ----------K-------------D------------------------------------
> str05: --F--F------------------RE--N-LA--------F----Q---------Q------------G------------K------------A---R------E--------------------------F-P-----------S---E-----EA-R----A--N-----S------P----TS-R---E-------L------------------------------------W---------V-R-------------R--G---------------------------GN--------P-------------L-S-E-AG----------A---E--------------R---------R----G-----------------T------------------------------
> str06: M------------------D---------P------------S----L----T--QV-----------------W-AV---------EG--S----------V------L-----SA-------------A-----------V------D-------------TA---------ET--N---D--T------E--------P--D-----E------G-L----------------S-AE-----------------N----E---G-----------------ET-------------------R----I----------I-------------R-I-----------------------------T--G---S--------------------------------------------
> str07: MAF----------------D--------------------F-S----------V-------------------T--------------G-------N----------TKL-D-------------T-S---GF--TQ---G-V---S---------------S-------------M--------T-V-------A-------A--G--------T---L-----------I------A-D-L----V-----------------------------K-------TAS-----S--------------------Q---L---------------T--------N---L---A-----Q---S---------------------------------------------------------
> str08: MA-V----------------------------I------L--------P----------S-------------T---------YTD--G----TA---------------------A------------------------------------------------------------------------------------------------C-TNGS-PDV------------------------V-------G---T------G------------------T--------------M------------------------------WVNT--I---------L----PG-----D---FF-WT-----PS------G---------E---S--------V-R----------V-
> str09: M----------N----------------------T---------------GI------------------I--------------D-----------L---F--D-N-----H----V-----D---SI-----PT-----I-L------------------------------------P--------HQL---A--T-L---D--Y-L--V--------------------R---------TI-------IDE--N-----R--------------S-----------VL-----------L-------------------------F---------------H---I------------M-------G---S------G-------------------------------------
> str10: M-FV-F-LVLL-PLVS-----SQC--V-N-L--RT------R-T-Q-LP------------P---A-----------------YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M------------------D-S-----K---------E-----T-------I--L---------------IE-----------------I------------------------I----P----K---I----------K------S-----Y-L-------------L---D--T--N----I--S--------------P------------K---S-------Y-----N-D------F--I---------------S--R-------------------------------NK-----------N-I------------------F--V----I-----N---L--Y------------------------N-V-----------------S------T--------I-------
> str12: M------L-L-----SGK---------K------------------K-------------M-L----L-----------------DN----------------Y-E-T--------A-------------A-------------AR------------GR----------G----------GD---------E---------R--------R---------------------R-G-WA--F-----------D---------R---PAI-V-------------T----------K--------RD-------------------K-S----------D---------------R------M------------------------A-------------------H-----------
> str13: M----------N----G--------E-----------E--------------------D-----D-N----E---QA-----------------A---------------------A----E--------------Q-----------Q--------------T-----K--------------K----------AK-----R-------E---K-----P---K---QA---R-----------K-V-----------TS-E-----A-----W---------E---H---------FD---------A------TD---------------------D-G---------A--E----------------C------------------K----------------H-----------
> str14: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S-V---E----------------E---VL--S---E------A-R------Q----------------------H-L----K-------D-G--------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-----------------------R------------------------Y-I-V-----S-P-------------Q--L-----------V------L---------------Q---V-------------G-------KG-------Q-E----VE--R----A---L----------Y-----------L------T--P-----Y-------------D----Y----I--D----E-----K--------------S------P-I---Y-----------------------YF----L-R-S-------------------------------------H-L---------------------------NI---------Q------R---------------------P---
> str16: M-----------P-----------R-V--P------V------------Y--------DS-P-------------Q-V-S--P---N------T--------V----------------P----------------Q-------AR--------L--A-----T----------------P-----S------F-A--T--P-------------T--------------F--R-G--A-D---------A-----P-----------A-F-------------------------------------------Q--D----------------T-A------N-------------Q----------------------------QA-----R-----------Q-------------
> str17: M-FV-F-LVLL-PLVS-----SQC--V-N-L--RT------R-T-Q-LP-----L----------A-----------------YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FV-F------------F-------V---L--------L--------P-----L-V--S-------------------S---------------Q----C-V---N--L---------------T---------T-R-------------------------T--Q-L-----------P--------------------P-A---Y-------TN-S-----------F------------T-----R-----G---------------V-Y-----------------------Y------P-D-------------------K-----V---------------F------R-----S------------S--V-L---H-----------S-----------------------
> str19: M---E--------------------------AI------------------I-------S---F-A--G-I-----------------GI------N------Y----K---------------K--------L--Q---------S------KL-----------Q----------------------H--------------DFG----RV------L----K----A------------LT---V-----------T--------A------------R----A----LP-G-------------------QP----------K------------------H---I-A------------------------I---R-----Q--------------------------------
> str20: MA----S--------SG------------P-------E---R--A--------------------------E----------------------------------------HQI-------------I----LP---E-------S----H--L-------S----------S------P----------L--------------------V-K--------HKL----------------L--------Y---------------------YW--K----L--T--------G--------LP-------------L-------------------PDE---C--------------D---F------------------DH--------L------I-------------------
> str21: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S-V---E----------------E---VL--S---E----V---R------Q----------------------H-L----K-------D-G--------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L-----------------------A----------------P----------S-P----N------------S-K-------I-----Q-L---F----N-------------------N-I------------------N-----------------I------D----------I--------------------------------N---------Y------------E------H------------T-L-----------Y---------F--AS--V--S---------------A----Q------------NSF------------------F--A-----Q--------W-----V----V----------------YSA-D-K---------AI-------
> str23: M-----S------------------------AI-T--E-----T--K-P---T-----------------IE------L---P-----------A--L------------------A----E---------GF---QR--------------Y--------------N-K-----T----PG-----------F----T--------------C--------V--L--------D--------------R-Y-D-----------HG----V-------I---------------N---D-------S------------------K----------I----V----L--Y------------------------N-------------------------------------------
> str24: M----------------K--N-----------I-----------A--------------------------E--------FK--------------------------K-------A--P-EL-------A-------EK---L----------L-E---VFS----NLKG-------N-------S-R-----S-----L---D---------------P---------------------------MRA----G---------------------K----------H----------D-----------V-----------V--------V----I--E--------------------S-----TK---------------------K-L--------------------------
> str25: M-----------P---------Q------PL---------------K--------Q---S--L-D----------Q---S-K-----------------------------------------------W---L---RE-----A-----E--K-----------------------------------H-L----------RA-----LE-------SL--V-----------D-S--------------------N---LE---------------------E-------------------------------------E---K---L---------------K-----P----Q--LSM-------G-------E---D---------------------VQ---S---------
> str26: M-FV-F-LVLL-PLVS-----SQC--V-N-L-I-T------R-T-Q-------------S-----------------------YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S------T--------------------Q-----------D----------------------------------------------------------------------------------------------------------------------------------------------
> str27: M----------------KFD------V---L-----------S----L---------------F-A----------------P----------------------------------------------WA--------K--V------DE---------------Q-------E----Y--D-------Q--------QL---------------N---------------N------------------------N---LE---------------SI-----TA-----P---K-FD------D-----G-----------A---------T-----E--------I----E------S----------------E-RGD----------------I-------------------
> str28: M-FV-F-LVLL-PLVS-----SQC--V-N-----------F--T----------------------N-----RT-Q--L---P--------S--A--------Y---T------------------NS----F--T-R--G-V---------Y--------------------------YP-D-K--V-----F--------R-----S---------S---V--L--------------------H-------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-------------------------------------------------------------------------W----S---------I------------------------I--V----L-K--------L-------I----S------------------IQ-------------P----------L--------L--------L--V--T--SLP----LY-----N-----------------------PN-----------------MD-S-C--------C-L---------I-----S-----------R-I------------T---P-E------L---A-G--------------K----------L--------TW---------I--------F--I-------
> str30: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S-V---E----------------E----------------------F------L----SE--A----------R-Q--------------------------------H-L-------------------K-------D-G---T---------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FV-F-LVLL-PLVS-----SQC--V---------------------------------MPLF--NL--I--T----------T--------T-Q-------------------S--Y------TN-----F--T-R--G-V---------Y--------------------------YP-D-K--V-----F--------R-----S---------S---V--L--------------------H--------------L-------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M----------------------------------H--Q------------ITV--V--S--------G-------------P-T--E--VS-T------CF--------G----S------L----------------------------H----------------------------P------------F-----Q--------SL----K-----P-V-------------------------M-A------N----------A---L---------------------G----------------V------L---E--GK-----------------------------------MF-------C--S-I----G-------------------G----R--S----L----
> str33: MA--------------------------------T----L-------L---------R-S--L--A-L------------FK----------------R-------N-K--D------------K---------P---------------------------------------------P--I-TS-------------------G-S--------G---------G-A-I-R-G--------IKH-----I----------------I---------I----------V-P--------I--P-------G----D--S-------S--------I-----------------------------T--------------------T----R-S----------R------------
> str34: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S----ME----------------E---VL--S---E------A-R------Q----------------------H-L----K-------D-G--------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FV-F-LVLL-PLVS-----SQC--V-N-L---T--------T------G-T--Q------L-------------------P------------------------------------P----------A---------------------Y----------T---N-----S-------------------F----T---R---G-----V-------------Y------------------------Y----P-------------------DK------------V-------F------R-S------------S--V------L--------------H---------------S---------------------------------------------------------
> str36: MA---------N--------------------I------------------I--------------NL------W-----------N-GIV----------------------------PM---------------------V-----QD-----V-----------N---V-----A--------S----------IT----A-F--------K---S-----------------------------M---IDE----T--------------W-DK------------------K----I--------------------E-A--N------T---------C----I-----------S---R--K--------------H---------R---N---------------------
> str37: M------L---N------------R-------I-----Q----T---L------------M--------------------K--T---------A-N---------N-----------Y--E---T--I---------E--I-L-R-N----Y-L----R--------L----------Y---I-------------I--L--A-------R----N----------------------E--------------EG-------R--G--I--L------I-----------------Y-D------D-N-I------D--S--V-----------------------------------------------------------------------------------------------
> str38: MA-----------------D---------P-A------------------G-T-------------N-G--E---------------EG----T-----GC-----N---G------------------W--F-------------------Y--VEA--V----------V--E---------K-----------K-T-------G--------------D-------A-I----S---D------------DE--N----E--------------------------------N---D-------S---------D----------------T------G------------E----DL-----------V---------D------------------------------------
> str39: M-FV-F-LVLL-PLVS-----SQC--V-N-L--RT------R-T-Q-LP------------P-----------------S---YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQV-------------------------------------------C---D------------V----L-------------------V--R------------G--F--------G-DS-------------V----E-----------------E-V------L----------------S--E----------A------------RQH------L----K---------------------D------------G---T------------------------------------------------------------------------------------------------------
> str41: M----------N--------N-Q-R--K------------------K-----T------------A------R---------P--------SF---N-----------------------M-L-K------------R------AR-N-----------RV-ST-------V-S----------------QL---AK-----R--F--S-----K--G-L-----L----------S------------------G--------Q-GP-------M-K----L-------V---------M--------A-------------------F-----------------------------------------------------------------------------------------
> str42: M-----S----N------FD-----------AIR----------A--L-----V----D--------------T-----------D--------A--------Y----KLG-H-I------------------------------------H------------------------M--YP-----------E-------------G--------T-----------------------E-----------Y-------------------VL-----S----------------N--F-----------------TD-R-----G--S------R-I--EGV------------------------T---------------H----T---------------V--H-----------
> str43: M-------------------------------I----E-L-R---------------------------H-E-----V-----------------Q---G----D----L-------V-------T--I------------------N-------V----V-------------ET----P-----------E-----------D----L-----------D-----G--F--RD------F--I----RA--------------H------L------IC-L---A---V--------D----------------T-----E-----------T--------------------------------T--G--------L--D----------------I------------------Y
> str44: M-FV-F-LVLL-PLVS-----SQC--V---------------------------------MPLF--NL--I--T----------T-N--------Q-------------------S--Y------TNS----F--T-R--G-V---------Y--------------------------YP-D-K--V-----F--------R-----S---------S---V--L--------------------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-----S----------K-D----------L-----V-------A------------R-----------------QA-L-----------------------------------------M----T----A------R--------------------------------------M-------K----------A--------DF------V-----------------F----------FL---------------------------FVL-W--K--------A----L-S---------LP------V---PT--R------------------------C------------Q------------------I-----D--M-A--K---------K--L-----SA-G------
> str46: MA----SL-L-------K---S--------L---T----LF-----K----------R---------------T------------------------R-----D--------Q-----P--------------P--------LA-S-----------G---S-------G----------G-------------A-I----R---G------------------------I-------------KHV----I----------------I-VL------I------------P-G----D-------S------------SI-V----------TR-------------------------S---R-----------------------------------------------------
> str47: M-----------------------R-V------R----------------GI--L--R--------N-------WQ-------------------Q---------------------------------W-----------------------------------------------------------------------------------------------------------W------I-------------WTSL----G---F---WM-------F----------------MIC----S---V-----------V-G-N--LWV-T-------V-------Y------------------YG-VP---V-----------WKE----A---K-T-------------T--
> str48: MA-VE-------P-----F----------P---R-------R------P--IT----R---P-------H------A--S---------I---------------E-----------V-----D-T-S---G---------I----------------G-----------G--S---A---G----S-------S---------------E---K-------V-------F-------------------------------------------------C-L------------------I----------G-Q---------A---------------EG-----------GE------------------P-N------------T---------------V--------------
> str49: M-F----------------------------------------------Y---------------A---H------A---F-------G----------G---YDEN--L--H---A---------------F-P-----GI----S---------------ST-------V-----AN---D----VR-------K----------YS---V---------V-------------S----------V---Y-----N-------------------K------------------KY----------N-IV--------------KN------------------K---Y-----------M---W----------------------------------------------------
> str50: MA---------N-------------------------------------Y---------S---------------------KP---------F----L-----------L-D--I--V--------------F--------------N-----K------------------D----------IK----------------------------C-----------------IN-D-S-------------------------------------------C------SH----S-----D--C--R-------YQ-----S------NS---------------------Y-----V-E-L----R--------------R---N-QA----L----N--K------------NL----
> 
> example file name: 'protein_n050k050.txt'
> best objective: 419
> best bound: 0.0
> wall time: 14.667506s
> ```
