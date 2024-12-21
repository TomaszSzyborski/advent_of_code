"""
--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
"""
import re
from part_1 import extract_mul_instructions, transform_extracted_tuples_to_int_tuples


def find_do_dont(data):
    """
    Find all do() and don't() in the data
    """
    do_dont = []
    for match in re.finditer(r'(do|don\'t)\(\)', data):
        do_dont.append((match.start(), match.group(1)))
    return do_dont


def calculate_valid_ranges_mul(data: str) -> list[tuple[int, int]]:
    start = 0
    do_dont = find_do_dont(data)
    valid = []
    valid.append((start, do_dont[0][0]))
    for i, instructions in enumerate(do_dont):
        index, instruction = instructions
        start = index
        if instruction == "don't":
            continue
        try:
            valid.append((start, do_dont[i+1][0]))
        except:
            valid.append((start, -1))
    return valid

def main():
    with open('input.txt') as f:
        data = f.read()
    valid_ranges = calculate_valid_ranges_mul(data)
    print(valid_ranges)
    final_data = []
    for ranges in valid_ranges:
        extracted_data = extract_mul_instructions(data[ranges[0]:ranges[1]])
        int_tuples = transform_extracted_tuples_to_int_tuples(extracted_data)
        final_data.extend(int_tuples)
    print(final_data)
    print(f"{sum(x * y for x, y in final_data)=}")

if __name__ == '__main__':
    main()

#184511516 too high
#2nd attempt 90044227