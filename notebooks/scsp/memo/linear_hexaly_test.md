In [ ]:
```python
import opt_note.scsp as scsp
import hexaly.optimizer
import linear_cpsat_test
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# ALPHABET から削り出すやつを Hexaly でやる

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        hxoptimizer = hexaly.optimizer.HexalyOptimizer()
        hxmodel = hxoptimizer.model
        assert isinstance(hxoptimizer, hexaly.optimizer.HexalyOptimizer)
        assert isinstance(hxmodel, hexaly.optimizer.HxModel)

        valids = [hxmodel.bool() for _ in range(max_len)]
        cvars = [
            [
                hxmodel.int(0, max(len(_s) for _s in instance) - 1)
                for c in s
            ]
            for s in instance
        ]

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                hxmodel.constraint(
                    len(chars) * cvars[sidx][cidx - 1] + chars.index(s[cidx - 1])
                    < len(chars) * cvars[sidx][cidx] + chars.index(s[cidx])
                )

        valids_array = hxmodel.array(valids)
        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                hxmodel.constraint(valids_array[len(chars) * cvars[sidx][cidx] + chars.index(c)] == 1)

        hxmodel.minimize(sum(valids))
        hxmodel.close()

        self.instance = instance
        self.chars = chars
        self.hxoptimizer = hxoptimizer
        self.hxmodel = hxmodel
        self.valids = valids
        self.status: hexaly.optimizer.HxSolutionStatus | None = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        assert isinstance(self.hxoptimizer.param, hexaly.optimizer.HxParam)
        if time_limit is not None:
            self.hxoptimizer.param.time_limit = time_limit
        self.hxoptimizer.param.verbosity = 1 if log else 0
        self.hxoptimizer.solve()
        self.status = self.hxoptimizer.solution.status
        return self

    def to_solution(self) -> str | None:
        assert isinstance(self.hxoptimizer.solution, hexaly.optimizer.HxSolution)

        if self.status not in {
            hexaly.optimizer.HxSolutionStatus.OPTIMAL,
            hexaly.optimizer.HxSolutionStatus.FEASIBLE,
        }:
            return None

        solution = ""
        for idx, valid in enumerate(self.valids):
            if valid.value:
                solution += self.chars[idx % len(self.chars)]

        return solution
```

In [ ]:
```python
def bench1(instance: list[str]) -> None:
    model = linear_cpsat_test.Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")
```

In [ ]:
```python
def bench2(instance: list[str]) -> None:
    model = Model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution is optimal: {model.hxoptimizer.solution.status == hexaly.optimizer.HxSolutionStatus.OPTIMAL}")
    print(f"bset bound: {model.hxoptimizer.solution.get_objective_bound(0)}")
```

In [ ]:
```python
instance01 = scsp.example.load("uniform_q26n004k015-025.txt")
```

In [ ]:
```python
bench1(instance01)
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 62) ---
>  Sol: tuklcignyckosuhjmoeiqvafozppglnbrxddxbcsvrsvnhtunqgpxzvxissbxf
> str1: t-k---gn--k--uh-m---------p------x----------nht--qg-xzvxis----
> str2: -----i-----o---j---iq--fo----lnb-x--x-c-v-s----u-q-p--v-issbxf
> str3: -u-lci-nyc-os----o---v--ozpp-l---------------------p----------
> str4: -----ig-----------e--va--z--g--br-dd-bcsvr-vn---n-g----------f
> 
> solution is feasible: True
> solution status: OPTIMAL
> bset bound: 62.0
> ```

In [ ]:
```python
bench2(instance01)
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 65) ---
>  Sol: itkgnekulvachmopxjinyzchotqsfgovborzdppdlnbxxcvzsuqvxprvinsnsbgxf
> str1: -tkgn-ku----hm-px--n---h-tq--g-------------x---z---vx---i-s------
> str2: i-------------o--ji-------q-f-o---------lnbxxcv-suq--p-vi-s-sb-xf
> str3: -------ul--c------iny-c-o--s--ov-o-z-pp-l------------p-----------
> str4: i--g-e---va----------z-------g--b-r-d--d--b--c--s--v--rv-n-n--g-f
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 32
> ```

In [ ]:
```python
instance02 = scsp.example.load("uniform_q26n008k015-025.txt")
```

In [ ]:
```python
bench1(instance02)
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
> --- Solution (of length 103) ---
>  Sol: iorxgjpwxbdeiqtvyafkopzglnrbdkruxzhlmpxcinuvyzcfhjopstumoqvdpgotxdefrzbuvxcisvcdmpsbroqvnnbibgpxflpwdeh
> str1: --------------t----k---g-n---k-u--h-mpx--n------h----t---q---g--x----z--vx-is--------------------------
> str2: io---j------iq----f-o---ln-b----x-----xc---v--------s-u--q--p-----------v--is-----sb-----------xf------
> str3: -------------------------------u---l---cin--y-c---o-s---o-v---o------z-----------p------------p--lp----
> str4: i---g------e---v-a----zg---b--r----------------------------d-----d----b---c-sv------r--vnn---g--f------
> str5: ------p---------y----p--l-r------z----x---u---c----p---m-qv--g-t-d-f---u---i-vcd--sb-o-----------------
> str6: ------p--bde---v------------d----------c---v---------------dp------f-z------s---m-sbroqv--b-b---------h
> str7: -----------e-------------n-b-----------c-----z-f-j---t----v-----x-e-rzb-------------r--v---i-gp--l---e-
> str8: --rx---wx----q-----k------r-d-r----l---c-------------t--o--d---t----------------mp--r---------px---wd--
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 75.0
> ```

In [ ]:
```python
bench2(instance02)
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
> --- Solution (of length 114) ---
>  Sol: ioprtxybdjkpwxginqefkovalnrzgxbdrucdlpvcdhmpqtvxzbfgijotvxzdenrsycfhtuimqvcgsuxzbqropqvdisborsvnnozbgpxlpwdefhilps
> str1: ----t-----k---g-n---k------------u-------hmp---x-------------n-----ht---q--g--xz------v---------------x-------i--s
> str2: io-------j-----i-q-f-o--ln----b----------------x---------x-------c-------v--su---q--p-v-is---s-----b--x-----f-----
> str3: ---------------------------------u--l--c------------i--------n--yc-----------------o-----s-o--v--oz--p--p------lp-
> str4: i-------------g---e---va---zg-b-r--d----d--------b---------------c----------s---------v-----r-vnn---g-------f-----
> str5: --p---y----p------------l-rz-x---uc--p----m-q-v----g---t---d------f--ui--vc------------d-sbo----------------------
> str6: --p----bd---------e---v--------d--c---v-d--p------f-------z----s-------m----s---b-ro-qv---b--------b---------h----
> str7: ------------------e------n----b---c-------------z-f--j-tvx--e-r----------------zb-r---v-i-----------gp-l---e------
> str8: ---r-x------wx---q--k-----r----dr---l--c-----t--------o----d--------t--m------------p-------r--------px--wd-------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 40
> ```

In [ ]:
```python
instance03 = scsp.example.load("uniform_q26n016k015-025.txt")
```

In [ ]:
```python
bench1(instance03)
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
> --- Solution (of length 146) ---
>   Sol: hklrtxioujkswxgipqbdefovajlnyzcfgpbklrsxzdxachuvcdipsuefhmnqrvzeflbcgpqsvdijqrtvwxybcenorzadhkmnstwbfkmorsuvgioquvzcdgkprsxzbjopvxbhlmwdefgimpsuwy
> str01: ----t-----k---g------------n-------k----------u---------hm-----------p-----------x----n-----h----t-------------q-----g----xz----vx---------i--s---
> str02: ------io-j-----i-q---fo---ln------b----x--x-c--v----su-----q---------p--v-i---------------------s--------s------------------b----x-------f--------
> str03: --------u-----------------l---c-------------------i-------n-----------------------y-c--o--------s------o---v--o---z----p-------p----l--------p----
> str04: ------i-------g-----e--va----z--g-b--r---d-------d----------------bc---sv----r-v------n--------n------------g----------------------------f--------
> str05: ----------------p-----------y----p--lr--z-x---u-c--p-----m-q-v------g---------t------------d--------f-----u--i---v-cd----s--b-o-------------------
> str06: ----------------p-bde--v-----------------d--c--v-d-p---f------z--------s----------------------m-s--b----r-----oq-v----------b-----bh--------------
> str07: --------------------e------n------b---------c-----------------z-f----------j--tv-x---e--rz---------b----r--v-i-------g-p------------l---e---------
> str08: ---r-x------wx---q-----------------k-r---d------------------r----l-c----------t--------o---d-----t----m----------------pr------p-x----wd----------
> str09: -k--------k------q------a------f------------------i-----------------g-q----j----w------o-----k-------k---s------------k-r---b-------l-----g-------
> str10: --l--x-------x--p-------a---------b---------------i----------v----b-----v----------------z---k---------o----------z--------z----v------d----------
> str11: -k-r--i--------------f----------------s----a---v----------n--------c-----d--q---w-----------h---------------------zc------------------------------
> str12: -----------------q------a--------------x------u--d------------------g-q-v---q-------ce------------wbf-------gi---------------jo-------w---------wy
> str13: ---r-------s-x---q-------j-n---f-p---------a-----di--u-----------------s--i-q------b-e---z--hk---------o---------------------------h-m----g-------
> str14: ------i-----w-------------------------s------h-v--------h----------c-------------------o------m--------------i--uv--d------------------d----m-----
> str15: h---tx-------x---q-------j---z-----------------------------q------bc----------t----b------a--k-n--------------------------------------------------
> str16: -----x--u--s---------f--------cf--------z----------p--e--------e---c----v-------w---------a----n-t--f-m-----g--q--z----------------------------u--
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 82.0
> ```

