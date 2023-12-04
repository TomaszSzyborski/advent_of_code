import math
from collections import defaultdict

with open("puzzle_input.txt", "r") as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

symbol_coords = {
    (x, y): c
    for y, line in enumerate(lines)
    for x, c in enumerate(line)
    if not c.isdigit() and c != "."
}

symbol_with_neighbours_coords = defaultdict(list)
symbol_neighbour_gears = defaultdict(list)

SURROUNDS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

for x, y in symbol_coords.keys():
    symbol_with_neighbours_coords[(x, y)].extend(
        [
            (x + dx, y + dy)
            for dx, dy in SURROUNDS
            if lines[y + dy][x + dx] and lines[y + dy][x + dx].isdigit()
        ]
    )


def solve_q1():
    part_numbers = []
    visited = set()
    max_len = len(lines[0])

    for (symx, symy), neighbour_coords in symbol_with_neighbours_coords.items():
        for x, y in neighbour_coords:
            if (x, y) in visited:
                continue

            start_ix, end_ix = x, x

            while start_ix >= 0 and lines[y][start_ix].isdigit():
                visited.add((start_ix, y))
                start_ix += -1

            while end_ix < max_len and lines[y][end_ix].isdigit():
                visited.add((end_ix, y))
                end_ix += 1

            num = int(lines[y][start_ix + 1 : end_ix])
            part_numbers.append(num)
            symbol_neighbour_gears[(symx, symy)].append(num)

    # assert sum(part_numbers) == 4361
    return sum(part_numbers)


def solve_q2():
    star_coords = dict(
        filter(lambda c: c[1] == "*", symbol_coords.items())
    ).keys()

    gears = [
        [g for g in symbol_neighbour_gears[(x, y)]]
        for x, y in star_coords
        if len(symbol_neighbour_gears[(x, y)]) == 2
    ]
    power_sum = sum(list(map(math.prod, gears)))

    # assert power_sum == 91622824
    return power_sum


print(f"Q1: {solve_q1()}") 539713
print(f"Q2: {solve_q2()}")


