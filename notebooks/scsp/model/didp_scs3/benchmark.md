In [ ]:
```python
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# ベンチマーク

In [ ]:
```python
def bench(instance: list[str]) -> None:
    model = scsp.model.didp_scs3.create_model(instance).solve()
    solution = model.to_solution()
    scsp.util.show(instance)
    if solution is not None:
        scsp.util.show(instance, solution)
        print(f"solution is feasible: {scsp.util.is_feasible(instance, solution)}")
    else:
        print("--- Solution not found ---\n")

    print(f"solution is optimal: {model.solution.is_optimal}")
    print(f"bset bound: {model.solution.best_bound}")
```

小さいインスタンスに対しては確かに dual bound が改善した... が今まで最適性を証明できていなかったインスタンスに対して最適性を証明できたりしたわけではなかった. また, primal bound はあまり改善しなかった.

大きいインスタンスでは事前計算が完了しないため, 一部のインスタンスはスキップする.
具体的に, 以下のインスタンスはスキップ.

- `uniform_q05n050k010-010.txt`
- `nucleotide_n050k050.txt`
- `protein_n050k050.txt`

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
>  Sol: utlkcignycosjiqfoevaozkgubrdhpmpldnbxxcsvsrvnhtuqngxzpvxissbxf
> str1: -t-k--gn--------------k-u---h-mp----x-------nht-q-gxz-vxis----
> str2: -----i----o-jiqfo---------------l-nbxxc-vs-----uq----pv-issbxf
> str3: u-l-ci-nycos----o-v-oz-------p-pl--------------------p--------
> str4: -----ig----------eva-z-g-brd-----d-b--csv-rvn----ng----------f
> 
> solution is feasible: True
> solution is optimal: True
> bset bound: 62
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
> --- Solution (of length 96) ---
>  Sol: iojiqtkfopyplrbgdxevwanzgbxqkruxdrlchpmqvgztdpfzsujtivxnybcohdtmsberoqvogxzbprvxinnssgpbxlfwdphe
> str1: -----tk--------g------n-----k-u-----h-m------p--------xn----h-t------q--gxz---vxi--s------------
> str2: iojiq--fo---l---------n--bx----x---c----v-------su-------------------q------p-v-i--ss--bx-f-----
> str3: ------------------------------u---lc----------------i--ny-co----s---o-vo--z-p---------p--l---p--
> str4: i--------------g--ev-a-zgb---r--d-----------d------------bc-----s-----v------rv--nn--g----f-----
> str5: ---------pyplr---------z--x---u----c-pmqvg-td-f--u--iv----c--d--sb--o---------------------------
> str6: ---------p----b-d-ev------------d--c----v---dpfzs--------------msb-roqv----b-----------b------h-
> str7: ------------------e---n--b---------c------z---f---jt-vx-----------er------zb-rv-i----gp--l-----e
> str8: -------------r---x--w-----xqkr--drlc-------t---------------o-dtm------------pr--------p-x--wd---
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 67
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
> --- Solution (of length 154) ---
>   Sol: rxiwuposxtyqpjkgenbidkqlefvcrpaozflxjudhicntgzqbxvrdpemapxqlueycfvejwzgtsodbirafnuhvntqcsompzsbevzkgkrivctxsdozujhkfimgqvownprsbhzdxakplnbiwdvmhgeucofpsyd
> str01: ---------t----kg-n---k---------------u-h--------------m-px----------------------n-h--tq------------g------x---z---------v----------x------i------------s--
> str02: --i---o------j-----i--q--f-----o--l-------n----bx--------x-----c-v------s--------u----q----p----v-----i----s------------------sb---x-----------------f----
> str03: ----u------------------l---c------------i-n-------------------yc---------o--------------so------v------------oz-------------p---------pl--------------p---
> str04: --i------------ge---------v---a-z-----------g--b--rd----------------------db-----------cs-------v----r-v-------------------n------------n-------g----f----
> str05: -----p----y-p----------l----r---z--x-u---c----------p-m---q------v----gt--d----f-u--------------------ivc---d-----------------sb--------------------o-----
> str06: -----p------------b-d---e-v-----------d--c-------v-dp-----------f----z--s-----------------m--sb------r-------o---------qv------b---------b-----h----------
> str07: ----------------enb--------c----zf--j------t-----v-------x---e---------------r--------------z-b------r-v------------i-g-----p----------l---------e--------
> str08: rx-w----x--q--k-------------r---------d-----------r--------l---c-------t-od----------t----mp---------r----------------------p------x-------wd-------------
> str09: --------------k------kq-------a--f------i---g-q--------------------jw----o------------------------k-k------s------k----------r-b-------l--------g---------
> str10: -----------------------l-----------x------------x---p--a-------------------bi------v----------b-vzk----------oz------------------z-----------v-----------d
> str11: --------------k-------------r-----------i-----------------------f-------s-----a----vn--c--------------------d----------q--w-----hz-----------------c------
> str12: -----------q------------------a----x-ud-----g-q--v--------q----c--e-w------b---f-------------------g--i---------j--------ow----------------w------------y-
> str13: r------sx--q-j---n-------f---pa-------d-i-------------------u-----------s---i---------q-------be-z---------------hk------o------h-------------m-g---------
> str14: --iw---s-------------------------------h---------v--------------------------------h----c-om-----------i--------u--------v---------d---------d-m-----------
> str15: ---------------------------------------h---t----x--------xq--------j-z----------------q-------b---------ct---------------------b----ak--n-----------------
> str16: -x--u--s-----------------f-c-----f-----------z------pe-------e-c-v--w---------a-n----t-----------------------------f-mgq---------z----------------u-------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 62
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
> --- Solution (of length 27) ---
>   Sol: bbaeddcbacdeeecbdbceabdcead
> str01: ----d-cb-c----c-dbc----ce--
> str02: b---dd-b---eee-----e-bd----
> str03: ------c-acdee-c----e-b--e--
> str04: --aedd----d-----d--e-bd---d
> str05: --a---cb---ee-c-----ab-ce--
> str06: bba----b---e---bd-c--b---a-
> str07: bbae----a--e---b----a-d--a-
> str08: ---e-------eeecbdb-e----e--
> str09: ------c--cdee---d---a-dc--d
> str10: b---d---a------bdb-ea----ad
> 
> solution is feasible: True
> solution is optimal: True
> bset bound: 27
> ```