In [ ]:
```python
bench2(instance03)
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
> --- Solution (of length 166) ---
>   Sol: ehiknoprtwxybdjkpqsuwafghlrsxzeuvacdinqxyzcfgoqsuvajqtceknpuwzbfghijlmopqrdnrvabglzcptxdefiouxeiknrsvzbcdhikpstvmqsubeqrwzahknopqrtvbfhimglnpqsznsuvxzbdglvwxcdefhimsy
> str01: --------t------k-------g-------------n------------------k--u-----h---m-p--------------x----------n-------h----t--q-----------------------g----------xz----v-x-----i-s-
> str02: --i--o--------j---------------------i-q----f-o----------------------l------n---b------x------x---------c-------v--su--q--------p---v---i------s--s----b-----x---f-----
> str03: -------------------u-----l--------c-in--y-c--o-s----------------------o------v-------------o---------z------p------------------p----------l-p-------------------------
> str04: --i--------------------g------e-va-------z--g-----------------b----------rd------------d--------------bc-----s-v-------r-----------v-------n----n-------g-------f-----
> str05: ------p----y----p--------lr--z---------x--------u-----c---p----------m--q----v--g----t-d-f--u--i----v--cd----s------b---------o---------------------------------------
> str06: ------p-----bd----------------e-v--d------c------v------------------------d---------p----f-----------z-------s--m-s-b--r------o-q--vb-----------------b----------h----
> str07: e---n-------b---------------------c------z-f-------j-t-----------------------v--------x-e---------r--zb----------------r-----------v---i-g--p------------l-----e------
> str08: -------r--x---------w-------x---------q-----------------k----------------rd-r----l-c-t-----o------------d-----t-m--------------p-r----------p-------x------w--d-------
> str09: ---k-----------k-q---af-------------i-------g-q----j--------w---------o-------------------------k----------k-s--------------k----r--b-----l-------------g-------------
> str10: -------------------------l--x----------x------------------p-------------------ab----------i---------v-b--------v---------z--k-o----------------z-----z----v---d-------
> str11: ---k---r----------------------------i------f---s--a--------------------------v-------------------n-----cd--------q------w--h-------------------z-------------c--------
> str12: -----------------q---a------x--u---d--------g-q--v--q-ce----w-bfg-ij--o-------------------------------------------------w----------------------------------w---------y
> str13: -------r----------s---------x---------q------------j-----n-----f-------p------a--------d--i-u------s------i------q--be---z-hk-o-------h-mg----------------------------
> str14: --i------w--------s-----h-------v--------------------------------h-----------------c-------o--------------------m----------------------i----------uv---d------d----m--
> str15: -h------t-x-----------------x---------q------------j---------z----------q------b---c-t----------------b-------------------a-kn----------------------------------------
> str16: ----------x--------u-------s---------------f----------c--------f------------------z-p---e-----e--------c-------v--------w-a--n----t--f--mg---q-z--u-------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 35
> ```

CP-SAT には勝てなそうですね...

Hexaly に関しては Weighted Majority Merge をベースにしたものの方が良さげ.

## ログを見よう

In [ ]:
```python
instance04 = scsp.example.load("uniform_q05n010k010-010.txt")
instance05 = scsp.example.load("uniform_q05n050k010-010.txt")
instance06 = scsp.example.load("nucleotide_n010k010.txt")
instance07 = scsp.example.load("nucleotide_n050k050.txt")
instance08 = scsp.example.load("protein_n010k010.txt")
instance09 = scsp.example.load("protein_n050k050.txt")
```

In [ ]:
```python
_model = Model(instance01)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 2097, decisions = 709, constraints = 164, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 111)
> [  1 sec,  251193 itr]:           70
> [  2 sec,  536299 itr]:           70
> [  3 sec,  860414 itr]:           68
> [  4 sec,  860414 itr]:           68
> [  5 sec, 1196162 itr]:           68
> [  6 sec, 1560312 itr]:           68
> [  7 sec, 1864670 itr]:           67
> [  8 sec, 1864670 itr]:           67
> [  9 sec, 2536200 itr]:           66
> [ 10 sec, 2836152 itr]:           66
> [ optimality gap     ]:       53.03%
> [ 11 sec, 3157457 itr]:           66
> [ 12 sec, 3491245 itr]:           66
> [ 13 sec, 3491245 itr]:           66
> [ 14 sec, 4169447 itr]:           66
> [ 15 sec, 4479625 itr]:           66
> [ 16 sec, 4817293 itr]:           66
> [ 17 sec, 5203556 itr]:           66
> [ 18 sec, 5203556 itr]:           66
> [ 19 sec, 5868778 itr]:           66
> [ 20 sec, 5868778 itr]:           66
> [ optimality gap     ]:       53.03%
> [ 21 sec, 6197674 itr]:           66
> [ 22 sec, 6479328 itr]:           66
> [ 23 sec, 6750990 itr]:           66
> [ 24 sec, 7032401 itr]:           66
> [ 25 sec, 7528503 itr]:           66
> [ 26 sec, 7802486 itr]:           66
> [ 27 sec, 8082161 itr]:           66
> [ 28 sec, 8383539 itr]:           66
> [ 29 sec, 8711559 itr]:           66
> [ 30 sec, 9042612 itr]:           66
> [ optimality gap     ]:       53.03%
> [ 31 sec, 9354399 itr]:           66
> [ 32 sec, 9637788 itr]:           66
> [ 33 sec, 9930372 itr]:           66
> [ 34 sec, 10210336 itr]:           66
> [ 35 sec, 10557500 itr]:           66
> [ 36 sec, 10870062 itr]:           66
> [ 37 sec, 11191285 itr]:           66
> [ 38 sec, 11370549 itr]:           66
> [ 39 sec, 11532507 itr]:           66
> [ 40 sec, 11820374 itr]:           66
> [ optimality gap      ]:       53.03%
> [ 41 sec, 12155586 itr]:           66
> [ 42 sec, 12427875 itr]:           66
> [ 43 sec, 12427875 itr]:           66
> [ 44 sec, 13068255 itr]:           66
> [ 45 sec, 13068255 itr]:           66
> [ 46 sec, 13688261 itr]:           66
> [ 47 sec, 14004867 itr]:           66
> [ 48 sec, 14317880 itr]:           66
> [ 49 sec, 14645023 itr]:           66
> [ 50 sec, 14959921 itr]:           66
> [ optimality gap      ]:       51.52%
> [ 51 sec, 14959921 itr]:           66
> [ 52 sec, 15619970 itr]:           66
> [ 53 sec, 15894299 itr]:           66
> [ 54 sec, 16230448 itr]:           66
> [ 55 sec, 16586047 itr]:           66
> [ 56 sec, 16898171 itr]:           66
> [ 57 sec, 17207954 itr]:           65
> [ 58 sec, 17207954 itr]:           65
> [ 59 sec, 17806645 itr]:           65
> [ 60 sec, 18113298 itr]:           65
> [ optimality gap      ]:       50.77%
> [ 61 sec, 18415183 itr]:           65
> [ 62 sec, 18726356 itr]:           65
> [ 63 sec, 19039001 itr]:           65
> [ 64 sec, 19339561 itr]:           65
> [ 65 sec, 19635032 itr]:           65
> [ 66 sec, 19635032 itr]:           65
> [ 67 sec, 20251803 itr]:           65
> [ 68 sec, 20554136 itr]:           65
> [ 69 sec, 20554136 itr]:           65
> [ 70 sec, 21162646 itr]:           65
> [ optimality gap      ]:       50.77%
> [ 71 sec, 21162646 itr]:           65
> [ 72 sec, 21524056 itr]:           65
> [ 73 sec, 21810295 itr]:           65
> [ 74 sec, 22121842 itr]:           65
> [ 75 sec, 22435688 itr]:           65
> [ 76 sec, 22746948 itr]:           65
> [ 77 sec, 23071343 itr]:           65
> [ 78 sec, 23357375 itr]:           65
> [ 79 sec, 23659226 itr]:           65
> [ 80 sec, 23969726 itr]:           65
> [ optimality gap      ]:       49.23%
> [ 81 sec, 24270628 itr]:           65
> [ 82 sec, 24565152 itr]:           65
> [ 83 sec, 24565152 itr]:           65
> [ 84 sec, 25158883 itr]:           65
> [ 85 sec, 25492425 itr]:           65
> [ 86 sec, 25822883 itr]:           65
> [ 87 sec, 26117215 itr]:           65
> [ 88 sec, 26412059 itr]:           65
> [ 89 sec, 26412059 itr]:           65
> [ 90 sec, 27084890 itr]:           65
> [ optimality gap      ]:       47.69%
> [ 91 sec, 27084890 itr]:           65
> [ 92 sec, 27742824 itr]:           65
> [ 93 sec, 28023729 itr]:           65
> [ 94 sec, 28321053 itr]:           65
> [ 95 sec, 28653748 itr]:           65
> [ 96 sec, 28653748 itr]:           65
> [ 97 sec, 29228704 itr]:           65
> [ 98 sec, 29528032 itr]:           65
> [ 99 sec, 29833257 itr]:           65
> [100 sec, 30123008 itr]:           65
> [ optimality gap      ]:       46.15%
> [101 sec, 30414437 itr]:           65
> [102 sec, 30709085 itr]:           65
> [103 sec, 30709085 itr]:           65
> [104 sec, 31011305 itr]:           65
> [105 sec, 31373521 itr]:           65
> [106 sec, 31373521 itr]:           65
> [107 sec, 31683717 itr]:           65
> [108 sec, 31959538 itr]:           65
> [109 sec, 32246736 itr]:           65
> [110 sec, 32718305 itr]:           65
> [ optimality gap      ]:       44.62%
> [111 sec, 32949422 itr]:           65
> [112 sec, 33228999 itr]:           65
> [113 sec, 33479210 itr]:           65
> [114 sec, 33714194 itr]:           65
> [115 sec, 33984001 itr]:           65
> [116 sec, 33984001 itr]:           65
> [117 sec, 34232359 itr]:           65
> [118 sec, 34750322 itr]:           65
> [119 sec, 35007121 itr]:           65
> [120 sec, 35007121 itr]:           65
> [ optimality gap      ]:       44.62%
> [120 sec, 35244706 itr]:           65
> [ optimality gap      ]:       44.62%
> 
> 35244706 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =           65
>   gap    =       44.62%
>   bounds =           36
> ```

