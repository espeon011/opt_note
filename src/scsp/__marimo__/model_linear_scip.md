In [ ]:
```python
import pyscipopt
```

In [ ]:
```python
import marimo as mo
import nbformat
import util
```

# MILP 定式化 (SCIP)

数理最適化モデルを用いて SCSP を解く. 以下のように定義する.

**決定変数**

- $x_{i,j} \in \mathbb{N} \ (\forall i \in \{ 1, \dots, n \}, \ \forall j \in \{ 1, \dots, |s_i| \})$: $i$ 番目の文字列の $j$ 番目の文字が解において何番目に対応するか.

**制約条件**

- $x_{i,j} < x_{i,j+1} \ (\forall i \in \{ 1, \dots, n \}, \ \forall j \in \{ 1, \dots, |s_i| - 1 \})$
- $i_1, i_2 \in \{ 1, \dots, n\} \ (i_1 \ne i_2)$ と $j_1 \in \{ 1, \dots, |s_{i_1}| \}, \ j_2 \in \{ 1, \dots, |s_{i_2}| \}$ に対し,
  $s_{i_1}[j_1] \ne s_{i_2}[j_2]$ ならば $x_{i_1, j_1} \ne x_{i_2, j_2}$.

**目的関数**

- minimize $\max_{i = 1, \dots, n} x_{i, |s_i|}$

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)

        scip: pyscipopt.Model = pyscipopt.Model()

        seqs = [
            [
                scip.addVar(vtype="I", lb=0, ub=max_len - 1)
                for _ in s
            ]
            for s in instance
        ]
        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                scip.addCons(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
                if idx1 >= idx2:
                    continue

                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            lt = scip.addVar(vtype="B")
                            gt = scip.addVar(vtype="B")
                            scip.addCons(lt + gt == 1)
                            scip.addConsIndicator(cvar1 + 1 <= cvar2, binvar=lt)
                            scip.addConsIndicator(cvar1 >= cvar2 + 1, binvar=gt)

        obj = scip.addVar(vtype="C", lb=0, ub=max_len)
        for seq in seqs:
            scip.addCons(obj >= seq[-1])
        scip.setObjective(obj + 1, sense="minimize")

        self.instance = instance
        self.scip = scip
        self.seqs = seqs

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        if time_limit is not None:
            self.scip.setParam("limits/time", time_limit)
        if not log:
            self.scip.hideOutput()
        self.scip.optimize()

        return self

    def to_solution(self) -> str | None:
        if self.scip.getNLimSolsFound() == 0:
            return None

        objval = int(round(self.scip.getObjVal()))
        sol_char_idx = 0
        solution = ""
        while sol_char_idx <= objval:
            found = False
            for idx, (s, seq) in enumerate(zip(self.instance, self.seqs)):
                for c_idx, cvar in enumerate(seq):
                    if int(round(self.scip.getVal(cvar))) == sol_char_idx:
                        solution += s[c_idx]
                        found = True
                        sol_char_idx += 1
                if found:
                    break
            if not found:
                sol_char_idx += 1

        return solution
```

In [ ]:
```python
def solve(instance: list[str], time_limit: int | None = 60, log: bool = False) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
```

In [ ]:
```python
instance_01 = util.parse("uniform_q26n004k015-025.txt")
solution_01 = solve(instance_01)
```

In [ ]:
```python
_instance = instance_01
_solution = solution_01

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 70) ---
>  Sol: itkgojniqfeokulvahmcnzgpibxxrndycvhodstoqgubcvsoxzvqpzprvxininsgslpbxf
> str1: -tkg--n-----ku---hm----p--x--n----h---t-qg------xzv------xi---s-------
> str2: i---oj-iqf-o--l-----n----bxx----cv---s----u--------qp---v-i---s-s--bxf
> str3: -------------ul----c----i----n-yc--o-s-o-----v-o-z--p-p----------lp---
> str4: i--g------e----va----zg--b--r-d-----d------bc-s---v----rv--n-n-g-----f
> 
> solution is feasible: True
> ```

In [ ]:
```python
instance_02 = util.parse("uniform_q26n008k015-025.txt")
solution_02 = solve(instance_02)
```

In [ ]:
```python
_instance = instance_02
_solution = solution_02

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
> solution is feasible: True
> ```

In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
solution_03 = solve(instance_03)
```

