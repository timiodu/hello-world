class Power:
    """Parent class for all blackjack powers."""

    name = "Power"
    description = "Base power"

    def __init__(self):
        self.used = False

    def reset(self):
        self.used = False

    def activate(self, player, dealer, deck):
        raise NotImplementedError


class PeekPower(Power):
    """Reveals the dealer's hidden card."""

    name = "Peek"
    description = "Reveal the dealer's hidden card."

    def activate(self, player, dealer, deck):
        if self.used:
            return False

        print(f"\nDealer's hidden card is {dealer.hand[1]}.")

        self.used = True
        return True


class RedrawPower(Power):
    """Replaces the player's most recent card."""

    name = "Redraw"
    description = "Replace your newest card with another card."

    def activate(self, player, dealer, deck):
        if self.used or len(player.hand) < 2:
            return False

        old_card = player.hand.pop()
        new_card = deck.draw()

        player.add_card(new_card)

        print(f"\nRedraw changed {old_card} into {new_card}.")

        self.used = True
        return True


class SafeHitPower(Power):
    """Allows one hit without the risk of going bust."""

    name = "Safe Hit"
    description = "Draw once. If it busts you, the card is cancelled."

    def activate(self, player, dealer, deck):
        if self.used:
            return False

        card = deck.draw()
        player.add_card(card)

        print(f"\nSafe Hit drew {card}.")

        if player.is_bust():
            player.hand.pop()

            print("The card would have busted you!")
            print("Safe Hit cancelled the card.")

        self.used = True
        return True