In [ ]:
```python
_model = Model(instance02)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 3038, decisions = 825, constraints = 342, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 262)
> [  1 sec,   49921 itr]:          130
> [  2 sec,  225192 itr]:          125
> [  3 sec,  225192 itr]:          125
> [  4 sec,  564950 itr]:          118
> [  5 sec,  751625 itr]:          117
> [  6 sec,  919208 itr]:          117
> [  7 sec, 1113245 itr]:          115
> [  8 sec, 1113245 itr]:          115
> [  9 sec, 1508946 itr]:          115
> [ 10 sec, 1508946 itr]:          115
> [ optimality gap     ]:       71.30%
> [ 11 sec, 1900979 itr]:          115
> [ 12 sec, 2088260 itr]:          115
> [ 13 sec, 2263748 itr]:          115
> [ 14 sec, 2457569 itr]:          115
> [ 15 sec, 2651590 itr]:          115
> [ 16 sec, 2842235 itr]:          115
> [ 17 sec, 3031432 itr]:          115
> [ 18 sec, 3216755 itr]:          115
> [ 19 sec, 3421492 itr]:          115
> [ 20 sec, 3421492 itr]:          115
> [ optimality gap     ]:       69.57%
> [ 21 sec, 3806001 itr]:          115
> [ 22 sec, 4002053 itr]:          115
> [ 23 sec, 4205015 itr]:          115
> [ 24 sec, 4205015 itr]:          115
> [ 25 sec, 4604922 itr]:          114
> [ 26 sec, 4604922 itr]:          114
> [ 27 sec, 4777381 itr]:          114
> [ 28 sec, 5155645 itr]:          114
> [ 29 sec, 5359852 itr]:          114
> [ 30 sec, 5552027 itr]:          114
> [ optimality gap     ]:       67.54%
> [ 31 sec, 5693134 itr]:          114
> [ 32 sec, 5693134 itr]:          114
> [ 33 sec, 5981008 itr]:          114
> [ 34 sec, 5981008 itr]:          114
> [ 35 sec, 6373436 itr]:          114
> [ 36 sec, 6580055 itr]:          114
> [ 37 sec, 6784229 itr]:          114
> [ 38 sec, 6784229 itr]:          114
> [ 39 sec, 6989659 itr]:          114
> [ 40 sec, 7405372 itr]:          114
> [ optimality gap     ]:       67.54%
> [ 41 sec, 7405372 itr]:          114
> [ 42 sec, 7614761 itr]:          114
> [ 43 sec, 7797340 itr]:          114
> [ 44 sec, 8166712 itr]:          114
> [ 45 sec, 8166712 itr]:          114
> [ 46 sec, 8371496 itr]:          114
> [ 47 sec, 8788352 itr]:          114
> [ 48 sec, 8970191 itr]:          114
> [ 49 sec, 8970191 itr]:          114
> [ 50 sec, 9330794 itr]:          114
> [ optimality gap     ]:       67.54%
> [ 51 sec, 9504891 itr]:          114
> [ 52 sec, 9681219 itr]:          114
> [ 53 sec, 9884406 itr]:          114
> [ 54 sec, 10049881 itr]:          114
> [ 55 sec, 10232153 itr]:          114
> [ 56 sec, 10411271 itr]:          114
> [ 57 sec, 10411271 itr]:          114
> [ 58 sec, 10798708 itr]:          114
> [ 59 sec, 11011128 itr]:          114
> [ 60 sec, 11186208 itr]:          114
> [ optimality gap      ]:       67.54%
> [ 61 sec, 11186208 itr]:          114
> [ 62 sec, 11553299 itr]:          114
> [ 63 sec, 11553299 itr]:          114
> [ 64 sec, 11836032 itr]:          114
> [ 65 sec, 11910812 itr]:          114
> [ 66 sec, 12064495 itr]:          113
> [ 67 sec, 12215241 itr]:          113
> [ 68 sec, 12383452 itr]:          113
> [ 69 sec, 12529644 itr]:          113
> [ 70 sec, 12676546 itr]:          113
> [ optimality gap      ]:       64.60%
> [ 71 sec, 12676546 itr]:          113
> [ 72 sec, 12996645 itr]:          113
> [ 73 sec, 13160219 itr]:          113
> [ 74 sec, 13321593 itr]:          113
> [ 75 sec, 13483899 itr]:          113
> [ 76 sec, 13652959 itr]:          113
> [ 77 sec, 13652959 itr]:          113
> [ 78 sec, 13823370 itr]:          113
> [ 79 sec, 14173847 itr]:          113
> [ 80 sec, 14348622 itr]:          113
> [ optimality gap      ]:       64.60%
> [ 81 sec, 14523290 itr]:          113
> [ 82 sec, 14688205 itr]:          113
> [ 83 sec, 14843182 itr]:          113
> [ 84 sec, 14843182 itr]:          113
> [ 85 sec, 15170345 itr]:          113
> [ 86 sec, 15341556 itr]:          113
> [ 87 sec, 15501796 itr]:          113
> [ 88 sec, 15644781 itr]:          113
> [ 89 sec, 15813617 itr]:          113
> [ 90 sec, 15976443 itr]:          113
> [ optimality gap      ]:       64.60%
> [ 91 sec, 16132463 itr]:          113
> [ 92 sec, 16132463 itr]:          113
> [ 93 sec, 16301048 itr]:          113
> [ 94 sec, 16625281 itr]:          113
> [ 95 sec, 16788339 itr]:          113
> [ 96 sec, 16788339 itr]:          113
> [ 97 sec, 16927069 itr]:          113
> [ 98 sec, 17133581 itr]:          113
> [ 99 sec, 17133581 itr]:          113
> [100 sec, 17311323 itr]:          113
> [ optimality gap      ]:       64.60%
> [101 sec, 17470913 itr]:          113
> [102 sec, 17627811 itr]:          113
> [103 sec, 17945893 itr]:          113
> [104 sec, 18103630 itr]:          113
> [105 sec, 18289702 itr]:          113
> [106 sec, 18453025 itr]:          113
> [107 sec, 18615143 itr]:          113
> [108 sec, 18761114 itr]:          113
> [109 sec, 18926224 itr]:          113
> [110 sec, 19091795 itr]:          113
> [ optimality gap      ]:       64.60%
> [111 sec, 19254777 itr]:          113
> [112 sec, 19254777 itr]:          113
> [113 sec, 19410799 itr]:          113
> [114 sec, 19568267 itr]:          113
> [115 sec, 19883040 itr]:          110
> [116 sec, 20037054 itr]:          110
> [117 sec, 20037054 itr]:          110
> [118 sec, 20351231 itr]:          109
> [119 sec, 20351231 itr]:          109
> [120 sec, 20679198 itr]:          109
> [ optimality gap      ]:       63.30%
> [120 sec, 20679198 itr]:          109
> [ optimality gap      ]:       63.30%
> 
> 20679198 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =          109
>   gap    =       63.30%
>   bounds =           40
> ```

