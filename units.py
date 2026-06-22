import pygame
import random
import math


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
        self.cooldowns = [0, 0, 0]
        self.gold_upgrade = 0

    def output(self):
        self.screen.blit(self.image, self.rect)


class Base_R(Base_L):
    def __init__(self, screen, health):
        super().__init__(screen, health)
        self.image = pygame.image.load("pictures/dark_castle.png")
        self.rect.bottomright = self.screen_rect.bottomright


class Units_1(pygame.sprite.Sprite):
    _LUNGE = 14   # рывок вправо (направление атаки)

    def __init__(self, screen, unit_type, health, speed, attack, armor):
        super(Units_1, self).__init__()
        self.screen = screen
        self.health = health
        self.max_health = health
        self.hit_timer = 0
        self.attack_timer = 0
        self.is_dying = False
        self.dying_timer = 0
        self.speed = speed
        self.attack = attack
        self.armor = armor
        self.unit_type = unit_type
        self.image = pygame.image.load(unit_type)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.x = self.rect.centerx

    def output(self):
        t = pygame.time.get_ticks()
        y_bob = int(math.sin(t * self.speed * 0.006) * 4) if not self.is_dying else 0
        x_lunge = self._LUNGE if self.attack_timer > 4 else 0
        pos = (self.rect.x + x_lunge, self.rect.y + y_bob)
        self.screen.blit(self.image, pos)
        if self.is_dying:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((180, 0, 0, 180))
            self.screen.blit(flash, pos)
        elif self.hit_timer > 0:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((255, 50, 50, 140))
            self.screen.blit(flash, pos)
            self.hit_timer -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1

    def move(self):
        if not self.is_dying:
            self.x += self.speed
            self.rect.centerx = self.x


class Arrows(pygame.sprite.Sprite):

    def __init__(self, screen, unit, size, color):
        super(Arrows, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(size)
        self.color = color
        self.speed = 5 + random.randint(0, 5)
        self.unit = unit
        self.rect.centery = unit.rect.centery
        self.rect.centerx = unit.rect.centerx
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Units_2(pygame.sprite.Sprite):
    _LUNGE = -14  # рывок влево (направление атаки)

    def __init__(self, screen, unit_type, health, speed, attack, armor):
        super(Units_2, self).__init__()
        self.screen = screen
        self.health = health
        self.max_health = health
        self.hit_timer = 0
        self.attack_timer = 0
        self.is_dying = False
        self.dying_timer = 0
        self.speed = speed
        self.attack = attack
        self.armor = armor
        self.unit_type = unit_type
        self.image = pygame.image.load(unit_type)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomright = self.screen_rect.bottomright
        self.x = self.rect.centerx

    def output(self):
        t = pygame.time.get_ticks()
        y_bob = int(math.sin(t * self.speed * 0.006) * 4) if not self.is_dying else 0
        x_lunge = self._LUNGE if self.attack_timer > 4 else 0
        pos = (self.rect.x + x_lunge, self.rect.y + y_bob)
        self.screen.blit(self.image, pos)
        if self.is_dying:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((180, 0, 0, 180))
            self.screen.blit(flash, pos)
        elif self.hit_timer > 0:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((255, 50, 50, 140))
            self.screen.blit(flash, pos)
            self.hit_timer -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1

    def move(self):
        if not self.is_dying:
            self.x -= self.speed
            self.rect.centerx = self.x


class Arrows2(pygame.sprite.Sprite):
    def __init__(self, screen, unit, size, color):
        super(Arrows2, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(size)
        self.color = color
        self.speed = 5 + random.randint(0, 5)
        self.unit = unit
        self.rect.centery = unit.rect.centery
        self.rect.centerx = unit.rect.centerx
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
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


MINER_TYPE_L = "miner_l"
MINER_TYPE_R = "miner_r"


class Miner_L(pygame.sprite.Sprite):
    is_passive = True

    def __init__(self, screen, base):
        super().__init__()
        self.screen = screen
        self.health = 55
        self.max_health = 55
        self.hit_timer = 0
        self.is_dying = False
        self.dying_timer = 0
        self.attack = 0
        self.armor = 3
        self.speed = 0
        self.unit_type = MINER_TYPE_L
        self.image = pygame.image.load("pictures/l_melee.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomleft = (base.rect.right, self.screen_rect.bottom)
        self.x = self.rect.centerx

    def output(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.circle(self.screen, (255, 200, 0),
                           (self.rect.right - 10, self.rect.top + 10), 8)
        if self.is_dying:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((180, 0, 0, 180))
            self.screen.blit(flash, self.rect)
        elif self.hit_timer > 0:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((255, 50, 50, 140))
            self.screen.blit(flash, self.rect)
            self.hit_timer -= 1

    def move(self):
        pass


class Miner_R(pygame.sprite.Sprite):
    is_passive = True

    def __init__(self, screen, base):
        super().__init__()
        self.screen = screen
        self.health = 55
        self.max_health = 55
        self.hit_timer = 0
        self.is_dying = False
        self.dying_timer = 0
        self.attack = 0
        self.armor = 3
        self.speed = 0
        self.unit_type = MINER_TYPE_R
        self.image = pygame.image.load("pictures/r_melee.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.bottomright = (base.rect.left, self.screen_rect.bottom)
        self.x = self.rect.centerx

    def output(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.circle(self.screen, (255, 200, 0),
                           (self.rect.left + 10, self.rect.top + 10), 8)
        if self.is_dying:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((180, 0, 0, 180))
            self.screen.blit(flash, self.rect)
        elif self.hit_timer > 0:
            flash = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            flash.fill((255, 50, 50, 140))
            self.screen.blit(flash, self.rect)
            self.hit_timer -= 1

    def move(self):
        pass


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
