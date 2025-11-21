"""
.. include:: ./README.md
"""


def solve(instance: list[str]) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
    solution = ""

    for i in range(max([len(s) for s in instance])):
        used = [False for _ in chars]
        for s in instance:
            if i >= len(s):
                continue
            used[chars.index(s[i])] = True

        for c, u in zip(chars, used):
            if u:
                solution += c

    return solution