In [ ]:
```python
_model = Model(instance03)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 4478, decisions = 973, constraints = 630, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 479)
> [  1 sec,  104609 itr]:          191
> [  2 sec,  172981 itr]:          185
> [  3 sec,  172981 itr]:          185
> [  4 sec,  398815 itr]:          176
> [  5 sec,  398815 itr]:          176
> [  6 sec,  622487 itr]:          176
> [  7 sec,  622487 itr]:          176
> [  8 sec,  804829 itr]:          174
> [  9 sec,  929683 itr]:          174
> [ 10 sec, 1017967 itr]:          173
> [ optimality gap     ]:       82.08%
> [ 11 sec, 1017967 itr]:          173
> [ 12 sec, 1200507 itr]:          173
> [ 13 sec, 1200507 itr]:          173
> [ 14 sec, 1313500 itr]:          171
> [ 15 sec, 1555283 itr]:          169
> [ 16 sec, 1555283 itr]:          169
> [ 17 sec, 1803108 itr]:          169
> [ 18 sec, 1922853 itr]:          169
> [ 19 sec, 1922853 itr]:          169
> [ 20 sec, 2162047 itr]:          169
> [ optimality gap     ]:       81.07%
> [ 21 sec, 2162047 itr]:          169
> [ 22 sec, 2264266 itr]:          168
> [ 23 sec, 2490334 itr]:          168
> [ 24 sec, 2604100 itr]:          168
> [ 25 sec, 2604100 itr]:          168
> [ 26 sec, 2849937 itr]:          167
> [ 27 sec, 2965080 itr]:          167
> [ 28 sec, 3089179 itr]:          167
> [ 29 sec, 3210332 itr]:          167
> [ 30 sec, 3327689 itr]:          167
> [ optimality gap     ]:       80.24%
> [ 31 sec, 3442694 itr]:          167
> [ 32 sec, 3536194 itr]:          167
> [ 33 sec, 3629650 itr]:          167
> [ 34 sec, 3693915 itr]:          167
> [ 35 sec, 3783326 itr]:          167
> [ 36 sec, 3783326 itr]:          167
> [ 37 sec, 4046980 itr]:          166
> [ 38 sec, 4178953 itr]:          166
> [ 39 sec, 4299190 itr]:          166
> [ 40 sec, 4299190 itr]:          166
> [ optimality gap     ]:       78.92%
> [ 41 sec, 4556817 itr]:          166
> [ 42 sec, 4675681 itr]:          166
> [ 43 sec, 4802749 itr]:          166
> [ 44 sec, 4935684 itr]:          166
> [ 45 sec, 5027897 itr]:          166
> [ 46 sec, 5027897 itr]:          166
> [ 47 sec, 5137601 itr]:          166
> [ 48 sec, 5350817 itr]:          166
> [ 49 sec, 5472197 itr]:          166
> [ 50 sec, 5577861 itr]:          166
> [ optimality gap     ]:       78.92%
> [ 51 sec, 5695493 itr]:          166
> [ 52 sec, 5817187 itr]:          166
> [ 53 sec, 5931625 itr]:          166
> [ 54 sec, 6049026 itr]:          166
> [ 55 sec, 6156308 itr]:          166
> [ 56 sec, 6274280 itr]:          166
> [ 57 sec, 6386486 itr]:          166
> [ 58 sec, 6498603 itr]:          166
> [ 59 sec, 6498603 itr]:          166
> [ 60 sec, 6714767 itr]:          166
> [ optimality gap     ]:       78.92%
> [ 61 sec, 6714767 itr]:          166
> [ 62 sec, 6934810 itr]:          166
> [ 63 sec, 6934810 itr]:          166
> [ 64 sec, 7145598 itr]:          166
> [ 65 sec, 7145598 itr]:          166
> [ 66 sec, 7258807 itr]:          166
> [ 67 sec, 7424935 itr]:          166
> [ 68 sec, 7424935 itr]:          166
> [ 69 sec, 7649014 itr]:          166
> [ 70 sec, 7757371 itr]:          166
> [ optimality gap     ]:       78.92%
> [ 71 sec, 7757371 itr]:          166
> [ 72 sec, 8003755 itr]:          166
> [ 73 sec, 8116265 itr]:          166
> [ 74 sec, 8116265 itr]:          166
> [ 75 sec, 8346135 itr]:          166
> [ 76 sec, 8461433 itr]:          166
> [ 77 sec, 8556036 itr]:          166
> [ 78 sec, 8556036 itr]:          166
> [ 79 sec, 8784236 itr]:          166
> [ 80 sec, 8903953 itr]:          166
> [ optimality gap     ]:       78.92%
> [ 81 sec, 9014678 itr]:          166
> [ 82 sec, 9121239 itr]:          166
> [ 83 sec, 9244670 itr]:          166
> [ 84 sec, 9356562 itr]:          166
> [ 85 sec, 9479038 itr]:          165
> [ 86 sec, 9592058 itr]:          165
> [ 87 sec, 9592058 itr]:          165
> [ 88 sec, 9814381 itr]:          165
> [ 89 sec, 9814381 itr]:          165
> [ 90 sec, 10031945 itr]:          165
> [ optimality gap      ]:       78.79%
> [ 91 sec, 10146371 itr]:          165
> [ 92 sec, 10146371 itr]:          165
> [ 93 sec, 10251584 itr]:          165
> [ 94 sec, 10492420 itr]:          165
> [ 95 sec, 10492420 itr]:          165
> [ 96 sec, 10727220 itr]:          165
> [ 97 sec, 10727220 itr]:          165
> [ 98 sec, 10942210 itr]:          165
> [ 99 sec, 11058226 itr]:          165
> [100 sec, 11110824 itr]:          165
> [ optimality gap      ]:       78.79%
> [101 sec, 11227277 itr]:          165
> [102 sec, 11332310 itr]:          165
> [103 sec, 11332310 itr]:          165
> [104 sec, 11566437 itr]:          165
> [105 sec, 11666099 itr]:          165
> [106 sec, 11783418 itr]:          165
> [107 sec, 11898901 itr]:          165
> [108 sec, 11898901 itr]:          165
> [109 sec, 12118796 itr]:          165
> [110 sec, 12240533 itr]:          165
> [ optimality gap      ]:       77.58%
> [111 sec, 12346728 itr]:          165
> [112 sec, 12452822 itr]:          165
> [113 sec, 12566345 itr]:          165
> [114 sec, 12692769 itr]:          165
> [115 sec, 12806815 itr]:          165
> [116 sec, 12924922 itr]:          165
> [117 sec, 13036580 itr]:          165
> [118 sec, 13143741 itr]:          165
> [119 sec, 13252927 itr]:          164
> [120 sec, 13252927 itr]:          164
> [ optimality gap      ]:       77.44%
> [120 sec, 13359014 itr]:          164
> [ optimality gap      ]:       76.83%
> 
> 13359014 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =          164
>   gap    =       76.83%
>   bounds =           38
> ```

In [ ]:
```python
_model = Model(instance04)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 1058, decisions = 150, constraints = 190, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 144)
> [  1 sec,  140372 itr]:           31
> [  2 sec,  571389 itr]:           30
> [  3 sec,  571389 itr]:           30
> [  4 sec,  947718 itr]:           30
> [  5 sec, 1309460 itr]:           29
> [  6 sec, 1583413 itr]:           29
> [  7 sec, 1887644 itr]:           29
> [  8 sec, 2139257 itr]:           29
> [  9 sec, 2443719 itr]:           29
> [ 10 sec, 2705361 itr]:           29
> [ optimality gap     ]:       34.48%
> [ 11 sec, 3279622 itr]:           29
> [ 12 sec, 3583311 itr]:           29
> [ 13 sec, 3583311 itr]:           29
> [ 14 sec, 4167049 itr]:           29
> [ 15 sec, 4465952 itr]:           29
> [ 16 sec, 4745265 itr]:           29
> [ 17 sec, 5035782 itr]:           29
> [ 18 sec, 5341573 itr]:           29
> [ 19 sec, 5619965 itr]:           29
> [ 20 sec, 5619965 itr]:           29
> [ optimality gap     ]:       31.03%
> [ 21 sec, 6216448 itr]:           29
> [ 22 sec, 6488039 itr]:           29
> [ 23 sec, 6793310 itr]:           29
> [ 24 sec, 6793310 itr]:           29
> [ 25 sec, 7081852 itr]:           29
> [ 26 sec, 7696455 itr]:           29
> [ 27 sec, 7970104 itr]:           29
> [ 28 sec, 7970104 itr]:           29
> [ 29 sec, 8574866 itr]:           29
> [ 30 sec, 8825871 itr]:           29
> [ optimality gap     ]:       31.03%
> [ 31 sec, 8825871 itr]:           29
> [ 32 sec, 9258300 itr]:           29
> [ 33 sec, 9258300 itr]:           29
> [ 34 sec, 9638417 itr]:           29
> [ 35 sec, 9638417 itr]:           29
> [ 35 sec, 9908565 itr]:           29
> [ optimality gap     ]:           0%
> 
> 9908565 iterations performed in 35 seconds
> 
> Optimal solution: 
>   obj    =           29
>   gap    =           0%
>   bounds =           29
> ```

In [ ]:
```python
_model = Model(instance05)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 4858, decisions = 550, constraints = 950, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 753)
> [  1 sec,       0 itr]: No feasible solution found (infeas = 753)
> [  2 sec,  121852 itr]:           38
> [ optimality gap     ]:       60.53%
> [  3 sec,  155923 itr]:           38
> [  4 sec,  203018 itr]:           37
> [  5 sec,  203018 itr]:           37
> [  6 sec,  314719 itr]:           37
> [  7 sec,  314719 itr]:           37
> [  8 sec,  370793 itr]:           37
> [  9 sec,  505977 itr]:           37
> [ 10 sec,  505977 itr]:           37
> [ 11 sec,  603908 itr]:           37
> [ 12 sec,  682944 itr]:           37
> [ optimality gap     ]:       40.54%
> [ 13 sec,  852674 itr]:           37
> [ 14 sec,  852674 itr]:           37
> [ 15 sec, 1021421 itr]:           37
> [ 16 sec, 1021421 itr]:           37
> [ 17 sec, 1168997 itr]:           37
> [ 18 sec, 1168997 itr]:           37
> [ 19 sec, 1297318 itr]:           37
> [ 20 sec, 1361659 itr]:           37
> [ 21 sec, 1361659 itr]:           36
> [ 22 sec, 1402243 itr]:           36
> [ optimality gap     ]:       38.89%
> [ 23 sec, 1519512 itr]:           36
> [ 24 sec, 1519512 itr]:           36
> [ 25 sec, 1661211 itr]:           36
> [ 26 sec, 1729781 itr]:           36
> [ 27 sec, 1729781 itr]:           36
> [ 28 sec, 1791297 itr]:           36
> [ 29 sec, 1939698 itr]:           36
> [ 30 sec, 1939698 itr]:           36
> [ 31 sec, 2072765 itr]:           36
> [ 32 sec, 2072765 itr]:           36
> [ optimality gap     ]:       38.89%
> [ 33 sec, 2147673 itr]:           36
> [ 34 sec, 2217967 itr]:           36
> [ 35 sec, 2291600 itr]:           36
> [ 36 sec, 2447326 itr]:           36
> [ 37 sec, 2520900 itr]:           36
> [ 38 sec, 2583273 itr]:           36
> [ 39 sec, 2583273 itr]:           36
> [ 40 sec, 2700094 itr]:           36
> [ 41 sec, 2700094 itr]:           36
> [ 42 sec, 2760860 itr]:           36
> [ optimality gap     ]:       38.89%
> [ 43 sec, 2821793 itr]:           36
> [ 44 sec, 2874465 itr]:           36
> [ 45 sec, 2989124 itr]:           36
> [ 46 sec, 2989124 itr]:           36
> [ 47 sec, 3051693 itr]:           36
> [ 48 sec, 3169555 itr]:           36
> [ 49 sec, 3169555 itr]:           36
> [ 50 sec, 3285841 itr]:           36
> [ 51 sec, 3285841 itr]:           36
> [ 52 sec, 3334308 itr]:           36
> [ optimality gap     ]:       38.89%
> [ 53 sec, 3437310 itr]:           36
> [ 54 sec, 3437310 itr]:           36
> [ 55 sec, 3512927 itr]:           36
> [ 56 sec, 3563336 itr]:           36
> [ 57 sec, 3613296 itr]:           36
> [ 58 sec, 3663843 itr]:           36
> [ 59 sec, 3719712 itr]:           36
> [ 60 sec, 3771492 itr]:           36
> [ 61 sec, 3821399 itr]:           36
> [ 62 sec, 3821399 itr]:           36
> [ optimality gap     ]:       38.89%
> [ 63 sec, 3870899 itr]:           36
> [ 64 sec, 3920610 itr]:           36
> [ 65 sec, 4014413 itr]:           36
> [ 66 sec, 4014413 itr]:           36
> [ 67 sec, 4060493 itr]:           36
> [ 68 sec, 4105255 itr]:           36
> [ 69 sec, 4194413 itr]:           36
> [ 70 sec, 4239757 itr]:           36
> [ 71 sec, 4286791 itr]:           36
> [ 72 sec, 4286791 itr]:           36
> [ optimality gap     ]:       38.89%
> [ 73 sec, 4379200 itr]:           35
> [ 74 sec, 4428382 itr]:           35
> [ 75 sec, 4479244 itr]:           35
> [ 76 sec, 4479244 itr]:           35
> [ 77 sec, 4578492 itr]:           35
> [ 78 sec, 4578492 itr]:           35
> [ 79 sec, 4675848 itr]:           35
> [ 80 sec, 4724423 itr]:           35
> [ 81 sec, 4767315 itr]:           35
> [ 82 sec, 4814761 itr]:           35
> [ optimality gap     ]:       37.14%
> [ 83 sec, 4864695 itr]:           35
> [ 84 sec, 4910022 itr]:           35
> [ 85 sec, 4954370 itr]:           35
> [ 86 sec, 5006595 itr]:           35
> [ 87 sec, 5006595 itr]:           35
> [ 88 sec, 5024995 itr]:           35
> [ 89 sec, 5122752 itr]:           35
> [ 90 sec, 5173738 itr]:           35
> [ 91 sec, 5173738 itr]:           35
> [ 92 sec, 5270979 itr]:           35
> [ optimality gap     ]:       37.14%
> [ 93 sec, 5270979 itr]:           35
> [ 94 sec, 5365633 itr]:           35
> [ 95 sec, 5415661 itr]:           35
> [ 96 sec, 5415661 itr]:           35
> [ 97 sec, 5462106 itr]:           35
> [ 98 sec, 5511917 itr]:           35
> [ 99 sec, 5608046 itr]:           35
> [100 sec, 5657366 itr]:           35
> [101 sec, 5703323 itr]:           35
> [102 sec, 5703323 itr]:           35
> [ optimality gap     ]:       37.14%
> [103 sec, 5751056 itr]:           35
> [104 sec, 5854565 itr]:           35
> [105 sec, 5854565 itr]:           35
> [106 sec, 5901166 itr]:           35
> [107 sec, 5953609 itr]:           35
> [108 sec, 6054066 itr]:           35
> [109 sec, 6104645 itr]:           35
> [110 sec, 6104645 itr]:           35
> [111 sec, 6152704 itr]:           35
> [112 sec, 6205952 itr]:           35
> [ optimality gap     ]:       37.14%
> [113 sec, 6256720 itr]:           35
> [114 sec, 6360244 itr]:           35
> [115 sec, 6360244 itr]:           35
> [116 sec, 6458927 itr]:           35
> [117 sec, 6458927 itr]:           35
> [118 sec, 6511783 itr]:           35
> [119 sec, 6607837 itr]:           35
> [120 sec, 6629077 itr]:           35
> [120 sec, 6629077 itr]:           35
> [ optimality gap     ]:       37.14%
> 
> 6629077 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =           35
>   gap    =       37.14%
>   bounds =           22
> ```

