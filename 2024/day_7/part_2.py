"""
--- Day 7: Bridge Repair ---
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line;
it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules.
Furthermore, numbers in the equations cannot be rearranged.
Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

"""
import dataclasses
import itertools
from functools import reduce
from itertools import product, zip_longest
from time import perf_counter


@dataclasses.dataclass
class EquationData:
    result: int
    values: list[int]
    operators: list[tuple] = dataclasses.field(init=False, default=None, repr=False)

    def __post_init__(self):
        possible_operators = len(self.values) - 1
        self.operators = list(product(["+", "*", "||"], repeat=possible_operators))

    def possible_equations(self):
        to_be_evaluated = ""
        for operator_entries in self.operators:
            for value, operator in zip(self.values, operator_entries):
                to_be_evaluated += f" {value} {operator} "
            to_be_evaluated += f"{self.values[-1]}"
            to_be_evaluated += ","
        # print(to_be_evaluated)
        return to_be_evaluated


def iterate_over_equation(equation: str):
    equation = list(filter(lambda x: x if x else False, equation.split()))

    while len(equation) > 1:
        eq = equation[:3]
        if "||" in eq:
            result = f"{eq[0].strip()}{eq[2].strip()}"
            equation = [result] + equation[3:]
        else:
            s = f"{''.join(eq)}"
            result = eval(s)
            equation = [f"{result}"] + equation[3:]
    if equation:
        return int(equation[0])
    else:
        return 0


def prepare_data(file_name: str):
    with open(file_name) as f:
        data = f.read().split('\n')

    prepared_data = []
    for line in data:
        equation_result, numbers = line.split(":")
        equation = EquationData(int(equation_result), [int(i) for i in numbers.split()])
        prepared_data.append(equation)
    return prepared_data


def check(file_name):
    prepared_data = prepare_data(file_name)
    results = []
    for i, data_point in enumerate(prepared_data):
        print(f"Processing {i} of {data_point}...", end ="")
        start = perf_counter()
        eq = data_point.possible_equations().split(",")
        for peq in eq:
            it_result = iterate_over_equation(peq)
            if data_point.result == it_result:
                results.append(data_point.result)
                break # for part 2
        end = perf_counter()
        print(f"took {((end - start)* 1000):.2f} milliseconds")
    return sum(results) # for part 2


if __name__ == '__main__':
    actual_test_part_2 = check("part_1_test_input.txt")
    assert actual_test_part_2 == 11387, f"Was {actual_test_part_2}"
    print(f"Part 2 test: {actual_test_part_2}")

    actual_part_2 = check("puzzle_input.txt")
    print(f"Part 2: {actual_part_2}")
    assert actual_part_2 == 945341732469724 , f"Was {actual_part_2}"
