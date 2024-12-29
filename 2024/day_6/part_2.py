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
import copy

class GuardBlockedException(Exception):
    def __init__(self, visited_positions: list[list[tuple[int, int]]]) -> None:
        super().__init__("Guard blocked!")
        self.visited_positions = visited_positions

MOVEMENT: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}


def load_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as file:
        lines = file.read().split('\n')
        data_map = [[char for char in line] for line in lines]
    return data_map


def find_guard(map_input: list[list[str]]) -> tuple[int, int] | None:
    for y in range(len(map_input)):
        for x in range(len(map_input[y])):
            if map_input[y][x] in MOVEMENT.keys():
                return y, x
    return None



def move_guard(map_input: list[list[str]]) -> (list[str], tuple[int, int], str):
    new_map = copy.deepcopy(map_input)
    guard_position = find_guard(map_input)
    guard_direction = new_map[guard_position[0]][guard_position[1]]

    exiting_up = guard_position[0] == 0 and guard_direction == "^" and MOVEMENT[guard_direction][0] == -1
    exiting_left = guard_position[1] == 0 and guard_direction == "<" and MOVEMENT[guard_direction][1] == -1
    exiting_down = guard_position[0] == len(map_input) - 1 and guard_direction == "v" and MOVEMENT[guard_direction][0] == 1
    exiting_right = guard_position[1] == len(map_input[0]) - 1 and guard_direction == ">" and MOVEMENT[guard_direction][1] == 1
    if any([exiting_right, exiting_down, exiting_left, exiting_up]):
        new_map[guard_position[0]][guard_position[1]] = "."
        guard_position = find_guard(new_map)
        return new_map, guard_position, guard_direction

    new_x = guard_position[0] + MOVEMENT[guard_direction][0]
    new_y = guard_position[1] + MOVEMENT[guard_direction][1]


    if new_map[new_x][new_y] == ".":
        new_map[guard_position[0]][guard_position[1]] = "."
        new_map[new_x][new_y] = guard_direction
    elif new_map[new_x][new_y] in ["#", "O"]:
        try:
            guard_direction = list(MOVEMENT.keys())[list((MOVEMENT.keys())).index(guard_direction) + 1]
        except IndexError:
            guard_direction =  list(MOVEMENT.keys())[0]
        new_map[guard_position[0]][guard_position[1]] = guard_direction
    else:
        pretty_map = '\n'.join([''.join(line) for line in new_map])
        raise NotImplementedError(f"That shouldn't have happened - has my guard seen something unexpected>\n {pretty_map}")
    guard_position = find_guard(new_map)
    return new_map, guard_position, guard_direction

def predict_route_size(map_input: list[list[str]]) -> tuple[int, list[list[tuple[int, int]]]]:
    guard_position = find_guard(map_input)
    positions_occupied = [[guard_position]]
    unique_positions_occupied_length = 0

    while find_guard(map_input) is not None:
        previous_guard_direction = map_input[guard_position[0]][guard_position[1]]
        map_input, guard_position, guard_direction = move_guard(map_input)
        guard_position = find_guard(map_input)
        if guard_position is None:
            break
        if guard_direction != previous_guard_direction:
            positions_occupied.append([])
        positions_occupied[-1].append(guard_position)
        unique_positions_occupied_length = len(set(tuple([tuple(p) for p in positions_occupied])))

        if len(positions_occupied) != unique_positions_occupied_length:
            raise GuardBlockedException(positions_occupied)
    return unique_positions_occupied_length, positions_occupied

def put_obstacle(map_input: list[list[str]], position: tuple[int, int]) -> tuple[bool, list[list[str]]]:
    new_map = copy.deepcopy(map_input)
    changed = False
    if new_map[position[0]][position[1]] == ".":
        new_map[position[0]][position[1]] = "O"
        changed = True
    return changed, new_map

def check_positions(positions, map_input):
    blockades = 0
    for number, position in enumerate(positions, start=1):
        try:
            changed, new_map = put_obstacle(map_input, position)
            if changed:
                predict_route_size(new_map)
        except GuardBlockedException:
            blockades += 1
    return blockades


def find_blockades(map_input: list[list[str]]) -> int:
    """
    This function takes a list of lists of strings representing a map and returns the number of possible blockades.
    A blockade is a position on the map that, if an obstacle is placed there, will cause the guard to loop.

    The function first calculates the number of unique positions that the guard visits in their normal patrol path.
    Then, for each of the positions that the guard visits, it tries adding an obstacle at that position and checks if the guard becomes stuck in a loop.
    If the guard does become stuck, then the position is counted as a blockade.

    The function returns the total number of blockades found.
    """
    blockades = 0
    unique_positions_occupied_length, positions_occupied = predict_route_size(map_input)
    # positions = [s for p in positions_occupied for s in p[1:]]
    # print(f"Searching potential {positions=}")

    with Pool(8) as p:
        results = p.starmap(check_positions, [(p, map_input) for p in positions_occupied])
    return sum(results)

def main():
    file_name = "puzzle_input.txt"
    data = load_data(file_name)
    blockades = find_blockades(data)
    print(blockades)

if __name__ == '__main__':
    main()
