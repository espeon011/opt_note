"""highspy と ortools が同梱する libhighs.so.1 の SONAME 衝突を解消する.

ortools と highspy はどちらも HiGHS の共有ライブラリを SONAME
``libhighs.so.1`` として wheel に同梱しているが, 中身のバージョンが異なる
(ortools 9.15 は HiGHS 1.12.0, highspy は自身と同じバージョン).
動的リンカはライブラリを SONAME 単位で重複排除するため, 先に import された
方のライブラリがプロセス全体で使われてしまい, もう一方の拡張モジュールが
シンボル解決に失敗する::

    ImportError: .../highspy/_core...so: undefined symbol: _ZN5Highs13releaseMemoryEv

highspy 側の同梱ライブラリを別名 ``libhighs_highspy.so.1`` として複製し,
highspy の ``_core`` がそちらを参照するように DT_NEEDED を書き換えることで
両者を共存させる.

Linux 専用の問題で, 他のプラットフォームでは何もしない. patchelf が必要
(``opt_note[patchelf]`` extra で PyPI 版が入る). highspy を再インストール
すると元に戻るのでその都度実行する. 何度実行しても安全.
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NEW_SONAME = "libhighs_highspy.so.1"
OLD_SONAME = "libhighs.so.1"


def find_highspy_dir() -> Path:
    spec = importlib.util.find_spec("highspy")
    if spec is None or not spec.submodule_search_locations:
        raise SystemExit("highspy が見つかりません. 先にインストールしてください.")
    return Path(next(iter(spec.submodule_search_locations)))


def unshare(path: Path) -> None:
    """ハードリンクを切って独立したファイルにする.

    venv 内のファイルは uv のグローバルキャッシュへのハードリンクなので,
    patchelf の in-place 書き換えをそのまま行うとキャッシュ側も壊れてしまう.
    """
    if path.stat().st_nlink == 1:
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp_path = Path(tmp.name)
    shutil.copy2(path, tmp_path)
    os.replace(tmp_path, path)


def patchelf(*args: str) -> str:
    return subprocess.run(
        ["patchelf", *args], check=True, capture_output=True, text=True
    ).stdout


def main() -> None:
    if sys.platform != "linux":
        print(f"{sys.platform} では不要なのでスキップします.")
        return
    if shutil.which("patchelf") is None:
        raise SystemExit(
            "patchelf が PATH にありません. "
            "`uv add opt_note[patchelf]` で PyPI 版を入れるか, "
            "OS のパッケージマネージャで導入してください."
        )

    highspy_dir = find_highspy_dir()

    cores = sorted(highspy_dir.glob("_core*.so"))
    if not cores:
        raise SystemExit(f"{highspy_dir} に _core*.so が見つかりません.")

    core = cores[0]
    new_lib = highspy_dir / NEW_SONAME
    needs_new_soname = NEW_SONAME in patchelf("--print-needed", str(core)).split()

    if needs_new_soname and new_lib.exists():
        print(f"適用済みです: {core.name} -> {NEW_SONAME}")
        return

    if not new_lib.exists():
        # libhighs.so.1 と libhighs.so.1.15.1 のように実体が複数あるので,
        # バージョン付きの方を複製元にする.
        sources = sorted(highspy_dir.glob(f"{OLD_SONAME}.*"))
        if not sources:
            raise SystemExit(f"{highspy_dir} に {OLD_SONAME}.* が見つかりません.")
        source = sources[-1]
        shutil.copy2(source, new_lib)
        new_lib.chmod(0o755)
        patchelf("--set-soname", NEW_SONAME, str(new_lib))
        print(f"{source.name} -> {NEW_SONAME} を作成しました.")

    if not needs_new_soname:
        unshare(core)
        patchelf("--replace-needed", OLD_SONAME, NEW_SONAME, str(core))
        print(f"{core.name} の参照を {OLD_SONAME} -> {NEW_SONAME} に張り替えました.")


if __name__ == "__main__":
    main()
