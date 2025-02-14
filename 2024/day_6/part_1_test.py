"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

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
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

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
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

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
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

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

import pytest
from .part_1 import predict_route_size, find_guard, move_guard


# find_guard tests


def test_find_guard_facing_up():
    """
    Test the find_guard function when the guard is facing up.

    This test case checks if the find_guard function can correctly
    identify the position of a guard marked with '^' in the map input.
    The expected position is returned as a tuple of (row, column).
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#...",
    ]
    map_input = [[char for char in line] for line in map_input]
    assert find_guard(map_input) == (6, 4)


def test_find_guard_facing_right():
    """
    Test the find_guard function when the guard is facing right.

    This test case checks if the find_guard function can correctly
    identify the position of a guard marked with '>' in the map input.
    The expected position is returned as a tuple of (row, column).
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#........",
        "........#.",
        "#......>..",
        "......#...",
    ]
    map_input = [[char for char in line] for line in map_input]

    assert find_guard(map_input) == (8, 7)


def test_find_guard_facing_down():
    """
    Test the find_guard function when the guard is facing down.

    This test case checks if the find_guard function can correctly
    identify the position of a guard marked with 'v' in the map input.
    The expected position is returned as a tuple of (row, column).
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#........",
        "........#.",
        "#......v..",
        "......#...",
    ]
    map_input = [[char for char in line] for line in map_input]

    assert find_guard(map_input) == (8, 7)


def test_find_guard_facing_left():
    """
    Test the find_guard function when the guard is facing left.

    This test case checks if the find_guard function can correctly
    identify the position of a guard marked with '<' in the map input.
    The expected position is returned as a tuple of (row, column).
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#........",
        "........#.",
        "#......<..",
        "......#...",
    ]
    map_input = [[char for char in line] for line in map_input]
    assert find_guard(map_input) == (8, 7)


def test_find_guard_when_no_guard():
    """
    Test the find_guard function when there is no guard in the map input.

    This test case checks if the find_guard function can correctly
    identify the absence of a guard in the map input and return None.
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#........",
        "........#.",
        "#.........",
        "......#...",
    ]
    map_input = [[char for char in line] for line in map_input]

    assert find_guard(map_input) is None


def test_move_guard_when_guard_blocked():
    """
    Test the move_guard function when the guard is blocked.

    This test case checks if the move_guard function can correctly
    handle the situation when the guard is blocked by obstacles.
    """
    map_input_blocked = ["#####", "#^###", "#####"]
    map_input_blocked = [[char for char in line] for line in map_input_blocked]
    move_guard(map_input_blocked)
    move_guard(map_input_blocked)
    move_guard(map_input_blocked)
    move_guard(map_input_blocked)


def test_predict_route_size_happy_path():
    """
    Test the predict_route function.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input.
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#...",
    ]
    map_input = [[char for char in line] for line in map_input]
    expected_visited_positions = 41
    assert predict_route_size(map_input) == expected_visited_positions


def test_predict_route_blocked():
    """
    Test the predict_route function when the guard is blocked.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    blocked by obstacles.
    """
    map_input_blocked = ["#####", "#^###", "#####"]
    map_input_blocked = [[char for char in line] for line in map_input_blocked]
    expected_error_message = "Guard blocked"
    with pytest.raises(Exception) as e_info:
        predict_route_size(map_input_blocked)
    assert f"{e_info.value}" == expected_error_message


def test_predict_route_open_up():
    """
    Test the predict_route function when the guard is facing up and has an open path above.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    facing up and has an open path above.
    """
    map_input_open = ["..........", ".^........", ".........."]
    map_input_open = [[char for char in line] for line in map_input_open]

    expected_visited_positions = 2
    assert predict_route_size(map_input_open) == expected_visited_positions


def test_predict_route_open_down():
    """
    Test the predict_route function when the guard is facing down and has an open path below.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    facing down and has an open path below.
    """
    map_input_open = ["..........", ".v........", ".........."]
    map_input_open = [[char for char in line] for line in map_input_open]
    expected_visited_positions = 2

    assert predict_route_size(map_input_open) == expected_visited_positions


