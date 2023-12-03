"""
--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""
import logging
from dataclasses import dataclass
import os
import re
from enum import StrEnum
from typing import Self

mode = 'test'
# mode = 'production'
if mode == 'test':
    logging.basicConfig(encoding='utf-8', level=os.getenv("loglevel", logging.DEBUG))
else:
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

with open("puzzle_input.txt") as f:
    data = f.read().split('\n')


class Colour(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass(order=True)
class Ball:
    quantity: int
    colour: Colour

    def __post_init__(self):
        if type(self.quantity) is not int:
            self.quantity = int(self.quantity)

        if type(self.colour) is not Colour:
            self.colour = Colour(self.colour)


@dataclass
class GameSet:
    balls: dict[Colour, Ball]

    def __add__(self, other):
        new = {}
        new.update(self.balls)
        for k, v in other.balls.items():
            if k in new.keys():
                if v > new[k]:
                    new[k] = v
            else:
                new[k] = v
        return GameSet(new)

@dataclass
class Game:
    game_id: int
    game_sets: list[GameSet]


def get_sets_from_game(raw_game_data: str, game_id: int):
    game_sets = [g.strip() for g in raw_game_data.split(";")]
    game = Game(game_id, [])
    for game_set in game_sets:
        b = [Ball(*ball_data.split(" ")) for ball_data in game_set.split(", ")]
        balls = {ba.colour: ba for ba in b}
        game.game_sets.append(GameSet(balls))
    return game


def strip_game_prefixes(games: list):
    # game_id = [re.findall("\d+", re.findall("Game \d+:", game)[0])[0] for game in games]
    games_results = [re.sub("Game \d+:", "", game).strip() for game in games]
    gamez = []
    for game_id, game in enumerate(games_results, start=1):
        sets = get_sets_from_game(game, game_id)
        gamez.append(sets)
    return gamez


def calculate_games_power(games_sets: list):
    power_set: GameSet = games_sets[0]
    for g in games_sets[1:]:
        power_set += g
    logging.debug(power_set)
    power = 1
    for c in [Colour.RED, Colour.GREEN, Colour.BLUE]:
        power *= power_set.balls[c].quantity
    return power

if __name__ == '__main__':
    games = strip_game_prefixes(data)
    valid_games = []
    for game in games:
        logging.debug(game)
        logging.debug(game.game_id)
        games_power = calculate_games_power(game.game_sets)
        valid_games.append(games_power)
    logging.info(valid_games)
    logging.info(sum(valid_games))
