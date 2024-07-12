import pygame
import csv
from settings import small_font, WHITE, BLACK, high_score_file

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
        pygame.draw.rect(pygame.display.get_surface(), active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(pygame.display.get_surface(), inactive_color, (x, y, width, height))

    draw_text(text, small_font, BLACK, pygame.display.get_surface(), x + (width / 2), y + (height / 2))
