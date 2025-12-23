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
>  Sol: utlcikgnycoejiqfsovakouhmzppxlnhtqgbrddxxbczvsxuqvrpvisnsnbgxf
> str1: -t---kgn------------k-uhm-p-x-nhtqg----x---zv-x------is-------
> str2: ----i-----o-jiqf-o-----------ln----b---xx-c-vs-uq--pvis-s-b-xf
> str3: u-lci--nyco-----sov--o---zpp-l---------------------p----------
> str4: ----i-g----e------va-----z--------gbrdd--bc--s---vr-v--n-n-g-f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 62
> best bound: 62.0
> wall time: 0.488143s
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
>  Sol: riojixwxqfpypotblkrdgevankzgbxrulxdcphmqvgztdpfjzsutivxnybcodhtmsberoqvogxzpbrvxnnisgsbplxfwdphe
> str1: --------------t--k--g---nk-----u-----hm------p--------xn-----ht------q--gxz---vx--is------------
> str2: -ioji---qf---o--l-------n---bx---x-c----v--------su------------------q-----p--v---is-sb--xf-----
> str3: -------------------------------ul--c----------------i--ny-co----s---o-vo--zp-----------pl----p--
> str4: -i------------------geva--zgb-r---d---------d------------bc-----s-----v------rv-nn--g-----f-----
> str5: ----------pyp---l-r-------z--x-u---cp-mqvg-td-f---u-iv----c-d---sb--o---------------------------
> str6: ----------p----b---d-ev-----------dc----v---dpf-zs-------------msb-roqv-----b---------b-------h-
> str7: ---------------------e--n---b------c------z---fj---t-vx-----------er------z-brv---i-g--pl------e
> str8: r----xwxq--------krd----------r-l--c-------t---------------od-tm-----------p-r---------p-x-wd---
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 96
> best bound: 67.0
> wall time: 61.795684s
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
> --- Solution (of length 150) ---
>   Sol: rxwioupstxqykgepjinkbqdlefcpvaorzflxudizgcqnjhbtxrpvdmplxqeycfezcvwusgatonhbdivhtfujrzqpmsbnckesromvozkgixdhsqpjkrtozuvwcdgpsbxbhznnaliwkgcvedmgopsynf
> str01: --------t---kg----nk----------------u--------h-------mp-x----------------nh-----t-----q----------------g-x----------z-v-------x-------i-----------s---
> str02: ---io-----------ji---q---f----o---l--------n--b-x-------x---c----v--s-------------u---qp-----------v----i---s---------------sbx----------------------f
> str03: -----u-----------------l--c-----------i----n---------------yc-----------o----------------s-------o-voz--------p------------p---------l-----------p----
> str04: ---i---------ge-------------va--z-------g-----b--r--d-----------------------d-------------b-c--s---v-------------r----v-----------nn-----g-----------f
> str05: ------p----y---p-------l-------rz--xu----c--------p--m---q-------v---g-t----d----fu---------------------i-------------v-cd--sb------------------o-----
> str06: ------p-------------b-d-e---v--------d---c---------vd-p------f-z----s-------------------msb-----ro-----------q--------v------b-bh---------------------
> str07: --------------e---n-b-----c-----zf----------j--t---v----x-e-------------------------rz----b-----r--v----i-----------------gp---------l------e---------
> str08: rxw------xq-k------------------r-----d-----------r-----l----c----------to---d---t-------m---------------------p--r---------p--x--------w-----d--------
> str09: ------------k------k-q-------a---f----i-g-q-j---------------------w-----o--------------------k--------k-----s---kr-----------b-------l---g------------
> str10: -----------------------l-----------x------------x-p-------------------a----b-iv-----------b--------v-zk------------oz------------z---------v-d--------
> str11: ------------k------------------r------i----------------------f------s-a-------v------------nc-------------d--q---------w--------hz--------c-----------
> str12: ----------q------------------a-----xud--g-q--------v-----q--c-e---w--------b-----f---------------------gi------j---o---w---------------w-----------y--
> str13: r------s-xq-----j-n------f-p-a-------di----------------------------us--------i--------q---b---e------z-----h----k--o------------h-------------mg------
> str14: ---i--------------------------------------------------------------w-s-----h---vh------------c----om-----i------------uv--d-------------------dm-------
> str15: ---------------------------------------------h-tx-------xq-------------------------j-zq---b-c---------------------t----------b------a---k-----------n-
> str16: -x---u-s-----------------fc------f-----z----------p-------e---e-cvw---a--n------tf------m--------------g-----q------zu--------------------------------
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: 150
> best bound: 62.0
> wall time: 67.997057s
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
> example file name: 'uniform_q05n010k010-010.txt'
> best objective: 27
> best bound: 27.0
> wall time: 0.463513s
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
> wall time: 0.28808s
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
>   Sol: MEEAQSNKHPLSFTYVRNELAQHDNAISFCRPKGFNGYVTAQEL
> str01: M--A------LS--Y--------------C-PKG-----T----
> str02: M---QS-----S-------L----NAI----P------V-----
> str03: M--------PLS--Y------QH-----F-R-K-----------
> str04: MEE-----H------V-NEL--HD--------------------
> str05: M----SN-----F----------D-AI---R---------A--L
> str06: M-----------F---RN---Q--N--S--R----NG-------
> str07: M-----------F-Y-----A-H--A--F----G--GY------
> str08: M----S-K----FT--R-------------RP-----Y---Q--
> str09: M----S------F--V----A------------G----VTAQ--
> str10: ME---S----L----V---------------P-GFN------E-
> 
> example file name: 'protein_n010k010.txt'
> best objective: 44
> best bound: 34.0
> wall time: 61.761688s
> ```

In [ ]:
```python
# 問題が大きすぎるためスキップ

# scsp.util.bench(Model, example_filename="protein_n050k050.txt")
```
