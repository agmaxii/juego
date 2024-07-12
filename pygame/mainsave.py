import pygame  # Importa la biblioteca Pygame para la creación de juegos
import random  # Importa el módulo random para generar números aleatorios
import sys     # Importa el módulo sys para interactuar con el sistema operativo
import math    # Importa el módulo math para operaciones matemáticas
import csv     # Importa el módulo csv para leer y escribir archivos CSV

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla del juego
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))  # Crea la pantalla del juego
pygame.display.set_caption("Zombie Nation")  # Establece el título de la ventana del juego

# Definición de colores usando tuplas RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Definición de fuentes para texto
font = pygame.font.Font(None, 74)    # Fuente grande para títulos
small_font = pygame.font.Font(None, 36)  # Fuente pequeña para texto secundario

# Cargar la imagen de fondo para la pantalla de inicio
start_screen_background = pygame.image.load("./src/assets/imagenes/BCRK2.png").convert()

# Cargar la imagen de fondo del juego
background = pygame.image.load("./src/assets/imagenes/roadd.png").convert()

# Cargar imágenes de los power-ups
speed_image = pygame.image.load("./src/assets/imagenes/speed.png").convert_alpha()
double_points_image = pygame.image.load("./src/assets/imagenes/coin.png").convert_alpha()

# Cargar skins del jugador
player_skins = ["./src/assets/imagenes/halo.png", "./src/assets/imagenes/h2.png"]
skin_previews = [pygame.image.load(skin).convert_alpha() for skin in player_skins]  # Carga las imágenes de las skins
skin_previews = [pygame.transform.scale(preview, (100, 100)) for preview in skin_previews]  # Escala las previsualizaciones a 100x100 píxeles
current_skin = player_skins[0]  # Establece la skin actual del jugador

# Archivo CSV para almacenar los puntajes más altos
high_score_file = 'high_scores.csv'

# Leer los puntajes más altos desde el archivo CSV
def read_high_scores():
    try:
        with open(high_score_file, mode='r') as file:
            reader = csv.reader(file)
            high_scores = sorted([int(score[0]) for score in reader], reverse=True)[:3]  # Lee y ordena los puntajes más altos
            return high_scores
    except (FileNotFoundError, StopIteration):
        return []

