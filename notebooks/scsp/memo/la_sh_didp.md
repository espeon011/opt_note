In [ ]:
```python
from dataclasses import dataclass
import opt_note.scsp as scsp
import datetime
import didppy
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# `LA_SH` アルゴリズムのサブルーチンを DIDP で置き換えてみる

In [ ]:
```python
def find_next_strategy(
    instance: list[str],
    chars: str,
    m: int,
) -> str:
    """
    現在の状態を受け取り, m 手進めたときに sum height が最大になる文字の選び方 (長さ m 以下の文字列として表される) を返す
    """

    dpmodel = didppy.Model(maximize=True, float_cost=False)

    instance_table = dpmodel.add_element_table(
        [[chars.index(c) for c in s] + [len(chars)] for s in instance]
    )

    index_types = [dpmodel.add_object_type(number=len(s) + 1) for s in instance]
    index_vars = [
        dpmodel.add_element_var(object_type=index_type, target=0)
        for index_type in index_types
    ]
    sol_len = dpmodel.add_int_var(target=0)

    dpmodel.add_base_case([sol_len == m])

    # 文字 char に従って進む
    for id_char, char in enumerate(chars):
        sum_height = sum(
            (instance_table[sidx, index_var] == id_char).if_then_else(1, 0)
            for sidx, index_var in enumerate(index_vars)
        )
        trans = didppy.Transition(
            name=f"{char}",
            cost=sum_height + didppy.IntExpr.state_cost(),
            effects=[
                (
                    index_var,
                    (instance_table[sidx, index_var] == id_char).if_then_else(
                        index_var + 1, index_var
                    ),
                )
                for sidx, index_var in enumerate(index_vars)
            ]
            + [(sol_len, sol_len + 1)],
            preconditions=[sum_height > 0],
        )
        dpmodel.add_transition(trans)

    # Force transition
    end = didppy.Transition(
        name="",
        cost=didppy.IntExpr.state_cost(),
        effects=[(sol_len, m)],
        preconditions=[
            index_var == len(s) for s, index_var in zip(instance, index_vars)
        ],
    )
    dpmodel.add_transition(end, forced=True)

    # Dual bound
    dual_bound_table = dpmodel.add_int_table(
        [[min(m, len(s) - idx) for idx in range(len(s) + 1)] for s in instance]
    )
    bound = didppy.IntExpr(0)
    for sidx, index_var in enumerate(index_vars):
        bound += dual_bound_table[sidx, index_var]
    dpmodel.add_dual_bound(bound)

    dpsolver = didppy.CABS(dpmodel, threads=8, quiet=True)
    solution = dpsolver.search()

    return "".join([trans.name for trans in solution.transitions])
```

## 計算時間の比較

In [ ]:
```python
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, m: int = 3, ll: int = 1, *args, **kwargs) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        state = tuple(0 for _ in self.instance)
        solution = ""

        count = 0
        while not all(idx == len(s) for idx, s in zip(state, self.instance)):
            next_str = find_next_strategy(
                [s[idx:] for idx, s in zip(state, self.instance)], chars, m
            )
            if len(next_str) == 0:
                break
            count += 1
            # print(f"{count=}, {next_str=}")
            solution += next_str[:ll]
            for next_char in next_str[:ll]:
                state = tuple(
                    idx + 1 if idx < len(s) and s[idx] == next_char else idx
                    for idx, s in zip(state, self.instance)
                )

        self.solution =  solution
        return self.solution
