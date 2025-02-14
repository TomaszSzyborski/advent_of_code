import json
import logging
from multiprocessing import Pool

description = """--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
"""


def parse(data: str):
    data = data.splitlines()
    obstacles = set()
    start = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                obstacles.add((x, y))
            elif char == "^":
                start = (x, y)
    width = len(data[0])
    height = len(data)
    return obstacles, start, width, height


def get_guard_positions(obstacles, start, width, height):
    visited = set()
    x, y = start
    direction = -1j

    while 0 <= x < width and 0 <= y < height:
        visited.add((x, y))
        next_pos = (x + direction.real, y + direction.imag)
        while next_pos in obstacles:
            # turn right - toggle through 4 positions by multiplying by imaginary part
            direction = direction * 1j
            next_pos = (x + direction.real, y + direction.imag)
        x, y = next_pos

    return visited


def is_loop(obstacles, start, width, height):
    visited = set()
    x, y = start
    direction = -1j

    while 0 <= x < width and 0 <= y < height:
        if ((x, y), direction) in visited:
            return True
        visited.add(((x, y), direction))
        next_pos = (x + direction.real, y + direction.imag)
        while next_pos in obstacles:
            # turn right
            direction = direction * 1j
            next_pos = (x + direction.real, y + direction.imag)
        x, y = next_pos

    return False


def part1(obstacles, start, width, height):
    return len(get_guard_positions(obstacles, start, width, height))


def part2(obstacles, start, width, height):
    guard_positions = get_guard_positions(obstacles, start, width, height)
    guard_positions.remove(start)

    good_positions = set()
    i = 0
    for position in guard_positions:
        i += 1
        if i % 100 == 0:
            print(".", end="")
        obstacles.add(position)
        if is_loop(obstacles, start, width, height):
            good_positions.add(position)
        obstacles.remove(position)
    print()

    return len(good_positions)


with open("part_1_test_input.txt") as f:
    data = f.read().strip()
obstacles, start, width, height = parse(data)
print("Part1:", part1(obstacles, start, width, height))  # 41
assert part1(obstacles, start, width, height) == 41
print("Part2:", part2(obstacles, start, width, height))
assert part2(obstacles, start, width, height) == 6

with open("puzzle_input.txt") as f:
    data = f.read().strip()
obstacles, start, width, height = parse(data)
part_1_answer = part1(obstacles, start, width, height)

print("Part1:", part_1_answer)
assert part_1_answer == 5177, f"Expected 5177, got {part_1_answer}"
part_2_answer = part2(obstacles, start, width, height)
print("Part2:", part_2_answer)
assert part_2_answer == 1686, f"Expected 1686, got {part_2_answer}"
