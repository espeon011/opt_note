In [ ]:
```python
from dataclasses import dataclass
from ortools.sat.python import cp_model
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# バイナリ変数のみで線形計画問題として定式化 (CP-SAT)

In [ ]:
```python
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        chars = "".join(sorted(list(set("".join(self.instance)))))
        max_len = sum(len(s) for s in self.instance)

        # sseq_valid[i]: 共通超配列の i 文字目を使用するか否か.
        sseq_valid = [cpmodel.new_bool_var("") for _ in range(max_len)]

        # sseq_char[i][j]: 共通超配列の i 文字目に j 番目の文字がおかれるか否か.
        sseq_char = [[cpmodel.new_bool_var("") for _ in chars] for _ in sseq_valid]

        # assign[s][c][i]: s 番目の文字列の c 番目の文字が共通超配列の i 番目に対応するか否か.
        assign = [
            [[cpmodel.new_bool_var("") for _ in sseq_valid] for c in s]
            for s in self.instance
        ]

        # 共通超配列の i 番目にはどれか 1 文字だけが置かれる.
        # 共通超配列の i 番目に文字が置かれるかどうか.
        for xs, xv in zip(sseq_char, sseq_valid):
            cpmodel.add_at_most_one(xs)
            cpmodel.add_max_equality(xv, xs)

        # s 番目の文字列の c 番目の文字は共通超配列のどこか一か所にのみ置かれる.
        for sidx, s in enumerate(self.instance):
            for cidx, c in enumerate(s):
                cpmodel.add_exactly_one(assign[sidx][cidx])

        # 共通超配列に置くときは同じ文字である必要がある.
        for idx, xs in enumerate(sseq_char):
            for j, _ in enumerate(chars):
                cpmodel.add_max_equality(
                    xs[j],
                    [
                        assign[sidx][cidx][idx]
                        for sidx, s in enumerate(self.instance)
                        for cidx, c in enumerate(s)
                        if c == chars[j]
                    ],
                )

        # s 番目の文字列の共通超配列への埋め込み順序固定.
        for sidx, s in enumerate(self.instance):
            order = [cpmodel.new_int_var(0, max_len - 1, "") for _ in s]
            for cidx, o in enumerate(order):
                cpmodel.add_map_domain(o, assign[sidx][cidx])
            for cidx, c in enumerate(s):
                if cidx == 0:
                    continue
                # cpmodel.add(
                #     sum(
                #         idx * assign[sidx][cidx - 1][idx]
                #         for idx, _ in enumerate(assign[sidx][cidx - 1])
                #     )
                #     + 1
                #     <= sum(
                #         idx * assign[sidx][cidx][idx]
                #         for idx, _ in enumerate(assign[sidx][cidx])
                #     )
                # )
                cpmodel.add(order[cidx - 1] < order[cidx])

        cpmodel.minimize(sum(sseq_valid))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            solution = ""
            for v, cs in zip(sseq_valid, sseq_char):
                if not cpsolver.boolean_value(v):
                    continue
                for cv, c in zip(cs, chars):
                    if cpsolver.boolean_value(cv):
                        solution += c
                        break
            self.solution = solution
        else:
            self.solution = None

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
> --- Solution (of length 63) ---
>  Sol: tkiojiqufoglevazcignbkrxxyddbcvosuhvmpxorvnhtoqngxzpvxissbpxlfp
> str1: tk--------g--------n-k-----------uh-mpx---nht-q-gxz-vxis-------
> str2: --iojiq-fo-l-------nb--xx----cv-su------------q----pv-issb-x-f-
> str3: -------u---l----ci-n-----y---c-os------o-v---o----zp------p-l-p
> str4: --i-------g-evaz--g-b-r---ddbc--s--v----rvn----ng------------f-
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 63
> best bound: 45.0
> wall time: 60.520087s
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
> --- Solution (of length 117) ---
>  Sol: tkignkuhmpxnoeyhjitpqgfolnbxxcvinazgbrycoddbcsvrvunneqzxucpmqvgtdfwoujtivcvdpfzsmsbxroqvbkferdzbrhvigpplctodtmprpxwed
> str1: tk-gnkuhmpxn---h--t-qg-----x------z-----------v--------x---------------i-------s-------------------------------------
> str2: --i---------o---ji--q-folnbxxcv--------------s---u---q----p--v---------i-------s-sbx------f--------------------------
> str3: ------u-----------------l----c-in-----yco----s---------------------o----v------------o--------z------ppl------p------
> str4: --ig---------e----------------v--azgbr---ddbcsvrv-nn----------g--f---------------------------------------------------
> str5: ---------p----y----p----l------------r----------------zxucpmqvgtdf--u--ivc-d---s--b--o-------------------------------
> str6: ---------p----------------b--------------d----------e--------v--d--------cvdpfzsmsb-roqvb------b-h-------------------
> str7: -------------e-----------nb--c----z------------------------------f---jt-v----------x-------er-zbr-vigp-l-----------e-
> str8: -------------------------------------r-----------------x----------w----------------x--q--k--rd--r------lctodtmprpxw-d
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 117
> best bound: 36.0
> wall time: 60.778012s
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
> --- Solution (of length 165) ---
>   Sol: phtkiyxkoprsjxguilqwexvjnasbqfokcilsxrnpzxgqdajuhfwevzrljctmgbrydcpxivmqenxdcvuosgkpbqvdhtufecziqpsvckbieomswzhapkbfgrivxjzdbnntrosfqzuvxbmidpbwxgqzhwplvcedmgsuboypf
> str01: --tk----------g---------n------k---------------uh----------m------px-----n--------------ht------q-------------------g---x-z------------vx--i------------------s------
> str02: ----i---o---j---i-q----------fo---l---n----------------------b-----x------x-cv--s---------u-----qp-v---i---s----------------------s------b------x-------------------f
> str03: ---------------u-l--------------ci----n------------------------y-c-------------os------------------------o-------------v---------o---z-------p--------pl-----------p-
> str04: ----i---------g-----e-v--a--------------z-g------------------br-d----------d--------b--------c----sv-----------------r-v-----nn------------------g------------------f
> str05: p----y---p-------l-------------------r--zx-----u---------c--------p---mq-----v---g-------t---------------------------------d-------f--u----i------------vc-d--s-bo---
> str06: p--------------------------b----------------d------ev-----------dc---v-----d-------p-------f--z---s-------ms------b--r-----------o--q--v-b----b-----h----------------
> str07: --------------------e---n--b----c-------z--------f------j-t----------v----x-----------------e------------------------r----z-b---r------v---i-----g----pl--e----------
> str08: ----------r--x-----w-x------q--k-----r------d---------rl-ct--------------------o-------d-t----------------m-----p----r-----------------------p--x----w-----d---------
> str09: ---k---k----------q------a---f---i--------gq--j---w----------------------------o--k------------------k-----s-----k---r------b--------------------------l-----g-------
> str10: -----------------l---x--------------x--p-----a---------------b------iv--------------b-v-------z------k---o---z------------z------------v----d------------------------
> str11: ---k------r-----i------------f-----s---------a------v--------------------n--c----------d--------q-----------w-h-----------z------------------------------c-----------
> str12: ------------------q------a----------x----------u----------------d----------------g---qv---------q---c---e---w-----bfg-i--j-------o-------------w-----w------------y--
> str13: ----------rs-x----q----jn----f---------p-----a------------------d---i---------u-s--------------iq-----b-e----zh--k---------------o------------------h-------mg-------
> str14: ----i--------------w------s---------------------h---v-----------------------------------h----c-----------om-----------i---------------uv----d--------------dm--------
> str15: -ht---x------x----q----j----------------z--q-----------------b---c-----------------------t------------b--------a-k-----------n---------------------------------------
> str16: ------x--------u----------s--f--c----------------f---z------------p-----e-------------------ec-----v--------w--a-------------n-t---f------m------gqz-----------u-----
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 165
> best bound: 16.0
> wall time: 62.742037s
> ```

割と良くなったかもしれない.
