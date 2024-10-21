import random


class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 20

    def attack(self, other):
        damage = self.attack_power
        other.health -= damage
        print(f"{self.name} attacks {other.name} for {damage} damage!")

    def heal(self):
        heal_amount = min(20, self.health)
        self.health += heal_amount
        print(f"{self.name} heals for {heal_amount} points.")

    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self):
        self.player = Hero("Player")
        self.computer = Hero("Computer")

    def display_status(self):
        print(f"\n{self.player.name}'s health: {self.player.health}")
        print(f"{self.computer.name}'s health: {self.computer.health}")

    def player_turn(self):
        action = input("Choose your action (attack/heal): ").lower()
        if action == "attack":
            self.player.attack(self.computer)
        elif action == "heal":
            self.player.heal()
        else:
            print("Invalid action. Please choose attack or heal.")

    def computer_turn(self):
        actions = ["attack", "heal"]
        action = random.choice(actions)
        if action == "attack":
            self.computer.attack(self.player)
        else:
            self.computer.heal()

    def check_winner(self):
        if not self.player.is_alive():
            return self.computer
        elif not self.computer.is_alive():
            return self.player
        return None

    def game_over(self):
        winner = self.check_winner()
        if winner == self.player:
            print("Player wins!")
        elif winner == self.computer:
            print("Computer wins!")
        else:
            print("It's a draw!")

    def start(self):
        round_num = 1
        while self.player.is_alive() and self.computer.is_alive():
            print(f"\nRound {round_num}:")
            self.display_status()
            self.player_turn()
            if not self.computer.is_alive():
                break
            self.computer_turn()
            round_num += 1

        self.game_over()


def main():
    game = Game()
    play_again = "yes"

    while play_again.lower() == "yes":
        game.start()
        play_again = input("\nDo you want to play again? (yes/no): ").lower()

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()