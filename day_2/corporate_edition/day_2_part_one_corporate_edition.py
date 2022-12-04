"""
--- Day 2: Rock Paper Scissors ---
The Elves begin to set up camp on the beach.
To decide whose tent gets to be closest to the snack storage,
a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round,
the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape.
Then, a winner for that round is selected:
Rock defeats Scissors,
Scissors defeats Paper,
and Paper defeats Rock.

If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday,
one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win.
"The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response:
X for Rock, Y for Paper, and Z for Scissors.
Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score.
Your total score is the sum of your scores for each round.
The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you,
you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

"""
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class HandShape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class HandStrategy(Protocol):
    def beats(self) -> HandShape:
        ...


class RockStrategy:
    def beats(self) -> HandShape:
        return HandShape.SCISSORS


class PaperStrategy:
    def beats(self) -> HandShape:
        return HandShape.ROCK


class ScissorsStrategy:
    def beats(self) -> HandShape:
        return HandShape.PAPER


class PlayerData(Enum):
    X = HandShape.ROCK
    Y = HandShape.PAPER
    Z = HandShape.SCISSORS


class ElfData(Enum):
    A = HandShape.ROCK
    B = HandShape.PAPER
    C = HandShape.SCISSORS


class Outcome:
    WIN = 6
    DRAW = 3
    LOSS = 0


class BattleStrategy(Protocol):
    def play(self, my_gesture: HandShape, enemy_gesture: HandShape) -> int:
        ...


class WinningStrategy:
    def play(self, my_gesture: HandShape, enemy_gesture: HandShape) -> int:
        return Outcome.WIN


class LoosingStrategy:
    def play(self, my_gesture: HandShape, enemy_gesture: HandShape) -> int:
        return Outcome.LOSS


class DrawStrategy:
    def play(self, my_gesture: HandShape, enemy_gesture: HandShape) -> int:
        return Outcome.DRAW


@dataclass
class Player:
    gesture: PlayerData
    strategy: BattleStrategy

    def play_against(self, opponent_gesture: ElfData):
        return self.strategy.play(self.gesture.value, opponent_gesture.value)


print(Player(PlayerData.X, WinningStrategy()).play_against(ElfData.C))
#
# class Clash:
#     def __init__(self, elf: ElfData, strategy: BattleStrategy):
#         self._elf = elf
#         self._strategy = strategy
#
#     # def result(self):
#
#
# class BattleStrategyFactory:
#     @staticmethod
#     def create(player: Player):
#         return {
#             HandShape.ROCK: RockStrategy(),
#             HandShape.PAPER: PaperStrategy(),
#             HandShape.SCISSORS: ScissorsStrategy(),
#         }.get(player.value, None)
#
#
#
#
# @dataclass
# class Round:
#     elf_choice: ElfData
#     player_choice: PlayerData
#
#     def calculate_result(self) -> int:
#         """
#         Calculates the result of the round.
#         :return int points earned in the round
#         """
#         total_points_in_the_round = 0
#         total_points_in_the_round += self.player_choice.value.value
#         return total_points_in_the_round
#
# if __name__ == "__main__":
#     # puzzle_input = "test_input.txt"
#     puzzle_input = "puzzle_input.txt"
#     with open(puzzle_input, 'r') as f:
#         lines = f.read().splitlines()
#         log.debug(lines)
#
#     rounds = [Round(*line.split()) for line in lines]
#
#     points_earned = sum([r.calculate_result() for r in rounds])
#     log.info(f"{points_earned=}")
