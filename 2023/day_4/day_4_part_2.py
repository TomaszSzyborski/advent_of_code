"""
--- Day 4: Scratchcards ---
--- Part Two ---
Just as you're about to report your findings to the Elf, one of you realizes that the rules have actually been printed on the back of every card this whole time.

There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)

This time, the above example goes differently:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
Your copy of card 2 also wins one copy each of cards 3 and 4.
Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?

"""
import copy
import functools
import logging
import string
from dataclasses import dataclass
import os
from functools import cache
from typing import Self
import math
from collections import defaultdict, Counter

# mode = 'test'
mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

file_name = "test_input.txt" if mode == "test" else "puzzle_input.txt"
with open(file_name) as f:
    data = f.read().split('\n')


@dataclass(eq=True, frozen=True)
class Game:
    game_number: int
    winning_numbers: tuple
    scratched_numbers: tuple


def clean_the_data(list_of_cards) -> tuple[Game]:
    clean_data = []
    for game_number, scratch_card in enumerate(list_of_cards, start=1):
        logging.info(f"{scratch_card=}")
        winning, your = scratch_card.split("|")
        winning = winning[str(winning.strip()).index(":") + 1:]
        winning_list = tuple([w.strip() for w in winning.split(" ") if w])
        your_list = tuple([y.strip() for y in your.split(" ") if y])
        logging.info(f"{winning_list=}")
        logging.info(f"{your_list=}")
        clean_data.append(Game(game_number, winning_list, your_list))
    return tuple(clean_data)


def solve():
    cleaned_data = clean_the_data(data)
    points = 0
    for game in cleaned_data:
        found_numbers = len([n for n in game.scratched_numbers if n in game.winning_numbers])
        points += int(2 ** (found_numbers - 1))
        logging.debug(points)
    return points


@dataclass(eq=True, frozen=True)
class GoldenDataSet:
    data: tuple





def solve_2():
    cleaned_data = clean_the_data(data)
    original: GoldenDataSet = GoldenDataSet(tuple(cleaned_data))

    @functools.lru_cache()
    # @cache
    def find_copies_in_data(game: Game):
        found_numbers = len(tuple([n for n in game.scratched_numbers if n in game.winning_numbers]))
        logging.debug(f"{game.game_number=} {found_numbers=}")
        winner = [game.game_number]
        copies = ()
        if found_numbers > 0:
            copies = tuple([original.data[game.game_number + i - 1] for i in range(1, found_numbers + 1)])
        return tuple(winner), tuple(copies)

    winners = []
    passes = 0
    # todo use with reduce and recursion
    # todo use cache function
    while True:
        passes += 1
        copies = []
        logging.info(f"{passes} pass of the game data - {passes - 0} copied data.")
        logging.debug(f"game data={[g.game_number for g in cleaned_data]}")
        for game in cleaned_data:
            winner, copiess = find_copies_in_data(game)
            winners.extend(winner)
            copies.extend(copiess)
        cleaned_data = copies[:]
        if len(copies) == 0:
            count_winners = Counter(winners)
            logging.info(f"{count_winners=}")
            logging.info(f"{sum(count_winners.values())=}")
            return len(winners)


if __name__ == '__main__':
    if mode == 'test':
        assert solve() == 13
        result = solve_2()
        assert result == 30, result
    else:
        result = solve()
        assert result == 25231, result
        result = solve_2()
        assert result == 9721255, result
