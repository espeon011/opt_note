In [ ]:
```python
import opt_note.scsp as scsp
import hexaly.optimizer
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
class Model:
    def __init__(
        self, instance: list[str], initial_weights: list[list[int]] | None = None
    ):
        chars = "".join(sorted(list(set("".join(instance)))))

        hxoptimizer = hexaly.optimizer.HexalyOptimizer()
        hxmodel = hxoptimizer.model
        assert isinstance(hxoptimizer, hexaly.optimizer.HexalyOptimizer)
        assert isinstance(hxmodel, hexaly.optimizer.HxModel)

        # 重みの最大値は初期重みが与えられた場合は初期重みの最大値の 2 倍,
        # 初期重みが与えられなかった場合は文字種数とする.
        max_weight = (
            max(max(w, len(s)) for s, ws in zip(instance, initial_weights) for w in ws)
            if initial_weights
            else len(chars)
        )
        priorities1d = [
            hxmodel.int(1, max_weight) for s in instance for cidx, _ in enumerate(s)
        ]

        func = hxmodel.create_int_external_function(self.objective)
        func.external_context.lower_bound = 0
        func.external_context.upper_bound = sum(len(s) for s in instance)

        indices_1d_to_2d: list[tuple[int, int]] = []
        counter = 0
        for s in instance:
            indices_1d_to_2d.append((counter, counter + len(s)))
            counter += len(s)

        self.instance = instance
        self.chars = chars
        self.hxoptimizer = hxoptimizer
        self.hxmodel = hxmodel
        self.priorities1d = priorities1d
        self.indices_1d_to_2d = indices_1d_to_2d

        # これらが実行される時点で self.* が必要になるため初期化の最後に移動

        hxmodel.minimize(func(*priorities1d))
        hxmodel.close()

        if initial_weights:
            priorities2d = self.priorities_1d_to_2d(priorities1d)
            for ps, ws in zip(priorities2d, initial_weights):
                for p, w in zip(ps, ws):
                    p.set_value(w)

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        assert isinstance(self.hxoptimizer.param, hexaly.optimizer.HxParam)
        if time_limit is not None:
            self.hxoptimizer.param.time_limit = time_limit
        self.hxoptimizer.param.verbosity = 1 if log else 0
        self.hxoptimizer.solve()
        return self

    def to_solution(self) -> str | None:
        assert isinstance(self.hxoptimizer.solution, hexaly.optimizer.HxSolution)
        status = self.hxoptimizer.solution.status
        if status not in {
            hexaly.optimizer.HxSolutionStatus.OPTIMAL,
            hexaly.optimizer.HxSolutionStatus.FEASIBLE,
        }:
            return None

        priorities1d_value: list[int] = [p.value for p in self.priorities1d]
        priorities2d_value = self.priorities_1d_to_2d(priorities1d_value)
        return self.wmm(priorities2d_value)

    def wmm(self, priorities2d: list[list[int]]) -> str:
        indices = tuple(0 for _ in self.instance)
        solution = ""

        # while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
        for _ in range(len(self.instance) * max(len(s) for s in self.instance)):
            if all(idx == len(s) for idx, s in zip(indices, self.instance)):
                break

            counts = [
                max(
                    [0] + [
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

    def priorities_1d_to_2d[T](self, priorities1d: list[T]) -> list[list[T]]:
        return [priorities1d[start:end] for start, end in self.indices_1d_to_2d]

    def objective(self, priorities1d: list[int]) -> int:
        priorities2d = self.priorities_1d_to_2d(
            [priorities1d[i] for i in range(len(priorities1d))]
        )
        solution = self.wmm(priorities2d)
        return len(solution)
```

In [ ]:
```python
def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
```

