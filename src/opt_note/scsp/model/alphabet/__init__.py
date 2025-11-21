"""
.. include:: ./README.md
"""


def solve(instance: list[str]) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
    return chars * max([len(s) for s in instance])
