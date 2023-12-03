"""
--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""
import dataclasses
import logging
import os

logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))


def get_first_number(text: str) -> str | None:
    for letter in text:
        if letter.isdigit():
            return letter
    return None


def find_word(text: str, word: str, last: bool = False) -> int:
    if last:
        last_word_index = text.rfind(word)
        return last_word_index if last_word_index != -1 else None
    else:
        first_word_index = text.find(word)
        return first_word_index if first_word_index != -1 else None


with open("input_part_1.txt") as f:
    data: list[str] = f.read().split('\n')

spelled_out = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
]

results = []
for line_number, line in enumerate(data):
    logging.debug(f"{line_number=}, {line=}")
    spelled_out_indexes = {}

    for word in spelled_out:
        first_index = find_word(line, word)
        last_index = find_word(line, word, True)
        if any([first_index, last_index]):
            spelled_out_indexes[word] = [i for i in [first_index, last_index] if i is not None]
    logging.debug(spelled_out_indexes)

    if spelled_out_indexes:
        logging.debug(f"{line=}")
        first_spelled_word = min(spelled_out_indexes, key=spelled_out_indexes.get)
        last_spelled_word = max(spelled_out_indexes, key=spelled_out_indexes.get)
        logging.debug(f"Min word: {first_spelled_word}")
        logging.debug(f"Max word: {last_spelled_word}")
        first_found_spelled_word_index = spelled_out_indexes[first_spelled_word]
        last_found_spelled_word_index = spelled_out_indexes[last_spelled_word]
        logging.debug(f"Min index : {first_found_spelled_word_index}")
        logging.debug(f"Max index: {last_found_spelled_word_index}")

        f = get_first_number(line[:first_found_spelled_word_index[0]])
        l = get_first_number(line[last_found_spelled_word_index[1]:][::-1])
        logging.debug(f"First found numeric number : {f}")
        logging.debug(f"Last found numeric number: {l}")

        first = f if f is not None else spelled_out.index(first_spelled_word) + 1
        last = l if l is not None else spelled_out.index(last_spelled_word) + 1
        logging.debug(f"First number data to combine for result: {first}")
        logging.debug(f"Last number data to combine for result: {last}")

        found_number = f"{first}{last}"
        logging.debug(f"WITH SPELLED OUT WORDS: {found_number=}")
        results.append(int(found_number))
    else:
        found_number = f"{get_first_number(line)}{get_first_number(line[::-1])}"
        logging.debug(f"NO SPELLED OUT WORDS: {found_number=}")
        results.append(int(found_number))

print(sum(results))
"""
DEBUG:root:line_number=992
DEBUG:root:line='bnjpqcqdzmeight2gtjhqeight'
DEBUG:root:{'one': -1, 'two': -1, 'three': -1, 'four': -1, 'five': -1, 'six': -1, 'seven': -1, 'eight': 10, 'nine': -1}
INFO:root:spelled_out_indexes={'eight': 10}
DEBUG:root:line='bnjpqcqdzmeight2gtjhqeight'
DEBUG:root:Min word: eight
DEBUG:root:Max word: eight
DEBUG:root:Min index : 10
DEBUG:root:Max index: 10
DEBUG:root:First found numeric number : None
DEBUG:root:Last found numeric number: 2
DEBUG:root:First number data to combine for result: 8
DEBUG:root:Last number data to combine for result: 2
DEBUG:root:WITH SPELLED OUT WORDS: found_number='82'
"""
"""
DEBUG:root:line='five3oneonefrvnbnnlz'
DEBUG:root:Min word: one
DEBUG:root:Max word: one
DEBUG:root:Min index : [5, 8]
DEBUG:root:Max index: [5, 8]
DEBUG:root:First found numeric number : 3
DEBUG:root:Last found numeric number: None
DEBUG:root:First number data to combine for result: 3
DEBUG:root:Last number data to combine for result: 1
DEBUG:root:WITH SPELLED OUT WORDS: found_number='31'
"""