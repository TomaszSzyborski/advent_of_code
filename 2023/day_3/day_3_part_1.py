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
import re
from enum import StrEnum
from typing import Self

mode = 'test'
# mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

file_name = "test_input.txt" if mode == "test" else "puzzle_input.txt"
with open(file_name) as f:
    data = f.read().split('\n')


@dataclass
class Point:
    x: int
    y: int


def find_symbols(lines: list[str]) -> list[Point]:
    symbols_placement: list[Point] = []
    for line_index, line in enumerate(lines):
        for symbol_index, character in enumerate(line):
            if character not in f"{string.digits}.":
                symbols_placement.append(Point(symbol_index, line_index))
    logging.debug(symbols_placement)
    return symbols_placement


def check_for_numbers(map: list[str], point: Point, x_offset: int, y_offset: int):
    check_x = point.x + x_offset
    check_y = point.y + y_offset
    logging.debug(f"{map=}")
    logging.debug(f"{point=}")
    logging.debug(f"{map[check_y][check_x]=}")

    character = map[check_y][check_x]
    return character.isnumeric()

def calculate_result(data):
    symbol_placement = find_symbols(data)
    for symbol in symbol_placement:
        check_for_numbers(data, symbol, -1, -1)
        check_for_numbers(data, symbol, -1, 0)
        check_for_numbers(data, symbol, -1, 1)
        check_for_numbers(data, symbol, 0, 1)
        check_for_numbers(data, symbol, 0, -1)
        check_for_numbers(data, symbol, 1, -1)
        check_for_numbers(data, symbol, 1, 0)
        check_for_numbers(data, symbol, 1, 1)

    return 0


if __name__ == '__main__':
    result = calculate_result(data)
    assert result == 4361, f"{result=}"
