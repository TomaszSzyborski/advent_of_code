description = """--- Part Two ---
While The Historians begin working around the guard's patrol route, 
you borrow their fancy device and step outside the lab.
From the safety of a supply closet, 
you time travel through the last few months and record the nightly 
status of the lab's guard post on the walls of the closet.
Returning after what seems like only a few seconds to The Historians, 
they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. 
They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox,
The Historians would like to know all of the possible positions for such an obstruction.
The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions 
where a new obstruction would cause the guard to get stuck in a loop. 
The diagrams of these six situations use 
O to mark the new obstruction, 
| to show a position where the guard moves up/down,
- to show a position where the guard moves left/right, 
and + to show a position where the guard moves both up/down and left/right.

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
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. 
The important thing is having enough options that you can find one that minimizes time paradoxes,
and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction.
How many different positions could you choose for this obstruction?
"""
import pytest
from .part_2 import predict_route_size, GuardBlockedException
from .part_2 import put_obstacle, find_blockades


def test_blocked_guard_obstacle_placed_next_to_guard():
    """
    Option one, put a printing press next to the guard's starting position:
    Map with guard walking in loop:

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

    positions occupied during guard route:
    [[(6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4)], [(1, 4)], [(1, 5)], [(1, 6)], [(1, 7)], [(1, 8)], [(1, 8)]]
    """
    map_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#.O^.....",
        "........#.",
        "#.........",
        "......#..."
    ]
    map_input = [[char for char in line] for line in map_input]
    with pytest.raises(GuardBlockedException) as e_info:
        route_length, positions_occupied = predict_route_size(map_input)
    assert f"{e_info.value}" == "Guard blocked!"
    print(e_info.value.visited_positions)
    assert e_info.value.visited_positions == [[(6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4)],
                                              [(1, 4), (1, 5), (1, 6), (1, 7), (1, 8)],
                                              [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8)],
                                              [(6, 8), (6, 7), (6, 6), (6, 5), (6, 4)],
                                              [(6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4)]]

def test_find_blockades():
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
        "......#..."
    ]
    map_input = [[char for char in line] for line in map_input]
    blockades = find_blockades(map_input)
    assert blockades == 6


option_two = """
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
            """

option_three =  """
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
                """

option_four =   """
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
                """
option_five =   """
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
                """
option_six =    """
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
                """


import pytest
from .part_2 import predict_route_size, find_guard, move_guard


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
        "......#..."
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
        "......#..."
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
        "......#..."
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
        "......#..."
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
        "......#..."
    ]
    map_input = [[char for char in line] for line in map_input]

    assert find_guard(map_input) is None


def test_move_guard_when_guard_blocked():
    """
    Test the move_guard function when the guard is blocked.

    This test case checks if the move_guard function can correctly
    handle the situation when the guard is blocked by obstacles.
    """
    map_input_blocked = [
        "#####",
        "#^###",
        "#####"
    ]
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
        "......#..."
    ]
    map_input = [[char for char in line] for line in map_input]
    expected_visited_positions = 41
    assert predict_route_size(map_input) == (11, expected_visited_positions)


def test_predict_route_blocked():
    """
    Test the predict_route function when the guard is blocked.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    blocked by obstacles.
    """
    map_input_blocked = [
        "#####",
        "#^###",
        "#####"
    ]
    map_input_blocked = [[char for char in line] for line in map_input_blocked]
    expected_error_message = "Guard blocked!"
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
    map_input_open = [
        "..........",
        ".^........",
        ".........."
    ]
    map_input_open = [[char for char in line] for line in map_input_open]

    expected_visited_positions = 2
    assert predict_route_size(map_input_open) == (1 , expected_visited_positions)

def test_predict_route_open_down():
    """
    Test the predict_route function when the guard is facing down and has an open path below.

    This test case checks if the predict_route function can correctly
    predict the route of the guard in the map input when the guard is
    facing down and has an open path below.
    """
    map_input_open = [
        "..........",
        ".v........",
        ".........."
    ]
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
    map_input_open = [
        "..........",
        "..<.......",
        ".........."
    ]
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
    map_input_open = [
        "..........",
        "..>.......",
        ".........."
    ]
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
    map_input = [
        "..........",
        "..^.......",
        ".........."
    ]
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
    map_input_blocked = [
        "##########",
        "#.^......#",
        "##########"
    ]
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
    map_input = [
        "..#.......",
        "..^.......",
        ".........."
    ]
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
    map_input = [
        "..#.......",
        "..>#......",
        ".........."
    ]
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
    map_input = [
        "..#.......",
        "..v.......",
        "..#......."
    ]
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
    map_input = [
        "..........",
        ".#<.......",
        "..#......."
    ]
    map_input = [[char for char in line] for line in map_input]

    expected_guard_position = (1, 2)
    new_map, guard_position, guard_direction = move_guard(map_input)
    assert guard_position == expected_guard_position
    assert guard_direction == "^"
    expected_guard_position = (0, 2)
    new_map, guard_position, guard_direction = move_guard(new_map)
    assert guard_position == expected_guard_position
    assert guard_direction == "^"