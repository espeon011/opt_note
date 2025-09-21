In [ ]:
```python
import opt_note.scsp as scsp
import datetime
import didppy
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# `LA_SH` アルゴリズムのスピードを DIDP で上げたい

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
            ] + [
                (sol_len, sol_len + 1)
            ],
            preconditions=[sum_height > 0],
        )
        dpmodel.add_transition(trans)

    # Force transition
    end = didppy.Transition(
        name="",
        cost=didppy.IntExpr.state_cost(),
        effects=[(sol_len, m)],
        preconditions=[index_var == len(s) for s, index_var in zip(instance, index_vars)]
    )
    dpmodel.add_transition(end, forced=True)

    # Dual bound
    dual_bound_table = dpmodel.add_int_table(
        [
            [min(m, len(s) - idx) for idx in range(len(s) + 1)]
            for s in instance
        ]
    )
    bound = didppy.IntExpr(0)
    for sidx, index_var in enumerate(index_vars):
        bound += dual_bound_table[sidx, index_var]
    dpmodel.add_dual_bound(bound)

    dpsolver = didppy.CABS(
        dpmodel, threads=8, quiet=True
    )
    solution = dpsolver.search()

    print(f"step_time: {solution.time:f}")

    return "".join([trans.name for trans in solution.transitions])
```

In [ ]:
```python
find_next_strategy(["ba", "cb", "ca", ""], "abc", 3)
```

> ```
> step_time: 0.004687
> ```

In [ ]:
```python
def solve(instance: list[str], m: int = 3, ll: int = 1) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
    state = tuple(0 for _ in instance)
    solution = ""

    count = 0
    while not all(idx == len(s) for idx, s in zip(state, instance)):
        next_str = find_next_strategy([s[idx:] for idx, s in zip(state, instance)], chars, m)
        if len(next_str) == 0:
            break
        count += 1
        # print(f"{count=}, {next_str=}")
        solution += next_str[:ll]
        for next_char in next_str[:ll]:
            state = tuple(
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(state, instance)
            )

    return solution
```

In [ ]:
```python
def bench1(instance: list[str], m = 3, l = 1) -> None:
    start = datetime.datetime.now()
    solution = scsp.model.la_sh.solve(instance, m, l)
    end = datetime.datetime.now()
    scsp.util.show(instance)
    scsp.util.show(instance, solution)
    print(f"wall time: {(end - start).total_seconds()}s")
    print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
```

In [ ]:
```python
def bench2(instance: list[str], m = 3, l = 1) -> None:
    start = datetime.datetime.now()
    solution = solve(instance, m, l)
    end = datetime.datetime.now()
    print()
    scsp.util.show(instance)
    scsp.util.show(instance, solution)
    print(f"wall time: {(end - start).total_seconds()}s")
    print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
```

In [ ]:
```python
bench1(scsp.example.load("uniform_q26n004k015-025.txt"))
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
> wall time: 0.007515s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("uniform_q26n004k015-025.txt"))
```

> ```
> step_time: 0.001013
> step_time: 0.000993
> step_time: 0.001013
> step_time: 0.000924
> step_time: 0.001018
> step_time: 0.000951
> step_time: 0.000947
> step_time: 0.000940
> step_time: 0.000967
> step_time: 0.000990
> step_time: 0.000954
> step_time: 0.000959
> step_time: 0.001004
> step_time: 0.000747
> step_time: 0.000931
> step_time: 0.000951
> step_time: 0.000953
> step_time: 0.000930
> step_time: 0.000988
> step_time: 0.001055
> step_time: 0.000799
> step_time: 0.000973
> step_time: 0.000988
> step_time: 0.000960
> step_time: 0.000768
> step_time: 0.000988
> step_time: 0.000976
> step_time: 0.001106
> step_time: 0.000980
> step_time: 0.000973
> step_time: 0.000791
> step_time: 0.000965
> step_time: 0.000792
> step_time: 0.000872
> step_time: 0.001023
> step_time: 0.000749
> step_time: 0.000965
> step_time: 0.000979
> step_time: 0.000782
> step_time: 0.001002
> step_time: 0.000989
> step_time: 0.001682
> step_time: 0.000829
> step_time: 0.000792
> step_time: 0.000760
> step_time: 0.000984
> step_time: 0.000939
> step_time: 0.000583
> step_time: 0.000675
> step_time: 0.000594
> step_time: 0.000590
> step_time: 0.000592
> step_time: 0.000957
> step_time: 0.000611
> step_time: 0.000576
> step_time: 0.000735
> step_time: 0.000734
> step_time: 0.000750
> step_time: 0.000757
> step_time: 0.000795
> step_time: 0.000733
> step_time: 0.000916
> step_time: 0.000904
> step_time: 0.000747
> step_time: 0.000741
> step_time: 0.000415
> step_time: 0.000110
> step_time: 0.000052
> 
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
> wall time: 0.636509s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("uniform_q26n008k015-025.txt"))
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
> wall time: 0.073475s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("uniform_q26n008k015-025.txt"))
```

> ```
> step_time: 0.001599
> step_time: 0.001648
> step_time: 0.001602
> step_time: 0.001620
> step_time: 0.002105
> step_time: 0.001644
> step_time: 0.001990
> step_time: 0.001968
> step_time: 0.001987
> step_time: 0.001631
> step_time: 0.002086
> step_time: 0.001882
> step_time: 0.002059
> step_time: 0.002024
> step_time: 0.001903
> step_time: 0.002027
> step_time: 0.002115
> step_time: 0.002010
> step_time: 0.001702
> step_time: 0.001623
> step_time: 0.001650
> step_time: 0.002008
> step_time: 0.001597
> step_time: 0.002070
> step_time: 0.002045
> step_time: 0.001912
> step_time: 0.001693
> step_time: 0.001801
> step_time: 0.001730
> step_time: 0.001987
> step_time: 0.001623
> step_time: 0.002066
> step_time: 0.001894
> step_time: 0.001915
> step_time: 0.001786
> step_time: 0.001477
> step_time: 0.001581
> step_time: 0.001539
> step_time: 0.001595
> step_time: 0.001587
> step_time: 0.001920
> step_time: 0.002049
> step_time: 0.002068
> step_time: 0.001586
> step_time: 0.001596
> step_time: 0.001834
> step_time: 0.002079
> step_time: 0.001869
> step_time: 0.002007
> step_time: 0.002161
> step_time: 0.002035
> step_time: 0.002079
> step_time: 0.001982
> step_time: 0.001997
> step_time: 0.001518
> step_time: 0.001708
> step_time: 0.001488
> step_time: 0.001673
> step_time: 0.001557
> step_time: 0.001444
> step_time: 0.001528
> step_time: 0.001972
> step_time: 0.002077
> step_time: 0.001607
> step_time: 0.001580
> step_time: 0.002116
> step_time: 0.001960
> step_time: 0.001735
> step_time: 0.001979
> step_time: 0.001942
> step_time: 0.001543
> step_time: 0.001730
> step_time: 0.001746
> step_time: 0.001464
> step_time: 0.001634
> step_time: 0.001535
> step_time: 0.002023
> step_time: 0.001586
> step_time: 0.001532
> step_time: 0.001550
> step_time: 0.001963
> step_time: 0.001624
> step_time: 0.001292
> step_time: 0.001499
> step_time: 0.001517
> step_time: 0.001551
> step_time: 0.001441
> step_time: 0.001556
> step_time: 0.001563
> step_time: 0.001403
> step_time: 0.001574
> step_time: 0.001553
> step_time: 0.001479
> step_time: 0.001554
> step_time: 0.001504
> step_time: 0.001582
> step_time: 0.001215
> step_time: 0.001234
> step_time: 0.001175
> step_time: 0.001200
> step_time: 0.001300
> step_time: 0.001003
> step_time: 0.001036
> step_time: 0.000855
> step_time: 0.000816
> step_time: 0.000804
> step_time: 0.000903
> step_time: 0.000822
> step_time: 0.000134
> step_time: 0.000078
> step_time: 0.000063
> 
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
>  Sol: igepnbdcevazfojtdcrvxkgberydpfzdbulcinrsvzwxqkruvnfychmoplxsnbdromqvhiglctodztmprpxfqgxczvsuqlipxvicwdssebbhoxf
> str1: ---------------t-----kg--------------n-------k-u-----hm-p-x-n-------h----t----------qgx-zv------x-i---s--------
> str2: i------------oj---------------------i-------q-----f----o-l--nb--------------------x---xc-vsuq--p-vi---ss-b---xf
> str3: ---------------------------------ulcin-------------yc--o---s----o--v------o-z--p-p-----------l-p---------------
> str4: ige------vaz----------gb-r-d---db--c---sv-----r-vn----------n---------g------------f---------------------------
> str5: ---p----------------------y-p-----l---r--z-x---u----c---p--------mqv--g--t-d-------f-------u--i--v-c-ds--b--o--
> str6: ---p-bd-ev------dc-v-------dpfz--------s--------------m----s-b-ro-qv-------------------------------------bbh---
> str7: --e-nb-c---zf-jt---vx---er----z-b-----r-v----------------------------ig--------p-------------l----------e------
> str8: ------------------r-x---------------------wxqkr---------------dr-------lctod-tmprpx-----------------wd---------
> 
> wall time: 2.000351s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("uniform_q26n016k015-025.txt"))
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
> wall time: 0.601304s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("uniform_q26n016k015-025.txt"))
```