In [ ]:
```python
_model = Model(instance06)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 1037, decisions = 140, constraints = 190, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 159)
> [  1 sec,       0 itr]: No feasible solution found (infeas = 159)
> [  2 sec,  703840 itr]:           25
> [ optimality gap     ]:       44.00%
> [  3 sec, 1096245 itr]:           24
> [  4 sec, 1519515 itr]:           24
> [  5 sec, 1883800 itr]:           24
> [  6 sec, 1883800 itr]:           24
> [  7 sec, 2392020 itr]:           24
> [  8 sec, 2392020 itr]:           24
> [  9 sec, 2910522 itr]:           24
> [ 10 sec, 3152623 itr]:           24
> [ 11 sec, 3152623 itr]:           24
> [ 12 sec, 3374301 itr]:           24
> [ optimality gap     ]:       29.17%
> [ 13 sec, 3605794 itr]:           24
> [ 14 sec, 3819178 itr]:           24
> [ 15 sec, 4278635 itr]:           24
> [ 16 sec, 4525587 itr]:           24
> [ 17 sec, 4745872 itr]:           24
> [ 18 sec, 4745872 itr]:           24
> [ 19 sec, 5192853 itr]:           24
> [ 20 sec, 5192853 itr]:           24
> [ 21 sec, 5601935 itr]:           24
> [ 22 sec, 5853510 itr]:           24
> [ optimality gap     ]:       25.00%
> [ 23 sec, 5853510 itr]:           24
> [ 24 sec, 6345254 itr]:           24
> [ 25 sec, 6595220 itr]:           24
> [ 26 sec, 6822777 itr]:           24
> [ 27 sec, 7040504 itr]:           24
> [ 28 sec, 7040504 itr]:           24
> [ 29 sec, 7531008 itr]:           24
> [ 30 sec, 7762306 itr]:           24
> [ 31 sec, 8001893 itr]:           24
> [ 32 sec, 8001893 itr]:           24
> [ optimality gap     ]:       16.67%
> [ 33 sec, 8466553 itr]:           24
> [ 34 sec, 8466553 itr]:           24
> [ 35 sec, 8708402 itr]:           24
> [ 36 sec, 9172090 itr]:           24
> [ 37 sec, 9172090 itr]:           24
> [ 38 sec, 9638843 itr]:           24
> [ 39 sec, 9882667 itr]:           24
> [ 40 sec, 9882667 itr]:           24
> [ 41 sec, 10127738 itr]:           24
> [ 42 sec, 10675491 itr]:           24
> [ optimality gap      ]:       16.67%
> [ 43 sec, 10675491 itr]:           24
> [ 44 sec, 11256244 itr]:           24
> [ 45 sec, 11519130 itr]:           24
> [ 46 sec, 11519130 itr]:           24
> [ 47 sec, 11793914 itr]:           24
> [ 48 sec, 12063470 itr]:           24
> [ 49 sec, 12614934 itr]:           24
> [ 50 sec, 12890989 itr]:           24
> [ 50 sec, 12993031 itr]:           24
> [ optimality gap      ]:           0%
> 
> 12993031 iterations performed in 50 seconds
> 
> Optimal solution: 
>   obj    =           24
>   gap    =           0%
>   bounds =           24
> ```

In [ ]:
```python
_model = Model(instance07)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 25258, decisions = 2750, constraints = 4950, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 4072)
> [  1 sec,   32930 itr]:          200
> [  2 sec,   32930 itr]:          200
> [  3 sec,   80034 itr]:          199
> [  4 sec,  152246 itr]:          199
> [  5 sec,  186470 itr]:          199
> [  6 sec,  219510 itr]:          199
> [  7 sec,  219510 itr]:          199
> [  8 sec,  285181 itr]:          199
> [  9 sec,  316418 itr]:          199
> [ 10 sec,  316418 itr]:          199
> [ optimality gap     ]:       93.47%
> [ 11 sec,  348356 itr]:          199
> [ 12 sec,  416102 itr]:          199
> [ 13 sec,  450509 itr]:          199
> [ 14 sec,  482100 itr]:          199
> [ 15 sec,  482100 itr]:          199
> [ 16 sec,  521291 itr]:          199
> [ 17 sec,  606407 itr]:          198
> [ 18 sec,  647481 itr]:          197
> [ 19 sec,  647481 itr]:          197
> [ 20 sec,  705763 itr]:          197
> [ optimality gap     ]:       93.40%
> [ 21 sec,  742646 itr]:          197
> [ 22 sec,  779733 itr]:          197
> [ 23 sec,  779733 itr]:          197
> [ 24 sec,  855853 itr]:          197
> [ 25 sec,  892972 itr]:          197
> [ 26 sec,  892972 itr]:          197
> [ 27 sec,  934697 itr]:          197
> [ 28 sec, 1012314 itr]:          197
> [ 29 sec, 1049670 itr]:          197
> [ 30 sec, 1049670 itr]:          197
> [ optimality gap     ]:       93.40%
> [ 31 sec, 1134899 itr]:          197
> [ 32 sec, 1178073 itr]:          196
> [ 33 sec, 1178073 itr]:          196
> [ 34 sec, 1257181 itr]:          196
> [ 35 sec, 1300345 itr]:          196
> [ 36 sec, 1339231 itr]:          196
> [ 37 sec, 1375553 itr]:          196
> [ 38 sec, 1419759 itr]:          196
> [ 39 sec, 1458758 itr]:          196
> [ 40 sec, 1496763 itr]:          196
> [ optimality gap     ]:       93.37%
> [ 41 sec, 1537268 itr]:          196
> [ 42 sec, 1576702 itr]:          196
> [ 43 sec, 1617782 itr]:          196
> [ 44 sec, 1658607 itr]:          196
> [ 45 sec, 1702245 itr]:          196
> [ 46 sec, 1741097 itr]:          196
> [ 47 sec, 1781148 itr]:          196
> [ 48 sec, 1817336 itr]:          196
> [ 49 sec, 1856744 itr]:          196
> [ 50 sec, 1894373 itr]:          196
> [ optimality gap     ]:       93.37%
> [ 51 sec, 1934154 itr]:          196
> [ 52 sec, 1950699 itr]:          196
> [ 53 sec, 1985577 itr]:          196
> [ 54 sec, 2025449 itr]:          196
> [ 55 sec, 2025449 itr]:          196
> [ 56 sec, 2103245 itr]:          196
> [ 57 sec, 2141238 itr]:          196
> [ 58 sec, 2183833 itr]:          196
> [ 59 sec, 2221433 itr]:          196
> [ 60 sec, 2259110 itr]:          196
> [ optimality gap     ]:       93.37%
> [ 61 sec, 2296932 itr]:          196
> [ 62 sec, 2333819 itr]:          196
> [ 63 sec, 2372707 itr]:          196
> [ 64 sec, 2411866 itr]:          196
> [ 65 sec, 2449652 itr]:          196
> [ 66 sec, 2488281 itr]:          196
> [ 67 sec, 2525698 itr]:          196
> [ 68 sec, 2565414 itr]:          196
> [ 69 sec, 2604799 itr]:          196
> [ 70 sec, 2643804 itr]:          196
> [ optimality gap     ]:       93.37%
> [ 71 sec, 2681285 itr]:          196
> [ 72 sec, 2719378 itr]:          196
> [ 73 sec, 2756705 itr]:          196
> [ 74 sec, 2794700 itr]:          196
> [ 75 sec, 2831564 itr]:          196
> [ 76 sec, 2869245 itr]:          196
> [ 77 sec, 2909020 itr]:          196
> [ 78 sec, 2945402 itr]:          196
> [ 79 sec, 2984888 itr]:          196
> [ 80 sec, 3022572 itr]:          196
> [ optimality gap     ]:       93.37%
> [ 81 sec, 3058402 itr]:          196
> [ 82 sec, 3098278 itr]:          196
> [ 83 sec, 3138766 itr]:          196
> [ 84 sec, 3174014 itr]:          196
> [ 85 sec, 3189645 itr]:          196
> [ 86 sec, 3227929 itr]:          196
> [ 87 sec, 3265315 itr]:          196
> [ 88 sec, 3305103 itr]:          196
> [ 89 sec, 3342580 itr]:          196
> [ 90 sec, 3342580 itr]:          196
> [ optimality gap     ]:       93.37%
> [ 91 sec, 3422320 itr]:          196
> [ 92 sec, 3459492 itr]:          196
> [ 93 sec, 3497360 itr]:          196
> [ 94 sec, 3535007 itr]:          196
> [ 95 sec, 3572281 itr]:          196
> [ 96 sec, 3613226 itr]:          196
> [ 97 sec, 3650720 itr]:          196
> [ 98 sec, 3687217 itr]:          196
> [ 99 sec, 3727864 itr]:          196
> [100 sec, 3766086 itr]:          196
> [ optimality gap     ]:       93.37%
> [101 sec, 3806566 itr]:          196
> [102 sec, 3844372 itr]:          196
> [103 sec, 3882512 itr]:          196
> [104 sec, 3918867 itr]:          196
> [105 sec, 3959010 itr]:          196
> [106 sec, 3996352 itr]:          196
> [107 sec, 4037666 itr]:          196
> [108 sec, 4074987 itr]:          196
> [109 sec, 4114775 itr]:          196
> [110 sec, 4151540 itr]:          196
> [ optimality gap     ]:       93.37%
> [111 sec, 4188803 itr]:          196
> [112 sec, 4223880 itr]:          196
> [113 sec, 4259999 itr]:          196
> [114 sec, 4296742 itr]:          196
> [115 sec, 4334097 itr]:          196
> [116 sec, 4373111 itr]:          196
> [117 sec, 4410477 itr]:          196
> [118 sec, 4419512 itr]:          196
> [119 sec, 4460305 itr]:          194
> [120 sec, 4495323 itr]:          194
> [ optimality gap     ]:       93.30%
> [120 sec, 4495323 itr]:          194
> [ optimality gap     ]:       93.30%
> 
> 4495323 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =          194
>   gap    =       93.30%
>   bounds =           13
> ```

