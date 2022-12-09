"""
--- Day 9: Rope Bridge ---
This rope bridge creaks as you walk along it.
You aren't sure how old it is, or whether it can even support your weight.
It seems to support the Elves just fine, though.
The bridge spans a gorge which was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist.
You decide to distract yourself by modeling rope physics;
maybe you can even figure out where not to step.

Consider a rope with a knot at each end;
these knots mark the head and the tail of the rope.
If the head moves far enough away from the tail, the tail is pulled toward the head.

Due to nebulous reasoning involving Planck lengths,
you should be able to model the positions of the knots on a two-dimensional grid.
Then, by following a hypothetical series of motions (your puzzle input)
 for the head, you can determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short;
in fact, the head (H) and tail (T) must always be touching
(diagonally adjacent and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...
If the head is ever two steps directly up, down, left, or right from the tail,
the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...
Otherwise, if the head and tail aren't touching and aren't in the same row or column,
the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....
You just need to work out where the tail goes as the head follows a series of motions.
Assume the head and the tail both start at the same position, overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
This series of motions moves the head right four steps,
then up four steps, then left three steps, then down one step, and so on.
After each step, you'll need to update the position of the tail
if the step means the head is no longer adjacent to the tail.
Visually, these motions occur as follows (s marks the starting position as a reference point):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....
After simulating the rope,
you can count up all of the positions the tail visited at least once.
In this diagram, s again marks the starting position (which the tail also visited)
and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..
So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions.
How many positions does the tail of the rope visit at least once?
"""
from itertools import combinations_with_replacement, permutations

from pytest import mark

from day_9_part_one import read_data_file, Direction, Rope, Point, process_data_to_planck_rope_movement, PlanckMovement


@mark.parametrize("move", [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
def test_move(move):
    rope = Rope()
    rope.move(move)
    assert rope.tail_history == [Point(0, 0), Point(0, 0)]
    assert rope.calculate_tail_visited_spaces() == 1


@mark.parametrize("moves, expected_history",
                  [((Direction.UP, Direction.UP), [Point(0, 0), Point(0, 0), Point(0, 1)]),
                   ((Direction.DOWN, Direction.DOWN), [Point(0, 0), Point(0, 0), Point(0, -1)]),
                   ((Direction.LEFT, Direction.LEFT), [Point(0, 0), Point(0, 0), Point(-1, 0)]),
                   ((Direction.RIGHT, Direction.RIGHT), [Point(0, 0), Point(0, 0), Point(1, 0)]),
                   ])
def test_move_with_rope_pull_in_line(moves, expected_history):
    rope = Rope()
    for move in moves:
        rope.move(move)
    assert rope.tail_history == expected_history
    assert rope.calculate_tail_visited_spaces() == 2


@mark.parametrize("moves, expected_history",
                  [((Direction.UP, Direction.LEFT), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.UP, Direction.RIGHT), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.DOWN, Direction.LEFT), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.DOWN, Direction.RIGHT), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.LEFT, Direction.UP), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.LEFT, Direction.DOWN), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.RIGHT, Direction.UP), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.RIGHT, Direction.DOWN), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ])
def test_move_with_rope_pull_diagonally(moves, expected_history):
    rope = Rope()
    for move in moves:
        rope.move(move)
    assert rope.tail_history == expected_history
    assert rope.calculate_tail_visited_spaces() == 1


@mark.parametrize("moves, expected_history",
                  [((Direction.UP, Direction.DOWN), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.DOWN, Direction.UP), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.RIGHT, Direction.LEFT), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ((Direction.LEFT, Direction.RIGHT), [Point(0, 0), Point(0, 0), Point(0, 0)]),
                   ])
def test_move_with_rope_pull_to_direction_and_back(moves, expected_history):
    rope = Rope()
    for move in moves:
        rope.move(move)
    assert rope.tail_history == expected_history
    assert rope.calculate_tail_visited_spaces() == 1


@mark.parametrize("moves, expected_tail_position",
                  [
                      ((Direction.UP, Direction.LEFT, Direction.UP, Direction.LEFT), Point(-1, 1)),
                      ((Direction.DOWN, Direction.LEFT, Direction.DOWN, Direction.LEFT), Point(-1, -1)),
                      ((Direction.UP, Direction.RIGHT, Direction.UP, Direction.RIGHT), Point(1, 1)),
                      ((Direction.DOWN, Direction.RIGHT, Direction.DOWN, Direction.RIGHT), Point(1, -1))
                  ])
def test_move_with_rope_pull_double_diagonal(moves, expected_tail_position):
    rope = Rope()
    for move in moves:
        rope.move(move)
    assert rope.tail_history[-1] == expected_tail_position
    assert rope.calculate_tail_visited_spaces() == 3


def combinations_for_chess_knight():
    three_moves_combinations = combinations_with_replacement(
        [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT], 3
    )
    two_directions_moves = list(filter(lambda it: len(set(it)) == 2, three_moves_combinations))
    opposite_directions = [{Direction.UP, Direction.DOWN}, {Direction.LEFT, Direction.RIGHT}]
    knight_moves = filter(lambda it: set(it) not in opposite_directions, two_directions_moves)
    moves = []
    for direction_names in knight_moves:
        same_spot_moves = permutations([Direction[d.name] for d in direction_names])
        for move in same_spot_moves:
            moves.append(move)
    return moves


@mark.parametrize("moves",
                  [*combinations_for_chess_knight()])