> ```
> step_time: 0.004948
> step_time: 0.004655
> step_time: 0.004794
> step_time: 0.007304
> step_time: 0.007811
> step_time: 0.007042
> step_time: 0.006977
> step_time: 0.006481
> step_time: 0.004938
> step_time: 0.006206
> step_time: 0.005599
> step_time: 0.006381
> step_time: 0.006635
> step_time: 0.006765
> step_time: 0.005325
> step_time: 0.006706
> step_time: 0.007049
> step_time: 0.007066
> step_time: 0.007052
> step_time: 0.007147
> step_time: 0.007140
> step_time: 0.007850
> step_time: 0.007344
> step_time: 0.008137
> step_time: 0.007153
> step_time: 0.007320
> step_time: 0.007547
> step_time: 0.007388
> step_time: 0.007203
> step_time: 0.006640
> step_time: 0.007003
> step_time: 0.007696
> step_time: 0.007416
> step_time: 0.007630
> step_time: 0.007759
> step_time: 0.006928
> step_time: 0.009354
> step_time: 0.006745
> step_time: 0.006541
> step_time: 0.005775
> step_time: 0.005305
> step_time: 0.006249
> step_time: 0.005504
> step_time: 0.007803
> step_time: 0.009911
> step_time: 0.008085
> step_time: 0.006812
> step_time: 0.005062
> step_time: 0.006701
> step_time: 0.004900
> step_time: 0.004600
> step_time: 0.004753
> step_time: 0.006193
> step_time: 0.006419
> step_time: 0.005274
> step_time: 0.005402
> step_time: 0.006924
> step_time: 0.008866
> step_time: 0.004566
> step_time: 0.004612
> step_time: 0.004898
> step_time: 0.005384
> step_time: 0.007062
> step_time: 0.006459
> step_time: 0.006623
> step_time: 0.006102
> step_time: 0.006760
> step_time: 0.007176
> step_time: 0.006972
> step_time: 0.007124
> step_time: 0.007105
> step_time: 0.005268
> step_time: 0.005110
> step_time: 0.007118
> step_time: 0.005154
> step_time: 0.006018
> step_time: 0.006581
> step_time: 0.006857
> step_time: 0.007121
> step_time: 0.007506
> step_time: 0.005966
> step_time: 0.005227
> step_time: 0.005289
> step_time: 0.006543
> step_time: 0.005411
> step_time: 0.007084
> step_time: 0.006814
> step_time: 0.005504
> step_time: 0.012521
> step_time: 0.006061
> step_time: 0.004798
> step_time: 0.004698
> step_time: 0.004187
> step_time: 0.004184
> step_time: 0.003408
> step_time: 0.004434
> step_time: 0.004352
> step_time: 0.004831
> step_time: 0.008580
> step_time: 0.006099
> step_time: 0.004534
> step_time: 0.004196
> step_time: 0.004231
> step_time: 0.003671
> step_time: 0.004155
> step_time: 0.003280
> step_time: 0.003472
> step_time: 0.004106
> step_time: 0.003193
> step_time: 0.003031
> step_time: 0.003012
> step_time: 0.002940
> step_time: 0.002814
> step_time: 0.002610
> step_time: 0.003229
> step_time: 0.003039
> step_time: 0.002905
> step_time: 0.003298
> step_time: 0.002820
> step_time: 0.002997
> step_time: 0.002983
> step_time: 0.002925
> step_time: 0.003064
> step_time: 0.002956
> step_time: 0.002660
> step_time: 0.002323
> step_time: 0.002203
> step_time: 0.002397
> step_time: 0.003069
> step_time: 0.002790
> step_time: 0.002813
> step_time: 0.002960
> step_time: 0.002189
> step_time: 0.002576
> step_time: 0.002569
> step_time: 0.002107
> step_time: 0.002159
> step_time: 0.002266
> step_time: 0.002237
> step_time: 0.002301
> step_time: 0.002179
> step_time: 0.001996
> step_time: 0.002068
> step_time: 0.002030
> step_time: 0.001537
> step_time: 0.001575
> step_time: 0.001507
> step_time: 0.001459
> step_time: 0.001150
> step_time: 0.001050
> step_time: 0.001015
> step_time: 0.000977
> step_time: 0.001020
> step_time: 0.000175
> step_time: 0.000168
> step_time: 0.000072
> 
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
>   Sol: kripxwuslxqhftkcgevaxjnfzpabdieusvdcgbqarvdnypfzhckodjiqbcesfmolvrzwxiuchozvnbpmgqjpwxanlctvfodkxgtdohmfkpskerzgqbcrtoqvigpxzsluivcwdqsjbopvxissaekgnbhwwxfy
> str01: -------------tk-g-----n---------------------------k-------------------u-h------m---p-x-n-------------h--------------t-q--g-xz----v----------xis-------------
> str02: --i------------------------------------------------o-jiq----f-ol------------nb-------x----------x-----------------c----v-----s-u-----q----pv-iss-----b---xf-
> str03: ------u-l------c-------------i-------------ny----c-o-------s--o-v--------oz---p----p----l----------------p--------------------------------------------------
> str04: --i-------------geva----z-----------gb--r-d---------d---bc-s----vr---------vn----------n---------g-----f----------------------------------------------------
> str05: ---p----------------------------------------yp-----------------l-rz-x-uc------pm-q---------v-----gtd---f-----------------------uivc-d-s-bo------------------
> str06: ---p-----------------------bd-e--vdc-----vd--pfz-----------s-m--------------------------------------------s------b-r-oqv----------------b------------bh-----
> str07: -----------------e----n----b-------c-----------z------------f---------------------j-------tv----x-----------erz--b-r---vigp---l------------------e----------
> str08: -r--xw---xq---k-------------------------r-d----------------------r----------------------lct--od---t---m--p---r------------px-------wd-----------------------
> str09: k-------------k-----------------------qa------f-------i-------------------------gqj-w--------o-k--------k-sk-r---b------------l--------------------g--------
> str10: --------lx----------x----pab-i---v---b---v-----z--ko--------------z-------zv------------------d-------------------------------------------------------------
> str11: kri---------f-------------------s------a-v-n-----c--d--q-----------w----h-z--------------c------------------------------------------------------------------
> str12: ----------q--------ax----------u--d-g-q--v-------------q-ce--------w---------b--------------f----g----------------------i--------------j-o-------------ww--y
> str13: -r-----s-xq----------jnf-pa-di-us---------------------iqb-e-------z-----h----------------------k----ohm--------g--------------------------------------------
> str14: --i--w-s---h------v-----------------------------hc-o---------m-------iu----v------------------d----d--m-----------------------------------------------------
> str15: -----------h-t------x-----------------------------------------------x------------qj---------------------------z-qbc-t-------------------b-------a-k-n-------
> str16: ----x-us----f--c-------fzp----e---------------------------e------------c---v--------w-an--t-f---------m--------gq-----------z--u----------------------------
> 
> wall time: 5.788494s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("uniform_q05n010k010-010.txt"))
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
> wall time: 0.004176s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("uniform_q05n010k010-010.txt"))
```

