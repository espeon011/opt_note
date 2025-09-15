"""
.. include:: ./README.md
"""


def solve(instance: list[str]) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
    indices = [0 for _ in instance]
    solution = ""

    while not all(idx == len(s) for idx, s in zip(indices, instance)):
        fronts = [s[idx] for idx, s in zip(indices, instance) if idx < len(s)]
        counts = [fronts.count(c) for c in chars]
        next_char = chars[counts.index(max(counts))]

        solution += next_char
        for jdx in range(len(instance)):
            s = instance[jdx]
            idx = indices[jdx]
            if idx < len(s) and s[idx] == next_char:
                indices[jdx] += 1

    return solution
