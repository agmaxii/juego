import pygame
import random
import sys
import math
import csv

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Zombie Nation")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fuentes
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Cargar la imagen del fondo de la pantalla de inicio
start_screen_background = pygame.image.load("./src/assets/imagenes/BCRK2.png").convert()

# Cargar la imagen del fondo
background = pygame.image.load("./src/assets/imagenes/roadd.png").convert()

# Cargar imágenes de los power-ups
speed_image = pygame.image.load("./src/assets/imagenes/speed.png").convert_alpha()
double_points_image = pygame.image.load("./src/assets/imagenes/coin.png").convert_alpha()

# Cargar skins del jugador
player_skins = ["./src/assets/imagenes/halo.png", "./src/assets/imagenes/h2.png"]
skin_previews = [pygame.image.load(skin).convert_alpha() for skin in player_skins]
skin_previews = [pygame.transform.scale(preview, (100, 100)) for preview in skin_previews]
current_skin = player_skins[0]

pygame.mixer.init()

shoot_sound = pygame.mixer.Sound("./src/assets/sonidos/bala.mp3")





# Archivo CSV para almacenar los puntajes más altos
high_score_file = 'high_scores.csv'

# Leer los puntajes más altos desde el archivo CSV
def read_high_scores():
    try:
        with open(high_score_file, mode='r') as file:
            reader = csv.reader(file)
            high_scores = sorted([int(score[0]) for score in reader], reverse=True)[:3]
            return high_scores
    except (FileNotFoundError, StopIteration):
        return []

# Escribir los puntajes más altos en el archivo CSV
def write_high_scores(new_score):
    high_scores = read_high_scores()
    high_scores.append(new_score)
    high_scores = sorted(high_scores, reverse=True)[:3]
    with open(high_score_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for score in high_scores:
            writer.writerow([score])

# Clase del Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, skin):
        super().__init__()
        self.original_image = pygame.image.load(skin).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.lives = 3
        self.score = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction_x = mouse_x - self.rect.centerx
        direction_y = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-direction_y, direction_x))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction_x = mouse_x - self.rect.centerx
        direction_y = mouse_y - self.rect.centery
        length = (direction_x**2 + direction_y**2)**0.5
        if length != 0:
            direction_x /= length
            direction_y /= length
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction_x, direction_y)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase del Zombie
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./src/assets/imagenes/zombie.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

# Clase de las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = 10

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
        if self.rect.bottom < 0 or self.rect.left > screen_width or self.rect.right < 0 or self.rect.top > screen_height:
            self.kill()

# Clase de los elementos especiales (power-ups)
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, power_type):
        super().__init__()
        self.type = power_type
        if self.type == "speed":
            self.image = speed_image
        elif self.type == "double_points":
            self.image = double_points_image
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        pass

# Función para dibujar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Función para crear botones en la pantalla
def button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    draw_text(text, small_font, BLACK, screen, x + (width / 2), y + (height / 2))

# Función para mostrar el menú principal
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

        # Manejo de eventos en el menú principal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

# Función para mostrar el menú de opciones
def options_menu():
    global current_skin

    options = True
    skin_images = [pygame.image.load(skin).convert_alpha() for skin in player_skins]
    skin_images = [pygame.transform.scale(img, (100, 100)) for img in skin_images]
    
    while options:
        screen.fill(BLACK)
        draw_text("Seleccione su Skin", font, WHITE, screen, screen_width // 2, 50)
        
        # Mostrar previsualización de skins
        for i, preview in enumerate(skin_previews):
            x = 150 + i * 200  # Espaciado horizontal para las imágenes de skins
            y = 200
            screen.blit(preview, (x, y))
            if player_skins[i] == current_skin:
                pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 110, 110), 3)  # Marco alrededor de la skin seleccionada

        draw_text("Para volver al menú toca la tecla ESCAPE", small_font, WHITE, screen, screen_width // 2, screen_height - 50)

        pygame.display.flip()

        # Manejo de eventos en el menú de opciones
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

# Función para establecer el skin del jugador
def set_skin(skin):
    global current_skin
    current_skin = skin

# Función para mostrar la pantalla de Game Over
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

# Función principal del juego
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
                    player.shoot()
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
