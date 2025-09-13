In [ ]:
```python
import util
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# Descending モデル

- 計算量: $O(nk^2)$
- 近似精度: ?

2 つの文字列の shortest common supersequence は動的計画法で計算することができる.
ここでは与えられた文字列を長さが長い順にソートし,
最初の 2 つを shortest common supersequence で置き換える操作を文字列が 1 つになるまで繰り返す.

文字列の集合 $S = \lbrace s_1, s_2, \dots, s_n \rbrace$ はソート済みで $|s_1| \geq |s_2| \geq \dots \geq |s_n|$ を満たしているとする.

- $n_0 = n$ とする.
- $l$ ステップ目において文字列集合が $\lbrace s_1, s_2, \dots, s_{n_l} \rbrace$ であるとする.
- $s_1$ と $s_2$ の shortest common supersequence を求め, $s_1$ をそれで置き換える.
  $s_2$ は削除し, $s_3$ 以降は番号を前に 1 つずらして更新し, $\lbrace s_1, s_2, \dots, s_{n_l - 1}\rbrace$ とする.
- 文字列集合が 1 元集合 $\lbrace s_1 \rbrace$ になったら終了.

この方法が common supersequence を与えるのは $s'$ が $s$ の supersequence であるという 2 項関係 $s \preceq s'$ が推移的 (さらにいえば半順序) であることからいえる.
一方でこの順序関係によって順序集合となった文字配列全体の集合には圏論的な余積 (最小上界) は存在しない.
したがって 2 つずつ shortest common supersequence を取るこの方法では基本的には最適解は得られない.

In [ ]:
```python
def scs2(s1: str, s2:str) -> str:
    """
    2 つの文字列の shortest common supersequence の 1 つを返す. 

    Args:
        s1(str): 文字列 1
        s2(str): 文字列 2
    """

    len1, len2 = len(s1), len(s2)

    dp = [["" for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for idx1 in range(len1 + 1):
        for idx2 in range(len2 + 1):
            if idx1 == 0:
                dp[idx1][idx2] = s2[:idx2]
            elif idx2 == 0:
                dp[idx1][idx2] = s1[:idx1]
            elif s1[idx1 - 1] == s2[idx2 - 1]:
                dp[idx1][idx2] = dp[idx1 - 1][idx2 - 1] + s1[idx1 - 1]
            else:
                if len(dp[idx1 - 1][idx2]) <= len(dp[idx1][idx2 - 2]):
                    dp[idx1][idx2] = dp[idx1 - 1][idx2] + s1[idx1 - 1]
                else:
                    dp[idx1][idx2] = dp[idx1][idx2 - 1] + s2[idx2 - 1]

    return dp[-1][-1]
```

In [ ]:
```python
def solve(instance: list[str]) -> str:
    instance_sorted = sorted(instance, key=lambda s: len(s), reverse=True)

    solution = instance_sorted[0]
    for s in instance_sorted[1:]:
        solution = scs2(solution, s)

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
> --- Solution (of length 64) ---
>  Sol: ulcingycosjieqfoltkvoazgnkbruhmpxnhtqgxzddbcvxsuqplvrissbxvnngfp
> str1: -----------------tk----gnk--uhmpxnhtqgxz----vx-------is---------
> str2: ---i----o-ji-qfol-------n-b-----x-----x----cv-suqp-v-issbx----f-
> str3: ulcin-ycos-----o---vo-z--------p-----------------pl------------p
> str4: ---i-g------e------v-azg--br------------ddbc--s----vr-----vnngf-
> 
> solution is feasible: True
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
> --- Solution (of length 108) ---
>  Sol: igojulcienrxwxqtkvazgfopbcyprddlrnkbzxuhxevdlcompmxnhfjtqvgstodtmprfuiqpxezvxirzsmcdsbroqxwfvinbbhdngzppflpe
> str1: ---------------tk---g------------nk---uh-------mp-xnh--tq-g-------------x-zvxi--s---------------------------
> str2: i-oj---i------q------fo--------l-n-b-x--x----c-----------v-s--------u-qp---v-i--s---sb---x-f----------------
> str3: ----ulci-n----------------y------------------co------------s-o-------------v-----------o-------------zpp-lp-
> str4: ig------e--------vazg---b---rdd----b---------c-------------s---------------v--r-------------v-n----ng---f---
> str5: -----------------------p--yp---lr---zxu------c--pm------qvg-t-d----fui-----v------cdsb-o--------------------
> str6: -----------------------pb----d-----------evd-c-----------v----d--p-f------z-----sm--sbroq---v--bbh----------
> str7: --------en--------------bc----------z----------------fjt-v--------------xe----rz-----br-----vi------g-p--l-e
> str8: ----------rxwxq-k-----------rd--r-----------lc---------t-----odtmpr----px-----------------w-------d---------
> 
> solution is feasible: True
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
> --- Solution (of length 157) ---
>   Sol: ulcingojiekrkiqafiopyplrxiwshtaenpbzlxudxcpmgqtkjwvazgbokksoktrdrenkfjuhiqpavdbiucsilctvxodtmpferzsmqwsbarpeezhkozqczviunbwbhxwanhtqgfmgqdxzvuxijsplpeowwyddm
> str01: -----------------------------t-----------------k-----g------------nk--uh--------------------mp-------------------------------x--nhtqg-----xzv-xi-s-----------
> str02: ---i--oji-----q-f-o---l---------n-b--x--xc--------v-------s-----------u--qp-v--i--s---------------s----b---------------------x-------f-----------------------
> str03: ulcin---------------y--------------------c-------------o--so----------------v------------o-------z--------p---------------------------------------plp--------
> str04: ---i-g---e----------------------------------------vazgb-------rd-------------db--cs----v--------r--------------------v--n-------n---gf-----------------------
> str05: -------------------pyplr-----------z-xu--cpm-q----v--g-------t-d----f-u-i---v----c--------d-------s----b--------o--------------------------------------------
> str06: -------------------p--------------b----d-------------------------e----------vd---c-----v--d--pf--zsm--sb-r------o-q--v---b-bh--------------------------------
> str07: ---------e----------------------n-b------c----------z---------------fj----------------tvx------erz-----b-r-----------vi-------------g-------------pl-e-------
> str08: -----------r------------x-w----------x-------q-k--------------rdr-------------------lct--odtmp--r---------p------------------xw----------d-------------------
> str09: ----------k-k-qafi--------------------------gq--jw-----okks-k-r---------------b-----l-----------------------------------------------g------------------------
> str10: -l----------------------x------------x----p--------a--b-----------------i---v-b--------v---------z-------------koz--zv-------------------d-------------------
> str11: ----------kr-i--f----------s--a-------------------v---------------n--------------c--------d---------qw--------h--z-c-----------------------------------------
> str12: --------------qa--------x-------------ud----gq----v----------------------q-------c-------------e-----w-b-----------------------------f-g-------ij-----owwy---
> str13: -----------r---------------s---------x-------q--j-----------------n-f-----pa-d-iu-si----------------q--b---e-zhko-----------h---------mg---------------------
> str14: ---i----------------------wsh---------------------v--------------------h---------c-------o--m-------------------------iu--------------------v-------------ddm
> str15: ----------------------------ht-------x--x----q--j---z--------------------q----b--c----t----------------ba------k--------n------------------------------------
> str16: ------------------------x-------------u-------------------s---------f------------c------------f--z--------pee------c-v----w----an-t--fmgq--z-u---------------
> 
> solution is feasible: True
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
> --- Solution (of length 37) ---
>   Sol: bbccbdaeeecaedbaccdddebdeacbabcebeebd
> str01: -----d----c---b-ccd---b---c---ce-----
> str02: b----d-------db------e--e------e-e-bd
> str03: --c---a---c--d-------e--e-c----ebe---
> str04: ------ae-----d----dddebd------------d
> str05: ------a---c---b------e--e-c-abce-----
> str06: bb----a-------b------ebd--cba--------
> str07: bb----ae---ae-ba--d------a-----------
> str08: -------eee--e---c-----bd---b---e-e---
> str09: --cc-d-ee----d-a--d-------c---------d
> str10: b----da-------b---d---b-ea--a-------d
> 
> solution is feasible: True
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
> --- Solution (of length 71) ---
>   Sol: bdeadbcdadccbeceaadebddebecdbaecaedaaecdadcedbaaccdddebdeacbabceabeebda
> str01: -d----c-----b-c-----------cdb--c------c----e---------------------------
> str02: bd--db-------e-e---e---eb--d-------------------------------------------
> str03: ------c-a-c-------de---e--c---e--------------b-------e-----------------
> str04: ---a---------e----d--dd----d--e--------------b----dd-------------------
> str05: ---a--c-----be-e----------c--a---------------b--c----e-----------------
> str06: b----b--a---be------bd----c-ba-----------------------------------------
> str07: b----b--a----e--a--eb--------a----da-----------------------------------
> str08: --e----------e-e---e------c-b-----d----------b-------e--e--------------
> str09: ------c---c-------de---e---d-a----d---cd-------------------------------
> str10: bd-a-b-d----be--aad----------------------------------------------------
> str11: --e-d--------e----d----------a--a--a-e--a-----a------------------------
> str12: ---a----a----e--aa--b--e-e---a-c---------------------------------------
> str13: --ea----a---b-c-a---------c----c--d----------b-------------------------
> str14: bde----------e--a-de---------a----d--e---------------------------------
> str15: ------c-a----e----d----------a----d--e-----e---------e-d---------------
> str16: --e--bc-ad--b---a---b---be---------------------------------------------
> str17: -d--d-c------e-ea---bd-e-----a-----------------------------------------
> str18: -d-a-bcd-d---e--a--e------c--------------------------------------------
> str19: ---a----adc--e-e--d----------a--a------------b-------------------------
> str20: ---a---------e-e----------c----c-e---e-----e--aa-----------------------
> str21: b----b-da----ec-aade---------------------------------------------------
> str22: -d-a--c------e----d----------ae---da---------b-------------------------
> str23: ---a----a----e--a---b---b---b----------------b--c----e-----------------
> str24: -de-dbc-----b-c-aa--b--------------------------------------------------
> str25: -d---b-da-------a--eb---b-c-b------------------------------------------
> str26: -de--b-------e----d-b--eb----a-c---------------------------------------
> str27: ------c------e-e----b-----cd---c-------------b----d--e-----------------
> str28: -d---b-------e----d----------a--a-daa--------b-------------------------
> str29: ------c---cc------d-------c-b-e--------------b----d-------c------------
> str30: ---a---------e-ea---------cdb--c-------------b----d--------------------
> str31: -d-a--c-----be--a---------c----c------cd-------------------------------
> str32: --e---c------e------b-----c----c--d----------b----d---b----------------
> str33: -d--db------b-ce--d----------a---------------b--------b----------------
> str34: ---a----a----e--a---b--------a--ae-----------ba------------------------
> str35: --e---c-----b-------b-----c--a--a-d---cd-------------------------------
> str36: -de--bc---c--ec---d-b-----c--------------------------------------------
> str37: -d-a----a-c-b---a--e---eb-c--------------------------------------------
> str38: ---ad---a---be--aa--------c----c-e-------------------------------------
> str39: -d-a---------ec---d-b--------a-ca--a-----------------------------------
> str40: -d-a--c-----b-------bd----c---e---d---c--------------------------------
> str41: -de-db-------e-e----b---b--d--e----------------------------------------
> str42: ------cdadc-------d-------cd-a--a--------------------------------------
> str43: ------c------e-e--d-------c-bae--ed------------------------------------
> str44: ------c------e--a--e------c--a--a--a--c-a------------------------------
> str45: -d----c---cc-e------b---b---ba----d------------------------------------
> str46: b--a---------e-ea--eb---b--d--e----------------------------------------
> str47: -d---b-d-----e------b--------a-c------cd-----b-------------------------
> str48: --e--bc-----be-e--d----------ae-a--------------------------------------
> str49: ---a---------e-e---eb---b--db--ca--------------------------------------
> str50: -d---b-da---b-ce----------c-b----------------b-------------------------
> 
> solution is feasible: True
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
> --- Solution (of length 35) ---
>   Sol: CTGTTCGCATCTAGAGTAGACTACTGTGACCGCAA
> str01: --------AT---G-G--GA-TAC-G---------
> str02: --------AT--A-------C--CT-T--CC-C--
> str03: C-------A-C--GA--A---T--TG--A------
> str04: -T------A---A-A--A---T-CTGT--------
> str05: --------A----G-GTA-AC-A-----A----A-
> str06: -T-T-C-C-T--AG-GTA-----------------
> str07: -T-T--G--T--AGA-T---CT-------------
> str08: -TG---G------GA--AG--T--T----C-----
> str09: -T-T-C-CA-C-A-A-----CT-------------
> str10: -T---C---T--A-A--A--C----G--A----A-
> 
> solution is feasible: True
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
> --- Solution (of length 185) ---
>   Sol: ACTTGACATAGAAGGACCGATTCGTACTGTAACCATGCAGGCATTTACATCAGATGGAACTCTGTCAACAGCATGACTTGAGCGTTAAGCCAATCAACGCAGCTCACGACCGGAAGTGACATGGAAGTCCACTATGATCTTAAACGCATACTGTGTCGCTGACTAGAATCCGACTTCGAARGCCT
> str01: --T--A----G---------T----A--GTA-----G-A--C-T---C--C-G--G-AA----GT-----G-A---C---A-----AA-CC---C--------T---GA----AA---A---G-AA-T-------G---------G-ATA-----------A--A---T---A-T---A------
> str02: ----G-----GA--------T----A----AAC-A--C-----T---C--C--------C---G--AA-A--AT-A----A---TT-------T----G-A-CT------------T-A-A---A---C-A--A----C------GC-----G--------AC-AG--T-----T-C-AA-G---
> str03: A-T--AC---------C---TTC---CT--A-----G--G---T--A-A-CA-A---A-C-C----AAC--CA--ACTT-----TT--G--A-TC--------TC-----------T----TG----T--A----GATCT-----G---------------------------------------
> str04: --T--A-A-A----------TT---A-T--AA---T-C-----TT-A--T-A-------CT-----A---G--T-A----A-----AA---AAT-A--G--G-----G--------TG---T--AA--CC-----GA----AAACG------GT--C----------------------------
> str05: --TT-A-A-A-A----C--A---G--C-----C--TG------T--------G--GG---T-TG-CA-C--C----C---A-C-T----C-A--CA--G--G-----G-CC--------CA-------C---T--G---------G------G---CGC--A--AG-------------------
> str06: A-T-GAC-T-----------T-C---C---AA---TG--G--AT---C--C--------C------AAC--C-T--C---A-----A-GC---T---------TC-C-ACC--------C--------C-A--ATG---------G--T--T-T--C----A---G---C---------------
> str07: A----ACA-A-A----CC-A-----AC-----C-A---A--C-TTT---T--GAT----CTCT-T-----G--T-A---GA---T----C---T----G----T------------T--C-T------C---TA--A----A--CG-A-AC----------------------------------
> str08: A-T-GA-A-A-A----C-GA-----A----AA---T-------T--A--T----T--A--TC----AA--G---G----G----T-A------T----G--G---A--A--G----TG----G-AAG-C---T--GA-C------G-A-A-----------A-T---------------------
> str09: ACT---C---G--G--C---T--G--C---A----TGC-----TT-A-----G-TG---C------A-C----T--C---A-CG-----C-A------G----T-A----------T-A-AT-----T--A--AT-A----A--C---TA-----------A-T----T---A------------
> str10: --TTG---TAGA--------T-C-T---GT-----T-C-----T---C-T-A-A---A-C---G--AAC----T---TT-A-----AA---A-TC--------T---G--------TG---TGG----C---T--G-TC--A--C---T-C----------------------------------
> str11: ----G-CA--GA-G--C--ATT--T--T----C--T--A---AT--A--TC--------C------A-CA--A--A----A---T---G--AA-----G--GC--A--A-------T-A-AT-----T-------G-T---A--C---TACT----C----------------------------
> str12: A-T-GA----G-----CC-A-----A--G-A----T-C---C----------GA-----C---G--AA--G-A-G-C-----C------CCAA-----G--G---A-G---G-A-G--A-A-GGA-G--------G---------G-A--C-----C-C---C------C---------------
> str13: --T---C-T-------C--A--C--A--GT-----T-CA---A---------GA---A-C-C---CAA-AG--T-AC-----C------CC---C--C--A--T-A-G-CC--------C-T------C---T-T-A----AA--GC---C----------AC----------------------
> str14: A---G-----G---------TT--TA-T--A-CC-T-------T---C--C---T--A-----G------G--T-A----A-C---AA---A--C--C--A----AC--C---AA----C-T-----T----T-----C------G-AT-CT----C--T---T-G--T---A------------
> str15: A---G-----G---------TT--TA-T--A-CC-T-------T---C--C--------C------A---G---G--T--A-----A--C-AA--A-C-CA----AC--C---AA----C-T-----T----T-----C------G-AT-CT----C--T---T-G--T---A------------
> str16: --T--A-A-A-A----C--A-----ACT----C-A---A----T--ACA--A-------C------A------T-A----AG----AA---AATCAACGCA----A--A----AA----CA-------C---T-----C--A--C--A-A-----------A-----------------------
> str17: -C----C---G-----CC----C--A-T-T-----TG--GGC----------G--G---CTCT--C----G-A-G-C--GA---T-A-GC---TC---G----TC--GA----A--T--C--------CC--T-----C------G-A--C-----C--T-------------------------
> str18: A-T--AC---------C---TTC---C-----C-A-G--G---T--A-A-CA-A---A-C-C----AAC--CA--ACTT-----T----C--------G-A--TC-----------T--C-T-----T-------G-T---A---G-AT-CTG--------------------------------
> str19: --T---C-T-------C--A--C--A--GT-----T-CA---A---------GA---A-C-CT--CAA--G--T--CT----C------CC---C--C--A--T-A-G---G-------C--------C---T-----CTT-------T-C----------A---G--TC--A----G-------
> str20: ----GA--T-------C---T-C-T-CT----C-A--C---C----------GA---A-C-CTG------GC----C-----C------C--------G--G-----G-C---AA---A--TG-----CC-CTA--ATC-----C--A----G--------A---G-----G--T--G-------
> str21: A---GA----G-----C--A-----A-T----C-A-G------T--------G------C------A------T--C---AG----AA---A-T-A-------T-AC--C------T-A--T-----T--A-TA----C--A--C---T--T-TG-C--T-A--AGAAT----------------
> str22: A----A--T-----------T----A----AA--A--CA----T---C-TCA-AT--A-C------AACA---T-A----AG----AA---AA--A-C--A----ACG-C---AA---A-A---A---C-ACT-----C--A------T------------------------------------
> str23: A----A-A--------C-GA-----ACT-T-----T--A---A---A-ATC---TG----T--GT-----G---G-CT-G----T----C-A--C--------TC--G---G-------C-TG-----C-A-T--G--CTTA---G--T---G---C----------------------------
> str24: A-T--A-A--------C---T----A----A----T-------T--AC-T--G-T----C---GT--------TGAC---AG-G--A--C-A--C---G-AG-T-A--AC------T--C--G----TC---TAT---CTT---C---T---G--------------------------------
> str25: A-T-GA----G---------T--GT-C---A-C---G-A---ATT--CA-C-G-T--A-C------AA-----TGA----A-C-T---G---------G-A--T---G--------T----T------C-AC---G-T-------G------G--------A--A---T---A-----A------
> str26: AC----C---G---------T--G----G-------GC-G--A---------G------C---G------G--TGAC-----CG----G----T----G----TC-----------T----T------CC--TA-G-T-------G------G-GTC-C---C-A----C-G--TT-GAAR----
> str27: A----A-A--G--G------TT--TA-T--A-CC-T-------T---C--C--------C------A---G---G--T--A-----A--C-AA--A-C-CA----AC--C---AA----C-T-----T----T-----C------G-AT-CT----C--T---T-G-------------------
> str28: A---G---TAG---------TTCG--C-----C--TG------T--------G-TG-A-----G-C-------TGAC---A-----AA-C---T---------T-A-G--------T-A---G----T-------G-T-TT----G--T---G--------A---G-----GA-TT--A------
> str29: --TT----TA----------T----AC-----C--T-------T---C--C---T--A-----G------G--T-A----A-C---AA---A--C--C--A----AC--C---AA----C-T-----T----T-----C------G-AT-CT----C--T---T-G--T---A----GA-----T
> str30: A-T-G-C---G--G------T-CGT-CT----C--T-C---C-----C--C-G--G---CT-T-T--------T---TT-----T----CC---C--CGC-GC-C--G-C-G----T----TGG----C------G--C-----CG-A-------------------------------------
> str31: ----G---T-GA----C--A-----A----AA--A--CA----T--A-AT--G--G-A-CTC---CAACA-C----C---A---T---G----TCAA-GC---T------------T----T------C-A----G---------G--TA--G--------AC----------------------
> str32: ----G---T-G---------T----A----A-----G-A---A---ACA---G-T--AA----G-C--C--C--G----GA-----A-G----T----G--G-T---G--------T----T-----T----T--G--C------G-AT--T-T--CG---A---G-----G-C--CG---G---
> str33: ----GA----GAA-------T--G-A--GT--C--T-CA----TT-AC--C-G------C-C---C----G---G--T--A-C-TTA-GC-AA-----GC---T-A--A-------T-A---G----TC-AC---G---------GC--------------------------------------
> str34: A-T-G---T-G--G------T-CG-A-TG---CCATG--G--A---------G--G---C-C---CA-C--CA-G--TT---C---A------T---------T-A--A--GG------C-T------CC--T--G---------GCAT--T---------------------------------
> str35: AC--GA----G-----C-G-TT--T--T--AA----G--GGC-----C--C-G------C---G--A-C----TG-C--GA-CG----GCCA--CA-------T---G---G-------C--------CC--T--G-T---A------T---GT-------------------------------
> str36: ----G-----G---------TT--TA-T--A-CC-T-------T---C--C--------C------A---G---G--T--A-----A--C-AA--A-C-CA----AC--C---AA----C-T-----T----T-----C------G-AT-CT----C--T---T-G--T---A----G-------
> str37: --T-G-----G--G-A---A---GT--T----CCA---A---A---A-----GAT----C------A-CA--A--A----A-C---A--C---T-A-C-CAG-TCA--ACC-----TGA-A-G----T--AC-A----C----------------------------------------------
> str38: ----GA-A--G-----C-G-TT---A----A-C---G------T--------G-T-----T--G--A---G---GA----A-----AAG--A--CA--GC---T------------T-A---GGA-G---A--A----C--AA--G-A----G---C--TG----G-----G-------------
> str39: AC----CA--G-----C-G---C--ACT-T--C---G--G-CA---------G------C---G------GCA-G-C---A-C------C---TC---G--GC--A-G-C---A-----C--------C---T-----C--A---GCA----G---C----A--A----C---------------
> str40: A-T-G-----G--G-AC--A-----ACT-TA----T-------T---C--C---T--A--TC----A------TG--T-G--C------C-AA-----G-AG-----G--------T----T-----T----TA----C-----C-C-----G-GT-G---AC------C--A------------
> str41: --TTG---TAGA--------T-C-T---GT-----T-C-----T---C-T-A-A---A-C---G--AAC----T---TT-A-----AA---A-TC--------T---G--------TG---TGG---T----T--G-TC--A--C---T-C----------------------------------
> str42: A----AC---------C--A-----AC-----C-A---A--C-TTT-C----GAT----CTCT-T-----G--T-A---GA---T----C---T----G----T------------T--C-T------C---TA--A----A--CG-A-ACT-T-T-----A-----------------------
> str43: ----G-----G--G------TTC-T---G---CCA-G--G-CAT--A-----G-T----CT-T-T--------T---TT-----T----C---T----G--GC----G---G-------C--------CC--T-TG-T-------G--TA-----------A--A----CC---T--G-------
> str44: ----G-----G-----C---T--G--C---A----TGC-----TT-A-----G-TG---C------A-C----T--C---A-CG-----C-A------G----T-A----------T-A-AT-----T--A--AT-A----A--C---TA-----------A-T----T---ACT--G------T
> str45: --T-G-CAT-G-----C---TT---A--GT------GCA--C-T---CA-C-G------C------A---G--T-A-T--A-----A------T---------T-A--A-------T-A-A-------C---TA--AT-T-A--C---T---GT--CG-T-------------------------
> str46: --TT--C---------C--A--C--A----A-C--T-------TT--C--CA-------C-C----AA--GC-T--CT-G--C---AAG--A-TC--C-CAG---A-G--------T--CA-GG--G--------G--C-----C---T---GT-------------------------------
> str47: --T---C-TA-AA---C-GA-----ACT-T-----T--A---A---A-ATC---TG----T--GT-----G---G-CT-G----T----C-A--C--------TC--G---G-------C-TG-----C-A-T--G--CTTA---G---------------------------------------
> str48: AC----C---G--G-A----T--G----G---CC--GC-G--ATTT---T----T----C---G------G-A-G--T----C------C---T---------T---G---GG--G-GAC--------C-ACT-----C--A---G-A-A-T---------A---GA------------------
> str49: -CTTG---TAGA--------T-C-T---GT-----T-C-----T---C-T-A-A---A-C---G--AAC----T---TT-A-----AA---A-TC--------T---G--------TG---TGG----C---T--G-TC--A--C---T------------------------------------
> str50: A-T-GA----G-----C--A--C-TA----A-----GC-G--A---A-----GA---A-C-C----AA-A--A--A---G--C---A-G--A--CAA------T-AC-A----A-----C--------CC-----G--CT-A------T--T---------AC----------------------
> 
> solution is feasible: True
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
> --- Solution (of length 53) ---
>   Sol: MSKFTRREMEPNQNSRALMSYAQCLHVPNFDAGIPVTELHDFRAKGGTLYQNE
> str01: M---------------AL-SY--C---P----------------KG-T-----
> str02: M-----------Q-S----S----L---N--A-IPV-----------------
> str03: M---------P------L-SY-Q--H---F------------R-K--------
> str04: M------E-E---------------HV-N--------ELHD------------
> str05: MS---------N-----------------FDA-I--------RA----L----
> str06: M--F-R-----NQNSR------------N---G--------------------
> str07: M--F----------------YA---H-----A---------F---GG--Y---
> str08: MSKFTRR---P---------Y-Q------------------------------
> str09: MS-F----------------------V----AG--VT------A------Q--
> str10: M------E------S--L--------VP----G--------F---------NE
> 
> solution is feasible: True
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
> --- Solution (of length 458) ---
>   Sol: MFSMYAHWKMNSLIMAINYVMFPMQMDMESPLKMLIDNMSFPMRWNTAVARPMFLDGEKIVQKTAPETIDKMLMDIRPHTAVQSLFNWERMLKRTGMAFDMFYHRLNRINDGIEKCTHVYSPSQQVTGNWWDLSLAITKWPNGVDYREHRLQDRKAFVSIPGTCIKLYPSGFASEQQYDACTNLQGWFYVESVHKKAKRNEKLPQLNDSFMTGNVLWHISPEDLDVEKALGRGFQSKHMSEYNEQWLARCKVDGTPPSEGDSIVAWFETCMLILYHRRLEFANDYSPTSRCGQEPLWKHAVRLYTFDRFIKILDSEGAGNFRTCSVQLIPMLPSAYNEVGDKTANDIEGSDLRFHFWTPRGVYILNADETKHRIMFIRIVSGYPICDQAYGYFQLRDKVPSQHLTWANIVRLPYAQWKSMGEDHGSNVFQARPKYMWSITSVLAHLISTVAIRSQDRH
> str01: M------------------------------------------R----------------------------------H-----L-N---------------------I-D-IE--T--YS-S-----N--D----I-K--NGV-Y--------K------------Y----A-----DA----------E----------------D-F-----------E----------------------------------------I--------L-L------FA--YS-----------------------I---D--G-G------------------EV--------E-------------------------------------C--------L-D------LT-----R-----------------------------------------------
> str02: M---------------------------E--------------R------R-------------A-------------H----------R----T--------H-------------------Q----NW-D---A-TK-P-----RE-R---RK--------------------Q-----T--Q--------H----R---L--------T-----H--P-D-D----------S--------------------------I-----------Y-----------P--R-------------------I-----E-------------------------K-A---EG---R-----------------K--------------------------------------------------EDHG---------------------------------
> str03: M---------------------------E-P-------------------------G-------A--------------------F----------------------------------S-----T--------A--------------L-----F---------------------DA---L-----------------------------------------------------------------C--D-------D-I--------L---HRRLE-----S------Q--L-----R---F----------G-G------VQ-IP--P----EV----------SD-------PR-VY---A--------------GY-----A-----L--------L------------------------------------------------------
> str04: M-------------------------------------------------------G-K--------------------------F----------------Y----------------YS-------N-----------------R--RL----A-V-------------FA--Q---A----Q------S------R------------------H-----L------G-G--S-----Y-EQWLA-C-V-----S-GDS--A-F---------R----A-----------E------V---------K------A---R---VQ--------------K---D----------------------------------------------------------------------------------------------------------------
> str05: -F-------------------F---------------------R-------------E----------------------------N----L-----AF------------------------QQ--G----------K----------------A------------------------------------------R-E--------F----------P--------------S----E--E---AR---------------A-----------------N--SPTSR---E-LW---VR-----R--------G-GN---------P-L-S---E-----A----G-----------------A-E---R----R---G----------------------T-----------------------------------------------------
> str06: M-------------------------D---P--------S--------------L--------T------------------Q-----------------------------------V----------W-----A-------V---E-------------G-------S-------------------V------------L-----S-------------------A------------------A---VD-T---------A--ET-------------ND---T-----EP-----------D--------EG----------L-----SA--E------N--EG-------------------ET--RI--IRI-------------------------T---------------G----S--------------------------------
> str07: M----A---------------F----D-------------F------------------------------------------S----------------------------------V-------TGN--------TK-----------L-D---------T------SGF---------T--QG---V-S----------------S-MT--V-------------A------------------A-----GT----------------LI--------A-D-----------L----V---------K-----------T-----------A--------------S------------------------------S------Q------L---------T--N---L--AQ--S---------------------------------------
> str08: M----A-------------V---------------I------------------L----------P-----------------S----------T-------Y-------------T--------------D----------G-------------------T---------A------ACTN--G-----S-----------P---D------V----------V----G-----------------------T----G--------T-M-------------------------W---V------------------N--T-----I--LP------GD------------F-FWTP---------------------SG---------------------------------------E---S-V---R---------V----------------
> str09: M---------N-----------------------------------T---------G--I--------ID--L------------F-------------D------N----------HV------------D-S--I---P---------------------T-I-L-P------------------------H----------QL----------------------A-------------------------T----------------L-----------DY----------L----VR--T----I-I-D-E---N-R--SV-L---L---------------------FH--------I----------M------G------------------S-------------------G-------------------------------------
> str10: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N--L----------------------------R----------------------T---------------------R----------T----Q--L---------------------------------P--P-AY------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--S----------
> str11: M-------------------------D--S--K------------------------E-----T----I---L--I------------E-------------------I---I--------P----------------K--------------------I-----K---S-------Y-----L------------------L----D---T-N----ISP------K-------S-----YN---------D-------------F-----I------------S---R-----------------------------N---------------------K--N-I------F-------V-I-N----------------------------L------------------Y------------NV---------S-T------I-----------
> str12: M-----------L------------------L-------S----------------G-K---K-------KML-----------L--------------D------N------------Y---------------------------E--------------T---------A------A----------------A-R-------------G------------------RG--------------------G------D------E--------RR-----------R-G----W--A-----FDR---------------------P----A-----------I--------------V-------TK-R-------------D----------K--S---------------------D--------R---M-------AH-------------
> str13: M---------N---------------------------------------------GE--------E--D----D-----------N-E----------------------------------Q-----------A-------------------A----------------A-EQQ----T------------KKAKR-EK-P-----------------------K------Q------------AR-KV--T--SE-----AW-E-------H----F--D---------------A----T-D------D--GA-------------------E-----------------------------------------------C-----------K----H-------------------------------------------------------
> str14: M---------------------------ES-L----------------V--P----G----------------------------FN-E---K-T--------H--------------V----Q--------LSL-----P--V------LQ-----V----------------------------------------R--------D------VL---------V-----RGF-------------------G------DS-V---E-----------E--------------------V-L-----------SE-A---R----Q---------------------------H---------L-----K---------------D---G-------------T-----------------------------------------------------
> str15: M------------------------------------------R----------------------------------------------------------Y-----I---------V-SP-Q--------L----------V------LQ-----V---G---K----G----Q--------------E-V-------E------------------------------R---------------A-----------------------L--Y---L--------T------P--------Y--D----------------------------Y----------I---D-----------------E-K---------S--PI----Y-YF-LR----S-HL---NI------Q---------------RP-------------------------
> str16: M---------------------P--------------------R----V--P--------V-----------------------------------------Y-------D---------SP-Q-V-------S------PN--------------------T--------------------------V-------------PQ-----------------------A--R--------------LA------TP-S--------F--------------A-----T------P---------TF-R--------GA----------------------D--A--------------P-------A--------F-----------Q--------D-------T-AN-------Q-------------QAR----------------------Q---
> str17: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N--L----------------------------R----------------------T---------------------R----------T----Q--L---------------------------------P-L--AY------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--S----------
> str18: MF-----------------V-F------------------F-------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N--L--------T------------------------------------------T---------------------R----------T----Q--L---------------------------------P--P-AY------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--S----------
> str19: M---------------------------E------------------A-----------I--------I--------------S-F-----------A-------------GI--------------G--------I----N---Y--------K----------KL--------Q---------------S--K-------L-Q------------H----D----------F-------------------G----------------------R-----------------------V-L-------K------A---------L--------------T------------------V-------T------------------A------R----------A----LP-------G--------Q--PK----------H-I---AIR-Q---
> str20: M----A-----S-----------------S--------------------------G--------PE---------R---A-------E--------------H-------------------Q------------I----------------------I------L-P-----E----------------S-H--------L-----S----------SP--L-V-K---------H------------K--------------------L-LY---------Y-----------WK----L-T-----------G----------L-P-LP-------D------E-------------------------------------CD-----F---D-----HL----I-------------------------------------------------
> str21: M---------------------------ES-L----------------V--P----G----------------------------FN-E---K-T--------H--------------V----Q--------LSL-----P--V------LQ-----V----------------------------------------R--------D------VL---------V-----RGF-------------------G------DS-V---E-----------E--------------------V-L-----------SE---------V--------------------------R----------------------------------Q--------------HL-------------K----D-G--------------T------------------
> str22: M-----------L--A------P------SP------N-S------------------KI-Q----------L------------FN-------------------N-IN--I------------------D----I----N---Y-EH-------------T---LY---FAS---------------V-S----A-------Q-N-SF-----------------------F-------------A--------------------------------------------Q---W---V------------------------V---------Y-------------S----------------AD--K-----------------A-------------------I-------------------------------------------------
> str23: M-S--A-------I--------------------------------T----------E-----T------K------P-T----------------------------I----E------------------L-------P--------------A----------L-----A-E----------G-F----------------Q--------------------------R---------YN-------K---TP---G------F-TC------------------------------V-L---DR---------------------------Y----D-------------H-----GV-I-N-D------------S----------------K----------IV-L-Y------------N-------------------------------
> str24: M-------K-N--I-A------------E-----------F-----------------K---K-APE-----L-------A-------E---K------------L--------------------------L--------------E---------V-------------F-S--------NL----------K-----------------GN-----S-----------R---S----------L-----D--P--------------M-----R----A---------G-----KH-------D------------------V------------V----------------------V-I----E-----------S-----------------------T------------K---------------K--------L---------------
> str25: M---------------------P-Q-----PLK----------------------------Q---------------------SL--------------D-----------------------Q---------S----KW----------L--R--------------------E----A----------E---K----------------------H-----L-------R---------------A-----------------------L-------E-----S---------L----V-----D-------S----N-------L---------E---------E--------------------E-K-----------------------L--K-P-Q-L--------------SMGED----V-Q-------S--------------------
> str26: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N--L---------------I-----------------------------------T---------------------R----------T----Q---------------------S--------------------Y------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--ST-----QD--
> str27: M-------K------------F----D---------------------V-----L----------------------------SLF-----------A-----------------------P-------W-----A--K----VD--E---Q----------------------E--YD-----Q-------------------QLN------N----------------------------N---L-----------E--SI-----T------------A----P----------K-------FD------D--GA----T--------------E--------IE-S------------------E---R--------G----D---------------------I-------------------------------------------------
> str28: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N---------F-T-N-----------------R----------------------T-------------------------------------Q--L---------------------------------P---SAY------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--S----------
> str29: M------W---S-I--I--V-----------LK-LI---S-------------------I-Q---P------L-----------L------L--------------------------V-------T------SL-----P---------L----------------Y--------------N--------------------P--N---M-----------D------------S-------------C-------------------C-LI------------S---R-------------------I------------T------P-------E-------------L--------------A--------------G---------------K-----LTW--I-------------------F---------I-------------------
> str30: M---------------------------ES-L----------------V--P----G----------------------------FN-E---K-T--------H--------------V----Q--------LSL-----P--V------LQ-----V----------------------------------------R--------D------VL---------V-----RGF-------------------G------DS-V---E-----------EF--------------L------------------SE-A---R----Q---------------------------H---------L-----K---------------D---G-------------T-----------------------------------------------------
> str31: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V--------------------M---------P--L---------F--------N---L---------------I-----T------------------T----------------T---------------------Q------S-Y------T-N--------F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-HL------------
> str32: M-----H-----------------Q----------I----------T-V-----------V----------------------S-----------G-------------------------P----T--------------------E---------VS---TC-------F-------------G-----S----------L--------------H--P------------FQS----------L---K----P-------V------M----------AN----------------A--L-------------G--------V-L---------E-G-K--------------------------------MF---------C--------------S-------I-----------G---G------R-----S----L---------------
> str33: M----A----------------------------------------T-------L-----------------L---R------SL------------A-------L--------------------------------------------------F--------K--------------------------------RN-K-----D-------------------K---------------------------PP-----I-----T----------------S-----G----------------------S-G-G---------------A-----------I-----R-------G--I------KH-I--I-IV---PI--------------P--------------------G-D--S-----------SIT--------T---RS--R-
> str34: M---------------------------ES-L----------------V--P----G----------------------------FN-E---K-T--------H--------------V----Q--------LSL-----P--V------LQ-----V----------------------------------------R--------D------VL---------V-----RGF-------------------G------DS--------M--------E-------------E------V-L-----------SE-A---R----Q---------------------------H---------L-----K---------------D---G-------------T-----------------------------------------------------
> str35: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N--L--------T------------------------------------------T----G--------T-----------------------Q--L---------------------------------P--P-AY------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--S----------
> str36: M----A----N--I--IN-------------L------------WN----------G--IV----P-----M---------VQ----------------D------------------V---------N--------------V-----------A--SI--T---------A--------------F------K-------------S-M-------I---D---E---------------------------T----------W-----------------D-------------K------------KI---E-A-N--TC----I----S------------------R-----------------KHR----------------------------------N--------------------------------------------------
> str37: M-----------L----N-------------------------R---------------I-Q-T--------LM------------------K-T--A--------N--N---------Y---------------------------E--------------T-I---------E-------------------------------------------I----L-------R----------N-------------------------------Y---L----------R-----L-------Y-----I-IL----A---R--------------NE---------EG---R-------G--IL--------I--------Y---D---------D----------NI-------------D--S-V------------------------------
> str38: M----A--------------------D---P----------------A--------G------T----------------------N--------G-----------------E---------------------------------E-------------GT-------G---------C-N--GWFYVE-----A-----------------V----------VEK--------K-----------------T----GD---A-------I------------S--------------------D------D-E---N-----------------E------ND---SD------T--G-------E-----------------D-------L---V-----------------------D-----------------------------------
> str39: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V---------N--L----------------------------R----------------------T---------------------R----------T----Q--L---------------------------------P--PS-Y------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H--S----------
> str40: M---------------------------ES-L----------------V--P----G----------------------------FN-E---K-T--------H--------------V----Q--------LSL-----P--V------LQ-----V-----C--------------D----------V------------L-----------V----------------RGF-------------------G------DS-V---E-----------E--------------------V-L-----------SE-A---R----Q---------------------------H---------L-----K---------------D---G-------------T-----------------------------------------------------
> str41: M---------N------N------Q------------------R--------------K---KTA-----------RP-----S-FN---MLKR---A------R-NR----------V-S-----T----------------V--------------S----------------Q-------L------------AKR----------F---------S-------K--G---------------L------------------------L-------------S-----GQ-----------------------G------------PM----------K---------L---------V------------M-------------A---F-----------------------------------------------------------------
> str42: M-S-------N----------F----D--------------------A-----------I----------------R---A---L---------------------------------V------------D-----T------D----------A-----------Y--------------------------K-------L---------G----HI------------------HM--Y-------------P--EG--------T----------E----Y---------------V-L-----------S----NF-T-----------------D-----------R-------G-------------------S--------------R------------I------------E--G--V-----------T----H---TV-------H
> str43: M------------I--------------E--L-----------R----------------------------------H---------E-----------------------------V----Q---G---DL----------V------------------T-I-----------------N------V--V-------E----------T--------PEDLD-----G--F--------------R---D-------------F-----I---R----A----------------H---L------I-------------C---L------A---V-D-T----E---------T-----------T-----------G------------L-D-----------I----Y--------------------------------------------
> str44: MF-----------------V-F---------L----------------V-----L-----------------L----P------L---------------------------------V-S-SQ---------------------------------------C-------------------------V--------------------M---------P--L---------F--------N---L---------------I-----T------------------T-------------------------------N------Q------S-Y------T-N----S---F---T-RGVY-------------------YP--D----------KV-----------------------------F--R-----S--SVL-H-------------
> str45: M-S-----K-----------------D----L----------------VAR----------Q--A-------LM-----TA--------RM-K----A-D-F----------------V-------------------------------------F--------------F-----------L---F-V------------L-------------W----------KAL-----S----------L--------P-------V----------------------PT-RC-Q----------------I---D----------------M---A------K----------------------------K-----------------------L-----S-----A-------------G-------------------------------------
> str46: M----A-----SL------------------LK------S--------------L--------T--------L------------F------KRT---------R-----D------------Q----------------P-------------------P-----L-----AS-----------G-----S--------------------G-----------------G----------------A--------------I-------------R--------------G-----------------IK-------------------------------------------H------V-I---------I-----V--------------L-------------I---P-------G-D--S-----------SI--V------T---RS--R-
> str47: M------------------------------------------R----V-R-----G--I------------L---R---------NW-----------------------------------QQ----WW-----I--W----------------------T------S-------------L-G-F----------------------------W---------------------M---------------------------F---M-I-----------------C-----------------------S----------V------------VG----N------L----W----V-------T---------V--Y------YG-------VP---------V------WK---E--------A--K-----T--------T---------
> str48: M----A-------------V--------E-P---------FP-R------RP-------I---T------------RPH-A--S------------------------I----E----V------------D-----T--------------------S--G--I-----G--------------G-----S----A---------------G------S---------------S----E---------KV--------------F--C-LI------------------GQ------A---------------EG-G------------------E--------------------P------N---T---------V------------------------------------------------------------------------------
> str49: MF--YAH--------A-----F----------------------------------G--------------------------------------G------Y-------D--E--------------N---L---------------H------AF---PG--I----S---S-------T-------V------A--N-------D------V----------------R----K----Y---------------S-----V------------------------------------V-------------S----------V---------YN----K----------------------------K-----------Y------------------------NIV-------K--------N------KYMW---------------------
> str50: M----A----N-------Y----------S--K--------P-----------FL-----------------L-DI-----V---FN-----K------D--------I-----KC--------------------I----N--D-------------S----C-----S-----------------------H--------------S-------------D--------------------------C--------------------------R-------Y-------Q---------------------S----N----S----------Y--V--------E---LR------R-----N---------------------QA-----L------------N---------K--------N---------------L---------------
> 
> solution is feasible: True
> ```
