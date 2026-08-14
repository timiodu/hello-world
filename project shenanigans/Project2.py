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

class Player(Participant):
    def __init__(self, name):
        super().__init__(name)
        self.round_wins = 0

    def choose_action(self):
        while True:
            choice = input("\n[H]it or [S]tand? ").strip().lower()

            if choice in ("h", "s"):
                return choice

            print("Please enter H or S.")

class Dealer(Participant):
    def __init__(self):
        super().__init__("Dealer")

    def play(self, deck):
        while self.score() < 17:
            self.add_card(deck.draw())

class Player(Participant):
    def __init__(self, name):
        super().__init__(name)
        self.round_wins = 0

    def choose_action(self):
        while True:
            choice = input("\n[H]it or [S]tand? ").strip().lower()

            if choice in ("h", "s"):
                return choice

            print("Please enter H or S.")

class Dealer(Participant):
    def __init__(self):
        super().__init__("Dealer")

    def play(self, deck):
        while self.score() < 17:
            self.add_card(deck.draw())

class BlackjackGame:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.dealer = Dealer()
        self.round_number = 1
        self.powers = [PeekPower(), RedrawPower(), SafeHitPower()]

    def reset_hands(self):
        self.player.hand = []
        self.dealer.hand = []

    def deal_starting_cards(self, deck):
        for _ in range(2):
            self.player.add_card(deck.draw())
            self.dealer.add_card(deck.draw())

    def show_table(self, hide_dealer=True):
        print(f"\n{self.player.name}: {self.player.hand_text()}")
        print(f"Your score: {self.player.score()}")

        if hide_dealer:
            print(f"Dealer: {self.dealer.hand[0]}, [HIDDEN]")
        else:
            print(f"Dealer: {self.dealer.hand_text()}")
            print(f"Dealer score: {self.dealer.score()}")

    def choose_power(self):
        print("\n--- POWER SELECTION ---")

        for number, power in enumerate(self.powers, start=1):
            print(f"{number}. {power.name} - {power.description}")

        print("4. No Power")

        while True:
            choice = input("\nChoose a power: ").strip()

            if choice in ("1", "2", "3", "4"):
                break

            print("Please choose 1, 2, 3 or 4.")


