# 数理最適化自由帳

## Jupyter 起動

```
$ uv run jupyter lab --no-browser --ServerApp.ip="*" --ServerApp.custom_display_url="http://$(hostname):8888/lab"
```

## Marimo 起動

```
$ uv run marimo --development-mode edit --headless --sandbox --no-token
```

Marimo をリモートマシンで起動している場合, ローカルマシンで下記コマンドを実行する. 

```
$ ssh -L {ポート番号}:localhost:{ポート番号} {リモートホスト名 or IP アドレス}
```

## Marimo notebook から Jupyter notebook への変換

```
$ uv run marimo export ipynb --include-outputs <Marimo notebook name(.py file)> --output <Jupyter notebook name(.ipynb file)>
```
