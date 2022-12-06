"""
--- Day 4: Camp Cleanup ---
Space needs to be cleared before the last supplies can be unloaded from the ships,
and so several Elves have been assigned the job of cleaning up sections of the camp.
Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other,
they've noticed that many of the assignments overlap.
To try to quickly find overlaps and reduce duplicated effort,
the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
For the first few pairs, this list means:

Within the first pair of Elves,
the first Elf was assigned sections 2-4 (sections 2, 3, and 4),
 while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
The Elves in the second pair were each assigned two sections.
The Elves in the third pair were each assigned three sections:
one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.
This example list uses single-digit section IDs to make it easier to draw;
your actual list might contain larger numbers.
Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
"""

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

puzzle_input = "puzzle_input.txt"
with open(puzzle_input, 'r') as f:
    lines = f.read().splitlines()
    log.debug(lines)

wholly_within_pair_count = 0

for line in lines:
    first_elf, second_elf = line.split(",")
    first_elf_min, first_elf_max = map(int, first_elf.split("-"))
    second_elf_min, second_elf_max = map(int, second_elf.split("-"))
    log.debug(f"{first_elf_min=}, {first_elf_max=}")
    log.debug(f"{second_elf_min=}, {second_elf_max=}")
    wholly_within_first_elf_min = first_elf_min >= second_elf_min
    wholly_within_first_elf_max = first_elf_max <= second_elf_max
    wholly_within_second_elf_min = second_elf_min >= first_elf_min
    wholly_within_second_elf_max = second_elf_max <= first_elf_max
    wholly_within_first_elf = wholly_within_first_elf_min and wholly_within_first_elf_max
    wholly_within_second_elf = wholly_within_second_elf_min and wholly_within_second_elf_max
    if wholly_within_first_elf or wholly_within_second_elf:
        log.info(f"Elf {first_elf} and {second_elf} assignments wholly overlap.")
        wholly_within_pair_count += 1
    else:
        log.info(f"Elf {first_elf} and {second_elf} assignments don't wholly overlap.")

log.debug(wholly_within_pair_count)
