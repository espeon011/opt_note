In [ ]:
```python
from dataclasses import dataclass
from functools import cached_property
import hexaly.optimizer
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# WMM_HEXALY モデルを max 演算で考えてみる

元の `WMM_HEXALY` モデルは `WMM` をパラメータ化しただけだったため,
一部のパラメータを動かしただけでは解が更新されにくかった. Majority Merge の部分を「最も大きい Weight を持つ文字を採用する」にすれば Weight の変換に解が追従しやすくなるのではないか.

In [ ]:
```python
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    @cached_property
    def chars(self) -> str:
        return "".join(sorted(list(set("".join(self.instance)))))

    @cached_property
    def indices_1d_to_2d(self) -> list[tuple[int, int]]:
        ans: list[tuple[int, int]] = []
        counter = 0
        for s in self.instance:
            ans.append((counter, counter + len(s)))
            counter += len(s)
        return ans

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [priorities1d[start:end] for start, end in self.indices_1d_to_2d]

    def wmm(self, priorities2d: list[list[int]]) -> str:
        max_len = len(self.instance) * max(len(s) for s in self.instance)
        indices = tuple(0 for _ in self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(max_len):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                max(
                    [0]
                    + [
                        priorities2d[sidx][idx]
                        for sidx, (idx, s) in enumerate(zip(indices, self.instance))
                        if idx < len(s) and s[idx] == c
                    ]
                )
                for c in self.chars
            ]
            next_char = self.chars[counts.index(max(counts))]

            solution += next_char
            indices = tuple(
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(indices, self.instance)
            )

        return solution

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d[i] for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        initial_weights: list[list[int]] | None = None,
        *args,
        **kwargs,
    ) -> str | None:
        # 重みの最大値は初期重みが与えられた場合は初期重みの最大値の 2 倍,
        # 初期重みが与えられなかった場合は文字種数とする.
        max_weight = (
            max(
                max(w, len(s))
                for s, ws in zip(self.instance, initial_weights)
                for w in ws
            )
            if initial_weights
            else len(self.chars)
        )

        with hexaly.optimizer.HexalyOptimizer() as hxoptimizer:
            hxmodel = hxoptimizer.model
            hxparam = hxoptimizer.param

            priorities1d = [
                hxmodel.int(1, max_weight)
                for s in self.instance
                for cidx, _ in enumerate(s)
            ]

            func = hxmodel.create_int_external_function(self.objective)
            func.external_context.lower_bound = 0
            func.external_context.upper_bound = sum(len(s) for s in self.instance)

            indices_1d_to_2d: list[tuple[int, int]] = []
            counter = 0
            for s in self.instance:
                indices_1d_to_2d.append((counter, counter + len(s)))
                counter += len(s)

            hxmodel.minimize(func(*priorities1d))
            hxmodel.close()

            if initial_weights:
                priorities2d = self.priorities_1d_to_2d(priorities1d)
                for ps, ws in zip(priorities2d, initial_weights):
                    for p, w in zip(ps, ws):
                        p.set_value(w)

            if time_limit is not None:
                hxparam.time_limit = time_limit
            hxparam.verbosity = 1 if log else 0
            hxoptimizer.solve()

            solution = hxoptimizer.solution
            status = solution.status
            if status in {
                hexaly.optimizer.HxSolutionStatus.OPTIMAL,
                hexaly.optimizer.HxSolutionStatus.FEASIBLE,
            }:
                priorities1d_value: list[int] = [p.value for p in priorities1d]
                priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
                self.solution = self.wmm(priorities2d_value)

        return self.solution
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
>  Sol: ultcikgenykcosouhmvajiqfozpxplnhtqgbxzrddxbcvxsuqpvissbxrvnngf
> str1: --t--kg-n-k----uhm--------px--nhtqg-xz------vx-----is---------
> str2: ----i-------o-------jiqfo----ln----bx----x-cv-suqpvissbx-----f
> str3: ul-ci---ny-coso---v-----ozp-pl-------------------p------------
> str4: ----i-ge----------va-----z--------gb--rdd-bc--s---v-----rvnngf
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 0.0
> wall time: 59.251519s
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
>  Sol: ipbdtkgevnkulahmzgbrdcvinyzdbcopfjtisvxnhtqfolgervonbnwxxczvxsuqckpmsbroqvigtdfprlsuivctodtmpesbobhrpxwfd
> str1: ----tkg--nku--hm---------------p------xnhtq---g--------x--zvx-------------i-------s----------------------
> str2: i-----------------------------o--j-i------qfol-----nb--xxc-v-suq--p------vi-------s-----------sb-----x-f-
> str3: -----------ul--------c-iny---co-----s-------o----vo-------z-------p------------p-l----------p------------
> str4: i-----gev----a--zgbrd------dbc------sv----------rv-n-n---------------------g--f--------------------------
> str5: -p-----------------------y-----p-------------l--r---------z-x-u-c-pm----qv-gtdf----uivc--d----sbo--------
> str6: -pbd---ev-----------dcv----d---pf-------------------------z--s-----msbroqv---------------------b-bh------
> str7: -------e-n--------b--c----z-----fjt--vx--------er---------z----------br--vig---p-l-----------e-----------
> str8: -------------------r------------------x---------------wx-------q-k----r------d--rl----ctodtmp------rpxw-d
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 105
> best bound: 0.0
> wall time: 59.997485s
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
> --- Solution (of length 156) ---
>   Sol: kiworshtxuxkqjanfpabdifzgeqfjwolcinbycoplkkrzxxusfcpfjaqkrdbgizhmpxqvngqctbvxeadqwrzhkctozvodpfzsmiuqgpbrvivddbgplecsbvrwatodqvbsbhnntfmgijqporpxfwzvuwydxis
> str01: -------t---k------------g---------n------k-----u---------------hmpx--n--------------h--t------------qg------------------------------------------x--zv----xis
> str02: -i-o---------j-------i----qf--ol--nb---------xx---c-----------------v---------------------------s--uq-p--vi---------s-----------sb--------------xf----------
> str03: ---------u---------------------lcin-yco---------s---------------------------------------o-vo---z------p---------pl--------------------------p---------------
> str04: -i----------------------ge------------------------------------------v---------a----z-----------------g-br---ddb----cs-vr------v----nn---g--------f----------
> str05: -----------------p------------------y--pl--rzx-u--cp------------m--qv-g--t-----d--------------f----u------iv-------c--------d---sb-----------o--------------
> str06: -----------------p-bd----e------------------------------------------v----------d------c---v-dpfzsm------------------sb-r---o-qvb-bh-------------------------
> str07: -------------------------e--------nb-c------z----f---j-------------------t-vxe----rz-------------------brvi----gple-----------------------------------------
> str08: ----r---x--------------------w---------------x---------qkrd-----------------------r------------------------------l-c------tod--------t-m----p-rpx-w-----d---
> str09: k----------kq-a-f----i--g-q-jwo----------kk-----s-------kr-b-----------------------------------------------------l----------------------g-------------------
> str10: -------------------------------l-------------xx----p--a----b-i------v-----bv-------z-k--oz-----z---------v--d-----------------------------------------------
> str11: k---r----------------if-------------------------s-----a-------------vn--c------dqw--h----z-------------------------c----------------------------------------
> str12: ------------q-a------------------------------x-u----------d-g------qv--qc----e---w---------------------b------------------------------f-gij--o----w---wy----
> str13: ----rs--x---qj-nfpa-di-------------------------us------------i-----q------b--e-----zhk--o-----------------------------------------h----mg-------------------
> str14: -iw--sh-------------------------------------------------------------v---------------h-c-o--------miu-----v--dd-------------------------m--------------------
> str15: ------htx-x-qj---------z--q--------b-c-----------------------------------tb---a------k---------------------------------------------n------------------------
> str16: --------xu--------------------------------------sfc-f---------z--p-----------e------------------------------------ec--v-wa---------n-tfmg--q-------z-u------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 156
> best bound: 0.0
> wall time: 59.971736s
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
>   Sol: baedcbacdbeeecdabdcebadeaced
> str01: ---dcb-c-----cd-b-c------ce-
> str02: b--d----dbeee------eb-d-----
> str03: ----c-acd-ee-c-----eb--e----
> str04: -aed----d-----d--d-eb-d----d
> str05: -a--cb----ee-c-ab-ce--------
> str06: b----ba--be-----bdc-ba------
> str07: b----ba---e----a---ebad-a---
> str08: --e-------eeec--bd--b--e--e-
> str09: ----c--cd-ee--da-dc---d-----
> str10: b--d--a--b----d-b--e-a--a--d
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 28
> best bound: 0.0
> wall time: 59.968051s
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
>   Sol: adcebdabcedabceadbcaebdcebadeabcdeae
> str01: -dc-b---c----c--dbc----ce-----------
> str02: ----bd----d-b-e-----e---e---e-b-d---
> str03: --c---a-c-d---e-----e--ceb--e-------
> str04: a--e-d----d-----d-----d-eb-d----d---
> str05: a-c-b----e----e---ca-b-ce-----------
> str06: ----b--b---ab-e--b----dc-ba---------
> str07: ----b--b---a--ea----eb----ad-a------
> str08: ---e-----e----e-----e--c-b-d--b--e-e
> str09: --c-----c-d---e-----e-d---ad---cd---
> str10: ----bdab--d-b-ea---a--d-------------
> str11: ---e-d---eda---a---ae-----a--a------
> str12: a-----a--e-a---a-b--e---e-a----c----
> str13: ---e--a----abc-a--c----c---d--b-----
> str14: ----bd---e----ead---e-----ade-------
> str15: --c---a--eda----d---e---e---e---d---
> str16: ---eb---c--a----db-a-b---b--e-------
> str17: -d---d--ce----ea-b----d-e-a---------
> str18: -d----abc-d-----d---e-----a-e--c----
> str19: a-----a---d--ce-----e-d---a--ab-----
> str20: a--e-----e---c----c-e---e---ea----a-
> str21: ----b--b--da--e---ca------ade-------
> str22: -d----a-ceda--e-d--a-b--------------
> str23: a-----a--e-ab----b---b---b-----c-e--
> str24: -d-e-d-bc---bc-a---a-b--------------
> str25: -d--bda----a--e--b---b-c-b----------
> str26: -d-eb----ed-b-e--b-a---c------------
> str27: --ce-----e--bc--d-c--bd-e-----------
> str28: -d--b----eda---ad--a------a---b-----
> str29: --c-----c----c--d-c--b--eb-d---c----
> str30: a--e-----e-a-c--dbc--bd-------------
> str31: -d----a-c---b-ea--c----c-------cd---
> str32: ---e----ce--bc----c---d--b-d--b-----
> str33: -d---d-b----bce-d--a-b---b----------
> str34: a-----a--e-ab--a---aeb----a---------
> str35: ---e----c---b----bca------ad---cd---
> str36: -d-eb---c----ce---c---d--b-----c----
> str37: -d----a----a-c---b-ae---eb-----c----
> str38: ad----ab-e-a---a--c----ce-----------
> str39: -d----a--e---c--db-a---c--a--a------
> str40: -d----a-c---b----b----dce--d---c----
> str41: -d-e-d-b-e----e--b---bd-e-----------
> str42: --c--da---d--c--d-c---d---a--a------
> str43: --ce-----ed--c---b-ae---e--d--------
> str44: --ce--a--e---c-a---a------a----c--a-
> str45: -dc-----c----ce--b---b---bad--------
> str46: ----b-a--e----ea----eb---b-de-------
> str47: -d--bd---e--b--a--c----c---d--b-----
> str48: ---eb---c---b-e-----e-d---a-ea------
> str49: a--e-----e----e--b---bd--b-----c--a-
> str50: -d--bdabce---c---b---b--------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 36
> best bound: 0.0
> wall time: 59.990072s
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
>   Sol: ATGGTGACCTACGAATCTGATACC
> str01: ATGG-GA--TACG-----------
> str02: AT----ACCT-----TC-----CC
> str03: -------C--ACGAAT-TGA----
> str04: -T----A---A--AATCTG-T---
> str05: A-GGT-A---AC-AA----A----
> str06: -T--T--CCTA-G-----G-TA--
> str07: -T--TG---TA-GA-TCT------
> str08: -TGG-GA---A-G--T-T----C-
> str09: -T--T--CC-AC-AA-CT------
> str10: -T-----C-TA--AA-C-GA-A--
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 0.0
> wall time: 59.97797s
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
> --- Solution (of length 169) ---
>   Sol: AGTAACGACATGTAGATCCAGTATCTAACGAACTAGTAGTGCAGCGAGATGCTACGGACGGTCAACAACGTACAGTAGTACACTCCAAGTTACTCATGGACAGTAACAGGCCACGTAAGCGTGAGCGATGCGTACGTCAAGATGCTAGACACGTGAAGCTACGARTAGT
> str01: --TA--G---T--AG-T--AG-A-CT--C---C--G--G---A---AG-TG--AC--A-----AAC--C---C--T-G-A-A----AAG--A---ATGGA---TAA-A-------TA----T-A---------------------------------------------
> str02: -G----GA--T--A-A---A----C-A-C----T-------C--C------C---G-A-----AA-A---TA-A-T--T----T----G--ACT--T--A-A--A-CA----ACG----CG--A-C-A-G--T---TCAAG----------------------------
> str03: A-TA-C--C-T-T----CC--TA------G-----GTA----A-C-A-A----AC---C----AAC--C--A-A------C--T-----TT--T---G-A---T--C--------T---C-T------TG--TA-G--A---T-CT-G---------------------
> str04: --TAA--A--T-TA--T--A--ATCT-------TA-TA---C-------T---A-G-----T-AA-AA---A-A-TAG----------G--------G-----T----G------TAA-C-----CGA-----A----AA----C--G----GT----C----------
> str05: --T-------T--A-A---A--A-C-A--G--C--------C-------TG-T--GG--G-T--------T---G-----CAC-CCA-----CTCA----CAG-----GGCC-C--A--C-TG-G-G---CG--C---AAG----------------------------
> str06: A-T---GAC-T-T----CCA--AT-----G-----G-A-T-C--C------C-A---AC---C-------T-CA--AG--C--T-----T--C-CA----C-----C---CCA---A----TG-G---T---T---TCA-G---C------------------------
> str07: A--A-C-A-A---A---CCA--A-C---C-AACT--T--T---------TG--A-------TC-------T-C--T--T---------GT-A-----G-A---T--C--------T--G--T------T-C-T-C-T-AA-A--C--GA-AC-----------------
> str08: A-T---GA-A---A-A-C--G-A---AA--A--T--TA-T---------T---A-------TCAA----G----G--GTA---T----G--------G-A-AGT----GG--A---A-GC-TGA-CGA-----A----A---T--------------------------
> str09: A----C----T------C--G--------G--CT-G-----CA------TGCT--------T-A-----GT---G-----CACTC-A-----C----G--CAGTA----------TAA---T------T----A----A---T---A-AC---T-AA--T-----TA--
> str10: --T-------TGTAGATC---T-------G---T--T----C-------T-CTA---A-----A-C---G-A-A------C--T-----TTA---A---A-A-T--C--------T--G--TG-----TG-G--C-T---G-T-C-A--C---T----C----------
> str11: -G---C-A---G-AG--C-A-T-T-T-------T-------C-------T---A---A---T-A------T-C-------CAC---AA---A---ATG-A-AG-----G-C-A---A----T-A---AT---T--GT-A-----CTA--C---T----C----------
> str12: A-T---GA---G-----CCA--A------GA--T-------C--CGA----C---G-A-----A-----G-A--G-----C-C-CCAAG--------G-A--G-----G---A-G-AAG-G--AG-G--G---AC--C------C----C-C-----------------
> str13: --T--C----T------C-A----C-A--G---T--T----CA---AGA----AC---C---CAA-A--GTAC-------C-C-CC------C--AT--A--G---C---CC---T---C-T------T----A----AAG---C----CAC-----------------
> str14: AG----G---T-T---T--A-TA-C---C----T--T----C--C----T---A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T-----T---CGAT-C-T-C-T-----TG-TA----------------------
> str15: AG----G---T-T---T--A-TA-C---C----T--T----C--C------C-A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T-----T---CGAT-C-T-C-T-----TG-TA----------------------
> str16: --TAA--A-A-------C-A--A-CT--C-AA-TA------CA---A----C-A-------T-AA----G-A-A--A--A---TC-AA----C----G--CA--AA-A----AC--A--C-T---C-A--C--A----AA-----------------------------
> str17: -----C--C--G-----CC-----C-A------T--T--TG--G-G-----C---GG-C--TC-------T-C-G-AG--C-------G--A-T-A-G--C--T--C-G------T---CG--A---AT-C---C--C----T-C--GAC-C-T---------------
> str18: A-TA-C--C-T-T----CC-----C-A--G-----GTA----A-C-A-A----AC---C----AAC--C--A-A------C--T-----TT-C----G-A---T--C--------T---C-T------TG--TA-G--A---T-CT-G---------------------
> str19: --T--C----T------C-A----C-A--G---T--T----CA---AGA----AC---C--TCAA----GT-C--T----C-C-CC------C--AT--A--G-----G-CC---T---C-T------T---T-C---A-G-T-C-AG---------------------
> str20: -G-A------T------C---T--CT--C----T-------CA-C------C---G-A-----A-C--C-T---G--G--C-C-CC--G--------GG-CA--AA---------T--GC-----C----C-TA----A---T-C----CA-G--A-G----G--T-G-
> str21: AG-A--G-CA---A--TC-AGT-------G--C-A-T----CAG--A-A----A-------T-A------TAC-------C--T--A--TTA-T-A----CA----C--------T-----T------TGC-TA----A-GA----A------T---------------
> str22: A--A------T-TA-A---A--A-C-A------T-------C-------T-C-A---A---T-A-CAAC--A---TA--A--------G--A---A---A-A--A-CA----ACG----C---A---A-----A----AA----C-A--C---T----C-A----T---
> str23: A--AACGA-A-------C---T-T-TAA--AA-T-------C-------TG-T--G-----T-------G----G-----C--T----GT--C--A----C--T--C-GGC----T--GC---A----TGC-T---T-A-G-TGC------------------------
> str24: A-TAAC----T--A-AT----TA-CT---G---T-------C-G-----T--T--G-AC----A-----G----G-A---CAC-----G--A-----G-----TAAC--------T---CGT---C--T----A--TC----T--T---C---TG--------------
> str25: A-T---GA---GT-G-TC-A----C----GAA-T--T----CA-CG---T---AC--A-----A------T---G-A--AC--T----G--------G-A---T----G------T-----T---C-A--CGT--G----GA----A------T-AA------------
> str26: A----C--C--GT-G-----G--------G--C--G-AG--C-G-G---TG--AC---CGGT-------GT-C--T--T-C-CT--A-GT-------GG---GT--C---CCACGT-----TGA---A------------------------------------R----
> str27: A--AA-G----GT---T----TAT--A-C---CT--T----C--C------C-A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T-----T---CGAT-C-T-C-T-----TG-------------------------
> str28: AGTA--G---T-T----C--G---C---C----T-GT-GTG-AGC----TG--AC--A-----AAC----T----TAGTA--------GT-------G-----T-----------T-----TG-----TG---A-G----GAT--TA----------------------
> str29: --T-------T-TA--T--A----C---C----T--T----C--C----T---A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T-----T---CGAT-C-T-C-T-----TG-TAGA----T---------------
> str30: A-T---G-C--G--G-TC--GT--CT--C----T-------C--C------C--CGG-C--T--------T----T--T----T-----TT-C-C-----C-----C-G-C---G----C-----CG---CGT---T---G--GC--G-C-CG--A-------------
> str31: -GT---GACA---A-A---A--A-C-A------TA--A-TG--G--A----CT-C---C----AACA-C---CA-T-GT-CA----A-G---CT--T------T--CAGG-----TA-G----A-C-------------------------------------------
> str32: -GT---G---T--A-A----G-A---AAC-A----GTA----AGC------C--CGGA-----A-----GT---G--GT---------GTT--T--TG--C-G-A----------T-----T------T-CG-A-G----G---C----C--G-G--------------
> str33: -G-A--GA-ATG-AG-TC---T--C-A------T--TA---C--CG-----C--C---CGGT-A-C----T----TAG--CA----A-G---CT-A---A---TA---G------T---C---A-CG--GC--------------------------------------
> str34: A-T---G---TG--G-TC--G-AT-----G--C--------CA------TG----G-A-GG-C--C--C--AC-------CA------GTT-C--AT------TAA--GGC----T---C-----C--TG-G--C---A---T--T-----------------------
> str35: A----CGA---G-----C--GT-T-T-------TA--AG-G--GC------C--CG--CG---A-C----T---G-----C-------G--AC----GG-C-----CA--C-A--T--G-G----C----C---C-T---G-T---A------TG----T---------
> str36: -G----G---T-T---T--A-TA-C---C----T--T----C--C------C-A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T-----T---CGAT-C-T-C-T-----TG-TAG---------------------
> str37: --T---G----G--GA---AGT-TC---C-AA--A--AG---A------T-C-AC--A-----AA-A-C--AC--TA---C-C---A-GT--C--A---AC-----C--------T--G----A---A-G--TAC---A-----C------------------------
> str38: -G-AA-G-C--GT---T--A--A-C----G---T-GT--TG-AG-GA-A----A---A-G---A-CA--G--C--T--TA--------G--------G-A--G-AACA----A-G-A-GC-TG-G-G------------------------------------------
> str39: A----C--CA-G-----C--G---C-A-C----T--T----C-G-G-----C-A-G--CGG-CA-----G--CA------C-CTC---G--------G--CAG---CA--CC---T---C---AGC-A-GC--A----A-----C------------------------
> str40: A-T---G----G--GA-C-A--A-CT-------TA-T--T-C--C----T---A-------TCA------T---GT-G--C-C---AAG--A-----GG----T-----------T-----T------T----AC--C------C--G----GTGA--C--C-A-----
> str41: --T-------TGTAGATC---T-------G---T--T----C-------T-CTA---A-----A-C---G-A-A------C--T-----TTA---A---A-A-T--C--------T--G--TG-----TG-GT---T---G-T-C-A--C---T----C----------
> str42: A--A-C--CA---A---CCA--A-CT-------T--T----C-G--A--T-CT-C------T--------T---GTAG-A---TC----T-------G-----T-----------T---C-T---C--T----A----AA----C--GA-AC-T-----T-----TA--
> str43: -G----G----GT---TC---T-------G--C--------CAG-G-----C-A-------T-A-----GT-C--T--T----T-----TT--T--T---C--T----GGC---G---GC-----C----C-T---T---G-TG-TA-A-AC------CT--G------
> str44: -G----G-C-TG-----C-A-T-------G--CT--TAGTGCA-C----T-C-ACG--C----A-----GTA---TA--A---T-----T-A---AT--A-A----C--------TAA---T------T----AC-T---G-T--------------------------
> str45: --T---G-CATG-----C---T-T--A--G---T-G-----CA-C----T-C-ACG--C----A-----GTA---TA--A---T-----T-A---AT--A-A----C--------TAA---T------T----AC-T---G-T-C--G-----T---------------
> str46: --T-------T------CCA----C-AAC----T--T--T-C--C-A----C--C--A-----A-----G--C--T----C--T----G---C--A---A--G-A----------T---C-----C----C--A-G--A-G-T-C-AG----G-G--GC--C---T-GT
> str47: --T--C----T--A-A---A----C----GAACT--T--T--A---A-A----A-------TC-------T---GT-GT---------G--------G--C--T----G------T---C---A-C--T-CG---G-C----TGC-A------TG---CT-----TAG-
> str48: A----C--C--G--GAT---G--------G--C--------C-GCGA--T--T--------T--------T----T----C-------G--------G-A--GT--C---C----T-----TG-G-G--G-G-AC--CA-----CT---CA-G--AA--TA-GA-----
> str49: -----C----T-T-G-T--AG-ATCT---G---T--T----C-------T-CTA---A-----A-C---G-A-A------C--T-----TTA---A---A-A-T--C--------T--G--TG-----TG-G--C-T---G-T-C-A--C---T---------------
> str50: A-T---GA---G-----C-A----CTAA-G--C--G-A----AG--A-A--C--C--A-----AA-AA-G--CAG-A---CA----A--T-AC--A---AC-----C---C---G----C-T-A----T---TAC----------------------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 169
> best bound: 0.0
> wall time: 60.024681s
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
> --- Solution (of length 45) ---
>   Sol: MAEPQSSKLSNFDVEHYCAIPGVTRNQHAFGNELSRNPKGYTQHD
> str01: MA------LS------YC--P-----------------KG-T---
> str02: M---QSS-L-N-------AIP-V----------------------
> str03: M--P----LS------Y---------QH-F-----R--K------
> str04: M-E-----------EH------V--N------EL---------HD
> str05: M----S----NFD-----AI----R---A----L-----------
> str06: M----------F------------RNQ----N--SRN--G-----
> str07: M----------F----Y-A--------HAFG--------GY----
> str08: M----S-K---F-----------TR----------R-P--Y-Q--
> str09: M----S-----F-V----A--GVT----A-------------Q--
> str10: M-E--S--L----V------PG-------F-NE------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 45
> best bound: 0.0
> wall time: 59.905132s
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
> --- Solution (of length 1009) ---
>   Sol: MATDHPVESLLKNIAFDVFRPGFNWSAEEDDFGHIIKFTQNLVLKKMAEFGEEGHIIDLFDIEIIKLDNHIDIETGCKLFKMKNGPEKIKLAEKLLENQAAAEQGKAQRAEFGHEIKKLNKDKPSEEAFAGIGIKIQLFADQIILMNNINIDINYAEHAFGGIVQLSKLPWFLSNGQCADITARPAARDAEAEGIEKKHLADFDAIKGNSFIGHLCDDILHMKADFNMLKPTSAGFGAIHLAEGFQNPPKHLASYSNDEFASGIKLGHIHMNLHAFPGLVFTDEAGFIEIKHKLQHVRDVLVYNKLRGFVYACDAEDFEGDEIKCGQEHIIIKLESLAQDFAYSDGGAIDGGELMEENDPNTNEVEEPAAGTCTDAIEFAGHAKLFDIADLMNDGLITQACLPEDLDGDFPAQSNAACDDENAEFFAIELEEEKLKNDNNLEPQDLRTFQHLACDFGGIKDGHDLNKNIFPPALAQRAHLICLAVLKTADIILNLPQDIPPERGFGDKSYTVEANFILTVATDHSQPFIPTRGVADCEDFKFDDGAIGGLADIKRFGADAMGEDNFMTDEEGIEIDENDLAQHLKDGPAFGQDPKHIAIRGILIQSRACCEGIEGKGILISIKLMIDEPRGDISEKVLLSYDAGDEAFCHILIGMANIADGLGQAEGGEPMKLNRQHLKDGSGNSTAEHKKLMNQPDEGLSAEFGKLNEGEQARQSRTVHLEGKMAFCRIGVIRISIGGRSLTGSWADATEFDHFDAIFIKKIAEALACNPQQREPAIRRKQTCDDGAECIKHLPLPDECDFDHLIQHRLSLPRKHRNTHPDDSIVPNRRGGNPLSEAGADSAFRAERRGTIKLPGDFFRDCKQIDMAKKLSADGRMAHVKARVQKDWTPSGESVRVWIWTSLGFWMFMICSVVGNLWVTVYPRIADEKVAEFGLLNKKRSSVLADHSKAEDHGILPIRNQALNKNLTQDYGNIPDKVFKNKYFLMWPRSHLNIQRPSVLHSWKEAKTT
> str01: M------------------R-------------H-------L--------------------------N-IDIET-------------------------------------------------------------------------------Y-----------S------SN----DI---------------K-----------N---G------------------------------------------------------------------V----------------------Y-K-----YA-DAEDFE---I----------L--L---FAYS----IDGGE-----------VE------C-----------L-D---L------T------------------------------------------------R----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str02: M------E-----------R----------------------------------------------------------------------------------------RA---H---------------------------------------------------------------------R-----------------------------------------------T-------H-----QN------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-DAT----------K---------P--RE---RRKQT-----------------------QHRL--------THPDDSI------------------------------------------------------------------------------------------------YPRI--EK-AE-G-----R--------K-EDHG-------------------------------------------------------
> str03: M------E------------PG----A----F--------------------------------------------------------------------------------------------S--------------------------------------------------------TA----------------L--FDA---------LCDDILH----------------------------------------------------------------------------R--------R--------------------------LES--Q--------------L--------------------------------------------------------------------------------------------R-F-------GG--------------------------V-----------Q-IPPE---------V------------S----------D---------------------------------------------------P-----------R------------------------------------V---Y-AG-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y---A--------LL-------------------------------------------------------------------------
> str04: M--------------------G--------------KF--------------------------------------------------------------------------------------------------------------------Y---------------------------------------------------------------------------------------------------YSN----------------------------------------R--------R--------------------------L---A--------------------------V-------------FA------------------QA------------QS--------------------------------R---HL----GG--------------------------------------------------SY--E------------Q---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W--------------------LAC--------------------------------------------------------V---------S--G-DSAFRAE--------------------------------VKARVQKD--------------------------------------------------------------------------------------------------------------------------
> str05: ---------------F--FR-------E------------NL-----A-F------------------------------------------------Q----QGKA-R-EF-----------PSEEA-------------------------------------------------------R-A----------------------NS--------------------PTS----------------------------------------------------------------R-----------------E-----------------L---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-------------------------------------------------------------------------------V--RRGGNPLSEAGA------ERRGT--------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: M--D-P--SL----------------------------TQ--V-------------------------------------------------------------------------------------------------------------------------------W-------A----------------------------------------------------------------------------------------------------V---E-G-------------------------------------------------S----------------------------V-------------------L----------------------------S-AA-------------------------------------------------------------------V----D--------------------T--A-----------------------E-----------------------------T---------ND----------------------------------------------------------------------------------------------------------T-E-------PDEGLSAE----NEGE------T----------RI--IRI-------TGS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str07: MA-------------FD-F------S----------------V-------------------------------TG-------N-------------------------------------------------------------------------------------------------T--------------K--L-D-----------------------------TS-GF---------------------------------------------T------------Q------------G-V-------------------------S-------S----------M------T--V---AAGT------------L--IADL---------------------------------------------------------------------------------------------V-KTA-------------------S---------------SQ-----------------------L-----------------T---------N-LAQ-----------------------S-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: MA----V------I---------------------------L-------------------------------------------P--------------------------------------S--------------------------------------------------------T------------------------------------------------------------------------Y--------------------------TD--G---------------------------------------------------------------------------T------AA--CT------------------N-G------------------S----------------------------P-D---------------------------------------V--------------------------V--------------------G----------------------------------T---G-----------------------------------------------------------------------------------------------------------------T------M----------------------------------------------------W-------------------------------------------------------------------------------V-N----------------------TI-LPGDFF----------------------------WTPSGESVRV----------------------------------------------------------------------------------------------------------------
> str09: M-----------N-------------------------T-----------G----IIDLFD-------NH---------------------------------------------------------------------------------------------V---------------D-----------------------------S-I------------------PT------I-L------P--H-------------------------------------------Q-----L----------A-------------------------------------------------T----------------------L-D--------------------------------------------------------------------------------------------------------------------------Y-------L-V-----------R-----------------------------------T----I-IDEN---------------------R-----S------------------------------VLL--------F-HI---M-----G--------------------SG--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N-LR------------------------------------------------------T------------------------------------------------------------------------------------RT-Q-L------------------PPA------------------------------------YT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--HS-------------------------------------------------------------
> str11: M--D----S--K---------------E----------T----------------I--L--IEII--------------------P-KIK----------------------------------S-----------------------------Y----------L--L----------D-T--------------------------N--I--------------------S--------------P-K---SY-ND-F---I-----------------------------------------------------------------------S--------------------------------------------------------------------------------------------------------------R------------------NKNIF--------------V-----I--NL--------------Y----N----V----S-----T---------------I------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: M--------LL--------------S------G---K-------KKM-----------L-------LDN-------------------------------------------------------------------------------------Y-E------------------------TA--AAR-----G-------------------------------------------------------------------------------------------------------R---------G-----------GDE----------------------------------------------------------------------------------------------------------------------------R-----------------------------R-------------------------RG-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------WA----FD--------------------R-PAI-----------------------------------------------V------------------------T-K------RD-K--------S-D-RMAH----------------------------------------------------------------------------------------------------------------------------------
> str13: M-----------N--------G-----EEDD---------N-------E-------------------------------------------------QAAAEQ---Q-------------------------------------------------------------------------T--------------KK--A-----K------------------------------------------------------------------------------------------R-----------------E-------K-----------------------------------P-----------------------K--------------QA----------------------------------------------R------------K------------------------V--T--------------------S---EA---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W----E--HFDA-------------------------T-DDGAEC-KH------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str14: M------ESL-------V--PGFN---E--------K-T---------------H------------------------------------------------------------------------------------------------------------VQLS-LP-------------------------------------------------------------------------------------------------------------V-------------LQ-VRDVLV----RGF----------GD--------------S----------------------------VEE---------------------------------------------------------------------------------------------------------------------VL----------------------S---EA-----------------R-------------------------------------------------QHLKDG--------------------------------------------------------------------------------------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M------------------R--------------------------------------------------------------------------------------------------------------------------------------Y-------IV--S--P------Q----------------------L-------------------------------------------------------------------------------V-------------LQ-V----------G---------------K-GQE------------------------------------VE--------------------------------------------------------------------------------R-----A-----------L--------------------------------------------Y-------LT-------P-----------------------------------------------------------------------------------------------------------------YD---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y--I-DEK-----------S---------------PI------------Y-----------YFL---RSHLNIQRP------------
> str16: M----P-------------R----------------------V------------------------------------------P-----------------------------------------------------------------------------V------------------------------------------------------------------------------------------Y--D---S--------------P-----------------Q-V--------------------------------------S-----------------------PNT--V--P------------------------------QA----------------------------------------------R----LA----------------------------------T-------P------------S------F----AT----P---T--------F--------------R-GADA---------------------------PAF-QD--------------------------------------------------------------------------------------------TA------NQ----------------QARQ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str17: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N-LR------------------------------------------------------T------------------------------------------------------------------------------------RT-Q-L------------------P--LA----------------------------------YT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--HS-------------------------------------------------------------
> str18: M--------------F-VF---F-------------------VL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N-L-------------------------------------------------------T---------T--------------------------------------------------------------------------RT-Q-L------------------PPA------------------------------------YT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--HS-------------------------------------------------------------
> str19: M------E------A-------------------II----------------------------------------------------------------------------------------S---FAGIGI------------N-------Y------------K----------------------------K--L---------------------------------------------Q-------S----------KL----------------------------QH--D---------F----------G------------------------------------------------------------------------------------------------------------------------------R-------------------------------------VLK-A---L-----------------TV------T-A----------R--A--------------L-------------------------------------P--GQ-PKHIAIR----Q--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: MA------S----------------S------G----------------------------------------------------PE---------------------RAE--H----------------------Q-----IIL------------------------P--------------------E------------------S---HL-----------------S--------------------S----------------------P-LV----------KHKL------L-Y-------Y--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W--------------K-----L---------------T---G------LPLPDECDFDHLI-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str21: M------ESL-------V--PGFN---E--------K-T---------------H------------------------------------------------------------------------------------------------------------VQLS-LP-------------------------------------------------------------------------------------------------------------V-------------LQ-VRDVLV----RGF----------GD--------------S----------------------------VEE---------------------------------------------------------------------------------------------------------------------VL----------------------S---E------V-----------R-------------------------------------------------QHLKDG--------------------------------------------------------------------------------------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M--------L----A-----P----S-----------------------------------------------------------P-----------N--------------------------S---------KIQLF-------NNINIDINY-EH-----------------------T-----------------L------------------------------------------------------Y----FAS-----------------V-------------------------------------------------------S-AQ------------------N-------------------------------------------------------S----------FFA----------------Q-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-------------------------------------------------------------------------------V-----------------------------------------------------V-----------------------------------------Y------------------S---AD--KA----I------------------------------------------------------
> str23: M-------S-----A-------------------I---T---------E-------------------------T--K-------P-----------------------------------------------------------------------------------------------T------------IE---L------------------------------P--A------LAEGFQ---------------------------------------------------R----YNK--------------------------------------------------------T-----P--G-------F------------------T--C-----------------------------------------------------------------------------------VL---D------------R------Y------------DH--------GV------------I-----------------N---D------------------------------------S---------K-I------------------VL--Y---------------N----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str24: M----------KNIA------------E---F----K-------K--A-------------------------------------PE---LAEKLLE------------------------------------------------------------------V-------F-SN------------------------L------KGNS---------------------------------------------------------------------------------------R-------------------------------------SL--D-------------------P-------------------------------M------------------------------------------------------R-----A---G--K--HD--------------------V--------------------------V-------V--------I--------E-------------------------------------------------------------------S-------------------------------------------------------------------------------T---KKL-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: M----P---------------------------------Q---------------------------------------------P----L--K----Q-------------------------S------------L--DQ------------------------SK--W-L----------R------EAE---K-HL-------------------------------------------------------------------------------------------------R-------------A---------------------LESL---------------------------V---------D--------------------------------------SN--------------LEEEKLK------PQ-L--------------------------------------------------------------S---------------------------------------------------MGED------------------------------------------------------------------------V--------------------------Q-----------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N-L----------------I--------------------------------------T------------------------------------------------------------------------------------RT-Q----------------------------------------------------------SYT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--HS-------------------TQD---------------------------------------
> str27: M----------K---FDV-----------------------L----------------------------------------------------------------------------------S------------LFA-----------------------------PW-------A-----------------K----------------------------------------------------------------------------------V--DE----------Q--------------------E--------------------------Y-D-----------------------------------------------------Q-------------Q----------------L------N-NNLE------------------------------------------------------------------S-------I-T-A-----P-------------KFDDGA---------------------T-E--IE-------------------------------S----E------------------RGDI----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str28: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N----F----------------------------------------------------TN-----------------------------------------------------------------------------------RT-Q-L------------------P-------------------------------------S----A------------------------------------------------------------------------------------------------------------------------------Y--------------------------------------------T-------N------S--F-------------T----------R-GV---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y------------------------------------------------Y---PDKVF---------RS-------SVLHS-------
> str29: M-----------------------WS--------II------VLK-------------L--I--------------------------------------------------------------S------I----Q--------------------------------P--L--------------------------L--------------L----------------------------------------------------------------V-T-----------------------------------------------------SL----------------------P------------------------L----------------------------------------------------------------------------------------------------------------------------Y----N-----------P-------------------------------------N-M-D------------------------------------S--CC--------LIS--------R--I----------------------------------------------------T---------P-E-L-A--GKL----------T---------------------------W-----------IFI---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str30: M------ESL-------V--PGFN---E--------K-T---------------H------------------------------------------------------------------------------------------------------------VQLS-LP-------------------------------------------------------------------------------------------------------------V-------------LQ-VRDVLV----RGF----------GD--------------S----------------------------VEE-----------F-----L----------------------------S------E-A-----------------------R--QHL-------KDG-------------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V--------------------------------------------------------------------------M----P------------------------LF------N--LIT-------------------------------------------------T---------------------------------------T--------Q-----------SYT---NF--T------------RGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--H--------L-----------------------------------------------------
> str32: M---H----------------------------------Q---------------I------------------T----------------------------------------------------------------------------------------V-------------------------------------------------------------------------------------------------------------------V-------------------------------------------------------S---------G-------------P-T-EV------------------------------------------------S---------------------------------T-----C-FG---------------------------------------------------S--------L-----H--PF-----------------------------------------------------Q-----------------------S------------L---K-----P-------V-----------------MAN-A--LG-------------------------------------------------------V-LEGKM-FC-------SIGGRSL---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: MAT------LL--------R-----S---------------L-----A----------LF-----K------------------------------------------R----------NKDKP---------------------------------------------P----------IT---------------------------S--G-------------------S-G-GAI----------------------------------------------------------R---------G--------------IK----HIII--------------------------------V--P--------I-------------------------P----GD----S----------------------------------------------------------------------------------------------S-------I-T--T---------R-------------------------------------------------------------------------SR------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: M------ESL-------V--PGFN---E--------K-T---------------H------------------------------------------------------------------------------------------------------------VQLS-LP-------------------------------------------------------------------------------------------------------------V-------------LQ-VRDVLV----RGF----------GD--------------S------------------MEE-------V-------------------L----------------------------S------E-A-----------------------R--QHL-------KDG-------------------------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N-L-------------------------------------------------------T---------T--------G----------------TQ--LP-------PA-------------------------------------------------------------------------------------------------YT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--HS-------------------------------------------------------------
> str36: MA----------NI--------------------I-----NL--------------------------------------------------------------------------------------------------------------------------------W---NG----I--------------------------------------------------------------------------------------------------V-------------------------------------------------------------------------------P-------------------------------M--------------------------------------------------------------------------------------------V-----------QD-------------V--N----VA---S---I-T---A----FK----------------------------------------------------------------S------------------MIDE---------------------------------------------------------T-----------------------------------------------------------W-D------------KKI-EA---N------------TC------I-------------------S--RKHRN-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str37: M--------L--N------R--------------I----Q----------------------------------T---L--MK--------------------------------------------------------------------------------------------------TA-------------------------N-----------------N---------------------------Y---E----------------------T-----IEI---L---R-----N------Y----------------------L----------------------------------------------------------------------------------------------------------------R----L---------------------------------------------------------Y------I-----------I--------------------LA---R---------N----EEG---------------------------RGILI------------------------------------YD--D-----------NI-D---------------------S------------------------------------V--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str38: MA-D-P--------A------G----------------T-N---------GEEG--------------------TGC------NG-------------------------------------------------------------------------------------WF----------------------------------------------------------------------------------Y------------------------V---EA-----------V--V---------------E-------K--------K----------------------------T--------G---DAI------------------------------------S----DDEN-E------------ND----------------------------------------------------------------------S-------------D-------T-G----ED----------L--------------------------------------------------------------------------------------V----D-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str39: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V-----------------------N-LR------------------------------------------------------T------------------------------------------------------------------------------------RT-Q-L------------------PP------------------------------------SYT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--HS-------------------------------------------------------------
> str40: M------ESL-------V--PGFN---E--------K-T---------------H------------------------------------------------------------------------------------------------------------VQLS-LP-------------------------------------------------------------------------------------------------------------V-------------LQ-V---------------CD--------------------------------------------------V-------------------L---------------------------------------------------------------------------------------------------V-----------------RGFGD-S--VE------------------------E--------------------------------------------------------------------------------------------------VL-S-----EA---------------------------RQHLKDG----T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M-----------N----------N---------------Q--------------------------------------------------------------------R-------KK---------------------------------------------------------------TARP------------------------SF---------------NMLK-------------------------------------------------------------------R-------------A--------------------------------------------------------------------------------------------------------------------------------------R------------------N----------R-------V-----------------------S-TV------------SQ-----------------------LA--KRF-------------------------------------------------S---------KG-L----L---------S---------G-------------------Q--G--PMKL---------------------------------------------V-----MAF------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: M-------S---N--FD---------A-------I-------------------------------------------------------------------------RA--------L--------------------------------------------V---------------D-T------DA----------------------------------------------------------------Y---------KLGHIHM-------------------------------Y--------------------------------------------------------P---E------GT-----E-----------------------------------------------------------------------------------------------------------------------------------Y-V-----L------S---------------------------------------NF-TD------------------------------RG----SR-----IEG---------------------V------------------------------------------------T--H----------------------------TVH-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: M------------I-------------E-------------L------------------------------------------------------------------R----HE------------------------------------------------VQ----------G---D-------------------L-------------------------------------------------------------------------------V-T-----I---------------N-----V------------------------------------------------------VE-----T------------------------------PEDLDG-F------------------------------------R-------DF--I-----------------RAHLICLAV----D--------------------T-E-----T--T----------G----------------L-DI---------------------------------------------------------------------------------------Y--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: M--------------F-VF----------------------LVL--------------L--------------------------P----L------------------------------------------------------------------------V--S------S--QC-----------------------------------------------------------------------------------------------------V--------------------------------------------------------------------------M----P------------------------LF------N--LIT-------------------------------------------------T-----------------N---------Q--------------------------------SYT---N---------S--F--TRGV----------------------------------------------------------------------------------------------------------Y----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------YP---D-KV--F------RSSVL--H--------------------------------------------------------------
> str45: M-------S--K----D------------------------LV----A------------------------------------------------------------R---------------------------Q--A----LM-----------------------------------TAR-------------------------------------MKADF-----------------------------------------------------VF-----F------L--------------FV-----------------------L---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W--------------K--A--L-------------------------------------------SLP------------VP-----------------------T--------R-C-QIDMAKKLSA-G--------------------------------------------------------------------------------------------------------------------------------------
> str46: MA------SLLK-------------S---------------L--------------------------------T---LFK---------------------------R------------------------------------------------------------------------T-R----D--------------------------------------------------------Q-PP--LAS--------G------------------------------------------------------------------------S---------GGAI-------------------------------------------------------------------------------------------------R---------G-IK--H---------------------V-----II-------------------V-----L----------IP--G--D---------------------------------------------------------------------S--------------SI--------------V------------------------------------------------T---------------------------R-SR----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M------------------R----------------------V-----------------------------------------------------------------R---G--I--L----------------------------------------------------------------R------------------------N--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-------------------------QQ------------------------------------------------------------------------------------------------------------------W---------WIWTSLGFWMFMICSVVGNLWVTVY------------------------------------------------YG-----V---------P----------V---WKEAKTT
> str48: MA----VE------------P-F--------------------------------------------------------------P----------------------R--------------------------------------------------------------------------RP---------I------------------------------------T-----------------------------------------------------------------R-------------------------------------------------------------P---------------------HA------------------------------S-------------IE-------------------------------------------------------V----D--------------------T-------------S-------G-------------IGG--------------------------------------------------------S-A---G--------S------------SEKV----------FC--LIG---------QAEGGEP---N-----------T--------------------------------V--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: M--------------F------------------------------------------------------------------------------------------------------------------------------------------YA-HAFGG--------------------------------------------------------------------------------------------Y--DE------------NLHAFPG---------I-----------------------------------------------S-------S-----------------T--V---A-----------------------ND------------------------------------------------------------------------------------------V-----------------R----K-Y--------------S--------V------------------------------------------------------------------------------------------------------V--S------------------------------------------------------------------------------V----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y--------------NKK-------------------------------Y-NI---V-KNKY--MW----------------------
> str50: MA----------N---------------------------------------------------------------------------------------------------------------------------------------------Y-----------SK-P-FL--------------------------L-D---I-------------------------------------------------------------------------VF----------------------NK--------D--------IKC----I---------------------------ND------------------------------------------------------S---C------------------------------------------------------------------------------------------S--------------HS----------DC-----------------R-------------------------------------------------------------------------------------Y----------------------Q-----------------S-NS--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Y-------V-E--L----R------------------RNQALNKNL------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 1009
> best bound: 0.0
> wall time: 60.317823s
> ```

元の `WMM_HEXALY` よりもだいぶ悪い結果となった.
