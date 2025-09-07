In [ ]:
```python
import marimo as mo
import nbformat
import util
```


# アルファベットアルゴリズム

- 計算量: $O(qk)$
- 近似精度: $q$

文字種全体を $\Sigma = \{ c_1, \dots, c_q \}$ とする.
与えられた文字列の中で最大の長さ $k$ に対して下記は与えられた文字列全ての supersequence になる:

$$
(c_1 c_2 \dots c_q)^k
$$

これを解とすることで長さ $qk$ の common supersequence を出力する.
この長さは文字列の数に直接は依存しない.

各文字列 $s_i$ の $j$ 番目の文字は上記 $(c_1 c_2 \dots c_q)^k$ の中の $j$ 番目のブロックに必ず含まれているが,
$j$ 番目のブロックの中にはどの文字列でも使用しない文字があるかもしれない.
そのような文字は捨てることで解を少し改善する.
これによって解が少し改善するが, 文字列の数が増えると削れる文字が少なくなり, 長さ $qk$ に近づく.

In [ ]:
```python
def solve(instance: list[str]) -> str:
    chars = sorted(list(set("".join(instance))))
    solution = ""

    for i in range(max([len(s) for s in instance])):
        used = [False for _ in chars]
        for s in instance:
            if i >= len(s):
                continue
            used[chars.index(s[i])] = True

        for c, u in zip(chars, used):
            if u:
                solution += c

    return solution
```


In [ ]:
```python
_instance = util.parse("uniform_q26n004k015-025.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
```


> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 79) ---
>  Sol: itugklocegjinvaknqfuyzcghoblmonprsbdoxdnvxbhoxctzpqsvgpsvlruxpqvznpvnvxgifssbxf
> str1: -t--k----g--n--k---u----h---m--p-----x-n---h---t--q--g------x---z--v--x-i-s----
> str2: i-----o---ji-----qf------o-l--n---b--x---x----c-----v--s---u--q---pv----i-ssbxf
> str3: --u--l-c---in-------y-c--o-------s--o---v---o---zp----p--l---p-----------------
> str4: i--g----e----va------z-g--b-----r--d--d---b---c----sv-----r----v-n--n--g-f-----
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("uniform_q26n008k015-025.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 155) ---
>  Sol: eiprtubgklnoxybcdegjpwceilnvxaknqrvzdfkuyzcghjorxbdlmotuvcdnprsvbdlopxcdefmnvxbhoqrtxzcostvzbdgmpqsvgprstvbdlmruvxfipqrvzgnopruvinpqvxgilvxbcefswbdsbhsbxfo
> str1: ----t---k---------g-------n---k--------u----h-------m-------p--------x-----n---h---t-------------q--g------------x------z------v-----x-i-------s-----------
> str2: -i---------o-------j----i-------q----f--------o----l-------n----b----x-------x--------c---v-------s------------u-----q------p--vi--------------s---sb---xf-
> str3: -----u---l-----c--------i-n-------------y-c---o---------------s----o--------v---o----z----------p----p------l-------p--------------------------------------
> str4: -i-----g---------e---------v-a-----z-------g-----b-----------r---d-----d------b-------c-s-v-----------r--v----------------n------n----g-------f------------
> str5: --p----------y------p----l-------r-z------------x------u-c--p-------------m------q--------v---g---------t--d------f-----------u-i---v-------c-----dsb-----o
> str6: --p---b---------de---------v--------d-----c-------------v-d-p------------f-----------z--s------m--s-------b---r------------o-----
> ```

> ```
> --qv------b-----b---h-----
> str7: e---------n---bc-------------------z-f-------j--------t-v------------x--e---------r--z------b---------r--v---------i-----g--p-----------l----e-------------
> str8: ---r--------x--------w------x---q-----k--------r--d----------r----l---c------------t---o-----d----------t----m------p-r-----p--------x----------w-d--------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("uniform_q26n016k015-025.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 256) ---
>   Sol: ehiklpqrtuxabgklnorstuwxybcdegijpqswxacefhilnpquvxacdfjknqrsvzabdfghijknuyzcfghijoqrvxzbdlmnopqtuvabcdejmnpqrsvbcdeilopvwxcdefimnoqtuvxzbhkoqrtuvwxzabcdhkostvwzabdfgikmpqsvzcgkmnpqrstvzbdilmrtuvxbdefijpqrvzglmnopruvzghinpqvwxgiklqvwxbcefoswyzbdhsubhmsbgxfo
> str01: --------t-----k--------------g--------------n----------k----------------u-----h-----------m--p---------------------------x------n--------h----t--------------------------q----g-------------------x----------z--------v---------x-i-----------s-----------------
> str02: --i--------------o-------------j----------i---q------f---------------------------o-------l-n-------b---------------------x------------x---------------c------v------------s---------------------u---------q--------p--v---i-------------------s------s-b-----xf-
> str03: ---------u-----l----------c---i-------------n----------------------------y-c-----o---------------------------s-------o-v---------o-----z--------------------------------p---------p---------l------------p------------------------------------------------------
> str04: --i----------g--------------e-------------------v-a----------z----g--------------------b--------------------r----d---------d------------b-------------c----s-v----------------------r--v-------------------------n---------n-----g----------f-------------------
> str05: -----p------------------y-------p----------l--------------r--z-----------------------x----------u---c-----p--------------------m--q--v------------------------------g-----------------t---d-----------f--------------u----i---v-----------c--------d-s-b-------o
> str06: -----p------b--------------de-------------------v---d----------------------c--------v---d----p-------------------------------f---------z-------------------s-----------m--s--------------b----r-------------------o----------qv----------b--------b-h-----------
> str07: e---------------n--------bc----------------------------------z---f---j-------------------------t-v-----------------------x--e----------------r-----z-b------------------------------r--v---i------------------g----p----------------l------e--------------------
> str08: -------r--x-----------wx---------q---------------------k--r-----d------------------r-----l----------c---
> ```

> ```
> ---------------------------t-------o-----------d----t----------mp-----------r--------------------p----------------------x------w-----------d------------
> str09: ---k----------k------------------q---a--f-i-----------------------g---------------q--------------------j----------------w--------o--------k--------------k-s----------k-------------r----b--l-----------------g-------------------------------------------------
> str10: ----l-----x------------x--------p----a-------------------------b----i---------------v--b---------v-------------------------------------z--ko-------z-----------z-----------v--------------d---------------------------------------------------------------------
> str11: ---k---r----------------------i---------f------------------s--a---------------------v------n--------cd-----q------------w----------------h---------z--c---------------------------------------------------------------------------------------------------------
> str12: ------q----a-----------x-----------------------u----d-------------g---------------q-v---------q-----c-e-----------------w---------------b--------------------------fgi----------------------------------j---------o------------w-------w--------y---------------
> str13: -------r-----------s---x---------q--------------------j-n--------f---------------------------p----a--d-------------i----------------u----------------------s---------i---q---------------b-----------e-------z-----------h---------k---------o------h----m--g---
> str14: --i-------------------w-----------s------h------v------------------h-------c-----o--------m------------------------i----------------uv-----------------d----------d----m----------------------------------------------------------------------------------------
> str15: -h------t-x------------x---------q--------------------j------z--------------------q----b------------c------------------------------t----b-----------a----k-----------------------n------------------------------------------------------------------------------
> str16: ----------x----------u------------s-----f----------c-f-------z-------------------------------p--------e-----------e-------c----------v-----------w--a----------------------------n----t---------------f---------m-------g----q-------------------z----u---------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("uniform_q05n010k010-010.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 45) ---
>   Sol: abcdeabcdeabcdebcdeacdebcdeabcdeabcdeabcdeade
> str01: ---d---c---bc---cd-----bc----c-e-------------
> str02: -b-d----d--b--e---e---e---e-b-d--------------
> str03: --c--a-cde----e-c-e----b--e------------------
> str04: a---e---d----d---d---deb-d----d--------------
> str05: a-c---b--e----e-c--a---bc-e------------------
> str06: -b----b---ab--eb-d--c--b---a-----------------
> str07: -b----b---a---e----a--eb---a--d-a------------
> str08: ----e----e----e---e-c--b-d--b--e----e--------
> str09: --c----cde----e--d-a-d--cd-------------------
> str10: -b-d-ab-d--b--e----a-------a--d--------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("uniform_q05n050k010-010.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 50) ---
>   Sol: abcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcde
> str01: ---d---c---bc----cd--bc----c-e--------------------
> str02: -b-d----d--b--e----e----e----e-b-d----------------
> str03: --c--a-cde----e--c-e-b--e-------------------------
> str04: a---e---d----d----d----de-b-d----d----------------
> str05: a-c---b--e----e--c--abc-e-------------------------
> str06: -b----b---ab--e-b-d---c---b---a-------------------
> str07: -b----b---a---ea---e-b---a--d-a-------------------
> str08: ----e----e----e----e--c---b-d--b--e----e----------
> str09: --c----cde----e---d-a--d---cd---------------------
> str10: -b-d-ab-d--b--ea----a--d--------------------------
> str11: ----e---de---d-a----a----a---ea----a--------------
> str12: a----a---ea----ab--e----ea-c----------------------
> str13: ----ea----abc--a-c----cd--b-----------------------
> str14: -b-de----ea--dea--de------------------------------
> str15: --c--a---e---d-a--de----e----e---d----------------
> str16: ----e-bc--a--d--b---ab----b--e--------------------
> str17: ---d----d---c-e----eab-dea------------------------
> str18: ---d-abcd----dea---e--c---------------------------
> str19: a----a--d---c-e----e---d-a----ab------------------
> str20: a---e----e--c----c-e----e----ea----a--------------
> str21: -b----b-d-a---e--c--a----a--de--------------------
> str22: ---d-a-c-e---d-a---e---d-ab-----------------------
> str23: a----a---eab----b----b----bc-e--------------------
> str24: ---de---d--bc---bc--a----ab-----------------------
> str25: ---d--b-d-a----a---e-b----bc---b------------------
> str26: ---de-b--e---d--b--e-b---a-c----------------------
> str27: --c-e----e-bcd---c---b-de-------------------------
> str28: ---d--b--e---d-a----a--d-a----ab------------------
> str29: --c----c----cd---c---b--e-b-d---c-----------------
> str30: a---e----ea-cd--bc---b-d--------------------------
> str31: ---d-a-c---b--ea-c----c----cd---------------------
> str32: ----e--c-e-bc----cd--b-d--b-----------------------
> str33: ---d----d--b----bc-e---d-ab----b------------------
> str34: a----a---eab---a----a---e-b---a-------------------
> str35: ----e--c---b----bc--a----a--d---cd----------------
> str36: ---de-bc----c-e--cd--bc---------------------------
> str37: ---d-a----a-c---b---a---e----e-bc-----------------
> str38: a--d-ab--ea----a-c----c-e-------------------------
> str39: ---d-a---e--cd--b---a-c--a----a-------------------
> str40: ---d-a-c---b----b-d---c-e---d---c-----------------
> str41: ---de---d--b--e----e-b----b-de--------------------
> str42: --cd-a--d---cd---cd-a----a------------------------
> str43: --c-e----e---d---c---b---a---e----e---d-----------
> str44: --c-ea---e--c--a----a----a-c--a-------------------
> str45: ---d---c----c----c-e-b----b----b---a--d-----------
> str46: -b---a---e----ea---e-b----b-de--------------------
> str47: ---d--b-de-b---a-c----cd--b-----------------------
> str48: ----e-bc---b--e----e---d-a---ea-------------------
> str49: a---e----e----e-b----b-d--bc--a-------------------
> str50: ---d--b-d-abc-e--c---b----b-----------------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("nucleotide_n010k010.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 39) ---
>   Sol: ACTACGTACGTACGTACGTACGTACGTACGTACGTACGT
> str01: A-T--G---G---G-A--TACG-----------------
> str02: A-TAC---C-T---T-C---C---C--------------
> str03: -C-ACG-A---A--T---T--G-A---------------
> str04: --TA---A---A---A--T-C-T--GT------------
> str05: A----G---GTA---AC--A---A---A-----------
> str06: --T---T-C---C-TA-G---GTA---------------
> str07: --T---T--GTA-G-A--T-C-T----------------
> str08: --T--G---G---G-A---A-GT---T-C----------
> str09: --T---T-C---C--AC--A---AC-T------------
> str10: --T-C-TA---A---ACG-A---A---------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("nucleotide_n050k050.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 201) ---
>   Sol: ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGRT
> str01: ---TA-GTA-GTA-G-AC-T-C---CG---G-A---A-GT--G-AC--A---A---AC---C---C-T--G-A---A---A---A-G-A---A--T--G---G-A--TA---A---A--TA--TA----------------------------------------------------------------------------
> str02: --G---G-A--TA---A---AC--AC-T-C---C---CG-A---A---A---A--TA---A--T---T---T--G-AC-T---TA---A---AC--A---ACG--CG-AC--A-GT---T-C--A---A-G----------------------------------------------------------------------
> str03: A--TAC---C-T---T-C---C-TA-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T---T--G-A--T-C-T-C-T---T--GTA-G-A--T-C-T--G--------------------------------------------------------------------------
> str04: ---TA---A---A--T---TA--TA---A--T-C-T---TA--TAC-TA-GTA---A---A---A---A---A--TA-G---G---GT--GTA---AC---CG-A---A---A---ACG---GT-C---------------------------------------------------------------------------
> str05: ---T---TA---A---A---AC--A-G--C---C-T--GT--G---G---GT-
> ```

> ```
> --T--G--C--AC---C---C--AC-T-C--AC--A-G---G---G--C---C---C--AC-T--G---G---G--CG--C--A---A-G----------------------------------------------------------
> str06: A--T--G-AC-T---T-C---C--A---A--T--G---G-A--T-C---C---C--A---AC---C-T-C--A---A-G--C-T---T-C---C--AC---C---C---C--A---A--T--G---GT---T---T-C--A-G--C-------------------------------------------------------
> str07: A---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T---T--G-A--T-C-T-C-T---T--GTA-G-A--T-C-T--GT---T-C-T-C-TA---A---ACG-A---AC---------------------------------------------------------------------------
> str08: A--T--G-A---A---A---ACG-A---A---A---A--T---TA--T---TA--T-C--A---A-G---G---GTA--T--G---G-A---A-GT--G---G-A---A-G--C-T--G-ACG-A---A---A--T-----------------------------------------------------------------
> str09: AC-T-CG---G--C-T--G--C--A--T--G--C-T---TA-GT--G--C--AC-T-C--ACG--C--A-GTA--TA---A--T---TA---A--TA---AC-TA---A--T---TA------------------------------------------------------------------------------------
> str10: ---T---T--GTA-G-A--T-C-T--GT---T-C-T-C-TA---A---ACG-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G---G--C-T--GT-C--AC-T-C-------------------------------------------------------------------------------
> str11: --G--C--A-G-A-G--C--A--T---T---T---T-C-TA---A--TA--T-C---C--AC--A---A---A---A--T--G-A---A-G---G--C--A---A--TA---A--T---T--GTAC-TAC-T-C-------------------------------------------------------------------
> str12: A--T--G-A-G--C---C--A---A-G-A--T-C---CG-ACG-A---A-G-A-G--C---C---C---C--A---A-G---G-A-G---G-A-G-A---A-G---G-A-G---G---G-AC---C---C---C---C---------------------------------------------------------------
> str13: ---T-C-T-C--AC--A-GT---T-C--A---A-G-A---AC---C---C--A---A---A-GTAC---C---C---C---C---C--A--TA-G--C---C---C-T-C-T---TA---A---A-G--C---C--AC---------------------------------------------------------------
> str14: A-G---GT---T---TA--TAC---C-T---T-C---C-TA-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--GTA----------------------------------------------------------------------------
> str15: A-G---GT---T---TA--TAC---C-T---T-C---C---C--A-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--GTA------------------------------------------------------------------------
> str16: ---TA---A---A---AC--A---AC-T-C--A---A--TAC--A---AC--A--TA---A-G-A---A---A---A--T-C--A---ACG--C--A---A---A---A---AC--AC-T-C--AC--A---A---A----------------------------------------------------------------
> str17: -C---CG--C---C---C--A--T---T---T--G---G---G--CG---G--C-T-C-T-CG-A-G--CG-A--TA-G--C-T-CGT-CG-A---A--T-C---C---C-T-CG-AC---C-T-----------------------------------------------------------------------------
> str18: A--TAC---C-T---T-C---C---C--A-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--GTA-G-A--T-C-T--G--------------------------------------------------------------------------
> str19: ---T-C-T-C--AC--A-GT---T-C--A---A-G-A---AC---C-T-C--A---A-GT-C-T-C---C---C---C---C--A--TA-G---G--C---C-T-C-T---T---T-C--A-GT-C--A-G----------------------------------------------------------------------
> str20: --G-A--T-C-T-C-T-C-T-C--AC---CG-A---AC---C-T--G---G--C---C---C---CG---G---G--C--A---A---A--T--G--C---C---C-TA---A--T-C---C--A-G-A-G---GT--G--------------------------------------------------------------
> str21: A-G-A-G--C--A---A--T-C--A-GT--G--C--A--T-C--A-G-A---A---A--TA--TAC---C-TA--T---TA--TAC--AC-T---T---T--G--C-TA---A-G-A---A--T-----------------------------------------------------------------------------
> str22: A---A--T---TA---A---A---AC--A--T-C-T-C--A---A--TAC--A---AC--A--TA---A-G-A---A---A---A---AC--A---ACG--C--A---A---A---A---AC--AC-T-C--A--T-----------------------------------------------------------------
> str23: A---A---ACG-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G---G--C-T--GT-C--AC-T-CG---G--C-T--G--C--A--T--G--C-T---TA-GT--G--C---------------------------------------------------------------------------
> str24: A--TA---AC-TA---A--T---TAC-T--GT-CGT---T--G-AC--A-G---G-AC--ACG-A-GTA---AC-T-CGT-C-TA--T-C-T---T-C-T--G-----
> ```

> ```
> ---------------------------------------------------------------------------------------------
> str25: A--T--G-A-GT--GT-C--ACG-A---A--T---T-C--ACGTAC--A---A--T--G-A---AC-T--G---G-A--T--GT---T-C--ACGT--G---G-A---A--TA---A------------------------------------------------------------------------------------
> str26: AC---CGT--G---G---G--CG-A-G--CG---GT--G-AC---CG---GT--GT-C-T---T-C---C-TA-GT--G---G---GT-C---C---C--ACGT---T--G-A---A----------------------------------------------------------------------------------R-
> str27: A---A---A-G---GT---T---TA--TAC---C-T---T-C---C---C--A-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--G------------------------------------------------------------------
> str28: A-GTA-GT---T-CG--C---C-T--GT--GT--G-A-G--C-T--G-AC--A---A---AC-T---TA-GTA-GT--GT---T---T--GT--G-A-G---G-A--T---TA----------------------------------------------------------------------------------------
> str29: ---T---T---TA--TAC---C-T---T-C---C-TA-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--GTA-G-A--T-------------------------------------------------------------------------
> str30: A--T--G--CG---GT-CGT-C-T-C-T-C---C---C---CG---G--C-T---T---T---T---T---T---T-C---C---C---CG--CG--C---CG--CGT---T--G---G--CG--C---CG-A--------------------------------------------------------------------
> str31: --GT--G-AC--A---A---A---A---AC--A--TA---A--T--G---G-AC-T-C---C--A---AC--AC---C--A--T--GT-C--A---A-G--C-T---T---T-C--A-G---GTA-G-AC-----------------------------------------------------------------------
> str32: --GT--GTA---A-G-A---A---AC--A-GTA---A-G--C---C---CG---G-A---A-GT--G---GT--GT---T---T---T--G--CG-A--T---T---T-CG-A-G---G--C---CG---G----------------------------------------------------------------------
> str33: --G-A-G-A---A--T--G-A-GT-C-T-C--A--T---TAC---CG--C---C---CG---GTAC-T---TA-G--C--A---A-G--C-TA---A--TA-GT-C--ACG---G--C-----------------------------------------------------------------------------------
> str34: A--T--GT--G---GT-CG-A--T--G--C---C--A--T--G---G-A-G---G--C---C---C--AC---C--A-GT---T-C--A--T---TA---A-G---G--C-T-C---C-T--G---G--C--A--T---T-------------------------------------------------------------
> str35: ACG-A-G--CGT---T---T---TA---A-G---G---G--C---C---CG--CG-AC-T--G--CG-ACG---G--C---C--AC--A--T--G---G--C---C---C-T--GTA--T--GT-----------------------------------------------------------------------------
> str36: --G---GT---T---TA--TAC---C-T---T-C---C---C--A-G---GTA---AC--A---A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--GTA-G----------------------------------------------------------------------
> str37: ---T--G---G---G-A---A-GT---T-C---C--A---A---A---A-G-A--T-C--AC--A---A---A---AC--AC-TAC---C--A-GT-C--A---AC---C-T--G-A---A-GTAC--AC-----------------------------------------------------------------------
> str38: --G-A---A-G--CGT---TA---ACGT--GT---T--G-A-G---G-A---A---A---A-G-AC--A-G--C-T---TA-G---G-A-G-A---AC--A---A-G-A-G--C-T--G---G---G--------------------------------------------------------------------------
> str39: AC---C--A-G--CG--C--AC-T---T-CG---G--C--A-G--CG---G--C--A-G--C--AC---C-T-CG---G--C
> ```

> ```
> --A-G--C--AC---C-T-C--A-G--C--A-G--C--A---AC---------------------------------------------------------------------------
> str40: A--T--G---G---G-AC--A---AC-T---TA--T---T-C---C-TA--T-C--A--T--GT--G--C---C--A---A-G-A-G---GT---T---T---TAC---C---CG---GT--G-AC---C--A--------------------------------------------------------------------
> str41: ---T---T--GTA-G-A--T-C-T--GT---T-C-T-C-TA---A---ACG-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G---GT---T--GT-C--AC-T-C-------------------------------------------------------------------------------
> str42: A---AC---C--A---AC---C--A---AC-T---T---T-CG-A--T-C-T-C-T---T--GTA-G-A--T-C-T--GT---T-C-T-C-TA---A---ACG-A---AC-T---T---TA--------------------------------------------------------------------------------
> str43: --G---G---GT---T-C-T--G--C---C--A-G---G--C--A--TA-GT-C-T---T---T---T---T---T---T-C-T--G---G--CG---G--C---C---C-T---T--GT--GTA---A---AC---C-T--G----------------------------------------------------------
> str44: --G---G--C-T--G--C--A--T--G--C-T---TA-GT--G--C--AC-T-C--ACG--C--A-GTA--TA---A--T---TA---A--TA---AC-TA---A--T---TAC-T--GT---------------------------------------------------------------------------------
> str45: ---T--G--C--A--T--G--C-T---TA-GT--G--C--AC-T-C--ACG--C--A-GTA--TA---A--T---TA---A--TA---AC-TA---A--T---TAC-T--GT-CGT-------------------------------------------------------------------------------------
> str46: ---T---T-C---C--AC--A---AC-T---T---T-C---C--AC---C--A---A-G--C-T-C-T--G--C--A---A-G-A--T-C---C---C--A-G-A-GT-C--A-G---G---G---G--C---C-T--GT-------------------------------------------------------------
> str47: ---T-C-TA---A---ACG-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G---G--C-T--GT-C--AC-T-CG---G--C-T--G--C--A--T--G--C-T---TA-G--------------------------------------------------------------------------
> str48: AC---CG---G-A--T--G---G--C---CG--CG-A--T---T---T---T---T-CG---G-A-GT-C---C-T---T--G---G---G---G---G-AC---C--AC-T-C--A-G-A---A--TA-G-A--------------------------------------------------------------------
> str49: -C-T---T--GTA-G-A--T-C-T--GT---T-C-T-C-TA---A---ACG-A---AC-T---T---TA---A---A---A--T-C-T--GT--GT--G---G--C-T--GT-C--AC-T---------------------------------------------------------------------------------
> str50: A--T--G-A-G--C--AC-TA---A-G--CG-A---A-G-A---AC---C--A---A---A---A---A-G--C--A-G-AC--A---A--TAC--A---AC---C---CG--C-TA--T---TAC---------------------------------------------------------------------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("protein_n010k010.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 71) ---
>   Sol: MAEFPQSEFKLNRSYAFHLNSVADHLQTVYACGNPQRAEFGHIPRSVFGIKLPRTAGHNPRYDEGKLQTVY
> str01: MA--------L--SY----------------C--P---------------K-----G-----------T--
> str02: M----QS------S----LN--A-------------------IP--V------------------------
> str03: M---P-----L--SY-----------Q--------------H-----F-----R-----------K-----
> str04: M-E----E---------H---V-----------N----E------------L-----H----D--------
> str05: M-----S----N----F------D------A-----------I-R----------A----------L----
> str06: M--F--------R------N------Q------N-----------S-------R----N-----G------
> str07: M--F----------YA-H----A----------------FG-------G------------Y---------
> str08: M-----S--K------F----------T--------R-------R-------P--------Y-----Q---
> str09: M-----S-F------------VA---------G-------------V-------TA-----------Q---
> str10: M-E---S---L----------V------------P-----G------F----------N----E-------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
_instance = util.parse("protein_n050k050.txt")
util.show(_instance)
_solution = solve(_instance)
util.show(_instance, _solution)
print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
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
> --- Solution (of length 782) ---
>   Sol: FMADEFGHIKLNPRSWADEFGHKLNPQRSTVYADEFGIKLPQRSVYADEFGHILNPRSTVYADEFGHIKLNPQRSTVYADEFGIKLNPQRSTVYADFGIKLNQRSTVWAEFGHIKLMNPQRSTWYADEGIKLNPQRTVWYADEFGHIKLNPQSTVYADEGHIKLMQSTVWADFGHIKLNPQRSTVWADEFGIKLMNPQRSTVWYACDEHIKLMNQRSTVYACDEFGIKLMNPQRSTVWYADEFGKLMNPQSTVAEFGIKLNPQRSTVWYADEFGHIKLNPQRSTVACEFGHIKLNQRSTVYADFGHIKLNPQRSTVYADEFHKLNPQRSTVWYADEFGHILMNPQRSTVYACDEFGHIKLNQRSTVYACDFGIKLMNPQSTVYAEFGHIKLNPQRSTVYACDEFGHKLNPQRSTVYADFGIKLMPQRSTVWYADEFIKLMRTVWYACDEFGHIKLMNPSTVWYACDFGIKLNPRSTVWYACDEFGKLNRSTVWYADEFGHILPQRSTVWADEFGHIKLMNPQRSTVWYADEFGIKLMNPRSTVYADEFGIKLNPRSTVWYACDEFGIKLPRSTVYADEFHIKLNPRTVYACDEFGHIKLPRSTVYADEFGIKLNPQRSTVADEGIKLMNPQRSTVWYADEFGIKLNPQRSTVACDEFGILMNPQRSTVYACDEFGHIKLMQRSTVWYACDEGHIKLNRSTVYADEFGHIKLNQRSTVADEGHIKLMNPQRSTVWYACDGHIKLMNQRSTVYADFGHIKLMNQRSTVYDFGHILNPQRSTVWY
> str01: -M-----------R-------H-LN------------I---------D----I----------E-----------T-Y------------S-------------S------------N--------D--IK-N-----------G---------VY------K----------------------------------------YA-D-------------A--E----------------D-F-----------E--I-L-----------------L----------F------------A--------------Y-----------S----------I------------D--G---------------G------------E------------V----E-------------------------------------------C-------L----------D----L----T------------R-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str02: -M--E--------R-------------R-
> ```

> ```
> ---A------------------H----R-T-------H-----Q-------------N--------------------W------------------D-------------A------------T--------K----------------P-R------E---------R----------------R-----------K----Q--T-------------Q------------------------H------R-----------L----T------H----P-------D---------------D-----------S----------I--------Y----------P----------------R-------------------------I-------------E--K-------A--E-G----------------------R-----------K----------E-------------D---H-----------------G---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str03: -M--E-------P-------G-----------A--F-------S--------------T--A-------L-----------F-------------D------------A------L-----------------------------------------------------------------------------------------CD---------------D---I-L---------------------------------------------H------R--------------R-----------L----------E--------S---------------Q--------------L--R-------FG--------------G----------V------------Q---------I---P--------------------------------P------------------------E--------V-------------S----D---------P-R--V-YA---G----------YA------L----------------L---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: -M----G--K---------F-----------Y-------------Y-----------S------------N--R---------------R----------L-------A----------------------------V-----F------------A--------Q----A---------Q-S---------------R---------H--L-------------G-----------------G------S-----------------Y--E--------Q--------------------------------------------------W--------L---------AC-------------V-------------S------G--------------D----------S---A-F-------R-----A-E-------V----------K---------A---------R--V--------------------------Q------------K------------D------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str05: F----F-------R----E-----N--------------L------A--F----------------------Q---------------Q--------G-K--------A-----------R------E---------------F------P-S-----E-----------------------------E---------------A----------R----A---------N---S-------------P--T------------S----------------R-----E-----L-------------------------------------W----------------V-------------R-------------------------------R---------G--------------G------------------------------------NP------------L---S-------E-----------A---G----------A-E----------R----------------R--------G-------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: -M-D--------P-S--------L-----T-----------Q--V--------------------------------------------------------------WA----------------------------V----E-G-------S-V--------L--S---A---------------A--------------V----D----------T--A--E-----------T-----------N----------------------D------------T---E----------------------P-------DE-----------------G--L-----S---A--E------N-----------------------E-G---------------E----------T------------R---------I---------------I--------------------R--------------------------I-----T------G---------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> ```

> ```
> --------------------------------------------------------------------------------
> str07: -MA--F-----------D-F--------S-V---------------------------T------G----N----T--------KL---------D---------T---------------S------G--------------F---------T-----------Q-------G----------V--------------S----------------S------------M-----TV--A-------------A--G--------T-----------L-------------I---------AD-----L------V------K------T---A------------S----------------S--------------Q-----------L-----T-----------N-------------L---------A----------------------------------------------------------------------Q-S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: -MA---------------------------V------I-LP--S--------------T-Y--------------T---D--G--------T--A-------------A------------------------------------------------------------------------------------------------C-----------T------------N------------G------S----------P--------D-------------V--------------V----G---------T----------------------G---------T---------------------------M------------------------------------------------------W-----------V-------------N--T--------I-L-P-----------G----------D-F--------------F-------------W--------------T-----------P-S---------G-----------E-----------------------S-V------------R--V------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str09: -M---------N-----------------T------GI--------------I---------D------L-----------F-------------D-----N----------H------------------------V---D----------S--------I-----------------P---T-------I-L--P-----------H-----Q-------------L----------A-----------T-------L----------D-----------------------------Y-------L------V-----------R-T---------I-----------------I-----------D--------------E------N--RS-V---------L--------------L------------F---------------HI--M-----------G------S---------G---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V-----------N--------------L-----------------R-T---------------R-T-----------Q------------L-P--------------P-------A---------------Y--------------T-----------N--S-----F----------T--------------R-------G---------V-Y------------Y------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H---------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: -M-D----------S-------K-----------E-----------------------T--------I-L-------------I-------------------------E---I---------------I---P-------------K-------------IK---S------------------------------------Y-------L----------------L-----------D----------T--------N--------------I------S---------------------------P-----------K-----S---Y---------N---------D-F--I-----S------------------------------R-------------N------------K----------------------------------N-----------I--------------F-------V--------I------------------N---------------L-------Y--------N----V-------------ST-------I---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: -M----
> ```

> ```
> ----L------------L----S-------G-K-----------------------------K---------------K-------------------------------M--------------L----------------L--------D--------------------N------------------------Y---E---------T--A------------------A-------------A---------R---------G-------R-------G--------------G-------------DE-------R-----------------R----------------R--------G----------------------------------------------------------W-A--F-----------D-------------------------R----------------------------P------A-----I---------V---------------T--------K---R-------D----K---S----D--------R-----------------------------------------M---------A-------------------------------------H----------------------------------------------------------------------------------------------------------
> str13: -M---------N--------G-------------E-------------E-------------D----------------D------N----------------------E---------Q-----A--------------A---------------A-E------Q--------------Q--T--------K-----------------K---------A------K-----R-------E--K---P---------K---Q------A-----------R----------K------V--------------T-------------S------E--------------A-------------------------------------------------------------------------------W---E----------------H--------------F--------------D------------A-----------T---D------------------D--G-----------A-E--------------C-----K-----------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str14: -M--E---------S--------L------V---------P---------G-------------F-----N---------E---K------T--------------------H------------------------V-------------Q-----------L--S----------L-P----V--------L---Q---V-------------R------D-------------V--------L------V----------R---------G--------------FG------------D----------S-V---E---------------E------------V----------L---S--------------------E--------------A-----------R-------------Q-------------------------H--L--------------K-----------D--G-----T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: -M-----------R-----------------Y-----I------V------------S-------------PQ------------L------V-------L-Q---V----G--K-------------G-----Q-------E-----------V---E----------------------R----A------L---------Y-------L-----T-------------P------Y-D---------------------------Y------I--------------------------D----------------E--K-----S--------------P-------------I--------Y---------------Y--F----L---RS---------H-LN-----------I----QR------------------------------P----
> ```

> ```
> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: -M----------PR----------------V---------P---VY-D---------S-------------PQ---V-------------S---------------------------P-------------N---TV------------PQ----A------------------------R-----------L----------A------------T-------------P--S-------F----------A-----------T-------------P---T----F-------R-------G------------AD--------------A---------P------A---F------Q-------D----------T--A-------N-Q----------------Q-----A---------R----------------------------------------------------------------------------Q--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V-----------N--------------L-----------------R-T---------------R-T-----------Q------------L-P------------L---------A---------------Y--------------T-----------N--S-----F----------T--------------R-------G---------V-Y------------Y------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H---------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: -M---F------------------------V----F-------------F---------V---------L---------------L-P------------L-----V--------------S------------------------------S------------Q---------------------------------------C------------V-----------N--------------L-----T-------------T---------------R-T-----------Q------------L-P--------------P-------A---------------Y--------------T-----------N--S-----F----------T--------------R-------G---------V-Y------------Y------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H---------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: -M--E-----------A--------------------I--------------I----S------F-------------A---GI-------------GI--N----------------------Y-----K----------------KL--QS---------KL-Q--------H------------D-FG-------R--V---------L---------------K-----------A-----L-----TV------------T---A-----------R---A-------L----------------P-------------------
> ```

> ```
> -------G------Q--------------------------------P-----------K---------------H--------------I-----------A---I---R--------------------------------------------------------------Q--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: -MA-----------S-------------S-------G---P-------E-------R----A-E--H-----Q----------I--------------I-L-----------------P--------E------------------------S-------H--L--S---------------S-------------P--------------L------V--------K----------------------------------------------H-KL---------------L------Y---------------Y--------------W--------------------------KL----T------G--L--P------------L-P--------DE-------------------------------------------CD-F---------------D---------------------------------H-L-------------I--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str21: -M--E---------S--------L------V---------P---------G-------------F-----N---------E---K------T--------------------H------------------------V-------------Q-----------L--S----------L-P----V--------L---Q---V-------------R------D-------------V--------L------V----------R---------G--------------FG------------D----------S-V---E---------------E------------V----------L---S--------------------E------------V-------------R-------------Q-------------------------H--L--------------K-----------D--G-----T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: -M--------L-----A--------P--S-----------P-------------N--S----------K--------------I----Q-----------L---------F------N--------------N-------------I--N-----------I---------D---I--N------------------------Y---EH--------T----------L---------Y---F----------A----------S-V---------------S--A---------Q-------------N---S------F---------------F-------------A----------Q--------------------------------------------------------------------W-----------V-----------------V-Y-----------S----A-D---K--------A-----I-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> ```

> ```
> ----------------
> str23: -M------------S-A--------------------I--------------------T----E-----------T--------K--P---T------I----------E-----L--P------A-----L--------A-E-G---------------------------F-------QR---------------------Y---------N-------------K-------T------------P-------G---------------F----------T--C------------V--------L---------D--------R----Y-D---H----------------G---------V------I---N------------------------D----------S--------K--------------I-----V-----------L-------Y--------N----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str24: -M-------K-N-------------------------I--------A-EF------------------K---------------K---------A-----------------------P--------E---L--------A-E----KL--------------L------------------------E------------V----------------------F---------S------------N-----------L----------------K------------G----N--S--------------RS---------L----------D--------P-------------------------------M------------------R----A----G-K--------------------------------------------H-------------D----------V--------------V---------------V-------I--------------E---------ST--------K----------------KL---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: -M----------P-------------Q-------------P------------L--------------K---Q-S----------L---------D------Q-S---------K--------W-------L---R------E-------------A-E---K-----------H--L---R----A------L-------------E--------S-----------L-------V---D---------S---------N----------------L---------E-------------------------------E---------------E----------------------KL-------------K---PQ-----------L----S---------------------------M--------------------------G-------------------------------E------------D-----------V-------------Q-S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V-----------N--------------L-----------I-------T---------------R-T-----------Q-S--Y-------------T---------N---S-------F----------T--------------R--------G---------VY---------------Y----------P-------D---K-------V-----F----R-----------------S---------------S-V---------L------------H-----ST--------------Q-------D-----------------------------------------------------------------------------------------------------------------------
> ```

> ```
> -------------------------------------------------------------------------------------------------------------------------------------
> str27: -M-------K---------F-------------D----------V--------L---S-----------L-----------F------------A-----------------------P----W-A----K------V---DE--------Q------E--------------------------------------------Y--D-------Q-----------------Q------------L-N------------N-----------------N--------------L-------------------------E--------S----------I-------T--A--------------------------P-----------K-------------F-------------D---------------D----------------G------------A-----------T------E-----------------I----------E-----------S------E--------R--------G-------------D---I-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str28: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V-----------N-----------F--------T--------N--R-T--------------Q------------L----------------P--S---A--------------Y--------------T------------N--S------F---------T-------------R---------G---------VY---------------Y-------------------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H---------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: -M-------------W------------S--------I--------------I------V---------L--------------KL------------I-----S--------I-----Q-------------P--------------L--------------L-------------L------V---------------T---------------S-----------L--P-------------L----------------------Y---------NP--------------N----------------------------------------------M----------D----------S----C-------------------------------C------L------------I------S------------R-----------I------T------------P---------E---L-------A---G-----------------KL------T-W------I-------------F-I----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str30: -M--E---------S--------L------V---------P---------G-------------F-----N---------E---K------T--------------------H------------------------V-------------Q-----------L--S----------L-P----V--------L---Q---V-------------R------D-------------V--------L------V----------R---------G--------------FG------------D----------S-V---E---------------EF---L-----S------E-------------A
> ```

> ```
> --------------------------R---------------Q----------------------------------------H--L--------------K-----------D--G-----T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V----------M-P-------------L---------F----N----------------L-------------I------T---------------T--------------T--------------Q-S--Y--------------T-----------N--------F----------T--------------R-------G---------V-Y------------Y------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H--L-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: -M-----H------------------Q----------I--------------------TV----------------V-------------S------G--------------------P---T----E---------V--------------ST---------------------------------------------------C------------------FG--------S----------L----------------------------H----P--------F------Q-S----------L-------------K--P----V----------M--------A---------N------A------L-----------G----------V---------L--------------------------E---------------G--K-M----------F-------------C--------S----------I------------G------------------G------RS----------L--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: -MA--------------------------T---------L-------------L--RS-----------L--------A------L----------F--K---R-------------N------------K----------D-----K--P----------------------------P-----------I--------T---------------S--------G--------S--------G------------G------------A-----I-----R-------G-IK------------HI--------------------------------I-----------------I-------V-----------P----------I---P-----------G------------D---------S------------------------------S---------I------T--------------T-------------RS----------------R-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: -M--E---------S--------L------V---------P---------G-------------F-----N---------E---K------T--------------------H------------------------V-------------Q-----------L--S----------L-P----V--------L---Q---V-------------R------D--------
> ```

> ```
> -----V--------L------V----------R---------G--------------FG------------D----------S---------------------------M-----------E------------------------------E------------V---------L----S---------------------E----------A---------------------------R-----------------------------Q----------H--L----------------K----------D--G-------T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V-----------N--------------L-----T-------------T-------G---------T-----------Q------------L-P--------------P-------A---------------Y--------------T-----------N--S-----F----------T--------------R-------G---------V-Y------------Y------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H---------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: -MA--------N-------------------------I--------------I-N--------------L-------------------------------------W---------N----------GI-------V------------P-------------M---V-----------Q------D-------------V-----------N----V-A-------------S----------------------I-------T---A--F---K-----S----------------------------------------------------------M---------------I-----------D--------------E-----------T---------------------------------W--D---K---------------K--------------I-------------E-----------A------------------------N----T------------------------------------C----I----S-------------R-----------K-----------------------------------------------------------------------------H-----R--------------N-------------------------------------------------------------------------------------
> str37: -M--------LN-R-----------------------I---Q----------------T----------L----------------------------------------------M-------------K-----T---A--------N----------------------------N------------------------Y---E---------T--------I--------------E---------------I-L---R--------------N---------------------Y-------L---R----------L--------Y------I-----------------I-L-------A--------------------------R-------------N-------------------------E-------------E-G----------------------R----------G---------------IL-------------I-----------Y-D---------------D------N-------------I---------D------------------------S-V----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str38: -MAD--------P---A---G--------T------------------------N----------G--------------E----------------------------E-G----------T-----G----------------------------------------------------------------------------C-------N-----------G-----------W----F-------------------------Y---------------V--E-------------A-------------V--------------V----E----------------------K--------------K------T-----G--------------D--------------A---I------S-----D-------------DE-------N-------------------------E----N-------D---------S----D-------------T-------G-------------E---------------D-----L----V--D-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str39: -M---F-------------
> ```

> ```
> -----------V----F---L----V--------L---------------L-P-------------L------V-----------S----------------S------------Q----------------------------------------------------------------------C------------V-----------N--------------L-----------------R-T---------------R-T-----------Q------------L-P--------------P--S---Y--------------T------------N--S------F---------T-------------R---------G---------VY---------------Y-------------------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H---------------------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: -M--E---------S--------L------V---------P---------G-------------F-----N---------E---K------T--------------------H------------------------V-------------Q-----------L--S----------L-P----V--------L---Q---V---CD-----------V---------L-------V--------------------------R---------G--------------FG------------D----------S-V---E---------------E------------V----------L---S--------------------E--------------A-----------R-------------Q-------------------------H--L--------------K-----------D--G-----T---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: -M---------N------------N-QR----------K-----------------------------K------T--A----------R----------------------------P--S---------------------F-----N--------------M------------L--------------K-----R-----A----------R--------------N--R--V-------------STV-----------S---------------Q------------L-------A-----K----R-------F-------S-----------------------------K------------G--L---------------L----S--------G-----Q--------G----P--------------M-------------KL-----V---------------------------------------------------------M---------A--F----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: -M------------S---------N----------F-----------D-------------A-----I-----R----A------L------V--D---------T--------------------D-------------A--------------Y------KL---------GHI--------------------------------H---M------Y-----------P---------E-G-------T--E-------------Y---------------V--------L---S-----------N----------F--------T----D----------R---------G-------S------------------------------R-------------------------I-------------E---------------G---------V--------------T-----------------------H------TV------H---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: -M------I---------E----L---R-----------------------H-----------E------------V-----------Q--------G----------------------------D----L-----V---------------T-------I----------------N-----V----------------V-----E---------T-------------P---------E----------------------------D------L------------------------D-G---------------F------R------D-F--I-----R----A-----H--L------------I---------------------------C------L--------A------------V---D-------T------E----------T---------------T--------G-L--------D----I--------------------------Y--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: -M---F------------------------V----F---L----V--------L---------------L-P-------------L------V-----------S-
> ```

> ```
> ---------------S------------Q----------------------------------------------------------------------C------------V----------M-P-------------L---------F----N----------------L-------------I------T---------------T---------N-Q-S---Y--------------T------------N--S------F---------T-------------R---------G---------VY---------------Y-------------------------P-------D---K------V------F----RS---------------S-V---------L-------------------------------------------------------------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: -M------------S-------K----------D-----L----V-A---------R---------------Q-----A------L------------------------------M-----T--A---------R----------------------------M-----------K---------AD-F-----------V----------------------F-----------------F--L---------F----------V----------L-----------------------------------------------------W--------------------------K--------A------L----S----------L-P----V-----------P---T------------R-------------------C--------------------------------------------------------Q-----------I-------------D------M-------A-----K----------------KL--S---A------------------G-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str46: -MA-----------S--------L---------------L----------------------------K-----S----------L-----T--------L---------F---K-----R-T------------R-----D---------Q---------------------------P----------------P--------------L--------A-------------S--------G------S-----G----------------G-----------A-----I----R-------G-IK-------------H--------V--------I-----------------I-------V--------L-------------I---P-----------G------------D---------S------------------------------S---------I-------V-------------T-------------RS----------------R-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: -M-----------R----------------V-----------R-------G-IL--R-------------N------------------------------------W-----------Q--------------Q---W------------------------------W-----I---------W--------------T---------------S-----------L--------------G-----------F-----------W-------------------------------------------------------------------------M------------F--------------------M------------I-----------C-----------S-V--------------V--------------------G-----N-------------L------W-------------V--------------TV-------------------Y---------------Y----G--------V-----------P---V-------------------------------------------------------------W-------K-----------E-------------A-------K-----T---------------T----------------------------
> ```

> ```
> ------------------------------------------------------
> str48: -MA---------------------------V---E-----P--------F-----PR----------------R-------------P----------I------T--------------R------------P-----------H----------A---------S--------I------------E------------V----D----------T----------------S--------G-------------I---------------G---------------G-------S---A--G--------S--------------S------E----------------------K------V----F-----------------------------C------L------------I-----------------------------G----------------------------------------------------Q-----A-E-G------------------G-------------E------P-----------------------------N--TV--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: -M---F-------------------------YA------------------H---------A--FG----------------G----------Y-D-------------E-------N-------------L-------------H----------A---------------F------P----------GI-------S----------------STV-A---------N---------D-----------V----------R------------K-----------------------Y------------S-V--------------V---------------S-VY----------N------------K---------------K--------Y---------N-----------I--------V-------K------------------N------------K--------Y---------------------------------------M-------W---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str50: -MA--------N-------------------Y-----------S------------------------K--P---------F---L--------------L-------------------------D--I-------V-----F-----N------------K--------D---IK----------------------------C---I---N--------D-----------S---------------------------------------------------C----------S-------H-------S----D--------------------------------C----------R---Y-----------QS-----------N---S--Y---------------V-------------------E---L-R--------------------------------R-------------N---------------Q-----A-------L-N--------------K--N-------------L--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> solution is feasible: True
> 
> ```


