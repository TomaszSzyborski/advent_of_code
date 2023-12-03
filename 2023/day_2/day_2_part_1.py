"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island
floating in the sky.
You gently land in a fluffy pile of leaves.
It's quite cold, but you don't see much snow.
An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow.
He'll be happy to explain the situation, but it's a bit of a walk, so you have some time.
They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue.
Each time you play this game, he will hide a secret number of cubes of each color in the bag,
and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag,
grab a handful of random cubes, show them to you, and then put them back in the bag.
He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input).
Each game is listed with its ID number (like the 11 in Game 11: ...)
followed by a semicolon-separated list
of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again).
 The first set is 3 blue cubes and 4 red cubes;
 the second set is 1 red cube, 2 green cubes, and 6 blue cubes;
 the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible
if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration.
However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once;
similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once.
If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only
12 red cubes, 13 green cubes, and 14 blue cubes.
What is the sum of the IDs of those games?
"""
import logging
from dataclasses import dataclass
import os
import re
from enum import StrEnum

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

    def __gt__(self, other):
        logging.debug(f"GT {self=}")
        logging.debug(f"GT {other=}")
        for c in self.balls.keys():
            if self.balls.get(c).quantity > other.balls.get(c).quantity:
                logging.debug(f"GT false")
                return False
        logging.debug(f"GT true")
        return True


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


def games_valid(l: list, master_set):
    valid = False
    for game_set in l:
        logging.debug(f"{game_set=}")
        logging.debug(f"{master_set=}")
        if game_set > master_set:
            valid = True
            break
    return valid


if __name__ == '__main__':
    master_set = GameSet({Colour.RED: Ball(12, Colour.RED),
                          Colour.GREEN: Ball(13, Colour.GREEN),
                          Colour.BLUE: Ball(14, Colour.BLUE)})
    games = strip_game_prefixes(data)
    valid_games = []
    for game in games:
        logging.debug(game)
        if games_valid(game.game_sets, master_set):
            valid_games.append(game.game_id)
    logging.info(valid_games)
    logging.info(sum(valid_games))