In [ ]:
```python
# bench(scsp.example.load("uniform_q05n050k010-010.txt"))
```

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
>   Sol: TACTGACGCGTAATCAGATCGTAC
> str01: -A-TG--G-G-A-T-A---CG---
> str02: -A-T-AC-C-T--TC----C---C
> str03: --C--ACG---AAT----T-G-A-
> str04: TA---A-----AATC---T-GT--
> str05: -A--G--G--TAA-CA-A----A-
> str06: T--T--C-C-TA----G---GTA-
> str07: T--TG-----TA----GATC-T--
> str08: T---G--G-G-AA---G-T--T-C
> str09: T--T--C-C--A--CA-A-C-T--
> str10: T-CT-A-----AA-C-GA----A-
> 
> solution is feasible: True
> solution is optimal: True
> bset bound: 24
> ```

In [ ]:
```python
# bench(scsp.example.load("nucleotide_n050k050.txt"))
```

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
> --- Solution (of length 44) ---
>   Sol: MAPLQESKFYTRNQEAFHSLVNSDAICFRPGFVNEKGTALYQHD
> str01: MA-L--S--Y----------------C--P-----KGT------
> str02: M---Q-S-----------SL-N--AI---P--V-----------
> str03: M-PL--S--Y---Q---H---------FR------K--------
> str04: M----E--------E--H--VN------------E----L--HD
> str05: M-----S-----N---F------DAI--R---------AL----
> str06: M-------F--RNQ-------NS-----R----N--G-------
> str07: M-------FY-----A-H------A--F--G-----G---Y---
> str08: M-----SKF-TR----------------RP----------YQ--
> str09: M-----S-F-----------V---A-----G-V----TA--Q--
> str10: M----ES------------LV--------PGF-NE---------
> 
> solution is feasible: True
> solution is optimal: False
> bset bound: 34
> ```

In [ ]:
```python
# bench(scsp.example.load("protein_n050k050.txt"))
```