# Escribir los puntajes más altos en el archivo CSV
def write_high_scores(new_score):
    high_scores = read_high_scores()
    high_scores.append(new_score)
    high_scores = sorted(high_scores, reverse=True)[:3]  # Agrega y ordena el nuevo puntaje en los más altos
    with open(high_score_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for score in high_scores:
            writer.writerow([score])

# Clase del Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, skin):
        super().__init__()
        self.original_image = pygame.image.load(skin).convert_alpha()  # Carga la imagen de la skin del jugador
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))  # Escala la imagen a 50x50 píxeles
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)  # Posiciona al jugador en el centro de la pantalla
        self.speed = 5  # Velocidad inicial del jugador
        self.lives = 3  # Número de vidas del jugador
        self.score = 0  # Puntaje inicial del jugador

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtiene la posición del ratón
        direction_x = mouse_x - self.rect.centerx  # Calcula la dirección en el eje X hacia el ratón
        direction_y = mouse_y - self.rect.centery  # Calcula la dirección en el eje Y hacia el ratón
        angle = math.degrees(math.atan2(-direction_y, direction_x))  # Calcula el ángulo de rotación hacia el ratón
        self.image = pygame.transform.rotate(self.original_image, angle)  # Rota la imagen del jugador hacia el ratón
        self.rect = self.image.get_rect(center=self.rect.center)  # Actualiza el rectángulo de colisión del jugador

        keys = pygame.key.get_pressed()  # Obtiene las teclas presionadas
        if keys[pygame.K_a]:  # Movimiento izquierda
            self.rect.x -= self.speed
        if keys[pygame.K_d]:  # Movimiento derecha
            self.rect.x += self.speed
        if keys[pygame.K_w]:  # Movimiento arriba
            self.rect.y -= self.speed
        if keys[pygame.K_s]:  # Movimiento abajo
            self.rect.y += self.speed

        # Limita al jugador dentro de los límites de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtiene la posición del ratón
        direction_x = mouse_x - self.rect.centerx  # Calcula la dirección en el eje X hacia el ratón
        direction_y = mouse_y - self.rect.centery  # Calcula la dirección en el eje Y hacia el ratón
        length = (direction_x**2 + direction_y**2)**0.5  # Calcula la distancia al ratón
        if length != 0:
            direction_x /= length
            direction_y /= length
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction_x, direction_y)  # Crea una bala
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase del Zombie
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./src/assets/imagenes/zombie.png").convert_alpha()  # Carga la imagen del zombie
        self.image = pygame.transform.scale(self.image, (50, 50))  # Escala la imagen a 50x50 píxeles
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)  # Posiciona al zombie en X aleatoriamente
        self.rect.y = random.randrange(-100, -40)  # Posiciona al zombie arriba de la pantalla aleatoriamente
        self.speedy = random.randrange(1, 4)  # Velocidad vertical aleatoria del zombie

    def update(self):
        self.rect.y += self.speedy  # Mueve al zombie hacia abajo
        if self.rect.top > screen_height + 10:  # Si el zombie pasa la parte inferior de la pantalla
            self.rect.x = random.randrange(screen_width - self.rect.width)  # Reposiciona al zombie en X aleatoriamente
            self.rect.y = random.randrange(-100, -40)  # Reposiciona al zombie arriba de la pantalla aleatoriamente
            self.speedy = random.randrange(1, 4)  # Cambia la velocidad vertical aleatoria

# Clase de las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # Crea una superficie para la bala
        self.image.fill(WHITE)  # Rellena la superficie con color blanco
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = 10  # Velocidad de la bala

    def update(self):
        self.rect.x += self.dir_x * self.speed  # Mueve la bala en X según su dirección y velocidad
        self.rect.y += self.dir_y * self.speed  # Mueve la bala en Y según su dirección y velocidad
        if self.rect.bottom < 0 or self.rect.left > screen_width or self.rect.right < 0 or self.rect.top > screen_height:
            self.kill()  # Elimina la bala si sale de la pantalla

# Clase de los elementos especiales (power-ups)
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, power_type):
        super().__init__()
        self.type = power_type  # Tipo de power-up
        if self.type == "speed":
            self.image = speed_image  # Imagen de power-up de velocidad
        elif self.type == "double_points":
            self.image = double_points_image  # Imagen de power-up de puntos dobles
        self.rect = self.image.get_rect()
        self.rect.center = center  # Centro del power-up en la pantalla

    def update(self):
        pass  # No hace nada en la actualización (los power-ups son estáticos)

# Función para dibujar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)  # Renderiza el texto
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)  # Dibuja el texto en la superficie

# Función para crear botones en la pantalla
def button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()  # Obtiene la posición del ratón
    click = pygame.mouse.get_pressed()  # Obtiene el estado del botón del ratón

    # Dibuja el botón en estado inactivo o activo
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:  # Si se hace clic en el botón
            action()  # Ejecuta la función asociada al botón
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    draw_text(text, small_font, BLACK, screen, x + (width / 2), y + (height / 2))  # Dibuja el texto en el botón

