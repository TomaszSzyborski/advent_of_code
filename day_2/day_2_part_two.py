"""
--- Part Two ---
The Elf finishes helping with the tent and sneaks back over to you. "Anyway,
the second column says how the round needs to end: X means you need to lose,
Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way,
but now you need to figure out what shape to choose so the round ends as indicated.
The example above now goes like this:

In the first round, your opponent will choose Rock (A),
and you need the round to end in a draw (Y),
so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B),
and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide,
you would get a total score of 12.

Following the Elf's instructions for the second column,
what would your total score be if everything goes exactly according to your strategy guide?
"""
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

me_loosing = 'X'
me_drawing = 'Y'
me_winning = 'Z'

elf_playing_rock = 'A'
elf_playing_paper = 'B'
elf_playing_scissors = 'C'

me_playing_rock_points = 1
me_playing_paper_points = 2
me_playing_scissors_points = 3

@dataclass
class Round:
    elf_choice: str
    my_choice: str

    def calculate_result(self) -> int:
        """
        Calculates the result of the round.
        :return int points earned in the round
        """
        my_points = {
            elf_playing_rock: {
                me_loosing: me_playing_scissors_points,
                me_drawing: me_playing_rock_points,
                me_winning: me_playing_paper_points
            },
            elf_playing_paper: {
                me_loosing: me_playing_rock_points,
                me_drawing: me_playing_paper_points,
                me_winning: me_playing_scissors_points
            },
            elf_playing_scissors: {
                me_loosing: me_playing_paper_points,
                me_drawing: me_playing_scissors_points,
                me_winning: me_playing_rock_points
            },
        }[self.elf_choice][self.my_choice]

        total_points_in_the_round = 0

        if self.my_choice == me_drawing:
            total_points_in_the_round += (3 + my_points)
        elif self.my_choice == me_winning:
            total_points_in_the_round += (6 + my_points)
        else:
            total_points_in_the_round += (0 + my_points)

        log.debug(self)
        log.debug(f"points earned in round: {total_points_in_the_round}")
        log.debug("#" * 80)
        return total_points_in_the_round


# puzzle_input = "test_input.txt"
puzzle_input = "puzzle_input.txt"
with open(puzzle_input, 'r') as f:
    lines = f.read().splitlines()
    log.debug(lines)

rounds = [Round(*line.split()) for line in lines]

"""
part one
"""
points_earned = sum([r.calculate_result() for r in rounds])
log.info(f"{points_earned=}")