In [ ]:
```python
def bench(instance: list[str]) -> None:
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
def bench0(instance: list[str]) -> None:
    model = scsp.model.wmm_hexaly.Model(instance).solve()
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
bench(scsp.example.load("uniform_q26n004k015-025.txt"))
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
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("uniform_q26n004k015-025.txt"))
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 62) ---
>  Sol: tkulcigneycojiqfsovoazpkuhmplxnhtqgbxzrddbxcvsxuqpvissbxrvnngf
> str1: tk----gn---------------kuhmp-xnhtqg-xz------v-x----is---------
> str2: -----i-----ojiqf-o----------l-n----bx-----xcvs-uqpvissbx-----f
> str3: --ulci-n-yco----sovo-zp----pl--------------------p------------
> str4: -----ig-e---------v-az------------gb--rddb-c-s----v-----rvnngf
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n008k015-025.txt"))
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
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("uniform_q26n008k015-025.txt"))
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
> --- Solution (of length 102) ---
>  Sol: ipuyplrogenbdcevadzfxwgbjtinyucvxerdpmqfozkrdbrlcsovgtondfkuibhtmpxrvnhntqgxzpcvxwdsubroqpvisslbxfbhep
> str1: -------------------------t----------------k---------g--n--ku--h-mpx--nh-tqgxz--vx----------is---------
> str2: i------o----------------j-i-----------qfo------l-------n-----b----x--------x--cv---su---qpviss-bxf----
> str3: --u--l-------c------------iny-c---------o--------sov--o---------------------zp-----------p----l------p
> str4: i-------ge-----va-z---gb----------rd--------db--cs-v---------------rvn-n--g----------------------f----
> str5: -p-yplr-----------z-x--------uc-----pmq------------vgt--df-ui-------v---------c---ds-b-o--------------
> str6: -p---------bd-ev-d------------cv---dp--f-z-------s--------------m------------------s-broq-v----b--bh--
> str7: ---------enb-c----zf----jt-----vxer------z---br----v--------i-------------g--p----------------l-----e-
> str8: ------r-------------xw----------x-----q---krd-rlc----to-d------tmp-r---------p--xwd-------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q26n016k015-025.txt"))
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
> --- Solution (of length 152) ---
>   Sol: ikrshtxxuokqjnafpbadigqfejwolkcinbycokplrzxuxsfjhcpafqkrdbicgzpmpxqvgnctbvxerdqwazhckotvodpfzsmiuiqgspbrviddbgplecsvrwtaodqvsbbhnntfmprgqpxzvxisjfuowwyd
> str01: -----t----k----------g----------n----k-----u----h--------------mpx---n------------h---t-----------qg--------------------------------------xzvxis--------
> str02: i--------o--j-------i-qf---ol---nb--------x-x----c-----------------v-------------------------s--u-q--p--vi--------s---------sb------------x------f------
> str03: --------u-------------------l-cin-yco--------s---------------------------------------o-vo---z--------p--------pl---------------------p------------------
> str04: i--------------------g--e------------------------------------------v------------az-----------------g--br--ddb----csvr------v----nn-----g---------f------
> str05: ----------------p-----------------y---plrzxu-----cp------------m--qvg--t-----d-------------f----ui------v--------c-------d--sb---------------------o----
> str06: ----------------pb-d----e------------------------------------------v---------d-----c---v-dpfzsm-----s-br----------------o-qv-bbh------------------------
> str07: ------------------------e-------nb-c-----z----fj-----------------------t-vxer----z--------------------brvi---gple---------------------------------------
> str08: --r---x-------------------w---------------x----------qkrd-------------------r----------------------------------l-c----t-od--------t-mpr--px---------w--d
> str09: -k--------kq--af----igq--jwo-k-------k-------s--------kr-b-----------------------------------------------------l-----------------------g----------------
> str10: ----------------------------l-------------x-x-----pa-----bi--------v----bv-------z--ko------z----------------------------------------------zv----------d
> str11: -kr-----------------i--f---------------------s-----a---------------v-nc------dqw--h---------z--------------------c--------------------------------------
> str12: -----------q--a---------------------------xu------------d---g-----qv----------q----c----------------------------e----w-------b-----f---g------i-j--owwy-
> str13: --rs--x----qjn-fp-adi----------------------u-s------------i-------q-----b--e-----zh-ko-----------------------------------------h----m--g----------------
> str14: i-------------------------w------------------s--h------------------v--------------hc-o--------miu-------v-dd------------------------m-------------------
> str15: ----htxx---qj----------------------------z-----------q---b-c-----------tb-------a---k-------------------------------------------n-----------------------
> str16: ------x-u------------------------------------sf--c--f--------zp------------e------------------------------------ec-v-w-a--------n-tfm--gq--z------u-----
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("uniform_q26n016k015-025.txt"))
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
>   Sol: irkepxulcswxqkarifsnydhtxpabcuojivncdqgbevzfakolrzgnkbxqujtpvxerdzqcevdwhbcsvrvwantfigplmqvgctdijowfuqpvokiszpsbxnhamiuvdtqgcdbfxezhknsbkroqvbbhmprlpgxwdyis
> str01: -----------------------t---------------------k----gnk---u---------------h---------------m-------------p---------xnh------tqg----x-z---------v---------x---is
> str02: i-----------------------------oji----q-----f--ol---n-bx------x-----c-v-----s------------------------uqpv--is--sbx--------------f----------------------------
> str03: ------ulc-------i--ny-------c-o--------------------------------------------s---------------------o-----vo---zp-----------------------------------p-lp-------
> str04: i-------------------------------------g-ev--a----zg--b---------rd-----d--bcsvrv--n-------------------------------n---------g---f----------------------------
> str05: ----p---------------y----p---------------------lrz----x-u----------c------------------p-mqvg-td----fu-----i------------v----cd--------sb--o-----------------
> str06: ----p----------------------b--------d---ev----------------------d--c-vd---------------p------------f--------z-s-----m-----------------sb-roqvbbh------------
> str07: ---e---------------n-------bc-------------zf-------------jt-vxer-z-------b---rv-----igpl-----------------------------------------e--------------------------
> str08: -r---x----wxqk-r-----d--------------------------r--------------------------------------l----ct---o----------------------dt----------------------mpr-p-xwd---
> str09: --k----------k-----------------------q------a--------------------------------------fig---q------j-w-----ok--------------------------k-s-kr---b-----l-g------
> str10: -------l---x------------xpab----iv-----b-vz--ko--z---------------z---vd-------------------------------------------------------------------------------------
> str11: --k------------rifs-------a------vncdq---------------------------------wh-----------------------------------z---------------c-------------------------------
> str12: ------------q-a---------x----u------d-g----------------q----v-----qce--w-b---------f-g---------ijow----------------------------------------------------w-y--
> str13: -r-------s-xq------------------j--n--------f---------------p--------------------a-------------di----u------s---------i----q---b--ezhk-----o----hm----g------
> str14: i---------w-------s---h----------v--------------------------------------h-c----------------------o------------------miuvd----d------------------m-----------
> str15: ----------------------htx-----------------------------xq-j-------zq------bc-------t----------------------------b---a----------------kn----------------------
> str16: -----xu--s-------f----------c--------------f-----z---------p--e-----e-----c-v--wantf----m--g---------q------z---------u-------------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q05n010k010-010.txt"))
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
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("uniform_q05n010k010-010.txt"))
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
> --- Solution (of length 27) ---
>   Sol: bbaedcdbeacdeecbdbeacbdacde
> str01: ----dc-b--c---c-db--c---c-e
> str02: b---d-dbe---ee----e--bd----
> str03: -----c---acdeec---e--b----e
> str04: --aed-d----d----d-e--bd--d-
> str05: --a--c-be---e-c----a-b--c-e
> str06: bba----be------bd---cb-a---
> str07: bbae-----a--e--b---a--da---
> str08: ---e----e---eecbdbe-------e
> str09: -----c----cdee--d--a--d-cd-
> str10: b---d----a-----bdbea---a-d-
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("uniform_q05n050k010-010.txt"))
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
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("uniform_q05n050k010-010.txt"))
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
> --- Solution (of length 34) ---
>   Sol: daecbdeabecdabcedaecbdaebcdeabacde
> str01: d--cb-----c---c-d---b----c-----c-e
> str02: ----bd-----d-b-e--e----e---e-b--d-
> str03: ---c---a--cd---e--ec---eb--e------
> str04: -ae--d-----d----d----d-eb-d-----d-
> str05: -a-cb-e--ec-abce------------------
> str06: ----b---b---ab-e----bd---c---ba---
> str07: ----b---b---a--e-ae-b-a---d-a-----
> str08: --e---e--e-----e---cbd--b--e-----e
> str09: ---c------cd---e--e--da---d----cd-
> str10: ----bd-ab--d-b-e-a----a---d-------
> str11: --e--de----da----a----ae----a-a---
> str12: -a-----a-e--a----a--b--e---ea--c--
> str13: --e----a----abc--a-c-----cd--b----
> str14: ----bde--e--a---d-e---a---de------
> str15: ---c---a-e-da---d-e----e---e----d-
> str16: --e-b-----c-a---d---b-a-b----b---e
> str17: d----d----c----e--e---a-b-dea-----
> str18: da--b-----cd----d-e---ae-c--------
> str19: -a-----a---d--ce--e--da-----ab----
> str20: -ae---e---c---ce--e----e----a-a---
> str21: ----b---b--da--e---c--a-----a---de
> str22: da-c--e----da--eda--b-------------
> str23: -a-----a-e--ab------b---b----b-c-e
> str24: d-e--d--b-c--bc--a----a-b---------
> str25: d---bd-a----a--e----b---bc---b----
> str26: d-e-b-e----d-b-e----b-a--c--------
> str27: ---c--e--e---bc-d--cbd-e----------
> str28: d---b-e----da----a---da-----ab----
> str29: ---c------c---c-d--cb--eb-d----c--
> str30: -ae---ea--cd-bc-----bd------------
> str31: da-cb-ea--c---c----c-d------------
> str32: --ec--e-b-c---c-d---bd--b---------
> str33: d----d--b----bceda--b---b---------
> str34: -a-----a-e--ab---a----aeb---a-----
> str35: --ecb---b-c-a----a---d---cd-------
> str36: d-e-b-----c---ce---c-d--bc--------
> str37: da-----a--c--b---ae----ebc--------
> str38: -a---d-abe--a----a-c-----c-e------
> str39: daec-d--b---a-c--a----a-----------
> str40: da-cb---b--d--ced--c--------------
> str41: d-e--d--be-----e----b---b-de------
> str42: ---c-d-a---d--c-d--c-da-----a-----
> str43: ---c--e--e-d--c-----b-ae---e----d-
> str44: ---c--ea-ec-a----a----a--c--a-----
> str45: d--c------c---ce----b---b----ba-d-
> str46: ----b--a-e-----e-ae-b---b-de------
> str47: d---bde-b---a-c----c-d--b---------
> str48: --e-b-----c--b-e--e--dae----a-----
> str49: -ae---e--e---b------bd--bc--a-----
> str50: d---bd-ab-c----e---cb---b---------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("nucleotide_n010k010.txt"))
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
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("nucleotide_n010k010.txt"))
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
>   Sol: TCATGACCGTAGATCAGTACGATC
> str01: --ATG---G--GAT-A---CG---
> str02: --AT-ACC-T---TC----C---C
> str03: -CA---C-G-A-AT---T--GA--
> str04: T-A--A----A-ATC--T--G-T-
> str05: --A-G---GTA-A-CA--A--A--
> str06: T--T--CC-TAG----GTA-----
> str07: T--TG----TAGATC--T------
> str08: T---G---G--GA--AGT----TC
> str09: T--T--CC--A---CA--AC--T-
> str10: TC-T-A----A-A-C-G-A--A--
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("nucleotide_n050k050.txt"))
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
> --- Solution (of length 166) ---
>   Sol: AGTAACGACATGTAGATCCAGTATCTAACGAACTAGTAGTGCAGCGAGATGCTACGGACGGTCAACAACGTACAGTAGTACACTCCAAGTTACTCATGGACAGTAACAGGCCACGTAGCTGAGCGATGCGTACGTCAAGATGCTAGACACGTAGAGCTACTAGART
> str01: --TA--G---T--AG-T--AG-A-CT--C---C--G--G---A---AG-TG--AC--A-----AAC--C---C--T-G-A-A----AAG--A---ATGGA---TAA-A-------TA--T-A--------------------------------------------
> str02: -G----GA--T--A-A---A----C-A-C----T-------C--C------C---G-A-----AA-A---TA-A-T--T----T----G--ACT--T--A-A--A-CA----ACG---C-GA-C-A-G--T---TCAAG---------------------------
> str03: A-TA-C--C-T-T----CC--TA------G-----GTA----A-C-A-A----AC---C----AAC--C--A-A------C--T-----TT--T---G-A---T--C--------T--CT------TG--TA-G--A---T-CT-G--------------------
> str04: --TAA--A--T-TA--T--A--ATCT-------TA-TA---C-------T---A-G-----T-AA-AA---A-A-TAG----------G--------G-----T----G------TA----A-C----CG-A----AA-A--C--G----GT----C---------
> str05: --T-------T--A-A---A--A-C-A--G--C--------C-------TG-T--GG--G-T--------T---G-----CAC-CCA-----CTCA----CAG-----GGCC-C--A-CTG-G-G---CG--C---AAG---------------------------
> str06: A-T---GAC-T-T----CCA--AT-----G-----G-A-T-C--C------C-A---AC---C-------T-CA--AG--C--T-----T--C-CA----C-----C---CCA---A--TG-G---T---T---TCA-G---C-----------------------
> str07: A--A-C-A-A---A---CCA--A-C---C-AACT--T--T---------TG--A-------TC-------T-C--T--T---------GT-A-----G-A---T--C--------T-G-T------T-C-T-C-T-AA-A--C--GA-AC----------------
> str08: A-T---GA-A---A-A-C--G-A---AA--A--T--TA-T---------T---A-------TCAA----G----G--GTA---T----G--------G-A-AGT----GG--A---AGCTGA-CGA-----A----A---T-------------------------
> str09: A----C----T------C--G--------G--CT-G-----CA------TGCT--------T-A-----GT---G-----CACTC-A-----C----G--CAGTA----------TA----A----T---TA----A---T---A-AC---TA-A--T--TA----
> str10: --T-------TGTAGATC---T-------G---T--T----C-------T-CTA---A-----A-C---G-A-A------C--T-----TTA---A---A-A-T--C--------T-G-TG-----TG-G--C-T---G-T-C-A--C---T----C---------
> str11: -G---C-A---G-AG--C-A-T-T-T-------T-------C-------T---A---A---T-A------T-C-------CAC---AA---A---ATG-A-AG-----G-C-A---A--T-A---AT---T--GT-A-----CTA--C---T----C---------
> str12: A-T---GA---G-----CCA--A------GA--T-------C--CGA----C---G-A-----A-----G-A--G-----C-C-CCAAG--------G-A--G-----G---A-G-A----AG-GA-G-G---G--A-----C----C-C------C--C------
> str13: --T--C----T------C-A----C-A--G---T--T----CA---AGA----AC---C---CAA-A--GTAC-------C-C-CC------C--AT--A--G---C---CC---T--CT------T----A----AAG---C----CAC----------------
> str14: AG----G---T-T---T--A-TA-C---C----T--T----C--C----T---A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T---T---CGAT-C-T-C-T-----TG-TA---------------------
> str15: AG----G---T-T---T--A-TA-C---C----T--T----C--C------C-A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T---T---CGAT-C-T-C-T-----TG-TA---------------------
> str16: --TAA--A-A-------C-A--A-CT--C-AA-TA------CA---A----C-A-------T-AA----G-A-A--A--A---TC-AA----C----G--CA--AA-A----AC--A-CT---C-A--C--A----AA----------------------------
> str17: -----C--C--G-----CC-----C-A------T--T--TG--G-G-----C---GG-C--TC-------T-C-G-AG--C-------G--A-T-A-G--C--T--C-G------T--C-GA---AT-C---C--C----T-C--GAC-C-T--------------
> str18: A-TA-C--C-T-T----CC-----C-A--G-----GTA----A-C-A-A----AC---C----AAC--C--A-A------C--T-----TT-C----G-A---T--C--------T--CT------TG--TA-G--A---T-CT-G--------------------
> str19: --T--C----T------C-A----C-A--G---T--T----CA---AGA----AC---C--TCAA----GT-C--T----C-C-CC------C--AT--A--G-----G-CC---T--CT------T---T-C---A-G-T-C-AG--------------------
> str20: -G-A------T------C---T--CT--C----T-------CA-C------C---G-A-----A-C--C-T---G--G--C-C-CC--G--------GG-CA--AA---------T-GC----C----C-TA----A---T-C----CA-G-AG-G-T----G---
> str21: AG-A--G-CA---A--TC-AGT-------G--C-A-T----CAG--A-A----A-------T-A------TAC-------C--T--A--TTA-T-A----CA----C--------T---T------TGC-TA----A-GA----A------T--------------
> str22: A--A------T-TA-A---A--A-C-A------T-------C-------T-C-A---A---T-A-CAAC--A---TA--A--------G--A---A---A-A--A-CA----ACG---C--A---A-----A----AA----C-A--C---T----C-A-T-----
> str23: A--AACGA-A-------C---T-T-TAA--AA-T-------C-------TG-T--G-----T-------G----G-----C--T----GT--C--A----C--T--C-GGC----T-GC--A----TGC-T---T-A-G-TGC-----------------------
> str24: A-TAAC----T--A-AT----TA-CT---G---T-------C-G-----T--T--G-AC----A-----G----G-A---CAC-----G--A-----G-----TAAC--------T--C-G-----T-C-TA--TC----T--T---C---T-G------------
> str25: A-T---GA---GT-G-TC-A----C----GAA-T--T----CA-CG---T---AC--A-----A------T---G-A--AC--T----G--------G-A---T----G------T---T---C-A--CGT--G----GA----A------TA-A-----------
> str26: A----C--C--GT-G-----G--------G--C--G-AG--C-G-G---TG--AC---CGGT-------GT-C--T--T-C-CT--A-GT-------GG---GT--C---CCACGT---TGA---A--------------------------------------R-
> str27: A--AA-G----GT---T----TAT--A-C---CT--T----C--C------C-A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T---T---CGAT-C-T-C-T-----TG------------------------
> str28: AGTA--G---T-T----C--G---C---C----T-GT-GTG-AGC----TG--AC--A-----AAC----T----TAGTA--------GT-------G-----T-----------T---TG-----TG---A-G----GAT--TA---------------------
> str29: --T-------T-TA--T--A----C---C----T--T----C--C----T---A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T---T---CGAT-C-T-C-T-----TG-TAGA----T--------------
> str30: A-T---G-C--G--G-TC--GT--CT--C----T-------C--C------C--CGG-C--T--------T----T--T----T-----TT-C-C-----C-----C-G-C---G---C----CG---CGT---T---G--GC--G-C-CG-A-------------
> str31: -GT---GACA---A-A---A--A-C-A------TA--A-TG--G--A----CT-C---C----AACA-C---CA-T-GT-CA----A-G---CT--T------T--CAGG-----TAG---A-C------------------------------------------
> str32: -GT---G---T--A-A----G-A---AAC-A----GTA----AGC------C--CGGA-----A-----GT---G--GT---------GTT--T--TG--C-G-A----------T---T------T-CG-A-G----G---C----C--G--G------------
> str33: -G-A--GA-ATG-AG-TC---T--C-A------T--TA---C--CG-----C--C---CGGT-A-C----T----TAG--CA----A-G---CT-A---A---TA---G------T--C--A-CG--GC-------------------------------------
> str34: A-T---G---TG--G-TC--G-AT-----G--C--------CA------TG----G-A-GG-C--C--C--AC-------CA------GTT-C--AT------TAA--GGC----T--C----C--TG-G--C---A---T--T----------------------
> str35: A----CGA---G-----C--GT-T-T-------TA--AG-G--GC------C--CG--CG---A-C----T---G-----C-------G--AC----GG-C-----CA--C-A--T-G--G--C----C---C-T---G-T---A------T-G---T--------
> str36: -G----G---T-T---T--A-TA-C---C----T--T----C--C------C-A-GG----T-AACAA---AC-------CA----A-----C-CA---AC--T-----------T---T---CGAT-C-T-C-T-----TG-TAG--------------------
> str37: --T---G----G--GA---AGT-TC---C-AA--A--AG---A------T-C-AC--A-----AA-A-C--AC--TA---C-C---A-GT--C--A---AC-----C--------T-G---A---A-G--TAC---A-----C-----------------------
> str38: -G-AA-G-C--GT---T--A--A-C----G---T-GT--TG-AG-GA-A----A---A-G---A-CA--G--C--T--TA--------G--------G-A--G-AACA----A-G-AGCTG-G-G-----------------------------------------
> str39: A----C--CA-G-----C--G---C-A-C----T--T----C-G-G-----C-A-G--CGG-CA-----G--CA------C-CTC---G--------G--CAG---CA--CC---T--C--AGC-A-GC--A----A-----C-----------------------
> str40: A-T---G----G--GA-C-A--A-CT-------TA-T--T-C--C----T---A-------TCA------T---GT-G--C-C---AAG--A-----GG----T-----------T---T------T----AC--C------C--G----GT-GA-C--C-A----
> str41: --T-------TGTAGATC---T-------G---T--T----C-------T-CTA---A-----A-C---G-A-A------C--T-----TTA---A---A-A-T--C--------T-G-TG-----TG-GT---T---G-T-C-A--C---T----C---------
> str42: A--A-C--CA---A---CCA--A-CT-------T--T----C-G--A--T-CT-C------T--------T---GTAG-A---TC----T-------G-----T-----------T--CT---C--T----A----AA----C--GA-AC-T-----T--TA----
> str43: -G----G----GT---TC---T-------G--C--------CAG-G-----C-A-------T-A-----GT-C--T--T----T-----TT--T--T---C--T----GGC---G--GC----C----C-T---T---G-TG-TA-A-AC------CT----G---
> str44: -G----G-C-TG-----C-A-T-------G--CT--TAGTGCA-C----T-C-ACG--C----A-----GTA---TA--A---T-----T-A---AT--A-A----C--------TA----A----T---TAC-T---G-T-------------------------
> str45: --T---G-CATG-----C---T-T--A--G---T-G-----CA-C----T-C-ACG--C----A-----GTA---TA--A---T-----T-A---AT--A-A----C--------TA----A----T---TAC-T---G-T-C--G-----T--------------
> str46: --T-------T------CCA----C-AAC----T--T--T-C--C-A----C--C--A-----A-----G--C--T----C--T----G---C--A---A--G-A----------T--C----C----C--A-G--A-G-T-C-AG----G--G-GC--CT-G--T
> str47: --T--C----T--A-A---A----C----GAACT--T--T--A---A-A----A-------TC-------T---GT-GT---------G--------G--C--T----G------T--C--A-C--T-CG---G-C----TGC-A------T-G--CT--TAG---
> str48: A----C--C--G--GAT---G--------G--C--------C-GCGA--T--T--------T--------T----T----C-------G--------G-A--GT--C---C----T---TG-G-G--G-G-AC--CA-----CT---CA-G-A-A--TA---GA--
> str49: -----C----T-T-G-T--AG-ATCT---G---T--T----C-------T-CTA---A-----A-C---G-A-A------C--T-----TTA---A---A-A-T--C--------T-G-TG-----TG-G--C-T---G-T-C-A--C---T--------------
> str50: A-T---GA---G-----C-A----CTAA-G--C--G-A----AG--A-A--C--C--A-----AA-AA-G--CAG-A---CA----A--T-AC--A---AC-----C---C---G---CT-A----T---TAC---------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("nucleotide_n050k050.txt"))
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
> --- Solution (of length 136) ---
>   Sol: ATGACTGACGTAACGTACATGCATCATGCATCGATCGATCAGTCATCGATGCAGCTACAGATCAGCTAGTCATCGATCAGTACGCATAGCTGATCAGTCGATCTGATCGATCAGTCAGTCATCGACCTGATGCTAR
> str01: -T-A--G---TA--GTA---G-A-C-T-C--CG---GA--AGT----GA--CA---A-A---C--C----C-T-GA--A--A---A--G---A--A-T-G----GAT--A--A---A-T-AT--A-----------
> str02: --G---GA--TAA---ACA--C-TC---C--CGA---A--A---AT--A---A--T-----T----T-G--A-C--T---TA---A-A-C--A--A--CG--C-GA-C-A---GT---TCA---A---G-------
> str03: AT-AC---C-T----T-C---C-T-A-G----G-T--A--A--CA---A---A-C--CA-A-C--C-A---A-C--T---T-----T---TGATC--TC--T-TG-T--A---G--A-TC-T-G------------
> str04: -T-A---A---A---T---T--AT-A---ATC--T---T-A-T-A-C--T--AG-TA-A-A--A---A---AT--A---G---G----G-TG-T-A----A-C----CGA--A---A---A-CG----G-T-C---
> str05: -T---T-A---AA---ACA-GC--C-TG--T-G---G----GT--T-G---CA-C--C----CA-CT---CA-C-A---G---G----GC----C---C-A-CTG---G----G-C-G-CA---A---G-------
> str06: ATGACT----T--C---CA---AT---G----GATC---C---CA---A--C--CT-CA-A---GCT--TC--C-A-C----C-C----C--A--A-T-G----G-T---T---TCAG-C----------------
> str07: A--AC--A---AAC---CA---A-C---CA---A-C--T---T--T---TG-A--T-C---TC---T--T----G-T-AG-A----T--CTG-T---TC--TCT-A---A--A--C-G--A---AC----------
> str08: ATGA---A---AACG-A-A---A--AT---T--AT---T-A-TCA---A-G--G-----G-T-A--T-G-----GA--AGT--G----G---A--AG-C--T--GA-CGA--A---A-T-----------------
> str09: A---CT--CG----G--C-TGCAT---GC-T---T--A---GT----G---CA-CT-CA---C-GC-AGT-AT--A--A-T-----TA----AT-A----A-CT-A---AT---T-A-------------------
> str10: -T---TG---TA--G-A--T-C-T---G--T---TC--TC--T-A---A---A-C----GA--A-CT--T--T--A--A--A---AT--CTG-T--GT-G----G--C--T--GTCA--C-TC-------------
> str11: --G-C--A-G-A--G--CAT---T--T---TC--T--A--A-T-ATC----CA-C-A-A-A--A--T-G--A---A---G---GCA-A--T-A--A-T---T--G-T--A-C--T-A--C-TC-------------
> str12: ATGA--G-C----C--A-A-G-ATC---C---GA-CGA--AG--A--G---C--C--C----CA---AG-----GA---G---G-A--G---A--AG--GA---G---G----G--A--C--C--CC-----C---
> str13: -T--CT--C--A-C--A---G--T--T-CA---A--GA--A--C--C----CA---A-AG-T-A-C----C--C---C----C-CATAGC----C---C--TCT--T--A--A---AG-C--C-AC----------
> str14: A-G---G---T----T---T--AT-A--C--C--T---TC---C-T--A-G--G-TA-A---CA---A---A-C---CA--AC-CA-A-CT--T---TCGATCT---C--T---T--GT-A---------------
> str15: A-G---G---T----T---T--AT-A--C--C--T---TC---C--C-A-G--G-TA-A---CA---A---A-C---CA--AC-CA-A-CT--T---TCGATCT---C--T---T--GT-A---------------
> str16: -T-A---A---AAC--A-A--C-TCA---AT--A-C-A--A--CAT--A---AG--A-A-A--A--T---CA---A-C-G--C--A-A----A--A----A-C--A-C--TCA--CA---A---A-----------
> str17: ----C---CG---C---C---CAT--T---T-G---G----G-C---G--GC---T-C---TC-G--AG-C---GAT-AG--C---T--C-G-TC-G---A----ATC---C---C--TC---GACCT--------
> str18: AT-AC---C-T----T-C---C--CA-G----G-T--A--A--CA---A---A-C--CA-A-C--C-A---A-C--T---T-----T--C-GATC--TC--T-TG-T--A---G--A-TC-T-G------------
> str19: -T--CT--C--A-C--A---G--T--T-CA---A--GA--A--C--C--T-CA---A--G-TC---T---C--C---C----C-CATAG--G--C---C--TCT--T---TCAGTCAG------------------
> str20: --GA-T--C-T--C-T-C-T-CA-C---C---GA---A-C---C-T-G--GC--C--C----C-G---G-----G--CA--A---AT-GC----C---C--T---A---ATC---CAG--A--G----G-TG----
> str21: A-GA--G-C--AA--T-CA-G--T---GCATC-A--GA--A---AT--AT--A-C--C---T-A--T--T-AT--A-CA---C---T---T--T--G-C--T---A---A---G--A---AT--------------
> str22: A--A-T----TAA---A-A--CATC-T-CA---AT--A-CA---A-C-AT--A---A--GA--A---A---A---A-CA--ACGCA-A----A--A----A-C--A-C--TCA-T---------------------
> str23: A--A---ACG-AAC-T---T---T-A---A---A---ATC--T----G-TG----T---G----GCT-GTCA-C--TC-G---GC-T-GC--AT--G-C--T-T-A--G-T--G-C--------------------
> str24: AT-A---AC-TAA--T---T--A-C-TG--TCG-T---T--G--A-C-A-G--G--ACA---C-G--AGT-A---A-C--T-CG--T--CT-ATC--T---TCTG-------------------------------
> str25: ATGA--G---T---GT-CA--C-----G-A---AT---TCA--C---G-T--A-C-A-A--T--G--A---A-C--T--G---G-AT-G-T--TCA--CG-T--G---GA--A-T-A---A---------------
> str26: A---C---CGT---G-----G------GC---GA--G--C-G-----G-TG-A-C--C-G----G-T-GTC-T---TC----C---TAG-TG----G--G-TC----C---CA--C-GT--T-GA----A-----R
> str27: A--A---A-G----GT---T---T-AT--A-C---C--T---TC--C----CAG-----G-T-A---A--CA---A--A---C-CA-A-C----CA----A-CT--T---TC-G--A-TC-TC----T--TG----
> str28: A-G--T-A-GT----T-C--GC--C-TG--T-G-T-GA---G-C-T-GA--CA---A-A---C---T--T-A--G-T-AGT--G--T---T--T--GT-GA---G---GAT---T-A-------------------
> str29: -T---T----TA---TAC---C-T--T-C--C--T--A---G-----G-T--A---ACA-A--A-C----CA---A-C----C--A-A-CT--T---TCGATCT---C--T---T--GT-A--GA--T--------
> str30: ATG-C-G--GT--CGT-C-T-C-TC---C--C---CG----G-C-T---T-----T-----T----T--T--TC---C----C-C---GC-G--C---CG--C-G-T---T--G---G-C---G-CC-GA------
> str31: --G--TGAC--AA---A-A---A-CAT--A---AT-G----G--A-C--T-C--C-A-A---CA-C----CAT-G-TCA--A-GC-T---T--TCAG--G-T---A--GA-C------------------------
> str32: --G--TG---TAA-G-A-A---A-CA-G--T--A---A---G-C--C----C-G-----GA--AG-T-G-----G-T--GT-----T---T--T--G-CGAT-T--TCGA---G---G-C--CG----G-------
> str33: --GA--GA---A---T----G-A----G--TC--TC-AT---T-A-C----C-GC--C----C-G---GT-A-C--T---TA-GCA-AGCT-A--A-T--A---G-TC-A-C-G---G-C----------------
> str34: ATG--TG--GT--CG-A--TGC--CATG----GA--G----G-C--C----CA-C--CAG-T----T---CAT---T-A--A-G----GCT---C---C--T--G---G--CA-T---T-----------------
> str35: A---C-GA-G---CGT---T---T--T--A---A--G----G-----G---C--C--C-G--C-G--A--C-T-G--C-G-ACG----GC----CA--C-AT--G---G--C---C---C-T-G---T-ATG-T--
> str36: --G---G---T----T---T--AT-A--C--C--T---TC---C--C-A-G--G-TA-A---CA---A---A-C---CA--AC-CA-A-CT--T---TCGATCT---C--T---T--GT-A--G------------
> str37: -TG---G--G-AA-GT---T-C--CA---A---A---A---G--ATC-A--CA---A-A-A-CA-CTA--C--C-A---GT-C--A-A-C----C--T-GA----A--G-T-A--CA--C----------------
> str38: --GA---A-G---CGT---T--A--A--C---G-T-G-T---T----GA-G--G--A-A-A--AG--A--CA--G--C--T-----TAG--GA---G---A----A-C-A--AG--AG-C-T-G----G--G----
> str39: A---C---C--A--G--C--GCA-C-T---TCG---G--CAG-C---G--GCAGC-AC----C---T---C---G----G--C--A--GC--A-C---C--TC--A--G--CAG-CA---A-C-------------
> str40: ATG---G--G-A-C--A-A--C-T--T--AT---TC---C--T-ATC-ATG----T---G--C--C-A---A--GA---G---G--T---T--T---T--A-C----C---C-G---GT----GACC--A------
> str41: -T---TG---TA--G-A--T-C-T---G--T---TC--TC--T-A---A---A-C----GA--A-CT--T--T--A--A--A---AT--CTG-T--GT-G----G-T---T--GTCA--C-TC-------------
> str42: A--AC---C--AAC---CA---A-C-T---T---TCGATC--TC-T---TG----TA--GATC---T-GT--TC--TC--TA---A-A-C-GA--A--C--T-T--T--A--------------------------
> str43: --G---G--GT----T-C-TGC--CA-G----G--C-AT-AGTC-T---T-----T-----T----T--T--TC--T--G---GC---G--G--C---C---CT--T-G-T--GT-A---A---ACCTG-------
> str44: --G---G-C-T---G--CATGC-T--T--A--G-T-G--CA--C-TC-A--C-GC-A--G-T-A--TA---AT---T-A--A----TA----A-C--T--A----AT---T-A--C--T----G---T--------
> str45: -TG-C--A--T---G--C-T---T-A-G--T-G--C-A-C--TCA-CG---CAG-TA----T-A---A-T--T--A--A-TA---A---CT-A--A-T---T---A-C--T--GTC-GT-----------------
> str46: -T---T--C----C--ACA---A-C-T---T---TC---CA--C--C-A---AGCT-C---T--GC-A---A--GATC----C-CA--G---A---GTC-A---G---G----G---G-C--C----TG-T-----
> str47: -T--CT-A---AACG-A-A--C-T--T---T--A---A--A---ATC--TG----T---G-T--G---G-C-T-G-TCA---C---T--C-G----G-C--T--G--C-AT--G-C--T--T--A---G-------
> str48: A---C---CG----G-A--TG------GC--CG--CGAT---T--T---T-----T-C-G----G--AGTC--C--T---T--G----G--G----G--GA-C----C-A-C--TCAG--A---A--T-A-G--A-
> str49: ----CT----T---GTA---G-ATC-TG--T---TC--TC--T-A---A---A-C----GA--A-CT--T--T--A--A--A---AT--CTG-T--GT-G----G--C--T--GTCA--C-T--------------
> str50: ATGA--G-C--A-C-TA-A-GC-----G-A---A--GA--A--C--C-A---A---A-A-A---GC-AG--A-C-A--A-TAC--A-A-C----C---CG--CT-AT---T-A--C--------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("protein_n010k010.txt"))
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
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("protein_n010k010.txt"))
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
> --- Solution (of length 44) ---
>   Sol: MEQPSLSKFTRYAEHVNQELNSYCHFDAIRPGFKGVTANEGYQL
> str01: M-----------A------L-SYC------P--KG-T-------
> str02: M-Q-S-S------------LN------AI-P----V--------
> str03: M--P-LS----Y-----Q------HF---R---K----------
> str04: ME-----------EHVN-EL----H-D-----------------
> str05: M---S-----------N--------FDAIR-------A-----L
> str06: M-------F-R-----NQ--NS-------R--------N-G---
> str07: M-------F--YA-H------------A----F-G-----GY--
> str08: M---S--KFTR------------------RP----------YQ-
> str09: M---S---F------V-----------A---G---VTA----Q-
> str10: ME--SL---------V--------------PGF-----NE----
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench(scsp.example.load("protein_n050k050.txt"))
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
> --- Solution (of length 882) ---
>   Sol: MARTDEHPSLLAKNIAFDVEPGFNRWSAEEDDFGIETQVILVLKFLNLTGAEEFGHIEIDIKKMALFDKLDNHMKPEKIKLAEKLLENQAAAEQGKAQRQAEFHEKKLMNKDKPSEEAFAGIGIKIQLFADQIILNNINIDINYAEHAFGGIVQLSKLPWSQCVADTALQRPAARDAEAEFDLAGCDIKKAHLCDIDIKLHMKADFNSFGILRNMLKPTNSEVFKRDVITLEFGFNQLSVACDEFVGDEGAITQCFGHKDGQEIKCILEPPKAHALASYSNWFDETASTACDFGVDEFQHADFGIEILAHPLVDEFKAHKLGHIHLMNMLDHAFPGIQVLNNNLEQDRFGFGDYNKYALDAEDFEIKHIIILLFAYSNLTPNTYDAQACTCEDLPPADEEFGFGAHSDCFGISTACDEGGEKLKMEENFDGPQKFDDGALRADFGVYEEQAPTNDVLSEAFTVRGAGTCDEFAIDESQAEHLADITADEFKDRGTADFHDIKLAICLAVYIIDHGKLAMANFPIFKKLTADEGDELGSAIDEKVILEFCRSSVLLADDENDEEFGAETRIPEAGDHSFATGIRIEAGKLMDFCGIDEKLNDPGQSIHTVADEFGGEPKHIAILYPDDKVDEFGLNIVDKKQGHPMKLRSRDGADAHLTGRSREDGHILNQALAQNKNLPDADFQDRSYEFIYLNIPRIEKAEGQRKEDHGSHLNIQRPTVLADHSKLMAFNQKYAGMWAFDEHFDAIFIKKIEANLACQARQPAITCDDGAECIKHLPLPDECDFDHLIQDSRKHRNVNSGDSAFRAETIKLPGDFFRDKSDRMAHVKARVQKDWTPSGELGFWMFMICSVVGNLRVWVTVYSADKAILLYGVPVWKEAKTT
> str01: M-R---H--L---NI--D----------------IET----------------------------------------------------------------------------------------------------------Y-----------S----S---------------------------------------------N-------------------D-I-----------------------------K---------------------N------------GV----------------------------------------------------------Y-KYA-DAEDFEI-----LLFAYS----------------------------------I----D-GGE------------------------V-E--------------------C------------L-D------------------L-------------------------T--------------------R--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str02: M----E------------------R-------------------------------------------------------------------------R-A--H------------------------------------------------------------------R-----------------------------------------------T--------------------------------------H---Q------------------NW-D--A-T---------------------------K-----------------P------------R-------------E------------------------------------------------------------------------------R----------------------R--------------------------K----------------------------------------------------------------------------------------------------------------Q---T--------------------------------Q-H----R--------LT-------H------------PD-D----S---IY---PRIEKAEG-RKEDHG----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str03: M----E-P-------------G-----A----F---------------------------------------------------------------------------------S---------------------------------------------------TAL-----------FD-A--------LCD-DI-LH-----------R------------R----LE------S--------------Q-------------L-------------------------------------------------------------------------------RFG-G---------------------------------------------------------------------------------------------V---Q-----------------------I------------------------------------------------P-----------------------------------------------PE------------------------------------V---------------------------------------S-D---------------------------P------R---------------------------------V-------------YAG-----------------------------------------------------------------------------------------------------------------------------Y-A----LL------------
> str04: M--------------------G---------------------KF--------------------------------------------------------------------------------------------------Y--------------------------------------------------------------------------------------------------------------------------------------YSN------------------------------------------------------------------R--------------------------------------------------------------------------------------------R---------------L--A--V--------FA----QA----------------------------------------------------------------------------------------------------------------------------QS------------------------------------------R-------HL-G-----G---------------------SYE--------------Q---------------------------------W-----------------LAC---------------------------------------V-SGDSAFRAE------------------VKARVQKD------------------------------------------------
> str05: ----------------F-----F-R---E-----------------NL--A--F----------------------------------Q----QGKA-R--EF----------PSEEA----------------------------------------------------R-A---------------------------------NS---------PT-S----R-----E-----L-------------------------------------------W------------V----------------------------------------------------R--------------------------------------------------------------------------------------------R---G-------------------G-------------------------------------------------------N-P----L---------S---E-------------A--------GAE-R-------------R---G--------------------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: M---D--PSL--------------------------TQV------------------------------------------------------------------------------------------------------------------------W----A---------------------------------------------------------V--------E-G----SV---------------------------L---------S--------A--A----VD-----------------------------------------------------------------------------------T-----A-----E---------------------T-------------N-D----------------------T-----E---------------------------------------------------------------P-------DEG--L-SA--E-----------------N-E--G-ETRI-----------IRI-----------------------T-----G----------------------------------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str07: MA--------------FD----F---S-----------V---------TG---------------------N----------------------------------------------------------------------------------------------T---------------------K---L-D-----------------------T-S------------GF-----------------TQ--G-------------------------------------V---------------------------------------------------------------------------------S-----------------------------S-----------------M---------------------------T--V---A-----AGT-------------L--I-AD--------------L-----V------K------------TA-------S------------S----------------------------------------------------Q------------------L----------------------------------T----------N--LAQ------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: MA----------------V---------------I-----L----------------------------------P--------------------------------------S---------------------------------------------------T---------------------------------------------------------------------------------------------------------------Y------T-----D-G-------------------------------------------------------------------------------------T-----A-ACT-------------------------------------N--G--------------------------S----------------------------------------------------------------P-------D------------V--------V-----------G--T-----G-----T---------M---------------------------------------------------------------------------------------------------------------------------------------------------W-----------------------------------------------------------VN---------TI-LPGDFF-----------------WTPSGE---------SV----RV-------------------------
> str09: M------------N----------------------T------------G------I-ID-----LFD---NH-------------------------------------------------------------------------------V------------D-----------------------------------------S--I------PT---------I-L--------------------------------------P---H------------------------Q--------LA----------------------------------------------------------------------T-------------L---D------------------------------------------------Y---------L-----VR---T-----I----------I--DE-------------------------------N----------------------------RS-VLL--------F-----------H-----I-------M---G----------S--------G----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str10: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N----LR-----T------R---T------QL-------------------------------PP-A-----Y------T-----------------------------------------N------------------------------------------------S-----------------------F------------T--------------------------R---GVY--------------------------------------------------------------Y------------P-------D-----------KV---F-RSSVL---------------------HS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M---D---S---K------E----------------T--IL---------------IEI-I--------------P-KIK----------------------------------S----------------------------Y----------L--L-------DT---------------------------------------N---I---------S------------------------------------------------P-K-----SY-N--D--------F-----------I-----------------------------------------------------------------------S---------------------------------------------------------------R------------N------------------------------------K-----------------------------N--IF------------------VI--------------N----------------------------L----------------------------------Y----------N-V-----------S--------T--------I-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str12: M--------LL---------------S------G---------K-----------------KKM-L---LDN-----------------------------------------------------------------------Y-E--------------------TA----AAR---------G---------------------------R--------------------G------------GDE--------------------------------------------------------------------------------------------------R--------------------------------------------------------------------------------------------R----------------------RG--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------WAFD-------------------R-PAI--------------------------------V----------T-K------RDKSDRMAH--------------------------------------------------------
> str13: M------------N-------G------EEDD--------------N----E------------------------------------QAAAEQ---Q--------------------------------------------------------------------T---------------------KKA-------K-------------R--------E--K--------------------------------------------P-K--------------------------Q-A----------------------------------------------R-------K-----------------------------------------------------------------------------------------V------T----SEA-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W---EHFDA-------------------T-DDGAEC-KH----------------------------------------------------------------------------------------------------------
> str14: M----E--SL--------V-PGFN----E--------------K----T------H------------------------------------------------------------------------------------------------VQLS-LP----V----LQ----------------------------------------------------V--RDV--L--------V-----------------------------------------------------------------------------------------------------------R-GFGD-----------------------S--------------------------------------------------------------------V-EE------VLSEA---R-------------Q--HL--------KD-GT---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-R--------------------------------------------------------------------------------------------------------------------------------------------Y-------IV--S--P--Q------L-----------------------------------------------------V-------L-----Q--V------G-----------K-GQE-------------------------------V-E--------------------------------------------------R---------AL----------------Y--LTP--YD-------------------------------------------------------------Y--------------------------IDE--------------K----------------------------------------------S--------------------------------P----------I-----------------------------------------Y---------------------------------------------------------------Y-F--L---R-------------SHLNIQRP--------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: M------P----------------R-------------V------------------------------------P----------------------------------------------------------------------------V-----------------------------------------------------------------------------------------------------------------------------Y----D---S----------------------P--------------------------QV-------------------------------------S---PNT--------------------------------------------------------------V-----P-------------------------QA-------------R---------LA------------------------T-----------------------------------------P-----SFAT---------------------P-----T----F----------------------------------R---GADA-----------------------P-A-FQD---------------------------------T--A--------NQ--------------------------QARQ------------------------------------------------------------------------------------------------------------------------
> str17: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N----LR-----T------R---T------QL-------------------------------P-----LA-Y------T-----------------------------------------N------------------------------------------------S-----------------------F------------T--------------------------R---GVY--------------------------------------------------------------Y------------P-------D-----------KV---F-RSSVL---------------------HS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M---------------F-V---F---------F-----V-L-L--------------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N----L------T----------T---------------------------------------------------------------------------------------------------------------------R-------------------------------T------Q------LPPA-------------------------------------------------Y-----TN---S--FT-RG-------------------------------------------VY-----------------------------------------------------------------------------------------------------------------YPD-KV--F---------------RS-----------S----------------------------------------------------------VL--HS-------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: M----E-----A--I-------------------I-------------------------------------------------------------------------------S---FAGIGI-----------N-------Y------------K-------------------------------K---L-------------------------------------------Q-S-------------------K--------L------------------------------QH-DFG-------------------------------------------R-------------------------------------------------------------------------------------------------V----------L---------------------------------K----A------L-------------------------T--------------V-----------------------T----A---------R--A--L------------PGQ------------PKHIAI-------------------------R---------------------Q--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str20: MA------S-----------------S------G-----------------------------------------PE---------------------R-AE-H----------------------Q-----IIL-----------------------P------------------E-----------------------------S-------------------------------------------------H---------L---------S-S------------------------------PLV---K-HKL----L---------------------------Y--Y--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-----------K-----L---------T---G------LPLPDECDFDHLI---------------------------------------------------------------------------------------------
> str21: M----E--SL--------V-PGFN----E--------------K----T------H------------------------------------------------------------------------------------------------VQLS-LP----V----LQ----------------------------------------------------V--RDV--L--------V-----------------------------------------------------------------------------------------------------------R-GFGD-----------------------S--------------------------------------------------------------------V-EE------VLSE---VR-------------Q--HL--------KD-GT---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M--------L-A--------P-----S------------------------------------------------P-----------N--------------------------S---------KIQLF------NNINIDINY-EH-------------------T-L-------------------------------------------------------------------------------------------------------------Y---F---AS------V---------------------------------------------------------------------------------S--------AQ----------------------------------------N-----------------------------S--F----------FA----Q-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W-----------------------------------------------------------V----------------------------V----------------------------------YSADKAI--------------
> str23: M-------S--A--I---------------------T--------------E------------------------------------------------------------------------------------------------------------------T---------------------K----------------------------PT---------I--E-----L-------------------------------P--A--LA-------E--------G---FQ------------------------------------------------R-----YNK-----------------------TP--------------------GF----------T-C-----------------------------V----------L------------D----------------------R----------------Y--DHG----------------------------VI--------------ND---------------S----------K------I-------------V-------------LY----------N-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str24: M-----------KNIA---E--F--------------------K-----------------K--A----------PE---LAEKLLE-----------------------------------------------------------------V---------------------------F--------------------------S-----N-LK----------------G-N--S------------------------------------------------------------------------------------------------------------R----------------------------S-L-----D---------P-----------------------------M---------------RA--G---------------------------------------------K-------HD--------V----------------------------------V--------V----------------I-E----S--T-------K---------KL-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: M------P-----------------------------Q-------------------------------------P----L--K----Q-------------------------S------------L--DQ-----------------------SK--W--------L-R------EAE--------K--HL-------------------R---------------------------A--------------------------LE--------S-----------------------------L----VD--------------------------------------------------------------SNL------------E------EE---------------------KLK-------PQ------L-----------------S------------------------------------------------------------M-------------G-E-----D--V-----------------------------------------------------------QS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str26: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N----L----------------IT---------------------------------------------------------------------------------------------------------------------R-------------------------------T------Q-------------------S---------------------------------------Y-----TN---S--FT-RG-------------------------------------------VY-----------------------------------------------------------------------------------------------------------------YPD-KV--F---------------RS-----------S----------------------------------------------------------VL--HS----------------------------------------T-----------------------QD-------------------------------------------------------------------------------------------
> str27: M-----------K---FDV---------------------L-------------------------------------------------------------------------S------------LFA----------------------------PW----A-----------------------K---------------------------------V---D----E----Q------E----------------------------------Y----D--------------Q--------------------------------------Q-LNNNLE-------------------------------S----------------------------------I-TA----------------P-KFDDGA-------------T-----E--------------I-ES--E------------RG--D---I---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str28: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N-F---------TN-----R---T------QL-------------------------------P-------S--------A------------------------------------------------------------------Y-------------------------T-N------------------------S--F---T--------------------------R---GVY--------------------------------------------------------------Y------------P-------D-----------KV---F-RSSVL---------------------HS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M------------------------WS-------I----I-VLK-L----------I---------------------------------------------------------S------I----Q-------------------------------P---------L-------------L---------L-----------------------------V------T--------S----------------------------L-P-----L--Y-N-----------------------------P----------------NM-D---------------------------------------------S-----------C-C--L-----------------IS---------------------------R--------------------------------I-----------T------------------------------------P--------E---L--A-------------------------G----------------------KL------------------T---------------------------------------------------------------------------------------------------------------------------------W--------IFI-------------------------------------------------------------------------------------------------------------------------------------
> str30: M----E--SL--------V-PGFN----E--------------K----T------H------------------------------------------------------------------------------------------------VQLS-LP----V----LQ----------------------------------------------------V--RDV--L--------V-----------------------------------------------------------------------------------------------------------R-GFGD-----------------------S--------------------------------------------------------------------V-EE-----------F--------------------L-------------------------------------------------------S---E-------------A------------R----------------------------------Q--H---------------L----K-D--G------------------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV-------------------------------------M---------------P------------L-F--N-L-------------IT--------------------------------T--T---------Q-----------------------------------------------------------------------------S------Y-----T-------------------------------------NF-----------------------T----------RG-------------------------------------------VY-----------------------------------------------------------------------------------------------------------------YPD-KV--F---------------RS-----------S----------------------------------------------------------VL--H--L-----------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M-----H------------------------------Q-I--------T-------------------------------------------------------------------------------------------------------V----------V-------------------------------------------S-G-------PT--EV---------------S-------------T-CFG--------------------S-----------------------------L-HP----F---------------------Q--------------------------------------S-L------------------------------------------K---------P-------------V------------------------------------------------------------------------MAN--------A-----LG------V-LE-----------------G----------------------K-M-FC-----------SI-------GG--------------------------------RS-------L---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: MA-T-----LL-------------R-S-------------L---------A--------------LF-K-----------------------------R----------NKDKP--------------------------------------------P----------------------------I------------------------------T-S------------G----S-------G--GAI-----------------------------------------------------------------------------------------------R-G---------------IKHIII--------------------------------------------------------------------------V-----P---------------------I------------------------------------------------P---------GD---S------------S------------------I---------T---------------------------T---------------------------------------RSR----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str34: M----E--SL--------V-PGFN----E--------------K----T------H------------------------------------------------------------------------------------------------VQLS-LP----V----LQ----------------------------------------------------V--RDV--L--------V-----------------------------------------------------------------------------------------------------------R-GFGD-----------------------S-----------------------------------------------MEE------------------V----------LSEA---R-------------Q--HL--------KD-GT---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N----L------T----------T---G------------------TQ-------------L-PP-A-----Y------T-----------------------------------------N------------------------------------------------S-----------------------F------------T--------------------------R---GVY--------------------------------------------------------------Y------------P-------D-----------KV---F-RSSVL---------------------HS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA-----------NI-------------------I-----------NL---------------------------------------------------------------------------------------------------------------W----------------------------------------------N--GI-----------V----------------------------------------------P--------------------------------------------------------M-----------V------QD--------------------------------------------------------------------------------------------------V-------N-V---A----------------S-------ITA--FK----------------------------------------------S---------------------------------------------------M----IDE----------T---------------------------------------------------------------------------------------------------------------------------------W--D--------KKIEAN----------TC------I-----------------SRKHRN-------------------------------------------------------------------------------------
> str37: M--------L---N----------R---------I--Q----------T----------------L-------MK-------------------------------------------------------------------------------------------TA--------------------------------------N------N----------------------------------------------------------------Y-----ET------------------IEIL---------------------------------------R------N-Y-L---------------------------------------------------------------------------------R---------------L----------------------------------------------------YII----LA-------------------------------R---------N-EE-G---R----G-------I------L-----I----------------------------Y-DD-------NI-D----------S----------------------------------------------------------------------V------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str38: MA--D--P---A---------G--------------T---------N--G-EE-G---------------------------------------------------------------------------------------------------------------T-----------------GC--------------------N--G-----------------------------------------------------------------------WF----------------------------------------------------------------------Y-------------------------------------------------------------------------------------------V-E--A----V------V-------E-------------------K----------K--------------------------T---GD----AI----------S-----DDEN-E-------------------------------------ND---S-----D----------------------------------------------TG---ED---L---------------------------------------------------V--D---------------------------------------------------------------------------------------------------------------------------------------------------------------
> str39: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV------------------------------------------N----LR-----T------R---T------QL-------------------------------PP------SY------T-----------------------------------------N------------------------------------------------S-----------------------F------------T--------------------------R---GVY--------------------------------------------------------------Y------------P-------D-----------KV---F-RSSVL---------------------HS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M----E--SL--------V-PGFN----E--------------K----T------H------------------------------------------------------------------------------------------------VQLS-LP----V----LQ----------------------------------------------------V------------------CD--V---------------------L--------------------------V----------------------------------------------------R-GFGD-----------------------S--------------------------------------------------------------------V-EE------VLSEA---R-------------Q--HL--------KD-GT---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M------------N---------N-------------Q------------------------------------------------------------R------KK-----------------------------------------------------------TA--RP-----------------------------------SF----NMLK--------R--------------A----------------------------------------------------------------------------------------------------------R------N-------------------------------------------------------------------------------------R----V-----------S---TV-------------SQ---LA-------K-R----F---------------------------------------S----K---------------------G-----------------------L---------L-----S--------G--------------------------QG-PMKL------------------------------------------------------------------------V-------MAF--------------------------------------------------------------------------------------------------------------------------------------------------------
> str42: M-------S----N--FD---------A------I---------------------------------------------------------------R-A------L--------------------------------------------V------------DT--------DA-----------------------------------------------------------------------------------------------------Y-------------------------------------K---LGHIH-M--------------------------Y--------------------------P----------E---------G-----------T---E----------------------------Y--------VLS--------------------------------------------------------------NF------T-D------------------R--------------G-----------S-----RIE-G---------------------V------------------------------------------------T-------H----------------------------------------------------TV---H--------------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: M-------------I----E--------------------L---------------------------------------------------------R----HE-----------------------------------------------VQ------------------------------G-D-----L-----------------------------V------T---------------------I----------------------------N-------------V-----------------V-E----------------------------------------------------------------TP----------EDL---D---GF-------------------------------------R-DF-----------------------------I------------------R--A--H---L-ICLAV---D---------------T--E-----------------------------------T-----------TG-------L-D---I----------------------------Y------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str44: M---------------F-V---F-----------------LVL--L-----------------------------P----L-----------------------------------------------------------------------V--S----SQCV-------------------------------------M---------------P------------L-F--N-L-------------IT--------------------------------T-----------------------------------------N---------Q--------------------------------------S------Y-----T-------------------------------------N-----------------------------S--FT-RG-------------------------------------------VY-----------------------------------------------------------------------------------------------------------------YPD-KV--F---------------RS-----------S----------------------------------------------------------VL--H--------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-------S---K----D----------------------LV--------A-----------------------------------------------RQA------LM---------------------------------------------------------TA--R------------------------------MKADF----------------VF--------F----L------FV---------------------L-------------W----------------------------------KA--L-------------------------------------------------------S-L-P----------------------------------------------------------------V-----PT----------R----C--------Q------I--D------------------------------MA-----KKL---------SA-------------------------G-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str46: MA------SLL-K-------------S-------------L-------T----------------LF-K-----------------------------R-------------------------------------------------------------------T---R----D------------------------------------------------------------Q--------------------------------PP----LAS---------------G----------------------------------------------------------------------------------S------------------------G-GA------I----------------------------R---G----------------------------I----------------K-------H---------V-II-------------------------------V-L-----------------------IP--GD-S---------------------------SI--V------------------------------------------------T-RSR----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M-R---------------V-----R--------GI-----L---------------------------------------------------------R----------N-------------------------------------------------W-Q-------Q---------------------------------------------------------------------------------------------------------------W-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------W--------I---------------------------------------------------------------------------------------WT-S--LGFWMFMICSVVGNL--WVTVY--------YGVPVWKEAKTT
> str48: MA----------------VEP-F----------------------------------------------------P----------------------R-----------------------------------------------------------------------RP---------------I------------------------------T------R-------------------------------------------P---HA--S--------------------------IE------VD-----------------------------------------------------------------T--------------------------S---GI------GG-------------------------------------S-A----G-----------S------------------------------------------------------------S---EKV---FC----L---------------I---G-----------------------------Q-----A-E-GGEP-----------------N----------------------T-------------------------------------------------------------V------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str49: M---------------F------------------------------------------------------------------------------------------------------------------------------YA-HAFGG-------------------------------------------------------------------------------------------------------------------------------Y----DE------------------------------------------N-L-HAFPGI---------------------------------------S-----------------------------S------T-------------------------------V----A--NDV-------R--------------------------K------------------Y---------------------------S-----V--------V-----------------------S-------------------------------V--------------Y----------N---KK-----------------------------------------------Y-----NI------------------------V-----K----N-KY--MW------------------------------------------------------------------------------------------------------------------------------------------------
> str50: MA-----------N---------------------------------------------------------------------------------------------------------------------------------Y-----------SK-P---------------------F-L---------L-DI--------------------------VF-----------N----------------------KD---IKCI-------------N--D---S--C-------------------------------------------------------------------------------------S----------------------------HSDC-------------------------------R-----Y--Q-------S--------------------------------------------------------------N----------------S-------------------------------------------------------------------------------------Y----V-E--L-------------R-R------------------NQAL--NKNL------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

In [ ]:
```python
bench0(scsp.example.load("protein_n050k050.txt"))
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
> --- Solution (of length 498) ---
>   Sol: MAFVFLESVLLPLVSSQCVNRPGFKNEDLKTHVQLSLPRAITRVLFQVSTGYALEIRDVLSPQLTKVRNGFMPLAGDSPTIEFLNDAYTVKLEQWNSFTRGIVDHAETYQPCGKIVLNRTAPSEAFNYLQGSAEKDHLMRTIEQLAVFPDKSEVILTRQHAGYPFSENDRTLKNSFAVRGQLTRGVYSDILPNVKTASGINLHPYPDKVFRSETSQLGVYLHSADFKRINPLCTNGSMRADEGKHVLWDAFSIPYTNVLEADGSVRIKGVELFTAIKPQGRDSWACSHITVLESDGKAFTRYEILNDRKVQGPADMSRIKLVTYFACSELIGQAHRYWLEGVSTNPDKHTVAILPDGEQSNDSFRISTPECLGFAVDSEGKILHIYNDSATVDERCLQWTMPRGIDFIRANEKHSGVKAECRLTNPDQYAGLNIVQKDSNRKIYMAKECDFHVIDLRICSVVGNLYWADKAHLINVTSAGQSTIVYYGVPVWKEAKTT
> str01: M-------------------R----------H--L---------------------------------N-----------I----D---------------I----ETY-------------S--------S-----------------------------------ND--------------------I----K-----N----------------GVY------K---------------------------Y-----AD------------A-----------------E-D---F---EIL---------------L---FA----------Y-----S---------I--DG---------------G-----E------------V-E-CL--------D----------------LT----------------R---------------------------------------------------------
> str02: M-----E-------------R-----------------RA----------------------------------------------------------------H-------------RT----------------H------Q-----------------------N-------------------------------------------------------------------------------WDA-----T-----------K---------P--R-----------E-------R------RK-Q-----------T---------Q-HR--L----T----H-----PD-----DS--I-------------------Y---------------PR-I------EK-----AE----------G---------RK-----E-D-H----------G-----------------------------------
> str03: M-----E----P----------G----------------A-----F--ST--AL----------------F-----D---------A----L-------------------C-----------------------D-------------D----IL---H---------R--------R--L------------------------------E-SQL----------R----------------------F-----------G-----GV--------Q---------I-----------------------P--------------------------------P-----------E-----------------V-S---------D-------------PR-------------V-----------YAG------------Y-A---------L--------L---------------------------------
> str04: M---------------------G-K--------------------F-----Y-----------------------------------Y--------S--------------------NR--------------------R----LAVF------------A-------------------Q---------------A------------------Q------S----R----------------H-L---------------G-----G-------------S------------------YE-------Q--------------------------WL------------A------------------C----V-S-G-------DSA----------------F-RA-E----VKA--R------------VQKD------------------------------------------------------------
> str05: --F-F---------------R-----E-----------------------------------------N----LA-------F----------Q---------------Q--GK------A------------------R--E----FP--SE-------------E---------A-R-----------------A---N----------S------------------P--T--S-R--E----LW---------V-------R--------------R--------------G---------------G--------------------------------NP-------L-----S---------E----A----G---------A---ER-------RG-------------------T--------------------------------------------------------------------------
> str06: M--------------------------D---------P----------S----L----------T----------------------------Q--------V------------------------------------------------------------------------------------------------------------------------------------------------W-A-------V-E--GSV------L----------S-A------------A-----------V----D-------T--A--E--------------TN-D--T-------E----------P-------D-EG--L-----SA---E----------------NE---G---E---T----------------R-I----------I--RI------------------T--G-S----------------
> str07: MAF------------------------D-----------------F--S---------V-----T----G--------------N---T-KL-----------D---T--------------S-------G----------------F--------T-Q--G---------------V---------S---------S---------------------------------------M-----------------T-V--A-------------A----G---------T-L-----------I---------AD-----LV-------------------------K-T-A-------S--S----------------------------------Q------------------------LTN------L-------------A----------------------------------QS----------------
> str08: MA-V------------------------------------I---L----------------P---------------S-T-------YT--------------D--------G------TA---A-----------------------------------------------------------------------------------------------------------CTNGS----------------P-------D--V----V---------G---------T-----G---T---------------M---------------------W---V--N----T--ILP-G----D-F---------F------------------------WT-P------------SG---E------------------S-------------V---R---V-------------------------------------
> str09: M------------------N----------T-------------------G----I------------------------I----D-----L-----F-----D-------------N------------------H---------V--D-S--I--------P------T------------------ILP----------H------------QL------A---------T------------L-D-----Y---L-----VR-------T-I------------I-----D-------E--N-R--------S----V-------L--------L------------------------F-------------------HI---------------M--G----------SG----------------------------------------------------------------------------------
> str10: M-FVFL--VLLPLVSSQCVN--------L---------R--TR------T------------QL--------P-----P-------AYT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M--------------------------D-------S-----------------------------K---------------E------T------------I--------------L------------------------IE-----------I----------------------------------I-P--K----I-------K---S-------YL----------L--------D--------------TN---------I---------------S-----------------------------P------K-------S--------Y-------N-D----------------F-IS---------------------------R---------------N-K-----------N--------I----------------F-VI---------NLY--------NV-S----TI--------------
> str12: M----L---L----S-------G-K----K-----------------------------------K-----M-L---------L-D---------N------------Y--------------E----------------T----A--------------A---------------A-RG---RG-------------G-------D-----E--------------R----------R--------------------------R--G--------------WA-------------F-------DR----PA----I--VT------------------------K----------------R-----------D---K-------S---D-R-----M--------A---H------------------------------------------------------------------------------------
> str13: M------------------N--G---E---------------------------E--D------------------D-------N-------EQ-----------A--------------A---A--------E---------Q--------------Q-----------T-K---------------------K-A----------K--R-E-------------K---P------------K----------------------------------Q-----A---------------R-------KV------------T----SE----A---W-E--------H--------------F------------D------------AT-D------------D---------G--AEC---------------K--------------H----------------------------------------------
> str14: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-----------V--E-------------E--------VL-----SEA--------------R---Q---------------H-----------LK---------------D---------G--------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-------------------R------------------------------Y---I--V-SPQL--V------L-------------------Q--------V---------GK----------------G------------Q--------EV------------E--R------A----L----Y---L----T-------PY-D------------Y--------I-----------DE-K-------S-P------------I----------------------------------Y---------------------YF----L-----R------S-----H----L------N----I-------------------------------Q----R----------------------P------------------------------------------------------------------------
> str16: M----------P--------R-----------V----P-----V-------Y-----D--SPQ---V----------SP-----N---TV--------------------P------------------Q--A------R----LA----------T------P-S---------FA-----T--------P---T-------------FR------G-----AD--------------A-------------P------A-----------F-----Q--D-------T-------A-------N----Q---------------------QA-R----------------------Q-------------------------------------------------------------------------------------------------------------------------------------------
> str17: M-FVFL--VLLPLVSSQCVN--------L---------R--TR------T------------QL--------PLA------------YT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FVF------------------F--------V-L-LP------L--VS-----------S-Q------------------------------------------------C---V-N----------L-----------T---------------TR------------T---------QL---------P-----------P-------------------A------------------------------YTN------S--------FT------R--------------G-------------V-------------Y------------Y--------PDK--V------------FR-S----------S-------------V----L----------------HS-----------------------------------------------------------------------------------
> str19: M-----E--------------------------------AI--------------I----S---------F---AG----I-------------------GI---------------N---------Y------K---------------K----L--Q------S------K--------L---------------------------------Q-----H--DF---------G--R------VL--------------------K------A----------------L-------T---------V------------T--A---------R---------------A-LP-G-Q---------P-----------K--HI----A--------------I---R------------------Q----------------------------------------------------------------------
> str20: MA-----S------S-------G--------------P----------------E-R-----------------A------E----------------------H----Q----I--------------------------I--L---P---E------------S------------------------------------H-------------L-----S-------------S----------------P----L-----V--K-------------------H--------K-------L---------------L--Y------------YW---------K-----L-------------T----G---------L------------------P--------------------L--PD--------------------ECDF---D----------------HLI------------------------
> str21: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-----------V--E-------------E--------VL-----SE----------------------V----------RQH-----------LK---------------D---------G--------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M----L---------------------------------A---------------------P---------------SP-----N-----------S----------------KI--------------Q-------L---------F-------------------N-----N---------------I--N------I------D---------------------IN------------------------Y----E---------------------------H-T-L---------Y----------------------FA-S-------------VS--------A------Q-N-SF---------FA----------------------QW-----------------V-----------------V--------Y---------------S-------ADKA--I------------------------
> str23: M------S-------------------------------AIT------------E---------TK------P------TIE-L--------------------------P---------A-------L---AE---------------------------G--F---------------Q--R--Y-----N-KT-------P-------------G-------F-------T---------------------------------------------------C----VL--D-----RY----D---------------------------H-----GV----------I-------NDS-----------------KI---------V----L-------------------------------Y---N-----------------------------------------------------------------
> str24: M-----------------------KN--------------I-----------A-E---------------F-------------------K----------------------K------AP-E----L---AEK--L------L-------EV----------FS-N---LK------G------------N----S------------RS----L-------D-----P------MRA--GKH---D--------V------V----V-----I----------------ES-----T--------K----------KL---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str25: M----------P----Q----P------LK---Q-SL--------------------D----Q--------------S------------K---W---------------------L-R----EA--------EK-HL-R-----A---------L----------E-------S------L---V--D--------S--NL----------E----------------------------E-----------------E-------K---L----KPQ------------L-S---------------------M---------------G-------E------D---V-------QS------------------------------------------------------------------------------------------------------------------------------------------
> str26: M-FVFL--VLLPLVSSQCVN--------L-----------ITR------T------------Q--------------S---------YT------NSFTRG-V-----Y------------------Y--------------------PDK--V----------F----R----S------------S-----V-------LH--------S-T-Q--------D---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M-----------------------K--------------------F-----------DVLS--L------F---A---P---------------W----------A-------K-V-------------------D------EQ--------E---------Y-----D-----------Q----------------------------------QL------------N----N---------------------N-LE---S--I------TA--P------------------K-F-------D-------D----------------G-A---------T-------------E-------I---E-------SE---------------R--------G-D-I------------------------------------------------------------------------------------------
> str28: M-FVFL--VLLPLVSSQCVN---F------T-------------------------------------N------------------------------R-------T-Q------L----PS-A--Y------------T--------------------------N------SF------TRGVY-----------------YPDKVFRS--S---V-LHS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M---------------------------------------------------------------------------------------------W-S----I------------IVL-----------------K--L---I---------S--I---Q----P-------L---------L--------L--V-T-S---L-P------------L--Y---------NP---N--M--D----------S---------------------------------C----------------------------------------C--LI-----------S---------------------RI-TPE-L--A----GK-L-------T-------W-----I-FI------------------------------------------------------------------------------------------
> str30: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS-----------V--E-------------E------------------F--L--S-E-----------A-----------RQH-----------LK---------------D---------G--------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FVFL--VLLPLVSSQCV----------------------------------------------------MPL--------F-N------L---------I-----T-----------T--------------------T--Q-------S----------Y-------T--N-F------TRGVY-----------------YPDKVFRS--S---V-LH---------L--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M------------------------------H-Q------IT-V---VS-G----------P--T----------------E-------V------S-T------------C-------------F----GS-----L---------------------H---PF---------------Q------S--L---K--------P----V----------------------------M-A----------------N---A----------L-------G----------VLE--GK------------------M--------F-CS--IG--------G-----------------------R-S----L------------------------------------------------------------------------------------------------------------------------------
> str33: MA----------------------------T---L-L-R---------S----L--------------------A--------L-------------F---------------K----R-------N-------KD--------------K------------P---------------------------P-------I-------------TS--G----S------------G------G------A--I------------R--G------IK----------HI--------------I--------------I--V-----------------------P------I-P-G----DS---S--------------I--------T--------T--R-----------S------R----------------------------------------------------------------------------
> str34: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV--------RDVL------VR-GF----GDS------------------------------------------------------------M---E---------EV-L---------SE---------A-R-Q---------------------H-------------L---------K-------------D-G------------T--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FVFL--VLLPLVSSQCVN--------L-T----------T--------G-------------T----------------------------Q----------------------L----P--------------------------P-----------A-Y-------T--NSF------TRGVY-----------------YPDKVFRS--S---V-LHS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA-----------------N--------------------I--------------I------------N----L--------------------WN----GIV-------P---------------------------M-------V-----------Q---------D--------V--------------NV--AS-I-------------T---------A-FK---------SM--------------I--------D--------E--T---------W----------D-K-----------K---------I---------E----A----------N----T--------------------C----------I------S-----R-----------------KH-------R--N-------------------------------------------------------------------------
> str37: M----L-------------NR-------------------I-----Q--T---L-----------------M------------------K-------T------A-----------N--------NY-----E------TIE-----------IL-R---------N------------------Y---L-------------------R-----L--Y--------I-----------------------I-----L-A----R---------------------------------------N----------------------E----------EG-----------------------R-------G--------IL-IY-D----D-----------------N----------------------I---DS-------------V---------------------------------------------
> str38: MA-------------------------D---------P-A----------G-------------T---NG-----------E----------E-------G------T----G-----------------------------------------------------------------------------------------------------------------------C-NG-----------W--F---Y--V-EA---V----VE-----K-------------------K--T-----------G--D----------A----I-----------S---D--------D-E--N--------E----------------NDS---D------T---G-------E--------------D----L--V--D------------------------------------------------------------
> str39: M-FVFL--VLLPLVSSQCVN--------L---------R--TR------T------------QL--------P-----P-----------------S-----------Y----------T------N----S---------------F--------TR---G---------------V--------Y-----------------YPDKVFRS--S---V-LHS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M-----ES-L---V-------PGF-NE--KTHVQLSLP-----VL-QV---------------------------------------------------------------C-----------------------D----------V--------L---------------------VRG-----------------------------F-------G------D-----------S--------V-------------E----------E-------------------VL-S--------E----------A---R--------------Q-H---L--------K-------DG----------T----------------------------------------------------------------------------------------------------------------------------------
> str41: M------------------N-----N-------Q----R--------------------------K------------------------K-------T------A------------R--PS--FN-----------M-----L-----K------R--A--------R---N----R------V-S-------T------------V--S---QL------A--KR----------------------FS---------------KG--L-------------------L-S-G--------------QGP--M---KLV------------------------------------------------------------------------------M--------A----------------------------------------F-----------------------------------------------
> str42: M------S-----------N---F---D-----------AI-R---------AL----V-----------------D--T-----DAY--KL--------G---H---------I---------------------H-M-----------------------YP--E------------G--T-----------------------------E------Y-------------------------VL----S----N---------------FT-------D------------------R----------G----SRI---------E--G---------V-T----HTV--------------------------------H------------------------------------------------------------------------------------------------------------------
> str43: M---------------------------------------I-------------E----L-------R------------------------------------H-E--------V-------------QG----D-L--------V---------T--------------------------------I--NV--------------V---ET----------------P----------E------D---------L--DG---------F-------RD----------------F----I---R-----A--------------------H---L-------------I-----------------CL--AVD-------------T--E-----T-----------------------T------GL-----D----IY------------------------------------------------------
> str44: M-FVFL--VLLPLVSSQCV----------------------------------------------------MPL--------F-N------L---------I-----T-----------T------N--Q-S------------------------------Y-------T--NSF------TRGVY-----------------YPDKVFRS--S---V-LH------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M------S----------------K--DL---V------A--R---Q-----AL-----------------M-------T------A------------R--------------------------------------M-----------K---------A-------D------F-V-------------------------------F---------------F-----L------------------F------VL------------------------W------------KA------L-----------S---L------------------------P----V---P------------T--------------------------RC-Q------ID--------------------------------------MAK----------------------K--L----SAG------------------
> str46: MA-----S-LL-------------K----------SL----T--LF-------------------K-R-----------T-------------------R---D-----QP----------P------L---A------------------S---------G---S-------------G----G-----------A--I----------R------G----------I--------------KHV------I-------------I--V-L---I-P-G-DS---S-I-V--------TR---------------SR------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M-------------------R-----------V-----R-----------G----I---L-------RN-------------------------W--------------Q-------------------Q---------------------------------------------------------------------------------------------------------------------W-----------------------------------W----I------------------------------------------------W-----T---------------S-----------LGF------------------------W-M-----F-------------------------------------M--------I----CSVVGNL-W--------VT-------VYYGVPVWKEAKTT
> str48: MA-V--E----P-----------F-------------PR---R------------------P------------------I-------T----------R----------P-------------------------H--------A-----S--I-----------E----------V----------D------T-SGI-----------------G-----------------GS--A--G--------S-----------S------E-----K-------------V-------F---------------------------C--LIGQA-----EG---------------GE----------P-----------------N---TV----------------------------------------------------------------------------------------------------------
> str49: M-F------------------------------------------------YA---------------------------------------------------HA-------------------F----G------------------------------GY-----D-------------------------------------------E----------------N-L------------H----AF--P--------G---I---------------S---S--TV------A-------ND--V-------R-K---Y---S-------------V--------V--------S---------------V---------YN-------------------------K----K----------Y---NIV-K--N-K-YM---------------------W-------------------------------
> str50: MA-----------------N-------------------------------Y--------S----K------P---------FL-------L-----------D----------IV---------FN-------KD-----I--------K---------------------------------------------------------------------------------C-------------------I---N----D-S---------------------CSH-----SD-------------------------------C--------RY---------------------QSN-S----------------------Y-----V-E--L-----R-----R-N----------------Q-A-LN---K--N---------------L------------------------------------------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 0
> ```

元の `WMM_HEXALY` よりもだいぶ悪い結果となった.
