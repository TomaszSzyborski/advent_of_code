"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid.
The Elves explain that a previous expedition planted these trees as a reforestation effort.
Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden.
To do this, you need to count the number of trees that are visible
from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map
with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height,
where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it.
Only consider trees in the same row or column;
that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible -
since they are already on the edge, there are no trees to block the view.
In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top.
(It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible,
 there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible,
there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior,
a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""

from day_8_part_one import read_data_file, process_raw_data_to_grid, Grid, is_tree_visible


def test_tree_visibility():
    raw_data = read_data_file('test_input.txt')
    grid_of_trees = process_raw_data_to_grid(raw_data)
    forest = Grid(grid_of_trees)
    print()
    print(forest)
    visible_trees = 0
    visibility_matrix = []
    for row_index, tree_row in enumerate(forest.data):
        visibility_matrix.append([])
        for tree_index, tree in enumerate(tree_row):
            if row_index in [0, len(forest.data)] or tree_index in [0, len(forest.data[0])]:
                visible_trees += 1
                visibility_matrix[row_index].append(True)
                continue
            row_of_trees = forest.get_row_from_grid(row_index)
            column_of_trees = forest.get_column_from_grid(tree_index)
            from_left = is_tree_visible(tree_under_analysis=tree,
                                        line_of_trees=row_of_trees[:tree_index])
            from_right = is_tree_visible(tree_under_analysis=tree,
                                         line_of_trees=row_of_trees[tree_index + 1:])
            from_top = is_tree_visible(tree_under_analysis=tree,
                                       line_of_trees=column_of_trees[:row_index])
            from_bottom = is_tree_visible(tree_under_analysis=tree,
                                          line_of_trees=column_of_trees[row_index + 1:])
            if any([from_left, from_right, from_top, from_bottom]):
                visible_trees += 1
                visibility_matrix[row_index].append(True)
            else:
                visibility_matrix[row_index].append(False)

    print()
    for row in visibility_matrix:
        print(row)
    print(f"{visible_trees=}")
    assert visible_trees == 21

