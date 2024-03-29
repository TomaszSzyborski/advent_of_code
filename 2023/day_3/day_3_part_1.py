"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""
import logging
import string
from dataclasses import dataclass
import os
from typing import Self
import math
from collections import defaultdict

# mode = 'test'
mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

file_name = "test_input.txt" if mode == "test" else "puzzle_input.txt"
with open(file_name) as f:
    data = f.read().split('\n')


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)


symbols = [
    Point(x, y)
    for y, line in enumerate(data)
    for x, character in enumerate(line)
    if not character.isdigit() and character != "."
]

surroundings = (
    Point(-1, -1),  # NW
    Point(0, -1),  # N
    Point(1, -1),  # NE
    Point(-1, 0),  # W
    Point(1, 0),  # E
    Point(-1, 1),  # SW
    Point(0, 1),  # S
    Point(1, 1),  # SE
)

symbols_with_numeric_neighbours = defaultdict(list)
symbol_neighbour_gears = defaultdict(list)

for point in symbols:
    symbols_with_numeric_neighbours[point].extend(
        [
            point + offset_point
            for offset_point in surroundings
            if data[point.y + offset_point.y][point.x + offset_point.x].isdigit()
        ]
    )


def solve_q1():
    parts = []
    visited = set()
    max_chars_in_line = len(data[0])

    for point, neighbours in symbols_with_numeric_neighbours.items():
        for point in neighbours:
            if point in visited:
                continue

            start_x, end_x = point.x, point.x

            while data[point.y][start_x].isdigit():
                visited.add(Point(start_x, point.y))
                start_x += -1

            while end_x < max_chars_in_line and data[point.y][end_x].isdigit():
                visited.add(Point(end_x, point.y))
                end_x += 1

            num = int(data[point.y][start_x+1: end_x])
            parts.append(num)
            symbol_neighbour_gears[point].append(num)
    if mode == 'test':
        assert sum(parts) == 4361
    else:
        assert sum(parts) == 539713
    return sum(parts)


def solve_q2():
    stars = [p for p in symbols if data[p.x][p.y] == "*"]

    gears = [
        [g for g in symbol_neighbour_gears[point]]
        for point in stars
        if len(symbol_neighbour_gears[point]) == 2
    ]
    power_sum = sum(list(map(math.prod, gears)))

    if mode == 'test':
        assert power_sum == 84159075, power_sum
    else:
        assert power_sum == 84159075, power_sum

    return power_sum


print(f"Q1: {solve_q1()}")
print(f"Q2: {solve_q2()}")
