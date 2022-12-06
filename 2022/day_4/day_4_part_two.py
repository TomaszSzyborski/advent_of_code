"""
--- Part Two ---
It seems like there is still quite a bit of duplicate work planned.
 Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap,
while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

5-7,7-9 overlaps in a single section, 7.
2-8,3-7 overlaps all of the sections 3 through 7.
6-6,4-6 overlaps in a single section, 6.
2-6,4-8 overlaps in sections 4, 5, and 6.
So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
"""

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

puzzle_input = "puzzle_input.txt"
with open(puzzle_input, 'r') as f:
    lines = f.read().splitlines()
    log.debug(lines)

within_pair_count = 0

for line in lines:
    first_elf, second_elf = line.split(",")
    first_elf_min, first_elf_max = map(int, first_elf.split("-"))
    second_elf_min, second_elf_max = map(int, second_elf.split("-"))
    log.debug(f"{first_elf_min=}, {first_elf_max=}")
    log.debug(f"{second_elf_min=}, {second_elf_max=}")
    within_first_elf_min = second_elf_max >= first_elf_min >= second_elf_min
    within_first_elf_max = second_elf_min <= first_elf_max <= second_elf_max
    within_second_elf_min = first_elf_max >= second_elf_min >= first_elf_min
    within_second_elf_max = first_elf_min <= second_elf_max <= first_elf_max
    within_first_elf = within_first_elf_min or within_first_elf_max
    within_second_elf = within_second_elf_min or within_second_elf_max
    if within_first_elf or within_second_elf:
        log.info(f"Elf {first_elf} and {second_elf} assignments overlap.")
        within_pair_count += 1
    else:
        log.info(f"Elf {first_elf} and {second_elf} assignments don't overlap.")

log.debug(within_pair_count)
