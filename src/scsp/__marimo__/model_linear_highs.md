In [ ]:
```python
import math
import highspy
import util
```


In [ ]:
```python
import marimo as mo
import nbformat
```


# MILP 定式化 (HiGHS)

数理最適化モデルを用いて SCSP を解く.
定式化については SCIP 版を参照.

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)

        highs = highspy.Highs()

        seqs = [
            [
                highs.addIntegral(lb=0, ub=max_len - 1)
                for idx, _ in enumerate(s)
            ]
            for s in instance
        ]
        for seq in seqs:
            for idx, _ in enumerate(seq):
                if idx == 0:
                    continue
                highs.addConstr(seq[idx - 1] + 1 <= seq[idx])

        for idx1, (s1, seq1) in enumerate(zip(instance, seqs)):
            for idx2, (s2, seq2) in enumerate(zip(instance, seqs)):
                if idx1 >= idx2:
                    continue

                for cidx1, (c1, cvar1) in enumerate(zip(s1, seq1)):
                    for cidx2, (c2, cvar2) in enumerate(zip(s2, seq2)):
                        if c1 != c2:
                            lt = highs.addBinary()
                            gt = highs.addBinary()
                            highs.addConstr(lt + gt == 1)
                            big_m = max_len
                            highs.addConstr(cvar1 + 1 <= cvar2 + big_m * (1 - lt))
                            highs.addConstr(cvar1 + big_m * (1 - gt) >= cvar2 + 1)

        obj = highs.addVariable(lb=0, ub=max_len)
        for seq in seqs:
            highs.addConstr(obj >= seq[-1])
        highs.setObjective(obj=obj, sense=highspy.ObjSense.kMinimize)

        self.instance = instance
        self.highs = highs
        self.seqs = seqs

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.highs.setOptionValue("output_flag", log)
        if time_limit is not None:
            self.highs.setOptionValue("time_limit", time_limit)
        self.highs.solve()
        return self

    def to_solution(self) -> str | None:
        info = self.highs.getInfo()
        primal_status = info.primal_solution_status
        if primal_status != highspy.SolutionStatus.kSolutionStatusFeasible:
            return None

        highssolution = self.highs.getSolution()
        objval = int(self.highs.getObjectiveValue())
        sol_char_idx = 0
        solution = ""
        while sol_char_idx <= objval:
            found = False
            for idx, (s, seq) in enumerate(zip(self.instance, self.seqs)):
                for c_idx, cvar in enumerate(seq):
                    if math.isclose(
                        highssolution.col_value[cvar.index],
                        sol_char_idx
                    ):
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


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> --- Solution (of length 75) ---
>  Sol: tkgnkuhmpxnhtqgxzvxulcinycosovozppljigqfolnbxxecvsuaqpvzissgbxrddbcsvrvnngf
> str1: tkgnkuhmpxnhtqgxzvx---i----s-----------------------------------------------
> str2: ----------------------i---o--------ji-qfolnbxx-cvsu-qpv-iss-bx------------f
> str3: -----u--------------lcinycosovozppl------------------p---------------------
> str4: ----------------------i--------------g--------e-v--a---z---gb-rddbcsvrvnngf
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_02 = util.parse("uniform_q26n008k015-025.txt")
solution_02 = solve(instance_02)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> --- Solution (of length 148) ---
>  Sol: ulcinygevacosovozpplrxwtknbczfjxqkrdrlctodtmprpxwgnkuhmpxnhvxerzbrvigpledcvdpfzsmsbroqvbbhtcsvrvnngyfqgxzplrzxucpmqvgtdfuxisolnbxxcvsuqpvissbxfcdsbo
> str1: -----------------------tk------------------------gnkuhmpxnh-------------------------------t----------qgxz----------v-----xis------------------------
> str2: ---i-------o------------------j------------------------------------i-----------------q--------------f-----------------------olnbxxcvsuqpvissbxf-----
> str3: ulciny----cosovozppl------------------------p-------------------------------------------------------------------------------------------------------
> str4: ---i--geva------z--------------------------------g--------------br------d--d------b--------csvrvnng-f-----------------------------------------------
> str5: -----------------p---------------------------------------------------------------------------------y-----plrzxucpmqvgtdfu-i--------v-----------cdsbo
> str6: -----------------p--------b--------d-------------------------e----v-----dcvdpfzsmsbroqvbbh----------------------------------------------------------
> str7: -------e-----------------nbczfj--------t-------------------vxerzbrvigple----------------------------------------------------------------------------
> str8: --------------------rxw--------xqkrdrlctodtmprpxw-----------------------d---------------------------------------------------------------------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_03 = util.parse("uniform_q26n016k015-025.txt")
solution_03 = solve(instance_03)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> 
> ```



In [ ]:
```python
instance_04 = util.parse("uniform_q05n010k010-010.txt")
solution_04 = solve(instance_04)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> --- Solution (of length 52) ---
>   Sol: dcbacdebadbaaeaebadacbeeadbccdeaeeadcbcdeedacbdbecde
> str01: dcb-c---------------c----dbcc-e---------------------
> str02: --b--d---db--e-e------ee--b--d----------------------
> str03: -c-acde------e------c-e---b---e---------------------
> str04: ---a--e--d--------d------d---de------b-d--d---------
> str05: ---ac--b-----e-e----c---a-bc--e---------------------
> str06: --b----ba-b--e--b-d-cb--a---------------------------
> str07: --b----ba----eaebada--------------------------------
> str08: ------e------e-e------e----c---------b-d-----b--e--e
> str09: -c--cde------e----da-----d-c-d----------------------
> str10: --b--d--a-b-------d--be-a------a---d----------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_05 = util.parse("uniform_q05n050k010-010.txt")
solution_05 = solve(instance_05)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> 
> ```



In [ ]:
```python
instance_06 = util.parse("nucleotide_n010k010.txt")
solution_06 = solve(instance_06)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> --- Solution (of length 32) ---
>   Sol: ATGGGATACGCTTCCCACGGAACTTGCTGTAA
> str01: ATGGGATACG----------------------
> str02: AT---A--C-CTTCCC----------------
> str03: --------C-------ACG-AA-TTG----A-
> str04: -T---A-A--------A---A--T--CTGT--
> str05: A-GG--TA--------AC--AA--------A-
> str06: -T----T-C-CT----A-GG---T------A-
> str07: -T----T--G-T----A-G-A--T--CT----
> str08: -TGGGA-A-G-TTC------------------
> str09: -T----T-C-C-----AC--AACT--------
> str10: -T------C--T----A---AAC--G----AA
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_07 = util.parse("nucleotide_n050k050.txt")
solution_07 = solve(instance_07)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> 
> ```



In [ ]:
```python
instance_08 = util.parse("protein_n010k010.txt")
solution_08 = solve(instance_08)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> --- Solution (of length 66) ---
>   Sol: MALSYCNFDAIQSSLNAIEEHVNELHDPKGTLSYQHFRKAGVTHLVPGFNEAFGGYQNSRRPYQNG
> str01: MALSYC---------------------PKGT-----------------------------------
> str02: M----------QSSLNAI---------P-------------V------------------------
> str03: M--------------------------P---LSYQHFRK---------------------------
> str04: M-----------------EEHVNELHD---------------------------------------
> str05: M--S--NFDAI--------------------------R-A----L---------------------
> str06: M------F-----------------------------R-----------N------QNSR----NG
> str07: M------F-------------------------Y-----A---H-------AFGGY----------
> str08: M--S------------------------K-------F-----T----------------RRPYQ--
> str09: M--S---F-------------V-----------------AGVT--------A----Q---------
> str10: M-----------------E-------------S-----------LVPGFNE---------------
> 
> solution is feasible: True
> 
> ```



In [ ]:
```python
instance_09 = util.parse("protein_n050k050.txt")
solution_09 = solve(instance_09)
```


> ```
> Running HiGHS 1.11.0 (git hash: 364c83a): Copyright (c) 2025 HiGHS under MIT licence terms
> 
> ```



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
> 
> ```