```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q26n004k015-025.txt")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 70) ---
>  Sol: itkgnekojiqfouhlcimpnbvaxxnhtqcgxycozgbrddbcsovxiorsuqzpplpvinngfssbxf
> str1: -tkgn-k------uh---mp----x-nhtq-gx---z---------vxi--s------------------
> str2: i------ojiqfo--l----nb--xx----c---------------v----suq-p---vi----ssbxf
> str3: -------------u-lci--n------------yco--------sov--o----zpplp-----------
> str4: i--g-e----------------va------------zgbrddbcs-v---r--------v-nngf-----
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 70
> best bound: 0.0
> wall time: 0.007853s
> ```

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
> --- Solution (of length 68) ---
>  Sol: itkgnekuhlcojimpxnhtqfycoslnbgxzoxcvaozxigpsubqrddbcspvirssvnblngxpf
> str1: -tkgn-kuh-----mpxnhtq--------gxz---v---xi--s------------------------
> str2: i----------oji------qf--o-lnb-x--xcv-------su-q------pvi-ss--b---x-f
> str3: -------u-lc--i---n----ycos------o--v-oz---p----------p--------l---p-
> str4: i--g-e-----------------------------va-z--g---b-rddbcs-v-r--vn--ng--f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 68
> best bound: 0.0
> wall time: 0.626536s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q26n008k015-025.txt")
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
> --- Solution (of length 132) ---
>  Sol: eingeojipbdcevaqdcrtkzfgjtbnkuhlcimpvxdnerddbycopflrhnzbsmorvigoplersbrowtxqgxckrdrlctodtmzprplpucpmqvxbbghinngfstdfuiqpvcdissbowdxf
> str1: -------------------tk--g---nkuh---mp-x-n------------h--------------------t-qgx------------z----------vx----i----s-------------------
> str2: -i---oji-------q------f------------------------o--l--n-b------------------x--xc----------------------v----------s---u-qpv--issb---xf
> str3: -----------------------------u-lci-----n-----yco--------s-o-v--o--------------------------zp-plp------------------------------------
> str4: -i-ge--------va------z-g--b--------------rddb-c---------s---v------r---------------------------------v------nngf--------------------
> str5: --------p------------------------------------y--p-lr--z-------------------x---------------------ucpmqv---g-------tdfui--vcd-s-bo----
> str6: --------pbd-ev--dc------------------v-d---------pf----z-sm----------sbro---q-------------------------v-bb-h-------------------------
> str7: e-n------b-c---------zf-jt----------vx--er------------zb---rvig-ple-----------------------------------------------------------------
> str8: ------------------r------------------x----------------------------------w-xq---krdrlctodtm-prp--------x-------------------------wd--
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 132
> best bound: 0.0
> wall time: 0.074634s
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
> --- Solution (of length 112) ---
>  Sol: igenpbdcevazfojtdcrvxkgberydpfzdbulcinrsvzwxqkruvnfychmoplxsnbdromqvhiglctodztmprpxfqgxcluizvcwdsuqxpvbisseobhxf
> str1: ---------------t-----kg--------------n-------k-u-----hm-p-x-n-------h----t----------qgx----zv------x---is-------
> str2: i------------oj---------------------i-------q-----f----o-l--nb--------------------x---xc----v---suq-pv-iss--b-xf
> str3: ---------------------------------ulcin-------------yc--o---s----o--v------o-z--p-p------l-----------p-----------
> str4: ige------vaz----------gb-r-d---db--c---sv-----r-vn----------n---------g------------f----------------------------
> str5: ----p---------------------y-p-----l---r--z-x---u----c---p--------mqv--g--t-d-------f-----ui-vc-ds-----b----o----
> str6: ----pbd-ev------dc-v-------dpfz--------s--------------m----s-b-ro-qv----------------------------------b-----bh--
> str7: --en-b-c---zf-jt---vx---er----z-b-----r-v----------------------------ig--------p--------l-----------------e-----
> str8: ------------------r-x---------------------wxqkr---------------dr-------lctod-tmprpx-----------wd----------------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 112
> best bound: 0.0
> wall time: 2.029878s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q26n016k015-025.txt")
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
> --- Solution (of length 170) ---
>   Sol: kpriflshtkqagenbkvxuwdgsfchxeqjafnvzfmpacdigqbcejtivwbahcokrdxerlcnvpfzksgjmiudbcrsvihtjodqbgkderwxzavntfmoybplngqrbpzvxucbbhefikoshmgopmqvgtowdfuivxcdvsbouqyzpplpvissbxf
> str01: --------tk--g-n-k--u------h----------mp----------------------x----n------------------ht---q-g-----xz-v-----------------x-------i--s---------------------------------------
> str02: ---i-----------------------------------------------------o----------------j-i-------------q-------------f-o---ln---b---x----------------------------xc-vs--uq--p---vissbxf
> str03: -------------------u--------------------------------------------lc----------i-------------------------n----y-------------c-------os---o---v--o----------------zpplp-------
> str04: ---i--------ge---v-------------a---z-------g-b-------------rd-----------------dbc-sv------------r----vn--------ng-------------f-------------------------------------------
> str05: -p---------------------------------------------------------------------------------------------------------y-pl---r--z-xuc-------------pmqvgt--dfuiv-cd-sbo---------------
> str06: -p-------------b-----d------e-----v------d----c----v--------d-------pfz-s--m------s--------b----r---------o------q----v---bbh---------------------------------------------
> str07: -------------enb---------c---------zf-----------jt-v---------xer------z--------b-r-vi-------g----------------pl--------------e--------------------------------------------
> str08: --r---------------x-w------x-q----------------------------krd--rlc--------------------t-od-------------t-m---p----r-p--x----------------------wd--------------------------
> str09: k--------kqa------------f-----------------igq---j---w----ok------------ks--------------------k--r-----------b-l-g---------------------------------------------------------
> str10: -----l------------x--------x----------pa-----b----iv-b-------------v--zk----------------o----------z-----------------zv------------------------d--------------------------
> str11: k-rif-s----a-----v---------------n------cd--q-------w--h--------------z---------c-----------------------------------------------------------------------------------------
> str12: ----------qa------xu-dg------q----v---------q-ce----wb---------------f---g--i----------jo--------w--------------------------------------------w--------------y------------
> str13: --r---s-----------x----------qj--n--f-pa-di----------------------------------u----s-i-----qb---e---z------------------------h---ko-hmg------------------------------------
> str14: ---i----------------w--s--h-------v--------------------hco-----------------miu-----v-----d----d----------m----------------------------------------------------------------
> str15: -------ht---------x--------x-qj----z--------qbc--t---ba---k-------n-------------------------------------------------------------------------------------------------------
> str16: ------------------xu---sfc------f--z--p--------e--------------e--c-v-----------------------------w--a-ntfm------gq---z--u-------------------------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 170
> best bound: 0.0
> wall time: 0.617095s
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
>   Sol: kripxwuslxqhftkcgevaxjnfzpabdieusvdcgbqarvdnypfzhckodjiqbcesfmolvrzwxiuchozvnbpmgqjpwxanlctvfodkxgtdohmfkpskerzgqbcrtoqvigpxszluivcwdsjboqpvxissaekgnbhwwxfy
> str01: -------------tk-g-----n---------------------------k-------------------u-h------m---p-x-n-------------h--------------t-q--g-x-z---v----------xis-------------
> str02: --i------------------------------------------------o-jiq----f-ol------------nb-------x----------x-----------------c----v----s--u---------qpv-iss-----b---xf-
> str03: ------u-l------c-------------i-------------ny----c-o-------s--o-v--------oz---p----p----l----------------p--------------------------------------------------
> str04: --i-------------geva----z-----------gb--r-d---------d---bc-s----vr---------vn----------n---------g-----f----------------------------------------------------
> str05: ---p----------------------------------------yp-----------------l-rz-x-uc------pm-q---------v-----gtd---f-----------------------uivc-ds-bo-------------------
> str06: ---p-----------------------bd-e--vdc-----vd--pfz-----------s-m--------------------------------------------s------b-r-oqv---------------b-------------bh-----
> str07: -----------------e----n----b-------c-----------z------------f---------------------j-------tv----x-----------erz--b-r---vigp---l------------------e----------
> str08: -r--xw---xq---k-------------------------r-d----------------------r----------------------lct--od---t---m--p---r------------px-------wd-----------------------
> str09: k-------------k-----------------------qa------f-------i-------------------------gqj-w--------o-k--------k-sk-r---b------------l--------------------g--------
> str10: --------lx----------x----pab-i---v---b---v-----z--ko--------------z-------zv------------------d-------------------------------------------------------------
> str11: kri---------f-------------------s------a-v-n-----c--d--q-----------w----h-z--------------c------------------------------------------------------------------
> str12: ----------q--------ax----------u--d-g-q--v-------------q-ce--------w---------b--------------f----g----------------------i-------------j-o--------------ww--y
> str13: -r-----s-xq----------jnf-pa-di-us---------------------iqb-e-------z-----h----------------------k----ohm--------g--------------------------------------------
> str14: --i--w-s---h------v-----------------------------hc-o---------m-------iu----v------------------d----d--m-----------------------------------------------------
> str15: -----------h-t------x-----------------------------------------------x------------qj---------------------------z-qbc-t------------------b--------a-k-n-------
> str16: ----x-us----f--c-------fzp----e---------------------------e------------c---v--------w-an--t-f---------m--------gq------------z-u----------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 156
> best bound: 0.0
> wall time: 5.833112s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q05n010k010-010.txt")
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
> --- Solution (of length 31) ---
>   Sol: abdcbacdbeecdaebdecbadabcdebdde
> str01: --dcb-c----cd--b--c-----c-e----
> str02: -bd----dbee---e--e-b-d---------
> str03: ---c-acd-eec--eb-e-------------
> str04: a--------e--d---d----d---debdd-
> str05: a--cb----eec-a-b--c-------e----
> str06: -b--ba--be-----bd-cba----------
> str07: -b--ba---e---aeb----ada--------
> str08: ---------ee---e--ecb-d-b--e---e
> str09: ---c--cd-ee-da--d-c--d---------
> str10: -bd--a--b---d--b-e--a-a--d-----
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 31
> best bound: 0.0
> wall time: 0.004444s
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
> --- Solution (of length 31) ---
>   Sol: bdacbacdbeecdaeebadcbddeacbddee
> str01: -d-cb-c----cd---b--c-----c---e-
> str02: bd-----dbee---eeb-d------------
> str03: ---c-acd-eec--e-b------e-------
> str04: --a------e--d-----d--dde--bdd--
> str05: --acb----eec-a--b--c---e-------
> str06: b---ba--be------b-dcb---a------
> str07: b---ba---e---ae-bad-----a------
> str08: ---------ee---ee---cbd----b--ee
> str09: ---c--cd-ee-da----dc-d---------
> str10: bda-b--dbe---a---ad------------
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 31
> best bound: 0.0
> wall time: 0.16773s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="uniform_q05n050k010-010.txt")
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
> --- Solution (of length 38) ---
>   Sol: dacbedabcedabcdeaecbdacebadbceabdcdeaa
> str01: d-cb----c----cd----b--c-----ce--------
> str02: ---b-d----d-b--e-e-----e-----e-bd-----
> str03: --c---a-c-d----e-ec----eb----e--------
> str04: -a--ed----d---d-----d--eb-d-----d-----
> str05: -acbe----e---c--a--b--ce--------------
> str06: ---b---b---ab--e---bd-c-ba------------
> str07: ---b---b---a---eae-b-a----d---a-------
> str08: ----e----e-----e-ecbd---b----e-----e--
> str09: --c-----c-d----e-e--da----d-c---d-----
> str10: ---b-dab--d-b--ea----a----d-----------
> str11: ----ed---eda----a----a-e-a----a-------
> str12: -a----a--e-a----a--b---e-----ea--c----
> str13: ----e-a----abc--a-c---c---db----------
> str14: ---b-d---e-----ea---d--e-ad--e--------
> str15: --c---a--eda--de-e-----e--d-----------
> str16: ----e--bc--a--d----b-a--b--b-e--------
> str17: d----d--ce-----ea--bd--e-a------------
> str18: da-b----c-d---deaec-------------------
> str19: -a----a---d--c-e-e--da---a-b----------
> str20: -a--e----e---c----c----e-----e-----eaa
> str21: ---b---b--da---e--c--a---ad--e--------
> str22: dac-eda--edab-------------------------
> str23: -a----a--e-ab------b----b--bce--------
> str24: d---ed-bc---bc--a----a--b-------------
> str25: d--b-da----a---e---b----b---c--b------
> str26: d---e--b-ed-b--e---b-ac---------------
> str27: --c-e----e--bcd---cbd--e--------------
> str28: d--beda----a--d-a----a--b-------------
> str29: --c-----c----cd---cb---eb-d-c---------
> str30: -a--e----e-a-cd----b--c-b-d-----------
> str31: dacbe-a-c----c----c-d-----------------
> str32: ----e---ce--bc----c-d---b-db----------
> str33: d----d-b----bc-e----da--b--b----------
> str34: -a----a--e-ab---a----a-eba------------
> str35: ----e---c---b------b--c--a----a-dcd---
> str36: d---e--bc----c-e--c-d---b---c---------
> str37: da----a-c---b---ae-----eb---c---------
> str38: -a---dab-e-a----a-c---ce--------------
> str39: da--e---c-d-b---a-c--a---a------------
> str40: dacb---b--d--c-e----d-c---------------
> str41: d---ed-b-e-----e---b----b-d--e--------
> str42: --c--da---d--cd---c-da---a------------
> str43: --c-e----ed--c-----b-a-e-----e--d-----
> str44: --c-e-a--e---c--a----a---a--c-a-------
> str45: d-c-----c----c-e---b----b--b--a-d-----
> str46: ---b--a--e-----eae-b----b-d--e--------
> str47: d--b-d---e--b---a-c---c---db----------
> str48: ----e--bc---b--e-e--da-e-a------------
> str49: -a--e----e-----e---b----b-dbc-a-------
> str50: d--b-dabce---c-----b----b-------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 38
> best bound: 0.0
> wall time: 0.023573s
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
> --- Solution (of length 38) ---
>   Sol: daecbdaebdacbecadebacbdebacebedabeadcd
> str01: d--cb------c--c-d-b-c-----ce----------
> str02: ----bd---d--be---e-----e---eb-d-------
> str03: ---c--a----c----de-----e--cebe--------
> str04: -ae--d---d------d-----deb-----d----d--
> str05: -a-cb--e-----eca--b-c--e--------------
> str06: ----b---b-a-be----b---d---c-b--a------
> str07: ----b---b-a--e-a-eba--d--a------------
> str08: --e----e-----e---e--cbd-b--e-e--------
> str09: ---c-------c----de-----e------da---dcd
> str10: ----bda-bd--be-a---a--d---------------
> str11: --e--d-e-da----a---a---e-a-----a------
> str12: -a----ae--a----a--b----e---e---a----c-
> str13: --e---a---a-b-ca----c-----c---d-b-----
> str14: ----bd-e-----e-ade-a--de--------------
> str15: ---c--ae-da-----de-----e---e--d-------
> str16: --e-b------c---ad-ba-b--b--e----------
> str17: d----d-----c-e---e-a-bde-a------------
> str18: da--b------c----d-----de-a-e--------c-
> str19: -a----a--d-c-e---e----d--a-----ab-----
> str20: -ae----e---c--c--e-----e---e---a--a---
> str21: ----b---bda--eca---a--de--------------
> str22: da-c---e-da--e--d--a-b----------------
> str23: -a----ae--a-b-----b--b--b-ce----------
> str24: d-e--d--b--cb-ca---a-b----------------
> str25: d---bda---a--e----b--b----c-b---------
> str26: d-e-b--e-d--be----bac-----------------
> str27: ---c---e-----e----b-c-d---c-b-d--e----
> str28: d---b--e-da----ad--a-----a--b---------
> str29: ---c-------c--c-d---cb-eb-----d-----c-
> str30: -ae----e--ac----d-b-cbd---------------
> str31: da-cb--e--ac--c-----c-d---------------
> str32: --ec---eb--c--c-d-b---d-b-------------
> str33: d----d--b---b-c--e----d--a--b---b-----
> str34: -a----ae--a-b--a---a---eba------------
> str35: --ecb---b--c---a---a--d---c---d-------
> str36: d-e-b------c--c--e--c-d-b-c-----------
> str37: da----a----cb--a-e-----eb-c-----------
> str38: -a---da-b----e-a---ac-----ce----------
> str39: daec-d--b-ac---a---a------------------
> str40: da-cb---bd-c-e--d---c-----------------
> str41: d-e--d--b----e---eb--bde--------------
> str42: ---c-da--d-c----d---c-d--a-----a------
> str43: ---c---e-----e--d---cb---a-e-ed-------
> str44: ---c---e--a--eca---a-----ac----a------
> str45: d--c-------c--c--eb--b--ba----d-------
> str46: ----b-ae-----e-a-eb--bde--------------
> str47: d---bd-eb-ac--c-d-b-------------------
> str48: --e-b------cbe---e----d--a-e---a------
> str49: -ae----e-----e----b--bd-b-c----a------
> str50: d---bda-b--c-ec---b--b----------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 38
> best bound: 0.0
> wall time: 0.91985s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="nucleotide_n010k010.txt")
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
> --- Solution (of length 28) ---
>   Sol: TATACACGGGATACGAATCGATCACAGA
> str01: -AT----GGGATACG-------------
> str02: -ATAC-C----T-----TC---C-C---
> str03: ----CACG--A-A----T---T----GA
> str04: TA-A-A----AT-C---T-G-T------
> str05: -A-----GG--TA--A--C-A--A-A--
> str06: T-T-C-C----TA-G----G-T-A----
> str07: T-T----G---TA-GA-TC--T------
> str08: T------GGGA-A-G--T---TC-----
> str09: T-T-C-C---A--C-AA-C--T------
> str10: T---C------TA--AA-CGA--A----
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 28
> best bound: 0.0
> wall time: 0.002503s
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
> --- Solution (of length 27) ---
>   Sol: TATCACGTAGGATACTGAATCCTAAAC
> str01: -AT---G--GGATAC-G----------
> str02: -AT-AC--------CT---TCC----C
> str03: ---CACG-A--AT--TGA---------
> str04: TA--A---A--AT-CTG--T-------
> str05: -A----G--G--TA---A--C--AAA-
> str06: T-TC-C-TAGG-TA-------------
> str07: T-T---GTAG-AT-CT-----------
> str08: T-----G--GGA-A--G--T--T---C
> str09: T-TC-C--A-----C--AA-C-T----
> str10: T--C---TA--A-AC-GAA--------
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 27
> best bound: 0.0
> wall time: 0.118291s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="nucleotide_n050k050.txt")
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
> --- Solution (of length 144) ---
>   Sol: ATGAGCTCAGCTAGATCGATAGCATCATGTCGATCTAGCTAGCGTAGATCATGACACGTACAGTAGCTCAAGCTGATATCGATGCATGACTAGCATGCTAGCATGCACTGCTACAGTGCTACGATCAGCTAGTCAACGTARGTG
> str01: -T-AG-T-AG-TAGA-C--T--C--C--G--GA---AG-T-G---A---CA--A-AC---C-----CT---G---A-A---A---A-GA--A---TG---G-AT--A-----A-A-T---A---T-A-----------------
> str02: --G-G---A--TA-A---A---CA-C-T--C---C---C--G---A-A--A--A----TA-A-T---T-----TGA---C--T---T-A--A--A--C-A--A--C---GC----G----AC-A---G-T--TCAA-G------
> str03: AT-A-C-C---T---TC-----C-T-A-G--G-T--A---A-C--A-A--A---C-C--A-A----C-CAA-CT--T-T---TG-AT--CT--C-T--T-G--T--A--G--A---T-CT--G---------------------
> str04: -T-A----A---A--T---TA---T-A-----ATCT---TA---TA---C-T-A---GTA-A--A----AA----ATA--G--G---G--T-G--T---A--A--C-C-G--A-A-----A--A-C-G---GTC----------
> str05: -T----T-A---A-A---A---CA----G-C---CT-G-T-G-G--G-T--TG-CAC---C-----C--A--CT-----C-A--CA-G----G---GC---C---CACTG-----G-GC---G--CA---AG------------
> str06: ATGA-CT----T----C-----CA--ATG--GATC---C---C--A-A-C----C---T-CA--AGCT-----T-----C----CA---C---C---C---CA---A-TG-----GT--T----TCAGC---------------
> str07: A--A-C--A---A-A-C-----CA--A---C---C-A---A-C-T---T--T------T---G-A--TC----T-----C--T---TG--TAG-AT-CT-G--T----T-CT-C--T---A--A--A-C--G--AAC-------
> str08: ATGA----A---A-A-CGA-A--A--AT-T--AT-TA--T--C--A-A----G----G----GTA--T---G--GA-A--G-TG---GA--AGC-TG--A-C--G-A-----A-A-T---------------------------
> str09: A----CTC-G---G--C--T-GCAT---G-C--T-TAG-T-GC--A---C-T--CACG--CAGTA--T-AA--T--TA---AT--A--ACTA--AT--TA--------------------------------------------
> str10: -T----T--G-TAGATC--T-G--T--T--C--TCTA---A----A---C--GA-AC-T----T---T-AA----A-ATC--TG--TG--T-G---GCT-G--T-CACT-C---------------------------------
> str11: --G--C--AG--AG--C-AT----T--T-TC--T--A---A---TA--TC----CAC--A-A--A----A---TGA-A--G--GCA--A-TA--AT--T-G--T--ACT---AC--T-C-------------------------
> str12: ATGAGC-CA---AGATC-----C-----G---A-C--G--A----AGA----G-C-C---C-----C--AAG--GA----G--G-A-GA--AG---G--AG---G----G--AC----C--C---C--C---------------
> str13: -T---CTCA-C-AG-T---T--CA--A-G---A---A-C---C------CA--A-A-GTAC-----C-C---C------C----CAT-A---GC---C---C-T-C--T--TA-A-----A-G--C--C-A--C----------
> str14: A-G-G-T----T---T--ATA-C--C-T-TC---CTAG---G--TA-A-CA--A-AC---CA--A-C-CAA-CT--T-TCGAT-C-T--CT----TG-TA--------------------------------------------
> str15: A-G-G-T----T---T--ATA-C--C-T-TC---C---C-AG-GTA-A-CA--A-AC---CA--A-C-CAA-CT--T-TCGAT-C-T--CT----TG-TA--------------------------------------------
> str16: -T-A----A---A-A-C-A-A-C-TCA-----AT--A-C-A----A---CAT-A-A-G-A-A--A----A---T-----C-A---A---C--GCA----A--A---A-----ACA---CT-C-A-CA---A---A---------
> str17: -----C-C-GC-----C-----CAT--T-T-G-----G---GCG--G--C-T--C---T-C-G-AGC----G---ATA--G---C-T--C--G--T-C--G-A---A-T-C--C----CT-CGA-C--CT--------------
> str18: AT-A-C-C---T---TC-----C--CA-G--G-T--A---A-C--A-A--A---C-C--A-A----C-CAA-CT--T-TCGAT-C-T--CT----TG-TAG-AT-C--TG----------------------------------
> str19: -T---CTCA-C-AG-T---T--CA--A-G---A---A-C---C-T----CA--A---GT-C--T--C-C---C------C----CAT-A---G---GC---C-T-C--T--T----T-C-A-G-TCAG----------------
> str20: --GA--TC---T----C--T--C-TCA---C---C--G--A----A---C----C---T---G--GC-C---C------CG--G---G-C-A--A----A---TGC-C--CTA-A-T-C--C-A---G--AG-----GT--G--
> str21: A-GAGC--A---A--TC-A--G--T---G-C-ATC-AG--A----A-AT-AT-AC-C-TA---T---T-A---T-A---C-A--C-T---T----TGCTA--A-G-A-----A---T---------------------------
> str22: A--A--T----TA-A---A-A-CATC-T--C-A---A--TA-C--A-A-CAT-A-A-G-A-A--A----AA-C--A-A-CG---CA--A--A--A----A-CA--C--T-C-A---T---------------------------
> str23: A--A----A-C--GA---A---C-T--T-T--A---A---A----A--TC-TG-----T---GT-G-----GCTG-T--C-A--C-T--C--G---GCT-GCATGC--T--TA--GTGC-------------------------
> str24: AT-A----A-CTA-AT---TA-C-T---GTCG-T-T-G--A-C--AG-----GACACG-A--GTA----A--CT-----CG-T-C-T-A-T--C-T--T--C-TG---------------------------------------
> str25: ATGAG-T--G-T----C-A---C-----G---A---A--T----T----CA---C--GTACA--A--T---G---A-A-C--TG---GA-T-G--T--T--CA--C---G-T---G-G--A--AT-A---A-------------
> str26: A----C-C-G-T-G---G---GC-----G---A----GC--G-GT-GA-C----C--G----GT-G-TC----T--T--C----C-T-A---G--TG---G---G---T-C--C----C-ACG-T----T-G--AA----R---
> str27: A--A----AG---G-T---T----T-AT----A-C---CT----T----C----C-C--A--G--G-T-AA-C--A-A---A--C----C-A--A--C---CA---ACT--T----T-C---GATC---T---C----T---TG
> str28: A-G---T-AG-T---TCG----C--C-TGT-G-T---G--AGC-T-GA-CA--A-AC-T----TAG-T-A-G-TG-T-T---TG--TGA---G---G--A---T----T---A-------------------------------
> str29: -T----T----TA--T--A---C--C-T-TC---CTAG---G--TA-A-CA--A-AC---CA--A-C-CAA-CT--T-TCGAT-C-T--CT----TG-TAG-AT----------------------------------------
> str30: ATG--C---G---G-TCG-T--C-TC-T--C---C---C---CG--G--C-T------T----T---T-----T--T-TC----C----C---C--GC--GC---C---GC----GT--T--G----GC--G-C--CG-A----
> str31: --G---T--G--A---C-A-A--A--A-----A-C-A--TA----A--T---G----G-AC--T--C-CAA-C--A---C----CATG--T--CA----AGC-T----T--T-CAG-G-TA-GA-C------------------
> str32: --G---T--G-TA-A--GA-A--A-CA-GT--A---AGC---C------C--G----G-A-AGT-G-----G-TG-T-T---T---TG-C--G-AT--T----T-C---G--A--G-GC--CG----G----------------
> str33: --GAG---A---A--T-GA--G--TC-T--C-AT-TA-C---CG-----C----C-CG----GTA-CT-----T-A----G---CA--A---GC-T---A--AT--A--G-T-CA---C---G----GC---------------
> str34: ATG---T--G---G-TCGAT-GC--CATG--GA----G---GC------C----CAC---CAGT---TCA---T--TA---A-G---G-CT--C---CT-G---GCA-T--T--------------------------------
> str35: A----C---G--AG--CG-T----T--T-T--A---AG---G-G-----C----C-CG--C-G-A-CT---GC-GA---CG--GC----C-A-CATG---GC---C-CTG-TA---TG-T------------------------
> str36: --G-G-T----T---T--ATA-C--C-T-TC---C---C-AG-GTA-A-CA--A-AC---CA--A-C-CAA-CT--T-TCGAT-C-T--CT----TG-TAG-------------------------------------------
> str37: -TG-G----G--A-A--G-T----TC----C-A---A---A----AGATCA---CA---A-A--A-C--A--CT-A---C----CA-G--T--CA----A-C---C--TG--A-AGT---AC-A-C------------------
> str38: --GA----AGC--G-T---TA--A-C--GT-G-T-T-G--AG-G-A-A--A--A---G-ACAG---CT-----T-A----G--G-A-GA--A-CA----AG-A-GC--TG-----G-G--------------------------
> str39: A----C-CAGC--G--C-A---C-T--T--CG-----GC-AGCG--G--CA-G-CAC---C--T--C----G--G----C-A-GCA---C---C-T-C-AGCA-GCA-----AC------------------------------
> str40: ATG-G----G--A---C-A-A-C-T--T----AT-T--C---C-TA--TCATG-----T---G---C-CAAG---A----G--G--T---T----T--TA-C---C-C-G-----GTG--AC---CA-----------------
> str41: -T----T--G-TAGATC--T-G--T--T--C--TCTA---A----A---C--GA-AC-T----T---T-AA----A-ATC--TG--TG--T-G---G-T----TG---T-C-AC--T-C-------------------------
> str42: A--A-C-CA---A---C-----CA--A---C--T-T---T--CG-A--TC-T--C---T----T-G-T-A-G---AT--C--TG--T---T--C-T-CTA--A---AC-G--A-A---CT----T----TA-------------
> str43: --G-G----G-T---TC--T-GC--CA-G--G--C-A--TAG--T----C-T------T----T---T-----T--T-TC--TG---G-C--G---GC---C---C--T--T---GTG-TA--A--A-C----C----T--G--
> str44: --G-GCT--GC-A--T-G----C-T--T----A----G-T-GC--A---C-T--CACG--CAGTA--T-AA--T--TA---AT--A--ACTA--AT--TA-C-TG---T-----------------------------------
> str45: -TG--C--A--T-G--C--T----T-A-GT-G--C-A-CT--C--A---C--G-CA-GTA---TA----A---T--TA---AT--A--ACTA--AT--TA-C-TG---T-C----GT---------------------------
> str46: -T----TC--C-A---C-A-A-C-T--T-TC---C-A-C---C--A-A----G-C---T-C--T-GC--AAG---AT--C----C----C-AG-A-G-T--CA-G----G-----G-GC--C--T--G-T--------------
> str47: -T---CT-A---A-A-CGA-A-C-T--T-T--A---A---A----A--TC-TG-----T---GT-G-----GCTG-T--C-A--C-T--C--G---GCT-GCATGC--T--TA--G----------------------------
> str48: A----C-C-G---GAT-G---GC--C--G-CGAT-T---T----T---TC--G----G-A--GT--C-C----T--T---G--G---G----G---G--A-C---CACT-C-A--G----A--AT-AG--A-------------
> str49: -----CT----T-G-T--A--G-ATC-TGT---TCT--CTA----A-A-C--GA-AC-T----T---T-AA----A-ATC--TG--TG--T-G---GCT-G--T-CACT-----------------------------------
> str50: ATGAGC--A-CTA-A--G----C-----G---A---AG--A----A---C----CA---A-A--A----A-GC--A----GA--CA--A-TA-CA----A-C---C-C-GCTA---T--TAC----------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 144
> best bound: 0.0
> wall time: 0.065113s
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
> --- Solution (of length 142) ---
>   Sol: ATGAGCTCAGTCAGTCATGACATGCTATCGATGCTAGCAGTGACTACGATCAGCTAGTACTGCATAGCCAACTAGTCAGTCGATCGTGCATGACTAGCTAGATCTGACTAGCTGACTAGCTAGTCACATGCAGACCTGRATG
> str01: -T-AG-T-AGT-AG--A---C-T-C---CG--G--A--AGTGAC-A--A--A-C-----C--C-T-G--AA--A---AG---A------ATG----G--A--T---A--A----A-TA--TA--------------------
> str02: --G-G---A-T-A---A--ACA--CT--C----C---C-G--A--A--A--A--TA--A-T---T-------T-G--A--C--T--T--A--A--A-C-A-A-C-G-C--G---AC-AG-T--TCA-A-G------------
> str03: AT-A-C-C--T---TC----C-T---A--G--G-TA--A----C-A--A--A-C-----C---A-A-CCAACT--T---T---T-G---AT--CT--CT---T--G--TAG---A-T--CT-G-------------------
> str04: -T-A----A---A-T--T-A--T---A---AT-CT-----T-A-TAC--T-AG-TA--A----A-A---AA-TAG---G--G-T-GT--A--AC---C--GA----A--A----AC--G---GTC-----------------
> str05: -T----T-A---A---A--ACA-GC---C--TG-T-G--G-G--T----T--GC-A---C--C----C-A-CT---CA--C-A--G-G---G-C---C-----C--ACT-G--G----GC--G-CA-A-G------------
> str06: ATGA-CT---TC---CA--A--TG-----GAT-C---C-----C-A--A-C--CT----C---A-AGC----T--TC---C-A-C---C----C---C-A-AT--G----G-T---T---T---CA---GC-----------
> str07: A--A-C--A---A---A---C---C-A---A--C---CA---ACT----T----T--T---G-AT--C----T---C--T---T-GT--A-GA-T--CT-G-T-T--CT--CT-A--A---A--C----G-A-AC-------
> str08: ATGA----A---A---A---C--G--A---A----A--A-T---TA---T----TA-T-C---A-AG-------G---GT--AT-G-G-A--A---G-T-G----GA--AGCTGAC--G--A---A-AT-------------
> str09: A----CTC-G---G-C-TG-CATGCT-T--A-G-T-GCA----CT-C-A-C-GC-AGTA-T--A-A------T--T-A----AT-----A--ACTA---A--T-T-A-----------------------------------
> str10: -T----T--GT-AG--AT--C-TG-T-TC--T-CTA--A---AC---GA--A-CT--T--T--A-A---AA-T---C--T-G-T-GTG---G-CT-G-T----C--ACT--C------------------------------
> str11: --G--C--AG--AG-CAT----T--T-TC--T---A--A-T-A-T-C---CA-C-A--A----A-A------T-G--A----A--G-GCA--A-TA---A--T-TG--TA-CT-ACT--C----------------------
> str12: ATGAGC-CA---AG--AT--C---C----GA--C--G-A---A----GA---GC-----C--C----C-AA---G---G---A--G-G-A-GA--AG---GA---G----G--GAC---C----C-C---C-----------
> str13: -T---CTCA--CAGT--T--CA----A--GA----A-C-----C--C-A--A---AGTAC--C----CC--C----CA-T--A--G--C----C---CT----CT---TA----A--AGC----CAC---------------
> str14: A-G-G-T---T---T-AT-AC---CT-TC----CTAG--GT-A--AC-A--A---A---C--CA-A-CCAACT--T---TCGATC-T-C-T---T-G-TA------------------------------------------
> str15: A-G-G-T---T---T-AT-AC---CT-TC----C---CAG-G--TA--A-CA---A--AC--CA-A-CCAACT--T---TCGATC-T-C-T---T-G-TA------------------------------------------
> str16: -T-A----A---A---A---CA----A-C--T-C-A--A-T-AC-A--A-CA--TA--A--G-A-A---AA-T---CA----A-CG--CA--A--A---A-A-C--ACT--C--AC-A---A---A----------------
> str17: -----C-C-G-C---C----CAT--T-T-G--G---GC-G-G-CT-C--TC-G--AG--C-G-ATAGC----T---C-GTCGA------AT--C---C-----CT--C--G---AC---CT---------------------
> str18: AT-A-C-C--T---TC----C---C-A--G--G-TA--A----C-A--A--A-C-----C---A-A-CCAACT--T---TCGATC-T-C-T---T-G-TAGATCTG------------------------------------
> str19: -T---CTCA--CAGT--T--CA----A--GA----A-C-----CT-C-A--AG-T----CT-C----CC--C----CA-T--A--G-GC----CT--CT---T-T--C-AG-T--C-AG-----------------------
> str20: --GA--TC--TC--TC-T--CA--C---CGA----A-C-----CT--G----GC-----C--C----C------G---G--G--C----A--A--A--T-G--C---C---CT-A--A--T---C-CA-G-AG----G--TG
> str21: A-GAGC--A---A-TCA-G---TGC-ATC-A-G--A--A---A-TA---T-A-C-----CT--AT-------TA-T-A--C-A-C-T---T---T-GCTA-A---GA--A--T-----------------------------
> str22: A--A--T---T-A---A--A-A--C-ATC--T-C-A--A-T-AC-A--A-CA--TA--A--G-A-A---AA--A--CA----A-CG--CA--A--A---A-A-C--ACT--C--A-T-------------------------
> str23: A--A----A--C-G--A--AC-T--T-T--A----A--A---A-T-C--T--G-T-GT---G----GC----T-GTCA--C--TCG-GC-TG-C-A--T-G--CT---TAG-TG-C--------------------------
> str24: AT-A----A--C--T-A--A--T--TA-C--TG-T--C-GT---T--GA-CAG---G-AC---A---C------G--AGT--A------A---CT--C--G-TCT-A-T--CT---T--CT-G-------------------
> str25: ATGAG-T--GTCA--C--GA-AT--T--C-A--C--G---T-AC-A--AT--G--A--ACTG----G--A--T-GT---TC-A-CGTG---GA--A--TA-A----------------------------------------
> str26: A----C-C-GT--G----G----GC----GA-GC--G--GTGAC--CG----G-T-GT-CT---T--CC---TAGT--G--G---GT-C----C---C-A---C-G--T---TGA--A--------------------R---
> str27: A--A----AG---GT--T----T---AT--A--C---C--T---T-C---C--C-AG----G--TA---A-C-A---A----A-C---CA--AC---C-A-A-CT---T---T--C--G--A-TC---T-C-----T---TG
> str28: A-G---T-AGT---TC--G-C---CT---G-TG-T-G-AG---CT--GA-CA---A--ACT---TAG-----TAGT--GT---T--TG--TGA---G---GAT-T-A-----------------------------------
> str29: -T----T---T-A-T-A---C---CT-TC----CTAG--GT-A--AC-A--A---A---C--CA-A-CCAACT--T---TCGATC-T-C-T---T-G-TAGAT---------------------------------------
> str30: ATG--C---G---GTC--G---T-CT--C--T-C---C-----C--CG----GCT--T--T---T-------T--T---TC---C---C----C--GC--G--C---C--GC-G--T---T-G------GC-G-CC-G-A--
> str31: --G---T--G--A--CA--A-A----A---A--C-A----T-A--A---T--G---G-ACT-C----C-AAC-A--C---C-AT-GT-CA--A---GCT---T-T--C-AG--G--TAG--A--C-----------------
> str32: --G---T--GT-A---A-GA-A----A-C-A-G-TA--AG---C--C---C-G---G-A----A--G-----T-G---GT-G-T--T---T---T-GC--GAT-T---T--C-GA---G---G-C-C--G--G---------
> str33: --GAG---A---A-T---GA---G-T--C--T-C-A----T---TAC---C-GC-----C--C---G-------GT-A--C--T--T--A-G-C-A---AG--CT-A--A--T-A---G-T---CAC--G--G-C-------
> str34: ATG---T--G---GTC--GA--TGC---C-ATG---G-AG-G-C--C---CA-C-----C---A--G-----T--TCA-T---T-----A--A---G---G--CT--C---CTG----GC-A-T----T-------------
> str35: A----C---G--AG-C--G---T--T-T---T---A--AG-G-----G--C--C-----C-GC---G--A-CT-G-C-G---A-CG-GC----C-A-C-A--T--G----GC---C---CT-GT-A--TG------T-----
> str36: --G-G-T---T---T-AT-AC---CT-TC----C---CAG-G--TA--A-CA---A--AC--CA-A-CCAACT--T---TCGATC-T-C-T---T-G-TAG-----------------------------------------
> str37: -TG-G----G--A---A-G---T--T--C----C-A--A---A--A-GATCA-C-A--A----A-A-C-A-CTA--C---C-A--GT-CA--AC---CT-GA----A---G-T-AC-A-C----------------------
> str38: --GA----AG-C-GT--T-A-A--C----G-TG-T-----TGA----G----G--A--A----A-AG--A-C-AG-C--T---T-----A-G----G--AGA----AC-A----A---G--AG-C---TG--G----G----
> str39: A----C-CAG-C-G-CA---C-T--T--CG--GC-AGC-G-G-C-A-G--CA-C-----CT-C---G-------G-CAG-C-A-C---C-T--C-AGC-AG--C--A--A-C------------------------------
> str40: ATG-G----G--A--CA--AC-T--TAT---T-C---C--T-A-T-C-AT--G-T-G--C--CA-AG--A----G---GT---T--T---T-AC---C-----C-G----G-TGAC---C-A--------------------
> str41: -T----T--GT-AG--AT--C-TG-T-TC--T-CTA--A---AC---GA--A-CT--T--T--A-A---AA-T---C--T-G-T-GTG---G--T---T-G-TC--ACT--C------------------------------
> str42: A--A-C-CA---A--C----CA----A-C--T--T-----T--C---GATC---T----CT---T-G-----TAG--A-TC--T-GT---T--CT--CTA-A----AC--G---A--A-CT--T----T--A----------
> str43: --G-G----GT---TC-TG-C---C-A--G--GC-A----T-A----G-TC---T--T--T---T-------T--T---TC--T-G-GC--G----GC-----C---CT---TG--T-G-TA---A-A--C---C-TG----
> str44: --G-GCT--G-CA-T---G-C-T--TA--G-TGC-A-C--T--C-ACG--CAG-TA-TA----AT-------TA---A-T--A------A---CTA---A--T-T-ACT-G-T-----------------------------
> str45: -TG--C--A-T--G-C-T----T---A--G-TGC-A-C--T--C-ACG--CAG-TA-TA----AT-------TA---A-T--A------A---CTA---A--T-T-ACT-G-T--C--G-T---------------------
> str46: -T----TC---CA--CA--AC-T--T-TC----C-A-C-----C-A--A---GCT----CTGCA-AG--A--T---C---C---C----A-GA---G-T----C--A---G--G----G---G-C-C-TG------T-----
> str47: -T---CT-A---A---A---C--G--A---A--CT-----T---TA--A--A---A-T-CTG--T-G-----T-G---G-C--T-GT-CA---CT--C--G----G-CT-GC--A-T-GCT--T-A---G------------
> str48: A----C-C-G---G--ATG----GC---CG---C--G-A-T---T----T----T--T-C-G----G--A----GTC---C--T--TG---G----G---G----GAC---C--ACT--C-AG--A-AT--AGA--------
> str49: -----CT---T--GT-A-GA--T-CT---G-T--T--C--T--CTA--A--A-C--G-A----A---C----T--T---T--A------A--A--A--T----CTG--T-G-TG----GCT-GTCAC-T-------------
> str50: ATGAGC--A--C--T-A--A---GC----GA----AG-A---AC--C-A--A---A--A----A--GC-A----G--A--C-A------AT-AC-A---A---C---C---C-G-CTA--T--T-AC---------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 142
> best bound: 0.0
> wall time: 3.330604s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="protein_n010k010.txt")
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
> --- Solution (of length 51) ---
>   Sol: MEQSKAFPLSVEYACHPGFLRVNTAEQHFRDAIKGGRALHDNPSRNGTVYQ
> str01: M----A--LS--Y-C-P----------------KG------------T---
> str02: M-QS-----S---------L--N-A-------I---------P-----V--
> str03: M------PLS--Y-------------QHFR---K-----------------
> str04: ME---------E---H-----VN--E------------LHD----------
> str05: M--S------------------N-----F-DAI---RAL------------
> str06: M-----F-------------R-N---Q--------------N-SRNG----
> str07: M-----F-----YA-H--------A---F-----GG-------------Y-
> str08: M--SK-F----------------T-----R------R-----P------YQ
> str09: M--S--F---V--A---G---V-TA-Q------------------------
> str10: ME-S----L-V-----PGF---N--E-------------------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 51
> best bound: 0.0
> wall time: 0.035008s
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
> --- Solution (of length 50) ---
>   Sol: MESKFALVPLSYAGQEHVFTRNAEQNSSRLNFCPKGDAGIYHDPQRALTV
> str01: M----AL---SY--------------------CPKG------------T-
> str02: M-------------Q-----------SS-LN------A-I---P-----V
> str03: M-------PLSY--Q-H-F-R-------------K---------------
> str04: ME-------------EHV---N-E-----L-----------HD-------
> str05: M-S------------------N---------F----DA-I-----RAL--
> str06: M---F---------------RN--QNS-R-N----G--------------
> str07: M---F------YA---H-----A--------F---G--G-Y---------
> str08: M-SKF--------------TR-------R----P------Y---Q-----
> str09: M-S-F--V----AG---V-T--A-Q-------------------------
> str10: MES---LVP----G----F--N-E--------------------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 50
> best bound: 0.0
> wall time: 0.841934s
> ```

In [ ]:
```python
scsp.util.bench(scsp.model.la_sh.Model, example_filename="protein_n050k050.txt")
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
> --- Solution (of length 497) ---
>   Sol: MAFVEFSLVLLPGFLNRVEKSSQCTHVNIDPQLAFSLIPRTVLQGVRDSETQVKLPYAIVNRGSLFKPTQAGIDERLMPSYTNVELSFHATERDGNKMQTVLWAPSICEDANYKTEFVNLYGPDIKSVFEATRQGHLSNQSKVDLIAHSGIPYEFNTIKLQRNSGVYPDCTILENGKSAVFRAHEQLSWDYALSTPRGEFVLDHAMSTYVESQLYFPADKSVRFEGTNIRGSSVAHILKDGTEYNPHRVALEGIKSNADLEVKTFARYCDNSGLEQHITSAMDFERGPWVLKAICNSFDRPGTAFIYQDLEGVAESGMTNEKLQHRAGPNVDKSILPGQYDTFRVEHCLDIRNPDSMWKIVLTGDRSEYNQADCHLFIRAGVWDTYEPQSTRNVIEADSTKAGKEGILQRPDEANLHSVFQCKDAEFRTDDCHGIAECKLHIMAKKLSSAGRKHRVLHSTWYMNFMICFISVKVGNKLYMWVTVYYGVPVWKEAKTT
> str01: M---------------R--------H------L---------------------------N-----------ID--------------------------------I-E-----T-----Y-----S----------SN----D-I------------K---N-GVY---------K-------------YA----------D-A-----E-------D----FE---I--------L------------L-------------FA-Y---S-----I----D---G--------------G--------E-V-E--------------------------------CLD-----------LT--R-----------------------------------------------------------------------------------------------------------------------------------
> str02: M---E-----------R----------------------R-----------------A------------------------------H---R------T-----------------------------------H---Q---------------N--------------------------------WD-A--T------------------------K-------------------------P-R---E--------------R------------------R-----K---------------Q----------T----QHR---------L-----T----H------PD---------D-S----------I-------Y-P---R--IE----KA--EG---R------------K--E---D--HG---------------------------------------------------------------
> str03: M---E------PG--------------------AFS----T----------------A------LF-------D---------------A-----------L-----C-D-------------DI-----------L----------H-------------R-------------------R----L-----------E-------S-----QL--------RF-G----G--V-----------------------------------------Q-I---------P------------P---------E-V--S---------------D----P------RV-----------------------Y--A--------G----Y----------A----------L-------L---------------------------------------------------------------------------------
> str04: M-----------G------K--------------F---------------------Y-----------------------Y-----S--------N------------------------------------R----------------------------R----------L-----AVF-A--Q-----A--------------------Q-------S-R------------H-L--G-----------G--S-----------Y------EQ------------W-L-A-C-----------------V--SG--------------D-S-------------------------------------A----F-RA------E------V------KA-------R--------V-Q-KD-------------------------------------------------------------------------
> str05: --F--F----------R-E--------N----LAF--------Q-------Q----------G---K---A----R--------E--F----------------PS--E------E--------------A-R-------------A--------N-------S---P--T------S---R--E-L-W-----------V---------------------R------RG---------G---NP----L----S----E----A------G-------A---ER-------------R-GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str06: M----------------------------DP----SL---T--Q-V--------------------------------------------------------WA-------------V-----------E----G--S----V-L---S-----------------------------A---A-----------------V-D----T---------A------E-TN-----------D-TE--P------------D-E-----------GL-----SA---E----------N--------------EG--E---T------R--------I---------------IR-------I--TG--S----------------------------------------------------------------------------------------------------------------------------------
> str07: MAF--------------------------D----FS-----V--------T-----------G-------------------N-------T-----K----L-------D----T-----------S-------G-------------------F-T---Q---GV-----------S---------S-----------------M-T-V-------A----------------A-----GT--------L--I---ADL-VKT-A-----S-------S---------------------------Q-L--------TN--L---A-----------Q----------------S---------------------------------------------------------------------------------------------------------------------------------------------
> str08: MA-V------------------------I---L-----P---------S-T-----Y-----------T----D--------------------G----T---A------A----------------------------------------------------------CT---NG-S-----------------P------D------V-----------V---GT---G----------T---------------------------------------M------WV-----N------T--I---L------------------P--------G--D-F---------------------------------F-----W-T--P-S------------G-E------------SV--------R---------------------------V-----------------------------------------
> str09: M--------------N--------T-------------------G-------------I-------------ID--L----------F-----D-N---------------------------------------H------VD----S-IP----TI-L-------P---------------H-QL----A--T------LD-----Y----L-------VR---T-I-------I--D--E-N--R-------S-----V-----------L----------------L------F--------------------------H---------I---------------------M------G--S-------------G--------------------------------------------------------------------------------------------------------------------
> str10: M-FV-F-LVLLP--L--V--SSQC--VN----L------RT-----R---TQ--LP-----------P--A---------YTN---SF--T-R-G-----V-----------Y-------Y-PD-K-VF---R----S--S-V-L--HS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M----------------------------D-----S-----------------K--------------------E------T------------------------I------------L----I----E---------------I----IP------K------------I----KS------------Y-L--------LD----T-------------------NI--S-------------P--------KS-----------Y--N-----------DF---------I--S--R-------------------N-K-------N----I-------F-V-----I-N--------L------YN-----------V-------ST---I------------------------------------------------------------------------------------------------------
> str12: M------L-L----------S-----------------------G--------K------------K-----------------------------KM---L-----------------L---D--------------N-------------YE--T---------------------A---A--------A----RG------------------------R--G----G--------D--E----R------------------R------------------RG-W---A----FDRP--A-I------V-----T--K---R-----DKS------D--R------------M--------------A--H--------------------------------------------------------------------------------------------------------------------------
> str13: M--------------N----------------------------G----E------------------------E------------------D---------------D-N---E-----------------Q------------A-------------------------------A---A-EQ--------------------------Q-------------T-----------K---------------K--A----K---R-------E----------------K--------P--------------------K-Q--A----------------R--------------K-V-T---SE---A----------W---E-----------------------------H--F---DA---TDD--G-AECK-H--------------------------------------------------------
> str14: M---E-SLV--PGF-N--EK----THV----QL--SL-P--VLQ-VRD----V-L----V-RG--F-----G-D-----S---VE------E--------VL---S--E-A---------------------RQ-HL----K-D-----G------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M---------------R---------------------------------------Y-IV---S---P-Q------L------V-L------------Q-V--------------------G---K--------G----Q-------------E-----------V-------E-------RA---L---Y-L-TP------------Y---------D------------------------Y---------I----D-E-K--------S---------------P-----I------------Y--------------------------------Y--F-----L--R---S------------------HL----------------N-I-------------QRP--------------------------------------------------------------------------------------
> str16: M----------P----RV------------P----------V--------------Y----------------D-----S------------------------P----------------------------Q--------V-----S--P---NT--------V-P-----------------Q-----A----R----L--A--T--------P---S--F----------A------T---P-----------------TF-R-----G-------A-D---------A-------P--AF--QD---------T-------A--N--------Q-------------------------------QA------R---------Q------------------------------------------------------------------------------------------------------------
> str17: M-FV-F-LVLLP--L--V--SSQC--VN----L------RT-----R---TQ--LP--------L-----A---------YTN---SF--T-R-G-----V-----------Y-------Y-PD-K-VF---R----S--S-V-L--HS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FV-F-------F---V--------------L---L-P---L--V--S--------------S-----Q-------------------------------------C---------VNL-----------T------------------------T----R--------T--------------QL--------P--------------------PA-------------------------Y-------------------T------NS-----------F------------------T----------------------R-G--V--------Y----------------------------Y------------------P---------D--K-----------------VF-------R-------------------SS------VLHS--------------------------------------
> str19: M---E----------------------------A---I--------------------I----S-F----AGI---------------------G-----------I----NYK-----------K----------L--QSK--L---------------Q----------------------H-----D---------F-------------------------G---R---V---LK----------AL------------T-------------------------V------------TA---------------------RA--------LPGQ--------------P----K---------------H--I-A--------------I--------------R----------Q----------------------------------------------------------------------------
> str20: MA----S-------------S-----------------------G----------P------------------ER-------------A-E-------------------------------------------H---Q-----I----I--------L-------P-----E---S-----H--LS-----S-P-----L-------V---------K---------------H--K-----------L--------L-------Y--------------------------------------Y--------------------------------------------------WK--LTG-----------L-----------P-------------------L--PDE--------C-D--F--D--H------L-I-------------------------------------------------------
> str21: M---E-SLV--PGF-N--EK----THV----QL--SL-P--VLQ-VRD----V-L----V-RG--F-----G-D-----S---VE------E--------VL---S--E--------V--------------RQ-HL----K-D-----G------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L-------------------------A----P---------S------P----N--S--K-----I-------------------------Q--L--------------F-N-------------------N------I---------N-I----------D--I--N---------------Y-------E----H---T-----LYF-A--SV---------S--A----------------------------------------Q-------------------NSF------F--------A---------Q---------------------------------W--V--------------------V---Y---S------AD--KA----I------------------------------------------------------------------------------------------
> str23: M-----S--------------------------A---I--T--------ET--K-P------------T---I-E-L-P----------A-----------L-A----E------------G------F----Q---------------------------R----Y-------N-K-----------------TP-G-F-------T------------------------------------------------------------C--------------------VL-------DR------Y-D---------------H--G--V---I-----------------N-DS--KIVL------YN-------------------------------------------------------------------------------------------------------------------------------
> str24: M------------------K-------NI----A---------------E---------------FK-----------------------------K------AP---E----------L----------A----------------------E----KL------------LE-----VF------S---------------------------------------N---------LK-G---N----------S----------R----S-L--------D----P-----------------------------M-------RAG----K-------------H--D----------V--------------------V-----------VIE--STK--K---L-----------------------------------------------------------------------------------------
> str25: M----------P----------Q-------P-L--------------------K---------------Q---------S-----L-------D----Q------S-------K--------------------------------------------------------------------------W---L---R-E-----A-----E--------K---------------H-L---------R-ALE---S---L-V-------D-S-----------------------N-------------LE---E-----EKL---------K---P-Q---------L------SM------G---E----D--------V------QS-----------------------------------------------------------------------------------------------------------
> str26: M-FV-F-LVLLP--L--V--SSQC--VN----L----I--T-----R---TQ-----------S----------------YTN---SF--T-R-G-----V-----------Y-------Y-PD-K-VF---R----S--S-V-L--HS-------T---Q-------D----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M------------------K--------------F------------D----V-L--------SLF----A-------P-----------------------WA---------K---V-----D-----E---Q-------------------E------------Y-D----------------Q--------------------------QL-------------N----------------N-----------N--LE----------S-----IT-A------P---K-----FD---------D--G-A----T-E-------------I----------E---------S-----------E----------R-G--D----------I------------------------------------------------------------------------------------------------------
> str28: M-FV-F-LVLLP--L--V--SSQC--VN------F-----T-------------------NR------TQ------L-PS---------A----------------------Y-T---N-------S-F--TR-G-------V---------Y-------------YPD-------K--VFR-----S-----S------VL-H--S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-----------------------------------------------------------------------------------------------------W--SI-----------------I--V--------L----K--LI--S-I---------Q------P----L-------------L-----L-------V------T---S-L--P--------------------L-----YNP----------N------------------------MD-------------S--------------------------------------------------C-------------------------C-L-I-----------S-R--I----T----------P-E--L--------A--------G----KL-------------------TW-----I-FI---------------------------
> str30: M---E-SLV--PGF-N--EK----THV----QL--SL-P--VLQ-VRD----V-L----V-RG--F-----G-D-----S---VE------E------------------------F--L------S--EA-RQ-HL----K-D-----G------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FV-F-LVLLP--L--V--SSQC--V--------------------------------------------------MP------L-F-------N-----L----I-------T----------------T------------------------T---Q--S--Y---T---N-----F-------------T-RG--V-------Y-----Y-P-DK-V-F-----R-SSV---L--------H---L------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M------------------------H-----Q-----I--TV---V--S-------------G----PT-----E--------V--S---T----------------C--------F----G----S---------L----------H---P--F-----Q--S--------L---K------------------P----V----M-----------A---------N------A--L--G-------V-LEG-K--------------------------M-F----------C-S--------I-----G----G--------R-------S-L-----------------------------------------------------------------------------------------------------------------------------------------------------------------
> str33: MA----------------------T-------L---L--R--------S-----L--A------LFK--------R------N-------------K------------D---K--------P----------------------------P-----I------------T------S-------------------G--------S------------------G----G---A-I----------R----GIK---------------------HI---------------I-----------I------V---------------P-----I-PG--D--------------S----------S----------I------T-----TR------S----------R---------------------------------------------------------------------------------------
> str34: M---E-SLV--PGF-N--EK----THV----QL--SL-P--VLQ-VRD----V-L----V-RG--F-----G-D-----S-----------------M----------E------E-V-L------S--EA-RQ-HL----K-D-----G------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FV-F-LVLLP--L--V--SSQC--VN----L-------T---------T-----------G-----TQ------L-P-------------------------P-----A-Y-T---N-------S-F--TR-G-------V---------Y-------------YPD-------K--VFR-----S-----S------VL-H--S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA-------------N------------I--------I----------------------N---L-------------------------------------W--------N---------G--I--V-----------------------P-----------------------------------------------------M---V--Q-----D--V-----N-----VA--------------------S---------------------IT-A--F-------K----S--------------------M----------------I-----D----E----------------T-------------------WD----------------K--K--I-----EAN-------------T--C--I------------S---RKHR--------N---------------------------------
> str37: M------L-------NR-----------I--Q--------T-L----------------------------------M------------------K--T---A-------N------N-Y--------E-T-------------I-------E---I-L-RN---Y-----L--------R----L---Y-------------------------------------I-------IL-----------A----------------R---N---E---------E-G------------R-G---I---L------------------------I----YD--------D--N------I----D-S--------------V-------------------------------------------------------------------------------------------------------------------
> str38: MA---------------------------DP--A----------G-----T---------N-G-----------E---------E---------G----T---------------------G-----------------------------------------------C----NG------------W----------F--------YVE------A---V-----------V--------E-----------K-------KT--------G---------D---------AI--S-D---------D-E--------NE--------N-D-S------DT---------------------G---E----D--L-----V-D-----------------------------------------------------------------------------------------------------------------
> str39: M-FV-F-LVLLP--L--V--SSQC--VN----L------RT-----R---TQ--LP-----------P-----------SYTN---SF--T-R-G-----V-----------Y-------Y-PD-K-VF---R----S--S-V-L--HS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M---E-SLV--PGF-N--EK----THV----QL--SL-P--VLQ-V-------------------------------------------------------------C-D-------V-L-------V----R-G-------------------F---------G---D--------S-V----E-------------E-VL----S---E------A----R----------------------------------------------------QH-------------LK------D--GT--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M--------------N-----------N---Q-------R-------------K------------K-T-A----R--PS-------F-------N-M---L-----------K------------------R-------------A--------------RN------------------R------------------V-----ST-V-SQL---A-K--RF-------S------K-G---------L--------L-----------SG--Q----------GP-----------------------------M---KL-------V-------------------------M--------------A----F------------------------------------------------------------------------------------------------------------------------
> str42: M-----S--------N------------------F------------D---------AI--R--------A-----L------V---------D-----T---------DA-YK-----L-G-------------H---------I-H---------------------------------------------------------M--Y-------P-------EGT---------------EY----V-L----SN-------F-------------T---D--RG---------S--R-----I----EGV-----T-----H----------------T--V-H------------------------------------------------------------------------------------------------------------------------------------------------------
> str43: M---------------------------I--------------------E----L------R--------------------------H--E--------V--------------------------------QG--------DL--------------------V----TI--N----V--------------------V---------E---------------T------------------P-----E------DL---------D--G----------F-R------------D-----FI-------------------RA-------------------H-L-I----------------------C-L---A-V-DT-E---T--------T--G----L---D----------------------I--------------------------Y-----------------------------------
> str44: M-FV-F-LVLLP--L--V--SSQC--V--------------------------------------------------MP------L-F-------N-----L----I-------T----------------T------NQS-----------Y---T-----NS----------------F-------------T-RG--V-------Y-----Y-P-DK-V-F-----R-SSV---L--------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-----S------------K---------D--L--------V---------------A---R-------QA-----LM---T-------A--R----M---------------K----------------A------------D----------F----------V--------------F------------------F-L-------------F-----V---------------L--------------------------------------------------W--KA----------------L-----S------L-----P-V-----P----T-R---C----------------------Q------I-----D----------------------------------------------------------MAKKLS-AG----------------------------------------------
> str46: MA----SL-L---------KS-----------L-------T-L----------------------FK--------R-----T----------RD----Q-----P-----------------P-------------L---------A-SG-------------SG----------G--A-------------------------------------------------IRG-----I-K-------H-V----I-----------------------I-----------VL--I------PG------D------S-----------------SI---------V-----------------T--RS-----------R----------------------------------------------------------------------------------------------------------------------
> str47: M---------------RV---------------------R----G-------------I-----L----------R------N-------------------W------------------------------Q-----Q------------------------------------------------W---------------------------------------------------------------------------------------------------W----I---------------------------------------------------------------W----T---S--------L----G--------------------------------------F----------------------------------------W-M-FMIC--SV-VGN-L--WVTVYYGVPVWKEAKTT
> str48: MA-VE------P-F----------------P--------R------R--------P--I---------T------R--P---------HA---------------SI-E--------V-----D-------T-----S-----------GI-------------G----------G-SA------------------G--------S----S------------E-------------K---------V---------------F---C----L---I--------G--------------------Q-----AE-G----------G-----------------E-------P---------------N--------------T--------V-------------------------------------------------------------------------------------------------------
> str49: M-F-----------------------------------------------------YA------------------------------HA--------------------------F----G------------G-----------------Y---------------D----EN-----------L----------------HA----------FP--------G--I--SS--------T------VA------N-D--V----R------------------------K--------------Y--------S--------------V-------------V----------S----V-------YN------------------------------K--K---------------------------------------------------------Y-N--I----VK--NK-YMW----------------
> str50: MA-------------N----------------------------------------Y------S--KP-------------------F-------------L-----------------L---DI--VF---------N--K-D-I------------K----------C-I--N--------------D---S--------------------------------------------------------------------------C--S----H--S--D-----------C----R------YQ-------S---N-------------S-----Y----VE--L--R-------------R---NQA---L----------------N-------K-------------NL---------------------------------------------------------------------------------
> 
> example file name: 'protein_n050k050.txt'
> best objective: 497
> best bound: 0.0
> wall time: 8.517355s
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
> --- Solution (of length 471) ---
>   Sol: MAFVFESLVLLPLVSGKFNSQCRVENLKRAITHVQDLPSLRTPVLFQSVYKERTDAGINVLSTPQVRGFKAMPLGIDTSVQEALFCDYTNRPSGHEFVNLIWTQSEARGVYYPDKTVFRNQSISVGLEAYHVSDTINVLKDGSFPMTRGVEAQLANYKDEISYGTPDKVFERANLIQSPHAESQVRDYITLHASGRCNSFKTPRLGGVYDQYIESLKTAHWPNDKVFRTISLPEKSMQVLYARGSPIDEGTNKPRHVLSAEKYWVDFISNLARPKGCVQWLADNTSFEIHLRKSGIVEQTALDRPMFGAKYSNIFLPDERAGQSHLGVITCDNRLIWEVTGSKHMFDAVPYNRDKSTLEGDKHIVCESALTYNISQDTEFRSGMVWKALDIENSTKYPVEQLKASMGRCEPSKVLRHNDTVWIQEKAFESDPTGNLRKEDWLCVQHINTVYYGDMAVPVWKEAKTNLSAGT
> str01: M---------------------R---------H---L---------------------N----------------ID-----------------------I----E---------T-------------Y--S---------S------------N--D-I------K-----N--------------------G------------VY-------K-----------------------YA-----D-----------AE----DF--------------------EI-L----------L----F-A-YS-I---D---G----G----------EV-------------------E------C---L------D-----------L-----T------------R---------------------------------------------------------------
> str02: M----E----------------R-----RA--H-------RT----------------------------------------------------H--------Q---------------N----------------------------------------------------------------------------------------------------W--D-----------------A--------T-KPR-----E-----------R------------------RK-----QT----------------------Q-H--------RL----T---H-----P---D------D------S-----I----------------------YP---------R--------------I-EKA-E----G--RKED-----H------G------------------
> str03: M----E-----P---G-------------A---------------F-S-----T-A----L-------F-------D-----AL-CD--------------------------D--------I---L---H----------------R-----------------------R--L------ESQ------L----R---F-----GGV--Q-I--------P----------PE----V-----S--D-----PR-V-----Y--------A---G----------------------------------Y---------A----L--------L----------------------------------------------------------------------------------------------------------------------------------------
> str04: M--------------GKF-------------------------------Y-------------------------------------Y----S-----N--------R----------R-------L-A--V-----------F-------AQ-A---------------------QS-------R-----H------------LGG-------S-------------------------Y-------E-----------------------------QWLA------------------------------------------------C-------V--S-----------------GD------SA----------FR------A---E------V---KA---R-----V---------Q-K----D----------------------------------------
> str05: --F-F-----------------R-ENL--A---------------FQ-----------------Q--G-KA-------------------R----EF---------------P--------S-----E----------------------EA-------------------RAN---SP----------T---S-R-----------------E-L----W----V-R--------------RG-----G-N-P---LS-E----------A---G-----A-----E---R-----------R---G---------------------T---------------------------------------------------------------------------------------------------------------------------------------------
> str06: M----------------------------------D-PSL-T----Q-V----------------------------------------------------W----A--V-----------------E-------------GS------V---L-------S----------A-------A---V-D--T--A--------------------E---T----ND----T----E-----------P-DEG-------LSAE--------N-----------------E------G--E-T---R---------I--------------I----R-I---TGS---------------------------------------------------------------------------------------------------------------------------------
> str07: MAF--------------------------------D---------F-SV----T--G-N---T------K---L--DTS--------------G--F-----TQ----GV-----------S-S---------------------MT--V-A--A--------GT---------LI----A-----D---L----------------V--------KTA-----------S----S-Q-L----------TN-----L-A------------------Q------S-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: MA-V--------------------------I-----LPS--T-------Y---TD-G-----T-------A-----------A--C--TN---G----------S-------PD--V-------VG--------T------G----T-----------------------------------------------------------------------------------------M--------------------------WV----N--------------T---I-L-------------P--G---------D---------------------------F---------------------------------F-----W--------T--P------S-G--E-S-V-R----V--------------------------------------------------
> str09: M-----------------N------------T------------------------GI-----------------ID------LF-D--N----H--V---------------D-------SI---------------------P-T-------------I-------------L---PH---Q------L-A--------T--L----D-Y---L---------V-RTI----------------IDE--N--R---S-----V-----L---------L-----F--H-----I---------M-G---S---------G-----------------------------------------------------------------------------------------------------------------------------------------------------
> str10: M-FVF--LVLLPLVS----SQC-V-NL-R--T--------RT----Q-------------L--P--------P---------A----YTN--S---F-----T----RGVYYPDK-VFR--S-SV-L---H-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M----------------------------------D--S-----------KE-T---I--L--------------I-----E------------------I---------------------I---------------------P------------K--I------K---------S---------Y--L-------------L----D-------T----N------IS-P-KS----Y----------N-------------DFIS---R----------N--------K-------------------NIF------------VI---N-L---------------YN------------V--S--T--I-------------------------------------------------------------------------------------------------
> str12: M------L-L----SGK----------K----------------------K--------------------M-L---------L--D--N--------------------Y----------------E------T----------------A--A-----------------A------------R--------GR---------GG--D---E-------------R--------------R-----------R--------------------G---W-A----F---------------DRP---A----I-------------V-T------------K---------RDKS----D-------------------R--M---A----------------------------H------------------------------------------------------
> str13: M-----------------N-------------------------------------G------------------------E-------------E-----------------D-------------------D--N-------------E-Q-A-----------------A-------AE-Q--------------------------Q------T------K---------K------A----------K-R-----EK-----------PK---Q--A---------RK---V--T-----------S------E-A---------------WE-----H-FDA--------T---D---------------D-----G----A---E----------------C---K---H------------------------------------------------------
> str14: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D----VL----VRGF-----G-D-SV-E-------------E-V-L----SEAR------------Q---------H-------LKDG----T------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M---------------------R--------------------------Y-------I-V-S-PQ--------L-----V---L-------------------Q-----V---------------G-------------K-G----------Q------E--------V-ERA-L------------Y--L----------TP-----YD-YI----------D---------EKS---------PI---------------Y-----------------------------------------------Y---FL---R---SHL------N--I---------------------------------------Q----R----------------P-------------------------------------------------------------------------
> str16: M----------P----------RV-------------P-----V-----Y----D------S-PQV------------S------------P------N---T------V--P-------Q-------A------------------R-----LA---------TP-----------S---------------------F------------------A---------T---P-----------------T---------------F-----R--G-----AD-----------------A---P---A-----F-------Q--------D-------T-------A---N-----------------------Q------------------------Q--A---R---------------Q-----------------------------------------------
> str17: M-FVF--LVLLPLVS----SQC-V-NL-R--T--------RT----Q-------------L--P---------L--------A----YTN--S---F-----T----RGVYYPDK-VFR--S-SV-L---H-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FVF------------F-----V--L---------LP-L---V---S-------------S--Q--------------------C-----------VNL--T------------T--R---------------T-----------------QL-----------P------------P-A------Y-T-------NSF-T-R-G-VY--Y---------P-DKVFR--S----S--VL---------------H--S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str19: M----E-----------------------AI--------------------------I---S------F-A---GI-----------------G------I------------------N---------Y---------K-----------------K----------------L-QS----------------------K---L-----Q--------H---D--F----------------G----------R-VL---K---------A--------L---T-----------V--TA--R----A------LP----GQ--------------------------P----K-------HI----A----I------R-------------------Q----------------------------------------------------------------------
> str20: MA----S-------SG---------------------P-------------ER--A-------------------------E------------H--------Q------------------I------------I--L-----P-----E----------S-----------------H----------L--S----S---P-L--V--------K--H----K------L-------LY---------------------YW----------K-----L---T---------G------L--P----------LPDE-----------CD-------------FD---------------H------L---I-------------------------------------------------------------------------------------------------
> str21: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D----VL----VRGF-----G-D-SV-E-------------E-V-L----SE---V--------R-Q---------H-------LKDG----T------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L---------------------A-------PS---P---------------N--S-------K-----I----Q--LF----N--------N-I------------------N--I----------D-IN-------------------Y--E-------------------H---------TL-----------------Y-----------------F--------------A--S-----------V-SA------------------Q----N-SF-------------------F-A-------------Q-------------W-V---------V-Y----S------------A-------D---------KA--I--------------------------------------------------------------------------------
> str23: M-----S----------------------AIT-------------------E-T---------------K--P----T----------------------I----E--------------------L-----------------P------A-LA----E---G-----F------Q--------R-Y---------N--KTP--G--------------------F-T-----------------------------------------------CV--L-D--------R------------------Y------D------H-GVI---N-------------D--------S-----K-IV----L-YN--------------------------------------------------------------------------------------------------
> str24: M---------------K-N-----------I------------------------A-------------------------E--F-----------------------------K------------------------K-----------A-------------P----E---L-----AE------------------K---L----------L-----------------E----V---------------------------F-SNL---KG-------N-S-----R-S-------LD-PM-------------RAG--------------------KH--D-V---------------V-------------------V-----IE-STK------K-----------L--------------------------------------------------------
> str25: M----------P--------Q----------------P-L----------K-------------Q-------------S----L--D----------------QS---------K---------------------------------------------------------------------------------------------------------W----------L----------R-----E----------AEK---------------------------HLR--------AL----------------E----S-L-V---D---------S---------N-----LE-------E-----------E-------K-L------K-P--QL--SMG--E--------D-V--Q-----S-----------------------------------------
> str26: M-FVF--LVLLPLVS----SQC-V-NL---IT--------RT----QS-Y---T----N--S------F--------T------------R--G---V------------YYPDK-VFR--S-SV-L---H-S-T-----------------Q-----D------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M---------------KF-----------------D-------VL--S------------L-------F-A-P----------------------------W----A-------K-V----------------D----------------E-Q------E--Y---D---------Q------Q------L------N------------------------N----------------------------N-----L--E-------S-------------------I----------TA---P----K----F--D-------------D--------G------A--------T-E----I--ES----------E-R-G------DI--------------------------------------------------------------------------------
> str28: M-FVF--LVLLPLVS----SQC-V-N-------------------F-------T----N-------R----------T--Q--L-------PS-------------A---Y----T---N-S---------------------F--TRGV------Y-----Y--PDKVF-R-----S----S-V-----LH-S-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M----------------------------------------------------------------------------------------------------W--S-----------------I------------I-VLK-------------L------IS-------------IQ-P-----------L-------------L----------L---------V--T-SLP------LY----------N-P---------------N-----------------------------------M-----------D-----S------C----------------------------------C---L---IS-----R---------I---T--P-E-L-A--G-----K-L----T-WI----F------------------I------------------------
> str30: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D----VL----VRGF-----G-D-SV-E-------------EF--L----SEAR------------Q---------H-------LKDG----T------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FVF--LVLLPLVS----SQC-V-----------------------------------------------MPL----------F----N---------LI-T------------T------------------T-----------------Q--------SY-T--------N-------------------------F-T-R-G-VY--Y---------P-DKVFR--S----S--VL---------------H-L---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M-------------------------------H-Q----------------------I----T--V-------------V------------SG------------------P--T-----------E---VS-T-------------------------------------------------------------C--F-----G--------SL---H-P----F----------Q------S------------L---K-----------P---V---------------------------M--A---N-------A----LGV------L--E--G-K-MF-------------------C-S-----I--------G-----------------------GR---S--L--------------------------------------------------------
> str33: MA-----------------------------T----L--LR------S------------L---------A--L----------F-----------------------------K---RN-------------------KD----------------K-------P------------P---------IT---SG---S------GG-----------A----------I------------RG--I-----K--H-----------I--------------------I------IV-------P--------I--P----G---------D---------S-------------S-------I------T------T--RS-------------------------R---------------------------------------------------------------
> str34: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D----VL----VRGF-----G-D-S------------------------------------------------------------------M----E--------E--------V-----L--S---E----------A--R--------------Q--------H-----------L--K------------D-GT----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FVF--LVLLPLVS----SQC-V-NL----T---------T--------------G-----T-Q--------L-----------------P--------------------P---------------AY----T-N-----SF--TRGV------Y-----Y--PDKVF-R-----S----S-V-----LH-S-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA----------------N-----------I--------------------------IN-L----------------------------------------W-----------------N-----G---------I-V------PM---V--Q-----D---------V----N----------V-------AS------------------I----TA-------F-------KSM---------IDE-T------------W-D--------K-----------------K--I-E--A-----------N----------------TC----I-----S----------R-K-------H-----------------R-----------N------------------------------------------------------------------------------
> str37: M------L----------N---R-------I---Q------T--L--------------------------M------------------------------------------KT------------A-------N------------------NY--E----T----------I-----E------I-L----R-N----------Y------L-----------R---L--------Y-----I--------------------I--LAR----------N---E---------E---------G-----------R-G------I-----LI--------------Y--D------D-----------NI--D----S--V--------------------------------------------------------------------------------------
> str38: MA---------------------------------D-P-----------------AG-----T--------------------------N---G-E---------E--G------T---------G----------------------------------------------------------------------CN-------G--------------W-----F-------------Y---------------V---E----------A-----V------------------VE-----------K--------------------------------K-------------T--GD-------A----IS-D------------D-EN------E-----------------ND----------SD-TG----ED-L-V---------D-----------------
> str39: M-FVF--LVLLPLVS----SQC-V-NL-R--T--------RT----Q-------------L--P--------P-----S--------YTN--S---F-----T----RGVYYPDK-VFR--S-SV-L---H-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V------------------------------------CD----------V-L---------V--------R------G-----------------F----G---------D--S------V-E----------E--V-----L--S-------------------E----A--------R---------Q-----------------H-L---K---D---------G--------T------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M-----------------N------N--------Q-----R---------K------------------K-------T----A-------RPS---F-N----------------------------------------------M-------L---K-------------RA------------R-----------N-----R---V------S--T-------V----S------Q-L-A----------K-R-----------F-S-----KG----L---------L--SG---Q--------G--------P---------------------------M---------K--L------V------------------M---A---------------------------------------F-------------------------------------------
> str42: M-----S-----------N--------------------------F--------DA-I--------R---A--L-----V------D-T------------------------D--------------AY---------K-------------L---------G---------------H--------I--H--------------------------------------------M---Y----P--EGT---------E-Y-V-----L--------------S--------------------------N-F--------------T-D-R------GS----------R----------I--E---------------G-V---------T---------------------H--TV------------------------H-------------------------
> str43: M-----------------------------I--------------------E--------L-----R---------------------------HE-V-----Q----G----D------------L----V--TINV-----------VE-------------TP----E---------------D---L------------------D---------------------------------G----------------------F-----R---------D---F-I--R--------A-----------------------HL--I-C---L------------AV----D--T-E-----------T------T----G-----LDI-----Y--------------------------------------------------------------------------
> str44: M-FVF--LVLLPLVS----SQC-V-----------------------------------------------MPL----------F----N---------LI-T------------T---NQS-------Y----T-N-----SF--TRGV------Y-----Y--PDKVF-R-----S----S-V-----LH---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-----S---------K------------------DL------V-----------A----------R-------------Q-AL-------------------------------------------------------------MT----A-------------------R----------------------------------------------------------------M---------------K------A-----DF----------V--------F-------------------F--------L-----------------------------F--V--------L---------------------------WKAL----S-------L--------P--V-----------------PT---R-----C-Q-I------DMA----K--K--LSAG-
> str46: MA----SL-L------K--S------L----T----L--------F----K-RT------------R---------D---Q----------P--------------------P-------------L-A---S--------GS-----G--------------G--------A--I---------R--------G-----------------I---K--H-----V---I----------------I---------VL---------I-----P-G------D--S-------S-IV--T---R-------S-------R-------------------------------------------------------------------------------------------------------------------------------------------------------
> str47: M---------------------RV----R---------------------------GI--L-----R----------------------N-----------W-Q----------------Q---------------------------------------------------------------------------------------------------W------------------------------------------W---I-----------W----TS----L---G-----------F-----------------------------W-------MF-------------------------------------M------I-----------------C--S-V------V------------GNL----W--V----TVYYG---VPVWKEAKT-----T
> str48: MA-V-E-----P-----F-------------------P--R-----------R----------P-----------I-T------------RP--H-----------A--------------SI----E---V-DT-------S-----G-----------I--G------------------------------G---S-------------------A------------------------GS-------------S-EK--V-F---------C---L-------I-----G---Q-A-----------------E--G----G----------E-----------P-N----T-------V----------------------------------------------------------------------------------------------------------
> str49: M-F----------------------------------------------Y-----A--------------------------------------H-----------A----------F-------G---------------G--------------Y-DE-------------NL----HA------------------F--P--G------I-S---------------S-------------------T-----V--A---------N------------D-------------V------R-----KYS---------------V----------V--S------V-YN--K------K---------YNI----------V-K-----N--KY--------M---------------W-------------------------------------------------
> str50: MA----------------N------------------------------Y-----------S-------K--P-----------F--------------L--------------------------L------D-I-V-----F-----------N-KD-I------K----------------------------C---------------I---------ND------S---------------------------------------------C--------S---H---S--------D---------------------------C--R----------------Y------------------------Q-----S----------NS--Y-VE-L-----R-------R-N-----Q--A--------L-----------N------------K----NL----
> 
> example file name: 'protein_n050k050.txt'
> best objective: 471
> best bound: 0.0
> wall time: 48.373516s
> ```

DIDP を使うと時間が長くなる.
小さな問題であれば直接プログラミングした方がよい.

## 先読みの手数を増やせないか

In [ ]:
```python
@dataclass
class Model2:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, m: int = 5, ll: int = 1, *args, **kwargs) -> str | None:
        model = Model(self.instance)
        self.solution = model.solve(m=m, ll=ll)
        self.best_bound = model.best_bound
        return self.solution
