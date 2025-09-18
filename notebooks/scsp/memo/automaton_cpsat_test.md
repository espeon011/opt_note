In [ ]:
```python
import opt_note.scsp as scsp
from ortools.sat.python import cp_model
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# `AUTOMATON_CPSAT` モデルの改良

`Alphabet` アルゴリズムで求めた巨大な共通超配列の部分列の中から最短な共通超配列を見つける方針.

ただし `Alphabet` アルゴリズムの部分列には本当の最短共通超配列は存在しない場合がある.
例えば `ba`, `cb` の最短共通超配列は `cba` だが `Alphabet` アルゴリズムで構築した解は `abcabc` であり, この中から最短な共通超配列を探すと `bcab` のようになってしまう.
これは `Alphabet` アルゴリズムにおいてアルファベットを並べる順序が固定されているからであり, アルファベットの並びをブロックごとに可変にしたら改善するんじゃないかと考えた.

ただしアルファベットの並びを可変にすれば最適解を実行可能領域に含むようになるかは証明していない.
従って改良モデルにおける dual bound は (あくまで最初に用意した大きな配列の部分配列の中での dual bound なため) 実際には最適解より大きくなってしまう可能性がある.

In [ ]:
```python
class Model:
    def __init__(self, instance: list[str], perm: bool = False):
        chars = "".join(sorted(list(set("".join(instance)))))
        max_len = len(chars) * max(len(s) for s in instance)

        cpmodel = cp_model.CpModel()

        if perm:
            cvars = [
                cpmodel.new_int_var(lb=0, ub=len(chars) - 1, name="") for _ in range(max_len)
            ]
        else:
            cvars = [
                cpmodel.new_constant(idx % len(chars)) for idx in range(max_len)
            ]

        valids = [cpmodel.new_bool_var("") for _ in cvars]
        transition_expressions = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="") for _ in range(max_len)
        ]

        # 初期解としてアルファベットアルゴリズムを設定
        if perm:
            for idx, cvar in enumerate(cvars):
                cpmodel.add_hint(cvar, idx % len(chars))
        for valid in valids:
            cpmodel.add_hint(valid, 1)
        for idx, texp in enumerate(transition_expressions):
            cpmodel.add_hint(texp, idx % len(chars) + 1)

        if perm:
            for t in range(max(len(s) for s in instance)):
                cpmodel.add_all_different(cvars[t * len(chars) : (t + 1) * len(chars)])

        for cvar, valid, texp in zip(cvars, valids, transition_expressions):
            cpmodel.add(texp == 0).only_enforce_if(~valid)
            cpmodel.add(texp == cvar + 1).only_enforce_if(valid)

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
                transition_expressions=transition_expressions,
                starting_state=0,
                final_states=[len(s)],
                transition_triples=transition_triples,
            )

        cpmodel.minimize(sum(valids))

        self.instance = instance
        self.chars = chars
        self.cpmodel = cpmodel
        self.cpsolver = cp_model.CpSolver()
        self.cvars = cvars
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
        for cvar, valid in zip(self.cvars, self.valids):
            if self.cpsolver.boolean_value(valid):
                cidx = self.cpsolver.value(cvar)
                solution += self.chars[cidx]

        return solution
```

In [ ]:
```python
def bench1(instance: list[str]) -> None:
    model = scsp.model.automaton_cpsat.Model(instance).solve()
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
def bench2(instance: list[str], perm: bool) -> None:
    model = Model(instance, perm).solve()
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

最初に示した例で計算してみよう.
`ba`, `cb` に対する最短共通超配列を `AUTOMATON_CPSAT` モデルで求めると最適解 (の 1 つ) は `cba` だとわかる.

In [ ]:
```python
bench1(["ba", "cb"])
```

> ```
> --- Condition (with 3 chars) ---
> str1: ba
> str2: cb
> 
> --- Solution (of length 3) ---
>  Sol: cba
> str1: -ba
> str2: cb-
> 
> solution is feasible: True
> solution status: OPTIMAL
> bset bound: 3.0
> ```

一方順番を固定した改良法だとこの最適解は出ない.

In [ ]:
```python
bench2(["ba", "cb"], perm=False)
```

> ```
> --- Condition (with 3 chars) ---
> str1: ba
> str2: cb
> 
> --- Solution (of length 4) ---
>  Sol: bcab
> str1: b-a-
> str2: -c-b
> 
> solution is feasible: True
> solution status: OPTIMAL
> bset bound: 4.0
> ```

アルファベットの順番を可変にすると元の最適解が出るようになる.

In [ ]:
```python
bench2(["ba", "cb"], perm=True)
```

> ```
> --- Condition (with 3 chars) ---
> str1: ba
> str2: cb
> 
> --- Solution (of length 3) ---
>  Sol: cba
> str1: -ba
> str2: cb-
> 
> solution is feasible: True
> solution status: OPTIMAL
> bset bound: 3.0
> ```

