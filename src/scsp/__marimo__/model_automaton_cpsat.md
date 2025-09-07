In [ ]:
```python
from ortools.sat.python import cp_model
import util
```


In [ ]:
```python
import marimo as mo
import nbformat
```


# オートマトン制約を用いた数理計画モデル

CP-SAT 固有のオートマトン制約を用いて定式化してみる.

**定数**

- $\Sigma = \{ \sigma_1, \dots, \sigma_q \}$: 文字の集合

**決定変数**

- $x_i \in \mathbb{Z}$: 解において $i$ 番目の文字が $\sigma_j$ であれば $j$ となる.
  どの文字も対応しないとき $0$.
  このとき解は $\sigma_{x_0} \sigma_{x_1} \dots$ となる.
  ただし $\sigma_0$ は空文字列とする.

- $v_i \in \{ 0, 1 \}$: 解の $i$ 番目が空でないとき $1$. 空のとき $0$.

**制約条件**

- $x_i > 0 \Rightarrow v_i = 1$
- 与えられた文字列 $s \in S$ の各文字を $\Sigma$ を基準にインデックスの配列としたものを $\mathrm{index}_s$ とする.
  $\mathrm{index}_s$ を部分配列にもつすべての配列を受理するオートマトンを文字列の数だけ作成し,
  $\{ x_i \}_i$ が受理されるという制約を課す.

**目的関数**

