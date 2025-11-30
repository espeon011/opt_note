In [ ]:
```python
from dataclasses import dataclass
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# LA-SH モデルと WMM を組み合わせる

LA-SH では $m$ 手進んだときに最も良い選択をするが,
より先を見て判断するため, 進んだ手数の代わりに Weight の和を採用する.

$m = 1$, $l = 1$ のときは WMM と同じである.

In [ ]:
```python
def find_next_strategy(
    instance: list[str],
    chars: str,
    state: tuple[int, ...],
    m: int,
) -> tuple[str, int]:
    """
    現在の状態を受け取り, m 手進めたときに weight の和が最大になる文字の選び方 (長さ m の文字列として表される) と sum-weight の値を組みにして返す
    """

    if m == 0 or all(idx == len(s) for idx, s in zip(state, instance)):
        return ("", 0)

    fronts = [s[idx] for idx, s in zip(state, instance) if idx < len(s)]
    counts = {char: fronts.count(char) for char in chars}
    weights = {
        char: sum(
            len(s) - idx for idx, s in zip(state, instance) if idx < len(s) and s[idx] == char
        ) for char in chars
    }
    max_sum_weight = 0
    max_str_front = ""
    explores = set()
    for char in chars:
        if char not in fronts or char in explores:
            continue
        explores.add(char)
        ahead_state = tuple(
            idx + 1 if idx < len(s) and s[idx] == char else idx
            for idx, s in zip(state, instance)
        )
        str_ahead, sum_ahead = find_next_strategy(instance, chars, ahead_state, m - 1)
        # if sum_ahead + counts[char] > max_sum_weight:
        #     max_sum_weight = sum_ahead + counts[char]
        #     max_str_front = char + str_ahead
        if sum_ahead + weights[char] > max_sum_weight:
            max_sum_weight = sum_ahead + weights[char]
            max_str_front = char + str_ahead
    return (max_str_front, max_sum_weight)
