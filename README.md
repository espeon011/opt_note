# 数理最適化自由帳

## Jupyter 起動

```
uv run jupyter lab --no-browser --ServerApp.ip="*" --ServerApp.custom_display_url="http://$(hostname):8888/lab"
```

## Marimo 起動

### ローカルマシンの場合

```
uv run marimo --development-mode edit --sandbox --no-token
```

### リモートマシンで起動してローカルのブラウザからアクセスしたい場合

```
uv run marimo --development-mode edit --headless --host 0.0.0.0 --sandbox --no-token
```

## Marimo notebook から Jupyter notebook への変換

```
uv run marimo export ipynb --include-outputs <Marimo notebook name(.py file)> --output <Jupyter notebook name(.ipynb file)>
```
