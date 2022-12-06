"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships.
Supplies are stored in stacks of marked crates,
but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks.
To ensure none of the crates get crushed or fall over,
the crane operator will rearrange them in a series of carefully-planned steps.
After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure,
but they forgot to ask her which crate will end up where,
and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks
of crates and the rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates.
Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top.
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D.
Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure,
a quantity of crates is moved from one stack to a different stack.
In the first step of the above rearrangement procedure,
one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3.
Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again,
 because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example,
the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

"""
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

puzzle_input = "puzzle_input.txt"
with open(puzzle_input, 'r') as f:
    crates_raw_data, crane_actions_raw_data = f.read().split("\n\n")
    log.debug(crates_raw_data)
    log.debug(crane_actions_raw_data)

reversed_crates = crates_raw_data.split("\n")[::-1]
number_of_columns = len([column for column in  reversed_crates[0].split()])


rows = []
columns = {index+1: [] for index in range(number_of_columns)}
for column_number, row in enumerate(reversed_crates[1:], start=1):
    split_row = row[1::4]
    for index, data in enumerate(split_row, start=1):
        if data.strip():
            columns[index].append(data)


@dataclass
class CraneAction:
    move_amount: int
    source_index: int
    target_index: int


crane_actions: list[CraneAction] = []

for action in crane_actions_raw_data.splitlines():
    crane_actions.append(CraneAction(*map(int, action.split()[1::2])))

for action in crane_actions:
    for _ in range(action.move_amount):
        crate = columns[action.source_index].pop()
        columns[action.target_index].append(crate)

top_crates_list = [column[-1] for column in columns.values()]
log.info(''.join(top_crates_list))
#answer should be QNNTGTPFN