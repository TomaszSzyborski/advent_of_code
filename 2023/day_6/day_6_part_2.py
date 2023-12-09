"""
--- Part Two ---
As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200
...now instead means this:

Time:      71530
Distance:  940200
Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?

"""
import copy
import dataclasses
import logging
import math
import os
import sys
from functools import reduce
from itertools import takewhile
from time import perf_counter

# mode = 'test'
mode = 'production'
logging.basicConfig(encoding='utf-8')
logger = logging.getLogger()
if mode == 'test':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

file_name = "test_input.txt" if mode == "test" else "puzzle_input.txt"
with open(file_name) as f:
    time, distance = [line.strip("Time:").strip("Distance:").strip().replace(" ","") for line in f.read().split('\n')]

logger.debug(f"{time=}")
logger.debug(f"{distance=}")

def debug(data):
    if mode == 'test':
        print(data)

@dataclasses.dataclass
class Ride:
    time: int
    distance: int

    def calculate_times(self):
        distance_over_time = int(self.distance / self.time)
        # return math.floor(self.time - 2 * distance_over_time)
        wins = 0
        start = perf_counter()
        for t in range(distance_over_time, self.time - distance_over_time):
            travel = t * (self.time - t)
            # if logger.level == logging.DEBUG:
            # debug(f"{travel=}")
            if travel > self.distance:
                wins += 1
        end = perf_counter()
        logger.info(f"Time elapsed:{end-start}")
        return wins


ride = Ride(int(time), int(distance))
logger.info(f"{ride}")
win = ride.calculate_times()
logger.info(win)

if mode == 'test':
    assert win == 71503, win
else:
    assert win == 36872656, win #42204338 too high