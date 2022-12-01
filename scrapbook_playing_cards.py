import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class Ranks(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4


RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()


class CardComparisonStrategy(Protocol):
    @staticmethod
    def sorting_index(rank: str, suit: str) -> int:
        ...


class RankFirstComparisonStrategy:
    @staticmethod
    def sorting_index(rank: str, suit: str):
        return RANKS.index(rank) * len(SUITS) + SUITS.index(suit)


class SuitFirstComparisonStrategy:
    @staticmethod
    def sorting_index(rank: str, suit: str):
        # return SUITS.index(suit), RANKS.index(rank)
        return SUITS.index(suit) * 100 + RANKS.index(rank)


@dataclass(order=True, kw_only=True)
class PlayingCard:
    sort_index: int = field(init=False, repr=False)
    rank: str
    suit: str
    comparison_strategy: CardComparisonStrategy = field(repr=False, default=RankFirstComparisonStrategy)

    def __post_init__(self):
        self.sort_index = self.comparison_strategy.sorting_index(self.rank, self.suit)

    def __str__(self):
        return f'{self.suit}{self.rank}'


def make_french_deck(comparison_strategy: CardComparisonStrategy = None) -> list[PlayingCard]:
    if comparison_strategy is None:
        comparison_strategy = RankFirstComparisonStrategy()
    return [PlayingCard(rank=rank, suit=suit, comparison_strategy=comparison_strategy)
            for suit in SUITS for rank in RANKS]


@dataclass
class Deck:
    cards: list[PlayingCard] = field(default_factory=make_french_deck)

    def __repr__(self):
        cards = ', '.join(f'{c!s}' for c in self.cards)
        return f'{self.__class__.__name__}({cards})'


if __name__ == '__main__':
    queen_of_hearts = PlayingCard(rank='Q', suit='♡')
    ace_of_spades = PlayingCard(rank='A', suit='♠')
    print(queen_of_hearts)
    print(ace_of_spades)
    print(f"{ace_of_spades > queen_of_hearts=}")
    ten_of_clubs = PlayingCard(rank="10", suit="♣")
    two_of_clubs = PlayingCard(rank="2", suit="♣")
    print(ten_of_clubs)
    print(two_of_clubs)
    print(f"{ten_of_clubs > two_of_clubs=}")
    deck = Deck()
    french_deck = make_french_deck(RankFirstComparisonStrategy)
    random.shuffle(french_deck)
    deck = Deck(french_deck)
    print(deck)
    deck = Deck(sorted(french_deck))
    print(deck)