- minimize $\Sigma_{i} v_i$

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        max_len = sum(len(s) for s in instance)
        chars = sorted(list(set("".join(instance))))

        cpmodel = cp_model.CpModel()

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="")
            for _ in range(max_len)
        ]

        for s in instance:
            transition_triples = (
                [
                    (idx, jdx + 1, (idx + 1 if c == next_char else idx))
                    for idx, next_char in enumerate(s)
                    for jdx, c in enumerate(chars)
                ]
                + [(idx, 0, idx) for idx, _ in enumerate(s)]
                + [(len(s), 0, len(s))]
                + [(len(s), jdx + 1, len(s)) for jdx, _ in enumerate(chars)]
            )
            cpmodel.add_automaton(
                transition_expressions=cvars,
                starting_state=0,
                final_states=[len(s)],
                transition_triples=transition_triples,
            )

        valids = [cpmodel.new_bool_var("") for _ in cvars]
        for cvar, valid in zip(cvars, valids):
            cpmodel.add(cvar == 0).only_enforce_if(~valid)
        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {cp_model.cp_model_pb2.OPTIMAL, cp_model.cp_model_pb2.FEASIBLE}:
            return None

        solution = ""
        for cvar in self.cvars:
            cidx = self.cpsolver.value(cvar) - 1
            if cidx >= 0:
                solution += self.chars[cidx]

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
> --- Solution (of length 65) ---
>  Sol: ulcignevazgbrdydbcosjoviqfotlnzkbxxgpcrvnksuhmpxlnhtqgxzpvxissbxf
> str1: ---------------------------t---k---g----nk-uhmpx-nhtqgxz-vxis----
> str2: ---i--------------o-j--iqfo-ln--bxx--c-v--su--------q---pv-issbxf
> str3: ulci-n--------y--cos-ov---o---z-----p---------p-l-------p--------
> str4: ---ig-evazgbrd-dbc-s--v---------------rvn--------n---g----------f
> 
> solution is feasible: True
> 
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
> --- Solution (of length 138) ---
>  Sol: tkgnkuhmpxnhtqgiojiqfolnbxxcvsuqplcvinycosgsoevoazgbrddbcpyspvlrvnzxuncpmqvgbtdefuivdcvdpfzsmsnbrczfjtoqvbxerzbrvwigpxqkhrdrlctodtmprpxwed
> str1: tkgnkuhmpxnhtqg----------x-----------------------z-----------v-----x--------------i--------s----------------------------------------------
> str2: ---------------iojiqfolnbxxcvsuqp--vi----s-s-------b---------------x------------f---------------------------------------------------------
> str3: -----u----------------l----c--------inycos--o-vo-z-------p--p-l--------p------------------------------------------------------------------
> str4: ---------------i--------------------------g--ev-azgbrddbc--s-v-rvn---n-----g----f---------------------------------------------------------
> str5: --------p-----------------------------y------------------p----lr--zxu-cpmqvg-td-fuiv-c-d---s---b------o-----------------------------------
> str6: --------p---------------b----------------------------d-------------------------e---vdcvdpfzsms-br-----oqvb----b---------h-----------------
> str7: ---------------------------------------------e-------------------n----------b--------c----z--------fjt--v-xerzbrv-igp-------l-----------e-
> str8: ----------------------------------------------------r--------------x---------------------------------------------w---xqk-rdrlctodtmprpxw-d
> 
> solution is feasible: True
> 
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
> --- Solution (of length 245) ---
>   Sol: tkgnkuhmpxnhiojiqfolnbxxulcinycosovoigevazgbrddbcsvpyplrzxucpmqvgtdfupbdevdcvdpfzsmsenbczfjtvxerzbrvigxwxqkrdrlctodtmpkkqafigqjwokkskrblxxpabivbvzkozrifsavnqaxudgqvqcewbfgijowwysxqjnfpadiusiqbezhkwshvhcomiuvddhtxxqjzqbctbakxusfcfzpeecvwantfmgqzu
> str01: tkgnkuhmpxnh-----------------------------------------------------t---------------------------------------q------------------g-----------x--------z--------v---x------------i-----s-------------------------------------------------------------------
> str02: ------------iojiqfolnbxx--c-------v--------------s--------u---q------p---v--------------------------i------------------------------s--------------------s---------------b---------x---f--------------------------------------------------------------
> str03: -----u-------------l------cinycosovo-----z---------p-pl-----p----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: ------------i------------------------gevazgbrddbcsv----r-------v---------------------n---------------------------------------------------------------------n-----g-------f---------------------------------------------------------------------------
> str05: --------p--------------------y---------------------p--lrzxucpmqvgtdfu-------------------------------i-----------------------------------------v----------------------c-------------------d--s--b----------o------------------------------------------
> str06: --------p------------b-----------------------d--------------------------evdcvdpfzsms--b--------r-----------------o------q---------------------vb------------------------b-------------------------h--------------------------------------------------
> str07: --------------------------------------e----------------------------------------------nbczfjtvxerzbrvig---------------p-----------------l------------------------------e------------------------------------------------------------------------------
> str08: --------------------------------------------r------------x---------------------------------------------wxqkrdrlctodtmp---------------r----p-------------------x--------w-----------------d-----------------------------------------------------------
> str09: -k--k-----------q-----------------------a--------------------------f--------------------------------ig---q--------------------jwokkskrbl-------------------------g-----------------------------------------------------------------------------------
> str10: -------------------l--xx---------------------------p---------------------------------------------------------------------a------------b------ivbvzkoz--------------------------------------------z-----v-------d-------------------------------------
> str11: -k------------------------------------------r-------------------------------------------------------i---------------------f--------s-------a--v------------n---------c-------------------d----q-----w-h----------------z--c--------------------------
> str12: ----------------q-----------------------a----------------xu-------d----------------------------------g---q------------------------------------v-------------q--------cewbfgijowwy--------------------------------------------------------------------
> str13: --------------------------------------------r----s-------x----q---------------------------j----------------------------------------------------------------n-------------f-------------padiusiqbezhk------o------h------------------------------mg---
> str14: ------------i------------------------------------------------------------------------------------------w---------------------------s--------------------------------------------------------------h----vhcomiuvdd-------------------------------m----
> str15: ------h----------------------------------------------------------t---------------------------x--------x--q--------------------j------------------z----------q-----------b--------------------------------c--------t------b---ak--------------n-------
> str16: ---------x--------------u-------s----------------------------------f-------c---fz------------------------------------p------------------------------------------------e-------------------------e--------c----v----------------------------wantfm
> ```

> ```
> gqzu
> 
> solution is feasible: True
> 
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
> --- Solution (of length 30) ---
>   Sol: bcdaecdbecdecadbeadcebadcbeead
> str01: --d--c-b-c--c-db---c----c-e---
> str02: b-d---dbe--e----e---eb-d------
> str03: -c-a-cd-e--ec---e----b----e---
> str04: ---ae-d---d---d---d-eb-d-----d
> str05: ---a-c-be--eca-b---ce---------
> str06: b------b-----a-be----b-dcb--a-
> str07: b------b-----a--ea--ebad----a-
> str08: ----e---e--e----e--c-b-d-bee--
> str09: -c---cd-e--e--d--adc---d------
> str10: b-da---b--d----bea----ad------
> 
> solution is feasible: True
> 
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
> --- Solution (of length 42) ---
>   Sol: dacebaedacebabcdbaedcbbcaedbacdaebdeabacde
> str01: d-c-b----c----cdb---c--c-e----------------
> str02: ----b--d-------db-e------e------e--e-b--d-
> str03: --c--a---c-----d--e------e---c--eb-e------
> str04: -a-e---d-------d---d------d-----ebd-----d-
> str05: -ac-b-e---e---c--a---b-c-e----------------
> str06: ----b------bab----e--b----d--c---b--a-----
> str07: ----b------ba-----e-----ae-ba-da----------
> str08: ---e--e---e-------e-cb----db----e--e------
> str09: --c------c-----d--e------ed-a-d--------cd-
> str10: ----b--da--b---db-e-----a---a-d-----------
> str11: ---e---d--e----d-a------a---a---e---a-a---
> str12: -a---ae-a---ab----e------e--ac------------
> str13: ---e-a--a--b--c--a--c--c--db--------------
> str14: ----b--d--e-------e-----a-d-----e---a---de
> str15: --c--aeda------d--e------e------e-d-------
> str16: ---eb----c--a--dba---bb--e----------------
> str17: d------d-ce-------e-----a--b--d-e---a-----
> str18: da--b----c-----d---d-----e--a---e------c--
> str19: -a---a-d-ce-------ed----a---a----b--------
> str20: -a-e--e--c----c---e------e------e---a-a---
> str21: ----b------b---d-ae-c---a---a-d-e---------
> str22: dace---da-e----d-a---b--------------------
> str23: -a---ae-a--b-b--b----b-c-e----------------
> str24: d--e---d---b--c-b---c---a---a----b--------
> str25: d---b--da---a-----e--bbc---b--------------
> str26: d--eb-ed---b------e--b--a----c------------
> str27: --ce--e----b--cd----cb----d-----e---------
> str28: d---b-eda---a--d-a------a--b--------------
> str29: --c------c----cd----cb---e-b--d--------c--
> str30: -a-e--e-ac-----db---cb----d---------------
> str31: dac-b-e-ac----c-----c-----d---------------
> str32: ---e-----ceb--c-----c-----db--d--b--------
> str33: d------d---b-bc---ed----a--b-----b--------
> str34: -a---ae-a--ba----ae--b--a-----------------
> str35: ---e-----c-b-bc--a------a-d--cd-----------
> str36: d--eb----c----c---e-c-----db-c------------
> str37: da---a---c-ba-----e------e-b-c------------
> str38: -a-----da--b------e-----a---ac---------c-e
> str39: da-e-----c-----dba--c---a---a-------------
> str40: dac-b------b---d----c----ed--c------------
> str41: d--e---d---b------e------e-b-----bde------
> str42: --c----da------d----c-----d--cda----a-----
> str43: --ce--ed-c-ba-----e------ed---------------
> str44: --ce-ae--c--a----a------a----c-a----------
> str45: d-c------c----c---e--bb----ba-d-----------
> str46: ----bae---e-a-----e--bb---d-----e---------
> str47: d---b--d--eba-c-----c-----db--------------
> str48: ---eb----c-b------e------ed-a---e---a-----
> str49: -a-e--e---eb-b-db---c---a-----------------
> str50: d---b--da--b--c---e-cbb-------------------
> 
> solution is feasible: True
> 
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
> --- Solution (of length 25) ---
>   Sol: ATGGTCGACACTAGAATCTCGTAAC
> str01: ATGG--GA---TA----C--G----
> str02: AT-----AC-CT----TC-C----C
> str03: -----C-AC----GAAT-T-G-A--
> str04: -T-----A-A--A-A-TCT-GT---
> str05: A-GGT--A-AC-A-AA---------
> str06: -T--TC--C--TAG------GTA--
> str07: -T--T-G----TAGA-TCT------
> str08: -TGG--GA-A---G--T-TC-----
> str09: -T--TC--CAC-A-A--CT------
> str10: -T---C-----TA-AA-C--G-AA-
> 
> solution is feasible: True
> 
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
> 
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
> --- Solution (of length 45) ---
>   Sol: MEQSFPARSNKFLQNDSEYVAICPKGQHVTRAFRKNEPGLGYQHD
> str01: M-----A-----L---S-Y---CPKG---T---------------
> str02: M-QS----S---L-N-----AI-P----V----------------
> str03: M----P------L---S-Y-------QH----FRK----------
> str04: ME---------------E---------HV------NE--L---HD
> str05: M--S-----N-F---D----AI--------RA-------L-----
> str06: M---F--R-N---QN-S-------------R----N--G------
> str07: M---F-------------Y-A------H---AF-----G-GY---
> str08: M--S------KF-----------------TR--R---P---YQ--
> str09: M--SF--------------VA----G--VT-A----------Q--
> str10: ME-S--------L------V---P-G------F--NE--------
> 
> solution is feasible: True
> 
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
> 
> ```


