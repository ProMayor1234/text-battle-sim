import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 400
WHITE = (255,255,255)
BLACK = (0,0,0)
FONT = pygame.font.SysFont("consolas", 24)
BIGFONT = pygame.font.SysFont("consolas", 32)

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
    log.append(f"{hero.name} uses Strike for {damage} damage! {monster.name} HP: {max(monster.hp, 0)}")

def heal(hero, log):
    heal_amount = hero.attack_power // 2
    hero.hp = min(hero.hp + heal_amount, hero.max_hp)
    log.append(f"{hero.name} heals for {heal_amount} HP! {hero.name} HP: {hero.hp}")

def power_up(hero, log):
    hero.attack_power = int(hero.attack_power * 1.5)
    log.append(f"{hero.name} uses Power Up! Attack power is now {hero.attack_power}.")

def cpu_attack(cpu, player, log):
    log.append(f"{cpu.name} is thinking...")
    if cpu.attack_power >= player.hp:
        log.append(f"{cpu.name}'s Attack ({cpu.attack_power}) can defeat {player.name} (HP {player.hp}). Choosing to attack!")
        strike(cpu, player, log)
    elif cpu.hp < player.hp and cpu.hp < cpu.max_hp - cpu.attack_power and cpu.hp >= player.attack_power:
        log.append(f"{cpu.name}'s HP ({cpu.hp}) is lower than {player.name}'s HP ({player.hp}), not at max, and not in immediate danger. Choosing to heal!")
        heal(cpu, log)
    elif cpu.attack_power < player.attack_power:
        log.append(f"{cpu.name}'s Attack ({cpu.attack_power}) is lower than {player.name}'s Attack ({player.attack_power}). Choosing to power up!")
        power_up(cpu, log)
    else:
        log.append(f"{cpu.name} has good stats. Choosing to attack!")
        strike(cpu, player, log)

def draw_text_lines(surface, lines, x, y, font, color=BLACK):
    for line in lines:
        txt = font.render(line, True, color)
        surface.blit(txt, (x, y))
        y += txt.get_height() + 2

def main():
    win_streak = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Text Battle Simulator (Pygame)")
    clock = pygame.time.Clock()

    while True:
        p1 = Player("Hero", (win_streak + 1) * 100, (win_streak + 1) * 10)
        enemy_names = ["Goblin", "Shadow", "DoomBot", "Crimson Fang", "Rogue AI"]
        base_attack = (win_streak + 1) * 10
        enemy_attack = random.randint(
            int(base_attack - base_attack/2), 
            int(base_attack + base_attack/2)
        )
        enemy_hp = (p1.attack_power + p1.hp) - enemy_attack
        p2 = Player(random.choice(enemy_names), enemy_hp, enemy_attack)
        log = ["Battle Start!"]
        turn = 0
        game_over = False
        winner = None

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and turn % 2 == 0 and not game_over:
                    if event.key == pygame.K_1:
                        strike(p1, p2, log)
                        turn += 1
                    elif event.key == pygame.K_2:
                        heal(p1, log)
                        turn += 1
                    elif event.key == pygame.K_3:
                        power_up(p1, log)
                        turn += 1

            if turn % 2 == 1 and not game_over:
                pygame.time.delay(500)
                cpu_attack(p2, p1, log)
                turn += 1

            if not p1.is_alive() or not p2.is_alive():
                game_over = True
                winner = p1 if p1.is_alive() else p2
                log.append(f"{winner.name} wins the battle!")

            screen.fill(WHITE)
            status_lines = [
                f"{p1.name}: HP = {p1.hp}, Attack = {p1.attack_power}",
                f"{p2.name}: HP = {p2.hp}, Attack = {p2.attack_power}",
                "",
                "Your move: 1=Strike  2=Heal  3=Power Up"
            ]
            draw_text_lines(screen, status_lines, 20, 20, FONT)
            draw_text_lines(screen, log[-7:], 20, 150, FONT)
            if game_over:
                end_msg = f"Win streak: {win_streak+1 if p1.is_alive() else 0}"
                txt = BIGFONT.render(end_msg, True, (0,128,0) if p1.is_alive() else (200,0,0))
                screen.blit(txt, (20, HEIGHT-60))
                txt2 = FONT.render("Press [SPACE] to play again or close window to quit.", True, BLACK)
                screen.blit(txt2, (20, HEIGHT-30))
            pygame.display.flip()
            clock.tick(30)

            if game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if p1.is_alive():
                        win_streak += 1
                    else:
                        win_streak = 0
                    pygame.time.wait(300)
                    break

if __name__ == "__main__":
    main()