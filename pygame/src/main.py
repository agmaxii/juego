import pygame
import sys
import random
from player import Player
from zombie import Zombie
from powerup import PowerUp
from utils import draw_text, button, read_high_scores, write_high_scores
from settings import *

def main_menu():
    global current_skin

    menu = True
    high_scores = read_high_scores()

    while menu:
        screen.blit(start_screen_background, (0, 0))
        button("Comenzar", 350, 400, 100, 50, WHITE, RED, main)
        button("Opciones", 350, 470, 100, 50, WHITE, RED, options_menu)
        button("Salir", 350, 540, 100, 50, WHITE, RED, quit_game)
        draw_text("High Scores:", small_font, WHITE, screen, screen_width // 2, 150)

        for i, high_score in enumerate(high_scores):
            draw_text(f"{i+1}. {high_score}", small_font, WHITE, screen, screen_width // 2, 180 + i * 30)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def options_menu():
    global current_skin

    options = True

    while options:
        screen.fill(BLACK)
        draw_text("Seleccione su Skin", font, WHITE, screen, screen_width // 2, 50)
        
        for i, preview in enumerate(skin_previews):
            x = 150 + i * 200
            y = 200
            screen.blit(preview, (x, y))
            if player_skins[i] == current_skin:
                pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 110, 110), 3)

        draw_text("Para volver al menú toca la tecla ESCAPE", small_font, WHITE, screen, screen_width // 2, screen_height - 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, preview in enumerate(skin_previews):
                    x = 150 + i * 200
                    y = 200
                    if x <= mouse_x <= x + 100 and y <= mouse_y <= y + 100:
                        set_skin(player_skins[i])

def set_skin(skin):
    global current_skin
    current_skin = skin

def show_game_over_screen(score):
    screen.fill(BLACK)
    draw_text("Game Over", font, WHITE, screen, screen_width // 2, screen_height // 2)
    draw_text(f"Score: {score}", small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 50)

    write_high_scores(score)
    high_scores = read_high_scores()

    draw_text("High Scores:", small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 100)
    for i, high_score in enumerate(high_scores):
        draw_text(f"{i + 1}. {high_score}", small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 130 + i * 30)

    pygame.display.flip()
    pygame.time.wait(3000)
    main_menu()

def main():
    global all_sprites, zombies, bullets, powerups, current_skin

    all_sprites = pygame.sprite.Group()
    zombies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    player = Player(current_skin)
    all_sprites.add(player)

    for i in range(8):
        zombie = Zombie()
        all_sprites.add(zombie)
        zombies.add(zombie)

    running = True
    double_points = False
    double_points_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets)
                    shoot_sound.play()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(zombies, bullets, True, True)
        for hit in hits:
            player.score += 2 if double_points else 1
            zombie = Zombie()
            all_sprites.add(zombie)
            zombies.add(zombie)
            if random.random() > 0.9:
                power_type = random.choice(["speed", "double_points"])
                powerup = PowerUp(hit.rect.center, power_type)
                all_sprites.add(powerup)
                powerups.add(powerup)

        if double_points and pygame.time.get_ticks() - double_points_timer > 10000:
            double_points = False

        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            if powerup.type == "speed":
                player.speed += 2
                pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
            elif powerup.type == "double_points":
                double_points = True
                double_points_timer = pygame.time.get_ticks()

        for event in pygame.event.get(pygame.USEREVENT + 1):
            if event.type == pygame.USEREVENT + 1:
                player.speed -= 2

        hits = pygame.sprite.spritecollide(player, zombies, True)
        for hit in hits:
            player.lives -= 1
            zombie = Zombie()
            all_sprites.add(zombie)
            zombies.add(zombie)
            if player.lives == 0:
                running = False
                show_game_over_screen(player.score)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        draw_text(f"Score: {player.score}", small_font, WHITE, screen, 70, 20)
        draw_text(f"Lives: {player.lives}", small_font, WHITE, screen, 70, 60)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
