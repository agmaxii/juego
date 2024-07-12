import pygame
import math
from settings import screen_width, screen_height, current_skin, WHITE
from bullets import Bullet

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

    def shoot(self, all_sprites, bullets):
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
