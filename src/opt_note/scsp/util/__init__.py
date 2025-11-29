"""
SCSP インスタンスの読み込み・書き込みや表示を行うユーティリティ.
"""

import os
import datetime
from typing import Protocol
from .. import example


def parse(filename: str | os.PathLike) -> list[str]:
    """
    問題インスタンスをファイルから読み込む.

    ファイルには文字列が改行区切りで書かれている想定.
    各行に書かれた文字列のリストを返す.

    Args:
        filename(str | os.PathLike): インスタンスファイル名
    """

    with open(filename, mode="r", encoding="UTF-8") as file:
        instance = [s.strip() for s in file.readlines()]
    return instance


def save(instance: list[str], filename: str | os.PathLike) -> None:
    """
    問題インスタンスをファイルに書き出す.

    Args:
        instance(list[str]): インスタンス
        filename(str | os.PathLike): ファイル名
    """

    with open(filename, mode="w", encoding="UTF-8", newline="\n") as file:
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


class ScspModel(Protocol):
    instance: list[str]
    solution: str | None
    best_bound: float

    def __init__(self, instance: list[str]): ...
    def solve(self, time_limit: int | None, log: bool) -> str | None: ...


def bench(
    Model: type[ScspModel],
    *,
    instance: list[str] | None = None,
    example_filename: example.ExampleFileName | None = None,
    time_limit: int | None = 60,
    log: bool = False,
) -> None:
    """
    与えられたモデルで与えられたインスタンスに対して最適化計算をし, 結果情報を出力する.
    `instance` と `example_filename` はどちらかだけを指定する必要がある.

    以下の情報を出力する.

    - 問題インスタンス.
    - 解があれば問題インスタンスと共に表示. なければその旨表示.
    - サンプルインスタンスファイル名が指定されている場合はその名前.
    - 目的関数値.
    - Dual Bound. 情報がなければ `0.0` と表示される.
    - サブモデルの dual bound があれば表示する. `inner_bound` という名前の属性の有無で判定する.

    Args:
        Model(type[ScspModel]): 最適化モデルクラス. 指定された属性やメソッドを持つ必要がある.
        instance(list[str] | None): 問題インスタンス.
        example_filename(ExampleFileName | None): サンプルインスタンスファイル名.
        time_limit(int): 計算時間上限.
        log(bool): 最適化モデルのログ出力を有効にするか.
    """

    if (instance is None and example_filename is None) or (
        instance is not None and example_filename is not None
    ):
        raise RuntimeError(
            "インスタンスとサンプルインスタンスファイル名は必ずどちらか一方のみを指定してください. "
        )

    instance_inner = None
    if instance is not None:
        instance_inner = instance
    if example_filename is not None:
        instance_inner = example.load(example_filename)
    assert instance_inner is not None

    model = Model(instance_inner)

    start = datetime.datetime.now()
    solution = model.solve(time_limit=time_limit, log=log)
    end = datetime.datetime.now()

    show(instance_inner)
    if solution is not None:
        show(instance_inner, solution)
    else:
        print("--- Solution not found ---\n")

    if example_filename is not None:
        print(f"example file name: '{example_filename}'")
    print(
        f"best objective: {len(model.solution) if model.solution is not None else None}"
    )
    print(f"best bound: {model.best_bound}")
    if hasattr(model, "inner_bound"):
        print(f"best submodel bound: {model.inner_bound}")
    print(f"wall time: {(end - start).total_seconds()}s")