```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="uniform_q26n004k015-025.txt")
```

> ```
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 66) ---
>  Sol: tkulcignyceojsovkaiuqfhozmpxplgnbhtqgxzxcvsrddbcuqxspvrvningsfsbxf
> str1: tk----gn--------k--u--h--mpx---n-htqgxz--v--------x------i--s-----
> str2: -----i-----oj-----i-qf-o-----l-nb----x-xcvs-----uq--pv---i--s-sbxf
> str3: --ulci-nyc-o-sov-------oz-p-pl----------------------p-------------
> str4: -----ig---e----v-a------z-----g-b----------rddbc---s-vrvn-ng-f----
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 66
> best bound: 0.0
> wall time: 0.647244s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="uniform_q26n008k015-025.txt")
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
>  Sol: igpbdevyplrazxulgnbrdcvdpozfjimtwxqkvgxnerzbyctdforsokuihmvlcdnsbtroqvzixgpxndhtmpnlrpcqgxzvxisuqpvissbbhefwdxf
> str1: -------------------------------t---k-g-n-------------ku-hm----------------pxn-ht-------qgxzvxis----------------
> str2: i------------------------o--ji----q-------------fo---------l--n-b-------x--x----------c----v--suqpvissb------xf
> str3: --------------ul-----c-------i---------n----yc---o-so-----v--------o--z---p------p-l-p-------------------------
> str4: ig---ev----az---g-brd--d-------------------b-c-----s------v-------r--v------n-----n-----g-----------------f----
> str5: --p----yplr-zxu------c--p-----m---q-vg--------tdf-----ui--v-cd-sb--o-------------------------------------------
> str6: --pbdev-------------dcvdp--f--------------z--------s-----m-----sb-roqv--------------------------------bbh------
> str7: -----e-----------nb--c----zfj--t----v-x-erzb------r-------v------------i-gp--------l---------------------e-----
> str8: ----------r--x------------------wxqk-----r-----d--r--------lc----t-o---------d-tmp--rp---x-----------------wd--
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 111
> best bound: 0.0
> wall time: 2.469393s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="uniform_q26n016k015-025.txt")
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
>   Sol: krixwushltxxkqjgenfpvabczfdojigqbxkuhetvnryddbcosvrmizdpfoalxevkrnctodgzhtqbgxeuzxcvspmuqprvpxiwangthszkcedjwsbfrdohmgqzuklikvpcdskrblbgexfhjnowwy
> str01: ---------t--k--g-n----------------kuh--------------m---p----x----n------htq-gx--z--v---------xi------s--------------------------------------------
> str02: --i------------------------oji-q------------------------fo-l-----n---------b-x---xcvs--uqp-v--i------s-------sb--------------------------xf-------
> str03: -----u--l--------------c-----i----------n-y---cos--------o----v-----o--z-------------p---p--------------------------------l---p-------------------
> str04: --i------------ge---va--z-----g-b--------r-ddbc-svr-----------v--n-------------------------------ng------------f----------------------------------
> str05: -------------------p----------------------y------------p---l----r------z-----x-u--c--pm-q--v------gt------d----f--------u--i-v-cds--b---------o---
> str06: -------------------p--b---d----------e-v---d--c--v----dpf--------------z------------s-m--------------s--------b-r-o---q------v------b-b----h------
> str07: ----------------en----bczf--j---------tv--------------------xe--r------z---b--------------rv--i---g---------------------------p------l--e---------
> str08: -r-xw-----x--q--------------------k------r-d------r--------l------ctod---t------------m--pr-px-w----------d---------------------------------------
> str09: k-----------kq-------a---f---igq---------------------------------------------------------------------------jw-----o------k--k----skrbl-g----------
> str10: --------l-xx-------p-ab------i---------v-----b---v---z---------k----o--z--------z--v----------------------d---------------------------------------
> str11: kri---------------f-----------------------------s---------a---v--nc--d----q--------------------w----h-z-c-----------------------------------------
> str12: -------------q-------a-----------x-u-------d--------------------------g---q--------v----q---------------ce--w-bf-----g-----i----------------j-owwy
> str13: -r----s---x--qj--nfp-a----d--i-----u------------s---i---------------------qb--e-z-------------------h--k----------ohmg----------------------------
> str14: --i-w-sh------------v---------------h---------co---mi--------------------------u---v----------------------d------d--m-----------------------------
> str15: -------h-txx-qj---------z------qb-------------c--------------------t-------b--------------------a------k-------------------------------------n----
> str16: ---x-us-----------f----c-f---------------------------z-p-----e----------------e---cv-----------wan-t-----------f----mgqzu-------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 146
> best bound: 0.0
> wall time: 13.113512s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="uniform_q05n010k010-010.txt")
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
>   Sol: bdbacbeacdebeedcbaedabccdeebdd
> str01: -d--cb--c------c---d-bcc-e----
> str02: bd-------d-bee----e------e-bd-
> str03: ----c--acde-e--c--e--b---e----
> str04: ---a--e--d----d----d----de-bdd
> str05: ---acbe---e----c-a---bc--e----
> str06: b-ba-be----b--dcba------------
> str07: b-ba--ea--eb-----a-da---------
> str08: ------e---e-ee-cb--d-b---ee---
> str09: ----c---cde-e-d--a-d--c-d-----
> str10: bd-a-b---d-be----a--a---d-----
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 30
> best bound: 0.0
> wall time: 0.224325s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="uniform_q05n050k010-010.txt")
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
> --- Solution (of length 38) ---
>   Sol: dacebcdaebdacdebcaebdacebadbecacadbebd
> str01: d-c-bc------cd-bc-----ce--------------
> str02: ----b-d---d----b--e----e----e------ebd
> str03: --c----a----cde---e---ceb---e---------
> str04: -a-e--d---d--d------d--eb-d------d----
> str05: -ac-b---e-----e-ca-b--ce--------------
> str06: ----b----b-a---b--ebd-c-ba------------
> str07: ----b----b-a--e--aeb-a----d---a-------
> str08: ---e----e-----e---e---c-b-dbe------e--
> str09: --c--cd-e-----e-----da----d--c---d----
> str10: ----b-da-bd----b--e--a---ad-----------
> str11: ---e--d-e-da-----a---a-e-a----a-------
> str12: -a-----ae--a-----a-b---e----e-ac------
> str13: ---e---a---a---bca----c------c---db---
> str14: ----b-d-e-----e--a--d--e-ad-e---------
> str15: --c----ae-da-de---e----e--d-----------
> str16: ---ebc-a--d----b-a-b----b---e---------
> str17: d-----d-----c-e---e--a--b-d-e-a-------
> str18: da--bcd---d---e--ae---c---------------
> str19: -a-----a--d-c-e---e-da---a-b----------
> str20: -a-e----e---c---c-e----e----e-a-a-----
> str21: ----b----bda--e-ca---a----d-e---------
> str22: dace--dae-da---b----------------------
> str23: -a-----ae--a---b---b----b--b-c-----e--
> str24: d--e--d--b--c--bca---a--b-------------
> str25: d---b-da---a--eb---b--c-b-------------
> str26: d--eb---e-d----b--eb-ac---------------
> str27: --ce----eb--cd--c--bd--e--------------
> str28: d---b---e-da-----a--da---a-b----------
> str29: --c--c------cd--c--b---eb-d--c--------
> str30: -a-e----e--acd-bc--bd-----------------
> str31: dac-b---e--ac---c-----c---d-----------
> str32: ---e-c--eb--c---c---d---b-db----------
> str33: d-----d--b-----bc-e-da--b--b----------
> str34: -a-----ae--a---b-a---a-eba------------
> str35: ---e-c---b-----bca---a----d--c---d----
> str36: d--ebc------c-e-c---d---b----c--------
> str37: da-----a----c--b-ae----eb----c--------
> str38: -a----da-b----e--a---ac------c-----e--
> str39: da-e-cd--b-ac----a---a----------------
> str40: dac-b----bd-c-e-----d-c---------------
> str41: d--e--d--b----e---eb----b-d-e---------
> str42: --c---da--d-cd--c---da---a------------
> str43: --ce----e-d-c--b-ae----e--d-----------
> str44: --ce---ae---c----a---a---a---ca-------
> str45: d-c--c------c-eb---b----bad-----------
> str46: ----b--ae-----e--aeb----b-d-e---------
> str47: d---b-d-eb-ac---c---d---b-------------
> str48: ---ebc---b----e---e-da-e-a------------
> str49: -a-e----e-----eb---bd---b----ca-------
> str50: d---b-da-b--c-e-c--b----b-------------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 38
> best bound: 0.0
> wall time: 1.500066s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="nucleotide_n010k010.txt")
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
> --- Solution (of length 26) ---
>   Sol: TCATACGGCTAGATACTGTAAATCCT
> str01: --AT--GG---GATAC-G--------
> str02: --ATAC--CT---T-C-------CC-
> str03: -CA--CG---A-AT--TG-A------
> str04: T-A-A-----A-AT-CTGT-------
> str05: --A---GG-TA-A--C---AAA----
> str06: T--T-C--CTAG-----GTA------
> str07: T--T--G--TAGAT-CT---------
> str08: T-----GG---GA-A--GT---TC--
> str09: T--T-C--C-A----C---AA--C-T
> str10: TC-TA-----A-A--C-G-AA-----
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 26
> best bound: 0.0
> wall time: 0.142456s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="nucleotide_n050k050.txt")
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
> --- Solution (of length 145) ---
>   Sol: ATGATCGTACGATACGTCATAGCTATCATGCATGACTACGATCAGTCAAGCTACGTAGCTGAACTACGCATGACTGCATAGCTACTGATCTAGCATGCTAGCTGACTGATCAGTCATCGATCAGCGTACGTCGAARCGAACTAGA
> str01: -T-A--GTA-G-TA-G--A---CT--C---C--G-----GA--AGT---G--AC--A----AAC--C-C-TGA----A-A---A--GA---A---TG---G---A-T-A--A---AT--AT-A----------------------
> str02: --G---G-A---TA----A-A-C-A-C-T-C----C--CGA--A---AA--TA---A--T----T-----TGACT---TA---A---A-C-A--A--C--GC-GAC--A---GT--TC-A--AG---------------------
> str03: AT-A-C---C--T---TC----CTA----G---G--TA--A-CA---AA-C--C--A----A-C--C--A--ACT---T---T--TGATCT--C-T--T-G-T-A--GATC--T----G--------------------------
> str04: -T-A----A--AT---T-ATA---ATC-T---T-A-TAC--T-AGT-AA---A---A----AA-TA-G---G---G--T-G-TA---A-C---C--G--A----A---A--A--C---G----G--T-C----------------
> str05: -T--T---A--A-A----A---C-A----GC----CT--G-T--G----G----GT---TG--C-AC-C----C---A---CT-C--A-C-AG---G---GC---C----CA--C-T-G----G-G--CG-C-AA--G-------
> str06: ATGA-C-T----T-C--CA-A--T-----G---GA-T-C---C---CAA-C--C-T--C--AA----GC-T---T-C----C-AC----C---C---C-A----A-TG----GT--T---TCAGC--------------------
> str07: A--A-C--A--A-AC--CA-A-C---CA---A---CT----T---T-----T--G-A--T---CT-C---T---TG--TAG--A-T---CT-G--T--T--CT--CT-A--A---A-CGA--A-C--------------------
> str08: ATGA----A--A-ACG--A-A---A--AT---T-A-T----T-A-TCAAG----G--G-T-A--T--G---GA----A--G-T---G-----G-A----AGCTGAC-GA--A---AT----------------------------
> str09: A----C-T-CG----G-C-T-GC-AT---GC-T---TA-G-T--G-CA--CT-C--A-C-G--C-A-G--T-A-T--A-A--T--T-A---A---T---A----ACT-A--A-T--T--A-------------------------
> str10: -T--T-GTA-GAT-C-T----G-T-TC-T-C-T-A--A--A-C-G--AA-CT---T---T-AA--A---AT--CTG--T-G-T---G-----GC-TG-T--C--ACT---C----------------------------------
> str11: --G--C--A-GA---G-CAT---T-T--T-C-T-A--A---T-A-TC---C-AC--A----AA--A----TGA----A--G-----G--C-A--AT---A----A-T--T--GT-A-C--T-A-C-T-C----------------
> str12: ATGA--G--C----C---A-AG--ATC---C--GAC---GA--AG--A-GC--C----C----C-A---A-G---G-A--G-----GA----G-A----AG--GA--G----G-----GA-C--C---C--C----C--------
> str13: -T---C-T-C-A--C---A--G-T-TCA---A-GA--AC---C---CAA---A-GTA-C----C--C-C----C--CATAGC--C----CT--C-T--TA----A---A---G-C--C-A-C-----------------------
> str14: A-G---GT----T---T-ATA-C---C-T---T--C--C--T-AG----G-TA---A-C--AA--AC-CA--AC--CA-A-CT--T--TC--G-AT-CT--CT---TG-T-A---------------------------------
> str15: A-G---GT----T---T-ATA-C---C-T---T--C--C---CAG----G-TA---A-C--AA--AC-CA--AC--CA-A-CT--T--TC--G-AT-CT--CT---TG-T-A---------------------------------
> str16: -T-A----A--A-AC---A-A-CT--CA---AT-AC-A--A-CA-T-AAG--A---A----AA-T-C--A--AC-GCA-A---A---A---A-CA--CT--C--AC--A--A---A-----------------------------
> str17: -----C---CG---C--C----C-AT--T---TG-----G----G-C--G----G---CT---CT-CG-A-G-C-G-ATAGCT-C-G-TC--G-A----A--T--C----C---C-TCGA-C--C-T------------------
> str18: AT-A-C---C--T---TC----C---CA-G---G--TA--A-CA---AA-C--C--A----A-C--C--A--ACT---T---T-C-GATCT--C-T--T-G-T-A--GATC--T----G--------------------------
> str19: -T---C-T-C-A--C---A--G-T-TCA---A-GA--AC---C--TCAAG-T-C-T--C----C--C-C----C---ATAG-----G--C---C-T-CT---T---T---CAGTCA--G--------------------------
> str20: --GATC-T-C--T-C-TCA---C---C--G-A--AC--C--T--G----GC--C----C----C---G---G---GCA-A---A-TG--C---C---CTA----A-T---C---CA--GA---G-GT--G---------------
> str21: A-GA--G--C-A-A--TCA--G-T-----GCAT--C-A-GA--A---A---TA--TA-C----CTA----T---T--ATA-C-ACT--T-T-GC-T---A----A--GA--A-T-------------------------------
> str22: A--AT--TA--A-A----A---C-ATC-T-CA--A-TAC-A--A--CA---TA---AG---AA--A---A--AC---A-A-C----G--C-A--A----A----A---A-CA--C-TC-AT------------------------
> str23: A--A----ACGA-AC-T--T---TA--A---A--A-T-C--T--GT---G-T--G--GCTG---T-C--A---CT-C---G-----G--CT-GCATGCT---T-A--G-T--G-C------------------------------
> str24: AT-A----AC--TA----AT---TA-C-TG--T--C---G-T---T---G--AC--AG--GA-C-ACG-A-G--T--A-A-CT-C-G-TCTA---T-CT---T--CTG-------------------------------------
> str25: ATGA--GT--G-T-C---A---C------G-A--A-T----TCA--C--G-TAC--A----A--T--G-A--ACTG----G--A-TG-T-T--CA--C--G-TG---GA--A-T-A---A-------------------------
> str26: A----C---CG-T--G-----G-------GC--GA----G--C-G----G-T--G-A-C----C---G---G--TG--T--CT--T---C---C-T---AG-TG---G----GTC--C---CA-CGT---T-GAAR---------
> str27: A--A----A-G----GT--T---TAT-A--C----CT----TC---C---C-A-G--G-T-AAC-A---A--AC--CA-A-C--C--A---A-C-T--T---T--C-GATC--TC-T---T--G---------------------
> str28: A-G-T---A-G-T---TC---GC---C-TG--TG--T--GA---G-C----T--G-A-C--AA--AC---T---T--A--G-TA--G-T---G--T--T---TG--TGA---G-----GAT-----TA-----------------
> str29: -T--T--TA---TAC--C-T---T--C---C-T-A----G----GT-AA-C-A---A----A-C--C--A--AC--CA-A-CT--T--TC--G-AT-CT--CT---TG-T-AG--AT----------------------------
> str30: ATG--CG---G-T-CGTC-T--CT--C---C----C--CG----G-C----T---T---T----T-----T---T---T--C--C----C---C--GC--GC---C-G--C-GT--T-G----GCG--C--CGA-----------
> str31: --G-T-G-AC-A-A----A-A---A-CAT--A--A-T--G----G--A--CT-C----C--AAC-AC-CATG--T-CA-AGCT--T--TC-AG---G-TAG---AC---------------------------------------
> str32: --G-T-GTA--A---G--A-A---A-CA-G--T-A--A-G--C---C---C---G--G---AA----G--TG---G--T-G-T--T--T-T-GC--G--A--T---T--TC-G--A--G----GC---CG--G------------
> str33: --GA--G-A--AT--G--A--G-T--C-T-CAT---TAC---C-G-C---C--CG--G-T-A-CT-----T-A--GCA-AGCTA---AT--AG--T-C-A-C-G---G--C----------------------------------
> str34: ATG-T-G---G-T-CG--AT-GC---CATG---GA----G----G-C---C--C--A-C----C-A-G--T---T-CAT---TA---A----G---GCT--C---CTG----G-CAT---T------------------------
> str35: A----CG-A-G---CGT--T---T-T-A---A-G-----G----G-C---C--CG---C-GA-CT--GC--GAC-G----GC--C--A-C-A---TG---GC---C----C--T----G-T-A---T--GT--------------
> str36: --G---GT----T---T-ATA-C---C-T---T--C--C---CAG----G-TA---A-C--AA--AC-CA--AC--CA-A-CT--T--TC--G-AT-CT--CT---TG-T-AG--------------------------------
> str37: -TG---G---GA-A-GT--T--C---CA---A--A--A-GATCA--CAA---A---A-C--A-CTAC-CA-G--T-CA-A-C--CTGA---AG--T---A-C--AC---------------------------------------
> str38: --GA----A-G---CGT--TA---A-C--G--TG--T----T--G--A-G----G-A----AA--A-G-A---C---A--GCT--T-A----G---G--AG---A---A-CA---A--GA---GC-T--G--G----G-------
> str39: A----C---C-A---G-C---GC-A-C-T---T--C---G----G-CA-GC---G--GC--A-----GCA---C--C-T--C----G-----GCA-GC-A-C---CT---CAG-CA--G--CA----AC----------------
> str40: ATG---G---GA--C---A-A-CT-T-AT---T--C--C--T-A-TCA---T--GT-GC----C-A---A-GA--G----G-T--T--T-TA-C---C---C-G---G-T--G--A-C---CA----------------------
> str41: -T--T-GTA-GAT-C-T----G-T-TC-T-C-T-A--A--A-C-G--AA-CT---T---T-AA--A---AT--CTG--T-G-T---G-----G--T--T-G-T--C--A-C--TC------------------------------
> str42: A--A-C---C-A-AC--CA-A-CT-T--T-C--GA-T-C--TC--T-----T--GTAG---A--T-C---TG--T---T--CT-CT-A---A--A--C--G---A---A-C--T--T---T-A----------------------
> str43: --G---G---G-T---TC-T-GC---CA-G---G-C-A---T-AGTC----T---T---T----T-----T---T---T--CT---G-----GC--G---GC---C----C--T--T-G-T--G--TA-----AA-C---CT-G-
> str44: --G---G--C--T--G-CAT-GCT-T-A-G--TG-C-AC--TCA--C--GC-A-GTA--T-AA-T-----T-A----ATA---ACT-A---A---T--TA-CTG--T--------------------------------------
> str45: -TG--C--A---T--G-C-T---TA----G--TG-C-AC--TCA--C--GC-A-GTA--T-AA-T-----T-A----ATA---ACT-A---A---T--TA-CTG--T---C-GT-------------------------------
> str46: -T--TC---C-A--C---A-A-CT-T--T-C----C-AC---CA---A-GCT-C-T-GC--AA----G-AT--C--C----C-A--GA----G--T-C-AG--G---G----G-C--C--T--G--T------------------
> str47: -T---C-TA--A-ACG--A-A-CT-T--T--A--A--A--ATC--T---G-T--GT-G--G--CT--G--T--C---A---CT-C-G-----GC-TGC-A--TG-CT--T-AG--------------------------------
> str48: A----C---CG----G--AT-G-------GC----C---G--C-G--A---T---T---T----T-----T--C-G----G--A--G-TC---C-T--T-G--G---G----G-----GA-C--C--AC-TC-A---GAA-TAGA
> str49: -----C-T----T--GT-A--G--ATC-TG--T---T-C--TC--T-AA---ACG-A----A-CT-----T---T--A-A---A---ATCT-G--TG-T-G--G-CTG-TCA--C-T----------------------------
> str50: ATGA--G--C-A--C-T-A-AGC------G-A--A----GA--A--C---C-A---A----AA--A-GCA-GAC---A-A--TAC--A---A-C---C---C-G-CT-AT---T-A-C---------------------------
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 145
> best bound: 0.0
> wall time: 4.692626s
> ```

In [ ]:
```python
scsp.util.bench(Model2, example_filename="protein_n010k010.txt")
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
> --- Solution (of length 48) ---
>   Sol: MQEPASFLSYLREHVNQACPKHGFDVTAINSRAREPFGNKGLHDQVYQ
> str01: M---A--LSY--------CPK-G---T---------------------
> str02: MQ---S--S-L----N-A----------I------P---------V--
> str03: M--P---LSY------Q----H-F-------R-------K--------
> str04: M-E---------EHVN------------------E------LHD----
> str05: M----S---------N-------FD--AI--RA--------L------
> str06: M-----F----R---NQ------------NSR------N-G-------
> str07: M-----F--Y-------A---H-----A--------FG--G-----Y-
> str08: M----S--------------K--F--T----R-R-P----------YQ
> str09: M----SF-------V--A----G--VTA----------------Q---
> str10: M-E--S-L------V----P--GF-----N----E-------------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 48
> best bound: 0.0
> wall time: 1.084148s
> ```

In [ ]:
```python
# 5 分以内に計算が終わらなかったのでスキップ

# scsp.util.bench(Model2, example_filename="protein_n050k050.txt")
```

改善はしたが, 計算時間の増加に見合うほどではなかった.
