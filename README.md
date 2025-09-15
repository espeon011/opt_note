# 数理最適化自由帳

数理最適化関連で勉強した内容を Marimo のノートブック形式でアップロードしています. 
Marimo の Jupyter Export 機能を使って `.ipynb` 形式で `__marimo__` 配下に Jupyter Notebook に変換されたものが保存されています. 
更に nbconvert を使って Jupyter Notebook を Markdown に変換したものもアップロードしています. 

## Marimo 起動

```
uv run marimo edit --headless --host 0.0.0.0 --sandbox --no-token <ノートブックのパス>
```

Marimo をリモートマシンで起動している場合,
表示された IP アドレスをリモートマシンの IP アドレスに変更してブラウザからアクセスする. 