```

In [ ]:
```python
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, m: int = 3, ll: int = 1, *args, **kwargs) -> str:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        state = tuple(0 for _ in self.instance)
        solution = ""

        while not all(idx == len(s) for idx, s in zip(state, self.instance)):
            next_str, _ = find_next_strategy(self.instance, chars, state, m)
            solution += next_str[:ll]
            for next_char in next_str[:ll]:
                state = tuple(
                    idx + 1 if idx < len(s) and s[idx] == next_char else idx
                    for idx, s in zip(state, self.instance)
                )

        self.solution = solution
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
> --- Solution (of length 68) ---
>  Sol: itkgonjikqefoulcinbvahmpxxyczgobrddnbcsohvstuqpgoxrzvxinpnpsglsbpfxf
> str1: -tkg-n--k----u-------hmpx----------n----h--t-q-g-x-zvxi----s--------
> str2: i---o-ji-q-fo-l--nb-----xx-c-------------vs-uqp-----v-i----s--sb--xf
> str3: -------------ulcin--------yc--o-------so-v------o--z----p-p--l--p---
> str4: i--g------e--------va-------zg-brdd-bcs--v--------r-v--n-n--g----f--
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 68
> best bound: 0.0
> wall time: 0.028912s
> ```

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
> wall time: 0.007959s
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
> --- Solution (of length 111) ---
>  Sol: igenopbdevdaczfjtrvkgxdiypwxlqnfkrzoxulcinbdehprmpqlxxycodvgstnhodbftmuqipcsbvrogxqzbrpvxcdisgplnnbgsbwdehopfxf
> str1: ----------------t--kg---------n-k----u-------h--mp--x---------nh----t--q--------gx-z---vx--is------------------
> str2: i---o----------j-------i-----q-f---o--l--nb---------xx-c--v-s---------uq-p---v-------------is-------sb-------xf
> str3: -------------------------------------ulcin------------yco---s---o------------v-o---z--p-------pl-----------p---
> str4: ige------v-a-z------g---------------------b----r---------d-------db-------cs-vr--------v--------nn-g--------f--
> str5: -----p------------------yp--l----rz-xu-c------p-m-q-------vg-t---d-f--u-i----v-----------cd-s-----b-------o----
> str6: -----pbdevd-c-----v---d--p-----f--z-------------------------s--------m-----sb-ro--q----v----------b--b---h-----
> str7: --en--b-----czfjt-v--x----------------------e--r-----------------------------------zbr-v---i-gpl--------e------
> str8: -----------------r---x----wx-q--kr---------d---r---l---c-----t--od--tm---p----r-------p-x-------------wd-------
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 111
> best bound: 0.0
> wall time: 0.213512s
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
> wall time: 0.07511s
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
> --- Solution (of length 153) ---
>   Sol: kprisxtkgenbqawxudsflcojignqfykzpehvalrdzxuhecoxpmqsabivglnbrtdpfxjulxctovdwozsiqbkxaenhtjmruzqpswbrfgvcihkdjosxqpmgzkvrstbvlnpahngqxbfiklmwwzceghnosuvdy
> str01: ------tkg-n-------------------k-----------uh-----m-------------p-x--------------------nht-----q------g---------x----z-v-------------x--i------------s----
> str02: ---i------------------oji--qf-----------------o----------lnb-----x---xc--v----s-------------u-qp------v-i-----s---------s-b---------x-f------------------
> str03: ----------------u---lc--i-n--y---------------co----s--------------------ov--oz-----------------p-----------------p----------l-p--------------------------
> str04: ---i----ge-------------------------va---z---------------g--br-d-----------d------b---------------------c------s-------vr---v-n---ng---f------------------
> str05: -p---------------------------y--p----lr-zxu--c--pmq----vg----td-f--u-----------i----------------------vc---d--s-----------b------------------------o-----
> str06: -p---------b-----d---------------e-v---d-----c---------v------dpf------------zs-----------m-----s-br---------o--q-----v---b----------b-----------h-------
> str07: ---------enb---------c---------z--------------------------------f-j----t-v---------x-e-----r-z----br--v-i----------g----------p----------l-----e---------
> str08: --r--x--------wx-----------q--k-------rd--------------------r-------l-cto-d-------------t-m----p---r-------------p------------------x------w-----------d-
> str09: k------k----qa-----f----ig-q--------------------------------------j--------wo-----k-----------------------k---s------k-r--b-l-----g----------------------
> str10: --------------------l--------------------x-----xp---abiv---b-------------v---z----k--------------------------o------z------------------------z--------vd-
> str11: k-ri---------------f-------------------------------sa--v--n-----------c---d-----q----------------w-------h----------z-------------------------c----------
> str12: ------------qa-xud-------g-q-------v--------------q-------------------c--------------e-----------wb-fg--i---jo-----------------------------ww-----------y
> str13: --r-sx------q----------j--n-f---p---a--d--------------i------------u----------siqb---e-------z-----------hk--o------------------h---------m-----g--------
> str14: ---i----------w---s---------------hv-------h-co--m----i------------u-----vd--------------------------------d------m--------------------------------------
> str15: ----------------------------------h--------------------------t---x---x----------q--------j---zq---b----c-----------------tb----a--------k---------n------
> str16: -----x----------u-sf-c------f--zpe----------ec---------v-------------------w--------a-n-t-----------f-------------mg---------------q---------z-------u---
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 153
> best bound: 0.0
> wall time: 1.424635s
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
> wall time: 0.610664s
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
>   Sol: abdcbacdbeecdaebdecbaddacebddee
> str01: --dcb-c----cd--b--c-----ce-----
> str02: -bd----dbee---e--e-b-d---------
> str03: ---c-acd-eec--eb-e-------------
> str04: a--------e--d---d----dd--ebdd--
> str05: a--cb----eec-a-b--c------e-----
> str06: -b--ba--be-----bd-cba----------
> str07: -b--ba---e---aeb----ad-a-------
> str08: ---------ee---e--ecb-d----b--ee
> str09: ---c--cd-ee-da--d-c--d---------
> str10: -bd--a--b---d--b-e--a--a---d---
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 31
> best bound: 0.0
> wall time: 0.007537s
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
> wall time: 0.004314s
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
>   Sol: dacebdacebdabceaedcbadeabcdebceaabcd
> str01: d-c-b--c-----c---d-b-----c---ce-----
> str02: ----bd----d-b-e-e-----e----eb------d
> str03: --c---ac--d---e-e-c---e-b--e--------
> str04: -a-e-d----d------d---de-b-d--------d
> str05: -ac-b---e-----e---c-a---bc-e--------
> str06: ----b----b-ab-e----b-d---c--b--a----
> str07: ----b----b-a--eae--bad-a------------
> str08: ---e----e-----e-e-cb-d--b--e--e-----
> str09: --c----c--d---e-ed--ad---cd---------
> str10: ----bda--bd-b-ea----ad--------------
> str11: ---e-d--e-da---a----a-ea-------a----
> str12: -a----a-e--a---a---b--e----e---a--c-
> str13: ---e--a----abc-a--c------cd-b-------
> str14: ----bd--e-----ea-d----ea--de--------
> str15: --c---a-e-da-----d----e----e--e----d
> str16: ---eb--c---a-----d-ba---b---b-e-----
> str17: d----d-ce-----ea---b-dea------------
> str18: da--b--c--d------d----ea---e-c------
> str19: -a----a---d--ce-ed--a--ab-----------
> str20: -a-e----e----c----c---e----e--eaa---
> str21: ----b----bda--e---c-a--a--de--------
> str22: dace-da-e-dab-----------------------
> str23: -a----a-e--ab------b----b---bce-----
> str24: d--e-d---b---c-----b-----c-----aab--
> str25: d---bda----a--e----b----bc--b-------
> str26: d--eb---e-d-b-e----ba----c----------
> str27: --ce----eb---c---dcb-de-------------
> str28: d---b---e-da---a-d--a--ab-----------
> str29: --c----c-----c---dcb--e-b-d--c------
> str30: -a-e----e--a-c---d-b-----c--b------d
> str31: dac-b---e--a-c----c------cd---------
> str32: ---e---ceb---c----c--d--b-d-b-------
> str33: d----d---b--bce--d--a---b---b-------
> str34: -a----a-e--ab--a----a-e-b------a----
> str35: ---e---c-b--bc-a----ad---cd---------
> str36: d--eb--c-----ce---c--d--bc----------
> str37: da----ac-b-a--e-e--b-----c----------
> str38: -a---da--b----ea----a----c---ce-----
> str39: da-e---c--d-b--a--c-a--a------------
> str40: dac-b----bd--ce--dc-----------------
> str41: d--e-d---b----e-e--b----b-de--------
> str42: --c--da---d--c---dc--d-a-------a----
> str43: --ce----e-d--c-----ba-e----e-------d
> str44: --ce--a-e----c-a----a--a-c-----a----
> str45: d-c----c-----ce----b----b---b--a---d
> str46: ----b-a-e-----eae--b----b-de--------
> str47: d---bd--eb-a-c----c--d--b-----------
> str48: ---eb--c-b----e-ed--a-ea------------
> str49: -a-e----e-----e----b----b-d-bc-a----
> str50: d---bda--b---ce---cb----b-----------
> 
> example file name: 'uniform_q05n050k010-010.txt'
> best objective: 36
> best bound: 0.0
> wall time: 0.038799s
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
> wall time: 0.024443s
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
> --- Solution (of length 26) ---
>   Sol: TCATACCGGGATATCGATCGTAAACT
> str01: --AT---GGGATA-CG----------
> str02: --ATACC----T-TC---C-----C-
> str03: -CA--C-G--A-AT---T-G-A----
> str04: T-A-A-----A-ATC--T-GT-----
> str05: --A----GG--TA---A-C--AAA--
> str06: T--T-CC----TA--G---GTA----
> str07: T--T---G---TA--GATC-T-----
> str08: T------GGGA-A--G-T--T---C-
> str09: T--T-CC---A---C-A----A--CT
> str10: TC-TA-----A-A-CGA----A----
> 
> example file name: 'nucleotide_n010k010.txt'
> best objective: 26
> best bound: 0.0
> wall time: 0.003961s
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
> wall time: 0.002543s
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
> --- Solution (of length 139) ---
>   Sol: ATGAGCTCAGCTAGATCGATAGCATCATGTGCATCTACGTAGCGTAGATCATGACACTGTCAGTAGCTACAGATCTGAACTAGTCGAGTCATAGTCATGCACTGACTAGTTCGACGTCATCGATGACCTGAGACTCGAR
> str01: -T-AG-T-AG-TAGA-C--T--C--C--G-G-A---A-GT-G---A---CA--A-AC---C-----CT---GA----AA--AG---A---AT-G----G-A-T-A--A-----A--T-AT--A----------------
> str02: --G-G---A--TA-A---A---CA-C-T---C--C--CG-A----A-A--AT-A-A-T-T---T-G--AC---T-T-AA--A--C-A---A----C--GC---GAC-AGTTC-A----A--G-----------------
> str03: AT-A-C-C---T---TC-----C-T-A-G-G--T--A---A-C--A-A--A---C-C----A--A-C--CA-A-CT----T--T----T----G--AT-C--T--CT--T--G---T-A--GAT--C-TG---------
> str04: -T-A----A---A--T---TA---T-A-----ATCT---TA---TA---C-T-A----GT-A--A---A-A-A----A--TAG--G-GT----GT-A---AC---C--G----A----A---A--AC--G-G--TC---
> str05: -T----T-A---A-A---A---CA----G--C--CT--GT-G-G--G-T--TG-CAC---C-----C-AC---TC--A-C-AG--G-G-C-----C---CACTG----G---G-CG-CA---A-G--------------
> str06: ATGA-CT----T----C-----CA--ATG-G-ATC--C----C--A-A-C----C--T--CA--AGCT-----TC----C-A--C----C-----C---CA---A-T-G---G---T--T---T--C---AG-C-----
> str07: A--A-C--A---A-A-C-----CA--A----C--C-A---A-C-T---T--T-----TG--A-T--CT-C---T-TG---TAG---A-TC-T-GT--T-C--T--CTA-----A----A-CGA--AC------------
> str08: ATGA----A---A-A-CGA-A--A--AT-T--AT-TA--T--C--A-A----G-----G---GTA--T---G----GAA---GT-G-G--A-AG-C-TG-AC-GA--A-----A--T----------------------
> str09: A----CTC-G---G--C--T-GCAT---G--C-T-TA-GT-GC--A---C-T--CAC-G-CAGTA--TA-A--T-T-AA-TA----A--C-TA---AT----T-A----------------------------------
> str10: -T----T--G-TAGATC--T-G--T--T---C-TCTA---A----A---C--GA-ACT-T---TA---A-A-ATCTG---T-GT-G-G-C-T-GTCA--C--T--C---------------------------------
> str11: --G--C--AG--AG--C-AT----T--T-T-C-T--A---A---TA--TC----CAC----A--A---A-A--T--GAA---G--G---CA-A-T-A---A-T---T-GT---AC-T-A-C--T--C------------
> str12: ATGAGC-CA---AGATC-----C-----G---A-C---G-A----AGA----G-C-C---C-----C-A-AG----GA----G--GAG--A-AG----G-A--G----G---GAC--C--C-----CC-----------
> str13: -T---CTCA-C-AG-T---T--CA--A-G---A---AC----C------CA--A-A--GT-A----C--C----C----C----C----CATAG-C---C-CT--CT--T---A----A---A-G-CC--A--C-----
> str14: A-G-G-T----T---T--ATA-C--C-T-T-C--CTA-G--G--TA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TA-------------------------------
> str15: A-G-G-T----T---T--ATA-C--C-T-T-C--C--C--AG-GTA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TA-------------------------------
> str16: -T-A----A---A-A-C-A-A-C-TCA-----AT--AC--A----A---CAT-A-A--G--A--A---A-A--TC--AAC--G-C-A---A-A---A---AC--ACT----C-AC---A---A--A-------------
> str17: -----C-C-GC-----C-----CAT--T-TG-------G--GCG--G--C-T--C--T--C-G-AGC----GAT---A----G-C---TC---GTC--G-A---A-T----C--C--C-TCGA---CCT----------
> str18: AT-A-C-C---T---TC-----C--CA-G-G--T--A---A-C--A-A--A---C-C----A--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TAG----A--TC-T-G-----------------
> str19: -T---CTCA-C-AG-T---T--CA--A-G---A---AC----C-T----CA--A----GTC--T--C--C----C----C----C-A-T-A--G----GC-CT--CT--TTC-A-GTCA--G-----------------
> str20: --GA--TC---T----C--T--C-TCA----C--C---G-A----A---C----C--TG---G---C--C----C----C--G--G-G-CA-A---ATGC-C---CTA-----A--TC--C-A-GA---G-G--T-G--
> str21: A-GAGC--A---A--TC-A--G--T---G--CATC-A-G-A----A-AT-AT-AC-CT---A-T---TA----T---A-C-A--C---T--T--T---GC--T-A--AG----A----AT-------------------
> str22: A--A--T----TA-A---A-A-CATC-T---CA---A--TA-C--A-A-CAT-A-A--G--A--A---A-A-A-C--AAC--G-C-A---A-A---A---AC--ACT----C-A--T----------------------
> str23: A--A----A-C--GA---A---C-T--T-T--A---A---A----A--TC-TG----TGT--G--GCT---G-TC--A-CT---CG-G-C-T-G-CATGC--T---TAGT--G-C------------------------
> str24: AT-A----A-CTA-AT---TA-C-T---GT-C------GT----T-GA-CA-G-----G--A----C-AC-GA---G---TA----A--C-T---C--G---T--CTA-T-C----T--TC--TG--------------
> str25: ATGAG-T--G-T----C-A---C-----G---A---A--T----T----CA---C---GT-A----C-A-A--T--GAACT-G--GA-T----GT--T-CAC-G--T-G---GA----AT--A--A-------------
> str26: A----C-C-G-T-G---G---GC-----G---A-----G---CG--G-T---GAC-C-G---GT-G-T-C---T-T---C----C---T-A--GT---G----G----GT-C--C--CA-CG-T----TGA-A-----R
> str27: A--A----AG---G-T---T----T-AT----A-C--C-T----T----C----C-C----AG--G-TA-A---C--AA--A--C----CA-A--C---CA---ACT--TTCGA--TC-TC--T----TG---------
> str28: A-G---T-AG-T---TCG----C--C-TGTG--T----G-AGC-T-GA-CA--A-ACT-T-AGTAG-T---G-T-T----T-GT-GAG-----G--AT----T-A----------------------------------
> str29: -T----T----TA--T--A---C--C-T-T-C--CTA-G--G--TA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TAG----A--T----------------------
> str30: ATG--C---G---G-TCG-T--C-TC-T---C--C--C----CG--G--C-T-----T-T---T---T-----T-T---C----C----C-----C--GC---G-C-----CG-CGT--T-G--G-C--G---C-CGA-
> str31: --G---T--G--A---C-A-A--A--A-----A-C-A--TA----A--T---G-----G--A----CT-C----C--AAC-A--C----CAT-GTCA---A--G-CT--TTC-A-G-----G-T-A---GA--C-----
> str32: --G---T--G-TA-A--GA-A--A-CA-GT--A---A-G---C------C----C---G---G-A---A--G-T--G-----GT-G--T--T--T--TGC---GA-T--TTCGA-G-----G----CC-G-G-------
> str33: --GAG---A---A--T-GA--G--TC-T---CAT-TAC----CG-----C----C-C-G---GTA-CT-----T---A----G-C-A---A--G-C-T--A---A-TAGT-C-ACG-----G----C------------
> str34: ATG---T--G---G-TCGAT-GC--CATG-G-A-----G--GC------C----CAC---CAGT---T-CA--T-T-AA---G--G---C-T---C---C--TG----G--C-A--T--T-------------------
> str35: A----C---G--AG--CG-T----T--T-T--A---A-G--G-G-----C----C-C-G-C-G-A-CT---G--C-GA-C--G--G---C-----CA--CA-TG----G--C--C--C-T-G-T-A--TG----T----
> str36: --G-G-T----T---T--ATA-C--C-T-T-C--C--C--AG-GTA-A-CA--A-AC---CA--A-C--CA-A-CT----T--TCGA-TC-T---C-T----TG--TAG------------------------------
> str37: -TG-G----G--A-A--G-T----TC-----CA---A---A----AGATCA---CA-----A--A---ACA---CT-A-C----C-AGTCA-A--C---C--TGA--AGT---AC---A-C------------------
> str38: --GA----AGC--G-T---TA--A-C--GTG--T-T--G-AG-G-A-A--A--A----G--A----C-A--G--CT----TAG--GAG--A-A--CA---A--GA---G--C----T----G--G----G---------
> str39: A----C-CAGC--G--C-A---C-T--T---C------G--GC--AG--C--G-----G-CAG---C-AC----CT---C--G--G---CA--G-CA--C-CT--C-AG--C-A-G-CA---A---C------------
> str40: ATG-G----G--A---C-A-A-C-T--T----AT-T-C----C-TA--TCATG----TG-C-----C-A-AGA---G-----GT----T--T--T-A--C-C---C--G---G---T----GA---CC--A--------
> str41: -T----T--G-TAGATC--T-G--T--T---C-TCTA---A----A---C--GA-ACT-T---TA---A-A-ATCTG---T-GT-G-GT--T-GTCA--C--T--C---------------------------------
> str42: A--A-C-CA---A---C-----CA--A----C-T-T---T--CG-A--TC-T--C--T-T--GTAG--A----TCTG---T--TC---TC-TA---A---AC-GA--A---C----T--T---T-A-------------
> str43: --G-G----G-T---TC--T-GC--CA-G-GCAT--A-GT--C-T---T--T-----T-T---T---T-C---T--G-----G-CG-G-C-----C---C--T---T-GT--G---T-A---A--ACCTG---------
> str44: --G-GCT--GC-A--T-G----C-T--T----A-----GT-GC--A---C-T--CAC-G-CAGTA--TA-A--T-T-AA-TA----A--C-TA---AT----T-ACT-GT-----------------------------
> str45: -TG--C--A--T-G--C--T----T-A-GTGCA-CT-C--A-CG-----CA-G----T---A-TA---A----T-T-AA-TA----A--C-TA---AT----T-ACT-GT-CG---T----------------------
> str46: -T----TC--C-A---C-A-A-C-T--T-T-C--C-AC----C--A-A----G-C--T--C--T-GC-A-AGATC----C----C-AG--A--GTCA-G----G----G---G-C--C-T-G-T---------------
> str47: -T---CT-A---A-A-CGA-A-C-T--T-T--A---A---A----A--TC-TG----TGT--G--GCT---G-TC--A-CT---CG-G-C-T-G-CATGC--T---TAG------------------------------
> str48: A----C-C-G---GAT-G---GC--C--G--C------G-A---T---T--T-----T-TC-G--G--A--G-TC----CT--T-G-G-----G----G----GAC-----C-AC-TCA--GA--A--T-AGA------
> str49: -----CT----T-G-T--A--G-ATC-TGT---TCT-C-TA----A-A-C--GA-ACT-T---TA---A-A-ATCTG---T-GT-G-G-C-T-GTCA--C--T------------------------------------
> str50: ATGAGC--A-CTA-A--G----C-----G---A---A-G-A----A---C----CA-----A--A---A-AG--C--A----G---A--CA-A-T-A--CA---AC-----C--CG-C-T--AT----T-A--C-----
> 
> example file name: 'nucleotide_n050k050.txt'
> best objective: 139
> best bound: 0.0
> wall time: 0.106167s
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
> wall time: 0.064997s
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
> --- Solution (of length 51) ---
>   Sol: MEQSKAFPLSVRNYAEQHAFGLVNDTAICPGERKFSLRNGAHPDELTVQYQ
> str01: M----A--LS---Y--------------CP---K-----G------T----
> str02: M-QS-----S-----------L-N--AI-P-----------------V---
> str03: M------PLS---Y--QH-F------------RK-----------------
> str04: ME-------------E-H----VN-------E----L----H-D-------
> str05: M--S--------N------F----D-AI----R-------A----L-----
> str06: M-----F----RN---Q------N-----------S-RNG-----------
> str07: M-----F------YA--HAFG---------G------------------Y-
> str08: M--SK-F------------------T------R----R----P------YQ
> str09: M--S--F---V---A-----G-V--TA---------------------Q--
> str10: ME-S----L-V------------------PG---F---N-----E------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 51
> best bound: 0.0
> wall time: 0.104955s
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
> wall time: 0.035093s
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
> --- Solution (of length 419) ---
>   Sol: MAFVEFSLVLLNPLVSGKFDNSQCREVKNPLAIRTHVEQLFRSTAQKLPYGITVLQVRDSMPLFDANLGHIERTWQAVLSFKPYTDNEGIVSFTAQNLRGCFVYDENTKLGDHQISAVYPMELDKTNSIWAGFLPTQREKGIVLARSNQDEHYKLVEAGRVFSTAIQNLKGVDSETMANYPGDIKTSVRHQLEFSAKITQLPRADFGYSLERVCKTNGSLPDVHKLYGQAFINRDGSWAEDFLTIKHVMRAYIDEGPNWTSLERQHGPAIFVLYWMDKSICRLFETASHCVLPSGNKYFDMICLPRDSNAIVGYQPTDLRSIEVAGKNSFLWVNTRAIPDEGVNCHKLFIYAPGERVQEDLSMFFRWTKYGCVPSNIVELRGDHNMQATWKELRYSANDIKGTLVQRHFSAIGNLPTVY
> str01: M-----------------------R----------H---L--------------------------N---I--------------D---I---------------E-T----------Y--------S------------------SN-D---------------I---K--------N--G-----V-------------------Y------K-----------Y--A----D---AEDF------------E--------------I--L---------LF--A----------Y---------S--I------D-------G---------------G------------E-V-E------------C-------L--D---------L---------T---R------------
> str02: M---E-------------------R--------R----------A------------------------H--RT--------------------------------------HQ------------N--W-------------------D-------A-----T-----K----------P-------R---E---------R--------R--K-------------Q--------------T--------------------QH---------------RL--T--H---P------D------DS--I--Y-P---R-IE---K---------A---EG-------------R------------K---------E---DH-----------------G-----------------
> str03: M---E-------P---G--------------A--------F-STA--L---------------FDA-L--------------------------------C---D------D--I-------L----------------------------H-------R----------------------------R--LE-S----QL-R--FG----------G----V-----Q--I------------------------P----------P----------------E-----V--S-----D----PR-----V-Y----------AG------------------------YA--------L------------------L---------------------------------------
> str04: M---------------GKF------------------------------Y---------------------------------Y-------S----N-R--------------------------------------R-----LA----------V-----F--A-Q----------A------------Q---S-------R--------------------H-L-G-------GS--------------Y--E---------Q---------W-------L---A--CV--SG----D-------S-A-------------------F-----RA---E-V---K----A---RVQ----------K-------------D------------------------------------
> str05: --F--F------------------RE--N-LA--------F----Q---------Q------------G------------K------------A---R------E--------------------------F-P-----------S---E-----EA-R----A--N-----S------P----TS-R---E-------L------------------------------------W---------V-R-------------R--G---------------------------GN--------P-------------L-S-E-AG----------A---E--------------R---------R----G-----------------T------------------------------
> str06: M------------------D---------P------------S----L----T--QV-----------------W-AV---------EG--S----------V------L-----SA-------------A-----------V------D-------------TA---------ET--N---D--T------E--------P--D-----E------G-L----------------S-AE-----------------N----E---G-----------------ET-------------------R----I----------I-------------R-I-----------------------------T--G---S--------------------------------------------
> str07: MAF----------------D--------------------F-S----------V-------------------T--------------G-------N----------TKL-D-------------T-S---GF--TQ---G-V---S---------------S-------------M--------T-V-------A-------A--G--------T---L-----------I------A-D-L----V-----------------------------K-------TAS-----S--------------------Q---L---------------T--------N---L---A-----Q---S---------------------------------------------------------
> str08: MA-V----------------------------I------L--------P----------S-------------T---------YTD--G----TA---------------------A------------------------------------------------------------------------------------------------C-TNGS-PDV------------------------V-------G---T------G------------------T--------------M------------------------------WVNT--I---------L----PG-----D---FF-WT-----PS------G---------E---S--------V-R----------V-
> str09: M----------N----------------------T---------------GI------------------I--------------D-----------L---F--D-N-----H----V-----D---SI-----PT-----I-L------------------------------------P--------HQL---A--T-L---D--Y-L--V--------------------R---------TI-------IDE--N-----R--------------S-----------VL-----------L-------------------------F---------------H---I------------M-------G---S------G-------------------------------------
> str10: M-FV-F-LVLL-PLVS-----SQC--V-N-L--RT------R-T-Q-LP------------P---A-----------------YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M------------------D-S-----K---------E-----T-------I--L---------------IE-----------------I------------------------I----P----K---I----------K------S-----Y-L-------------L---D--T--N----I--S--------------P------------K---S-------Y-----N-D------F--I---------------S--R-------------------------------NK-----------N-I------------------F--V----I-----N---L--Y------------------------N-V-----------------S------T--------I-------
> str12: M------L-L-----SGK---------K------------------K-------------M-L----L-----------------DN----------------Y-E-T--------A-------------A-------------AR------------GR----------G----------GD---------E---------R--------R---------------------R-G-WA--F-----------D---------R---PAI-V-------------T----------K--------RD-------------------K-S----------D---------------R------M------------------------A-------------------H-----------
> str13: M----------N----G--------E-----------E--------------------D-----D-N----E---QA-----------------A---------------------A----E--------------Q-----------Q--------------T-----K--------------K----------AK-----R-------E---K-----P---K---QA---R-----------K-V-----------TS-E-----A-----W---------E---H---------FD---------A------TD---------------------D-G---------A--E----------------C------------------K----------------H-----------
> str14: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S-V---E----------------E---VL--S---E------A-R------Q----------------------H-L----K-------D-G--------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M-----------------------R------------------------Y-I-V-----S-P-------------Q--L-----------V------L---------------Q---V-------------G-------KG-------Q-E----VE--R----A---L----------Y-----------L------T--P-----Y-------------D----Y----I--D----E-----K--------------S------P-I---Y-----------------------YF----L-R-S-------------------------------------H-L---------------------------NI---------Q------R---------------------P---
> str16: M-----------P-----------R-V--P------V------------Y--------DS-P-------------Q-V-S--P---N------T--------V----------------P----------------Q-------AR--------L--A-----T----------------P-----S------F-A--T--P-------------T--------------F--R-G--A-D---------A-----P-----------A-F-------------------------------------------Q--D----------------T-A------N-------------Q----------------------------QA-----R-----------Q-------------
> str17: M-FV-F-LVLL-PLVS-----SQC--V-N-L--RT------R-T-Q-LP-----L----------A-----------------YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FV-F------------F-------V---L--------L--------P-----L-V--S-------------------S---------------Q----C-V---N--L---------------T---------T-R-------------------------T--Q-L-----------P--------------------P-A---Y-------TN-S-----------F------------T-----R-----G---------------V-Y-----------------------Y------P-D-------------------K-----V---------------F------R-----S------------S--V-L---H-----------S-----------------------
> str19: M---E--------------------------AI------------------I-------S---F-A--G-I-----------------GI------N------Y----K---------------K--------L--Q---------S------KL-----------Q----------------------H--------------DFG----RV------L----K----A------------LT---V-----------T--------A------------R----A----LP-G-------------------QP----------K------------------H---I-A------------------------I---R-----Q--------------------------------
> str20: MA----S--------SG------------P-------E---R--A--------------------------E----------------------------------------HQI-------------I----LP---E-------S----H--L-------S----------S------P----------L--------------------V-K--------HKL----------------L--------Y---------------------YW--K----L--T--------G--------LP-------------L-------------------PDE---C--------------D---F------------------DH--------L------I-------------------
> str21: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S-V---E----------------E---VL--S---E----V---R------Q----------------------H-L----K-------D-G--------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L-----------------------A----------------P----------S-P----N------------S-K-------I-----Q-L---F----N-------------------N-I------------------N-----------------I------D----------I--------------------------------N---------Y------------E------H------------T-L-----------Y---------F--AS--V--S---------------A----Q------------NSF------------------F--A-----Q--------W-----V----V----------------YSA-D-K---------AI-------
> str23: M-----S------------------------AI-T--E-----T--K-P---T-----------------IE------L---P-----------A--L------------------A----E---------GF---QR--------------Y--------------N-K-----T----PG-----------F----T--------------C--------V--L--------D--------------R-Y-D-----------HG----V-------I---------------N---D-------S------------------K----------I----V----L--Y------------------------N-------------------------------------------
> str24: M----------------K--N-----------I-----------A--------------------------E--------FK--------------------------K-------A--P-EL-------A-------EK---L----------L-E---VFS----NLKG-------N-------S-R-----S-----L---D---------------P---------------------------MRA----G---------------------K----------H----------D-----------V-----------V--------V----I--E--------------------S-----TK---------------------K-L--------------------------
> str25: M-----------P---------Q------PL---------------K--------Q---S--L-D----------Q---S-K-----------------------------------------------W---L---RE-----A-----E--K-----------------------------------H-L----------RA-----LE-------SL--V-----------D-S--------------------N---LE---------------------E-------------------------------------E---K---L---------------K-----P----Q--LSM-------G-------E---D---------------------VQ---S---------
> str26: M-FV-F-LVLL-PLVS-----SQC--V-N-L-I-T------R-T-Q-------------S-----------------------YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S------T--------------------Q-----------D----------------------------------------------------------------------------------------------------------------------------------------------
> str27: M----------------KFD------V---L-----------S----L---------------F-A----------------P----------------------------------------------WA--------K--V------DE---------------Q-------E----Y--D-------Q--------QL---------------N---------------N------------------------N---LE---------------SI-----TA-----P---K-FD------D-----G-----------A---------T-----E--------I----E------S----------------E-RGD----------------I-------------------
> str28: M-FV-F-LVLL-PLVS-----SQC--V-N-----------F--T----------------------N-----RT-Q--L---P--------S--A--------Y---T------------------NS----F--T-R--G-V---------Y--------------------------YP-D-K--V-----F--------R-----S---------S---V--L--------------------H-------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-------------------------------------------------------------------------W----S---------I------------------------I--V----L-K--------L-------I----S------------------IQ-------------P----------L--------L--------L--V--T--SLP----LY-----N-----------------------PN-----------------MD-S-C--------C-L---------I-----S-----------R-I------------T---P-E------L---A-G--------------K----------L--------TW---------I--------F--I-------
> str30: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S-V---E----------------E----------------------F------L----SE--A----------R-Q--------------------------------H-L-------------------K-------D-G---T---------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FV-F-LVLL-PLVS-----SQC--V---------------------------------MPLF--NL--I--T----------T--------T-Q-------------------S--Y------TN-----F--T-R--G-V---------Y--------------------------YP-D-K--V-----F--------R-----S---------S---V--L--------------------H--------------L-------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M----------------------------------H--Q------------ITV--V--S--------G-------------P-T--E--VS-T------CF--------G----S------L----------------------------H----------------------------P------------F-----Q--------SL----K-----P-V-------------------------M-A------N----------A---L---------------------G----------------V------L---E--GK-----------------------------------MF-------C--S-I----G-------------------G----R--S----L----
> str33: MA--------------------------------T----L-------L---------R-S--L--A-L------------FK----------------R-------N-K--D------------K---------P---------------------------------------------P--I-TS-------------------G-S--------G---------G-A-I-R-G--------IKH-----I----------------I---------I----------V-P--------I--P-------G----D--S-------S--------I-----------------------------T--------------------T----R-S----------R------------
> str34: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQVRD------------------VL-----------V-------RG-F--------GD---S----ME----------------E---VL--S---E------A-R------Q----------------------H-L----K-------D-G--------T-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FV-F-LVLL-PLVS-----SQC--V-N-L---T--------T------G-T--Q------L-------------------P------------------------------------P----------A---------------------Y----------T---N-----S-------------------F----T---R---G-----V-------------Y------------------------Y----P-------------------DK------------V-------F------R-S------------S--V------L--------------H---------------S---------------------------------------------------------
> str36: MA---------N--------------------I------------------I--------------NL------W-----------N-GIV----------------------------PM---------------------V-----QD-----V-----------N---V-----A--------S----------IT----A-F--------K---S-----------------------------M---IDE----T--------------W-DK------------------K----I--------------------E-A--N------T---------C----I-----------S---R--K--------------H---------R---N---------------------
> str37: M------L---N------------R-------I-----Q----T---L------------M--------------------K--T---------A-N---------N-----------Y--E---T--I---------E--I-L-R-N----Y-L----R--------L----------Y---I-------------I--L--A-------R----N----------------------E--------------EG-------R--G--I--L------I-----------------Y-D------D-N-I------D--S--V-----------------------------------------------------------------------------------------------
> str38: MA-----------------D---------P-A------------------G-T-------------N-G--E---------------EG----T-----GC-----N---G------------------W--F-------------------Y--VEA--V----------V--E---------K-----------K-T-------G--------------D-------A-I----S---D------------DE--N----E--------------------------------N---D-------S---------D----------------T------G------------E----DL-----------V---------D------------------------------------
> str39: M-FV-F-LVLL-PLVS-----SQC--V-N-L--RT------R-T-Q-LP------------P-----------------S---YT-N----SFT----RG--VY--------------YP---DK-----------------V------------------F--------------------------R-----S-------------S---V------L---H------------S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M---E-SLV---P---G-F-N----E-K------THV-QL--S----LP----VLQV-------------------------------------------C---D------------V----L-------------------V--R------------G--F--------G-DS-------------V----E-----------------E-V------L----------------S--E----------A------------RQH------L----K---------------------D------------G---T------------------------------------------------------------------------------------------------------
> str41: M----------N--------N-Q-R--K------------------K-----T------------A------R---------P--------SF---N-----------------------M-L-K------------R------AR-N-----------RV-ST-------V-S----------------QL---AK-----R--F--S-----K--G-L-----L----------S------------------G--------Q-GP-------M-K----L-------V---------M--------A-------------------F-----------------------------------------------------------------------------------------
> str42: M-----S----N------FD-----------AIR----------A--L-----V----D--------------T-----------D--------A--------Y----KLG-H-I------------------------------------H------------------------M--YP-----------E-------------G--------T-----------------------E-----------Y-------------------VL-----S----------------N--F-----------------TD-R-----G--S------R-I--EGV------------------------T---------------H----T---------------V--H-----------
> str43: M-------------------------------I----E-L-R---------------------------H-E-----V-----------------Q---G----D----L-------V-------T--I------------------N-------V----V-------------ET----P-----------E-----------D----L-----------D-----G--F--RD------F--I----RA--------------H------L------IC-L---A---V--------D----------------T-----E-----------T--------------------------------T--G--------L--D----------------I------------------Y
> str44: M-FV-F-LVLL-PLVS-----SQC--V---------------------------------MPLF--NL--I--T----------T-N--------Q-------------------S--Y------TNS----F--T-R--G-V---------Y--------------------------YP-D-K--V-----F--------R-----S---------S---V--L--------------------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-----S----------K-D----------L-----V-------A------------R-----------------QA-L-----------------------------------------M----T----A------R--------------------------------------M-------K----------A--------DF------V-----------------F----------FL---------------------------FVL-W--K--------A----L-S---------LP------V---PT--R------------------------C------------Q------------------I-----D--M-A--K---------K--L-----SA-G------
> str46: MA----SL-L-------K---S--------L---T----LF-----K----------R---------------T------------------------R-----D--------Q-----P--------------P--------LA-S-----------G---S-------G----------G-------------A-I----R---G------------------------I-------------KHV----I----------------I-VL------I------------P-G----D-------S------------SI-V----------TR-------------------------S---R-----------------------------------------------------
> str47: M-----------------------R-V------R----------------GI--L--R--------N-------WQ-------------------Q---------------------------------W-----------------------------------------------------------------------------------------------------------W------I-------------WTSL----G---F---WM-------F----------------MIC----S---V-----------V-G-N--LWV-T-------V-------Y------------------YG-VP---V-----------WKE----A---K-T-------------T--
> str48: MA-VE-------P-----F----------P---R-------R------P--IT----R---P-------H------A--S---------I---------------E-----------V-----D-T-S---G---------I----------------G-----------G--S---A---G----S-------S---------------E---K-------V-------F-------------------------------------------------C-L------------------I----------G-Q---------A---------------EG-----------GE------------------P-N------------T---------------V--------------
> str49: M-F----------------------------------------------Y---------------A---H------A---F-------G----------G---YDEN--L--H---A---------------F-P-----GI----S---------------ST-------V-----AN---D----VR-------K----------YS---V---------V-------------S----------V---Y-----N-------------------K------------------KY----------N-IV--------------KN------------------K---Y-----------M---W----------------------------------------------------
> str50: MA---------N-------------------------------------Y---------S---------------------KP---------F----L-----------L-D--I--V--------------F--------------N-----K------------------D----------IK----------------------------C-----------------IN-D-S-------------------------------------------C------SH----S-----D--C--R-------YQ-----S------NS---------------------Y-----V-E-L----R--------------R---N-QA----L----N--K------------NL----
> 
> example file name: 'protein_n050k050.txt'
> best objective: 419
> best bound: 0.0
> wall time: 14.569084s
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
> wall time: 8.616101s
> ```

In [ ]:
```python

```
