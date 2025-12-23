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
> --- Solution (of length 62) ---
>  Sol: ulctikgnycojkisoeqvufoahzmgpbplrnddbxxcvsvrvnuhntqgxzpvxissbxf
> str1: ---t-kgn----k------u---h-m-p--------x-------n-h-tqgxz-vxis----
> str2: ----i-----oj-i---q--fo--------l-n--bxxcvs----u---q---pv-issbxf
> str3: ulc-i--nyco---so--v--o--z--p-pl----------------------p--------
> str4: ----i-g---------e-v---a-z-g-b--r-ddb--c-svrvn--n--g----------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 45.0
> wall time: 60.203233s
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
> --- Solution (of length 104) ---
>  Sol: itpkgbypuldrevazdocjxiwvxnykughqbckrdmpdfzforsomxlnhjstqvcbrgtxxodzcvftmsepurqpxvizbrvicnnwdlgpssbhxfloe
> str1: -t-kg--------------------n-ku-h------mp---------x-nh--tq----g-x---z-v----------x-i-------------s--------
> str2: i----------------o-j-i---------q--------f--o-----ln-------b---xx---cv---s--u-qp-vi-------------ssb-xf---
> str3: --------ul--------c--i---ny------c---------o-so---------v-------o-z-------p---p-------------l-p---------
> str4: i---g-------evaz-------------g--b--rd--d------------------b--------c----s-------v---rv--nn---g------f---
> str5: --p---yp-l-r---z----x-------u----c----p--------m-------qv---gt---d---f-----u-----i---v-c---d---s-b----o-
> str6: --p--b----d-ev--d-c----v------------d-p-fz---s-m-----s----br----o------------q--v--b-------------bh-----
> str7: ------------e------------n------bc-------zf---------j-t-v-----x----------e--r-----zbrvi------gp------l-e
> str8: -----------r--------x-w-x------q--krd-------r----l-------c---t--od----tm--p-r-px----------wd------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 104
> best bound: 37.0
> wall time: 60.824981s
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
>   Sol: iktkgerxuqnkwahpibsldtwxuefvcqfihakxdrzgqcsoajvidhnypqflecmeojpwrmzilxausnmqsdhbxxctpvriuswiaqnodtfubmqkdxvegqazkophbcsvxizkrtdsjvrpfownhunzsbmixpwvcrzdgvlfisgboydhple
> str01: --tkg-----nk------------u-------h-------------------------m---p------x---n----h----t---------q--------------g-----------x-z------v--------------x-----------is---------
> str02: i------------------------------------------o-j-i-----qf-----o-------l----n-----bxxc--v---s---------u--q-----------p----v-i-----s------------sb--x----------f-----------
> str03: --------u----------l--------c--i------------------ny-----c--o-----------s----------------------o----------v------o--------z--------p-------------p--------l---------p--
> str04: i---ge---------------------v-----a----zg---------------------------------------b------r---------d-------d-----------bcsv----r----v-----n--n-------------g--f-----------
> str05: ---------------p-----------------------------------yp--l--------r-z--x-u----------c-p----------------mq---v-g----------------td-----f----u-----i---vc--d-----s-bo------
> str06: ---------------p-b--d----e-v--------d----c----v-d---p-f-----------z-----s-m-s--b------r--------o------q---v---------b------------------------b---------------------h---
> str07: -----e----n------b----------c---------z---------------f------j---------------------t-v-------------------x-e----------------r--------------z-b-------r---v--i-g-----ple
> str08: ------rx----w----------x-----q----k--r----------d---------------r---l-------------ct-----------odt---m------------p---------r------p------------x-w----d---------------
> str09: -k-k-----q---a------------f----i-------gq----j-----------------w-------------------------------o-------k--------k-----s----kr----------------b------------l---g--------
> str10: -------------------l---x-----------x----------------p-----------------a--------b-------i------------------v---------b--v--zk---------o-----z----------z--v--------d----
> str11: -k----r---------i---------f---------------s-a-v---n------c-------------------d---------------q----------------------------------------w-h--z--------c------------------
> str12: ---------q---a---------xu-----------d--gq-----v------q---c-e---w---------------b------------------f---------g------------i------j----ow-----------w--------------y-----
> str13: ------r-----------s----x-----q---------------j----n---f-------p-------a------d---------ius-i-q------b------e---z---h-------k---------o--h-----m---------g--------------
> str14: i-----------w-----s-------------h-------------v--h-------c--o----m-i---u-------------v----------d-------d-------------------------------------m------------------------
> str15: --------------h------t-x-----------x----q----j--------------------z--------q---b--ct----------------b---------a-k----------------------n-------------------------------
> str16: -------xu---------s-------f-c-f-------z-------------p---e--e----------------------c--v----w-a-n--tf--m------gq-z-------------------------u-----------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 167
> best bound: 15.0
> wall time: 62.678601s
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
>   Sol: bbaeddcabcdebedecbadbacecbde
> str01: ----d-c-bc------c--db-c-c--e
> str02: b---dd--b--e-e-e-------e-bd-
> str03: ------ca-cde-e--c------e-b-e
> str04: --aedd----d---de-b-d------d-
> str05: --a---c-b--e-e--c-a-b-ce----
> str06: bba-----b--eb-d-cba---------
> str07: bbae---a---eb-----ad-a------
> str08: ---e-------e-e-ecb-db--e---e
> str09: ------c--cde-ed---ad--c---d-
> str10: b---d--ab-d-be----a--a----d-
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 28
> best bound: 16.0
> wall time: 60.697508s
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
> --- Solution (of length 44) ---
>   Sol: cddcdaeeacbdebaecbcdbeabdbaeeaebcdaebcdcadeb
> str01: -d-c------b-----c-cdb-----------c----c----e-
> str02: ----------bd-------dbe-----ee-eb-d----------
> str03: c----a---c-de--ec----e-b---e----------------
> str04: -----ae----d-------d----d--------d-eb-d--d--
> str05: -----a---cb-e--ec-----ab--------c--e--------
> str06: ----------b--ba--b---e-bd-------c---b---a---
> str07: ----------b--bae------a----e---b--a---d-a---
> str08: ------ee----e--ecb-dbe-----e----------------
> str09: c--cd-ee---d--a----d------------cd----------
> str10: ----------bd--a--b-dbea---a------d----------
> str11: ------e----de------d--a---a--ae---a-----a---
> str12: -----a--a---e-a-------ab---eea--c-----------
> str13: ------e-a-----a--bc---a---------c----cd----b
> str14: ----------bde--e------a-d--e-a---d-e--------
> str15: c----ae----d--a----d-e-----ee----d----------
> str16: ------e---b-----c-----a-dba----b----b-----e-
> str17: -ddc--eea-bde-a-----------------------------
> str18: -d---a----b-----c--d----d--e-ae-c-----------
> str19: -----a--a--d----c----e-----e-----da-----a--b
> str20: -----aee-c------c----e-----eea----a---------
> str21: ----------b--b-----d--a----e----c-a-----ade-
> str22: -d---a---c--e------d--a----e-----da-b-------
> str23: -----a--a---e-a--b--b--b-b------c--e--------
> str24: -d----e----d-b--cbc---a---a----b------------
> str25: -d--------bd--a-------a----e---b----bc-----b
> str26: -d----e---b-e------dbe-b--a-----c-----------
> str27: c-----ee--b-----c--d------------c---b-d---e-
> str28: -d--------b-e------d--a---a------da-----a--b
> str29: c--c-----c-d----cb---e-bd-------c-----------
> str30: -----aeeac-d-b--cb-d------------------------
> str31: -d---a---cb-e-a-c-c-------------cd----------
> str32: ------e--c--eb--c-cdb---db------------------
> str33: -dd-------b--b--c----e--d-a----b----b-------
> str34: -----a--a---e-a--b----a---ae---b--a---------
> str35: ------e--cb--b--c-----a---a------d---cd-----
> str36: -d----e---b-----c-c--e----------cd--bc------
> str37: -d---a--acb---ae-----e-b--------c-----------
> str38: -----a-----d--a--b---ea---a-----c----c----e-
> str39: -d---ae--c-d-ba-c-----a---a-----------------
> str40: -d---a---cb--b-----d------------c--e--dc----
> str41: -d----e----d-b-e-----e-b-b-------d-e--------
> str42: cd---a-----d----c--d------------cda-----a---
> str43: c-----ee---d----cb----a----ee----d----------
> str44: c-----e-a---e---c-----a---a--a--c-a---------
> str45: -d-c-----c------c----e-b-b-----b--a---d-----
> str46: ----------b---ae-----ea----e---b----b-d---e-
> str47: -d--------bdeba-c-cdb-----------------------
> str48: ------e---b-----cb---e-----e-----dae----a---
> str49: -----aee----eb---b-db-----------c-a---------
> str50: -d--------bd--a--bc--e----------c---b------b
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 44
> best bound: 2.0
> wall time: 66.014481s
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
>   Sol: TCATACCGGTAATCGATACGTTCA
> str01: --AT---GG-----GATACG----
> str02: --ATACC--T--TC----C---C-
> str03: -CA--C-G--AAT---T--G---A
> str04: T-A-A-----AATC--T--GT---
> str05: --A----GGTAA-C-A-A-----A
> str06: T--T-CC--TA---G----GT--A
> str07: T--T---G-TA---GAT-C-T---
> str08: T------GG-----GA-A-GTTC-
> str09: T--T-CC---A--C-A-AC-T---
> str10: TC-TA-----AA-CGA-A------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 13.0
> wall time: 60.254439s
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
> wall time: 187.109324s
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
>   Sol: MQESPSALEFRNSVYAQCPNKGHVFTDAIRSRNPFEVKALGGYHQD
> str01: M-----AL----S-Y--CP-KG---T--------------------
> str02: MQ-S-S-L---N---A------------I----P--V---------
> str03: M---P--L----S-Y-Q-----H-F----R-------K--------
> str04: M-E-----E-------------HV--------N--E---L---H-D
> str05: M--S-------N------------F-DAIR--------AL------
> str06: M--------FRN----Q--N----------SRN-------G-----
> str07: M--------F----YA------H----A------F-----GGY---
> str08: M--S----------------K---FT---R-R-P--------Y-Q-
> str09: M--S-----F---V-A-----G-V-T-A----------------Q-
> str10: M-ES---L-----V----P--G--F-------N--E----------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 46
> best bound: 27.0
> wall time: 60.330017s
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
> wall time: 198.044607s
> ```
