import pygame
import random


class Base_L:
    def __init__(self, screen, health):
        self.screen = screen
        self.health = health
        self.image = pygame.image.load("pictures/light_castle.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.gold = 0
        self.timer = 0

    def output(self):
        self.screen.blit(self.image, self.rect)


class Base_R(Base_L):
    def __init__(self, screen, health):
        super().__init__(screen, health)
        self.image = pygame.image.load("pictures/dark_castle.png")
        self.rect.bottomright = self.screen_rect.bottomright


# Юниты


class Units_1(pygame.sprite.Sprite):
    def __init__(self, screen, unit_type, health, speed, attack, armor):
        super(Units_1, self).__init__()
        self.screen = screen
        self.health = health
        self.speed = speed
        self.attack = attack
        self.armor = armor
        self.ready = 0
        self.unit_type = unit_type
        self.image = pygame.image.load(unit_type)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.x = self.rect.centerx


    def output(self):
        self.screen.blit(self.image, self.rect)

    def move(self):
        self.x += self.speed
        self.rect.centerx = self.x


class Arrows(pygame.sprite.Sprite):

    def __init__(self, screen, unit, size, color):
        """создание снаряда"""
        super(Arrows, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(size)
        self.color = (color)
        self.speed = 5 + random.randint(0, 5)
        self.unit = unit
        self.rect.centery = unit.rect.centery
        self.rect.centerx = unit.rect.centerx
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """перемещение снаряда"""
        self.x += self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        """отображение на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Units_2(pygame.sprite.Sprite):
    def __init__(self, screen, unit_type, health, speed, attack, armor):
        super(Units_2, self).__init__()
        self.screen = screen
        self.health = health
        self.speed = speed
        self.attack = attack
        self.armor = armor
        self.unit_type = unit_type
        self.ready = 0
        self.image = pygame.image.load(unit_type)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomright = self.screen_rect.bottomright
        self.x = self.rect.centerx

    def output(self):
        self.screen.blit(self.image, self.rect)

    def move(self):
        self.x -= self.speed
        self.rect.centerx = self.x


class Arrows2(pygame.sprite.Sprite):
    def __init__(self, screen, unit, size, color):
        """создание снаряда"""
        super(Arrows2, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(size)
        self.color = (color)
        self.speed = 5 + random.randint(0, 5)
        self.unit = unit
        self.rect.centery = unit.rect.centery
        self.rect.centerx = unit.rect.centerx
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """перемещение снаряда"""
        self.x -= self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        """отображение на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Banner(pygame.sprite.Sprite):
    def __init__(self, screen, banner_type):
        super(Banner, self).__init__()
        self.screen = screen
        self.banner_type = banner_type
        self.image = pygame.image.load(banner_type)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = self.rect.centerx

    def output(self):
        self.screen.blit(self.image, self.rect)
# Текст


class Text:
    def __init__(self, screen, text, x, y, font, size):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, 1, self.text_color)
        self.rect = self.text.get_rect(center=(x, y))

    def output(self, text):
        self.text = self.font.render(text, 1, self.text_color)
        self.screen.blit(self.text, self.rect)


class Text2:
    def __init__(self, screen, text, object):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (0,200,100)
        self.font = pygame.font.SysFont("Times New Roman", 18)
        self.text = self.font.render(text, 1, self.text_color)
        self.rect = self.text.get_rect()
        self.unit = object
        self.rect.centerx = object.rect.centerx
        self.rect.bottom = object.rect.top

    def output(self):
        self.screen.blit(self.text, self.rect)

