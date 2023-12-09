"""
--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""
import copy
import dataclasses
import logging
import os
import sys
from itertools import takewhile

mode = 'test'
# mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

file_name = "test_input.txt" if mode == "test" else "puzzle_input.txt"
with open(file_name) as f:
    data = [l.strip() for l in f.read().split('\n')]

dirty_seeds = data[0].strip("seeds :")
seed_data = [int(i) for i in dirty_seeds.strip().split()]
seeds_pairs = [range(seed_data[index], seed_data[index] + seed_data[index + 1])
               for index in range(0, len(seed_data), 2)]
logging.info(seeds_pairs)
if mode == 'test':
    seeds = []
    for s in seeds_pairs:
        seeds.extend(s)
    logging.info(f"{seeds=}")
    assert len(seeds) == 27, f"{len(seeds)=} {seeds}"

# cleaned_data = {}
#
#
# @dataclasses.dataclass
# class Mapping:
#     destination_range_start: int
#     source_range_start: int
#     range_length: int
#
#     def __post_init__(self):
#         self.source_range_start = int(self.source_range_start)
#         self.destination_range_start = int(self.destination_range_start)
#         self.range_length = int(self.range_length)
#
#     def check_mapping(self, point):
#         return self.source_range_start + self.range_length >= point >= self.source_range_start
#
#     def map_source_to_destination(self, point: int):
#         return self.destination_range_start + (point - self.source_range_start)
#
#
# for element in [
#     "seed-to-soil",
#     "soil-to-fertilizer",
#     "fertilizer-to-water",
#     "water-to-light",
#     "light-to-temperature",
#     "temperature-to-humidity",
#     "humidity-to-location",
# ]:
#     index = data.index(f"{element} map:")
#     lines = takewhile(lambda line: line != '', data[index + 1:])
#     cleaned_data[element] = [Mapping(*line.split()) for line in lines]
#     # logging.debug(cleaned_data[element])
#
# logging.info(cleaned_data)
# logging.info(f"{len(cleaned_data)=}")
#
# locations = []
# min_destination = sys.maxsize
# for seed_range in seeds_pairs:
#     places = copy.deepcopy(seed_range)
#     logging.info(f"loop for {places}")
#     for seed in seed_range:
#         logging.debug(f"checking {seed=}")
#         for place in places:
#             source = place
#             for element in [
#                 "seed-to-soil",
#                 "soil-to-fertilizer",
#                 "fertilizer-to-water",
#                 "water-to-light",
#                 "light-to-temperature",
#                 "temperature-to-humidity",
#                 "humidity-to-location",
#             ]:
#                 destination = None
#                 for mapping in cleaned_data[element]:
#                     logging.debug(
#                         f"{element=} source={source}; is_mapped={mapping.check_mapping(place)}; destination={mapping.map_source_to_destination(place)} ")
#                     if mapping.check_mapping(place):
#                         destination = mapping.map_source_to_destination(place)
#                         place = destination
#                         break
#                     else:
#                         destination = place
#                 logging.debug(
#                     f"FINAL PLACEMENT {element=} {source=} {destination=}")
#                 source = destination
#             if destination <= min_destination:
#                 min_destination = destination
#             logging.info(f"{min_destination=}")
# if mode == 'test':
#     assert min_destination == 46, f"{min_destination=}"
# if mode == 'production':
#     assert min_destination == 825516882, f"{min_destination=}"
with open("puzzle_input.txt") as f:
    inputs, *blocks = f.read().split("\n\n")

inputs = list(map(int, inputs.split(":")[1].split()))

seeds = []

for i in range(0, len(inputs), 2):
    seeds.append((inputs[i], inputs[i] + inputs[i + 1]))

for block in blocks:
    ranges = []
    for line in block.splitlines()[1:]:
        ranges.append(list(map(int, line.split())))
    new = []
    while len(seeds) > 0:
        s, e = seeds.pop()
        for a, b, c in ranges:
            os = max(s, b)
            oe = min(e, b + c)
            if os < oe:
                new.append((os - b + a, oe - b + a))
                if os > s:
                    seeds.append((s, os))
                if e > oe:
                    seeds.append((oe, e))
                break
        else:
            new.append((s, e))
    seeds = new

print(min(seeds)[0])