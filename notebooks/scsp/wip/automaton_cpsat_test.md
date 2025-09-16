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

        cvars = [
            cpmodel.new_int_var(lb=0, ub=len(chars) - 1, name="") for _ in range(max_len)
        ]
        valids = [cpmodel.new_bool_var("") for _ in cvars]
        transition_expressions = [
            cpmodel.new_int_var(lb=0, ub=len(chars), name="") for _ in range(max_len)
        ]

        # 初期解としてアルファベットアルゴリズムを設定
        for valid in valids:
            cpmodel.add_hint(valid, 1)
        for idx, cvar in enumerate(cvars):
            cpmodel.add_hint(cvar, idx % len(chars))
        for texp in transition_expressions:
            cpmodel.add_hint(texp, idx % len(chars) + 1)

        if perm:
            for t in range(max(len(s) for s in instance)):
                cpmodel.add_all_different(cvars[t * len(chars) : (t + 1) * len(chars)])
        else:
            for idx, cvar in enumerate(cvars):
                cpmodel.add(cvar == idx % len(chars))

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
>  Sol: tulckigojiqfolnbyxxcovskuhmoqpxnehtqvioagssxzvgbxipprddblcsvrvnngpf
> str1: t---k-g-------n--------kuhm--pxn-htq----g--xzv--xi--------s--------
> str2: -----i-ojiqfolnb-xxc-vs-u---qp------vi---ss----bx-----------------f
> str3: -ulc-i--------n-y--co-s----o--------v-o-----z-----pp----l--------p-
> str4: -----ig-------------------------e---v--a----z-gb----rddb-csvrvnng-f
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 10.0
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
> --- Solution (of length 66) ---
>  Sol: iotujklcginqycefvaoszglnbkrudxhmpxdbcnovhostuqgvxzprvnxisnsbgpxflp
> str1: --t--k--g-n--------------k-u--hmpx---n--h--t-qg-xz--v-xis---------
> str2: io--j----i-q---f--o---lnb----x---x--c--v--s-uq----p-v--is-sb--xf--
> str3: ---u--lc-in-yc----os------------------ov-o-------zp----------p--lp
> str4: i-------g-----e-va--zg--b-r-d-----dbc-----s----v---rvn---n--g--f--
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 49.0
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
> --- Solution (of length 99) ---
>  Sol: iogjeiqlfvjkanopqrtulzcdegiqrtvnzbyqrtcxoxcdhkvnsdbcsgvqhsnkuhmqropvxdozgisnpyefghjnptsbqlgpxzvxfis
> str1: ------------------t--------------------------k-------g----nkuhm---p-x------n-----h---t--q-g-xzvx-is
> str2: io-j-iq-f-----o-----l----------n-b-----x-xc---v-s-----------u--q--pv-----is-----------sb----x---f--
> str3: -------------------ul-c---i----n--y---c-o-------s----------------o-v--oz----p-------p----l-p-------
> str4: i-g-e----v--a--------z---g-------b--r------d-----dbcs-v---------r--v-------n-------n------g-----f--
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
> --- Solution (of length 134) ---
>  Sol: tkgnkuhmpxnhtqgiojiqfolnbxxcvsuqpvlcisnycosogevaozgbrddbcpsvlrzxucpmqvnngtbdfueivdcvdpfzsmsnbrczofqjtvbxewxqrzbkhrvidgprlctodtmprpxwed
> str1: tkgnkuhmpxnhtqg----------x-----------------------z---------v---x---------------i--------s---------------------------------------------
> str2: ---------------iojiqfolnbxxcvsuqpv--is----s--------b-----------x------------f---------------------------------------------------------
> str3: -----u----------------l----c--------i-nycoso--v-oz-------p--------p-----------------------------------------------------l------p------
> str4: ---------------i----------------------------geva-zgbrddbc-sv-r-------vnng---f---------------------------------------------------------
> str5: --------p------------------------------y-----------------p--lrzxucpmqv--gt-dfu-iv-c-d---s---b---o-------------------------------------
> str6: --------p---------------b----------------------------d------------------------e-vdcvdpfzsms-br--o-q--vb-------b-h---------------------
> str7: ---------------------------------------------e------------------------n---b-------c----z---------f-jtv-xe---rzb--rvi-gp-l-----------e-
> str8: ----------------------------------------------------r----------x-----------------------------------------wxq---k-r--d--rlctodtmprpxw-d
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
> --- Solution (of length 115) ---
>  Sol: iogjprxybdeintuvwxabcdklqzcfgjnoptviklnruzbdhmpxycefruzbdlnosdhorxbcptvimoqsuvbdgqtxzdfmprupvxinoqsvwbcdlnsbeghopxf
> str1: -------------t--------k-----g-n-----k---u---hmpx----------n---h------t----q-----g--xz-------vxi---s----------------
> str2: io-j-------i------------q--f---o-----ln---b----x-----------------x-c--v----su----q------p---v-i---s-------sb-----xf
> str3: --------------u--------l--c--------i--n---------yc---------os--o------v--o----------z---p--p------------l-------p--
> str4: i-g-------e----v--a------z--g-------------b---------r---d----d----bc-------s-v-----------r--v--n---------n---g----f
> str5: ----p--y------------------------p----l-r-z-----x-----u-------------cp---m-q--v--g-t--df---u---i----v--cd--sb---o---
> str6: ----p---bde----v-----d----c-------v--------d--p----f--z-----s-----------m--s--b----------r------oq-v-b-----b--h----
> str7: ----------e-n------bc----z-f-j---tv------------x--e-r-zb--------r-----vi--------g-------p---------------l---e------
> str8: -----rx---------wx------q-----------k--r---d--------r----l---------c-t---o-----d--t----mpr-p-x------w--d-----------
> 
> solution is feasible: True
> solution status: FEASIBLE
> bset bound: 56.0
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
> --- Solution (of length 520) ---
>  Sol: zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbayxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbzyxwvutsrqponmlkjihgfedcbzyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcbayxwvu
> str1: ------t--------k---g------------------n--k--------------u------------h--------------------m---------------------p-----------------x---------n-----h-------------t--q---------g--------x----------------------z---v----------------------x--------------i---------------s----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str2: -----------------i-------------------o----ji----------------q----------f----------------o--l----------------------n-----------b---x-------------------------x--------------------c------v--s----------------------u---qp------------------v------------i---------------s-------------------------s----------------b---x----------------f------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str3: -----u--------l--------c-------------------i-------------------n--------------y--------------------c-------------o---------------------s---o------------------v------o--------------z---------p------------------------p---l--------------------p---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str4: -----------------i-g-e--------v--------------------a-------------------------z-----------------g----b---------r-------------d-------------------------d-b------------------------c---------s---------------------v---r--------------------v-------n-------------------------n------gf---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str5: ----------p----------------y--------p---l------------------r-----------------z-x--u----------------c------------p--m---------------------q--------------------v--------------g------------t---------------d----------------------f---------u-----------i------------v------------------c------------------------d----------s---------------b------------o-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str6: ----------p-------------b-----------------------d-----------------------e--------v----------------dc------v-----------------d-------------p---------f-----z------s-----m-------------------s----------------b--------r--o----------------------q--------------------v-------------------b-------------------------b-------------------h-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str7: ---------------------e----------------n-----------b-----------------------c--z------------------f---------------------j---------------t-----------------------v-----------------------x------------------e-----------r----------------z-----------------------b---------r---------------------v------------i-g----------------p---l-----e-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str8: --------r-------------------xw-----------------------x------q-----k------------------r------------d-----------r-----l--------c--------t----o----------d---------t------m----------------------p----------------------r-p----------------xw------------------d---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
> --- Solution (of length 247) ---
>   Sol: tkgnkuhmpxnhiojiqfolnbxxulcinycosovoigevazgbrddbcsvpyplrzxucpmqvgtdfupbdevdcvdpfzsmsenbczfjtvxerzbrvigxwxqkrdrlctodtmpkkqafigqjwokkskrblxxpabivbvzkozrifsavnqaxudgqvqcewbfgijowwyrsxqjnfpadiusiqbezhkiwshvhcomiuvddhtxxqjzqbctbakxusfcfzpeecvwantfmgqzu
> str01: tkgnkuhmpxnh-----------------------------------------------------t---------------------------------------q------------------g-----------x--------z--------v---x------------i------s--------------------------------------------------------------------
> str02: ------------iojiqfolnbxx--c-------v--------------s--------u---q------p---v--------------------------i------------------------------s--------------------s---------------b----------x---f---------------------------------------------------------------
> str03: -----u-------------l------cinycosovo-----z---------p-pl-----p------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str04: ------------i------------------------gevazgbrddbcsv----r-------v---------------------n---------------------------------------------------------------------n-----g-------f-----------------------------------------------------------------------------
> str05: --------p--------------------y---------------------p--lrzxucpmqvgtdfu-------------------------------i-----------------------------------------v----------------------c--------------------d--s--b-----------o------------------------------------------
> str06: --------p------------b-----------------------d--------------------------evdcvdpfzsms--b--------r-----------------o------q---------------------vb------------------------b--------------------------h---------------------------------------------------
> str07: --------------------------------------e----------------------------------------------nbczfjtvxerzbrvig---------------p-----------------l------------------------------e--------------------------------------------------------------------------------
> str08: --------------------------------------------r------------x---------------------------------------------wxqkrdrlctodtmp---------------r----p-------------------x--------w------------------d------------------------------------------------------------
> str09: -k--k-----------q-----------------------a--------------------------f--------------------------------ig---q--------------------jwokkskrbl-------------------------g-------------------------------------------------------------------------------------
> str10: -------------------l--xx---------------------------p---------------------------------------------------------------------a------------b------ivbvzkoz---------------------------------------------z------v-------d-------------------------------------
> str11: -k------------------------------------------r-------------------------------------------------------i---------------------f--------s-------a--v------------n---------c--------------------d----q------w-h----------------z--c--------------------------
> str12: ----------------q-----------------------a----------------xu-------d----------------------------------g---q------------------------------------v-------------q--------cewbfgijowwy----------------------------------------------------------------------
> str13: --------------------------------------------r----s-------x----q---------------------------j----------------------------------------------------------------n-------------f--------------padiusiqbezhk-------o------h------------------------------mg---
> str14: ------------i------------------------------------------------------------------------------------------w---------------------------s---------------------------------------------------------------h-----vhcomiuvdd-------------------------------m----
> str15: ------h----------------------------------------------------------t---------------------------x--------x--q--------------------j------------------z----------q-----------b----------------------------------c--------t------b---ak--------------n-------
> str16: ---------x--------------u-------s----------------------------------f-------c---fz------------------------------------p------------------------------------------------e--------------------------e---------c----v----------------------------wantfmgqzu
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
> --- Solution (of length 166) ---
>   Sol: iklxgkrxehopqtuvwxabdefjsxinquvybcdfhjklnzcfgjnovbdipqsafklnruyzbdxdhimptuvxbcejoqrsweilnoptzbchkmqvegtwdksuabqrfgijopquvdiknsentvwzbcdfmprswbghkopqxzchlyemuvwxdfgips
> str01: -------------t------------------------k-----g-n----------k---u------h-mp---x------------n------h------t-------q--g----------------------------------xz-------v-x---i-s
> str02: i---------o------------j--i-q------f-----------o----------ln----b-x--------x-c---------------------v------su--q------p--v-i--s-------------s-b------x------------f----
> str03: --------------u------------------------l--c--------i-------n--y--------------c--o--s-----o---------v----------------o--------------z-----p--------p-----l-----------p-
> str04: i---g---e------v--a----------------------z--g----b----------r----d-d--------bc-----s---------------v-----------r--------v---n--n--------------g------------------f----
> str05: -----------p-------------------y--------------------p-----l-r--z--x------u---c------------p------mqv-gt-d-------f------u--i------v---cd----s-b---o--------------------
> str06: -----------p-------bde--------v---d-------c-----v-d-p---f------z-------------------s-------------m--------s--b-r----o-q-v-----------b--------b-h----------------------
> str07: --------e------------------n----bc-------z-f-j--------------------------t-vx--e---r---------zb-----------------r--------v-i-------------------g---p-----l-e-----------
> str08: ------rx--------wx----------q---------k---------------------r----d----------------r----l------c-------t-------------o----d------t-------mpr-------p-x---------w-d-----
> str09: -k---k------q-----a---f---i-----------------g--------q-------------------------j----w----o------k--------ks----------------k--------------r--b----------l---------g---
> str10: --lx---x---p------ab------i---v-b---------------v--------------z--------------------------------k-------------------o--------------z-----------------z-------v--d-----
> str11: -k----r-------------------i--------f------------------sa------------------v-------------n-----c---------d-----q-------------------w------------h-----zc---------------
> str12: ------------q-----a------x---u----d---------g--------q--------------------v------q------------c-----e--w-----b--fgijo-------------w---------w------------y------------
> str13: ------r-----------------sx--q--------j--n--f--------p--a---------d---i---u---------s--i-----------q----------b----------------e----z-----------hko-----h---m------g---
> str14: i---------------w-------s-----------h-----------v-------------------h--------c--o----------------m----------------i----uvd------------d-m-----------------------------
> str15: ---------h---t---x-------x--q--------j---z-----------q----------b------------c-------------t-b--------------a--------------kn-----------------------------------------
> str16: ---x----------u---------s----------f------cf-------------------z-------p------e------e--------c----v---w----a---------------n---t------fm-----g----q-z------u---------
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
> Initial optimization model '': (model_fingerprint: 0xac2ee5e301656111)
> #Variables: 1'875 (#bools: 625 in objective) (1'250 primary variables)
>   - 625 Booleans in [0,1]
>   - 625 in [0,24]
>   - 625 in [0,25]
> #kAutomaton: 4
> #kLinear1: 1'250 (#enforced: 625)
> #kLinear2: 625 (#enforced: 625)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   2.21e-04s  0.00e+00d  [DetectDominanceRelations] 
>   6.37e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   2.56e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   5.51e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.90e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=78'735 
> [Symmetry] Graph for symmetry has 214'516 nodes and 561'604 arcs.
> [Symmetry] Symmetry computation done. time: 0.0538328 dtime: 0.0919706
> [Symmetry] #generators: 112, average support size: 25.2143
> [Symmetry] The model contains 4 duplicate constraints !
> [Symmetry] 938 orbits on 2313 variables with sizes: 32,24,8,6,6,6,6,6,6,6,...
> [Symmetry] Found orbitope of size 27 x 6
> [SAT presolve] num removable Booleans: 1062 / 58837
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:151963 literals:386901 vars:58710 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0158876s] clauses:151959 literals:386889 vars:58710 one_side_vars:0 simple_definition:5 singleton_clauses:0
> [SAT presolve] [0.0180126s] clauses:151911 literals:386889 vars:58686 one_side_vars:0 simple_definition:5 singleton_clauses:0
>   3.48e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.77e-01s  1.00e+00d *[Probe] #probed=5'232 #equiv=15 #new_binary_clauses=3'117 
>   1.85e-01s  1.00e+00d *[MaxClique] Merged 117'347(234'694 literals) into 66'512(183'860 literals) at_most_ones. 
>   1.53e-02s  0.00e+00d  [DetectDominanceRelations] 
>   7.66e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.32e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.60e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=90 
>   4.35e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.17e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.75e-03s  0.00e+00d  [DetectDifferentVariables] 
>   4.01e-02s  1.84e-03d  [ProcessSetPPC] #relevant_constraints=103'374 #num_inclusions=66'456 
>   2.21e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.19e-02s  2.57e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   3.31e-03s  1.67e-03d  [FindBigVerticalLinearOverlap] 
>   2.04e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   7.29e-03s  4.64e-04d  [MergeClauses] #num_collisions=198 #num_merges=198 #num_saved_literals=420 
>   1.45e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.96e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.44e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.92e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.68e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   3.56e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 213'592 nodes and 449'820 arcs.
> [Symmetry] Symmetry computation done. time: 0.051365 dtime: 0.101102
> [Symmetry] #generators: 28, average support size: 91.2857
> [Symmetry] 910 orbits on 2188 variables with sizes: 6,6,6,6,6,6,6,6,6,6,...
> [Symmetry] Found orbitope of size 27 x 6
> [SAT presolve] num removable Booleans: 1023 / 58663
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:92412 literals:217022 vars:58125 one_side_vars:0 simple_definition:50927 singleton_clauses:0
> [SAT presolve] [0.00661025s] clauses:92412 literals:217022 vars:58125 one_side_vars:0 simple_definition:50927 singleton_clauses:0
> [SAT presolve] [0.00858513s] clauses:92412 literals:217022 vars:58125 one_side_vars:0 simple_definition:50927 singleton_clauses:0
>   4.01e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.92e-01s  1.00e+00d *[Probe] #probed=5'216 #equiv=42 #new_binary_clauses=3'142 
>   1.39e-01s  7.32e-01d  [MaxClique] Merged 62'164(124'329 literals) into 30'051(92'048 literals) at_most_ones. 
>   1.43e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.49e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.57e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.93e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=84 
>   4.07e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.64e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.12e-03s  0.00e+00d  [DetectDifferentVariables] 
>   3.95e-02s  1.21e-03d  [ProcessSetPPC] #relevant_constraints=66'881 #num_inclusions=30'048 
>   2.56e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.01e-02s  2.50e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.63e-03s  1.05e-03d  [FindBigVerticalLinearOverlap] 
>   2.54e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.03e-03s  2.04e-06d  [MergeClauses] #num_collisions=26 #num_merges=26 #num_saved_literals=76 
>   2.79e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.23e-02s  0.00e+00d  [DetectDominanceRelations] 
>   7.90e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   1.22e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.73e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.18e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   3.90e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=1 
> [Symmetry] Graph for symmetry has 99'708 nodes and 211'584 arcs.
> [Symmetry] Symmetry computation done. time: 0.0233583 dtime: 0.048287
> [Symmetry] #generators: 49, average support size: 62.7755
> [Symmetry] 945 orbits on 2467 variables with sizes: 10,10,10,10,10,10,10,10,10,10,...
> [Symmetry] Found orbitope of size 19 x 10
> [SAT presolve] num removable Booleans: 0 / 58608
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:123 literals:414 vars:125 one_side_vars:5 simple_definition:120 singleton_clauses:0
> [SAT presolve] [8.426e-05s] clauses:123 literals:414 vars:125 one_side_vars:5 simple_definition:120 singleton_clauses:0
> [SAT presolve] [0.000605309s] clauses:123 literals:414 vars:125 one_side_vars:5 simple_definition:120 singleton_clauses:0
>   4.24e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.97e-01s  1.00e+00d *[Probe] #probed=5'212 #new_binary_clauses=3'058 
>   2.41e-03s  1.15e-04d  [MaxClique] 
>   1.23e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.82e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.63e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.15e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.08e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.55e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.09e-03s  0.00e+00d  [DetectDifferentVariables] 
>   1.85e-02s  6.52e-04d  [ProcessSetPPC] #relevant_constraints=36'817 
>   2.43e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.00e-02s  2.49e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.64e-03s  1.05e-03d  [FindBigVerticalLinearOverlap] 
>   2.54e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.07e-03s  2.04e-06d  [MergeClauses] #num_collisions=26 #num_merges=26 #num_saved_literals=76 
>   1.22e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.73e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.38e-02s  0.00e+00d  [ExpandObjective] #entries=2'724'994 #tight_variables=208'413 #tight_constraints=36'694 #expands=660 
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
>   - rule 'linear1: x in domain' was applied 625 times.
>   - rule 'linear: always true' was applied 1'225 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'225 times.
>   - rule 'linear: fixed or dup variables' was applied 1'225 times.
>   - rule 'linear: remapped using affine relations' was applied 3'725 times.
>   - rule 'new_bool: automaton expansion' was applied 58'212 times.
>   - rule 'objective: expanded via tight equality' was applied 660 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 636 times.
>   - rule 'objective: variable not used elsewhere' was applied 15 times.
>   - rule 'presolve: 644 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 34'326 times.
>   - rule 'setppc: removed dominated constraints' was applied 17 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 625 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'250 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x78abd6ca6449fe3d)
> #Variables: 58'608 (#bools: 847 in objective) (27'226 primary variables)
>   - 58'608 Booleans in [0,1]
> #kBoolAnd: 27 (#enforced: 27 #multi: 25) (#literals: 130)
> #kBoolOr: 69 (#literals: 207)
> #kExactlyOne: 36'694 (#literals: 208'413)
> [Symmetry] Graph for symmetry has 98'229 nodes and 211'584 arcs.
> [Symmetry] Symmetry computation done. time: 0.0232418 dtime: 0.0476242
> [Symmetry] #generators: 47, average support size: 64.8936
> [Symmetry] 945 orbits on 2458 variables with sizes: 10,10,10,10,10,10,10,10,10,10,...
> [Symmetry] Found orbitope of size 19 x 10
> 
> Preloading model.
> #Bound   2.81s best:inf   next:[0,609]    initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model   2.83s var:58608/58608 constraints:36790/36790
> 
> Starting search at 2.84s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       3.97s best:533   next:[0,532]    core
> #Model   4.02s var:58559/58608 constraints:36766/36790
> #2       4.03s best:532   next:[0,531]    no_lp [hint]
> #3       4.07s best:531   next:[0,530]    default_lp [hint]
> #4       4.13s best:91    next:[0,90]     rens_pump_lns (d=5.00e-01 s=15 t=0.10 p=0.00 stall=0 h=base)
> #5       4.30s best:90    next:[0,89]     rnd_cst_lns (d=5.00e-01 s=20 t=0.10 p=0.00 stall=0 h=base) [hint]
> #6       4.44s best:85    next:[0,84]     graph_cst_lns (d=5.00e-01 s=23 t=0.10 p=0.00 stall=0 h=base) [hint]
> #7       4.53s best:84    next:[0,83]     ls_restart_decay(batch:1 lin{mvs:67 evals:385} #w_updates:23 #perturb:0)
> #8       4.60s best:79    next:[0,78]     graph_var_lns (d=5.00e-01 s=21 t=0.10 p=0.00 stall=0 h=base)
> #9       4.97s best:78    next:[0,77]     rnd_cst_lns (d=7.07e-01 s=31 t=0.10 p=1.00 stall=0 h=base) [hint]
> #10      4.97s best:71    next:[0,70]     graph_cst_lns (d=7.07e-01 s=28 t=0.10 p=1.00 stall=0 h=base)
> #11      5.60s best:70    next:[0,69]     graph_cst_lns (d=5.38e-01 s=44 t=0.10 p=0.50 stall=0 h=base) [hint]
> #12      5.97s best:69    next:[0,68]     graph_dec_lns (d=8.76e-01 s=54 t=0.10 p=1.00 stall=1 h=base) [hint]
> #Bound   7.36s best:69    next:[1,68]     bool_core (num_cores=1 [size:11 mw:1 d:4] a=837 d=4 fixed=49/58617 clauses=36'449)
> #Bound   7.67s best:69    next:[2,68]     bool_core (num_cores=2 [size:12 mw:1 d:4] a=826 d=4 fixed=49/58637 clauses=36'500)
> #Bound   7.96s best:69    next:[3,68]     bool_core (num_cores=3 [size:11 mw:1 d:4] a=816 d=4 fixed=49/58657 clauses=36'520)
> #Bound   8.24s best:69    next:[4,68]     bool_core (num_cores=4 [size:11 mw:1 d:4] a=806 d=4 fixed=49/58676 clauses=36'541)
> #Bound   8.55s best:69    next:[5,68]     bool_core (num_cores=5 [size:12 mw:1 d:4] a=795 d=4 fixed=49/58696 clauses=36'563)
> #Bound   8.87s best:69    next:[6,68]     bool_core (num_cores=6 [size:11 mw:1 d:4] a=785 d=4 fixed=49/58716 clauses=36'588)
> #13      9.14s best:68    next:[6,67]     graph_arc_lns (d=2.16e-01 s=119 t=0.10 p=0.40 stall=9 h=base)
> #Bound   9.22s best:68    next:[7,67]     bool_core (num_cores=7 [size:15 mw:1 amo:1 lit:2 d:4] a=772 d=4 fixed=49/58739 clauses=36'612)
> #Bound   9.69s best:68    next:[8,67]     bool_core (num_cores=8 [size:17 mw:1 d:5] a=756 d=5 fixed=49/58767 clauses=36'643)
> #Bound   9.92s best:68    next:[9,67]     bool_core (num_cores=9 [size:11 mw:1 d:4] a=746 d=5 fixed=49/58792 clauses=36'669)
> #Bound  10.18s best:68    next:[10,67]    bool_core (num_cores=10 [size:11 mw:1 d:4] a=736 d=5 fixed=49/58811 clauses=36'691)
> #Bound  10.46s best:68    next:[11,67]    bool_core (num_cores=11 [size:11 mw:1 d:4] a=726 d=5 fixed=49/58830 clauses=36'710)
> #Bound  10.91s best:68    next:[12,67]    bool_core (num_cores=12 [size:20 mw:1 amo:2 lit:4 d:5] a=707 d=5 fixed=49/58858 clauses=36'740)
> #Bound  11.18s best:68    next:[13,67]    bool_core (num_cores=13 [size:11 mw:1 d:4] a=697 d=5 fixed=49/58884 clauses=36'769)
> #Bound  11.46s best:68    next:[14,67]    bool_core (num_cores=14 [size:12 mw:1 d:4] a=686 d=5 fixed=49/58904 clauses=36'791)
> #Bound  11.71s best:68    next:[15,67]    bool_core (num_cores=15 [size:11 mw:1 d:4] a=676 d=5 fixed=49/58924 clauses=36'812)
> #Bound  11.96s best:68    next:[16,67]    bool_core (num_cores=16 [size:12 mw:1 d:4] a=665 d=5 fixed=49/58944 clauses=36'835)
> #Bound  12.22s best:68    next:[17,67]    bool_core (num_cores=17 [size:11 mw:1 d:4] a=655 d=5 fixed=49/58964 clauses=36'855)
> #Bound  12.50s best:68    next:[18,67]    bool_core (num_cores=18 [size:12 mw:1 d:4] a=644 d=5 fixed=49/58984 clauses=36'875)
> #Bound  12.96s best:68    next:[19,67]    bool_core (num_cores=19 [size:20 mw:1 amo:1 lit:3 d:5] a=625 d=5 fixed=49/59012 clauses=36'903)
> #Bound  13.21s best:68    next:[20,67]    bool_core (num_cores=20 [size:11 mw:1 d:4] a=615 d=5 fixed=49/59038 clauses=36'931)
> #Bound  13.62s best:68    next:[21,67]    bool_core (num_cores=21 [size:17 mw:1 amo:1 lit:2 d:5] a=600 d=5 fixed=49/59063 clauses=36'957)
> #Bound  13.94s best:68    next:[22,67]    bool_core (num_cores=22 [size:12 mw:1 d:4] a=589 d=5 fixed=49/59088 clauses=36'983)
> #Bound  14.29s best:68    next:[23,67]    bool_core (num_cores=23 [size:16 mw:1 amo:1 lit:2 d:4] a=576 d=5 fixed=49/59113 clauses=37'008)
> #Bound  14.59s best:68    next:[24,67]    bool_core (num_cores=24 [size:11 mw:1 d:4] a=566 d=5 fixed=49/59136 clauses=37'034)
> #Bound  15.04s best:68    next:[25,67]    bool_core (num_cores=25 [size:21 mw:1 amo:1 lit:7 d:4] a=553 d=5 fixed=49/59160 clauses=37'058)
> #Bound  15.50s best:68    next:[26,67]    bool_core (num_cores=26 [size:22 mw:1 amo:2 lit:7 d:5] a=537 d=5 fixed=49/59191 clauses=37'093)
> #14     15.63s best:67    next:[26,66]    graph_dec_lns (d=9.81e-01 s=223 t=0.10 p=0.91 stall=7 h=base)
> #Bound  15.97s best:67    next:[27,66]    bool_core (num_cores=27 [size:22 mw:1 amo:1 lit:8 d:4] a=524 d=5 fixed=49/59221 clauses=37'123)
> #Bound  16.84s best:67    next:[28,66]    bool_core (num_cores=28 [size:40 mw:1 amo:4 lit:31 d:5] a=499 d=5 fixed=49/59250 clauses=37'162)
> #Bound  17.10s best:67    next:[29,66]    bool_core (num_cores=29 [size:11 mw:1 d:4] a=489 d=5 fixed=49/59271 clauses=37'187)
> #Bound  18.06s best:67    next:[30,66]    bool_core (num_cores=30 [size:44 mw:1 amo:3 lit:34 d:4] a=457 d=5 fixed=49/59295 clauses=37'215)
> #Bound  18.55s best:67    next:[31,66]    bool_core (num_cores=31 [size:19 mw:1 amo:1 lit:16 d:5] a=455 d=5 fixed=49/59310 clauses=37'258)
> #Bound  18.93s best:67    next:[32,66]    bool_core (num_cores=32 [size:13 mw:1 amo:1 lit:7 d:6] a=448 d=6 fixed=49/59326 clauses=37'312)
> #Bound  19.11s best:67    next:[33,66]    bool_core (num_cores=33 [size:8 mw:1 d:5] a=441 d=6 fixed=49/59351 clauses=37'365)
> #Bound  19.20s best:67    next:[34,66]    bool_core (num_cores=34 [size:2 mw:1 d:5] a=440 d=6 fixed=49/59363 clauses=37'401)
> #Bound  19.37s best:67    next:[35,66]    bool_core (num_cores=35 [size:5 mw:1 d:5] a=436 d=6 fixed=49/59372 clauses=37'432)
> #Bound  19.65s best:67    next:[36,66]    bool_core (num_cores=36 [size:7 mw:1 d:7] a=430 d=7 fixed=49/59386 clauses=37'499)
> #Bound  20.18s best:67    next:[37,66]    bool_core (num_cores=37 [size:2 mw:1 d:8] a=429 d=8 fixed=49/59407 clauses=37'874)
> #Bound  20.53s best:67    next:[38,66]    bool_core (num_cores=38 [size:8 mw:1 amo:1 lit:2 d:5] a=422 d=8 fixed=49/59427 clauses=37'968)
> #Bound  21.37s best:67    next:[39,66]    bool_core (num_cores=39 [size:27 mw:1 amo:2 lit:24 d:5] a=415 d=8 fixed=49/59443 clauses=38'117)
> #Bound  22.35s best:67    next:[40,66]    bool_core (num_cores=40 [size:26 mw:1 amo:2 lit:19 d:6] a=408 d=8 fixed=49/59461 clauses=38'200)
> #Bound  22.63s best:67    next:[41,66]    bool_core (num_cores=41 [size:2 mw:1 d:5] a=407 d=8 fixed=49/59482 clauses=38'350)
> #Bound  23.23s best:67    next:[42,66]    bool_core (num_cores=42 [size:13 mw:1 amo:1 lit:9 d:6] a=404 d=8 fixed=49/59498 clauses=38'469)
> #Bound  24.00s best:67    next:[43,66]    bool_core (num_cores=43 [size:22 mw:1 amo:1 lit:20 d:5] a=400 d=8 fixed=49/59512 clauses=38'587)
> #Bound  24.75s best:67    next:[44,66]    bool_core (num_cores=44 [size:4 mw:1 d:7] a=397 d=8 fixed=49/59523 clauses=38'772)
> #Bound  25.61s best:67    next:[45,66]    bool_core (num_cores=45 [size:7 mw:1 d:6] a=391 d=8 fixed=49/59552 clauses=39'224)
> #Bound  26.44s best:67    next:[46,66]    bool_core (num_cores=46 [size:24 mw:1 amo:3 lit:18 d:7] a=382 d=8 fixed=49/59580 clauses=39'302)
> #Bound  26.90s best:67    next:[47,66]    bool_core (num_cores=47 [size:141 mw:1 amo:13 lit:91 d:10] a=254 d=10 fixed=49/59680 clauses=39'609) [skipped_logs=0]
> #Bound  28.32s best:67    next:[48,66]    bool_core (num_cores=47 [cover] a=254 d=10 fixed=49/59862 clauses=40'649)
> #15     31.90s best:66    next:[48,65]    quick_restart
> #Bound  35.83s best:66    next:[49,65]    bool_core (num_cores=48 [size:1 mw:1] a=254 d=10 fixed=50/59986 clauses=44'556)
> #16     42.92s best:65    next:[49,64]    graph_var_lns (d=2.91e-01 s=707 t=0.10 p=0.50 stall=79 h=stalling)
> #17     44.44s best:64    next:[49,63]    quick_restart_no_lp
> #Bound  67.40s best:64    next:[50,63]    bool_core (num_cores=49 [size:1 mw:1] a=254 d=10 fixed=51/60094 clauses=54'743)
> #Bound  81.70s best:64    next:[51,63]    bool_core (num_cores=50 [size:123 mw:1 amo:10 lit:76 d:11] a=144 d=11 fixed=52/60248 clauses=45'866)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.23m,    1.23m]    1.23m   0.00ns    1.23m
>            'default_lp':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.41m,    1.41m]    1.41m   0.00ns    1.41m
>      'feasibility_pump':       511 [ 51.61us, 358.56ms] 909.69us  15.84ms 464.85ms       500 [  4.34us,   8.68us]   4.35us 193.81ns   2.17ms
>                    'fj':         2 [190.79ms, 355.51ms] 273.15ms  82.36ms 546.30ms         2 [101.94ms, 101.94ms] 101.94ms 725.00ns 203.88ms
>                    'fj':         2 [253.21ms, 294.07ms] 273.64ms  20.43ms 547.27ms         2 [101.94ms, 101.94ms] 101.94ms 400.00ns 203.87ms
>             'fs_random':         1 [   1.14s,    1.14s]    1.14s   0.00ns    1.14s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   1.33s,    1.33s]    1.33s   0.00ns    1.33s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':       258 [ 57.76ms, 520.22ms] 202.76ms  84.88ms   52.31s       249 [ 10.00ns, 108.76ms]  57.34ms  48.21ms   14.28s
>         'graph_cst_lns':       126 [118.97ms, 756.74ms] 407.28ms 147.95ms   51.32s       126 [ 10.00ns, 104.46ms]  57.48ms  47.10ms    7.24s
>         'graph_dec_lns':        78 [198.55ms,    1.04s] 668.25ms 180.64ms   52.12s        78 [ 10.00ns, 102.15ms]  52.26ms  46.26ms    4.08s
>         'graph_var_lns':       259 [ 55.88ms, 428.32ms] 198.02ms  83.40ms   51.29s       259 [ 10.00ns, 108.70ms]  58.12ms  48.15ms   15.05s
>                    'ls':       276 [ 35.28ms, 384.23ms] 183.77ms  58.18ms   50.72s       276 [389.29us, 100.91ms]  99.41ms   7.66ms   27.44s
>                'ls_lin':       287 [101.21ms, 332.66ms] 177.50ms  55.12ms   50.94s       287 [ 61.61ms, 100.70ms]  99.93ms   2.27ms   28.68s
>            'max_lp_sym':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  33.98s,   33.98s]   33.98s   0.00ns   33.98s
>                 'no_lp':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [   1.13m,    1.13m]    1.13m   0.00ns    1.13m
>          'pseudo_costs':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  23.14s,   23.14s]   23.14s   0.00ns   23.14s
>         'quick_restart':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  59.68s,   59.68s]   59.68s   0.00ns   59.68s
>   'quick_restart_no_lp':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  50.87s,   50.87s]   50.87s   0.00ns   50.87s
>         'reduced_costs':         1 [   1.95m,    1.95m]    1.95m   0.00ns    1.95m         1 [  24.85s,   24.85s]   24.85s   0.00ns   24.85s
>             'rins/rens':        84 [ 20.51ms,    1.16s] 618.17ms 447.15ms   51.93s        74 [ 10.00ns, 103.54ms]  71.84ms  45.23ms    5.32s
>           'rnd_cst_lns':        86 [165.64ms, 937.35ms] 610.22ms 151.63ms   52.48s        86 [ 10.00ns, 102.13ms]  53.09ms  45.12ms    4.57s
>           'rnd_var_lns':        82 [148.52ms,    1.02s] 638.94ms 169.30ms   52.39s        82 [ 10.00ns, 102.78ms]  51.75ms  46.05ms    4.24s
> 
> Search stats               Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  60'452     41'924    719'995    10'994  509'162'615      2'180'918
>            'default_lp':  58'608    161'588    427'781     9'890  328'771'479     24'928'504
>             'fs_random':  58'608          0      5'084     5'084    9'431'668         31'407
>       'fs_random_no_lp':  58'608          0      5'084     5'084    9'431'668         31'405
>            'max_lp_sym':  58'608        135     51'109     6'409   28'486'801     28'277'298
>                 'no_lp':  58'608    118'404    356'748     9'164  289'849'934     14'605'472
>          'pseudo_costs':  58'608      3'549     48'327     6'444   39'519'723     35'544'532
>         'quick_restart':  58'608     35'732  1'258'029    12'307  369'188'178      8'901'603
>   'quick_restart_no_lp':  58'608     30'209  1'113'159    11'805  310'422'695      6'951'376
>         'reduced_costs':  58'608      1'094     54'175     6'456   31'664'250     30'213'730
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        37'421   3'522'540   6'834'016     2'121'203        71     4'266      73'063         0      1'341       22'931      473
>            'default_lp':       104'091   1'220'547  23'437'909    22'176'630       249     5'222      90'953         0      1'761       31'341      737
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':           129      19'256      52'057             0         0     1'316      30'050         0        336        7'709        0
>                 'no_lp':        93'041   1'211'735  17'285'055    13'200'178       279     4'274      73'155         0      1'305       22'318      529
>          'pseudo_costs':         3'437     346'208   2'037'386             0         3     1'354      31'100         0        324        7'295        0
>         'quick_restart':        22'621     204'401   4'047'456     2'358'612       102     4'303      73'705         0      1'293       21'816      515
>   'quick_restart_no_lp':        19'523     168'936   3'424'301     1'396'093        80     4'258      72'939         0      1'334       22'396      449
>         'reduced_costs':         1'087      66'453     715'959             0         0     1'361      31'303         0        371        8'676        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         28           0          0  743'879        0        0
>       'fs_random':         28           0          0        0        0        0
>      'max_lp_sym':          1      37'159          0        0    1'129        0
>    'pseudo_costs':          1      92'183        291      368    8'858        0
>   'quick_restart':         28           0          0  430'854        0        0
>   'reduced_costs':          1      76'030        478      369    6'494        0
> 
> Lp dimension               Final dimension of first component
>      'default_lp':              0 rows, 22 columns, 0 entries
>       'fs_random':              0 rows, 22 columns, 0 entries
>      'max_lp_sym':  35579 rows, 57095 columns, 203288 entries
>    'pseudo_costs':   11579 rows, 58608 columns, 55246 entries
>   'quick_restart':              0 rows, 22 columns, 0 entries
>   'reduced_costs':   17235 rows, 58608 columns, 81563 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>      'max_lp_sym':          0            0   1'091         0       0           0
>    'pseudo_costs':          0            0   4'140         0   9'522           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0   4'966         0  10'057           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':          100        0        0       0          0      0             0        0/0
>       'fs_random':          100        0        0       0          0      0             0        0/0
>      'max_lp_sym':       35'579        0        0       0          0      0             0        0/0
>    'pseudo_costs':       37'082        0      174       0        102      0             0  291/1'202
>   'quick_restart':          100        0        0       0          0      0             0        0/0
>   'reduced_costs':       37'269        0      222       0        102      0            84  478/1'256
> 
> Lp Cut           reduced_costs  pseudo_costs
>          CG_FF:             60            72
>           CG_K:             12             1
>           CG_R:             15             4
>         Clique:             16            26
>      MIR_1_RLT:             56            39
>       MIR_3_FF:              -             2
>       MIR_4_FF:              -             2
>   ZERO_HALF_FF:            221           117
>    ZERO_HALF_R:             98            28
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':         2/249     50%    2.62e-01       0.11
>   'graph_cst_lns':         3/126     50%    5.94e-01       0.10
>   'graph_dec_lns':          3/78     55%    9.78e-01       0.10
>   'graph_var_lns':         2/259     49%    2.26e-01       0.11
>       'rins/rens':          3/75     29%    1.88e-03       0.10
>     'rnd_cst_lns':          3/86     55%    9.80e-01       0.10
>     'rnd_var_lns':          1/82     55%    9.80e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1     49'790         0              0          0             50         42'588
>         'fj_restart_compound_perturb_obj':        1                  1          0    29'080         11'831      8'620              4        458'067
>   'fj_restart_decay_compound_perturb_obj':        1                  1          0    31'331         18'351      6'488              4        414'956
>                'fj_restart_decay_perturb':        1                  1     47'875         0              0          0             29         45'781
>                          'ls_lin_restart':       57                 33  2'653'190         0              0          0         33'231      1'413'085
>                 'ls_lin_restart_compound':       33                 15          0   515'841         28'293    243'739          3'492     11'157'013
>         'ls_lin_restart_compound_perturb':       36                 22          0   489'392         27'014    231'143          3'965     11'608'677
>                    'ls_lin_restart_decay':       25                 18  1'103'989         0              0          0          1'880      1'397'538
>           'ls_lin_restart_decay_compound':       36                 24          0   458'704        139'332    159'591          1'096     11'590'842
>   'ls_lin_restart_decay_compound_perturb':       28                 19          0   354'955        110'317    122'248            825      9'118'379
>            'ls_lin_restart_decay_perturb':       39                 19  1'706'036         0              0          0          2'263      2'140'399
>                  'ls_lin_restart_perturb':       33                 19  1'556'981         0              0          0         19'512        821'933
>                              'ls_restart':       33                 22  1'530'193         0              0          0         22'551        802'293
>                     'ls_restart_compound':       38                 20          0   555'318         31'232    261'994          3'976     12'603'240
>             'ls_restart_compound_perturb':       27                 19          0   319'991         16'569    151'685          2'894      8'239'080
>                        'ls_restart_decay':       29                 21  1'226'881         0              0          0          2'117      1'568'039
>               'ls_restart_decay_compound':       31                 23          0   356'470        106'310    125'023          1'051      9'934'488
>       'ls_restart_decay_compound_perturb':       43                 24          0   628'805        194'587    217'071          1'120     14'301'996
>                'ls_restart_decay_perturb':       32                 18  1'419'548         0              0          0          2'108      1'775'331
>                      'ls_restart_perturb':       43                 17  1'962'686         0              0          0         18'525      1'096'042
> 
> Solutions (17)            Num     Rank
>                  'core':    1    [1,1]
>            'default_lp':    1    [3,3]
>         'graph_arc_lns':    1  [13,13]
>         'graph_cst_lns':    3   [6,11]
>         'graph_dec_lns':    2  [12,14]
>         'graph_var_lns':    2   [8,16]
>      'ls_restart_decay':    1    [7,7]
>                 'no_lp':    1    [2,2]
>         'quick_restart':    1  [15,15]
>   'quick_restart_no_lp':    1  [17,17]
>         'rens_pump_lns':    1    [4,4]
>           'rnd_cst_lns':    2    [5,9]
> 
> Objective bounds     Num
>        'bool_core':   51
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    790    2'330      505
>    'fj solution hints':      0        0        0
>         'lp solutions':    134       31      130
>                 'pump':    510       53
> 
> Improving bounds shared    Num  Sym
>                   'core':   49    0
> 
> Clauses shared                Num
>                  'core':  214'018
>            'default_lp':   38'737
>                 'no_lp':   74'343
>          'pseudo_costs':      190
>         'quick_restart':   16'333
>   'quick_restart_no_lp':   10'952
>         'reduced_costs':  181'479
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 64
> best_bound: 51
> integers: 910
> booleans: 58608
> conflicts: 0
> branches: 5084
> propagations: 9431668
> integer_propagations: 31407
> restarts: 5084
> lp_iterations: 0
> walltime: 120.135
> usertime: 120.135
> deterministic_time: 534.736
> gap_integral: 1395.11
> solution_fingerprint: 0x1b68fde5267873e8
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
> Initial optimization model '': (model_fingerprint: 0x35f52cb388ed36e9)
> #Variables: 1'950 (#bools: 650 in objective) (1'300 primary variables)
>   - 650 Booleans in [0,1]
>   - 650 in [0,25]
>   - 650 in [0,26]
> #kAutomaton: 8
> #kLinear1: 1'300 (#enforced: 650)
> #kLinear2: 650 (#enforced: 650)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   3.24e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.41e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   4.28e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   2.24e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   4.47e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=177'015 
> [Symmetry] Graph for symmetry has 475'324 nodes and 1'254'896 arcs.
> [Symmetry] Symmetry computation done. time: 0.163631 dtime: 0.197999
> [Symmetry] #generators: 214, average support size: 8.37383
> [Symmetry] The model contains 8 duplicate constraints !
> [Symmetry] 649 orbits on 1482 variables with sizes: 56,32,8,7,7,7,7,7,7,7,...
> [Symmetry] Found orbitope of size 9 x 2
> [SAT presolve] num removable Booleans: 2272 / 130988
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:339266 literals:865092 vars:130733 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0464399s] clauses:339258 literals:865068 vars:130733 one_side_vars:0 simple_definition:9 singleton_clauses:0
> [SAT presolve] [0.0517283s] clauses:339136 literals:865068 vars:130672 one_side_vars:0 simple_definition:9 singleton_clauses:0
>   7.82e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.49e-01s  1.00e+00d *[Probe] #probed=4'870 #equiv=16 #new_binary_clauses=3'832 
>   2.49e-01s  1.00e+00d *[MaxClique] Merged 262'604(525'208 literals) into 233'306(495'911 literals) at_most_ones. 
>   3.76e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.00e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.41e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.38e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=96 
>   1.34e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.36e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   4.25e-03s  0.00e+00d  [DetectDifferentVariables] 
>   1.03e-01s  6.32e-03d  [ProcessSetPPC] #relevant_constraints=314'699 #num_inclusions=233'250 
>   5.68e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.97e-02s  5.03e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   9.47e-03s  4.64e-03d  [FindBigVerticalLinearOverlap] 
>   4.57e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.91e-02s  1.52e-03d  [MergeClauses] #num_collisions=391 #num_merges=391 #num_saved_literals=843 
>   3.75e-02s  0.00e+00d  [DetectDominanceRelations] 
>   9.63e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.75e-02s  0.00e+00d  [DetectDominanceRelations] 
>   9.52e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.00e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   8.31e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=3 
> [Symmetry] Graph for symmetry has 474'395 nodes and 1'187'442 arcs.
> [Symmetry] Symmetry computation done. time: 0.155982 dtime: 0.205673
> [Symmetry] #generators: 5, average support size: 246
> [Symmetry] 615 orbits on 1230 variables with sizes: 2,2,2,2,2,2,2,2,2,2,...
> [SAT presolve] num removable Booleans: 2195 / 130637
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:302948 literals:763359 vars:130425 one_side_vars:0 simple_definition:30131 singleton_clauses:0
> [SAT presolve] [0.0356538s] clauses:302948 literals:763359 vars:130425 one_side_vars:0 simple_definition:30131 singleton_clauses:0
> [SAT presolve] [0.0416436s] clauses:302948 literals:763359 vars:130425 one_side_vars:0 simple_definition:30131 singleton_clauses:0
>   8.63e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.74e-01s  1.00e+00d *[Probe] #probed=4'850 #equiv=76 #new_binary_clauses=3'923 
>   2.43e-01s  1.00e+00d *[MaxClique] Merged 229'844(459'694 literals) into 190'970(420'793 literals) at_most_ones. 
>   8.53e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.85e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.34e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   3.86e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.84e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=428 
>   1.47e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   6.87e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.51e-03s  0.00e+00d  [DetectDifferentVariables] 
>   9.76e-02s  5.01e-03d  [ProcessSetPPC] #relevant_constraints=271'974 #num_inclusions=190'686 
>   6.94e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.21e-02s  5.61e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   9.36e-03s  4.22e-03d  [FindBigVerticalLinearOverlap] 
>   5.87e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.05e-02s  1.30e-03d  [MergeClauses] #num_collisions=239 #num_merges=239 #num_saved_literals=539 
>   3.87e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.01e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.86e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.00e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.15e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   1.08e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 473'894 nodes and 1'104'329 arcs.
> [Symmetry] Symmetry computation done. time: 0.148788 dtime: 0.21098
> [Symmetry] #generators: 22, average support size: 67.0909
> [Symmetry] 709 orbits on 1439 variables with sizes: 6,6,6,6,3,3,3,3,3,2,...
> [Symmetry] Found orbitope of size 4 x 2
> [SAT presolve] num removable Booleans: 2127 / 130558
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:259505 literals:637468 vars:130113 one_side_vars:0 simple_definition:68225 singleton_clauses:0
> [SAT presolve] [0.0289371s] clauses:259505 literals:637468 vars:130113 one_side_vars:0 simple_definition:68225 singleton_clauses:0
> [SAT presolve] [0.0354582s] clauses:259503 literals:637464 vars:130112 one_side_vars:0 simple_definition:68224 singleton_clauses:0
>   1.04e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.74e-01s  1.00e+00d *[Probe] #probed=4'852 #new_binary_clauses=3'771 
>   2.30e-01s  1.00e+00d *[MaxClique] Merged 188'618(377'236 literals) into 137'927(326'546 literals) at_most_ones. 
>   8.34e-02s  0.00e+00d  [DetectDominanceRelations] 
>   3.85e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.33e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   4.11e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.49e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.43e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.03e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   6.49e-03s  0.00e+00d  [DetectDifferentVariables] 
>   8.45e-02s  3.60e-03d  [ProcessSetPPC] #relevant_constraints=219'201 #num_inclusions=137'917 
>   7.91e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.15e-02s  6.11e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   8.35e-03s  3.66e-03d  [FindBigVerticalLinearOverlap] 
>   7.70e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.02e-02s  9.94e-04d  [MergeClauses] #num_collisions=239 #num_merges=239 #num_saved_literals=539 
>   3.82e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.04e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.01e-02s  0.00e+00d  [ExpandObjective] #entries=6'208'240 #tight_variables=268'223 #tight_constraints=15'747 #expands=635 
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
>   - rule 'linear1: x in domain' was applied 650 times.
>   - rule 'linear: always true' was applied 1'275 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'275 times.
>   - rule 'linear: fixed or dup variables' was applied 1'275 times.
>   - rule 'linear: remapped using affine relations' was applied 6'475 times.
>   - rule 'new_bool: automaton expansion' was applied 130'338 times.
>   - rule 'objective: expanded via tight equality' was applied 635 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 632 times.
>   - rule 'objective: variable not used elsewhere' was applied 12 times.
>   - rule 'presolve: 668 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 10'809 times.
>   - rule 'setppc: removed dominated constraints' was applied 35 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 650 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'300 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xfd66ec22058f3555)
> #Variables: 130'549 (#bools: 638 in objective) (120'019 primary variables)
>   - 130'549 Booleans in [0,1]
> #kBoolAnd: 4'947 (#enforced: 4'947 #multi: 237) (#literals: 138'295)
> #kBoolOr: 65'049 (#literals: 197'266)
> #kExactlyOne: 15'747 (#literals: 268'223)
> [Symmetry] Graph for symmetry has 468'570 nodes and 988'628 arcs.
> [Symmetry] Symmetry computation done. time: 0.136423 dtime: 0.20938
> [Symmetry] #generators: 24, average support size: 65.4167
> [Symmetry] The model contains 2 duplicate constraints !
> [Symmetry] 727 orbits on 1496 variables with sizes: 8,8,8,8,4,4,4,4,4,4,...
> [Symmetry] Found orbitope of size 4 x 2
> 
> Preloading model.
> #Bound   6.54s best:inf   next:[0,636]    initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model   6.59s var:130549/130549 constraints:85743/85743
> 
> Starting search at 6.60s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       8.33s best:633   next:[0,632]    quick_restart_no_lp [hint]
> #2       8.39s best:602   next:[0,601]    quick_restart_no_lp
> #Bound   8.43s best:602   next:[1,601]    bool_core (num_cores=1 [size:11 mw:1 d:4] a=628 d=4 fixed=0/130558 clauses=81'281)
> #3       8.53s best:601   next:[1,600]    no_lp
> #Model   8.74s var:130394/130549 constraints:85663/85743
> #4       9.42s best:458   next:[1,457]    graph_var_lns (d=5.00e-01 s=19 t=0.10 p=0.00 stall=0 h=base)
> #5       9.77s best:403   next:[1,402]    graph_cst_lns (d=5.00e-01 s=21 t=0.10 p=0.00 stall=0 h=base) [hint]
> #6      10.21s best:402   next:[1,401]    ls_lin_restart_perturb(batch:1 lin{mvs:323 evals:15'195} #w_updates:101 #perturb:0)
> #7      10.57s best:401   next:[1,400]    rnd_var_lns (d=7.07e-01 s=25 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: ls_lin_restart_pertu...]
> #8      10.85s best:395   next:[1,394]    rnd_cst_lns (d=7.07e-01 s=27 t=0.10 p=1.00 stall=1 h=base) [hint]
> #9      10.85s best:394   next:[1,393]    rnd_cst_lns (d=7.07e-01 s=27 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: rnd_var_lns (d=7.07e...]
> #10     11.19s best:393   next:[1,392]    ls_lin_restart_perturb(batch:1 lin{mvs:59 evals:2'074} #w_updates:26 #perturb:0)
> #11     11.28s best:212   next:[1,211]    graph_cst_lns (d=7.07e-01 s=28 t=0.10 p=1.00 stall=0 h=base)
> #12     11.29s best:211   next:[1,210]    graph_cst_lns (d=7.07e-01 s=28 t=0.10 p=1.00 stall=0 h=base) [combined with: rnd_cst_lns (d=7.07e...]
> #13     11.82s best:205   next:[1,204]    rnd_var_lns (d=8.14e-01 s=39 t=0.10 p=1.00 stall=0 h=base) [hint]
> #14     11.93s best:200   next:[1,199]    rnd_cst_lns (d=8.14e-01 s=40 t=0.10 p=1.00 stall=0 h=base) [hint] [combined with: rnd_var_lns (d=8.14e...]
> #15     12.20s best:142   next:[1,141]    quick_restart
> #16     12.29s best:133   next:[1,132]    quick_restart
> #Bound  12.46s best:133   next:[2,132]    bool_core (num_cores=2 [size:11 mw:1 d:4] a=618 d=4 fixed=155/130577 clauses=80'972)
> #17     12.52s best:125   next:[2,124]    quick_restart_no_lp
> #Bound  13.15s best:125   next:[3,124]    bool_core (num_cores=3 [size:12 mw:1 d:4] a=607 d=4 fixed=155/130597 clauses=81'000)
> #18     13.28s best:122   next:[3,121]    quick_restart
> #Bound  13.87s best:122   next:[4,121]    bool_core (num_cores=4 [size:13 mw:1 d:4] a=595 d=4 fixed=155/130619 clauses=81'025)
> #Bound  14.50s best:122   next:[5,121]    bool_core (num_cores=5 [size:11 mw:1 d:4] a=585 d=4 fixed=155/130640 clauses=81'047)
> #Bound  15.10s best:122   next:[6,121]    bool_core (num_cores=6 [size:11 mw:1 d:4] a=575 d=4 fixed=155/130659 clauses=81'067)
> #19     15.19s best:121   next:[6,120]    graph_arc_lns (d=1.86e-01 s=70 t=0.10 p=0.00 stall=0 h=base)
> #Bound  15.82s best:121   next:[7,120]    bool_core (num_cores=7 [size:14 mw:1 d:4] a=562 d=4 fixed=155/130681 clauses=81'090)
> #20     16.15s best:120   next:[7,119]    rnd_cst_lns (d=9.14e-01 s=75 t=0.10 p=1.00 stall=1 h=base) [hint] [combined with: graph_arc_lns (d=1.8...]
> #21     16.51s best:119   next:[7,118]    graph_arc_lns (d=1.79e-01 s=92 t=0.10 p=0.25 stall=1 h=base)
> #Bound  16.78s best:119   next:[8,118]    bool_core (num_cores=8 [size:17 mw:1 d:5] a=546 d=5 fixed=155/130709 clauses=81'121)
> #Bound  17.65s best:119   next:[9,118]    bool_core (num_cores=9 [size:14 mw:1 d:4] a=533 d=5 fixed=155/130737 clauses=81'153)
> #22     18.25s best:118   next:[9,117]    quick_restart
> #Bound  18.32s best:118   next:[10,117]   bool_core (num_cores=10 [size:11 mw:1 d:4] a=523 d=5 fixed=155/130759 clauses=81'176)
> #23     18.35s best:117   next:[10,116]   quick_restart_no_lp
> #Bound  19.10s best:117   next:[11,116]   bool_core (num_cores=11 [size:13 mw:1 d:4] a=511 d=5 fixed=155/130780 clauses=81'198)
> #Bound  19.84s best:117   next:[12,116]   bool_core (num_cores=12 [size:13 mw:1 d:4] a=499 d=5 fixed=155/130803 clauses=81'221)
> #Bound  20.54s best:117   next:[13,116]   bool_core (num_cores=13 [size:11 mw:1 d:4] a=489 d=5 fixed=155/130824 clauses=81'243)
> #Bound  21.31s best:117   next:[14,116]   bool_core (num_cores=14 [size:12 mw:1 d:4] a=478 d=5 fixed=155/130844 clauses=81'274)
> #Bound  21.94s best:117   next:[15,116]   bool_core (num_cores=15 [size:12 mw:1 d:4] a=467 d=5 fixed=155/130865 clauses=81'297)
> #Bound  22.65s best:117   next:[16,116]   bool_core (num_cores=16 [size:12 mw:1 d:4] a=456 d=5 fixed=155/130886 clauses=81'319)
> #24     23.30s best:116   next:[16,115]   graph_var_lns (d=2.48e-01 s=166 t=0.10 p=0.25 stall=2 h=base)
> #Bound  23.31s best:116   next:[17,115]   bool_core (num_cores=17 [size:12 mw:1 d:4] a=445 d=5 fixed=155/130907 clauses=81'345)
> #Bound  24.14s best:116   next:[18,115]   bool_core (num_cores=18 [size:14 mw:1 d:4] a=432 d=5 fixed=155/130930 clauses=81'371)
> #Bound  24.78s best:116   next:[19,115]   bool_core (num_cores=19 [size:11 mw:1 d:4] a=422 d=5 fixed=155/130952 clauses=81'395)
> #25     25.17s best:115   next:[19,114]   graph_arc_lns (d=2.47e-01 s=190 t=0.10 p=0.45 stall=6 h=base)
> #Bound  25.54s best:115   next:[20,114]   bool_core (num_cores=20 [size:13 mw:1 d:4] a=410 d=5 fixed=155/130973 clauses=81'421)
> #Bound  26.12s best:115   next:[21,114]   bool_core (num_cores=21 [size:11 mw:1 d:4] a=400 d=5 fixed=155/130994 clauses=81'445)
> #Bound  26.68s best:115   next:[22,114]   bool_core (num_cores=22 [size:11 mw:1 d:4] a=390 d=5 fixed=155/131013 clauses=81'469)
> #Model  26.96s var:130343/130549 constraints:85637/85743
> #Bound  27.26s best:115   next:[23,114]   bool_core (num_cores=23 [size:11 mw:1 d:4] a=380 d=5 fixed=155/131032 clauses=81'493)
> #Bound  28.07s best:115   next:[24,114]   bool_core (num_cores=24 [size:15 mw:1 d:4] a=366 d=5 fixed=206/131055 clauses=81'523)
> #Bound  28.67s best:115   next:[25,114]   bool_core (num_cores=25 [size:11 mw:1 d:4] a=356 d=5 fixed=206/131078 clauses=81'548)
> #Bound  29.26s best:115   next:[26,114]   bool_core (num_cores=26 [size:12 mw:1 d:4] a=345 d=5 fixed=206/131098 clauses=81'570)
> #Bound  29.90s best:115   next:[27,114]   bool_core (num_cores=27 [size:13 mw:1 d:4] a=333 d=5 fixed=206/131120 clauses=81'597)
> #Bound  30.50s best:115   next:[28,114]   bool_core (num_cores=28 [size:11 mw:1 d:4] a=323 d=5 fixed=206/131141 clauses=81'618)
> #Bound  31.36s best:115   next:[29,114]   bool_core (num_cores=29 [size:17 mw:1 d:5] a=307 d=5 fixed=206/131166 clauses=81'644)
> #26     31.56s best:114   next:[29,113]   graph_var_lns (d=1.81e-01 s=254 t=0.10 p=0.36 stall=6 h=base)
> #Bound  32.10s best:114   next:[30,113]   bool_core (num_cores=30 [size:14 mw:1 d:4] a=294 d=5 fixed=206/131194 clauses=81'672)
> #Bound  32.73s best:114   next:[31,113]   bool_core (num_cores=31 [size:13 mw:1 d:4] a=282 d=5 fixed=206/131218 clauses=81'699)
> #Bound  33.26s best:114   next:[32,113]   bool_core (num_cores=32 [size:11 mw:1 d:4] a=272 d=5 fixed=206/131239 clauses=81'723)
> #27     33.61s best:113   next:[32,112]   graph_dec_lns (d=9.81e-01 s=265 t=0.10 p=1.00 stall=9 h=base)
> #Bound  34.01s best:113   next:[33,112]   bool_core (num_cores=33 [size:13 mw:1 d:4] a=260 d=5 fixed=206/131260 clauses=81'747)
> #Bound  34.58s best:113   next:[34,112]   bool_core (num_cores=34 [size:8 mw:1 d:5] a=253 d=5 fixed=206/131278 clauses=81'804)
> #Bound  35.27s best:113   next:[35,112]   bool_core (num_cores=35 [size:10 mw:1 d:5] a=244 d=5 fixed=206/131298 clauses=81'844)
> #Bound  36.09s best:113   next:[36,112]   bool_core (num_cores=36 [size:14 mw:1 d:4] a=231 d=5 fixed=206/131325 clauses=81'877)
> #28     36.99s best:112   next:[36,111]   graph_var_lns (d=1.45e-01 s=296 t=0.10 p=0.36 stall=2 h=base)
> #Bound  37.62s best:112   next:[37,111]   bool_core (num_cores=37 [size:16 mw:1 d:6] a=216 d=6 fixed=206/131352 clauses=82'033)
> #Bound  38.26s best:112   next:[38,111]   bool_core (num_cores=38 [size:6 mw:1 d:5] a=211 d=6 fixed=206/131379 clauses=82'117)
> #29     39.08s best:111   next:[38,110]   graph_var_lns (d=1.80e-01 s=323 t=0.10 p=0.41 stall=1 h=base)
> #Bound  39.21s best:111   next:[39,110]   bool_core (num_cores=39 [size:12 mw:1 d:5] a=200 d=6 fixed=206/131399 clauses=82'166)
> #Bound  40.45s best:111   next:[40,110]   bool_core (num_cores=40 [size:16 mw:1 d:5] a=185 d=6 fixed=206/131429 clauses=82'230)
> #30     40.72s best:110   next:[40,109]   quick_restart
> #Bound  41.93s best:110   next:[41,109]   bool_core (num_cores=41 [size:11 mw:1 d:6] a=175 d=6 fixed=206/131459 clauses=82'384)
> #Bound  44.17s best:110   next:[42,109]   bool_core (num_cores=42 [size:3 mw:1 d:7] a=173 d=7 fixed=206/131490 clauses=82'932)
> #Bound  45.14s best:110   next:[43,109]   bool_core (num_cores=43 [size:5 mw:1 d:5] a=169 d=7 fixed=206/131517 clauses=83'093)
> #Bound  45.83s best:110   next:[44,109]   bool_core (num_cores=44 [size:8 mw:1 d:6] a=162 d=7 fixed=206/131532 clauses=83'135)
> #Bound  46.31s best:110   next:[45,109]   bool_core (num_cores=45 [size:3 mw:1 d:5] a=160 d=7 fixed=206/131548 clauses=83'192)
> #31     47.17s best:109   next:[45,108]   graph_var_lns (d=3.30e-01 s=402 t=0.10 p=0.50 stall=5 h=base)
> #Bound  47.65s best:109   next:[46,108]   bool_core (num_cores=46 [size:7 mw:1 d:7] a=154 d=7 fixed=206/131560 clauses=83'457)
> #Bound  50.67s best:109   next:[47,108]   bool_core (num_cores=47 [size:13 mw:1 d:7] a=142 d=7 fixed=206/131596 clauses=83'980)
> #Bound  52.01s best:109   next:[48,108]   bool_core (num_cores=48 [size:2 mw:1 d:5] a=141 d=7 fixed=206/131626 clauses=84'266)
> #Bound  52.33s best:109   next:[49,108]   bool_core (num_cores=49 [size:2 mw:1 d:5] a=140 d=7 fixed=206/131632 clauses=84'306)
> #Bound  53.22s best:109   next:[50,108]   bool_core (num_cores=50 [size:3 mw:1 d:6] a=138 d=7 fixed=206/131644 clauses=84'518)
> #Bound  53.77s best:109   next:[51,108]   bool_core (num_cores=51 [size:2 mw:1 d:5] a=137 d=7 fixed=206/131668 clauses=84'662)
> #Bound  54.35s best:109   next:[52,108]   bool_core (num_cores=52 [size:2 mw:1 d:5] a=136 d=7 fixed=206/131681 clauses=84'819)
> #Bound  59.07s best:109   next:[53,108]   bool_core (num_cores=53 [size:2 mw:1 d:6] a=135 d=7 fixed=206/131693 clauses=84'437)
> #Bound  59.99s best:109   next:[54,108]   bool_core (num_cores=54 [size:2 mw:1 d:7] a=134 d=7 fixed=206/131716 clauses=84'721)
> #Bound  64.07s best:109   next:[55,108]   bool_core (num_cores=55 [size:4 mw:1 d:8] a=131 d=8 fixed=206/131739 clauses=85'922)
> #Bound  65.95s best:109   next:[56,108]   bool_core (num_cores=56 [size:10 mw:1 d:6] a=122 d=8 fixed=206/131776 clauses=86'282)
> #Bound  74.32s best:109   next:[57,108]   bool_core (num_cores=57 [size:2 mw:1 d:8] a=121 d=8 fixed=206/131795 clauses=88'312)
> #Bound  78.97s best:109   next:[58,108]   bool_core (num_cores=58 [size:2 mw:1 d:6] a=120 d=8 fixed=206/131839 clauses=89'466)
> #Bound  81.67s best:109   next:[59,108]   bool_core (num_cores=59 [size:5 mw:1 d:7] a=116 d=8 fixed=206/131857 clauses=90'131)
> #Bound  82.79s best:109   next:[60,108]   bool_core (num_cores=60 [size:3 mw:1 d:7] a=114 d=8 fixed=206/131886 clauses=90'398)
> #Bound 114.90s best:109   next:[61,108]   bool_core (num_cores=61 [size:5 mw:1 d:9] a=110 d=9 fixed=206/131914 clauses=94'732)
> #32    115.24s best:108   next:[61,107]   graph_var_lns (d=1.83e-01 s=1092 t=0.10 p=0.48 stall=62 h=base)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  56.70s,   56.70s]   56.70s   0.00ns   56.70s
>            'default_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [   1.12m,    1.12m]    1.12m   0.00ns    1.12m
>      'feasibility_pump':       476 [ 84.86us, 510.14ms]   1.41ms  23.35ms 671.50ms       473 [ 54.00ns,  54.00ns]  54.00ns   0.00ns  25.54us
>                    'fj':         1 [528.60ms, 528.60ms] 528.60ms   0.00ns 528.60ms         1 [104.20ms, 104.20ms] 104.20ms   0.00ns 104.20ms
>                    'fj':         1 [634.46ms, 634.46ms] 634.46ms   0.00ns 634.46ms         1 [104.20ms, 104.20ms] 104.20ms   0.00ns 104.20ms
>             'fs_random':         1 [   1.75s,    1.75s]    1.75s   0.00ns    1.75s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   1.85s,    1.85s]    1.85s   0.00ns    1.85s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        87 [157.15ms,    1.67s] 555.75ms 300.05ms   48.35s        87 [ 10.00ns, 102.38ms]  56.53ms  47.83ms    4.92s
>         'graph_cst_lns':        41 [349.12ms,    2.41s]    1.20s 529.46ms   49.16s        41 [ 10.00ns, 100.76ms]  48.32ms  47.35ms    1.98s
>         'graph_dec_lns':        30 [377.69ms,    2.97s]    1.75s 618.87ms   52.63s        30 [ 10.00ns, 100.35ms]  48.87ms  46.31ms    1.47s
>         'graph_var_lns':        98 [152.08ms,    2.47s] 491.59ms 350.63ms   48.18s        97 [ 10.00ns, 102.63ms]  59.24ms  47.27ms    5.75s
>                    'ls':       173 [135.24ms, 561.92ms] 274.69ms 117.29ms   47.52s       173 [ 31.65ms, 101.09ms]  99.71ms   5.19ms   17.25s
>                'ls_lin':       177 [ 25.89ms, 653.31ms] 268.17ms 117.48ms   47.47s       177 [  1.03ms, 102.19ms]  98.94ms  10.25ms   17.51s
>            'max_lp_sym':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  24.92s,   24.92s]   24.92s   0.00ns   24.92s
>                 'no_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  57.36s,   57.36s]   57.36s   0.00ns   57.36s
>          'pseudo_costs':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  12.73s,   12.73s]   12.73s   0.00ns   12.73s
>         'quick_restart':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  51.63s,   51.63s]   51.63s   0.00ns   51.63s
>   'quick_restart_no_lp':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'reduced_costs':         1 [   1.89m,    1.89m]    1.89m   0.00ns    1.89m         1 [  14.45s,   14.45s]   14.45s   0.00ns   14.45s
>             'rins/rens':        23 [ 65.58ms,    5.00s]    2.61s    2.12s    1.00m        20 [ 10.00ns, 100.13ms]  65.03ms  47.72ms    1.30s
>           'rnd_cst_lns':        34 [288.57ms,    2.31s]    1.40s 476.85ms   47.63s        34 [ 10.00ns, 100.29ms]  45.36ms  46.61ms    1.54s
>           'rnd_var_lns':        40 [268.86ms,    2.29s]    1.23s 542.34ms   49.08s        35 [ 10.00ns, 100.83ms]  36.43ms  46.47ms    1.28s
> 
> Search stats                Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  131'950     17'212   636'291     9'706  424'691'836      1'081'050
>            'default_lp':  130'549    120'831   197'378     5'876  182'798'842     11'714'802
>             'fs_random':  130'549          0     4'714     4'714    9'468'537          7'505
>       'fs_random_no_lp':  130'549          0     4'714     4'714    9'468'537          7'505
>            'max_lp_sym':  130'549         50    39'569     5'857   28'916'013     29'017'045
>                 'no_lp':  130'549     79'350   237'313     8'229  244'963'879      7'712'403
>          'pseudo_costs':  130'549      1'324    44'473     5'884   35'565'082     31'915'194
>         'quick_restart':  130'549     15'630   840'776     9'646  348'434'761      2'878'479
>   'quick_restart_no_lp':  130'549     12'373   667'238     9'336  285'489'630      2'268'060
>         'reduced_costs':  130'549        345    44'229     5'891   29'796'127     29'562'708
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        14'102     925'956   2'830'319       754'045        23     3'377      80'913         0        804       19'354        0
>            'default_lp':        87'924     766'620  24'463'689    22'203'168       258     1'153      28'751         0        271        6'662        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':            15          59       7'291             0         2     1'137      28'488         0        279        7'008        0
>                 'no_lp':        54'196     737'875  18'020'838    12'565'239       100     3'451      84'362         0        821       20'432        0
>          'pseudo_costs':         1'033      10'045     272'039             0         1     1'155      28'780         0        293        7'325        0
>         'quick_restart':         9'257      99'382   2'445'875       761'717       100     3'443      84'002         0        858       21'507        0
>   'quick_restart_no_lp':         6'996      64'965   1'866'610       759'629        80     3'444      84'047         0        819       19'551        0
>         'reduced_costs':           330      23'670     119'700             0         0     1'167      28'936         0        293        7'292        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          3           0          0      658        0        0
>       'fs_random':          3           0          0        0        0        0
>      'max_lp_sym':          1      32'560          0        0      669        0
>    'pseudo_costs':          1      50'392      2'178      624    4'353        0
>   'quick_restart':          3           0          0    4'270        0        0
>   'reduced_costs':          1      59'928      1'762      369    4'933        0
> 
> Lp dimension                 Final dimension of first component
>      'default_lp':                 0 rows, 2 columns, 0 entries
>       'fs_random':                 0 rows, 2 columns, 0 entries
>      'max_lp_sym':  193696 rows, 129779 columns, 690784 entries
>    'pseudo_costs':    18018 rows, 130547 columns, 62721 entries
>   'quick_restart':                 0 rows, 2 columns, 0 entries
>   'reduced_costs':    15990 rows, 130547 columns, 58903 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>      'max_lp_sym':          0            0      48         0       0           0
>    'pseudo_costs':          0            0     132         0  43'106           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0     911         0  31'087           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':            3        0        0       0          0      0             0          0/0
>       'fs_random':            3        0        0       0          0      0             0          0/0
>      'max_lp_sym':      193'696        0        0   9'243          0      0             0          0/0
>    'pseudo_costs':      196'870       86    2'820   9'433        632      0           173  2'178/9'289
>   'quick_restart':            3        0        0       0          0      0             0          0/0
>   'reduced_costs':      196'488       84    2'273   9'399        632      0             3  1'762/7'049
> 
> Lp Cut           reduced_costs  pseudo_costs
>          CG_FF:             99           127
>           CG_K:             11             2
>          CG_KL:              2             1
>           CG_R:             42            38
>         Clique:            143           194
>      MIR_1_RLT:            104           174
>       MIR_3_FF:             30            43
>       MIR_4_FF:             15            17
>       MIR_5_FF:              7            11
>       MIR_6_FF:              5             7
>   ZERO_HALF_FF:            939         1'099
>    ZERO_HALF_R:            365           465
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          5/87     48%    1.90e-01       0.10
>   'graph_cst_lns':          2/41     56%    8.56e-01       0.10
>   'graph_dec_lns':          1/30     60%    9.71e-01       0.10
>   'graph_var_lns':          8/97     46%    1.24e-01       0.10
>       'rins/rens':          2/20     35%    9.61e-02       0.10
>     'rnd_cst_lns':          3/34     59%    9.64e-01       0.10
>     'rnd_var_lns':          3/35     66%    9.85e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1     36'878         0              0          0             63        111'966
>   'fj_restart_decay_compound_perturb_obj':        1                  1          0    19'092         14'970      2'056              1        534'176
>                          'ls_lin_restart':       19                 13    662'113         0              0          0         15'733      1'419'024
>                 'ls_lin_restart_compound':       14                 14          0    56'642          1'055     27'788            299      6'201'058
>         'ls_lin_restart_compound_perturb':       18                 13          0   144'542          2'275     71'126            868      7'888'188
>                    'ls_lin_restart_decay':       28                 21  1'032'016         0              0          0          1'912      3'456'096
>           'ls_lin_restart_decay_compound':       16                 15          0    68'252          5'527     31'354            282      7'173'906
>   'ls_lin_restart_decay_compound_perturb':       32                 17          0   356'951         94'489    131'178            509     14'473'688
>            'ls_lin_restart_decay_perturb':       17                 13    621'763         0              0          0          1'201      2'111'360
>                  'ls_lin_restart_perturb':       33                 26  1'118'327         0              0          0         32'203      2'338'954
>                              'ls_restart':       14                 13    486'717         0              0          0         15'473      1'042'765
>                     'ls_restart_compound':       13                 13          0    50'561            990     24'784            252      5'768'456
>             'ls_restart_compound_perturb':       24                 20          0   109'279          2'132     53'563            659     10'709'208
>                        'ls_restart_decay':       29                 16  1'087'823         0              0          0          1'692      3'517'751
>               'ls_restart_decay_compound':       42                 27          0   301'504         69'209    116'102            674     18'859'457
>       'ls_restart_decay_compound_perturb':       17                 13          0    80'622          5'916     37'334            377      7'581'859
>                'ls_restart_decay_perturb':       15                 12    550'450         0              0          0          1'042      1'844'096
>                      'ls_restart_perturb':       19                 14    668'505         0              0          0         16'900      1'355'122
> 
> Solutions (32)               Num     Rank
>            'graph_arc_lns':    3  [19,25]
>            'graph_cst_lns':    3   [5,12]
>            'graph_dec_lns':    1  [27,27]
>            'graph_var_lns':    7   [4,32]
>   'ls_lin_restart_perturb':    2   [6,10]
>                    'no_lp':    1    [3,3]
>            'quick_restart':    5  [15,30]
>      'quick_restart_no_lp':    4   [1,23]
>              'rnd_cst_lns':    4   [8,20]
>              'rnd_var_lns':    2   [7,13]
> 
> Objective bounds     Num
>        'bool_core':   61
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    208      978      151
>    'fj solution hints':      0        0        0
>         'lp solutions':    106       10      105
>                 'pump':    475       13
> 
> Improving bounds shared    Num  Sym
>    'quick_restart_no_lp':  206    0
> 
> Clauses shared                Num
>                  'core':    4'352
>            'default_lp':        2
>                 'no_lp':        2
>          'pseudo_costs':      566
>         'quick_restart':       97
>   'quick_restart_no_lp':  178'207
>         'reduced_costs':        5
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 108
> best_bound: 61
> integers: 667
> booleans: 130549
> conflicts: 0
> branches: 4714
> propagations: 9468537
> integer_propagations: 7505
> restarts: 4714
> lp_iterations: 0
> walltime: 120.315
> usertime: 120.315
> deterministic_time: 344.241
> gap_integral: 1317.7
> solution_fingerprint: 0x842b040214c7489
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
> Initial optimization model '': (model_fingerprint: 0xc40556ee531c4fb3)
> #Variables: 1'950 (#bools: 650 in objective) (1'300 primary variables)
>   - 650 Booleans in [0,1]
>   - 650 in [0,25]
>   - 650 in [0,26]
> #kAutomaton: 16
> #kLinear1: 1'300 (#enforced: 650)
> #kLinear2: 650 (#enforced: 650)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   4.12e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.61e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.01e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   3.57e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   9.27e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=352'449 
> [Symmetry] Graph for symmetry has 942'934 nodes and 2'495'980 arcs.
> [Symmetry] Symmetry computation done. time: 0.383925 dtime: 0.392474
> [Symmetry] #generators: 423, average support size: 2.22695
> [Symmetry] The model contains 16 duplicate constraints !
> [Symmetry] 41 orbits on 467 variables with sizes: 64,16,16,15,15,15,15,15,15,15,...
> [Symmetry] Found orbitope of size 17 x 2
> [SAT presolve] num removable Booleans: 4545 / 260021
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:675238 literals:1721538 vars:259548 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.100382s] clauses:675222 literals:1721490 vars:259548 one_side_vars:0 simple_definition:17 singleton_clauses:0
> [SAT presolve] [0.111378s] clauses:674864 literals:1721490 vars:259369 one_side_vars:0 simple_definition:17 singleton_clauses:0
>   1.43e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.75e-01s  1.00e+00d *[Probe] #probed=4'286 #equiv=16 #new_binary_clauses=4'941 
>   3.60e-01s  1.05e+00d *[MaxClique] Merged 522'247(1'044'494 literals) into 503'525(1'025'773 literals) at_most_ones. 
>   7.78e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.06e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   7.07e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.20e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=96 
>   3.07e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.05e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   8.64e-03s  0.00e+00d  [DetectDifferentVariables] 
>   2.28e-01s  1.34e-02d  [ProcessSetPPC] #relevant_constraints=665'979 #num_inclusions=503'477 
>   1.05e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.89e-02s  9.51e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   1.99e-02s  9.66e-03d  [FindBigVerticalLinearOverlap] 
>   9.07e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.01e-02s  3.25e-03d  [MergeClauses] #num_collisions=869 #num_merges=869 #num_saved_literals=1'917 
>   7.70e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.00e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.83e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.99e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.25e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   1.77e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2 
> [Symmetry] Graph for symmetry has 941'459 nodes and 2'447'117 arcs.
> [Symmetry] Symmetry computation done. time: 0.374485 dtime: 0.408166
> [SAT presolve] num removable Booleans: 4350 / 259319
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:648466 literals:1649926 vars:259205 one_side_vars:0 simple_definition:20379 singleton_clauses:0
> [SAT presolve] [0.0865243s] clauses:648466 literals:1649926 vars:259205 one_side_vars:0 simple_definition:20379 singleton_clauses:0
> [SAT presolve] [0.0980393s] clauses:648466 literals:1649926 vars:259205 one_side_vars:0 simple_definition:20379 singleton_clauses:0
>   1.67e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.26e-01s  1.00e+00d *[Probe] #probed=4'156 #equiv=173 #new_binary_clauses=5'145 
>   3.50e-01s  1.00e+00d *[MaxClique] Merged 499'670(999'343 literals) into 480'025(979'635 literals) at_most_ones. 
>   2.00e-01s  0.00e+00d  [DetectDominanceRelations] 
>   8.30e-02s  0.00e+00d  [DetectDominanceRelations] 
>   5.36e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   7.93e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   3.92e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=974 
>   3.65e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.39e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.16e-02s  0.00e+00d  [DetectDifferentVariables] 
>   2.29e-01s  1.28e-02d  [ProcessSetPPC] #relevant_constraints=641'530 #num_inclusions=479'330 
>   1.32e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.01e-01s  9.63e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.10e-02s  9.43e-03d  [FindBigVerticalLinearOverlap] 
>   1.22e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.29e-02s  3.13e-03d  [MergeClauses] #num_collisions=523 #num_merges=523 #num_saved_literals=1'225 
>   8.24e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.15e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.27e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.15e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.48e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   2.32e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 940'635 nodes and 2'401'893 arcs.
> [Symmetry] Symmetry computation done. time: 0.384529 dtime: 0.405736
> [Symmetry] #generators: 32, average support size: 8
> [Symmetry] 108 orbits on 236 variables with sizes: 3,3,3,3,3,3,3,3,3,3,...
> [Symmetry] Found orbitope of size 4 x 2
> [SAT presolve] num removable Booleans: 4193 / 259143
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:624301 literals:1581727 vars:258839 one_side_vars:96 simple_definition:40499 singleton_clauses:0
> [SAT presolve] [0.0828255s] clauses:624301 literals:1581727 vars:258839 one_side_vars:96 simple_definition:40499 singleton_clauses:0
> [SAT presolve] [0.094523s] clauses:624299 literals:1581723 vars:258838 one_side_vars:96 simple_definition:40498 singleton_clauses:0
>   2.75e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.40e-01s  1.00e+00d *[Probe] #probed=4'156 #new_binary_clauses=4'799 
>   3.46e-01s  1.00e+00d *[MaxClique] Merged 477'640(955'342 literals) into 455'903(933'606 literals) at_most_ones. 
>   1.98e-01s  0.00e+00d  [DetectDominanceRelations] 
>   8.81e-02s  0.00e+00d  [DetectDominanceRelations] 
>   5.46e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   8.46e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.02e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   3.82e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.71e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.42e-02s  0.00e+00d  [DetectDifferentVariables] 
>   2.23e-01s  1.22e-02d  [ProcessSetPPC] #relevant_constraints=618'033 #num_inclusions=455'836 
>   1.59e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.02e-01s  9.90e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   2.03e-02s  9.19e-03d  [FindBigVerticalLinearOverlap] 
>   1.51e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.60e-02s  3.00e-03d  [MergeClauses] #num_collisions=523 #num_merges=523 #num_saved_literals=1'225 
>   8.78e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.30e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.19e-01s  0.00e+00d  [ExpandObjective] #entries=8'740'690 #tight_variables=329'149 #tight_constraints=17'343 #expands=223 
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
>   - rule 'linear1: x in domain' was applied 650 times.
>   - rule 'linear: always true' was applied 1'275 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'275 times.
>   - rule 'linear: fixed or dup variables' was applied 1'275 times.
>   - rule 'linear: remapped using affine relations' was applied 11'675 times.
>   - rule 'new_bool: automaton expansion' was applied 259'371 times.
>   - rule 'objective: expanded via tight equality' was applied 223 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 222 times.
>   - rule 'objective: variable not used elsewhere' was applied 6 times.
>   - rule 'presolve: 660 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 7'432 times.
>   - rule 'setppc: removed dominated constraints' was applied 67 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 650 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'300 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x6a97f9e36fb3d9f)
> #Variables: 259'139 (#bools: 643 in objective) (245'499 primary variables)
>   - 259'139 Booleans in [0,1]
> #kAtMostOne: 51 (#literals: 163)
> #kBoolAnd: 10'641 (#enforced: 10'641 #multi: 521) (#literals: 466'317)
> #kBoolOr: 143'743 (#literals: 597'470)
> #kExactlyOne: 17'343 (#literals: 329'149)
> [Symmetry] Graph for symmetry has 936'513 nodes and 2'352'623 arcs.
> [Symmetry] Symmetry computation done. time: 0.367766 dtime: 0.412407
> [Symmetry] #generators: 32, average support size: 8
> [Symmetry] 108 orbits on 236 variables with sizes: 3,3,3,3,3,3,3,3,3,3,...
> [Symmetry] Found orbitope of size 4 x 2
> 
> Preloading model.
> #Bound  13.06s best:inf   next:[0,643]    initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model  13.17s var:259139/259139 constraints:171778/171778
> 
> Starting search at 13.19s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1      15.64s best:637   next:[0,636]    fs_random [hint]
> #2      15.86s best:636   next:[0,635]    default_lp
> #3      15.91s best:599   next:[0,598]    quick_restart_no_lp
> #4      15.96s best:353   next:[0,352]    quick_restart
> #Bound  16.62s best:353   next:[1,352]    bool_core (num_cores=1 [size:11 mw:1 d:4] a=633 d=4 fixed=0/259148 clauses=162'140)
> #Model  16.65s var:258984/259139 constraints:171698/171778
> #Model  17.20s var:258725/259139 constraints:171564/171778
> #5      18.82s best:313   next:[1,312]    graph_var_lns (d=5.00e-01 s=19 t=0.10 p=0.00 stall=0 h=base)
> #6      19.64s best:301   next:[1,300]    graph_cst_lns (d=5.00e-01 s=21 t=0.10 p=0.00 stall=0 h=base) [hint]
> #7      20.36s best:300   next:[1,299]    ls_restart_decay(batch:1 lin{mvs:9 evals:310} #w_updates:5 #perturb:0)
> #8      20.47s best:299   next:[1,298]    default_lp
> #9      20.57s best:195   next:[1,194]    default_lp
> #10     20.65s best:194   next:[1,193]    default_lp
> #11     20.74s best:193   next:[1,192]    default_lp
> #12     20.82s best:192   next:[1,191]    default_lp
> #13     20.89s best:191   next:[1,190]    default_lp
> #14     20.96s best:190   next:[1,189]    default_lp
> #15     21.03s best:189   next:[1,188]    default_lp
> #16     21.09s best:188   next:[1,187]    default_lp
> #17     21.17s best:187   next:[1,186]    default_lp
> #18     21.25s best:186   next:[1,185]    default_lp
> #19     21.32s best:185   next:[1,184]    default_lp
> #20     21.40s best:183   next:[1,182]    default_lp
> #21     21.51s best:182   next:[1,181]    default_lp
> #22     21.59s best:181   next:[1,180]    default_lp
> #23     21.68s best:180   next:[1,179]    default_lp
> #24     21.76s best:179   next:[1,178]    default_lp
> #25     21.84s best:178   next:[1,177]    default_lp
> #26     21.98s best:177   next:[1,176]    default_lp
> #Bound  22.42s best:177   next:[2,176]    bool_core (num_cores=2 [size:11 mw:1 d:4] a=623 d=4 fixed=155/259167 clauses=161'843)
> #Bound  23.84s best:177   next:[3,176]    bool_core (num_cores=3 [size:11 mw:1 d:4] a=613 d=4 fixed=414/259186 clauses=161'871)
> #Bound  25.20s best:177   next:[4,176]    bool_core (num_cores=4 [size:11 mw:1 d:4] a=603 d=4 fixed=414/259205 clauses=161'899)
> #27     25.96s best:173   next:[4,172]    quick_restart_no_lp
> #Bound  27.07s best:173   next:[5,172]    bool_core (num_cores=5 [size:15 mw:1 d:4] a=589 d=4 fixed=414/259228 clauses=161'929)
> #Bound  28.57s best:173   next:[6,172]    bool_core (num_cores=6 [size:13 mw:1 d:4] a=577 d=4 fixed=414/259253 clauses=161'958)
> #28     29.45s best:172   next:[6,171]    quick_restart_no_lp
> #Bound  29.91s best:172   next:[7,171]    bool_core (num_cores=7 [size:12 mw:1 d:4] a=566 d=4 fixed=414/259275 clauses=161'983)
> #Bound  31.47s best:172   next:[8,171]    bool_core (num_cores=8 [size:13 mw:1 d:4] a=554 d=4 fixed=414/259297 clauses=162'012)
> #29     32.41s best:171   next:[8,170]    ls_restart(batch:1 lin{mvs:2'614 evals:48'479} #w_updates:1'565 #perturb:0)
> #Bound  33.10s best:171   next:[9,170]    bool_core (num_cores=9 [size:13 mw:1 d:4] a=542 d=4 fixed=414/259320 clauses=162'044)
> #Model  33.18s var:258570/259139 constraints:171484/171778
> #Bound  34.83s best:171   next:[10,170]   bool_core (num_cores=10 [size:13 mw:1 d:4] a=530 d=4 fixed=569/259343 clauses=162'071)
> #30     35.85s best:170   next:[10,169]   graph_arc_lns (d=2.93e-01 s=86 t=0.10 p=0.00 stall=0 h=base)
> #31     36.07s best:169   next:[10,168]   quick_restart
> #Bound  36.75s best:169   next:[11,168]   bool_core (num_cores=11 [size:15 mw:1 d:4] a=516 d=4 fixed=569/259368 clauses=162'100)
> #Bound  38.39s best:169   next:[12,168]   bool_core (num_cores=12 [size:13 mw:1 d:4] a=504 d=4 fixed=569/259393 clauses=162'128)
> #32     39.18s best:168   next:[12,167]   quick_restart
> #33     40.18s best:167   next:[12,166]   graph_arc_lns (d=1.86e-01 s=117 t=0.10 p=0.00 stall=0 h=base)
> #Bound  40.22s best:167   next:[13,166]   bool_core (num_cores=13 [size:14 mw:1 d:4] a=491 d=4 fixed=569/259417 clauses=162'155)
> #Bound  41.72s best:167   next:[14,166]   bool_core (num_cores=14 [size:11 mw:1 d:4] a=481 d=4 fixed=569/259439 clauses=162'182)
> #34     43.11s best:165   next:[14,164]   graph_arc_lns (d=2.79e-01 s=132 t=0.10 p=0.33 stall=0 h=base)
> #Bound  43.77s best:165   next:[15,164]   bool_core (num_cores=15 [size:18 mw:1 d:5] a=464 d=5 fixed=569/259465 clauses=162'212)
> #Bound  45.32s best:165   next:[16,164]   bool_core (num_cores=16 [size:13 mw:1 d:4] a=452 d=5 fixed=569/259493 clauses=162'252)
> #Bound  46.61s best:165   next:[17,164]   bool_core (num_cores=17 [size:11 mw:1 d:4] a=442 d=5 fixed=569/259514 clauses=162'304)
> #Model  47.44s var:258259/259139 constraints:171323/171778
> #Bound  47.95s best:165   next:[18,164]   bool_core (num_cores=18 [size:12 mw:1 d:4] a=431 d=5 fixed=569/259534 clauses=162'334)
> #Bound  49.47s best:165   next:[19,164]   bool_core (num_cores=19 [size:14 mw:1 d:4] a=418 d=5 fixed=880/259557 clauses=162'368)
> #Bound  51.32s best:165   next:[20,164]   bool_core (num_cores=20 [size:17 mw:1 d:5] a=402 d=5 fixed=880/259585 clauses=162'409)
> #35     52.65s best:164   next:[20,163]   graph_var_lns (d=1.51e-01 s=240 t=0.10 p=0.20 stall=2 h=base)
> #Bound  52.72s best:164   next:[21,163]   bool_core (num_cores=21 [size:13 mw:1 d:4] a=390 d=5 fixed=880/259612 clauses=162'439)
> #36     53.31s best:163   next:[21,162]   graph_cst_lns (d=9.39e-01 s=227 t=0.10 p=1.00 stall=1 h=base) [combined with: graph_var_lns (d=1.5...]
> #Bound  54.03s best:163   next:[22,162]   bool_core (num_cores=22 [size:11 mw:1 d:4] a=380 d=5 fixed=880/259633 clauses=162'465)
> #Model  54.33s var:258156/259139 constraints:171270/171778
> #Bound  55.44s best:163   next:[23,162]   bool_core (num_cores=23 [size:11 mw:1 d:4] a=370 d=5 fixed=983/259652 clauses=162'513)
> #Model  56.04s var:258001/259139 constraints:171190/171778
> #Bound  56.56s best:163   next:[24,162]   bool_core (num_cores=24 [size:11 mw:1 d:4] a=360 d=5 fixed=983/259671 clauses=162'542)
> #Bound  57.91s best:163   next:[25,162]   bool_core (num_cores=25 [size:15 mw:1 d:4] a=346 d=5 fixed=1138/259694 clauses=162'570)
> #37     58.49s best:162   next:[25,161]   graph_var_lns (d=2.61e-01 s=282 t=0.10 p=0.44 stall=3 h=base)
> #Bound  59.28s best:162   next:[26,161]   bool_core (num_cores=26 [size:13 mw:1 d:4] a=334 d=5 fixed=1138/259719 clauses=162'602)
> #Bound  60.37s best:162   next:[27,161]   bool_core (num_cores=27 [size:11 mw:1 d:4] a=324 d=5 fixed=1138/259740 clauses=162'624)
> #38     60.38s best:161   next:[27,160]   quick_restart
> #Bound  61.48s best:161   next:[28,160]   bool_core (num_cores=28 [size:11 mw:1 d:4] a=314 d=5 fixed=1138/259759 clauses=162'644)
> #Bound  62.72s best:161   next:[29,160]   bool_core (num_cores=29 [size:12 mw:1 d:4] a=303 d=5 fixed=1138/259779 clauses=162'667)
> #Bound  63.96s best:161   next:[30,160]   bool_core (num_cores=30 [size:12 mw:1 d:4] a=292 d=5 fixed=1138/259800 clauses=162'691)
> #Bound  65.20s best:161   next:[31,160]   bool_core (num_cores=31 [size:12 mw:1 d:4] a=281 d=5 fixed=1138/259821 clauses=162'719)
> #Bound  66.61s best:161   next:[32,160]   bool_core (num_cores=32 [size:13 mw:1 d:4] a=269 d=5 fixed=1138/259843 clauses=162'754)
> #Bound  67.96s best:161   next:[33,160]   bool_core (num_cores=33 [size:13 mw:1 d:4] a=257 d=5 fixed=1138/259866 clauses=162'780)
> #39     68.75s best:160   next:[33,159]   graph_var_lns (d=1.97e-01 s=397 t=0.10 p=0.43 stall=4 h=base)
> #Model  70.69s var:257950/259139 constraints:171164/171778
> #40     72.87s best:159   next:[33,158]   rnd_cst_lns (d=9.76e-01 s=415 t=0.10 p=0.90 stall=9 h=base)
> #41     75.24s best:158   next:[33,157]   quick_restart
> #Bound  76.06s best:158   next:[34,157]   bool_core (num_cores=34 [size:15 mw:1 d:4] a=243 d=5 fixed=1189/259891 clauses=162'007)
> #Bound  77.99s best:158   next:[35,157]   bool_core (num_cores=35 [size:13 mw:1 d:4] a=231 d=5 fixed=1189/259916 clauses=162'053)
> #Bound  79.72s best:158   next:[36,157]   bool_core (num_cores=36 [size:13 mw:1 d:4] a=219 d=5 fixed=1189/259939 clauses=162'083)
> #Bound  81.53s best:158   next:[37,157]   bool_core (num_cores=37 [size:13 mw:1 d:4] a=207 d=5 fixed=1189/259962 clauses=162'109)
> #Bound  83.02s best:158   next:[38,157]   bool_core (num_cores=38 [size:11 mw:1 d:5] a=197 d=5 fixed=1189/259983 clauses=162'163)
> #Bound  84.52s best:158   next:[39,157]   bool_core (num_cores=39 [size:9 mw:1 d:5] a=189 d=5 fixed=1189/260005 clauses=162'200)
> #Bound  85.74s best:158   next:[40,157]   bool_core (num_cores=40 [size:6 mw:1 d:5] a=184 d=5 fixed=1189/260023 clauses=162'261)
> #Bound  86.98s best:158   next:[41,157]   bool_core (num_cores=41 [size:7 mw:1 d:5] a=178 d=5 fixed=1189/260039 clauses=162'333)
> #Bound  89.18s best:158   next:[42,157]   bool_core (num_cores=42 [size:12 mw:1 d:6] a=167 d=6 fixed=1189/260061 clauses=162'429)
> #Bound  90.51s best:158   next:[43,157]   bool_core (num_cores=43 [size:9 mw:1 d:5] a=159 d=6 fixed=1189/260088 clauses=162'491)
> #Bound  92.56s best:158   next:[44,157]   bool_core (num_cores=44 [size:11 mw:1 d:6] a=149 d=6 fixed=1189/260110 clauses=162'595)
> #Bound  93.53s best:158   next:[45,157]   bool_core (num_cores=45 [size:3 mw:1 d:6] a=147 d=6 fixed=1189/260130 clauses=162'718)
> #Model  94.53s var:257847/259139 constraints:171110/171778
> #Bound  95.75s best:158   next:[46,157]   bool_core (num_cores=46 [size:15 mw:1 d:6] a=133 d=6 fixed=1189/260159 clauses=162'803)
> #Bound  96.83s best:158   next:[47,157]   bool_core (num_cores=47 [size:6 mw:1 d:5] a=128 d=6 fixed=1292/260191 clauses=162'908)
> #Bound  98.71s best:158   next:[48,157]   bool_core (num_cores=48 [size:4 mw:1 d:6] a=125 d=6 fixed=1292/260203 clauses=163'063)
> #Bound 100.18s best:158   next:[49,157]   bool_core (num_cores=49 [size:8 mw:1 d:6] a=118 d=6 fixed=1292/260231 clauses=163'163)
> #Bound 101.74s best:158   next:[50,157]   bool_core (num_cores=50 [size:8 mw:1 d:5] a=111 d=6 fixed=1292/260252 clauses=163'249)
> #42    102.28s best:154   next:[50,153]   graph_arc_lns (d=1.77e-01 s=690 t=0.10 p=0.47 stall=32 h=base)
> #Bound 102.60s best:154   next:[51,153]   bool_core (num_cores=51 [size:2 mw:1 d:5] a=110 d=6 fixed=1292/260264 clauses=163'369)
> #Bound 103.66s best:154   next:[52,153]   bool_core (num_cores=52 [size:2 mw:1 d:6] a=109 d=6 fixed=1292/260275 clauses=163'553)
> #Bound 104.56s best:154   next:[53,153]   bool_core (num_cores=53 [size:2 mw:1 d:6] a=108 d=6 fixed=1292/260288 clauses=163'656)
> #Bound 107.97s best:154   next:[54,153]   bool_core (num_cores=54 [size:8 mw:1 d:6] a=101 d=6 fixed=1292/260309 clauses=164'012)
> #Bound 108.92s best:154   next:[55,153]   bool_core (num_cores=55 [size:2 mw:1 d:5] a=100 d=6 fixed=1292/260332 clauses=164'134)
> #Bound 109.79s best:154   next:[56,153]   bool_core (num_cores=56 [size:2 mw:1 d:5] a=99 d=6 fixed=1292/260343 clauses=164'276)
> #Bound 111.06s best:154   next:[57,153]   bool_core (num_cores=57 [size:2 mw:1 d:5] a=98 d=6 fixed=1292/260351 clauses=164'474)
> #43    112.92s best:153   next:[57,152]   rnd_cst_lns (d=9.71e-01 s=745 t=0.10 p=0.73 stall=4 h=base)
> #Bound 113.41s best:153   next:[58,152]   bool_core (num_cores=58 [size:3 mw:1 d:7] a=96 d=7 fixed=1292/260366 clauses=164'703)
> #44    115.43s best:151   next:[58,150]   graph_arc_lns (d=1.77e-01 s=784 t=0.10 p=0.47 stall=3 h=base)
> #45    115.59s best:150   next:[58,149]   graph_var_lns (d=1.44e-01 s=799 t=0.10 p=0.44 stall=17 h=stalling) [combined with: graph_arc_lns (d=1.7...]
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  42.49s,   42.49s]   42.49s   0.00ns   42.49s
>            'default_lp':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  57.20s,   57.20s]   57.20s   0.00ns   57.20s
>      'feasibility_pump':       415 [ 90.88us, 787.22ms]   2.20ms  38.58ms 912.48ms       407 [ 18.00ns,  18.00ns]  18.00ns   0.00ns   7.33us
>                    'fj':         1 [   1.06s,    1.06s]    1.06s   0.00ns    1.06s         1 [108.65ms, 108.65ms] 108.65ms   0.00ns 108.65ms
>                    'fj':         1 [947.68ms, 947.68ms] 947.68ms   0.00ns 947.68ms         1 [108.65ms, 108.65ms] 108.65ms   0.00ns 108.65ms
>             'fs_random':         1 [   2.45s,    2.45s]    2.45s   0.00ns    2.45s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   2.55s,    2.55s]    2.55s   0.00ns    2.55s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        48 [362.82ms,    3.33s] 925.44ms 580.97ms   44.42s        42 [ 10.00ns, 100.66ms]  55.14ms  49.59ms    2.32s
>         'graph_cst_lns':        15 [813.89ms,    7.26s]    3.13s    1.51s   46.88s        15 [ 10.00ns, 100.34ms]  33.02ms  43.10ms 495.26ms
>         'graph_dec_lns':        15 [   1.14s,    5.53s]    3.33s    1.35s   49.92s        15 [ 10.00ns, 100.23ms]  29.00ms  43.67ms 434.99ms
>         'graph_var_lns':        35 [394.22ms,    4.89s]    1.21s 852.54ms   42.19s        35 [ 12.33us, 100.77ms]  64.13ms  45.07ms    2.24s
>                    'ls':       135 [ 81.79ms, 815.53ms] 306.16ms 145.65ms   41.33s       135 [184.66us, 104.48ms]  98.07ms  12.32ms   13.24s
>                'ls_lin':       127 [159.51ms, 683.17ms] 323.66ms 137.02ms   41.10s       126 [ 60.44ms, 103.25ms]  99.49ms   4.79ms   12.54s
>            'max_lp_sym':         1 [   1.79m,    1.79m]    1.79m   0.00ns    1.79m         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  41.66s,   41.66s]   41.66s   0.00ns   41.66s
>          'pseudo_costs':         1 [   1.79m,    1.79m]    1.79m   0.00ns    1.79m         1 [   8.37s,    8.37s]    8.37s   0.00ns    8.37s
>         'quick_restart':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  45.52s,   45.52s]   45.52s   0.00ns   45.52s
>   'quick_restart_no_lp':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [  36.48s,   36.48s]   36.48s   0.00ns   36.48s
>         'reduced_costs':         1 [   1.78m,    1.78m]    1.78m   0.00ns    1.78m         1 [   6.86s,    6.86s]    6.86s   0.00ns    6.86s
>             'rins/rens':         3 [  17.31s,   19.18s]   18.02s 828.20ms   54.06s         3 [100.01ms, 100.02ms] 100.01ms   1.50us 300.04ms
>           'rnd_cst_lns':        19 [754.27ms,    3.54s]    2.54s 804.06ms   48.20s        19 [ 10.00ns, 100.16ms]  22.25ms  40.25ms 422.72ms
>           'rnd_var_lns':        20 [702.79ms,    4.51s]    2.68s 966.01ms   53.52s        18 [ 10.00ns, 100.19ms]  25.52ms  40.42ms 459.40ms
> 
> Search stats                Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  260'398      3'589   561'189     7'783  323'016'985        494'124
>            'default_lp':  259'139     74'882   174'702     6'186  201'202'487      6'175'824
>             'fs_random':  259'139          0     4'668     4'027    9'795'257          8'708
>       'fs_random_no_lp':  259'139          0     4'026     4'026    9'536'760          6'176
>            'max_lp_sym':  259'139          0     4'092     4'026    9'589'768      9'594'153
>                 'no_lp':  259'139     33'914   162'720     7'301  229'400'833      3'169'082
>          'pseudo_costs':  259'139        854    35'564     5'016   33'495'995     30'600'316
>         'quick_restart':  259'139      7'229   481'027     7'911  306'452'334      1'413'968
>   'quick_restart_no_lp':  259'139      6'243   483'372     6'726  256'752'056      1'198'558
>         'reduced_costs':  259'139        219    37'721     5'083   29'375'342     29'278'775
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         2'299      26'747     240'113             0         9     2'160      49'925         0        526       12'293        0
>            'default_lp':        36'280     152'474  17'010'431    13'894'381       287     2'121      48'599         0        524       12'153        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':        23'992     168'169   7'090'116     4'477'224       156     3'194      75'220         0        829       19'472        0
>          'pseudo_costs':           837      15'654     245'286             0         0       984      24'525         0        236        5'961        0
>         'quick_restart':         4'019      39'419   1'307'315             0        86     3'182      75'103         0        816       19'361        0
>   'quick_restart_no_lp':         3'577      36'624   1'117'119             0        68     2'104      47'964         0        523       11'838        0
>         'reduced_costs':           210       7'496      54'152             0         0     1'051      26'616         0        264        6'204        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          1           0          0   23'197        0        0
>       'fs_random':          1           0          0        4        0        0
>      'max_lp_sym':          1      79'359          0        0       73        0
>    'pseudo_costs':          1      26'340        221      407    2'266        0
>   'quick_restart':          1           0          0    1'333        0        0
>   'reduced_costs':          1      24'094        239      325    2'032        0
> 
> Lp dimension                  Final dimension of first component
>      'default_lp':                  0 rows, 2 columns, 0 entries
>       'fs_random':                  0 rows, 2 columns, 0 entries
>      'max_lp_sym':  608440 rows, 259010 columns, 1826678 entries
>    'pseudo_costs':     11383 rows, 259138 columns, 32873 entries
>   'quick_restart':                  0 rows, 2 columns, 0 entries
>   'reduced_costs':     14332 rows, 259138 columns, 42341 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow    Bad  BadScaling
>      'default_lp':          0            0       0         0      0           0
>       'fs_random':          0            0       0         0      0           0
>      'max_lp_sym':          0            0       0         0      0           0
>    'pseudo_costs':          0            0      87         0  5'905           0
>   'quick_restart':          0            0       0         0      0           0
>   'reduced_costs':          0            0   1'002         0  4'489           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':            1        0        0       0          0      0             0        0/0
>       'fs_random':            1        0        0       0          0      0             0        0/0
>      'max_lp_sym':      608'440        0        0     394          0      0             0        0/0
>    'pseudo_costs':      608'771       20    5'444     444      2'312      0             0  221/2'356
>   'quick_restart':            1        0        0       0          0      0             0        0/0
>   'reduced_costs':      608'776        8    7'125     457      3'993      0             0  239/2'279
> 
> Lp Cut           reduced_costs  pseudo_costs
>          CG_FF:             36            58
>           CG_R:             10            10
>         Clique:             81            98
>      MIR_1_RLT:              4             9
>       MIR_3_FF:             13            15
>       MIR_4_FF:              -             3
>       MIR_5_FF:              1             -
>   ZERO_HALF_FF:             83            28
>    ZERO_HALF_R:             11             -
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          6/42     45%    1.33e-01       0.10
>   'graph_cst_lns':          4/15     73%    9.59e-01       0.10
>   'graph_dec_lns':          0/15     73%    9.72e-01       0.10
>   'graph_var_lns':          6/35     46%    1.69e-01       0.10
>       'rins/rens':           3/3      0%    1.24e-01       0.10
>     'rnd_cst_lns':          3/19     79%    9.87e-01       0.10
>     'rnd_var_lns':          1/18     78%    9.85e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1    31'270         0              0          0             11        210'165
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0    15'380         11'837      1'767              0        565'206
>                          'ls_lin_restart':       13                 13   430'384         0              0          0         24'069      1'458'114
>                 'ls_lin_restart_compound':       15                 14         0    28'155             78     14'037             46      7'925'385
>         'ls_lin_restart_compound_perturb':       18                 17         0    33'459            110     16'672             60      9'547'698
>                    'ls_lin_restart_decay':       20                 18   624'580         0              0          0          1'856      4'082'841
>           'ls_lin_restart_decay_compound':       17                 17         0    32'376            234     16'069             79      8'758'275
>   'ls_lin_restart_decay_compound_perturb':       16                 15         0    29'811            200     14'805             71      8'273'815
>            'ls_lin_restart_decay_perturb':       18                 18   554'775         0              0          0          1'933      3'631'455
>                  'ls_lin_restart_perturb':       10                 10   268'448         0              0          0         12'540      1'041'275
>                              'ls_restart':       23                 20   656'643         0              0          0         29'128      2'509'967
>                     'ls_restart_compound':       10                  9         0    18'743             46      9'348             30      5'288'266
>             'ls_restart_compound_perturb':       20                 20         0    37'480            114     18'681             70     10'599'345
>                        'ls_restart_decay':       24                 22   736'649         0              0          0          2'334      4'600'369
>               'ls_restart_decay_compound':       11                 11         0    20'986            128     10'426             51      5'803'843
>       'ls_restart_decay_compound_perturb':       15                 15         0    27'880            169     13'854             62      7'729'479
>                'ls_restart_decay_perturb':       11                 11   337'800         0              0          0          1'160      2'223'430
>                      'ls_restart_perturb':       21                 19   645'416         0              0          0         26'189      2'408'546
> 
> Solutions (45)            Num     Rank
>            'default_lp':   20   [2,26]
>             'fs_random':    1    [1,1]
>         'graph_arc_lns':    5  [30,44]
>         'graph_cst_lns':    2   [6,36]
>         'graph_var_lns':    5   [5,45]
>            'ls_restart':    1  [29,29]
>      'ls_restart_decay':    1    [7,7]
>         'quick_restart':    5   [4,41]
>   'quick_restart_no_lp':    3   [3,28]
>           'rnd_cst_lns':    2  [40,43]
> 
> Objective bounds     Num
>        'bool_core':   58
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    122      556       96
>    'fj solution hints':      0        0        0
>         'lp solutions':     38        0       38
>                 'pump':    414        3
> 
> Improving bounds shared    Num  Sym
>             'default_lp':  569    0
>                  'no_lp':   51    0
>          'quick_restart':  517    0
>    'quick_restart_no_lp':  155    0
> 
> Clauses shared                Num
>                  'core':  164'019
>            'default_lp':  158'567
>                 'no_lp':      101
>          'pseudo_costs':      758
>         'quick_restart':      637
>   'quick_restart_no_lp':      117
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 150
> best_bound: 58
> integers: 670
> booleans: 259139
> conflicts: 0
> branches: 4668
> propagations: 9795257
> integer_propagations: 8708
> restarts: 4027
> lp_iterations: 0
> walltime: 120.649
> usertime: 120.649
> deterministic_time: 277.684
> gap_integral: 1236.98
> solution_fingerprint: 0x90d0f973479e7ff8
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
> Initial optimization model '': (model_fingerprint: 0x1e463cfd1133f60b)
> #Variables: 150 (#bools: 50 in objective) (100 primary variables)
>   - 50 Booleans in [0,1]
>   - 50 in [0,4]
>   - 50 in [0,5]
> #kAutomaton: 10
> #kLinear1: 100 (#enforced: 50)
> #kLinear2: 50 (#enforced: 50)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   3.45e-05s  0.00e+00d  [DetectDominanceRelations] 
>   2.34e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.14e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   2.95e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   9.15e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=4'356 
> [Symmetry] Graph for symmetry has 18'875 nodes and 48'407 arcs.
> [Symmetry] Symmetry computation done. time: 0.00367967 dtime: 0.0071468
> [Symmetry] #generators: 28, average support size: 2
> [Symmetry] The model contains 10 duplicate constraints !
> [Symmetry] 8 orbits on 36 variables with sizes: 10,8,6,4,2,2,2,2
> [Symmetry] Found orbitope of size 1 x 6
> [SAT presolve] num removable Booleans: 314 / 4917
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:13732 literals:34028 vars:4879 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000842069s] clauses:13722 literals:33998 vars:4879 one_side_vars:0 simple_definition:10 singleton_clauses:0
> [SAT presolve] [0.00123581s] clauses:13624 literals:33998 vars:4830 one_side_vars:0 simple_definition:10 singleton_clauses:0
>   2.73e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.03e-02s  3.40e-01d  [Probe] #probed=9'836 #fixed_bools=9 #equiv=55 #new_binary_clauses=9'891 
>   2.72e-02s  1.02e-01d  [MaxClique] Merged 9'898(19'796 literals) into 3'397(13'085 literals) at_most_ones. 
>   1.17e-03s  0.00e+00d  [DetectDominanceRelations] 
>   5.78e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   6.71e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.49e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=100 
>   1.90e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.39e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   6.47e-05s  0.00e+00d  [DetectDifferentVariables] 
>   2.82e-03s  1.35e-04d  [ProcessSetPPC] #relevant_constraints=7'460 #num_inclusions=3'386 
>   8.87e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.93e-04s  9.95e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.48e-04s  9.21e-05d  [FindBigVerticalLinearOverlap] 
>   6.23e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.12e-04s  4.16e-06d  [MergeClauses] #num_collisions=147 #num_merges=147 #num_saved_literals=343 
>   7.51e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.58e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.35e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.42e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.85e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.27e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 9'864 nodes and 18'939 arcs.
> [Symmetry] Symmetry computation done. time: 0.001756 dtime: 0.00369537
> [Symmetry] #generators: 9, average support size: 8
> [Symmetry] 28 orbits on 64 variables with sizes: 4,4,4,4,2,2,2,2,2,2,...
> [Symmetry] Found orbitope of size 4 x 4
> [SAT presolve] num removable Booleans: 0 / 4747
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:245 literals:833 vars:234 one_side_vars:0 simple_definition:223 singleton_clauses:0
> [SAT presolve] [2.4847e-05s] clauses:245 literals:833 vars:234 one_side_vars:0 simple_definition:223 singleton_clauses:0
> [SAT presolve] [9.986e-05s] clauses:245 literals:833 vars:234 one_side_vars:0 simple_definition:223 singleton_clauses:0
>   1.63e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.59e-02s  3.55e-01d  [Probe] #probed=9'705 #fixed_bools=66 #equiv=211 #new_binary_clauses=9'623 
>   1.26e-04s  1.00e-04d  [MaxClique] 
>   7.46e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.71e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.99e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.64e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=154 
>   1.22e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.43e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.62e-05s  0.00e+00d  [DetectDifferentVariables] 
>   1.17e-03s  5.40e-05d  [ProcessSetPPC] #relevant_constraints=3'884 
>   7.69e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.57e-04s  9.26e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.44e-04s  8.83e-05d  [FindBigVerticalLinearOverlap] 
>   5.45e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.14e-04s  4.16e-06d  [MergeClauses] #num_collisions=147 #num_merges=147 #num_saved_literals=343 
>   7.42e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.37e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.25e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.36e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.83e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.26e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 9'644 nodes and 18'168 arcs.
> [Symmetry] Symmetry computation done. time: 0.00162702 dtime: 0.00349715
> [SAT presolve] num removable Booleans: 0 / 4470
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:255 literals:853 vars:247 one_side_vars:13 simple_definition:223 singleton_clauses:0
> [SAT presolve] [2.5078e-05s] clauses:255 literals:853 vars:247 one_side_vars:13 simple_definition:223 singleton_clauses:0
> [SAT presolve] [0.000101483s] clauses:255 literals:853 vars:247 one_side_vars:13 simple_definition:223 singleton_clauses:0
>   1.62e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.36e-02s  3.09e-01d  [Probe] #probed=9'704 #equiv=22 #new_binary_clauses=9'260 
>   1.28e-04s  9.99e-05d  [MaxClique] 
>   7.58e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.51e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.90e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.45e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=27 
>   1.19e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.94e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.65e-05s  0.00e+00d  [DetectDifferentVariables] 
>   1.15e-03s  5.37e-05d  [ProcessSetPPC] #relevant_constraints=3'857 
>   7.73e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.53e-04s  9.30e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.43e-04s  8.78e-05d  [FindBigVerticalLinearOverlap] 
>   5.54e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.11e-04s  4.16e-06d  [MergeClauses] #num_collisions=147 #num_merges=147 #num_saved_literals=343 
>   7.43e-04s  0.00e+00d  [DetectDominanceRelations] 
>   2.39e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.89e-03s  0.00e+00d  [ExpandObjective] #entries=90'696 #tight_variables=16'647 #tight_constraints=3'602 #expands=79 
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
>   - rule 'linear1: x in domain' was applied 50 times.
>   - rule 'linear: always true' was applied 90 times.
>   - rule 'linear: enforcement literal in expression' was applied 90 times.
>   - rule 'linear: fixed or dup variables' was applied 90 times.
>   - rule 'linear: remapped using affine relations' was applied 590 times.
>   - rule 'new_bool: automaton expansion' was applied 4'867 times.
>   - rule 'objective: expanded via tight equality' was applied 79 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 73 times.
>   - rule 'presolve: 125 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'probing: bool_or reduced to implication' was applied 1 time.
>   - rule 'probing: simplified clauses.' was applied 11 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 3'376 times.
>   - rule 'setppc: removed dominated constraints' was applied 10 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 50 times.
>   - rule 'variables: detect half reified value encoding' was applied 100 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xde32f698e4580dc3)
> #Variables: 4'448 (#bools: 79 in objective) (1'812 primary variables)
>   - 4'448 Booleans in [0,1]
> #kBoolAnd: 105 (#enforced: 105 #multi: 98) (#literals: 507)
> #kExactlyOne: 3'602 (#literals: 16'647)
> [Symmetry] Graph for symmetry has 9'045 nodes and 18'054 arcs.
> [Symmetry] Symmetry computation done. time: 0.00156379 dtime: 0.00328918
> 
> Preloading model.
> #Bound   0.38s best:inf   next:[0,50]     initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model   0.38s var:4448/4448 constraints:3707/3707
> 
> Starting search at 0.38s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.55s best:50    next:[0,49]     quick_restart_no_lp [hint]
> #2       0.55s best:40    next:[0,39]     quick_restart_no_lp
> #3       0.55s best:38    next:[0,37]     core
> #4       0.60s best:37    next:[0,36]     quick_restart [hint]
> #5       0.61s best:36    next:[0,35]     default_lp [hint]
> #6       0.61s best:34    next:[0,33]     default_lp
> #7       0.65s best:32    next:[0,31]     graph_var_lns (d=7.07e-01 s=27 t=0.10 p=1.00 stall=1 h=base)
> #Bound   0.80s best:32    next:[1,31]     reduced_costs
> #Bound   0.82s best:32    next:[2,31]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=74 d=2 fixed=0/4453 clauses=3'180)
> #Bound   0.82s best:32    next:[3,31]     bool_core (num_cores=3 [size:4 mw:1 d:2] a=71 d=2 fixed=0/4458 clauses=3'187)
> #Bound   0.82s best:32    next:[4,31]     bool_core (num_cores=4 [size:3 mw:1 d:2] a=69 d=2 fixed=0/4462 clauses=3'192)
> #Bound   0.83s best:32    next:[5,31]     bool_core (num_cores=5 [size:3 mw:1 d:2] a=67 d=2 fixed=0/4465 clauses=3'200)
> #Bound   0.83s best:32    next:[6,31]     bool_core (num_cores=6 [size:3 mw:1 d:2] a=65 d=2 fixed=0/4468 clauses=3'205)
> #Bound   0.83s best:32    next:[7,31]     bool_core (num_cores=7 [size:5 mw:1 d:3] a=61 d=3 fixed=0/4473 clauses=3'213)
> #Bound   0.83s best:32    next:[8,31]     bool_core (num_cores=8 [size:3 mw:1 d:2] a=59 d=3 fixed=0/4478 clauses=3'219)
> #8       0.84s best:31    next:[8,30]     quick_restart_no_lp
> #Bound   0.84s best:31    next:[9,30]     bool_core (num_cores=9 [size:4 mw:1 d:2] a=56 d=3 fixed=0/4482 clauses=3'227)
> #Bound   0.84s best:31    next:[10,30]    bool_core (num_cores=10 [size:4 mw:1 d:3] a=53 d=3 fixed=0/4487 clauses=3'234)
> #Bound   0.85s best:31    next:[11,30]    bool_core (num_cores=11 [size:4 mw:1 d:2] a=50 d=3 fixed=0/4493 clauses=3'243)
> #Bound   0.85s best:31    next:[12,30]    bool_core (num_cores=12 [size:2 mw:1 d:3] a=49 d=3 fixed=0/4496 clauses=3'248)
> #Bound   0.85s best:31    next:[13,30]    bool_core (num_cores=13 [size:2 mw:1 d:3] a=48 d=3 fixed=0/4498 clauses=3'254)
> #Bound   0.85s best:31    next:[14,30]    bool_core (num_cores=14 [size:3 mw:1 d:4] a=46 d=4 fixed=0/4501 clauses=3'270)
> #Bound   0.86s best:31    next:[15,30]    bool_core (num_cores=15 [size:6 mw:1 amo:1 lit:3 d:5] a=41 d=5 fixed=0/4508 clauses=3'303)
> #Bound   0.87s best:31    next:[16,30]    bool_core (num_cores=16 [size:4 mw:1 amo:1 lit:2 d:4] a=38 d=5 fixed=0/4518 clauses=3'326)
> #9       0.87s best:30    next:[16,29]    quick_restart_no_lp
> #Bound   0.87s best:30    next:[17,29]    bool_core (num_cores=17 [size:5 mw:1 amo:1 lit:2 d:5] a=35 d=5 fixed=0/4525 clauses=3'358)
> #Bound   0.88s best:30    next:[18,29]    bool_core (num_cores=18 [size:4 mw:1 amo:1 lit:2 d:6] a=32 d=6 fixed=0/4535 clauses=3'419)
> #Bound   0.88s best:30    next:[19,29]    bool_core (num_cores=19 [size:2 mw:1 d:3] a=31 d=6 fixed=0/4543 clauses=3'442)
> #Bound   0.89s best:30    next:[20,29]    bool_core (num_cores=20 [size:2 mw:1 d:6] a=30 d=6 fixed=0/4546 clauses=3'466)
> #Bound   1.00s best:30    next:[28,29]    max_lp [skipped_logs=4]
> #10      1.29s best:29    next:[28,28]    graph_var_lns (d=8.82e-01 s=83 t=0.10 p=0.71 stall=2 h=base)
> #Done    1.94s quick_restart_no_lp
> #Done    1.94s quick_restart
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         1 [   2.42s,    2.42s]    2.42s   0.00ns    2.42s
>            'default_lp':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         1 [   1.74s,    1.74s]    1.74s   0.00ns    1.74s
>      'feasibility_pump':        12 [ 30.22us,  27.52ms]   2.34ms   7.59ms  28.02ms        11 [558.00ns, 558.00ns] 558.00ns   0.00ns   6.14us
>                    'fj':         2 [ 97.05ms, 122.06ms] 109.55ms  12.51ms 219.11ms         2 [100.17ms, 100.18ms] 100.18ms   2.28us 200.35ms
>                    'fj':         2 [ 98.11ms, 126.37ms] 112.24ms  14.13ms 224.48ms         2 [100.17ms, 100.17ms] 100.17ms 742.50ns 200.35ms
>             'fs_random':         1 [164.66ms, 164.66ms] 164.66ms   0.00ns 164.66ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [179.44ms, 179.44ms] 179.44ms   0.00ns 179.44ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        12 [  8.48ms, 106.41ms]  49.78ms  36.31ms 597.31ms        12 [ 10.00ns, 100.03ms]  37.27ms  44.87ms 447.27ms
>         'graph_cst_lns':        12 [  8.22ms,  96.32ms]  36.80ms  27.38ms 441.55ms        12 [ 10.00ns, 100.12ms]  20.99ms  32.69ms 251.85ms
>         'graph_dec_lns':        12 [ 14.09ms,  48.79ms]  25.53ms  11.46ms 306.40ms        12 [ 10.00ns,   2.81ms] 387.83us 809.96us   4.65ms
>         'graph_var_lns':        12 [ 16.81ms,  97.09ms]  54.15ms  35.10ms 649.86ms        12 [ 10.00ns, 100.13ms]  45.47ms  46.67ms 545.59ms
>                    'ls':        11 [  6.29ms, 127.59ms] 102.40ms  32.52ms    1.13s        11 [  3.81ms, 100.01ms]  91.26ms  27.65ms    1.00s
>                'ls_lin':        11 [ 96.76ms, 126.89ms] 109.90ms  11.17ms    1.21s        11 [100.00ms, 100.04ms] 100.01ms  12.11us    1.10s
>                'max_lp':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         1 [   2.05s,    2.05s]    2.05s   0.00ns    2.05s
>          'pseudo_costs':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         1 [679.18ms, 679.18ms] 679.18ms   0.00ns 679.18ms
>         'quick_restart':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         1 [   1.69s,    1.69s]    1.69s   0.00ns    1.69s
>   'quick_restart_no_lp':         1 [   1.55s,    1.55s]    1.55s   0.00ns    1.55s         1 [   2.01s,    2.01s]    2.01s   0.00ns    2.01s
>         'reduced_costs':         1 [   1.56s,    1.56s]    1.56s   0.00ns    1.56s         1 [707.21ms, 707.21ms] 707.21ms   0.00ns 707.21ms
>             'rins/rens':        11 [  6.46ms,  98.32ms]  33.52ms  34.15ms 368.76ms         5 [ 10.80ms, 100.10ms]  47.31ms  43.08ms 236.55ms
>           'rnd_cst_lns':        12 [  9.25ms, 154.66ms]  35.92ms  44.09ms 431.06ms        12 [ 10.00ns,  11.14ms]   1.02ms   3.06ms  12.29ms
>           'rnd_var_lns':        12 [  8.67ms,  67.83ms]  22.51ms  16.13ms 270.13ms        12 [ 10.00ns,  39.72ms]   4.57ms  11.35ms  54.85ms
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  4'618      9'268    58'221    18'315  18'028'277        125'338
>            'default_lp':  4'448      8'703    51'218    18'013  11'258'115        302'863
>             'fs_random':  4'448          0     8'896     8'896   2'637'210         31'173
>       'fs_random_no_lp':  4'448          0     8'896     8'896   2'637'210         31'173
>                'max_lp':  4'448          0     8'896     8'896   2'637'875      2'646'891
>                 'no_lp':  4'448     12'768    56'083    18'145  12'838'687        336'885
>          'pseudo_costs':  4'448         51    40'816    17'983   6'783'122      6'819'177
>         'quick_restart':  4'448      5'111    62'199    18'488  11'423'917        240'030
>   'quick_restart_no_lp':  4'448      6'742    69'397    18'735  12'725'780        244'482
>         'reduced_costs':  4'448         60    40'870    17'958   6'808'316      6'840'302
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         7'810     128'903     213'358             0        26     7'229      22'997         0        673        4'447    1'737
>            'default_lp':         7'753     161'536     528'950             0         3     7'210      23'075         0        708        4'503    1'672
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':        10'939     169'394     666'007       269'132         8     7'260      23'262         0        664        4'285    1'646
>          'pseudo_costs':            36         777       2'614             0         0     7'229      23'043         0        684        4'425    1'685
>         'quick_restart':         3'939      47'695     250'367             0        14     7'221      22'993         0        682        4'442    1'650
>   'quick_restart_no_lp':         5'213      66'431     334'762             0        11     7'217      23'079         0        689        4'431    1'598
>         'reduced_costs':            46         473       3'103             0         0     7'232      23'059         0        669        4'311    1'711
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         14           0          0   17'517        0        0
>       'fs_random':         14           0          0        0        0        0
>          'max_lp':          1       4'595        141        4        3        0
>    'pseudo_costs':          1       2'881        547       22      118        0
>   'quick_restart':         14           0          0    9'719        0        0
>   'reduced_costs':          1       3'504      1'054       27      163        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':            0 rows, 2 columns, 0 entries
>       'fs_random':            0 rows, 2 columns, 0 entries
>          'max_lp':  3524 rows, 4448 columns, 16408 entries
>    'pseudo_costs':   1422 rows, 4448 columns, 8594 entries
>   'quick_restart':            0 rows, 2 columns, 0 entries
>   'reduced_costs':   1609 rows, 4448 columns, 9195 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0       7         0  54'359           0
>    'pseudo_costs':          0            0      85         0   9'730           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0      58         0   9'893           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':           16        0        0       0          0      0             0          0/0
>       'fs_random':           16        0        0       0          0      0             0          0/0
>          'max_lp':        3'851      163    1'156       0      1'156      0             0      141/271
>    'pseudo_costs':        4'257        0        0       0          0      0             0    547/1'140
>   'quick_restart':           16        0        3       0          2      0             0          0/0
>   'reduced_costs':        4'764        0        0       0          0      0             0  1'054/2'106
> 
> Lp Cut           max_lp  reduced_costs  pseudo_costs
>          CG_FF:      22             54            71
>           CG_K:       -             14             4
>           CG_R:       -             22             9
>         Clique:      30             58            43
>      MIR_1_RLT:       -            123           162
>       MIR_4_FF:       -              -             2
>       MIR_5_FF:       -              3             -
>       MIR_6_FF:       1              2             -
>   ZERO_HALF_FF:      64            479           104
>    ZERO_HALF_R:      24            299           152
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          1/12     67%    9.12e-01       0.10
>   'graph_cst_lns':          0/12     83%    9.77e-01       0.10
>   'graph_dec_lns':          0/12    100%    9.91e-01       0.10
>   'graph_var_lns':          3/12     58%    8.39e-01       0.10
>       'rins/rens':          6/11     73%    9.24e-01       0.10
>     'rnd_cst_lns':          1/12     92%    9.86e-01       0.10
>     'rnd_var_lns':          0/12    100%    9.91e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1    73'630         0              0          0          6'741          4'448
>                        'fj_restart_decay':        1                  1    84'453         0              0          0            576          8'896
>   'fj_restart_decay_compound_perturb_obj':        2                  2         0    96'307         32'390     31'956             51      1'048'520
>                          'ls_lin_restart':        1                  1    74'272         0              0          0          5'479          4'448
>         'ls_lin_restart_compound_perturb':        2                  2         0    57'621          4'709     26'455            413      1'066'775
>                    'ls_lin_restart_decay':        2                  2   167'051         0              0          0          1'187         17'792
>           'ls_lin_restart_decay_compound':        1                  1         0    35'369         11'057     12'151             48        509'059
>   'ls_lin_restart_decay_compound_perturb':        1                  1         0    35'753         10'065     12'836             51        510'240
>            'ls_lin_restart_decay_perturb':        1                  1    83'456         0              0          0            575          8'896
>                  'ls_lin_restart_perturb':        3                  3   225'516         0              0          0         14'997         13'344
>                              'ls_restart':        2                  2    77'326         0              0          0          4'668          7'848
>                     'ls_restart_compound':        1                  1         0    31'238          3'082     14'076            191        532'302
>             'ls_restart_compound_perturb':        1                  1         0    27'978          2'687     12'645            171        535'712
>                        'ls_restart_decay':        2                  2   167'050         0              0          0          1'200         17'792
>               'ls_restart_decay_compound':        3                  3         0   111'788         32'975     39'396            148      1'537'428
>                      'ls_restart_perturb':        2                  2   148'136         0              0          0         13'116          8'896
> 
> Solutions (10)            Num    Rank
>                  'core':    1   [3,3]
>            'default_lp':    2   [5,6]
>         'graph_var_lns':    2  [7,10]
>         'quick_restart':    1   [4,4]
>   'quick_restart_no_lp':    4   [1,9]
> 
> Objective bounds     Num
>        'bool_core':   23
>   'initial_domain':    1
>           'max_lp':    1
>    'reduced_costs':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     24      191       22
>    'fj solution hints':      0        0        0
>         'lp solutions':      1        0        1
>                 'pump':     11       11
> 
> Improving bounds shared    Num  Sym
>                 'max_lp':  665    0
>          'quick_restart':    1    0
>    'quick_restart_no_lp':    1    0
> 
> Clauses shared            Num
>                  'core':  314
>          'pseudo_costs':  114
>         'quick_restart':  344
>   'quick_restart_no_lp':  733
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 29
> best_bound: 29
> integers: 94
> booleans: 4448
> conflicts: 0
> branches: 8896
> propagations: 2637210
> integer_propagations: 31173
> restarts: 8896
> lp_iterations: 0
> walltime: 1.95329
> usertime: 1.95329
> deterministic_time: 16.4686
> gap_integral: 4.98006
> solution_fingerprint: 0x1aa28a1f5dc77a22
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
> Initial optimization model '': (model_fingerprint: 0xdf29b4cfa3f90377)
> #Variables: 150 (#bools: 50 in objective) (100 primary variables)
>   - 50 Booleans in [0,1]
>   - 50 in [0,4]
>   - 50 in [0,5]
> #kAutomaton: 50
> #kLinear1: 100 (#enforced: 50)
> #kLinear2: 50 (#enforced: 50)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   7.26e-05s  0.00e+00d  [DetectDominanceRelations] 
>   9.60e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.12e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.61e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   5.91e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=21'474 
> [Symmetry] Graph for symmetry has 91'458 nodes and 236'551 arcs.
> [Symmetry] Symmetry computation done. time: 0.0200392 dtime: 0.0389288
> [Symmetry] #generators: 244, average support size: 2
> [Symmetry] The model contains 50 duplicate constraints !
> [Symmetry] 9 orbits on 253 variables with sizes: 50,40,38,33,28,25,21,11,7
> [Symmetry] Found orbitope of size 1 x 38
> [SAT presolve] num removable Booleans: 1499 / 23946
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:67090 literals:166366 vars:23692 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00422307s] clauses:67040 literals:166216 vars:23692 one_side_vars:0 simple_definition:50 singleton_clauses:0
> [SAT presolve] [0.00621727s] clauses:66442 literals:166216 vars:23393 one_side_vars:0 simple_definition:50 singleton_clauses:0
>   1.53e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.02e-01s  1.00e+00d *[Probe] #probed=8'660 #fixed_bools=68 #equiv=63 #new_binary_clauses=19'487 
>   2.44e-01s  1.00e+00d *[MaxClique] Merged 48'118(96'236 literals) into 27'986(75'864 literals) at_most_ones. 
>   6.66e-03s  0.00e+00d  [DetectDominanceRelations] 
>   3.48e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   6.24e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.26e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=104 
>   1.76e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.54e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   7.42e-04s  0.00e+00d  [DetectDifferentVariables] 
>   1.90e-02s  7.67e-04d  [ProcessSetPPC] #relevant_constraints=48'256 #num_inclusions=27'874 
>   1.46e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.77e-03s  5.01e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   1.26e-03s  6.71e-04d  [FindBigVerticalLinearOverlap] 
>   1.01e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   3.09e-03s  1.83e-04d  [MergeClauses] #num_collisions=1'170 #num_merges=1'170 #num_saved_literals=2'639 
>   6.18e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.84e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.08e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.74e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.88e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.61e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 82'297 nodes and 170'477 arcs.
> [Symmetry] Symmetry computation done. time: 0.0178802 dtime: 0.0328232
> [Symmetry] #generators: 8, average support size: 8
> [Symmetry] 28 orbits on 60 variables with sizes: 3,3,3,3,2,2,2,2,2,2,...
> [Symmetry] Found orbitope of size 4 x 2
> [SAT presolve] num removable Booleans: 971 / 23163
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:32982 literals:79188 vars:19363 one_side_vars:0 simple_definition:12017 singleton_clauses:0
> [SAT presolve] [0.00184564s] clauses:32982 literals:79188 vars:19363 one_side_vars:0 simple_definition:12017 singleton_clauses:0
> [SAT presolve] [0.00322851s] clauses:32982 literals:79188 vars:19363 one_side_vars:0 simple_definition:12017 singleton_clauses:0
>   1.96e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.10e-01s  1.00e+00d *[Probe] #probed=7'802 #fixed_bools=111 #equiv=225 #new_binary_clauses=19'982 
>   1.51e-01s  6.08e-01d  [MaxClique] Merged 21'359(42'718 literals) into 10'072(31'119 literals) at_most_ones. 
>   6.05e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.95e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.90e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.92e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=264 
>   1.66e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.18e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   9.18e-04s  0.00e+00d  [DetectDifferentVariables] 
>   1.35e-02s  4.63e-04d  [ProcessSetPPC] #relevant_constraints=30'078 #num_inclusions=9'974 
>   1.58e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.12e-03s  4.77e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   9.91e-04s  4.52e-04d  [FindBigVerticalLinearOverlap] 
>   1.33e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.03e-03s  2.61e-05d  [MergeClauses] #num_collisions=897 #num_merges=897 #num_saved_literals=2'093 
>   5.03e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.69e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.18e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.61e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.33e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.60e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 47'840 nodes and 92'856 arcs.
> [Symmetry] Symmetry computation done. time: 0.0108407 dtime: 0.0200972
> [Symmetry] #generators: 63, average support size: 8
> [Symmetry] 56 orbits on 308 variables with sizes: 14,14,14,14,9,9,9,9,8,8,...
> [Symmetry] Found orbitope of size 4 x 6
> [SAT presolve] num removable Booleans: 0 / 22827
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1593 literals:5327 vars:1594 one_side_vars:148 simple_definition:1397 singleton_clauses:0
> [SAT presolve] [0.000152199s] clauses:1593 literals:5327 vars:1594 one_side_vars:148 simple_definition:1397 singleton_clauses:0
> [SAT presolve] [0.000602514s] clauses:1593 literals:5327 vars:1594 one_side_vars:148 simple_definition:1397 singleton_clauses:0
>   2.09e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.13e-01s  1.00e+00d *[Probe] #probed=8'486 #fixed_bools=19 #equiv=50 #new_binary_clauses=20'880 
>   3.74e-03s  8.42e-03d  [MaxClique] 
>   5.34e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.72e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.97e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.68e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=52 
>   1.51e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.17e-03s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   8.86e-04s  0.00e+00d  [DetectDifferentVariables] 
>   9.22e-03s  2.77e-04d  [ProcessSetPPC] #relevant_constraints=20'042 
>   1.16e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.53e-03s  4.74e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   1.33e-03s  4.50e-04d  [FindBigVerticalLinearOverlap] 
>   1.12e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.19e-03s  2.61e-05d  [MergeClauses] #num_collisions=897 #num_merges=897 #num_saved_literals=2'093 
>   5.27e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.64e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.59e-02s  0.00e+00d  [ExpandObjective] #entries=462'296 #tight_variables=84'572 #tight_constraints=18'401 #expands=80 
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
>   - rule 'linear1: x in domain' was applied 50 times.
>   - rule 'linear: always true' was applied 90 times.
>   - rule 'linear: enforcement literal in expression' was applied 90 times.
>   - rule 'linear: fixed or dup variables' was applied 90 times.
>   - rule 'linear: remapped using affine relations' was applied 2'590 times.
>   - rule 'new_bool: automaton expansion' was applied 23'896 times.
>   - rule 'objective: expanded via tight equality' was applied 80 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 71 times.
>   - rule 'presolve: 248 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'probing: bool_or reduced to implication' was applied 9 times.
>   - rule 'probing: simplified clauses.' was applied 70 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 16'487 times.
>   - rule 'setppc: removed dominated constraints' was applied 51 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 50 times.
>   - rule 'variables: detect half reified value encoding' was applied 100 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xc4418936e46755c5)
> #Variables: 22'758 (#bools: 98 in objective) (9'232 primary variables)
>   - 22'758 Booleans in [0,1]
> #kAtMostOne: 48 (#literals: 144)
> #kBoolAnd: 607 (#enforced: 607 #multi: 598) (#literals: 3'049)
> #kBoolOr: 48 (#literals: 144)
> #kExactlyOne: 18'401 (#literals: 84'572)
> [Symmetry] Graph for symmetry has 46'483 nodes and 92'580 arcs.
> [Symmetry] Symmetry computation done. time: 0.00977966 dtime: 0.0195655
> [Symmetry] #generators: 61, average support size: 8
> [Symmetry] 56 orbits on 300 variables with sizes: 14,14,14,14,8,8,8,8,8,8,...
> [Symmetry] Found orbitope of size 4 x 6
> 
> Preloading model.
> #Bound   1.94s best:inf   next:[0,50]     initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model   1.95s var:22758/22758 constraints:19104/19104
> 
> Starting search at 1.95s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       3.07s best:38    next:[0,37]     core
> #Model   3.08s var:22728/22758 constraints:19089/19104
> #2       3.47s best:36    next:[0,35]     default_lp
> #Model   3.56s var:22709/22758 constraints:19080/19104
> #Model   3.75s var:22568/22758 constraints:19014/19104
> #Model   3.85s var:22553/22758 constraints:19007/19104
> #Model   3.94s var:22521/22758 constraints:18990/19104
> #Model   3.96s var:22511/22758 constraints:18985/19104
> #Model   4.06s var:22491/22758 constraints:18975/19104
> #Model   4.08s var:22445/22758 constraints:18951/19104
> #Model   4.20s var:22415/22758 constraints:18936/19104
> #Model   4.37s var:22340/22758 constraints:18901/19104
> #Model   4.61s var:22095/22758 constraints:18786/19104
> #Model   4.72s var:21975/22758 constraints:18727/19104
> #Model   4.84s var:21965/22758 constraints:18722/19104
> #Model   4.97s var:21935/22758 constraints:18707/19104
> #Model   5.02s var:21925/22758 constraints:18702/19104
> #Model   5.20s var:21916/22758 constraints:18698/19104
> #Model   5.49s var:21906/22758 constraints:18693/19104
> #Model   5.55s var:21875/22758 constraints:18678/19104
> #Model   5.68s var:21853/22758 constraints:18668/19104
> #Model   5.81s var:21822/22758 constraints:18653/19104
> #Model   5.90s var:21811/22758 constraints:18648/19104
> #Model   5.93s var:21810/22758 constraints:18648/19104
> #Bound   5.98s best:36    next:[15,35]    max_lp_sym
> #Model   6.05s var:21809/22758 constraints:18647/19104
> #Model   6.70s var:21808/22758 constraints:18647/19104
> #Bound   6.74s best:36    next:[19,35]    max_lp_sym
> #Model   6.85s var:21797/22758 constraints:18642/19104
> #Model   6.95s var:21788/22758 constraints:18637/19104
> #Bound   7.18s best:36    next:[20,35]    bool_core (num_cores=20 [size:2 mw:1 d:4] a=45 d=4 fixed=970/22824 clauses=17'854)
> #Model   7.38s var:21787/22758 constraints:18637/19104
> #Bound   7.56s best:36    next:[21,35]    bool_core (num_cores=21 [size:4 mw:1 d:5] a=42 d=5 fixed=970/22829 clauses=18'156)
> #Bound   7.66s best:36    next:[22,35]    bool_core (num_cores=22 [size:2 mw:1 d:5] a=40 d=5 fixed=988/22834 clauses=18'217)
> #Bound   7.79s best:36    next:[23,35]    bool_core (num_cores=23 [size:4 mw:1 d:6] a=37 d=6 fixed=988/22840 clauses=18'290)
> #Bound   7.93s best:36    next:[24,35]    bool_core (num_cores=24 [size:2 mw:1 d:4] a=36 d=6 fixed=988/22846 clauses=18'383)
> #Bound   7.99s best:36    next:[26,35]    max_lp_sym
> #Model   7.57s var:21770/22758 constraints:18628/19104 [skipped_logs=0]
> #3       8.41s best:35    next:[26,34]    default_lp
> #Model   8.88s var:21728/22758 constraints:18606/19104 [skipped_logs=2]
> #Bound   9.40s best:35    next:[27,34]    bool_core (num_cores=27 [size:2 mw:1 d:7] a=30 d=7 fixed=1030/22864 clauses=19'365)
> #Bound   9.52s best:35    next:[28,34]    max_lp_sym
> #Model   9.91s var:21688/22758 constraints:18585/19104 [skipped_logs=3]
> #Bound  11.01s best:35    next:[29,34]    bool_core (num_cores=29 [size:2 mw:1 d:9] a=27 d=9 fixed=1080/22880 clauses=20'494)
> #Model  10.90s var:21588/22758 constraints:18533/19104 [skipped_logs=4]
> #Bound  11.14s best:35    next:[30,34]    max_lp_sym
> #Model  14.57s var:21587/22758 constraints:18533/19104
> #Model  15.39s var:21586/22758 constraints:18533/19104
> #Model  15.58s var:21577/22758 constraints:18529/19104
> #Model  16.83s var:21576/22758 constraints:18529/19104
> #Bound  19.75s best:35    next:[31,34]    bool_core (num_cores=31 [size:1 mw:1] a=24 d=10 fixed=1172/22898 clauses=27'277)
> #Bound  27.87s best:35    next:[32,34]    bool_core (num_cores=32 [size:5 mw:1 amo:1 lit:3 d:11] a=20 d=11 fixed=1183/22909 clauses=26'992)
> #Model  27.97s var:21575/22758 constraints:18529/19104
> #Model  28.83s var:21565/22758 constraints:18524/19104
> #Model  32.06s var:21555/22758 constraints:18519/19104
> #Model  34.64s var:21545/22758 constraints:18514/19104
> #Model  34.84s var:21544/22758 constraints:18514/19104
> #Model  36.78s var:21543/22758 constraints:18514/19104
> #Model  37.18s var:21542/22758 constraints:18514/19104
> #Model  38.07s var:21531/22758 constraints:18509/19104
> #Model  38.39s var:21513/22758 constraints:18499/19104
> #Bound  39.13s best:35    next:[33,34]    bool_core (num_cores=33 [size:4 mw:1 amo:1 lit:2 d:12] a=16 d=12 fixed=1183/22921 clauses=34'463)
> #Model  39.24s var:21510/22758 constraints:18499/19104
> #Model  40.66s var:21501/22758 constraints:18494/19104
> #Model  40.94s var:21490/22758 constraints:18489/19104
> #Model  41.22s var:21489/22758 constraints:18489/19104
> #Model  41.39s var:21487/22758 constraints:18489/19104
> #Model  41.47s var:21477/22758 constraints:18484/19104
> #Model  43.04s var:21463/22758 constraints:18479/19104
> #Model  43.15s var:21462/22758 constraints:18479/19104
> #Model  43.21s var:21448/22758 constraints:18467/19104
> #Model  43.47s var:21447/22758 constraints:18467/19104
> #Model  43.51s var:21446/22758 constraints:18467/19104
> #Model  44.18s var:21445/22758 constraints:18467/19104
> #Bound  62.19s best:35    next:[34,34]    bool_core (num_cores=34 [size:4 mw:1 exo] a=0 d=12 fixed=1289/22941 clauses=36'772)
> #Model  62.20s var:21399/22758 constraints:18447/19104
> #Model  63.46s var:21389/22758 constraints:18441/19104
> #Model  63.52s var:21387/22758 constraints:18441/19104
> #Model  64.32s var:21360/22758 constraints:18426/19104
> #Model  64.35s var:21359/22758 constraints:18426/19104
> #Model  64.76s var:21349/22758 constraints:18421/19104
> #Model  66.14s var:21339/22758 constraints:18416/19104
> #Model  74.03s var:21335/22758 constraints:18416/19104
> #4      74.80s best:34    next:[]         core
> #Done   74.80s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.21m,    1.21m]    1.21m   0.00ns    1.21m         1 [  48.97s,   48.97s]   48.97s   0.00ns   48.97s
>            'default_lp':         1 [   1.22m,    1.22m]    1.22m   0.00ns    1.22m         1 [  45.09s,   45.09s]   45.09s   0.00ns   45.09s
>      'feasibility_pump':       313 [ 16.39us, 429.04ms]   1.45ms  24.21ms 452.76ms       312 [  1.05us,   1.05us]   1.05us   0.00ns 327.60us
>                    'fj':         4 [166.55ms, 231.35ms] 198.14ms  30.93ms 792.58ms         4 [100.79ms, 100.80ms] 100.80ms   2.01us 403.19ms
>                    'fj':         4 [173.67ms, 238.67ms] 207.78ms  23.29ms 831.10ms         4 [100.79ms, 100.80ms] 100.80ms 394.18ns 403.18ms
>             'fs_random':         1 [   1.32s,    1.32s]    1.32s   0.00ns    1.32s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   1.12s,    1.12s]    1.12s   0.00ns    1.12s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        64 [ 56.27ms, 976.46ms] 487.79ms 249.68ms   31.22s        64 [ 10.00ns, 102.69ms]  54.79ms  44.20ms    3.51s
>         'graph_cst_lns':        67 [ 53.26ms, 984.08ms] 471.74ms 249.56ms   31.61s        67 [ 10.00ns, 103.09ms]  56.24ms  42.90ms    3.77s
>         'graph_dec_lns':        69 [ 80.35ms, 950.26ms] 456.68ms 275.17ms   31.51s        67 [ 10.00ns, 103.09ms]  49.06ms  45.90ms    3.29s
>         'graph_var_lns':        68 [ 57.55ms, 935.72ms] 470.45ms 235.09ms   31.99s        68 [ 10.00ns, 102.83ms]  70.19ms  37.05ms    4.77s
>                    'ls':       158 [107.03ms, 314.97ms] 198.38ms  44.73ms   31.34s       158 [100.00ms, 100.27ms] 100.04ms  48.05us   15.81s
>                'ls_lin':       155 [103.49ms, 336.83ms] 202.24ms  41.04ms   31.35s       155 [ 88.79ms, 100.31ms]  99.98ms 903.59us   15.50s
>            'max_lp_sym':         1 [   1.21m,    1.21m]    1.21m   0.00ns    1.21m         1 [  24.72s,   24.72s]   24.72s   0.00ns   24.72s
>                 'no_lp':         1 [   1.21m,    1.21m]    1.21m   0.00ns    1.21m         1 [  39.71s,   39.71s]   39.71s   0.00ns   39.71s
>          'pseudo_costs':         1 [   1.21m,    1.21m]    1.21m   0.00ns    1.21m         1 [  16.46s,   16.46s]   16.46s   0.00ns   16.46s
>         'quick_restart':         1 [   1.22m,    1.22m]    1.22m   0.00ns    1.22m         1 [  41.94s,   41.94s]   41.94s   0.00ns   41.94s
>   'quick_restart_no_lp':         1 [   1.21m,    1.21m]    1.21m   0.00ns    1.21m         1 [  38.43s,   38.43s]   38.43s   0.00ns   38.43s
>         'reduced_costs':         1 [   1.21m,    1.21m]    1.21m   0.00ns    1.21m         1 [  17.10s,   17.10s]   17.10s   0.00ns   17.10s
>             'rins/rens':       125 [ 11.31ms, 604.91ms] 257.73ms 193.58ms   32.22s        87 [ 10.00ns, 102.29ms]  60.87ms  45.97ms    5.30s
>           'rnd_cst_lns':        70 [ 54.84ms, 950.70ms] 451.20ms 277.96ms   31.58s        70 [ 10.00ns, 103.36ms]  49.44ms  46.05ms    3.46s
>           'rnd_var_lns':        72 [ 52.92ms, 973.53ms] 458.96ms 270.44ms   33.05s        71 [ 10.00ns, 103.53ms]  49.33ms  45.16ms    3.50s
> 
> Search stats               Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  22'941     40'895   140'797    17'770  291'578'258        339'411
>            'default_lp':  22'758     46'730   117'080    14'482  179'179'128        956'747
>             'fs_random':  22'758          0     7'846     7'846    9'077'322         29'146
>       'fs_random_no_lp':  22'758          0     6'788     6'788    7'835'433         25'933
>            'max_lp_sym':  22'758        783    37'826    10'943   27'753'148     26'632'260
>                 'no_lp':  22'758     44'892   111'755    14'338  169'322'639        842'965
>          'pseudo_costs':  22'758      7'334    46'523    11'049   49'519'947     41'976'297
>         'quick_restart':  22'758     27'801   172'971    16'633  174'291'136        799'150
>   'quick_restart_no_lp':  22'758     26'851   164'966    16'671  167'948'527        649'378
>         'reduced_costs':  22'758      5'856    45'157    11'070   46'263'124     42'844'326
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        36'123   1'046'813   1'339'224       482'764        78    11'532      47'426        10      1'811       12'114    2'306
>            'default_lp':        41'387   1'215'467   2'672'244     1'722'742        40     6'594      39'158         0      1'755       11'991      251
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':           734      32'239      48'042             0         0     3'143      21'356         0      1'100        7'010       85
>                 'no_lp':        39'910   1'111'663   2'408'262     1'105'557        25     6'375      38'753         0      1'805       12'248      165
>          'pseudo_costs':         6'696     197'953     378'549             0         4     3'202      21'721         0      1'125        7'334       90
>         'quick_restart':        22'653     580'139   1'832'703       798'997        19     6'325      38'713         0      1'725       11'808      177
>   'quick_restart_no_lp':        21'985     529'754   1'684'829       787'034        18     6'393      38'657         0      1'646       11'313      224
>         'reduced_costs':         5'285     128'488     503'735             0         3     3'183      21'636         0      1'104        7'160       82
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         13           0          0   78'163        0        0
>       'fs_random':         13           0          0        0        0        0
>      'max_lp_sym':          1      49'869      1'231        3    1'511        0
>    'pseudo_costs':          1     120'554      4'329      196   11'371        0
>   'quick_restart':         13           0          0   60'862        0        0
>   'reduced_costs':          1     102'869      8'975      203    9'273        0
> 
> Lp dimension              Final dimension of first component
>      'default_lp':              0 rows, 2 columns, 0 entries
>       'fs_random':              0 rows, 2 columns, 0 entries
>      'max_lp_sym':  18365 rows, 22514 columns, 84892 entries
>    'pseudo_costs':   6806 rows, 22758 columns, 23715 entries
>   'quick_restart':              0 rows, 2 columns, 0 entries
>   'reduced_costs':   6897 rows, 22758 columns, 24453 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow      Bad  BadScaling
>      'default_lp':          0            0       0         0        0           0
>       'fs_random':          0            0       0         0        0           0
>      'max_lp_sym':          0            0   1'514         0  280'434           0
>    'pseudo_costs':          0            0   1'485         0  140'301           0
>   'quick_restart':          0            0       0         0        0           0
>   'reduced_costs':          0            0   1'365         0  288'004           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':           36        0      142       0         36      0             0           0/0
>       'fs_random':           36        0        0       0          0      0             0           0/0
>      'max_lp_sym':       20'061      623    2'671       0      2'163      0             1   1'231/2'375
>    'pseudo_costs':       23'464        7    5'571       0      2'901      0             0  4'329/10'553
>   'quick_restart':           36        0      188       0         36      0             0           0/0
>   'reduced_costs':       28'109       11    6'305       1      3'249      0             0  8'975/21'808
> 
> Lp Cut           max_lp_sym  reduced_costs  pseudo_costs
>          CG_FF:          19            358           308
>           CG_K:           -             12            10
>           CG_R:          11             21            64
>         Clique:          24            485           368
>      MIR_1_RLT:           -          1'006           562
>       MIR_3_FF:           -              8             -
>       MIR_4_FF:           9              4             -
>       MIR_5_FF:           3              3            10
>       MIR_6_FF:          14              4            27
>   ZERO_HALF_FF:         448          4'631         2'143
>    ZERO_HALF_R:         703          2'443           837
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':          0/64     55%    9.75e-01       0.10
>   'graph_cst_lns':          1/67     63%    9.97e-01       0.10
>   'graph_dec_lns':          0/67     63%    9.97e-01       0.10
>   'graph_var_lns':          1/68     50%    8.71e-01       0.10
>       'rins/rens':        35/121     62%    9.93e-01       0.10
>     'rnd_cst_lns':          0/70     60%    9.96e-01       0.10
>     'rnd_var_lns':          0/71     63%    9.98e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        2                  2    156'757         0              0          0          1'187         44'438
>         'fj_restart_compound_perturb_obj':        1                  1          0    34'035          9'265     12'377              3        554'156
>       'fj_restart_decay_compound_perturb':        2                  2          0    77'549         13'260     32'143              3      1'074'333
>   'fj_restart_decay_compound_perturb_obj':        2                  2          0    75'578         17'528     28'983              4      1'060'697
>                          'fj_restart_obj':        1                  1     79'209         0              0          0            423         22'460
>                          'ls_lin_restart':       12                  4    934'094         0              0          0         24'298        137'319
>                 'ls_lin_restart_compound':        9                  6          0    34'776          1'495     16'636            276      5'663'740
>         'ls_lin_restart_compound_perturb':       27                 14          0   128'787          6'062     61'354          1'031     16'609'163
>                    'ls_lin_restart_decay':       22                 12  1'843'114         0              0          0          3'664        497'432
>           'ls_lin_restart_decay_compound':       20                 15          0   124'145         14'619     54'748            489     12'193'442
>   'ls_lin_restart_decay_compound_perturb':       33                 11          0   661'429         65'953    297'717            506     17'561'721
>            'ls_lin_restart_decay_perturb':       23                 11  1'922'477         0              0          0          3'716        521'813
>                  'ls_lin_restart_perturb':        9                  9    704'101         0              0          0         17'349        149'440
>                              'ls_restart':       22                  8  1'700'907         0              0          0         40'238        256'272
>                     'ls_restart_compound':       15                 10          0    55'862          1'770     27'044            431      9'511'532
>             'ls_restart_compound_perturb':       19                 13          0    90'326          4'000     43'155            875     11'641'338
>                        'ls_restart_decay':       19                 12  1'590'668         0              0          0          3'245        410'700
>               'ls_restart_decay_compound':       18                 10          0   202'106         29'941     86'054            438     10'251'232
>       'ls_restart_decay_compound_perturb':       23                 11          0   372'015         43'965    163'976            479     12'770'000
>                'ls_restart_decay_perturb':       35                 13  2'928'758         0              0          0          5'524        824'203
>                      'ls_restart_perturb':        7                  6    548'219         0              0          0         14'009        117'486
> 
> Solutions (4)    Num   Rank
>         'core':    2  [1,4]
>   'default_lp':    2  [2,3]
> 
> Objective bounds     Num
>        'bool_core':   11
>   'initial_domain':    1
>       'max_lp_sym':    5
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    191    1'309      180
>    'fj solution hints':      0        0        0
>         'lp solutions':    172       53      159
>                 'pump':    312       72
> 
> Improving bounds shared    Num  Sym
>                   'core':  926    0
>             'default_lp':   68    0
>             'max_lp_sym':   34    0
>                  'no_lp':   44    0
>           'pseudo_costs':   27    0
>          'quick_restart':   73    0
>    'quick_restart_no_lp':   93    0
>          'reduced_costs':  158    0
> 
> Clauses shared               Num
>                  'core':  86'242
>            'default_lp':  11'675
>            'max_lp_sym':  31'571
>                 'no_lp':   7'893
>          'pseudo_costs':      41
>         'quick_restart':  32'555
>   'quick_restart_no_lp':   3'846
>         'reduced_costs':  34'363
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 34
> best_bound: 34
> integers: 99
> booleans: 22758
> conflicts: 0
> branches: 6788
> propagations: 7835433
> integer_propagations: 25933
> restarts: 6788
> lp_iterations: 0
> walltime: 74.9915
> usertime: 74.9915
> deterministic_time: 336.757
> gap_integral: 63.8926
> solution_fingerprint: 0xd7ab88962cb60908
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
> Initial optimization model '': (model_fingerprint: 0x651540384666de3f)
> #Variables: 120 (#bools: 40 in objective) (80 primary variables)
>   - 40 Booleans in [0,1]
>   - 40 in [0,3]
>   - 40 in [0,4]
> #kAutomaton: 10
> #kLinear1: 80 (#enforced: 40)
> #kLinear2: 40 (#enforced: 40)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   2.80e-05s  0.00e+00d  [DetectDominanceRelations] 
>   1.59e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   9.81e-07s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.93e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   5.62e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2'697 
> [Symmetry] Graph for symmetry has 13'169 nodes and 33'522 arcs.
> [Symmetry] Symmetry computation done. time: 0.00251456 dtime: 0.00501928
> [Symmetry] #generators: 39, average support size: 2
> [Symmetry] The model contains 10 duplicate constraints !
> [Symmetry] 7 orbits on 46 variables with sizes: 10,7,7,6,6,6,4
> [Symmetry] Found orbitope of size 1 x 6
> [SAT presolve] num removable Booleans: 239 / 3403
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:9575 literals:23609 vars:3356 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000545987s] clauses:9565 literals:23579 vars:3356 one_side_vars:0 simple_definition:10 singleton_clauses:0
> [SAT presolve] [0.000849733s] clauses:9465 literals:23579 vars:3306 one_side_vars:0 simple_definition:10 singleton_clauses:0
>   9.91e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.26e-02s  1.93e-01d  [Probe] #probed=6'826 #equiv=39 #new_binary_clauses=7'647 
>   1.68e-02s  5.94e-02d  [MaxClique] Merged 6'762(13'524 literals) into 2'382(8'992 literals) at_most_ones. 
>   7.51e-04s  0.00e+00d  [DetectDominanceRelations] 
>   3.70e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   4.21e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.75e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=71 
>   1.27e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.68e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.86e-05s  0.00e+00d  [DetectDifferentVariables] 
>   1.94e-03s  9.36e-05d  [ProcessSetPPC] #relevant_constraints=5'368 #num_inclusions=2'392 
>   5.41e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.68e-04s  6.15e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.04e-04s  6.47e-05d  [FindBigVerticalLinearOverlap] 
>   4.15e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.55e-04s  4.25e-06d  [MergeClauses] #num_collisions=150 #num_merges=150 #num_saved_literals=350 
>   5.23e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.73e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.23e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.66e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.97e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   8.89e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 7'078 nodes and 13'319 arcs.
> [Symmetry] Symmetry computation done. time: 0.00125631 dtime: 0.00265006
> [Symmetry] #generators: 12, average support size: 8
> [Symmetry] 20 orbits on 68 variables with sizes: 5,5,5,5,4,4,4,4,3,3,...
> [Symmetry] Found orbitope of size 4 x 5
> [SAT presolve] num removable Booleans: 0 / 3248
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:250 literals:850 vars:231 one_side_vars:0 simple_definition:212 singleton_clauses:0
> [SAT presolve] [2.3104e-05s] clauses:250 literals:850 vars:231 one_side_vars:0 simple_definition:212 singleton_clauses:0
> [SAT presolve] [8.4781e-05s] clauses:250 literals:850 vars:231 one_side_vars:0 simple_definition:212 singleton_clauses:0
>   1.32e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.95e-02s  2.11e-01d  [Probe] #probed=6'696 #fixed_bools=66 #equiv=195 #new_binary_clauses=7'831 
>   1.00e-04s  8.54e-05d  [MaxClique] 
>   5.41e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.93e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.11e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.25e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=154 
>   9.09e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.77e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.87e-05s  0.00e+00d  [DetectDifferentVariables] 
>   8.08e-04s  3.70e-05d  [ProcessSetPPC] #relevant_constraints=2'781 
>   5.42e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.42e-04s  5.66e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   1.02e-04s  6.09e-05d  [FindBigVerticalLinearOverlap] 
>   3.67e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.49e-04s  4.25e-06d  [MergeClauses] #num_collisions=150 #num_merges=150 #num_saved_literals=350 
>   5.15e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.62e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.45e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.64e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.95e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   8.77e-05s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 6'852 nodes and 12'530 arcs.
> [Symmetry] Symmetry computation done. time: 0.00112091 dtime: 0.00241973
> [SAT presolve] num removable Booleans: 0 / 2987
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:260 literals:870 vars:245 one_side_vars:14 simple_definition:212 singleton_clauses:0
> [SAT presolve] [2.3875e-05s] clauses:260 literals:870 vars:245 one_side_vars:14 simple_definition:212 singleton_clauses:0
> [SAT presolve] [8.5111e-05s] clauses:260 literals:870 vars:245 one_side_vars:14 simple_definition:212 singleton_clauses:0
>   9.89e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.89e-02s  1.73e-01d  [Probe] #probed=6'694 #equiv=31 #new_binary_clauses=7'297 
>   9.78e-05s  8.54e-05d  [MaxClique] 
>   5.28e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.73e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.05e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.08e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=33 
>   8.81e-05s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.81e-05s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   3.96e-05s  0.00e+00d  [DetectDifferentVariables] 
>   7.92e-04s  3.66e-05d  [ProcessSetPPC] #relevant_constraints=2'748 
>   5.36e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.35e-04s  5.63e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   9.92e-05s  6.02e-05d  [FindBigVerticalLinearOverlap] 
>   4.02e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.54e-04s  4.25e-06d  [MergeClauses] #num_collisions=150 #num_merges=150 #num_saved_literals=350 
>   5.50e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.67e-03s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
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
>   - rule 'linear1: x in domain' was applied 40 times.
>   - rule 'linear: always true' was applied 70 times.
>   - rule 'linear: enforcement literal in expression' was applied 70 times.
>   - rule 'linear: fixed or dup variables' was applied 70 times.
>   - rule 'linear: remapped using affine relations' was applied 470 times.
>   - rule 'new_bool: automaton expansion' was applied 3'363 times.
>   - rule 'objective: expanded via tight equality' was applied 72 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 66 times.
>   - rule 'presolve: 106 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 2'382 times.
>   - rule 'setppc: removed dominated constraints' was applied 10 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 40 times.
>   - rule 'variables: detect half reified value encoding' was applied 80 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x87ec4ca7234959a1)
> #Variables: 2'956 (#bools: 74 in objective) (1'168 primary variables)
>   - 2'956 Booleans in [0,1]
> #kBoolAnd: 107 (#enforced: 107 #multi: 100) (#literals: 517)
> #kExactlyOne: 2'488 (#literals: 11'126)
> [Symmetry] Graph for symmetry has 6'288 nodes and 12'390 arcs.
> [Symmetry] Symmetry computation done. time: 0.00106875 dtime: 0.00219773
> 
> Preloading model.
> #Bound   0.24s best:inf   next:[0,40]     initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model   0.24s var:2956/2956 constraints:2595/2595
> 
> Starting search at 0.24s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       0.34s best:40    next:[0,39]     quick_restart_no_lp [hint]
> #2       0.34s best:31    next:[0,30]     core
> #3       0.35s best:30    next:[0,29]     graph_cst_lns (d=5.00e-01 s=17 t=0.10 p=0.00 stall=0 h=base) [hint]
> #4       0.36s best:29    next:[0,28]     quick_restart [hint]
> #5       0.37s best:28    next:[0,27]     no_lp
> #6       0.37s best:27    next:[0,26]     default_lp
> #7       0.42s best:25    next:[0,24]     rins_pump_lns (d=5.00e-01 s=28 t=0.10 p=0.00 stall=0 h=base)
> #Bound   0.47s best:25    next:[1,24]     reduced_costs
> #Bound   0.48s best:25    next:[2,24]     reduced_costs
> #Bound   0.51s best:25    next:[4,24]     reduced_costs
> #Bound   0.52s best:25    next:[5,24]     bool_core (num_cores=5 [size:4 mw:1 d:2] a=63 d=2 fixed=0/2971 clauses=2'239)
> #Bound   0.52s best:25    next:[6,24]     bool_core (num_cores=6 [size:4 mw:1 d:2] a=60 d=2 fixed=0/2976 clauses=2'245)
> #Bound   0.52s best:25    next:[7,24]     bool_core (num_cores=7 [size:4 mw:1 d:2] a=57 d=2 fixed=0/2981 clauses=2'252)
> #Bound   0.52s best:25    next:[8,24]     bool_core (num_cores=8 [size:4 mw:1 d:3] a=54 d=3 fixed=0/2986 clauses=2'263)
> #Bound   0.53s best:25    next:[9,24]     bool_core (num_cores=9 [size:8 mw:1 amo:1 lit:5 d:3] a=47 d=3 fixed=0/2993 clauses=2'282)
> #Bound   0.53s best:25    next:[10,24]    bool_core (num_cores=10 [size:5 mw:1 d:3] a=43 d=3 fixed=0/2999 clauses=2'295)
> #Bound   0.54s best:25    next:[11,24]    bool_core (num_cores=11 [size:7 mw:1 amo:1 lit:4 d:4] a=37 d=4 fixed=0/3006 clauses=2'314)
> #8       0.54s best:24    next:[11,23]    quick_restart_no_lp
> #Bound   0.54s best:24    next:[12,23]    bool_core (num_cores=12 [size:6 mw:1 amo:1 lit:4 d:5] a=32 d=5 fixed=0/3013 clauses=2'345)
> #Bound   0.54s best:24    next:[13,23]    bool_core (num_cores=13 [size:3 mw:1 d:3] a=30 d=5 fixed=0/3020 clauses=2'360)
> #Bound   0.55s best:24    next:[14,23]    bool_core (num_cores=14 [size:5 mw:1 d:6] a=26 d=6 fixed=0/3026 clauses=2'482)
> #Bound   0.56s best:24    next:[15,23]    bool_core (num_cores=15 [size:2 mw:1 d:7] a=25 d=7 fixed=0/3035 clauses=2'564)
> #Bound   0.58s best:24    next:[16,23]    bool_core (num_cores=16 [size:2 mw:1 d:8] a=24 d=8 fixed=0/3044 clauses=2'732)
> #Bound   0.59s best:24    next:[17,23]    bool_core (num_cores=16 [cover] a=24 d=8 fixed=0/3053 clauses=2'891)
> #Bound   0.59s best:24    next:[18,23]    bool_core (num_cores=17 [size:2 mw:1 d:4] a=23 d=8 fixed=1/3061 clauses=2'960)
> #Bound   0.61s best:24    next:[22,23]    max_lp
> #Model   0.77s var:2949/2956 constraints:2592/2595
> #Bound   0.90s best:24    next:[23,23]    bool_core (num_cores=21 [size:1 mw:1] a=1 d=10 fixed=9/3095 clauses=6'529)
> #Model   0.91s var:2851/2956 constraints:2549/2595
> #Done    1.00s core
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [757.90ms, 757.90ms] 757.90ms   0.00ns 757.90ms         1 [   1.25s,    1.25s]    1.25s   0.00ns    1.25s
>            'default_lp':         1 [758.87ms, 758.87ms] 758.87ms   0.00ns 758.87ms         1 [925.24ms, 925.24ms] 925.24ms   0.00ns 925.24ms
>      'feasibility_pump':         9 [ 28.33us,  17.55ms]   1.99ms   5.50ms  17.89ms         8 [648.00ns, 648.00ns] 648.00ns   0.00ns   5.18us
>                    'fj':         1 [ 97.16ms,  97.16ms]  97.16ms   0.00ns  97.16ms         1 [100.12ms, 100.12ms] 100.12ms   0.00ns 100.12ms
>                    'fj':         1 [121.70ms, 121.70ms] 121.70ms   0.00ns 121.70ms         1 [100.12ms, 100.12ms] 100.12ms   0.00ns 100.12ms
>             'fs_random':         1 [ 95.29ms,  95.29ms]  95.29ms   0.00ns  95.29ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [ 93.90ms,  93.90ms]  93.90ms   0.00ns  93.90ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':        10 [  1.20ms,  90.82ms]  27.24ms  30.86ms 272.41ms         8 [ 10.00ns, 100.18ms]  25.38ms  43.17ms 203.01ms
>         'graph_cst_lns':        10 [  5.51ms,  61.83ms]  19.32ms  18.14ms 193.25ms         9 [ 10.00ns,  56.83ms]   9.24ms  18.69ms  83.15ms
>         'graph_dec_lns':         9 [  6.61ms,  14.63ms]  10.40ms   2.59ms  93.63ms         8 [ 10.00ns, 106.00ns]  22.00ns  31.75ns 176.00ns
>         'graph_var_lns':        10 [  5.46ms,  85.73ms]  38.28ms  31.60ms 382.76ms        10 [ 10.00ns, 100.23ms]  35.13ms  44.33ms 351.28ms
>                    'ls':         6 [ 72.86ms, 127.60ms] 108.64ms  18.01ms 651.83ms         6 [ 56.39ms, 100.01ms]  92.73ms  16.26ms 556.40ms
>                'ls_lin':         6 [ 84.03ms, 123.58ms] 108.46ms  13.32ms 650.73ms         6 [ 70.80ms, 100.01ms]  95.13ms  10.88ms 570.81ms
>                'max_lp':         1 [792.38ms, 792.38ms] 792.38ms   0.00ns 792.38ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [758.77ms, 758.77ms] 758.77ms   0.00ns 758.77ms         1 [   1.02s,    1.02s]    1.02s   0.00ns    1.02s
>          'pseudo_costs':         1 [758.03ms, 758.03ms] 758.03ms   0.00ns 758.03ms         1 [228.00ms, 228.00ms] 228.00ms   0.00ns 228.00ms
>         'quick_restart':         1 [758.77ms, 758.77ms] 758.77ms   0.00ns 758.77ms         1 [881.91ms, 881.91ms] 881.91ms   0.00ns 881.91ms
>   'quick_restart_no_lp':         1 [758.63ms, 758.63ms] 758.63ms   0.00ns 758.63ms         1 [   1.14s,    1.14s]    1.14s   0.00ns    1.14s
>         'reduced_costs':         1 [758.73ms, 758.73ms] 758.73ms   0.00ns 758.73ms         1 [343.95ms, 343.95ms] 343.95ms   0.00ns 343.95ms
>             'rins/rens':         8 [  4.25ms,  28.90ms]  12.24ms  10.29ms  97.95ms         3 [324.04us,   5.98ms]   4.09ms   2.66ms  12.28ms
>           'rnd_cst_lns':        10 [  5.60ms,  28.93ms]  13.02ms   7.71ms 130.21ms        10 [ 10.00ns,   2.92ms] 379.98us 886.28us   3.80ms
>           'rnd_var_lns':        10 [  5.97ms,  31.08ms]  12.36ms   7.29ms 123.57ms        10 [ 10.00ns,   2.05ms] 227.12us 610.33us   2.27ms
> 
> Search stats              Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  3'102      5'354    38'237    12'361   9'643'204        116'971
>            'default_lp':  2'956      4'553    32'444    12'022   6'284'011        213'848
>             'fs_random':  2'956          0     5'912     5'912   1'441'726         30'705
>       'fs_random_no_lp':  2'956          0     5'952     5'913   1'444'642         30'819
>                'max_lp':  2'956          0     5'912     5'912   1'441'733      1'447'647
>                 'no_lp':  2'956      6'165    34'387    12'090   6'883'896        215'020
>          'pseudo_costs':  2'956         51    13'257     8'230   2'044'971      2'052'151
>         'quick_restart':  2'956      3'110    37'117    12'376   6'254'719        190'149
>   'quick_restart_no_lp':  2'956      4'697    41'998    12'518   7'327'474        194'954
>         'reduced_costs':  2'956         50    19'957    10'029   2'957'384      2'971'891
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         4'386      52'051      91'326             0        21     5'116      15'750         0        524        2'986    1'105
>            'default_lp':         3'845      69'544     173'400             0         7     5'110      15'649         0        526        3'088    1'181
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':         5'133      80'519     223'417             0         2     5'103      15'632         0        532        3'043    1'106
>          'pseudo_costs':            41         531       1'891             0         0       194       1'539         0         54          470        0
>         'quick_restart':         2'377      28'964     116'986             0         2     5'096      15'591         0        540        3'115    1'085
>   'quick_restart_no_lp':         3'688      43'049     175'752             0         8     5'110      15'665         0        514        2'941    1'101
>         'reduced_costs':            39         690       2'473             0         0     2'528       8'206         0        302        1'768      528
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         12           0          0    9'790        0        0
>       'fs_random':         12           0          0        0        0        0
>          'max_lp':          1       2'369        222        3        1        0
>    'pseudo_costs':          1       3'333        996       29      123        0
>   'quick_restart':         12           0          0    5'979        0        0
>   'reduced_costs':          1       3'329        642       30      124        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':            0 rows, 2 columns, 0 entries
>       'fs_random':            0 rows, 2 columns, 0 entries
>          'max_lp':  2667 rows, 2956 columns, 15722 entries
>    'pseudo_costs':   1274 rows, 2956 columns, 6568 entries
>   'quick_restart':            0 rows, 2 columns, 0 entries
>   'reduced_costs':   1375 rows, 2956 columns, 6891 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0       4         0  38'817           0
>    'pseudo_costs':          0            0      42         0  21'020           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0      42         0  13'636           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened  Cuts/Call
>      'default_lp':           16        0       14       0         14      0             0        0/0
>       'fs_random':           16        0        0       0          0      0             0        0/0
>          'max_lp':        2'820      129       20       0         25      2             7    222/304
>    'pseudo_costs':        3'594        0       52       0         60      0             6  996/2'076
>   'quick_restart':           16        0       14       0         14      0             0        0/0
>   'reduced_costs':        3'240        0        0       0          0      0             0  642/1'126
> 
> Lp Cut           reduced_costs  pseudo_costs  max_lp
>          CG_FF:             60            92      15
>           CG_K:             16            23       -
>           CG_R:             24            57      23
>         Clique:             47            69      30
>       MIR_1_FF:              -             -       1
>      MIR_1_RLT:            153           184       1
>       MIR_4_FF:              -             -       1
>   ZERO_HALF_FF:            115           379      24
>    ZERO_HALF_R:            227           192     127
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           1/9     78%    9.35e-01       0.10
>   'graph_cst_lns':          3/10     90%    9.76e-01       0.10
>   'graph_dec_lns':           1/9    100%    9.81e-01       0.10
>   'graph_var_lns':          3/10     60%    8.22e-01       0.10
>       'rins/rens':           6/8    100%    9.76e-01       0.10
>     'rnd_cst_lns':          2/10    100%    9.86e-01       0.10
>     'rnd_var_lns':          1/10    100%    9.86e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1    77'928         0              0          0         15'603          2'956
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0    52'732         15'382     18'672             46        520'275
>         'ls_lin_restart_compound_perturb':        3                  3         0    90'730          9'494     40'610            501      1'409'692
>   'ls_lin_restart_decay_compound_perturb':        1                  1         0    43'942         10'798     16'569             55        503'651
>                  'ls_lin_restart_perturb':        2                  2   152'503         0              0          0         15'707          5'905
>                              'ls_restart':        1                  1    75'932         0              0          0          7'540          2'956
>             'ls_restart_compound_perturb':        1                  1         0    31'291          3'155     14'066            163        516'308
>                        'ls_restart_decay':        1                  1    88'203         0              0          0            864          7'358
>               'ls_restart_decay_compound':        1                  1         0    21'170          5'652      7'759             37        282'383
>       'ls_restart_decay_compound_perturb':        1                  1         0    41'099         10'297     15'395             53        501'988
>                      'ls_restart_perturb':        1                  1    77'299         0              0          0          5'692          2'956
> 
> Solutions (8)             Num   Rank
>                  'core':    1  [2,2]
>            'default_lp':    1  [6,6]
>         'graph_cst_lns':    1  [3,3]
>                 'no_lp':    1  [5,5]
>         'quick_restart':    1  [4,4]
>   'quick_restart_no_lp':    2  [1,8]
>         'rins_pump_lns':    1  [7,7]
> 
> Objective bounds     Num
>        'bool_core':   15
>   'initial_domain':    1
>           'max_lp':    1
>    'reduced_costs':    3
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     17      150       17
>    'fj solution hints':      0        0        0
>         'lp solutions':      0        0        0
>                 'pump':      8        8
> 
> Improving bounds shared    Num  Sym
>                   'core':  105    0
> 
> Clauses shared            Num
>                  'core':  489
>            'default_lp':    6
>                 'no_lp':    7
>          'pseudo_costs':   33
>         'quick_restart':  248
>   'quick_restart_no_lp':  424
>         'reduced_costs':   93
> 
> CpSolverResponse summary:
> status: OPTIMAL
> objective: 24
> best_bound: 24
> integers: 75
> booleans: 2956
> conflicts: 0
> branches: 5952
> propagations: 1444642
> integer_propagations: 30819
> restarts: 5913
> lp_iterations: 0
> walltime: 1.03645
> usertime: 1.03645
> deterministic_time: 8.41674
> gap_integral: 2.77135
> solution_fingerprint: 0x4bb8feb725303ea7
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
> Initial optimization model '': (model_fingerprint: 0x80b6bec51450515)
> #Variables: 750 (#bools: 250 in objective) (500 primary variables)
>   - 250 Booleans in [0,1]
>   - 250 in [0,4]
>   - 250 in [0,5]
> #kAutomaton: 50
> #kLinear1: 500 (#enforced: 250)
> #kLinear2: 250 (#enforced: 250)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   3.29e-04s  0.00e+00d  [DetectDominanceRelations] 
>   1.85e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.67e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   7.87e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   1.38e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=459'333 
> [Symmetry] Graph for symmetry has 1'819'779 nodes and 4'884'866 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 41594 / 503057
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1337881 literals:3417627 vars:502819 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.225152s] clauses:1337831 literals:3417477 vars:502819 one_side_vars:0 simple_definition:50 singleton_clauses:0
> [SAT presolve] [0.306878s] clauses:1323129 literals:3417477 vars:495468 one_side_vars:0 simple_definition:50 singleton_clauses:0
>   3.18e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.72e-01s  1.01e+00d *[Probe] #probed=1'484 #new_binary_clauses=63'775 
>   1.17e+00s  2.02e+00d *[MaxClique] Merged 1'003'093(2'006'186 literals) into 994'835(1'997'929 literals) at_most_ones. 
>   1.53e-01s  0.00e+00d  [DetectDominanceRelations] 
>   8.68e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.52e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   7.68e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   7.27e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.87e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.55e-02s  0.00e+00d  [DetectDifferentVariables] 
>   4.94e-01s  2.95e-02d  [ProcessSetPPC] #relevant_constraints=1'327'134 #num_inclusions=994'885 
>   1.79e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.01e-01s  2.19e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   3.94e-02s  1.93e-02d  [FindBigVerticalLinearOverlap] 
>   1.67e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   9.84e-02s  6.99e-03d  [MergeClauses] #num_collisions=22'410 #num_merges=22'410 #num_saved_literals=52'171 
>   1.55e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.30e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.55e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.30e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.15e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   3.67e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'804'054 nodes and 4'795'816 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 34243 / 495369
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1310463 literals:3383837 vars:495349 one_side_vars:0 simple_definition:6939 singleton_clauses:0
> [SAT presolve] [0.223453s] clauses:1310463 literals:3383837 vars:495349 one_side_vars:0 simple_definition:6939 singleton_clauses:0
> [SAT presolve] [0.283985s] clauses:1310463 literals:3383837 vars:495349 one_side_vars:0 simple_definition:6939 singleton_clauses:0
>   3.49e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.76e-01s  1.01e+00d *[Probe] #probed=1'322 #equiv=117 #new_binary_clauses=68'155 
>   1.16e+00s  1.99e+00d *[MaxClique] Merged 992'631(1'985'263 literals) into 984'434(1'976'871 literals) at_most_ones. 
>   1.67e-01s  0.00e+00d  [DetectDominanceRelations] 
>   6.02e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.75e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   9.89e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=506 
>   1.07e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.65e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.19e-02s  0.00e+00d  [DetectDifferentVariables] 
>   5.14e-01s  2.93e-02d  [ProcessSetPPC] #relevant_constraints=1'316'127 #num_inclusions=984'064 
>   2.42e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.23e-01s  2.19e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   4.74e-02s  1.92e-02d  [FindBigVerticalLinearOverlap] 
>   2.37e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.07e-01s  6.94e-03d  [MergeClauses] #num_collisions=22'182 #num_merges=22'182 #num_saved_literals=51'715 
>   1.69e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.66e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.69e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.67e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.85e-02s  0.00e+00d  [DetectDuplicateColumns] 
>   5.13e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 1'803'292 nodes and 4'775'842 arcs.
> [Symmetry] Graph too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 34176 / 495252
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:1299725 literals:3354177 vars:495028 one_side_vars:73 simple_definition:12951 singleton_clauses:0
> [SAT presolve] [0.219365s] clauses:1299725 literals:3354177 vars:495028 one_side_vars:73 simple_definition:12951 singleton_clauses:0
> [SAT presolve] [0.274295s] clauses:1299725 literals:3354177 vars:495028 one_side_vars:73 simple_definition:12951 singleton_clauses:0
>   7.54e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.97e-01s  1.01e+00d *[Probe] #probed=1'322 #new_binary_clauses=67'921 
>   1.12e+00s  1.97e+00d *[MaxClique] Merged 983'143(1'966'339 literals) into 974'547(1'957'743 literals) at_most_ones. 
>   1.81e-01s  0.00e+00d  [DetectDominanceRelations] 
>   6.35e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.82e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.07e-01s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.28e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.41e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   2.83e-02s  0.00e+00d  [DetectDifferentVariables] 
>   5.27e-01s  2.91e-02d  [ProcessSetPPC] #relevant_constraints=1'306'512 #num_inclusions=974'449 
>   3.05e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.24e-01s  2.20e-01d  [FindBigAtMostOneAndLinearOverlap] 
>   4.76e-02s  1.91e-02d  [FindBigVerticalLinearOverlap] 
>   3.06e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.18e-01s  6.89e-03d  [MergeClauses] #num_collisions=22'182 #num_merges=22'182 #num_saved_literals=51'715 
>   1.84e-01s  0.00e+00d  [DetectDominanceRelations] 
>   5.01e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
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
>   - rule 'linear1: x in domain' was applied 250 times.
>   - rule 'linear: always true' was applied 450 times.
>   - rule 'linear: enforcement literal in expression' was applied 450 times.
>   - rule 'linear: fixed or dup variables' was applied 450 times.
>   - rule 'linear: remapped using affine relations' was applied 12'950 times.
>   - rule 'new_bool: automaton expansion' was applied 502'807 times.
>   - rule 'objective: expanded via tight equality' was applied 40 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 39 times.
>   - rule 'presolve: 250 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 4'122 times.
>   - rule 'setppc: removed dominated constraints' was applied 202 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 250 times.
>   - rule 'variables: detect half reified value encoding' was applied 500 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xaae0966c5c458d13)
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
> #Bound  23.32s best:inf   next:[0,250]    initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model  23.54s var:495252/495252 constraints:381217/381217
> 
> Starting search at 23.57s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1      28.02s best:248   next:[0,247]    quick_restart_no_lp [hint]
> #2      28.35s best:247   next:[0,246]    no_lp
> #Model  28.46s var:495203/495252 constraints:381188/381217
> #3      29.30s best:246   next:[0,245]    quick_restart [hint]
> #4      29.57s best:142   next:[0,141]    quick_restart
> #Bound  31.47s best:142   next:[1,141]    bool_core (num_cores=1 [size:16 mw:1 d:4] a=235 d=4 fixed=49/495266 clauses=332'110)
> #Model  41.14s var:495094/495252 constraints:381123/381217
> #5      41.25s best:141   next:[1,140]    quick_restart_no_lp
> #Bound  45.68s best:141   next:[2,140]    bool_core (num_cores=2 [size:14 mw:1 d:4] a=222 d=4 fixed=49/495293 clauses=331'973)
> #6      46.15s best:140   next:[2,139]    quick_restart
> #7      50.02s best:139   next:[2,138]    quick_restart
> #Bound  50.38s best:139   next:[3,138]    bool_core (num_cores=3 [size:14 mw:1 d:4] a=209 d=4 fixed=158/495318 clauses=332'085)
> #Bound  54.87s best:139   next:[4,138]    bool_core (num_cores=4 [size:15 mw:1 d:4] a=195 d=4 fixed=158/495344 clauses=332'123)
> #8      56.82s best:138   next:[4,137]    pseudo_costs
> #9      57.38s best:137   next:[4,136]    quick_restart_no_lp
> #Bound  59.37s best:137   next:[5,136]    bool_core (num_cores=5 [size:15 mw:1 d:4] a=181 d=4 fixed=158/495371 clauses=332'156)
> #Bound  63.63s best:137   next:[6,136]    bool_core (num_cores=6 [size:15 mw:1 d:4] a=167 d=4 fixed=158/495398 clauses=332'234)
> #Bound  69.01s best:137   next:[7,136]    bool_core (num_cores=7 [size:21 mw:1 d:5] a=147 d=5 fixed=158/495431 clauses=332'325)
> #Bound  72.76s best:137   next:[8,136]    bool_core (num_cores=8 [size:14 mw:1 d:4] a=134 d=5 fixed=158/495463 clauses=332'394)
> #Bound  76.86s best:137   next:[9,136]    bool_core (num_cores=9 [size:15 mw:1 d:4] a=120 d=5 fixed=158/495489 clauses=332'460)
> #Bound  80.56s best:137   next:[10,136]   bool_core (num_cores=10 [size:14 mw:1 d:4] a=107 d=5 fixed=158/495515 clauses=332'497)
> #Bound  84.75s best:137   next:[11,136]   bool_core (num_cores=11 [size:16 mw:1 d:4] a=92 d=5 fixed=158/495542 clauses=332'540)
> #Bound  88.79s best:137   next:[12,136]   bool_core (num_cores=12 [size:14 mw:1 d:4] a=79 d=5 fixed=158/495569 clauses=332'626)
> #Bound  90.73s best:137   next:[13,136]   bool_core (num_cores=13 [size:2 mw:1 d:5] a=78 d=5 fixed=158/495582 clauses=332'691)
> #Model  92.78s var:495045/495252 constraints:381094/381217
> #Bound  93.76s best:137   next:[14,136]   bool_core (num_cores=14 [size:3 mw:1 d:5] a=76 d=5 fixed=158/495590 clauses=332'771)
> #Model  93.80s var:494996/495252 constraints:381065/381217
> #Bound 107.55s best:137   next:[15,136]   bool_core (num_cores=15 [size:2 mw:1 d:5] a=75 d=5 fixed=256/495599 clauses=332'618)
> #Model 108.03s var:494947/495252 constraints:381036/381217
> #Bound 113.07s best:137   next:[16,136]   bool_core (num_cores=16 [size:5 mw:1 d:6] a=71 d=6 fixed=305/495610 clauses=333'147)
> #Bound 116.05s best:137   next:[17,136]   bool_core (num_cores=17 [size:5 mw:1 d:5] a=67 d=6 fixed=305/495624 clauses=333'228)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  33.15s,   33.15s]   33.15s   0.00ns   33.15s
>            'default_lp':         1 [   1.63m,    1.63m]    1.63m   0.00ns    1.63m         1 [  42.76s,   42.76s]   42.76s   0.00ns   42.76s
>      'feasibility_pump':       356 [ 22.26us,    1.87s]   5.98ms  99.13ms    2.13s       343 [ 18.00ns,  18.00ns]  18.00ns   0.00ns   6.17us
>                    'fj':         2 [598.23ms,    1.41s]    1.01s 408.38ms    2.01s         2 [117.64ms, 117.64ms] 117.64ms  62.50ns 235.28ms
>                    'fj':         2 [622.49ms,    1.33s] 974.00ms 351.51ms    1.95s         2 [120.98ms, 123.84ms] 122.41ms   1.43ms 244.83ms
>             'fs_random':         1 [   4.51s,    4.51s]    4.51s   0.00ns    4.51s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   4.68s,    4.68s]    4.68s   0.00ns    4.68s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         3 [   5.98s,   17.71s]   12.94s    5.03s   38.82s         3 [ 12.33ms, 100.18ms]  70.87ms  41.39ms 212.62ms
>         'graph_cst_lns':         7 [   1.94s,   14.33s]    5.43s    3.81s   38.01s         6 [ 10.00ns, 100.55ms]  17.47ms  37.19ms 104.80ms
>         'graph_dec_lns':         9 [   1.91s,    5.36s]    4.15s    1.06s   37.39s         8 [ 10.00ns,  10.00ns]  10.00ns   0.00ns  80.00ns
>         'graph_var_lns':         3 [   6.15s,   18.63s]   12.68s    5.11s   38.04s         3 [ 28.81ms, 104.93ms]  78.06ms  34.87ms 234.17ms
>                    'ls':       102 [173.61ms,    1.69s] 361.16ms 197.34ms   36.84s       102 [ 97.40ms, 105.13ms] 100.41ms   1.01ms   10.24s
>                'ls_lin':       106 [ 87.31ms,    1.09s] 334.50ms 136.17ms   35.46s       106 [ 25.10ms, 103.03ms]  99.60ms   7.29ms   10.56s
>                'max_lp':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [   7.45s,    7.45s]    7.45s   0.00ns    7.45s
>                 'no_lp':         1 [   1.63m,    1.63m]    1.63m   0.00ns    1.63m         1 [  43.11s,   43.11s]   43.11s   0.00ns   43.11s
>          'pseudo_costs':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [   7.50s,    7.50s]    7.50s   0.00ns    7.50s
>         'quick_restart':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  34.16s,   34.16s]   34.16s   0.00ns   34.16s
>   'quick_restart_no_lp':         1 [   1.61m,    1.61m]    1.61m   0.00ns    1.61m         1 [  36.04s,   36.04s]   36.04s   0.00ns   36.04s
>         'reduced_costs':         1 [   1.63m,    1.63m]    1.63m   0.00ns    1.63m         1 [   4.85s,    4.85s]    4.85s   0.00ns    4.85s
>             'rins/rens':         3 [  25.35s,   25.64s]   25.49s 121.29ms    1.27m         3 [100.12ms, 100.18ms] 100.16ms  30.14us 300.49ms
>           'rnd_cst_lns':        11 [   1.49s,    4.58s]    3.42s 896.53ms   37.66s        10 [ 10.00ns,  10.00ns]  10.00ns   0.00ns 100.00ns
>           'rnd_var_lns':        15 [   1.22s,    4.61s]    2.77s    1.10s   41.60s        11 [ 10.00ns,  10.00ns]  10.00ns   0.00ns 110.00ns
> 
> Search stats                Bools  Conflicts  Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  495'646      1'613    83'558     2'549  234'474'167         79'539
>            'default_lp':  495'252      7'939    49'211     2'084  157'664'417        474'532
>             'fs_random':  495'252          0     1'190     1'190    9'633'061          1'800
>       'fs_random_no_lp':  495'252          0     1'190     1'190    9'633'061          1'800
>                'max_lp':  495'252        467    22'314     1'683   36'562'095     36'285'026
>                 'no_lp':  495'252     12'036    35'134     1'650  135'747'647        618'582
>          'pseudo_costs':  495'252        422    22'295     1'685   36'417'115     35'857'442
>         'quick_restart':  495'252      2'716   191'272     2'359  224'406'469        197'083
>   'quick_restart_no_lp':  495'252      2'778   207'692     2'451  226'616'862        205'593
>         'reduced_costs':  495'252         98    22'414     1'696   29'699'099     29'618'351
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':         1'060      23'613     187'375             0         1       825      30'030         0        239        9'221        0
>            'default_lp':         6'819     279'505   2'476'826             0        13       883      33'487         0        245       10'114        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':           366      13'779     168'709             0         0       488      17'894         0        127        4'695        0
>                 'no_lp':         9'952     478'269   4'471'694     1'740'220         3       454      17'534         0        124        4'907        0
>          'pseudo_costs':           361      13'315     156'727             0         1       490      17'906         0        128        4'701        0
>         'quick_restart':         1'841      69'790     703'820             0         4       917      35'227         0        226        9'016        0
>   'quick_restart_no_lp':         1'891      72'358     699'104             0         9     1'001      36'576         0        284       11'071        0
>         'reduced_costs':            96       3'298      24'413             0         0       503      18'049         0        149        5'725        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          1           0          0      249        0        0
>       'fs_random':          1           0          0        0        0        0
>          'max_lp':          1      10'231        741      131      745        0
>    'pseudo_costs':          1      10'390        777      157      737        0
>   'quick_restart':          1           0          0      339        0        0
>   'reduced_costs':          1      10'913        581      151      824        0
> 
> Lp dimension              Final dimension of first component
>      'default_lp':              0 rows, 2 columns, 0 entries
>       'fs_random':              0 rows, 2 columns, 0 entries
>          'max_lp':  6390 rows, 495252 columns, 19010 entries
>    'pseudo_costs':  6154 rows, 495252 columns, 18296 entries
>   'quick_restart':              0 rows, 2 columns, 0 entries
>   'reduced_costs':  7547 rows, 495252 columns, 21980 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0      10         0  11'724           0
>    'pseudo_costs':          0            0       2         0  13'314           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0      43         0   6'151           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened   Cuts/Call
>      'default_lp':            1        0        0       0          0      0             0         0/0
>       'fs_random':            1        0        0       0          0      0             0         0/0
>          'max_lp':    1'283'942        9    2'881     127      1'105      0            12   741/9'405
>    'pseudo_costs':    1'283'970       26    2'881     135      1'105      0            27  777/10'423
>   'quick_restart':            1        0        0       0          0      0             0         0/0
>   'reduced_costs':    1'283'826       13    1'221      83        681      0             3   581/6'489
> 
> Lp Cut           max_lp  pseudo_costs  reduced_costs
>          CG_FF:     111           106             65
>           CG_K:       -             1              1
>           CG_R:       5             7              2
>         Clique:     137           150             88
>      MIR_1_RLT:     100            80             63
>       MIR_3_FF:      87            94             72
>       MIR_4_FF:      35            40             26
>        MIR_4_R:       1             -              -
>       MIR_5_FF:       5            11              6
>       MIR_6_FF:       3             8              3
>   ZERO_HALF_FF:     205           227            214
>    ZERO_HALF_R:      52            53             41
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':           0/3     33%    3.59e-01       0.10
>   'graph_cst_lns':           0/6     83%    9.16e-01       0.10
>   'graph_dec_lns':           0/8    100%    9.76e-01       0.10
>   'graph_var_lns':           0/3     33%    3.59e-01       0.10
>       'rins/rens':           3/3      0%    1.24e-01       0.10
>     'rnd_cst_lns':          1/10    100%    9.86e-01       0.10
>     'rnd_var_lns':          0/11    100%    9.89e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1    21'804         0              0          0              2        273'739
>                        'fj_restart_decay':        1                  1    22'635         0              0          0              1        251'541
>               'fj_restart_decay_compound':        1                  1         0    13'230         13'222          4              0        418'031
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0    13'064         13'064          0              0        406'357
>                          'ls_lin_restart':       16                 10   305'386         0              0          0         11'353      2'511'115
>                 'ls_lin_restart_compound':       18                 10         0     9'144              6      4'568              4     12'555'908
>         'ls_lin_restart_compound_perturb':       11                  7         0     5'684             13      2'833              2      7'653'410
>                    'ls_lin_restart_decay':       12                 10   461'917         0              0          0          1'018      1'548'096
>           'ls_lin_restart_decay_compound':        7                  5         0     3'140              0      1'570              0      4'388'137
>   'ls_lin_restart_decay_compound_perturb':       21                 13         0    10'902             17      5'442              7     14'648'939
>            'ls_lin_restart_decay_perturb':       14                  7   466'813         0              0          0            742      2'640'435
>                  'ls_lin_restart_perturb':        7                  7    96'714         0              0          0          7'712      1'259'521
>                              'ls_restart':       15                 11   265'814         0              0          0         10'285      2'713'854
>                     'ls_restart_compound':       12                  8         0     6'100             21      3'038              0      8'392'821
>             'ls_restart_compound_perturb':       20                 11         0    10'189              4      5'092              4     13'964'056
>                        'ls_restart_decay':       16                  7   476'665         0              0          0            712      3'582'077
>               'ls_restart_decay_compound':       10                  9         0     5'029              0      2'514              0      7'009'754
>       'ls_restart_decay_compound_perturb':       10                  5         0     5'189              0      2'594              0      7'003'505
>                'ls_restart_decay_perturb':       10                  7   355'778         0              0          0            713      1'485'920
>                      'ls_restart_perturb':        9                  8   129'991         0              0          0          8'216      1'628'503
> 
> Solutions (9)             Num   Rank
>                 'no_lp':    1  [2,2]
>          'pseudo_costs':    1  [8,8]
>         'quick_restart':    4  [3,7]
>   'quick_restart_no_lp':    3  [1,9]
> 
> Objective bounds     Num
>        'bool_core':   17
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     18      233       17
>    'fj solution hints':      0        0        0
>         'lp solutions':     22        0       22
>                 'pump':    355        3
> 
> Improving bounds shared    Num  Sym
>                   'core':   49    0
>    'quick_restart_no_lp':  256    0
> 
> Clauses shared                Num
>                  'core':      480
>            'default_lp':  121'537
>                 'no_lp':      542
>          'pseudo_costs':    5'659
>         'quick_restart':       19
>   'quick_restart_no_lp':  137'607
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 137
> best_bound: 17
> integers: 267
> booleans: 495252
> conflicts: 0
> branches: 1190
> propagations: 9633061
> integer_propagations: 1800
> restarts: 1190
> lp_iterations: 0
> walltime: 121.91
> usertime: 121.91
> deterministic_time: 240.995
> gap_integral: 1108.33
> solution_fingerprint: 0xbd0f9022eec6c73c
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
> Initial optimization model '': (model_fingerprint: 0x9ebdd9df53298c9)
> #Variables: 570 (#bools: 190 in objective) (380 primary variables)
>   - 190 Booleans in [0,1]
>   - 190 in [0,18]
>   - 190 in [0,19]
> #kAutomaton: 10
> #kLinear1: 380 (#enforced: 190)
> #kLinear2: 190 (#enforced: 190)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   9.87e-05s  0.00e+00d  [DetectDominanceRelations] 
>   1.95e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.40e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.23e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   5.73e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=24'747 
> [Symmetry] Graph for symmetry has 74'771 nodes and 190'840 arcs.
> [Symmetry] Symmetry computation done. time: 0.0161939 dtime: 0.0304498
> [Symmetry] #generators: 170, average support size: 4.56471
> [Symmetry] The model contains 10 duplicate constraints !
> [Symmetry] 83 orbits on 390 variables with sizes: 100,10,10,9,8,7,7,7,5,5,...
> [Symmetry] Found orbitope of size 11 x 2
> [SAT presolve] num removable Booleans: 486 / 19760
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:53187 literals:132403 vars:19563 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00283411s] clauses:53177 literals:132373 vars:19563 one_side_vars:0 simple_definition:11 singleton_clauses:0
> [SAT presolve] [0.00362908s] clauses:53161 literals:132373 vars:19555 one_side_vars:0 simple_definition:11 singleton_clauses:0
>   1.19e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.37e-01s  1.00e+00d *[Probe] #probed=11'800 #equiv=27 #new_binary_clauses=4'588 
>   1.54e-01s  5.08e-01d  [MaxClique] Merged 39'563(79'126 literals) into 13'506(52'955 literals) at_most_ones. 
>   1.03e-02s  0.00e+00d  [DetectDominanceRelations] 
>   4.78e-03s  0.00e+00d  [DetectDominanceRelations] 
>   3.66e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=4 #num_dual_strengthening=2 
>   3.95e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.27e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=52 
>   1.07e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.99e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   4.49e-04s  0.00e+00d  [DetectDifferentVariables] 
>   1.37e-02s  5.42e-04d  [ProcessSetPPC] #relevant_constraints=28'763 #num_inclusions=13'514 
>   1.03e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.55e-03s  4.48e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   5.77e-04s  3.61e-04d  [FindBigVerticalLinearOverlap] 
>   8.14e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.19e-03s  6.80e-07d  [MergeClauses] #num_collisions=8 #num_merges=8 #num_saved_literals=24 
>   3.72e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.27e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.74e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.20e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.69e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   9.84e-04s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=1 
> [Symmetry] Graph for symmetry has 36'611 nodes and 73'168 arcs.
> [Symmetry] Symmetry computation done. time: 0.00729813 dtime: 0.015708
> [Symmetry] #generators: 5, average support size: 56.8
> [Symmetry] 73 orbits on 215 variables with sizes: 3,3,3,3,3,3,3,3,3,3,...
> [Symmetry] Found orbitope of size 4 x 3
> [SAT presolve] num removable Booleans: 0 / 19507
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:40 literals:136 vars:40 one_side_vars:0 simple_definition:40 singleton_clauses:0
> [SAT presolve] [3.3233e-05s] clauses:40 literals:136 vars:40 one_side_vars:0 simple_definition:40 singleton_clauses:0
> [SAT presolve] [0.000199679s] clauses:40 literals:136 vars:40 one_side_vars:0 simple_definition:40 singleton_clauses:0
>   1.34e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.69e-01s  1.00e+00d *[Probe] #probed=7'817 #fixed_bools=226 #equiv=184 #new_binary_clauses=5'980 
>   9.56e-04s  1.23e-04d  [MaxClique] 
>   3.75e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.21e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.17e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.14e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=189 
>   9.72e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   6.97e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.01e-04s  0.00e+00d  [DetectDifferentVariables] 
>   5.97e-03s  2.18e-04d  [ProcessSetPPC] #relevant_constraints=14'943 
>   7.19e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.87e-03s  4.34e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   8.39e-04s  3.54e-04d  [FindBigVerticalLinearOverlap] 
>   6.84e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.15e-03s  6.80e-07d  [MergeClauses] #num_collisions=8 #num_merges=8 #num_saved_literals=24 
>   3.71e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.20e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.70e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.21e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.75e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   1.02e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 36'235 nodes and 71'719 arcs.
> [Symmetry] Symmetry computation done. time: 0.00777772 dtime: 0.0157181
> [Symmetry] #generators: 54, average support size: 17.6667
> [Symmetry] 171 orbits on 612 variables with sizes: 12,12,12,12,9,9,9,9,8,8,...
> [Symmetry] Found orbitope of size 4 x 7
> [SAT presolve] num removable Booleans: 0 / 19097
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:49 literals:154 vars:57 one_side_vars:17 simple_definition:40 singleton_clauses:0
> [SAT presolve] [3.3574e-05s] clauses:49 literals:154 vars:57 one_side_vars:17 simple_definition:40 singleton_clauses:0
> [SAT presolve] [0.000204409s] clauses:49 literals:154 vars:57 one_side_vars:17 simple_definition:40 singleton_clauses:0
>   1.32e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.65e-01s  1.00e+00d *[Probe] #probed=10'040 #equiv=18 #new_binary_clauses=6'190 
>   9.12e-04s  1.24e-04d  [MaxClique] 
>   3.91e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.26e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   4.85e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.16e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=15 
>   8.91e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.52e-04s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   5.81e-04s  0.00e+00d  [DetectDifferentVariables] 
>   6.24e-03s  2.18e-04d  [ProcessSetPPC] #relevant_constraints=14'928 
>   6.97e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   4.85e-03s  4.30e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   8.34e-04s  3.54e-04d  [FindBigVerticalLinearOverlap] 
>   6.75e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.13e-03s  6.80e-07d  [MergeClauses] #num_collisions=8 #num_merges=8 #num_saved_literals=24 
>   3.67e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.17e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.17e-02s  0.00e+00d  [ExpandObjective] #entries=425'190 #tight_variables=70'373 #tight_constraints=14'879 #expands=200 
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
>   - rule 'linear1: x in domain' was applied 190 times.
>   - rule 'linear: always true' was applied 370 times.
>   - rule 'linear: enforcement literal in expression' was applied 370 times.
>   - rule 'linear: fixed or dup variables' was applied 370 times.
>   - rule 'linear: remapped using affine relations' was applied 2'270 times.
>   - rule 'new_bool: automaton expansion' was applied 19'570 times.
>   - rule 'objective: expanded via tight equality' was applied 200 times.
>   - rule 'objective: shifted cost with exactly ones' was applied 190 times.
>   - rule 'objective: variable not used elsewhere' was applied 10 times.
>   - rule 'presolve: 427 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 13'505 times.
>   - rule 'setppc: removed dominated constraints' was applied 9 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 190 times.
>   - rule 'variables: detect half reified value encoding' was applied 380 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x265abff00cf87ccc)
> #Variables: 19'079 (#bools: 236 in objective) (7'935 primary variables)
>   - 19'079 Booleans in [0,1]
> #kBoolAnd: 16 (#enforced: 16 #multi: 8) (#literals: 57)
> #kBoolOr: 24 (#literals: 72)
> #kExactlyOne: 14'879 (#literals: 70'373)
> [Symmetry] Graph for symmetry has 35'159 nodes and 71'672 arcs.
> [Symmetry] Symmetry computation done. time: 0.00738587 dtime: 0.0153355
> [Symmetry] #generators: 50, average support size: 16.48
> [Symmetry] 173 orbits on 561 variables with sizes: 8,8,8,8,8,8,8,8,7,7,...
> [Symmetry] Found orbitope of size 4 x 7
> 
> Preloading model.
> #Bound   1.41s best:inf   next:[0,180]    initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model   1.41s var:19079/19079 constraints:14919/14919
> 
> Starting search at 1.42s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp_sym, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1       2.29s best:162   next:[0,161]    core
> #2       2.32s best:161   next:[0,160]    no_lp [hint]
> #3       2.37s best:160   next:[0,159]    quick_restart_no_lp [hint]
> #4       2.42s best:142   next:[0,141]    graph_cst_lns (d=5.00e-01 s=36 t=0.10 p=0.00 stall=0 h=base) [hint]
> #5       2.44s best:130   next:[0,129]    graph_arc_lns (d=5.00e-01 s=35 t=0.10 p=0.00 stall=0 h=base)
> #6       2.44s best:112   next:[0,111]    graph_arc_lns (d=5.00e-01 s=35 t=0.10 p=0.00 stall=0 h=base) [combined with: graph_cst_lns (d=5.0...]
> #7       2.45s best:111   next:[0,110]    ls_restart_decay(batch:1 lin{mvs:101 evals:321} #w_updates:25 #perturb:0)
> #8       2.49s best:100   next:[0,99]     graph_var_lns (d=5.00e-01 s=34 t=0.10 p=0.00 stall=0 h=base)
> #9       2.54s best:89    next:[0,88]     default_lp
> #10      2.56s best:74    next:[0,73]     graph_cst_lns (d=7.07e-01 s=43 t=0.10 p=1.00 stall=0 h=base) [hint]
> #11      2.59s best:65    next:[0,64]     graph_arc_lns (d=7.07e-01 s=42 t=0.10 p=1.00 stall=0 h=base)
> #12      2.67s best:64    next:[0,63]     rnd_var_lns (d=8.14e-01 s=48 t=0.10 p=1.00 stall=2 h=base) [hint]
> #Model   2.73s var:18740/19079 constraints:14751/14919
> #Model   2.76s var:18625/19079 constraints:14693/14919
> #13      2.93s best:58    next:[0,57]     graph_arc_lns (d=8.14e-01 s=51 t=0.10 p=1.00 stall=0 h=base)
> #14      3.06s best:56    next:[0,55]     graph_cst_lns (d=8.76e-01 s=59 t=0.10 p=1.00 stall=1 h=base)
> #15      3.27s best:52    next:[0,51]     graph_arc_lns (d=7.21e-01 s=63 t=0.10 p=0.67 stall=0 h=base)
> #Bound   3.97s best:52    next:[1,51]     bool_core (num_cores=1 [size:4 mw:1 d:2] a=231 d=2 fixed=454/19081 clauses=12'829)
> #Bound   4.01s best:52    next:[2,51]     bool_core (num_cores=2 [size:4 mw:1 d:2] a=228 d=2 fixed=454/19086 clauses=12'834)
> #Bound   4.05s best:52    next:[3,51]     bool_core (num_cores=3 [size:4 mw:1 d:2] a=225 d=2 fixed=454/19091 clauses=12'839)
> #16      4.07s best:51    next:[3,50]     graph_var_lns (d=6.38e-01 s=90 t=0.10 p=0.57 stall=3 h=base)
> #Bound   4.08s best:51    next:[4,50]     bool_core (num_cores=4 [size:4 mw:1 d:2] a=222 d=2 fixed=454/19096 clauses=12'844)
> #Bound   4.12s best:51    next:[5,50]     bool_core (num_cores=5 [size:4 mw:1 d:2] a=219 d=2 fixed=454/19101 clauses=12'849)
> #Bound   4.16s best:51    next:[6,50]     bool_core (num_cores=6 [size:4 mw:1 d:2] a=216 d=2 fixed=454/19106 clauses=12'854)
> #Bound   4.21s best:51    next:[7,50]     bool_core (num_cores=7 [size:5 mw:1 d:3] a=212 d=3 fixed=454/19112 clauses=12'860)
> #Bound   4.25s best:51    next:[8,50]     bool_core (num_cores=8 [size:5 mw:1 d:3] a=208 d=3 fixed=454/19119 clauses=12'867)
> #Bound   4.29s best:51    next:[9,50]     bool_core (num_cores=9 [size:4 mw:1 d:2] a=205 d=3 fixed=454/19125 clauses=12'875)
> #Bound   4.33s best:51    next:[10,50]    bool_core (num_cores=10 [size:4 mw:1 d:2] a=202 d=3 fixed=454/19130 clauses=12'880)
> #Bound   4.36s best:51    next:[11,50]    bool_core (num_cores=11 [size:4 mw:1 d:2] a=199 d=3 fixed=454/19135 clauses=12'885)
> #Bound   4.40s best:51    next:[12,50]    bool_core (num_cores=12 [size:4 mw:1 d:2] a=196 d=3 fixed=454/19140 clauses=12'890)
> #Bound   4.45s best:51    next:[13,50]    bool_core (num_cores=13 [size:6 mw:1 d:3] a=191 d=3 fixed=454/19147 clauses=12'897)
> #Bound   4.49s best:51    next:[14,50]    bool_core (num_cores=14 [size:4 mw:1 d:2] a=188 d=3 fixed=454/19154 clauses=12'904)
> #Bound   4.53s best:51    next:[15,50]    bool_core (num_cores=15 [size:4 mw:1 d:2] a=185 d=3 fixed=454/19159 clauses=12'912)
> #Bound   4.58s best:51    next:[16,50]    bool_core (num_cores=16 [size:4 mw:1 d:2] a=182 d=3 fixed=454/19164 clauses=12'918)
> #Bound   4.61s best:51    next:[17,50]    bool_core (num_cores=17 [size:4 mw:1 d:2] a=179 d=3 fixed=454/19169 clauses=12'924)
> #Bound   4.66s best:51    next:[18,50]    bool_core (num_cores=18 [size:5 mw:1 d:3] a=175 d=3 fixed=454/19175 clauses=12'932)
> #Bound   4.71s best:51    next:[19,50]    bool_core (num_cores=19 [size:6 mw:1 d:3] a=170 d=3 fixed=454/19183 clauses=12'940)
> #Bound   4.74s best:51    next:[20,50]    bool_core (num_cores=20 [size:4 mw:1 d:2] a=167 d=3 fixed=454/19190 clauses=12'948)
> #Bound   4.83s best:51    next:[21,50]    bool_core (num_cores=21 [size:12 mw:1 amo:2 lit:10 d:3] a=157 d=3 fixed=454/19197 clauses=12'957)
> #Bound   4.87s best:51    next:[22,50]    bool_core (num_cores=22 [size:5 mw:1 d:3] a=153 d=3 fixed=454/19203 clauses=12'963)
> #Bound   4.92s best:51    next:[23,50]    bool_core (num_cores=23 [size:6 mw:1 d:3] a=148 d=3 fixed=454/19211 clauses=12'971)
> #Bound   4.97s best:51    next:[24,50]    bool_core (num_cores=24 [size:5 mw:1 d:3] a=144 d=3 fixed=454/19219 clauses=12'979)
> #Bound   5.04s best:51    next:[25,50]    bool_core (num_cores=25 [size:11 mw:1 amo:1 lit:7 d:4] a=136 d=4 fixed=454/19227 clauses=12'992)
> #17      5.98s best:50    next:[36,49]    graph_cst_lns (d=9.17e-01 s=140 t=0.10 p=0.70 stall=5 h=base)
> #Bound   5.82s best:51    next:[36,50]    bool_core (num_cores=36 [size:5 mw:1 d:8] a=82 d=8 fixed=454/19346 clauses=13'388) [skipped_logs=10]
> #Bound   6.45s best:50    next:[38,49]    bool_core (num_cores=38 [size:5 mw:1 d:7] a=73 d=9 fixed=454/19398 clauses=14'137) [skipped_logs=1]
> #Bound   7.24s best:50    next:[39,49]    bool_core (num_cores=39 [size:3 mw:1 d:8] a=71 d=9 fixed=454/19425 clauses=14'916) [skipped_logs=0]
> #Bound  11.30s best:50    next:[40,49]    bool_core (num_cores=40 [size:2 mw:1 d:10] a=70 d=10 fixed=454/19447 clauses=19'759)
> #18     11.57s best:49    next:[40,48]    quick_restart_no_lp
> #19     13.50s best:48    next:[40,47]    graph_arc_lns (d=6.46e-01 s=343 t=0.10 p=0.51 stall=7 h=base)
> #Bound  16.85s best:48    next:[41,47]    bool_core (num_cores=41 [size:1 mw:1] a=70 d=10 fixed=454/19484 clauses=24'950)
> #Bound  37.45s best:48    next:[42,47]    bool_core (num_cores=42 [size:4 mw:1 d:11] a=67 d=11 fixed=455/19515 clauses=36'624)
> #Bound  65.14s best:48    next:[43,47]    bool_core (num_cores=43 [size:10 mw:1 d:12] a=58 d=12 fixed=455/19555 clauses=42'057)
> #Model  85.88s var:18288/19079 constraints:14527/14919
> #Bound 103.60s best:48    next:[44,47]    bool_core (num_cores=44 [size:19 mw:1 amo:4 lit:13 d:13] a=43 d=13 fixed=455/19606 clauses=47'934)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.33m,    1.33m]    1.33m   0.00ns    1.33m
>            'default_lp':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.38m,    1.38m]    1.38m   0.00ns    1.38m
>      'feasibility_pump':       520 [ 23.51us, 167.22ms] 418.72us   7.32ms 217.73ms       513 [  1.19us,   1.19us]   1.19us   0.00ns 609.44us
>                    'fj':         4 [164.68ms, 215.24ms] 183.80ms  20.21ms 735.20ms         4 [100.67ms, 100.67ms] 100.67ms 915.59ns 402.68ms
>                    'fj':         5 [110.21ms, 205.56ms] 168.03ms  32.35ms 840.17ms         5 [100.67ms, 100.96ms] 100.73ms 116.48us 503.63ms
>             'fs_random':         1 [874.04ms, 874.04ms] 874.04ms   0.00ns 874.04ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [900.05ms, 900.05ms] 900.05ms   0.00ns 900.05ms         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':       355 [ 36.85ms, 292.89ms] 146.76ms  54.50ms   52.10s       355 [ 10.00ns, 113.29ms]  59.43ms  48.64ms   21.10s
>         'graph_cst_lns':       251 [ 39.91ms, 550.62ms] 210.31ms  76.61ms   52.79s       251 [ 10.00ns, 108.59ms]  59.89ms  47.01ms   15.03s
>         'graph_dec_lns':       197 [ 56.65ms, 605.14ms] 265.68ms 101.60ms   52.34s       197 [ 10.00ns, 106.62ms]  63.05ms  44.25ms   12.42s
>         'graph_var_lns':       362 [ 26.32ms, 282.69ms] 143.43ms  57.42ms   51.92s       362 [ 10.00ns, 113.40ms]  62.01ms  47.72ms   22.45s
>                    'ls':       313 [ 14.32ms, 281.38ms] 166.07ms  38.55ms   51.98s       313 [300.04us, 100.28ms]  99.49ms   7.02ms   31.14s
>                'ls_lin':       312 [ 91.67ms, 287.01ms] 166.77ms  39.11ms   52.03s       312 [100.00ms, 100.33ms] 100.06ms  67.61us   31.22s
>            'max_lp_sym':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  46.64s,   46.64s]   46.64s   0.00ns   46.64s
>                 'no_lp':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.28m,    1.28m]    1.28m   0.00ns    1.28m
>          'pseudo_costs':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  31.33s,   31.33s]   31.33s   0.00ns   31.33s
>         'quick_restart':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [   1.16m,    1.16m]    1.16m   0.00ns    1.16m
>   'quick_restart_no_lp':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  57.78s,   57.78s]   57.78s   0.00ns   57.78s
>         'reduced_costs':         1 [   1.98m,    1.98m]    1.98m   0.00ns    1.98m         1 [  31.39s,   31.39s]   31.39s   0.00ns   31.39s
>             'rins/rens':       221 [  8.43ms, 623.91ms] 237.05ms 148.44ms   52.39s       169 [ 10.00ns, 101.31ms]  66.02ms  45.35ms   11.16s
>           'rnd_cst_lns':       211 [ 44.29ms, 593.28ms] 247.29ms  87.83ms   52.18s       211 [ 10.00ns, 106.68ms]  63.13ms  43.26ms   13.32s
>           'rnd_var_lns':       214 [ 42.45ms, 577.84ms] 248.48ms 106.48ms   53.17s       208 [ 10.00ns, 106.55ms]  59.54ms  45.08ms   12.38s
> 
> Search stats               Bools  Conflicts   Branches  Restarts   BoolPropag  IntegerPropag
>                  'core':  19'646     99'419    418'737    87'756  506'294'398      1'306'324
>            'default_lp':  19'079    253'414    728'605   136'467  367'218'434     14'959'879
>             'fs_random':  19'079          0      9'658     9'658    8'703'364         64'849
>       'fs_random_no_lp':  19'079          0      9'658     9'658    8'703'364         64'849
>            'max_lp_sym':  19'079      1'771    196'168    73'817   51'584'398     47'575'215
>                 'no_lp':  19'079    204'749    623'255   132'566  339'152'889     12'082'198
>          'pseudo_costs':  19'079      7'932    203'732    73'830   58'621'549     51'738'236
>         'quick_restart':  19'079     89'704  1'122'189   117'330  324'850'869      7'890'434
>   'quick_restart_no_lp':  19'079     75'156    937'769    94'809  273'945'190      6'331'587
>         'reduced_costs':  19'079      4'279    145'860    52'462   40'368'493     38'454'091
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        93'550   3'664'259   4'434'046     2'432'419       159    16'235      84'092         0      2'617       54'342    3'866
>            'default_lp':       205'133   3'435'698  26'479'955    25'106'465       301    40'165     151'705         0      3'334       28'084   10'784
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>            'max_lp_sym':         1'677      27'776     134'339             0         4    21'636      80'377         0      2'207       16'434    5'610
>                 'no_lp':       166'615   2'594'644  24'659'070    22'683'724       368    35'417     122'081         0      2'941       22'134    9'690
>          'pseudo_costs':         7'720     287'314   1'256'699             0         1    20'842      79'920         0      2'277       17'069    5'181
>         'quick_restart':        62'215     849'050   7'717'757     5'830'112       417    23'893     135'735         0      3'298       43'272    5'639
>   'quick_restart_no_lp':        51'530     659'838   6'250'349     4'892'204       420    17'070     119'825         0      2'616       42'178    3'999
>         'reduced_costs':         4'146     198'777     781'584             0         1    13'933      51'271         0      1'586       11'787    3'565
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         13           0          0  725'812        0        0
>       'fs_random':         13           0          0        0        0        0
>      'max_lp_sym':          1      80'052        831        5    5'186        0
>    'pseudo_costs':          1     189'887      1'879      300   18'007        0
>   'quick_restart':         13           0          0  327'375        0        0
>   'reduced_costs':          1     157'923      1'049      192   14'753        0
> 
> Lp dimension              Final dimension of first component
>      'default_lp':              0 rows, 2 columns, 0 entries
>       'fs_random':              0 rows, 2 columns, 0 entries
>      'max_lp_sym':  14412 rows, 18691 columns, 78856 entries
>    'pseudo_costs':   7770 rows, 19079 columns, 31910 entries
>   'quick_restart':              0 rows, 2 columns, 0 entries
>   'reduced_costs':   8903 rows, 19079 columns, 37231 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow      Bad  BadScaling
>      'default_lp':          0            0       0         0        0           0
>       'fs_random':          0            0       0         0        0           0
>      'max_lp_sym':          0            0   5'190         0  319'357           0
>    'pseudo_costs':          0            0  12'074         0   56'971           0
>   'quick_restart':          0            0       0         0        0           0
>   'reduced_costs':          0            0  13'503         0   33'224           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':           33        0       39       0          3      0             0          0/0
>       'fs_random':           33        0        0       0          0      0             0          0/0
>      'max_lp_sym':       15'319      220      905       0        679      2             1    831/2'059
>    'pseudo_costs':       16'799        3    3'631       0      1'605      0             0  1'879/4'819
>   'quick_restart':           33        0       90       0          3      0             0          0/0
>   'reduced_costs':       15'969        5    2'261       0        688      0             2  1'049/2'505
> 
> Lp Cut           max_lp_sym  reduced_costs  pseudo_costs
>          CG_FF:          28            119           144
>           CG_K:          10             12             8
>           CG_R:          35             24            13
>         Clique:          33            131           151
>      MIR_1_RLT:           -            170           336
>       MIR_3_FF:           -              8             2
>       MIR_4_FF:           -              7             -
>       MIR_5_FF:           1              1             2
>       MIR_6_FF:           5              1             1
>   ZERO_HALF_FF:         390            439           921
>    ZERO_HALF_K:           1              -             -
>    ZERO_HALF_R:         328            137           301
> 
> LNS stats           Improv/Calls  Closed  Difficulty  TimeLimit
>   'graph_arc_lns':         6/355     50%    5.20e-01       0.11
>   'graph_cst_lns':         5/251     51%    9.26e-01       0.11
>   'graph_dec_lns':         1/197     53%    9.89e-01       0.11
>   'graph_var_lns':         3/362     50%    4.74e-01       0.11
>       'rins/rens':        42/207     50%    9.25e-01       0.10
>     'rnd_cst_lns':         1/211     53%    9.88e-01       0.11
>     'rnd_var_lns':         1/208     53%    9.89e-01       0.11
> 
> LS stats                                    Batches  Restarts/Perturbs   LinMoves   GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1     76'317          0              0          0            354         18'758
>                        'fj_restart_decay':        1                  1     77'191          0              0          0             86         19'023
>               'fj_restart_decay_compound':        2                  2          0     92'128         26'050     33'010             10        992'991
>   'fj_restart_decay_compound_perturb_obj':        2                  2          0     91'339         28'167     31'575             11        992'902
>                'fj_restart_decay_perturb':        2                  2    158'653          0              0          0            232         38'071
>                  'fj_restart_perturb_obj':        1                  1     74'959          0              0          0            406         18'561
>                          'ls_lin_restart':       38                 17  2'843'597          0              0          0         37'579        534'660
>                 'ls_lin_restart_compound':       27                 17          0    817'903         43'377    387'223          4'479     12'449'104
>         'ls_lin_restart_compound_perturb':       22                 19          0    657'536         24'477    316'465          4'487     10'126'858
>                    'ls_lin_restart_decay':       27                 16  2'072'140          0              0          0          3'874        527'008
>           'ls_lin_restart_decay_compound':       39                 19          0  1'140'615        200'469    469'955          1'092     17'214'387
>   'ls_lin_restart_decay_compound_perturb':       50                 20          0  1'551'596        336'097    607'659          1'193     22'201'676
>            'ls_lin_restart_decay_perturb':       74                 22  5'686'650          0              0          0          9'177      1'525'644
>                  'ls_lin_restart_perturb':       35                 19  2'599'767          0              0          0         36'484        502'851
>                              'ls_restart':       26                 19  1'939'174          0              0          0         28'119        422'655
>                     'ls_restart_compound':       44                 17          0  1'466'104         86'468    689'781          6'169     19'922'676
>             'ls_restart_compound_perturb':       50                 16          0  1'709'659         89'643    809'948          7'170     22'462'968
>                        'ls_restart_decay':       52                 33  3'855'298          0              0          0          7'535        981'819
>               'ls_restart_decay_compound':       39                 15          0  1'192'293        211'032    490'560            920     17'168'212
>       'ls_restart_decay_compound_perturb':       34                 19          0    954'936        203'655    375'570          1'109     15'394'791
>                'ls_restart_decay_perturb':       31                 14  2'375'807          0              0          0          4'171        620'738
>                      'ls_restart_perturb':       37                 16  2'761'440          0              0          0         38'458        491'423
> 
> Solutions (19)            Num     Rank
>                  'core':    1    [1,1]
>            'default_lp':    1    [9,9]
>         'graph_arc_lns':    6   [5,19]
>         'graph_cst_lns':    4   [4,17]
>         'graph_var_lns':    2   [8,16]
>      'ls_restart_decay':    1    [7,7]
>                 'no_lp':    1    [2,2]
>   'quick_restart_no_lp':    2   [3,18]
>           'rnd_var_lns':    1  [12,12]
> 
> Objective bounds     Num
>        'bool_core':   44
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':  1'120    4'072      788
>    'fj solution hints':      1        0        1
>         'lp solutions':    321      102      303
>                 'pump':    519      119
> 
> Improving bounds shared    Num  Sym
>                   'core':  454    0
>          'quick_restart':  337    0
> 
> Clauses shared               Num
>                  'core':  71'421
>            'default_lp':      25
>            'max_lp_sym':      65
>                 'no_lp':     654
>          'pseudo_costs':   2'043
>         'quick_restart':     741
>   'quick_restart_no_lp':     256
>         'reduced_costs':      86
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 48
> best_bound: 44
> integers: 263
> booleans: 19079
> conflicts: 0
> branches: 9658
> propagations: 8703364
> integer_propagations: 64849
> restarts: 9658
> lp_iterations: 0
> walltime: 120.063
> usertime: 120.063
> deterministic_time: 650.314
> gap_integral: 969.922
> solution_fingerprint: 0xca512ad681ed6149
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
> Initial optimization model '': (model_fingerprint: 0x68b50e7caa897b05)
> #Variables: 3'000 (#bools: 1'000 in objective) (2'000 primary variables)
>   - 1'000 Booleans in [0,1]
>   - 1'000 in [0,19]
>   - 1'000 in [0,20]
> #kAutomaton: 50
> #kLinear1: 2'000 (#enforced: 1'000)
> #kLinear2: 1'000 (#enforced: 1'000)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   1.26e-03s  0.00e+00d  [DetectDominanceRelations] 
>   2.23e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   3.91e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   4.31e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   1.04e+00s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=3'166'290 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 54446 / 2389968
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:6154334 literals:15819832 vars:2389035 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [1.1287s] clauses:6154284 literals:15819682 vars:2389035 one_side_vars:0 simple_definition:51 singleton_clauses:0
> [SAT presolve] [1.31643s] clauses:6149756 literals:15819682 vars:2386771 one_side_vars:0 simple_definition:51 singleton_clauses:0
>   1.71e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.60e+00s  1.03e+00d *[Probe] #probed=2'178 #equiv=3 #new_binary_clauses=57'383 
>   4.30e+00s  9.66e+00d *[MaxClique] Merged 4'821'404(9'642'808 literals) into 4'785'773(9'607'178 literals) at_most_ones. 
>   7.35e-01s  0.00e+00d  [DetectDominanceRelations] 
>   4.02e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   6.19e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.09e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=18 
>   4.95e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   8.59e-02s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   7.36e-02s  0.00e+00d  [DetectDifferentVariables] 
>   2.13e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=6'163'179 #num_inclusions=3'728'080 
>   9.85e-02s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   8.50e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   1.85e-01s  9.03e-02d  [FindBigVerticalLinearOverlap] 
>   7.77e-02s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.13e-01s  3.06e-02d  [MergeClauses] #num_collisions=6'228 #num_merges=6'228 #num_saved_literals=14'720 
>   7.47e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.00e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.46e-01s  0.00e+00d  [DetectDominanceRelations] 
>   1.99e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.34e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   2.11e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=5 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 52179 / 2386663
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:6097673 literals:15679830 vars:2386582 one_side_vars:0 simple_definition:38197 singleton_clauses:0
> [SAT presolve] [1.08051s] clauses:6097673 literals:15679830 vars:2386582 one_side_vars:0 simple_definition:38197 singleton_clauses:0
> [SAT presolve] [1.25839s] clauses:6097673 literals:15679830 vars:2386582 one_side_vars:0 simple_definition:38197 singleton_clauses:0
>   3.41e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.38e+00s  1.03e+00d *[Probe] #probed=1'986 #equiv=508 #new_binary_clauses=58'121 
>   4.59e+00s  9.58e+00d *[MaxClique] Merged 4'777'543(9'555'088 literals) into 4'760'257(9'537'549 literals) at_most_ones. 
>   2.15e+00s  0.00e+00d  [DetectDominanceRelations] 
>   8.01e-01s  0.00e+00d  [DetectDominanceRelations] 
>   5.31e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   6.99e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   6.64e-01s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2'794 
>   8.00e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.17e-01s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.02e-01s  0.00e+00d  [DetectDifferentVariables] 
>   2.19e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=6'134'768 #num_inclusions=3'715'341 
>   1.07e-01s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   8.86e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   2.08e-01s  9.01e-02d  [FindBigVerticalLinearOverlap] 
>   1.11e-01s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   4.62e-01s  3.05e-02d  [MergeClauses] #num_collisions=5'212 #num_merges=5'212 #num_saved_literals=12'688 
>   8.12e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.16e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.07e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.15e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.28e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   3.86e-01s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 51721 / 2386152
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:6073521 literals:15613597 vars:2385823 one_side_vars:216 simple_definition:56818 singleton_clauses:0
> [SAT presolve] [1.06366s] clauses:6073521 literals:15613597 vars:2385823 one_side_vars:216 simple_definition:56818 singleton_clauses:0
> [SAT presolve] [1.25036s] clauses:6073519 literals:15613593 vars:2385822 one_side_vars:216 simple_definition:56817 singleton_clauses:0
>   3.64e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.30e+00s  1.02e+00d *[Probe] #probed=1'986 #new_binary_clauses=57'105 
>   4.88e+00s  9.53e+00d *[MaxClique] Merged 4'756'474(9'513'070 literals) into 4'749'185(9'505'782 literals) at_most_ones. 
>   2.27e+00s  0.00e+00d  [DetectDominanceRelations] 
>   8.63e-01s  0.00e+00d  [DetectDominanceRelations] 
>   5.62e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=2 
>   7.51e-01s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   8.16e-01s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.31e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.49e-01s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.30e-01s  0.00e+00d  [DetectDifferentVariables] 
>   2.27e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=6'125'462 #num_inclusions=3'711'773 
>   1.32e-01s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   8.83e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   2.07e-01s  9.00e-02d  [FindBigVerticalLinearOverlap] 
>   1.40e-01s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.77e-01s  3.04e-02d  [MergeClauses] #num_collisions=5'212 #num_merges=5'212 #num_saved_literals=12'688 
>   8.69e-01s  0.00e+00d  [DetectDominanceRelations] 
>   2.30e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.24e-01s  0.00e+00d  [ExpandObjective] #entries=100'000'057 #tight_variables=1'660'889 #tight_constraints=34'910 
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
>   - rule 'linear1: x in domain' was applied 1'000 times.
>   - rule 'linear: always true' was applied 1'950 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'950 times.
>   - rule 'linear: fixed or dup variables' was applied 1'950 times.
>   - rule 'linear: remapped using affine relations' was applied 51'950 times.
>   - rule 'new_bool: automaton expansion' was applied 2'388'968 times.
>   - rule 'objective: variable not used elsewhere' was applied 5 times.
>   - rule 'presolve: 1015 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'setppc: bool_or in at_most_one.' was applied 12'018 times.
>   - rule 'setppc: removed dominated constraints' was applied 203 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 1'000 times.
>   - rule 'variables: detect half reified value encoding' was applied 2'000 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x34b81eb81b880faf)
> #Variables: 2'386'139 (#bools: 991 in objective) (2'330'991 primary variables)
>   - 2'386'139 Booleans in [0,1]
> #kAtMostOne: 115 (#literals: 345)
> #kBoolAnd: 115'281 (#enforced: 115'281 #multi: 4'247) (#literals: 4'878'428)
> #kBoolOr: 1'305'793 (#literals: 6'056'857)
> #kExactlyOne: 61'025 (#literals: 2'417'310)
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> 
> Preloading model.
> #Bound 104.44s best:inf   next:[0,991]    initial_domain
> The solution hint is complete, but it is infeasible! we will try to repair it.
> #Model 105.57s var:2386139/2386139 constraints:1482214/1482214
> 
> Starting search at 105.72s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 10 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #1     116.33s best:989   next:[0,988]    fs_random_no_lp [hint]
> #Model 116.72s var:2385900/2386139 constraints:1482089/1482214
> #2     118.67s best:988   next:[0,987]    default_lp
> #3     119.46s best:497   next:[0,496]    quick_restart
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  14.95s,   14.95s]   14.95s   0.00ns   14.95s         1 [   2.69s,    2.69s]    2.69s   0.00ns    2.69s
>            'default_lp':         1 [  20.05s,   20.05s]   20.05s   0.00ns   20.05s         1 [   2.00s,    2.00s]    2.00s   0.00ns    2.00s
>      'feasibility_pump':         1 [   5.70s,    5.70s]    5.70s   0.00ns    5.70s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'fj':         1 [   4.68s,    4.68s]    4.68s   0.00ns    4.68s         1 [190.10ms, 190.10ms] 190.10ms   0.00ns 190.10ms
>                    'fj':         5 [687.48ms,    4.95s]    1.67s    1.64s    8.37s         5 [190.10ms, 190.12ms] 190.10ms   9.02us 950.51ms
>             'fs_random':         1 [  10.61s,   10.61s]   10.61s   0.00ns   10.61s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [  10.62s,   10.62s]   10.62s   0.00ns   10.62s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_arc_lns':         1 [   6.14s,    6.14s]    6.14s   0.00ns    6.14s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_cst_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_dec_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_var_lns':         1 [   4.58s,    4.58s]    4.58s   0.00ns    4.58s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'ls':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                'ls_lin':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                'max_lp':         1 [  24.30s,   24.30s]   24.30s   0.00ns   24.30s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                 'no_lp':         1 [  18.83s,   18.83s]   18.83s   0.00ns   18.83s         1 [   2.00s,    2.00s]    2.00s   0.00ns    2.00s
>          'pseudo_costs':         1 [  23.52s,   23.52s]   23.52s   0.00ns   23.52s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'quick_restart':         1 [  20.50s,   20.50s]   20.50s   0.00ns   20.50s         1 [   1.95s,    1.95s]    1.95s   0.00ns    1.95s
>   'quick_restart_no_lp':         1 [  19.50s,   19.50s]   19.50s   0.00ns   19.50s         1 [   2.95s,    2.95s]    2.95s   0.00ns    2.95s
>         'reduced_costs':         1 [  24.30s,   24.30s]   24.30s   0.00ns   24.30s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>             'rins/rens':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>           'rnd_cst_lns':         1 [   4.26s,    4.26s]    4.26s   0.00ns    4.26s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>           'rnd_var_lns':         1 [   4.35s,    4.35s]    4.35s   0.00ns    4.35s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
> 
> Search stats                  Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  2'386'157        197     6'842     2'002  30'164'302          6'018
>            'default_lp':  2'386'139          0     3'905     1'978  13'720'733          9'702
>             'fs_random':  2'386'139          0     2'076     1'976   9'397'204          2'374
>       'fs_random_no_lp':  2'386'139          0     2'966     1'977  11'335'772          5'905
>                'max_lp':  2'386'139          0     1'976     1'976   8'950'623      8'952'600
>                 'no_lp':  2'386'139          0     3'906     1'978  13'720'971          9'700
>          'pseudo_costs':  2'386'139          0     1'976     1'976   8'950'623      8'952'600
>         'quick_restart':  2'386'139          0     3'460     1'978  13'721'178          7'286
>   'quick_restart_no_lp':  2'386'139         11     3'649     1'978  14'268'345          8'321
>         'reduced_costs':  2'386'139          0     1'976     1'976   8'950'623      8'952'600
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':           127       4'319     101'318             0         0         0           0         0          0            0        0
>            'default_lp':             0           0           0             0         0         0           0         0          0            0        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':             0           0           0             0         0         0           0         0          0            0        0
>          'pseudo_costs':             0           0           0             0         0         0           0         0          0            0        0
>         'quick_restart':             0           0           0             0         0         0           0         0          0            0        0
>   'quick_restart_no_lp':             1           1       1'152             0         0         0           0         0          0            0        0
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
>     'rnd_cst_lns':           0/0      0%    5.00e-01       0.10
>     'rnd_var_lns':           0/0      0%    5.00e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1    21'523         0              0          0              0        284'338
>         'fj_restart_compound_perturb_obj':        1                  1         0    20'008         20'007          0              0        196'352
>               'fj_restart_decay_compound':        1                  1         0    19'729         19'729          0              0        194'429
>       'fj_restart_decay_compound_perturb':        1                  1         0    19'748         19'748          0              0        191'518
>   'fj_restart_decay_compound_perturb_obj':        1                  1         0    19'664         19'593          0              0        192'066
>                'fj_restart_decay_perturb':        1                  1    21'482         0              0          0              0        283'632
> 
> Solutions (3)         Num   Rank
>        'default_lp':    1  [2,2]
>   'fs_random_no_lp':    1  [1,1]
>     'quick_restart':    1  [3,3]
> 
> Objective bounds     Num
>   'initial_domain':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':      8        8        6
>    'fj solution hints':      0        0        0
>         'lp solutions':      0        0        0
>                 'pump':      0        0
> 
> Improving bounds shared    Num  Sym
>                   'core':  239    0
> 
> Clauses shared            Num
>                  'core':    1
>   'quick_restart_no_lp':    1
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 497
> best_bound: 0
> integers: 1023
> booleans: 2386139
> conflicts: 0
> branches: 2966
> propagations: 11335772
> integer_propagations: 5905
> restarts: 1977
> lp_iterations: 0
> walltime: 131.837
> usertime: 131.837
> deterministic_time: 48.2503
> gap_integral: 79.8758
> solution_fingerprint: 0xa2b2b053dd4df6b8
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
> Initial optimization model '': (model_fingerprint: 0xc8dc4b595fff8e42)
> #Variables: 1'800 (#bools: 600 in objective) (1'200 primary variables)
>   - 600 Booleans in [0,1]
>   - 600 in [0,5]
>   - 600 in [0,6]
> #kAutomaton: 100
> #kLinear1: 1'200 (#enforced: 600)
> #kLinear2: 600 (#enforced: 600)
> 
> Starting presolve at 0.00s
> The solution hint is complete, but it is infeasible! we will try to repair it.
>   1.33e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.90e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   2.76e-06s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.01e+00s  0.00e+00d  [DetectDuplicateColumns] 
>   2.14e+00s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=4'783'638 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 353801 / 4823320
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:12637846 literals:32489084 vars:4822737 one_side_vars:0 simple_definition:0 singleton_clauses:0
> [SAT presolve] [2.34314s] clauses:12637746 literals:32488784 vars:4822737 one_side_vars:0 simple_definition:100 singleton_clauses:0
> [SAT presolve] [3.22887s] clauses:12556546 literals:32488784 vars:4782137 one_side_vars:0 simple_definition:100 singleton_clauses:0
>   5.18e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   5.31e+00s  1.02e+00d *[Probe] #probed=558 #new_binary_clauses=8'955 
>   1.39e+01s  1.95e+01d *[MaxClique] Merged 9'722'569(19'445'138 literals) into 9'703'667(19'426'237 literals) at_most_ones. 
>   2.21e+00s  0.00e+00d  [DetectDominanceRelations] 
>   8.98e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.25e+00s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.66e+00s  0.00e+00d  [DetectDuplicateConstraints] 
>   1.44e+00s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.64e-01s  0.00e+00d  [DetectDominatedLinearConstraints] 
>   1.41e-01s  0.00e+00d  [DetectDifferentVariables] 
>   4.12e+00s  1.00e-01d  [ProcessSetPPC] #relevant_constraints=12'597'063 #num_inclusions=3'451'802 
>   1.95e-01s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   9.63e-01s  1.00e+00d *[FindBigAtMostOneAndLinearOverlap] 
>   3.73e-01s  1.85e-01d  [FindBigVerticalLinearOverlap] 
>   1.52e-01s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.38e+00s  6.52e-02d  [MergeClauses] #num_collisions=122'624 #num_merges=122'624 #num_saved_literals=285'848 
>   2.42e+00s  0.00e+00d  [DetectDominanceRelations] 
>   5.16e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.43e+00s  0.00e+00d  [DetectDominanceRelations] 
>   5.14e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   7.66e-01s  0.00e+00d  [DetectDuplicateColumns] 
>   6.27e-01s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Problem too large. Skipping. You can use symmetry_level:3 or more to force it.
> [SAT presolve] num removable Booleans: 313201 / 4781963
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:12532284 literals:32440185 vars:4781963 one_side_vars:26 simple_definition:17195 singleton_clauses:0
> [SAT presolve] [2.39768s] clauses:12532284 literals:32440185 vars:4781963 one_side_vars:26 simple_definition:17195 singleton_clauses:0
> [SAT presolve] [3.10949s] clauses:12532284 literals:32440185 vars:4781963 one_side_vars:26 simple_definition:17195 singleton_clauses:0
>   7.25e-01s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   6.26e+00s  1.02e+00d *[Probe] #probed=550 #equiv=272 #new_binary_clauses=8'409 
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
>   - rule 'linear1: x in domain' was applied 600 times.
>   - rule 'linear: always true' was applied 1'100 times.
>   - rule 'linear: enforcement literal in expression' was applied 1'100 times.
>   - rule 'linear: fixed or dup variables' was applied 1'100 times.
>   - rule 'linear: remapped using affine relations' was applied 61'100 times.
>   - rule 'new_bool: automaton expansion' was applied 4'822'720 times.
>   - rule 'objective: variable not used elsewhere' was applied 1 time.
>   - rule 'presolve: 601 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 2 times.
>   - rule 'setppc: removed dominated constraints' was applied 375 times.
>   - rule 'variables: both boolean and its negation fix the same variable' was applied 600 times.
>   - rule 'variables: detect half reified value encoding' was applied 1'200 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x36ed40f78e056b61)
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
> walltime: 128.228
> usertime: 128.228
> deterministic_time: 42.3856
> gap_integral: 0
> ```

presolve が終わらなかった...
