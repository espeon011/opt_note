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
Model = scsp.model.linear2_cpsat.Model
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
> --- Solution (of length 63) ---
>  Sol: tkiognkuhmpelvjciqfoalxnhtzqgbxyrxddbcosovoszruqpvpnxnlipgssbxf
> str1: tk--gnkuhmp-----------xnht-qg-x-------------z----v--x--i--s----
> str2: --io----------j-iqfo-l-n-----bx--x---c---v-s--uqpv-----i--ssbxf
> str3: -------u----l--ci------n-------y-----cosovo-z---p-p---l-p------
> str4: --i-g------e-v------a-----z-gb--r-ddbc-s-v---r---v-n-n---g----f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 63
> best bound: 45.0
> wall time: 60.412583s
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
> --- Solution (of length 109) ---
>  Sol: igeprxwyvazojinplxqgkbrczxfuodrlcinpjtodtbvxxmqycevorsgotdcvfuozqipbrvkigcdplnkufzshmspxnbrhtoqgexzvfxisbwdbh
> str1: -------------------------------------t--------------------------------k-g----nku---hm-pxn--ht-qg-xzv-xis-----
> str2: i----------oji----q-------f-o--l--n------b-xx---c-v--s-------u--q-p--v-i----------s--s---b-------x--f--------
> str3: ---------------------------u---lcin------------yc--o-s-o---v--oz--p--------pl---------p----------------------
> str4: ige-----vaz--------g-br------d---------d-b------c----s-----v--------rv-------n----------n------g----f--------
> str5: ---p---y-------pl-----r-zx-u----c--p---------mq---v---g-td--fu---i---v---cd-------s------b---o---------------
> str6: ---p-----------------b-------d-------------------ev------dcv--------------dp----fzs-ms---br--oq----v----b--bh
> str7: --e-----------n------b-cz-f---------jt----vx-----e--r----------z---brv-ig--pl-------------------e------------
> str8: ----rxw----------xq-k-r------drlc----todt----m--------------------p-r------p-----------x-----------------wd--
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 109
> best bound: 28.0
> wall time: 60.813588s
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
> --- Solution (of length 167) ---
>   Sol: tprxqyisapbowdklegxqjnvkurziqsfdhoxplcuafgbcdzqvrinmbqdcpsmeaetlcxvwhxtbnyqfcjhvgoaznmtuqdgstkovizxjwqfmgepbuokrekwsizbddrbovqdhcspktvrvzbinoxswdnplaykihmsugnbxplhfeco
> str01: t-------------k--g---n-ku-------h------------------m----p--------x------n-----h-------t-q-g-------x------------------z------v----------------x---------i--s------------
> str02: ------i----o--------j------iq-f--o--l-------------n-b------------x---x------c--v-----------s----------------u----------------q----p--v----i---s-----------s---bx---f---
> str03: ------------------------u-----------lc-----------in----------------------y--c----o---------s--ov-------------o-------z------------p---------------pl------------p------
> str04: ------i----------g-----------------------------------------e------v---------------az------g----------------b---r-------dd-b-----cs---vrv---n-----n----------g------f---
> str05: -p---y---p-----l---------rz-------x---u----c------------p-m---------------q----vg-----t--d------------f-----u-------i-------v---c---------------d---------s---b-------o
> str06: -p--------b--d--e-----v--------d-----c---------v------d-p------------------f-------z-------s-----------m-----------s--b--r-o-q-------v---b--------------------b---h----
> str07: ----------------e----n--------------------bc-z-----------------------------f-j--------t--------v--x------e-----r-----zb--r--v-------------i-----------------g---pl--e--
> str08: --rx--------w-----xq---k-r-----d----------------r--------------lc-----t----------o-------d--t----------m--p----r------------------p----------x-wd----------------------
> str09: --------------k--------k----q----------af--------i------------------------------g-------q----------jw--------ok--k-s---------------k--r--b---------l--------g----------
> str10: ---------------l--x---------------xp---a--b------i----------------v----b-------v---z---------ko--z-------------------z------v-d----------------------------------------
> str11: --------------k----------r-i--f--------------------------s--a-----v-----n---c------------d-----------q------------w------------h--------z----------------------------c-
> str12: ----q---a---------x-----u------d---------g----qv-----q-c---e-------w---b---f----g---------------i--j---------o----w----------------------------w-----y-----------------
> str13: --r----s----------xqjn--------f----p---a----d----i-------------------------------------u---s----i----q-----b----e----z---------h---k--------o-----------hm--g----------
> str14: ------i-----w----------------s--h--------------v--------------------h-------c----o---m----------i-----------u---------------v-d-----------------d--------m-------------
> str15: --------------------------------h-----------------------------t--x---x----q--j-----z----q------------------b--------------------c---t----b----------a-k------n---------
> str16: ---x--------------------u----sf------c--f----z----------p--e-e--c-vw--------------a-n-t---------------fmg--------------------q----------z------------------u-----------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 167
> best bound: 17.0
> wall time: 62.86025s
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
> --- Solution (of length 28) ---
>   Sol: dcbbaceddbdeeecabdbecbadcaed
> str01: dcb--c--------c--db-c---c-e-
> str02: --b----ddb-eee-----e-b-d----
> str03: -c--ac-d---ee-c----e-b----e-
> str04: ----a-edd-d------d-e-b-d---d
> str05: ----ac---b-ee-cab---c-----e-
> str06: --bba----b-e----bd--cba-----
> str07: --bba-e--------a---e-bad-a--
> str08: ------e----eeec-bdbe------e-
> str09: -c---c-d---ee----d----adc--d
> str10: --b----d-------abdbe--a--a-d
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 28
> best bound: 17.0
> wall time: 60.378224s
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
> --- Solution (of length 45) ---
>   Sol: baedecabedaacbecdbdabceadebbaeedbdacbedbacead
> str01: ---d-c-b----c--cdb---c-------------c-e-------
> str02: b--d-----d---be-------e--e---e--bd-----------
> str03: -----ca-----c---d-----e--e---------c-e-b--e--
> str04: -aed-----d------d-d---e---b----d-d-----------
> str05: -a---c-be-----ec---abce----------------------
> str06: b------b--a--be--bd--c----b-a----------------
> str07: b------b--a---e----a--e---b-a--d--a----------
> str08: --e-e---e-----ec-bd-b-e--e-------------------
> str09: -----c------c---d-----e--e-----d--a---d--c--d
> str10: b--d--ab-d---be----a---ad--------------------
> str11: --ede----daa-------a--ea----a----------------
> str12: -a----a-e-aa-be-------ea-----------c---------
> str13: --e---a---a--b-c---a-c-------------c--db-----
> str14: b--de---e-a-----d-----eade-------------------
> str15: -----ca-eda-----d-----e--e---e-d-------------
> str16: --e----b----c------a----d-b-a---b---be-------
> str17: ---d-----d--c-e-------ea--b----d-----e--a----
> str18: ---d--ab----c---d-d---ea-e---------c---------
> str19: -a----a--d--c-e-------e-d---a-----a-b--------
> str20: -ae-ec------c-e-------e--e--a-----a----------
> str21: b------b-da---ec---a---ade-------------------
> str22: ---d--a-----c-e-d--a--e-d---a---b------------
> str23: -a----a-e-a--b---b--b-----b--------c-e-------
> str24: ---de----d---b-c-b---c-a----a---b------------
> str25: ---d---b-daa--e--b--bc----b------------------
> str26: ---de--bed---be--b-a-c-----------------------
> str27: -----c--e-----e--b---c--d----------cb-d---e--
> str28: ---d---bedaa----d--a---a--b------------------
> str29: -----c------c--cd----c----b--e--bd-c---------
> str30: -ae-e-a-----c---db---c----b----d-------------
> str31: ---d--a-----cbe----a-c-------------c-----c--d
> str32: --e--c--e----b-c-----c--d-b----db------------
> str33: ---d-----d---b---b---ce-d---a---b---b--------
> str34: -a----a-e-a--b-----a---a-eb-a----------------
> str35: --e--c-b-----b-c---a---ad----------c--d------
> str36: ---de--b----c--c------e------------c--db-c---
> str37: ---d--a---a-cb-----a--e--eb--------c---------
> str38: -a-d--abe-aac--c------e----------------------
> str39: ---d--a-e---c---db-a-c-a----a----------------
> str40: ---d--a-----cb---bd--ce-d----------c---------
> str41: ---de----d---be-------e---bb---d-----e-------
> str42: -----c---da-----d----c--d----------c--d-a--a-
> str43: -----c--e-----e-d----c----b-aeed-------------
> str44: -----c--e-a---ec---a---a----a------c----a----
> str45: ---d-c------c--c------e---bb----b-a---d------
> str46: bae-e-a-e----b---bd---e----------------------
> str47: ---d---b-d----e--b-a-c-------------c--db-----
> str48: --e----b----cbe-------e-d---ae----a----------
> str49: -ae-e---e----b---bd-bc-a---------------------
> str50: ---d---b-da--b-c------e------------cb--b-----
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 45
> best bound: 2.0
> wall time: 65.93192s
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
> --- Solution (of length 24) ---
>   Sol: TCATGGACCTGAATCGAATCGTAC
> str01: --ATGG----GA-T--A--CG---
> str02: --AT--ACCT---TC----C---C
> str03: -CA----C--GAAT----T-G-A-
> str04: T-A---A----AATC---T-GT--
> str05: --A-GG---T-AA-C-AA----A-
> str06: T--T---CCT-A---G----GTA-
> str07: T--TG----T-A---GA-TC-T--
> str08: T---GG----GAA--G--T--T-C
> str09: T--T---CC--A--C-AA-C-T--
> str10: TC-T--A----AA-CGAA------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 13.0
> wall time: 60.258975s
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
> best bound: 0.0
> wall time: 187.182389s
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
> --- Solution (of length 47) ---
>   Sol: MEQSSLFVPRNAQNLSYAGQEFDHAKFVTCIRANRPEVKGGLHYTDQ
> str01: M----------A--LSY------------C-----P--KG----T--
> str02: M-QSSL----NA------------------I----P-V---------
> str03: M-------P-----LSY--Q---H--F----R------K--------
> str04: ME------------------E--H---V-----N--E----LH--D-
> str05: M--S------N----------FD-A-----IRA--------L-----
> str06: M-----F--RN-QN-S---------------R-N-----G-------
> str07: M-----F---------YA-----HA-F------------GG--Y---
> str08: M--S---------------------KF-T--R--RP-------Y--Q
> str09: M--S--FV---A------G--------VT---A-------------Q
> str10: ME-S-L-VP---------G--F-----------N--E----------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 47
> best bound: 27.0
> wall time: 60.318558s
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
> best bound: 0.0
> wall time: 192.605031s
> ```
