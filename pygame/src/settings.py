import pygame

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