In [ ]:
```python
_instance = instance_03
_solution = solution_03

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
> ```

In [ ]:
```python
instance_04 = util.parse("uniform_q05n010k010-010.txt")
solution_04 = solve(instance_04)
```

In [ ]:
```python
_instance = instance_04
_solution = solution_04

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
>   Sol: eacbeecabcedcedabcdebceacdedbdecabecdabdceade
> str01: -----------dc---bc---c---d--b--c---c-----e---
> str02: ---b-------d--d-b--e--e---e---e--b--d--------
> str03: --c----a-c-d-e-----e-ce-----b-e--------------
> str04: -a--e------d--d---d------de-bd------d--------
> str05: -acbeecabce----------------------------------
> str06: ---b----b------ab--eb----d-----c-b---a-------
> str07: ---b----b------a---e---a--e-b---a---da-------
> str08: e---ee----e-c---b-d-b-e---e------------------
> str09: --c---c----d-e-----e-----d------a---d---c--d-
> str10: ---b-------d---ab-d-b-ea--------a---d--------
> 
> solution is feasible: True
> ```

In [ ]:
```python
instance_05 = util.parse("uniform_q05n050k010-010.txt")
solution_05 = solve(instance_05)
```

In [ ]:
```python
_instance = instance_05
_solution = solution_05

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
> ```

In [ ]:
```python
instance_06 = util.parse("nucleotide_n010k010.txt")
solution_06 = solve(instance_06)
```

In [ ]:
```python
_instance = instance_06
_solution = solution_06

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
>   Sol: TACTATATCGATCAGCTACGCTATAGTCATGCGTCATCGCTA
> str01: -A-T-----G----G----G--ATA--C--G-----------
> str02: -A-TA---C---C---T----T-----C---C--C-------
> str03: --C-A---CGA--A--T----T---G--A-------------
> str04: TA--A-A---ATC---T--G-T--------------------
> str05: -A-------G----G-TA----A----CA------A-----A
> str06: T--T----C---C---TA-G-----GT-A-------------
> str07: T--T-----G-T-AG--A---T-----C-T------------
> str08: T--------G----G----G--A-AGT--T-C----------
> str09: T--T----C---CA-C-A----A----C-T------------
> str10: T-CTA-A---A-C-G--A----A-------------------
> 
> solution is feasible: True
> ```

In [ ]:
```python
instance_07 = util.parse("nucleotide_n050k050.txt")
solution_07 = solve(instance_07)
```

In [ ]:
```python
_instance = instance_07
_solution = solution_07

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
> ```

In [ ]:
```python
instance_08 = util.parse("protein_n010k010.txt")
solution_08 = solve(instance_08)
```

In [ ]:
```python
_instance = instance_08
_solution = solution_08

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
>   Sol: MSEFVAGVLSYCQLVPGKSSNFDAIRLNASYEHVNEQNSAHAKFTRRGTIPVQHFRKLHDLNGGYTAQNE
> str01: M----A--LSYC---P-K-----------------------------GT---------------------
> str02: M-----------Q-----SS------LNA--------------------IPV------------------
> str03: M--------------P----------L--SY-----Q---H--F-R----------K-------------
> str04: M-E----------------------------EHVNE---------------------LHD----------
> str05: MS------------------NFDAIR--A----------------------------L------------
> str06: M--F---------------------R-N--------QNS------R---------------NG-------
> str07: M--F------Y------------A--------H------A---F---G--------------G-Y-----
> str08: MS---------------K---F----------------------TRR---P-------------Y--Q--
> str09: MS-FVAGV------------------------------------T---------------------AQ--
> str10: M-E------S---LVPG----F-----N---E--------------------------------------
> 
> solution is feasible: True
> ```

In [ ]:
```python
instance_09 = util.parse("protein_n050k050.txt")
solution_09 = solve(instance_09)
```

In [ ]:
```python
_instance = instance_09
_solution = solution_09

util.show(_instance)
if _solution is not None:
    util.show(_instance, _solution)
    print(f"solution is feasible: {util.is_feasible(_instance, _solution)}")
else:
    print("--- Solution not found ---")
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
> ```
