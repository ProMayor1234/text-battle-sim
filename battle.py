import random
import sys

class Player:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def is_alive(self):
        return self.hp > 0

def strike(hero, monster, log):
    damage = hero.attack_power
    monster.hp -= damage
    log.append(f"{hero.name} uses Strike for {damage} damage!")

def heal(hero, log):
    heal_amount = hero.attack_power * 2
    hero.hp = min(hero.hp + heal_amount, hero.max_hp)
    log.append(f"{hero.name} heals for {heal_amount} HP!")

def power_up(hero, log):
    hero.attack_power = int(hero.attack_power * 1.5)
    log.append(f"{hero.name} uses Power Up!")

def cpu_attack(cpu, player, log, last_move):
    log.append(f"{cpu.name} is thinking...")
    if cpu.attack_power < player.attack_power and last_move != "power_up":
        log.append(f"{cpu.name} is choosing to power up!")
        power_up(cpu, log)
        return "power_up"
    elif cpu.hp < player.hp and last_move != "heal" and cpu.hp < cpu.max_hp - cpu.attack_power * 2:
        log.append(f"{cpu.name} is choosing to heal!")
        heal(cpu, log)
        return "heal"
    else:
        log.append(f"{cpu.name} is choosing to attack!")
        strike(cpu, player, log)
        return "strike"

def display_status(player, enemy, log):
    print("\n--- Status ---")
    print(f"{player.name}: HP = {player.hp}/{player.max_hp}, Attack = {player.attack_power}")
    print(f"{enemy.name}: HP = {enemy.hp}/{enemy.max_hp}")
    print("\n--- Log ---")
    for line in log[-4:]:
        print(line)

def main():
    win_streak = 0

    while True:
        # Initialize players
        base_attack = (win_streak + 1) * 10
        p1 = Player("Hero", (win_streak + 1) * 100, base_attack)
        enemy_names = ["Goblin", "Shadow", "DoomBot", "Crimson Fang", "Rogue AI"]
        enemy_attack = random.randint(
            int(base_attack * 0.5),
            int(base_attack * 1.5)
        )
        enemy_hp = (p1.attack_power + p1.hp) - enemy_attack
        p2 = Player(random.choice(enemy_names), enemy_hp, enemy_attack)
        log = ["Battle Start!"]
        global turn
        turn = 0
        game_over = False
        cpu_last_move = None

        while not game_over:
            display_status(p1, p2, log)

            if turn % 2 == 0:  # Player's turn
                # Show current stats before choice
                print(f"\n[Hero HP: {p1.hp}/{p1.max_hp}] [Hero Attack: {p1.attack_power}] [CPU HP: {p2.hp}/{p2.max_hp}]")
                print("\nYour move: 1 = Strike  2 = Heal  3 = Power Up")
                choice = input("Enter your choice: ").strip()
                if choice == "1":
                    strike(p1, p2, log)
                    turn += 1
                elif choice == "2":
                    heal(p1, log)
                    turn += 1
                elif choice == "3":
                    power_up(p1, log)
                    turn += 1
                else:
                    print("Invalid choice. Try again.")
            else:  # CPU's turn
                cpu_last_move = cpu_attack(p2, p1, log, cpu_last_move)
                turn += 1

            # Check for game over
            if not p1.is_alive() or not p2.is_alive():
                game_over = True
                winner = p1 if p1.is_alive() else p2
                log.append(f"{winner.name} wins the battle!")

        # Display game over message
        display_status(p1, p2, log)
        if p1.is_alive():
            print(f"\nYou won! Win streak: {win_streak + 1}")
            win_streak += 1
        else:
            print("\nYou lost! Win streak reset to 0.")
            win_streak = 0

        # Ask to play again
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()