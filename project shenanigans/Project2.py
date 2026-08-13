import csv
import random
import re
from dataclasses import dataclass
from powers import PeekPower, RedrawPower, SafeHitPower

HISTORY_FILE = "game_history.csv"
NAME_PATTERN = r"[A-Za-z][A-Za-z0-9 _-]{1,19}"

@dataclass
class Card:
    rank: str
    suit: str

    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        ranks = ["A", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise RuntimeError("The deck is empty.")
        return self.cards.pop()

class Participant:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def score(self):
        total = sum(card.value() for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == "A")

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_bust(self):
        return self.score() > 21

    def hand_text(self):
        return ", ".join(str(card) for card in self.hand)
