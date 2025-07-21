import random
import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")

font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
class Player:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = int(hp)
        self.max_hp = int(hp)  # Save initial health value
        self.attack_power = int(attack_power)  # default attack power

    def is_alive(self):
        return self.hp > 0

def strike(hero, monster):
    damage = int(hero.attack_power)
    monster.hp -= damage
    print(f"{hero.name} uses Strike for {damage} damage! {monster.name} HP: {max(monster.hp, 0)}")

def heal(hero):
    # Heal amount is half of current attack power (rounded down)
    heal_amount = int(hero.attack_power) // 2
    if heal_amount <= 0:
        heal_amount = 1
    hero.hp = min(hero.hp + heal_amount, hero.max_hp)
    print(f"{hero.name} heals for {heal_amount} HP! {hero.name} HP: {hero.hp}")

def power_up(hero):
    hero.attack_power = int(max(1, hero.attack_power * 1.5))  # Increase attack power by 50%, minimum 1
    print(f"{hero.name} uses Power Up! Attack power is now {hero.attack_power}.")

def hero_attack(hero, monster):
    print("\nChoose your attack:")
    print(f"1. Strike (deal current attack power damage: {hero.attack_power})")
    print(f"2. Heal (+{hero.attack_power // 2} HP)")
    print("3. Power Up (increase your attack power by 50%)")
    choice = input("Enter 1, 2 or 3: ")
    if choice == "1":
        strike(hero, monster)
    elif choice == "2":
        heal(hero)
    elif choice == "3":
        power_up(hero)
    else:
        print("Invalid choice. Defaulting to Strike.")
        strike(hero, monster)

def cpu_attack(cpu, player):
    print(f"\n{cpu.name} is thinking...")
    # If CPU can defeat the player in one hit, always attack
    if cpu.attack_power >= player.hp:
        print(f"{cpu.name}'s Attack ({cpu.attack_power}) can defeat {player.name} (HP {player.hp}). Choosing to attack!")
        strike(cpu, player)
    # Only heal if it will actually increase HP (not already at max or above)
    # and only if CPU HP is not less than player's attack power (would die next turn anyway)
    elif cpu.hp < player.hp and cpu.hp < cpu.max_hp - cpu.attack_power and cpu.hp >= player.attack_power:
        print(f"{cpu.name}'s HP ({cpu.hp}) is lower than {player.name}'s HP ({player.hp}), not at max, and not in immediate danger. Choosing to heal!")
        heal(cpu)
    elif cpu.attack_power < player.attack_power:
        print(f"{cpu.name}'s Attack ({cpu.attack_power}) is lower than {player.name}'s Attack ({player.attack_power}). Choosing to power up!")
        power_up(cpu)
    else:
        print(f"{cpu.name} has good stats. Choosing to attack!")
        strike(cpu, player)

def battle(player1, player2):
    print(f"\n{player1.name} moves first!")
    turn = 0
    while player1.is_alive() and player2.is_alive():
        print(f"\n--- Status ---")
        print(f"{player1.name}: HP = {player1.hp}, Attack = {player1.attack_power}")
        print(f"{player2.name}: HP = {player2.hp}, Attack = {player2.attack_power}")
        if turn % 2 == 0:
            hero_attack(player1, player2)
        else:
            cpu_attack(player2, player1)
        turn += 1
    winner = player1 if player1.is_alive() else player2
    print(f"\n{winner.name} wins the battle!")

def main():
    win_streak = 0
    while True:
        p1_hp = (win_streak + 1) * 100
        p1_attack = (win_streak + 1) * 10
        p1 = Player("Hero", p1_hp, p1_attack)
        enemy_names = ["Goblin", "Shadow", "DoomBot", "Crimson Fang", "Rogue AI"]
        base_attack = (win_streak + 1) * 10
        min_attack = int(base_attack // 2)
        max_attack = int(base_attack + base_attack // 2)
        enemy_attack = random.randint(min_attack, max_attack)
        enemy_hp = int(p1.attack_power + p1.hp - enemy_attack)
        if enemy_hp < 1:
            enemy_hp = 1
        p2 = Player(random.choice(enemy_names), enemy_hp, enemy_attack)
        print("Battle Start!")
        battle(p1, p2)
        if p1.is_alive():
            win_streak += 1
            print(f"Win streak: {win_streak}")
        else:
            win_streak = 0
            print("Your win streak has been reset.")
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with black
            screen.fill((0, 0, 0))

            # Update the display
            pygame.display.flip()

        # Clean exit
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()