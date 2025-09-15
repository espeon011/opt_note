"""
.. include:: ./README.md
"""


def find_next_strategy(
    instance: list[str],
    chars: str,
    state: tuple[int, ...],
    m: int,
) -> tuple[str, int]:
    """
    現在の状態を受け取り, m 手進めたときに sum height が最大になる文字の選び方 (長さ m の文字列として表される) と sum-height の値を組みにして返す
    """

    if m == 0 or all(idx == len(s) for idx, s in zip(state, instance)):
        return ("", 0)

    fronts = [s[idx] for idx, s in zip(state, instance) if idx < len(s)]
    counts = {char: fronts.count(char) for char in chars}
    max_sum_height = 0
    max_str_front = ""
    explores = set()
    for char in chars:
        if char not in fronts or char in explores:
            continue
        explores.add(char)
        ahead_state = tuple(
            idx + 1 if idx < len(s) and s[idx] == char else idx
            for idx, s in zip(state, instance)
        )
        str_ahead, sum_ahead = find_next_strategy(instance, chars, ahead_state, m - 1)
        if sum_ahead + counts[char] > max_sum_height:
            max_sum_height = sum_ahead + counts[char]
            max_str_front = char + str_ahead
    return (max_str_front, max_sum_height)


def solve(instance: list[str], m: int = 3, ll: int = 1) -> str:
    chars = "".join(sorted(list(set("".join(instance)))))
    state = tuple(0 for _ in instance)
    solution = ""

    while not all(idx == len(s) for idx, s in zip(state, instance)):
        next_str, _ = find_next_strategy(instance, chars, state, m)
        solution += next_str[:ll]
        for next_char in next_str[:ll]:
            state = tuple(
                idx + 1 if idx < len(s) and s[idx] == next_char else idx
                for idx, s in zip(state, instance)
            )

    return solution