## ベンチマーク

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
> --- Solution (of length 67) ---
>  Sol: iutkglcojiqfolenbkxxycvosuhamqopvixnozhtsqgxbzprplpsvddbxicsvrvnngf
> str1: --tkg----------n-k-------uh-m--p--xn--ht-qgx-z------v---xi-s-------
> str2: i------ojiqfol-nb-xx-cv-su---q-pvi------s----------s---bx---------f
> str3: -u---lc--i-----n----yc-os-----o-v---oz--------p-plp----------------
> str4: i---g---------e-------v----a---------z----g-b--r-----ddb--csvrvnngf
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 11.0
> ```

In [ ]:
```python
bench2(instance01, perm=False)
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 64) ---
>  Sol: iogjeiqtvafkozglnbkruxdhlmpxcdinvybchostuoqvgoxzprvxipslpsbnnxgf
> str1: -------t---k--g-n-k-u--h-mpx---n----h--t--q-g-xz--vxi-s---------
> str2: io-j-iq---f-o--lnb---x-----xc---v-----s-u-q-----p-v-i-s--sb--x-f
> str3: --------------------u---l---c-in-y-c-os--o-v-o-zp----p-lp-------
> str4: i-g-e---va---zg--b-r--d------d----bc--s----v-----rv--------nn-gf
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 50.0
> ```

In [ ]:
```python
bench2(instance01, perm=True)
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 75) ---
>  Sol: iotugjklceginqvyacfkosuzghlmnopvxbnorxzdhptxcdpqvbcglsuvxzqrvxinpvinsgsfbxf
> str1: --t---k---g-n------k--u--h-m--p-x-n-----h-t----q---g----xz--vxi-----s------
> str2: io---j-----i-q----f-o-----l-n----b---x-----xc---v----su---q-----pvi-s-s-bxf
> str3: ---u---lc--in--y-c--os-------o-v---o--z--p----p-----l-----------p----------
> str4: i---g----e----v-a------zg--------b--r--d-----d---bc--s-v---rv--n---n-g-f---
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 3.0
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
> --- Solution (of length 137) ---
>  Sol: tkgnkuhmpxnhtqgiojiqfolnbxxcvsuqplcvisngycoesovazgbrddbcplsvorzvnnxucpmqvgtdfeuivdcvdpfzsmsbroenqvbczfjtvxerzbrvigphwxqkrdrlctodtmprpxwed
> str1: tkgnkuhmpxnhtqg----------x----------------------z----------v------x------------i--------s------------------------------------------------
> str2: ---------------iojiqfolnbxxcvsuqp--vis------s-----b---------------x---------f------------------------------------------------------------
> str3: -----u----------------l----c--------i-n-yco-sov-------------o-z------p---------------p-------------------------------------l------p------
> str4: ---------------i-----------------------g---e--vazgbrddbc--sv-r-vnn-------g--f------------------------------------------------------------
> str5: --------p-------------------------------y---------------pl---rz---xucpmqvgtdf-uiv-c-d---s--b-o-------------------------------------------
> str6: --------p---------------b---------------------------d------------------------e--vdcvdpfzsmsbro--qvb----------b-----h---------------------
> str7: -------------------------------------------e--------------------n--------------------------b-------czfjtvxerzbrvigp--------l-----------e-
> str8: ---------------------------------------------------r--------------x-------------------------------------------------wxqkrdrlctodtmprpxw-d
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 6.0
> ```

In [ ]:
```python
bench2(instance02, perm=False)
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
> --- Solution (of length 112) ---
>  Sol: iugloprtxbdejnvbcwxadiknqyzcfjotvdglnpbfklrxzdrxcdlsuvbcempsuvbhmqrtopvxgtdfnuhistozbmpqrvinbcgpxzvwxdisblpxefho
> str1: -------t--------------k-----------g-n---k-----------u----------hm----p-x----n-h--t-----q------g-xzv-x-is--------
> str2: i---o-------j--------i--q---f-o----ln-b----x---xc----v-----su----q---pv--------is----------------------sb--x-f--
> str3: -u-l------------c----i-n-y-c--o--------------------s----------------o-v-----------oz--p--------p---------lp-----
> str4: i-g--------e--v----a------z-------g---b---r--d---d----bc---s-v----r---v-----n--------------n--g--------------f--
> str5: -----p-------------------y-----------p---lr-z--x----u--c--p-----mq----v-gtdf-u-i---------v---c-------d-sb------o
> str6: -----p---bde--v-----d------c----vd---p-f----z------s-----m-s--b---r-o------------------q-v--b-----------b-----h-
> str7: -----------e-n-bc---------z-fj-tv----------x------------e---------r----------------zb---rvi---gp---------l--e---
> str8: ------r-x--------wx-----q---------------k-r--dr---l----c-----------to-----d------t---mp-r------px--w-d----------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 57.0
> ```

In [ ]:
```python
bench2(instance02, perm=True)
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
> --- Solution (of length 289) ---
>  Sol: iogqrsetvxayzbcdefghijklmnopqrstuvwxyzbcdefghijklmnopqvwxyzbcdefghijklmnopqrstuvwxyzbcdefghijklmnopqrstavwxyubrdefghijlcnopqustyvwxmzabcdefgqijkxtuvgeorstucvxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnsqbcdefghijklmnopqrvwxzabcdefghijklmoqpstuvwxyzarstuvwxyzabcdefghijklmnopqrstuvwxyzabwxhf
> str1: -------t--------------k--------------------g------n-----------------k---------u-----------h----m--p-------x-------------n----------------------------------------------h-----------t---------------------q-----g-------------xz-------------------v-x--------------------i---------s-------------
> str2: io-------------------j-----------------------i-------q---------f--------o---------------------l-n------------b--------------------x-------------x----------cv---------------------s-u--------------------q--------------p--v-----------i-------s---------s--------b---------------------x-------f
> str3: --------------------------------u---------------l-----------c-----i----n----------y--c-----------o---s-------------------o------v---------------------o--------z---------------p----------------------------------------p-----------------l---p--------------------------------------------------
> str4: i-g---e-v-a-z-----g-------------------b------------------------------------r----------d------------------------d----------------------bc----------------s---v--------------------r---v-----------------n--------------n--------------g--------------------------------f--------------------------
> str5: ---------------------------p--------y---------------p----------------l-----r-------z----------------------x-u----------c--p--------m--------q------vg----t---------d-f--------------u-------------i------------------------v-----cd------------s------------------b------------o-----------------
> str6: ---------------------------p----------b-de------------v------d-----------------------c------------------v------d----------p---------------f--------------------z------------------s-------------------m-s-b---------------r-----------------oq----v---------------b-------------------------b--h-
> str7: ------e------------------n------------bc------------------z----f---j---------t-v-x-----e------------r-------------------------------z-b----------------r----v-----------i-----------------------g-----------------------p-----------------l--------------------------e---------------------------
> str8: ----r----x------------------------wx-----------------q--------------k------r----------d-------------r-----------------lc------t-----------------------o------------d---------------t------------------m-----------------p-r-------------------p-----x--------w------d----------------------------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 2.0
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
> --- Solution (of length 241) ---
>   Sol: tkgnkuhmpxnhiojiqfolnbxxulcinycosoigevoazgbrddbcsvpyplrzxucpmqvgtbdevdfucvdpfzsmsnbczfjtvxerzbrvigxwxqkrdrlctodtmpkkqafigqjwokkskrblxxpabivbvzkozrifsavnqaxudgqvqcewbfgijowwyrsxqjnfpadiusiqbwezshkvhcomiuvddhtxxqjzqbctbakxusfcfzpeecvwantfmgqzu
> str01: tkgnkuhmpxnh----------------------------------------------------t------------------------------------q------------------g-----------x--------z--------v---x------------i------s------------------------------------------------------------------
> str02: ------------iojiqfolnbxx--c----------v----------s--------u---q-------------p------------v-------i------------------------------s--------------------s---------------b----------x---f-------------------------------------------------------------
> str03: -----u-------------l------cinycoso---vo-z---------p-pl-----p-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: ------------i----------------------gev-azgbrddbcsv----r-------v------------------n---------------------------------------------------------------------n-----g-------f---------------------------------------------------------------------------
> str05: --------p--------------------y--------------------p--lrzxucpmqvgt-d---fu------------------------i-----------------------------------------v----------------------c--------------------d--s--b---------o------------------------------------------
> str06: --------p------------b----------------------d----------------------evd--cvdpfzsms-b--------r-----------------o------q---------------------vb------------------------b----------------------------h-----------------------------------------------
> str07: ------------------------------------e--------------------------------------------nbczfjtvxerzbrvig---------------p-----------------l------------------------------e------------------------------------------------------------------------------
> str08: -------------------------------------------r------------x------------------------------------------wxqkrdrlctodtmp---------------r----p-------------------x--------w------------------d----------------------------------------------------------
> str09: -k--k-----------q----------------------a------------------------------f-------------------------ig---q--------------------jwokkskrbl-------------------------g-----------------------------------------------------------------------------------
> str10: -------------------l--xx--------------------------p------------------------------------------------------------------a------------b------ivbvzkoz----------------------------------------------z---v-------d-------------------------------------
> str11: -k-----------------------------------------r----------------------------------------------------i---------------------f--------s-------a--v------------n---------c--------------------d----q-w---h-----------------z--c--------------------------
> str12: ----------------q----------------------a----------------xu--------d------------------------------g---q------------------------------------v-------------q--------cewbfgijowwy--------------------------------------------------------------------
> str13: -------------------------------------------r----s-------x----q------------------------j----------------------------------------------------------------n-------------f--------------padiusiqb-ez-hk---o------h------------------------------mg---
> str14: ------------i--------------------------------------------------------------------------------------w---------------------------s-----------------------------------------------------------------h-vhcomiuvdd-------------------------------m----
> str15: ------h---------------------------------------------------------t------------------------x--------x--q--------------------j------------------z----------q-----------b--------------------------------c--------t------b---ak--------------n-------
> str16: ---------x--------------u-------s-------------------------------------f-c---fz-----------------------------------p------------------------------------------------e---------------------------e------c----v----------------------------wantfmgqzu
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 2.0
> ```

In [ ]:
```python
bench2(instance03, perm=False)
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
> --- Solution (of length 164) ---
>   Sol: ioxhjktuwgikpqrxyesvafipwxzghnoqubdejklnrvxzbdgqrwxdfpuabcfhpsvzdilmpquxacefjotvzgknwbehkmstycimoqsxdefgruxzbeijkqtmoprvwzabchkozhlnptxdfimnqsvbgpqszbhlopceuvwxdfmy
> str01: ------t----k---------------g-n-------k----------------u----h-------mp--x-----------n---h---t-----q-----g--xz-----------v--------------x--i---s----------------------
> str02: io--j-----i--q-------f--------o-------ln----b-----x--------------------x-c-----v----------s--------------u-------q---p-v-----------------i---s-----s-b---------x-f--
> str03: -------u------------------------------l------------------c-------i-----------------n--------yc--o-s-----------------o--v-------oz---p------------p-----l-p----------
> str04: i--------g-------e-va-----zg-----b------r----d-----d----bc---sv-----------------------------------------r--------------v-----------n-------n----g----------------f--
> str05: ------------p---y------p--------------l-r--z------x---u--c--p------m-q---------v-g---------t--------d-f--u----i--------v----c----------d-----s-b--------o-----------
> str06: ------------p--------------------bde-----v---d-----------c----v-d---p------f----z---------s----m--s---------b---------r--------o------------q-vb-----bh-------------
> str07: -----------------e-----------n---b-----------------------c-----z-----------fj-tv-------------------x-e--r--zb---------rv-----------------i------gp-----l---e--------
> str08: --------------rx--------wx-----q-----k--r----d--r-----------------l------c----t-----------------o---d-------------tm-pr-------------p-x-----------------------w-d---
> str09: -----k-----k-q------afi----g---q----j------------w---------------------------o----k-----k-s---------------------k-----r----b------l-------------g-------------------
> str10: --------------------------------------l---x-------x--p-ab--------i-------------v-----b---------------------------------v-z----koz-------------------z--------v--d---
> str11: -----k--------r-------i-----------------------------f--------s----------a------v---n---------c------d------------q------w----h--z-------------------------c---------
> str12: -------------q------a----x------u-d-----------gq--------------v------q---ce---------wb----------------fg------ij----o---w-------------------------------------w----y
> str13: --------------r---s------x-----q----j--n------------fp-a--------di----u-------------------s---i--q----------be-----------z---hko-h--------m-----g-------------------
> str14: i-------w---------s---------h------------v-----------------h-------------c---o-----------m----i----------u-------------v---------------d------------------------d-m-
> str15: ---h--t--------x---------x-----q----j------z---q--------bc--------------------t------b------------------------------------a---k----n--------------------------------
> str16: --x----u----------s--f-----------------------------------cf----z----p-----e-----------e------c-------------------------vw-a--------n-t--f-m-----g-q-z-------u-------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 26.0
> ```

In [ ]:
```python
bench2(instance03, perm=True)
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
> solution status: UNKNOWN
> bset bound: 0.0
> ```

アルファベットの順番を可変にすると解が悪化した.

## ログを見よう

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
> Initial optimization model '': (model_fingerprint: 0xcdd8bbc2799f944b)
> #Variables: 1'275 (#bools: 625 in objective) (1'275 primary variables)
>   - 625 Booleans in [0,1]
>   - 625 in [0,25]
>   - 25 constants in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24} 
> #kAutomaton: 4
> #kLinear1: 625 (#enforced: 625)
> #kLinear2: 625 (#enforced: 625)
> 
> Starting presolve at 0.01s
> The solution hint is complete and is feasible. Its objective value is 625.
>   1.87e-04s  0.00e+00d  [DetectDominanceRelations] 
>   9.77e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   2.71e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   4.11e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.81e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=78'735 
> [Symmetry] Graph for symmetry has 213'916 nodes and 561'604 arcs.
> [Symmetry] Symmetry computation done. time: 0.0587248 dtime: 0.0919346
> [Symmetry] #generators: 112, average support size: 25.2143
> [Symmetry] The model contains 4 duplicate constraints !
> [Symmetry] 938 orbits on 2313 variables with sizes: 32,24,8,6,6,6,6,6,6,6,...
> [Symmetry] Found orbitope of size 27 x 6
> [SAT presolve] num removable Booleans: 1062 / 58837
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:151963 literals:386901 vars:58710 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0155709s] clauses:151959 literals:386889 vars:58710 one_side_vars:0 simple_definition:5 singleton_clauses:0
> [SAT presolve] [0.0177018s] clauses:151911 literals:386889 vars:58686 one_side_vars:0 simple_definition:5 singleton_clauses:0
>   3.51e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.73e-01s  1.00e+00d *[Probe] #probed=5'232 #equiv=15 #new_binary_clauses=3'117 
>   1.81e-01s  1.00e+00d *[MaxClique] Merged 117'347(234'694 literals) into 66'512(183'860 literals) at_most_ones. 
>   1.52e-02s  0.00e+00d  [DetectDominanceRelations] 
>   7.62e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.29e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.85e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=90 
>   4.29e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.36e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.83e-03s  0.00e+00d  [DetectDifferentVariables] 
>   3.57e-02s  1.84e-03d  [ProcessSetPPC] #relevant_constraints=103'374 #num_inclusions=66'456 
>   3.28e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.24e-02s  2.57e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   3.32e-03s  1.67e-03d  [FindBigVerticalLinearOverlap] 
>   2.18e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   6.95e-03s  4.64e-04d  [MergeClauses] #num_collisions=198 #num_merges=198 #num_saved_literals=420 
>   1.46e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.94e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.46e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.84e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.06e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   3.66e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 212'992 nodes and 449'820 arcs.
> [Symmetry] Symmetry computation done. time: 0.0492245 dtime: 0.101066
> [Symmetry] #generators: 28, average support size: 91.2857
> [Symmetry] 910 orbits on 2188 variables with sizes: 6,6,6,6,6,6,6,6,6,6,...
> [Symmetry] Found orbitope of size 27 x 6
> [SAT presolve] num removable Booleans: 1023 / 58663
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:92412 literals:217022 vars:58125 one_side_vars:0 simple_definition:50927 singleton_clauses:0
> [SAT presolve] [0.00646088s] clauses:92412 literals:217022 vars:58125 one_side_vars:0 simple_definition:50927 singleton_clauses:0
> [SAT presolve] [0.00840976s] clauses:92412 literals:217022 vars:58125 one_side_vars:0 simple_definition:50927 singleton_clauses:0
>   3.88e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.88e-01s  1.00e+00d *[Probe] #probed=5'216 #equiv=42 #new_binary_clauses=3'142 
>   1.38e-01s  7.32e-01d  [MaxClique] Merged 62'164(124'329 literals) into 30'051(92'048 literals) at_most_ones. 
>   1.41e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.40e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.51e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.46e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=84 
>   3.97e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.77e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.10e-03s  0.00e+00d  [DetectDifferentVariables] 
>   3.48e-02s  1.21e-03d  [ProcessSetPPC] #relevant_constraints=66'881 #num_inclusions=30'048 
>   3.53e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.03e-02s  2.50e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.50e-03s  1.05e-03d  [FindBigVerticalLinearOverlap] 
>   2.81e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.13e-03s  2.04e-06d  [MergeClauses] #num_collisions=26 #num_merges=26 #num_saved_literals=76 
>   2.69e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.20e-02s  0.00e+00d  [DetectDominanceRelations] 
>   7.73e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   1.20e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.69e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.43e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   4.05e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=1 
> [Symmetry] Graph for symmetry has 99'108 nodes and 211'584 arcs.
> [Symmetry] Symmetry computation done. time: 0.0213694 dtime: 0.048251
> [Symmetry] #generators: 49, average support size: 62.7755
> [Symmetry] 945 orbits on 2467 variables with sizes: 10,10,10,10,10,10,10,10,10,10,...
> [Symmetry] Found orbitope of size 19 x 10
> [SAT presolve] num removable Booleans: 0 / 58608
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:123 literals:414 vars:125 one_side_vars:5 simple_definition:120 singleton_clauses:0
> [SAT presolve] [8.0573e-05s] clauses:123 literals:414 vars:125 one_side_vars:5 simple_definition:120 singleton_clauses:0
> [SAT presolve] [0.000565432s] clauses:123 literals:414 vars:125 one_side_vars:5 simple_definition:120 singleton_clauses:0
>   4.06e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.93e-01s  1.00e+00d *[Probe] #probed=5'212 #new_binary_clauses=3'058 
>   2.48e-03s  1.15e-04d  [MaxClique] 
>   1.20e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.77e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.52e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.86e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.34e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.69e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.13e-03s  0.00e+00d  [DetectDifferentVariables] 
>   1.58e-02s  6.52e-04d  [ProcessSetPPC] #relevant_constraints=36'817 
>   3.44e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.06e-02s  2.50e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.52e-03s  1.05e-03d  [FindBigVerticalLinearOverlap] 
>   2.89e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.13e-03s  2.04e-06d  [MergeClauses] #num_collisions=26 #num_merges=26 #num_saved_literals=76 
>   1.20e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.68e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.19e-02s  0.00e+00d  [ExpandObjective] #entries=2'724'994 #tight_variables=208'413 #tight_constraints=36'694 #expands=660 
> 
> Presolve summary:
>   - 803 affine relations were detected.
>   - rule 'affine: new relation' was applied 803 times.
>   - rule 'at_most_one: dominated singleton' was applied 1 time.
>   - rule 'at_most_one: resolved two constraints with opposite literal' was applied 4 times.
>   - rule 'at_most_one: size one' was applied 1 time.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'automaton: expanded' was applied 4 times.
>   - rule 'bool_and: x => x' was applied 25 times.
>   - rule 'deductions: 1250 stored' was applied 1 time.
>   - rule 'domination: in exactly one' was applied 4 times.
>   - rule 'dual: fix variable' was applied 14 times.
>   - rule 'duplicate: removed constraint' was applied 78'910 times.
>   - rule 'exactly_one: removed literals' was applied 9 times.
>   - rule 'exactly_one: simplified objective' was applied 2 times.
>   - rule 'exactly_one: singleton' was applied 4 times.
>   - rule 'exactly_one: size two' was applied 5 times.
>   - rule 'exactly_one: x and not(x)' was applied 9 times.
>   - rule 'linear: always true' was applied 1'225 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'225 times.
>   - rule 'linear: fixed or dup variables' was applied 1'225 times.
>   - rule 'linear: remapped using affine relations' was applied 3'725 times.
>   - rule 'new_bool: automaton expansion' was applied 58'212 times.
>   - rule 'objective: expanded via tight equality' was applied 660 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 636 times.
>   - rule 'objective: variable not used elsewhere' was applied 15 times.
>   - rule 'presolve: 44 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 34'326 times.
>   - rule 'setppc: removed dominated constraints' was applied 17 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 625 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'250 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x6392f79123483ccc)
> #Variables: 58'608 (#bools: 847 in objective) (27'226 primary variables)
>   - 58'608 Booleans in [0,1]
> #kBoolAnd: 27 (#enforced: 27 #multi: 25) (#literals: 130)
> #kBoolOr: 69 (#literals: 207)
> #kExactlyOne: 36'694 (#literals: 208'413)
> [Symmetry] Graph for symmetry has 98'229 nodes and 211'584 arcs.
> [Symmetry] Symmetry computation done. time: 0.0209816 dtime: 0.0476242
> [Symmetry] #generators: 47, average support size: 64.8936
> [Symmetry] 945 orbits on 2458 variables with sizes: 10,10,10,10,10,10,10,10,10,10,...
> [Symmetry] Found orbitope of size 19 x 10
> 
> Preloading model.
> #Bound   2.79s best:inf   next:[0,609]    initial_domain
> #1       2.80s best:608   next:[0,607]    complete_hint
> #Model   2.81s var:58608/58608 constraints:36790/36790
> 
> Starting search at 2.82s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2       3.03s best:601   next:[0,600]    rnd_cst_lns (d=5.00e-01 s=9 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3       3.17s best:516   next:[0,515]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base) [hint]
> #4       3.18s best:509   next:[0,508]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: rnd_cst_lns (d=5.00e...]
> #5       3.23s best:375   next:[0,374]    graph_arc_lns (d=5.00e-01 s=11 t=0.10 p=0.00 stall=0 h=base)
> #6       3.58s best:374   next:[0,373]    ls_restart_decay(batch:1 lin{mvs:41 evals:582} #w_updates:12 #perturb:0)
> #7       3.60s best:373   next:[0,372]    ls_lin_restart_perturb(batch:1 lin{mvs:93 evals:872} #w_updates:53 #perturb:0)
> #8       3.60s best:372   next:[0,371]    ls_lin_restart_perturb(batch:1 lin{mvs:89 evals:860} #w_updates:52 #perturb:0)
> #9       3.62s best:371   next:[0,370]    ls_lin_restart_perturb(batch:1 lin{mvs:191 evals:2'603} #w_updates:103 #perturb:0)
> #10      3.71s best:357   next:[0,356]    rnd_var_lns (d=7.07e-01 s=18 t=0.10 p=1.00 stall=1 h=base) [hint]
> #11      3.72s best:354   next:[0,353]    rnd_var_lns (d=7.07e-01 s=18 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: ls_lin_restart_pertu...]
> #12      3.79s best:353   next:[0,352]    no_lp [hint]
> #13      3.86s best:352   next:[0,351]    graph_dec_lns (d=7.07e-01 s=22 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: no_lp [hint]...]
> #Model   3.87s var:58559/58608 constraints:36766/36790
> #14      3.88s best:183   next:[0,182]    graph_cst_lns (d=7.07e-01 s=17 t=0.10 p=1.00 stall=0 h=base)
> #15      4.08s best:163   next:[0,162]    rnd_var_lns (d=8.14e-01 s=32 t=0.10 p=1.00 stall=0 h=base) [hint]
> #16      4.09s best:149   next:[0,148]    rnd_cst_lns (d=8.14e-01 s=33 t=0.10 p=1.00 stall=0 h=base) [hint]
> #17      4.09s best:132   next:[0,131]    rnd_cst_lns (d=8.14e-01 s=33 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=8.14e...]
> #18      4.10s best:131   next:[0,130]    ls_lin_restart_perturb(batch:1 lin{mvs:195 evals:5'120} #w_updates:107 #perturb:0)
> #19      4.19s best:130   next:[0,129]    quick_restart
> #20      4.29s best:129   next:[0,128]    ls_restart_perturb(batch:1 lin{mvs:271 evals:6'299} #w_updates:142 #perturb:0)
> #21      4.30s best:128   next:[0,127]    ls_lin_restart_decay_perturb(batch:1 lin{mvs:77 evals:514} #w_updates:24 #perturb:0)
> #22      4.40s best:113   next:[0,112]    graph_dec_lns (d=8.14e-01 s=38 t=0.10 p=1.00 stall=0 h=base) [hint]
> #23      4.59s best:112   next:[0,111]    graph_arc_lns (d=4.62e-01 s=43 t=0.10 p=0.50 stall=1 h=base) [combined with: graph_dec_lns (d=8.1...]
> #24      4.66s best:100   next:[0,99]     rens_pump_lns (d=5.00e-01 s=30 t=0.10 p=0.00 stall=0 h=base)
> #25      4.70s best:75    next:[0,74]     rins_pump_lns (d=5.00e-01 s=28 t=0.10 p=0.00 stall=0 h=base)
> #26      4.86s best:74    next:[0,73]     ls_restart_perturb(batch:1 lin{mvs:9 evals:83} #w_updates:8 #perturb:0)
> #27      4.92s best:72    next:[0,71]     rnd_cst_lns (d=8.76e-01 s=47 t=0.10 p=1.00 stall=0 h=base) [hint]
> #28      6.09s best:71    next:[0,70]     graph_var_lns (d=3.00e-01 s=78 t=0.10 p=0.40 stall=4 h=base)
> #29      6.10s best:70    next:[0,69]     ls_lin_restart_decay_perturb(batch:1 lin{mvs:49 evals:411} #w_updates:20 #perturb:0)
> #Bound   7.43s best:70    next:[1,69]     bool_core (num_cores=1 [size:11 mw:1 d:4] a=837 d=4 fixed=49/58617 clauses=36'482)
> #Bound   7.73s best:70    next:[2,69]     bool_core (num_cores=2 [size:11 mw:1 d:4] a=827 d=4 fixed=49/58636 clauses=36'503)
> #Bound   8.01s best:70    next:[3,69]     bool_core (num_cores=3 [size:12 mw:1 d:4] a=816 d=4 fixed=49/58656 clauses=36'526)
> #Bound   8.33s best:70    next:[4,69]     bool_core (num_cores=4 [size:11 mw:1 d:4] a=806 d=4 fixed=49/58676 clauses=36'547)
> #Bound   8.67s best:70    next:[5,69]     bool_core (num_cores=5 [size:12 mw:1 d:4] a=795 d=4 fixed=49/58696 clauses=36'586)
> #Bound   9.00s best:70    next:[6,69]     bool_core (num_cores=6 [size:11 mw:1 d:4] a=785 d=4 fixed=49/58716 clauses=36'618)
> #Bound   9.28s best:70    next:[7,69]     bool_core (num_cores=7 [size:11 mw:1 d:4] a=775 d=4 fixed=49/58735 clauses=36'640)
> #Bound   9.62s best:70    next:[8,69]     bool_core (num_cores=8 [size:12 mw:1 d:4] a=764 d=4 fixed=49/58755 clauses=36'663)
> #Bound   9.89s best:70    next:[9,69]     bool_core (num_cores=9 [size:11 mw:1 d:4] a=754 d=4 fixed=49/58775 clauses=36'683)
> #Bound  10.14s best:70    next:[10,69]    bool_core (num_cores=10 [size:11 mw:1 d:4] a=744 d=4 fixed=49/58794 clauses=36'702)
> #Bound  10.47s best:70    next:[11,69]    bool_core (num_cores=11 [size:11 mw:1 d:4] a=734 d=4 fixed=49/58813 clauses=36'722)
> #Bound  10.75s best:70    next:[12,69]    bool_core (num_cores=12 [size:12 mw:1 d:4] a=723 d=4 fixed=49/58833 clauses=36'743)
> #Bound  11.02s best:70    next:[13,69]    bool_core (num_cores=13 [size:11 mw:1 d:4] a=713 d=4 fixed=49/58853 clauses=36'766)
> #Bound  11.37s best:70    next:[14,69]    bool_core (num_cores=14 [size:15 mw:1 amo:1 lit:2 d:4] a=700 d=4 fixed=49/58876 clauses=36'790)
> #Bound  11.68s best:70    next:[15,69]    bool_core (num_cores=15 [size:11 mw:1 d:4] a=690 d=4 fixed=49/58898 clauses=36'818)
> #Bound  11.93s best:70    next:[16,69]    bool_core (num_cores=16 [size:11 mw:1 d:4] a=680 d=4 fixed=49/58917 clauses=36'838)
> #Bound  12.22s best:70    next:[17,69]    bool_core (num_cores=17 [size:12 mw:1 d:4] a=669 d=4 fixed=49/58937 clauses=36'859)
> #30     12.77s best:69    next:[17,68]    quick_restart_no_lp
> #Bound  12.78s best:69    next:[18,68]    bool_core (num_cores=18 [size:22 mw:1 amo:1 lit:11 d:4] a=648 d=4 fixed=49/58959 clauses=36'889)
> #Bound  13.19s best:69    next:[19,68]    bool_core (num_cores=19 [size:17 mw:1 amo:1 lit:2 d:5] a=633 d=5 fixed=49/58985 clauses=36'924)
> #Bound  13.50s best:69    next:[20,68]    bool_core (num_cores=20 [size:12 mw:1 d:4] a=622 d=5 fixed=49/59010 clauses=36'951)
> #Bound  13.81s best:69    next:[21,68]    bool_core (num_cores=21 [size:12 mw:1 d:4] a=611 d=5 fixed=49/59031 clauses=36'972)
> #31     13.83s best:68    next:[21,67]    quick_restart
> #32     14.01s best:66    next:[21,65]    graph_var_lns (d=3.46e-01 s=212 t=0.10 p=0.50 stall=14 h=base)
> #Bound  14.15s best:66    next:[22,65]    bool_core (num_cores=22 [size:16 mw:1 amo:1 lit:2 d:4] a=598 d=5 fixed=49/59056 clauses=36'997)
> #Bound  14.62s best:66    next:[23,65]    bool_core (num_cores=23 [size:21 mw:1 amo:2 lit:8 d:5] a=585 d=5 fixed=49/59085 clauses=37'030)
> #Bound  15.43s best:66    next:[24,65]    bool_core (num_cores=24 [size:34 mw:1 amo:2 lit:20 d:5] a=570 d=5 fixed=49/59115 clauses=37'064)
> #Bound  15.68s best:66    next:[25,65]    bool_core (num_cores=25 [size:11 mw:1 d:4] a=560 d=5 fixed=49/59139 clauses=37'089)
> #Bound  16.11s best:66    next:[26,65]    bool_core (num_cores=26 [size:19 mw:1 amo:2 lit:4 d:5] a=542 d=5 fixed=49/59166 clauses=37'117)
> #Bound  16.60s best:66    next:[27,65]    bool_core (num_cores=27 [size:22 mw:1 amo:2 lit:7 d:5] a=526 d=5 fixed=49/59199 clauses=37'162)
> #Bound  17.08s best:66    next:[28,65]    bool_core (num_cores=28 [size:22 mw:1 amo:2 lit:9 d:5] a=513 d=5 fixed=49/59230 clauses=37'193)
> #Bound  17.79s best:66    next:[29,65]    bool_core (num_cores=29 [size:33 mw:1 amo:1 lit:22 d:4] a=485 d=5 fixed=49/59255 clauses=37'218)
> #Bound  18.08s best:66    next:[30,65]    bool_core (num_cores=30 [size:11 mw:1 d:4] a=475 d=5 fixed=49/59275 clauses=37'238)
> #Bound  18.65s best:66    next:[31,65]    bool_core (num_cores=31 [size:22 mw:1 amo:2 lit:16 d:5] a=469 d=5 fixed=49/59293 clauses=37'266)
> #Bound  19.60s best:66    next:[32,65]    bool_core (num_cores=32 [size:36 mw:1 amo:5 lit:32 d:5] a=452 d=5 fixed=49/59317 clauses=37'343)
> #Bound  20.00s best:66    next:[33,65]    bool_core (num_cores=33 [size:5 mw:1 d:6] a=448 d=6 fixed=49/59333 clauses=37'435)
> #Bound  20.25s best:66    next:[34,65]    bool_core (num_cores=34 [size:6 mw:1 d:6] a=443 d=6 fixed=49/59354 clauses=37'511)
> #Bound  20.40s best:66    next:[35,65]    bool_core (num_cores=35 [size:2 mw:1 d:5] a=442 d=6 fixed=49/59373 clauses=37'580)
> #Bound  20.90s best:66    next:[36,65]    bool_core (num_cores=36 [size:16 mw:1 amo:2 lit:4 d:6] a=427 d=6 fixed=49/59393 clauses=37'635)
> #Bound  21.24s best:66    next:[37,65]    bool_core (num_cores=37 [size:8 mw:1 d:5] a=420 d=6 fixed=49/59422 clauses=37'718)
> #Bound  21.41s best:66    next:[38,65]    bool_core (num_cores=38 [size:4 mw:1 d:5] a=417 d=6 fixed=49/59436 clauses=37'762)
> #Bound  22.18s best:66    next:[39,65]    bool_core (num_cores=39 [size:21 mw:1 amo:2 lit:19 d:6] a=414 d=6 fixed=49/59448 clauses=37'889)
> #Bound  22.47s best:66    next:[40,65]    bool_core (num_cores=40 [size:4 mw:1 d:6] a=411 d=6 fixed=49/59460 clauses=37'977)
> #Bound  22.68s best:66    next:[41,65]    bool_core (num_cores=41 [size:2 mw:1 d:6] a=410 d=6 fixed=49/59473 clauses=38'090)
> #33     22.78s best:64    next:[41,63]    graph_arc_lns (d=3.81e-01 s=380 t=0.10 p=0.50 stall=25 h=base)
> #Bound  23.48s best:64    next:[42,63]    bool_core (num_cores=42 [size:12 mw:1 amo:1 lit:7 d:7] a=399 d=7 fixed=49/59485 clauses=38'255)
> #Bound  24.05s best:64    next:[43,63]    bool_core (num_cores=43 [size:15 mw:1 amo:2 lit:14 d:5] a=397 d=7 fixed=49/59513 clauses=38'367)
> #Bound  24.97s best:64    next:[44,63]    bool_core (num_cores=44 [size:21 mw:1 amo:2 lit:14 d:8] a=390 d=8 fixed=49/59531 clauses=38'534)
> #Bound  26.10s best:64    next:[45,63]    bool_core (num_cores=45 [size:8 mw:1 d:9] a=383 d=9 fixed=49/59573 clauses=38'931)
> #Bound  33.52s best:64    next:[46,63]    bool_core (num_cores=46 [size:2 mw:1 d:10] a=382 d=10 fixed=49/59607 clauses=42'355)
> #Bound  37.49s best:64    next:[47,63]    bool_core (num_cores=47 [size:4 mw:1 d:11] a=379 d=11 fixed=49/59637 clauses=44'016)
> #Bound  38.92s best:64    next:[48,63]    bool_core (num_cores=48 [size:22 mw:1 amo:2 lit:20 d:6] a=368 d=11 fixed=49/59680 clauses=44'509)
> #Bound  39.93s best:64    next:[49,63]    bool_core (num_cores=49 [size:2 mw:1 d:7] a=367 d=11 fixed=49/59693 clauses=44'959)
> #Bound  54.07s best:64    next:[50,63]    bool_core (num_cores=50 [size:2 mw:1 d:12] a=366 d=12 fixed=49/59711 clauses=48'207)
> #Bound  85.48s best:64    next:[51,63]    bool_core (num_cores=51 [size:3 mw:1 d:13] a=364 d=13 fixed=49/59755 clauses=53'557)
> #Bound  95.19s best:64    next:[52,63]    bool_core (num_cores=52 [size:17 mw:1 amo:2 lit:10 d:9] a=353 d=13 fixed=49/59805 clauses=52'325)
> #Bound  96.69s best:64    next:[53,63]    bool_core (num_cores=53 [size:111 mw:1 amo:9 lit:67 d:10] a=257 d=13 fixed=49/59919 clauses=53'206)
> #Bound 112.98s best:64    next:[54,63]    bool_core (num_cores=54 [size:1 mw:1] a=257 d=13 fixed=49/60073 clauses=54'991)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.22m,    1.22m]    1.22m   0.00ns    1.22m
>            'default_lp':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.25m,    1.25m]    1.25m   0.00ns    1.25m
>      'feasibility_pump':       508 [ 62.39us, 349.33ms] 885.13us  15.48ms 449.65ms       507 [  4.34us,   4.34us]   4.34us   0.00ns   2.20ms
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':       205 [ 77.83ms, 573.17ms] 247.69ms 102.05ms   50.78s       205 [ 10.00ns, 106.43ms]  59.37ms  46.16ms   12.17s
>         'graph_cst_lns':       125 [100.60ms, 749.14ms] 414.25ms 142.55ms   51.78s       125 [ 10.00ns, 102.63ms]  55.22ms  47.64ms    6.90s
>         'graph_dec_lns':        77 [201.62ms,    1.11s] 685.55ms 182.75ms   52.79s        77 [ 10.00ns, 102.43ms]  53.03ms  45.30ms    4.08s
>         'graph_var_lns':       217 [ 60.84ms, 616.28ms] 236.81ms 106.18ms   51.39s       214 [ 10.00ns, 106.65ms]  59.93ms  46.14ms   12.83s
>                    'ls':       275 [  8.62ms, 318.45ms] 185.33ms  58.15ms   50.97s       275 [113.28us, 101.10ms]  98.38ms  12.22ms   27.05s
>                'ls_lin':       288 [  8.49ms, 396.19ms] 177.19ms  62.64ms   51.03s       288 [103.82us, 101.04ms]  97.69ms  15.17ms   28.13s
>            'max_lp_sym':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  33.96s,   33.96s]   33.96s   0.00ns   33.96s
>                 'no_lp':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.45m,    1.45m]    1.45m   0.00ns    1.45m
>          'pseudo_costs':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  23.68s,   23.68s]   23.68s   0.00ns   23.68s
>         'quick_restart':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.02m,    1.02m]    1.02m   0.00ns    1.02m
>   'quick_restart_no_lp':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  52.26s,   52.26s]   52.26s   0.00ns   52.26s
>         'reduced_costs':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  25.41s,   25.41s]   25.41s   0.00ns   25.41s
>             'rins/rens':        97 [ 19.89ms,    1.19s] 539.39ms 458.95ms   52.32s        76 [ 10.00ns, 102.52ms]  71.25ms  45.48ms    5.42s
>           'rnd_cst_lns':        85 [188.52ms,    1.01s] 628.57ms 168.06ms   53.43s        85 [ 10.00ns, 102.47ms]  51.02ms  46.31ms    4.34s
>           'rnd_var_lns':        84 [184.44ms, 950.72ms] 628.44ms 166.54ms   52.79s        84 [ 10.00ns, 102.40ms]  53.62ms  46.07ms    4.50s
> 
> Search stats               Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  60'188     42'022    792'406    11'738  485'108'438      2'164'962
>            'default_lp':  58'608    166'180    378'506     9'088  241'591'568     19'517'012
>             'fs_random':       0          0          0         0            0              0
>       'fs_random_no_lp':       0          0          0         0            0              0
>            'max_lp_sym':  58'608        103     92'529     7'905   45'218'302     45'379'790
>                 'no_lp':  58'608    165'341    426'725    11'030  286'752'161     27'034'703
>          'pseudo_costs':  58'608      3'718     50'368     6'421   44'916'957     36'924'611
>         'quick_restart':  58'608     37'124  1'293'988    12'453  383'090'002      9'168'830
>   'quick_restart_no_lp':  58'608     31'648  1'153'713    11'917  320'521'022      7'228'794
>         'reduced_costs':  58'608        573     98'214     8'099   47'983'834     47'688'670
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        36'870   2'694'200   6'201'116     3'040'673        59     5'160      89'888         0      1'752       30'781      651
>            'default_lp':       116'618   1'951'180  29'209'265    25'866'841       779     4'282      73'360         0      1'337       22'889      472
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':            94       5'798      32'370             0         0     2'922      56'548         0        726       13'705      116
>                 'no_lp':       112'243     945'159  28'293'981    26'430'722       383     6'697     108'711         0      2'358       39'201    1'022
>          'pseudo_costs':         3'590     120'016   1'155'095             0         2     1'330      30'418         0        324        7'376        0
>         'quick_restart':        23'347     207'817   4'225'979     2'353'125       128     4'297      73'614         0      1'304       21'831      496
>   'quick_restart_no_lp':        20'437     187'874   3'646'501     2'381'082       106     4'279      73'274         0      1'336       22'503      502
>         'reduced_costs':           543      71'421     435'054             0         0     3'143      58'050         0        810       14'867      206
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         28           0          0  551'324        0        0
>      'max_lp_sym':          1      34'620          0        0      875        0
>    'pseudo_costs':          1      97'603        279      393    9'291        0
>   'quick_restart':         28           0          0  446'411        0        0
>   'reduced_costs':          1      78'385        555      408    6'140        0
> 
> Lp dimension               Final dimension of first component
>      'default_lp':              0 rows, 22 columns, 0 entries
>      'max_lp_sym':  35579 rows, 57095 columns, 203288 entries
>    'pseudo_costs':   12671 rows, 58608 columns, 54921 entries
>   'quick_restart':              0 rows, 22 columns, 0 entries
>   'reduced_costs':   19302 rows, 58608 columns, 88305 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>      'max_lp_sym':          0            0     857         0       0           0
>    'pseudo_costs':          0            0   2'146         0  11'154           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0   2'731         0   7'972           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':          100        0        0       0          0      0             0        0/0
>      'max_lp_sym':       35'579        0        0       0          0      0             0        0/0
>    'pseudo_costs':       37'070        0      174       0        102      0             0  279/1'224
>   'quick_restart':          100        0        0       0          0      0             0        0/0
>   'reduced_costs':       37'346        0      294       0        102      0             0  555/1'464
> 
> Lp Cut           pseudo_costs  reduced_costs
>          CG_FF:            72             53
>           CG_K:             -             23
>           CG_R:             -             20
>         Clique:            36             30
>      MIR_1_RLT:            56             18
>       MIR_3_FF:             5              -
>       MIR_4_FF:             6              -
>   ZERO_HALF_FF:           104            300
>    ZERO_HALF_R:             -            111
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':         4/205     49%    2.83e-01       0.11
>   'graph_cst_lns':         4/125     50%    6.32e-01       0.10
>   'graph_dec_lns':          3/77     57%    9.86e-01       0.10
>   'graph_var_lns':         3/214     50%    2.79e-01       0.11
>       'rins/rens':          3/77     30%    5.91e-04       0.10
>     'rnd_cst_lns':          4/85     59%    9.90e-01       0.10
>     'rnd_var_lns':          3/84     56%    9.84e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                          'ls_lin_restart':       39                 21  1'728'455         0              0          0         22'946        934'164
>                 'ls_lin_restart_compound':       51                 23          0   796'389         51'627    372'341          4'592     17'430'981
>         'ls_lin_restart_compound_perturb':       40                 20          0   574'345         29'734    272'253          3'936     13'703'927
>                    'ls_lin_restart_decay':       26                 18  1'137'444         0              0          0          1'893      1'449'357
>           'ls_lin_restart_decay_compound':       37                 16          0   621'946        196'006    212'922            721     12'761'349
>   'ls_lin_restart_decay_compound_perturb':       38                 20          0   561'250        182'830    189'139            911     12'858'839
>            'ls_lin_restart_decay_perturb':       38                 21  1'543'299         0              0          0          2'174      1'936'076
>                  'ls_lin_restart_perturb':       19                 15    674'655         0              0          0         11'904        372'066
>                              'ls_restart':       33                 17  1'403'132         0              0          0         15'153        821'154
>                     'ls_restart_compound':       17                 13          0   204'173         10'526     96'791          1'616      5'523'183
>             'ls_restart_compound_perturb':       36                 16          0   562'685         35'600    263'512          3'177     12'522'788
>                        'ls_restart_decay':       45                 21  1'920'674         0              0          0          2'420      2'431'840
>               'ls_restart_decay_compound':       44                 22          0   647'667        210'867    218'358          1'035     14'812'262
>       'ls_restart_decay_compound_perturb':       53                 28          0   741'225        250'531    245'244          1'258     17'562'102
>                'ls_restart_decay_perturb':       27                 17  1'184'928         0              0          0          1'882      1'502'798
>                      'ls_restart_perturb':       20                 15    768'149         0              0          0         12'121        445'477
> 
> Solutions (33)                     Num     Rank
>                  'complete_hint':    1    [1,1]
>                  'graph_arc_lns':    3   [5,33]
>                  'graph_cst_lns':    3   [3,14]
>                  'graph_dec_lns':    2  [13,22]
>                  'graph_var_lns':    2  [28,32]
>   'ls_lin_restart_decay_perturb':    2  [21,29]
>         'ls_lin_restart_perturb':    4   [7,18]
>               'ls_restart_decay':    1    [6,6]
>             'ls_restart_perturb':    2  [20,26]
>                          'no_lp':    1  [12,12]
>                  'quick_restart':    2  [19,31]
>            'quick_restart_no_lp':    1  [30,30]
>                  'rens_pump_lns':    1  [24,24]
>                  'rins_pump_lns':    1  [25,25]
>                    'rnd_cst_lns':    4   [2,27]
>                    'rnd_var_lns':    3  [10,15]
> 
> Objective bounds     Num
>        'bool_core':   54
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    713    2'144      477
>    'fj solution hints':      0        0        0
>         'lp solutions':    159       43      156
>                 'pump':    507       54
> 
> Improving bounds shared    Num  Sym
>                   'core':   49    0
> 
> Clauses shared                Num
>                  'core':   13'822
>            'default_lp':   72'413
>            'max_lp_sym':    9'822
>                 'no_lp':  245'265
>          'pseudo_costs':   89'068
>         'quick_restart':   21'332
>   'quick_restart_no_lp':   10'855
>         'reduced_costs':   88'222
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 64
> best_bound: 54
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.092
> usertime: 120.092
> deterministic_time: 542.307
> gap_integral: 1295.96
> solution_fingerprint: 0xf7fbca22da326429
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
> Initial optimization model '': (model_fingerprint: 0xc7a082dbe57f8289)
> #Variables: 1'326 (#bools: 650 in objective) (1'326 primary variables)
>   - 650 Booleans in [0,1]
>   - 650 in [0,26]
>   - 26 constants in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25} 
> #kAutomaton: 8
> #kLinear1: 650 (#enforced: 650)
> #kLinear2: 650 (#enforced: 650)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 650.
>   2.48e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.40e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.14e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   2.13e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   4.57e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=177'015 
> [Symmetry] Graph for symmetry has 474'700 nodes and 1'254'896 arcs.
> [Symmetry] Symmetry computation done. time: 0.166773 dtime: 0.197962
> [Symmetry] #generators: 214, average support size: 8.37383
> [Symmetry] The model contains 8 duplicate constraints !
> [Symmetry] 649 orbits on 1482 variables with sizes: 56,32,8,7,7,7,7,7,7,7,...
> [Symmetry] Found orbitope of size 9 x 2
> [SAT presolve] num removable Booleans: 2272 / 130988
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:339266 literals:865092 vars:130733 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0463272s] clauses:339258 literals:865068 vars:130733 one_side_vars:0 simple_definition:9 singleton_clauses:0
> [SAT presolve] [0.0515367s] clauses:339136 literals:865068 vars:130672 one_side_vars:0 simple_definition:9 singleton_clauses:0
>   1.13e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.55e-01s  1.00e+00d *[Probe] #probed=4'870 #equiv=16 #new_binary_clauses=3'832 
>   2.48e-01s  1.00e+00d *[MaxClique] Merged 262'604(525'208 literals) into 233'306(495'911 literals) at_most_ones. 
>   3.79e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.01e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.40e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.50e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=96 
>   1.36e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.47e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   4.32e-03s  0.00e+00d  [DetectDifferentVariables] 
>   1.08e-01s  6.32e-03d  [ProcessSetPPC] #relevant_constraints=314'699 #num_inclusions=233'250 
>   5.81e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.08e-02s  5.03e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   9.90e-03s  4.64e-03d  [FindBigVerticalLinearOverlap] 
>   4.66e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.92e-02s  1.52e-03d  [MergeClauses] #num_collisions=391 #num_merges=391 #num_saved_literals=843 
>   3.75e-02s  0.00e+00d  [DetectDominanceRelations] 
>   9.67e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.82e-02s  0.00e+00d  [DetectDominanceRelations] 
>   9.79e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.07e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   8.38e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=3 
> [Symmetry] Graph for symmetry has 473'771 nodes and 1'187'442 arcs.
> [Symmetry] Symmetry computation done. time: 0.154554 dtime: 0.205635
> [Symmetry] #generators: 5, average support size: 246
> [Symmetry] 615 orbits on 1230 variables with sizes: 2,2,2,2,2,2,2,2,2,2,...
> [SAT presolve] num removable Booleans: 2195 / 130637
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:302948 literals:763359 vars:130425 one_side_vars:0 simple_definition:30131 singleton_clauses:0
> [SAT presolve] [0.0361358s] clauses:302948 literals:763359 vars:130425 one_side_vars:0 simple_definition:30131 singleton_clauses:0
> [SAT presolve] [0.0420595s] clauses:302948 literals:763359 vars:130425 one_side_vars:0 simple_definition:30131 singleton_clauses:0
>   9.29e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.73e-01s  1.00e+00d *[Probe] #probed=4'850 #equiv=76 #new_binary_clauses=3'923 
>   2.43e-01s  1.00e+00d *[MaxClique] Merged 229'844(459'694 literals) into 190'970(420'793 literals) at_most_ones. 
>   8.59e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.86e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.35e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   3.81e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.61e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=428 
>   1.53e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   6.96e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   6.44e-03s  0.00e+00d  [DetectDifferentVariables] 
>   9.70e-02s  5.01e-03d  [ProcessSetPPC] #relevant_constraints=271'974 #num_inclusions=190'686 
>   7.06e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.36e-02s  5.61e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   9.46e-03s  4.22e-03d  [FindBigVerticalLinearOverlap] 
>   5.92e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.02e-02s  1.30e-03d  [MergeClauses] #num_collisions=239 #num_merges=239 #num_saved_literals=539 
>   3.88e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.02e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.87e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.00e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.14e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   1.11e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 473'270 nodes and 1'104'329 arcs.
> [Symmetry] Symmetry computation done. time: 0.152539 dtime: 0.210943
> [Symmetry] #generators: 22, average support size: 67.0909
> [Symmetry] 709 orbits on 1439 variables with sizes: 6,6,6,6,3,3,3,3,3,2,...
> [Symmetry] Found orbitope of size 4 x 2
> [SAT presolve] num removable Booleans: 2127 / 130558
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:259505 literals:637468 vars:130113 one_side_vars:0 simple_definition:68225 singleton_clauses:0
> [SAT presolve] [0.0290106s] clauses:259505 literals:637468 vars:130113 one_side_vars:0 simple_definition:68225 singleton_clauses:0
> [SAT presolve] [0.0355443s] clauses:259503 literals:637464 vars:130112 one_side_vars:0 simple_definition:68224 singleton_clauses:0
>   1.07e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.76e-01s  1.00e+00d *[Probe] #probed=4'852 #new_binary_clauses=3'771 
>   2.33e-01s  1.00e+00d *[MaxClique] Merged 188'618(377'236 literals) into 137'927(326'546 literals) at_most_ones. 
>   8.35e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.85e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.33e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   4.08e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.54e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.44e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.09e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   6.58e-03s  0.00e+00d  [DetectDifferentVariables] 
>   8.80e-02s  3.60e-03d  [ProcessSetPPC] #relevant_constraints=219'201 #num_inclusions=137'917 
>   8.05e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.33e-02s  6.11e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   8.31e-03s  3.66e-03d  [FindBigVerticalLinearOverlap] 
>   7.76e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.04e-02s  9.94e-04d  [MergeClauses] #num_collisions=239 #num_merges=239 #num_saved_literals=539 
>   3.85e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.04e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.05e-02s  0.00e+00d  [ExpandObjective] #entries=6'208'240 #tight_variables=268'223 #tight_constraints=15'747 #expands=635 
> 
> Presolve summary:
>   - 996 affine relations were detected.
>   - rule 'affine: new relation' was applied 996 times.
>   - rule 'at_most_one: dominated singleton' was applied 1 time.
>   - rule 'at_most_one: removed literals' was applied 6 times.
>   - rule 'at_most_one: resolved two constraints with opposite literal' was applied 5 times.
>   - rule 'at_most_one: size one' was applied 1 time.
>   - rule 'at_most_one: transformed into max clique.' was applied 3 times.
>   - rule 'automaton: expanded' was applied 8 times.
>   - rule 'bool_and: x => x' was applied 25 times.
>   - rule 'bool_or: implications' was applied 8 times.
>   - rule 'deductions: 1300 stored' was applied 1 time.
>   - rule 'domination: in exactly one' was applied 6 times.
>   - rule 'dual: fix variable' was applied 11 times.
>   - rule 'duplicate: removed constraint' was applied 177'542 times.
>   - rule 'exactly_one: removed literals' was applied 11 times.
>   - rule 'exactly_one: simplified objective' was applied 3 times.
>   - rule 'exactly_one: singleton' was applied 8 times.
>   - rule 'exactly_one: size two' was applied 3 times.
>   - rule 'linear: always true' was applied 1'275 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'275 times.
>   - rule 'linear: fixed or dup variables' was applied 1'275 times.
>   - rule 'linear: remapped using affine relations' was applied 6'475 times.
>   - rule 'new_bool: automaton expansion' was applied 130'338 times.
>   - rule 'objective: expanded via tight equality' was applied 635 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 632 times.
>   - rule 'objective: variable not used elsewhere' was applied 12 times.
>   - rule 'presolve: 44 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 10'809 times.
>   - rule 'setppc: removed dominated constraints' was applied 35 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 650 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'300 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x235a60ea732fc007)
> #Variables: 130'549 (#bools: 638 in objective) (120'019 primary variables)
>   - 130'549 Booleans in [0,1]
> #kBoolAnd: 4'947 (#enforced: 4'947 #multi: 237) (#literals: 138'295)
> #kBoolOr: 65'049 (#literals: 197'266)
> #kExactlyOne: 15'747 (#literals: 268'223)
> [Symmetry] Graph for symmetry has 468'570 nodes and 988'628 arcs.
> [Symmetry] Symmetry computation done. time: 0.143205 dtime: 0.20938
> [Symmetry] #generators: 24, average support size: 65.4167
> [Symmetry] The model contains 2 duplicate constraints !
> [Symmetry] 727 orbits on 1496 variables with sizes: 8,8,8,8,4,4,4,4,4,4,...
> [Symmetry] Found orbitope of size 4 x 2
> 
> Preloading model.
> #Bound   6.60s best:inf   next:[0,636]    initial_domain
> #1       6.61s best:635   next:[0,634]    complete_hint
> #Model   6.66s var:130549/130549 constraints:85743/85743
> 
> Starting search at 6.67s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2       7.04s best:633   next:[0,632]    rnd_cst_lns (d=5.00e-01 s=9 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3       7.42s best:597   next:[0,596]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base)
> #4       7.43s best:595   next:[0,594]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base) [combined with: rnd_cst_lns (d=5.00e...]
> #5       7.47s best:593   next:[0,592]    graph_dec_lns (d=5.00e-01 s=13 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: graph_cst_lns (d=5.0...]
> #6       7.52s best:484   next:[0,483]    graph_var_lns (d=5.00e-01 s=10 t=0.10 p=0.00 stall=0 h=base)
> #7       7.74s best:453   next:[0,452]    graph_arc_lns (d=5.00e-01 s=11 t=0.10 p=0.00 stall=0 h=base)
> #8       7.99s best:452   next:[0,451]    ls_lin_restart_perturb(batch:1 lin{mvs:3 evals:457} #w_updates:3 #perturb:0)
> #9       8.02s best:451   next:[0,450]    ls_lin_restart_decay(batch:1 lin{mvs:6 evals:462} #w_updates:3 #perturb:0)
> #10      8.03s best:450   next:[0,449]    ls_restart(batch:1 lin{mvs:6 evals:462} #w_updates:6 #perturb:0) [combined with: ls_lin_restart_decay...]
> #11      8.21s best:448   next:[0,447]    rnd_var_lns (d=7.07e-01 s=17 t=0.10 p=1.00 stall=1 h=base) [hint]
> #12      8.25s best:443   next:[0,442]    rnd_cst_lns (d=7.07e-01 s=18 t=0.10 p=1.00 stall=0 h=base) [hint]
> #13      8.26s best:441   next:[0,440]    rnd_cst_lns (d=7.07e-01 s=18 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=7.07e...]
> #Bound   8.32s best:441   next:[1,440]    bool_core (num_cores=1 [size:11 mw:1 d:4] a=628 d=4 fixed=0/130558 clauses=81'281)
> #14      8.42s best:440   next:[1,439]    no_lp
> #Model   8.59s var:130394/130549 constraints:85663/85743
> #15      8.80s best:439   next:[1,438]    quick_restart_no_lp [hint]
> #16      9.12s best:436   next:[1,435]    graph_cst_lns (d=7.07e-01 s=33 t=0.10 p=1.00 stall=0 h=base) [hint]
> #17      9.15s best:435   next:[1,434]    ls_restart_perturb(batch:1 lin{mvs:13 evals:455} #w_updates:10 #perturb:0)
> #18      9.47s best:434   next:[1,433]    ls_restart(batch:1 lin{mvs:15 evals:466} #w_updates:11 #perturb:0)
> #19      9.76s best:421   next:[1,420]    rnd_var_lns (d=8.14e-01 s=41 t=0.10 p=1.00 stall=0 h=base) [hint]
> #20      9.77s best:420   next:[1,419]    rnd_var_lns (d=8.14e-01 s=41 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: ls_restart(batch:1 l...]
> #21      9.79s best:419   next:[1,418]    ls_restart_decay(batch:1 lin{mvs:15 evals:454} #w_updates:9 #perturb:0)
> #22      9.81s best:418   next:[1,417]    ls_lin_restart_perturb(batch:1 lin{mvs:19 evals:471} #w_updates:14 #perturb:0)
> #23      9.93s best:404   next:[1,403]    rnd_cst_lns (d=8.14e-01 s=44 t=0.10 p=1.00 stall=0 h=base) [hint]
> #24      9.94s best:389   next:[1,388]    rnd_cst_lns (d=8.14e-01 s=44 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: ls_lin_restart_pertu...]
> #25     10.11s best:388   next:[1,387]    ls_restart_decay(batch:1 lin{mvs:81 evals:1'342} #w_updates:29 #perturb:0)
> #26     10.14s best:387   next:[1,386]    ls_restart(batch:1 lin{mvs:47 evals:1'100} #w_updates:30 #perturb:0)
> #27     10.61s best:386   next:[1,385]    ls_restart_decay_perturb(batch:1 lin{mvs:49 evals:746} #w_updates:20 #perturb:0)
> #28     10.76s best:382   next:[1,381]    graph_dec_lns (d=8.14e-01 s=55 t=0.10 p=1.00 stall=1 h=base) [hint]
> #29     10.77s best:381   next:[1,380]    graph_dec_lns (d=8.14e-01 s=55 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: ls_restart_decay_per...]
> #30     10.94s best:380   next:[1,379]    default_lp
> #31     10.96s best:379   next:[1,378]    default_lp
> #32     10.99s best:378   next:[1,377]    default_lp
> #33     11.02s best:377   next:[1,376]    default_lp
> #34     11.05s best:376   next:[1,375]    default_lp
> #35     11.09s best:375   next:[1,374]    default_lp
> #36     11.15s best:279   next:[1,278]    default_lp
> #37     11.18s best:278   next:[1,277]    default_lp
> #38     11.20s best:277   next:[1,276]    ls_lin_restart_decay_compound(batch:1 lin{mvs:0 evals:818} gen{mvs:8 evals:0} comp{mvs:2 btracks:3} #w_updates:0 #perturb:0) [combined with: default_lp...]
> #39     11.25s best:276   next:[1,275]    default_lp
> #40     11.28s best:275   next:[1,274]    default_lp
> #41     11.32s best:274   next:[1,273]    default_lp
> #42     11.35s best:273   next:[1,272]    default_lp
> #43     11.38s best:272   next:[1,271]    default_lp
> #44     11.41s best:271   next:[1,270]    default_lp
> #45     11.44s best:270   next:[1,269]    default_lp
> #46     11.46s best:269   next:[1,268]    ls_restart_perturb(batch:1 lin{mvs:357 evals:650} #w_updates:361 #perturb:0) [combined with: default_lp...]
> #47     11.50s best:268   next:[1,267]    default_lp
> #48     11.54s best:267   next:[1,266]    default_lp
> #49     11.57s best:266   next:[1,265]    default_lp
> #50     11.60s best:265   next:[1,264]    default_lp
> #51     11.63s best:264   next:[1,263]    default_lp
> #52     11.67s best:263   next:[1,262]    default_lp
> #53     11.71s best:262   next:[1,261]    default_lp
> #54     11.72s best:139   next:[1,138]    quick_restart
> #55     11.78s best:136   next:[1,135]    quick_restart
> #Bound  11.82s best:136   next:[2,135]    bool_core (num_cores=2 [size:11 mw:1 d:4] a=618 d=4 fixed=155/130577 clauses=80'972)
> #56     11.91s best:135   next:[2,134]    default_lp
> #57     11.97s best:134   next:[2,133]    default_lp
> #58     12.03s best:133   next:[2,132]    default_lp
> #59     12.07s best:132   next:[2,131]    default_lp
> #60     12.11s best:131   next:[2,130]    default_lp
> #61     12.15s best:130   next:[2,129]    default_lp
> #62     12.20s best:129   next:[2,128]    default_lp
> #63     12.23s best:128   next:[2,127]    default_lp
> #64     12.28s best:127   next:[2,126]    default_lp
> #65     12.33s best:126   next:[2,125]    default_lp
> #66     12.39s best:125   next:[2,124]    default_lp
> #67     12.43s best:124   next:[2,123]    default_lp
> #68     12.47s best:123   next:[2,122]    default_lp
> #69     12.51s best:122   next:[2,121]    default_lp
> #Bound  12.54s best:122   next:[3,121]    bool_core (num_cores=3 [size:12 mw:1 d:4] a=607 d=4 fixed=155/130597 clauses=80'993)
> #70     12.55s best:121   next:[3,120]    default_lp
> #71     12.59s best:120   next:[3,119]    default_lp
> #72     12.63s best:119   next:[3,118]    default_lp
> #73     12.68s best:118   next:[3,117]    default_lp
> #Bound  13.19s best:118   next:[4,117]    bool_core (num_cores=4 [size:12 mw:1 d:4] a=596 d=4 fixed=155/130618 clauses=81'018)
> #Bound  13.82s best:118   next:[5,117]    bool_core (num_cores=5 [size:11 mw:1 d:4] a=586 d=4 fixed=155/130638 clauses=81'038)
> #Bound  14.57s best:118   next:[6,117]    bool_core (num_cores=6 [size:14 mw:1 d:4] a=573 d=4 fixed=155/130660 clauses=81'064)
> #Bound  15.24s best:118   next:[7,117]    bool_core (num_cores=7 [size:13 mw:1 d:4] a=561 d=4 fixed=155/130684 clauses=81'091)
> #Bound  15.88s best:118   next:[8,117]    bool_core (num_cores=8 [size:11 mw:1 d:4] a=551 d=4 fixed=155/130705 clauses=81'117)
> #74     16.52s best:116   next:[8,115]    graph_arc_lns (d=2.13e-01 s=118 t=0.10 p=0.25 stall=3 h=base)
> #Bound  16.70s best:116   next:[9,115]    bool_core (num_cores=9 [size:13 mw:1 d:4] a=539 d=4 fixed=155/130726 clauses=81'139)
> #Bound  17.66s best:116   next:[10,115]   bool_core (num_cores=10 [size:17 mw:1 d:5] a=523 d=5 fixed=155/130753 clauses=81'171)
> #75     17.98s best:115   next:[10,114]   graph_cst_lns (d=9.14e-01 s=120 t=0.10 p=1.00 stall=1 h=base) [combined with: graph_arc_lns (d=2.1...]
> #Bound  18.40s best:115   next:[11,114]   bool_core (num_cores=11 [size:11 mw:1 d:4] a=513 d=5 fixed=155/130778 clauses=81'198)
> #Bound  19.12s best:115   next:[12,114]   bool_core (num_cores=12 [size:12 mw:1 d:4] a=502 d=5 fixed=155/130798 clauses=81'222)
> #Bound  19.91s best:115   next:[13,114]   bool_core (num_cores=13 [size:13 mw:1 d:4] a=490 d=5 fixed=155/130820 clauses=81'247)
> #Bound  20.51s best:115   next:[14,114]   bool_core (num_cores=14 [size:11 mw:1 d:4] a=480 d=5 fixed=155/130841 clauses=81'270)
> #76     21.08s best:114   next:[14,113]   graph_dec_lns (d=9.56e-01 s=164 t=0.10 p=1.00 stall=3 h=base)
> #Bound  21.28s best:114   next:[15,113]   bool_core (num_cores=15 [size:14 mw:1 d:4] a=467 d=5 fixed=155/130863 clauses=81'293)
> #Bound  21.94s best:114   next:[16,113]   bool_core (num_cores=16 [size:11 mw:1 d:4] a=457 d=5 fixed=155/130885 clauses=81'318)
> #Bound  22.61s best:114   next:[17,113]   bool_core (num_cores=17 [size:11 mw:1 d:4] a=447 d=5 fixed=155/130904 clauses=81'339)
> #Bound  23.44s best:114   next:[18,113]   bool_core (num_cores=18 [size:15 mw:1 d:4] a=433 d=5 fixed=155/130927 clauses=81'365)
> #Bound  24.10s best:114   next:[19,113]   bool_core (num_cores=19 [size:11 mw:1 d:4] a=423 d=5 fixed=155/130950 clauses=81'391)
> #77     24.32s best:113   next:[19,112]   graph_cst_lns (d=8.34e-01 s=204 t=0.10 p=0.67 stall=1 h=base)
> #Bound  24.74s best:113   next:[20,112]   bool_core (num_cores=20 [size:11 mw:1 d:4] a=413 d=5 fixed=155/130969 clauses=81'415)
> #Bound  25.41s best:113   next:[21,112]   bool_core (num_cores=21 [size:13 mw:1 d:4] a=401 d=5 fixed=155/130990 clauses=81'441)
> #Bound  26.01s best:113   next:[22,112]   bool_core (num_cores=22 [size:11 mw:1 d:4] a=391 d=5 fixed=155/131011 clauses=81'467)
> #Bound  26.61s best:113   next:[23,112]   bool_core (num_cores=23 [size:11 mw:1 d:4] a=381 d=5 fixed=155/131030 clauses=81'487)
> #Bound  27.28s best:113   next:[24,112]   bool_core (num_cores=24 [size:12 mw:1 d:4] a=370 d=5 fixed=155/131050 clauses=81'511)
> #Bound  28.11s best:113   next:[25,112]   bool_core (num_cores=25 [size:15 mw:1 d:4] a=356 d=5 fixed=155/131074 clauses=81'540)
> #Bound  28.72s best:113   next:[26,112]   bool_core (num_cores=26 [size:12 mw:1 d:4] a=345 d=5 fixed=155/131098 clauses=81'565)
> #Bound  29.57s best:113   next:[27,112]   bool_core (num_cores=27 [size:17 mw:1 d:5] a=329 d=5 fixed=155/131124 clauses=81'592)
> #Bound  30.26s best:113   next:[28,112]   bool_core (num_cores=28 [size:13 mw:1 d:4] a=317 d=5 fixed=155/131151 clauses=81'626)
> #Bound  30.96s best:113   next:[29,112]   bool_core (num_cores=29 [size:14 mw:1 d:4] a=304 d=5 fixed=155/131175 clauses=81'654)
> #Bound  31.58s best:113   next:[30,112]   bool_core (num_cores=30 [size:13 mw:1 d:4] a=292 d=5 fixed=155/131199 clauses=81'681)
> #Bound  32.02s best:113   next:[31,112]   bool_core (num_cores=31 [size:6 mw:1 d:5] a=287 d=5 fixed=155/131215 clauses=81'717)
> #Bound  32.60s best:113   next:[32,112]   bool_core (num_cores=32 [size:11 mw:1 d:4] a=277 d=5 fixed=155/131235 clauses=81'742)
> #Bound  32.85s best:113   next:[33,112]   bool_core (num_cores=33 [size:2 mw:1 d:5] a=276 d=5 fixed=155/131245 clauses=81'768)
> #Bound  33.83s best:113   next:[34,112]   bool_core (num_cores=34 [size:17 mw:1 d:5] a=260 d=5 fixed=155/131266 clauses=81'800)
> #78     34.14s best:112   next:[34,111]   graph_var_lns (d=2.91e-01 s=312 t=0.10 p=0.47 stall=14 h=base)
> #Bound  34.62s best:112   next:[35,111]   bool_core (num_cores=35 [size:14 mw:1 d:4] a=247 d=5 fixed=155/131294 clauses=81'829)
> #Bound  35.17s best:112   next:[36,111]   bool_core (num_cores=36 [size:7 mw:1 d:5] a=241 d=5 fixed=155/131312 clauses=81'875)
> #Bound  35.56s best:112   next:[37,111]   bool_core (num_cores=37 [size:4 mw:1 d:5] a=238 d=5 fixed=155/131325 clauses=81'911)
> #Bound  36.26s best:112   next:[38,111]   bool_core (num_cores=38 [size:8 mw:1 d:6] a=231 d=6 fixed=155/131339 clauses=81'946)
> #Bound  37.39s best:112   next:[39,111]   bool_core (num_cores=39 [size:15 mw:1 d:5] a=217 d=6 fixed=155/131367 clauses=81'998)
> #Bound  38.17s best:112   next:[40,111]   bool_core (num_cores=40 [size:9 mw:1 d:5] a=209 d=6 fixed=155/131395 clauses=82'054)
> #Bound  39.08s best:112   next:[41,111]   bool_core (num_cores=41 [size:13 mw:1 d:5] a=197 d=6 fixed=155/131419 clauses=82'086)
> #Bound  39.73s best:112   next:[42,111]   bool_core (num_cores=42 [size:7 mw:1 d:5] a=191 d=6 fixed=155/131442 clauses=82'142)
> #Bound  40.80s best:112   next:[43,111]   bool_core (num_cores=43 [size:12 mw:1 d:6] a=180 d=6 fixed=155/131464 clauses=82'216)
> #Bound  41.48s best:112   next:[44,111]   bool_core (num_cores=44 [size:6 mw:1 d:6] a=175 d=6 fixed=155/131487 clauses=82'282)
> #Bound  42.18s best:112   next:[45,111]   bool_core (num_cores=45 [size:9 mw:1 d:6] a=167 d=6 fixed=155/131507 clauses=82'345)
> #79     42.36s best:111   next:[45,110]   graph_var_lns (d=1.96e-01 s=407 t=0.10 p=0.43 stall=2 h=base)
> #Bound  42.65s best:111   next:[46,110]   bool_core (num_cores=46 [size:4 mw:1 d:5] a=164 d=6 fixed=155/131525 clauses=82'429)
> #Bound  44.22s best:111   next:[47,110]   bool_core (num_cores=47 [size:6 mw:1 d:6] a=159 d=6 fixed=155/131537 clauses=82'677)
> #Bound  45.24s best:111   next:[48,110]   bool_core (num_cores=48 [size:7 mw:1 d:6] a=153 d=6 fixed=155/131565 clauses=82'782)
> #80     45.76s best:109   next:[48,108]   graph_var_lns (d=2.38e-01 s=437 t=0.10 p=0.46 stall=0 h=base)
> #Bound  46.40s best:109   next:[49,108]   bool_core (num_cores=49 [size:2 mw:1 d:7] a=152 d=7 fixed=155/131581 clauses=83'216)
> #Bound  48.13s best:109   next:[50,108]   bool_core (num_cores=50 [size:9 mw:1 d:6] a=144 d=7 fixed=155/131598 clauses=83'550)
> #Bound  48.59s best:109   next:[51,108]   bool_core (num_cores=51 [size:2 mw:1 d:5] a=143 d=7 fixed=155/131618 clauses=83'638)
> #Bound  50.46s best:109   next:[52,108]   bool_core (num_cores=52 [size:3 mw:1 d:7] a=141 d=7 fixed=155/131630 clauses=84'186)
> #Bound  51.66s best:109   next:[53,108]   bool_core (num_cores=53 [size:8 mw:1 d:6] a=134 d=7 fixed=155/131660 clauses=84'353)
> #Bound  52.88s best:109   next:[54,108]   bool_core (num_cores=54 [size:5 mw:1 d:6] a=130 d=7 fixed=155/131684 clauses=84'524)
> #Bound  53.61s best:109   next:[55,108]   bool_core (num_cores=55 [size:2 mw:1 d:5] a=129 d=7 fixed=155/131707 clauses=84'650)
> #Model  53.86s var:130343/130549 constraints:85637/85743
> #Bound  54.09s best:109   next:[56,108]   bool_core (num_cores=56 [size:2 mw:1 d:5] a=128 d=7 fixed=206/131719 clauses=84'733)
> #Bound  58.35s best:109   next:[57,108]   bool_core (num_cores=57 [size:6 mw:1 d:7] a=123 d=7 fixed=206/131734 clauses=85'675)
> #Bound  64.13s best:109   next:[58,108]   bool_core (num_cores=58 [size:5 mw:1 d:5] a=119 d=7 fixed=206/131765 clauses=85'323)
> #Bound  68.06s best:109   next:[59,108]   bool_core (num_cores=59 [size:6 mw:1 d:8] a=114 d=8 fixed=206/131779 clauses=86'469)
> #Bound  73.19s best:109   next:[60,108]   bool_core (num_cores=60 [size:8 mw:1 d:8] a=107 d=8 fixed=206/131822 clauses=87'617)
> #Bound  95.74s best:109   next:[61,108]   bool_core (num_cores=61 [size:5 mw:1 d:9] a=103 d=9 fixed=206/131854 clauses=93'114)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  51.40s,   51.40s]   51.40s   0.00ns   51.40s
>            'default_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [   1.06m,    1.06m]    1.06m   0.00ns    1.06m
>      'feasibility_pump':       477 [ 94.46us, 410.61ms]   1.17ms  18.77ms 557.68ms       456 [ 54.00ns,  54.00ns]  54.00ns   0.00ns  24.62us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        83 [147.39ms,    1.33s] 607.89ms 332.89ms   50.45s        83 [ 10.00ns, 102.49ms]  52.86ms  48.60ms    4.39s
>         'graph_cst_lns':        32 [440.33ms,    2.77s]    1.54s 481.02ms   49.17s        32 [186.47us, 100.77ms]  65.36ms  43.16ms    2.09s
>         'graph_dec_lns':        32 [423.67ms,    3.07s]    1.73s 624.89ms   55.39s        32 [ 10.00ns, 100.42ms]  38.83ms  47.58ms    1.24s
>         'graph_var_lns':        83 [173.11ms,    2.07s] 608.73ms 336.15ms   50.52s        83 [ 10.00ns, 102.92ms]  56.98ms  46.21ms    4.73s
>                    'ls':       202 [ 19.79ms, 554.45ms] 236.38ms 108.71ms   47.75s       202 [131.81us, 100.97ms]  95.65ms  20.56ms   19.32s
>                'ls_lin':       200 [ 20.70ms, 537.76ms] 238.57ms 100.76ms   47.71s       200 [138.19us, 101.34ms]  97.57ms  15.59ms   19.51s
>            'max_lp_sym':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  25.18s,   25.18s]   25.18s   0.00ns   25.18s
>                 'no_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  44.65s,   44.65s]   44.65s   0.00ns   44.65s
>          'pseudo_costs':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  13.29s,   13.29s]   13.29s   0.00ns   13.29s
>         'quick_restart':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  55.19s,   55.19s]   55.19s   0.00ns   55.19s
>   'quick_restart_no_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  43.06s,   43.06s]   43.06s   0.00ns   43.06s
>         'reduced_costs':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  14.38s,   14.38s]   14.38s   0.00ns   14.38s
>             'rins/rens':        27 [ 98.15ms,    4.77s]    1.81s    1.84s   48.78s        26 [ 10.00ns, 102.79ms]  34.73ms  47.74ms 903.07ms
>           'rnd_cst_lns':        34 [379.33ms,    2.97s]    1.46s 560.65ms   49.66s        34 [ 10.00ns, 100.97ms]  42.13ms  46.79ms    1.43s
>           'rnd_var_lns':        35 [323.13ms,    3.49s]    1.51s 671.61ms   52.73s        32 [ 10.00ns, 101.82ms]  45.36ms  44.63ms    1.45s
> 
> Search stats                Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  131'923     17'833   615'992     8'772  403'496'093      1'090'993
>            'default_lp':  130'549    166'174   288'476     5'955  193'404'227     12'085'995
>             'fs_random':        0          0         0         0            0              0
>       'fs_random_no_lp':        0          0         0         0            0              0
>            'max_lp_sym':  130'549         50    40'070     5'895   28'943'379     29'048'450
>                 'no_lp':  130'549     66'719   162'176     5'933  210'347'573      5'703'653
>          'pseudo_costs':  130'549      1'687    43'758     5'898   35'692'642     31'805'853
>         'quick_restart':  130'549     16'816   913'464     9'739  365'086'151      3'093'003
>   'quick_restart_no_lp':  130'549     13'953   696'206     8'531  288'709'670      2'508'142
>         'reduced_costs':  130'549        284    44'476     5'934   29'932'175     29'776'990
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        14'394     695'729   3'407'475     1'024'751        25     2'403      56'366         0        542       12'366        0
>            'default_lp':       121'449   1'102'098  35'202'148    32'201'944       196     1'177      29'047         0        280        7'066        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':            24         158       9'792             0         0     1'175      29'025         0        270        6'782        0
>                 'no_lp':        49'832     862'552  14'817'923    10'796'865       113     1'184      29'111         0        298        7'474        0
>          'pseudo_costs':         1'484      14'733     471'918             0         2     1'174      29'014         0        290        7'156        0
>         'quick_restart':         9'316      91'597   2'625'373       785'212        94     3'420      82'972         0        860       21'476        0
>   'quick_restart_no_lp':         7'830      75'486   2'106'074       760'755        86     2'498      56'856         0        642       14'899        0
>         'reduced_costs':           271      18'641      87'764             0         0     1'210      29'332         0        311        7'865        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          3           0          0    1'716        0        0
>      'max_lp_sym':          1      32'240          0        0      637        0
>    'pseudo_costs':          1      49'108      1'184      655    4'308        0
>   'quick_restart':          3           0          0    3'978        0        0
>   'reduced_costs':          1      56'704      1'139      366    4'712        0
> 
> Lp dimension                 Final dimension of first component
>      'default_lp':                 0 rows, 2 columns, 0 entries
>      'max_lp_sym':  193696 rows, 129779 columns, 690784 entries
>    'pseudo_costs':    17896 rows, 130547 columns, 66292 entries
>   'quick_restart':                 0 rows, 2 columns, 0 entries
>   'reduced_costs':    16247 rows, 130547 columns, 59628 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>      'max_lp_sym':          0            0       0         0       0           0
>    'pseudo_costs':          0            0     397         0  22'198           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0     819         0  25'009           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':            3        0        0       0          0      0             0          0/0
>      'max_lp_sym':      193'696        0        0   9'243          0      0             0          0/0
>    'pseudo_costs':      195'881       71    2'431   9'428        632      0            15  1'184/7'009
>   'quick_restart':            3        0        0       0          0      0             0          0/0
>   'reduced_costs':      195'853       49    2'196   9'411        632      0             0  1'139/6'008
> 
> Lp Cut           reduced_costs  pseudo_costs
>          CG_FF:            107           129
>           CG_K:              3             7
>           CG_R:             22            32
>         Clique:            149           171
>      MIR_1_RLT:            116            92
>       MIR_3_FF:             39            52
>       MIR_4_FF:             12            24
>       MIR_5_FF:              7            16
>       MIR_6_FF:              2            11
>   ZERO_HALF_FF:            393           520
>    ZERO_HALF_R:            289           130
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          4/83     49%    2.58e-01       0.10
>   'graph_cst_lns':          5/32     47%    7.17e-01       0.10
>   'graph_dec_lns':          3/32     62%    9.79e-01       0.10
>   'graph_var_lns':          6/83     49%    2.70e-01       0.10
>       'rins/rens':          0/26     65%    9.05e-01       0.10
>     'rnd_cst_lns':          4/34     62%    9.77e-01       0.10
>     'rnd_var_lns':          3/32     66%    9.86e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                          'ls_lin_restart':       27                 18    967'422         0              0          0         19'978      1'866'368
>                 'ls_lin_restart_compound':       20                 13          0    57'843            411     28'712            129      9'393'126
>         'ls_lin_restart_compound_perturb':       31                 20          0   142'319          3'182     69'563            502     14'622'031
>                    'ls_lin_restart_decay':       15                 12    499'453         0              0          0            895      1'717'351
>           'ls_lin_restart_decay_compound':       31                 27          0   101'446          7'111     47'157            145     14'226'586
>   'ls_lin_restart_decay_compound_perturb':       27                 14          0   197'943         36'511     80'704            150     12'996'374
>            'ls_lin_restart_decay_perturb':       17                 16    606'183         0              0          0          1'253      2'081'565
>                  'ls_lin_restart_perturb':       32                 18  1'028'890         0              0          0         19'276      2'088'556
>                              'ls_restart':       49                 28  1'673'917         0              0          0         30'330      3'201'733
>                     'ls_restart_compound':       24                 17          0    69'374            402     34'481            145     11'451'133
>             'ls_restart_compound_perturb':       20                 18          0    52'524              3     26'257             68      9'551'764
>                        'ls_restart_decay':       13                 12    355'801         0              0          0            744      1'231'331
>               'ls_restart_decay_compound':       37                 22          0   176'583         25'018     75'770            245     17'615'533
>       'ls_restart_decay_compound_perturb':       10                  9          0    26'318              0     13'159             35      4'812'679
>                'ls_restart_decay_perturb':       30                 19  1'051'632         0              0          0          1'654      3'515'884
>                      'ls_restart_perturb':       19                 17    596'908         0              0          0         15'968      1'316'060
> 
> Solutions (80)                      Num     Rank
>                   'complete_hint':    1    [1,1]
>                      'default_lp':   40  [30,73]
>                   'graph_arc_lns':    2   [7,74]
>                   'graph_cst_lns':    5   [3,77]
>                   'graph_dec_lns':    4   [5,76]
>                   'graph_var_lns':    4   [6,80]
>            'ls_lin_restart_decay':    1    [9,9]
>   'ls_lin_restart_decay_compound':    1  [38,38]
>          'ls_lin_restart_perturb':    2   [8,22]
>                      'ls_restart':    3  [10,26]
>                'ls_restart_decay':    2  [21,25]
>        'ls_restart_decay_perturb':    1  [27,27]
>              'ls_restart_perturb':    2  [17,46]
>                           'no_lp':    1  [14,14]
>                   'quick_restart':    2  [54,55]
>             'quick_restart_no_lp':    1  [15,15]
>                     'rnd_cst_lns':    5   [2,24]
>                     'rnd_var_lns':    3  [11,20]
> 
> Objective bounds     Num
>        'bool_core':   61
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    242      953      188
>    'fj solution hints':      0        0        0
>         'lp solutions':     93       18       93
>                 'pump':    476        9
> 
> Improving bounds shared    Num  Sym
>             'default_lp':  155    0
>          'quick_restart':   51    0
> 
> Clauses shared                Num
>                  'core':      907
>            'default_lp':  181'438
>          'pseudo_costs':      385
>         'quick_restart':      787
>   'quick_restart_no_lp':    4'167
>         'reduced_costs':       43
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 109
> best_bound: 61
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.357
> usertime: 120.357
> deterministic_time: 371.917
> gap_integral: 1430.5
> solution_fingerprint: 0xf213e71da48fdbd1
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
> Initial optimization model '': (model_fingerprint: 0x165220b78a585bd9)
> #Variables: 1'326 (#bools: 650 in objective) (1'326 primary variables)
>   - 650 Booleans in [0,1]
>   - 650 in [0,26]
>   - 26 constants in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25} 
> #kAutomaton: 16
> #kLinear1: 650 (#enforced: 650)
> #kLinear2: 650 (#enforced: 650)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 650.
>   3.41e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.60e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.19e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   3.67e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   9.15e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=352'449 
> [Symmetry] Graph for symmetry has 942'310 nodes and 2'495'980 arcs.
> [Symmetry] Symmetry computation done. time: 0.393617 dtime: 0.392437
> [Symmetry] #generators: 423, average support size: 2.22695
> [Symmetry] The model contains 16 duplicate constraints !
> [Symmetry] 41 orbits on 467 variables with sizes: 64,16,16,15,15,15,15,15,15,15,...
> [Symmetry] Found orbitope of size 17 x 2
> [SAT presolve] num removable Booleans: 4545 / 260021
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:675238 literals:1721538 vars:259548 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.100381s] clauses:675222 literals:1721490 vars:259548 one_side_vars:0 simple_definition:17 singleton_clauses:0
> [SAT presolve] [0.1115s] clauses:674864 literals:1721490 vars:259369 one_side_vars:0 simple_definition:17 singleton_clauses:0
>   1.42e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.83e-01s  1.00e+00d *[Probe] #probed=4'286 #equiv=16 #new_binary_clauses=4'941 
>   3.54e-01s  1.05e+00d *[MaxClique] Merged 522'247(1'044'494 literals) into 503'525(1'025'773 literals) at_most_ones. 
>   7.72e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.05e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   6.96e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.19e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=96 
>   3.06e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.06e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   8.66e-03s  0.00e+00d  [DetectDifferentVariables] 
>   2.29e-01s  1.34e-02d  [ProcessSetPPC] #relevant_constraints=665'979 #num_inclusions=503'477 
>   1.04e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.01e-01s  9.51e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.01e-02s  9.66e-03d  [FindBigVerticalLinearOverlap] 
>   9.18e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.02e-02s  3.25e-03d  [MergeClauses] #num_collisions=869 #num_merges=869 #num_saved_literals=1'917 
>   7.74e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.04e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.73e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.99e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.13e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   1.76e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2 
> [Symmetry] Graph for symmetry has 940'835 nodes and 2'447'117 arcs.
> [Symmetry] Symmetry computation done. time: 0.384487 dtime: 0.408128
> [SAT presolve] num removable Booleans: 4350 / 259319
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:648466 literals:1649926 vars:259205 one_side_vars:0 simple_definition:20379 singleton_clauses:0
> [SAT presolve] [0.086395s] clauses:648466 literals:1649926 vars:259205 one_side_vars:0 simple_definition:20379 singleton_clauses:0
> [SAT presolve] [0.0974364s] clauses:648466 literals:1649926 vars:259205 one_side_vars:0 simple_definition:20379 singleton_clauses:0
>   1.86e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.28e-01s  1.00e+00d *[Probe] #probed=4'156 #equiv=173 #new_binary_clauses=5'145 
>   3.45e-01s  1.00e+00d *[MaxClique] Merged 499'670(999'343 literals) into 480'025(979'635 literals) at_most_ones. 
>   1.96e-01s  0.00e+00d  [DetectDominanceRelations] 
>   8.34e-02s  0.00e+00d  [DetectDominanceRelations] 
>   5.32e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   7.88e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.45e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=974 
>   3.81e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.56e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.18e-02s  0.00e+00d  [DetectDifferentVariables] 
>   2.31e-01s  1.28e-02d  [ProcessSetPPC] #relevant_constraints=641'530 #num_inclusions=479'330 
>   1.35e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.05e-01s  9.65e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.10e-02s  9.43e-03d  [FindBigVerticalLinearOverlap] 
>   1.23e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.05e-02s  3.13e-03d  [MergeClauses] #num_collisions=523 #num_merges=523 #num_saved_literals=1'225 
>   8.31e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.16e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.39e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.16e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.47e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   2.37e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 940'011 nodes and 2'401'893 arcs.
> [Symmetry] Symmetry computation done. time: 0.376996 dtime: 0.405698
> [Symmetry] #generators: 32, average support size: 8
> [Symmetry] 108 orbits on 236 variables with sizes: 3,3,3,3,3,3,3,3,3,3,...
> [Symmetry] Found orbitope of size 4 x 2
> [SAT presolve] num removable Booleans: 4193 / 259143
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:624301 literals:1581727 vars:258839 one_side_vars:96 simple_definition:40499 singleton_clauses:0
> [SAT presolve] [0.0823374s] clauses:624301 literals:1581727 vars:258839 one_side_vars:96 simple_definition:40499 singleton_clauses:0
> [SAT presolve] [0.0940028s] clauses:624299 literals:1581723 vars:258838 one_side_vars:96 simple_definition:40498 singleton_clauses:0
>   2.70e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.39e-01s  1.00e+00d *[Probe] #probed=4'156 #new_binary_clauses=4'799 
>   3.44e-01s  1.00e+00d *[MaxClique] Merged 477'640(955'342 literals) into 455'903(933'606 literals) at_most_ones. 
>   2.09e-01s  0.00e+00d  [DetectDominanceRelations] 
>   8.90e-02s  0.00e+00d  [DetectDominanceRelations] 
>   5.59e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   8.71e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.04e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.90e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.75e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.45e-02s  0.00e+00d  [DetectDifferentVariables] 
>   2.27e-01s  1.22e-02d  [ProcessSetPPC] #relevant_constraints=618'033 #num_inclusions=455'836 
>   1.70e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.23e-01s  9.89e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.06e-02s  9.19e-03d  [FindBigVerticalLinearOverlap] 
>   1.53e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.02e-02s  3.00e-03d  [MergeClauses] #num_collisions=523 #num_merges=523 #num_saved_literals=1'225 
>   8.93e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.33e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.21e-01s  0.00e+00d  [ExpandObjective] #entries=8'740'690 #tight_variables=329'149 #tight_constraints=17'343 #expands=223 
> 
> Presolve summary:
>   - 1324 affine relations were detected.
>   - rule 'affine: new relation' was applied 1'324 times.
>   - rule 'at_most_one: dominated singleton' was applied 1 time.
>   - rule 'at_most_one: removed literals' was applied 4 times.
>   - rule 'at_most_one: resolved two constraints with opposite literal' was applied 2 times.
>   - rule 'at_most_one: size one' was applied 1 time.
>   - rule 'at_most_one: transformed into max clique.' was applied 3 times.
>   - rule 'automaton: expanded' was applied 16 times.
>   - rule 'bool_and: x => x' was applied 25 times.
>   - rule 'bool_or: implications' was applied 6 times.
>   - rule 'deductions: 1300 stored' was applied 1 time.
>   - rule 'domination: in exactly one' was applied 4 times.
>   - rule 'dual: fix variable' was applied 5 times.
>   - rule 'duplicate: removed constraint' was applied 353'521 times.
>   - rule 'exactly_one: removed literals' was applied 18 times.
>   - rule 'exactly_one: simplified objective' was applied 2 times.
>   - rule 'exactly_one: singleton' was applied 16 times.
>   - rule 'exactly_one: size two' was applied 2 times.
>   - rule 'linear: always true' was applied 1'275 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'275 times.
>   - rule 'linear: fixed or dup variables' was applied 1'275 times.
>   - rule 'linear: remapped using affine relations' was applied 11'675 times.
>   - rule 'new_bool: automaton expansion' was applied 259'371 times.
>   - rule 'objective: expanded via tight equality' was applied 223 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 222 times.
>   - rule 'objective: variable not used elsewhere' was applied 6 times.
>   - rule 'presolve: 36 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 7'432 times.
>   - rule 'setppc: removed dominated constraints' was applied 67 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 650 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'300 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x80a660408b8674e9)
> #Variables: 259'139 (#bools: 643 in objective) (245'499 primary variables)
>   - 259'139 Booleans in [0,1]
> #kAtMostOne: 51 (#literals: 163)
> #kBoolAnd: 10'641 (#enforced: 10'641 #multi: 521) (#literals: 466'317)
> #kBoolOr: 143'743 (#literals: 597'470)
> #kExactlyOne: 17'343 (#literals: 329'149)
> [Symmetry] Graph for symmetry has 936'513 nodes and 2'352'623 arcs.
> [Symmetry] Symmetry computation done. time: 0.357936 dtime: 0.412407
> [Symmetry] #generators: 32, average support size: 8
> [Symmetry] 108 orbits on 236 variables with sizes: 3,3,3,3,3,3,3,3,3,3,...
> [Symmetry] Found orbitope of size 4 x 2
> 
> Preloading model.
> #Bound  13.14s best:inf   next:[0,643]    initial_domain
> #1      13.16s best:642   next:[0,641]    complete_hint
> #Model  13.25s var:259139/259139 constraints:171778/171778
> 
> Starting search at 13.27s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2      14.04s best:636   next:[0,635]    rnd_cst_lns (d=5.00e-01 s=9 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3      14.64s best:624   next:[0,623]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base) [hint]
> #4      14.66s best:619   next:[0,618]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: rnd_cst_lns (d=5.00e...]
> #5      15.09s best:618   next:[0,617]    graph_dec_lns (d=5.00e-01 s=13 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: graph_cst_lns (d=5.0...]
> #6      15.52s best:517   next:[0,516]    graph_var_lns (d=5.00e-01 s=10 t=0.10 p=0.00 stall=0 h=base)
> #7      15.70s best:516   next:[0,515]    ls_restart_decay(batch:1 lin{mvs:7 evals:574} #w_updates:4 #perturb:0)
> #8      15.73s best:515   next:[0,514]    ls_lin_restart_perturb(batch:1 lin{mvs:5 evals:526} #w_updates:4 #perturb:0) [combined with: ls_restart_decay(bat...]
> #9      15.77s best:514   next:[0,513]    ls_lin_restart_decay(batch:1 lin{mvs:13 evals:552} #w_updates:8 #perturb:0)
> #10     15.78s best:353   next:[0,352]    quick_restart
> #11     16.02s best:352   next:[0,351]    ls_restart_perturb(batch:1 lin{mvs:9 evals:362} #w_updates:7 #perturb:0)
> #12     16.28s best:268   next:[0,267]    no_lp
> #Bound  16.40s best:268   next:[1,267]    bool_core (num_cores=1 [size:11 mw:1 d:4] a=633 d=4 fixed=0/259148 clauses=162'140)
> #Model  16.44s var:258984/259139 constraints:171698/171778
> #Model  16.89s var:258725/259139 constraints:171564/171778
> #13     18.10s best:255   next:[1,254]    graph_cst_lns (d=7.07e-01 s=36 t=0.10 p=1.00 stall=0 h=base) [hint]
> #14     18.32s best:254   next:[1,253]    ls_lin_restart_compound(batch:1 lin{mvs:0 evals:318'420} gen{mvs:1'667 evals:0} comp{mvs:3 btracks:832} #w_updates:1 #perturb:0)
> #15     18.54s best:253   next:[1,252]    ls_restart_compound(batch:1 lin{mvs:0 evals:309'544} gen{mvs:1'647 evals:0} comp{mvs:5 btracks:821} #w_updates:2 #perturb:0)
> #16     18.65s best:252   next:[1,251]    ls_lin_restart_perturb(batch:1 lin{mvs:5 evals:258} #w_updates:4 #perturb:0)
> #17     19.15s best:251   next:[1,250]    ls_lin_restart_perturb(batch:1 lin{mvs:211 evals:462} #w_updates:202 #perturb:0)
> #18     19.42s best:250   next:[1,249]    quick_restart
> #19     19.58s best:249   next:[1,248]    ls_restart_decay(batch:1 lin{mvs:35 evals:353} #w_updates:16 #perturb:0)
> #20     19.68s best:187   next:[1,186]    quick_restart
> #21     21.23s best:186   next:[1,185]    quick_restart
> #22     22.56s best:181   next:[1,180]    quick_restart
> #Bound  22.96s best:181   next:[2,180]    bool_core (num_cores=2 [size:14 mw:1 d:4] a=620 d=4 fixed=155/259170 clauses=161'861)
> #23     23.87s best:180   next:[2,179]    quick_restart
> #Bound  25.15s best:180   next:[3,179]    bool_core (num_cores=3 [size:15 mw:1 d:4] a=606 d=4 fixed=414/259196 clauses=161'895)
> #24     25.84s best:177   next:[3,176]    graph_var_lns (d=2.93e-01 s=72 t=0.10 p=0.00 stall=0 h=base)
> #25     26.41s best:176   next:[3,175]    quick_restart_no_lp
> #Bound  27.00s best:176   next:[4,175]    bool_core (num_cores=4 [size:14 mw:1 d:4] a=593 d=4 fixed=414/259222 clauses=161'931)
> #Bound  28.64s best:176   next:[5,175]    bool_core (num_cores=5 [size:12 mw:1 d:4] a=582 d=4 fixed=414/259245 clauses=161'956)
> #Bound  30.50s best:176   next:[6,175]    bool_core (num_cores=6 [size:15 mw:1 d:4] a=568 d=4 fixed=414/259269 clauses=161'988)
> #26     31.60s best:168   next:[6,167]    quick_restart_no_lp
> #Bound  32.36s best:168   next:[7,167]    bool_core (num_cores=7 [size:13 mw:1 d:4] a=556 d=4 fixed=414/259294 clauses=162'028)
> #Bound  33.93s best:168   next:[8,167]    bool_core (num_cores=8 [size:11 mw:1 d:4] a=546 d=4 fixed=414/259315 clauses=162'053)
> #Bound  35.55s best:168   next:[9,167]    bool_core (num_cores=9 [size:13 mw:1 d:4] a=534 d=4 fixed=414/259336 clauses=162'077)
> #Bound  37.22s best:168   next:[10,167]   bool_core (num_cores=10 [size:12 mw:1 d:4] a=523 d=4 fixed=414/259358 clauses=162'113)
> #Bound  38.80s best:168   next:[11,167]   bool_core (num_cores=11 [size:11 mw:1 d:4] a=513 d=4 fixed=414/259378 clauses=162'137)
> #Bound  40.63s best:168   next:[12,167]   bool_core (num_cores=12 [size:13 mw:1 d:4] a=501 d=4 fixed=414/259399 clauses=162'176)
> #Model  41.10s var:258466/259139 constraints:171430/171778
> #Bound  42.27s best:168   next:[13,167]   bool_core (num_cores=13 [size:12 mw:1 d:4] a=490 d=4 fixed=673/259421 clauses=162'207)
> #Bound  44.46s best:168   next:[14,167]   bool_core (num_cores=14 [size:18 mw:1 d:5] a=473 d=5 fixed=673/259448 clauses=162'239)
> #27     45.28s best:167   next:[14,166]   graph_var_lns (d=1.83e-01 s=180 t=0.10 p=0.33 stall=4 h=base)
> #28     45.52s best:166   next:[14,165]   graph_cst_lns (d=9.14e-01 s=166 t=0.10 p=1.00 stall=2 h=base) [combined with: graph_var_lns (d=1.8...]
> #Bound  45.83s best:166   next:[15,165]   bool_core (num_cores=15 [size:11 mw:1 d:4] a=463 d=5 fixed=673/259474 clauses=162'271)
> #29     45.95s best:165   next:[15,164]   quick_restart
> #Bound  47.28s best:165   next:[16,164]   bool_core (num_cores=16 [size:11 mw:1 d:4] a=453 d=5 fixed=673/259493 clauses=162'299)
> #Bound  48.86s best:165   next:[17,164]   bool_core (num_cores=17 [size:13 mw:1 d:4] a=441 d=5 fixed=673/259514 clauses=162'335)
> #30     48.97s best:164   next:[17,163]   quick_restart_no_lp
> #31     49.57s best:163   next:[17,162]   rnd_cst_lns (d=9.56e-01 s=215 t=0.10 p=1.00 stall=4 h=base) [hint] [combined with: quick_restart_no_lp...]
> #Bound  50.36s best:163   next:[18,162]   bool_core (num_cores=18 [size:13 mw:1 d:4] a=429 d=5 fixed=673/259537 clauses=162'371)
> #32     50.91s best:162   next:[18,161]   quick_restart_no_lp
> #Bound  51.69s best:162   next:[19,161]   bool_core (num_cores=19 [size:11 mw:1 d:4] a=419 d=5 fixed=673/259558 clauses=162'400)
> #Model  53.13s var:258311/259139 constraints:171350/171778
> #Bound  53.22s best:162   next:[20,161]   bool_core (num_cores=20 [size:13 mw:1 d:4] a=407 d=5 fixed=673/259579 clauses=162'439)
> #Bound  54.60s best:162   next:[21,161]   bool_core (num_cores=21 [size:11 mw:1 d:4] a=397 d=5 fixed=828/259600 clauses=162'471)
> #33     54.73s best:161   next:[21,160]   graph_var_lns (d=1.46e-01 s=280 t=0.10 p=0.36 stall=3 h=base)
> #Model  55.85s var:258156/259139 constraints:171270/171778
> #Bound  56.49s best:161   next:[22,160]   bool_core (num_cores=22 [size:17 mw:1 d:5] a=381 d=5 fixed=828/259625 clauses=162'503)
> #34     57.26s best:160   next:[22,159]   graph_arc_lns (d=1.88e-01 s=307 t=0.10 p=0.40 stall=8 h=base)
> #Bound  57.80s best:160   next:[23,159]   bool_core (num_cores=23 [size:11 mw:1 d:4] a=371 d=5 fixed=983/259650 clauses=162'533)
> #Bound  59.02s best:160   next:[24,159]   bool_core (num_cores=24 [size:11 mw:1 d:4] a=361 d=5 fixed=983/259669 clauses=162'556)
> #35     59.30s best:159   next:[24,158]   graph_arc_lns (d=2.42e-01 s=324 t=0.10 p=0.45 stall=0 h=base)
> #36     60.19s best:158   next:[24,157]   graph_var_lns (d=1.88e-01 s=329 t=0.10 p=0.43 stall=2 h=base)
> #Bound  60.63s best:158   next:[25,157]   bool_core (num_cores=25 [size:13 mw:1 d:4] a=349 d=5 fixed=983/259690 clauses=162'583)
> #Bound  61.74s best:158   next:[26,157]   bool_core (num_cores=26 [size:11 mw:1 d:4] a=339 d=5 fixed=983/259711 clauses=162'605)
> #Bound  63.32s best:158   next:[27,157]   bool_core (num_cores=27 [size:13 mw:1 d:4] a=327 d=5 fixed=983/259732 clauses=162'630)
> #Bound  64.83s best:158   next:[28,157]   bool_core (num_cores=28 [size:13 mw:1 d:4] a=315 d=5 fixed=983/259755 clauses=162'657)
> #37     64.87s best:157   next:[28,156]   graph_arc_lns (d=2.44e-01 s=370 t=0.10 p=0.46 stall=0 h=base)
> #Bound  66.11s best:157   next:[29,156]   bool_core (num_cores=29 [size:12 mw:1 d:4] a=304 d=5 fixed=983/259777 clauses=162'683)
> #Bound  67.34s best:157   next:[30,156]   bool_core (num_cores=30 [size:11 mw:1 d:4] a=294 d=5 fixed=983/259797 clauses=162'711)
> #Bound  69.00s best:157   next:[31,156]   bool_core (num_cores=31 [size:13 mw:1 d:4] a=282 d=5 fixed=983/259818 clauses=162'734)
> #Bound  70.50s best:157   next:[32,156]   bool_core (num_cores=32 [size:13 mw:1 d:4] a=270 d=5 fixed=983/259841 clauses=162'759)
> #Bound  72.05s best:157   next:[33,156]   bool_core (num_cores=33 [size:12 mw:1 d:4] a=259 d=5 fixed=983/259863 clauses=162'782)
> #Bound  79.04s best:157   next:[34,156]   bool_core (num_cores=34 [size:13 mw:1 d:4] a=247 d=5 fixed=983/259885 clauses=162'134)
> #Bound  80.88s best:157   next:[35,156]   bool_core (num_cores=35 [size:15 mw:1 d:4] a=233 d=5 fixed=983/259910 clauses=162'165)
> #Bound  82.58s best:157   next:[36,156]   bool_core (num_cores=36 [size:13 mw:1 d:4] a=221 d=5 fixed=983/259935 clauses=162'199)
> #Bound  84.41s best:157   next:[37,156]   bool_core (num_cores=37 [size:14 mw:1 d:4] a=208 d=5 fixed=983/259959 clauses=162'228)
> #Bound  86.15s best:157   next:[38,156]   bool_core (num_cores=38 [size:15 mw:1 d:4] a=194 d=5 fixed=983/259985 clauses=162'261)
> #Bound  87.48s best:157   next:[39,156]   bool_core (num_cores=39 [size:5 mw:1 d:5] a=190 d=5 fixed=983/260002 clauses=162'302)
> #Bound  88.58s best:157   next:[40,156]   bool_core (num_cores=40 [size:6 mw:1 d:5] a=185 d=5 fixed=983/260017 clauses=162'344)
> #Bound  90.77s best:157   next:[41,156]   bool_core (num_cores=41 [size:13 mw:1 d:6] a=173 d=6 fixed=983/260038 clauses=162'432)
> #Model  90.78s var:258053/259139 constraints:171217/171778
> #Bound  93.00s best:157   next:[42,156]   bool_core (num_cores=42 [size:15 mw:1 d:5] a=159 d=6 fixed=1086/260078 clauses=162'506)
> #Bound  94.46s best:157   next:[43,156]   bool_core (num_cores=43 [size:7 mw:1 d:5] a=153 d=6 fixed=1086/260103 clauses=162'593)
> #Bound  95.83s best:157   next:[44,156]   bool_core (num_cores=44 [size:7 mw:1 d:5] a=147 d=6 fixed=1086/260120 clauses=162'685)
> #Bound  96.74s best:157   next:[45,156]   bool_core (num_cores=45 [size:3 mw:1 d:6] a=145 d=6 fixed=1086/260133 clauses=162'748)
> #Bound  97.88s best:157   next:[46,156]   bool_core (num_cores=46 [size:3 mw:1 d:5] a=143 d=6 fixed=1086/260144 clauses=162'864)
> #Bound 100.10s best:157   next:[47,156]   bool_core (num_cores=47 [size:11 mw:1 d:6] a=133 d=6 fixed=1086/260161 clauses=162'975)
> #Bound 101.05s best:157   next:[48,156]   bool_core (num_cores=48 [size:4 mw:1 d:5] a=130 d=6 fixed=1086/260186 clauses=163'064)
> #Bound 101.78s best:157   next:[49,156]   bool_core (num_cores=49 [size:2 mw:1 d:5] a=129 d=6 fixed=1086/260195 clauses=163'119)
> #Bound 102.73s best:157   next:[50,156]   bool_core (num_cores=50 [size:3 mw:1 d:5] a=127 d=6 fixed=1086/260202 clauses=163'169)
> #Bound 104.03s best:157   next:[51,156]   bool_core (num_cores=51 [size:5 mw:1 d:5] a=123 d=6 fixed=1086/260212 clauses=163'251)
> #Bound 104.94s best:157   next:[52,156]   bool_core (num_cores=52 [size:4 mw:1 d:5] a=120 d=6 fixed=1086/260224 clauses=163'294)
> #Bound 106.76s best:157   next:[53,156]   bool_core (num_cores=53 [size:12 mw:1 d:5] a=109 d=6 fixed=1086/260242 clauses=163'338)
> #Bound 107.78s best:157   next:[54,156]   bool_core (num_cores=54 [size:2 mw:1 d:5] a=108 d=6 fixed=1086/260258 clauses=163'436)
> #Bound 108.56s best:157   next:[55,156]   bool_core (num_cores=55 [size:2 mw:1 d:5] a=107 d=6 fixed=1086/260269 clauses=163'520)
> #Bound 109.70s best:157   next:[56,156]   bool_core (num_cores=56 [size:2 mw:1 d:5] a=106 d=6 fixed=1086/260276 clauses=163'633)
> #Bound 110.82s best:157   next:[57,156]   bool_core (num_cores=57 [size:4 mw:1 d:5] a=103 d=6 fixed=1086/260290 clauses=163'747)
> #Bound 112.23s best:157   next:[58,156]   bool_core (num_cores=58 [size:4 mw:1 d:6] a=100 d=6 fixed=1086/260301 clauses=163'913)
> #Bound 113.27s best:157   next:[59,156]   bool_core (num_cores=59 [size:2 mw:1 d:5] a=99 d=6 fixed=1086/260317 clauses=164'054)
> #Bound 117.02s best:157   next:[60,156]   bool_core (num_cores=60 [size:5 mw:1 d:6] a=95 d=6 fixed=1086/260331 clauses=164'628)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  40.09s,   40.09s]   40.09s   0.00ns   40.09s
>            'default_lp':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  48.53s,   48.53s]   48.53s   0.00ns   48.53s
>      'feasibility_pump':       419 [ 80.69us, 709.06ms]   2.03ms  34.59ms 849.09ms       409 [ 18.00ns,  18.00ns]  18.00ns   0.00ns   7.36us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        31 [454.89ms,    2.88s]    1.39s 663.16ms   43.08s        31 [  4.58us, 101.31ms]  61.17ms  46.52ms    1.90s
>         'graph_cst_lns':        19 [743.55ms,    5.18s]    2.79s 912.79ms   52.96s        18 [ 10.00ns, 100.56ms]  42.40ms  47.67ms 763.13ms
>         'graph_dec_lns':        15 [   1.05s,    5.67s]    3.37s    1.43s   50.52s        15 [ 10.00ns, 100.30ms]  29.21ms  43.74ms 438.22ms
>         'graph_var_lns':        35 [477.11ms,    3.07s]    1.25s 643.51ms   43.59s        35 [ 16.18us, 101.90ms]  56.35ms  47.26ms    1.97s
>                    'ls':       135 [ 53.53ms, 707.76ms] 312.91ms 135.46ms   42.24s       135 [205.64us, 103.76ms]  97.10ms  16.94ms   13.11s
>                'ls_lin':       138 [ 38.05ms, 711.31ms] 304.76ms 153.92ms   42.06s       138 [122.13us, 103.51ms]  97.23ms  16.76ms   13.42s
>            'max_lp_sym':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  49.89s,   49.89s]   49.89s   0.00ns   49.89s
>          'pseudo_costs':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [   8.47s,    8.47s]    8.47s   0.00ns    8.47s
>         'quick_restart':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  48.14s,   48.14s]   48.14s   0.00ns   48.14s
>   'quick_restart_no_lp':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  36.73s,   36.73s]   36.73s   0.00ns   36.73s
>         'reduced_costs':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [   8.30s,    8.30s]    8.30s   0.00ns    8.30s
>             'rins/rens':         4 [ 18.15ms,   19.40s]   14.15s    8.17s   56.59s         3 [100.01ms, 100.01ms] 100.01ms 845.70ns 300.03ms
>           'rnd_cst_lns':        21 [703.47ms,    3.61s]    2.18s 940.08ms   45.86s        17 [ 10.00ns, 100.17ms]  29.97ms  45.28ms 509.51ms
>           'rnd_var_lns':        19 [651.52ms,    4.91s]    2.63s    1.14s   50.03s        19 [ 10.00ns, 100.34ms]  22.74ms  40.41ms 432.03ms
> 
> Search stats                Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  260'360      2'722   581'971     7'760  300'499'122        493'692
>            'default_lp':  259'139     60'838   151'999     6'172  193'992'097      5'026'792
>             'fs_random':        0          0         0         0            0              0
>       'fs_random_no_lp':        0          0         0         0            0              0
>            'max_lp_sym':  259'139          0     4'095     4'026    9'599'903      9'604'316
>                 'no_lp':  259'139     58'165   142'462     6'179  169'535'744      4'812'714
>          'pseudo_costs':  259'139        896    35'585     5'012   31'998'650     30'178'106
>         'quick_restart':  259'139      7'908   588'377     7'796  327'680'540      1'555'737
>   'quick_restart_no_lp':  259'139      6'497   474'023     6'765  256'523'835      1'214'332
>         'reduced_costs':  259'139        232    37'378     5'064   29'437'053     29'302'068
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         1'545      15'288     166'207             0         1     2'133      48'989         0        486       11'023        0
>            'default_lp':        40'583     347'586  14'658'402    12'220'305       127     2'117      48'413         0        516       11'883        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':        32'593     220'923  14'612'974     9'607'917        63     2'135      49'063         0        520       11'866        0
>          'pseudo_costs':           876      13'922     245'028             0         0       980      24'383         0        227        5'753        0
>         'quick_restart':         4'479      40'805   1'436'488             0        89     3'001      73'000         0        703       17'575        0
>   'quick_restart_no_lp':         3'815      35'732   1'201'456             0        75     2'115      48'343         0        514       11'794        0
>         'reduced_costs':           221       9'730      58'140             0         0     1'032      26'065         0        269        6'591        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          1           0          0   20'317        0        0
>      'max_lp_sym':          1      82'288          0        0       76        0
>    'pseudo_costs':          1      27'069        264      463    2'325        0
>   'quick_restart':          1           0          0    1'399        0        0
>   'reduced_costs':          1      25'940        367      324    2'214        0
> 
> Lp dimension                  Final dimension of first component
>      'default_lp':                  0 rows, 2 columns, 0 entries
>      'max_lp_sym':  608440 rows, 259010 columns, 1826678 entries
>    'pseudo_costs':     11302 rows, 259138 columns, 33009 entries
>   'quick_restart':                  0 rows, 2 columns, 0 entries
>   'reduced_costs':     14310 rows, 259138 columns, 42564 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>      'max_lp_sym':          0            0       0         0      0           0
>    'pseudo_costs':          0            0     295         0  3'975           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0     582         0  3'921           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':            1        0        0       0          0      0             0        0/0
>      'max_lp_sym':      608'440        0        0     394          0      0             0        0/0
>    'pseudo_costs':      608'800       15    5'865     458      2'733      0             0  264/2'380
>   'quick_restart':            1        0        0       0          0      0             0        0/0
>   'reduced_costs':      608'924        1    5'451     437      3'363      0             0  367/3'336
> 
> Lp Cut           reduced_costs  pseudo_costs
>          CG_FF:             24            60
>           CG_K:              3             -
>          CG_KL:              1             -
>           CG_R:              5            10
>         Clique:             65            93
>      MIR_1_RLT:              4            14
>       MIR_3_FF:              7            19
>       MIR_4_FF:              1             5
>       MIR_5_FF:              -             1
>   ZERO_HALF_FF:            209            51
>    ZERO_HALF_R:             48            11
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          5/31     42%    1.21e-01       0.10
>   'graph_cst_lns':          3/18     61%    9.08e-01       0.10
>   'graph_dec_lns':          2/15     73%    9.72e-01       0.10
>   'graph_var_lns':          6/35     49%    2.36e-01       0.10
>       'rins/rens':           3/3      0%    1.24e-01       0.10
>     'rnd_cst_lns':          3/17     71%    9.68e-01       0.10
>     'rnd_var_lns':          1/19     79%    9.88e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                          'ls_lin_restart':        8                  8   223'045         0              0          0         17'989        963'770
>                 'ls_lin_restart_compound':       21                 18         0    56'756            580     28'085            226     11'168'643
>         'ls_lin_restart_compound_perturb':       26                 17         0   110'779          1'463     54'654            611     13'761'221
>                    'ls_lin_restart_decay':       18                 10   541'465         0              0          0          1'529      3'506'761
>           'ls_lin_restart_decay_compound':       20                 15         0    85'960         12'852     36'549            331     10'417'863
>   'ls_lin_restart_decay_compound_perturb':       13                 11         0    44'492          1'657     21'413            239      6'834'787
>            'ls_lin_restart_decay_perturb':       12                 12   367'198         0              0          0          1'415      2'391'143
>                  'ls_lin_restart_perturb':       20                 19   525'680         0              0          0         35'157      1'993'152
>                              'ls_restart':       11                 10   336'688         0              0          0         23'485      1'274'943
>                     'ls_restart_compound':       14                 13         0    34'603            246     17'176            113      7'419'011
>             'ls_restart_compound_perturb':       22                 14         0    79'728          1'092     39'314            421     11'728'730
>                        'ls_restart_decay':       15                 14   363'538         0              0          0          1'407      2'486'060
>               'ls_restart_decay_compound':       26                 17         0    83'950          4'034     39'939            421     13'616'224
>       'ls_restart_decay_compound_perturb':       14                  7         0   121'113         30'390     45'303            183      7'118'130
>                'ls_restart_decay_perturb':       14                 14   443'813         0              0          0          2'071      2'674'450
>                      'ls_restart_perturb':       19                 12   564'450         0              0          0         23'598      2'106'336
> 
> Solutions (37)                Num     Rank
>             'complete_hint':    1    [1,1]
>             'graph_arc_lns':    3  [34,37]
>             'graph_cst_lns':    4   [3,28]
>             'graph_dec_lns':    1    [5,5]
>             'graph_var_lns':    5   [6,36]
>   'ls_lin_restart_compound':    1  [14,14]
>      'ls_lin_restart_decay':    1    [9,9]
>    'ls_lin_restart_perturb':    3   [8,17]
>       'ls_restart_compound':    1  [15,15]
>          'ls_restart_decay':    2   [7,19]
>        'ls_restart_perturb':    1  [11,11]
>                     'no_lp':    1  [12,12]
>             'quick_restart':    7  [10,29]
>       'quick_restart_no_lp':    4  [25,32]
>               'rnd_cst_lns':    2   [2,31]
> 
> Objective bounds     Num
>        'bool_core':   60
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     90      500       77
>    'fj solution hints':      0        0        0
>         'lp solutions':     39        0       39
>                 'pump':    418        3
> 
> Improving bounds shared    Num  Sym
>                   'core':  259    0
>          'quick_restart':  672    0
>    'quick_restart_no_lp':  155    0
> 
> Clauses shared                Num
>                  'core':      498
>            'default_lp':   51'400
>          'pseudo_costs':    3'606
>         'quick_restart':  158'222
>   'quick_restart_no_lp':       42
>         'reduced_costs':        1
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 157
> best_bound: 60
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.703
> usertime: 120.703
> deterministic_time: 279.399
> gap_integral: 1258.43
> solution_fingerprint: 0xd15198151b42b937
> ```