In [ ]:
```python
_model = Model(instance08)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 1351, decisions = 290, constraints = 190, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 100)
> [  1 sec,  210981 itr]:           50
> [  2 sec,  210981 itr]:           50
> [  3 sec,  520703 itr]:           50
> [  4 sec, 1182273 itr]:           50
> [  5 sec, 1182273 itr]:           50
> [  6 sec, 1818712 itr]:           50
> [  7 sec, 1818712 itr]:           50
> [  8 sec, 2143276 itr]:           50
> [  9 sec, 2730139 itr]:           50
> [ 10 sec, 3005664 itr]:           50
> [ optimality gap     ]:       30.00%
> [ 11 sec, 3332225 itr]:           49
> [ 12 sec, 3332225 itr]:           49
> [ 13 sec, 3904301 itr]:           49
> [ 14 sec, 3904301 itr]:           49
> [ 15 sec, 4236037 itr]:           49
> [ 16 sec, 4657701 itr]:           49
> [ 17 sec, 4976428 itr]:           49
> [ 18 sec, 5292397 itr]:           49
> [ 19 sec, 5591352 itr]:           49
> [ 20 sec, 5892613 itr]:           49
> [ optimality gap     ]:       28.57%
> [ 21 sec, 6187819 itr]:           49
> [ 22 sec, 6448285 itr]:           49
> [ 23 sec, 6720035 itr]:           49
> [ 24 sec, 6720035 itr]:           49
> [ 25 sec, 7251611 itr]:           49
> [ 26 sec, 7251611 itr]:           49
> [ 27 sec, 7521653 itr]:           49
> [ 28 sec, 8051093 itr]:           49
> [ 29 sec, 8318725 itr]:           49
> [ 30 sec, 8574737 itr]:           49
> [ optimality gap     ]:       28.57%
> [ 31 sec, 8847509 itr]:           49
> [ 32 sec, 9117016 itr]:           49
> [ 33 sec, 9378251 itr]:           49
> [ 34 sec, 9647707 itr]:           49
> [ 35 sec, 9647707 itr]:           49
> [ 36 sec, 9899167 itr]:           49
> [ 37 sec, 10198724 itr]:           49
> [ 38 sec, 10762133 itr]:           49
> [ 39 sec, 11078806 itr]:           49
> [ 40 sec, 11078806 itr]:           49
> [ optimality gap      ]:       28.57%
> [ 41 sec, 11411138 itr]:           49
> [ 42 sec, 12024242 itr]:           49
> [ 43 sec, 12350682 itr]:           49
> [ 44 sec, 12643965 itr]:           49
> [ 45 sec, 12937546 itr]:           49
> [ 46 sec, 13211690 itr]:           49
> [ 47 sec, 13476942 itr]:           49
> [ 48 sec, 13476942 itr]:           49
> [ 49 sec, 13808790 itr]:           49
> [ 50 sec, 14046784 itr]:           49
> [ optimality gap      ]:       28.57%
> [ 51 sec, 14281388 itr]:           49
> [ 52 sec, 14525973 itr]:           49
> [ 53 sec, 14525973 itr]:           49
> [ 54 sec, 14982875 itr]:           49
> [ 55 sec, 14982875 itr]:           49
> [ 56 sec, 15206644 itr]:           49
> [ 57 sec, 15704103 itr]:           49
> [ 58 sec, 15962868 itr]:           49
> [ 59 sec, 16207341 itr]:           49
> [ 60 sec, 16446596 itr]:           49
> [ optimality gap      ]:       26.53%
> [ 61 sec, 16446596 itr]:           49
> [ 62 sec, 16689459 itr]:           49
> [ 63 sec, 16925361 itr]:           49
> [ 64 sec, 17420615 itr]:           49
> [ 65 sec, 17670567 itr]:           49
> [ 66 sec, 17936660 itr]:           49
> [ 67 sec, 17936660 itr]:           49
> [ 68 sec, 18414308 itr]:           49
> [ 69 sec, 18666304 itr]:           49
> [ 70 sec, 18666304 itr]:           49
> [ optimality gap      ]:       26.53%
> [ 71 sec, 19112479 itr]:           49
> [ 72 sec, 19320885 itr]:           49
> [ 73 sec, 19320885 itr]:           49
> [ 74 sec, 19805337 itr]:           49
> [ 75 sec, 19805337 itr]:           49
> [ 76 sec, 20268400 itr]:           49
> [ 77 sec, 20519784 itr]:           49
> [ 78 sec, 20519784 itr]:           49
> [ 79 sec, 21030901 itr]:           49
> [ 80 sec, 21268587 itr]:           49
> [ optimality gap      ]:       26.53%
> [ 81 sec, 21346583 itr]:           47
> [ 82 sec, 21346583 itr]:           47
> [ 83 sec, 21800304 itr]:           47
> [ 84 sec, 22029349 itr]:           47
> [ 85 sec, 22029349 itr]:           47
> [ 86 sec, 22520320 itr]:           47
> [ 87 sec, 22775387 itr]:           47
> [ 88 sec, 22775387 itr]:           47
> [ 89 sec, 23001119 itr]:           47
> [ 90 sec, 23234854 itr]:           47
> [ optimality gap      ]:       23.40%
> [ 91 sec, 23739790 itr]:           47
> [ 92 sec, 23988513 itr]:           47
> [ 93 sec, 23988513 itr]:           47
> [ 94 sec, 24254926 itr]:           47
> [ 95 sec, 24503156 itr]:           47
> [ 96 sec, 24995182 itr]:           47
> [ 97 sec, 24995182 itr]:           47
> [ 98 sec, 25239403 itr]:           47
> [ 99 sec, 25726498 itr]:           47
> [100 sec, 25976749 itr]:           47
> [ optimality gap      ]:       23.40%
> [101 sec, 25976749 itr]:           47
> [102 sec, 26446032 itr]:           47
> [103 sec, 26446032 itr]:           47
> [104 sec, 26700913 itr]:           47
> [105 sec, 27206275 itr]:           47
> [106 sec, 27206275 itr]:           47
> [107 sec, 27420031 itr]:           47
> [108 sec, 27910175 itr]:           47
> [109 sec, 28134988 itr]:           47
> [110 sec, 28391635 itr]:           47
> [ optimality gap      ]:       23.40%
> [111 sec, 28652668 itr]:           47
> [112 sec, 28652668 itr]:           47
> [113 sec, 28891551 itr]:           47
> [114 sec, 29195468 itr]:           47
> [115 sec, 29439204 itr]:           47
> [116 sec, 29674569 itr]:           47
> [117 sec, 29674569 itr]:           47
> [118 sec, 30156892 itr]:           47
> [119 sec, 30413840 itr]:           47
> [120 sec, 30657339 itr]:           47
> [ optimality gap      ]:       21.28%
> [120 sec, 30657339 itr]:           47
> [ optimality gap      ]:       21.28%
> 
> 30657339 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =           47
>   gap    =       21.28%
>   bounds =           37
> ```