> ```
> step_time: 0.001375
> step_time: 0.001335
> step_time: 0.003161
> step_time: 0.002144
> step_time: 0.003060
> step_time: 0.001280
> step_time: 0.001083
> step_time: 0.001233
> step_time: 0.001055
> step_time: 0.003933
> step_time: 0.001278
> step_time: 0.001380
> step_time: 0.001191
> step_time: 0.001258
> step_time: 0.000984
> step_time: 0.001354
> step_time: 0.002153
> step_time: 0.001244
> step_time: 0.001023
> step_time: 0.002065
> step_time: 0.001078
> step_time: 0.000962
> step_time: 0.001050
> step_time: 0.000862
> step_time: 0.000797
> step_time: 0.000577
> step_time: 0.000837
> step_time: 0.000584
> step_time: 0.000111
> step_time: 0.000057
> step_time: 0.000051
> 
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
>   Sol: bdacbacdbeecdaeebadcbddeabcddee
> str01: -d-cb-c----cd---b--c------c--e-
> str02: bd-----dbee---eeb-d------------
> str03: ---c-acd-eec--e-b------e-------
> str04: --a------e--d-----d--dde-b-dd--
> str05: --acb----eec-a--b--c---e-------
> str06: b---ba--be------b-dcb---a------
> str07: b---ba---e---ae-bad-----a------
> str08: ---------ee---ee---cbd---b---ee
> str09: ---c--cd-ee-da----dc-d---------
> str10: bda-b--dbe---a---ad------------
> 
> wall time: 0.195555s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("uniform_q05n050k010-010.txt"))
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
> wall time: 0.023053s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("uniform_q05n050k010-010.txt"))
```

> ```
> step_time: 0.002597
> step_time: 0.003094
> step_time: 0.002628
> step_time: 0.002948
> step_time: 0.002946
> step_time: 0.002964
> step_time: 0.002881
> step_time: 0.002605
> step_time: 0.003142
> step_time: 0.002956
> step_time: 0.003289
> step_time: 0.002896
> step_time: 0.002908
> step_time: 0.002809
> step_time: 0.002781
> step_time: 0.002860
> step_time: 0.002739
> step_time: 0.002895
> step_time: 0.003118
> step_time: 0.003329
> step_time: 0.002221
> step_time: 0.002665
> step_time: 0.002364
> step_time: 0.002761
> step_time: 0.002753
> step_time: 0.002577
> step_time: 0.002750
> step_time: 0.002900
> step_time: 0.002928
> step_time: 0.002432
> step_time: 0.002100
> step_time: 0.002307
> step_time: 0.002207
> step_time: 0.001467
> step_time: 0.001121
> step_time: 0.000355
> step_time: 0.000181
> step_time: 0.000123
> 
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
> wall time: 0.883917s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("nucleotide_n010k010.txt"))
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
> wall time: 0.002421s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("nucleotide_n010k010.txt"))
```

> ```
> step_time: 0.001063
> step_time: 0.001184
> step_time: 0.001070
> step_time: 0.000973
> step_time: 0.001031
> step_time: 0.001095
> step_time: 0.001249
> step_time: 0.001018
> step_time: 0.001018
> step_time: 0.001009
> step_time: 0.001013
> step_time: 0.000799
> step_time: 0.003905
> step_time: 0.001041
> step_time: 0.001056
> step_time: 0.000972
> step_time: 0.001015
> step_time: 0.000767
> step_time: 0.000824
> step_time: 0.000598
> step_time: 0.000797
> step_time: 0.000793
> step_time: 0.000781
> step_time: 0.000599
> step_time: 0.000124
> step_time: 0.000119
> step_time: 0.000062
> 
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
> wall time: 0.143077s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("nucleotide_n050k050.txt"))
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
> wall time: 0.065491s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("nucleotide_n050k050.txt"))
```

