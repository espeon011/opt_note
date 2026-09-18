# 数理最適化自由帳

数理最適化関連で勉強した内容を Marimo のノートブック形式で `notebooks` 配下にアップロードしています. 
Marimo の Jupyter Export 機能を使って `.ipynb` 形式で `__marimo__` 配下に Jupyter Notebook に変換されたものが保存されています. 
更に nbconvert を使って Jupyter Notebook を Markdown に変換したものもアップロードしています. 

## 使い方

このリポジトリ自体をパッケージとしてインポートすることができます. 

```shell
uv add "opt_note @ git+https://github.com/espeon011/opt_note"
```

例えば次のように使用する. 

```python
>>> import opt_note.scsp as scsp
>>> instance = scsp.example.load("uniform_q26n008k015-025.txt")
>>> model = scsp.model.wmm.Model(instance)
>>> solution = model.solve()
>>> scsp.util.show(instance, solution)
--- Solution (of length 128) ---
 Sol: pioyjpbilrdeqtxfgknwzxubcevgolndcqkazbfpruvdghmpxjbrinqtvxcflcdgtdvyzscoebhmsrucdtqfzbrovpsviguimprvoxzpcqvxsdsbnnplbgiwxfdehops
str1: -------------t---k---------g--n---k------u---hmpx----n--------------------h------tq----------g-------xz---vx----------i--------s
str2: -io-j--i----q--f------------oln------b----------x--------xc-------v--s--------u---q------p-vi---------------s-sb--------xf------
str3: ----------------------u------l--c-------------------in-------------y--co----s----------ov-----------o-zp----------pl----------p-
str4: -i--------------g--------ev--------az-------g-----br----------d--d-------b-----c----------sv------rv------------nn---g---f------
str5: p--y-p--lr----------zxu-c--------------p------m-------q-v------gtd-----------------f----------ui---v----c----dsb-------------o--
str6: p-----b---de--------------v----dc---------vd---p-----------f--------zs-----ms--------bro-----------------qv----b----b-------h---
str7: -----------e------n----bc-----------z-f----------j-----tvx--------------e----r------zbr-v---ig---p-----------------l-------e----
str8: ---------r----x----w-x-----------qk-----r--d-------r--------lc--t------o--------dt--------------mpr----p---x-----------w--d-----
```

## HiGHS モデルを使う場合 (Linux)

`highspy` と `ortools` が同じ SONAME `libhighs.so.1` で別バージョンの HiGHS を同梱しているため,
1 つのプロセス内で HiGHS モデル (`scsp.model.linear1_highs` など) と
OR-Tools モデル (`scsp.model.linear1_cpsat` など) を混ぜると後から読み込んだ方が壊れます.

```
ImportError: .../highspy/_core...so: undefined symbol: _ZN5Highs13releaseMemoryEv
```

モデルは遅延 import されるので混ぜなければそのまま動きます. 混ぜたい場合はパッチを当ててください.

```shell
uv add "opt_note[patchelf] @ git+https://github.com/espeon011/opt_note"
uv run opt-note-fix-highspy
```

`patchelf` extra は patchelf コマンドを入れるだけなので, 既に導入済みなら不要です.
`highspy` を再インストールすると元に戻るので, その都度実行してください (何度実行しても安全).
仕組みは `src/opt_note/fix_highspy_soname.py` を参照.

## Marimo 起動

```shell
uv run marimo edit --headless --host 0.0.0.0 --sandbox --no-token <ノートブックのパス>
```

Marimo をリモートマシンで起動している場合,
表示された IP アドレスをリモートマシンの IP アドレスに変更してブラウザからアクセスする. 