In [ ]:
```python
_model = Model(instance09)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 26773, decisions = 3500, constraints = 4950, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 3831)
> [  1 sec,   18187 itr]:          690
> [  2 sec,   41130 itr]:          654
> [  3 sec,   64432 itr]:          641
> [  4 sec,   87468 itr]:          634
> [  5 sec,  110749 itr]:          632
> [  6 sec,  132723 itr]:          628
> [  7 sec,  157577 itr]:          625
> [  8 sec,  179647 itr]:          620
> [  9 sec,  202437 itr]:          619
> [ 10 sec,  224470 itr]:          617
> [ optimality gap     ]:      100.00%
> [ 11 sec,  248308 itr]:          614
> [ 12 sec,  271146 itr]:          612
> [ 13 sec,  292777 itr]:          611
> [ 14 sec,  312507 itr]:          605
> [ 15 sec,  331194 itr]:          602
> [ 16 sec,  350925 itr]:          599
> [ 17 sec,  370937 itr]:          597
> [ 18 sec,  381705 itr]:          597
> [ 19 sec,  407767 itr]:          597
> [ 20 sec,  428269 itr]:          594
> [ optimality gap     ]:      100.00%
> [ 21 sec,  448965 itr]:          594
> [ 22 sec,  473835 itr]:          593
> [ 23 sec,  497694 itr]:          592
> [ 24 sec,  517961 itr]:          589
> [ 25 sec,  542881 itr]:          586
> [ 26 sec,  563378 itr]:          586
> [ 27 sec,  587273 itr]:          586
> [ 28 sec,  607899 itr]:          586
> [ 29 sec,  633824 itr]:          585
> [ 30 sec,  658637 itr]:          582
> [ optimality gap     ]:      100.00%
> [ 31 sec,  683106 itr]:          581
> [ 32 sec,  705813 itr]:          581
> [ 33 sec,  727709 itr]:          581
> [ 34 sec,  750625 itr]:          579
> [ 35 sec,  774981 itr]:          579
> [ 36 sec,  797638 itr]:          578
> [ 37 sec,  822357 itr]:          578
> [ 38 sec,  845907 itr]:          578
> [ 39 sec,  868396 itr]:          576
> [ 40 sec,  891342 itr]:          576
> [ optimality gap     ]:      100.00%
> [ 41 sec,  916611 itr]:          576
> [ 42 sec,  939987 itr]:          575
> [ 43 sec,  965396 itr]:          575
> [ 44 sec,  988592 itr]:          574
> [ 45 sec, 1012268 itr]:          574
> [ 46 sec, 1035275 itr]:          574
> [ 47 sec, 1059333 itr]:          574
> [ 48 sec, 1082762 itr]:          573
> [ 49 sec, 1104423 itr]:          573
> [ 50 sec, 1121247 itr]:          572
> [ optimality gap     ]:      100.00%
> [ 51 sec, 1132148 itr]:          570
> [ 52 sec, 1156059 itr]:          570
> [ 53 sec, 1178102 itr]:          570
> [ 54 sec, 1201065 itr]:          570
> [ 55 sec, 1228031 itr]:          570
> [ 56 sec, 1250948 itr]:          569
> [ 57 sec, 1275434 itr]:          569
> [ 58 sec, 1299831 itr]:          569
> [ 59 sec, 1325881 itr]:          569
> [ 60 sec, 1351670 itr]:          569
> [ optimality gap     ]:      100.00%
> [ 61 sec, 1380272 itr]:          569
> [ 62 sec, 1408537 itr]:          569
> [ 63 sec, 1435532 itr]:          569
> [ 64 sec, 1462976 itr]:          569
> [ 65 sec, 1487178 itr]:          565
> [ 66 sec, 1513332 itr]:          563
> [ 67 sec, 1538888 itr]:          563
> [ 68 sec, 1563254 itr]:          563
> [ 69 sec, 1587176 itr]:          563
> [ 70 sec, 1612118 itr]:          563
> [ optimality gap     ]:      100.00%
> [ 71 sec, 1632207 itr]:          562
> [ 72 sec, 1652135 itr]:          562
> [ 73 sec, 1672996 itr]:          562
> [ 74 sec, 1691867 itr]:          562
> [ 75 sec, 1713335 itr]:          561
> [ 76 sec, 1733890 itr]:          560
> [ 77 sec, 1754003 itr]:          560
> [ 78 sec, 1775200 itr]:          559
> [ 79 sec, 1797391 itr]:          559
> [ 80 sec, 1818118 itr]:          559
> [ optimality gap     ]:      100.00%
> [ 81 sec, 1838377 itr]:          559
> [ 82 sec, 1860068 itr]:          559
> [ 83 sec, 1876838 itr]:          559
> [ 84 sec, 1886089 itr]:          559
> [ 85 sec, 1906405 itr]:          559
> [ 86 sec, 1924569 itr]:          558
> [ 87 sec, 1943730 itr]:          558
> [ 88 sec, 1964424 itr]:          558
> [ 89 sec, 1984773 itr]:          558
> [ 90 sec, 2004153 itr]:          557
> [ optimality gap     ]:      100.00%
> [ 91 sec, 2026352 itr]:          557
> [ 92 sec, 2044311 itr]:          557
> [ 93 sec, 2066584 itr]:          557
> [ 94 sec, 2085947 itr]:          556
> [ 95 sec, 2113879 itr]:          555
> [ 96 sec, 2142011 itr]:          555
> [ 97 sec, 2167291 itr]:          554
> [ 98 sec, 2193908 itr]:          554
> [ 99 sec, 2219485 itr]:          554
> [100 sec, 2242370 itr]:          554
> [ optimality gap     ]:      100.00%
> [101 sec, 2258941 itr]:          554
> [102 sec, 2274238 itr]:          554
> [103 sec, 2290370 itr]:          554
> [104 sec, 2308998 itr]:          554
> [105 sec, 2330311 itr]:          554
> [106 sec, 2352967 itr]:          554
> [107 sec, 2376195 itr]:          552
> [108 sec, 2400184 itr]:          550
> [109 sec, 2423215 itr]:          549
> [110 sec, 2449268 itr]:          548
> [ optimality gap     ]:      100.00%
> [111 sec, 2473453 itr]:          547
> [112 sec, 2497912 itr]:          547
> [113 sec, 2520555 itr]:          546
> [114 sec, 2540388 itr]:          546
> [115 sec, 2560117 itr]:          546
> [116 sec, 2576212 itr]:          545
> [117 sec, 2585276 itr]:          545
> [118 sec, 2607059 itr]:          545
> [119 sec, 2630630 itr]:          544
> [120 sec, 2652753 itr]:          544
> [ optimality gap     ]:      100.00%
> [120 sec, 2652753 itr]:          544
> [ optimality gap     ]:      100.00%
> 
> 2652753 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =          544
>   gap    =      100.00%
>   bounds =            0
> ```

巨大なインスタンスで試してみよう

In [ ]:
```python
instance_large1 = scsp.example.load("nucleotide_n100k100.txt")
instance_large2 = scsp.example.load("protein_n100k100.txt")
```

In [ ]:
```python
_model = Model(instance_large1)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 100709, decisions = 10600, constraints = 19900, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 16267)
> [  1 sec,     474 itr]: No feasible solution found (infeas = 7857)
> [  2 sec,    6973 itr]:          421
> [ optimality gap     ]:      100.00%
> [  3 sec,   16319 itr]:          391
> [  4 sec,   26746 itr]:          390
> [  5 sec,   37501 itr]:          390
> [  6 sec,   51030 itr]:          388
> [  7 sec,   61780 itr]:          387
> [  8 sec,   65406 itr]:          387
> [  9 sec,   78331 itr]:          387
> [ 10 sec,   92537 itr]:          386
> [ 11 sec,  106384 itr]:          386
> [ 12 sec,  120899 itr]:          386
> [ optimality gap     ]:      100.00%
> [ 13 sec,  135400 itr]:          385
> [ 14 sec,  150595 itr]:          385
> [ 15 sec,  166284 itr]:          384
> [ 16 sec,  182047 itr]:          384
> [ 17 sec,  200216 itr]:          384
> [ 18 sec,  217677 itr]:          384
> [ 19 sec,  227767 itr]:          384
> [ 20 sec,  237397 itr]:          383
> [ 21 sec,  253099 itr]:          381
> [ 22 sec,  269216 itr]:          381
> [ optimality gap     ]:      100.00%
> [ 23 sec,  285801 itr]:          380
> [ 24 sec,  302382 itr]:          380
> [ 25 sec,  317948 itr]:          380
> [ 26 sec,  333869 itr]:          379
> [ 27 sec,  348337 itr]:          379
> [ 28 sec,  365353 itr]:          379
> [ 29 sec,  382636 itr]:          379
> [ 30 sec,  397975 itr]:          379
> [ 31 sec,  413643 itr]:          379
> [ 32 sec,  427537 itr]:          379
> [ optimality gap     ]:      100.00%
> [ 33 sec,  437015 itr]:          379
> [ 34 sec,  446106 itr]:          379
> [ 35 sec,  455712 itr]:          379
> [ 36 sec,  464941 itr]:          379
> [ 37 sec,  473645 itr]:          379
> [ 38 sec,  483928 itr]:          379
> [ 39 sec,  493019 itr]:          379
> [ 40 sec,  502336 itr]:          379
> [ 41 sec,  504782 itr]:          379
> [ 42 sec,  514532 itr]:          379
> [ optimality gap     ]:      100.00%
> [ 43 sec,  523618 itr]:          378
> [ 44 sec,  533580 itr]:          378
> [ 45 sec,  542162 itr]:          378
> [ 46 sec,  550206 itr]:          378
> [ 47 sec,  557497 itr]:          378
> [ 48 sec,  566077 itr]:          378
> [ 49 sec,  574113 itr]:          378
> [ 50 sec,  583005 itr]:          378
> [ 51 sec,  592198 itr]:          378
> [ 52 sec,  602160 itr]:          377
> [ optimality gap     ]:      100.00%
> [ 53 sec,  611386 itr]:          377
> [ 54 sec,  620652 itr]:          377
> [ 55 sec,  629308 itr]:          377
> [ 56 sec,  638110 itr]:          377
> [ 57 sec,  647257 itr]:          377
> [ 58 sec,  656156 itr]:          377
> [ 59 sec,  664427 itr]:          377
> [ 60 sec,  673238 itr]:          377
> [ 61 sec,  680526 itr]:          377
> [ 62 sec,  689131 itr]:          376
> [ optimality gap     ]:      100.00%
> [ 63 sec,  697546 itr]:          376
> [ 64 sec,  706378 itr]:          376
> [ 65 sec,  715014 itr]:          376
> [ 66 sec,  723510 itr]:          376
> [ 67 sec,  732671 itr]:          376
> [ 68 sec,  741102 itr]:          376
> [ 69 sec,  749440 itr]:          375
> [ 70 sec,  757653 itr]:          375
> [ 71 sec,  766395 itr]:          375
> [ 72 sec,  775177 itr]:          375
> [ optimality gap     ]:      100.00%
> [ 73 sec,  784272 itr]:          375
> [ 74 sec,  785896 itr]:          375
> [ 75 sec,  794509 itr]:          375
> [ 76 sec,  803245 itr]:          375
> [ 77 sec,  812215 itr]:          375
> [ 78 sec,  820177 itr]:          375
> [ 79 sec,  828170 itr]:          375
> [ 80 sec,  836346 itr]:          375
> [ 81 sec,  844730 itr]:          375
> [ 82 sec,  853479 itr]:          375
> [ optimality gap     ]:      100.00%
> [ 83 sec,  863099 itr]:          375
> [ 84 sec,  872083 itr]:          375
> [ 85 sec,  881125 itr]:          375
> [ 86 sec,  889637 itr]:          375
> [ 87 sec,  898631 itr]:          375
> [ 88 sec,  906314 itr]:          375
> [ 89 sec,  914846 itr]:          375
> [ 90 sec,  923501 itr]:          375
> [ 91 sec,  932483 itr]:          375
> [ 92 sec,  941135 itr]:          375
> [ optimality gap     ]:      100.00%
> [ 93 sec,  949976 itr]:          375
> [ 94 sec,  958429 itr]:          375
> [ 95 sec,  966332 itr]:          375
> [ 96 sec,  975185 itr]:          375
> [ 97 sec,  983792 itr]:          375
> [ 98 sec,  992150 itr]:          375
> [ 99 sec, 1001580 itr]:          375
> [100 sec, 1010539 itr]:          375
> [101 sec, 1018918 itr]:          375
> [102 sec, 1027579 itr]:          375
> [ optimality gap     ]:      100.00%
> [103 sec, 1036587 itr]:          375
> [104 sec, 1045526 itr]:          375
> [105 sec, 1054935 itr]:          375
> [106 sec, 1063173 itr]:          375
> [107 sec, 1064476 itr]:          375
> [108 sec, 1072483 itr]:          375
> [109 sec, 1081496 itr]:          375
> [110 sec, 1090323 itr]:          375
> [111 sec, 1099426 itr]:          375
> [112 sec, 1108772 itr]:          375
> [ optimality gap     ]:      100.00%
> [113 sec, 1116737 itr]:          375
> [114 sec, 1126006 itr]:          375
> [115 sec, 1134945 itr]:          375
> [116 sec, 1144572 itr]:          375
> [117 sec, 1153817 itr]:          375
> [118 sec, 1164549 itr]:          375
> [119 sec, 1174758 itr]:          375
> [120 sec, 1185344 itr]:          375
> [120 sec, 1185344 itr]:          375
> [ optimality gap     ]:      100.00%
> 
> 1185344 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =          375
>   gap    =      100.00%
>   bounds =            0
> ```