def test_predict_route_open_left():
    """
    Test the predict_route function when the guard is facing left and has an open path left.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    facing left and has an open path left.
    """
    map_input_open = ["..........", "..<.......", ".........."]
    map_input_open = [[char for char in line] for line in map_input_open]
    expected_visited_positions = 3

    assert predict_route_size(map_input_open) == expected_visited_positions


def test_predict_route_open_right():
    """
    Test the predict_route function when the guard is facing right and has an open path to the right.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    facing right and has an open path to the right.
    """
    map_input_open = ["..........", "..>.......", ".........."]
    map_input_open = [[char for char in line] for line in map_input_open]

    expected_visited_positions = 8
    assert predict_route_size(map_input_open) == expected_visited_positions


# move_guard tests
def test_move_guard():
    """
    Test the move_guard function.

    This test case checks if the move_guard function can correctly
    move the guard in the map input based on the guard's position and
    the direction given.
    """
    map_input = ["..........", "..^.......", ".........."]
    map_input = [[char for char in line] for line in map_input]

    expected_guard_position = (0, 2)
    new_map, guard_position, guard_direction = move_guard(map_input)
    assert guard_position == expected_guard_position
    assert guard_direction == "^"


def test_move_guard_blocked():
    """
    Test the move_guard function when the guard is blocked.

    This test case checks if the move_guard function can correctly
    handle the case where the guard is blocked by checking if the
    guard's position is the same before and after calling the function.
    """
    map_input_blocked = ["##########", "#.^......#", "##########"]
    map_input_blocked = [[char for char in line] for line in map_input_blocked]
    new_map, guard_position, guard_direction = move_guard(map_input_blocked)
    assert guard_position == (1, 2)
    assert guard_direction == ">"


def test_guard_turns_when_facing_up():
    """
    Test the move_guard function.

    This test case checks if the move_guard function can correctly
    move the guard in the map input based on the guard's position and
    the direction given.
    """
    map_input = ["..#.......", "..^.......", ".........."]
    map_input = [[char for char in line] for line in map_input]

    expected_guard_position = (1, 2)
    new_map, guard_position, guard_direction = move_guard(map_input)
    assert guard_position == expected_guard_position
    assert guard_direction == ">"
    expected_guard_position = (1, 3)
    new_map, guard_position, guard_direction = move_guard(new_map)
    assert guard_position == expected_guard_position
    assert guard_direction == ">"


def test_guard_turns_when_facing_right():
    """
    Test the move_guard function.

    This test case checks if the move_guard function can correctly
    move the guard in the map input based on the guard's position and
    the direction given.
    """
    map_input = ["..#.......", "..>#......", ".........."]
    map_input = [[char for char in line] for line in map_input]

    expected_guard_position = (1, 2)
    new_map, guard_position, guard_direction = move_guard(map_input)
    assert guard_position == expected_guard_position
    assert guard_direction == "v"
    expected_guard_position = (2, 2)
    new_map, guard_position, guard_direction = move_guard(new_map)
    assert guard_position == expected_guard_position
    assert guard_direction == "v"


def test_guard_turns_when_facing_down():
    """
    Test the move_guard function.

    This test case checks if the move_guard function can correctly
    move the guard in the map input based on the guard's position and
    the direction given.
    """
    map_input = ["..#.......", "..v.......", "..#......."]
    map_input = [[char for char in line] for line in map_input]

    expected_guard_position = (1, 2)
    new_map, guard_position, guard_direction = move_guard(map_input)
    assert guard_position == expected_guard_position
    assert guard_direction == "<"
    expected_guard_position = (1, 1)
    new_map, guard_position, guard_direction = move_guard(new_map)
    assert guard_position == expected_guard_position
    assert guard_direction == "<"


def test_guard_turns_when_facing_left():
    """
    Test the move_guard function.

    This test case checks if the move_guard function can correctly
    move the guard in the map input based on the guard's position and
    the direction given.
    """
    map_input = ["..........", ".#<.......", "..#......."]
    map_input = [[char for char in line] for line in map_input]

    expected_guard_position = (1, 2)
    new_map, guard_position, guard_direction = move_guard(map_input)
    assert guard_position == expected_guard_position
    assert guard_direction == "^"
    expected_guard_position = (0, 2)
    new_map, guard_position, guard_direction = move_guard(new_map)
    assert guard_position == expected_guard_position
    assert guard_direction == "^"


if __name__ == "__main__":
    pytest.main()