> ```
> step_time: 0.002234
> step_time: 0.002013
> step_time: 0.001952
> step_time: 0.002128
> step_time: 0.002434
> step_time: 0.002094
> step_time: 0.002103
> step_time: 0.002211
> step_time: 0.001884
> step_time: 0.002035
> step_time: 0.002227
> step_time: 0.002239
> step_time: 0.002061
> step_time: 0.002076
> step_time: 0.002001
> step_time: 0.002119
> step_time: 0.002009
> step_time: 0.002187
> step_time: 0.002592
> step_time: 0.002127
> step_time: 0.001959
> step_time: 0.002360
> step_time: 0.002164
> step_time: 0.002505
> step_time: 0.002190
> step_time: 0.001989
> step_time: 0.001984
> step_time: 0.002000
> step_time: 0.002147
> step_time: 0.002053
> step_time: 0.001957
> step_time: 0.002220
> step_time: 0.002082
> step_time: 0.002207
> step_time: 0.002177
> step_time: 0.002020
> step_time: 0.002467
> step_time: 0.002072
> step_time: 0.002123
> step_time: 0.002087
> step_time: 0.001985
> step_time: 0.002379
> step_time: 0.002007
> step_time: 0.002189
> step_time: 0.002061
> step_time: 0.001997
> step_time: 0.002253
> step_time: 0.002270
> step_time: 0.002228
> step_time: 0.002033
> step_time: 0.002123
> step_time: 0.002057
> step_time: 0.002198
> step_time: 0.002243
> step_time: 0.002152
> step_time: 0.002044
> step_time: 0.002367
> step_time: 0.002166
> step_time: 0.002204
> step_time: 0.002228
> step_time: 0.002257
> step_time: 0.002272
> step_time: 0.002216
> step_time: 0.002277
> step_time: 0.002354
> step_time: 0.002181
> step_time: 0.002138
> step_time: 0.002075
> step_time: 0.002381
> step_time: 0.002280
> step_time: 0.002438
> step_time: 0.002239
> step_time: 0.002326
> step_time: 0.002146
> step_time: 0.001985
> step_time: 0.002072
> step_time: 0.002035
> step_time: 0.002168
> step_time: 0.002141
> step_time: 0.002032
> step_time: 0.002100
> step_time: 0.002177
> step_time: 0.002075
> step_time: 0.002164
> step_time: 0.002239
> step_time: 0.002130
> step_time: 0.002210
> step_time: 0.002401
> step_time: 0.002084
> step_time: 0.002251
> step_time: 0.002234
> step_time: 0.002314
> step_time: 0.002005
> step_time: 0.002329
> step_time: 0.002304
> step_time: 0.002142
> step_time: 0.001973
> step_time: 0.002033
> step_time: 0.002083
> step_time: 0.002054
> step_time: 0.002116
> step_time: 0.002071
> step_time: 0.002203
> step_time: 0.002182
> step_time: 0.002138
> step_time: 0.002145
> step_time: 0.002392
> step_time: 0.002133
> step_time: 0.002317
> step_time: 0.001909
> step_time: 0.001935
> step_time: 0.002067
> step_time: 0.002246
> step_time: 0.002157
> step_time: 0.002273
> step_time: 0.002142
> step_time: 0.002269
> step_time: 0.002317
> step_time: 0.002455
> step_time: 0.002425
> step_time: 0.002719
> step_time: 0.002227
> step_time: 0.002457
> step_time: 0.002247
> step_time: 0.002241
> step_time: 0.002375
> step_time: 0.002299
> step_time: 0.002199
> step_time: 0.001998
> step_time: 0.001647
> step_time: 0.001750
> step_time: 0.002122
> step_time: 0.002318
> step_time: 0.002382
> step_time: 0.001807
> step_time: 0.001485
> step_time: 0.001584
> step_time: 0.001623
> step_time: 0.001137
> step_time: 0.000230
> step_time: 0.000166
> step_time: 0.000114
> 
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
>   Sol: ATGAGCTCAGTCAGTCATGACATGCTATCGATGCTAGCAGTGACTACGATCAGCTAGTACTGCATAGCCAACTAGTCAGTCGATCGTGCATGACTAGCTAGATCTGACTAGCTGACTAGCTAGTCACATGCAGAGCCTRTGA
> str01: -T-AG-T-AGT-AG--A---C-T-C---CG--G--A--AGTGAC-A--A--A-C-----C--C-T-G--AA--A---AG---A------ATG----G--A--T---A--A----A-TA--TA--------------------
> str02: --G-G---A-T-A---A--ACA--CT--C----C---C-G--A--A--A--A--TA--A-T---T-------T-G--A--C--T--T--A--A--A-C-A-A-C-G-C--G---AC-AG-T--TCA-A-G------------
> str03: AT-A-C-C--T---TC----C-T---A--G--G-TA--A----C-A--A--A-C-----C---A-A-CCAACT--T---T---T-G---AT--CT--CT---T--G--TAG---A-T--CT-G-------------------
> str04: -T-A----A---A-T--T-A--T---A---AT-CT-----T-A-TAC--T-AG-TA--A----A-A---AA-TAG---G--G-T-GT--A--AC---C--GA----A--A----AC--G---GTC-----------------
> str05: -T----T-A---A---A--ACA-GC---C--TG-T-G--G-G--T----T--GC-A---C--C----C-A-CT---CA--C-A--G-G---G-C---C-----C--ACT-G--G----GC--G-CA-A-G------------
> str06: ATGA-CT---TC---CA--A--TG-----GAT-C---C-----C-A--A-C--CT----C---A-AGC----T--TC---C-A-C---C----C---C-A-AT--G----G-T---T---T---CA---GC-----------
> str07: A--A-C--A---A---A---C---C-A---A--C---CA---ACT----T----T--T---G-AT--C----T---C--T---T-GT--A-GA-T--CT-G-T-T--CT--CT-A--A---A--C----G-A-A-C------
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
> str20: --GA--TC--TC--TC-T--CA--C---CGA----A-C-----CT--G----GC-----C--C----C------G---G--G--C----A--A--A--T-G--C---C---CT-A--A--T---C-CA-G-AG-G--T--G-
> str21: A-GAGC--A---A-TCA-G---TGC-ATC-A-G--A--A---A-TA---T-A-C-----CT--AT-------TA-T-A--C-A-C-T---T---T-GCTA-A---GA--A--T-----------------------------
> str22: A--A--T---T-A---A--A-A--C-ATC--T-C-A--A-T-AC-A--A-CA--TA--A--G-A-A---AA--A--CA----A-CG--CA--A--A---A-A-C--ACT--C--A-T-------------------------
> str23: A--A----A--C-G--A--AC-T--T-T--A----A--A---A-T-C--T--G-T-GT---G----GC----T-GTCA--C--TCG-GC-TG-C-A--T-G--CT---TAG-TG-C--------------------------
> str24: AT-A----A--C--T-A--A--T--TA-C--TG-T--C-GT---T--GA-CAG---G-AC---A---C------G--AGT--A------A---CT--C--G-TCT-A-T--CT---T--CT-G-------------------
> str25: ATGAG-T--GTCA--C--GA-AT--T--C-A--C--G---T-AC-A--AT--G--A--ACTG----G--A--T-GT---TC-A-CGTG---GA--A--TA-A----------------------------------------
> str26: A----C-C-GT--G----G----GC----GA-GC--G--GTGAC--CG----G-T-GT-CT---T--CC---TAGT--G--G---GT-C----C---C-A---C-G--T---TGA--A--------------------R---
> str27: A--A----AG---GT--T----T---AT--A--C---C--T---T-C---C--C-AG----G--TA---A-C-A---A----A-C---CA--AC---C-A-A-CT---T---T--C--G--A-TC---T-C------T-TG-
> str28: A-G---T-AGT---TC--G-C---CT---G-TG-T-G-AG---CT--GA-CA---A--ACT---TAG-----TAGT--GT---T--TG--TGA---G---GAT-T-A-----------------------------------
> str29: -T----T---T-A-T-A---C---CT-TC----CTAG--GT-A--AC-A--A---A---C--CA-A-CCAACT--T---TCGATC-T-C-T---T-G-TAGAT---------------------------------------
> str30: ATG--C---G---GTC--G---T-CT--C--T-C---C-----C--CG----GCT--T--T---T-------T--T---TC---C---C----C--GC--G--C---C--GC-G--T---T-G------GC-G--CC---GA
> str31: --G---T--G--A--CA--A-A----A---A--C-A----T-A--A---T--G---G-ACT-C----C-AAC-A--C---C-AT-GT-CA--A---GCT---T-T--C-AG--G--TAG--A--C-----------------
> str32: --G---T--GT-A---A-GA-A----A-C-A-G-TA--AG---C--C---C-G---G-A----A--G-----T-G---GT-G-T--T---T---T-GC--GAT-T---T--C-GA---G---G-C-C--G--G---------
> str33: --GAG---A---A-T---GA---G-T--C--T-C-A----T---TAC---C-GC-----C--C---G-------GT-A--C--T--T--A-G-C-A---AG--CT-A--A--T-A---G-T---CAC--G--G--C------
> str34: ATG---T--G---GTC--GA--TGC---C-ATG---G-AG-G-C--C---CA-C-----C---A--G-----T--TCA-T---T-----A--A---G---G--CT--C---CTG----GC-A-T----T-------------
> str35: A----C---G--AG-C--G---T--T-T---T---A--AG-G-----G--C--C-----C-GC---G--A-CT-G-C-G---A-CG-GC----C-A-C-A--T--G----GC---C---CT-GT-A--TG-------T----
> str36: --G-G-T---T---T-AT-AC---CT-TC----C---CAG-G--TA--A-CA---A--AC--CA-A-CCAACT--T---TCGATC-T-C-T---T-G-TAG-----------------------------------------
> str37: -TG-G----G--A---A-G---T--T--C----C-A--A---A--A-GATCA-C-A--A----A-A-C-A-CTA--C---C-A--GT-CA--AC---CT-GA----A---G-T-AC-A-C----------------------
> str38: --GA----AG-C-GT--T-A-A--C----G-TG-T-----TGA----G----G--A--A----A-AG--A-C-AG-C--T---T-----A-G----G--AGA----AC-A----A---G--AG-C---TG--G-G-------
> str39: A----C-CAG-C-G-CA---C-T--T--CG--GC-AGC-G-G-C-A-G--CA-C-----CT-C---G-------G-CAG-C-A-C---C-T--C-AGC-AG--C--A--A-C------------------------------
> str40: ATG-G----G--A--CA--AC-T--TAT---T-C---C--T-A-T-C-AT--G-T-G--C--CA-AG--A----G---GT---T--T---T-AC---C-----C-G----G-TGAC---C-A--------------------
> str41: -T----T--GT-AG--AT--C-TG-T-TC--T-CTA--A---AC---GA--A-CT--T--T--A-A---AA-T---C--T-G-T-GTG---G--T---T-G-TC--ACT--C------------------------------
> str42: A--A-C-CA---A--C----CA----A-C--T--T-----T--C---GATC---T----CT---T-G-----TAG--A-TC--T-GT---T--CT--CTA-A----AC--G---A--A-CT--T----T--A----------
> str43: --G-G----GT---TC-TG-C---C-A--G--GC-A----T-A----G-TC---T--T--T---T-------T--T---TC--T-G-GC--G----GC-----C---CT---TG--T-G-TA---A-A--C----C-T--G-
> str44: --G-GCT--G-CA-T---G-C-T--TA--G-TGC-A-C--T--C-ACG--CAG-TA-TA----AT-------TA---A-T--A------A---CTA---A--T-T-ACT-G-T-----------------------------
> str45: -TG--C--A-T--G-C-T----T---A--G-TGC-A-C--T--C-ACG--CAG-TA-TA----AT-------TA---A-T--A------A---CTA---A--T-T-ACT-G-T--C--G-T---------------------
> str46: -T----TC---CA--CA--AC-T--T-TC----C-A-C-----C-A--A---GCT----CTGCA-AG--A--T---C---C---C----A-GA---G-T----C--A---G--G----G---G-C-C-TG-------T----
> str47: -T---CT-A---A---A---C--G--A---A--CT-----T---TA--A--A---A-T-CTG--T-G-----T-G---G-C--T-GT-CA---CT--C--G----G-CT-GC--A-T-GCT--T-A---G------------
> str48: A----C-C-G---G--ATG----GC---CG---C--G-A-T---T----T----T--T-C-G----G--A----GTC---C--T--TG---G----G---G----GAC---C--ACT--C-AG--A-AT--AGA--------
> str49: -----CT---T--GT-A-GA--T-CT---G-T--T--C--T--CTA--A--A-C--G-A----A---C----T--T---T--A------A--A--A--T----CTG--T-G-TG----GCT-GTCAC-T-------------
> str50: ATGAGC--A--C--T-A--A---GC----GA----AG-A---AC--C-A--A---A--A----A--GC-A----G--A--C-A------AT-AC-A---A---C---C---C-G-CTA--T--T-AC---------------
> 
> wall time: 3.321768s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("protein_n010k010.txt"))
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
> wall time: 0.034474s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("protein_n010k010.txt"))
```

