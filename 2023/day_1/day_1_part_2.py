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

# mode = 'test'
mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)


@dataclasses.dataclass
class Word:
    word: str
    first_index: int
    last_index: int

    def __post_init__(self):
        self.first_index = None if self.first_index == -1 else self.first_index
        self.last_index = None if self.last_index == -1 else self.last_index

    def __lt__(self, other):
        return self.first_index is not None and self.first_index < other.first_index

    def __gt__(self, other):
        return self.last_index is not None and self.last_index > other.last_index


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


file_name = "test.txt" if mode == 'test' else "input_part_1.txt"
with open(file_name) as f:
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
        logging.debug(f"{word=}: {first_index=}, {last_index=}")
        if first_index is not None and last_index is not None:
            spelled_out_indexes[word] = Word(word, first_index, last_index)
    logging.debug(f"{spelled_out_indexes=}")

    if spelled_out_indexes:
        min_found_spelled_word = min(spelled_out_indexes.values())
        max_found_spelled_word = max(spelled_out_indexes.values())
        logging.debug(f"{min_found_spelled_word=}")
        logging.debug(f"{max_found_spelled_word=}")

        first_chunk = line[:min_found_spelled_word.first_index]
        last_chunk = line[max_found_spelled_word.last_index:]

        first_numeric_number = get_first_number(first_chunk)
        last_numeric_number = get_first_number(last_chunk[::-1])
        first_part = first_numeric_number if first_numeric_number else spelled_out.index(
            min_found_spelled_word.word) + 1
        last_part = last_numeric_number if last_numeric_number else spelled_out.index(max_found_spelled_word.word) + 1
        found_number = f"{first_part}{last_part}"
        logging.debug(f"WITH SPELLED OUT WORDS: {found_number=}")
    else:
        found_number = f"{get_first_number(line)}{get_first_number(line[::-1])}"
        logging.debug(f"NO SPELLED OUT WORDS: {found_number=}")
    results.append(int(found_number))

if __name__ == '__main__':
    logging.info(sum(results))
    if mode == 'test':
        assert sum(results) == 281
