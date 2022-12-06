"""
--- Part Two ---
Your device's communication system is correctly detecting packets, but still isn't working.
It looks like it also needs to look for messages.

A start-of-message marker is just like a start-of-packet marker,
except it consists of 14 distinct characters rather than 4.

Here are the first positions of start-of-message markers for all of the above examples:

mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
How many characters need to be processed before the first start-of-message marker is detected?

--- Part Two ---
Your device's communication system is correctly detecting packets, but still isn't working.
It looks like it also needs to look for messages.

A start-of-message marker is just like a start-of-packet marker,
except it consists of 14 distinct characters rather than 4.

Here are the first positions of start-of-message markers for all of the above examples:

mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
How many characters need to be processed before the first start-of-message marker is detected?
"""
import logging
import os
from day_6_part_one import find_buffer_starting_marker

log_level = {
    "debug": logging.DEBUG,
    "info": logging.INFO
}.get(os.environ.get('LOG_LEVEL'), logging.DEBUG)

logging.basicConfig(level=log_level)
log = logging.getLogger()


if __name__ == '__main__':
    puzzle_input_file_path = "puzzle_input.txt"
    window_size = 14

    with open(puzzle_input_file_path, 'r') as f:
        data_stream = f.read().strip()

    buffer_starting_index_generator = find_buffer_starting_marker(data_stream, window_size)
    first_message_marker = next(buffer_starting_index_generator) + window_size
    print(f"{first_message_marker=}")

