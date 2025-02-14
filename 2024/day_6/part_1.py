"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again,
this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518!
It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes,
and so it will be important to avoid anyone from 1518 while The Historians search for the Chief.
Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^
(to indicate the guard is currently facing up from the perspective of the map).
Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle
(in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area
(after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path.
Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""

import copy
import dataclasses


MOVEMENT: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def load_data(file_name: str) -> list[list[str]]:
    with open(file_name, "r") as file:
        lines = file.read().split("\n")
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

    exiting_up = (
        guard_position[0] == 0
        and guard_direction == "^"
        and MOVEMENT[guard_direction][0] == -1
    )
    exiting_left = (
        guard_position[1] == 0
        and guard_direction == "<"
        and MOVEMENT[guard_direction][1] == -1
    )
    exiting_down = (
        guard_position[0] == len(map_input) - 1
        and guard_direction == "v"
        and MOVEMENT[guard_direction][0] == 1
    )
    exiting_right = (
        guard_position[1] == len(map_input[0]) - 1
        and guard_direction == ">"
        and MOVEMENT[guard_direction][1] == 1
    )
    if any([exiting_right, exiting_down, exiting_left, exiting_up]):
        new_map[guard_position[0]][guard_position[1]] = "."
        guard_position = find_guard(new_map)
        return new_map, guard_position, guard_direction

    new_x = guard_position[0] + MOVEMENT[guard_direction][0]
    new_y = guard_position[1] + MOVEMENT[guard_direction][1]

    if new_map[new_x][new_y] == ".":
        new_map[guard_position[0]][guard_position[1]] = "."
        new_map[new_x][new_y] = guard_direction
    elif new_map[new_x][new_y] == "#":
        try:
            guard_direction = list(MOVEMENT.keys())[
                list((MOVEMENT.keys())).index(guard_direction) + 1
            ]
        except IndexError:
            guard_direction = list(MOVEMENT.keys())[0]
        new_map[guard_position[0]][guard_position[1]] = guard_direction
    else:
        raise NotImplementedError("That shouldn't happen...")
    guard_position = find_guard(new_map)
    return new_map, guard_position, guard_direction


def predict_route_size(map_input: list[list[str]]) -> int:
    guard_position = find_guard(map_input)
    positions_occupied = [guard_position]
    while find_guard(map_input) is not None:
        map_input, guard_position, guard_direction = move_guard(map_input)
        guard_position = find_guard(map_input)
        if guard_position is None:
            break
        positions_occupied.append(guard_position)
        if positions_occupied[-4:] == [guard_position for _ in range(4)]:
            raise Exception("Guard blocked")
    return len(set(positions_occupied))


def main():
    file_name = "puzzle_input.txt"
    data = load_data(file_name)
    result = predict_route_size(data)
    print(result)


if __name__ == "__main__":
    main()
    # first attempt 5177