> ```
> step_time: 0.004159
> step_time: 0.002024
> step_time: 0.002008
> step_time: 0.002457
> step_time: 0.002220
> step_time: 0.003137
> step_time: 0.002378
> step_time: 0.002579
> step_time: 0.002471
> step_time: 0.002637
> step_time: 0.002325
> step_time: 0.002201
> step_time: 0.002240
> step_time: 0.002402
> step_time: 0.002480
> step_time: 0.002374
> step_time: 0.002242
> step_time: 0.002219
> step_time: 0.002089
> step_time: 0.001695
> step_time: 0.001715
> step_time: 0.001734
> step_time: 0.002259
> step_time: 0.002402
> step_time: 0.001806
> step_time: 0.001754
> step_time: 0.001576
> step_time: 0.001645
> step_time: 0.001319
> step_time: 0.001691
> step_time: 0.001624
> step_time: 0.001729
> step_time: 0.001734
> step_time: 0.001563
> step_time: 0.001670
> step_time: 0.001298
> step_time: 0.001223
> step_time: 0.001230
> step_time: 0.001265
> step_time: 0.001214
> step_time: 0.001200
> step_time: 0.001267
> step_time: 0.001257
> step_time: 0.001189
> step_time: 0.000940
> step_time: 0.000946
> step_time: 0.000891
> step_time: 0.000879
> step_time: 0.000139
> step_time: 0.000122
> step_time: 0.000060
> 
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
>   Sol: MESKFALVPLSYAGQEHVFTRNAEQNSSRLNFCPKDAYQIGGHDPRALTVY
> str01: M----AL---SY--------------------CPK-----G-------T--
> str02: M-------------Q-----------SS-LN-----A--I----P----V-
> str03: M-------PLSY--Q-H-F-R-------------K----------------
> str04: ME-------------EHV---N-E-----L------------HD-------
> str05: M-S------------------N---------F---DA--I-----RAL---
> str06: M---F---------------RN--QNS-R-N---------G----------
> str07: M---F------YA---H-----A--------F--------GG--------Y
> str08: M-SKF--------------TR-------R----P---YQ------------
> str09: M-S-F--V----AG---V-T--A-Q--------------------------
> str10: MES---LVP----G----F--N-E---------------------------
> 
> wall time: 0.864689s
> solution is feasible: True
> ```

In [ ]:
```python
bench1(scsp.example.load("protein_n050k050.txt"))
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
> wall time: 8.804934s
> solution is feasible: True
> ```

In [ ]:
```python
bench2(scsp.example.load("protein_n050k050.txt"))
```

