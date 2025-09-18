In [ ]:
```python
import opt_note.scsp as scsp
from ortools.sat.python import cp_model
import automaton_cpsat_test
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# ALPHABET から削り出すやつを整数線形計画でやる

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str]):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        valids = [cpmodel.new_bool_var("") for _ in range(max_len)]
        cvars = [
            [
                cpmodel.new_int_var(0, max(len(s) for s in instance) - 1, "")
                for c in s
            ]
            for s in instance
        ]

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                cpmodel.add(
                    len(chars) * cvars[sidx][cidx - 1] + chars.index(s[cidx - 1])
                    < len(chars) * cvars[sidx][cidx] + chars.index(s[cidx])
                )

        for sidx, s in enumerate(instance):
            for cidx, c in enumerate(s):
                cpmodel.add_element(
                    len(chars) * cvars[sidx][cidx] + chars.index(c),
                    valids,
                    1,
                )

        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.valids = valids
        self.status: cp_model.cp_model_pb2.CpSolverStatus | None = None

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        self.cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            self.cpsolver.parameters.max_time_in_seconds = time_limit
        self.status = self.cpsolver.solve(self.cpmodel)

        return self

    def to_solution(self) -> str | None:
        if self.status not in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            return None

        solution = ""
        for idx, valid in enumerate(self.valids):
            if self.cpsolver.boolean_value(valid):
                solution += self.chars[idx % len(self.chars)]

        return solution
```

In [ ]:
```python
def bench1(instance: list[str]) -> None:
    model = automaton_cpsat_test.Model(instance, False).solve()
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

    print(f"solution status: {model.cpsolver.status_name()}")
    print(f"bset bound: {model.cpsolver.best_objective_bound}")
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
> --- Solution (of length 64) ---
>  Sol: iougjteiqvafkozglnbkruxdhmpxcdinvybchostuoqvgoxzprvxinsnsbgpxflp
> str1: -----t------k--g-n-k-u--hmpx---n----h--t--q-g-xz--vxi-s---------
> str2: io--j--iq--f-o--lnb---x----xc---v-----s-u-q-----p-v-i-s-sb--xf--
> str3: --u-------------l-----------c-in-y-c-os--o-v-o-zp----------p--lp
> str4: i--g--e--va---zg--b-r--d-----d----bc--s----v-----rv--n-n--g--f--
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 52.0
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
> --- Solution (of length 111) ---
>  Sol: iruxlowjptbdeikvxydgnqbcfikoruvdhmprzefjlnrtvabxyzgnxbcertvdosdhtubcmopsvzbmqrvgnotxzdfpuvxinqsvwcdgpsblpxbfheo
> str1: ---------t----k----gn-----k--u--hmp------------x---n-----------ht-----------q--g---xz----vxi--s----------------
> str2: i----o-j-----i-------q--f--o------------ln----bx----x-c---v--s---u----------q----------p-v-i--s------sb--x-f---
> str3: --u-l------------------c-i---------------n------y-----c-----os-------o--v--------o--z--p------------p--lp------
> str4: i------------------g-----------------e------va---zg--b--r--d--d---bc---sv----rv-n-----------n------g-------f---
> str5: --------p--------y----------------p-----l-r------z--x------------u-c--p----mq-vg--t--df-u--i---v-cd--sb-------o
> str6: --------p-bde--v--d----c------vd--p---f----------z-----------s------m--s--b--r---o-----------q-v------b---b-h--
> str7: ------------e-------n-bc------------z-fj---tv--x-------er----------------zb--rv------------i-------gp--l-----e-
> str8: -r-x--w---------x----q----k-r--d---r----l-------------c--t--o-d-t---m-p------r---------p--x-----w-d------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 54.0
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
> --- Solution (of length 103) ---
>  Sol: iorxgjpwxbdeiqtvyafkopzglnrbdkruxlxchmzpvxinsuycfhjptmoqvdgptxdefrzuvxisvbcdmsbpvroqvnozinpgpxblwbdefhp
> str1: --------------t----k---g-n---k-u----hm-p-x-n-----h--t--q--g--x----z-vxis-------------------------------
> str2: io---j------iq----f-o---ln-b----x-xc----v---su---------q---p--------v-is-----sb--------------x------f--
> str3: -------------------------------u-l-c------in--yc------o----------------s----------o-v-oz--p-p--l------p
> str4: i---g------e---v-a----zg---b--r--------------------------d----d----------bc--s--vr--vn---n-g--------f--
> str5: ------p---------y----p--l-r-----------z--x---u-c---p-m-qv-g-t-d-f--u--i-v-cd-sb---o--------------------
> str6: ------p--bde---v------------d------c----v----------------d-p----f-z----s----msb--roqv---------b--b---h-
> str7: -----------e-------------n-b-------c--z---------f-j-t---v----x-e-rz------b-------r--v---i--gp--l---e---
> str8: --rx---wx----q-----k------r-d-r--l-c----------------t-o--d--t---------------m--p-r--------p--x--w-d----
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 75.0
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
> --- Solution (of length 159) ---
>   Sol: hiklorstxjkpqwabdfginqxefkouvydghlmnpqsxabjlnrwxzfhipxacovzdgiknpsuybcfjqrvzdkopsvimrtdhloqvxbceoszemtvbcgrvwahknoptxzbdfnpqrtuvxbgiuvcdjsbdhlmoprgwpqxzluwdefy
> str01: -------t--k-------g-n----k-u----h-m-p--x----n-----h----------------------------------t----q--------------g----------xz---------vx--i-----s---------------------
> str02: -i--o----j---------i-q--f-o------l-n-----b-----x-----x-c-v-------su-----q------p-vi--------------s---------------------------------------sb-----------x------f-
> str03: ---------------------------u-----l---------------------c-----i-n---y-c--------o-s--------o-v----o-z---------------p-------p------------------l--p--------------
> str04: -i----------------g----e----v-----------a-------z-----------g-------b----r--d---------d------bc--s----v---rv----n--------n--------g--------------------------f-
> str05: -----------p-----------------y------p------l-r--z----x------------u--c---------p---m------qv-------------g---------t---df-----u----i-vcd-sb----o---------------
> str06: -----------p---bd------e----v-d------------------------c-v-d----p-----f----z----s--m-------------s-----b--r------o---------q---v-b--------b-h------------------
> str07: -----------------------e-----------n-----b-------------c--z-----------fj-------------t-----vx--e----------r----------zb-----r--v---i--------------g-p---l---e--
> str08: -----r--x----w--------x--------------q------------------------k----------r--d-------r---l-----c------t-----------o-----d-----t----------------m-pr--p-x---wd---
> str09: --k-------k-q-a--f-i-----------g-----q----j---w---------o-----k--------------k--s------------------------------k------------r----b-----------l----g------------
> str10: ---l----x-------------x-------------p---ab---------i-----v----------b-----vz-ko-------------------z------------------z---------v-------d-----------------------
> str11: --k--r-------------i----f-------------s-a----------------v-----n-----c------d-------------q-----------------w-h------z----------------c------------------------
> str12: ------------q-a-------x----u--dg-----q-------------------v--------------q---------------------ce------------w---------b-f---------gi----j------o---w------w---y
> str13: -----rs-x---q-----------------------------j-n----f--p-a----d-i----u-------------s-i-------q--b-e--z-----------hk-o--------------------------h-m---g------------
> str14: -i-----------w------------------------s-----------h------v-----------------------------h------c-o---m------------------------------iuv-d---d--m----------------
> str15: h------tx-------------x--------------q----j-----z-----------------------q--------------------bc------t-b-----a-kn----------------------------------------------
> str16: --------x------------------u----------s----------f-----c--------------f----z---p---------------e---e----c--vwa--n--t----f---------------------m---g--q-z-u-----
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 23.0
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
> --- Solution (of length 147) ---
>   Sol: htikrxgpwxybdeknopquvadjklrsxbcfiquvzdfghmopqrxjlnvcfhquyzbcopstmoqvxerwagosxzbcdeirtvdfkpubciknsuvzcdgijkmopqrblpvwxaeinstwzfhkmnsbgoqzcvxbdhmfguy
> str01: -t-k--g--------n--------k---------u-----hm-p--x--n---h---------t--q------g--xz-------v------------------------------x--i-s-------------------------
> str02: --i-------------o------j--------iq----f---o-----ln--------b---------x-------x--c-----v----------su-----------q---pv----i-s--------sb------x----f---
> str03: -------------------u-----l----c-i----------------n------y--co-s--o-v------o--z-----------p------------------p---lp---------------------------------
> str04: --i---g------e------va--------------z--g------------------b-----------r---------d-----d----bc---s-v-----------r---v-----n--------n--g----------f---
> str05: -------p--y------p-------lr---------z---------x--------u---c-p--m-qv-----g----------t-df--u--i----v-cd-------------------s---------b-o-------------
> str06: -------p---bde------v-d-------c----v-d-----p--------f----z----s-m----------s--b----r-----------------------o-q----v----------------b-------b-h-----
> str07: -------------e-n-------------bc-----z-f--------j---------------t---vxer------zb----r-v-------i--------g-----p---l-----e----------------------------
> str08: ----rx--wx--------q-----k-r----------d-------r--l--c-----------t-o--------------d---t---------------------m-p-r--p--x------w----------------d------
> str09: ---k----------k---q--a---------fi------g----q--j-----------------------w--o-------------k-----k-s--------k----rbl-------------------g--------------
> str10: -------------------------l--x-----------------x--------------p----------a-----b---i--v-----b------vz-----k-o----------------z----------z-v--d------
> str11: ---kr---------------------------i-----f-----------------------s---------a------------v---------n----cd-------q-----w----------h--------zc----------
> str12: ------------------q--a------x-----u--d-g----q-----v---q----c---------e-w------b--------f--------------gij--o-------w-------w----------------------y
> str13: ----r----------------------sx----q-------------j-n--f--------p----------a-------d-i-------u-----s------i-----q-b------e-----z-hk-----o-------hm-g--
> str14: --i-----w------------------s------------h---------v--h-----co---m-----------------i-------u-------v--d--------------------------------------d-m----
> str15: ht---x---x--------q----j------------z-------q-------------bc---t--------------b--------------------------------------a---------k-n-----------------
> str16: -----x-------------u-------s---f-------------------cf----z---p-------e-----------e----------c-----v----------------w-a--n-t--f--m---g-qz---------u-
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 82.0
> ```

