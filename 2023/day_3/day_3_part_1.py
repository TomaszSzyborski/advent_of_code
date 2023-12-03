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

# mode = 'test'
mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

file_name = "test_input.txt" if mode == "test" else "puzzle_input.txt"
with open(file_name) as f:
    data = f.read().split('\n')


def get_numbers_from(text: str, reverse=False) -> str | None:
    numbers = ""
    for letter in text:
        if letter.isdigit():
            numbers += letter
        else:
            break
    return numbers[::-1] if reverse else numbers


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)


def find_symbols(lines: list[str]) -> list[Point]:
    symbols_placement: list[Point] = []
    for line_index, line in enumerate(lines):
        for symbol_index, character in enumerate(line):
            if character not in f"{string.digits}.":
                symbols_placement.append(Point(symbol_index, line_index))
    logging.debug(symbols_placement)
    return symbols_placement


def get_symbol_from_map(map: list[str], point: Point, offset_point: Point = Point(0, 0)):
    logging.debug(f"{map=}")
    logging.debug(f"{point=}")
    logging.debug(f"{offset_point=}")
    check_point = point + offset_point
    if any([check_point.x < 0,
            check_point.x > len(map[0]),
            check_point.y < 0,
            check_point.y > len(map),
            ]):
        raise ValueError("Point outside of the map")

    check_point_value = map[check_point.y][check_point.x]
    logging.debug(f"{check_point_value=}")
    return check_point_value


def check_for_numbers(map: list[str], point: Point, offset_point: Point):
    try:
        check_point_value = get_symbol_from_map(map, point, offset_point)
        logging.debug(f"{check_point_value=}: {check_point_value.isnumeric()=}")
        return check_point_value.isnumeric()
    except ValueError:
        return False


def get_chunk_from_map(map: list[str], point: Point, offset_point: Point, max_size_of_data_chunk: int,
                       direction: str = None):
    selected_line = map[point.y + offset_point.y]
    logging.info(f"{selected_line}")
    logging.info(f"{point.x=} {offset_point.x=}")
    if direction == "left":
        selected_points = selected_line[point.x - max_size_of_data_chunk: point.x + 1]
    elif direction == "right":
        selected_points = selected_line[point.x: point.x + max_size_of_data_chunk+1]
    else:
        selected_points = [selected_line[point.x + offset_point.x]]
    logging.info(f"{direction} => {selected_points=}")
    numeric_value = int(''.join([s for s in selected_points if s.isnumeric()]))
    logging.info(f"{direction} => {numeric_value=}")
    return numeric_value


def calculate_result(data: list[str]):
    max_number_size = 3
    symbol_placement = find_symbols(data)
    parts = []
    for i, symbol in enumerate(symbol_placement):
        logging.info(f"{i} {symbol} {get_symbol_from_map(data, symbol, Point(0, 0))}")
        left_up = check_for_numbers(data, symbol, Point(-1, -1))  # LEFT UP
        mid_up = check_for_numbers(data, symbol, Point(0, -1))  # STILL UP
        right_up = check_for_numbers(data, symbol, Point(1, -1))  # RIGHT UP
        if left_up and not mid_up:
            parts.append(get_chunk_from_map(data, symbol, Point(-1, -1), max_number_size, "left"))
        if left_up and mid_up and not right_up:
            parts.append(get_chunk_from_map(data, symbol, Point(0, -1), max_number_size, "left"))
        if left_up and mid_up and right_up:
            a = get_chunk_from_map(data, symbol, Point(-1, -1), 1)
            b = get_chunk_from_map(data, symbol, Point(0, -1), 1)
            c = get_chunk_from_map(data, symbol, Point(1, -1), 1)
            logging.info(f"MID TOP {int(f'{a}{b}{c}')}")
            parts.append(int(f"{a}{b}{c}"))
        if not left_up and mid_up and right_up:
            parts.append(get_chunk_from_map(data, symbol, Point(0, -1), max_number_size, "right"))
        if not left_up and not mid_up and right_up:
            parts.append(get_chunk_from_map(data, symbol, Point(1, -1), max_number_size, "right"))

        left = check_for_numbers(data, symbol, Point(-1, 0))  # LEFT STILL
        if left:
            parts.append(get_chunk_from_map(data, symbol, Point(-1, 0), max_number_size, "left"))
        left_down = check_for_numbers(data, symbol, Point(-1, 1))  # LEFT DOWN
        mid_down = check_for_numbers(data, symbol, Point(0, 1))  # STILL DOWN
        right_down = check_for_numbers(data, symbol, Point(1, 1))  # RIGHT DOWN
        if left_down and not mid_down:
            parts.append(get_chunk_from_map(data, symbol, Point(-1, 1), max_number_size, "left"))
        if left_down and mid_down and not right_down:
            parts.append(get_chunk_from_map(data, symbol, Point(0, 1), max_number_size, "left"))
        if left_down and mid_down and right_down:
            a = get_chunk_from_map(data, symbol, Point(-1, 1), 1)
            b = get_chunk_from_map(data, symbol, Point(0, 1), 1)
            c = get_chunk_from_map(data, symbol, Point(1, 1), 1)
            parts.append(int(f"{a}{b}{c}"))
        if not left_down and mid_down and right_down:
            parts.append(get_chunk_from_map(data, symbol, Point(0, 1), max_number_size, "right"))
        if not left_down and not mid_down and right_down:
            parts.append(get_chunk_from_map(data, symbol, Point(1, 1), max_number_size, "right"))

        right = check_for_numbers(data, symbol, Point(1, 0))  # RIGHT STILL
        if right:
            parts.append(get_chunk_from_map(data, symbol, Point(1, 0), max_number_size, "right"))

    logging.debug(f"{parts=}")
    return sum(parts)


if __name__ == '__main__':
    result = calculate_result(data)
    print(result)
    if mode == 'test':
        assert result == 4361, f"{result=}"
    else:
        assert result == 444598, f"{result=}" ## 444598 is too small
        # 456506 - źle
        # 533476 źle