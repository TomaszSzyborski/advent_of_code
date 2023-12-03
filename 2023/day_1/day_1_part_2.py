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
import logging
import os

logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))


def get_first_number(text: str) -> str | None:
    for letter in text:
        if letter.isdigit():
            return letter
    return None

with open("input_part_1.txt") as f:
    data = f.read().split('\n')

spelled_out = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
]
spelled_out_data = {numeric_value: word
                    for numeric_value, word
                    in enumerate(spelled_out, start=1)}
logging.debug(f"{spelled_out_data=}")
results = []
for line_number, line in enumerate(data):
    logging.debug(f"{line_number=}")
    logging.debug(f"{line=}")
    spelled_oud_indexes = {word: line.find(word) for word in spelled_out_data.values()}
    logging.debug(spelled_oud_indexes)
    data_dict = {key: value for key, value in spelled_oud_indexes.items() if value != -1}
    logging.info(f"{data_dict=}")
    if data_dict:
        logging.debug(f"{line=}")
        first_spelled_word = min(data_dict, key=data_dict.get)
        last_spelled_word = max(data_dict, key=data_dict.get)
        logging.debug(f"Min word: {first_spelled_word}")
        logging.debug(f"Max word: {last_spelled_word}")
        first_found_spelled_word_index = data_dict[first_spelled_word]
        last_found_spelled_word_index = data_dict[last_spelled_word]
        logging.debug(f"Min index : {first_found_spelled_word_index}")
        logging.debug(f"Max index: {last_found_spelled_word_index}")

        f = get_first_number(line[:first_found_spelled_word_index])
        l = get_first_number(line[last_found_spelled_word_index:][::-1])
        logging.debug(f"First found numeric number : {f}")
        logging.debug(f"Last found numeric number: {l}")

        first = f if f is not None else [k for k, v in spelled_out_data.items() if v == first_spelled_word][0]
        last = l if l is not None else [k for k, v in spelled_out_data.items() if v == last_spelled_word][0]
        logging.debug(f"First number data to combine for result: {first}")
        logging.debug(f"Last number data to combine for result: {last}")

        found_number = f"{first}{last}"
        logging.debug(f"WITH SPELLED OUT WORDS: {found_number=}")
    else:
        found_number = f"{get_first_number(line)}{get_first_number(line[::-1])}"
        logging.debug(f"NO SPELLED OUT WORDS: {found_number=}")
    results.append(int(found_number))

print(sum(results))

# spelled_out = [
#     "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
# ]
# spelled_out_data = {spelled_out: {"numeric_value": numeric_value}
#                     for numeric_value, spelled
#                     in enumerate(spelled_out, start=1)}
#
#
# def get_first_number(text: str) -> str | None:
#     for letter in text:
#         if letter.isdigit():
#             return letter
#
#
# results = []
# for line in data:
#     spelled_oud_indexes = []
#     filtered_spelled_out_indexes = [index for index in spelled_oud_indexes if index is not -1]
#     if filtered_spelled_out_indexes:
#         first_spelled_out = min(filtered_spelled_out_indexes)
#         last_spelled_out = max(filtered_spelled_out_indexes)
#         print(first_spelled_out, last_spelled_out)
#     found_number = get_first_number(line) + get_first_number(line[::-1])
#     results.append(int(found_number))
#
# print(sum(results))
