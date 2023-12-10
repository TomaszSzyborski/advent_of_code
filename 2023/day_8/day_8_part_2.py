"""
-- Part Two ---
The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
Here, there are two starting nodes, 11A and 22A (because they both end with A).
As you follow each left/right instruction, use that instruction to simultaneously
navigate away from both nodes you're currently on.
Repeat this process until all of the nodes you're currently on end with Z.
(If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.)
In this example, you would proceed as follows:

Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

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

mode = 'test'
# mode = 'production'
logging.basicConfig(encoding='utf-8')
logger = logging.getLogger()
if mode in ['test', 'test2']:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

file_name = ({"test": "part_2_test_input.txt",
              }
             .get(mode, "puzzle_input.txt"))


@dataclasses.dataclass(frozen=True)
class Mapping(dict):
    left: str
    right: str

    def __post_init__(self):
        self.update({
            "L": self.left,
            "R": self.right
        })

    def __setitem__(self, key, value):
        raise Exception("Instance is Frozen")

    def __getitem__(self, key):
        if key == "L":
            return self.left
        if key == "R":
            return self.right
        raise Exception("wrong key")


with open(file_name) as f:
    lines = [line.strip() for line in f.read().split('\n')]
moves = lines[0]
mapping_data = {}
for l in lines[2:]:
    source, mapping = l.split(" = ")
    mapping_data[source] = Mapping(*mapping.strip("()").split(", "))

total_steps = 0

logger.debug(mapping_data)
current_places = {k: v for k, v in mapping_data.items() if str(k).endswith("A")}
logger.info(f"{len(current_places)=}")

for move in cycle(moves):
    if all([str(k).endswith("Z") for k, v in current_places.items()]):
        break
    # logger.debug(current_places)
    new_items = {}
    for source, mapping in current_places.items():
        new_source = mapping_data[source][move]
        new_items[new_source] = mapping_data[new_source]
    logger.info(f"{len(new_items)=}")
    current_places = new_items
    total_steps += 1

if mode == 'test':
    assert total_steps == 6, total_steps
else:
    #TODO find correct answer
    assert total_steps == 6, total_steps
