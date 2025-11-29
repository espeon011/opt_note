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
Model = scsp.model.didp_scs3.Model
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
> --- Solution (of length 62) ---
>  Sol: ulctikgnycosjiqfoevaozgkuphmplnbrxxddbcsvsrvnhutqngxzpvxissbxf
> str1: ---t-kgn---------------ku-hmp----x----------nh-tq-gxz-vxis----
> str2: ----i-----o-jiqfo------------lnb-xx---c-vs----u-q----pv-issbxf
> str3: ulc-i--nycos----o-v-oz---p--pl-----------------------p--------
> str4: ----i-g----------eva-zg--------br--ddbcsv-rvn----ng----------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 0.508398s
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
> --- Solution (of length 96) ---
>  Sol: iorjtixwxqpypfkgoblrdevazgnbrxkuxldcphmqvgztdpfzsuivxnbjychodtmsbroqvogxerzbprvxissnnbgpxlhepwdf
> str1: ----t---------kg----------n---ku-----hm------p------xn----h--t-----q--gx--z---vxis--------------
> str2: io-j-i---q---f--o-l-------nb-x--x--c----v-------su-----------------q--------p-v-iss--b--x------f
> str3: -------------------------------u-l-c--------------i--n--yc-o---s--o-vo----z-p----------p-l--p---
> str4: i--------------g-----evazg-br-----d---------d---------b--c-----s----v----r----v----nn-g--------f
> str5: ----------pyp-----lr----z----x-u---cp-mqvg-td-f--uiv-----c--d--sb-o-----------------------------
> str6: ----------p------b--dev-----------dc----v---dpfzs-------------msbroqv------b---------b----h-----
> str7: ---------------------e----nb-------c------z---f--------j-----t------v--xerzb-rv-i-----gp-l-e----
> str8: --r---xwxq----k----rd-------r----l-c-------t---------------odtm-------------pr---------px----wd-
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 96
> best bound: 67.0
> wall time: 61.198551s
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
> --- Solution (of length 151) ---
>   Sol: rxiuwopstyxqkgejnbikqfdplcevaorzxfjudlinhctgbxzqvrdmpxmlqyeecvfjuzasbingehtwdauvqrbofnezcdtmpkksobrvuofmgzxiuhkrvjsoqnzgpwcdhpzvsbnxialwdbmguyksncofhpe
> str01: --------t---kg--n--k---------------u----h----------mpx----------------n--ht-----q-----------------------g-x-----------z--------v---xi----------s-------
> str02: --i--o---------j--i-qf-------o-------l-n----bx-------x------cv-----s----------u-q-----------p------v-------i------s-------------sb-x---------------f---
> str03: ---u--------------------lc------------in-----------------y--c----------------------o-----------so--v-o---z--------------p----p--------l--------------p-
> str04: --i----------ge------------va--z-----------gb----rd-------------------------d-----b-----c------s---v-----------rv----n------------n--------g-------f---
> str05: ------p--y-------------pl-----rzx--u-----c----------p-m-q----v---------g--t-d-------f---------------u------i----v---------cd----sb----------------o----
> str06: ------p----------b----d---ev--------d----c------v-d-p---------f--z-s-----------------------m---s-br--o--------------q----------v-b-------b----------h--
> str07: --------------e-nb-------c-----z-fj-------t-----v----x----e----------------------r-----z---------brv-------i-----------gp-------------l---------------e
> str08: rx--w-----xqk-----------------r-----d------------r-----l----c-------------t--------o-----dtmp-----r---------------------p----------x---wd--------------
> str09: ------------k------kq-------a----f----i----g---q---------------j-----------w-------o---------kks--------------kr-----------------b----l----g-----------
> str10: ------------------------l-------x------------x------p-------------a-bi---------v--b----------------v-----z----k----o--z-------zv--------d--------------
> str11: ------------k-----------------r-------i-----------------------f----s---------a-v-----n--cd--------------------------q----w--h-z------------------c-----
> str12: -----------q----------------a---x--ud------g---qv-------q---c-----------e--w------b-f-------------------g--i-----j-o-----w-------------w-----y---------
> str13: r------s--xq---jn----f-p----a-------d-i-------------------------u--s-i----------q-b---ez---------------------hk----o--------h-------------mg-----------
> str14: --i-w--s--------------------------------h-------v------------------------h--------------c-------o------m---iu---v----------d------------d-m------------
> str15: ----------------------------------------h-t--x-------x--q------j-z--------------q-b-----c-t------b-----------------------------------a--------k-n------
> str16: -x-u---s-------------f---c-------f------------z-----p-----eecv-------------w-a-------n----t-----------fmg-----------q-z---------------------u----------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 151
> best bound: 62.0
> wall time: 67.512497s
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
> --- Solution (of length 27) ---
>   Sol: bbaedcadbcedeecbdbceabdcead
> str01: ----dc--bc----c-dbc----ce--
> str02: b---d--db-e-ee-----e-bd----
> str03: -----ca--c-deec----e-b--e--
> str04: --aed--d---d----d--e-bd---d
> str05: --a--c--b-e-e-c-----ab-ce--
> str06: bba-----b-e----bd-c--b---a-
> str07: bbae--a---e----b----a-d--a-
> str08: ---e------e-eecbdb-e----e--
> str09: -----c---c-dee--d---a-dc--d
> str10: b---d-a-b--d---b---ea----ad
> 
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 27.0
> wall time: 0.564036s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="uniform_q05n050k010-010.txt")
```

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
> example file name: 'nucleotide_n010k010.txt'
> best objective: 24
> best bound: 24.0
> wall time: 0.238986s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="nucleotide_n050k050.txt")
```

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
> --- Solution (of length 44) ---
>   Sol: MAPLSKFYAEETRNQHFSSLVNSDAICRPFGVFKNGTEALHYDQ
> str01: MA-LS--Y------------------C-P----K-GT-------
> str02: M-------------Q--SSL-N--AI--P--V------------
> str03: M-PLS--Y------QHF----------R-----K----------
> str04: M--------EE----H----VN---------------E-LH-D-
> str05: M---S--------N--F------DAI-R----------AL----
> str06: M-----F-----RNQ------NS----R------NG--------
> str07: M-----FYA------H--------A----FG----G-----Y--
> str08: M---SKF----TR--------------RP------------Y-Q
> str09: M---S-F-------------V---A-----GV----T-A----Q
> str10: M--------E-------S-LV-------P-G-F-N--E------
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 34.0
> wall time: 62.015336s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
