"""
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
"""
import re

def extract_mul_instructions(data: str) -> list[tuple[str, str]]:
    """
    Extract valid mul(X,Y) instructions from the given data.

    Args:
        data (str): The corrupted memory data containing potential mul instructions.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the operands of each valid mul instruction.
    """
    # Define regex pattern to match valid mul(X,Y) instructions
    # Extract valid mul(X,Y) instructions using regex
    # pattern = r"mul\(\d+,\d+\)"
    # return re.findall(pattern, data)
    extracted = [(match.group(1), match.group(2)) for match in re.finditer(r"mul\((\d+),(\d+)\)", data)]
    return extracted

def transform_extracted_tuples_to_int_tuples(data: list[tuple[str, str]]) -> list[tuple[int, int]]:
    return  [(int(x), int(y)) for x, y in data]

def calculate_mul_sum(data):
    extracted_instructions = extract_mul_instructions(data)
    cleared_data = transform_extracted_tuples_to_int_tuples(extracted_instructions)
    return sum(x * y for x, y in cleared_data)


def main():
    # Read the input data from file
    with open("input.txt", "r") as file:
        data = file.read()

    # Calculate the sum of the results of valid mul instructions
    result = calculate_mul_sum(data)
    print(f"Sum of valid mul instructions: {result}")

if __name__ == "__main__":
    # import pytest
    # pytest.main([__file__])
    main()