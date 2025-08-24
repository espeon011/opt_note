"""
SCSP インスタンスの読み込み・書き込みや表示を行う.
"""

import os
import pathlib

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


def parse(filename: str | os.PathLike) -> list[str]:
    """
    問題インスタンスをファイルから読み込む.

    ファイルには文字列が改行区切りで書かれている想定.
    各行に書かれた文字列のリストを返す.

    Args:
        filename(str | os.PathLike): インスタンスファイル名
    """

    file_path = DATA_DIR / filename
    with open(file_path, mode="r", encoding="UTF-8") as file:
        instance = [s.strip() for s in file.readlines()]
    return instance


def save(instance: list[str], filename: str | os.PathLike) -> None:
    """
    問題インスタンスをファイルに書き出す.

    Args:
        instance(list[str]): インスタンス
        filename(str | os.PathLike): ファイル名
    """

    file_path = DATA_DIR / filename
    with open(file_path, mode="w", encoding="UTF-8", newline="\n") as file:
        file.write("\n".join(instance))


def is_feasible(instance: list[str], solution: str) -> bool:
    """
    解が実行可能かどうか判定する.

    solution 文字列が instance 内の全ての文字列の supersequence になっていれば True,
    どれか 1 つでも満たさなければ False を返す.

    Args:
        instance(list[str]): 問題インスタンス
        solution(str): 共通超配列
    """

    for seq in instance:
        state = 0
        for c in solution:
            if state >= len(seq):
                break
            elif c == seq[state]:
                state += 1

        if state < len(seq):
            return False

    return True

def show(instance: list[str], solution: str | None = None) -> None:
    """
    最適化条件または最適化結果を表示する.

    solution 引数が与えられなかった場合は問題インスタンスの文字列を表示する.
    solution 引数が与えられた場合は最適化条件の各文字列がどのように解の部分列になっているかを表示する.

    solution が instance 内の各文字列の supersequence となっているかどうかはチェックしない.

    Args:
        instance(list[str]): 問題インスタンス(文字列のリスト)
        solution(str | None): 共通超配列(文字列)
    """

    instance_len = len(instance)
    tag_width = int(len(str(instance_len))) + 3

    if solution is None:
        # 問題インスタンスを出力する
        print(f"--- Condition (with {len(set(''.join(instance)))} chars) ---")
        for idx, seq in enumerate(instance):
            print(f"str{str(idx + 1).rjust(tag_width - 3, '0')}", end=": ")
            print(seq)
    else:
        # 解とインスタンスの関係を出力する
        print(f"--- Solution (of length {len(solution)}) ---")
        print("Sol".rjust(tag_width), end=": ")
        print(solution)

        for idx, seq in enumerate(instance):
            print(f"str{str(idx + 1).rjust(tag_width - 3, '0')}", end=": ")
            state = 0
            for c in solution:
                if state < len(seq) and c == seq[state]:
                    print(c, end="")
                    state += 1
                else:
                    print("-", end="")
            print()

    print()
