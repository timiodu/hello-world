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

        if choice == "4":
            return None

        selected_power = self.powers[int(choice) - 1]
        selected_power.reset()

        return selected_power

    def player_turn(self, deck, power):
        while not self.player.is_bust():
            self.show_table()

            if power and not power.used:
                answer = input(
                    f"\nUse {power.name}? [Y/N]: "
                ).strip().lower()

                if answer == "y":
                    power.activate(self.player, self.dealer, deck)
                    self.show_table()

            action = self.player.choose_action()

            if action == "s":
                break

            self.player.add_card(deck.draw())

    def decide_winner(self):
        player_score = self.player.score()
        dealer_score = self.dealer.score()

        if self.player.is_bust():
            return "dealer"

        if self.dealer.is_bust():
            return "player"

        if player_score > dealer_score:
            return "player"

        if dealer_score > player_score:
            return "dealer"

        return "draw"
    
    def play_round(self):
        print("\n" + "=" * 45)
        print(f"ROUND {self.round_number}")
        print("=" * 45)

        deck = Deck()
        self.reset_hands()
        self.deal_starting_cards(deck)

        power = self.choose_power() if self.round_number >= 2 else None

        self.player_turn(deck, power)

        if not self.player.is_bust():
            self.dealer.play(deck)

        self.show_table(hide_dealer=False)
        result = self.decide_winner()

        if result == "player":
            self.player.round_wins += 1
            print("\nYOU WON THE ROUND!")

        elif result == "dealer":
            print("\nDealer won the round.")

        else:
            print("\nThe round was a draw.")

        save_result(
            self.player.name,
            self.round_number,
            self.player.score(),
            self.dealer.score(),
            result
        )

        return result

    def run(self):
        print(f"\nWelcome to Power Blackjack, {self.player.name}!")
        print("There are three rounds.")
        print("Round 1 is normal blackjack.")
        print("Special powers unlock in rounds 2 and 3.")

        for number in range(1, 4):
            self.round_number = number
            self.play_round()

        print("\n" + "=" * 45)
        print("FINAL RESULTS")
        print("=" * 45)

        print(f"You won {self.player.round_wins}/3 rounds.")

        if self.player.round_wins == 3:
            print("\nJACKPOT! You won every round and earned the payout!")
        else:
            print("\nYou did not win all three rounds.")

    def clean_player_name(name):
        return re.sub(r"\s+", " ", name.strip())

    def valid_player_name(name):
        return re.fullmatch(NAME_PATTERN, name) is not None

    def get_player_name():
        while True:
            name = clean_player_name(input("Enter player name: "))

            if valid_player_name(name):
                return name

            print("Name must contain 2-20 characters.")
            print("Letters, numbers, spaces, _ and - are allowed.")

    def load_history():
        try:
            with open(
            HISTORY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
                return list(csv.DictReader(file))

        except FileNotFoundError:
            return []

def save_result(name, round_number, player_score, dealer_score, result):
    history = load_history()

    with open(
        HISTORY_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        if len(history) == 0:
            writer.writerow([
                "Player",
                "Round",
                "Player Score",
                "Dealer Score",
                "Result"
            ])

        writer.writerow([
            name,
            round_number,
            player_score,
            dealer_score,
            result
        ])

def show_previous_games():
    history = load_history()

    if not history:
        print("\nNo previous game history found.")
        return

    print("\n--- RECENT GAME HISTORY ---")

    for result in history[-5:]:
        print(
            f"{result['Player']} | Round {result['Round']} | "
            f"{result['Result'].upper()}"
        )

def main():
    print("=" * 45)
    print("POWER BLACKJACK")
    print("=" * 45)

    show_previous_games()

    name = get_player_name()
    game = BlackjackGame(name)

    game.run()

if __name__ == "__main__":
    main()



