"""
--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats,
an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
However, the action of moving three crates from stack 1 to stack 3
means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1,
they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2,
but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes,
update your simulation so that the Elves know where they should stand to be ready to unload the final supplies.
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
    stack = columns[action.source_index][-action.move_amount:]
    columns[action.target_index].extend(stack)
    for _ in range(action.move_amount):
        columns[action.source_index].pop()

top_crates_list = [column[-1] for column in columns.values()]
log.info(''.join(top_crates_list))
#answer should be QNNTGTPFN