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