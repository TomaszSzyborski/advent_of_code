"""
--- Part Two ---
Now, given the same instructions,
find the position of the first character that causes him to enter the basement (floor -1).
The first character in the instructions has position 1,
the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""
if __name__ == '__main__':
    with open("puzzle_input.txt") as f:
        steps = f.read().strip()

    floor_number = 0
    first_step_to_basement = 0
    for index, step in enumerate(steps, start=1):
        if step == "(":
            floor_number += 1
        elif step == ")":
            floor_number -= 1
        if floor_number < 0:
            first_step_to_basement = index
            break

    print(first_step_to_basement)
    #answer 1797