In [ ]:
```python
_model = Model(instance_large2)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Model:  expressions = 103523, decisions = 12000, constraints = 19900, objectives = 1
> Param:  time limit = 120 sec, no iteration limit
> 
> [objective direction ]:     minimize
> 
> [  0 sec,       0 itr]: No feasible solution found (infeas = 15229)
> [  1 sec,     106 itr]: No feasible solution found (infeas = 13673)
> [  2 sec,    3182 itr]: No feasible solution found (infeas = 2492)
> [  3 sec,    6541 itr]: No feasible solution found (infeas = 21)
> [  4 sec,   14231 itr]:         1785
> [ optimality gap     ]:      100.00%
> [  5 sec,   22673 itr]:         1720
> [  6 sec,   30810 itr]:         1692
> [  7 sec,   38716 itr]:         1677
> [  8 sec,   47379 itr]:         1668
> [  9 sec,   54867 itr]:         1658
> [ 10 sec,   62609 itr]:         1648
> [ 11 sec,   70248 itr]:         1643
> [ 12 sec,   77059 itr]:         1638
> [ 13 sec,   84271 itr]:         1630
> [ 14 sec,   91827 itr]:         1626
> [ optimality gap     ]:      100.00%
> [ 15 sec,   99119 itr]:         1624
> [ 16 sec,  106325 itr]:         1619
> [ 17 sec,  113769 itr]:         1614
> [ 18 sec,  121720 itr]:         1613
> [ 19 sec,  129295 itr]:         1609
> [ 20 sec,  136926 itr]:         1606
> [ 21 sec,  142696 itr]:         1605
> [ 22 sec,  148930 itr]:         1604
> [ 23 sec,  155118 itr]:         1601
> [ 24 sec,  161171 itr]:         1599
> [ optimality gap     ]:      100.00%
> [ 25 sec,  168319 itr]:         1597
> [ 26 sec,  175533 itr]:         1595
> [ 27 sec,  182214 itr]:         1592
> [ 28 sec,  189301 itr]:         1590
> [ 29 sec,  196698 itr]:         1589
> [ 30 sec,  199101 itr]:         1589
> [ 31 sec,  205544 itr]:         1587
> [ 32 sec,  212173 itr]:         1586
> [ 33 sec,  219574 itr]:         1582
> [ 34 sec,  226561 itr]:         1580
> [ optimality gap     ]:      100.00%
> [ 35 sec,  233307 itr]:         1579
> [ 36 sec,  240101 itr]:         1579
> [ 37 sec,  247318 itr]:         1576
> [ 38 sec,  254838 itr]:         1576
> [ 39 sec,  262663 itr]:         1575
> [ 40 sec,  270374 itr]:         1575
> [ 41 sec,  276620 itr]:         1574
> [ 42 sec,  282929 itr]:         1573
> [ 43 sec,  288505 itr]:         1572
> [ 44 sec,  294380 itr]:         1572
> [ optimality gap     ]:      100.00%
> [ 45 sec,  300368 itr]:         1572
> [ 46 sec,  307276 itr]:         1571
> [ 47 sec,  314666 itr]:         1569
> [ 48 sec,  321862 itr]:         1566
> [ 49 sec,  329486 itr]:         1566
> [ 50 sec,  336812 itr]:         1566
> [ 51 sec,  343416 itr]:         1564
> [ 52 sec,  350184 itr]:         1562
> [ 53 sec,  357617 itr]:         1561
> [ 54 sec,  364307 itr]:         1560
> [ optimality gap     ]:      100.00%
> [ 55 sec,  371231 itr]:         1559
> [ 56 sec,  377441 itr]:         1558
> [ 57 sec,  383237 itr]:         1557
> [ 58 sec,  389589 itr]:         1557
> [ 59 sec,  395934 itr]:         1554
> [ 60 sec,  402601 itr]:         1554
> [ 61 sec,  408344 itr]:         1553
> [ 62 sec,  413369 itr]:         1552
> [ 63 sec,  415285 itr]:         1550
> [ 64 sec,  419202 itr]:         1550
> [ optimality gap     ]:      100.00%
> [ 65 sec,  424397 itr]:         1549
> [ 66 sec,  429049 itr]:         1548
> [ 67 sec,  432658 itr]:         1546
> [ 68 sec,  436546 itr]:         1546
> [ 69 sec,  440844 itr]:         1544
> [ 70 sec,  444831 itr]:         1542
> [ 71 sec,  449894 itr]:         1541
> [ 72 sec,  455687 itr]:         1541
> [ 73 sec,  463806 itr]:         1540
> [ 74 sec,  470483 itr]:         1540
> [ optimality gap     ]:      100.00%
> [ 75 sec,  477163 itr]:         1540
> [ 76 sec,  484025 itr]:         1537
> [ 77 sec,  490791 itr]:         1537
> [ 78 sec,  497344 itr]:         1536
> [ 79 sec,  504363 itr]:         1536
> [ 80 sec,  511624 itr]:         1535
> [ 81 sec,  518670 itr]:         1533
> [ 82 sec,  526237 itr]:         1530
> [ 83 sec,  533291 itr]:         1529
> [ 84 sec,  539724 itr]:         1528
> [ optimality gap     ]:      100.00%
> [ 85 sec,  544705 itr]:         1527
> [ 86 sec,  550396 itr]:         1527
> [ 87 sec,  555597 itr]:         1527
> [ 88 sec,  561406 itr]:         1526
> [ 89 sec,  567118 itr]:         1526
> [ 90 sec,  572781 itr]:         1526
> [ 91 sec,  578793 itr]:         1526
> [ 92 sec,  585050 itr]:         1525
> [ 93 sec,  591084 itr]:         1522
> [ 94 sec,  597491 itr]:         1522
> [ optimality gap     ]:      100.00%
> [ 95 sec,  603328 itr]:         1521
> [ 96 sec,  605937 itr]:         1521
> [ 97 sec,  610443 itr]:         1521
> [ 98 sec,  616187 itr]:         1521
> [ 99 sec,  622513 itr]:         1521
> [100 sec,  629147 itr]:         1519
> [101 sec,  635153 itr]:         1519
> [102 sec,  641750 itr]:         1519
> [103 sec,  648992 itr]:         1519
> [104 sec,  655994 itr]:         1517
> [ optimality gap     ]:      100.00%
> [105 sec,  663162 itr]:         1516
> [106 sec,  670936 itr]:         1516
> [107 sec,  677582 itr]:         1515
> [108 sec,  684847 itr]:         1513
> [109 sec,  691633 itr]:         1513
> [110 sec,  697396 itr]:         1513
> [111 sec,  702729 itr]:         1510
> [112 sec,  708053 itr]:         1510
> [113 sec,  714239 itr]:         1510
> [114 sec,  719868 itr]:         1510
> [ optimality gap     ]:      100.00%
> [115 sec,  725341 itr]:         1510
> [116 sec,  731193 itr]:         1510
> [117 sec,  736702 itr]:         1510
> [118 sec,  742021 itr]:         1510
> [119 sec,  748181 itr]:         1509
> [120 sec,  754085 itr]:         1509
> [120 sec,  754085 itr]:         1509
> [ optimality gap     ]:      100.00%
> 
> 754085 iterations performed in 120 seconds
> 
> Feasible solution: 
>   obj    =         1509
>   gap    =      100.00%
>   bounds =            0
> ```

この定式化をするんだったら CP-SAT でよいでしょう.