def test_move_with_rope_pull_like_chess_knight(moves):
    rope = Rope()
    for move in moves:
        rope.move(move)
    assert rope.calculate_tail_visited_spaces() == 2


def test_raw_data_processing():
    raw_data = read_data_file("test_input.txt")
    movements = process_data_to_planck_rope_movement(raw_data)
    assert len(movements) == 8
    assert movements[0] == PlanckMovement(direction=Direction.RIGHT, multiplier=4)
    assert movements[1] == PlanckMovement(direction=Direction.UP, multiplier=4)
    assert movements[2] == PlanckMovement(direction=Direction.LEFT, multiplier=3)
    assert movements[3] == PlanckMovement(direction=Direction.DOWN, multiplier=1)
    assert movements[4] == PlanckMovement(direction=Direction.RIGHT, multiplier=4)
    assert movements[5] == PlanckMovement(direction=Direction.DOWN, multiplier=1)
    assert movements[6] == PlanckMovement(direction=Direction.LEFT, multiplier=5)
    assert movements[7] == PlanckMovement(direction=Direction.RIGHT, multiplier=2)


def test_raw_data_processing_checking_outcomes():
    raw_data = read_data_file("test_input.txt")
    movements = process_data_to_planck_rope_movement(raw_data)

    rope = Rope()
    assert len(movements) == 8
    assert movements[0] == PlanckMovement(direction=Direction.RIGHT, multiplier=4)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    """
    S##TH
    """
    assert rope.tail_history == [Point(0, 0), Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]
    assert rope.calculate_tail_visited_spaces() == 4
    assert movements[1] == PlanckMovement(direction=Direction.UP, multiplier=4)
    rope.move(Direction.UP)
    rope.move(Direction.UP)
    rope.move(Direction.UP)
    rope.move(Direction.UP)
    """
    ....H
    ...T.
    ...#.
    ...#.
    S####
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3)]
    assert rope.calculate_tail_visited_spaces() == 7
    assert movements[2] == PlanckMovement(direction=Direction.LEFT, multiplier=3)
    rope.move(Direction.LEFT)
    rope.move(Direction.LEFT)
    rope.move(Direction.LEFT)
    """
    .H...
    ..T#.
    ...#.
    ...#.
    S####
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                                 Point(3, 3), Point(3, 3), Point(2, 3)]
    assert rope.calculate_tail_visited_spaces() == 8
    assert movements[3] == PlanckMovement(direction=Direction.DOWN, multiplier=1)
    rope.move(Direction.DOWN)
    """
    .....
    .HT#.
    ...#.
    ...#.
    S####
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                                 Point(3, 3), Point(3, 3), Point(2, 3),
                                 Point(2, 3)]
    assert rope.calculate_tail_visited_spaces() == 8
    assert movements[4] == PlanckMovement(direction=Direction.RIGHT, multiplier=4)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    """
    ......
    ..##TH
    ...#..
    ...#..
    S####.
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                                 Point(3, 3), Point(3, 3), Point(2, 3),
                                 Point(2, 3),
                                 Point(2, 3), Point(2, 3), Point(3, 3), Point(4, 3),
                                 ]
    assert rope.calculate_tail_visited_spaces() == 9

    assert movements[5] == PlanckMovement(direction=Direction.DOWN, multiplier=1)
    rope.move(Direction.DOWN)
    """
    ......
    ..##T.
    ...#.H
    ...#..
    S####.
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                                 Point(3, 3), Point(3, 3), Point(2, 3),
                                 Point(2, 3),
                                 Point(2, 3), Point(2, 3), Point(3, 3), Point(4, 3),
                                 Point(4, 3)
                                 ]
    assert rope.calculate_tail_visited_spaces() == 9
    assert movements[6] == PlanckMovement(direction=Direction.LEFT, multiplier=5)
    rope.move(Direction.LEFT)
    rope.move(Direction.LEFT)
    rope.move(Direction.LEFT)
    rope.move(Direction.LEFT)
    rope.move(Direction.LEFT)
    """
    ......
    .T###.
    H..#..
    ...#..
    S####.
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                                 Point(3, 3), Point(3, 3), Point(2, 3),
                                 Point(2, 3),
                                 Point(2, 3), Point(2, 3), Point(3, 3), Point(4, 3),
                                 Point(4, 3),
                                 Point(4, 3), Point(4, 3), Point(3, 3), Point(2, 3), Point(1, 3)
                                 ]
    assert rope.calculate_tail_visited_spaces() == 10
    assert movements[7] == PlanckMovement(direction=Direction.RIGHT, multiplier=2)
    rope.move(Direction.RIGHT)
    rope.move(Direction.RIGHT)
    """
    ......
    .T###.
    ..H#..
    ...#..
    S####.
    """
    assert rope.tail_history == [Point(0, 0),
                                 Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
                                 Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                                 Point(3, 3), Point(3, 3), Point(2, 3),
                                 Point(2, 3),
                                 Point(2, 3), Point(2, 3), Point(3, 3), Point(4, 3),
                                 Point(4, 3),
                                 Point(4, 3), Point(4, 3), Point(3, 3), Point(2, 3), Point(1, 3),
                                 Point(1, 3), Point(1, 3)
                                 ]

    assert rope.calculate_tail_visited_spaces() == 10


def test_rope_plank_distance_pull():
    raw_data = read_data_file("test_input.txt")
    movements = process_data_to_planck_rope_movement(raw_data)
    rope = Rope()
    for movement in movements:
        print(movement)
        for _ in range(movement.multiplier):
            rope.move(movement.direction)

    assert rope.calculate_tail_visited_spaces() == 13