In [ ]:
```python
instance04 = scsp.example.load("uniform_q05n010k010-010.txt")
```

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
> Initial optimization model '': (model_fingerprint: 0x36a98f53e50a01f8)
> #Variables: 105 (#bools: 50 in objective) (105 primary variables)
>   - 50 Booleans in [0,1]
>   - 50 in [0,5]
>   - 5 constants in {0,1,2,3,4} 
> #kAutomaton: 10
> #kLinear1: 50 (#enforced: 50)
> #kLinear2: 50 (#enforced: 50)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 50.
>   3.60e-05s  0.00e+00d  [DetectDominanceRelations] 
>   4.64e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.19e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   2.59e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   7.95e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=4'356 
> [Symmetry] Graph for symmetry has 18'830 nodes and 48'407 arcs.
> [Symmetry] Symmetry computation done. time: 0.00351307 dtime: 0.0071441
> [Symmetry] #generators: 28, average support size: 2
> [Symmetry] The model contains 10 duplicate constraints !
> [Symmetry] 8 orbits on 36 variables with sizes: 10,8,6,4,2,2,2,2
> [Symmetry] Found orbitope of size 1 x 6
> [SAT presolve] num removable Booleans: 314 / 4917
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:13732 literals:34028 vars:4879 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000715767s] clauses:13722 literals:33998 vars:4879 one_side_vars:0 simple_definition:10 singleton_clauses:0
> [SAT presolve] [0.00109404s] clauses:13624 literals:33998 vars:4830 one_side_vars:0 simple_definition:10 singleton_clauses:0
>   2.15e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.96e-02s  3.40e-01d  [Probe] #probed=9'836 #fixed_bools=9 #equiv=55 #new_binary_clauses=9'891 
>   2.71e-02s  1.02e-01d  [MaxClique] Merged 9'898(19'796 literals) into 3'397(13'085 literals) at_most_ones. 
>   1.05e-03s  0.00e+00d  [DetectDominanceRelations] 
>   5.37e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   5.94e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.30e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=100 
>   1.69e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.35e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   6.01e-05s  0.00e+00d  [DetectDifferentVariables] 
>   2.73e-03s  1.35e-04d  [ProcessSetPPC] #relevant_constraints=7'460 #num_inclusions=3'386 
>   7.82e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.00e-03s  9.95e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.42e-04s  9.21e-05d  [FindBigVerticalLinearOverlap] 
>   6.14e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.07e-04s  4.16e-06d  [MergeClauses] #num_collisions=147 #num_merges=147 #num_saved_literals=343 
>   7.46e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.51e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.32e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.35e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.90e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.26e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 9'819 nodes and 18'939 arcs.
> [Symmetry] Symmetry computation done. time: 0.00173487 dtime: 0.00369267
> [Symmetry] #generators: 9, average support size: 8
> [Symmetry] 28 orbits on 64 variables with sizes: 4,4,4,4,2,2,2,2,2,2,...
> [Symmetry] Found orbitope of size 4 x 4
> [SAT presolve] num removable Booleans: 0 / 4747
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:245 literals:833 vars:234 one_side_vars:0 simple_definition:223 singleton_clauses:0
> [SAT presolve] [2.5268e-05s] clauses:245 literals:833 vars:234 one_side_vars:0 simple_definition:223 singleton_clauses:0
> [SAT presolve] [0.000100411s] clauses:245 literals:833 vars:234 one_side_vars:0 simple_definition:223 singleton_clauses:0
>   1.56e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.54e-02s  3.55e-01d  [Probe] #probed=9'705 #fixed_bools=66 #equiv=211 #new_binary_clauses=9'623 
>   1.27e-04s  1.00e-04d  [MaxClique] 
>   7.41e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.65e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.91e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.68e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=154 
>   1.21e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.41e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.61e-05s  0.00e+00d  [DetectDifferentVariables] 
>   1.14e-03s  5.40e-05d  [ProcessSetPPC] #relevant_constraints=3'884 
>   7.66e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.67e-04s  9.24e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.42e-04s  8.83e-05d  [FindBigVerticalLinearOverlap] 
>   5.49e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.15e-04s  4.16e-06d  [MergeClauses] #num_collisions=147 #num_merges=147 #num_saved_literals=343 
>   7.30e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.32e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.18e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.31e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.80e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.23e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 9'599 nodes and 18'168 arcs.
> [Symmetry] Symmetry computation done. time: 0.00162087 dtime: 0.00349445
> [SAT presolve] num removable Booleans: 0 / 4470
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:255 literals:853 vars:247 one_side_vars:13 simple_definition:223 singleton_clauses:0
> [SAT presolve] [2.4657e-05s] clauses:255 literals:853 vars:247 one_side_vars:13 simple_definition:223 singleton_clauses:0
> [SAT presolve] [0.000102534s] clauses:255 literals:853 vars:247 one_side_vars:13 simple_definition:223 singleton_clauses:0
>   1.65e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.36e-02s  3.09e-01d  [Probe] #probed=9'704 #equiv=22 #new_binary_clauses=9'260 
>   1.26e-04s  9.99e-05d  [MaxClique] 
>   7.46e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.47e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.89e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.53e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=27 
>   1.19e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.43e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.64e-05s  0.00e+00d  [DetectDifferentVariables] 
>   1.12e-03s  5.37e-05d  [ProcessSetPPC] #relevant_constraints=3'857 
>   7.73e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.70e-04s  9.29e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.42e-04s  8.78e-05d  [FindBigVerticalLinearOverlap] 
>   5.60e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.08e-04s  4.16e-06d  [MergeClauses] #num_collisions=147 #num_merges=147 #num_saved_literals=343 
>   7.22e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.32e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.85e-03s  0.00e+00d  [ExpandObjective] #entries=90'696 #tight_variables=16'647 #tight_constraints=3'602 #expands=79 
> 
> Presolve summary:
>   - 385 affine relations were detected.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 7 times.
>   - rule 'affine: new relation' was applied 385 times.
>   - rule 'at_most_one: removed literals' was applied 12 times.
>   - rule 'at_most_one: satisfied' was applied 8 times.
>   - rule 'at_most_one: size one' was applied 12 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'automaton: expanded' was applied 10 times.
>   - rule 'bool_and: x => x' was applied 10 times.
>   - rule 'bool_or: always true' was applied 5 times.
>   - rule 'deductions: 100 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 4'637 times.
>   - rule 'exactly_one: removed literals' was applied 122 times.
>   - rule 'exactly_one: satisfied' was applied 31 times.
>   - rule 'exactly_one: singleton' was applied 10 times.
>   - rule 'exactly_one: x and not(x)' was applied 5 times.
>   - rule 'linear: always true' was applied 90 times.
>   - rule 'linear: enforcement literal in expression' was applied 90 times.
>   - rule 'linear: fixed or dup variables' was applied 90 times.
>   - rule 'linear: remapped using affine relations' was applied 590 times.
>   - rule 'new_bool: automaton expansion' was applied 4'867 times.
>   - rule 'objective: expanded via tight equality' was applied 79 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 73 times.
>   - rule 'presolve: 80 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'probing: bool_or reduced to implication' was applied 1 time.
>   - rule 'probing: simplified clauses.' was applied 11 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 3'376 times.
>   - rule 'setppc: removed dominated constraints' was applied 10 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 50 times.
>   - rule 'variables: detect half reified value encoding' was applied 100 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x6bf575ba44d440b7)
> #Variables: 4'448 (#bools: 79 in objective) (1'812 primary variables)
>   - 4'448 Booleans in [0,1]
> #kBoolAnd: 105 (#enforced: 105 #multi: 98) (#literals: 507)
> #kExactlyOne: 3'602 (#literals: 16'647)
> [Symmetry] Graph for symmetry has 9'045 nodes and 18'054 arcs.
> [Symmetry] Symmetry computation done. time: 0.00155701 dtime: 0.00328918
> 
> Preloading model.
> #Bound   0.43s best:inf   next:[0,50]     initial_domain
> #1       0.43s best:50    next:[0,49]     complete_hint
> #Model   0.43s var:4448/4448 constraints:3707/3707
> 
> Starting search at 0.43s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2       0.44s best:49    next:[0,48]     rnd_var_lns (d=5.00e-01 s=8 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3       0.48s best:48    next:[0,47]     ls_restart_decay(batch:1 lin{mvs:589 evals:1'165} #w_updates:57 #perturb:0)
> #4       0.49s best:47    next:[0,46]     graph_var_lns (d=7.07e-01 s=19 t=0.10 p=1.00 stall=1 h=base)
> #5       0.50s best:45    next:[0,44]     graph_cst_lns (d=7.07e-01 s=21 t=0.10 p=1.00 stall=1 h=base)
> #6       0.52s best:44    next:[0,43]     rnd_var_lns (d=8.14e-01 s=26 t=0.10 p=1.00 stall=0 h=base) [hint]
> #7       0.52s best:43    next:[0,42]     ls_restart_decay_compound(batch:1 lin{mvs:0 evals:56'851} gen{mvs:2'705 evals:0} comp{mvs:233 btracks:1'236} #w_updates:23 #perturb:0) [combined with: rnd_var_lns (d=8.14e...]
> #8       0.55s best:41    next:[0,40]     graph_arc_lns (d=8.14e-01 s=29 t=0.10 p=1.00 stall=0 h=base) [hint]
> #9       0.55s best:38    next:[0,37]     graph_var_lns (d=8.14e-01 s=28 t=0.10 p=1.00 stall=0 h=base)
> #10      0.59s best:35    next:[0,34]     rins_pump_lns (d=5.00e-01 s=24 t=0.10 p=0.00 stall=0 h=base)
> #11      0.60s best:33    next:[0,32]     no_lp
> #12      0.64s best:32    next:[0,31]     default_lp
> #Bound   0.86s best:32    next:[1,31]     reduced_costs
> #Bound   0.87s best:32    next:[2,31]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=74 d=2 fixed=0/4453 clauses=3'180)
> #Bound   0.87s best:32    next:[3,31]     bool_core (num_cores=3 [size:4 mw:1 d:2] a=71 d=2 fixed=0/4458 clauses=3'187)
> #Bound   0.87s best:32    next:[4,31]     bool_core (num_cores=4 [size:3 mw:1 d:2] a=69 d=2 fixed=0/4462 clauses=3'192)
> #Bound   0.88s best:32    next:[5,31]     bool_core (num_cores=5 [size:3 mw:1 d:2] a=67 d=2 fixed=0/4465 clauses=3'200)
> #Bound   0.88s best:32    next:[6,31]     bool_core (num_cores=6 [size:3 mw:1 d:2] a=65 d=2 fixed=0/4468 clauses=3'208)
> #Bound   0.89s best:32    next:[7,31]     bool_core (num_cores=7 [size:5 mw:1 d:3] a=61 d=3 fixed=0/4473 clauses=3'216)
> #Bound   0.89s best:32    next:[8,31]     bool_core (num_cores=8 [size:3 mw:1 d:2] a=59 d=3 fixed=0/4478 clauses=3'222)
> #Bound   0.89s best:32    next:[9,31]     bool_core (num_cores=9 [size:4 mw:1 d:2] a=56 d=3 fixed=0/4482 clauses=3'233)
> #Bound   0.90s best:32    next:[10,31]    bool_core (num_cores=10 [size:4 mw:1 d:3] a=53 d=3 fixed=0/4487 clauses=3'242)
> #Bound   0.90s best:32    next:[11,31]    bool_core (num_cores=11 [size:4 mw:1 d:2] a=50 d=3 fixed=0/4493 clauses=3'263)
> #Bound   0.90s best:32    next:[12,31]    bool_core (num_cores=12 [size:2 mw:1 d:3] a=49 d=3 fixed=0/4496 clauses=3'271)
> #Bound   0.91s best:32    next:[13,31]    bool_core (num_cores=13 [size:2 mw:1 d:3] a=48 d=3 fixed=0/4498 clauses=3'280)
> #Bound   0.91s best:32    next:[14,31]    bool_core (num_cores=14 [size:6 mw:1 amo:1 lit:3 d:4] a=43 d=4 fixed=0/4503 clauses=3'296)
> #Bound   0.92s best:32    next:[15,31]    bool_core (num_cores=15 [size:2 mw:1 d:3] a=42 d=4 fixed=0/4508 clauses=3'305)
> #13      0.92s best:31    next:[15,30]    no_lp
> #Bound   0.92s best:31    next:[16,30]    bool_core (num_cores=16 [size:4 mw:1 amo:1 lit:2 d:3] a=39 d=4 fixed=0/4513 clauses=3'318)
> #Bound   0.93s best:31    next:[17,30]    bool_core (num_cores=17 [size:4 mw:1 amo:1 lit:2 d:5] a=36 d=5 fixed=0/4518 clauses=3'336)
> #14      0.94s best:30    next:[17,29]    quick_restart_no_lp
> #Bound   0.94s best:30    next:[18,29]    bool_core (num_cores=18 [size:15 mw:1 amo:2 lit:14 d:4] a=23 d=5 fixed=0/4527 clauses=3'372)
> #Bound   0.95s best:30    next:[19,29]    bool_core (num_cores=19 [size:4 mw:1 d:6] a=20 d=6 fixed=0/4533 clauses=3'465)
> #Bound   0.98s best:30    next:[20,29]    bool_core (num_cores=20 [size:4 mw:1 amo:1 lit:2 d:7] a=17 d=7 fixed=0/4543 clauses=3'692)
> #Bound   1.00s best:30    next:[23,29]    bool_core (num_cores=23 [size:3 mw:1 d:6] a=13 d=7 fixed=0/4560 clauses=3'851) [skipped_logs=2]
> #Bound   1.07s best:30    next:[28,29]    max_lp [skipped_logs=2]
> #15      2.18s best:29    next:[28,28]    pseudo_costs
> #Done    2.49s bool_core (num_cores=28 [size:5 mw:1 exo] a=0 d=9 fixed=3/4622 clauses=16'063)
> #Done    2.49s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [   3.15s,    3.15s]    3.15s   0.00ns    3.15s
>            'default_lp':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [   2.51s,    2.51s]    2.51s   0.00ns    2.51s
>      'feasibility_pump':        15 [ 32.10us,  26.52ms]   1.81ms   6.60ms  27.16ms        14 [558.00ns, 558.00ns] 558.00ns   0.00ns   7.81us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        15 [ 12.40ms, 122.03ms]  63.21ms  38.46ms 948.08ms        15 [ 10.00ns, 100.22ms]  48.39ms  44.80ms 725.84ms
>         'graph_cst_lns':        15 [  7.87ms, 117.27ms]  44.73ms  37.45ms 670.91ms        15 [ 10.00ns, 100.01ms]  26.78ms  40.90ms 401.68ms
>         'graph_dec_lns':        15 [ 10.44ms, 163.57ms]  47.01ms  50.17ms 705.21ms        15 [ 10.00ns, 100.04ms]  19.78ms  37.47ms 296.70ms
>         'graph_var_lns':        16 [  3.75ms, 104.75ms]  53.00ms  34.22ms 848.06ms        15 [ 10.00ns, 100.16ms]  43.46ms  46.44ms 651.96ms
>                    'ls':        15 [  3.36ms, 142.26ms] 100.24ms  37.30ms    1.50s        15 [876.16us, 100.01ms]  87.88ms  31.05ms    1.32s
>                'ls_lin':        14 [ 99.60ms, 133.68ms] 113.35ms  10.57ms    1.59s        14 [100.00ms, 100.02ms] 100.00ms   4.04us    1.40s
>                'max_lp':         1 [   2.07s,    2.07s]    2.07s   0.00ns    2.07s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [   2.66s,    2.66s]    2.66s   0.00ns    2.66s
>          'pseudo_costs':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [883.71ms, 883.71ms] 883.71ms   0.00ns 883.71ms
>         'quick_restart':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [   2.20s,    2.20s]    2.20s   0.00ns    2.20s
>   'quick_restart_no_lp':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [   2.53s,    2.53s]    2.53s   0.00ns    2.53s
>         'reduced_costs':         1 [   2.06s,    2.06s]    2.06s   0.00ns    2.06s         1 [862.18ms, 862.18ms] 862.18ms   0.00ns 862.18ms
>             'rins/rens':        16 [  1.68ms,  96.56ms]  42.26ms  32.45ms 676.24ms        11 [  2.75us, 100.12ms]  40.00ms  41.18ms 440.05ms
>           'rnd_cst_lns':        16 [  8.99ms, 173.06ms]  41.36ms  47.02ms 661.80ms        15 [ 10.00ns, 100.24ms]  14.27ms  33.74ms 214.03ms
>           'rnd_var_lns':        16 [  9.09ms, 113.31ms]  34.97ms  31.69ms 559.46ms        15 [ 10.00ns, 100.09ms]  15.88ms  33.56ms 238.14ms
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  4'622     12'796    63'803    18'315  22'430'535        133'098
>            'default_lp':  4'448     13'056    55'978    18'009  13'875'759        391'022
>             'fs_random':      0          0         0         0           0              0
>       'fs_random_no_lp':      0          0         0         0           0              0
>                'max_lp':  4'448          0     8'896     8'896   2'637'215      2'646'115
>                 'no_lp':  4'448     16'724    61'274    18'134  14'871'265        423'161
>          'pseudo_costs':  4'448        174    41'243    17'988   6'858'449      6'862'531
>         'quick_restart':  4'448      7'043    69'769    18'687  13'082'437        292'992
>   'quick_restart_no_lp':  4'448      8'428    74'720    18'848  14'090'694        284'848
>         'reduced_costs':  4'448        235    41'209    18'003   6'925'046      6'947'216
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        11'047     181'488     288'787             0        47     7'229      22'997         0        673        4'447    1'737
>            'default_lp':        12'130     282'351     787'344       306'642         9     7'226      23'078         0        694        4'430    1'706
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':        14'775     278'515     922'748       290'424        34     7'234      23'186         0        681        4'367    1'635
>          'pseudo_costs':           152       2'151      10'930             0         0     7'249      23'238         0        661        4'176    1'698
>         'quick_restart':         5'394      75'924     368'526             0        23     7'231      23'171         0        669        4'216    1'648
>   'quick_restart_no_lp':         6'539      83'762     438'378             0        11     7'245      23'100         0        682        4'386    1'670
>         'reduced_costs':           203       3'052      17'774             0         0     7'246      23'161         0        668        4'255    1'674
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         14           0          0   25'231        0        0
>          'max_lp':          1       2'559         84        4        1        0
>    'pseudo_costs':          1       7'024      1'167       39      415        0
>   'quick_restart':         14           0          0   13'338        0        0
>   'reduced_costs':          1       7'492        911       31      512        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':            0 rows, 2 columns, 0 entries
>          'max_lp':  3773 rows, 4448 columns, 17962 entries
>    'pseudo_costs':  1907 rows, 4448 columns, 10129 entries
>   'quick_restart':            0 rows, 2 columns, 0 entries
>   'reduced_costs':   1709 rows, 4448 columns, 9512 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>          'max_lp':          0            0       5         0  57'976           0
>    'pseudo_costs':          0            0     271         0  17'781           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0     191         0  13'750           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':           16        0        0       0          0      0             0          0/0
>          'max_lp':        3'794      135       13       0         13      0             0       84/176
>    'pseudo_costs':        4'877        0        0       0          0      0             8  1'167/2'625
>   'quick_restart':           16        0        0       0          0      0             0          0/0
>   'reduced_costs':        4'621        0        0       0          0      0             0    911/1'893
> 
> Lp Cut           reduced_costs  pseudo_costs  max_lp
>          CG_FF:             66            84      11
>           CG_K:              9            22       -
>           CG_R:             12            29       -
>         Clique:             58            62      30
>      MIR_1_RLT:            143           169       -
>       MIR_4_FF:              -             1       -
>       MIR_5_FF:              2             -       -
>       MIR_6_FF:              2             -       -
>   ZERO_HALF_FF:            348           680      41
>    ZERO_HALF_R:            271           120       2
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          3/15     60%    9.05e-01       0.10
>   'graph_cst_lns':          2/15     87%    9.89e-01       0.10
>   'graph_dec_lns':          0/15     87%    9.89e-01       0.10
>   'graph_var_lns':          2/15     60%    8.80e-01       0.10
>       'rins/rens':          5/14     79%    9.26e-01       0.10
>     'rnd_cst_lns':          1/15     87%    9.89e-01       0.10
>     'rnd_var_lns':          3/15     87%    9.89e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>         'ls_lin_restart_compound_perturb':        3                  3         0    83'342          7'675     37'831            495      1'629'354
>                    'ls_lin_restart_decay':        1                  1    83'085         0              0          0            601          8'896
>           'ls_lin_restart_decay_compound':        1                  1         0    37'923         10'893     13'515             52        511'305
>   'ls_lin_restart_decay_compound_perturb':        2                  2         0    74'177         22'234     25'969             89      1'025'152
>            'ls_lin_restart_decay_perturb':        3                  3   249'883         0              0          0          1'781         26'688
>                  'ls_lin_restart_perturb':        4                  4   301'600         0              0          0         20'324         17'790
>                              'ls_restart':        2                  2   147'878         0              0          0          9'177          8'896
>                     'ls_restart_compound':        1                  1         0    26'590          2'544     12'023            137        529'594
>                        'ls_restart_decay':        3                  3   167'215         0              0          0          1'221         18'957
>               'ls_restart_decay_compound':        3                  3         0    73'767         16'916     28'423            111      1'115'635
>       'ls_restart_decay_compound_perturb':        1                  1         0    35'162          9'026     13'065             47        508'697
>                'ls_restart_decay_perturb':        4                  4   333'359         0              0          0          2'332         35'584
>                      'ls_restart_perturb':        1                  1    73'617         0              0          0          6'274          4'448
> 
> Solutions (15)                  Num     Rank
>               'complete_hint':    1    [1,1]
>                  'default_lp':    1  [12,12]
>               'graph_arc_lns':    1    [8,8]
>               'graph_cst_lns':    1    [5,5]
>               'graph_var_lns':    2    [4,9]
>            'ls_restart_decay':    1    [3,3]
>   'ls_restart_decay_compound':    1    [7,7]
>                       'no_lp':    2  [11,13]
>                'pseudo_costs':    1  [15,15]
>         'quick_restart_no_lp':    1  [14,14]
>               'rins_pump_lns':    1  [10,10]
>                 'rnd_var_lns':    2    [2,6]
> 
> Objective bounds     Num
>        'bool_core':   24
>   'initial_domain':    1
>           'max_lp':    1
>    'reduced_costs':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     44      258       34
>    'fj solution hints':      0        0        0
>         'lp solutions':      5        3        4
>                 'pump':     14       13
> 
> Improving bounds shared    Num  Sym
>                   'core':   65    0
>                 'max_lp':    5    0
> 
> Clauses shared            Num
>                  'core':  813
>            'default_lp':  254
>          'pseudo_costs':   90
>         'quick_restart':   44
>   'quick_restart_no_lp':   84
>         'reduced_costs':    1
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 29
> best_bound: 29
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 2.51075
> usertime: 2.51075
> deterministic_time: 21.5873
> gap_integral: 7.17732
> solution_fingerprint: 0x4ebcddcc7f957389
> ```

In [ ]:
```python
instance05 = scsp.example.load("uniform_q05n050k010-010.txt")
```

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
> Initial optimization model '': (model_fingerprint: 0xd54b493ab9d279de)
> #Variables: 105 (#bools: 50 in objective) (105 primary variables)
>   - 50 Booleans in [0,1]
>   - 50 in [0,5]
>   - 5 constants in {0,1,2,3,4} 
> #kAutomaton: 50
> #kLinear1: 50 (#enforced: 50)
> #kLinear2: 50 (#enforced: 50)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 50.
>   6.97e-05s  0.00e+00d  [DetectDominanceRelations] 
>   9.60e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.08e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   3.96e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   6.39e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=21'474 
> [Symmetry] Graph for symmetry has 91'413 nodes and 236'551 arcs.
> [Symmetry] Symmetry computation done. time: 0.0276285 dtime: 0.0389261
> [Symmetry] #generators: 244, average support size: 2
> [Symmetry] The model contains 50 duplicate constraints !
> [Symmetry] 9 orbits on 253 variables with sizes: 50,40,38,33,28,25,21,11,7
> [Symmetry] Found orbitope of size 1 x 38
> [SAT presolve] num removable Booleans: 1499 / 23946
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:67090 literals:166366 vars:23692 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00431719s] clauses:67040 literals:166216 vars:23692 one_side_vars:0 simple_definition:50 singleton_clauses:0
> [SAT presolve] [0.0065543s] clauses:66442 literals:166216 vars:23393 one_side_vars:0 simple_definition:50 singleton_clauses:0
>   1.49e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.99e-01s  1.00e+00d *[Probe] #probed=8'660 #fixed_bools=68 #equiv=63 #new_binary_clauses=19'487 
>   2.42e-01s  1.00e+00d *[MaxClique] Merged 48'118(96'236 literals) into 27'986(75'864 literals) at_most_ones. 
>   6.87e-03s  0.00e+00d  [DetectDominanceRelations] 
>   3.48e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   5.96e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.14e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=104 
>   1.80e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.55e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   7.19e-04s  0.00e+00d  [DetectDifferentVariables] 
>   1.92e-02s  7.67e-04d  [ProcessSetPPC] #relevant_constraints=48'256 #num_inclusions=27'874 
>   1.38e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.99e-03s  5.01e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   1.40e-03s  6.71e-04d  [FindBigVerticalLinearOverlap] 
>   9.87e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   3.70e-03s  1.83e-04d  [MergeClauses] #num_collisions=1'170 #num_merges=1'170 #num_saved_literals=2'639 
>   6.23e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.84e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.02e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.78e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.97e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.67e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 82'252 nodes and 170'477 arcs.
> [Symmetry] Symmetry computation done. time: 0.0214112 dtime: 0.0328205
> [Symmetry] #generators: 8, average support size: 8
> [Symmetry] 28 orbits on 60 variables with sizes: 3,3,3,3,2,2,2,2,2,2,...
> [Symmetry] Found orbitope of size 4 x 2
> [SAT presolve] num removable Booleans: 971 / 23163
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:32982 literals:79188 vars:19363 one_side_vars:0 simple_definition:12017 singleton_clauses:0
> [SAT presolve] [0.00183182s] clauses:32982 literals:79188 vars:19363 one_side_vars:0 simple_definition:12017 singleton_clauses:0
> [SAT presolve] [0.00321035s] clauses:32982 literals:79188 vars:19363 one_side_vars:0 simple_definition:12017 singleton_clauses:0
>   1.95e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.11e-01s  1.00e+00d *[Probe] #probed=7'802 #fixed_bools=111 #equiv=225 #new_binary_clauses=19'982 
>   1.49e-01s  6.08e-01d  [MaxClique] Merged 21'359(42'718 literals) into 10'072(31'119 literals) at_most_ones. 
>   6.00e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.95e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.85e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.93e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=264 
>   1.67e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.10e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   8.49e-04s  0.00e+00d  [DetectDifferentVariables] 
>   1.58e-02s  4.63e-04d  [ProcessSetPPC] #relevant_constraints=30'078 #num_inclusions=9'974 
>   1.11e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.61e-03s  4.77e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   1.36e-03s  4.52e-04d  [FindBigVerticalLinearOverlap] 
>   1.07e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.72e-03s  2.61e-05d  [MergeClauses] #num_collisions=897 #num_merges=897 #num_saved_literals=2'093 
>   5.13e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.72e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.23e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.62e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.34e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.62e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 47'795 nodes and 92'856 arcs.
> [Symmetry] Symmetry computation done. time: 0.0116283 dtime: 0.0200945
> [Symmetry] #generators: 63, average support size: 8
> [Symmetry] 56 orbits on 308 variables with sizes: 14,14,14,14,9,9,9,9,8,8,...
> [Symmetry] Found orbitope of size 4 x 6
> [SAT presolve] num removable Booleans: 0 / 22827
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1593 literals:5327 vars:1594 one_side_vars:148 simple_definition:1397 singleton_clauses:0
> [SAT presolve] [0.000163049s] clauses:1593 literals:5327 vars:1594 one_side_vars:148 simple_definition:1397 singleton_clauses:0
> [SAT presolve] [0.000607062s] clauses:1593 literals:5327 vars:1594 one_side_vars:148 simple_definition:1397 singleton_clauses:0
>   2.17e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.12e-01s  1.00e+00d *[Probe] #probed=8'486 #fixed_bools=19 #equiv=50 #new_binary_clauses=20'880 
>   3.76e-03s  8.42e-03d  [MaxClique] 
>   5.35e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.72e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.83e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.63e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=52 
>   1.31e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.13e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   8.61e-04s  0.00e+00d  [DetectDifferentVariables] 
>   9.13e-03s  2.77e-04d  [ProcessSetPPC] #relevant_constraints=20'042 
>   1.11e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.75e-03s  4.75e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   1.38e-03s  4.50e-04d  [FindBigVerticalLinearOverlap] 
>   1.07e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.68e-03s  2.61e-05d  [MergeClauses] #num_collisions=897 #num_merges=897 #num_saved_literals=2'093 
>   5.13e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.63e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.78e-02s  0.00e+00d  [ExpandObjective] #entries=462'296 #tight_variables=84'572 #tight_constraints=18'401 #expands=80 
> 
> Presolve summary:
>   - 691 affine relations were detected.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 7 times.
>   - rule 'affine: new relation' was applied 691 times.
>   - rule 'at_most_one: removed literals' was applied 85 times.
>   - rule 'at_most_one: satisfied' was applied 63 times.
>   - rule 'at_most_one: size one' was applied 85 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'automaton: expanded' was applied 50 times.
>   - rule 'bool_and: x => x' was applied 10 times.
>   - rule 'bool_or: always true' was applied 40 times.
>   - rule 'deductions: 100 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 21'894 times.
>   - rule 'exactly_one: removed literals' was applied 299 times.
>   - rule 'exactly_one: satisfied' was applied 61 times.
>   - rule 'exactly_one: singleton' was applied 50 times.
>   - rule 'exactly_one: x and not(x)' was applied 12 times.
>   - rule 'linear: always true' was applied 90 times.
>   - rule 'linear: enforcement literal in expression' was applied 90 times.
>   - rule 'linear: fixed or dup variables' was applied 90 times.
>   - rule 'linear: remapped using affine relations' was applied 2'590 times.
>   - rule 'new_bool: automaton expansion' was applied 23'896 times.
>   - rule 'objective: expanded via tight equality' was applied 80 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 71 times.
>   - rule 'presolve: 203 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'probing: bool_or reduced to implication' was applied 9 times.
>   - rule 'probing: simplified clauses.' was applied 70 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 16'487 times.
>   - rule 'setppc: removed dominated constraints' was applied 51 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 50 times.
>   - rule 'variables: detect half reified value encoding' was applied 100 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x6f3a5afa6374d42c)
> #Variables: 22'758 (#bools: 98 in objective) (9'232 primary variables)
>   - 22'758 Booleans in [0,1]
> #kAtMostOne: 48 (#literals: 144)
> #kBoolAnd: 607 (#enforced: 607 #multi: 598) (#literals: 3'049)
> #kBoolOr: 48 (#literals: 144)
> #kExactlyOne: 18'401 (#literals: 84'572)
> [Symmetry] Graph for symmetry has 46'483 nodes and 92'580 arcs.
> [Symmetry] Symmetry computation done. time: 0.0103183 dtime: 0.0195655
> [Symmetry] #generators: 61, average support size: 8
> [Symmetry] 56 orbits on 300 variables with sizes: 14,14,14,14,8,8,8,8,8,8,...
> [Symmetry] Found orbitope of size 4 x 6
> 
> Preloading model.
> #Bound   1.98s best:inf   next:[0,50]     initial_domain
> #1       1.98s best:50    next:[0,49]     complete_hint
> #Model   1.99s var:22758/22758 constraints:19104/19104
> 
> Starting search at 1.99s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2       2.14s best:49    next:[0,48]     graph_dec_lns (d=5.00e-01 s=13 t=0.10 p=0.00 stall=0 h=base) [hint]
> #Model   3.09s var:22728/22758 constraints:19089/19104
> #3       3.09s best:38    next:[0,37]     core
> #4       3.12s best:36    next:[0,35]     no_lp
> #Model   3.61s var:22709/22758 constraints:19080/19104
> #Model   3.71s var:22568/22758 constraints:19014/19104
> #Model   3.80s var:22553/22758 constraints:19007/19104
> #Model   3.91s var:22511/22758 constraints:18985/19104
> #Model   4.03s var:22455/22758 constraints:18956/19104
> #Model   4.10s var:22434/22758 constraints:18945/19104
> #Model   4.14s var:22425/22758 constraints:18941/19104
> #Model   4.28s var:22350/22758 constraints:18906/19104
> #Model   4.51s var:22028/22758 constraints:18754/19104
> #Model   4.53s var:22027/22758 constraints:18754/19104
> #Model   4.56s var:21975/22758 constraints:18727/19104
> #Model   5.01s var:21965/22758 constraints:18722/19104
> #Model   5.05s var:21956/22758 constraints:18718/19104
> #Model   5.16s var:21946/22758 constraints:18713/19104
> #Model   5.25s var:21936/22758 constraints:18708/19104
> #Model   5.38s var:21925/22758 constraints:18703/19104
> #Model   5.40s var:21914/22758 constraints:18697/19104
> #Model   5.53s var:21875/22758 constraints:18678/19104
> #Model   5.56s var:21874/22758 constraints:18678/19104
> #Model   5.68s var:21863/22758 constraints:18673/19104
> #Model   5.70s var:21842/22758 constraints:18662/19104
> #Model   5.82s var:21831/22758 constraints:18657/19104
> #Model   6.01s var:21830/22758 constraints:18657/19104
> #Bound   6.14s best:36    next:[1,35]     pseudo_costs
> #Model   6.15s var:21811/22758 constraints:18647/19104
> #Bound   6.21s best:36    next:[15,35]    max_lp_sym
> #Model   6.68s var:21810/22758 constraints:18647/19104
> #Bound   6.91s best:36    next:[19,35]    max_lp_sym
> #Model   7.15s var:21807/22758 constraints:18647/19104
> #Bound   7.40s best:36    next:[20,35]    bool_core (num_cores=20 [size:4 mw:1 amo:1 lit:2 d:6] a=42 d=6 fixed=952/22827 clauses=17'966)
> #Bound   7.52s best:36    next:[21,35]    bool_core (num_cores=21 [size:5 mw:1 amo:1 lit:4 d:3] a=37 d=6 fixed=961/22833 clauses=18'010)
> #Bound   7.61s best:36    next:[22,35]    bool_core (num_cores=22 [size:2 mw:1 d:3] a=36 d=6 fixed=968/22835 clauses=18'041)
> #Bound   7.67s best:36    next:[23,35]    bool_core (num_cores=23 [size:2 mw:1 d:4] a=35 d=6 fixed=968/22838 clauses=18'064)
> #Bound   7.86s best:36    next:[24,35]    bool_core (num_cores=24 [size:4 mw:1 d:7] a=31 d=7 fixed=978/22843 clauses=18'195)
> #Bound   7.96s best:36    next:[25,35]    bool_core (num_cores=25 [size:3 mw:1 d:4] a=30 d=7 fixed=978/22852 clauses=18'251)
> #Model   7.69s var:21780/22758 constraints:18632/19104 [skipped_logs=3]
> #Bound   8.06s best:36    next:[26,35]    bool_core (num_cores=26 [size:2 mw:1 d:5] a=29 d=7 fixed=978/22856 clauses=18'295)
> #Bound   8.06s best:36    next:[27,35]    max_lp_sym
> #5       8.40s best:35    next:[27,34]    quick_restart_no_lp
> #Model   8.90s var:21761/22758 constraints:18622/19104 [skipped_logs=1]
> #Bound   9.22s best:35    next:[28,34]    bool_core (num_cores=28 [size:3 mw:1 d:6] a=26 d=8 fixed=978/22869 clauses=19'057)
> #Model   9.98s var:21702/22758 constraints:18590/19104 [skipped_logs=3]
> #Bound  10.35s best:35    next:[29,34]    bool_core (num_cores=29 [size:3 mw:1 d:9] a=24 d=9 fixed=1007/22878 clauses=19'756)
> #Model  10.91s var:21657/22758 constraints:18568/19104 [skipped_logs=4]
> #Bound  11.70s best:35    next:[30,34]    bool_core (num_cores=30 [size:2 mw:1 d:10] a=23 d=10 fixed=1079/22886 clauses=20'728)
> #Model  11.15s var:21627/22758 constraints:18553/19104 [skipped_logs=1]
> #Model  12.78s var:21617/22758 constraints:18548/19104 [skipped_logs=0]
> #Model  13.16s var:21607/22758 constraints:18543/19104 [skipped_logs=0]
> #Bound  16.48s best:35    next:[31,34]    bool_core (num_cores=31 [size:1 mw:1] a=21 d=10 fixed=1141/22897 clauses=24'216)
> #Model  17.26s var:21597/22758 constraints:18538/19104
> #Model  20.60s var:21587/22758 constraints:18533/19104
> #Bound  21.16s best:35    next:[32,34]    bool_core (num_cores=32 [size:2 mw:1 d:11] a=17 d=11 fixed=1162/22906 clauses=27'329)
> #Model  28.06s var:21585/22758 constraints:18533/19104
> #Bound  28.49s best:35    next:[33,34]    bool_core (num_cores=33 [size:3 mw:1 amo:1 lit:2 d:12] a=15 d=12 fixed=1172/22917 clauses=32'218)
> #Model  30.04s var:21567/22758 constraints:18523/19104
> #Model  30.23s var:21557/22758 constraints:18518/19104
> #Model  30.59s var:21547/22758 constraints:18513/19104
> #Model  30.89s var:21532/22758 constraints:18508/19104
> #Model  32.60s var:21530/22758 constraints:18508/19104
> #Model  36.07s var:21521/22758 constraints:18503/19104
> #Model  36.55s var:21453/22758 constraints:18470/19104
> #Model  37.27s var:21440/22758 constraints:18465/19104
> #Model  37.55s var:21430/22758 constraints:18460/19104
> #Model  37.68s var:21412/22758 constraints:18460/19104
> #Model  37.79s var:21402/22758 constraints:18455/19104
> #Model  38.08s var:21400/22758 constraints:18455/19104
> #Model  38.24s var:21392/22758 constraints:18450/19104
> #Model  39.68s var:21382/22758 constraints:18445/19104
> #Bound  41.67s best:35    next:[34,34]    bool_core (num_cores=34 [size:4 mw:1 exo] a=0 d=12 fixed=1174/22933 clauses=35'391)
> #Model  41.74s var:21354/22758 constraints:18431/19104
> #Model  42.52s var:21353/22758 constraints:18431/19104
> #Model  42.67s var:21352/22758 constraints:18431/19104
> #Model  43.82s var:21351/22758 constraints:18431/19104
> #Model  48.64s var:20828/22758 constraints:18249/19104
> #6      51.40s best:34    next:[]         core
> #Done   51.40s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  49.41s,   49.41s]   49.41s   0.00ns   49.41s         1 [  32.89s,   32.89s]   32.89s   0.00ns   32.89s
>            'default_lp':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  30.62s,   30.62s]   30.62s   0.00ns   30.62s
>      'feasibility_pump':       209 [ 16.05us, 416.71ms]   2.06ms  28.75ms 431.40ms       208 [  1.05us,   1.05us]   1.05us   0.00ns 218.40us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        53 [ 68.66ms, 805.49ms] 402.57ms 226.66ms   21.34s        53 [ 10.00ns, 101.69ms]  46.10ms  44.73ms    2.44s
>         'graph_cst_lns':        56 [ 57.07ms, 913.23ms] 406.44ms 256.17ms   22.76s        56 [ 10.00ns, 101.64ms]  45.64ms  45.08ms    2.56s
>         'graph_dec_lns':        49 [ 72.43ms, 912.06ms] 444.65ms 291.40ms   21.79s        49 [ 10.00ns, 103.17ms]  43.54ms  45.40ms    2.13s
>         'graph_var_lns':        52 [ 60.30ms, 886.66ms] 416.91ms 197.69ms   21.68s        52 [ 10.00ns, 103.36ms]  67.63ms  36.38ms    3.52s
>                    'ls':       112 [ 60.29ms, 243.72ms] 185.96ms  37.14ms   20.83s       112 [ 40.26ms, 100.29ms]  99.51ms   5.62ms   11.14s
>                'ls_lin':       113 [105.70ms, 284.54ms] 184.59ms  43.99ms   20.86s       113 [ 62.33ms, 100.31ms]  99.70ms   3.53ms   11.27s
>            'max_lp_sym':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  18.24s,   18.24s]   18.24s   0.00ns   18.24s
>                 'no_lp':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  28.29s,   28.29s]   28.29s   0.00ns   28.29s
>          'pseudo_costs':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  11.30s,   11.30s]   11.30s   0.00ns   11.30s
>         'quick_restart':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  29.81s,   29.81s]   29.81s   0.00ns   29.81s
>   'quick_restart_no_lp':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  26.94s,   26.94s]   26.94s   0.00ns   26.94s
>         'reduced_costs':         1 [  49.42s,   49.42s]   49.42s   0.00ns   49.42s         1 [  11.86s,   11.86s]   11.86s   0.00ns   11.86s
>             'rins/rens':        98 [  7.36ms, 811.99ms] 216.84ms 211.52ms   21.25s        69 [ 10.00ns, 100.90ms]  65.75ms  47.28ms    4.54s
>           'rnd_cst_lns':        52 [ 79.09ms, 932.95ms] 425.05ms 288.60ms   22.10s        52 [ 10.00ns, 101.39ms]  44.92ms  46.34ms    2.34s
>           'rnd_var_lns':        54 [ 74.44ms, 971.01ms] 420.57ms 276.21ms   22.71s        54 [ 10.00ns, 101.39ms]  41.90ms  45.02ms    2.26s
> 
> Search stats               Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  22'933     27'318   106'604    14'862  199'843'979        235'085
>            'default_lp':  22'758     29'824    95'929    14'455  128'113'816        676'296
>             'fs_random':       0          0         0         0            0              0
>       'fs_random_no_lp':       0          0         0         0            0              0
>            'max_lp_sym':  22'758        212    37'267    10'931   25'006'285     24'852'828
>                 'no_lp':  22'758     28'715    94'029    14'332  120'953'067        561'971
>          'pseudo_costs':  22'758      4'605    42'613    10'983   40'261'970     35'782'037
>         'quick_restart':  22'758     19'147   137'641    16'112  132'387'234        593'635
>   'quick_restart_no_lp':  22'758     17'185   130'001    15'814  122'052'548        461'250
>         'reduced_costs':  22'758      3'334    41'973    11'102   36'768'684     34'556'114
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        23'860     588'585     839'112       121'958        70     6'543      39'083         0      1'740       11'993      180
>            'default_lp':        26'493     776'562   1'645'710       646'708        16     6'606      39'204         0      1'748       12'241      233
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':           176       6'075      13'632             0         0     3'126      21'310         0      1'135        7'534       81
>                 'no_lp':        25'110     598'796   1'521'783       634'972        11     6'525      38'932         0      1'792       12'359      282
>          'pseudo_costs':         4'059     103'482     238'346             0         4     3'128      21'440         0      1'153        7'542       85
>         'quick_restart':        15'469     384'513   1'291'647       333'282        22     6'534      39'059         0      1'751       12'022      204
>   'quick_restart_no_lp':        13'931     323'564   1'091'530       316'028        10     6'417      38'712         0      1'734       11'934      196
>         'reduced_costs':         2'931      73'844     274'946             0         2     3'221      21'861         0      1'165        7'746       70
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         13           0          0   49'868        0        0
>      'max_lp_sym':          1      41'783      1'073        1      536        0
>    'pseudo_costs':          1      73'996        654      177    6'965        0
>   'quick_restart':         13           0          0   42'344        0        0
>   'reduced_costs':          1      65'992      3'527      241    5'591        0
> 
> Lp dimension              Final dimension of first component
>      'default_lp':              0 rows, 2 columns, 0 entries
>      'max_lp_sym':  18319 rows, 22514 columns, 83454 entries
>    'pseudo_costs':   6332 rows, 22758 columns, 22073 entries
>   'quick_restart':              0 rows, 2 columns, 0 entries
>   'reduced_costs':   7624 rows, 22758 columns, 26688 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow      Bad  BadScaling
>      'default_lp':          0            0       0         0        0           0
>      'max_lp_sym':          0            0     536         0  141'577           0
>    'pseudo_costs':          0            0   1'003         0   16'720           0
>   'quick_restart':          0            0       0         0        0           0
>   'reduced_costs':          0            0     504         0   87'273           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':           36        0      102       0         31      0             0          0/0
>      'max_lp_sym':       19'903      442    2'060       0      2'104      0             0  1'073/1'777
>    'pseudo_costs':       19'789        3    5'217       0      2'399      0             0    654/1'669
>   'quick_restart':           36        0      150       0         31      0             0          0/0
>   'reduced_costs':       22'662        5    6'410       0      3'428      0             1  3'527/8'932
> 
> Lp Cut           max_lp_sym  reduced_costs  pseudo_costs
>          CG_FF:          10            322           164
>           CG_K:           -             10             -
>           CG_R:          11             19             -
>         Clique:          12            388           201
>      MIR_1_RLT:           -            379           224
>       MIR_4_FF:           2              -             2
>       MIR_5_FF:           3              2             3
>       MIR_6_FF:           9              7             -
>   ZERO_HALF_FF:         212          2'073            59
>    ZERO_HALF_R:         814            327             1
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          1/53     64%    9.93e-01       0.10
>   'graph_cst_lns':          1/56     64%    9.97e-01       0.10
>   'graph_dec_lns':          1/49     67%    9.98e-01       0.10
>   'graph_var_lns':          3/52     56%    9.63e-01       0.10
>       'rins/rens':         21/90     49%    9.28e-02       0.10
>     'rnd_cst_lns':          0/52     63%    9.96e-01       0.10
>     'rnd_var_lns':          0/54     67%    9.98e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                          'ls_lin_restart':       20                  9  1'537'841         0              0          0         36'071        277'445
>                 'ls_lin_restart_compound':       12                  8          0    44'234          1'632     21'298            357      7'592'391
>         'ls_lin_restart_compound_perturb':       13                  8          0    64'412          3'305     30'544            446      7'972'509
>                    'ls_lin_restart_decay':        8                  6    668'381         0              0          0          1'432        165'653
>           'ls_lin_restart_decay_compound':       18                 11          0   113'394         13'672     49'841            437     10'556'502
>   'ls_lin_restart_decay_compound_perturb':       18                  8          0   303'400         32'845    135'077            322      9'971'635
>            'ls_lin_restart_decay_perturb':       12                  7  1'000'475         0              0          0          2'039        266'734
>                  'ls_lin_restart_perturb':       12                 10    943'886         0              0          0         24'083        194'061
>                              'ls_restart':        9                  7    658'453         0              0          0         16'636        137'870
>                     'ls_restart_compound':        8                  7          0    32'877          1'359     15'756            284      4'964'577
>             'ls_restart_compound_perturb':       13                  6          0    62'868          3'713     29'569            435      8'026'881
>                        'ls_restart_decay':       17                  9  1'420'240         0              0          0          2'910        384'964
>               'ls_restart_decay_compound':       17                  8          0   283'928         31'556    126'132            322      9'310'319
>       'ls_restart_decay_compound_perturb':       22                 10          0   290'935         40'827    124'991            417     12'270'824
>                'ls_restart_decay_perturb':       13                  9  1'081'361         0              0          0          2'336        281'239
>                      'ls_restart_perturb':       13                 10  1'013'254         0              0          0         23'586        216'539
> 
> Solutions (6)             Num   Rank
>         'complete_hint':    1  [1,1]
>                  'core':    2  [3,6]
>         'graph_dec_lns':    1  [2,2]
>                 'no_lp':    1  [4,4]
>   'quick_restart_no_lp':    1  [5,5]
> 
> Objective bounds     Num
>        'bool_core':   14
>   'initial_domain':    1
>       'max_lp_sym':    3
>     'pseudo_costs':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    173    1'034      125
>    'fj solution hints':      0        0        0
>         'lp solutions':    100       33       92
>                 'pump':    208       65
> 
> Improving bounds shared      Num  Sym
>                   'core':  1'401    0
>             'default_lp':    119    0
>             'max_lp_sym':     66    0
>                  'no_lp':      9    0
>           'pseudo_costs':    172    0
>          'quick_restart':     94    0
>    'quick_restart_no_lp':     69    0
> 
> Clauses shared               Num
>                  'core':  72'805
>            'default_lp':  16'230
>            'max_lp_sym':  28'411
>                 'no_lp':  13'681
>          'pseudo_costs':  35'323
>         'quick_restart':  14'632
>   'quick_restart_no_lp':   4'876
>         'reduced_costs':      97
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 34
> best_bound: 34
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 51.4557
> usertime: 51.4557
> deterministic_time: 236.776
> gap_integral: 47.291
> solution_fingerprint: 0x6f36fcc5693bf881
> ```

In [ ]:
```python
instance06 = scsp.example.load("nucleotide_n010k010.txt")
```

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
> Initial optimization model '': (model_fingerprint: 0xf915dff1f4e91e99)
> #Variables: 84 (#bools: 40 in objective) (84 primary variables)
>   - 40 Booleans in [0,1]
>   - 40 in [0,4]
>   - 4 constants in {0,1,2,3} 
> #kAutomaton: 10
> #kLinear1: 40 (#enforced: 40)
> #kLinear2: 40 (#enforced: 40)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 40.
>   2.60e-05s  0.00e+00d  [DetectDominanceRelations] 
>   1.55e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.57e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.69e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   5.47e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2'697 
> [Symmetry] Graph for symmetry has 13'133 nodes and 33'522 arcs.
> [Symmetry] Symmetry computation done. time: 0.00243195 dtime: 0.00501712
> [Symmetry] #generators: 39, average support size: 2
> [Symmetry] The model contains 10 duplicate constraints !
> [Symmetry] 7 orbits on 46 variables with sizes: 10,7,7,6,6,6,4
> [Symmetry] Found orbitope of size 1 x 6
> [SAT presolve] num removable Booleans: 239 / 3403
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:9575 literals:23609 vars:3356 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000502884s] clauses:9565 literals:23579 vars:3356 one_side_vars:0 simple_definition:10 singleton_clauses:0
> [SAT presolve] [0.00080136s] clauses:9465 literals:23579 vars:3306 one_side_vars:0 simple_definition:10 singleton_clauses:0
>   9.12e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.26e-02s  1.93e-01d  [Probe] #probed=6'826 #equiv=39 #new_binary_clauses=7'647 
>   1.69e-02s  5.94e-02d  [MaxClique] Merged 6'762(13'524 literals) into 2'382(8'992 literals) at_most_ones. 
>   7.45e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.68e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   4.14e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.84e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=71 
>   1.36e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.76e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.90e-05s  0.00e+00d  [DetectDifferentVariables] 
>   1.95e-03s  9.36e-05d  [ProcessSetPPC] #relevant_constraints=5'368 #num_inclusions=2'392 
>   5.36e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.74e-04s  6.15e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.05e-04s  6.47e-05d  [FindBigVerticalLinearOverlap] 
>   4.12e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.51e-04s  4.25e-06d  [MergeClauses] #num_collisions=150 #num_merges=150 #num_saved_literals=350 
>   5.17e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.71e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.17e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.66e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.96e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   9.47e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 7'042 nodes and 13'319 arcs.
> [Symmetry] Symmetry computation done. time: 0.00128296 dtime: 0.0026479
> [Symmetry] #generators: 12, average support size: 8
> [Symmetry] 20 orbits on 68 variables with sizes: 5,5,5,5,4,4,4,4,3,3,...
> [Symmetry] Found orbitope of size 4 x 5
> [SAT presolve] num removable Booleans: 0 / 3248
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:250 literals:850 vars:231 one_side_vars:0 simple_definition:212 singleton_clauses:0
> [SAT presolve] [2.3454e-05s] clauses:250 literals:850 vars:231 one_side_vars:0 simple_definition:212 singleton_clauses:0
> [SAT presolve] [8.3438e-05s] clauses:250 literals:850 vars:231 one_side_vars:0 simple_definition:212 singleton_clauses:0
>   1.07e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.92e-02s  2.11e-01d  [Probe] #probed=6'696 #fixed_bools=66 #equiv=195 #new_binary_clauses=7'831 
>   9.89e-05s  8.54e-05d  [MaxClique] 
>   5.25e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.88e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.12e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.25e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=154 
>   8.96e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.74e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.87e-05s  0.00e+00d  [DetectDifferentVariables] 
>   7.99e-04s  3.70e-05d  [ProcessSetPPC] #relevant_constraints=2'781 
>   5.47e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.44e-04s  5.64e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.02e-04s  6.09e-05d  [FindBigVerticalLinearOverlap] 
>   4.08e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.49e-04s  4.25e-06d  [MergeClauses] #num_collisions=150 #num_merges=150 #num_saved_literals=350 
>   5.16e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.60e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.08e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.59e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.87e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   8.48e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 6'816 nodes and 12'530 arcs.
> [Symmetry] Symmetry computation done. time: 0.00113933 dtime: 0.00241757
> [SAT presolve] num removable Booleans: 0 / 2987
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:260 literals:870 vars:245 one_side_vars:14 simple_definition:212 singleton_clauses:0
> [SAT presolve] [2.3465e-05s] clauses:260 literals:870 vars:245 one_side_vars:14 simple_definition:212 singleton_clauses:0
> [SAT presolve] [8.4621e-05s] clauses:260 literals:870 vars:245 one_side_vars:14 simple_definition:212 singleton_clauses:0
>   9.86e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.91e-02s  1.73e-01d  [Probe] #probed=6'694 #equiv=31 #new_binary_clauses=7'297 
>   9.79e-05s  8.54e-05d  [MaxClique] 
>   5.18e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.69e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.03e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.10e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=33 
>   8.62e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.83e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   4.01e-05s  0.00e+00d  [DetectDifferentVariables] 
>   7.87e-04s  3.66e-05d  [ProcessSetPPC] #relevant_constraints=2'748 
>   5.36e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.41e-04s  5.60e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   9.93e-05s  6.02e-05d  [FindBigVerticalLinearOverlap] 
>   4.14e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.53e-04s  4.25e-06d  [MergeClauses] #num_collisions=150 #num_merges=150 #num_saved_literals=350 
>   5.17e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.62e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.24e-03s  0.00e+00d  [ExpandObjective] #entries=53'206 #tight_variables=11'126 #tight_constraints=2'488 #expands=72 
> 
> Presolve summary:
>   - 361 affine relations were detected.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 7 times.
>   - rule 'affine: new relation' was applied 361 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'automaton: expanded' was applied 10 times.
>   - rule 'bool_and: x => x' was applied 10 times.
>   - rule 'deductions: 80 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 2'955 times.
>   - rule 'exactly_one: removed literals' was applied 125 times.
>   - rule 'exactly_one: satisfied' was applied 30 times.
>   - rule 'exactly_one: singleton' was applied 10 times.
>   - rule 'exactly_one: x and not(x)' was applied 11 times.
>   - rule 'linear: always true' was applied 70 times.
>   - rule 'linear: enforcement literal in expression' was applied 70 times.
>   - rule 'linear: fixed or dup variables' was applied 70 times.
>   - rule 'linear: remapped using affine relations' was applied 470 times.
>   - rule 'new_bool: automaton expansion' was applied 3'363 times.
>   - rule 'objective: expanded via tight equality' was applied 72 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 66 times.
>   - rule 'presolve: 70 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 2'382 times.
>   - rule 'setppc: removed dominated constraints' was applied 10 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 40 times.
>   - rule 'variables: detect half reified value encoding' was applied 80 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x1011578e0168de09)
> #Variables: 2'956 (#bools: 74 in objective) (1'168 primary variables)
>   - 2'956 Booleans in [0,1]
> #kBoolAnd: 107 (#enforced: 107 #multi: 100) (#literals: 517)
> #kExactlyOne: 2'488 (#literals: 11'126)
> [Symmetry] Graph for symmetry has 6'288 nodes and 12'390 arcs.
> [Symmetry] Symmetry computation done. time: 0.00104685 dtime: 0.00219773
> 
> Preloading model.
> #Bound   0.24s best:inf   next:[0,40]     initial_domain
> #1       0.24s best:40    next:[0,39]     complete_hint
> #Model   0.24s var:2956/2956 constraints:2595/2595
> 
> Starting search at 0.24s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2       0.24s best:39    next:[0,38]     rnd_cst_lns (d=5.00e-01 s=9 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3       0.27s best:38    next:[0,37]     ls_restart_decay(batch:1 lin{mvs:49 evals:147} #w_updates:22 #perturb:0)
> #4       0.27s best:37    next:[0,36]     ls_lin_restart_perturb(batch:1 lin{mvs:129 evals:262} #w_updates:93 #perturb:0) [combined with: ls_restart_decay(bat...]
> #5       0.28s best:36    next:[0,35]     graph_arc_lns (d=7.07e-01 s=20 t=0.10 p=1.00 stall=1 h=base) [hint]
> #6       0.29s best:35    next:[0,34]     rnd_cst_lns (d=8.14e-01 s=28 t=0.10 p=1.00 stall=1 h=base) [hint]
> #7       0.30s best:34    next:[0,33]     graph_var_lns (d=8.14e-01 s=29 t=0.10 p=1.00 stall=0 h=base)
> #8       0.30s best:33    next:[0,32]     graph_var_lns (d=8.14e-01 s=29 t=0.10 p=1.00 stall=0 h=base) [combined with: rnd_cst_lns (d=8.14e...]
> #9       0.31s best:31    next:[0,30]     graph_arc_lns (d=8.14e-01 s=30 t=0.10 p=1.00 stall=0 h=base)
> #10      0.33s best:27    next:[0,26]     rins_pump_lns (d=7.07e-01 s=34 t=0.10 p=1.00 stall=0 h=base)
> #11      0.34s best:26    next:[0,25]     ls_restart_compound_perturb(batch:1 lin{mvs:0 evals:68'429} gen{mvs:5'389 evals:0} comp{mvs:343 btracks:2'523} #w_updates:67 #perturb:0) [combined with: rins_pump_lns (d=7.0...]
> #12      0.43s best:25    next:[0,24]     graph_var_lns (d=8.21e-01 s=49 t=0.10 p=0.75 stall=0 h=base)
> #Bound   0.46s best:25    next:[1,24]     pseudo_costs
> #Bound   0.46s best:25    next:[2,24]     pseudo_costs
> #Bound   0.51s best:25    next:[4,24]     pseudo_costs
> #Bound   0.52s best:25    next:[5,24]     pseudo_costs
> #Bound   0.52s best:25    next:[6,24]     bool_core (num_cores=6 [size:4 mw:1 d:2] a=60 d=2 fixed=0/2976 clauses=2'243)
> #Bound   0.53s best:25    next:[7,24]     bool_core (num_cores=7 [size:4 mw:1 d:2] a=57 d=2 fixed=0/2981 clauses=2'251)
> #Bound   0.53s best:25    next:[8,24]     bool_core (num_cores=8 [size:4 mw:1 d:2] a=54 d=2 fixed=0/2986 clauses=2'257)
> #Bound   0.53s best:25    next:[9,24]     bool_core (num_cores=9 [size:9 mw:1 amo:1 lit:6 d:3] a=46 d=3 fixed=0/2992 clauses=2'269)
> #Bound   0.54s best:25    next:[10,24]    bool_core (num_cores=10 [size:7 mw:1 amo:2 lit:5 d:3] a=40 d=3 fixed=0/2999 clauses=2'284)
> #Bound   0.54s best:25    next:[11,24]    bool_core (num_cores=11 [size:2 mw:1 d:3] a=39 d=3 fixed=0/3002 clauses=2'298)
> #Bound   0.54s best:25    next:[12,24]    bool_core (num_cores=12 [size:3 mw:1 d:4] a=37 d=4 fixed=0/3006 clauses=2'312)
> #Bound   0.55s best:25    next:[13,24]    bool_core (num_cores=13 [size:10 mw:1 amo:4 lit:9 d:4] a=28 d=4 fixed=0/3016 clauses=2'360)
> #Bound   0.56s best:25    next:[14,24]    bool_core (num_cores=14 [size:3 mw:1 d:5] a=26 d=5 fixed=0/3022 clauses=2'448)
> #Bound   0.56s best:25    next:[15,24]    bool_core (num_cores=15 [size:3 mw:1 d:4] a=24 d=5 fixed=0/3029 clauses=2'497)
> #Bound   0.57s best:25    next:[16,24]    bool_core (num_cores=16 [size:2 mw:1 d:6] a=23 d=6 fixed=0/3034 clauses=2'527)
> #Bound   0.59s best:25    next:[17,24]    bool_core (num_cores=17 [size:3 mw:1 d:7] a=21 d=7 fixed=0/3042 clauses=2'738)
> #13      0.60s best:24    next:[17,23]    graph_arc_lns (d=9.16e-01 s=67 t=0.10 p=0.83 stall=2 h=base)
> #Bound   0.60s best:24    next:[18,23]    bool_core (num_cores=18 [size:3 mw:1 amo:1 lit:2 d:5] a=19 d=7 fixed=0/3051 clauses=2'836)
> #Bound   0.63s best:24    next:[22,23]    max_lp
> #Model   0.84s var:2949/2956 constraints:2592/2595
> #Model   0.85s var:2948/2956 constraints:2592/2595
> #Bound   1.25s best:24    next:[23,23]    bool_core (num_cores=22 [size:2 mw:1 exo] a=0 d=9 fixed=10/3101 clauses=9'691)
> #Model   1.28s var:2860/2956 constraints:2553/2595
> #Done    1.42s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [   1.94s,    1.94s]    1.94s   0.00ns    1.94s
>            'default_lp':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [   1.43s,    1.43s]    1.43s   0.00ns    1.43s
>      'feasibility_pump':        12 [ 38.25us,  17.45ms]   1.50ms   4.81ms  17.98ms        11 [648.00ns, 648.00ns] 648.00ns   0.00ns   7.13us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        12 [  8.35ms,  98.32ms]  45.17ms  31.70ms 542.05ms        12 [ 10.00ns, 100.06ms]  37.18ms  39.85ms 446.11ms
>         'graph_cst_lns':        12 [  5.39ms,  60.96ms]  22.87ms  16.31ms 274.39ms        12 [ 10.00ns,  49.10ms]   8.60ms  14.82ms 103.15ms
>         'graph_dec_lns':        12 [  7.03ms, 143.29ms]  26.27ms  35.93ms 315.29ms        12 [ 10.00ns,  11.98ms]   1.67ms   3.66ms  20.06ms
>         'graph_var_lns':        12 [  8.46ms,  96.54ms]  46.86ms  28.76ms 562.35ms        12 [ 10.00ns, 100.04ms]  42.64ms  37.91ms 511.64ms
>                    'ls':        12 [  1.74ms, 125.82ms]  87.71ms  42.41ms    1.05s        12 [102.71us, 100.01ms]  79.24ms  36.48ms 950.90ms
>                'ls_lin':        11 [  1.90ms, 125.67ms] 103.25ms  34.23ms    1.14s        11 [257.44us, 100.01ms]  88.48ms  28.81ms 973.31ms
>                'max_lp':         1 [   1.19s,    1.19s]    1.19s   0.00ns    1.19s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [   1.72s,    1.72s]    1.72s   0.00ns    1.72s
>          'pseudo_costs':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [583.35ms, 583.35ms] 583.35ms   0.00ns 583.35ms
>         'quick_restart':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [   1.47s,    1.47s]    1.47s   0.00ns    1.47s
>   'quick_restart_no_lp':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [   1.76s,    1.76s]    1.76s   0.00ns    1.76s
>         'reduced_costs':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [558.77ms, 558.77ms] 558.77ms   0.00ns 558.77ms
>             'rins/rens':        13 [  4.59ms,  66.91ms]  28.54ms  17.15ms 371.07ms        11 [217.62us,  68.04ms]  13.86ms  23.02ms 152.43ms
>           'rnd_cst_lns':        12 [  5.93ms,  71.34ms]  18.43ms  17.60ms 221.13ms        12 [ 10.00ns,  75.19ms]   6.59ms  20.70ms  79.11ms
>           'rnd_var_lns':        12 [  5.95ms,  55.07ms]  16.74ms  13.60ms 200.90ms        12 [ 10.00ns,  46.35ms]   5.22ms  12.76ms  62.61ms
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  3'101      8'786    44'256    12'466  13'206'405        131'844
>            'default_lp':  2'956      8'616    38'259    12'226   8'368'774        309'525
>             'fs_random':      0          0         0         0           0              0
>       'fs_random_no_lp':      0          0         0         0           0              0
>                'max_lp':  2'956          0     5'912     5'912   1'441'734      1'447'648
>                 'no_lp':  2'956     11'429    41'772    12'215   9'382'561        313'624
>          'pseudo_costs':  2'956        131    27'772    12'060   4'161'720      4'166'403
>         'quick_restart':  2'956      6'020    45'326    12'585   8'257'645        262'899
>   'quick_restart_no_lp':  2'956      7'377    49'703    12'733   9'122'285        247'463
>         'reduced_costs':  2'956         96    27'468    12'061   4'131'610      4'148'222
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         7'204     101'860     174'086             0        33     5'116      15'750         0        524        2'986    1'105
>            'default_lp':         7'359     114'207     324'489             0         5     5'208      17'076         0        553        3'653    1'084
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':         9'597     173'197     438'347             0        14     5'208      17'188         0        550        3'700    1'108
>          'pseudo_costs':           119       2'258       4'929             0         0     5'112      15'935         0        542        3'226    1'093
>         'quick_restart':         4'759      70'834     242'717             0         3     5'095      15'581         0        545        3'121    1'139
>   'quick_restart_no_lp':         5'892      77'415     292'499             0        12     5'118      15'652         0        530        3'022    1'140
>         'reduced_costs':            85       2'230       4'284             0         0     5'098      15'642         0        552        3'188    1'075
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         12           0          0   18'868        0        0
>          'max_lp':          1       3'166        489        5        1        0
>    'pseudo_costs':          1       5'401      1'095       31      248        0
>   'quick_restart':         12           0          0   11'562        0        0
>   'reduced_costs':          1       4'969        683       32      237        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':            0 rows, 2 columns, 0 entries
>          'max_lp':  2715 rows, 2956 columns, 17533 entries
>    'pseudo_costs':   1425 rows, 2956 columns, 7071 entries
>   'quick_restart':            0 rows, 2 columns, 0 entries
>   'reduced_costs':   1475 rows, 2956 columns, 7239 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>          'max_lp':          0            0       6         0  58'633           0
>    'pseudo_costs':          0            0     153         0  18'105           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0     137         0  21'671           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':           16        0       20       0         15      0             0          0/0
>          'max_lp':        3'087      191       39       0         45      2             7      489/830
>    'pseudo_costs':        3'693        0        0       0          3      0             0  1'095/2'206
>   'quick_restart':           16        0       50       0         20      0             0          0/0
>   'reduced_costs':        3'281        3        0       0          0      0             0    683/1'243
> 
> Lp Cut           reduced_costs  pseudo_costs  max_lp
>          CG_FF:             72            84      15
>           CG_K:             10            26       -
>           CG_R:             28            45      23
>         Clique:             50            67      45
>       MIR_1_FF:              -             -       1
>      MIR_1_RLT:            249           201       1
>       MIR_4_FF:              -             -       1
>       MIR_6_FF:              -             1       -
>   ZERO_HALF_FF:            154           491     166
>    ZERO_HALF_R:            120           180     237
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          4/12     83%    9.72e-01       0.10
>   'graph_cst_lns':          1/12     92%    9.86e-01       0.10
>   'graph_dec_lns':          0/12    100%    9.91e-01       0.10
>   'graph_var_lns':          4/12     83%    9.70e-01       0.10
>       'rins/rens':          2/12    100%    9.91e-01       0.10
>     'rnd_cst_lns':          2/12    100%    9.91e-01       0.10
>     'rnd_var_lns':          0/12    100%    9.91e-01       0.10
> 
> LS stats                                Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                      'ls_lin_restart':        1                  1    77'650         0              0          0          6'729          2'956
>             'ls_lin_restart_compound':        3                  3         0   100'464         12'044     44'201            438      1'532'867
>     'ls_lin_restart_compound_perturb':        2                  2         0    57'839          5'629     26'101            339        895'771
>                'ls_lin_restart_decay':        1                  1    87'541         0              0          0            840          5'912
>       'ls_lin_restart_decay_compound':        1                  1         0    42'644          9'500     16'571             56        502'860
>        'ls_lin_restart_decay_perturb':        1                  1    86'781         0              0          0            862          5'800
>              'ls_lin_restart_perturb':        2                  2    77'474         0              0          0          5'824          3'211
>                          'ls_restart':        1                  1    76'497         0              0          0          7'197          2'956
>         'ls_restart_compound_perturb':        6                  6         0   157'386         15'800     70'779            965      2'307'661
>                    'ls_restart_decay':        1                  1        49         0              0          0             22            147
>           'ls_restart_decay_compound':        1                  1         0    40'064          9'662     15'196             46        495'836
>   'ls_restart_decay_compound_perturb':        1                  1         0    40'476          8'168     16'154             45        489'292
>                  'ls_restart_perturb':        2                  2   152'741         0              0          0         14'478          5'816
> 
> Solutions (13)                    Num     Rank
>                 'complete_hint':    1    [1,1]
>                 'graph_arc_lns':    3   [5,13]
>                 'graph_var_lns':    3   [7,12]
>        'ls_lin_restart_perturb':    1    [4,4]
>   'ls_restart_compound_perturb':    1  [11,11]
>              'ls_restart_decay':    1    [3,3]
>                 'rins_pump_lns':    1  [10,10]
>                   'rnd_cst_lns':    2    [2,6]
> 
> Objective bounds     Num
>        'bool_core':   14
>   'initial_domain':    1
>           'max_lp':    1
>     'pseudo_costs':    4
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     30      203       25
>    'fj solution hints':      0        0        0
>         'lp solutions':      2        2        2
>                 'pump':     11       11
> 
> Improving bounds shared      Num  Sym
>                   'core':  1'588    0
>          'quick_restart':    177    0
>    'quick_restart_no_lp':     75    0
> 
> Clauses shared              Num
>                  'core':  2'374
>            'default_lp':    228
>                 'no_lp':      7
>          'pseudo_costs':     20
>         'quick_restart':      7
>   'quick_restart_no_lp':     73
>         'reduced_costs':     47
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 24
> best_bound: 24
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 1.45896
> usertime: 1.45896
> deterministic_time: 13.3942
> gap_integral: 3.62245
> solution_fingerprint: 0xb960794dc6e595e4
> ```

In [ ]:
```python
instance07 = scsp.example.load("nucleotide_n050k050.txt")
```

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
> Initial optimization model '': (model_fingerprint: 0x8cd991355f0c11fb)
> #Variables: 505 (#bools: 250 in objective) (505 primary variables)
>   - 250 Booleans in [0,1]
>   - 250 in [0,5]
>   - 5 constants in {0,1,2,3,4} 
> #kAutomaton: 50
> #kLinear1: 250 (#enforced: 250)
> #kLinear2: 250 (#enforced: 250)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 250.
>   3.11e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.85e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.84e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   7.22e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   1.40e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=459'333 
> [Symmetry] Graph for symmetry has 1'819'534 nodes and 4'884'866 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 41594 / 503057
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1337881 literals:3417627 vars:502819 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.228009s] clauses:1337831 literals:3417477 vars:502819 one_side_vars:0 simple_definition:50 singleton_clauses:0
> [SAT presolve] [0.3067s] clauses:1323129 literals:3417477 vars:495468 one_side_vars:0 simple_definition:50 singleton_clauses:0
>   2.75e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.30e-01s  1.01e+00d *[Probe] #probed=1'484 #new_binary_clauses=63'775 
>   1.20e+00s  2.02e+00d *[MaxClique] Merged 1'003'093(2'006'186 literals) into 994'835(1'997'929 literals) at_most_ones. 
>   1.51e-01s  0.00e+00d  [DetectDominanceRelations] 
>   8.64e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.46e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   7.32e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   7.45e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.86e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.54e-02s  0.00e+00d  [DetectDifferentVariables] 
>   5.02e-01s  2.95e-02d  [ProcessSetPPC] #relevant_constraints=1'327'134 #num_inclusions=994'885 
>   1.78e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.08e-01s  2.19e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   3.94e-02s  1.93e-02d  [FindBigVerticalLinearOverlap] 
>   1.66e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   9.95e-02s  6.99e-03d  [MergeClauses] #num_collisions=22'410 #num_merges=22'410 #num_saved_literals=52'171 
>   1.59e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.34e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.56e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.31e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.39e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   3.89e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'803'809 nodes and 4'795'816 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 34243 / 495369
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1310463 literals:3383837 vars:495349 one_side_vars:0 simple_definition:6939 singleton_clauses:0
> [SAT presolve] [0.221859s] clauses:1310463 literals:3383837 vars:495349 one_side_vars:0 simple_definition:6939 singleton_clauses:0
> [SAT presolve] [0.276914s] clauses:1310463 literals:3383837 vars:495349 one_side_vars:0 simple_definition:6939 singleton_clauses:0
>   4.47e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.65e-01s  1.01e+00d *[Probe] #probed=1'322 #equiv=117 #new_binary_clauses=68'155 
>   1.20e+00s  1.99e+00d *[MaxClique] Merged 992'631(1'985'263 literals) into 984'434(1'976'871 literals) at_most_ones. 
>   1.72e-01s  0.00e+00d  [DetectDominanceRelations] 
>   6.10e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.69e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.08e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=506 
>   1.31e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.67e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.22e-02s  0.00e+00d  [DetectDifferentVariables] 
>   5.21e-01s  2.93e-02d  [ProcessSetPPC] #relevant_constraints=1'316'127 #num_inclusions=984'064 
>   2.41e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.30e-01s  2.19e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   4.73e-02s  1.92e-02d  [FindBigVerticalLinearOverlap] 
>   2.36e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.22e-01s  6.94e-03d  [MergeClauses] #num_collisions=22'182 #num_merges=22'182 #num_saved_literals=51'715 
>   1.71e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.67e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.70e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.65e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.91e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   5.25e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'803'047 nodes and 4'775'842 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 34176 / 495252
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1299725 literals:3354177 vars:495028 one_side_vars:73 simple_definition:12951 singleton_clauses:0
> [SAT presolve] [0.221926s] clauses:1299725 literals:3354177 vars:495028 one_side_vars:73 simple_definition:12951 singleton_clauses:0
> [SAT presolve] [0.276546s] clauses:1299725 literals:3354177 vars:495028 one_side_vars:73 simple_definition:12951 singleton_clauses:0
>   5.95e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.82e-01s  1.01e+00d *[Probe] #probed=1'322 #new_binary_clauses=67'921 
>   1.12e+00s  1.97e+00d *[MaxClique] Merged 983'143(1'966'339 literals) into 974'547(1'957'743 literals) at_most_ones. 
>   1.81e-01s  0.00e+00d  [DetectDominanceRelations] 
>   6.35e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.82e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.04e-01s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.37e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.46e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.87e-02s  0.00e+00d  [DetectDifferentVariables] 
>   5.25e-01s  2.91e-02d  [ProcessSetPPC] #relevant_constraints=1'306'512 #num_inclusions=974'449 
>   3.03e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.30e-01s  2.20e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   4.71e-02s  1.91e-02d  [FindBigVerticalLinearOverlap] 
>   3.06e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.20e-01s  6.89e-03d  [MergeClauses] #num_collisions=22'182 #num_merges=22'182 #num_saved_literals=51'715 
>   1.84e-01s  0.00e+00d  [DetectDominanceRelations] 
>   5.04e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.27e-01s  0.00e+00d  [ExpandObjective] #entries=21'299'906 #tight_variables=493'929 #tight_constraints=16'335 #expands=40 
> 
> Presolve summary:
>   - 654 affine relations were detected.
>   - rule 'TODO dual: only one unspecified blocking constraint?' was applied 7 times.
>   - rule 'affine: new relation' was applied 654 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 3 times.
>   - rule 'automaton: expanded' was applied 50 times.
>   - rule 'bool_and: x => x' was applied 50 times.
>   - rule 'deductions: 500 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 459'839 times.
>   - rule 'exactly_one: removed literals' was applied 50 times.
>   - rule 'exactly_one: singleton' was applied 50 times.
>   - rule 'linear: always true' was applied 450 times.
>   - rule 'linear: enforcement literal in expression' was applied 450 times.
>   - rule 'linear: fixed or dup variables' was applied 450 times.
>   - rule 'linear: remapped using affine relations' was applied 12'950 times.
>   - rule 'new_bool: automaton expansion' was applied 502'807 times.
>   - rule 'objective: expanded via tight equality' was applied 40 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 39 times.
>   - rule 'presolve: 5 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 4'122 times.
>   - rule 'setppc: removed dominated constraints' was applied 202 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 250 times.
>   - rule 'variables: detect half reified value encoding' was applied 500 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x3eba2390ad2d84e3)
> #Variables: 495'252 (#bools: 250 in objective) (480'952 primary variables)
>   - 495'252 Booleans in [0,1]
> #kAtMostOne: 48 (#literals: 144)
> #kBoolAnd: 86'250 (#enforced: 86'250 #multi: 14'864) (#literals: 1'119'009)
> #kBoolOr: 278'584 (#literals: 1'251'546)
> #kExactlyOne: 16'335 (#literals: 493'929)
> [Symmetry] Graph for symmetry has 1'794'229 nodes and 4'755'886 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> 
> Preloading model.
> #Bound  23.45s best:inf   next:[0,250]    initial_domain
> #1      23.49s best:250   next:[0,249]    complete_hint
> #Model  23.68s var:495252/495252 constraints:381217/381217
> 
> Starting search at 23.71s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2      25.03s best:249   next:[0,248]    rnd_var_lns (d=5.00e-01 s=8 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3      25.24s best:248   next:[0,247]    rnd_cst_lns (d=5.00e-01 s=9 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=5.00e...]
> #4      26.11s best:232   next:[0,231]    graph_var_lns (d=5.00e-01 s=10 t=0.10 p=0.00 stall=0 h=base) [hint]
> #5      26.15s best:230   next:[0,229]    graph_var_lns (d=5.00e-01 s=10 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: rnd_cst_lns (d=5.00e...]
> #6      26.27s best:227   next:[0,226]    graph_arc_lns (d=5.00e-01 s=11 t=0.10 p=0.00 stall=0 h=base) [hint]
> #7      26.31s best:223   next:[0,222]    graph_arc_lns (d=5.00e-01 s=11 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: graph_var_lns (d=5.0...]
> #8      28.31s best:222   next:[0,221]    no_lp [hint]
> #9      28.69s best:221   next:[0,220]    ls_lin_restart_perturb(batch:1 lin{mvs:465 evals:47'950} #w_updates:227 #perturb:0)
> #Model  29.10s var:495203/495252 constraints:381188/381217
> #10     29.85s best:220   next:[0,219]    default_lp [hint]
> #11     29.89s best:219   next:[0,218]    rnd_cst_lns (d=7.07e-01 s=18 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: default_lp [hint]...]
> #12     30.01s best:218   next:[0,217]    ls_lin_restart_perturb(batch:1 lin{mvs:2'687 evals:342'603} #w_updates:372 #perturb:0) [combined with: rnd_cst_lns (d=7.07e...]
> #13     30.33s best:142   next:[0,141]    quick_restart
> #Bound  31.96s best:142   next:[1,141]    bool_core (num_cores=1 [size:16 mw:1 d:4] a=235 d=4 fixed=49/495266 clauses=332'110)
> #14     37.68s best:141   next:[1,140]    no_lp
> #15     44.13s best:140   next:[1,139]    default_lp
> #16     44.46s best:139   next:[1,138]    default_lp
> #Bound  46.98s best:139   next:[2,138]    bool_core (num_cores=2 [size:14 mw:1 d:4] a=222 d=4 fixed=49/495293 clauses=331'971)
> #17     50.57s best:138   next:[2,137]    quick_restart
> #Bound  51.20s best:138   next:[3,137]    bool_core (num_cores=3 [size:14 mw:1 d:4] a=209 d=4 fixed=49/495318 clauses=332'053)
> #Bound  55.93s best:138   next:[4,137]    bool_core (num_cores=4 [size:15 mw:1 d:4] a=195 d=4 fixed=49/495344 clauses=332'104)
> #Bound  60.24s best:138   next:[5,137]    bool_core (num_cores=5 [size:15 mw:1 d:4] a=181 d=4 fixed=49/495371 clauses=332'146)
> #Bound  63.87s best:138   next:[6,137]    bool_core (num_cores=6 [size:14 mw:1 d:4] a=168 d=4 fixed=49/495397 clauses=332'174)
> #Bound  68.25s best:138   next:[7,137]    bool_core (num_cores=7 [size:15 mw:1 d:4] a=154 d=4 fixed=49/495423 clauses=332'294)
> #Bound  73.16s best:138   next:[8,137]    bool_core (num_cores=8 [size:21 mw:1 d:5] a=134 d=5 fixed=49/495456 clauses=332'394)
> #Bound  76.60s best:138   next:[9,137]    bool_core (num_cores=9 [size:14 mw:1 d:4] a=121 d=5 fixed=49/495488 clauses=332'447)
> #Bound  80.65s best:138   next:[10,137]   bool_core (num_cores=10 [size:14 mw:1 d:4] a=108 d=5 fixed=49/495513 clauses=332'519)
> #Bound  84.69s best:138   next:[11,137]   bool_core (num_cores=11 [size:14 mw:1 d:4] a=95 d=5 fixed=49/495538 clauses=332'569)
> #Bound  88.91s best:138   next:[12,137]   bool_core (num_cores=12 [size:15 mw:1 d:4] a=81 d=5 fixed=49/495564 clauses=332'595)
> #Bound  93.15s best:138   next:[13,137]   bool_core (num_cores=13 [size:14 mw:1 d:4] a=68 d=5 fixed=49/495590 clauses=332'625)
> #Model  94.03s var:495154/495252 constraints:381159/381217
> #Bound  97.90s best:138   next:[14,137]   bool_core (num_cores=14 [size:15 mw:1 d:4] a=54 d=5 fixed=49/495616 clauses=332'688)
> #Bound 112.67s best:138   next:[15,137]   bool_core (num_cores=15 [size:2 mw:1 d:5] a=53 d=5 fixed=98/495630 clauses=332'664)
> #Bound 114.20s best:138   next:[16,137]   bool_core (num_cores=15 [cover] a=53 d=5 fixed=98/495643 clauses=332'746)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  31.91s,   31.91s]   31.91s   0.00ns   31.91s
>            'default_lp':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  38.89s,   38.89s]   38.89s   0.00ns   38.89s
>      'feasibility_pump':       362 [ 19.57us,    1.64s]   5.22ms  86.20ms    1.89s       361 [ 18.00ns,  18.00ns]  18.00ns   0.00ns   6.50us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         3 [   2.60s,   18.25s]   12.11s    6.81s   36.32s         3 [ 10.00ns, 101.40ms]  67.16ms  47.49ms 201.49ms
>         'graph_cst_lns':         6 [   1.80s,    9.50s]    6.04s    3.02s   36.22s         6 [ 10.00ns, 101.55ms]  41.28ms  43.56ms 247.67ms
>         'graph_dec_lns':         9 [   2.13s,    5.54s]    4.40s 987.65ms   39.64s         8 [ 10.00ns,  10.00ns]  10.00ns   0.00ns  80.00ns
>         'graph_var_lns':         4 [   2.44s,   15.47s]   10.30s    5.39s   41.22s         3 [ 10.00ns, 114.69ms]  71.59ms  50.97ms 214.76ms
>                    'ls':       101 [180.55ms,    1.16s] 360.28ms 116.88ms   36.39s       101 [100.00ms, 102.28ms] 100.29ms 493.33us   10.13s
>                'ls_lin':       110 [187.10ms, 932.60ms] 332.60ms  95.29ms   36.59s       110 [ 11.59ms, 102.60ms]  99.21ms   8.66ms   10.91s
>                'max_lp':         1 [   1.60m,    1.60m]    1.60m   0.00ns    1.60m         1 [   6.00s,    6.00s]    6.00s   0.00ns    6.00s
>                 'no_lp':         1 [   1.62m,    1.62m]    1.62m   0.00ns    1.62m         1 [  39.59s,   39.59s]   39.59s   0.00ns   39.59s
>          'pseudo_costs':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [   5.86s,    5.86s]    5.86s   0.00ns    5.86s
>         'quick_restart':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  34.51s,   34.51s]   34.51s   0.00ns   34.51s
>   'quick_restart_no_lp':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  34.29s,   34.29s]   34.29s   0.00ns   34.29s
>         'reduced_costs':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [   4.97s,    4.97s]    4.97s   0.00ns    4.97s
>             'rins/rens':         3 [  26.06s,   27.04s]   26.47s 414.18ms    1.32m         3 [100.13ms, 100.47ms] 100.35ms 161.40us 301.06ms
>           'rnd_cst_lns':        11 [   1.53s,    4.85s]    3.48s    1.02s   38.24s        11 [ 10.00ns,  10.00ns]  10.00ns   0.00ns 110.00ns
>           'rnd_var_lns':        13 [   1.33s,    4.41s]    3.02s    1.08s   39.21s        11 [ 10.00ns,  10.00ns]  10.00ns   0.00ns 110.00ns
> 
> Search stats                Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  495'656      1'003    83'489     2'476  226'296'889         78'479
>            'default_lp':  495'252      9'997    53'762     2'125  160'048'312        508'187
>             'fs_random':        0          0         0         0            0              0
>       'fs_random_no_lp':        0          0         0         0            0              0
>                'max_lp':  495'252        492    22'349     1'677   35'084'949     34'607'707
>                 'no_lp':  495'252      9'752    49'900     2'056  157'719'734        485'080
>          'pseudo_costs':  495'252        453    22'302     1'677   34'128'622     33'794'419
>         'quick_restart':  495'252      2'659   130'521     2'370  225'410'153        204'304
>   'quick_restart_no_lp':  495'252      2'599   162'396     2'439  224'539'447        200'678
>         'reduced_costs':  495'252        115    22'564     1'701   29'886'986     29'807'878
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':           628      17'081     134'719             0         0       795      28'478         0        201        7'417        0
>            'default_lp':         7'628     273'356   2'658'145             0         5       920      35'217         0        251       10'140        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':           425      21'810     156'757             0         0       483      17'879         0        132        5'008        0
>                 'no_lp':         8'143     417'112   3'608'620             0         2       854      31'803         0        235        9'202        0
>          'pseudo_costs':           376      16'631     148'579             0         2       483      17'879         0        132        5'008        0
>         'quick_restart':         1'834      66'061     581'960             0         5       930      35'605         0        246        9'931        0
>   'quick_restart_no_lp':         1'778      70'140     602'467             0         5     1'005      36'647         0        273       10'197        0
>         'reduced_costs':            95       3'970      26'627             0         0       508      18'130         0        141        5'191        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          1           0          0    2'589        0        0
>          'max_lp':          1      11'177        549      136      827        0
>    'pseudo_costs':          1      10'670        537      131      782        0
>   'quick_restart':          1           0          0      333        0        0
>   'reduced_costs':          1      11'845        474      152      908        0
> 
> Lp dimension              Final dimension of first component
>      'default_lp':              0 rows, 2 columns, 0 entries
>          'max_lp':  6295 rows, 495252 columns, 18700 entries
>    'pseudo_costs':  6389 rows, 495252 columns, 19038 entries
>   'quick_restart':              0 rows, 2 columns, 0 entries
>   'reduced_costs':  7656 rows, 495252 columns, 22204 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>          'max_lp':          0            0      18         0  6'466           0
>    'pseudo_costs':          0            0       7         0  6'607           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0     128         0  4'855           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':            1        0        0       0          0      0             0        0/0
>          'max_lp':    1'283'768        9      939     109        427      0             5  549/5'345
>    'pseudo_costs':    1'283'769       26      811      96        427      0             0  537/5'933
>   'quick_restart':            1        0        0       0          0      0             0        0/0
>   'reduced_costs':    1'283'702       13      597     100        213      0             2  474/4'226
> 
> Lp Cut           max_lp  reduced_costs  pseudo_costs
>          CG_FF:      79             57            77
>           CG_R:       4              -             4
>         Clique:     119             92           109
>      MIR_1_RLT:      58             43            58
>       MIR_3_FF:      76             66            90
>       MIR_4_FF:      23             18            22
>       MIR_5_FF:       2              1             4
>       MIR_6_FF:       3              -             5
>   ZERO_HALF_FF:     140            154           148
>    ZERO_HALF_R:      45             43            20
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           1/3     33%    3.59e-01       0.10
>   'graph_cst_lns':           2/6     67%    8.03e-01       0.10
>   'graph_dec_lns':           0/8    100%    9.76e-01       0.10
>   'graph_var_lns':           1/3     33%    3.59e-01       0.10
>       'rins/rens':           3/3      0%    1.24e-01       0.10
>     'rnd_cst_lns':          2/11    100%    9.89e-01       0.10
>     'rnd_var_lns':          1/11    100%    9.89e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                          'ls_lin_restart':       10                  6   184'495         0              0          0          4'563      1'779'399
>                 'ls_lin_restart_compound':        9                  6         0     7'427            277      3'574             51      6'216'224
>         'ls_lin_restart_compound_perturb':       29                 10         0    15'808             21      7'892              8     20'117'982
>                    'ls_lin_restart_decay':       12                  9   399'034         0              0          0            877      1'886'805
>           'ls_lin_restart_decay_compound':       10                  8         0     7'061            144      3'458             19      6'958'380
>   'ls_lin_restart_decay_compound_perturb':       10                  6         0     5'194              5      2'593              0      6'991'427
>            'ls_lin_restart_decay_perturb':       10                  7   396'925         0              0          0            735      1'212'286
>                  'ls_lin_restart_perturb':       20                 11   420'451         0              0          0          7'305      3'105'946
>                              'ls_restart':        7                  6   140'329         0              0          0          3'360      1'161'133
>                     'ls_restart_compound':       15                  8         0     8'807             14      4'396             11     10'333'364
>             'ls_restart_compound_perturb':        6                  5         0     4'000            132      1'934             29      4'169'029
>                        'ls_restart_decay':       19                 13   663'156         0              0          0          1'283      2'918'838
>               'ls_restart_decay_compound':        5                  4         0     5'224            145      2'539             18      3'433'914
>       'ls_restart_decay_compound_perturb':       21                  9         0    10'995             12      5'490              2     14'692'106
>                'ls_restart_decay_perturb':       11                  9   377'639         0              0          0            874      1'672'905
>                      'ls_restart_perturb':       17                  6   383'003         0              0          0          4'841      2'904'884
> 
> Solutions (17)               Num     Rank
>            'complete_hint':    1    [1,1]
>               'default_lp':    3  [10,16]
>            'graph_arc_lns':    2    [6,7]
>            'graph_var_lns':    2    [4,5]
>   'ls_lin_restart_perturb':    2   [9,12]
>                    'no_lp':    2   [8,14]
>            'quick_restart':    2  [13,17]
>              'rnd_cst_lns':    2   [3,11]
>              'rnd_var_lns':    1    [2,2]
> 
> Objective bounds     Num
>        'bool_core':   16
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     32      222       27
>    'fj solution hints':      0        0        0
>         'lp solutions':     24        0       24
>                 'pump':    361        3
> 
> Improving bounds shared    Num  Sym
>                   'core':   49    0
>          'quick_restart':   49    0
> 
> Clauses shared                Num
>                  'core':    6'268
>            'default_lp':  121'936
>                 'no_lp':  137'424
>         'quick_restart':      199
>   'quick_restart_no_lp':       23
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 138
> best_bound: 16
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 121.256
> usertime: 121.256
> deterministic_time: 227.864
> gap_integral: 1048.77
> solution_fingerprint: 0x1809135ea2ad211f
> ```

In [ ]:
```python
instance08 = scsp.example.load("protein_n010k010.txt")
```

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
> Initial optimization model '': (model_fingerprint: 0xe864effb1f6f5f8)
> #Variables: 399 (#bools: 190 in objective) (399 primary variables)
>   - 190 Booleans in [0,1]
>   - 190 in [0,19]
>   - 19 constants in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18} 
> #kAutomaton: 10
> #kLinear1: 190 (#enforced: 190)
> #kLinear2: 190 (#enforced: 190)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 190.
>   8.22e-05s  0.00e+00d  [DetectDominanceRelations] 
>   1.92e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.47e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.24e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   5.45e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=24'747 
> [Symmetry] Graph for symmetry has 74'600 nodes and 190'840 arcs.
> [Symmetry] Symmetry computation done. time: 0.0151266 dtime: 0.0304396
> [Symmetry] #generators: 170, average support size: 4.56471
> [Symmetry] The model contains 10 duplicate constraints !
> [Symmetry] 83 orbits on 390 variables with sizes: 100,10,10,9,8,7,7,7,5,5,...
> [Symmetry] Found orbitope of size 11 x 2
> [SAT presolve] num removable Booleans: 486 / 19760
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:53187 literals:132403 vars:19563 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00282739s] clauses:53177 literals:132373 vars:19563 one_side_vars:0 simple_definition:11 singleton_clauses:0
> [SAT presolve] [0.00362404s] clauses:53161 literals:132373 vars:19555 one_side_vars:0 simple_definition:11 singleton_clauses:0
>   1.12e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.35e-01s  1.00e+00d *[Probe] #probed=11'800 #equiv=27 #new_binary_clauses=4'588 
>   1.28e-01s  5.08e-01d  [MaxClique] Merged 39'563(79'126 literals) into 13'506(52'955 literals) at_most_ones. 
>   1.02e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.69e-03s  0.00e+00d  [DetectDominanceRelations] 
>   3.69e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=4 #num_dual_strengthening=2 
>   3.95e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.30e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=52 
>   1.06e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.20e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.95e-04s  0.00e+00d  [DetectDifferentVariables] 
>   1.39e-02s  5.42e-04d  [ProcessSetPPC] #relevant_constraints=28'763 #num_inclusions=13'514 
>   9.75e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.47e-03s  4.48e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   5.88e-04s  3.61e-04d  [FindBigVerticalLinearOverlap] 
>   7.61e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.23e-03s  6.80e-07d  [MergeClauses] #num_collisions=8 #num_merges=8 #num_saved_literals=24 
>   3.75e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.26e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.75e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.17e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.55e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   9.61e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=1 
> [Symmetry] Graph for symmetry has 36'440 nodes and 73'168 arcs.
> [Symmetry] Symmetry computation done. time: 0.00706719 dtime: 0.0156978
> [Symmetry] #generators: 5, average support size: 56.8
> [Symmetry] 73 orbits on 215 variables with sizes: 3,3,3,3,3,3,3,3,3,3,...
> [Symmetry] Found orbitope of size 4 x 3
> [SAT presolve] num removable Booleans: 0 / 19507
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:40 literals:136 vars:40 one_side_vars:0 simple_definition:40 singleton_clauses:0
> [SAT presolve] [3.6409e-05s] clauses:40 literals:136 vars:40 one_side_vars:0 simple_definition:40 singleton_clauses:0
> [SAT presolve] [0.000224737s] clauses:40 literals:136 vars:40 one_side_vars:0 simple_definition:40 singleton_clauses:0
>   1.29e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.67e-01s  1.00e+00d *[Probe] #probed=7'817 #fixed_bools=226 #equiv=184 #new_binary_clauses=5'980 
>   9.30e-04s  1.23e-04d  [MaxClique] 
>   3.69e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.21e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.59e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   9.78e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=189 
>   8.00e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.79e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.60e-04s  0.00e+00d  [DetectDifferentVariables] 
>   5.54e-03s  2.18e-04d  [ProcessSetPPC] #relevant_constraints=14'943 
>   7.63e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.42e-03s  4.33e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   5.65e-04s  3.54e-04d  [FindBigVerticalLinearOverlap] 
>   7.01e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.06e-03s  6.80e-07d  [MergeClauses] #num_collisions=8 #num_merges=8 #num_saved_literals=24 
>   3.60e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.17e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.64e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.17e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.52e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   9.36e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 36'064 nodes and 71'719 arcs.
> [Symmetry] Symmetry computation done. time: 0.00723395 dtime: 0.0157078
> [Symmetry] #generators: 54, average support size: 17.6667
> [Symmetry] 171 orbits on 612 variables with sizes: 12,12,12,12,9,9,9,9,8,8,...
> [Symmetry] Found orbitope of size 4 x 7
> [SAT presolve] num removable Booleans: 0 / 19097
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:49 literals:154 vars:57 one_side_vars:17 simple_definition:40 singleton_clauses:0
> [SAT presolve] [3.4255e-05s] clauses:49 literals:154 vars:57 one_side_vars:17 simple_definition:40 singleton_clauses:0
> [SAT presolve] [0.00020582s] clauses:49 literals:154 vars:57 one_side_vars:17 simple_definition:40 singleton_clauses:0
>   1.31e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.63e-01s  1.00e+00d *[Probe] #probed=10'040 #equiv=18 #new_binary_clauses=6'190 
>   9.53e-04s  1.24e-04d  [MaxClique] 
>   3.68e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.20e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.60e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   9.35e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=15 
>   7.89e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.75e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.58e-04s  0.00e+00d  [DetectDifferentVariables] 
>   5.58e-03s  2.18e-04d  [ProcessSetPPC] #relevant_constraints=14'928 
>   7.63e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.45e-03s  4.31e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   5.61e-04s  3.54e-04d  [FindBigVerticalLinearOverlap] 
>   7.03e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.06e-03s  6.80e-07d  [MergeClauses] #num_collisions=8 #num_merges=8 #num_saved_literals=24 
>   3.63e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.16e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   9.62e-03s  0.00e+00d  [ExpandObjective] #entries=425'190 #tight_variables=70'373 #tight_constraints=14'879 #expands=200 
> 
> Presolve summary:
>   - 616 affine relations were detected.
>   - rule 'affine: new relation' was applied 616 times.
>   - rule 'at_most_one: resolved two constraints with opposite literal' was applied 1 time.
>   - rule 'at_most_one: transformed into max clique.' was applied 1 time.
>   - rule 'at_most_one: x and not(x)' was applied 1 time.
>   - rule 'automaton: expanded' was applied 10 times.
>   - rule 'bool_and: x => x' was applied 10 times.
>   - rule 'bool_or: always true' was applied 1 time.
>   - rule 'deductions: 380 stored' was applied 1 time.
>   - rule 'domination: in exactly one' was applied 1 time.
>   - rule 'dual: fix variable' was applied 10 times.
>   - rule 'duplicate: removed constraint' was applied 25'004 times.
>   - rule 'exactly_one: removed literals' was applied 311 times.
>   - rule 'exactly_one: satisfied' was applied 112 times.
>   - rule 'exactly_one: singleton' was applied 9 times.
>   - rule 'exactly_one: size two' was applied 1 time.
>   - rule 'exactly_one: x and not(x)' was applied 3 times.
>   - rule 'linear: always true' was applied 370 times.
>   - rule 'linear: enforcement literal in expression' was applied 370 times.
>   - rule 'linear: fixed or dup variables' was applied 370 times.
>   - rule 'linear: remapped using affine relations' was applied 2'270 times.
>   - rule 'new_bool: automaton expansion' was applied 19'570 times.
>   - rule 'objective: expanded via tight equality' was applied 200 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 190 times.
>   - rule 'objective: variable not used elsewhere' was applied 10 times.
>   - rule 'presolve: 256 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 13'505 times.
>   - rule 'setppc: removed dominated constraints' was applied 9 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 190 times.
>   - rule 'variables: detect half reified value encoding' was applied 380 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x9d4c9b671641fc0d)
> #Variables: 19'079 (#bools: 236 in objective) (7'935 primary variables)
>   - 19'079 Booleans in [0,1]
> #kBoolAnd: 16 (#enforced: 16 #multi: 8) (#literals: 57)
> #kBoolOr: 24 (#literals: 72)
> #kExactlyOne: 14'879 (#literals: 70'373)
> [Symmetry] Graph for symmetry has 35'159 nodes and 71'672 arcs.
> [Symmetry] Symmetry computation done. time: 0.00702009 dtime: 0.0153355
> [Symmetry] #generators: 50, average support size: 16.48
> [Symmetry] 173 orbits on 561 variables with sizes: 8,8,8,8,8,8,8,8,7,7,...
> [Symmetry] Found orbitope of size 4 x 7
> 
> Preloading model.
> #Bound   1.36s best:inf   next:[0,180]    initial_domain
> #1       1.36s best:179   next:[0,178]    complete_hint
> #Model   1.36s var:19079/19079 constraints:14919/14919
> 
> Starting search at 1.37s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2       1.42s best:154   next:[0,153]    graph_var_lns (d=5.00e-01 s=10 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3       1.45s best:153   next:[0,152]    graph_arc_lns (d=5.00e-01 s=11 t=0.10 p=0.00 stall=0 h=base) [hint]
> #4       1.47s best:147   next:[0,146]    graph_cst_lns (d=5.00e-01 s=12 t=0.10 p=0.00 stall=0 h=base) [hint] [combined with: graph_arc_lns (d=5.0...]
> #5       1.65s best:146   next:[0,145]    ls_restart_decay(batch:1 lin{mvs:27 evals:219} #w_updates:9 #perturb:0)
> #6       1.66s best:145   next:[0,144]    ls_lin_restart_perturb(batch:1 lin{mvs:165 evals:406} #w_updates:109 #perturb:0)
> #7       1.71s best:144   next:[0,143]    rnd_cst_lns (d=7.07e-01 s=18 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: ls_lin_restart_pertu...]
> #8       1.77s best:116   next:[0,115]    graph_var_lns (d=7.07e-01 s=19 t=0.10 p=1.00 stall=0 h=base)
> #9       1.77s best:114   next:[0,113]    graph_var_lns (d=7.07e-01 s=19 t=0.10 p=1.00 stall=0 h=base) [combined with: rnd_cst_lns (d=7.07e...]
> #10      1.80s best:113   next:[0,112]    graph_dec_lns (d=7.07e-01 s=22 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: graph_var_lns (d=7.0...]
> #11      1.82s best:100   next:[0,99]     graph_arc_lns (d=7.07e-01 s=20 t=0.10 p=1.00 stall=0 h=base)
> #12      1.88s best:99    next:[0,98]     ls_restart_decay_compound(batch:1 lin{mvs:0 evals:175'995} gen{mvs:4'159 evals:0} comp{mvs:71 btracks:2'044} #w_updates:15 #perturb:0) [combined with: graph_arc_lns (d=7.0...]
> #13      1.89s best:96    next:[0,95]     rnd_var_lns (d=8.14e-01 s=27 t=0.10 p=1.00 stall=2 h=base) [hint]
> #14      1.89s best:95    next:[0,94]     rnd_var_lns (d=8.14e-01 s=27 t=0.10 p=1.00 stall=2 h=base) [hint] [combined with: ls_restart_decay_com...]
> #15      1.94s best:93    next:[0,92]     rnd_cst_lns (d=8.14e-01 s=28 t=0.10 p=1.00 stall=0 h=base) [hint]
> #16      1.94s best:91    next:[0,90]     rnd_cst_lns (d=8.14e-01 s=28 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=8.14e...]
> #17      2.02s best:75    next:[0,74]     graph_cst_lns (d=8.14e-01 s=30 t=0.10 p=1.00 stall=0 h=base)
> #18      2.03s best:74    next:[0,73]     ls_restart_decay_perturb(batch:1 lin{mvs:149 evals:296} #w_updates:44 #perturb:0)
> #19      2.15s best:73    next:[0,72]     no_lp
> #20      2.16s best:70    next:[0,69]     rins_pump_lns (d=5.00e-01 s=26 t=0.10 p=0.00 stall=0 h=base)
> #21      2.17s best:69    next:[0,68]     rnd_cst_lns (d=8.76e-01 s=38 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=8.76e...]
> #22      2.21s best:68    next:[0,67]     ls_restart_perturb(batch:1 lin{mvs:77 evals:245} #w_updates:68 #perturb:0)
> #23      2.25s best:67    next:[0,66]     graph_dec_lns (d=8.76e-01 s=41 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: ls_restart_perturb(b...]
> #24      2.28s best:65    next:[0,64]     graph_cst_lns (d=8.76e-01 s=40 t=0.10 p=1.00 stall=0 h=base)
> #25      2.36s best:63    next:[0,62]     rnd_var_lns (d=9.14e-01 s=47 t=0.10 p=1.00 stall=0 h=base) [hint]
> #26      2.36s best:62    next:[0,61]     rnd_cst_lns (d=9.14e-01 s=48 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=9.14e...]
> #Model   2.37s var:18778/19079 constraints:14770/14919
> #Model   2.38s var:18740/19079 constraints:14751/14919
> #Model   2.47s var:18625/19079 constraints:14693/14919
> #27      2.52s best:58    next:[0,57]     graph_cst_lns (d=9.14e-01 s=49 t=0.10 p=1.00 stall=0 h=base)
> #28      2.54s best:55    next:[0,54]     rins_pump_lns (d=5.38e-01 s=45 t=0.10 p=0.50 stall=0 h=base)
> #29      2.61s best:50    next:[0,49]     rnd_var_lns (d=9.39e-01 s=55 t=0.10 p=1.00 stall=0 h=base) [hint]
> #Bound   3.52s best:50    next:[1,49]     bool_core (num_cores=1 [size:4 mw:1 d:2] a=231 d=2 fixed=454/19081 clauses=12'827)
> #Bound   3.56s best:50    next:[2,49]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=228 d=2 fixed=454/19086 clauses=12'833)
> #Bound   3.59s best:50    next:[3,49]     bool_core (num_cores=3 [size:4 mw:1 d:2] a=225 d=2 fixed=454/19091 clauses=12'839)
> #Bound   3.62s best:50    next:[4,49]     bool_core (num_cores=4 [size:4 mw:1 d:2] a=222 d=2 fixed=454/19096 clauses=12'844)
> #Bound   3.67s best:50    next:[5,49]     bool_core (num_cores=5 [size:4 mw:1 d:2] a=219 d=2 fixed=454/19101 clauses=12'849)
> #Bound   3.71s best:50    next:[6,49]     bool_core (num_cores=6 [size:4 mw:1 d:2] a=216 d=2 fixed=454/19106 clauses=12'855)
> #Bound   3.75s best:50    next:[7,49]     bool_core (num_cores=7 [size:5 mw:1 d:3] a=212 d=3 fixed=454/19112 clauses=12'861)
> #Bound   3.78s best:50    next:[8,49]     bool_core (num_cores=8 [size:4 mw:1 d:2] a=209 d=3 fixed=454/19118 clauses=12'867)
> #Bound   3.82s best:50    next:[9,49]     bool_core (num_cores=9 [size:5 mw:1 d:3] a=205 d=3 fixed=454/19124 clauses=12'873)
> #Bound   3.86s best:50    next:[10,49]    bool_core (num_cores=10 [size:4 mw:1 d:2] a=202 d=3 fixed=454/19130 clauses=12'881)
> #Bound   3.89s best:50    next:[11,49]    bool_core (num_cores=11 [size:4 mw:1 d:2] a=199 d=3 fixed=454/19135 clauses=12'886)
> #Bound   3.93s best:50    next:[12,49]    bool_core (num_cores=12 [size:4 mw:1 d:2] a=196 d=3 fixed=454/19140 clauses=12'891)
> #Bound   3.98s best:50    next:[13,49]    bool_core (num_cores=13 [size:5 mw:1 d:3] a=192 d=3 fixed=454/19146 clauses=12'897)
> #Bound   4.03s best:50    next:[14,49]    bool_core (num_cores=14 [size:6 mw:1 d:3] a=187 d=3 fixed=454/19154 clauses=12'905)
> #Bound   4.06s best:50    next:[15,49]    bool_core (num_cores=15 [size:4 mw:1 d:2] a=184 d=3 fixed=454/19161 clauses=12'913)
> #Bound   4.11s best:50    next:[16,49]    bool_core (num_cores=16 [size:6 mw:1 d:3] a=179 d=3 fixed=454/19168 clauses=12'920)
> #Bound   4.15s best:50    next:[17,49]    bool_core (num_cores=17 [size:4 mw:1 d:2] a=176 d=3 fixed=454/19175 clauses=12'928)
> #Bound   4.18s best:50    next:[18,49]    bool_core (num_cores=18 [size:4 mw:1 d:2] a=173 d=3 fixed=454/19180 clauses=12'933)
> #Bound   4.21s best:50    next:[19,49]    bool_core (num_cores=19 [size:4 mw:1 d:2] a=170 d=3 fixed=454/19185 clauses=12'939)
> #Bound   4.24s best:50    next:[20,49]    bool_core (num_cores=20 [size:4 mw:1 d:2] a=167 d=3 fixed=454/19190 clauses=12'944)
> #Bound   4.34s best:50    next:[21,49]    bool_core (num_cores=21 [size:12 mw:1 amo:1 lit:9 d:3] a=157 d=3 fixed=454/19196 clauses=12'950)
> #Bound   4.38s best:50    next:[22,49]    bool_core (num_cores=22 [size:5 mw:1 d:3] a=153 d=3 fixed=454/19202 clauses=12'957)
> #Bound   4.42s best:50    next:[23,49]    bool_core (num_cores=23 [size:5 mw:1 d:3] a=149 d=3 fixed=454/19209 clauses=12'964)
> #Bound   4.46s best:50    next:[24,49]    bool_core (num_cores=24 [size:6 mw:1 d:3] a=144 d=3 fixed=454/19217 clauses=12'972)
> #Bound   4.99s best:50    next:[33,49]    bool_core (num_cores=33 [size:3 mw:1 d:5] a=94 d=5 fixed=454/19289 clauses=13'128) [skipped_logs=8]
> #Bound   5.64s best:50    next:[38,49]    bool_core (num_cores=38 [size:4 mw:1 d:5] a=79 d=9 fixed=454/19366 clauses=13'901) [skipped_logs=4]
> #Bound   6.68s best:50    next:[40,49]    bool_core (num_cores=40 [size:2 mw:1 d:11] a=77 d=11 fixed=454/19392 clauses=15'323) [skipped_logs=1]
> #Bound   9.80s best:50    next:[41,49]    bool_core (num_cores=41 [size:6 mw:1 amo:1 lit:2 d:12] a=74 d=12 fixed=454/19412 clauses=19'465)
> #30     10.63s best:49    next:[41,48]    graph_arc_lns (d=7.58e-01 s=264 t=0.10 p=0.54 stall=19 h=base)
> #Bound  14.35s best:49    next:[42,48]    bool_core (num_cores=42 [size:4 mw:1 d:13] a=71 d=13 fixed=454/19430 clauses=24'564)
> #31     18.33s best:48    next:[42,47]    graph_arc_lns (d=6.50e-01 s=460 t=0.10 p=0.50 stall=18 h=base)
> #Bound  28.55s best:48    next:[43,47]    bool_core (num_cores=43 [size:7 mw:1 d:14] a=65 d=14 fixed=454/19458 clauses=34'752)
> #32     42.37s best:47    next:[43,46]    quick_restart
> #Bound  57.13s best:47    next:[44,46]    bool_core (num_cores=44 [size:13 mw:1 d:15] a=53 d=15 fixed=454/19498 clauses=44'258)
> #Model  83.65s var:18288/19079 constraints:14527/14919
> #Bound  98.50s best:47    next:[45,46]    bool_core (num_cores=45 [size:18 mw:1 amo:2 lit:6 d:16] a=37 d=16 fixed=454/19559 clauses=45'726)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.42m,    1.42m]    1.42m   0.00ns    1.42m
>            'default_lp':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.37m,    1.37m]    1.37m   0.00ns    1.37m
>      'feasibility_pump':       521 [ 23.08us, 182.29ms] 444.28us   7.97ms 231.47ms       519 [  1.19us,   1.19us]   1.19us   0.00ns 616.57us
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':       323 [ 45.00ms, 425.43ms] 163.18ms  53.46ms   52.71s       323 [ 10.00ns, 110.92ms]  60.72ms  46.43ms   19.61s
>         'graph_cst_lns':       239 [ 48.06ms, 560.69ms] 220.56ms  88.42ms   52.71s       239 [ 10.00ns, 108.59ms]  60.07ms  46.98ms   14.36s
>         'graph_dec_lns':       191 [ 65.70ms, 614.37ms] 278.93ms 106.68ms   53.28s       191 [ 10.00ns, 106.62ms]  62.46ms  42.99ms   11.93s
>         'graph_var_lns':       328 [ 28.75ms, 493.98ms] 159.59ms  54.50ms   52.35s       328 [ 10.00ns, 112.92ms]  64.08ms  45.38ms   21.02s
>                    'ls':       313 [  3.28ms, 270.17ms] 166.51ms  44.31ms   52.12s       313 [144.93us, 100.36ms]  98.97ms   9.94ms   30.98s
>                'ls_lin':       318 [ 29.51ms, 288.50ms] 164.17ms  37.99ms   52.21s       318 [611.07us, 100.42ms]  99.47ms   6.68ms   31.63s
>            'max_lp_sym':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  48.39s,   48.39s]   48.39s   0.00ns   48.39s
>                 'no_lp':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.26m,    1.26m]    1.26m   0.00ns    1.26m
>          'pseudo_costs':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  31.15s,   31.15s]   31.15s   0.00ns   31.15s
>         'quick_restart':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.13m,    1.13m]    1.13m   0.00ns    1.13m
>   'quick_restart_no_lp':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.06m,    1.06m]    1.06m   0.00ns    1.06m
>         'reduced_costs':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  35.85s,   35.85s]   35.85s   0.00ns   35.85s
>             'rins/rens':       284 [  6.71ms, 604.78ms] 187.07ms 151.68ms   53.13s       210 [ 10.00ns, 101.05ms]  55.65ms  49.21ms   11.69s
>           'rnd_cst_lns':       211 [ 59.82ms, 552.30ms] 247.56ms  87.17ms   52.23s       211 [ 10.00ns, 106.62ms]  60.72ms  44.86ms   12.81s
>           'rnd_var_lns':       199 [ 51.69ms, 575.19ms] 264.71ms 103.36ms   52.68s       199 [ 10.00ns, 106.65ms]  61.30ms  44.29ms   12.20s
> 
> Search stats               Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  19'612    107'923    432'630    87'956  533'948'517      1'552'053
>            'default_lp':  19'079    257'573    657'515   116'337  356'429'171     14'929'301
>             'fs_random':       0          0          0         0            0              0
>       'fs_random_no_lp':       0          0          0         0            0              0
>            'max_lp_sym':  19'079      1'280    253'719    94'355   60'719'172     58'684'913
>                 'no_lp':  19'079    214'746    563'495    95'189  335'566'344     12'340'873
>          'pseudo_costs':  19'079      7'505    204'657    73'878   58'336'415     52'071'998
>         'quick_restart':  19'079     87'233  1'099'651   118'630  318'013'780      7'626'238
>   'quick_restart_no_lp':  19'079     79'269  1'044'524   114'138  294'680'575      6'643'903
>         'reduced_costs':  19'079      4'632    211'339    74'484   53'498'829     50'064'126
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':       101'061   3'870'303   4'962'451     3'153'067       161    16'239      84'551         0      2'716       53'223    3'757
>            'default_lp':       206'526   3'342'241  27'282'697    24'869'993       497    35'895     122'515         0      2'733       21'048   10'011
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':         1'139      13'521      83'618             0         1    28'186     105'032         0      2'566       19'102    7'688
>                 'no_lp':       181'596   2'806'000  23'500'381    21'851'879       613    27'367     100'118         0      2'546       19'503    7'276
>          'pseudo_costs':         7'189     185'744   1'103'486             0         3    21'614      80'354         0      2'217       16'633    5'569
>         'quick_restart':        59'515     803'668   7'421'776     5'825'336       520    27'274     137'461         0      3'085       47'202    7'117
>   'quick_restart_no_lp':        54'455     703'732   6'724'662     5'022'089       433    20'392     152'006         0      3'410       66'522    4'456
>         'reduced_costs':         4'514     192'537     825'152             0         1    22'176      81'288         0      2'174       16'187    5'537
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         13           0          0  726'544        0        0
>      'max_lp_sym':          1      81'098        589        3    4'206        0
>    'pseudo_costs':          1     189'735      1'578      298   18'130        0
>   'quick_restart':         13           0          0  328'765        0        0
>   'reduced_costs':          1     159'292      2'291      197   14'418        0
> 
> Lp dimension              Final dimension of first component
>      'default_lp':              0 rows, 2 columns, 0 entries
>      'max_lp_sym':  14412 rows, 18691 columns, 92217 entries
>    'pseudo_costs':   7952 rows, 19079 columns, 32946 entries
>   'quick_restart':              0 rows, 2 columns, 0 entries
>   'reduced_costs':   8577 rows, 19079 columns, 35839 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow      Bad  BadScaling
>      'default_lp':          0            0       0         0        0           0
>      'max_lp_sym':          0            0   4'208         0  318'886           0
>    'pseudo_costs':          0            0  13'988         0   42'284           0
>   'quick_restart':          0            0       0         0        0           0
>   'reduced_costs':          0            0  12'880         0   70'234           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':           33        0       36       0          3      0             0          0/0
>      'max_lp_sym':       15'077      264      905       0        679      2             0    589/1'180
>    'pseudo_costs':       16'498        2    3'331       0      1'524      0             0  1'578/3'794
>   'quick_restart':           33        0       75       0          3      0             0          0/0
>   'reduced_costs':       17'211        0    3'557       0      1'535      0             0  2'291/5'858
> 
> Lp Cut           max_lp_sym  pseudo_costs  reduced_costs
>          CG_FF:          35           131            144
>           CG_K:           7             2              4
>           CG_R:          31             2              2
>          CG_RB:           1             -              -
>         Clique:          37           166            123
>      MIR_1_RLT:           -           297            323
>       MIR_3_FF:           -             3              5
>       MIR_4_FF:           1             1              5
>       MIR_5_FF:           2             1              5
>       MIR_6_FF:           3             -              3
>   ZERO_HALF_FF:         239           681          1'291
>    ZERO_HALF_R:         233           294            386
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':         6/323     50%    6.33e-01       0.11
>   'graph_cst_lns':         5/239     49%    9.04e-01       0.11
>   'graph_dec_lns':         2/191     52%    9.86e-01       0.11
>   'graph_var_lns':         4/328     50%    6.34e-01       0.11
>       'rins/rens':        46/251     54%    9.22e-01       0.10
>     'rnd_cst_lns':         4/211     52%    9.87e-01       0.11
>     'rnd_var_lns':         4/199     52%    9.88e-01       0.11
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves   GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                          'ls_lin_restart':       38                 28  2'850'357          0              0          0         41'633        625'197
>                 'ls_lin_restart_compound':       49                 21          0  1'624'783         68'913    777'883          8'739     22'326'497
>         'ls_lin_restart_compound_perturb':       56                 31          0  1'632'466         66'432    782'942          9'327     25'601'021
>                    'ls_lin_restart_decay':       26                 18  1'992'692          0              0          0          3'923        493'512
>           'ls_lin_restart_decay_compound':       34                 19          0  1'012'010        197'070    407'386          1'038     14'906'206
>   'ls_lin_restart_decay_compound_perturb':       44                 20          0  1'406'693        291'252    557'607          1'137     19'553'864
>            'ls_lin_restart_decay_perturb':       46                 19  3'531'515          0              0          0          6'000        938'184
>                  'ls_lin_restart_perturb':       25                 20  1'801'512          0              0          0         26'142        401'457
>                              'ls_restart':       50                 22  3'756'820          0              0          0         54'486        657'130
>                     'ls_restart_compound':       35                 24          0    993'435         40'300    476'476          6'472     16'249'366
>             'ls_restart_compound_perturb':       36                 27          0    974'193         39'946    467'075          6'423     16'640'356
>                        'ls_restart_decay':       18                 14  1'305'273          0              0          0          2'661        331'968
>               'ls_restart_decay_compound':       49                 26          0  1'453'040        309'811    571'492          1'444     21'724'623
>       'ls_restart_decay_compound_perturb':       34                 13          0  1'121'766        219'886    450'816            738     15'049'068
>                'ls_restart_decay_perturb':       56                 21  4'228'128          0              0          0          7'061      1'144'602
>                      'ls_restart_perturb':       35                 28  2'546'398          0              0          0         37'037        575'906
> 
> Solutions (32)                  Num     Rank
>               'complete_hint':    1    [1,1]
>               'graph_arc_lns':    4   [3,31]
>               'graph_cst_lns':    4   [4,27]
>               'graph_dec_lns':    2  [10,23]
>               'graph_var_lns':    3    [2,9]
>      'ls_lin_restart_perturb':    1    [6,6]
>            'ls_restart_decay':    1    [5,5]
>   'ls_restart_decay_compound':    1  [12,12]
>    'ls_restart_decay_perturb':    1  [18,18]
>          'ls_restart_perturb':    1  [22,22]
>                       'no_lp':    1  [19,19]
>               'quick_restart':    1  [32,32]
>               'rins_pump_lns':    2  [20,28]
>                 'rnd_cst_lns':    5   [7,26]
>                 'rnd_var_lns':    4  [13,29]
> 
> Objective bounds     Num
>        'bool_core':   45
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':  1'073    4'112      774
>    'fj solution hints':      0        0        0
>         'lp solutions':    347      134      329
>                 'pump':    520      150
> 
> Improving bounds shared    Num  Sym
>                   'core':  454    0
>          'quick_restart':  337    0
> 
> Clauses shared               Num
>                  'core':  71'422
>            'default_lp':   2'088
>            'max_lp_sym':       7
>                 'no_lp':     778
>          'pseudo_costs':      83
>         'quick_restart':     102
>   'quick_restart_no_lp':     125
>         'reduced_costs':       1
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 47
> best_bound: 45
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 120.233
> usertime: 120.233
> deterministic_time: 660.242
> gap_integral: 567.032
> solution_fingerprint: 0xe68b0068200e9447
> ```

In [ ]:
```python
instance09 = scsp.example.load("protein_n050k050.txt")
```

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
> Initial optimization model '': (model_fingerprint: 0x4bc14be872f6a772)
> #Variables: 2'020 (#bools: 1'000 in objective) (2'020 primary variables)
>   - 1'000 Booleans in [0,1]
>   - 1'000 in [0,20]
>   - 20 constants in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19} 
> #kAutomaton: 50
> #kLinear1: 1'000 (#enforced: 1'000)
> #kLinear2: 1'000 (#enforced: 1'000)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 1000.
>   1.16e-03s  0.00e+00d  [DetectDominanceRelations] 
>   2.23e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.98e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   5.14e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   1.11e+00s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=3'166'290 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 54446 / 2389968
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:6154334 literals:15819832 vars:2389035 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [1.13366s] clauses:6154284 literals:15819682 vars:2389035 one_side_vars:0 simple_definition:51 singleton_clauses:0
> [SAT presolve] [1.32162s] clauses:6149756 literals:15819682 vars:2386771 one_side_vars:0 simple_definition:51 singleton_clauses:0
>   2.39e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.88e+00s  1.03e+00d *[Probe] #probed=2'178 #equiv=3 #new_binary_clauses=57'383 
>   4.52e+00s  9.66e+00d *[MaxClique] Merged 4'821'404(9'642'808 literals) into 4'785'773(9'607'178 literals) at_most_ones. 
>   7.40e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.04e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   5.98e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   6.33e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=18 
>   6.21e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.43e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   7.32e-02s  0.00e+00d  [DetectDifferentVariables] 
>   2.21e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=6'163'179 #num_inclusions=3'728'080 
>   7.99e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   8.75e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   1.89e-01s  9.03e-02d  [FindBigVerticalLinearOverlap] 
>   7.66e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.86e-01s  3.06e-02d  [MergeClauses] #num_collisions=6'228 #num_merges=6'228 #num_saved_literals=14'720 
>   7.47e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.99e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.45e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.99e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.88e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   2.06e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=5 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 52179 / 2386663
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:6097673 literals:15679830 vars:2386582 one_side_vars:0 simple_definition:38197 singleton_clauses:0
> [SAT presolve] [1.07558s] clauses:6097673 literals:15679830 vars:2386582 one_side_vars:0 simple_definition:38197 singleton_clauses:0
> [SAT presolve] [1.24163s] clauses:6097673 literals:15679830 vars:2386582 one_side_vars:0 simple_definition:38197 singleton_clauses:0
>   3.45e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.39e+00s  1.03e+00d *[Probe] #probed=1'986 #equiv=508 #new_binary_clauses=58'121 
>   4.63e+00s  9.58e+00d *[MaxClique] Merged 4'777'543(9'555'088 literals) into 4'760'257(9'537'549 literals) at_most_ones. 
>   2.22e+00s  0.00e+00d  [DetectDominanceRelations] 
>   8.08e-01s  0.00e+00d  [DetectDominanceRelations] 
>   5.39e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   6.67e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   8.71e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2'794 
>   7.82e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.20e-01s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.02e-01s  0.00e+00d  [DetectDifferentVariables] 
>   2.30e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=6'134'768 #num_inclusions=3'715'341 
>   1.08e-01s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.16e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   2.06e-01s  9.01e-02d  [FindBigVerticalLinearOverlap] 
>   1.10e-01s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.93e-01s  3.05e-02d  [MergeClauses] #num_collisions=5'212 #num_merges=5'212 #num_saved_literals=12'688 
>   8.12e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.16e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.04e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.15e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.15e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   3.88e-01s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 51721 / 2386152
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:6073521 literals:15613597 vars:2385823 one_side_vars:216 simple_definition:56818 singleton_clauses:0
> [SAT presolve] [1.06012s] clauses:6073521 literals:15613597 vars:2385823 one_side_vars:216 simple_definition:56818 singleton_clauses:0
> [SAT presolve] [1.22979s] clauses:6073519 literals:15613593 vars:2385822 one_side_vars:216 simple_definition:56817 singleton_clauses:0
>   3.67e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.47e+00s  1.02e+00d *[Probe] #probed=1'986 #new_binary_clauses=57'105 
>   4.84e+00s  9.53e+00d *[MaxClique] Merged 4'756'474(9'513'070 literals) into 4'749'185(9'505'782 literals) at_most_ones. 
>   2.35e+00s  0.00e+00d  [DetectDominanceRelations] 
>   8.70e-01s  0.00e+00d  [DetectDominanceRelations] 
>   5.71e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   7.27e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   8.86e-01s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.23e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.50e-01s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.30e-01s  0.00e+00d  [DetectDifferentVariables] 
>   2.38e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=6'125'462 #num_inclusions=3'711'773 
>   1.38e-01s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.26e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   2.07e-01s  9.00e-02d  [FindBigVerticalLinearOverlap] 
>   1.40e-01s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   7.07e-01s  3.04e-02d  [MergeClauses] #num_collisions=5'212 #num_merges=5'212 #num_saved_literals=12'688 
>   8.73e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.34e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.27e-01s  0.00e+00d  [ExpandObjective] #entries=100'000'057 #tight_variables=1'660'889 #tight_constraints=34'910 
> 
> Presolve summary:
>   - 2494 affine relations were detected.
>   - rule 'affine: new relation' was applied 2'494 times.
>   - rule 'at_most_one: dominated singleton' was applied 1 time.
>   - rule 'at_most_one: removed literals' was applied 10 times.
>   - rule 'at_most_one: resolved two constraints with opposite literal' was applied 5 times.
>   - rule 'at_most_one: size one' was applied 1 time.
>   - rule 'at_most_one: transformed into max clique.' was applied 3 times.
>   - rule 'automaton: expanded' was applied 50 times.
>   - rule 'bool_and: x => x' was applied 50 times.
>   - rule 'bool_or: implications' was applied 12 times.
>   - rule 'deductions: 2000 stored' was applied 1 time.
>   - rule 'domination: in exactly one' was applied 10 times.
>   - rule 'dual: fix variable' was applied 4 times.
>   - rule 'duplicate: removed constraint' was applied 3'169'107 times.
>   - rule 'exactly_one: removed literals' was applied 55 times.
>   - rule 'exactly_one: simplified objective' was applied 5 times.
>   - rule 'exactly_one: singleton' was applied 50 times.
>   - rule 'exactly_one: size two' was applied 5 times.
>   - rule 'linear: always true' was applied 1'950 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'950 times.
>   - rule 'linear: fixed or dup variables' was applied 1'950 times.
>   - rule 'linear: remapped using affine relations' was applied 51'950 times.
>   - rule 'new_bool: automaton expansion' was applied 2'388'968 times.
>   - rule 'objective: variable not used elsewhere' was applied 5 times.
>   - rule 'presolve: 35 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 12'018 times.
>   - rule 'setppc: removed dominated constraints' was applied 203 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 1'000 times.
>   - rule 'variables: detect half reified value encoding' was applied 2'000 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x178180983c326623)
> #Variables: 2'386'139 (#bools: 991 in objective) (2'330'991 primary variables)
>   - 2'386'139 Booleans in [0,1]
> #kAtMostOne: 115 (#literals: 345)
> #kBoolAnd: 115'281 (#enforced: 115'281 #multi: 4'247) (#literals: 4'878'428)
> #kBoolOr: 1'305'793 (#literals: 6'056'857)
> #kExactlyOne: 61'025 (#literals: 2'417'310)
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> 
> Preloading model.
> #Bound 107.38s best:inf   next:[0,991]    initial_domain
> #1     107.53s best:990   next:[0,989]    complete_hint
> #Model 108.64s var:2386139/2386139 constraints:1482214/1482214
> 
> Starting search at 108.81s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #2     115.54s best:980   next:[0,979]    rnd_cst_lns (d=5.00e-01 s=9 t=0.10 p=0.00 stall=0 h=base) [hint]
> #3     119.63s best:979   next:[0,978]    no_lp [hint]
> #Model 121.88s var:2385900/2386139 constraints:1482089/1482214
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  11.22s,   11.22s]   11.22s   0.00ns   11.22s         1 [631.24ms, 631.24ms] 631.24ms   0.00ns 631.24ms
>            'default_lp':         1 [  11.18s,   11.18s]   11.18s   0.00ns   11.18s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>      'feasibility_pump':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'fs_random':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         1 [  11.69s,   11.69s]   11.69s   0.00ns   11.69s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_cst_lns':         1 [   4.70s,    4.70s]    4.70s   0.00ns    4.70s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_dec_lns':         1 [   9.22s,    9.22s]    9.22s   0.00ns    9.22s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_var_lns':         1 [  11.76s,   11.76s]   11.76s   0.00ns   11.76s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'ls':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                'ls_lin':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                'max_lp':         1 [  19.87s,   19.87s]   19.87s   0.00ns   19.87s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [  11.19s,   11.19s]   11.19s   0.00ns   11.19s         1 [ 75.01ms,  75.01ms]  75.01ms   0.00ns  75.01ms
>          'pseudo_costs':         1 [  19.87s,   19.87s]   19.87s   0.00ns   19.87s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'quick_restart':         1 [  11.17s,   11.17s]   11.17s   0.00ns   11.17s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>   'quick_restart_no_lp':         1 [  11.19s,   11.19s]   11.19s   0.00ns   11.19s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'reduced_costs':         1 [  19.13s,   19.13s]   19.13s   0.00ns   19.13s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'rins/rens':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>           'rnd_cst_lns':         1 [   6.84s,    6.84s]    6.84s   0.00ns    6.84s         1 [ 10.00ns,  10.00ns]  10.00ns   0.00ns  10.00ns
>           'rnd_var_lns':         1 [   5.77s,    5.77s]    5.77s   0.00ns    5.77s         1 [ 10.00ns,  10.00ns]  10.00ns   0.00ns  10.00ns
> 
> Search stats                  Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  2'386'294         15     3'857     2'137  16'187'161          3'734
>            'default_lp':  2'386'139          0     2'207     1'976   9'985'771          2'903
>             'fs_random':          0          0         0         0           0              0
>       'fs_random_no_lp':          0          0         0         0           0              0
>                'max_lp':  2'386'139          0     1'412     1'412   6'453'453      6'454'866
>                 'no_lp':  2'386'139          0     3'310     1'977  11'817'964          7'290
>          'pseudo_costs':  2'386'139          0     1'374     1'374   6'306'784      6'308'159
>         'quick_restart':  2'386'139          0     2'157     1'976   9'766'860          2'703
>   'quick_restart_no_lp':  2'386'139          0     2'921     1'976  11'331'973          5'760
>         'reduced_costs':  2'386'139          0     1'338     1'338   6'159'273      6'160'612
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':             9         438       5'696             0         0         0           0         0          0            0        0
>            'default_lp':             0           0           0             0         0         0           0         0          0            0        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':             0           0           0             0         0         0           0         0          0            0        0
>          'pseudo_costs':             0           0           0             0         0         0           0         0          0            0        0
>         'quick_restart':             0           0           0             0         0         0           0         0          0            0        0
>   'quick_restart_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>         'reduced_costs':             0           0           0             0         0         0           0         0          0            0        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>          'max_lp':          1           0          0        0        0        0
>    'pseudo_costs':          1           0          0        0        0        0
>   'reduced_costs':          1           0          0        0        0        0
> 
> Lp dimension        Final dimension of first component
>          'max_lp':  0 rows, 2386135 columns, 0 entries
>    'pseudo_costs':  0 rows, 2386135 columns, 0 entries
>   'reduced_costs':  0 rows, 2386135 columns, 0 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow  Bad  BadScaling
>          'max_lp':          0            0       0         0    0           0
>    'pseudo_costs':          0            0       0         0    0           0
>   'reduced_costs':          0            0       0         0    0           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>          'max_lp':    6'119'363        0        0       0          0      0             0        0/0
>    'pseudo_costs':    6'119'363        0        0       0          0      0             0        0/0
>   'reduced_costs':    6'119'363        0        0       0          0      0             0        0/0
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           0/0      0%    5.00e-01       0.10
>   'graph_cst_lns':           0/0      0%    5.00e-01       0.10
>   'graph_dec_lns':           0/0      0%    5.00e-01       0.10
>   'graph_var_lns':           0/0      0%    5.00e-01       0.10
>       'rins/rens':           0/0      0%    5.00e-01       0.10
>     'rnd_cst_lns':           1/1    100%    7.07e-01       0.10
>     'rnd_var_lns':           0/1    100%    7.07e-01       0.10
> 
> Solutions (3)       Num   Rank
>   'complete_hint':    1  [1,1]
>           'no_lp':    1  [3,3]
>     'rnd_cst_lns':    1  [2,2]
> 
> Objective bounds     Num
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':      3       12        3
>    'fj solution hints':      0        0        0
>         'lp solutions':      0        0        0
>                 'pump':      0        0
> 
> Improving bounds shared    Num  Sym
>                   'core':  239    0
> 
> Clauses shared    Num
>          'core':    1
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 979
> best_bound: 0
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 130.422
> usertime: 130.422
> deterministic_time: 36.2181
> gap_integral: 4.86433
> solution_fingerprint: 0xc2224aa698994a72
> ```