> ```
> step_time: 0.005662
> step_time: 0.022808
> step_time: 0.024436
> step_time: 0.029126
> step_time: 0.022653
> step_time: 0.024248
> step_time: 0.022595
> step_time: 0.026524
> step_time: 0.028740
> step_time: 0.022052
> step_time: 0.022678
> step_time: 0.022681
> step_time: 0.022008
> step_time: 0.023562
> step_time: 0.022209
> step_time: 0.020684
> step_time: 0.018000
> step_time: 0.015615
> step_time: 0.019997
> step_time: 0.027075
> step_time: 0.026131
> step_time: 0.026779
> step_time: 0.025631
> step_time: 0.024628
> step_time: 0.024706
> step_time: 0.023170
> step_time: 0.028399
> step_time: 0.025363
> step_time: 0.023591
> step_time: 0.024363
> step_time: 0.025214
> step_time: 0.024022
> step_time: 0.025306
> step_time: 0.027130
> step_time: 0.028681
> step_time: 0.025115
> step_time: 0.026627
> step_time: 0.030180
> step_time: 0.023049
> step_time: 0.020969
> step_time: 0.019711
> step_time: 0.026789
> step_time: 0.027941
> step_time: 0.029609
> step_time: 0.025939
> step_time: 0.022466
> step_time: 0.022956
> step_time: 0.030259
> step_time: 0.027448
> step_time: 0.026789
> step_time: 0.031566
> step_time: 0.028524
> step_time: 0.027459
> step_time: 0.024128
> step_time: 0.026183
> step_time: 0.026714
> step_time: 0.027815
> step_time: 0.026258
> step_time: 0.034250
> step_time: 0.025368
> step_time: 0.021764
> step_time: 0.025842
> step_time: 0.022753
> step_time: 0.025323
> step_time: 0.025676
> step_time: 0.030165
> step_time: 0.026796
> step_time: 0.026436
> step_time: 0.024166
> step_time: 0.027784
> step_time: 0.028992
> step_time: 0.028405
> step_time: 0.028265
> step_time: 0.026477
> step_time: 0.028821
> step_time: 0.028822
> step_time: 0.033892
> step_time: 0.028429
> step_time: 0.032304
> step_time: 0.032592
> step_time: 0.033149
> step_time: 0.032446
> step_time: 0.026908
> step_time: 0.030193
> step_time: 0.031679
> step_time: 0.029707
> step_time: 0.024915
> step_time: 0.026671
> step_time: 0.021070
> step_time: 0.025438
> step_time: 0.022096
> step_time: 0.016275
> step_time: 0.021141
> step_time: 0.017761
> step_time: 0.022535
> step_time: 0.017590
> step_time: 0.021391
> step_time: 0.021275
> step_time: 0.030902
> step_time: 0.021070
> step_time: 0.021207
> step_time: 0.024537
> step_time: 0.023493
> step_time: 0.023246
> step_time: 0.029073
> step_time: 0.027274
> step_time: 0.026764
> step_time: 0.028532
> step_time: 0.025489
> step_time: 0.028335
> step_time: 0.029888
> step_time: 0.028244
> step_time: 0.029367
> step_time: 0.024407
> step_time: 0.025865
> step_time: 0.023465
> step_time: 0.029509
> step_time: 0.026907
> step_time: 0.030262
> step_time: 0.026297
> step_time: 0.022048
> step_time: 0.025232
> step_time: 0.029045
> step_time: 0.026573
> step_time: 0.026469
> step_time: 0.025156
> step_time: 0.025995
> step_time: 0.026735
> step_time: 0.026490
> step_time: 0.027625
> step_time: 0.029035
> step_time: 0.027495
> step_time: 0.026253
> step_time: 0.022823
> step_time: 0.024799
> step_time: 0.024191
> step_time: 0.028755
> step_time: 0.033274
> step_time: 0.031072
> step_time: 0.029613
> step_time: 0.027031
> step_time: 0.028119
> step_time: 0.030507
> step_time: 0.026094
> step_time: 0.027320
> step_time: 0.026361
> step_time: 0.026831
> step_time: 0.028672
> step_time: 0.029202
> step_time: 0.024399
> step_time: 0.028078
> step_time: 0.028230
> step_time: 0.027245
> step_time: 0.032422
> step_time: 0.029238
> step_time: 0.023347
> step_time: 0.025242
> step_time: 0.029639
> step_time: 0.034476
> step_time: 0.027378
> step_time: 0.030532
> step_time: 0.027813
> step_time: 0.030322
> step_time: 0.031555
> step_time: 0.030652
> step_time: 0.028374
> step_time: 0.033919
> step_time: 0.025429
> step_time: 0.024928
> step_time: 0.027574
> step_time: 0.024843
> step_time: 0.025581
> step_time: 0.024354
> step_time: 0.023458
> step_time: 0.020413
> step_time: 0.021158
> step_time: 0.020178
> step_time: 0.015546
> step_time: 0.023062
> step_time: 0.024962
> step_time: 0.026138
> step_time: 0.026640
> step_time: 0.029562
> step_time: 0.031599
> step_time: 0.029550
> step_time: 0.024441
> step_time: 0.022921
> step_time: 0.029440
> step_time: 0.020468
> step_time: 0.022379
> step_time: 0.023630
> step_time: 0.024306
> step_time: 0.019476
> step_time: 0.025879
> step_time: 0.026185
> step_time: 0.022734
> step_time: 0.018775
> step_time: 0.015598
> step_time: 0.015470
> step_time: 0.019062
> step_time: 0.023770
> step_time: 0.023571
> step_time: 0.027914
> step_time: 0.022462
> step_time: 0.024516
> step_time: 0.025906
> step_time: 0.028974
> step_time: 0.024185
> step_time: 0.026752
> step_time: 0.026117
> step_time: 0.029621
> step_time: 0.023780
> step_time: 0.026611
> step_time: 0.024630
> step_time: 0.029384
> step_time: 0.029492
> step_time: 0.032332
> step_time: 0.029222
> step_time: 0.031484
> step_time: 0.025380
> step_time: 0.023483
> step_time: 0.022061
> step_time: 0.022999
> step_time: 0.020224
> step_time: 0.022460
> step_time: 0.022869
> step_time: 0.024466
> step_time: 0.023555
> step_time: 0.026986
> step_time: 0.023808
> step_time: 0.025919
> step_time: 0.028772
> step_time: 0.027857
> step_time: 0.025831
> step_time: 0.025798
> step_time: 0.027412
> step_time: 0.026749
> step_time: 0.029021
> step_time: 0.040507
> step_time: 0.023480
> step_time: 0.023770
> step_time: 0.024267
> step_time: 0.023718
> step_time: 0.023610
> step_time: 0.025205
> step_time: 0.028407
> step_time: 0.033351
> step_time: 0.025212
> step_time: 0.026361
> step_time: 0.025150
> step_time: 0.029627
> step_time: 0.030669
> step_time: 0.027028
> step_time: 0.025921
> step_time: 0.029905
> step_time: 0.025016
> step_time: 0.020970
> step_time: 0.019757
> step_time: 0.025182
> step_time: 0.022341
> step_time: 0.024943
> step_time: 0.025971
> step_time: 0.021081
> step_time: 0.016001
> step_time: 0.025403
> step_time: 0.025043
> step_time: 0.026167
> step_time: 0.028467
> step_time: 0.022335
> step_time: 0.023791
> step_time: 0.026938
> step_time: 0.024792
> step_time: 0.023308
> step_time: 0.023825
> step_time: 0.022008
> step_time: 0.024825
> step_time: 0.028437
> step_time: 0.024812
> step_time: 0.027536
> step_time: 0.027168
> step_time: 0.023844
> step_time: 0.024911
> step_time: 0.023948
> step_time: 0.016559
> step_time: 0.017671
> step_time: 0.018123
> step_time: 0.023948
> step_time: 0.022176
> step_time: 0.017587
> step_time: 0.018973
> step_time: 0.020705
> step_time: 0.018593
> step_time: 0.015172
> step_time: 0.020255
> step_time: 0.019692
> step_time: 0.023262
> step_time: 0.024470
> step_time: 0.025731
> step_time: 0.025858
> step_time: 0.026559
> step_time: 0.029301
> step_time: 0.029989
> step_time: 0.026621
> step_time: 0.028444
> step_time: 0.021732
> step_time: 0.024694
> step_time: 0.022273
> step_time: 0.024462
> step_time: 0.021995
> step_time: 0.024922
> step_time: 0.018100
> step_time: 0.024319
> step_time: 0.029174
> step_time: 0.025417
> step_time: 0.023263
> step_time: 0.021213
> step_time: 0.016605
> step_time: 0.016380
> step_time: 0.024976
> step_time: 0.015340
> step_time: 0.014914
> step_time: 0.018361
> step_time: 0.024564
> step_time: 0.025395
> step_time: 0.020790
> step_time: 0.024045
> step_time: 0.028525
> step_time: 0.029311
> step_time: 0.024825
> step_time: 0.025768
> step_time: 0.029211
> step_time: 0.025998
> step_time: 0.025217
> step_time: 0.027326
> step_time: 0.025225
> step_time: 0.025969
> step_time: 0.023341
> step_time: 0.021454
> step_time: 0.016523
> step_time: 0.017569
> step_time: 0.025452
> step_time: 0.025681
> step_time: 0.022854
> step_time: 0.023887
> step_time: 0.026639
> step_time: 0.023586
> step_time: 0.023351
> step_time: 0.024908
> step_time: 0.017536
> step_time: 0.021377
> step_time: 0.018586
> step_time: 0.018496
> step_time: 0.019147
> step_time: 0.018078
> step_time: 0.019189
> step_time: 0.018072
> step_time: 0.025376
> step_time: 0.020163
> step_time: 0.021659
> step_time: 0.021683
> step_time: 0.019674
> step_time: 0.031163
> step_time: 0.020043
> step_time: 0.022842
> step_time: 0.022376
> step_time: 0.018489
> step_time: 0.021807
> step_time: 0.016472
> step_time: 0.019380
> step_time: 0.016417
> step_time: 0.023358
> step_time: 0.017795
> step_time: 0.020362
> step_time: 0.014888
> step_time: 0.015585
> step_time: 0.015347
> step_time: 0.019500
> step_time: 0.017780
> step_time: 0.017264
> step_time: 0.021719
> step_time: 0.016854
> step_time: 0.018893
> step_time: 0.021419
> step_time: 0.020357
> step_time: 0.023584
> step_time: 0.022535
> step_time: 0.019744
> step_time: 0.018377
> step_time: 0.018267
> step_time: 0.018898
> step_time: 0.015527
> step_time: 0.015567
> step_time: 0.014415
> step_time: 0.018292
> step_time: 0.015049
> step_time: 0.013446
> step_time: 0.011820
> step_time: 0.009978
> step_time: 0.014560
> step_time: 0.016883
> step_time: 0.013903
> step_time: 0.019931
> step_time: 0.017803
> step_time: 0.009778
> step_time: 0.019512
> step_time: 0.011732
> step_time: 0.010334
> step_time: 0.012017
> step_time: 0.015193
> step_time: 0.014178
> step_time: 0.019216
> step_time: 0.012282
> step_time: 0.011930
> step_time: 0.010281
> step_time: 0.009681
> step_time: 0.013661
> step_time: 0.010135
> step_time: 0.009496
> step_time: 0.009019
> step_time: 0.008467
> step_time: 0.009870
> step_time: 0.012903
> step_time: 0.009162
> step_time: 0.009356
> step_time: 0.008523
> step_time: 0.008029
> step_time: 0.008300
> step_time: 0.008277
> step_time: 0.007337
> step_time: 0.007687
> step_time: 0.007984
> step_time: 0.007351
> step_time: 0.007540
> step_time: 0.005471
> step_time: 0.005284
> step_time: 0.004699
> step_time: 0.004402
> step_time: 0.004417
> step_time: 0.004221
> step_time: 0.003625
> step_time: 0.002842
> step_time: 0.004177
> step_time: 0.004345
> step_time: 0.004176
> step_time: 0.004195
> step_time: 0.004349
> step_time: 0.004198
> step_time: 0.003447
> step_time: 0.002769
> step_time: 0.003546
> step_time: 0.003740
> step_time: 0.003302
> step_time: 0.003580
> step_time: 0.003859
> step_time: 0.003374
> step_time: 0.003173
> step_time: 0.002948
> step_time: 0.003025
> step_time: 0.002538
> step_time: 0.002071
> step_time: 0.001793
> step_time: 0.001895
> step_time: 0.002545
> step_time: 0.002234
> step_time: 0.001740
> step_time: 0.001697
> step_time: 0.001314
> step_time: 0.000433
> step_time: 0.000335
> step_time: 0.000122
> 
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
> --- Solution (of length 470) ---
>   Sol: MAFVFESLVLLPLVSGKFNSQRCVENLKRAITHVQDLPSLRTPVLFQSVYKERTDAGIVNLVRSPTQGFKALGIDPSVMEAYTNSPEVLFTRWNSGIEAVRQHLYYPDKVFRTQDNSEGSIVLHASYKCTPQLASEGDIVFNMKLTAVQDRSGTIAENQVSPYDTNKELARSFGTHAILRGVYYPGDESIKLVFRNATSQLPYEHDGTSVQWFLRGACYFVINDGSEKTALHIVSPWFRGIKDSAYVQNLSEATKFMIRDNAHLYPEVRGTFICLSWDKARVQNPEIDTSHLKGFENIVRSLDQARPEKVLGFATYSIRGVDNETCQAIGLPGDSWMRAKNIVFLESTVYQHDAIRDGENKCLMISADTRIEGVNSTKYHPFDLKAITVPDEQLFCRSDMGAHERNIVVGKNLTWFADSIVRQESTKVYMFCKHAPSLIYGRVPVWINEKAEGHDRSNLVAKEDHGRTTV
> str01: M--------------------R----------H---L----------------------N-------------ID---------------------IE--------------T-------------Y-------S----------------S-----N-----D-------------I------------K----N----------G--V--------Y--------K-----------------Y------A------D-A----E----------D----------------FE-I---L--------L-FA-YSI---D-------G--G------------E--V---------E--CL----D---------------L---T--------R-------------------------------------------------------------------------
> str02: M----E---------------R------RA--H-------RT------------------------------------------------------------H----------Q-N-----------------------------------------------------------------------------------------------W-----------D-----A-----------------------TK----------P--R----------------E-------------R-----R--K-----------------Q--------------------T--QH---R------L-----T----------HP-D-------D------S--------I---------------------Y------P-----R----I-EKAEG--R-----KEDHG----
> str03: M----E-----P---G-------------A---------------F-S-----T-A----L-------F-----D-----A-------L---------------------------------------C--------D-----------D----I-------------L------H---R--------------R-----L--E----S-Q--LR----F----G--------------G------VQ---------I-------P------------------PE------------V-S-D---P-----------R-V----------------------------Y---A---G--------------------Y------A-------L------------------L---------------------------------------------------------
> str04: M--------------GKF-------------------------------Y-------------------------------Y--S--------N------R----------R----------L-A--------------VF-----A-Q------A--Q-S---------R----H--L-G----G--S-------------YE------QW-L--AC--V----S-------------G--DSA----------F--R--A----EV----------KARVQ---------K---------D-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str05: --F-F----------------R--ENL--A---------------FQ-------------------QG-KA--------------------R-----E------------F-------------------P---SE--------------------E------------AR-----A------------------N--S--P-----TS-----R-----------E---L-----W---------V-----------R---------RG-----------------------G--N---------P---L-----S------E---A-G--------A------E---------R-------------R--G---T---------------------------------------------------------------------------------------------
> str06: M----------------------------------D-PSL-T----Q-V-------------------------------------------W-----AV-----------------EGS-VL--S-------A------------AV-D---T-AE-------TN--------------------D----------T-----E-------------------------------P------D--------E-----------------G----LS---A-----E----------N----------E---G-----------ET------------R---I------------IR--------I---T---G--S----------------------------------------------------------------------------------------------
> str07: MAF--------------------------------D---------F-SV----T--G--N-----T---K-L--D-------T-S----------G--------------F-TQ----G--V---S--------S-------M--T-V-------A-------------A---GT---L----------I------A--------D-------L------V------KTA----S--------S---Q-L---T------N--L---------------A--Q------S------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str08: MA-V--------------------------I-----LPS--T-------Y---TD-G--------T----A---------A-----------------------------------------------CT-----------N----------G-------SP-D-----------------V----------V-------------GT-------G------------T---------------------------M-------------------W----V-N----T--------I---L----P----G---------D---------------------F-------------------------------------F--------------------------------W----------T---------PS---G-------E-------S--V------R--V
> str09: M-----------------N------------T------------------------GI---------------ID-------------LF-----------------D-------N-------H---------------V---------D-S--I------P--T------------IL-----P-------------------H-----Q--L--A-----------T-L-----------D--Y---L-----------------VR-T-I-------------ID-------EN--RS--------VL-------------------L------------F-------H--I--------M--------G--S------------------------G---------------------------------------------------------------------
> str10: M-FVF--LVLLPLVS----SQ-CV-NL-R--T--------RT----Q-------------L---P----------P----AYTNS----FTR---G---V----YYPDKVFR----S--S-VLH-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str11: M----------------------------------D--S-----------KE-T---I--L------------I-----E----------------I-----------------------I---------P------------K----------I-----------K----S----------Y--------L--------L----D-T--------------N---------I-SP-----K-S-Y--N----------D-----------FI--S----R--N--------K---NI--------------F-------V-------I-----------N---L----Y---------N-------------V-ST---------I-----------------------------------------------------------------------------------
> str12: M------L-L----SGK----------K----------------------K---------------------------M---------L--------------L---D-------N----------Y--------E---------TA--------A-------------AR--G-----RG----GDE------R-------------------R-----------------------RG------------------------------------W--A--------------F-------D--RP------A---I--V---T--------------K---------------RD---K----S-D-R-----------------------------M-AH-------------------------------------------------------------------
> str13: M-----------------N-------------------------------------G----------------------E------E--------------------D------DN-E-------------Q-A------------A--------AE-Q----------------------------------------Q-------T-------------------K-------------K--A---------K---R-------E-----------K-----P-------K----------QAR--KV----T-S------E---A-------W---------E-----H-----------------------------FD--A-T--D-------D-GA-E---------------------------CKH------------------------------------
> str14: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D---V-LVR----GF---G-D-SV-E------EVL-----S--EA-RQHL----K-----D---G----------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str15: M--------------------R---------------------------Y-------IV----SP-Q----L-----V----------L------------Q-------V--------G--------K--------G-----------Q-------E--V-------E--R-----A-L---Y--------L-----T---PY--D------------Y--I-D--EK------SP----I----Y------------------Y------F--L-----R--------SHL----NI-----Q-RP-------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str16: M----------P---------R-V-------------P-----V-----Y----D--------SP-Q----------V------SP-------N------------------T--------V--------PQ-A----------------R-----------------LA----T---------P---S----F--AT---P-----T----F-RGA------D-----A-----P--------A----------F--------------------------Q----DT---------------A-----------------N---Q-----------------------Q--A-R------------------------------------Q-----------------------------------------------------------------------------
> str17: M-FVF--LVLLPLVS----SQ-CV-NL-R--T--------RT----Q-------------L---P------L--------AYTNS----FTR---G---V----YYPDKVFR----S--S-VLH-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str18: M-FVF------------F-----V--L---------LP-L---V---S---------------S--Q-------------------------------------------------------------C----------V-N--LT-------T----------------R---T------------------------QLP---------------------------------P--------AY-------T------N--------------S------------------F-------------------T---RGV----------------------------Y----------------------------Y-P-D-K---V-----F-RS--------------------S-V----------------L---------------H--S-------------
> str19: M----E-----------------------AI--------------------------I-----S----F-A-GI---------------------GI------------------N----------YK---------------KL---Q--S--------------K-L------------------------------Q----HD------F--G----------------------R-------V--L----K------A-L------T----------V------T---------------AR-------A----------------LPG-----------------Q-----------------------------P---K-----------------H---I---------A--I-RQ-----------------------------------------------
> str20: MA----S-------SG---------------------P-------------ER--A-----------------------E----------------------H----------Q------I-----------------I-----L----------------P-----E---S---H--L---------S---------S--P-----------L------V------K---H---------K-------L-------------LY--------------------------------------------------Y-------------------W---K----L--T---------G----L-----------------P--L-----PDE---C--D----------------F-D---------------H---LI-------------------------------
> str21: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D---V-LVR----GF---G-D-SV-E------EVL-----S--E-VRQHL----K-----D---G----------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str22: M------L---------------------A-------PS---P----------------N---S-----K---I---------------------------Q-L------F----N-------------------------N------------I--N-------------------I--------D--I-----N------YEH--T-----L----YF---------A----S-----------V---S-A-----------------------------QN-----S----F-----------------FA------------Q--------W------V-----VY---------------SAD---------K-------AI-----------------------------------------------------------------------------------
> str23: M-----S----------------------AIT-------------------E-T---------------K-----P------T-------------IE-----L--P-----------------A-------LA-EG---F-------Q-R-----------Y--NK-------T---------PG-------F---T-------------------C--V---------L-----------D---------------R-----Y------------D------------H--G----V------------------I----N----------DS----K-IV-L----Y---------N--------------------------------------------------------------------------------------------------------------
> str24: M---------------K-N-----------I------------------------A-----------------------E---------F------------------K------------------K-----A---------------------------P-----ELA-----------------E--KL--------L--E-----V--F------------S----------------------NL----K--------------G-------------N-----S---------RSLD---P-----------------------------MRA------------------G--K------------------H--D-----V------------------VV----------I---ESTK-----K----L--------------------------------
> str25: M----------P--------Q----------------P-L----------K---------------Q---------S-----------L------------------D-----Q--S----------K-----------------------------------------------------------------------------------W-LR-----------E--A---------------------E--K-------HL----R----------A-----------L---E----SL-------V-----------D------------S-----N---LE------------E------------E-----K-----LK----P--QL---S-MG--E-------------D--V-Q-S---------------------------------------------
> str26: M-FVF--LVLLPLVS----SQ-CV-NL---IT--------RT----QS-Y---T-----N---S----F-------------T--------R---G---V----YYPDKVFR----S--S-VLH-S---T-Q-----D--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str27: M---------------KF-----------------D-------VL--S------------L-------F-A----P----------------W-----A---------KV----D--E-------------Q---E--------------------------YD-----------------------------------Q----------Q--L--------N-------------------------N-----------N--L--E--------S----------I-T---------------A-P-K---F--------D-----------D-----------------------G--------A-T--E--------------I----E-----S-----ER----G-------D-I--------------------------------------------------
> str28: M-FVF--LVLLPLVS----SQ-CV-N-------------------F-------T-----N--R--TQ----L---PS---AYTNS----FTR---G---V----YYPDKVFR----S--S-VLH-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str29: M-------------------------------------------------------------------------------------------W-S-I-----------------------IVL----K----L-----I------------S--I---Q--P------L---------L------------LV----TS-LP-----------L----Y---N------------P------------N-------M--D---------------S-------------------------------------------------C-----------------------------------CL-IS---RI-----T---P----------E-L-------A-------GK-LTW----I----------F-------I-------------------------------
> str30: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D---V-LVR----GF---G-D-SV-E------E--F-------------L------------SE------A-------------------------R-------Q----------------H--L-----------K--------------DGT----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str31: M-FVF--LVLLPLVS----SQ-CV------------------------------------------------------M------P--LF---N---------L----------------I--------T---------------T-------T----Q-S-Y-TN------F-T----RGVYYP-D---K-VFR---S---------SV---L-----------------H-----------------L----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str32: M-------------------------------H-Q----------------------I-------T-----------V---------V------SG----------P-----T----E---V---S---T---------------------------------------------------------------------------------------C-F----GS----LH---P-F---------Q--S------------L--------------K-----P-------------V-------------------------------------M-A-N------------A--------L---------GV---------L-------E--------G---------K------------------MFC----S-I-G-----------G--RS-L-----------
> str33: MA-----------------------------T----L--LR------S------------L---------AL-----------------F------------------K--R---N-----------K---------D-----K-----------------P----------------------P----I-------TS-------G-S------G--------G----A--I-----RGIK--------------------H---------I-------------I----------IV-------P----------I-------------PGDS-----------S-------I-------------T-------T-------------------RS------R-----------------------------------------------------------------
> str34: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V---R-D---V-LVR----GF---G-D-S-ME------EVL-----S--EA-RQHL----K-----D---G----------T----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str35: M-FVF--LVLLPLVS----SQ-CV-NL----T---------T--------------G--------TQ----L---P---------P------------A-----Y-------T--NS-----------------------F----T----R-G------V--Y-------------------Y-P-D---K-VFR---S---------SV---L-----------------H--S-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str36: MA----------------N-----------I--------------------------I-NL-------------------------------WN-GI--V------P-----------------------------------M----VQD---------V-----N---------------V--------------A-S----------------------I------TA-------F---K-S------------MI-D------E---T-----WDK-------------K----I---------E-----A--------N-TC--I-----S--R-K-----------H---R---N--------------------------------------------------------------------------------------------------------------
> str37: M------L----------N--R--------I---Q------T--L---------------------------------M-----------------------------K---T-----------A----------------N---------------N----Y----E------T--I---------E-I-L--RN------Y----------LR---------------L--------------Y-----------I--------------I-L----AR--N-E---------E---------------G------RG--------I-L----------I-------Y--D---D--N----I--D-------S------------V---------------------------------------------------------------------------------
> str38: MA---------------------------------D-P-----------------AG--------T-----------------N-----------G-E-------------------EG----------T------G--------------------------------------------------------------------------------C----N-G-----------WF-------YV----EA--------------V-------------V---E------K---------------K-----T----G-D-----AI-----S-----------------D---D-EN-----------E--N-------D--------------SD--------------T--------------------------G-------E-----D---LV---D------
> str39: M-FVF--LVLLPLVS----SQ-CV-NL-R--T--------RT----Q-------------L---P----------PS----YTNS----FTR---G---V----YYPDKVFR----S--S-VLH-S--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str40: M----ESLV--P---G-FN-----E--K---THVQ-L-SL--PVL-Q-V-------------------------------------------------------------------------------C--------D-V----L--V--R-G-------------------FG------------D-S---V----------E----------------------E------V---------------LSEA-----R-----------------------Q-------HLK---------D--------G--T-----------------------------------------------------------------------------------------------------------------------------------------------------------
> str41: M-----------------N------N--------Q-----R---------K------------------K------------T---------------A-R-----P---------S-----------------------FNM-L---------------------K---R-----A--R---------------N------------------R-----V----S--T----VS------------Q-L--A-K---R------------F---S--K--------------G-------L--------L-----S--G------Q--G-P----M--K----L---V--------------M--A--------------F----------------------------------------------------------------------------------------
> str42: M-----S-----------N--------------------------F--------DA-I----R-------AL-----V-----------------------------D----T-D---------A-YK----L---G--------------------------------------H-I--------------------------H---------------------------------------------------M-------YPE--GT--------------E-----------------------------Y----V---------L---S-----N--F---T----D--R-G-------S---RIEGV--T--H-------TV-------------H-------------------------------------------------------------------
> str43: M-----------------------------I--------------------E--------L-R---------------------------------------H--------------E---V---------Q----GD------L--V-----TI--N-V---------------------V-----E---------T---P-E-D-------L---------DG------------FR---D------------F-IR--AHL--------ICL----A-V-----DT------E------------------T---------T----GL--D-------I-------Y------------------------------------------------------------------------------------------------------------------------
> str44: M-FVF--LVLLPLVS----SQ-CV------------------------------------------------------M------P--LF---N---------L----------------I--------T---------------T-----------NQ-S-Y-TN-----SF-T----RGVYYP-D---K-VFR---S---------SV---L-----------------H----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
> str45: M-----S---------K------------------DL------V-----------A------R---Q---AL------M---T---------------A-R-----------------------------------------MK--A--D----------------------F--------V-----------F------------------FL-----FV---------L-----W----K--A----LS------------L-P-V----------------P---T----------R-------------------------CQ-I----D--M-AK--------------------K-L--SA-----G-------------------------------------------------------------------------------------------------
> str46: MA----SL-L------K--S------L----T----L--------F----K-RT--------R-----------D--------------------------Q----P-----------------------P-LAS-G--------------SG--------------------G--AI-RG--------IK-------------H----V-----------I----------IV---------------L-------I-------P---G-------D-----------S----------S----------------I--V---T------------R--------S--------R------------------------------------------------------------------------------------------------------------------
> str47: M--------------------R-V----R---------------------------GI--L-R--------------------N--------W--------Q-----------Q-------------------------------------------------------------------------------------------------W------------------------W---I-----------------------------------W-----------TS-L-GF----------------------------------------WM------F-------------------MI------------------------------C-S---------VVG-NL-W-----V----T-VY----------YG-VPVW---K-E--------AK-----TT-
> str48: MA-V-E-----P-----F-------------------P--R-----------R-----------P--------I--------T--------R--------------P----------------HAS------------I-----------------E--V---DT------S-G---I--G----G--S-------A---------G-S----------------SEK-----V---F-----------------------------------CL-----------I------G---------QA--E---G-------G---E-------P--------N------TV-------------------------------------------------------------------------------------------------------------------------
> str49: M-F----------------------------------------------Y-----A----------------------------------------------H---------------------A---------------F-----------G--------------------G--------Y---DE-------N----L---H-----------A--F---------------P---GI--S------S--T-------------V-----------A---N---D----------VR--------K------YS---V---------------------V---S-VY---------NK----------------KY--------------------------NIV--KN--------------K-YM---------------W------------------------
> str50: MA----------------N------------------------------Y-------------S-----K-----P-------------F-------------L------------------L--------------DIVFN-K-----D----I-----------K--------------------------------------------------C---IND-S-----------------------------------------------C-S--------------H---------S-D----------------------C-----------R-----------YQ--------------S--------NS--Y---------V--E-L--R-------RN----------------Q-----------A--L---------N-K-------NL-----------
> 
> wall time: 48.255862s
> solution is feasible: True
> ```

DIDP を使うと時間が長くなる.
小さな問題であれば直接プログラミングした方がよい.
