"""
--- Day 9: Mirage Maintenance ---
You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. The sandstorm subsequently subsides, somehow seeing you standing at an oasis!

The camel goes to get some water and you stretch your neck. As you look up, you discover what must be yet another giant floating island, this one made of metal! That must be where the parts to fix the sand machines come from.

There's even a hang glider partially buried in the sand here; once the sun rises and heats up the sand, you might be able to use the glider and the hot air to get all the way up to the metal island!

While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. It must have a delicate ecosystem; you might as well take some ecological readings while you wait. Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.

You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a single value. For example:

0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.

In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:

0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:

0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0
You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:

0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0
Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:

0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0
So, the next value of the first history is 18.

Finding all-zero differences for the second history requires an additional sequence:

1   3   6  10  15  21
  2   3   4   5   6
    1   1   1   1
      0   0   0
Then, following the same process as before, work out the next value in each sequence from the bottom up:

1   3   6  10  15  21  28
  2   3   4   5   6   7
    1   1   1   1   1
      0   0   0   0
So, the next value of the second history is 28.

The third history requires even more sequences, but its next value can be found the same way:

10  13  16  21  30  45  68
   3   3   5   9  15  23
     0   2   4   6   8
       2   2   2   2
         0   0   0
So, the next value of the third history is 68.

If you find the next value for each history in this example and add them together, you get 114.

Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?
"""
import copy
import dataclasses
import logging
import math
import os
import sys
from collections import Counter
from functools import reduce
from itertools import takewhile, cycle
from time import perf_counter
from typing import Self

# mode = 'test'
mode = 'production'
logging.basicConfig(encoding='utf-8')
logger = logging.getLogger()
if mode in ['test', 'test2']:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

file_name = ({"test": "test_input.txt",
              "test2": "test_input_2.txt"}
             .get(mode, "puzzle_input.txt"))


@dataclasses.dataclass
class History:
    original_data: tuple[int]
    tmp_history: list[int] = dataclasses.field(init=False, default_factory=list, repr=False)
    all_histories: list[list[int]] = dataclasses.field(init=False, default_factory=list)

    def __post_init__(self):
        self.tmp_history = list(copy.deepcopy(self.original_data))

    def extrapolate_right(self):
        self.all_histories.append(self.tmp_history)
        logger.debug(self.tmp_history)
        if len(self.tmp_history) == 1:
            self.tmp_history.append(self.tmp_history[0])
        if all([t == 0 for t in self.tmp_history]):
            # reversing histories from all zeroes to original as last element
            self.all_histories = self.all_histories[::-1]
            return
        self.tmp_history = [self.tmp_history[i + 1] - self.tmp_history[i]
                            for i, _ in enumerate(self.tmp_history[:-1])]
        # recursive extrapolation
        self.extrapolate_right()

    def extrapolate_left(self):
        self.all_histories.append(self.tmp_history)
        logger.debug(self.tmp_history)
        if len(self.tmp_history) == 1:
            self.tmp_history.insert(0, self.tmp_history[0])
        if all([t == 0 for t in self.tmp_history]):
            # reversing histories from all zeroes to original as last element
            self.all_histories = self.all_histories[::-1]
            return
        self.tmp_history = [self.tmp_history[i + 1] - self.tmp_history[i]
                            for i, _ in enumerate(self.tmp_history[:-1])]
        # recursive extrapolation
        self.extrapolate_left()


with open(file_name) as f:
    histories = [History(tuple([int(l.strip()) for l in line.split()])) for line in f.read().split('\n')]


result = 0
for h in histories:
    logger.info(f"{h.original_data=}")
    h.extrapolate_left()
    logger.info(f"{h.all_histories=}")
    h.all_histories[0].append(0)
    for i, _ in enumerate(h.all_histories[:-1], start=1):
        first_previous = h.all_histories[i - 1][0]
        first_current = h.all_histories[i][0]
        missing_result = first_current - first_previous
        h.all_histories[i].insert(0, missing_result)
    logger.info(f"new.{h.all_histories=}")
    logger.info(f"first ELEMENT {h.all_histories[-1][0]}")
    result += h.all_histories[-1][0]

logger.info(result)
if mode == 'test':
    assert result == 2 , result
else:
    assert result == 1050, result