# Función para mostrar el menú principal
def main_menu():
    global current_skin

    menu = True
    high_scores = read_high_scores()  # Lee los puntajes más altos almacenados

    while menu:
        screen.blit(start_screen_background, (0, 0))  # Dibuja el fondo de la pantalla de inicio
        button("Comenzar", 350, 400, 100, 50, WHITE, RED, main)  # Botón para comenzar el juego
        button("Opciones", 350, 470, 100, 50, WHITE, RED, options_menu)  # Botón para ir al menú de opciones
        button("Salir", 350, 540, 100, 50, WHITE, RED, quit_game)  # Botón para salir del juego

        draw_text("High Scores:", small_font, WHITE, screen, screen_width // 2, 150)  # Muestra el título de los puntajes más altos

        for i, high_score in enumerate(high_scores):
            draw_text(f"{i+1}. {high_score}", small_font, WHITE, screen, screen_width // 2, 180 + i * 30)  # Muestra los puntajes más altos

        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():  # Manejo de eventos del juego
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                quit_game()  # Sale del juego

# Función para mostrar el menú de opciones
def options_menu():
    global current_skin

    options = True
    skin_images = [pygame.image.load(skin).convert_alpha() for skin in player_skins]  # Carga las imágenes de las skins
    skin_images = [pygame.transform.scale(img, (100, 100)) for img in skin_images]  # Escala las imágenes a 100x100 píxeles
    
    while options:
        screen.fill(BLACK)  # Limpia la pantalla con color negro
        draw_text("Seleccione su Skin", font, WHITE, screen, screen_width // 2, 50)  # Muestra el título del menú de opciones
        
        # Muestra las previsualizaciones de las skins
        for i, preview in enumerate(skin_previews):
            x = 150 + i * 200  # Espaciado horizontal para las imágenes de skins
            y = 200
            screen.blit(preview, (x, y))
            if player_skins[i] == current_skin:
                pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 110, 110), 3)  # Marco alrededor de la skin seleccionada

        draw_text("Para volver al menú toca la tecla ESCAPE", small_font, WHITE, screen, screen_width // 2, screen_height - 50)

        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():  # Manejo de eventos del juego
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                quit_game()  # Sale del juego
            elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_ESCAPE:  # Si la tecla es ESCAPE
                    main_menu()  # Vuelve al menú principal
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic con el ratón
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtiene la posición del ratón
                for i, preview in enumerate(skin_previews):
                    x = 150 + i * 200
                    y = 200
                    if x <= mouse_x <= x + 100 and y <= mouse_y <= y + 100:
                        set_skin(player_skins[i])  # Establece la skin seleccionada para el jugador

# Función para establecer la skin del jugador
def set_skin(skin):
    global current_skin
    current_skin = skin  # Establece la skin actual del jugador

# Función para mostrar la pantalla de Game Over
def show_game_over_screen(score):
    screen.fill(BLACK)  # Limpia la pantalla con color negro
    draw_text("Game Over", font, WHITE, screen, screen_width // 2, screen_height // 2)  # Muestra "Game Over"
    draw_text(f"Score: {score}", small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 50)  # Muestra el puntaje obtenido

    write_high_scores(score)  # Escribe el puntaje en el archivo CSV
    high_scores = read_high_scores()  # Lee los puntajes más altos almacenados

    draw_text("High Scores:", small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 100)  # Muestra el título de los puntajes más altos
    for i, high_score in enumerate(high_scores):
        draw_text(f"{i + 1}. {high_score}", small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 130 + i * 30)  # Muestra los puntajes más altos

    pygame.display.flip()  # Actualiza la pantalla
    pygame.time.wait(3000)  # Espera 3 segundos antes de volver al menú principal
    main_menu()  # Vuelve al menú principal

# Función principal del juego
def main():
    global all_sprites, zombies, bullets, powerups, current_skin

    all_sprites = pygame.sprite.Group()  # Grupo para todos los sprites (jugador, zombies, balas, power-ups)
    zombies = pygame.sprite.Group()  # Grupo para los zombies
    bullets = pygame.sprite.Group()  # Grupo para las balas
    powerups = pygame.sprite.Group()  # Grupo para los power-ups

    player = Player(current_skin)  # Crea al jugador con la skin actual
    all_sprites.add(player)  # Añade al jugador al grupo de sprites

    for i in range(8):
        zombie = Zombie()  # Crea un zombie
        all_sprites.add(zombie)  # Añade el zombie al grupo de sprites
        zombies.add(zombie)  # Añade el zombie al grupo de zombies

    running = True
    double_points = False  # Indicador de puntos dobles activados o desactivados
    double_points_timer = 0  # Temporizador para los puntos dobles

    while running:
        for event in pygame.event.get():  # Manejo de eventos del juego
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                running = False  # Sale del bucle principal del juego
            elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_SPACE:  # Si la tecla es ESPACIO
                    player.shoot()  # El jugador dispara una bala

        all_sprites.update()  # Actualiza todos los sprites

        # Colisión entre balas y zombies
        hits = pygame.sprite.groupcollide(zombies, bullets, True, True)  # Detecta las colisiones y elimina los sprites impactados
        for hit in hits:
            player.score += 2 if double_points else 1  # Suma puntos al jugador (x2 si están activados los puntos dobles)
            zombie = Zombie()  # Crea un nuevo zombie
            all_sprites.add(zombie)  # Añade el zombie al grupo de sprites
            zombies.add(zombie)  # Añade el zombie al grupo de zombies
            if random.random() > 0.9:  # Probabilidad del 10% de que aparezca un power-up
                power_type = random.choice(["speed", "double_points"])  # Elige aleatoriamente el tipo de power-up
                powerup = PowerUp(hit.rect.center, power_type)  # Crea un power-up en la posición del zombie eliminado
                all_sprites.add(powerup)  # Añade el power-up al grupo de sprites
                powerups.add(powerup)  # Añade el power-up al grupo de power-ups

        # Desactiva los puntos dobles después de 10 segundos
        if double_points and pygame.time.get_ticks() - double_points_timer > 10000:
            double_points = False

        # Colisión entre el jugador y los power-ups
        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)  # Detecta las colisiones y elimina los power-ups impactados
        for powerup in powerup_hits:
            if powerup.type == "speed":  # Si el power-up es de velocidad
                player.speed += 2  # Aumenta la velocidad del jugador
                pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # Activa un temporizador para restablecer la velocidad original
            elif powerup.type == "double_points":  # Si el power-up son puntos dobles
                double_points = True  # Activa los puntos dobles
                double_points_timer = pygame.time.get_ticks()  # Reinicia el temporizador de puntos dobles

        # Temporizador para restablecer la velocidad original del jugador
        for event in pygame.event.get(pygame.USEREVENT + 1):
            if event.type == pygame.USEREVENT + 1:
                player.speed -= 2  # Restablece la velocidad del jugador

        # Colisión entre el jugador y los zombies
        hits = pygame.sprite.spritecollide(player, zombies, True)  # Detecta las colisiones entre el jugador y los zombies
        for hit in hits:
            player.lives -= 1  # Reduce las vidas del jugador
            zombie = Zombie()  # Crea un nuevo zombie
            all_sprites.add(zombie)  # Añade el zombie al grupo de sprites
            zombies.add(zombie)  # Añade el zombie al grupo de zombies
            if player.lives == 0:  # Si el jugador se queda sin vidas
                running = False  # Termina el juego
                show_game_over_screen(player.score)  # Muestra la pantalla de Game Over con el puntaje obtenido

        screen.blit(background, (0, 0))  # Dibuja el fondo de la pantalla de juego
        all_sprites.draw(screen)  # Dibuja todos los sprites en la pantalla

        draw_text(f"Score: {player.score}", small_font, WHITE, screen, 70, 20)  # Muestra el puntaje del jugador
        draw_text(f"Lives: {player.lives}", small_font, WHITE, screen, 70, 60)  # Muestra las vidas restantes del jugador

        pygame.display.flip()  # Actualiza la pantalla
        pygame.time.Clock().tick(60)  # Controla la velocidad de fotogramas (60 FPS)

    pygame.quit()  # Sale de Pygame
    sys.exit()  # Sale del programa

def quit_game():
    pygame.quit()  # Sale de Pygame
    sys.exit()  # Sale del programa

if __name__ == "__main__":
    main_menu()  # Inicia el juego mostrando el menú principal