性能自体は悪くないかも.
例えば `protein_n050k050.txt` で 497 は `WMM_HEXALY` を 1 だけ上回っている.

一方で巨大なインスタンスでは presolve に時間がかかりすぎていて初期解をちょっと改善して終わりみたいになったりする.
DNA 配列の長さ 100 を 100 個用意して計算してみると...

In [ ]:
```python
instance_large1 = scsp.example.load("nucleotide_n100k100.txt")
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
> Initial optimization model '': (model_fingerprint: 0xa753fb3562db7aba)
> #Variables: 1'206 (#bools: 600 in objective) (1'206 primary variables)
>   - 600 Booleans in [0,1]
>   - 600 in [0,6]
>   - 6 constants in {0,1,2,3,4,5} 
> #kAutomaton: 100
> #kLinear1: 600 (#enforced: 600)
> #kLinear2: 600 (#enforced: 600)
> 
> Starting presolve at 0.00s
> The solution hint is complete and is feasible. Its objective value is 600.
>   1.28e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.91e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   2.58e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   9.72e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   2.17e+00s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=4'783'638 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 353801 / 4823320
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:12637846 literals:32489084 vars:4822737 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [2.32853s] clauses:12637746 literals:32488784 vars:4822737 one_side_vars:0 simple_definition:100 singleton_clauses:0
> [SAT presolve] [3.20244s] clauses:12556546 literals:32488784 vars:4782137 one_side_vars:0 simple_definition:100 singleton_clauses:0
>   5.23e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.30e+00s  1.02e+00d *[Probe] #probed=558 #new_binary_clauses=8'955 
>   1.36e+01s  1.95e+01d *[MaxClique] Merged 9'722'569(19'445'138 literals) into 9'703'667(19'426'237 literals) at_most_ones. 
>   2.21e+00s  0.00e+00d  [DetectDominanceRelations] 
>   8.99e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.24e+00s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.65e+00s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.46e+00s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.59e-01s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.39e-01s  0.00e+00d  [DetectDifferentVariables] 
>   4.16e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=12'597'063 #num_inclusions=3'451'802 
>   1.55e-01s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.81e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   3.66e-01s  1.85e-01d  [FindBigVerticalLinearOverlap] 
>   1.51e-01s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.38e+00s  6.52e-02d  [MergeClauses] #num_collisions=122'624 #num_merges=122'624 #num_saved_literals=285'848 
>   2.42e+00s  0.00e+00d  [DetectDominanceRelations] 
>   5.16e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.42e+00s  0.00e+00d  [DetectDominanceRelations] 
>   5.14e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.80e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   6.25e-01s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 313201 / 4781963
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:12532284 literals:32440185 vars:4781963 one_side_vars:26 simple_definition:17195 singleton_clauses:0
> [SAT presolve] [2.387s] clauses:12532284 literals:32440185 vars:4781963 one_side_vars:26 simple_definition:17195 singleton_clauses:0
> [SAT presolve] [3.09213s] clauses:12532284 literals:32440185 vars:4781963 one_side_vars:26 simple_definition:17195 singleton_clauses:0
>   7.12e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   6.17e+00s  1.02e+00d *[Probe] #probed=550 #equiv=272 #new_binary_clauses=8'409 
>   1.40e+01s  1.95e+01d *[MaxClique] Merged 9'703'442(19'425'787 literals) into 9'698'495(19'420'440 literals) at_most_ones. 
> 272 affine relations still in the model.
> 
> Presolve summary:
>   - 1553 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 50 times.
>   - rule 'affine: new relation' was applied 1'553 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'automaton: expanded' was applied 100 times.
>   - rule 'bool_and: x => x' was applied 100 times.
>   - rule 'deductions: 1200 stored' was applied 1 time.
>   - rule 'dual: fix variable' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 4'783'638 times.
>   - rule 'exactly_one: removed literals' was applied 75 times.
>   - rule 'exactly_one: singleton' was applied 75 times.
>   - rule 'linear: always true' was applied 1'100 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'100 times.
>   - rule 'linear: fixed or dup variables' was applied 1'100 times.
>   - rule 'linear: remapped using affine relations' was applied 61'100 times.
>   - rule 'new_bool: automaton expansion' was applied 4'822'720 times.
>   - rule 'objective: variable not used elsewhere' was applied 1 time.
>   - rule 'presolve: 7 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 2 times.
>   - rule 'setppc: removed dominated constraints' was applied 375 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 600 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'200 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x3e61f363711afec3)
> #Variables: 4'781'963 (#bools: 599 in objective) (4'722'347 primary variables)
>   - 4'781'963 Booleans in [0,1]
> #kAtMostOne: 5'898 (#literals: 35'246)
> #kBoolAnd: 604'474 (#enforced: 604'474) (#literals: 10'297'071)
> #kBoolOr: 2'833'902 (#literals: 13'043'421)
> #kExactlyOne: 59'344 (#literals: 4'468'213)
> #kLinear2: 272
> Stopped after presolve.
> PresolvedNumVariables: 4781963
> PresolvedNumConstraints: 3503890
> PresolvedNumTerms: 27843807
> CpSolverResponse summary:
> status: UNKNOWN
> objective: 0
> best_bound: 0
> integers: 0
> booleans: 0
> conflicts: 0
> branches: 0
> propagations: 0
> integer_propagations: 0
> restarts: 0
> lp_iterations: 0
> walltime: 127.683
> usertime: 127.683
> deterministic_time: 42.3856
> gap_integral: 0
> ```

presolve が終わらなかった...
