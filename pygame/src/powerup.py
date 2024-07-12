import pygame
from settings import speed_image, double_points_image

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
