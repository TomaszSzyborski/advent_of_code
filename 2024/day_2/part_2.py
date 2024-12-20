"""
--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems
tolerate a single bad level in what would otherwise be a safe report.
It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level
from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports.
How many reports are now safe?
"""
def is_report_safe_with_problem_dampener(numbers: list[int]) -> bool:
    """
    Given a list of numbers, returns True if the report is safe according to the rules
    of Day 2 Part 2 of the Advent of Code, and False otherwise.

    The rules for safety are as follows:

    1. The levels in a report must be distinct.
    2. The levels in a report must be strictly increasing or strictly decreasing.
    3. Adjacent levels in a report must not have differences of more than 3.

    The Problem Dampener allows for a single bad level in an unsafe report
    to be removed to make the report safe. It's like the bad level never happened!
    """
    increasing = lambda n: all(1 <= b - a <= 3 for a, b in zip(n, n[1:]))
    decreasing = lambda n: all(1 <= a - b <= 3 for a, b in zip(n, n[1:]))
    if increasing(numbers) or decreasing(numbers):
        return True

    new_numbers = numbers.copy()
    for i in range(0, len(numbers)):
        chunked = new_numbers[:i] + new_numbers[i+1:]
        if increasing(chunked) or decreasing(chunked):
            return True
    else:
        return False

def main(data: list[str]) -> int:
    """
    Given a list of strings, each string representing a report of levels separated by spaces,
    returns the total number of safe reports according to the rules of Day 2 Part 2 of the Advent of Code.
    """
    return sum(is_report_safe_with_problem_dampener(list(map(int, report.split()))) for report in data)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read().splitlines()

    print("Part 2:")
    print(f"Answer: {main(data)} ")
    #317 is too high
    #282 is too low
    #297 not the right answer
    #311 is right!!