オートマトン制約を使うよりも線形制約で定式化した方が良さげ

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
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x99cb903f0d9752b8)
> #Variables: 709 (#bools: 625 in objective) (709 primary variables)
>   - 625 Booleans in [0,1]
>   - 84 in [0,24]
> #kElement: 84
> #kLinear2: 80
> 
> Starting presolve at 0.00s
>   1.34e-04s  0.00e+00d  [DetectDominanceRelations] 
>   9.98e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=25 #num_dual_strengthening=1 
>   1.55e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.99e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.17e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 6'608 nodes and 9'288 arcs.
> [Symmetry] Symmetry computation done. time: 0.00102778 dtime: 0.00173038
>   6.79e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=662 
>   3.11e-02s  9.15e-02d  [Probe] #probed=4'958 #new_binary_clauses=71'762 
>   6.91e-06s  0.00e+00d  [MaxClique] 
>   6.41e-04s  0.00e+00d  [DetectDominanceRelations] 
>   8.27e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   1.30e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.04e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.23e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.48e-05s  4.80e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=80 
>   1.55e-04s  0.00e+00d  [DetectDifferentVariables] #different=45 
>   7.23e-05s  3.39e-06d  [ProcessSetPPC] #relevant_constraints=84 
>   1.54e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   3.44e-04s  4.43e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   8.36e-05s  4.24e-05d  [FindBigVerticalLinearOverlap] 
>   9.92e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.38e-05s  0.00e+00d  [MergeClauses] 
>   6.33e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.71e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.27e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.70e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.83e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   1.05e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 7'060 nodes and 10'547 arcs.
> [Symmetry] Symmetry computation done. time: 0.000883115 dtime: 0.00160177
> [SAT presolve] num removable Booleans: 0 / 1438
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:969 literals:1938 vars:1276 one_side_vars:1276 simple_definition:0 singleton_clauses:0
> [SAT presolve] [3.4466e-05s] clauses:969 literals:1938 vars:1276 one_side_vars:1276 simple_definition:0 singleton_clauses:0
> [SAT presolve] [9.0011e-05s] clauses:969 literals:1938 vars:1276 one_side_vars:1276 simple_definition:0 singleton_clauses:0
>   9.54e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.20e-02s  9.34e-02d  [Probe] #probed=4'958 #new_binary_clauses=71'646 
>   3.57e-03s  3.05e-02d  [MaxClique] Merged 969(1'938 literals) into 663(1'632 literals) at_most_ones. 
>   6.14e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.70e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.26e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.04e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.45e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.56e-05s  4.80e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=80 
>   1.49e-04s  0.00e+00d  [DetectDifferentVariables] #different=45 
>   1.88e-04s  8.13e-06d  [ProcessSetPPC] #relevant_constraints=747 
>   2.46e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   3.24e-04s  3.23e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   8.50e-05s  4.02e-05d  [FindBigVerticalLinearOverlap] 
>   1.24e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.12e-05s  0.00e+00d  [MergeClauses] 
>   6.05e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.59e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.02e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.56e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.69e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   9.28e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 6'646 nodes and 9'569 arcs.
> [Symmetry] Symmetry computation done. time: 0.00063794 dtime: 0.00138162
> [SAT presolve] num removable Booleans: 0 / 1365
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:478 literals:956 vars:750 one_side_vars:750 simple_definition:0 singleton_clauses:0
> [SAT presolve] [2.2022e-05s] clauses:478 literals:956 vars:750 one_side_vars:750 simple_definition:0 singleton_clauses:0
> [SAT presolve] [8.1184e-05s] clauses:478 literals:956 vars:750 one_side_vars:750 simple_definition:0 singleton_clauses:0
>   1.24e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.22e-02s  9.34e-02d  [Probe] #probed=4'958 #new_binary_clauses=71'694 
>   3.66e-03s  3.12e-02d  [MaxClique] Merged 663(1'559 literals) into 630(1'559 literals) at_most_ones. 
>   6.09e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.64e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.31e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.05e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.65e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.80e-05s  4.80e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=80 
>   1.49e-04s  0.00e+00d  [DetectDifferentVariables] #different=45 
>   1.83e-04s  8.11e-06d  [ProcessSetPPC] #relevant_constraints=714 
>   2.70e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   3.29e-04s  3.27e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   7.96e-05s  4.02e-05d  [FindBigVerticalLinearOverlap] 
>   2.02e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.16e-05s  0.00e+00d  [MergeClauses] 
>   6.10e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.59e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.55e-04s  0.00e+00d  [ExpandObjective] #entries=14'556 #tight_variables=1'131 #tight_constraints=84 
> 
> Presolve summary:
>   - 162 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 170 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 2'398 times.
>   - rule 'affine: new relation' was applied 162 times.
>   - rule 'at_most_one: removed literals' was applied 73 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'bool_and: x => x' was applied 162 times.
>   - rule 'deductions: 3717 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 162 times.
>   - rule 'dual: fix variable' was applied 89 times.
>   - rule 'element: expanded' was applied 84 times.
>   - rule 'exactly_one: simplified objective' was applied 15 times.
>   - rule 'exactly_one: singleton' was applied 73 times.
>   - rule 'linear: divide by GCD' was applied 80 times.
>   - rule 'linear: reduced variable domains' was applied 523 times.
>   - rule 'new_bool: integer encoding' was applied 1'131 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 1 time.
>   - rule 'objective: variable not used elsewhere' was applied 156 times.
>   - rule 'presolve: 156 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 1'131 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x8b2c5cb899cd9f7)
> #Variables: 1'449 (#bools: 336 in objective) (1'365 primary variables)
>   - 1'365 Booleans in [0,1]
>   - 2 in [0,10]
>   - 1 in [0,11]
>   - 1 in [0,14]
>   - 1 in [0,16]
>   - 1 in [1,11]
>   - 1 in [1,12]
>   - 1 in [1,15]
>   - 1 in [1,17]
>   - 2 in [2,12]
>   - 2 in [2,13]
>   - 2 in [2,16]
>   - 4 in [2,18]
>   - 2 in [3,13]
>   - 2 in [3,14]
>   - 2 in [3,17]
>   - 3 in [3,19]
>   - 2 in [4,14]
>   - 1 in [4,15]
>   - 4 in [4,18]
>   - 2 in [4,20]
>   - 2 in [5,15]
>   - 2 in [5,16]
>   - 1 in [5,19]
>   - 2 in [5,21]
>   - 1 in [6,16]
>   - 1 in [6,17]
>   - 2 in [6,20]
>   - 1 in [6,22]
>   - 2 in [7,17]
>   - 1 in [7,18]
>   - 1 in [7,21]
>   - 1 in [7,23]
>   - 2 in [8,18]
>   - 4 in [8,19]
>   - 3 in [8,22]
>   - 2 in [8,24]
>   - 1 in [9,19]
>   - 2 in [9,20]
>   - 2 in [9,23]
>   - 2 in [10,20]
>   - 1 in [10,21]
>   - 2 in [10,24]
>   - 2 in [11,21]
>   - 1 in [11,22]
>   - 1 in [12,22]
>   - 1 in [12,23]
>   - 2 in [13,23]
>   - 1 in [13,24]
>   - 1 in [14,24]
> #kAtMostOne: 204 (#literals: 707)
> #kBoolAnd: 220 (#enforced: 220) (#literals: 646)
> #kExactlyOne: 84 (#literals: 1'131)
> #kLinear1: 2'262 (#enforced: 2'262)
> #kLinear2: 80
> [Symmetry] Graph for symmetry has 6'170 nodes and 9'465 arcs.
> [Symmetry] Symmetry computation done. time: 0.000624455 dtime: 0.0013687
> 
> Preloading model.
> #Bound   0.17s best:inf   next:[15,351]   initial_domain
> #Model   0.17s var:1449/1449 constraints:2850/2850
> 
> Starting search at 0.17s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.18s best:77    next:[15,76]    fj_restart(batch:1 lin{mvs:133 evals:1'083} #w_updates:0 #perturb:0)
> #2       0.19s best:75    next:[15,74]    graph_var_lns (d=5.00e-01 s=14 t=0.10 p=0.00 stall=0 h=base)
> #3       0.20s best:74    next:[15,73]    ls_lin_restart_perturb(batch:1 lin{mvs:91 evals:449} #w_updates:67 #perturb:0)
> #4       0.23s best:72    next:[15,71]    graph_cst_lns (d=7.07e-01 s=24 t=0.10 p=1.00 stall=0 h=base)
> #5       0.24s best:70    next:[15,69]    graph_arc_lns (d=7.07e-01 s=23 t=0.10 p=1.00 stall=0 h=base)
> #Bound   0.26s best:70    next:[16,69]    am1_presolve (num_literals=336 num_am1=1 increase=1 work_done=5971)
> #Bound   0.26s best:70    next:[17,69]    bool_core (num_cores=1 [size:11 mw:1 amo:1 lit:3 d:4] a=325 d=4 fixed=0/2253 clauses=1'056)
> #Bound   0.31s best:70    next:[52,69]    max_lp
> #6       0.33s best:69    next:[52,68]    quick_restart_no_lp
> #7       0.40s best:67    next:[52,66]    quick_restart_no_lp
> #8       0.43s best:66    next:[52,65]    quick_restart_no_lp
> #Bound   0.60s best:66    next:[53,65]    bool_core (num_cores=37 [size:8 mw:1 amo:1 lit:3 d:7] a=31 d=9 fixed=0/2908 clauses=3'238)
> #Bound   0.62s best:66    next:[54,65]    bool_core (num_cores=38 [size:11 mw:1 amo:3 lit:9 d:9] a=21 d=9 fixed=0/2940 clauses=3'556)
> #9       0.67s best:65    next:[54,64]    graph_cst_lns (d=8.76e-01 s=46 t=0.10 p=1.00 stall=0 h=base)
> #Bound   0.69s best:65    next:[55,64]    bool_core (num_cores=39 [size:5 mw:1 amo:1 lit:2 d:10] a=17 d=10 fixed=0/2977 clauses=4'751)
> #Bound   0.80s best:65    next:[56,64]    bool_core (num_cores=40 [size:2 mw:1 d:11] a=16 d=11 fixed=0/3022 clauses=6'467)
> #10      1.00s best:64    next:[56,63]    graph_cst_lns (d=8.21e-01 s=55 t=0.10 p=0.75 stall=0 h=base)
> #11      1.55s best:63    next:[56,62]    rnd_var_lns (d=8.77e-01 s=82 t=0.10 p=0.71 stall=7 h=base)
> #Bound   1.76s best:63    next:[57,62]    bool_core (num_cores=41 [size:1 mw:1] a=16 d=11 fixed=0/3094 clauses=6'494)
> #Bound   2.04s best:63    next:[58,62]    bool_core (num_cores=42 [size:1 mw:1] a=16 d=11 fixed=1/3157 clauses=10'110)
> #Bound   2.86s best:63    next:[59,62]    bool_core (num_cores=43 [size:4 mw:1 d:12] a=13 d=12 fixed=2/3215 clauses=14'075)
> #Bound   4.14s best:63    next:[60,62]    bool_core (num_cores=44 [size:7 mw:1 amo:1 lit:2 d:13] a=7 d=13 fixed=2/3275 clauses=19'238)
> #Bound   6.13s best:63    next:[61,62]    bool_core (num_cores=45 [size:1 mw:1] a=7 d=13 fixed=2/3334 clauses=25'958)
> #Bound  12.59s best:63    next:[62,62]    bool_core (num_cores=46 [size:1 mw:1] a=1 d=13 fixed=3/3382 clauses=31'134)
> #Model  12.63s var:1415/1449 constraints:2781/2850
> #12     15.21s best:62    next:[]         core
> #Done   15.21s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [  20.85s,   20.85s]   20.85s   0.00ns   20.85s
>            'default_lp':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [   6.03s,    6.03s]    6.03s   0.00ns    6.03s
>      'feasibility_pump':        64 [  6.43ms,  13.25ms]  11.80ms 813.43us 755.32ms        63 [  2.97ms,   4.37ms]   3.04ms 170.64us 191.46ms
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         1 [  1.87ms,   1.87ms]   1.87ms   0.00ns   1.87ms         1 [260.70us, 260.70us] 260.70us   0.00ns 260.70us
>             'fs_random':         1 [  4.90ms,   4.90ms]   4.90ms   0.00ns   4.90ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [  8.00ms,   8.00ms]   8.00ms   0.00ns   8.00ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        55 [ 10.72ms, 284.75ms] 120.61ms  85.01ms    6.63s        55 [ 26.09us, 100.11ms]  60.84ms  43.85ms    3.35s
>         'graph_cst_lns':        52 [  9.37ms, 408.44ms] 130.64ms 105.95ms    6.79s        52 [ 31.58us, 100.09ms]  55.36ms  46.60ms    2.88s
>         'graph_dec_lns':        42 [  3.70ms, 475.13ms] 153.17ms 121.92ms    6.43s        42 [ 10.00ns, 100.06ms]  51.28ms  45.96ms    2.15s
>         'graph_var_lns':        55 [  9.41ms, 346.59ms] 119.91ms 103.00ms    6.59s        55 [  2.94us, 100.06ms]  56.35ms  46.91ms    3.10s
>                    'ls':        58 [ 11.81ms, 129.40ms] 110.04ms  19.52ms    6.38s        58 [  8.76ms, 100.02ms]  97.06ms  15.65ms    5.63s
>                'ls_lin':        54 [  1.08ms, 129.49ms] 117.38ms  20.30ms    6.34s        54 [406.34us, 100.03ms]  96.80ms  16.54ms    5.23s
>                'max_lp':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [  13.23s,   13.23s]   13.23s   0.00ns   13.23s
>                 'no_lp':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [  12.55s,   12.55s]   12.55s   0.00ns   12.55s
>          'pseudo_costs':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [  11.54s,   11.54s]   11.54s   0.00ns   11.54s
>         'quick_restart':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [   4.43s,    4.43s]    4.43s   0.00ns    4.43s
>   'quick_restart_no_lp':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [  11.80s,   11.80s]   11.80s   0.00ns   11.80s
>         'reduced_costs':         1 [  15.04s,   15.04s]   15.04s   0.00ns   15.04s         1 [  12.02s,   12.02s]   12.02s   0.00ns   12.02s
>             'rins/rens':        38 [  3.41ms, 508.00ms] 168.88ms 175.39ms    6.42s        38 [ 10.00ns, 100.07ms]  52.67ms  49.91ms    2.00s
>           'rnd_cst_lns':        48 [ 14.90ms, 368.99ms] 152.64ms 100.42ms    7.33s        48 [ 10.00ns, 100.12ms]  58.08ms  45.00ms    2.79s
>           'rnd_var_lns':        51 [  3.66ms, 371.90ms] 125.40ms 101.46ms    6.40s        49 [ 10.00ns, 100.11ms]  56.69ms  43.57ms    2.78s
> 
> Search stats              Bools  Conflicts   Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  3'425    104'906    423'066    28'031  75'579'645      6'192'502
>            'default_lp':  2'244    102'395    253'874    24'248  18'290'083     13'959'194
>             'fs_random':  1'831          0          0         0           0              0
>       'fs_random_no_lp':  1'377          0          0         0           0              0
>                'max_lp':  2'244        494     57'168    20'943   4'041'225      2'888'134
>                 'no_lp':  2'244    268'194    511'445    30'917  28'582'722     28'130'493
>          'pseudo_costs':  2'244        898    104'281    30'944   6'343'225      4'538'310
>         'quick_restart':  2'244     30'908    427'859    27'405  13'482'481      7'099'701
>   'quick_restart_no_lp':  2'244     92'305  1'258'763    46'269  34'269'305     20'299'269
>         'reduced_costs':  2'244      1'203    107'855    30'747   6'261'835      4'519'177
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        97'030   2'542'275   2'953'211     1'850'240       279    17'940     126'892         0      5'645      102'701      643
>            'default_lp':       101'028   1'177'683   6'359'714     5'482'536        78    12'406      35'048         0          4           44        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':           483      23'993      95'124             0         1    10'410      29'082         0         12          144        0
>                 'no_lp':       263'732   3'597'017  17'111'915    15'461'586       213    16'648      46'408         0         14          171        0
>          'pseudo_costs':           878      49'877     128'747             0         0    16'825      61'688         0         33        2'601      178
>         'quick_restart':        29'054     256'050   1'726'967     1'074'232        84    12'984      48'626         0         66        1'903      687
>   'quick_restart_no_lp':        83'999     768'925   5'203'901     4'249'868       445    23'661     177'851         0        458       15'050    5'711
>         'reduced_costs':         1'196      87'398     188'648             0         4    16'664      62'096         0         28        1'963       43
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          4      56'116        411  264'887        0        0
>          'max_lp':          1     160'286      4'371    1'135      747        0
>    'pseudo_costs':          1     177'835      6'710    2'346    1'016        0
>   'quick_restart':          4     173'146        424  278'991        0        0
>   'reduced_costs':          1     216'576      7'650    2'710    1'347        0
> 
> Lp dimension           Final dimension of first component
>      'default_lp':        28 rows, 35 columns, 57 entries
>          'max_lp':   936 rows, 1449 columns, 7252 entries
>    'pseudo_costs':   987 rows, 1449 columns, 8680 entries
>   'quick_restart':        17 rows, 35 columns, 40 entries
>   'reduced_costs':  1370 rows, 1449 columns, 9612 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0  40'733         0       3           0
>          'max_lp':          0            0   1'882         0  19'610           0
>    'pseudo_costs':          0            0   3'329         0  13'666           0
>   'quick_restart':          0            0  58'415         0       3           0
>   'reduced_costs':          0            9   4'028         0   6'101           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':          629        0       32       8         14      0             5     411/6'342
>          'max_lp':        5'501      112        0       0          0    165           556  4'371/12'308
>    'pseudo_costs':        7'840      244        0       0          0     19         1'078  6'710/12'660
>   'quick_restart':          650        0       62       0         20      0             5    424/15'328
>   'reduced_costs':        8'780      148    1'018       0        963     30         1'551  7'650/13'504
> 
> Lp Cut            default_lp  max_lp  quick_restart  reduced_costs  pseudo_costs
>           CG_FF:           -       -              -             81            35
>            CG_K:           -       -              -             58            15
>           CG_KL:           -       -              -              8             3
>            CG_R:           -       -              -             58            21
>           CG_RB:           -       -              -             88            36
>          CG_RBP:           -       -              -             45            24
>          Clique:           -      58              -             44            49
>              IB:         409      25            422          1'932         1'813
>        MIR_1_FF:           -     274              -            510           416
>         MIR_1_K:           1     240              -            483           394
>        MIR_1_KL:           -      67              -            245           154
>         MIR_1_R:           -       6              -              6             5
>        MIR_1_RB:           -     257              -            463           344
>       MIR_1_RBP:           -     118              -            182           169
>        MIR_2_FF:           1     337              1            467           314
>         MIR_2_K:           -     294              1            428           369
>        MIR_2_KL:           -      78              -            125           140
>         MIR_2_R:           -       5              -             19             9
>        MIR_2_RB:           -     408              -            422           346
>       MIR_2_RBP:           -     144              -            160           170
>        MIR_3_FF:           -     159              -            101            97
>         MIR_3_K:           -     104              -             79            97
>        MIR_3_KL:           -      22              -             25            21
>         MIR_3_R:           -      34              -             35            27
>        MIR_3_RB:           -     117              -             74            75
>       MIR_3_RBP:           -      50              -             28            35
>        MIR_4_FF:           -     120              -             53            49
>         MIR_4_K:           -      62              -             31            36
>        MIR_4_KL:           -      12              -              7             8
>         MIR_4_R:           -     103              -             31            33
>        MIR_4_RB:           -      59              -             26            53
>       MIR_4_RBP:           -      14              -             10            21
>        MIR_5_FF:           -      82              -             42            38
>         MIR_5_K:           -      39              -             23            33
>        MIR_5_KL:           -       8              -              4             3
>         MIR_5_R:           -      95              -             34            28
>        MIR_5_RB:           -      36              -             20            31
>       MIR_5_RBP:           -       6              -              5            13
>        MIR_6_FF:           -      68              -             29            28
>         MIR_6_K:           -      34              -             15            21
>        MIR_6_KL:           -       6              -              6             5
>         MIR_6_R:           -      62              -             15            20
>        MIR_6_RB:           -      17              -              9            19
>       MIR_6_RBP:           -       5              -              4             5
>    ZERO_HALF_FF:           -      43              -            181           108
>     ZERO_HALF_K:           -      33              -            128            82
>    ZERO_HALF_KL:           -       8              -             12            12
>     ZERO_HALF_R:           -     557              -            489           646
>    ZERO_HALF_RB:           -      78              -            183           135
>   ZERO_HALF_RBP:           -      27              -            127           105
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          3/55     49%    6.03e-01       0.10
>   'graph_cst_lns':          5/52     50%    7.16e-01       0.10
>   'graph_dec_lns':          0/42     55%    9.14e-01       0.10
>   'graph_var_lns':          4/55     49%    5.29e-01       0.10
>       'rins/rens':          1/38     47%    7.48e-01       0.10
>     'rnd_cst_lns':          1/48     50%    8.05e-01       0.10
>     'rnd_var_lns':          1/49     55%    9.16e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1       133         0              0          0              0          1'083
>                          'ls_lin_restart':        8                  7   288'403         0              0          0         11'302      1'479'068
>                 'ls_lin_restart_compound':        8                  5         0   236'384         27'883    104'238            975      2'300'545
>         'ls_lin_restart_compound_perturb':        3                  3         0    94'238         13'183     40'523            422        959'634
>                    'ls_lin_restart_decay':        9                  6   543'304         0              0          0          8'028      1'990'107
>           'ls_lin_restart_decay_compound':        9                  7         0   272'519         80'945     95'762            702      3'239'405
>   'ls_lin_restart_decay_compound_perturb':        5                  4         0   148'975         43'926     52'510            374      1'792'413
>            'ls_lin_restart_decay_perturb':        1                  1    62'586         0              0          0            941        224'372
>                  'ls_lin_restart_perturb':       11                  7   344'456         0              0          0         15'285      1'916'242
>                              'ls_restart':        9                  4   254'983         0              0          0         73'387        920'674
>                     'ls_restart_compound':        4                  4         0   112'943          6'528     53'202            666        932'702
>             'ls_restart_compound_perturb':        8                  8         0   227'344         12'639    107'339          1'388      1'877'282
>                        'ls_restart_decay':       10                  6   338'770         0              0          0          7'481        968'936
>               'ls_restart_decay_compound':       10                  9         0   235'346         52'542     91'383            624      2'131'171
>       'ls_restart_decay_compound_perturb':        2                  2         0    52'103         12'768     19'666            134        469'952
>                'ls_restart_decay_perturb':        9                  6   331'996         0              0          0          7'126        945'817
>                      'ls_restart_perturb':        6                  3   171'732         0              0          0         47'822        625'356
> 
> Solutions (12)               Num     Rank
>                     'core':    1  [12,12]
>               'fj_restart':    1    [1,1]
>            'graph_arc_lns':    1    [5,5]
>            'graph_cst_lns':    3   [4,10]
>            'graph_var_lns':    1    [2,2]
>   'ls_lin_restart_perturb':    1    [3,3]
>      'quick_restart_no_lp':    3    [6,8]
>              'rnd_var_lns':    1  [11,11]
> 
> Objective bounds     Num
>     'am1_presolve':    1
>        'bool_core':   11
>   'initial_domain':    1
>           'max_lp':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    400      787      250
>    'fj solution hints':      0        0        0
>         'lp solutions':     87       19       83
>                 'pump':  1'323       19
> 
> Improving bounds shared    Num  Sym
>                   'core':   50    0
> 
> Clauses shared            Num
>                  'core':    1
>         'quick_restart':    6
>   'quick_restart_no_lp':    4
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 62
> best_bound: 62
> integers: 420
> booleans: 1831
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 15.2256
> usertime: 15.2256
> deterministic_time: 122.87
> gap_integral: 28.1436
> solution_fingerprint: 0xf0c33620c0470fcb
> ```

In [ ]:
```python
_model = Model(instance02)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x62caf4921ff464ba)
> #Variables: 825 (#bools: 650 in objective) (825 primary variables)
>   - 650 Booleans in [0,1]
>   - 175 in [0,24]
> #kElement: 175
> #kLinear2: 167
> 
> Starting presolve at 0.01s
>   1.84e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.13e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=25 #num_dual_strengthening=1 
>   1.83e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   4.24e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   3.85e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 13'564 nodes and 20'069 arcs.
> [Symmetry] Symmetry computation done. time: 0.00230293 dtime: 0.00411182
>   1.79e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=1'877 
>   7.24e-02s  2.22e-01d  [Probe] #probed=9'872 #new_binary_clauses=169'657 
>   1.56e-05s  0.00e+00d  [MaxClique] 
>   1.31e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.68e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   2.78e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.74e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.53e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.65e-05s  1.00e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=167 
>   2.64e-04s  0.00e+00d  [DetectDifferentVariables] #different=87 
>   1.48e-04s  7.34e-06d  [ProcessSetPPC] #relevant_constraints=175 
>   3.18e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   7.35e-04s  9.84e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.77e-04s  9.23e-05d  [FindBigVerticalLinearOverlap] 
>   2.27e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.81e-05s  0.00e+00d  [MergeClauses] 
>   1.30e-03s  0.00e+00d  [DetectDominanceRelations] 
>   8.03e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.29e-03s  0.00e+00d  [DetectDominanceRelations] 
>   8.02e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.23e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   3.81e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 14'375 nodes and 23'108 arcs.
> [Symmetry] Symmetry computation done. time: 0.00172447 dtime: 0.00389579
> [SAT presolve] num removable Booleans: 0 / 2906
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:2337 literals:4674 vars:2797 one_side_vars:2797 simple_definition:0 singleton_clauses:0
> [SAT presolve] [8.2015e-05s] clauses:2337 literals:4674 vars:2797 one_side_vars:2797 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000175563s] clauses:2337 literals:4674 vars:2797 one_side_vars:2797 simple_definition:0 singleton_clauses:0
>   2.51e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.08e-02s  2.21e-01d  [Probe] #probed=9'872 #new_binary_clauses=168'952 
>   1.01e-02s  8.68e-02d  [MaxClique] Merged 2'337(4'674 literals) into 1'690(4'027 literals) at_most_ones. 
>   1.33e-03s  0.00e+00d  [DetectDominanceRelations] 
>   8.07e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.81e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.10e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.76e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.09e-05s  1.00e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=167 
>   2.67e-04s  0.00e+00d  [DetectDifferentVariables] #different=87 
>   4.45e-04s  1.95e-05d  [ProcessSetPPC] #relevant_constraints=1'865 
>   5.47e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.78e-04s  6.73e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.66e-04s  8.90e-05d  [FindBigVerticalLinearOverlap] 
>   2.68e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.68e-05s  0.00e+00d  [MergeClauses] 
>   1.30e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.71e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.32e-03s  0.00e+00d  [DetectDominanceRelations] 
>   8.33e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.79e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   2.04e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 13'696 nodes and 21'264 arcs.
> [Symmetry] Symmetry computation done. time: 0.00164255 dtime: 0.00329719
> [SAT presolve] num removable Booleans: 0 / 2887
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1191 literals:2382 vars:1638 one_side_vars:1638 simple_definition:0 singleton_clauses:0
> [SAT presolve] [6.3069e-05s] clauses:1191 literals:2382 vars:1638 one_side_vars:1638 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000187776s] clauses:1191 literals:2382 vars:1638 one_side_vars:1638 simple_definition:0 singleton_clauses:0
>   2.30e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.18e-02s  2.22e-01d  [Probe] #probed=9'872 #new_binary_clauses=169'328 
>   9.72e-03s  8.25e-02d  [MaxClique] Merged 1'690(4'008 literals) into 1'683(4'008 literals) at_most_ones. 
>   1.31e-03s  0.00e+00d  [DetectDominanceRelations] 
>   8.13e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.89e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.21e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.84e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.65e-05s  1.00e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=167 
>   2.81e-04s  0.00e+00d  [DetectDifferentVariables] #different=87 
>   4.37e-04s  1.95e-05d  [ProcessSetPPC] #relevant_constraints=1'858 
>   6.14e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.97e-04s  6.87e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.68e-04s  8.90e-05d  [FindBigVerticalLinearOverlap] 
>   3.19e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.03e-05s  0.00e+00d  [MergeClauses] 
>   1.31e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.77e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.19e-04s  0.00e+00d  [ExpandObjective] #entries=32'436 #tight_variables=2'446 #tight_constraints=175 
> 
> Presolve summary:
>   - 109 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 125 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 4'045 times.
>   - rule 'affine: new relation' was applied 109 times.
>   - rule 'at_most_one: removed literals' was applied 19 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'bool_and: x => x' was applied 109 times.
>   - rule 'deductions: 7556 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 109 times.
>   - rule 'dual: fix variable' was applied 50 times.
>   - rule 'element: expanded' was applied 175 times.
>   - rule 'exactly_one: simplified objective' was applied 3 times.
>   - rule 'exactly_one: singleton' was applied 19 times.
>   - rule 'linear: divide by GCD' was applied 167 times.
>   - rule 'linear: reduced variable domains' was applied 1'056 times.
>   - rule 'new_bool: integer encoding' was applied 2'446 times.
>   - rule 'objective: variable not used elsewhere' was applied 81 times.
>   - rule 'presolve: 81 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 2'446 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x8ce5c1bfac5fcbba)
> #Variables: 3'062 (#bools: 552 in objective) (2'887 primary variables)
>   - 2'887 Booleans in [0,1]
>   - 2 in [0,10]
>   - 1 in [0,11]
>   - 2 in [0,12]
>   - 3 in [0,13]
>   - 1 in [0,14]
>   - 3 in [0,16]
>   - 1 in [1,11]
>   - 1 in [1,12]
>   - 2 in [1,13]
>   - 5 in [1,14]
>   - 1 in [1,15]
>   - 4 in [1,17]
>   - 2 in [2,12]
>   - 2 in [2,13]
>   - 1 in [2,14]
>   - 4 in [2,15]
>   - 2 in [2,16]
>   - 9 in [2,18]
>   - 2 in [3,13]
>   - 2 in [3,14]
>   - 2 in [3,15]
>   - 3 in [3,16]
>   - 2 in [3,17]
>   - 6 in [3,19]
>   - 2 in [4,14]
>   - 1 in [4,15]
>   - 2 in [4,16]
>   - 3 in [4,17]
>   - 4 in [4,18]
>   - 5 in [4,20]
>   - 2 in [5,15]
>   - 2 in [5,16]
>   - 1 in [5,17]
>   - 4 in [5,18]
>   - 1 in [5,19]
>   - 3 in [5,21]
>   - 1 in [6,16]
>   - 1 in [6,17]
>   - 2 in [6,18]
>   - 4 in [6,19]
>   - 2 in [6,20]
>   - 3 in [6,22]
>   - 2 in [7,17]
>   - 1 in [7,18]
>   - 1 in [7,19]
>   - 4 in [7,20]
>   - 1 in [7,21]
>   - 2 in [7,23]
>   - 2 in [8,18]
>   - 4 in [8,19]
>   - 2 in [8,20]
>   - 5 in [8,21]
>   - 3 in [8,22]
>   - 3 in [8,24]
>   - 1 in [9,19]
>   - 2 in [9,20]
>   - 3 in [9,21]
>   - 5 in [9,22]
>   - 2 in [9,23]
>   - 2 in [10,20]
>   - 1 in [10,21]
>   - 2 in [10,22]
>   - 4 in [10,23]
>   - 2 in [10,24]
>   - 2 in [11,21]
>   - 1 in [11,22]
>   - 1 in [11,23]
>   - 4 in [11,24]
>   - 1 in [12,22]
>   - 1 in [12,23]
>   - 1 in [12,24]
>   - 2 in [13,23]
>   - 1 in [13,24]
>   - 1 in [14,24]
> #kAtMostOne: 502 (#literals: 1'646)
> #kBoolAnd: 437 (#enforced: 437) (#literals: 1'618)
> #kExactlyOne: 175 (#literals: 2'446)
> #kLinear1: 4'892 (#enforced: 4'892)
> #kLinear2: 167
> [Symmetry] Graph for symmetry has 13'470 nodes and 21'244 arcs.
> [Symmetry] Symmetry computation done. time: 0.00148115 dtime: 0.00331232
> 
> Preloading model.
> #Bound   0.38s best:inf   next:[3,555]    initial_domain
> #Model   0.38s var:3062/3062 constraints:6173/6173
> 
> Starting search at 0.38s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.39s best:143   next:[3,142]    fj_restart(batch:1 lin{mvs:292 evals:2'401} #w_updates:0 #perturb:0)
> #2       0.42s best:142   next:[3,141]    rnd_cst_lns (d=5.00e-01 s=13 t=0.10 p=0.00 stall=0 h=base)
> #3       0.45s best:141   next:[3,140]    ls_restart_decay(batch:1 lin{mvs:5'409 evals:9'032} #w_updates:231 #perturb:0)
> #4       0.48s best:140   next:[3,139]    rnd_cst_lns (d=7.07e-01 s=21 t=0.10 p=1.00 stall=0 h=base)
> #5       0.52s best:138   next:[3,137]    graph_cst_lns (d=7.07e-01 s=24 t=0.10 p=1.00 stall=1 h=base)
> #6       0.56s best:136   next:[3,135]    default_lp
> #7       0.57s best:135   next:[3,134]    ls_lin_restart_compound_perturb(batch:1 lin{mvs:0 evals:23'273} gen{mvs:1'642 evals:0} comp{mvs:70 btracks:786} #w_updates:24 #perturb:0)
> #8       0.58s best:134   next:[3,133]    no_lp
> #Bound   0.59s best:134   next:[4,133]    bool_core (num_cores=1 [size:11 mw:1 amo:1 lit:3 d:4] a=542 d=4 fixed=0/4816 clauses=2'279)
> #9       0.66s best:126   next:[4,125]    graph_var_lns (d=7.07e-01 s=22 t=0.10 p=1.00 stall=1 h=base)
> #10      0.71s best:125   next:[4,124]    graph_dec_lns (d=8.14e-01 s=33 t=0.10 p=1.00 stall=2 h=base) [hint]
> #11      0.72s best:121   next:[4,120]    quick_restart_no_lp
> #Bound   0.74s best:121   next:[5,120]    bool_core (num_cores=2 [size:12 mw:1 d:4] a=531 d=4 fixed=0/4834 clauses=2'295)
> #Bound   0.76s best:121   next:[57,120]   max_lp
> #12      0.82s best:120   next:[57,119]   ls_lin_restart_compound(batch:1 lin{mvs:0 evals:88'400} gen{mvs:10'058 evals:0} comp{mvs:248 btracks:4'905} #w_updates:98 #perturb:0)
> #13      0.87s best:119   next:[57,118]   rnd_var_lns (d=7.21e-01 s=42 t=0.10 p=0.67 stall=0 h=base)
> #14      0.90s best:118   next:[57,117]   rnd_cst_lns (d=7.21e-01 s=43 t=0.10 p=0.67 stall=0 h=base) [hint]
> #15      0.96s best:116   next:[57,115]   graph_dec_lns (d=8.76e-01 s=44 t=0.10 p=1.00 stall=0 h=base)
> #Bound   0.98s best:116   next:[65,115]   max_lp
> #16      1.01s best:115   next:[65,114]   quick_restart_no_lp
> #17      1.05s best:114   next:[65,113]   quick_restart
> #18      1.13s best:113   next:[65,112]   quick_restart
> #19      1.27s best:112   next:[65,111]   ls_restart_perturb(batch:1 lin{mvs:20'211 evals:32'104} #w_updates:3'647 #perturb:0)
> #20      1.51s best:111   next:[65,110]   graph_cst_lns (d=5.97e-01 s=65 t=0.10 p=0.50 stall=1 h=base)
> #21      1.53s best:110   next:[65,109]   graph_var_lns (d=3.59e-01 s=67 t=0.10 p=0.33 stall=0 h=base)
> #22      1.79s best:109   next:[65,108]   rnd_cst_lns (d=8.03e-01 s=72 t=0.10 p=0.67 stall=1 h=base)
> #23      2.78s best:108   next:[65,107]   ls_restart(batch:1 lin{mvs:12'634 evals:20'606} #w_updates:4'133 #perturb:0)
> #24      3.00s best:107   next:[65,106]   rnd_cst_lns (d=8.03e-01 s=119 t=0.10 p=0.60 stall=3 h=base)
> #25      3.16s best:106   next:[65,105]   graph_cst_lns (d=6.07e-01 s=125 t=0.10 p=0.50 stall=5 h=base)
> #26      3.57s best:105   next:[65,104]   graph_arc_lns (d=3.94e-01 s=138 t=0.10 p=0.46 stall=10 h=base)
> #27      3.74s best:104   next:[65,103]   graph_cst_lns (d=4.94e-01 s=147 t=0.10 p=0.45 stall=0 h=base)
> #Bound   4.12s best:104   next:[66,103]   bool_core (num_cores=63 [size:4 mw:1 d:10] a=45 d=10 fixed=0/6203 clauses=11'303)
> #Bound   4.40s best:104   next:[67,103]   bool_core (num_cores=64 [size:2 mw:1 d:11] a=44 d=11 fixed=0/6245 clauses=13'130)
> #Bound   5.13s best:104   next:[68,103]   bool_core (num_cores=65 [size:9 mw:1 amo:3 lit:7 d:11] a=36 d=11 fixed=0/6322 clauses=18'253)
> #Bound   5.61s best:104   next:[69,103]   bool_core (num_cores=66 [size:1 mw:1] a=36 d=11 fixed=0/6367 clauses=17'737)
> #Bound   6.67s best:104   next:[70,103]   bool_core (num_cores=67 [size:2 mw:1 d:12] a=35 d=12 fixed=1/6425 clauses=24'233)
> #28      9.05s best:103   next:[70,102]   rnd_cst_lns (d=7.57e-01 s=312 t=0.10 p=0.52 stall=14 h=base)
> #Bound  10.16s best:103   next:[71,102]   bool_core (num_cores=68 [size:6 mw:1 d:13] a=30 d=13 fixed=1/6504 clauses=31'688)
> #29     11.30s best:102   next:[71,101]   rnd_cst_lns (d=8.29e-01 s=365 t=0.10 p=0.55 stall=4 h=base)
> #Bound  14.60s best:102   next:[72,101]   bool_core (num_cores=69 [size:5 mw:1 d:14] a=26 d=14 fixed=1/6620 clauses=33'390)
> #Bound  20.83s best:102   next:[73,101]   bool_core (num_cores=70 [size:11 mw:1 amo:1 lit:2 d:15] a=16 d=15 fixed=1/6732 clauses=36'906)
> #Bound  29.88s best:102   next:[74,101]   bool_core (num_cores=71 [size:5 mw:1 amo:1 lit:2 d:16] a=12 d=16 fixed=1/6837 clauses=47'790)
> #Bound  46.41s best:102   next:[75,101]   bool_core (num_cores=72 [size:7 mw:1 amo:1 lit:2 d:17] a=6 d=17 fixed=1/6934 clauses=55'088)
> #Bound  79.21s best:102   next:[76,101]   bool_core (num_cores=73 [size:3 mw:1 d:18] a=4 d=18 fixed=1/7017 clauses=66'429)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.93m,    1.93m]    1.93m   0.00ns    1.93m
>            'default_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [  37.18s,   37.18s]   37.18s   0.00ns   37.18s
>      'feasibility_pump':       529 [ 14.58us,  14.65ms] 233.28us 643.69us 123.40ms       524 [ 41.91us,   2.48ms]  46.57us 106.55us  24.40ms
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         1 [  4.59ms,   4.59ms]   4.59ms   0.00ns   4.59ms         1 [591.54us, 591.54us] 591.54us   0.00ns 591.54us
>             'fs_random':         1 [  5.29ms,   5.29ms]   5.29ms   0.00ns   5.29ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [  5.35ms,   5.35ms]   5.35ms   0.00ns   5.35ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':       349 [ 12.05ms, 551.93ms] 151.69ms 120.79ms   52.94s       347 [169.00ns, 112.68ms]  61.78ms  46.98ms   21.44s
>         'graph_cst_lns':       292 [ 20.56ms, 544.47ms] 182.35ms 126.25ms   53.25s       292 [ 64.46us, 110.49ms]  63.91ms  45.20ms   18.66s
>         'graph_dec_lns':       251 [  7.19ms, 759.63ms] 213.02ms 169.64ms   53.47s       251 [ 10.00ns, 108.36ms]  59.70ms  46.81ms   14.98s
>         'graph_var_lns':       338 [ 13.23ms, 479.12ms] 157.17ms 116.48ms   53.12s       338 [ 10.00ns, 112.69ms]  63.53ms  46.63ms   21.47s
>                    'ls':       444 [ 26.26ms, 213.26ms] 118.89ms  11.76ms   52.79s       444 [ 21.69ms, 100.03ms]  99.36ms   6.11ms   44.11s
>                'ls_lin':       431 [ 11.59ms, 154.05ms] 122.46ms   8.61ms   52.78s       431 [  9.91ms, 100.19ms]  99.67ms   4.96ms   42.96s
>                'max_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.81m,    1.81m]    1.81m   0.00ns    1.81m
>                 'no_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m
>          'pseudo_costs':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.50m,    1.50m]    1.50m   0.00ns    1.50m
>         'quick_restart':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [  37.90s,   37.90s]   37.90s   0.00ns   37.90s
>   'quick_restart_no_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.27m,    1.27m]    1.27m   0.00ns    1.27m
>         'reduced_costs':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.57m,    1.57m]    1.57m   0.00ns    1.57m
>             'rins/rens':       248 [  1.07ms, 899.66ms] 213.61ms 242.99ms   52.97s       229 [ 10.00ns, 104.25ms]  51.15ms  50.68ms   11.71s
>           'rnd_cst_lns':       256 [ 18.96ms, 661.53ms] 208.49ms 155.98ms   53.37s       256 [  8.91us, 108.29ms]  60.10ms  46.70ms   15.38s
>           'rnd_var_lns':       262 [  9.97ms, 625.16ms] 203.87ms 161.10ms   53.41s       262 [ 10.00ns, 108.31ms]  59.84ms  46.98ms   15.68s
> 
> Search stats              Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  7'090    406'712  1'322'586    66'419  510'361'402     30'349'245
>            'default_lp':  4'808    446'384    909'287    73'354   71'752'110     57'247'574
>             'fs_random':  3'067          0          0         0            0              0
>       'fs_random_no_lp':  3'139          0          0         0            0              0
>                'max_lp':  4'808      2'652    126'760    45'016   10'355'466      7'442'229
>                 'no_lp':  4'808  1'458'570  2'861'381   220'160  189'010'543    174'870'140
>          'pseudo_costs':  4'808      4'257    351'027   115'549   26'800'454     18'727'470
>         'quick_restart':  4'808    133'329  3'240'567   141'623  100'570'476     50'433'456
>   'quick_restart_no_lp':  4'808    320'194  8'006'686   263'316  222'761'956    116'060'802
>         'reduced_costs':  4'808      5'323    165'804    52'132   12'783'642      9'264'428
> 
> SAT stats                 ClassicMinim  LitRemoved   LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':       382'297  10'611'672   12'070'320    10'011'935       684    34'590     270'722         0      9'480      199'972    1'231
>            'default_lp':       431'605   3'528'910   72'672'367    69'738'647       305    40'553     112'519         0         33          424        0
>             'fs_random':             0           0            0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0            0             0         0         0           0         0          0            0        0
>                'max_lp':         2'601     278'591    1'138'572             0         3    22'630      63'716         0         19          246        0
>                 'no_lp':     1'318'293   9'139'696  193'064'260   190'082'119       857   133'401     352'703         0         73          980        0
>          'pseudo_costs':         4'205     490'290    2'428'824             0         4    67'622     187'851         0         30          388        0
>         'quick_restart':       112'306   1'091'593   15'687'055    13'645'520       463    76'188     206'990         0         64          870        0
>   'quick_restart_no_lp':       261'284   2'548'674   36'920'435    34'636'696     1'907   142'939     463'603         0        121        3'356    6'904
>         'reduced_costs':         5'295     606'446    2'748'950             0         1    27'191      76'732         0         17          233        0
> 
> Lp stats            Component  Iterations  AddedCuts    OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          8     263'777        711  2'732'986        0        0
>          'max_lp':          1   1'183'267      7'744      5'573    3'505        0
>    'pseudo_costs':          1   1'244'484      9'603     10'899    4'099        0
>   'quick_restart':          8   1'209'648        716  1'939'304        1        0
>   'reduced_costs':          1   1'500'181      9'874     10'629    5'403        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':          7 rows, 46 columns, 21 entries
>          'max_lp':  1820 rows, 3062 columns, 12795 entries
>    'pseudo_costs':  1618 rows, 3062 columns, 10586 entries
>   'quick_restart':         22 rows, 46 columns, 53 entries
>   'reduced_costs':   1464 rows, 3062 columns, 9786 entries
> 
> Lp debug            CutPropag  CutEqPropag   Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0   82'209         0       0           0
>          'max_lp':          0            0    9'078         0  25'933           0
>    'pseudo_costs':          0            0   14'979         0   2'980           0
>   'quick_restart':          0            0  158'138         0       0           0
>   'reduced_costs':          0            0   15'963         0   3'149           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':        1'073        0        0       0          0      0             0    711/20'872
>          'max_lp':       10'469      122        0       0          0    331           750  7'744/19'666
>    'pseudo_costs':       12'328       51        0       0          0     43         1'561  9'603/14'631
>   'quick_restart':        1'078        0        0       0          0      0             0   716/141'403
>   'reduced_costs':       12'599       45        0       0          0     20         1'593  9'874/15'508
> 
> Lp Cut            pseudo_costs  default_lp  max_lp  quick_restart  reduced_costs
>           CG_FF:            60           -       6              -             56
>            CG_K:            31           -       7              -             28
>           CG_KL:             7           -       2              -              9
>            CG_R:            21           -       6              -             27
>           CG_RB:            48           -       7              -             45
>          CG_RBP:            20           -       5              -             28
>          Clique:            23           -      32              -             30
>              IB:         5'083         711     952            716          4'321
>        MIR_1_FF:           349           -     429              -            501
>         MIR_1_K:           351           -     397              -            400
>        MIR_1_KL:           147           -     140              -            215
>         MIR_1_R:             1           -       6              -              1
>        MIR_1_RB:           335           -     491              -            336
>       MIR_1_RBP:           153           -     202              -            150
>        MIR_2_FF:           422           -     551              -            590
>         MIR_2_K:           417           -     586              -            488
>        MIR_2_KL:           107           -     147              -            120
>         MIR_2_R:             3           -       1              -              6
>        MIR_2_RB:           368           -     816              -            396
>       MIR_2_RBP:           144           -     352              -            198
>        MIR_3_FF:           111           -     190              -            164
>         MIR_3_K:            76           -     128              -             78
>        MIR_3_KL:            19           -      41              -             30
>         MIR_3_R:            45           -      75              -             73
>        MIR_3_RB:            47           -     154              -             52
>       MIR_3_RBP:            16           -      46              -             28
>        MIR_4_FF:            74           -     172              -             83
>         MIR_4_K:            44           -      95              -             29
>        MIR_4_KL:             9           -      20              -             16
>         MIR_4_R:            40           -     153              -             47
>        MIR_4_RB:            25           -      56              -             21
>       MIR_4_RBP:            16           -      18              -              6
>        MIR_5_FF:            34           -     131              -             43
>         MIR_5_K:            10           -      45              -             17
>        MIR_5_KL:             7           -       8              -             10
>         MIR_5_R:            14           -      90              -             25
>        MIR_5_RB:            12           -      45              -              5
>       MIR_5_RBP:             4           -      15              -              5
>        MIR_6_FF:            21           -      87              -             25
>         MIR_6_K:             6           -      40              -              6
>        MIR_6_KL:             2           -       8              -              3
>         MIR_6_R:             9           -      65              -             14
>        MIR_6_RB:             8           -      23              -              5
>       MIR_6_RBP:             1           -      10              -              3
>    ZERO_HALF_FF:           147           -      68              -            225
>     ZERO_HALF_K:           130           -      68              -            157
>    ZERO_HALF_KL:            11           -       9              -             29
>     ZERO_HALF_R:           300           -     639              -            386
>    ZERO_HALF_RB:           163           -      77              -            218
>   ZERO_HALF_RBP:           112           -      33              -            126
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':         4/347     50%    4.87e-01       0.11
>   'graph_cst_lns':         5/292     50%    6.19e-01       0.11
>   'graph_dec_lns':         2/251     51%    8.99e-01       0.11
>   'graph_var_lns':         4/338     49%    4.14e-01       0.11
>       'rins/rens':         5/234     51%    8.68e-01       0.10
>     'rnd_cst_lns':        10/256     51%    8.28e-01       0.11
>     'rnd_var_lns':         4/262     50%    8.37e-01       0.11
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves   GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1        292          0              0          0              0          2'401
>                          'ls_lin_restart':       62                 22  1'844'956          0              0          0         37'300      9'679'303
>                 'ls_lin_restart_compound':       56                 26          0  1'123'213        185'180    468'847          4'318     13'901'371
>         'ls_lin_restart_compound_perturb':       66                 27          0  1'313'593        211'174    551'081          4'400     15'859'634
>                    'ls_lin_restart_decay':       37                 26  1'932'946          0              0          0         14'241      7'258'768
>           'ls_lin_restart_decay_compound':       92                 22          0  1'780'523        710'919    534'719          3'411     26'917'769
>   'ls_lin_restart_decay_compound_perturb':       43                 24          0    893'840        330'496    281'602          1'864     12'983'800
>            'ls_lin_restart_decay_perturb':       40                 19  2'288'821          0              0          0         15'931      8'361'673
>                  'ls_lin_restart_perturb':       35                 22  1'062'653          0              0          0         65'953      5'896'623
>                              'ls_restart':       47                 21  1'208'516          0              0          0        121'882      4'379'021
>                     'ls_restart_compound':       39                 25          0    728'195         53'827    337'142          4'421      7'827'989
>             'ls_restart_compound_perturb':       45                 20          0    875'838         67'601    404'079          4'231      8'862'580
>                        'ls_restart_decay':       55                 24  1'754'736          0              0          0         16'139      5'022'441
>               'ls_restart_decay_compound':       56                 24          0  1'065'565        307'063    379'197          1'994     11'455'552
>       'ls_restart_decay_compound_perturb':      100                 29          0  1'964'881        558'346    703'163          2'739     20'510'381
>                'ls_restart_decay_perturb':       44                 25  1'433'923          0              0          0         13'284      4'089'415
>                      'ls_restart_perturb':       58                 25  1'461'053          0              0          0        154'566      5'378'562
> 
> Solutions (29)                        Num     Rank
>                        'default_lp':    1    [6,6]
>                        'fj_restart':    1    [1,1]
>                     'graph_arc_lns':    1  [26,26]
>                     'graph_cst_lns':    4   [5,27]
>                     'graph_dec_lns':    2  [10,15]
>                     'graph_var_lns':    2   [9,21]
>           'ls_lin_restart_compound':    1  [12,12]
>   'ls_lin_restart_compound_perturb':    1    [7,7]
>                        'ls_restart':    1  [23,23]
>                  'ls_restart_decay':    1    [3,3]
>                'ls_restart_perturb':    1  [19,19]
>                             'no_lp':    1    [8,8]
>                     'quick_restart':    2  [17,18]
>               'quick_restart_no_lp':    2  [11,16]
>                       'rnd_cst_lns':    7   [2,29]
>                       'rnd_var_lns':    1  [13,13]
> 
> Objective bounds     Num
>        'bool_core':   13
>   'initial_domain':    1
>           'max_lp':    2
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':  3'259    4'566    1'756
>    'fj solution hints':      0        0        0
>         'lp solutions':    363      129      339
>                 'pump':    528      119
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 102
> best_bound: 76
> integers: 727
> booleans: 3139
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.029
> usertime: 120.029
> deterministic_time: 853.87
> gap_integral: 2795.54
> solution_fingerprint: 0x14671148092bdbb
> ```

In [ ]:
```python
_model = Model(instance03)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x6fcf0a5bda8383ae)
> #Variables: 973 (#bools: 650 in objective) (973 primary variables)
>   - 650 Booleans in [0,1]
>   - 323 in [0,24]
> #kElement: 323
> #kLinear2: 307
> 
> Starting presolve at 0.01s
>   2.61e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.69e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=25 #num_dual_strengthening=1 
>   2.89e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.05e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   6.67e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 26'105 nodes and 39'633 arcs.
> [Symmetry] Symmetry computation done. time: 0.00483572 dtime: 0.00911198
>   3.99e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=4'212 
>   1.42e-01s  4.38e-01d  [Probe] #probed=18'672 #new_binary_clauses=332'985 
>   5.39e-05s  0.00e+00d  [MaxClique] 
>   2.40e-03s  0.00e+00d  [DetectDominanceRelations] 
>   3.24e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   5.30e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   7.25e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.68e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.63e-05s  1.84e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=307 
>   4.51e-04s  0.00e+00d  [DetectDifferentVariables] #different=156 
>   3.04e-04s  1.45e-05d  [ProcessSetPPC] #relevant_constraints=323 
>   6.20e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.53e-03s  2.07e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   3.18e-04s  1.81e-04d  [FindBigVerticalLinearOverlap] 
>   4.48e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.35e-05s  0.00e+00d  [MergeClauses] 
>   2.39e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.56e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.37e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.55e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.36e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   7.20e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 27'194 nodes and 45'451 arcs.
> [Symmetry] Symmetry computation done. time: 0.00358106 dtime: 0.00819958
> [SAT presolve] num removable Booleans: 0 / 5411
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:4784 literals:9568 vars:5356 one_side_vars:5356 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000150265s] clauses:4784 literals:9568 vars:5356 one_side_vars:5356 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00028487s] clauses:4784 literals:9568 vars:5356 one_side_vars:5356 simple_definition:0 singleton_clauses:0
>   3.80e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.35e-01s  4.37e-01d  [Probe] #probed=18'672 #new_binary_clauses=331'750 
>   2.19e-02s  1.78e-01d  [MaxClique] Merged 4'784(9'568 literals) into 3'645(8'429 literals) at_most_ones. 
>   2.56e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.61e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.75e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.18e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.24e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.29e-05s  1.84e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=307 
>   4.71e-04s  0.00e+00d  [DetectDifferentVariables] #different=156 
>   9.46e-04s  4.01e-05d  [ProcessSetPPC] #relevant_constraints=3'968 
>   1.15e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.41e-03s  1.38e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   3.43e-04s  1.75e-04d  [FindBigVerticalLinearOverlap] 
>   5.12e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.11e-04s  0.00e+00d  [MergeClauses] 
>   2.43e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.52e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.45e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.58e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.41e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   3.17e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 26'053 nodes and 42'258 arcs.
> [Symmetry] Symmetry computation done. time: 0.00359019 dtime: 0.00754193
> [SAT presolve] num removable Booleans: 0 / 5409
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:2734 literals:5468 vars:3306 one_side_vars:3306 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000112704s] clauses:2734 literals:5468 vars:3306 one_side_vars:3306 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000325848s] clauses:2734 literals:5468 vars:3306 one_side_vars:3306 simple_definition:0 singleton_clauses:0
>   4.64e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.35e-01s  4.38e-01d  [Probe] #probed=18'672 #new_binary_clauses=332'388 
>   2.07e-02s  1.70e-01d  [MaxClique] 
>   2.46e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.59e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.19e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.46e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.31e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.03e-04s  1.84e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=307 
>   4.87e-04s  0.00e+00d  [DetectDifferentVariables] #different=156 
>   9.31e-04s  4.01e-05d  [ProcessSetPPC] #relevant_constraints=3'968 
>   1.30e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.41e-03s  1.36e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   3.42e-04s  1.75e-04d  [FindBigVerticalLinearOverlap] 
>   6.69e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.14e-04s  0.00e+00d  [MergeClauses] 
>   2.46e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.53e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   9.96e-04s  0.00e+00d  [ExpandObjective] #entries=69'208 #tight_variables=4'839 #tight_constraints=323 
> 
> Presolve summary:
>   - 55 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 87 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 5'138 times.
>   - rule 'affine: new relation' was applied 55 times.
>   - rule 'at_most_one: removed literals' was applied 2 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'bool_and: x => x' was applied 55 times.
>   - rule 'deductions: 14627 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 55 times.
>   - rule 'dual: fix variable' was applied 8 times.
>   - rule 'element: expanded' was applied 323 times.
>   - rule 'exactly_one: singleton' was applied 2 times.
>   - rule 'linear: divide by GCD' was applied 307 times.
>   - rule 'linear: reduced variable domains' was applied 1'742 times.
>   - rule 'new_bool: integer encoding' was applied 4'839 times.
>   - rule 'objective: variable not used elsewhere' was applied 23 times.
>   - rule 'presolve: 23 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 4'839 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xc983f3130d1d66eb)
> #Variables: 5'732 (#bools: 629 in objective) (5'409 primary variables)
>   - 5'409 Booleans in [0,1]
>   - 2 in [0,10]
>   - 1 in [0,11]
>   - 3 in [0,12]
>   - 3 in [0,13]
>   - 5 in [0,14]
>   - 7 in [0,16]
>   - 6 in [0,17]
>   - 1 in [1,11]
>   - 1 in [1,12]
>   - 3 in [1,13]
>   - 5 in [1,14]
>   - 4 in [1,15]
>   - 6 in [1,17]
>   - 4 in [1,18]
>   - 2 in [2,12]
>   - 2 in [2,13]
>   - 2 in [2,14]
>   - 4 in [2,15]
>   - 7 in [2,16]
>   - 12 in [2,18]
>   - 4 in [2,19]
>   - 2 in [3,13]
>   - 2 in [3,14]
>   - 3 in [3,15]
>   - 3 in [3,16]
>   - 6 in [3,17]
>   - 11 in [3,19]
>   - 8 in [3,20]
>   - 2 in [4,14]
>   - 1 in [4,15]
>   - 5 in [4,16]
>   - 3 in [4,17]
>   - 10 in [4,18]
>   - 10 in [4,20]
>   - 3 in [4,21]
>   - 2 in [5,15]
>   - 2 in [5,16]
>   - 2 in [5,17]
>   - 4 in [5,18]
>   - 3 in [5,19]
>   - 7 in [5,21]
>   - 10 in [5,22]
>   - 1 in [6,16]
>   - 1 in [6,17]
>   - 3 in [6,18]
>   - 4 in [6,19]
>   - 5 in [6,20]
>   - 7 in [6,22]
>   - 10 in [6,23]
>   - 2 in [7,17]
>   - 1 in [7,18]
>   - 2 in [7,19]
>   - 4 in [7,20]
>   - 6 in [7,21]
>   - 4 in [7,23]
>   - 6 in [7,24]
>   - 2 in [8,18]
>   - 4 in [8,19]
>   - 5 in [8,20]
>   - 5 in [8,21]
>   - 8 in [8,22]
>   - 6 in [8,24]
>   - 1 in [9,19]
>   - 2 in [9,20]
>   - 6 in [9,21]
>   - 5 in [9,22]
>   - 6 in [9,23]
>   - 2 in [10,20]
>   - 1 in [10,21]
>   - 4 in [10,22]
>   - 4 in [10,23]
>   - 4 in [10,24]
>   - 2 in [11,21]
>   - 1 in [11,22]
>   - 4 in [11,23]
>   - 4 in [11,24]
>   - 1 in [12,22]
>   - 1 in [12,23]
>   - 2 in [12,24]
>   - 2 in [13,23]
>   - 1 in [13,24]
>   - 1 in [14,24]
> #kAtMostOne: 911 (#literals: 2'959)
> #kBoolAnd: 572 (#enforced: 572) (#literals: 3'306)
> #kExactlyOne: 323 (#literals: 4'839)
> #kLinear1: 9'678 (#enforced: 9'678)
> #kLinear2: 307
> [Symmetry] Graph for symmetry has 25'973 nodes and 42'258 arcs.
> [Symmetry] Symmetry computation done. time: 0.00339491 dtime: 0.00753713
> 
> Preloading model.
> #Bound   0.73s best:inf   next:[0,627]    initial_domain
> #Model   0.74s var:5732/5732 constraints:11791/11791
> 
> Starting search at 0.74s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.78s best:219   next:[0,218]    fj_restart(batch:1 lin{mvs:523 evals:4'679} #w_updates:0 #perturb:0)
> #2       0.81s best:218   next:[0,217]    rnd_var_lns (d=5.00e-01 s=13 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3       0.82s best:216   next:[0,215]    rnd_cst_lns (d=5.00e-01 s=14 t=0.10 p=0.00 stall=0 h=base)
> #4       0.84s best:214   next:[0,213]    graph_arc_lns (d=5.00e-01 s=16 t=0.10 p=0.00 stall=0 h=base)
> #5       0.84s best:213   next:[0,212]    graph_var_lns (d=5.00e-01 s=15 t=0.10 p=0.00 stall=0 h=base) [combined with: rnd_cst_lns (d=5.00e...]
> #6       0.91s best:209   next:[0,208]    rnd_cst_lns (d=7.07e-01 s=22 t=0.10 p=1.00 stall=0 h=base)
> #7       1.03s best:207   next:[0,206]    rins_pump_lns (d=5.00e-01 s=28 t=0.10 p=0.00 stall=0 h=base)
> #8       1.03s best:206   next:[0,205]    ls_restart_decay_perturb(batch:1 lin{mvs:3 evals:210} #w_updates:0 #perturb:0)
> #9       1.13s best:205   next:[0,204]    quick_restart_no_lp
> #10      1.13s best:203   next:[0,202]    graph_arc_lns (d=7.07e-01 s=24 t=0.10 p=1.00 stall=0 h=base)
> #11      1.18s best:202   next:[0,201]    ls_restart_decay(batch:1 lin{mvs:3 evals:207} #w_updates:0 #perturb:0)
> #Bound   1.20s best:202   next:[1,201]    bool_core (num_cores=1 [size:18 mw:1 amo:1 lit:2 d:5] a=612 d=5 fixed=0/9295 clauses=4'532)
> #12      1.21s best:201   next:[1,200]    graph_var_lns (d=5.38e-01 s=37 t=0.10 p=0.50 stall=0 h=base)
> #13      1.33s best:200   next:[1,199]    graph_arc_lns (d=5.38e-01 s=38 t=0.10 p=0.50 stall=0 h=base)
> #14      1.33s best:198   next:[1,197]    graph_arc_lns (d=5.38e-01 s=38 t=0.10 p=0.50 stall=0 h=base) [combined with: graph_var_lns (d=5.3...]
> #Bound   1.39s best:198   next:[57,197]   max_lp
> #15      1.43s best:192   next:[57,191]   no_lp
> #16      1.43s best:187   next:[57,186]   no_lp
> #17      1.43s best:175   next:[57,174]   quick_restart_no_lp
> #18      1.50s best:174   next:[57,173]   quick_restart_no_lp
> #19      1.50s best:173   next:[57,172]   no_lp
> #20      1.51s best:172   next:[57,171]   no_lp
> #21      1.52s best:171   next:[57,170]   no_lp
> #22      1.52s best:170   next:[57,169]   no_lp
> #23      1.55s best:169   next:[57,168]   no_lp
> #24      1.59s best:168   next:[57,167]   quick_restart_no_lp
> #Bound   1.67s best:168   next:[69,167]   max_lp
> #25      1.68s best:167   next:[69,166]   quick_restart
> #26      1.72s best:166   next:[69,165]   quick_restart_no_lp
> #27      1.74s best:165   next:[69,164]   quick_restart_no_lp
> #28      1.82s best:164   next:[69,163]   quick_restart
> #29      1.84s best:163   next:[69,162]   quick_restart_no_lp
> #30      1.97s best:162   next:[69,161]   graph_dec_lns (d=8.80e-01 s=59 t=0.10 p=0.80 stall=0 h=base)
> #Bound   2.08s best:162   next:[73,161]   max_lp
> #31      2.12s best:161   next:[73,160]   graph_var_lns (d=5.54e-01 s=57 t=0.10 p=0.50 stall=0 h=base)
> #32      2.12s best:160   next:[73,159]   graph_var_lns (d=5.54e-01 s=57 t=0.10 p=0.50 stall=0 h=base) [combined with: graph_arc_lns (d=2.4...]
> #33      2.35s best:159   next:[73,158]   graph_arc_lns (d=4.81e-01 s=70 t=0.10 p=0.50 stall=2 h=base)
> #34      2.38s best:158   next:[73,157]   graph_var_lns (d=3.94e-01 s=76 t=0.10 p=0.40 stall=0 h=base)
> #Bound   2.50s best:158   next:[74,157]   max_lp
> #35      2.78s best:157   next:[74,156]   quick_restart_no_lp
> #Bound   2.80s best:157   next:[75,156]   max_lp
> #36      3.36s best:156   next:[75,155]   graph_var_lns (d=5.34e-01 s=101 t=0.10 p=0.50 stall=2 h=base)
> #37      5.92s best:155   next:[75,154]   graph_cst_lns (d=6.47e-01 s=170 t=0.10 p=0.53 stall=11 h=base)
> #38      6.09s best:153   next:[75,152]   rnd_cst_lns (d=7.25e-01 s=178 t=0.10 p=0.55 stall=7 h=base)
> #39     10.72s best:152   next:[75,151]   graph_cst_lns (d=6.21e-01 s=306 t=0.10 p=0.52 stall=9 h=base)
> #Bound  10.77s best:152   next:[76,151]   bool_core (num_cores=76 [size:2 mw:1 d:11] a=32 d=11 fixed=1/11181 clauses=21'964)
> #Bound  12.29s best:152   next:[77,151]   bool_core (num_cores=77 [size:1 mw:1] a=32 d=11 fixed=1/11251 clauses=23'808)
> #40     13.81s best:151   next:[77,150]   graph_arc_lns (d=3.71e-01 s=390 t=0.10 p=0.48 stall=26 h=base)
> #Bound  14.83s best:151   next:[78,150]   bool_core (num_cores=78 [size:1 mw:1] a=32 d=11 fixed=2/11313 clauses=34'123)
> #Bound  21.12s best:151   next:[79,150]   bool_core (num_cores=79 [size:5 mw:1 d:12] a=28 d=12 fixed=3/11368 clauses=35'795)
> #Bound  26.87s best:151   next:[80,150]   bool_core (num_cores=80 [size:9 mw:1 d:13] a=20 d=13 fixed=3/11423 clauses=39'745)
> #41     27.11s best:150   next:[80,149]   ls_restart(batch:4 lin{mvs:103'144 evals:189'014} #w_updates:15'578 #perturb:0)
> #42     27.38s best:149   next:[80,148]   quick_restart_no_lp
> #43     27.49s best:148   next:[80,147]   ls_lin_restart_compound(batch:1 lin{mvs:0 evals:2'290} gen{mvs:136 evals:0} comp{mvs:12 btracks:62} #w_updates:2 #perturb:0)
> #44     27.71s best:147   next:[80,146]   quick_restart
> #45     27.78s best:146   next:[80,145]   quick_restart_no_lp
> #46     28.39s best:145   next:[80,144]   graph_var_lns (d=4.41e-01 s=787 t=0.10 p=0.50 stall=2 h=base)
> #47     30.34s best:144   next:[80,143]   quick_restart
> #48     30.61s best:143   next:[80,142]   graph_var_lns (d=4.37e-01 s=857 t=0.10 p=0.50 stall=4 h=base)
> #49     30.98s best:142   next:[80,141]   quick_restart_no_lp
> #50     32.86s best:141   next:[80,140]   graph_cst_lns (d=5.12e-01 s=920 t=0.10 p=0.49 stall=50 h=base)
> #51     33.83s best:140   next:[80,139]   graph_dec_lns (d=9.08e-01 s=947 t=0.10 p=0.53 stall=55 h=stalling)
> #52     34.40s best:139   next:[80,138]   quick_restart
> #53     35.45s best:138   next:[80,137]   graph_dec_lns (d=9.34e-01 s=978 t=0.10 p=0.55 stall=0 h=base)
> #Bound  35.93s best:138   next:[81,137]   bool_core (num_cores=81 [size:12 mw:1 amo:1 lit:3 d:14] a=9 d=14 fixed=3/11572 clauses=49'050)
> #Bound  47.40s best:138   next:[82,137]   bool_core (num_cores=82 [size:4 mw:1 amo:1 lit:2 d:15] a=6 d=15 fixed=3/11705 clauses=46'820)
> #54     49.87s best:137   next:[82,136]   rnd_cst_lns (d=7.78e-01 s=1360 t=0.10 p=0.52 stall=78 h=base)
> #Bound  78.76s best:137   next:[83,136]   bool_core (num_cores=83 [size:5 mw:1 amo:1 lit:2 d:16] a=2 d=16 fixed=3/11823 clauses=56'475)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.43m,    1.43m]    1.43m   0.00ns    1.43m
>            'default_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [  49.31s,   49.31s]   49.31s   0.00ns   49.31s
>      'feasibility_pump':       525 [ 55.15us,  28.67ms] 350.09us   1.26ms 183.80ms       522 [ 60.92us,   3.33ms]  67.19us 143.15us  35.07ms
>                    'fj':         1 [ 10.78ms,  10.78ms]  10.78ms   0.00ns  10.78ms         1 [  1.15ms,   1.15ms]   1.15ms   0.00ns   1.15ms
>                    'fj':         1 [ 26.85ms,  26.85ms]  26.85ms   0.00ns  26.85ms         1 [ 12.79ms,  12.79ms]  12.79ms   0.00ns  12.79ms
>             'fs_random':         1 [ 47.33ms,  47.33ms]  47.33ms   0.00ns  47.33ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [ 42.19ms,  42.19ms]  42.19ms   0.00ns  42.19ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':       350 [ 20.38ms, 663.69ms] 150.21ms 112.09ms   52.57s       350 [ 44.20us, 110.47ms]  60.03ms  46.66ms   21.01s
>         'graph_cst_lns':       267 [ 23.32ms, 634.70ms] 196.86ms 135.43ms   52.56s       265 [ 49.01us, 108.35ms]  59.28ms  46.31ms   15.71s
>         'graph_dec_lns':       223 [ 18.19ms, 769.44ms] 237.05ms 179.30ms   52.86s       223 [ 10.00ns, 106.22ms]  55.63ms  47.93ms   12.40s
>         'graph_var_lns':       328 [ 19.96ms, 558.52ms] 161.61ms 107.20ms   53.01s       328 [117.85us, 110.49ms]  62.31ms  45.74ms   20.44s
>                    'ls':       424 [  1.69ms, 198.08ms] 123.87ms  14.86ms   52.52s       424 [ 64.55us, 100.06ms]  99.51ms   6.87ms   42.19s
>                'ls_lin':       408 [  4.86ms, 212.03ms] 128.67ms  13.05ms   52.50s       408 [  1.26ms, 100.21ms]  99.80ms   4.89ms   40.72s
>                'max_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.02m,    1.02m]    1.02m   0.00ns    1.02m
>                 'no_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.28m,    1.28m]    1.28m   0.00ns    1.28m
>          'pseudo_costs':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [  56.46s,   56.46s]   56.46s   0.00ns   56.46s
>         'quick_restart':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [  37.69s,   37.69s]   37.69s   0.00ns   37.69s
>   'quick_restart_no_lp':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [  58.57s,   58.57s]   58.57s   0.00ns   58.57s
>         'reduced_costs':         1 [   1.99m,    1.99m]    1.99m   0.00ns    1.99m         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m
>             'rins/rens':       198 [  1.87ms, 905.60ms] 272.39ms 304.38ms   53.93s       180 [ 10.00ns, 106.63ms]  52.31ms  51.13ms    9.42s
>           'rnd_cst_lns':       206 [ 26.32ms, 824.82ms] 254.57ms 176.00ms   52.44s       205 [ 97.00ns, 106.15ms]  59.79ms  45.60ms   12.26s
>           'rnd_var_lns':       199 [ 25.84ms, 855.66ms] 271.48ms 212.06ms   54.02s       199 [ 10.00ns, 106.21ms]  60.56ms  46.42ms   12.05s
> 
> Search stats               Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  11'931    265'152  1'465'205    92'455  480'663'603     39'255'784
>            'default_lp':   9'279    473'039  1'252'981   156'822  130'235'846     84'335'153
>             'fs_random':   9'279          0      1'158     1'158       12'936         12'960
>       'fs_random_no_lp':   9'279          0      1'104     1'104       11'663         11'766
>                'max_lp':   9'279      8'207    473'635   156'417   39'202'336     26'520'017
>                 'no_lp':   9'279    890'286  1'882'720   239'023  199'898'298    142'126'437
>          'pseudo_costs':   9'279      9'936    567'978   184'012   45'878'947     31'236'134
>         'quick_restart':   9'279     99'588  3'498'662   165'448  136'358'743     56'655'077
>   'quick_restart_no_lp':   9'279    161'922  5'804'312   253'490  213'428'488     89'219'779
>         'reduced_costs':   9'279      3'209    339'394   115'001   25'786'404     17'870'426
> 
> SAT stats                 ClassicMinim  LitRemoved   LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':       247'555   6'975'833    7'768'390     5'875'980       523    38'753     267'643         0     10'359      185'797    1'221
>            'default_lp':       442'226   3'356'933  101'785'104    99'094'322       122    90'012     254'138         0         33          453        0
>             'fs_random':             0           0            0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0            0             0         0         0           0         0          0            0        0
>                'max_lp':         8'117   1'204'122    4'898'221             0         2    89'898     252'846         0         37          497        0
>                 'no_lp':       876'290  10'296'533  200'222'858   198'075'760       118   143'626     400'975         0         59          875        0
>          'pseudo_costs':         9'853   1'526'153    5'131'387             0         4   107'878     303'267         0         46          627        0
>         'quick_restart':        83'891     563'243   16'966'105    13'307'246       714    89'687     249'784         0         63          893        0
>   'quick_restart_no_lp':       136'857   1'007'811   27'886'808    25'343'664     1'255   143'109     395'016         0         86        1'198        0
>         'reduced_costs':         3'192   1'109'269    2'724'820             0         0    62'866     176'136         0         44          596        0
> 
> Lp stats            Component  Iterations  AddedCuts    OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         16     104'522        481  1'750'893        0        0
>       'fs_random':         16           0          0          0        0        0
>          'max_lp':          1     492'953      6'837      1'269   23'325        0
>    'pseudo_costs':          1     461'938     22'764      1'154   28'485        0
>   'quick_restart':         16   1'208'904        466  1'427'513        0        0
>   'reduced_costs':          1     871'801     19'215      3'706    8'499        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':           0 rows, 24 columns, 0 entries
>       'fs_random':           0 rows, 24 columns, 0 entries
>          'max_lp':  2895 rows, 5732 columns, 19535 entries
>    'pseudo_costs':  4346 rows, 5732 columns, 26652 entries
>   'quick_restart':         13 rows, 24 columns, 26 entries
>   'reduced_costs':  2345 rows, 5732 columns, 18432 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0   9'866         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0  24'594         0  18'069           0
>    'pseudo_costs':          0            0  29'601         0  12'384           0
>   'quick_restart':          0            0  12'381         0       0           0
>   'reduced_costs':          0            9  12'058         0   9'705           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened      Cuts/Call
>      'default_lp':          931        0        0       0          0      0             0     481/12'267
>       'fs_random':          450        0        0       0          0      0             0            0/0
>          'max_lp':       12'404      123        0       0          0    282         1'214   6'837/15'202
>    'pseudo_costs':       15'331      190        0       0          0    202         5'510  22'764/39'660
>   'quick_restart':          916        0        0       0          0      0             0     466/42'064
>   'reduced_costs':       14'782      192        0       0          0     94         4'339  19'215/31'422
> 
> Lp Cut            max_lp  default_lp  quick_restart  reduced_costs  pseudo_costs
>           CG_FF:       7           -              -             91            92
>            CG_K:       7           -              -             45            49
>           CG_KL:       1           -              -              4             6
>            CG_R:       6           -              -             49            47
>           CG_RB:       7           -              -             90            87
>          CG_RBP:       6           -              -             45            37
>          Clique:      12           -              -             42            39
>              IB:     681         481            466          4'492         6'894
>        MIR_1_FF:     411           -              -          1'342         1'192
>         MIR_1_K:     427           -              -          1'060         1'222
>        MIR_1_KL:     162           -              -            575           487
>         MIR_1_R:       2           -              -              5             1
>        MIR_1_RB:     418           -              -            914         1'067
>       MIR_1_RBP:     167           -              -            407           469
>        MIR_2_FF:     518           -              -          1'632         1'455
>         MIR_2_K:     592           -              -          1'171         1'430
>        MIR_2_KL:     145           -              -            360           343
>         MIR_2_R:       5           -              -             28            19
>        MIR_2_RB:     644           -              -          1'019         1'277
>       MIR_2_RBP:     263           -              -            517           556
>        MIR_3_FF:     181           -              -            434           420
>         MIR_3_K:     123           -              -            284           310
>        MIR_3_KL:      39           -              -            138           101
>         MIR_3_R:      64           -              -            150           177
>        MIR_3_RB:     106           -              -            127           192
>       MIR_3_RBP:      48           -              -             90            92
>        MIR_4_FF:     136           -              -            262           256
>         MIR_4_K:      68           -              -             98           141
>        MIR_4_KL:      18           -              -             52            45
>         MIR_4_R:     113           -              -            116           123
>        MIR_4_RB:      36           -              -             42            65
>       MIR_4_RBP:      13           -              -             20            28
>        MIR_5_FF:      86           -              -            112           124
>         MIR_5_K:      42           -              -             32            61
>        MIR_5_KL:       8           -              -             19            24
>         MIR_5_R:      62           -              -             49            55
>        MIR_5_RB:      37           -              -             18            37
>       MIR_5_RBP:      11           -              -             12            17
>        MIR_6_FF:      60           -              -             59            86
>         MIR_6_K:      24           -              -             27            53
>        MIR_6_KL:       4           -              -              7            12
>         MIR_6_R:      47           -              -             26            50
>        MIR_6_RB:      15           -              -             13            20
>       MIR_6_RBP:       3           -              -              8            10
>    ZERO_HALF_FF:      83           -              -            567           641
>     ZERO_HALF_K:     124           -              -            437           482
>    ZERO_HALF_KL:      22           -              -             49            49
>     ZERO_HALF_R:     589           -              -          1'057         1'293
>    ZERO_HALF_RB:     111           -              -            666           664
>   ZERO_HALF_RBP:      83           -              -            356           367
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':         7/350     50%    4.02e-01       0.11
>   'graph_cst_lns':         6/265     51%    6.56e-01       0.11
>   'graph_dec_lns':         6/223     52%    9.27e-01       0.11
>   'graph_var_lns':        10/328     50%    4.46e-01       0.11
>       'rins/rens':         2/181     50%    7.82e-01       0.11
>     'rnd_cst_lns':         7/205     50%    7.40e-01       0.11
>     'rnd_var_lns':         3/199     50%    7.85e-01       0.11
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves   GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1        523          0              0          0              0          4'679
>   'fj_restart_decay_compound_perturb_obj':        1                  1          0      5'529          3'271      1'129             17         53'267
>                          'ls_lin_restart':       57                 33  1'811'238          0              0          0         31'705     10'264'279
>                 'ls_lin_restart_compound':       75                 37          0  1'422'218        248'525    586'704         10'046     19'536'716
>         'ls_lin_restart_compound_perturb':       43                 24          0    796'732        169'696    313'396          4'853     11'794'324
>                    'ls_lin_restart_decay':       48                 34  2'750'153          0              0          0        103'046     11'925'316
>           'ls_lin_restart_decay_compound':       57                 28          0  1'102'929        456'398    323'187          1'812     17'919'506
>   'ls_lin_restart_decay_compound_perturb':       44                 27          0    865'165        387'820    238'581          1'615     14'272'112
>            'ls_lin_restart_decay_perturb':       39                 27  2'225'871          0              0          0        120'537     10'125'330
>                  'ls_lin_restart_perturb':       45                 31  1'528'764          0              0          0        160'747      9'105'481
>                              'ls_restart':       73                 35  1'997'553          0              0          0        108'615      7'743'826
>                     'ls_restart_compound':       37                 26          0    525'530         61'639    231'896          3'529      7'531'258
>             'ls_restart_compound_perturb':       57                 34          0    849'048        108'411    370'279          4'430     11'126'909
>                        'ls_restart_decay':       38                 24  1'243'277          0              0          0          6'729      3'698'782
>               'ls_restart_decay_compound':       67                 36          0  1'187'635        409'746    388'815          2'331     15'031'433
>       'ls_restart_decay_compound_perturb':       55                 28          0    978'824        343'991    317'348          1'859     12'550'525
>                'ls_restart_decay_perturb':       54                 36  1'775'306          0              0          0          9'582      5'264'736
>                      'ls_restart_perturb':       43                 28  1'206'030          0              0          0         49'411      4'481'656
> 
> Solutions (54)                 Num     Rank
>                 'fj_restart':    1    [1,1]
>              'graph_arc_lns':    6   [4,40]
>              'graph_cst_lns':    3  [37,50]
>              'graph_dec_lns':    3  [30,53]
>              'graph_var_lns':    8   [5,48]
>    'ls_lin_restart_compound':    1  [43,43]
>                 'ls_restart':    1  [41,41]
>           'ls_restart_decay':    1  [11,11]
>   'ls_restart_decay_perturb':    1    [8,8]
>                      'no_lp':    7  [15,23]
>              'quick_restart':    5  [25,52]
>        'quick_restart_no_lp':   11   [9,49]
>              'rins_pump_lns':    1    [7,7]
>                'rnd_cst_lns':    4   [3,54]
>                'rnd_var_lns':    1    [2,2]
> 
> Objective bounds     Num
>        'bool_core':    9
>   'initial_domain':    1
>           'max_lp':    5
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':  3'033    4'181    1'691
>    'fj solution hints':      0        0        0
>         'lp solutions':    546       96      495
>                 'pump':    524      102
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 137
> best_bound: 83
> integers: 978
> booleans: 9279
> conflicts: 0
> branches: 1104
> propagations: 11663
> integer_propagations: 11766
> restarts: 1104
> lp_iterations: 0
> walltime: 120.04
> usertime: 120.04
> deterministic_time: 700.586
> gap_integral: 2807.46
> solution_fingerprint: 0xf1d9bffe66399315
> ```

In [ ]:
```python
_model = Model(instance04)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0xbeccfc87c55e4ee)
> #Variables: 150 (#bools: 50 in objective) (150 primary variables)
>   - 50 Booleans in [0,1]
>   - 100 in [0,9]
> #kElement: 100
> #kLinear2: 90
> 
> Starting presolve at 0.00s
>   4.17e-05s  0.00e+00d  [DetectDominanceRelations] 
>   1.51e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=10 #num_dual_strengthening=1 
>   2.01e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   8.92e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   5.62e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'780 nodes and 4'030 arcs.
> [Symmetry] Symmetry computation done. time: 0.000504607 dtime: 0.0009608
>   1.81e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=420 
>   4.19e-03s  4.32e-03d  [Probe] #probed=1'380 #new_binary_clauses=4'590 
>   5.65e-06s  0.00e+00d  [MaxClique] 
>   2.24e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.00e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   6.87e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.68e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.56e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.75e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   1.04e-04s  0.00e+00d  [DetectDifferentVariables] #different=53 
>   5.29e-05s  1.41e-06d  [ProcessSetPPC] #relevant_constraints=100 
>   7.68e-06s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   7.55e-05s  7.92e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   2.36e-05s  1.94e-05d  [FindBigVerticalLinearOverlap] 
>   4.00e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   7.11e-06s  0.00e+00d  [MergeClauses] 
>   2.20e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.46e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.58e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.50e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.39e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   3.62e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'880 nodes and 4'600 arcs.
> [Symmetry] Symmetry computation done. time: 0.000484529 dtime: 0.00091365
> [SAT presolve] num removable Booleans: 0 / 520
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:470 literals:940 vars:520 one_side_vars:520 simple_definition:0 singleton_clauses:0
> [SAT presolve] [1.8465e-05s] clauses:470 literals:940 vars:520 one_side_vars:520 simple_definition:0 singleton_clauses:0
> [SAT presolve] [3.2752e-05s] clauses:470 literals:940 vars:520 one_side_vars:520 simple_definition:0 singleton_clauses:0
>   5.11e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.84e-03s  4.32e-03d  [Probe] #probed=1'380 #new_binary_clauses=4'590 
>   4.02e-04s  1.11e-03d  [MaxClique] Merged 470(940 literals) into 291(761 literals) at_most_ones. 
>   2.19e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.47e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.92e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.33e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.80e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.20e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   9.22e-05s  0.00e+00d  [DetectDifferentVariables] #different=53 
>   1.05e-04s  3.72e-06d  [ProcessSetPPC] #relevant_constraints=391 
>   1.20e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   8.51e-05s  7.23e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   3.07e-05s  1.85e-05d  [FindBigVerticalLinearOverlap] 
>   5.40e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.48e-05s  0.00e+00d  [MergeClauses] 
>   2.17e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.44e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.15e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.43e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.62e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   3.97e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'700 nodes and 4'122 arcs.
> [Symmetry] Symmetry computation done. time: 0.000389799 dtime: 0.00076164
> [SAT presolve] num removable Booleans: 0 / 520
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:172 literals:344 vars:221 one_side_vars:221 simple_definition:0 singleton_clauses:0
> [SAT presolve] [1.1421e-05s] clauses:172 literals:344 vars:221 one_side_vars:221 simple_definition:0 singleton_clauses:0
> [SAT presolve] [3.8242e-05s] clauses:172 literals:344 vars:221 one_side_vars:221 simple_definition:0 singleton_clauses:0
>   3.71e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.05e-03s  4.42e-03d  [Probe] #probed=1'380 #new_binary_clauses=4'783 
>   4.23e-04s  1.07e-03d  [MaxClique] 
>   2.18e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.46e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.91e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.23e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.71e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.30e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   9.31e-05s  0.00e+00d  [DetectDifferentVariables] #different=53 
>   1.35e-04s  3.72e-06d  [ProcessSetPPC] #relevant_constraints=391 
>   1.28e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   8.52e-05s  7.23e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   3.10e-05s  1.85e-05d  [FindBigVerticalLinearOverlap] 
>   6.29e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.50e-05s  0.00e+00d  [MergeClauses] 
>   2.16e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.44e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.24e-05s  0.00e+00d  [ExpandObjective] #entries=1'840 #tight_variables=470 #tight_constraints=100 
> 
> Presolve summary:
>   - 0 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 20 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 400 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'deductions: 1410 stored' was applied 1 time.
>   - rule 'element: expanded' was applied 100 times.
>   - rule 'linear: divide by GCD' was applied 90 times.
>   - rule 'linear: reduced variable domains' was applied 290 times.
>   - rule 'new_bool: integer encoding' was applied 470 times.
>   - rule 'presolve: 0 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 470 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xfe4ec177fcbb13dc)
> #Variables: 620 (#bools: 50 in objective) (520 primary variables)
>   - 520 Booleans in [0,1]
>   - 1 in [0,2]
>   - 6 in [0,3]
>   - 2 in [0,4]
>   - 5 in [0,5]
>   - 1 in [1,3]
>   - 4 in [1,4]
>   - 4 in [1,5]
>   - 9 in [1,6]
>   - 1 in [2,4]
>   - 8 in [2,5]
>   - 3 in [2,6]
>   - 4 in [2,7]
>   - 1 in [3,5]
>   - 6 in [3,6]
>   - 3 in [3,7]
>   - 4 in [3,8]
>   - 1 in [4,6]
>   - 5 in [4,7]
>   - 4 in [4,8]
>   - 8 in [4,9]
>   - 2 in [5,7]
>   - 6 in [5,8]
>   - 4 in [5,9]
>   - 2 in [6,8]
>   - 5 in [6,9]
>   - 1 in [7,9]
> #kAtMostOne: 119 (#literals: 417)
> #kBoolAnd: 49 (#enforced: 49) (#literals: 221)
> #kExactlyOne: 100 (#literals: 470)
> #kLinear1: 940 (#enforced: 940)
> #kLinear2: 90
> [Symmetry] Graph for symmetry has 2'700 nodes and 4'122 arcs.
> [Symmetry] Symmetry computation done. time: 0.00038471 dtime: 0.00076164
> 
> Preloading model.
> #Bound   0.04s best:inf   next:[0,50]     initial_domain
> #Model   0.04s var:620/620 constraints:1298/1298
> 
> Starting search at 0.04s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.04s best:35    next:[0,34]     fj_restart(batch:1 lin{mvs:135 evals:537} #w_updates:0 #perturb:0)
> #2       0.05s best:34    next:[0,33]     no_lp
> #Bound   0.05s best:34    next:[1,33]     bool_core (num_cores=1 [size:4 mw:1 d:2] a=47 d=2 fixed=0/692 clauses=372)
> #3       0.05s best:32    next:[1,31]     quick_restart
> #4       0.06s best:31    next:[1,30]     no_lp
> #Bound   0.06s best:31    next:[2,30]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=44 d=2 fixed=0/697 clauses=314)
> #Bound   0.06s best:31    next:[3,30]     bool_core (num_cores=3 [size:3 mw:1 d:2] a=42 d=2 fixed=0/701 clauses=318)
> #Bound   0.06s best:31    next:[4,30]     bool_core (num_cores=4 [size:5 mw:1 d:3] a=38 d=3 fixed=0/706 clauses=323)
> #Bound   0.06s best:31    next:[5,30]     bool_core (num_cores=5 [size:4 mw:1 d:2] a=35 d=3 fixed=0/712 clauses=329)
> #Bound   0.06s best:31    next:[6,30]     bool_core (num_cores=6 [size:3 mw:1 d:2] a=33 d=3 fixed=0/716 clauses=336)
> #Bound   0.06s best:31    next:[7,30]     bool_core (num_cores=7 [size:4 mw:1 d:3] a=30 d=3 fixed=0/720 clauses=341)
> #Bound   0.06s best:31    next:[8,30]     bool_core (num_cores=8 [size:3 mw:1 d:2] a=28 d=3 fixed=0/725 clauses=349)
> #Bound   0.07s best:31    next:[9,30]     bool_core (num_cores=9 [size:2 mw:1 d:3] a=27 d=3 fixed=0/727 clauses=354)
> #Bound   0.07s best:31    next:[10,30]    reduced_costs
> #Bound   0.07s best:31    next:[27,30]    max_lp
> #5       0.07s best:30    next:[27,29]    no_lp
> #Bound   0.10s best:30    next:[28,29]    bool_core (num_cores=24 [size:2 mw:1 d:8] a=2 d=8 fixed=4/816 clauses=1'020)
> #Bound   0.14s best:30    next:[29,29]    bool_core (num_cores=25 [size:2 mw:1 exo] a=0 d=8 fixed=4/831 clauses=1'015)
> #6       0.14s best:29    next:[]         core
> #Done    0.14s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [106.06ms, 106.06ms] 106.06ms   0.00ns 106.06ms         1 [ 77.18ms,  77.18ms]  77.18ms   0.00ns  77.18ms
>            'default_lp':         1 [107.01ms, 107.01ms] 107.01ms   0.00ns 107.01ms         1 [ 62.34ms,  62.34ms]  62.34ms   0.00ns  62.34ms
>      'feasibility_pump':         2 [462.50us,   2.50ms]   1.48ms   1.02ms   2.97ms         1 [ 70.65us,  70.65us]  70.65us   0.00ns  70.65us
>                    'fj':         1 [ 18.80ms,  18.80ms]  18.80ms   0.00ns  18.80ms         1 [ 12.99ms,  12.99ms]  12.99ms   0.00ns  12.99ms
>                    'fj':         1 [819.90us, 819.90us] 819.90us   0.00ns 819.90us         1 [165.88us, 165.88us] 165.88us   0.00ns 165.88us
>             'fs_random':         1 [  6.29ms,   6.29ms]   6.29ms   0.00ns   6.29ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [  3.50ms,   3.50ms]   3.50ms   0.00ns   3.50ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         3 [  4.79ms,  21.29ms]  14.41ms   7.01ms  43.22ms         2 [ 21.03us,  65.25us]  43.14us  22.11us  86.29us
>         'graph_cst_lns':         3 [  6.26us,  21.03ms]   7.83ms   9.39ms  23.48ms         2 [ 10.00ns, 174.55us]  87.28us  87.27us 174.56us
>         'graph_dec_lns':         2 [  2.05ms,   2.91ms]   2.48ms 431.51us   4.96ms         2 [ 10.00ns,  10.00ns]  10.00ns   0.00ns  20.00ns
>         'graph_var_lns':         3 [  7.89ms,  33.81ms]  16.94ms  11.93ms  50.83ms         3 [ 48.07us,   4.21ms]   1.44ms   1.96ms   4.31ms
>                    'ls':         1 [ 93.18ms,  93.18ms]  93.18ms   0.00ns  93.18ms         1 [ 67.96ms,  67.96ms]  67.96ms   0.00ns  67.96ms
>                'ls_lin':         1 [ 92.26ms,  92.26ms]  92.26ms   0.00ns  92.26ms         1 [ 64.69ms,  64.69ms]  64.69ms   0.00ns  64.69ms
>                'max_lp':         1 [106.95ms, 106.95ms] 106.95ms   0.00ns 106.95ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [106.91ms, 106.91ms] 106.91ms   0.00ns 106.91ms         1 [ 79.25ms,  79.25ms]  79.25ms   0.00ns  79.25ms
>          'pseudo_costs':         1 [106.86ms, 106.86ms] 106.86ms   0.00ns 106.86ms         1 [ 26.13ms,  26.13ms]  26.13ms   0.00ns  26.13ms
>         'quick_restart':         1 [106.00ms, 106.00ms] 106.00ms   0.00ns 106.00ms         1 [ 50.66ms,  50.66ms]  50.66ms   0.00ns  50.66ms
>   'quick_restart_no_lp':         1 [106.85ms, 106.85ms] 106.85ms   0.00ns 106.85ms         1 [ 91.26ms,  91.26ms]  91.26ms   0.00ns  91.26ms
>         'reduced_costs':         1 [106.90ms, 106.90ms] 106.90ms   0.00ns 106.90ms         1 [ 26.75ms,  26.75ms]  26.75ms   0.00ns  26.75ms
>             'rins/rens':         1 [  9.40ms,   9.40ms]   9.40ms   0.00ns   9.40ms         1 [ 31.31us,  31.31us]  31.31us   0.00ns  31.31us
>           'rnd_cst_lns':         3 [  2.93ms,  16.20ms]   8.62ms   5.58ms  25.86ms         3 [ 10.00ns,  30.74us]  10.70us  14.18us  32.09us
>           'rnd_var_lns':         3 [  2.28ms,  10.55ms]   5.36ms   3.69ms  16.09ms         3 [ 10.00ns, 406.00ns] 148.00ns 182.58ns 444.00ns
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':    831      1'161    20'470     4'874     522'939        170'883
>            'default_lp':    690      1'647    14'318     2'947     269'911        125'591
>             'fs_random':    690          0        60        60         797          1'171
>       'fs_random_no_lp':    690          0        84        84       1'118          1'629
>                'max_lp':    690          0     1'380     1'380      27'300         34'954
>                 'no_lp':    690      2'614    11'814     3'409     396'633        176'734
>          'pseudo_costs':    690         50     4'476     2'410      66'548         82'150
>         'quick_restart':    690      1'072    13'289     3'528     243'443        117'777
>   'quick_restart_no_lp':    690      1'935    18'237     3'586     357'037        170'434
>         'reduced_costs':    690         35     4'527     2'420      64'826         80'944
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':           816       2'443       7'306             0        13     2'686       7'423         0        270        1'692      165
>            'default_lp':           682       1'416      53'971             0        21       929       8'307         0        137        2'706      122
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':         1'048       1'960      87'097             0        24     1'359       4'500         0         93          795      131
>          'pseudo_costs':            50         407       1'050             0         0       689       1'643         0         67          302        0
>         'quick_restart':           497       1'141      32'963             0        26     1'390       4'422         0         82          636       39
>   'quick_restart_no_lp':           869       2'177      60'733             0        29     1'371       4'530         0         83          578       42
>         'reduced_costs':            32         106         536             0         0       699       1'677         0         60          274        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         10           0          0    2'897        0        0
>       'fs_random':         10           0          0        0        0        0
>          'max_lp':          1         439        696        2        0        0
>    'pseudo_costs':          1       2'002        863       19      129        0
>   'quick_restart':         10           0          0    3'778        0        0
>   'reduced_costs':          1       1'867        914       18      120        0
> 
> Lp dimension         Final dimension of first component
>      'default_lp':        0 rows, 10 columns, 0 entries
>       'fs_random':        0 rows, 10 columns, 0 entries
>          'max_lp':  886 rows, 620 columns, 2962 entries
>    'pseudo_costs':  600 rows, 620 columns, 1734 entries
>   'quick_restart':        0 rows, 10 columns, 0 entries
>   'reduced_costs':  650 rows, 620 columns, 1919 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>       'fs_random':          0            0       0         0      0           0
>          'max_lp':          0            0       2         0  2'714           0
>    'pseudo_costs':          0            0     140         0    613           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0     131         0    828           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':           90        0        0       0          0      0             0        0/0
>       'fs_random':           90        0        0       0          0      0             0        0/0
>          'max_lp':        1'577       91        0       0          0     57             4  696/2'342
>    'pseudo_costs':        1'744        4        0       0          0      4            52  863/1'722
>   'quick_restart':           90        0        0       0          0      0             0        0/0
>   'reduced_costs':        1'795        0        0       0          0      0            15  914/1'852
> 
> Lp Cut            max_lp  reduced_costs  pseudo_costs
>           CG_FF:       -             28            32
>            CG_K:       -             12            14
>           CG_KL:       -              2             -
>            CG_R:       5              4             1
>           CG_RB:      10             24            24
>          CG_RBP:       7              4             6
>          Clique:       5             19            23
>              IB:       -            438           393
>        MIR_1_FF:      91             41            39
>         MIR_1_K:      65             54            41
>        MIR_1_KL:       9              9             3
>        MIR_1_RB:      37              6             6
>       MIR_1_RBP:       7              1             2
>        MIR_2_FF:      92             24            28
>         MIR_2_K:      41             29            31
>        MIR_2_KL:      13              3             4
>         MIR_2_R:       -              -             2
>        MIR_2_RB:      51              4             7
>       MIR_2_RBP:       7              1             3
>        MIR_3_FF:      39              6             9
>         MIR_3_K:      14              6            11
>        MIR_3_KL:       3              1             2
>         MIR_3_R:       2              2             -
>        MIR_3_RB:      12              4             7
>       MIR_3_RBP:       7              3             -
>        MIR_4_FF:      25              2             8
>         MIR_4_K:       6              -             2
>        MIR_4_KL:       2              1             1
>         MIR_4_R:       8              -             -
>        MIR_4_RB:       6              1             1
>       MIR_4_RBP:       1              -             -
>        MIR_5_FF:       9              -             2
>         MIR_5_K:       2              -             2
>        MIR_5_KL:       2              -             -
>         MIR_5_R:       2              -             -
>        MIR_5_RB:       4              -             1
>       MIR_5_RBP:       3              -             -
>        MIR_6_FF:       1              -             3
>         MIR_6_K:       1              -             -
>        MIR_6_RB:       1              -             -
>    ZERO_HALF_FF:      15             42            45
>     ZERO_HALF_K:       5             32            29
>    ZERO_HALF_KL:       -              2             -
>     ZERO_HALF_R:      83             70            48
>    ZERO_HALF_RB:       3             26            21
>   ZERO_HALF_RBP:       -             13            12
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           0/2    100%    8.14e-01       0.10
>   'graph_cst_lns':           0/2    100%    8.14e-01       0.10
>   'graph_dec_lns':           0/2    100%    8.14e-01       0.10
>   'graph_var_lns':           0/3    100%    8.76e-01       0.10
>       'rins/rens':           0/1    100%    7.07e-01       0.10
>     'rnd_cst_lns':           0/3    100%    8.76e-01       0.10
>     'rnd_var_lns':           0/3    100%    8.76e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1       135         0              0          0              0            537
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0     8'202          1'844      3'179             62         62'936
>                  'ls_lin_restart_perturb':        1                  1    59'456         0              0          0          8'960        470'815
>                        'ls_restart_decay':        1                  1    57'551         0              0          0          1'872        142'716
> 
> Solutions (6)       Num   Rank
>            'core':    1  [6,6]
>      'fj_restart':    1  [1,1]
>           'no_lp':    3  [2,5]
>   'quick_restart':    1  [3,3]
> 
> Objective bounds     Num
>        'bool_core':   11
>   'initial_domain':    1
>           'max_lp':    1
>    'reduced_costs':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     28       37       18
>    'fj solution hints':      0        0        0
>         'lp solutions':      0        0        0
>                 'pump':      1        1
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 29
> best_bound: 29
> integers: 151
> booleans: 690
> conflicts: 0
> branches: 84
> propagations: 1118
> integer_propagations: 1629
> restarts: 84
> lp_iterations: 0
> walltime: 0.148206
> usertime: 0.148206
> deterministic_time: 0.579588
> gap_integral: 0.0481075
> solution_fingerprint: 0xbaac759c9e0d5b7a
> ```

In [ ]:
```python
_model = Model(instance05)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0xb402e8729ca35680)
> #Variables: 550 (#bools: 50 in objective) (550 primary variables)
>   - 50 Booleans in [0,1]
>   - 500 in [0,9]
> #kElement: 500
> #kLinear2: 450
> 
> Starting presolve at 0.00s
>   1.52e-04s  0.00e+00d  [DetectDominanceRelations] 
>   7.67e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=10 #num_dual_strengthening=1 
>   3.28e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   4.29e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.72e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 13'550 nodes and 19'910 arcs.
> [Symmetry] Symmetry computation done. time: 0.00329766 dtime: 0.00620883
>   8.32e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=2'270 
>   1.91e-02s  2.08e-02d  [Probe] #probed=6'380 #new_binary_clauses=22'230 
>   1.65e-05s  0.00e+00d  [MaxClique] 
>   1.04e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.44e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   2.72e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.59e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.12e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.41e-05s  2.70e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=450 
>   3.48e-04s  0.00e+00d  [DetectDifferentVariables] #different=268 
>   1.74e-04s  6.96e-06d  [ProcessSetPPC] #relevant_constraints=500 
>   3.26e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   3.59e-04s  3.85e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.27e-04s  9.50e-05d  [FindBigVerticalLinearOverlap] 
>   2.34e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   3.21e-05s  0.00e+00d  [MergeClauses] 
>   1.03e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.17e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.02e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.15e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.20e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.45e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 13'650 nodes and 22'330 arcs.
> [Symmetry] Symmetry computation done. time: 0.00255946 dtime: 0.00586918
> [SAT presolve] num removable Booleans: 0 / 2370
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:2320 literals:4640 vars:2370 one_side_vars:2370 simple_definition:0 singleton_clauses:0
> [SAT presolve] [7.4942e-05s] clauses:2320 literals:4640 vars:2370 one_side_vars:2370 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000107203s] clauses:2320 literals:4640 vars:2370 one_side_vars:2370 simple_definition:0 singleton_clauses:0
>   1.73e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.77e-02s  2.08e-02d  [Probe] #probed=6'380 #new_binary_clauses=22'230 
>   3.45e-03s  1.19e-02d  [MaxClique] Merged 2'320(4'640 literals) into 1'482(3'802 literals) at_most_ones. 
>   1.01e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.12e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.76e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.51e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.37e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.90e-05s  2.70e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=450 
>   3.46e-04s  0.00e+00d  [DetectDifferentVariables] #different=268 
>   4.53e-04s  1.85e-05d  [ProcessSetPPC] #relevant_constraints=1'982 
>   5.24e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.12e-04s  3.36e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.28e-04s  9.08e-05d  [FindBigVerticalLinearOverlap] 
>   2.83e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.08e-05s  0.00e+00d  [MergeClauses] 
>   1.01e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.95e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.01e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.94e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.38e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.30e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 12'812 nodes and 20'037 arcs.
> [Symmetry] Symmetry computation done. time: 0.00217762 dtime: 0.004544
> [SAT presolve] num removable Booleans: 0 / 2370
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:865 literals:1730 vars:915 one_side_vars:915 simple_definition:0 singleton_clauses:0
> [SAT presolve] [3.9394e-05s] clauses:865 literals:1730 vars:915 one_side_vars:915 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000118805s] clauses:865 literals:1730 vars:915 one_side_vars:915 simple_definition:0 singleton_clauses:0
>   1.45e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.88e-02s  2.12e-02d  [Probe] #probed=6'380 #new_binary_clauses=23'086 
>   3.54e-03s  1.18e-02d  [MaxClique] 
>   1.01e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.10e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.82e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.53e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.42e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.74e-05s  2.70e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=450 
>   3.55e-04s  0.00e+00d  [DetectDifferentVariables] #different=268 
>   4.32e-04s  1.85e-05d  [ProcessSetPPC] #relevant_constraints=1'982 
>   5.51e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.02e-04s  3.37e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.29e-04s  9.08e-05d  [FindBigVerticalLinearOverlap] 
>   3.02e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.98e-05s  0.00e+00d  [MergeClauses] 
>   1.01e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.95e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.40e-04s  0.00e+00d  [ExpandObjective] #entries=8'880 #tight_variables=2'320 #tight_constraints=500 
> 
> Presolve summary:
>   - 0 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 100 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 400 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'deductions: 6960 stored' was applied 1 time.
>   - rule 'element: expanded' was applied 500 times.
>   - rule 'linear: divide by GCD' was applied 450 times.
>   - rule 'linear: reduced variable domains' was applied 1'483 times.
>   - rule 'new_bool: integer encoding' was applied 2'320 times.
>   - rule 'presolve: 0 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 2'320 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x636fa17ebc583388)
> #Variables: 2'870 (#bools: 50 in objective) (2'370 primary variables)
>   - 2'370 Booleans in [0,1]
>   - 7 in [0,2]
>   - 22 in [0,3]
>   - 22 in [0,4]
>   - 14 in [0,5]
>   - 3 in [0,6]
>   - 6 in [1,3]
>   - 27 in [1,4]
>   - 34 in [1,5]
>   - 20 in [1,6]
>   - 1 in [1,7]
>   - 5 in [2,4]
>   - 28 in [2,5]
>   - 33 in [2,6]
>   - 15 in [2,7]
>   - 3 in [2,8]
>   - 7 in [3,5]
>   - 27 in [3,6]
>   - 30 in [3,7]
>   - 13 in [3,8]
>   - 3 in [3,9]
>   - 5 in [4,6]
>   - 26 in [4,7]
>   - 27 in [4,8]
>   - 18 in [4,9]
>   - 8 in [5,7]
>   - 27 in [5,8]
>   - 34 in [5,9]
>   - 6 in [6,8]
>   - 23 in [6,9]
>   - 6 in [7,9]
> #kAtMostOne: 617 (#literals: 2'072)
> #kBoolAnd: 50 (#enforced: 50) (#literals: 915)
> #kExactlyOne: 500 (#literals: 2'320)
> #kLinear1: 4'640 (#enforced: 4'640)
> #kLinear2: 450
> [Symmetry] Graph for symmetry has 12'812 nodes and 20'037 arcs.
> [Symmetry] Symmetry computation done. time: 0.00213772 dtime: 0.004544
> 
> Preloading model.
> #Bound   0.17s best:inf   next:[0,50]     initial_domain
> #Model   0.17s var:2870/2870 constraints:6257/6257
> 
> Starting search at 0.17s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.20s best:38    next:[0,37]     fj_restart(batch:1 lin{mvs:538 evals:2'500} #w_updates:0 #perturb:0)
> #2       0.23s best:37    next:[0,36]     quick_restart
> #Bound   0.24s best:37    next:[1,36]     bool_core (num_cores=1 [size:3 mw:1 d:2] a=48 d=2 fixed=0/3191 clauses=1'821)
> #3       0.29s best:36    next:[1,35]     no_lp
> #Bound   0.29s best:36    next:[2,35]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=45 d=2 fixed=0/3195 clauses=1'556)
> #Bound   0.29s best:36    next:[3,35]     bool_core (num_cores=3 [size:3 mw:1 d:2] a=43 d=2 fixed=0/3199 clauses=1'560)
> #Bound   0.30s best:36    next:[4,35]     bool_core (num_cores=4 [size:3 mw:1 d:2] a=41 d=2 fixed=0/3202 clauses=1'563)
> #Bound   0.30s best:36    next:[5,35]     bool_core (num_cores=5 [size:3 mw:1 d:2] a=39 d=2 fixed=0/3205 clauses=1'567)
> #Bound   0.30s best:36    next:[8,35]     pseudo_costs
> #Bound   0.32s best:36    next:[9,35]     bool_core (num_cores=9 [size:4 mw:1 d:2] a=30 d=2 fixed=0/3218 clauses=1'580)
> #Bound   0.33s best:36    next:[10,35]    bool_core (num_cores=10 [size:3 mw:1 d:2] a=28 d=2 fixed=0/3222 clauses=1'584)
> #Bound   0.34s best:36    next:[11,35]    bool_core (num_cores=11 [size:3 mw:1 d:2] a=26 d=2 fixed=0/3225 clauses=1'587)
> #Bound   0.34s best:36    next:[12,35]    bool_core (num_cores=12 [size:3 mw:1 d:3] a=24 d=3 fixed=0/3228 clauses=1'591)
> #Bound   0.35s best:36    next:[13,35]    bool_core (num_cores=13 [size:4 mw:1 d:2] a=21 d=3 fixed=0/3233 clauses=1'596)
> #Bound   0.36s best:36    next:[14,35]    bool_core (num_cores=14 [size:3 mw:1 d:3] a=19 d=3 fixed=0/3237 clauses=1'603)
> #Bound   0.36s best:36    next:[15,35]    bool_core (num_cores=15 [size:3 mw:1 d:2] a=17 d=3 fixed=0/3241 clauses=1'607)
> #Bound   0.37s best:36    next:[16,35]    bool_core (num_cores=16 [size:2 mw:1 d:3] a=16 d=3 fixed=0/3243 clauses=1'610)
> #Bound   0.37s best:36    next:[17,35]    bool_core (num_cores=17 [size:2 mw:1 d:3] a=15 d=3 fixed=0/3245 clauses=1'618)
> #Bound   0.38s best:36    next:[18,35]    bool_core (num_cores=18 [size:3 mw:1 d:5] a=13 d=5 fixed=0/3248 clauses=1'627)
> #Bound   0.39s best:36    next:[19,35]    bool_core (num_cores=19 [size:3 mw:1 d:4] a=11 d=5 fixed=0/3253 clauses=1'638)
> #Bound   0.39s best:36    next:[20,35]    bool_core (num_cores=20 [size:2 mw:1 d:5] a=10 d=5 fixed=0/3257 clauses=1'651)
> #Bound   0.40s best:36    next:[21,35]    bool_core (num_cores=21 [size:2 mw:1 d:6] a=9 d=6 fixed=0/3261 clauses=1'673)
> #Bound   0.40s best:36    next:[22,35]    bool_core (num_cores=22 [size:2 mw:1 d:3] a=8 d=6 fixed=0/3266 clauses=1'688)
> #4       0.55s best:35    next:[33,34]    quick_restart
> #5       0.90s best:34    next:[]         core
> #Done    0.90s core
> #Bound   0.84s best:35    next:[34,34]    bool_core (num_cores=30 [size:1 mw:1] a=1 d=10 fixed=4/3318 clauses=2'807) [skipped_logs=11]
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [721.32ms, 721.32ms] 721.32ms   0.00ns 721.32ms         1 [441.33ms, 441.33ms] 441.33ms   0.00ns 441.33ms
>            'default_lp':         1 [723.88ms, 723.88ms] 723.88ms   0.00ns 723.88ms         1 [218.04ms, 218.04ms] 218.04ms   0.00ns 218.04ms
>      'feasibility_pump':         5 [277.97us,  12.85ms]   3.26ms   4.88ms  16.28ms         4 [ 66.08us, 638.71us] 209.24us 247.96us 836.96us
>                    'fj':         1 [  5.28ms,   5.28ms]   5.28ms   0.00ns   5.28ms         1 [746.85us, 746.85us] 746.85us   0.00ns 746.85us
>                    'fj':         1 [ 18.98ms,  18.98ms]  18.98ms   0.00ns  18.98ms         1 [  4.45ms,   4.45ms]   4.45ms   0.00ns   4.45ms
>             'fs_random':         1 [ 23.19ms,  23.19ms]  23.19ms   0.00ns  23.19ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [ 19.24ms,  19.24ms]  19.24ms   0.00ns  19.24ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         5 [ 22.22ms, 103.10ms]  63.58ms  27.02ms 317.91ms         5 [ 64.47us,   1.42ms] 647.28us 457.15us   3.24ms
>         'graph_cst_lns':         5 [ 25.75ms,  89.50ms]  54.55ms  22.54ms 272.76ms         5 [  2.08us, 919.74us] 355.60us 350.81us   1.78ms
>         'graph_dec_lns':         5 [  6.36ms,  29.09ms]  16.45ms   7.82ms  82.23ms         5 [ 10.00ns,   1.84us] 896.40ns 756.28ns   4.48us
>         'graph_var_lns':         5 [ 28.10ms,  93.30ms]  66.18ms  23.34ms 330.88ms         5 [217.79us,   1.31ms] 596.41us 386.36us   2.98ms
>                    'ls':         4 [ 64.09ms, 158.00ms] 130.65ms  38.59ms 522.59ms         4 [ 49.57ms, 100.00ms]  87.39ms  21.84ms 349.58ms
>                'ls_lin':         4 [ 81.93ms, 146.18ms] 127.34ms  26.39ms 509.36ms         4 [ 52.63ms, 100.00ms]  88.16ms  20.51ms 352.64ms
>                'max_lp':         1 [729.00ms, 729.00ms] 729.00ms   0.00ns 729.00ms         1 [ 44.82ms,  44.82ms]  44.82ms   0.00ns  44.82ms
>                 'no_lp':         1 [729.04ms, 729.04ms] 729.04ms   0.00ns 729.04ms         1 [525.04ms, 525.04ms] 525.04ms   0.00ns 525.04ms
>          'pseudo_costs':         1 [726.60ms, 726.60ms] 726.60ms   0.00ns 726.60ms         1 [145.45ms, 145.45ms] 145.45ms   0.00ns 145.45ms
>         'quick_restart':         1 [723.54ms, 723.54ms] 723.54ms   0.00ns 723.54ms         1 [177.67ms, 177.67ms] 177.67ms   0.00ns 177.67ms
>   'quick_restart_no_lp':         1 [722.92ms, 722.92ms] 722.92ms   0.00ns 722.92ms         1 [390.25ms, 390.25ms] 390.25ms   0.00ns 390.25ms
>         'reduced_costs':         1 [728.41ms, 728.41ms] 728.41ms   0.00ns 728.41ms         1 [149.04ms, 149.04ms] 149.04ms   0.00ns 149.04ms
>             'rins/rens':         6 [854.32us,  64.61ms]  43.36ms  22.95ms 260.17ms         4 [ 70.28us,   1.72ms] 871.68us 584.23us   3.49ms
>           'rnd_cst_lns':         5 [ 29.40ms,  72.61ms]  45.94ms  16.92ms 229.69ms         5 [ 52.00ns, 408.46us]  85.42us 161.60us 427.12us
>           'rnd_var_lns':         6 [ 10.87ms,  67.43ms]  41.25ms  18.44ms 247.47ms         5 [ 70.00ns, 521.00us] 108.19us 206.45us 540.95us
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  3'325      2'722    84'526    18'260   3'210'428      1'083'842
>            'default_lp':  3'190      2'118    37'470    12'998   1'487'912        545'254
>             'fs_random':  3'190          0       536       536      15'514         15'293
>       'fs_random_no_lp':  3'190          0        56        56       3'737          5'374
>                'max_lp':  3'190          0     6'380     6'380     130'780        169'338
>                 'no_lp':  3'190      4'165    75'639    13'997   2'625'074      1'139'911
>          'pseudo_costs':  3'190        318    21'562    11'324     450'771        488'686
>         'quick_restart':  3'190      1'314    44'598    14'488   1'149'785        470'393
>   'quick_restart_no_lp':  3'190      3'127    66'738    16'325   2'174'902        853'708
>         'reduced_costs':  3'190        347    21'594    11'310     460'782        506'071
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         1'962       7'835      22'125             0        26     8'872      24'139         0        915        5'468      281
>            'default_lp':           656       1'661      81'221             0        40     3'675      16'143         0        367        4'622       21
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':         1'282       3'749     154'948             0        64     4'752      52'823         0        827       24'118      601
>          'pseudo_costs':           182         585      11'821             0         2     3'470       8'392         0        254        1'091        0
>         'quick_restart':           532       1'234      48'700             0        26     5'057      14'097         0        350        2'109       13
>   'quick_restart_no_lp':         1'406       4'265     120'185             0        48     6'747      20'498         0        373        2'847      115
>         'reduced_costs':           204         847      12'393             0         1     3'454       8'335         0        254        1'091        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         50           0          0   14'196        0        0
>       'fs_random':         50           0          0        0        0        0
>          'max_lp':          1       2'332      3'042        1        1        0
>    'pseudo_costs':          1       7'569      2'430       34      486        0
>   'quick_restart':         50           0          0   14'964        0        0
>   'reduced_costs':          1       8'379      1'808       27      542        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':           0 rows, 10 columns, 0 entries
>       'fs_random':           0 rows, 10 columns, 0 entries
>          'max_lp':  4437 rows, 2870 columns, 14672 entries
>    'pseudo_costs':   1800 rows, 2870 columns, 5801 entries
>   'quick_restart':           0 rows, 10 columns, 0 entries
>   'reduced_costs':   1750 rows, 2870 columns, 5720 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0       2         0  11'480           0
>    'pseudo_costs':          0            0     475         0   3'080           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0     535         0   2'300           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':          450        0        0       0          0      0             0           0/0
>       'fs_random':          450        0        0       0          0      0             0           0/0
>          'max_lp':        7'474      453        0       0          0    277            99  3'042/10'656
>    'pseudo_costs':        6'862       16        0       0          0     33           289   2'430/5'734
>   'quick_restart':          450        0        0       0          0      0             0           0/0
>   'reduced_costs':        6'240        0        0       0          0      0           136   1'808/4'384
> 
> Lp Cut            max_lp  reduced_costs  pseudo_costs
>           CG_FF:       -             29            58
>            CG_K:       -             15            26
>           CG_KL:       -              6             -
>            CG_R:       -              3             4
>           CG_RB:       1             36            44
>          CG_RBP:       -              9            14
>          Clique:       4             21            29
>              IB:       -            695           738
>        MIR_1_FF:     452             77           127
>         MIR_1_K:     406             95           128
>        MIR_1_KL:      74             23            25
>        MIR_1_RB:     225              5            20
>       MIR_1_RBP:      56              6            14
>        MIR_2_FF:     432             57            96
>         MIR_2_K:     284             69           115
>        MIR_2_KL:      54             22            16
>         MIR_2_R:       -              -             2
>        MIR_2_RB:     225             12            17
>       MIR_2_RBP:      47              1            10
>        MIR_3_FF:     181             11            32
>         MIR_3_K:     104             11            33
>        MIR_3_KL:      25              3            10
>         MIR_3_R:      29              1             1
>        MIR_3_RB:      75              5             8
>       MIR_3_RBP:      25              1             4
>        MIR_4_FF:     107              9            19
>         MIR_4_K:      32              5             7
>        MIR_4_KL:      12              3             3
>         MIR_4_R:      31              -             3
>        MIR_4_RB:      19              2             1
>       MIR_4_RBP:       3              1             1
>        MIR_5_FF:      59              -             5
>         MIR_5_K:      16              -             -
>        MIR_5_KL:       1              -             -
>         MIR_5_R:      12              -             -
>        MIR_5_RB:      11              -             -
>       MIR_5_RBP:       2              -             -
>        MIR_6_FF:      19              -             -
>         MIR_6_K:       9              -             -
>         MIR_6_R:       3              -             -
>        MIR_6_RB:       4              -             -
>       MIR_6_RBP:       3              -             -
>    ZERO_HALF_FF:       -            152           205
>     ZERO_HALF_K:       -             73           120
>    ZERO_HALF_KL:       -             11            11
>     ZERO_HALF_R:       -            229           294
>    ZERO_HALF_RB:       -             63            96
>   ZERO_HALF_RBP:       -             47            94
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           0/5    100%    9.39e-01       0.10
>   'graph_cst_lns':           0/5    100%    9.39e-01       0.10
>   'graph_dec_lns':           0/5    100%    9.39e-01       0.10
>   'graph_var_lns':           1/5    100%    9.39e-01       0.10
>       'rins/rens':           0/4    100%    9.14e-01       0.10
>     'rnd_cst_lns':           0/5    100%    9.39e-01       0.10
>     'rnd_var_lns':           0/5    100%    9.39e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1       538         0              0          0              0          2'500
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0     3'082          2'266        408             12         25'393
>                          'ls_lin_restart':        1                  1   102'394         0              0          0         97'000        674'358
>                 'ls_lin_restart_compound':        1                  1         0    59'263         10'608     24'326            159        570'087
>                  'ls_lin_restart_perturb':        2                  2   137'725         0              0          0          3'724        986'198
>                              'ls_restart':        1                  1    34'219         0              0          0          2'562        161'295
>                        'ls_restart_decay':        1                  1    87'091         0              0          0            758        239'294
>               'ls_restart_decay_compound':        1                  1         0    56'884         17'842     19'521             82        513'109
>       'ls_restart_decay_compound_perturb':        1                  1         0    54'079         15'070     19'503             77        514'539
> 
> Solutions (5)       Num   Rank
>            'core':    1  [5,5]
>      'fj_restart':    1  [1,1]
>           'no_lp':    1  [3,3]
>   'quick_restart':    2  [2,4]
> 
> Objective bounds     Num
>        'bool_core':   31
>   'initial_domain':    1
>     'pseudo_costs':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     52       85       36
>    'fj solution hints':      0        0        0
>         'lp solutions':      8        3        7
>                 'pump':      4        3
> 
> Clauses shared    Num
>         'no_lp':    1
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 34
> best_bound: 34
> integers: 551
> booleans: 3190
> conflicts: 0
> branches: 56
> propagations: 3737
> integer_propagations: 5374
> restarts: 56
> lp_iterations: 0
> walltime: 0.911824
> usertime: 0.911824
> deterministic_time: 2.90018
> gap_integral: 1.00369
> solution_fingerprint: 0xc14698cfde08c7b4
> ```

In [ ]:
```python
_model = Model(instance06)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x637912b6fd74a00e)
> #Variables: 140 (#bools: 40 in objective) (140 primary variables)
>   - 40 Booleans in [0,1]
>   - 100 in [0,9]
> #kElement: 100
> #kLinear2: 90
> 
> Starting presolve at 0.00s
>   4.29e-05s  0.00e+00d  [DetectDominanceRelations] 
>   1.44e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=10 #num_dual_strengthening=1 
>   1.44e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   7.32e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   4.43e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'470 nodes and 3'550 arcs.
> [Symmetry] Symmetry computation done. time: 0.000461125 dtime: 0.0008805
>   1.44e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=370 
>   3.37e-03s  3.01e-03d  [Probe] #probed=1'120 #new_binary_clauses=3'375 
>   4.01e-06s  0.00e+00d  [MaxClique] 
>   2.00e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.70e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   6.82e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.60e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.29e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.74e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   9.40e-05s  0.00e+00d  [DetectDifferentVariables] #different=59 
>   4.58e-05s  1.23e-06d  [ProcessSetPPC] #relevant_constraints=100 
>   6.35e-06s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.08e-05s  6.14e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   2.03e-05s  1.72e-05d  [FindBigVerticalLinearOverlap] 
>   3.61e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.03e-05s  0.00e+00d  [MergeClauses] 
>   1.95e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.29e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.98e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.29e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.98e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   2.98e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'544 nodes and 4'030 arcs.
> [Symmetry] Symmetry computation done. time: 0.000450314 dtime: 0.00085589
> [SAT presolve] num removable Booleans: 0 / 448
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:408 literals:816 vars:446 one_side_vars:446 simple_definition:0 singleton_clauses:0
> [SAT presolve] [1.7323e-05s] clauses:408 literals:816 vars:446 one_side_vars:446 simple_definition:0 singleton_clauses:0
> [SAT presolve] [2.9546e-05s] clauses:408 literals:816 vars:446 one_side_vars:446 simple_definition:0 singleton_clauses:0
>   2.79e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.09e-03s  2.99e-03d  [Probe] #probed=1'120 #new_binary_clauses=3'350 
>   3.50e-04s  8.89e-04d  [MaxClique] Merged 408(816 literals) into 247(655 literals) at_most_ones. 
>   1.91e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.29e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.05e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.39e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.76e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.65e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   8.99e-05s  0.00e+00d  [DetectDifferentVariables] #different=59 
>   8.79e-05s  3.20e-06d  [ProcessSetPPC] #relevant_constraints=347 
>   8.92e-06s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   7.13e-05s  5.82e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   2.14e-05s  1.64e-05d  [FindBigVerticalLinearOverlap] 
>   4.33e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.05e-05s  0.00e+00d  [MergeClauses] 
>   1.92e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.27e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.87e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.26e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.54e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   2.85e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'382 nodes and 3'591 arcs.
> [Symmetry] Symmetry computation done. time: 0.000332551 dtime: 0.0007131
> [SAT presolve] num removable Booleans: 0 / 448
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:131 literals:262 vars:168 one_side_vars:168 simple_definition:0 singleton_clauses:0
> [SAT presolve] [9.719e-06s] clauses:131 literals:262 vars:168 one_side_vars:168 simple_definition:0 singleton_clauses:0
> [SAT presolve] [2.8935e-05s] clauses:131 literals:262 vars:168 one_side_vars:168 simple_definition:0 singleton_clauses:0
>   3.02e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.18e-03s  3.07e-03d  [Probe] #probed=1'120 #new_binary_clauses=3'531 
>   3.54e-04s  8.79e-04d  [MaxClique] 
>   1.92e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.30e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.99e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.32e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.59e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.64e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   8.78e-05s  0.00e+00d  [DetectDifferentVariables] #different=59 
>   8.67e-05s  3.20e-06d  [ProcessSetPPC] #relevant_constraints=347 
>   9.73e-06s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   7.25e-05s  5.81e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   2.13e-05s  1.64e-05d  [FindBigVerticalLinearOverlap] 
>   4.89e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.06e-05s  0.00e+00d  [MergeClauses] 
>   1.92e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.28e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.96e-05s  0.00e+00d  [ExpandObjective] #entries=1'300 #tight_variables=410 #tight_constraints=100 
> 
> Presolve summary:
>   - 2 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 22 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 342 times.
>   - rule 'affine: new relation' was applied 2 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'bool_and: x => x' was applied 2 times.
>   - rule 'deductions: 1234 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 2 times.
>   - rule 'element: expanded' was applied 100 times.
>   - rule 'linear: divide by GCD' was applied 90 times.
>   - rule 'linear: reduced variable domains' was applied 311 times.
>   - rule 'new_bool: integer encoding' was applied 410 times.
>   - rule 'presolve: 0 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 410 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x2ae814e7da526044)
> #Variables: 548 (#bools: 40 in objective) (448 primary variables)
>   - 448 Booleans in [0,1]
>   - 1 in [0,2]
>   - 9 in [0,3]
>   - 3 in [0,4]
>   - 1 in [1,3]
>   - 12 in [1,4]
>   - 2 in [1,5]
>   - 1 in [2,4]
>   - 8 in [2,5]
>   - 3 in [2,6]
>   - 1 in [3,5]
>   - 10 in [3,6]
>   - 3 in [3,7]
>   - 1 in [4,6]
>   - 12 in [4,7]
>   - 4 in [4,8]
>   - 3 in [5,7]
>   - 9 in [5,8]
>   - 5 in [5,9]
>   - 1 in [6,8]
>   - 10 in [6,9]
>   - 1 in [7,9]
> #kAtMostOne: 116 (#literals: 393)
> #kBoolAnd: 37 (#enforced: 37) (#literals: 168)
> #kExactlyOne: 100 (#literals: 410)
> #kLinear1: 820 (#enforced: 820)
> #kLinear2: 90
> [Symmetry] Graph for symmetry has 2'380 nodes and 3'591 arcs.
> [Symmetry] Symmetry computation done. time: 0.000333062 dtime: 0.00071298
> 
> Preloading model.
> #Bound   0.03s best:inf   next:[0,40]     initial_domain
> #Model   0.03s var:548/548 constraints:1163/1163
> 
> Starting search at 0.03s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.04s best:29    next:[0,28]     fj_restart(batch:1 lin{mvs:127 evals:476} #w_updates:0 #perturb:0)
> #2       0.04s best:28    next:[0,27]     no_lp
> #Bound   0.04s best:28    next:[1,27]     bool_core (num_cores=1 [size:4 mw:1 d:2] a=37 d=2 fixed=0/560 clauses=312)
> #3       0.04s best:27    next:[1,26]     default_lp
> #4       0.05s best:26    next:[1,25]     no_lp
> #Bound   0.05s best:26    next:[2,25]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=34 d=2 fixed=0/565 clauses=252)
> #Bound   0.05s best:26    next:[3,25]     bool_core (num_cores=3 [size:3 mw:1 d:2] a=32 d=2 fixed=0/569 clauses=256)
> #Bound   0.05s best:26    next:[4,25]     bool_core (num_cores=4 [size:3 mw:1 d:2] a=30 d=2 fixed=0/572 clauses=259)
> #Bound   0.05s best:26    next:[5,25]     bool_core (num_cores=5 [size:3 mw:1 d:3] a=28 d=3 fixed=0/575 clauses=262)
> #Bound   0.05s best:26    next:[6,25]     bool_core (num_cores=6 [size:3 mw:1 d:2] a=26 d=3 fixed=0/579 clauses=267)
> #5       0.05s best:25    next:[6,24]     no_lp
> #Bound   0.05s best:25    next:[7,24]     bool_core (num_cores=7 [size:4 mw:1 d:2] a=23 d=3 fixed=0/583 clauses=271)
> #Bound   0.05s best:25    next:[8,24]     bool_core (num_cores=8 [size:3 mw:1 d:2] a=21 d=3 fixed=0/587 clauses=275)
> #Bound   0.05s best:25    next:[9,24]     bool_core (num_cores=9 [size:3 mw:1 d:2] a=19 d=3 fixed=0/590 clauses=278)
> #Bound   0.05s best:25    next:[10,24]    bool_core (num_cores=10 [size:4 mw:1 d:2] a=16 d=3 fixed=0/594 clauses=282)
> #Bound   0.05s best:25    next:[11,24]    bool_core (num_cores=11 [size:3 mw:1 d:2] a=14 d=3 fixed=0/598 clauses=286)
> #Bound   0.06s best:25    next:[12,24]    bool_core (num_cores=12 [size:3 mw:1 d:3] a=12 d=3 fixed=0/601 clauses=293)
> #Bound   0.06s best:25    next:[13,24]    bool_core (num_cores=13 [size:2 mw:1 d:4] a=11 d=4 fixed=0/604 clauses=303)
> #Bound   0.06s best:25    next:[14,24]    bool_core (num_cores=14 [size:3 mw:1 d:3] a=9 d=4 fixed=0/609 clauses=313)
> #Bound   0.06s best:25    next:[15,24]    bool_core (num_cores=15 [size:2 mw:1 d:3] a=8 d=4 fixed=0/612 clauses=319)
> #Bound   0.06s best:25    next:[16,24]    bool_core (num_cores=16 [size:2 mw:1 d:4] a=7 d=4 fixed=0/615 clauses=323)
> #Bound   0.06s best:25    next:[17,24]    bool_core (num_cores=17 [size:2 mw:1 d:5] a=6 d=5 fixed=0/618 clauses=339)
> #Bound   0.06s best:25    next:[18,24]    bool_core (num_cores=18 [size:2 mw:1 d:5] a=5 d=5 fixed=0/624 clauses=383)
> #Bound   0.06s best:25    next:[19,24]    bool_core (num_cores=19 [size:2 mw:1 d:6] a=4 d=6 fixed=0/628 clauses=434)
> #Bound   0.06s best:25    next:[20,24]    bool_core (num_cores=20 [size:2 mw:1 d:3] a=3 d=6 fixed=0/633 clauses=461)
> #6       0.15s best:24    next:[]         core
> #Done    0.15s core
> #Bound   0.15s best:25    next:[24,24]    bool_core (num_cores=23 [size:1 mw:1] a=1 d=8 fixed=1/659 clauses=944) [skipped_logs=3]
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [119.50ms, 119.50ms] 119.50ms   0.00ns 119.50ms         1 [105.77ms, 105.77ms] 105.77ms   0.00ns 105.77ms
>            'default_lp':         1 [120.25ms, 120.25ms] 120.25ms   0.00ns 120.25ms         1 [ 80.04ms,  80.04ms]  80.04ms   0.00ns  80.04ms
>      'feasibility_pump':         4 [ 69.52us,   2.30ms] 757.14us 914.58us   3.03ms         3 [ 14.33us, 169.34us]  66.00us  73.07us 197.99us
>                    'fj':         1 [ 10.40ms,  10.40ms]  10.40ms   0.00ns  10.40ms         1 [  6.52ms,   6.52ms]   6.52ms   0.00ns   6.52ms
>                    'fj':         1 [806.76us, 806.76us] 806.76us   0.00ns 806.76us         1 [149.54us, 149.54us] 149.54us   0.00ns 149.54us
>             'fs_random':         1 [  6.27ms,   6.27ms]   6.27ms   0.00ns   6.27ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [  5.58ms,   5.58ms]   5.58ms   0.00ns   5.58ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         5 [  4.10ms,  15.32ms]   9.27ms   4.07ms  46.37ms         4 [ 34.00ns,   1.27ms] 394.59us 515.69us   1.58ms
>         'graph_cst_lns':         5 [  3.83ms,  11.99ms]   6.57ms   2.88ms  32.83ms         4 [ 91.00ns, 351.29us]  87.97us 152.03us 351.87us
>         'graph_dec_lns':         4 [  1.41ms,   3.87ms]   2.48ms 886.06us   9.91ms         4 [ 10.00ns,  28.00ns]  14.50ns   7.79ns  58.00ns
>         'graph_var_lns':         5 [  7.74ms,  18.73ms]  11.77ms   3.80ms  58.86ms         5 [102.11us, 941.83us] 296.64us 324.29us   1.48ms
>                    'ls':         1 [106.50ms, 106.50ms] 106.50ms   0.00ns 106.50ms         1 [ 83.30ms,  83.30ms]  83.30ms   0.00ns  83.30ms
>                'ls_lin':         1 [106.48ms, 106.48ms] 106.48ms   0.00ns 106.48ms         1 [ 73.80ms,  73.80ms]  73.80ms   0.00ns  73.80ms
>                'max_lp':         1 [120.14ms, 120.14ms] 120.14ms   0.00ns 120.14ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [120.45ms, 120.45ms] 120.45ms   0.00ns 120.45ms         1 [117.58ms, 117.58ms] 117.58ms   0.00ns 117.58ms
>          'pseudo_costs':         1 [119.84ms, 119.84ms] 119.84ms   0.00ns 119.84ms         1 [ 35.80ms,  35.80ms]  35.80ms   0.00ns  35.80ms
>         'quick_restart':         1 [119.90ms, 119.90ms] 119.90ms   0.00ns 119.90ms         1 [ 64.57ms,  64.57ms]  64.57ms   0.00ns  64.57ms
>   'quick_restart_no_lp':         1 [120.50ms, 120.50ms] 120.50ms   0.00ns 120.50ms         1 [115.89ms, 115.89ms] 115.89ms   0.00ns 115.89ms
>         'reduced_costs':         1 [119.90ms, 119.90ms] 119.90ms   0.00ns 119.90ms         1 [ 37.43ms,  37.43ms]  37.43ms   0.00ns  37.43ms
>             'rins/rens':         3 [  2.85ms,   8.64ms]   5.20ms   2.49ms  15.61ms         3 [  1.14us, 275.43us]  94.02us 128.29us 282.05us
>           'rnd_cst_lns':         5 [  2.40ms,  15.34ms]   7.32ms   4.58ms  36.58ms         5 [ 10.00ns, 596.89us] 130.64us 234.13us 653.18us
>           'rnd_var_lns':         5 [  2.18ms,  11.00ms]   5.66ms   3.14ms  28.30ms         5 [ 10.00ns,  84.98us]  20.18us  32.92us 100.91us
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':    665      1'482    19'006     4'831     635'533        219'759
>            'default_lp':    558      1'245    25'143     3'163     288'565        168'205
>             'fs_random':    558          0       452       452       7'349          6'206
>       'fs_random_no_lp':    558          0       498       498       8'016          6'650
>                'max_lp':    558          0     1'116     1'116      18'022         26'504
>                 'no_lp':    558      1'803    27'558     3'054     343'461        209'235
>          'pseudo_costs':    558         59     3'657     1'954      47'569         65'802
>         'quick_restart':    558      1'274    15'433     3'040     254'363        137'175
>   'quick_restart_no_lp':    558      2'127    18'167     3'343     364'999        182'811
>         'reduced_costs':    558         50     3'650     1'952      44'846         62'411
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         1'091       3'522       9'094             0        12     3'091       9'310         0        603        3'645      156
>            'default_lp':           900       2'647      31'399             0         8     1'678      20'796         0        297        6'296      655
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':           883       3'531      45'577             0        32     1'508      22'785         0        318        8'188      426
>          'pseudo_costs':            55         450       1'254             0         0       569       1'334         0         69          276        0
>         'quick_restart':           724       2'056      31'433             0        24     1'361       8'392         0        136        1'621      189
>   'quick_restart_no_lp':         1'082       3'104      54'891             0        49     1'263       6'397         0        128        1'551       66
>         'reduced_costs':            42         167       1'012             0         0       568       1'334         0         66          261       15
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         10         428         17    1'572        0        0
>       'fs_random':         10           0          0        0        0        0
>          'max_lp':          1         547        576        2        0        0
>    'pseudo_costs':          1       2'405        905       20      147        0
>   'quick_restart':         10         932         17    3'668        0        0
>   'reduced_costs':          1       2'081      1'129       22      108        0
> 
> Lp dimension         Final dimension of first component
>      'default_lp':        0 rows, 10 columns, 0 entries
>       'fs_random':        0 rows, 10 columns, 0 entries
>          'max_lp':  842 rows, 548 columns, 2675 entries
>    'pseudo_costs':  650 rows, 548 columns, 1824 entries
>   'quick_restart':        0 rows, 10 columns, 0 entries
>   'reduced_costs':  800 rows, 548 columns, 2202 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>       'fs_random':          0            0       0         0      0           0
>          'max_lp':          0            0       2         0  2'578           0
>    'pseudo_costs':          0            0     160         0  1'150           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0     123         0  1'165           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':          113        0        0       0          0      0             0        17/17
>       'fs_random':           96        0        0       0          0      0             0          0/0
>          'max_lp':        1'413       70        0       0          0     25             6    576/2'057
>    'pseudo_costs':        1'742        5        0       0          0      2            20    905/1'918
>   'quick_restart':          113        0        0       0          0      0             0        17/19
>   'reduced_costs':        1'966        6        0       0          0      2            14  1'129/2'468
> 
> Lp Cut            default_lp  max_lp  quick_restart  reduced_costs  pseudo_costs
>           CG_FF:           -       -              -             35            26
>            CG_K:           -       -              -              6            15
>           CG_KL:           -       -              -              1             -
>            CG_R:           -       -              -              1             7
>           CG_RB:           -       -              -             20            27
>          CG_RBP:           -       -              -              2             7
>          Clique:           -       7              -             23            22
>              IB:          17       -             17            587           445
>        MIR_1_FF:           -      95              -             54            57
>         MIR_1_K:           -      64              -             60            37
>        MIR_1_KL:           -       8              -              4             5
>        MIR_1_RB:           -      36              -             10             6
>       MIR_1_RBP:           -      10              -              2             1
>        MIR_2_FF:           -      97              -             46            38
>         MIR_2_K:           -      46              -             43            19
>        MIR_2_KL:           -       5              -              6             5
>        MIR_2_RB:           -      34              -             16             7
>       MIR_2_RBP:           -       9              -              2             1
>        MIR_3_FF:           -      28              -             15            11
>         MIR_3_K:           -      21              -             13             8
>        MIR_3_KL:           -       3              -              3             3
>         MIR_3_R:           -       4              -              -             1
>        MIR_3_RB:           -      12              -              4             -
>       MIR_3_RBP:           -       5              -              -             -
>        MIR_4_FF:           -      26              -              9             3
>         MIR_4_K:           -      10              -              1             3
>        MIR_4_KL:           -       -              -              -             1
>         MIR_4_R:           -       4              -              -             -
>        MIR_4_RB:           -       6              -              -             -
>       MIR_4_RBP:           -       2              -              -             -
>        MIR_5_FF:           -      16              -              5             4
>         MIR_5_K:           -       6              -              1             1
>        MIR_5_KL:           -       2              -              -             -
>         MIR_5_R:           -       4              -              -             -
>        MIR_5_RB:           -       4              -              1             2
>       MIR_5_RBP:           -       2              -              -             -
>        MIR_6_FF:           -       7              -              2             1
>         MIR_6_K:           -       -              -              1             -
>         MIR_6_R:           -       2              -              -             -
>        MIR_6_RB:           -       1              -              -             -
>    ZERO_HALF_FF:           -       -              -             45            54
>     ZERO_HALF_K:           -       -              -             28            26
>    ZERO_HALF_KL:           -       -              -              1             -
>     ZERO_HALF_R:           -       -              -             68            55
>    ZERO_HALF_RB:           -       -              -             10             5
>   ZERO_HALF_RBP:           -       -              -              4             2
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           0/4    100%    9.14e-01       0.10
>   'graph_cst_lns':           0/4    100%    9.14e-01       0.10
>   'graph_dec_lns':           0/4    100%    9.14e-01       0.10
>   'graph_var_lns':           0/5    100%    9.39e-01       0.10
>       'rins/rens':           0/3    100%    8.76e-01       0.10
>     'rnd_cst_lns':           0/5    100%    9.39e-01       0.10
>     'rnd_var_lns':           0/5    100%    9.39e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1       127         0              0          0              0            476
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0     4'527          1'019      1'754             31         31'664
>                  'ls_lin_restart_perturb':        1                  1    65'994         0              0          0         74'449        583'854
>                        'ls_restart_decay':        1                  1    75'732         0              0          0          2'682        184'061
> 
> Solutions (6)    Num   Rank
>         'core':    1  [6,6]
>   'default_lp':    1  [3,3]
>   'fj_restart':    1  [1,1]
>        'no_lp':    3  [2,5]
> 
> Objective bounds     Num
>        'bool_core':   23
>   'initial_domain':    1
>           'max_lp':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     45       66       27
>    'fj solution hints':      0        0        0
>         'lp solutions':      0        0        0
>                 'pump':      3        3
> 
> Clauses shared    Num
>         'no_lp':    1
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 24
> best_bound: 24
> integers: 141
> booleans: 558
> conflicts: 0
> branches: 498
> propagations: 8016
> integer_propagations: 6650
> restarts: 498
> lp_iterations: 0
> walltime: 0.155341
> usertime: 0.155341
> deterministic_time: 0.736584
> gap_integral: 0.100726
> solution_fingerprint: 0x57aa58fd14d63df5
> ```

In [ ]:
```python
_model = Model(instance07)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x9a73ef9c5835379)
> #Variables: 2'750 (#bools: 250 in objective) (2'750 primary variables)
>   - 250 Booleans in [0,1]
>   - 2'500 in [0,49]
> #kElement: 2'500
> #kLinear2: 2'450
> 
> Starting presolve at 0.04s
>   1.50e-03s  0.00e+00d  [DetectDominanceRelations] 
>   4.31e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=50 #num_dual_strengthening=1 
>   3.00e-05s  0.00e+00d  [ExtractEncodingFromLinear] 
>   9.78e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   5.16e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 242'150 nodes and 378'550 arcs.
> [Symmetry] Symmetry computation done. time: 0.0558583 dtime: 0.104319
>   4.29e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=46'179 
>   5.37e-01s  1.00e+00d *[Probe] #probed=14'942 #new_binary_clauses=1'424'275 
>   1.07e-03s  0.00e+00d  [MaxClique] 
>   2.15e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.19e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   7.27e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.75e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.58e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.57e-03s  1.47e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=2'450 
>   5.03e-03s  0.00e+00d  [DetectDifferentVariables] #different=1'572 
>   4.28e-03s  1.39e-04d  [ProcessSetPPC] #relevant_constraints=2'500 
>   1.43e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.83e-02s  2.39e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   5.95e-03s  1.70e-03d  [FindBigVerticalLinearOverlap] 
>   1.33e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.47e-03s  0.00e+00d  [MergeClauses] 
>   2.16e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.59e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.16e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.58e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.16e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   5.18e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 242'529 nodes and 425'287 arcs.
> [Symmetry] Symmetry computation done. time: 0.0462703 dtime: 0.100702
> [SAT presolve] num removable Booleans: 0 / 46600
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:46379 literals:92758 vars:46579 one_side_vars:46579 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00238105s] clauses:46379 literals:92758 vars:46579 one_side_vars:46579 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00286337s] clauses:46379 literals:92758 vars:46579 one_side_vars:46579 simple_definition:0 singleton_clauses:0
>   4.78e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.00e-01s  1.00e+00d *[Probe] #probed=14'904 #new_binary_clauses=1'422'690 
>   1.72e-01s  1.00e+00d *[MaxClique] Merged 46'379(92'758 literals) into 44'528(90'907 literals) at_most_ones. 
>   2.63e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.64e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.41e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.67e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   6.02e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.26e-03s  1.47e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=2'450 
>   6.23e-03s  0.00e+00d  [DetectDifferentVariables] #different=1'572 
>   1.75e-02s  4.15e-04d  [ProcessSetPPC] #relevant_constraints=47'028 
>   3.19e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.82e-02s  1.45e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   6.56e-03s  1.69e-03d  [FindBigVerticalLinearOverlap] 
>   1.59e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.12e-03s  0.00e+00d  [MergeClauses] 
>   2.62e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.56e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.63e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.54e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.44e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   4.11e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 240'678 nodes and 421'087 arcs.
> [Symmetry] Symmetry computation done. time: 0.046333 dtime: 0.0967801
> [SAT presolve] num removable Booleans: 0 / 46600
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:44030 literals:88060 vars:44230 one_side_vars:44230 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00300709s] clauses:44030 literals:88060 vars:44230 one_side_vars:44230 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00356s] clauses:44030 literals:88060 vars:44230 one_side_vars:44230 simple_definition:0 singleton_clauses:0
>   4.29e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.07e-01s  1.00e+00d *[Probe] #probed=14'680 #new_binary_clauses=1'432'717 
>   1.77e-01s  1.00e+00d *[MaxClique] Merged 44'528(90'907 literals) into 44'230(90'609 literals) at_most_ones. 
>   2.77e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.65e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.36e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   6.06e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   5.51e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.51e-03s  1.47e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=2'450 
>   6.46e-03s  0.00e+00d  [DetectDifferentVariables] #different=1'572 
>   1.79e-02s  4.14e-04d  [ProcessSetPPC] #relevant_constraints=46'730 
>   3.41e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.82e-02s  1.46e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   6.46e-03s  1.69e-03d  [FindBigVerticalLinearOverlap] 
>   1.79e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.44e-03s  0.00e+00d  [MergeClauses] 
>   2.72e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.57e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.21e-02s  0.00e+00d  [ExpandObjective] #entries=825'800 #tight_variables=46'400 #tight_constraints=2'500 
> 
> Presolve summary:
>   - 21 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 121 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 1'800 times.
>   - rule 'affine: new relation' was applied 21 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'bool_and: x => x' was applied 21 times.
>   - rule 'deductions: 139242 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 21 times.
>   - rule 'element: expanded' was applied 2'500 times.
>   - rule 'exactly_one: simplified objective' was applied 1 time.
>   - rule 'linear: divide by GCD' was applied 2'450 times.
>   - rule 'linear: reduced variable domains' was applied 39'957 times.
>   - rule 'new_bool: integer encoding' was applied 46'400 times.
>   - rule 'objective: variable not used elsewhere' was applied 29 times.
>   - rule 'presolve: 29 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 46'400 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xfc33aa7009289cff)
> #Variables: 49'100 (#bools: 200 in objective) (46'600 primary variables)
>   - 46'600 Booleans in [0,1]
>   - 323 different domains in [0,49] with a largest complexity of 1.
> #kAtMostOne: 552 (#literals: 3'253)
> #kBoolAnd: 200 (#enforced: 200) (#literals: 43'878)
> #kExactlyOne: 2'500 (#literals: 46'400)
> #kLinear1: 92'800 (#enforced: 92'800)
> #kLinear2: 2'450
> [Symmetry] Graph for symmetry has 240'330 nodes and 420'437 arcs.
> [Symmetry] Symmetry computation done. time: 0.0529326 dtime: 0.0961812
> 
> Preloading model.
> #Bound   4.76s best:inf   next:[1,201]    initial_domain
> #Model   4.80s var:49100/49100 constraints:98502/98502
> 
> Starting search at 4.82s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       5.03s best:144   next:[1,143]    fj_restart(batch:1 lin{mvs:2'643 evals:44'861} #w_updates:0 #perturb:0)
> #2       5.68s best:143   next:[1,142]    graph_arc_lns (d=5.00e-01 s=15 t=0.10 p=0.00 stall=0 h=base)
> #Bound   7.48s best:143   next:[2,142]    bool_core (num_cores=1 [size:14 mw:1 d:4] a=187 d=4 fixed=0/85512 clauses=43'912)
> #Bound   8.11s best:143   next:[9,142]    max_lp
> #3       8.34s best:142   next:[9,141]    no_lp
> #Bound   8.43s best:142   next:[10,141]   max_lp
> #4       8.65s best:141   next:[10,140]   no_lp
> #5       8.80s best:140   next:[10,139]   no_lp
> #6       9.12s best:139   next:[10,138]   quick_restart_no_lp
> #Bound   9.26s best:139   next:[17,138]   max_lp
> #7       9.42s best:138   next:[17,137]   quick_restart_no_lp
> #Bound   9.60s best:138   next:[18,137]   max_lp
> #8      11.08s best:137   next:[18,136]   quick_restart
> #9      23.56s best:136   next:[18,135]   reduced_costs
> #Bound  28.44s best:136   next:[19,135]   bool_core (num_cores=18 [size:2 mw:1 d:5] a=25 d=7 fixed=0/85863 clauses=44'827)
> #Bound  29.49s best:136   next:[20,135]   bool_core (num_cores=19 [size:2 mw:1 d:6] a=24 d=7 fixed=0/85871 clauses=45'008)
> #Bound  30.41s best:136   next:[21,135]   bool_core (num_cores=20 [size:2 mw:1 d:5] a=23 d=7 fixed=0/85879 clauses=45'124)
> #Bound  31.41s best:136   next:[22,135]   bool_core (num_cores=21 [size:5 mw:1 d:5] a=19 d=7 fixed=0/85889 clauses=45'246)
> #Bound  33.91s best:136   next:[23,135]   bool_core (num_cores=22 [size:2 mw:1 d:8] a=18 d=8 fixed=0/85899 clauses=45'568)
> #Bound  38.67s best:136   next:[24,135]   bool_core (num_cores=22 [cover] a=18 d=8 fixed=0/85915 clauses=46'349)
> #Bound  41.42s best:136   next:[25,135]   bool_core (num_cores=23 [size:2 mw:1 d:5] a=17 d=8 fixed=1/85926 clauses=46'843)
> #Bound  42.00s best:136   next:[26,135]   bool_core (num_cores=24 [size:2 mw:1 d:7] a=16 d=8 fixed=1/85933 clauses=46'924)
> #Bound  42.33s best:136   next:[27,135]   bool_core (num_cores=24 [cover] a=16 d=8 fixed=1/85945 clauses=47'020)
> #Bound  44.51s best:136   next:[28,135]   bool_core (num_cores=24 [cover] a=16 d=8 fixed=2/85957 clauses=47'641)
> #Bound  47.27s best:136   next:[29,135]   bool_core (num_cores=24 [cover] a=16 d=8 fixed=3/85966 clauses=48'378)
> #Bound  51.87s best:136   next:[30,135]   bool_core (num_cores=25 [size:2 mw:1 d:6] a=15 d=8 fixed=4/85974 clauses=49'506)
> #Bound  52.15s best:136   next:[31,135]   bool_core (num_cores=25 [cover] a=15 d=8 fixed=4/85988 clauses=49'592)
> #Bound  53.22s best:136   next:[32,135]   bool_core (num_cores=25 [cover] a=15 d=8 fixed=5/85999 clauses=49'866)
> #Bound  54.01s best:136   next:[33,135]   bool_core (num_cores=25 [cover] a=15 d=8 fixed=6/86007 clauses=50'184)
> #Bound  54.74s best:136   next:[34,135]   bool_core (num_cores=25 [cover] a=15 d=8 fixed=7/86014 clauses=50'518)
> #Bound  57.05s best:136   next:[35,135]   bool_core (num_cores=26 [size:3 mw:1 d:5] a=13 d=8 fixed=8/86021 clauses=51'090)
> #Bound  58.27s best:136   next:[36,135]   bool_core (num_cores=27 [size:2 mw:1 d:6] a=12 d=8 fixed=8/86030 clauses=51'330)
> #Bound  58.47s best:136   next:[37,135]   bool_core (num_cores=27 [cover] a=12 d=8 fixed=8/86045 clauses=51'411)
> #Bound  59.06s best:136   next:[38,135]   bool_core (num_cores=27 [cover] a=12 d=8 fixed=9/86056 clauses=51'581)
> #Bound  59.65s best:136   next:[39,135]   bool_core (num_cores=27 [cover] a=12 d=8 fixed=10/86064 clauses=51'809)
> #Bound  65.01s best:136   next:[40,135]   bool_core (num_cores=28 [size:1 mw:1] a=12 d=8 fixed=11/86072 clauses=53'096)
> #Bound  70.07s best:136   next:[41,135]   bool_core (num_cores=29 [size:3 mw:1 d:5] a=10 d=8 fixed=12/86080 clauses=54'319)
> #Bound  74.78s best:136   next:[42,135]   bool_core (num_cores=30 [size:2 mw:1 d:9] a=9 d=9 fixed=12/86088 clauses=51'788)
> #Bound  75.65s best:136   next:[43,135]   bool_core (num_cores=30 [cover] a=9 d=9 fixed=12/86108 clauses=51'973)
> #Bound  78.87s best:136   next:[44,135]   bool_core (num_cores=30 [cover] a=9 d=9 fixed=13/86122 clauses=52'498)
> #Bound  83.88s best:136   next:[45,135]   bool_core (num_cores=30 [cover] a=9 d=9 fixed=14/86135 clauses=53'343)
> #Bound  88.74s best:136   next:[46,135]   bool_core (num_cores=30 [cover] a=9 d=9 fixed=15/86146 clauses=54'234)
> #Bound  94.46s best:136   next:[47,135]   bool_core (num_cores=31 [size:2 mw:1 d:6] a=8 d=9 fixed=16/86157 clauses=55'485)
> #Bound  95.46s best:136   next:[48,135]   bool_core (num_cores=31 [cover] a=8 d=9 fixed=16/86173 clauses=55'722)
> #Bound  96.51s best:136   next:[49,135]   bool_core (num_cores=31 [cover] a=8 d=9 fixed=17/86182 clauses=56'018)
> #Bound 105.13s best:136   next:[50,135]   bool_core (num_cores=32 [size:1 mw:1] a=8 d=9 fixed=18/86191 clauses=58'211)
> #Bound 111.08s best:136   next:[51,135]   bool_core (num_cores=33 [size:2 mw:1 d:7] a=7 d=9 fixed=19/86197 clauses=54'817)
> #Bound 112.63s best:136   next:[52,135]   bool_core (num_cores=34 [size:1 mw:1] a=7 d=9 fixed=20/86203 clauses=55'192)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  35.35s,   35.35s]   35.35s   0.00ns   35.35s
>            'default_lp':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  25.22s,   25.22s]   25.22s   0.00ns   25.22s
>      'feasibility_pump':       484 [ 79.04us, 365.65ms]   2.66ms  16.67ms    1.29s       476 [341.99us,   5.70ms] 356.95us 258.19us 169.91ms
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         1 [206.00ms, 206.00ms] 206.00ms   0.00ns 206.00ms         1 [ 11.22ms,  11.22ms]  11.22ms   0.00ns  11.22ms
>             'fs_random':         1 [251.26ms, 251.26ms] 251.26ms   0.00ns 251.26ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [212.84ms, 212.84ms] 212.84ms   0.00ns 212.84ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        34 [471.58ms,    2.52s]    1.47s 499.35ms   50.11s        34 [ 34.39us, 101.64ms]  52.68ms  43.07ms    1.79s
>         'graph_cst_lns':        30 [417.80ms,    2.54s]    1.79s 542.27ms   53.63s        30 [  7.67us, 101.61ms]  54.43ms  41.03ms    1.63s
>         'graph_dec_lns':        38 [164.23ms,    2.87s]    1.31s 770.22ms   49.86s        38 [ 10.00ns, 101.27ms]  36.28ms  43.37ms    1.38s
>         'graph_var_lns':        37 [445.72ms,    3.21s]    1.54s 719.40ms   57.07s        37 [  3.85us, 101.13ms]  52.63ms  45.05ms    1.95s
>                    'ls':       134 [142.94ms, 573.35ms] 364.10ms 112.77ms   48.79s       134 [100.00ms, 100.24ms] 100.03ms  47.84us   13.40s
>                'ls_lin':       172 [100.28ms, 505.86ms] 281.36ms 102.61ms   48.39s       172 [100.00ms, 101.30ms] 100.16ms 346.37us   17.23s
>                'max_lp':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  38.96s,   38.96s]   38.96s   0.00ns   38.96s
>                 'no_lp':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  26.67s,   26.67s]   26.67s   0.00ns   26.67s
>          'pseudo_costs':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  17.94s,   17.94s]   17.94s   0.00ns   17.94s
>         'quick_restart':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  24.10s,   24.10s]   24.10s   0.00ns   24.10s
>   'quick_restart_no_lp':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  33.05s,   33.05s]   33.05s   0.00ns   33.05s
>         'reduced_costs':         1 [   1.92m,    1.92m]    1.92m   0.00ns    1.92m         1 [  15.73s,   15.73s]   15.73s   0.00ns   15.73s
>             'rins/rens':        33 [ 20.96ms,    2.84s]    1.47s 687.81ms   48.36s        32 [  1.08ms, 101.40ms]  62.00ms  39.50ms    1.98s
>           'rnd_cst_lns':        38 [448.91ms,    1.97s]    1.40s 338.88ms   53.33s        34 [385.00ns, 100.50ms]  47.63ms  44.42ms    1.62s
>           'rnd_var_lns':        31 [219.38ms,    2.61s]    1.58s 588.80ms   49.10s        31 [  2.92us, 101.90ms]  50.59ms  43.59ms    1.57s
> 
> Search stats               Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  86'208     20'286   613'000    32'177  232'733'988     66'242'234
>            'default_lp':  85'500     36'998   150'335    32'042  112'740'578     47'712'525
>             'fs_random':  85'500          0         0         0            0              0
>       'fs_random_no_lp':  85'500          0         0         0            0              0
>                'max_lp':  85'500        612   113'954    32'191   35'113'811     26'421'465
>                 'no_lp':  85'500     53'747   116'611    23'160  129'372'889     65'701'124
>          'pseudo_costs':  85'500      8'192    63'676    20'876   36'508'758     30'007'094
>         'quick_restart':  85'500      8'849   376'089    32'822  112'448'655     45'184'570
>   'quick_restart_no_lp':  85'500     13'889   626'659    33'273  158'508'038     66'548'797
>         'reduced_costs':  85'500      4'880    63'400    20'940   31'538'317     30'917'254
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        16'928     230'049     420'328        77'785        75    17'099      34'198         0          0            0        0
>            'default_lp':        26'219     217'465   8'573'072     4'765'655        30    17'593      35'186         0          0            0        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':           437       2'834     121'896             0         0    17'768      35'536         0          0            0        0
>                 'no_lp':        40'390     264'075  10'894'209     8'104'948        24     8'756      17'512         0          0            0        0
>          'pseudo_costs':         7'157     103'848   2'450'587             0         3     6'458      12'916         0          0            0        0
>         'quick_restart':         5'525      45'131   2'852'367             0        53    17'647      35'294         0          0            0        0
>   'quick_restart_no_lp':         8'507      74'168   4'263'791     1'657'869       127    17'654      35'308         0          0            0        0
>         'reduced_costs':         2'591      77'075     867'503             0         1     6'473      12'946         0          0            0        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         50           0          0  315'146        0        0
>          'max_lp':          1      43'370          0        0    2'944        0
>    'pseudo_costs':          1     161'134     19'599      502   14'660        0
>   'quick_restart':         50           0          0  426'197        0        0
>   'reduced_costs':          1     131'934    129'049      265   10'466        0
> 
> Lp dimension               Final dimension of first component
>      'default_lp':              0 rows, 50 columns, 0 entries
>          'max_lp':  59056 rows, 49100 columns, 249824 entries
>    'pseudo_costs':   10072 rows, 49100 columns, 49141 entries
>   'quick_restart':              0 rows, 50 columns, 0 entries
>   'reduced_costs':    8519 rows, 49100 columns, 72453 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow      Bad  BadScaling
>      'default_lp':          0            0       0         0        0           0
>          'max_lp':          0            0   2'944         0        0           0
>    'pseudo_costs':          0            0  13'825         0   21'592           0
>   'quick_restart':          0            0       0         0        0           0
>   'reduced_costs':          0            0   8'308         0  348'349           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened        Cuts/Call
>      'default_lp':        2'450        0        0       0          0      0             0              0/0
>          'max_lp':       59'056        0        0       0          0      0             0              0/0
>    'pseudo_costs':       68'655        5        0       0          0      6         3'565    19'599/30'349
>   'quick_restart':        2'450        0        0       0          0      0             0              0/0
>   'reduced_costs':      127'105      113        0       0          0  1'440        93'783  129'049/599'173
> 
> Lp Cut            reduced_costs  pseudo_costs
>           CG_FF:            193            95
>            CG_K:            101            12
>           CG_KL:             16             2
>            CG_R:            151            20
>           CG_RB:            294           105
>          CG_RBP:             67            10
>          Clique:            250           115
>              IB:          5'659        11'679
>        MIR_1_FF:          2'525           326
>         MIR_1_K:          2'408           163
>        MIR_1_KL:          1'244           106
>         MIR_1_R:            960             5
>        MIR_1_RB:          3'075           225
>       MIR_1_RBP:            645            10
>        MIR_2_FF:          3'622           420
>         MIR_2_K:          5'433           254
>        MIR_2_KL:          1'545           285
>         MIR_2_R:            509             -
>        MIR_2_RB:          6'034           467
>       MIR_2_RBP:          2'845            13
>        MIR_3_FF:          5'870           316
>         MIR_3_K:          6'573           203
>        MIR_3_KL:          1'823           321
>         MIR_3_R:          2'797            11
>        MIR_3_RB:          6'026           539
>       MIR_3_RBP:          2'747             4
>        MIR_4_FF:          5'843           161
>         MIR_4_K:          4'281            95
>        MIR_4_KL:          1'346           146
>         MIR_4_R:          3'549             1
>        MIR_4_RB:          2'923           251
>       MIR_4_RBP:          1'321             6
>        MIR_5_FF:          3'880            99
>         MIR_5_K:          2'435            45
>        MIR_5_KL:            719            78
>         MIR_5_R:          2'271             2
>        MIR_5_RB:          1'346           126
>       MIR_5_RBP:            606             4
>        MIR_6_FF:          1'992            72
>         MIR_6_K:          1'161            23
>        MIR_6_KL:            338            39
>         MIR_6_R:          1'073             1
>        MIR_6_RB:            602            76
>       MIR_6_RBP:            263             2
>    ZERO_HALF_FF:          5'342           820
>     ZERO_HALF_K:          5'575           301
>    ZERO_HALF_KL:            471            51
>     ZERO_HALF_R:         10'663           906
>    ZERO_HALF_RB:          5'328           470
>   ZERO_HALF_RBP:          2'309           118
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          1/34     59%    9.29e-01       0.10
>   'graph_cst_lns':          0/30     63%    9.70e-01       0.10
>   'graph_dec_lns':          0/38     71%    9.97e-01       0.10
>   'graph_var_lns':          0/37     59%    9.60e-01       0.10
>       'rins/rens':          0/32     56%    8.52e-01       0.10
>     'rnd_cst_lns':          0/34     62%    9.62e-01       0.10
>     'rnd_var_lns':          0/31     58%    9.60e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1      2'643         0              0          0              0         44'861
>                          'ls_lin_restart':       47                 17  2'248'202         0              0          0        280'552     14'825'555
>                 'ls_lin_restart_compound':       14                  9          0    55'088            776     27'151            117      7'187'127
>         'ls_lin_restart_compound_perturb':       17                 12          0    77'780          3'574     37'098            185      8'763'830
>                    'ls_lin_restart_decay':       19                 14    961'568         0              0          0          1'912      5'937'619
>           'ls_lin_restart_decay_compound':       26                 16          0   158'153         30'644     63'731            181     13'487'170
>   'ls_lin_restart_decay_compound_perturb':       12                  8          0    69'892         13'027     28'424             84      6'193'719
>            'ls_lin_restart_decay_perturb':       26                 16  1'301'622         0              0          0          2'260      8'269'886
>                  'ls_lin_restart_perturb':       11                  6    573'123         0              0          0         60'461      3'542'465
>                              'ls_restart':       11                  8    255'009         0              0          0         11'459      2'009'582
>                     'ls_restart_compound':       23                 12          0   108'115          7'909     50'100            271     11'614'084
>             'ls_restart_compound_perturb':       17                 12          0    65'094            892     32'100            115      8'703'735
>                        'ls_restart_decay':       12                  7    399'703         0              0          0          1'206      1'928'988
>               'ls_restart_decay_compound':       21                 10          0   155'088         46'718     54'164            142     10'366'728
>       'ls_restart_decay_compound_perturb':       18                 13          0    88'230         14'536     36'838            152      9'053'025
>                'ls_restart_decay_perturb':       20                  9    672'740         0              0          0          1'760      3'237'240
>                      'ls_restart_perturb':       12                 11    272'368         0              0          0         13'526      2'169'312
> 
> Solutions (9)             Num   Rank
>            'fj_restart':    1  [1,1]
>         'graph_arc_lns':    1  [2,2]
>                 'no_lp':    3  [3,5]
>         'quick_restart':    1  [8,8]
>   'quick_restart_no_lp':    2  [6,7]
>         'reduced_costs':    1  [9,9]
> 
> Objective bounds     Num
>        'bool_core':   35
>   'initial_domain':    1
>           'max_lp':    4
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    326      687      251
>    'fj solution hints':      0        0        0
>         'lp solutions':    243       13      231
>                 'pump':    482       20
> 
> Clauses shared               Num
>                  'core':  11'027
>                 'no_lp':  11'729
>   'quick_restart_no_lp':   5'166
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 136
> best_bound: 52
> integers: 2700
> booleans: 85500
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.236
> usertime: 120.236
> deterministic_time: 264.813
> gap_integral: 1158.42
> solution_fingerprint: 0x20c966c85e985007
> ```

In [ ]:
```python
_model = Model(instance08)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x83e688bb8355a5e0)
> #Variables: 290 (#bools: 190 in objective) (290 primary variables)
>   - 190 Booleans in [0,1]
>   - 100 in [0,9]
> #kElement: 100
> #kLinear2: 90
> 
> Starting presolve at 0.00s
>   6.23e-05s  0.00e+00d  [DetectDominanceRelations] 
>   2.89e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=10 #num_dual_strengthening=1 
>   1.43e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   9.71e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   5.09e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 3'120 nodes and 4'350 arcs.
> [Symmetry] Symmetry computation done. time: 0.00057964 dtime: 0.00104613
>   1.70e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=354 
>   4.87e-03s  5.23e-03d  [Probe] #probed=1'752 #new_binary_clauses=5'400 
>   4.22e-06s  0.00e+00d  [MaxClique] 
>   2.78e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.56e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   7.03e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.80e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.53e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.77e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   9.73e-05s  0.00e+00d  [DetectDifferentVariables] #different=49 
>   4.62e-05s  1.53e-06d  [ProcessSetPPC] #relevant_constraints=100 
>   7.20e-06s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.98e-05s  9.10e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   3.67e-05s  2.09e-05d  [FindBigVerticalLinearOverlap] 
>   4.27e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   8.12e-06s  0.00e+00d  [MergeClauses] 
>   2.70e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.66e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.66e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.64e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.35e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   4.89e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 3'318 nodes and 4'982 arcs.
> [Symmetry] Symmetry computation done. time: 0.00050116 dtime: 0.00100072
> [SAT presolve] num removable Booleans: 0 / 628
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:472 literals:944 vars:590 one_side_vars:590 simple_definition:0 singleton_clauses:0
> [SAT presolve] [2.0358e-05s] clauses:472 literals:944 vars:590 one_side_vars:590 simple_definition:0 singleton_clauses:0
> [SAT presolve] [4.3933e-05s] clauses:472 literals:944 vars:590 one_side_vars:590 simple_definition:0 singleton_clauses:0
>   4.93e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.65e-03s  5.11e-03d  [Probe] #probed=1'752 #new_binary_clauses=5'105 
>   4.57e-04s  1.18e-03d  [MaxClique] Merged 472(944 literals) into 421(893 literals) at_most_ones. 
>   2.87e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.68e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.46e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.20e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   4.07e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.75e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   9.37e-05s  0.00e+00d  [DetectDifferentVariables] #different=49 
>   1.11e-04s  4.24e-06d  [ProcessSetPPC] #relevant_constraints=521 
>   1.42e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.21e-04s  8.07e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   3.75e-05s  2.07e-05d  [FindBigVerticalLinearOverlap] 
>   5.02e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.39e-05s  0.00e+00d  [MergeClauses] 
>   2.79e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.64e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.74e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.61e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.81e-05s  0.00e+00d  [DetectDuplicateColumns] 
>   4.39e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 3'266 nodes and 4'830 arcs.
> [Symmetry] Symmetry computation done. time: 0.000451236 dtime: 0.00091078
> [SAT presolve] num removable Booleans: 0 / 627
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:373 literals:746 vars:491 one_side_vars:491 simple_definition:0 singleton_clauses:0
> [SAT presolve] [1.572e-05s] clauses:373 literals:746 vars:491 one_side_vars:491 simple_definition:0 singleton_clauses:0
> [SAT presolve] [4.2571e-05s] clauses:373 literals:746 vars:491 one_side_vars:491 simple_definition:0 singleton_clauses:0
>   4.56e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.71e-03s  5.13e-03d  [Probe] #probed=1'752 #new_binary_clauses=5'126 
>   4.52e-04s  1.19e-03d  [MaxClique] 
>   2.82e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.67e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.19e-05s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.34e-05s  0.00e+00d  [DetectDuplicateConstraints] 
>   4.20e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.92e-05s  5.40e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=90 
>   9.38e-05s  0.00e+00d  [DetectDifferentVariables] #different=49 
>   1.11e-04s  4.24e-06d  [ProcessSetPPC] #relevant_constraints=521 
>   1.56e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.15e-04s  8.15e-05d  [FindBigAtMostOneAndLinearOverlap] 
>   3.73e-05s  2.07e-05d  [FindBigVerticalLinearOverlap] 
>   7.13e-06s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.46e-05s  0.00e+00d  [MergeClauses] 
>   2.81e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.65e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   9.26e-05s  0.00e+00d  [ExpandObjective] #entries=2'200 #tight_variables=510 #tight_constraints=100 
> 
> Presolve summary:
>   - 38 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 58 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 1'057 times.
>   - rule 'affine: new relation' was applied 38 times.
>   - rule 'at_most_one: removed literals' was applied 1 time.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'bool_and: x => x' was applied 38 times.
>   - rule 'deductions: 1606 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 38 times.
>   - rule 'dual: fix variable' was applied 10 times.
>   - rule 'element: expanded' was applied 100 times.
>   - rule 'exactly_one: simplified objective' was applied 1 time.
>   - rule 'exactly_one: singleton' was applied 1 time.
>   - rule 'linear: divide by GCD' was applied 90 times.
>   - rule 'linear: reduced variable domains' was applied 285 times.
>   - rule 'new_bool: integer encoding' was applied 510 times.
>   - rule 'objective: variable not used elsewhere' was applied 34 times.
>   - rule 'presolve: 34 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 510 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x5dbe1933951615fb)
> #Variables: 727 (#bools: 151 in objective) (627 primary variables)
>   - 627 Booleans in [0,1]
>   - 5 in [0,3]
>   - 4 in [0,4]
>   - 4 in [0,5]
>   - 3 in [0,6]
>   - 6 in [1,4]
>   - 4 in [1,5]
>   - 8 in [1,6]
>   - 1 in [1,7]
>   - 9 in [2,5]
>   - 2 in [2,6]
>   - 7 in [2,7]
>   - 2 in [2,8]
>   - 5 in [3,6]
>   - 2 in [3,7]
>   - 5 in [3,8]
>   - 4 in [3,9]
>   - 5 in [4,7]
>   - 5 in [4,8]
>   - 6 in [4,9]
>   - 6 in [5,8]
>   - 3 in [5,9]
>   - 4 in [6,9]
> #kAtMostOne: 48 (#literals: 146)
> #kBoolAnd: 118 (#enforced: 118) (#literals: 491)
> #kExactlyOne: 100 (#literals: 510)
> #kLinear1: 1'020 (#enforced: 1'020)
> #kLinear2: 90
> [Symmetry] Graph for symmetry has 3'193 nodes and 4'830 arcs.
> [Symmetry] Symmetry computation done. time: 0.000450274 dtime: 0.0009064
> 
> Preloading model.
> #Bound   0.04s best:inf   next:[1,151]    initial_domain
> #Model   0.04s var:727/727 constraints:1376/1376
> 
> Starting search at 0.04s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.05s best:61    next:[1,60]     fj_restart(batch:1 lin{mvs:149 evals:595} #w_updates:0 #perturb:0)
> #2       0.06s best:60    next:[1,59]     no_lp
> #Bound   0.06s best:60    next:[2,59]     bool_core (num_cores=1 [size:5 mw:1 amo:1 lit:2 d:3] a=147 d=3 fixed=0/840 clauses=413)
> #3       0.06s best:59    next:[2,58]     graph_cst_lns (d=5.00e-01 s=17 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: graph_arc_lns (d=5.0...]
> #4       0.06s best:58    next:[2,57]     rnd_var_lns (d=7.07e-01 s=21 t=0.10 p=1.00 stall=1 h=base)
> #5       0.07s best:57    next:[2,56]     graph_var_lns (d=5.00e-01 s=15 t=0.10 p=0.00 stall=0 h=base)
> #6       0.07s best:56    next:[2,55]     graph_var_lns (d=5.00e-01 s=15 t=0.10 p=0.00 stall=0 h=base) [combined with: graph_cst_lns (d=5.0...]
> #7       0.07s best:55    next:[2,54]     no_lp
> #Bound   0.07s best:55    next:[3,54]     bool_core (num_cores=2 [size:6 mw:1 d:3] a=142 d=3 fixed=0/847 clauses=374)
> #Bound   0.07s best:55    next:[4,54]     bool_core (num_cores=3 [size:5 mw:1 amo:1 lit:3 d:2] a=138 d=3 fixed=0/854 clauses=381)
> #8       0.07s best:54    next:[4,53]     no_lp
> #Bound   0.08s best:54    next:[5,53]     bool_core (num_cores=4 [size:7 mw:1 amo:1 lit:2 d:3] a=132 d=3 fixed=0/861 clauses=388)
> #Bound   0.08s best:54    next:[37,53]    max_lp
> #9       0.08s best:53    next:[37,52]    graph_cst_lns (d=7.07e-01 s=25 t=0.10 p=1.00 stall=0 h=base)
> #10      0.09s best:52    next:[37,51]    no_lp
> #11      0.10s best:50    next:[37,49]    graph_arc_lns (d=7.07e-01 s=24 t=0.10 p=1.00 stall=0 h=base)
> #12      0.10s best:49    next:[37,48]    quick_restart_no_lp
> #Bound   0.15s best:49    next:[38,48]    bool_core (num_cores=37 [size:7 mw:1 d:6] a=27 d=6 fixed=0/1057 clauses=649)
> #Bound   0.16s best:49    next:[39,48]    bool_core (num_cores=38 [size:5 mw:1 amo:1 lit:2 d:7] a=23 d=7 fixed=0/1080 clauses=743)
> #Bound   0.16s best:49    next:[40,48]    bool_core (num_cores=39 [size:3 mw:1 d:8] a=21 d=8 fixed=0/1103 clauses=949)
> #Bound   0.17s best:49    next:[41,48]    bool_core (num_cores=40 [size:2 mw:1 d:9] a=20 d=9 fixed=0/1125 clauses=1'238)
> #Bound   0.19s best:49    next:[42,48]    bool_core (num_cores=40 [cover] a=20 d=9 fixed=0/1149 clauses=1'804)
> #13      0.25s best:48    next:[42,47]    ls_restart_compound_perturb(batch:1 lin{mvs:0 evals:41'829} gen{mvs:7'731 evals:0} comp{mvs:391 btracks:3'670} #w_updates:117 #perturb:0)
> #Bound   0.36s best:48    next:[43,47]    bool_core (num_cores=41 [size:4 mw:1 d:10] a=17 d=10 fixed=1/1170 clauses=3'335)
> #Bound   0.48s best:48    next:[44,47]    bool_core (num_cores=42 [size:2 mw:1 d:11] a=16 d=11 fixed=1/1191 clauses=6'229)
> #Bound   0.86s best:48    next:[45,47]    bool_core (num_cores=43 [size:3 mw:1 d:12] a=14 d=12 fixed=1/1213 clauses=13'987)
> #Bound   1.86s best:48    next:[46,47]    bool_core (num_cores=44 [size:6 mw:1 d:13] a=9 d=13 fixed=1/1242 clauses=15'726)
> #14      1.92s best:46    next:[]         core
> #Done    1.92s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [   3.06s,    3.06s]    3.06s   0.00ns    3.06s
>            'default_lp':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [877.58ms, 877.58ms] 877.58ms   0.00ns 877.58ms
>      'feasibility_pump':        12 [ 98.79us,   2.86ms] 419.18us 783.31us   5.03ms        11 [ 20.56us, 517.41us]  65.72us 142.84us 722.97us
>                    'fj':         1 [  1.12ms,   1.12ms]   1.12ms   0.00ns   1.12ms         1 [174.17us, 174.17us] 174.17us   0.00ns 174.17us
>                    'fj':         1 [  2.50ms,   2.50ms]   2.50ms   0.00ns   2.50ms         1 [  1.22ms,   1.22ms]   1.22ms   0.00ns   1.22ms
>             'fs_random':         1 [  5.57ms,   5.57ms]   5.57ms   0.00ns   5.57ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [  7.78ms,   7.78ms]   7.78ms   0.00ns   7.78ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        12 [  4.55ms, 121.80ms]  64.41ms  49.45ms 772.98ms        12 [ 21.35us, 100.12ms]  48.67ms  45.70ms 584.04ms
>         'graph_cst_lns':        12 [  4.60ms, 130.22ms]  51.76ms  52.80ms 621.08ms        12 [  2.58us, 100.08ms]  34.48ms  46.40ms 413.81ms
>         'graph_dec_lns':        12 [  2.23ms, 253.34ms]  69.65ms  77.79ms 835.81ms        12 [ 10.00ns, 100.01ms]  37.23ms  43.90ms 446.81ms
>         'graph_var_lns':        12 [ 12.01ms, 126.61ms]  65.86ms  49.27ms 790.38ms        12 [  1.38ms, 100.07ms]  48.97ms  44.31ms 587.69ms
>                    'ls':        12 [ 13.24ms, 133.04ms] 102.09ms  41.31ms    1.23s        12 [ 10.26ms, 100.01ms]  80.81ms  32.48ms 969.72ms
>                'ls_lin':         9 [ 25.02ms, 170.93ms] 133.66ms  40.54ms    1.20s         9 [ 19.97ms, 100.00ms]  91.11ms  25.15ms 819.98ms
>                'max_lp':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [567.47ms, 567.47ms] 567.47ms   0.00ns 567.47ms
>                 'no_lp':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [   2.05s,    2.05s]    2.05s   0.00ns    2.05s
>          'pseudo_costs':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [   1.12s,    1.12s]    1.12s   0.00ns    1.12s
>         'quick_restart':         1 [   1.88s,    1.88s]    1.88s   0.00ns    1.88s         1 [   1.04s,    1.04s]    1.04s   0.00ns    1.04s
>   'quick_restart_no_lp':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [   2.12s,    2.12s]    2.12s   0.00ns    2.12s
>         'reduced_costs':         1 [   1.87s,    1.87s]    1.87s   0.00ns    1.87s         1 [   1.26s,    1.26s]    1.26s   0.00ns    1.26s
>             'rins/rens':        12 [502.83us, 136.09ms]  59.25ms  56.34ms 710.97ms        11 [ 10.00ns, 100.02ms]  46.70ms  45.20ms 513.67ms
>           'rnd_cst_lns':        12 [  4.11ms, 179.22ms]  63.65ms  57.54ms 763.86ms        12 [ 55.00ns, 100.06ms]  35.62ms  40.80ms 427.45ms
>           'rnd_var_lns':        12 [  2.48ms, 129.62ms]  44.36ms  49.79ms 532.34ms        12 [ 10.00ns, 100.02ms]  32.61ms  45.33ms 391.28ms
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  1'274     25'250   137'206    15'171   9'080'214      1'303'243
>            'default_lp':    837     21'654    40'329     5'231   1'701'421      1'638'384
>             'fs_random':    837          0       294       294       2'327          2'588
>       'fs_random_no_lp':    837          0     1'156     1'156      21'141         13'248
>                'max_lp':    837         17     1'709     1'674      34'387         41'193
>                 'no_lp':    837     38'039    57'816     4'084   3'161'216      2'620'465
>          'pseudo_costs':    837        163    12'046     5'180     164'576        200'053
>         'quick_restart':    837     10'650    93'332    10'475   1'568'566      1'325'010
>   'quick_restart_no_lp':    837     18'726   155'155    13'576   2'587'476      2'204'718
>         'reduced_costs':    837        133    13'466     5'231     168'681        208'256
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        22'705     163'929     358'662        55'782       119    11'500      65'216         0      3'355       39'776      858
>            'default_lp':        18'280      50'131   1'109'440       644'726        14     2'174       5'108         0         73          347        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':            17         268         618             0         0         0           0         0          0            0        0
>                 'no_lp':        27'801     127'898   2'195'169     1'237'735        68     1'500       3'587         0         63          299        0
>          'pseudo_costs':           163       3'904       8'460             0         0     2'162       5'040         0         78          377        0
>         'quick_restart':         8'862      37'030     515'544       230'908        71     4'673      10'737         0         83          402        0
>   'quick_restart_no_lp':        14'893      56'702     905'432       229'432       106     6'116      13'630         0         89          439        0
>         'reduced_costs':           133       2'828       4'561             0         0     2'215       6'330         0         76          520        5
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         10       5'742        104   51'654        0        0
>       'fs_random':         10           0          0        0        0        0
>          'max_lp':          1       7'657      3'122       58       35        0
>    'pseudo_costs':          1      22'372      2'697      453      203        0
>   'quick_restart':         10      24'782         94   44'495        0        0
>   'reduced_costs':          1      22'482      2'822      375      172        0
> 
> Lp dimension          Final dimension of first component
>      'default_lp':         2 rows, 12 columns, 4 entries
>       'fs_random':         0 rows, 12 columns, 0 entries
>          'max_lp':  1521 rows, 727 columns, 6387 entries
>    'pseudo_costs':  1128 rows, 727 columns, 4333 entries
>   'quick_restart':        9 rows, 12 columns, 18 entries
>   'reduced_costs':  1264 rows, 727 columns, 4487 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0   8'722         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0      93         0  22'970           0
>    'pseudo_costs':          0            0     649         0   6'113           0
>   'quick_restart':          0            0     433         0       0           0
>   'reduced_costs':          0            0     533         0   6'862           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':          282        0        0       0          0      0             0       104/348
>       'fs_random':          178        0        0       0          0      0             0           0/0
>          'max_lp':        4'133      245        0       0          0    184            64  3'122/11'412
>    'pseudo_costs':        3'708       82        0       0          0     16            48   2'697/6'177
>   'quick_restart':          272        0        0       0          0      0             0        94/392
>   'reduced_costs':        3'833       77        0       0          0     22           141   2'822/6'590
> 
> Lp Cut            default_lp  max_lp  reduced_costs  pseudo_costs  quick_restart
>           CG_FF:           -       -             32            27              -
>            CG_K:           -       -             11            16              -
>           CG_KL:           -       -              1             3              -
>            CG_R:           -       1             24             4              -
>           CG_RB:           -       1             38            31              -
>          CG_RBP:           -       2             12            16              -
>          Clique:           -      48             33            28              -
>              IB:         104       -            887           893             94
>        MIR_1_FF:           -     189            154           141              -
>         MIR_1_K:           -     220            184           151              -
>        MIR_1_KL:           -      36             20            36              -
>         MIR_1_R:           -       -              1             -              -
>        MIR_1_RB:           -     204            111           101              -
>       MIR_1_RBP:           -      33             20            20              -
>        MIR_2_FF:           -     277            139           172              -
>         MIR_2_K:           -     222            140           132              -
>        MIR_2_KL:           -      38             24            26              -
>         MIR_2_R:           -       2              2             2              -
>        MIR_2_RB:           -     293            102            85              -
>       MIR_2_RBP:           -      52             19            24              -
>        MIR_3_FF:           -     132             68            62              -
>         MIR_3_K:           -      76             48            29              -
>        MIR_3_KL:           -      15              8             8              -
>         MIR_3_R:           -      23              9            14              -
>        MIR_3_RB:           -      91             38            16              -
>       MIR_3_RBP:           -      13              5             5              -
>        MIR_4_FF:           -     103             45            42              -
>         MIR_4_K:           -      51              8             8              -
>        MIR_4_KL:           -       5              4             3              -
>         MIR_4_R:           -      69             16            21              -
>        MIR_4_RB:           -      43             17            12              -
>       MIR_4_RBP:           -       9              3             3              -
>        MIR_5_FF:           -      69             29            29              -
>         MIR_5_K:           -      26             12             8              -
>        MIR_5_KL:           -       1              2             1              -
>         MIR_5_R:           -      55             20            12              -
>        MIR_5_RB:           -      29              8             4              -
>       MIR_5_RBP:           -       3              2             2              -
>        MIR_6_FF:           -      49             11            17              -
>         MIR_6_K:           -      15              7             5              -
>        MIR_6_KL:           -       1              -             4              -
>         MIR_6_R:           -      32              3            12              -
>        MIR_6_RB:           -      17              4             2              -
>       MIR_6_RBP:           -       1              -             -              -
>    ZERO_HALF_FF:           -       9             71            84              -
>     ZERO_HALF_K:           -       5             47            36              -
>    ZERO_HALF_KL:           -       -              -             2              -
>     ZERO_HALF_R:           -     559            295           291              -
>    ZERO_HALF_RB:           -       2             52            28              -
>   ZERO_HALF_RBP:           -       1             36            29              -
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          2/12     58%    7.95e-01       0.10
>   'graph_cst_lns':          2/12     67%    9.10e-01       0.10
>   'graph_dec_lns':          0/12     67%    9.24e-01       0.10
>   'graph_var_lns':          1/12     58%    8.02e-01       0.10
>       'rins/rens':          0/11     64%    8.27e-01       0.10
>     'rnd_cst_lns':          0/12     67%    9.17e-01       0.10
>     'rnd_var_lns':          1/12     75%    9.45e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1       149         0              0          0              0            595
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0     1'091            659        216              9          7'281
>                          'ls_lin_restart':        1                  1    12'957         0              0          0            821         77'041
>         'ls_lin_restart_compound_perturb':        1                  1         0    61'073          5'762     27'654            371        421'562
>                    'ls_lin_restart_decay':        1                  1    82'174         0              0          0          1'533        323'938
>           'ls_lin_restart_decay_compound':        1                  1         0    56'509         18'498     19'003            177        473'031
>   'ls_lin_restart_decay_compound_perturb':        2                  2         0   228'760         25'253    101'751          4'133      1'673'994
>                  'ls_lin_restart_perturb':        3                  3   254'789         0              0          0        253'190      2'001'203
>                              'ls_restart':        2                  2   108'678         0              0          0         26'115        428'409
>                     'ls_restart_compound':        3                  3         0   126'614          5'778     60'418          1'146        898'403
>             'ls_restart_compound_perturb':        3                  3         0   108'368          7'024     50'669            815        750'320
>                        'ls_restart_decay':        1                  1     5'976         0              0          0            374         15'225
>               'ls_restart_decay_compound':        1                  1         0    46'868         12'406     17'231            135        352'447
>                'ls_restart_decay_perturb':        2                  2   126'432         0              0          0          3'200        313'593
> 
> Solutions (14)                    Num     Rank
>                          'core':    1  [14,14]
>                    'fj_restart':    1    [1,1]
>                 'graph_arc_lns':    1  [11,11]
>                 'graph_cst_lns':    2    [3,9]
>                 'graph_var_lns':    2    [5,6]
>   'ls_restart_compound_perturb':    1  [13,13]
>                         'no_lp':    4   [2,10]
>           'quick_restart_no_lp':    1  [12,12]
>                   'rnd_var_lns':    1    [4,4]
> 
> Objective bounds     Num
>        'bool_core':   13
>   'initial_domain':    1
>           'max_lp':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    130      200       73
>    'fj solution hints':      0        0        0
>         'lp solutions':      6        8        6
>                 'pump':     11        4
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 46
> best_bound: 46
> integers: 264
> booleans: 837
> conflicts: 0
> branches: 1156
> propagations: 21141
> integer_propagations: 13248
> restarts: 1156
> lp_iterations: 0
> walltime: 1.92961
> usertime: 1.92961
> deterministic_time: 17.264
> gap_integral: 8.78196
> solution_fingerprint: 0x5a4e94a337c43a9d
> ```

In [ ]:
```python
_model = Model(instance09)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x47233af4258049d6)
> #Variables: 3'500 (#bools: 1'000 in objective) (3'500 primary variables)
>   - 1'000 Booleans in [0,1]
>   - 2'500 in [0,49]
> #kElement: 2'500
> #kLinear2: 2'450
> 
> Starting presolve at 0.14s
>   1.99e-03s  0.00e+00d  [DetectDominanceRelations] 
>   9.48e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=50 #num_dual_strengthening=1 
>   4.36e-05s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.07e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   7.29e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 303'150 nodes and 474'950 arcs.
> [Symmetry] Symmetry computation done. time: 0.0683245 dtime: 0.128181
>   7.88e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=57'466 
>   6.03e-01s  1.00e+00d *[Probe] #probed=12'954 #new_binary_clauses=1'461'965 
>   1.17e-03s  0.00e+00d  [MaxClique] 
>   2.78e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.03e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   1.05e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   7.27e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   4.75e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.98e-03s  1.47e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=2'450 
>   6.01e-03s  0.00e+00d  [DetectDifferentVariables] #different=1'331 
>   5.31e-03s  1.75e-04d  [ProcessSetPPC] #relevant_constraints=2'500 
>   1.78e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.77e-02s  3.71e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   8.74e-03s  2.12e-03d  [FindBigVerticalLinearOverlap] 
>   1.74e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.85e-03s  0.00e+00d  [MergeClauses] 
>   2.79e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.03e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.79e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.03e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.17e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   7.31e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 305'070 nodes and 535'288 arcs.
> [Symmetry] Symmetry computation done. time: 0.0650657 dtime: 0.114815
> [SAT presolve] num removable Booleans: 0 / 59418
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:58434 literals:116868 vars:59402 one_side_vars:59402 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00314053s] clauses:58434 literals:116868 vars:59402 one_side_vars:59402 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0039019s] clauses:58434 literals:116868 vars:59402 one_side_vars:59402 simple_definition:0 singleton_clauses:0
>   6.52e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.35e-01s  1.00e+00d *[Probe] #probed=12'952 #new_binary_clauses=1'461'473 
>   1.51e-01s  1.00e+00d *[MaxClique] Merged 58'434(116'868 literals) into 57'179(115'614 literals) at_most_ones. 
>   4.36e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.21e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.91e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   7.69e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   6.35e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.67e-03s  1.47e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=2'450 
>   7.07e-03s  0.00e+00d  [DetectDifferentVariables] #different=1'331 
>   2.80e-02s  5.26e-04d  [ProcessSetPPC] #relevant_constraints=59'679 #num_inclusions=1 
>   3.63e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.58e-02s  2.16e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   9.05e-03s  2.12e-03d  [FindBigVerticalLinearOverlap] 
>   2.04e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.95e-03s  0.00e+00d  [MergeClauses] 
>   4.29e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.09e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.30e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.07e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.43e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   5.86e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 303'814 nodes and 532'097 arcs.
> [Symmetry] Symmetry computation done. time: 0.074939 dtime: 0.113476
> [SAT presolve] num removable Booleans: 0 / 59418
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:56499 literals:112998 vars:57467 one_side_vars:57467 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00477436s] clauses:56499 literals:112998 vars:57467 one_side_vars:57467 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00562761s] clauses:56499 literals:112998 vars:57467 one_side_vars:57467 simple_definition:0 singleton_clauses:0
>   5.36e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.27e-01s  1.00e+00d *[Probe] #probed=12'936 #new_binary_clauses=1'461'674 
>   1.50e-01s  1.00e+00d *[MaxClique] Merged 57'178(115'612 literals) into 57'039(115'474 literals) at_most_ones. 
>   4.34e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.19e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.13e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.00e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   6.67e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.80e-03s  1.47e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=2'450 
>   7.59e-03s  0.00e+00d  [DetectDifferentVariables] #different=1'331 
>   2.45e-02s  5.26e-04d  [ProcessSetPPC] #relevant_constraints=59'539 #num_inclusions=1 
>   3.62e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.66e-02s  2.16e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   9.37e-03s  2.12e-03d  [FindBigVerticalLinearOverlap] 
>   2.33e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   3.21e-03s  0.00e+00d  [MergeClauses] 
>   4.36e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.10e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.64e-02s  0.00e+00d  [ExpandObjective] #entries=1'318'300 #tight_variables=58'450 #tight_constraints=2'500 
> 
> Presolve summary:
>   - 16 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 116 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 8'712 times.
>   - rule 'affine: new relation' was applied 16 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'bool_and: x => x' was applied 16 times.
>   - rule 'deductions: 175382 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 16 times.
>   - rule 'dual: fix variable' was applied 2 times.
>   - rule 'element: expanded' was applied 2'500 times.
>   - rule 'linear: divide by GCD' was applied 2'450 times.
>   - rule 'linear: reduced variable domains' was applied 34'142 times.
>   - rule 'new_bool: integer encoding' was applied 58'450 times.
>   - rule 'objective: variable not used elsewhere' was applied 16 times.
>   - rule 'presolve: 16 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: removed dominated constraints' was applied 2 times.
>   - rule 'variables: add encoding constraint' was applied 58'450 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x4800a64d28d1bd2d)
> #Variables: 61'918 (#bools: 984 in objective) (59'418 primary variables)
>   - 59'418 Booleans in [0,1]
>   - 243 different domains in [0,49] with a largest complexity of 1.
> #kAtMostOne: 735 (#literals: 2'866)
> #kBoolAnd: 968 (#enforced: 968) (#literals: 57'271)
> #kExactlyOne: 2'500 (#literals: 58'450)
> #kLinear1: 116'900 (#enforced: 116'900)
> #kLinear2: 2'450
> [Symmetry] Graph for symmetry has 303'642 nodes and 531'761 arcs.
> [Symmetry] Symmetry computation done. time: 0.0644271 dtime: 0.113485
> 
> Preloading model.
> #Bound   6.38s best:inf   next:[0,984]    initial_domain
> #Model   6.43s var:61918/61918 constraints:123553/123553
> 
> Starting search at 6.46s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       6.69s best:536   next:[0,535]    fj_restart(batch:1 lin{mvs:3'030 evals:55'735} #w_updates:0 #perturb:0)
> #2       7.41s best:535   next:[0,534]    rnd_cst_lns (d=5.00e-01 s=13 t=0.10 p=0.00 stall=0 h=base)
> #3       7.49s best:534   next:[0,533]    ls_lin_restart_perturb(batch:1 lin{mvs:602 evals:6'066} #w_updates:427 #perturb:0)
> #4       7.75s best:533   next:[0,532]    ls_restart(batch:1 lin{mvs:559 evals:5'609} #w_updates:526 #perturb:0)
> #5       7.78s best:530   next:[0,529]    ls_restart(batch:1 lin{mvs:5 evals:587} #w_updates:0 #perturb:0)
> #6       8.31s best:529   next:[0,528]    ls_lin_restart_decay_compound(batch:1 lin{mvs:0 evals:13'783} gen{mvs:172 evals:0} comp{mvs:12 btracks:80} #w_updates:3 #perturb:0)
> #7       8.79s best:527   next:[0,526]    default_lp
> #8       8.96s best:526   next:[0,525]    ls_restart_perturb(batch:1 lin{mvs:1'238 evals:12'588} #w_updates:558 #perturb:0)
> #9       9.00s best:517   next:[0,516]    rins_pump_lns (d=5.00e-01 s=32 t=0.10 p=0.00 stall=0 h=base)
> #10      9.14s best:516   next:[0,515]    ls_lin_restart_decay(batch:1 lin{mvs:9 evals:847} #w_updates:6 #perturb:0)
> #11      9.30s best:515   next:[0,514]    ls_lin_restart(batch:1 lin{mvs:220 evals:3'021} #w_updates:132 #perturb:0)
> #12      9.33s best:514   next:[0,513]    ls_lin_restart_perturb(batch:1 lin{mvs:290 evals:3'502} #w_updates:176 #perturb:0)
> #13      9.35s best:513   next:[0,512]    ls_lin_restart_compound(batch:1 lin{mvs:0 evals:608} gen{mvs:17 evals:0} comp{mvs:3 btracks:7} #w_updates:0 #perturb:0)
> #14      9.55s best:512   next:[0,511]    ls_lin_restart_compound(batch:1 lin{mvs:0 evals:51'358} gen{mvs:878 evals:0} comp{mvs:36 btracks:421} #w_updates:14 #perturb:0)
> #Bound   9.62s best:512   next:[1,511]    bool_core (num_cores=1 [size:20 mw:1 d:5] a=965 d=5 fixed=0/110386 clauses=55'968)
> #Bound   9.70s best:512   next:[3,511]    max_lp
> #15     10.02s best:511   next:[3,510]    graph_arc_lns (d=4.62e-01 s=58 t=0.10 p=0.50 stall=1 h=base)
> #16     10.04s best:510   next:[3,509]    graph_arc_lns (d=4.62e-01 s=58 t=0.10 p=0.50 stall=1 h=base) [combined with: ls_lin_restart_compo...]
> #Bound  10.14s best:510   next:[8,509]    max_lp
> #17     10.28s best:509   next:[8,508]    ls_lin_restart(batch:1 lin{mvs:205 evals:1'956} #w_updates:163 #perturb:0)
> #18     10.40s best:487   next:[8,486]    quick_restart_no_lp
> #Bound  10.40s best:487   next:[11,486]   max_lp
> #19     10.43s best:479   next:[11,478]   no_lp
> #20     10.51s best:478   next:[11,477]   ls_restart_decay_compound_perturb(batch:1 lin{mvs:0 evals:16'901} gen{mvs:165 evals:0} comp{mvs:15 btracks:75} #w_updates:6 #perturb:0)
> #21     10.69s best:476   next:[11,475]   no_lp
> #Bound  10.79s best:476   next:[15,475]   max_lp
> #22     10.82s best:475   next:[15,474]   no_lp
> #23     10.97s best:472   next:[15,471]   no_lp
> #24     11.13s best:471   next:[15,470]   no_lp
> #25     11.44s best:467   next:[15,466]   no_lp
> #26     11.67s best:466   next:[15,465]   quick_restart_no_lp
> #27     11.72s best:465   next:[15,464]   quick_restart_no_lp
> #28     14.97s best:464   next:[15,463]   graph_dec_lns (d=9.76e-01 s=118 t=0.10 p=1.00 stall=8 h=base)
> #29     17.39s best:463   next:[15,462]   graph_dec_lns (d=9.68e-01 s=152 t=0.10 p=0.89 stall=0 h=base) [hint]
> #30     17.82s best:462   next:[15,461]   ls_lin_restart_compound(batch:1 lin{mvs:0 evals:51'693} gen{mvs:1'034 evals:0} comp{mvs:34 btracks:500} #w_updates:15 #perturb:0)
> #31     19.05s best:461   next:[15,460]   quick_restart
> #32     19.09s best:459   next:[15,458]   ls_lin_restart(batch:1 lin{mvs:2 evals:461} #w_updates:0 #perturb:0)
> #33     19.48s best:458   next:[15,457]   graph_arc_lns (d=3.26e-01 s=180 t=0.10 p=0.44 stall=6 h=base) [hint]
> #34     21.81s best:457   next:[15,456]   graph_dec_lns (d=9.81e-01 s=200 t=0.10 p=0.91 stall=1 h=base)
> #35     22.06s best:456   next:[15,455]   graph_dec_lns (d=9.81e-01 s=201 t=0.10 p=0.91 stall=1 h=base)
> #36     25.08s best:455   next:[15,454]   quick_restart_no_lp
> #37     25.86s best:454   next:[15,453]   quick_restart
> #38     28.50s best:453   next:[15,452]   ls_restart_decay_compound(batch:1 lin{mvs:0 evals:72'782} gen{mvs:1'098 evals:0} comp{mvs:72 btracks:513} #w_updates:27 #perturb:0)
> #39     32.44s best:452   next:[15,451]   quick_restart_no_lp
> #40     34.48s best:451   next:[15,450]   rnd_cst_lns (d=7.40e-01 s=340 t=0.10 p=0.56 stall=1 h=base)
> #41     34.85s best:450   next:[15,449]   ls_restart(batch:1 lin{mvs:18 evals:644} #w_updates:16 #perturb:0)
> #42     34.92s best:449   next:[15,448]   ls_lin_restart_compound(batch:1 lin{mvs:0 evals:90'766} gen{mvs:2'104 evals:0} comp{mvs:54 btracks:1'025} #w_updates:25 #perturb:0) [combined with: ls_restart(batch:1 l...]
> #43     35.20s best:448   next:[15,447]   ls_restart_compound_perturb(batch:1 lin{mvs:0 evals:3'108} gen{mvs:41 evals:0} comp{mvs:5 btracks:18} #w_updates:1 #perturb:0)
> #44     36.51s best:447   next:[15,446]   quick_restart
> #Bound  39.68s best:447   next:[16,446]   bool_core (num_cores=16 [size:22 mw:1 d:5] a=661 d=5 fixed=0/110974 clauses=56'578)
> #Bound  41.66s best:447   next:[17,446]   bool_core (num_cores=17 [size:20 mw:1 d:5] a=642 d=5 fixed=0/111013 clauses=56'617)
> #Bound  43.89s best:447   next:[18,446]   bool_core (num_cores=18 [size:20 mw:1 d:5] a=623 d=5 fixed=0/111050 clauses=56'656)
> #Bound  45.94s best:447   next:[19,446]   bool_core (num_cores=19 [size:21 mw:1 d:5] a=603 d=5 fixed=0/111088 clauses=56'696)
> #45     47.62s best:446   next:[19,445]   quick_restart_no_lp
> #Bound  48.22s best:446   next:[20,445]   bool_core (num_cores=20 [size:22 mw:1 d:5] a=582 d=5 fixed=0/111128 clauses=56'740)
> #Bound  50.27s best:446   next:[21,445]   bool_core (num_cores=21 [size:20 mw:1 d:5] a=563 d=5 fixed=0/111167 clauses=56'779)
> #46     52.17s best:445   next:[21,444]   graph_dec_lns (d=9.88e-01 s=532 t=0.10 p=0.77 stall=9 h=base)
> #Bound  52.75s best:445   next:[22,444]   bool_core (num_cores=22 [size:24 mw:1 d:5] a=540 d=5 fixed=0/111208 clauses=56'822)
> #Bound  54.80s best:445   next:[23,444]   bool_core (num_cores=23 [size:20 mw:1 d:5] a=521 d=5 fixed=0/111249 clauses=56'864)
> #Bound  56.98s best:445   next:[24,444]   bool_core (num_cores=24 [size:21 mw:1 d:5] a=501 d=5 fixed=0/111287 clauses=56'906)
> #Bound  59.06s best:445   next:[25,444]   bool_core (num_cores=25 [size:21 mw:1 d:5] a=481 d=5 fixed=0/111326 clauses=56'947)
> #47     60.69s best:444   next:[25,443]   quick_restart_no_lp
> #Bound  61.24s best:444   next:[26,443]   bool_core (num_cores=26 [size:22 mw:1 d:5] a=460 d=5 fixed=0/111366 clauses=56'994)
> #Bound  63.34s best:444   next:[27,443]   bool_core (num_cores=27 [size:20 mw:1 d:5] a=441 d=5 fixed=0/111405 clauses=57'035)
> #48     64.75s best:443   next:[27,442]   quick_restart_no_lp
> #Bound  65.34s best:443   next:[28,442]   bool_core (num_cores=28 [size:20 mw:1 d:5] a=422 d=5 fixed=0/111442 clauses=57'073)
> #Bound  67.44s best:443   next:[29,442]   bool_core (num_cores=29 [size:20 mw:1 d:5] a=403 d=5 fixed=0/111479 clauses=57'111)
> #Bound  69.56s best:443   next:[30,442]   bool_core (num_cores=30 [size:20 mw:1 d:5] a=384 d=5 fixed=0/111516 clauses=57'150)
> #Bound  71.59s best:443   next:[31,442]   bool_core (num_cores=31 [size:20 mw:1 d:5] a=365 d=5 fixed=0/111553 clauses=57'195)
> #Bound  73.60s best:443   next:[32,442]   bool_core (num_cores=32 [size:20 mw:1 d:5] a=346 d=5 fixed=0/111590 clauses=57'234)
> #Bound  75.53s best:443   next:[33,442]   bool_core (num_cores=33 [size:20 mw:1 d:5] a=327 d=5 fixed=0/111627 clauses=57'274)
> #Bound  77.50s best:443   next:[34,442]   bool_core (num_cores=34 [size:20 mw:1 d:5] a=308 d=5 fixed=0/111664 clauses=57'318)
> #Bound  79.57s best:443   next:[35,442]   bool_core (num_cores=35 [size:20 mw:1 d:5] a=289 d=5 fixed=0/111701 clauses=57'360)
> #Bound  80.43s best:443   next:[36,442]   bool_core (num_cores=36 [size:5 mw:1 d:6] a=285 d=6 fixed=0/111723 clauses=57'437)
> #Bound  82.41s best:443   next:[37,442]   bool_core (num_cores=37 [size:20 mw:1 d:5] a=266 d=6 fixed=0/111754 clauses=57'479)
> #Bound  84.47s best:443   next:[38,442]   bool_core (num_cores=38 [size:22 mw:1 d:5] a=245 d=6 fixed=0/111793 clauses=57'519)
> #49     86.28s best:442   next:[38,441]   graph_var_lns (d=5.40e-01 s=911 t=0.10 p=0.48 stall=42 h=stalling)
> #Bound  86.47s best:442   next:[39,441]   bool_core (num_cores=39 [size:22 mw:1 d:5] a=224 d=6 fixed=0/111834 clauses=57'560)
> #Bound  88.53s best:442   next:[40,441]   bool_core (num_cores=40 [size:22 mw:1 d:5] a=203 d=6 fixed=0/111875 clauses=57'605)
> #Bound  90.46s best:442   next:[41,441]   bool_core (num_cores=41 [size:20 mw:1 d:5] a=184 d=6 fixed=0/111914 clauses=57'647)
> #50     91.85s best:441   next:[41,440]   quick_restart
> #Bound  91.87s best:441   next:[42,440]   bool_core (num_cores=42 [size:3 mw:1 d:7] a=182 d=7 fixed=0/111934 clauses=57'886)
> #Bound  95.36s best:441   next:[43,440]   bool_core (num_cores=43 [size:2 mw:1 d:6] a=181 d=7 fixed=0/111947 clauses=57'888)
> #Bound  95.60s best:441   next:[44,440]   bool_core (num_cores=43 [cover] a=181 d=7 fixed=0/111967 clauses=57'971)
> #51     95.72s best:440   next:[44,439]   graph_var_lns (d=6.02e-01 s=1066 t=0.10 p=0.49 stall=5 h=base)
> #52     96.00s best:439   next:[44,438]   graph_var_lns (d=6.02e-01 s=1065 t=0.10 p=0.49 stall=5 h=base) [combined with: graph_var_lns (d=6.0...]
> #Bound  96.46s best:439   next:[45,438]   bool_core (num_cores=43 [cover] a=181 d=7 fixed=1/111987 clauses=58'275)
> #Bound  97.64s best:439   next:[46,438]   bool_core (num_cores=43 [cover] a=181 d=7 fixed=2/111997 clauses=58'692)
> #Bound  98.14s best:439   next:[47,438]   bool_core (num_cores=44 [size:2 mw:1 d:6] a=180 d=7 fixed=3/112007 clauses=58'763)
> #Bound  98.41s best:439   next:[48,438]   bool_core (num_cores=44 [cover] a=180 d=7 fixed=3/112026 clauses=58'843)
> #Bound  98.92s best:439   next:[49,438]   bool_core (num_cores=44 [cover] a=180 d=7 fixed=4/112045 clauses=59'011)
> #53     99.24s best:438   next:[49,437]   quick_restart_no_lp
> #Bound 100.60s best:438   next:[50,437]   bool_core (num_cores=44 [cover] a=180 d=7 fixed=5/112054 clauses=59'463)
> #54    100.61s best:437   next:[50,436]   graph_dec_lns (d=9.77e-01 s=1116 t=0.10 p=0.62 stall=11 h=base)
> #Bound 103.97s best:437   next:[51,436]   bool_core (num_cores=44 [cover] a=180 d=7 fixed=6/112063 clauses=60'314)
> #Bound 108.16s best:437   next:[52,436]   bool_core (num_cores=45 [size:2 mw:1 d:6] a=179 d=7 fixed=7/112072 clauses=61'359)
> #Bound 108.35s best:437   next:[53,436]   bool_core (num_cores=45 [cover] a=179 d=7 fixed=7/112091 clauses=61'430)
> #Bound 110.24s best:437   next:[54,436]   bool_core (num_cores=45 [cover] a=179 d=7 fixed=8/112110 clauses=61'867)
> #Bound 111.09s best:437   next:[55,436]   bool_core (num_cores=46 [size:7 mw:1 d:6] a=173 d=7 fixed=9/112124 clauses=61'938)
> #Bound 111.43s best:437   next:[56,436]   bool_core (num_cores=47 [size:2 mw:1 d:6] a=172 d=7 fixed=9/112139 clauses=61'974)
> #Bound 111.58s best:437   next:[57,436]   bool_core (num_cores=47 [cover] a=172 d=7 fixed=9/112158 clauses=62'042)
> #Bound 112.09s best:437   next:[58,436]   bool_core (num_cores=47 [cover] a=172 d=7 fixed=10/112177 clauses=62'220)
> #Bound 112.71s best:437   next:[59,436]   bool_core (num_cores=47 [cover] a=172 d=7 fixed=11/112186 clauses=62'496)
> #Bound 113.61s best:437   next:[60,436]   bool_core (num_cores=48 [size:4 mw:1 d:6] a=169 d=7 fixed=12/112197 clauses=62'597)
> #Bound 114.10s best:437   next:[61,436]   bool_core (num_cores=49 [size:2 mw:1 d:6] a=168 d=7 fixed=12/112210 clauses=62'668)
> #Bound 114.26s best:437   next:[62,436]   bool_core (num_cores=49 [cover] a=168 d=7 fixed=12/112230 clauses=62'754)
> #Bound 114.56s best:437   next:[63,436]   bool_core (num_cores=50 [size:2 mw:1 d:6] a=167 d=7 fixed=13/112250 clauses=62'802)
> #Bound 114.68s best:437   next:[64,436]   bool_core (num_cores=50 [cover] a=167 d=7 fixed=13/112272 clauses=62'874)
> #Bound 115.61s best:437   next:[65,436]   bool_core (num_cores=51 [size:4 mw:1 d:6] a=164 d=7 fixed=14/112295 clauses=63'080)
> #Bound 116.07s best:437   next:[66,436]   bool_core (num_cores=52 [size:2 mw:1 d:6] a=163 d=7 fixed=14/112309 clauses=63'125)
> #Bound 116.09s best:437   next:[67,436]   bool_core (num_cores=52 [cover] a=163 d=7 fixed=14/112329 clauses=63'182)
> #Bound 117.00s best:437   next:[68,436]   bool_core (num_cores=53 [size:4 mw:1 d:6] a=160 d=7 fixed=15/112349 clauses=63'256)
> #Bound 117.48s best:437   next:[69,436]   bool_core (num_cores=54 [size:2 mw:1 d:6] a=159 d=7 fixed=15/112361 clauses=63'307)
> #Bound 118.42s best:437   next:[70,436]   bool_core (num_cores=55 [size:4 mw:1 d:6] a=156 d=7 fixed=15/112373 clauses=63'392)
> #Bound 119.28s best:437   next:[71,436]   bool_core (num_cores=56 [size:2 mw:1 d:6] a=155 d=7 fixed=15/112386 clauses=63'482)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  30.39s,   30.39s]   30.39s   0.00ns   30.39s
>            'default_lp':         1 [   1.90m,    1.90m]    1.90m   0.00ns    1.90m         1 [  20.93s,   20.93s]   20.93s   0.00ns   20.93s
>      'feasibility_pump':       486 [ 80.54us, 358.66ms]   2.25ms  16.22ms    1.09s       473 [354.60us,   5.75ms] 377.17us 346.32us 178.40ms
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         1 [223.02ms, 223.02ms] 223.02ms   0.00ns 223.02ms         1 [ 13.42ms,  13.42ms]  13.42ms   0.00ns  13.42ms
>             'fs_random':         1 [228.13ms, 228.13ms] 228.13ms   0.00ns 228.13ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [230.03ms, 230.03ms] 230.03ms   0.00ns 230.03ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        75 [289.08ms,    1.73s] 681.98ms 319.17ms   51.15s        67 [ 82.27us, 102.09ms]  55.62ms  46.60ms    3.73s
>         'graph_cst_lns':        38 [476.59ms,    2.46s]    1.37s 464.68ms   52.22s        38 [130.87us, 100.38ms]  52.92ms  45.60ms    2.01s
>         'graph_dec_lns':        41 [175.00ms,    2.48s]    1.23s 659.86ms   50.28s        41 [ 10.00ns, 100.76ms]  49.25ms  47.06ms    2.02s
>         'graph_var_lns':        68 [249.79ms,    1.92s] 751.35ms 317.07ms   51.09s        68 [ 10.00ns, 100.20ms]  61.87ms  43.12ms    4.21s
>                    'ls':       230 [ 30.83ms, 359.95ms] 209.56ms  67.65ms   48.20s       230 [148.92us, 100.27ms]  96.86ms  16.79ms   22.28s
>                'ls_lin':       264 [ 18.03ms, 408.84ms] 181.27ms  79.91ms   47.86s       264 [ 90.26us, 101.45ms]  95.98ms  18.97ms   25.34s
>                'max_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  26.47s,   26.47s]   26.47s   0.00ns   26.47s
>                 'no_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  37.70s,   37.70s]   37.70s   0.00ns   37.70s
>          'pseudo_costs':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  15.70s,   15.70s]   15.70s   0.00ns   15.70s
>         'quick_restart':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  16.29s,   16.29s]   16.29s   0.00ns   16.29s
>   'quick_restart_no_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  28.50s,   28.50s]   28.50s   0.00ns   28.50s
>         'reduced_costs':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  17.11s,   17.11s]   17.11s   0.00ns   17.11s
>             'rins/rens':        54 [ 27.79ms,    2.50s] 907.65ms 646.94ms   49.01s        48 [ 10.00ns, 100.21ms]  53.46ms  49.04ms    2.57s
>           'rnd_cst_lns':        39 [570.32ms,    2.16s]    1.31s 424.04ms   51.16s        39 [  2.59us, 100.13ms]  49.36ms  48.45ms    1.92s
>           'rnd_var_lns':        47 [273.71ms,    2.39s]    1.15s 460.90ms   53.99s        47 [109.00ns, 100.35ms]  52.82ms  47.69ms    2.48s
> 
> Search stats                Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  112'402      5'365  2'622'883    28'709  198'113'171     50'011'929
>            'default_lp':  110'368     74'986    159'253    17'914   47'227'834     24'377'048
>             'fs_random':  104'402          0          0         0            0              0
>       'fs_random_no_lp':  104'609          0          0         0            0              0
>                'max_lp':  110'368          0     15'170    12'790    6'241'241      5'364'473
>                 'no_lp':  110'368    218'637    367'174    29'787  104'541'533     53'576'138
>          'pseudo_costs':  110'368      3'214     54'172    17'883   20'895'215     15'829'178
>         'quick_restart':  110'368      6'137    622'184    18'394   84'511'338     36'112'379
>   'quick_restart_no_lp':  110'368      9'801  1'069'464    27'411  141'508'652     57'134'085
>         'reduced_costs':  110'368      2'579     65'330    17'909   22'211'079     19'067'706
> 
> SAT stats                 ClassicMinim  LitRemoved   LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         4'025      50'438      139'515             0        17    13'805      27'610         0          0            0        0
>            'default_lp':        54'437     497'768   49'768'823    40'398'919        43     5'064      10'128         0          0            0        0
>             'fs_random':             0           0            0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0            0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0            0             0         0         0           0         0          0            0        0
>                 'no_lp':       133'250     677'932  116'950'680   106'205'874       409    16'914      33'828         0          0            0        0
>          'pseudo_costs':         3'180     177'762    4'859'126             0         0     5'053      10'106         0          0            0        0
>         'quick_restart':         4'108      22'945    3'132'139             0        41     5'012      10'024         0          0            0        0
>   'quick_restart_no_lp':         6'744      38'703    5'029'028             0        72    13'648      27'296         0          0            0        0
>         'reduced_costs':         2'562     182'718    3'656'220             0         0     5'060      10'120         0          0            0        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         50       8'567        276  356'067        0        0
>          'max_lp':          1      33'800          0        0    2'385        0
>    'pseudo_costs':          1     115'180     18'733      742   10'134        0
>   'quick_restart':         50      90'065        277  495'543        0        0
>   'reduced_costs':          1     150'820     42'773      258   10'421        0
> 
> Lp dimension               Final dimension of first component
>      'default_lp':              0 rows, 50 columns, 0 entries
>          'max_lp':  71778 rows, 61918 columns, 310623 entries
>    'pseudo_costs':    8565 rows, 61918 columns, 95201 entries
>   'quick_restart':              0 rows, 50 columns, 0 entries
>   'reduced_costs':    9415 rows, 61918 columns, 96057 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow      Bad  BadScaling
>      'default_lp':          0            0      44         0        0           0
>          'max_lp':          0            0   2'385         0        0           0
>    'pseudo_costs':          0            0  10'547         0   19'888           0
>   'quick_restart':          0            0     130         0        0           0
>   'reduced_costs':          0            8  10'280         0  102'497           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened       Cuts/Call
>      'default_lp':        2'768        0        0       0          0      0             0       276/1'490
>          'max_lp':       71'778        0        0       0          0      0             0             0/0
>    'pseudo_costs':       81'511        4        0       0          0     19         9'415   18'733/34'106
>   'quick_restart':        2'769        0        0       0          0      0             0       277/2'804
>   'reduced_costs':       81'551      333        0       0          0    207        17'561  42'773/116'491
> 
> Lp Cut            quick_restart  reduced_costs  pseudo_costs  default_lp
>           CG_FF:              -            122            71           -
>            CG_K:              -             87            14           -
>           CG_KL:              -             14             5           -
>            CG_R:              -            145            29           -
>           CG_RB:              -            120            76           -
>          CG_RBP:              -             59            12           -
>          Clique:              -            144            47           -
>              IB:            277          5'218         9'594         276
>        MIR_1_FF:              -            440           370           -
>         MIR_1_K:              -            607           144           -
>        MIR_1_KL:              -            362           100           -
>         MIR_1_R:              -            417            96           -
>        MIR_1_RB:              -            892           128           -
>       MIR_1_RBP:              -             40            22           -
>        MIR_2_FF:              -          1'173           719           -
>         MIR_2_K:              -          2'391           763           -
>        MIR_2_KL:              -            738           246           -
>         MIR_2_R:              -            173             5           -
>        MIR_2_RB:              -          2'143           513           -
>       MIR_2_RBP:              -          1'211           110           -
>        MIR_3_FF:              -          2'132           791           -
>         MIR_3_K:              -          2'760           601           -
>        MIR_3_KL:              -            727           219           -
>         MIR_3_R:              -            861            93           -
>        MIR_3_RB:              -          1'806           419           -
>       MIR_3_RBP:              -          1'160            45           -
>        MIR_4_FF:              -          1'384           369           -
>         MIR_4_K:              -          1'288           197           -
>        MIR_4_KL:              -            290            92           -
>         MIR_4_R:              -            731            39           -
>        MIR_4_RB:              -            651           153           -
>       MIR_4_RBP:              -            468            22           -
>        MIR_5_FF:              -            683           203           -
>         MIR_5_K:              -            577           100           -
>        MIR_5_KL:              -            119            45           -
>         MIR_5_R:              -            328            40           -
>        MIR_5_RB:              -            268            55           -
>       MIR_5_RBP:              -            201             8           -
>        MIR_6_FF:              -            321           104           -
>         MIR_6_K:              -            252            52           -
>        MIR_6_KL:              -             47            28           -
>         MIR_6_R:              -            161            20           -
>        MIR_6_RB:              -            125            26           -
>       MIR_6_RBP:              -            109             5           -
>    ZERO_HALF_FF:              -          1'486           526           -
>     ZERO_HALF_K:              -          1'683           320           -
>    ZERO_HALF_KL:              -            170            26           -
>     ZERO_HALF_R:              -          3'561           589           -
>    ZERO_HALF_RB:              -          1'178           407           -
>   ZERO_HALF_RBP:              -            750            75           -
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          3/67     49%    3.91e-01       0.10
>   'graph_cst_lns':          4/38     55%    8.37e-01       0.10
>   'graph_dec_lns':          6/41     59%    9.73e-01       0.10
>   'graph_var_lns':          3/68     50%    6.53e-01       0.10
>       'rins/rens':          1/48     48%    3.35e-01       0.10
>     'rnd_cst_lns':          5/39     54%    8.12e-01       0.10
>     'rnd_var_lns':          2/47     51%    7.61e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1      3'030         0              0          0              0         55'735
>                          'ls_lin_restart':       38                 35    674'972         0              0          0        103'984      5'336'792
>                 'ls_lin_restart_compound':       28                 27          0   112'336          3'606     54'356            907      4'446'101
>         'ls_lin_restart_compound_perturb':       44                 39          0   240'038          8'740    115'640          3'134      8'087'820
>                    'ls_lin_restart_decay':       30                 24  1'180'909         0              0          0          2'829      7'249'633
>           'ls_lin_restart_decay_compound':       28                 23          0   156'062         41'548     57'199        226'448      6'242'384
>   'ls_lin_restart_decay_compound_perturb':       31                 29          0   157'472         29'718     63'857         78'202      6'394'549
>            'ls_lin_restart_decay_perturb':       26                 25  1'051'663         0              0          0         41'593      6'329'625
>                  'ls_lin_restart_perturb':       39                 32    718'678         0              0          0        153'245      5'598'680
>                              'ls_restart':       27                 26    360'475         0              0          0         12'051      2'959'868
>                     'ls_restart_compound':       31                 24          0   104'596          2'093     51'240            764      4'879'515
>             'ls_restart_compound_perturb':       30                 26          0    91'601          1'488     45'050            655      4'294'259
>                        'ls_restart_decay':       31                 28    697'727         0              0          0          2'588      4'138'381
>               'ls_restart_decay_compound':       27                 25          0    91'934          5'098     43'411            755      4'364'755
>       'ls_restart_decay_compound_perturb':       36                 35          0   139'254         20'956     59'138          1'016      6'115'446
>                'ls_restart_decay_perturb':       26                 25    577'265         0              0          0          2'336      3'441'901
>                      'ls_restart_perturb':       22                 19    324'199         0              0          0          8'175      2'635'125
> 
> Solutions (54)                          Num     Rank
>                          'default_lp':    1    [7,7]
>                          'fj_restart':    1    [1,1]
>                       'graph_arc_lns':    3  [15,33]
>                       'graph_dec_lns':    6  [28,54]
>                       'graph_var_lns':    3  [49,52]
>                      'ls_lin_restart':    3  [11,32]
>             'ls_lin_restart_compound':    4  [13,42]
>                'ls_lin_restart_decay':    1  [10,10]
>       'ls_lin_restart_decay_compound':    1    [6,6]
>              'ls_lin_restart_perturb':    2   [3,12]
>                          'ls_restart':    3   [4,41]
>         'ls_restart_compound_perturb':    1  [43,43]
>           'ls_restart_decay_compound':    1  [38,38]
>   'ls_restart_decay_compound_perturb':    1  [20,20]
>                  'ls_restart_perturb':    1    [8,8]
>                               'no_lp':    6  [19,25]
>                       'quick_restart':    4  [31,50]
>                 'quick_restart_no_lp':    9  [18,53]
>                       'rins_pump_lns':    1    [9,9]
>                         'rnd_cst_lns':    2   [2,40]
> 
> Objective bounds     Num
>        'bool_core':   57
>   'initial_domain':    1
>           'max_lp':    4
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    580    1'209      431
>    'fj solution hints':      0        0        0
>         'lp solutions':    296       26      278
>                 'pump':    484       28
> 
> Clauses shared               Num
>                  'core':     104
>            'default_lp':   3'504
>                 'no_lp':  12'481
>          'pseudo_costs':       1
>   'quick_restart_no_lp':   6'713
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 437
> best_bound: 71
> integers: 3484
> booleans: 104609
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.351
> usertime: 120.351
> deterministic_time: 264.922
> gap_integral: 1542.42
> solution_fingerprint: 0x4db0e6c4e2da7ccc
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
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0xbacd301d4dee94a1)
> #Variables: 10'600 (#bools: 600 in objective) (10'600 primary variables)
>   - 600 Booleans in [0,1]
>   - 10'000 in [0,99]
> #kElement: 10'000
> #kLinear2: 9'900
> 
> Starting presolve at 0.34s
>   9.51e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.49e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=100 #num_dual_strengthening=1 
>   7.51e-05s  0.00e+00d  [ExtractEncodingFromLinear] 
>   6.90e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   5.34e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'906'900 nodes and 3'016'100 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
>   4.58e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=372'831 
>   2.16e+00s  1.00e+00d *[Probe] #probed=3'802 #new_binary_clauses=1'543'294 
>   6.89e-03s  0.00e+00d  [MaxClique] 
>   1.71e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.67e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   5.30e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.54e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   4.42e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.24e-02s  5.94e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=9'900 
>   3.67e-02s  0.00e+00d  [DetectDifferentVariables] #different=6'267 
>   3.26e-02s  1.12e-03d  [ProcessSetPPC] #relevant_constraints=10'000 
>   1.19e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.31e-01s  3.69e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   4.91e-02s  1.34e-02d  [FindBigVerticalLinearOverlap] 
>   1.16e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.24e-02s  0.00e+00d  [MergeClauses] 
>   1.72e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.34e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.72e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.34e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.61e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   5.51e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'907'631 nodes and 3'389'993 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 0 / 373700
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:373231 literals:746462 vars:373631 one_side_vars:373631 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0299412s] clauses:373231 literals:746462 vars:373631 one_side_vars:373631 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0336802s] clauses:373231 literals:746462 vars:373631 one_side_vars:373631 simple_definition:0 singleton_clauses:0
>   4.90e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.60e+00s  1.00e+00d *[Probe] #probed=3'712 #new_binary_clauses=1'519'715 
>   5.49e-01s  1.00e+00d *[MaxClique] Merged 373'231(746'462 literals) into 373'146(746'377 literals) at_most_ones. 
>   2.23e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.41e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.22e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   6.37e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   6.60e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.07e-02s  5.94e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=9'900 
>   4.50e-02s  0.00e+00d  [DetectDifferentVariables] #different=6'267 
>   1.80e-01s  3.38e-03d  [ProcessSetPPC] #relevant_constraints=383'146 
>   1.68e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.91e-01s  2.04e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   5.31e-02s  1.34e-02d  [FindBigVerticalLinearOverlap] 
>   1.31e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.77e-02s  0.00e+00d  [MergeClauses] 
>   2.23e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.31e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.23e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.29e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.79e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   4.22e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'907'546 nodes and 3'389'780 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 0 / 373700
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:373103 literals:746206 vars:373503 one_side_vars:373503 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0372991s] clauses:373103 literals:746206 vars:373503 one_side_vars:373503 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.041072s] clauses:373103 literals:746206 vars:373503 one_side_vars:373503 simple_definition:0 singleton_clauses:0
>   4.19e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.58e+00s  1.00e+00d *[Probe] #probed=3'710 #new_binary_clauses=1'521'411 
>   5.56e-01s  1.00e+00d *[MaxClique] 
>   2.26e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.41e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.30e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   6.75e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   6.83e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.36e-02s  5.94e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=9'900 
>   4.41e-02s  0.00e+00d  [DetectDifferentVariables] #different=6'267 
>   1.85e-01s  3.38e-03d  [ProcessSetPPC] #relevant_constraints=383'146 
>   1.83e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.91e-01s  2.04e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   5.31e-02s  1.34e-02d  [FindBigVerticalLinearOverlap] 
>   1.46e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.93e-02s  0.00e+00d  [MergeClauses] 
>   2.27e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.31e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.21e-01s  0.00e+00d  [ExpandObjective] #entries=13'706'800 #tight_variables=373'300 #tight_constraints=10'000 
> 
> Presolve summary:
>   - 69 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 269 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 3'600 times.
>   - rule 'affine: new relation' was applied 69 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'bool_and: x => x' was applied 69 times.
>   - rule 'deductions: 1120038 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 69 times.
>   - rule 'dual: fix variable' was applied 128 times.
>   - rule 'element: expanded' was applied 10'000 times.
>   - rule 'exactly_one: simplified objective' was applied 2 times.
>   - rule 'linear: divide by GCD' was applied 9'900 times.
>   - rule 'linear: reduced variable domains' was applied 315'591 times.
>   - rule 'new_bool: integer encoding' was applied 373'300 times.
>   - rule 'objective: variable not used elsewhere' was applied 131 times.
>   - rule 'presolve: 131 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 373'300 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x3a6f25a60ab2e1d8)
> #Variables: 383'700 (#bools: 400 in objective) (373'700 primary variables)
>   - 373'700 Booleans in [0,1]
>   - 1'089 different domains in [0,99] with a largest complexity of 1.
> #kAtMostOne: 43 (#literals: 171)
> #kBoolAnd: 400 (#enforced: 400) (#literals: 373'503)
> #kExactlyOne: 10'000 (#literals: 373'300)
> #kLinear1: 746'600 (#enforced: 746'600)
> #kLinear2: 9'900
> [Symmetry] Graph for symmetry has 1'907'346 nodes and 3'389'780 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> 
> Preloading model.
> #Bound  32.60s best:inf   next:[2,402]    initial_domain
> #Model  32.89s var:383700/383700 constraints:766943/766943
> 
> Starting search at 33.15s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1      34.68s best:293   next:[2,292]    fj_restart(batch:1 lin{mvs:10'291 evals:347'956} #w_updates:0 #perturb:0)
> #2      38.05s best:292   next:[2,291]    rnd_var_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base)
> #3      42.82s best:291   next:[2,290]    default_lp
> #4      44.48s best:283   next:[2,282]    quick_restart_no_lp
> #Bound  56.20s best:283   next:[3,282]    bool_core (num_cores=1 [size:26 mw:1 d:5] a=375 d=5 fixed=0/717024 clauses=363'324)
> #5      73.24s best:282   next:[3,281]    no_lp
> #6      74.59s best:281   next:[3,280]    reduced_costs
> #Bound  79.26s best:281   next:[4,280]    bool_core (num_cores=2 [size:26 mw:1 d:5] a=350 d=5 fixed=0/717073 clauses=363'373)
> #7      96.18s best:279   next:[4,278]    pseudo_costs
> #Bound  97.51s best:279   next:[5,278]    bool_core (num_cores=3 [size:26 mw:1 d:5] a=325 d=5 fixed=0/717122 clauses=363'422)
> #Bound 118.03s best:279   next:[6,278]    bool_core (num_cores=4 [size:26 mw:1 d:5] a=300 d=5 fixed=0/717171 clauses=363'471)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [  16.66s,   16.66s]   16.66s   0.00ns   16.66s
>            'default_lp':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [  10.39s,   10.39s]   10.39s   0.00ns   10.39s
>      'feasibility_pump':       363 [307.99us,    2.93s]  14.46ms 153.23ms    5.25s       337 [  1.37ms,  14.10ms]   1.54ms   1.34ms 518.09ms
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         1 [   1.53s,    1.53s]    1.53s   0.00ns    1.53s         1 [ 85.62ms,  85.62ms]  85.62ms   0.00ns  85.62ms
>             'fs_random':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   1.57s,    1.57s]    1.57s   0.00ns    1.57s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         5 [   4.66s,   12.68s]    7.40s    2.80s   37.02s         5 [108.08us, 101.78ms]  40.55ms  49.27ms 202.74ms
>         'graph_cst_lns':         6 [   3.94s,    9.59s]    6.23s    1.97s   37.40s         5 [ 31.44us,  10.03ms]   2.33ms   3.87ms  11.66ms
>         'graph_dec_lns':        36 [697.56ms,    3.06s]    1.39s 705.86ms   49.99s         5 [ 10.00ns,  10.00ns]  10.00ns   0.00ns  50.00ns
>         'graph_var_lns':         6 [   3.71s,   20.78s]    7.77s    6.18s   46.63s         5 [ 32.53us,  41.01ms]   9.73ms  15.75ms  48.64ms
>                    'ls':        52 [262.49ms,    2.80s] 715.55ms 358.88ms   37.21s        52 [ 55.93ms, 100.17ms]  99.20ms   6.06ms    5.16s
>                'ls_lin':        55 [116.58ms, 945.84ms] 633.78ms 162.71ms   34.86s        55 [ 17.23ms, 101.55ms]  98.61ms  11.08ms    5.42s
>                'max_lp':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [  15.74s,   15.74s]   15.74s   0.00ns   15.74s
>                 'no_lp':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [  16.24s,   16.24s]   16.24s   0.00ns   16.24s
>          'pseudo_costs':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [   6.79s,    6.79s]    6.79s   0.00ns    6.79s
>         'quick_restart':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [  11.70s,   11.70s]   11.70s   0.00ns   11.70s
>   'quick_restart_no_lp':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [  15.50s,   15.50s]   15.50s   0.00ns   15.50s
>         'reduced_costs':         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m         1 [   6.53s,    6.53s]    6.53s   0.00ns    6.53s
>             'rins/rens':         4 [   2.39s,   12.38s]    9.63s    4.19s   38.54s         3 [100.00ms, 100.00ms] 100.00ms 671.75ns 300.01ms
>           'rnd_cst_lns':         5 [   3.85s,   13.96s]    7.87s    3.45s   39.33s         5 [288.66us,  73.92ms]  15.14ms  29.39ms  75.70ms
>           'rnd_var_lns':         8 [   1.79s,    9.04s]    4.62s    2.07s   36.95s         7 [131.48us, 100.08ms]  29.19ms  42.91ms 204.34ms
> 
> Search stats                Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  717'215          5  1'025'158     5'821  108'624'252     28'488'568
>            'default_lp':  717'000      3'827     22'742     5'583   54'549'755     18'377'240
>             'fs_random':  650'324          0          0         0            0              0
>       'fs_random_no_lp':  591'845          0          0         0            0              0
>                'max_lp':  717'000          0      3'936     3'552    6'377'025      6'685'869
>                 'no_lp':  717'000      8'530     45'049     5'585   88'751'616     35'199'648
>          'pseudo_costs':  717'000        150     19'091     5'581   23'027'929     19'601'812
>         'quick_restart':  717'000        644    131'693     5'630   59'854'561     21'155'797
>   'quick_restart_no_lp':  717'000      1'027    198'222     5'656   88'396'052     37'288'807
>         'reduced_costs':  717'000         82     18'844     5'576   20'889'385     18'630'255
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':             0           0           0             0         0     2'020       4'040         0          0            0        0
>            'default_lp':         2'271      15'169   1'644'377             0         4     2'022       4'044         0          0            0        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':         3'802      22'672   3'474'548             0        18     2'028       4'056         0          0            0        0
>          'pseudo_costs':           119         716      55'269             0         0     2'023       4'046         0          0            0        0
>         'quick_restart':           366       4'594     229'255             0         5     2'021       4'042         0          0            0        0
>   'quick_restart_no_lp':           645       5'843     396'392             0         5     2'019       4'038         0          0            0        0
>         'reduced_costs':            24         147      22'415             0         0     2'020       4'040         0          0            0        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':        100           0          0  102'753        0        0
>          'max_lp':          1      13'840          0        0      389        0
>    'pseudo_costs':          1      14'573      5'256      147    1'190        0
>   'quick_restart':        100           0          0  113'202        0        0
>   'reduced_costs':          1      13'688      1'598      153    1'102        0
> 
> Lp dimension                  Final dimension of first component
>      'default_lp':                0 rows, 100 columns, 0 entries
>          'max_lp':  433046 rows, 383700 columns, 1946077 entries
>    'pseudo_costs':     6690 rows, 383700 columns, 154189 entries
>   'quick_restart':                0 rows, 100 columns, 0 entries
>   'reduced_costs':     7937 rows, 383700 columns, 260093 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>          'max_lp':          0            0     383         0      0           0
>    'pseudo_costs':          0            0       0         0  6'326           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0       0         0    846           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':        9'900        0        0       0          0      0             0           0/0
>          'max_lp':      433'046        0        0       0          0      0             0           0/0
>    'pseudo_costs':      438'302        0        0       0          0      0         1'670  5'256/10'652
>   'quick_restart':        9'900        0        0       0          0      0             0           0/0
>   'reduced_costs':      434'644        1        0       0          0      0           254   1'598/6'772
> 
> Lp Cut            reduced_costs  pseudo_costs
>           CG_FF:             17            36
>            CG_K:             18             9
>           CG_KL:              1             2
>            CG_R:             26            23
>           CG_RB:             21            45
>          CG_RBP:              5            10
>          Clique:             24            27
>              IB:            815         3'158
>        MIR_1_FF:              8           315
>         MIR_1_K:              6            49
>        MIR_1_KL:              6            19
>         MIR_1_R:              8             -
>        MIR_1_RB:             15           164
>       MIR_1_RBP:              2             -
>        MIR_2_FF:              5           243
>         MIR_2_K:             54            49
>        MIR_2_KL:             20            37
>        MIR_2_RB:             32            88
>       MIR_2_RBP:             19             1
>        MIR_3_FF:             67           126
>         MIR_3_K:             60            84
>        MIR_3_KL:              9            72
>         MIR_3_R:             29             3
>        MIR_3_RB:             33           106
>       MIR_3_RBP:             13             1
>        MIR_4_FF:             51            43
>         MIR_4_K:             26            39
>        MIR_4_KL:              1            40
>         MIR_4_R:             22             -
>        MIR_4_RB:              -            43
>        MIR_5_FF:              9            17
>         MIR_5_K:              3            28
>        MIR_5_KL:              1            16
>         MIR_5_R:              3             -
>        MIR_5_RB:              -            22
>       MIR_5_RBP:              -             2
>        MIR_6_FF:              3             9
>         MIR_6_K:              -            17
>        MIR_6_KL:              -            16
>        MIR_6_RB:              -            11
>       MIR_6_RBP:              -             1
>    ZERO_HALF_FF:             22            59
>     ZERO_HALF_K:             24            22
>    ZERO_HALF_KL:              2             5
>     ZERO_HALF_R:             58           102
>    ZERO_HALF_RB:             45            95
>   ZERO_HALF_RBP:             15             2
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           0/5     60%    7.29e-01       0.10
>   'graph_cst_lns':           0/5    100%    9.39e-01       0.10
>   'graph_dec_lns':           0/5    100%    9.39e-01       0.10
>   'graph_var_lns':           0/5    100%    9.39e-01       0.10
>       'rins/rens':           0/3      0%    1.24e-01       0.10
>     'rnd_cst_lns':           0/5    100%    9.39e-01       0.10
>     'rnd_var_lns':           1/7     86%    9.32e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1    10'291         0              0          0              0        347'956
>                          'ls_lin_restart':        4                  4    40'394         0              0          0          3'728      1'342'248
>                 'ls_lin_restart_compound':        8                  8         0     8'464             12      4'226              6      3'994'865
>         'ls_lin_restart_compound_perturb':       13                 13         0    14'790             38      7'374             19      7'268'399
>                    'ls_lin_restart_decay':        2                  2    29'116         0              0          0            158        824'258
>           'ls_lin_restart_decay_compound':        9                  9         0    10'818             81      5'367             35      4'970'541
>   'ls_lin_restart_decay_compound_perturb':        6                  6         0     6'758             24      3'367             12      3'343'060
>            'ls_lin_restart_decay_perturb':        5                  5    69'590         0              0          0            412      2'098'338
>                  'ls_lin_restart_perturb':        8                  8   147'771         0              0          0         53'598      2'742'606
>                              'ls_restart':        3                  3    25'400         0              0          0          3'571        603'962
>                     'ls_restart_compound':        5                  5         0     5'360             24      2'667             11      2'799'300
>             'ls_restart_compound_perturb':        6                  5         0     6'233             18      3'107              9      3'065'191
>                        'ls_restart_decay':        5                  5    49'753         0              0          0            701      1'882'215
>               'ls_restart_decay_compound':        6                  6         0     6'844             27      3'408             10      3'346'053
>       'ls_restart_decay_compound_perturb':       11                 11         0    12'397             59      6'169             27      6'096'135
>                'ls_restart_decay_perturb':        5                  5    51'258         0              0          0            765      1'871'036
>                      'ls_restart_perturb':       11                 11    93'555         0              0          0         14'025      2'227'715
> 
> Solutions (7)             Num   Rank
>            'default_lp':    1  [3,3]
>            'fj_restart':    1  [1,1]
>                 'no_lp':    1  [5,5]
>          'pseudo_costs':    1  [7,7]
>   'quick_restart_no_lp':    1  [4,4]
>         'reduced_costs':    1  [6,6]
>           'rnd_var_lns':    1  [2,2]
> 
> Objective bounds     Num
>        'bool_core':    4
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     56      250       55
>    'fj solution hints':      0        0        0
>         'lp solutions':     26        0       26
>                 'pump':    358        4
> 
> Clauses shared              Num
>            'default_lp':  5'084
>                 'no_lp':  1'273
>          'pseudo_costs':     17
>         'quick_restart':    253
>   'quick_restart_no_lp':  2'504
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 279
> best_bound: 6
> integers: 10400
> booleans: 591845
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 122.396
> usertime: 122.396
> deterministic_time: 117.405
> gap_integral: 626.122
> solution_fingerprint: 0xf005b86f66d7f43f
> ```

In [ ]:
```python
_model = Model(instance_large2)
_model.solve(time_limit=120, log=True)
_model.to_solution()
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 120 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x9d2ad25dcaf63b62)
> #Variables: 12'000 (#bools: 2'000 in objective) (12'000 primary variables)
>   - 2'000 Booleans in [0,1]
>   - 10'000 in [0,99]
> #kElement: 10'000
> #kLinear2: 9'900
> 
> Starting presolve at 1.12s
>   1.15e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.27e+01s  0.00e+00d  [PresolveToFixPoint] #num_loops=100 #num_dual_strengthening=1 
>   7.61e-05s  0.00e+00d  [ExtractEncodingFromLinear] 
>   8.91e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   6.97e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'427'300 nodes and 3'846'500 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
>   6.64e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] #without_enforcements=475'112 
>   2.71e+00s  1.00e+00d *[Probe] #probed=6'376 #new_binary_clauses=1'408'326 
>   8.72e-03s  0.00e+00d  [MaxClique] 
>   2.17e-01s  0.00e+00d  [DetectDominanceRelations] 
>   3.43e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=3 #num_dual_strengthening=2 
>   7.13e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   7.76e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   5.26e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.53e-02s  5.94e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=9'900 
>   4.52e-02s  0.00e+00d  [DetectDifferentVariables] #different=5'229 
>   4.08e-02s  1.43e-03d  [ProcessSetPPC] #relevant_constraints=10'000 
>   1.49e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   3.64e-01s  5.93e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   7.34e-02s  1.70e-02d  [FindBigVerticalLinearOverlap] 
>   1.46e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.53e-02s  0.00e+00d  [MergeClauses] 
>   2.16e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.73e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.16e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.73e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.48e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   7.30e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'431'270 nodes and 4'327'566 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 0 / 479086
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:477098 literals:954196 vars:479084 one_side_vars:479084 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0380443s] clauses:477098 literals:954196 vars:479084 one_side_vars:479084 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0432714s] clauses:477098 literals:954196 vars:479084 one_side_vars:479084 simple_definition:0 singleton_clauses:0
>   6.14e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.86e+00s  1.00e+00d *[Probe] #probed=6'376 #new_binary_clauses=1'408'327 
>   6.06e-01s  1.00e+00d *[MaxClique] Merged 477'098(954'196 literals) into 476'919(954'017 literals) at_most_ones. 
>   2.72e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.81e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.66e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   8.33e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.45e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.33e-02s  5.94e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=9'900 
>   5.11e-02s  0.00e+00d  [DetectDifferentVariables] #different=5'229 
>   2.33e-01s  4.32e-03d  [ProcessSetPPC] #relevant_constraints=486'919 
>   1.80e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.91e-01s  3.22e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   7.90e-02s  1.70e-02d  [FindBigVerticalLinearOverlap] 
>   1.65e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.17e-02s  0.00e+00d  [MergeClauses] 
>   2.79e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.69e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.79e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.66e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.67e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   5.74e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 2'431'091 nodes and 4'327'091 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 0 / 479086
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:476802 literals:953604 vars:478788 one_side_vars:478788 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0505269s] clauses:476802 literals:953604 vars:478788 one_side_vars:478788 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0558272s] clauses:476802 literals:953604 vars:478788 one_side_vars:478788 simple_definition:0 singleton_clauses:0
>   5.89e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.86e+00s  1.00e+00d *[Probe] #probed=6'376 #new_binary_clauses=1'410'153 
>   6.31e-01s  1.00e+00d *[MaxClique] Merged 476'919(954'017 literals) into 476'917(954'015 literals) at_most_ones. 
>   2.80e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.83e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.76e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   9.89e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.00e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.68e-02s  5.94e-05d  [DetectDominatedLinearConstraints] #relevant_constraints=9'900 
>   5.32e-02s  0.00e+00d  [DetectDifferentVariables] #different=5'229 
>   2.35e-01s  4.32e-03d  [ProcessSetPPC] #relevant_constraints=486'917 
>   1.97e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.89e-01s  3.21e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   7.90e-02s  1.70e-02d  [FindBigVerticalLinearOverlap] 
>   1.89e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.39e-02s  0.00e+00d  [MergeClauses] 
>   2.81e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.69e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.68e-01s  0.00e+00d  [ExpandObjective] #entries=22'375'400 #tight_variables=477'100 #tight_constraints=10'000 
> 
> Presolve summary:
>   - 2 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 202 times.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 17'874 times.
>   - rule 'affine: new relation' was applied 2 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'bool_and: x => x' was applied 2 times.
>   - rule 'deductions: 1431304 stored' was applied 1 time.
>   - rule 'dual: enforced equivalence' was applied 2 times.
>   - rule 'element: expanded' was applied 10'000 times.
>   - rule 'linear: divide by GCD' was applied 9'900 times.
>   - rule 'linear: reduced variable domains' was applied 261'118 times.
>   - rule 'new_bool: integer encoding' was applied 477'100 times.
>   - rule 'objective: variable not used elsewhere' was applied 12 times.
>   - rule 'presolve: 12 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: add encoding constraint' was applied 477'100 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x72cc18ed63304951)
> #Variables: 489'086 (#bools: 1'988 in objective) (479'086 primary variables)
>   - 479'086 Booleans in [0,1]
>   - 749 different domains in [0,99] with a largest complexity of 1.
> #kAtMostOne: 118 (#literals: 417)
> #kBoolAnd: 1'986 (#enforced: 1'986) (#literals: 478'785)
> #kExactlyOne: 10'000 (#literals: 477'100)
> #kLinear1: 954'200 (#enforced: 954'200)
> #kLinear2: 9'900
> [Symmetry] Graph for symmetry has 2'431'075 nodes and 4'327'086 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> 
> Preloading model.
> #Bound  48.02s best:inf   next:[0,1988]   initial_domain
> #Model  48.40s var:489086/489086 constraints:976204/976204
> 
> Starting search at 48.73s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1      54.11s best:1098  next:[0,1097]   fj_restart(batch:1 lin{mvs:11'097 evals:442'700} #w_updates:0 #perturb:0)
> #2      56.54s best:1096  next:[0,1095]   rnd_var_lns (d=5.00e-01 s=14 t=0.10 p=0.00 stall=0 h=base)
> #3      57.20s best:1094  next:[0,1093]   graph_var_lns (d=5.00e-01 s=16 t=0.10 p=0.00 stall=0 h=base) [combined with: rnd_var_lns (d=5.00e...]
> #4      60.32s best:1093  next:[0,1092]   ls_lin_restart_perturb(batch:1 lin{mvs:311 evals:5'850} #w_updates:236 #perturb:0)
> #5      61.05s best:1092  next:[0,1091]   ls_lin_restart(batch:1 lin{mvs:299 evals:5'740} #w_updates:225 #perturb:0)
> #6      61.42s best:1091  next:[0,1090]   ls_restart_perturb(batch:1 lin{mvs:725 evals:12'571} #w_updates:443 #perturb:0)
> #7      61.63s best:1090  next:[0,1089]   ls_lin_restart_decay_compound(batch:1 lin{mvs:0 evals:19'602} gen{mvs:111 evals:0} comp{mvs:5 btracks:53} #w_updates:1 #perturb:0)
> #8      61.88s best:1089  next:[0,1088]   ls_lin_restart_decay_compound(batch:1 lin{mvs:0 evals:68'795} gen{mvs:430 evals:0} comp{mvs:22 btracks:204} #w_updates:7 #perturb:0)
> #9      62.82s best:1088  next:[0,1087]   ls_lin_restart(batch:1 lin{mvs:85 evals:2'849} #w_updates:61 #perturb:0)
> #10     64.59s best:1087  next:[0,1086]   no_lp
> #11     66.26s best:1028  next:[0,1027]   no_lp
> #12     67.22s best:1027  next:[0,1026]   ls_lin_restart_compound_perturb(batch:1 lin{mvs:0 evals:94'000} gen{mvs:732 evals:0} comp{mvs:20 btracks:356} #w_updates:8 #perturb:0)
> #13     69.05s best:1026  next:[0,1025]   ls_lin_restart_compound(batch:1 lin{mvs:0 evals:138'220} gen{mvs:961 evals:0} comp{mvs:33 btracks:464} #w_updates:14 #perturb:0)
> #14     70.59s best:1025  next:[0,1024]   no_lp
> #15     71.98s best:1024  next:[0,1023]   no_lp
> #16     72.40s best:1023  next:[0,1022]   ls_restart_perturb(batch:1 lin{mvs:142 evals:3'610} #w_updates:158 #perturb:0)
> #Bound  76.00s best:1023  next:[1,1022]   bool_core (num_cores=1 [size:45 mw:1 d:6] a=1944 d=6 fixed=0/926229 clauses=467'143)
> #Bound 105.44s best:1023  next:[2,1022]   bool_core (num_cores=2 [size:41 mw:1 d:6] a=1904 d=6 fixed=0/926312 clauses=467'227)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.23m,    1.23m]    1.23m   0.00ns    1.23m         1 [  17.75s,   17.75s]   17.75s   0.00ns   17.75s
>            'default_lp':         1 [   1.19m,    1.19m]    1.19m   0.00ns    1.19m         1 [   8.92s,    8.92s]    8.92s   0.00ns    8.92s
>      'feasibility_pump':       283 [300.57us,    3.73s]  21.48ms 221.06ms    6.08s       246 [  1.38ms,  19.17ms]   1.62ms   1.75ms 399.16ms
>                    'fj':         1 [   1.66s,    1.66s]    1.66s   0.00ns    1.66s         1 [102.47ms, 102.47ms] 102.47ms   0.00ns 102.47ms
>                    'fj':         2 [823.72ms,    1.49s]    1.16s 332.89ms    2.31s         2 [102.46ms, 124.16ms] 113.31ms  10.85ms 226.62ms
>             'fs_random':         1 [   6.16s,    6.16s]    6.16s   0.00ns    6.16s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   5.72s,    5.72s]    5.72s   0.00ns    5.72s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         4 [   3.80s,   14.76s]    7.43s    4.30s   29.71s         3 [  1.36ms, 100.20ms]  34.86ms  46.21ms 104.59ms
>         'graph_cst_lns':         4 [   4.92s,   11.06s]    7.84s    2.86s   31.37s         4 [  4.09ms, 100.05ms]  53.20ms  46.86ms 212.79ms
>         'graph_dec_lns':        16 [   1.03s,    4.46s]    2.49s 903.26ms   39.86s         7 [ 10.00ns, 833.00ns] 127.57ns 287.99ns 893.00ns
>         'graph_var_lns':         6 [   2.38s,    7.49s]    4.91s    1.52s   29.47s         6 [612.11us, 100.48ms]  52.91ms  47.46ms 317.43ms
>                    'ls':        67 [187.81ms,    1.39s] 404.85ms 183.10ms   27.12s        67 [294.16us, 101.26ms]  95.22ms  20.45ms    6.38s
>                'ls_lin':        70 [ 90.84ms,    2.82s] 419.45ms 350.19ms   29.36s        70 [628.12us, 110.85ms]  91.84ms  25.81ms    6.43s
>                'max_lp':         1 [   1.19m,    1.19m]    1.19m   0.00ns    1.19m         1 [  11.42s,   11.42s]   11.42s   0.00ns   11.42s
>                 'no_lp':         1 [   1.23m,    1.23m]    1.23m   0.00ns    1.23m         1 [  11.55s,   11.55s]   11.55s   0.00ns   11.55s
>          'pseudo_costs':         1 [   1.19m,    1.19m]    1.19m   0.00ns    1.19m         1 [   6.17s,    6.17s]    6.17s   0.00ns    6.17s
>         'quick_restart':         1 [   1.19m,    1.19m]    1.19m   0.00ns    1.19m         1 [   9.55s,    9.55s]    9.55s   0.00ns    9.55s
>   'quick_restart_no_lp':         1 [   1.19m,    1.19m]    1.19m   0.00ns    1.19m         1 [  13.12s,   13.12s]   13.12s   0.00ns   13.12s
>         'reduced_costs':         1 [   1.19m,    1.19m]    1.19m   0.00ns    1.19m         1 [   5.81s,    5.81s]    5.81s   0.00ns    5.81s
>             'rins/rens':         6 [338.96ms,   14.84s]    4.81s    6.34s   28.87s         2 [100.00ms, 100.01ms] 100.01ms   3.32us 200.01ms
>           'rnd_cst_lns':         4 [   2.42s,   12.75s]    7.62s    4.17s   30.46s         3 [688.27us, 100.00ms]  34.24ms  46.50ms 102.72ms
>           'rnd_var_lns':         5 [   2.40s,    9.29s]    6.66s    2.45s   33.28s         4 [198.21us, 100.46ms]  29.41ms  41.20ms 117.62ms
> 
> Search stats                Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  926'396          8  1'028'943     8'335  131'863'181     18'381'266
>            'default_lp':  926'186      6'532     32'734     8'092   39'534'150     10'641'922
>             'fs_random':  926'186          0      1'736     1'736      659'525        965'852
>       'fs_random_no_lp':  926'186          0      1'876     1'876      700'962        989'626
>                'max_lp':  926'186          0      6'468     6'220    6'594'319      6'693'256
>                 'no_lp':  926'186     17'115     66'445     8'093   48'699'313     15'977'926
>          'pseudo_costs':  926'186         50     20'849     8'084   27'866'732     20'284'753
>         'quick_restart':  926'186        255     93'779     8'108   52'808'650     15'490'800
>   'quick_restart_no_lp':  926'186        493    172'298     8'115   72'870'212     25'516'612
>         'reduced_costs':  926'186          0     27'162     8'086   21'933'592     17'565'501
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':             0           0         222             0         0     1'864       3'728         0          0            0        0
>            'default_lp':         3'495      27'047   8'433'125             0         5     1'862       3'724         0          0            0        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':         2'814      11'400  19'354'661     5'372'491       581     1'863       3'726         0          0            0        0
>          'pseudo_costs':            35         190      55'129             0         0     1'862       3'724         0          0            0        0
>         'quick_restart':           122         824     313'311             0         3     1'863       3'726         0          0            0        0
>   'quick_restart_no_lp':           238       1'931     637'200             0         2     1'847       3'694         0          0            0        0
>         'reduced_costs':             0           0           0             0         0     1'863       3'726         0          0            0        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':        100       1'261         98   73'838        0        0
>       'fs_random':        100           0          0        0        0        0
>          'max_lp':          1      12'470          0        0      252        0
>    'pseudo_costs':          1       9'179      3'365       90      733        0
>   'quick_restart':        100       1'502         98   87'634        0        0
>   'reduced_costs':          1       7'369      1'637      109      476        0
> 
> Lp dimension                  Final dimension of first component
>      'default_lp':                0 rows, 100 columns, 0 entries
>       'fs_random':                0 rows, 100 columns, 0 entries
>          'max_lp':  536817 rows, 489086 columns, 2465115 entries
>    'pseudo_costs':      5150 rows, 489086 columns, 55856 entries
>   'quick_restart':                0 rows, 100 columns, 0 entries
>   'reduced_costs':     5605 rows, 489086 columns, 221551 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>       'fs_random':          0            0       0         0      0           0
>          'max_lp':          0            0     242         0      0           0
>    'pseudo_costs':          0            0      18         0  1'146           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0      45         0    679           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':       10'004        0        0       0          0      0             0       98/164
>       'fs_random':        9'906        0        0       0          0      0             0          0/0
>          'max_lp':      536'817        0        0       0          0      0             0          0/0
>    'pseudo_costs':      540'182        0        0       0          0      0           244  3'365/4'843
>   'quick_restart':       10'004        0        0       0          0      0             0       98/204
>   'reduced_costs':      538'454        3        0       0          0      0         1'644  1'637/4'489
> 
> Lp Cut            default_lp  quick_restart  reduced_costs  pseudo_costs
>           CG_FF:           -              -             19            17
>            CG_K:           -              -              9             -
>           CG_KL:           -              -              6             -
>            CG_R:           -              -             23             5
>           CG_RB:           -              -             29            25
>          CG_RBP:           -              -             15             2
>          Clique:           -              -             25            11
>              IB:          98             98            659         2'933
>        MIR_1_FF:           -              -            136            68
>         MIR_1_K:           -              -             49             -
>        MIR_1_KL:           -              -             72             5
>         MIR_1_R:           -              -             86             -
>        MIR_1_RB:           -              -             23            19
>        MIR_2_FF:           -              -             24            66
>         MIR_2_K:           -              -             38            11
>        MIR_2_KL:           -              -              6            13
>         MIR_2_R:           -              -             18             -
>        MIR_2_RB:           -              -             28            16
>       MIR_2_RBP:           -              -             15             -
>        MIR_3_FF:           -              -             45            27
>         MIR_3_K:           -              -             39            18
>        MIR_3_KL:           -              -              5            10
>         MIR_3_R:           -              -             27             3
>        MIR_3_RB:           -              -             15            20
>       MIR_3_RBP:           -              -              8             -
>        MIR_4_FF:           -              -             37            20
>         MIR_4_K:           -              -             10             3
>        MIR_4_KL:           -              -              2             1
>         MIR_4_R:           -              -             15             -
>        MIR_4_RB:           -              -              -             4
>        MIR_5_FF:           -              -              5             6
>         MIR_5_R:           -              -              1             -
>        MIR_5_RB:           -              -              -             1
>        MIR_6_FF:           -              -              -             2
>        MIR_6_RB:           -              -              -             1
>    ZERO_HALF_FF:           -              -             19            15
>     ZERO_HALF_K:           -              -             23             1
>    ZERO_HALF_KL:           -              -              2             -
>     ZERO_HALF_R:           -              -             53            25
>    ZERO_HALF_RB:           -              -             37            17
>   ZERO_HALF_RBP:           -              -             14             -
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           2/3     67%    7.21e-01       0.10
>   'graph_cst_lns':           1/4     50%    5.97e-01       0.10
>   'graph_dec_lns':           0/7    100%    9.67e-01       0.10
>   'graph_var_lns':           1/6     50%    5.87e-01       0.10
>       'rins/rens':           0/2      0%    1.86e-01       0.10
>     'rnd_cst_lns':           1/3     67%    7.21e-01       0.10
>     'rnd_var_lns':           2/4     75%    8.08e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        2                  2    22'194         0              0          0              0        885'870
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0     9'946          9'944          0              0        448'929
>                          'ls_lin_restart':        8                  5    24'496         0              0          0          3'026        942'177
>                 'ls_lin_restart_compound':        9                  7         0    14'588            304      7'139            154      1'887'200
>         'ls_lin_restart_compound_perturb':        6                  5         0     9'406            212      4'596            101      1'222'245
>                    'ls_lin_restart_decay':       10                  7    94'846         0              0          0            693      3'512'171
>           'ls_lin_restart_decay_compound':        7                  7         0     9'609            296      4'652            117      1'278'765
>   'ls_lin_restart_decay_compound_perturb':        6                  5         0    42'071          4'957     18'556          3'399      1'878'143
>            'ls_lin_restart_decay_perturb':       13                  9   132'988         0              0          0            898      4'569'664
>                  'ls_lin_restart_perturb':       11                  7    50'493         0              0          0          8'740      1'593'993
>                              'ls_restart':        7                  5    39'696         0              0          0          2'410      1'219'241
>                     'ls_restart_compound':        5                  5         0     6'308            181      3'063             89      1'073'341
>             'ls_restart_compound_perturb':        7                  3         0     9'085            163      4'460             75      1'346'227
>                        'ls_restart_decay':        8                  8    47'405         0              0          0          1'053      1'762'769
>               'ls_restart_decay_compound':       11                 10         0    16'623            819      7'899            245      2'399'530
>       'ls_restart_decay_compound_perturb':       11                  7         0    15'130            477      7'325            181      2'284'355
>                'ls_restart_decay_perturb':       11                  6    94'352         0              0          0            485      3'021'135
>                      'ls_restart_perturb':        7                  6    28'469         0              0          0          2'704        875'090
> 
> Solutions (16)                        Num     Rank
>                        'fj_restart':    1    [1,1]
>                     'graph_var_lns':    1    [3,3]
>                    'ls_lin_restart':    2    [5,9]
>           'ls_lin_restart_compound':    1  [13,13]
>   'ls_lin_restart_compound_perturb':    1  [12,12]
>     'ls_lin_restart_decay_compound':    2    [7,8]
>            'ls_lin_restart_perturb':    1    [4,4]
>                'ls_restart_perturb':    2   [6,16]
>                             'no_lp':    4  [10,15]
>                       'rnd_var_lns':    1    [2,2]
> 
> Objective bounds     Num
>        'bool_core':    2
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     71      194       69
>    'fj solution hints':      0        0        0
>         'lp solutions':     29        6       28
>                 'pump':    278        0
> 
> Clauses shared              Num
>                  'core':  1'855
>            'default_lp':    992
>                 'no_lp':  1'939
>          'pseudo_costs':  1'872
>         'quick_restart':  1'896
>   'quick_restart_no_lp':  1'170
>         'reduced_costs':  4'359
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 1023
> best_bound: 2
> integers: 12034
> booleans: 926186
> conflicts: 0
> branches: 1876
> propagations: 700962
> integer_propagations: 989626
> restarts: 1876
> lp_iterations: 0
> walltime: 122.763
> usertime: 122.763
> deterministic_time: 105.195
> gap_integral: 685.372
> solution_fingerprint: 0xa76a43436fc56e15
> ```

大きなインスタンスに対しても実行可能解がきちんと出る.
Dual Bound はカスだけど...
