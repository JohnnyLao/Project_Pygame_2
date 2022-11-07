import pygame
from controls import events, update_arrows, health_control, arrow_collide, banner_spawn
from units import Base_L, Base_R, Text, Text2, Banner
from pygame.sprite import Group
from sounds import Sounds


FPS = 60
W, H = 1920, 1000
clock = pygame.time.Clock()
bg = pygame.image.load("pictures/fon_1980.jpg")


def start():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.music.load("sounds/Fon track_1.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    sounds = Sounds()       # Import all sounds
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Window")
    # pygame.display.set_icon("")
    units_1, units_2, arrows_1, arrows_2, banners = Group(), Group(), Group(), Group(), Group()

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    base = Base_L(screen, 500)
    health_base = Text(screen,f'Health {base.health}', 100, 700, "Times New Roman", 30)
    gold_1 = Text(screen, f'Gold:{base.gold}', 100, 100, "Times New Roman", 30)
    base_2 = Base_R(screen, 500)
    health_base_2 = Text(screen,f'Health {base_2.health}', 1820, 700, "Times New Roman", 30)
    gold_2 = Text(screen, f'Gold:{base_2.gold}', 1820, 100, "Times New Roman", 30)
    sounds.game_start.play()

    while True:
        pygame.display.update()
        events(screen, units_1, units_2, base, base_2, sounds, arrows_1, arrows_2, banners)
        update(screen, base, base_2, health_base, health_base_2, gold_1, gold_2, units_1, units_2, arrows_1, arrows_2, sounds, banners)
        update_arrows(arrows_1, arrows_2)
        health_control(units_1, units_2, base, base_2, sounds, banners)
        banner_spawn(units_1, units_2, banners, sounds, screen)
        clock.tick(FPS)


def update(screen, base, base_2, health_base, health_base_2, gold_1, gold_2, units_1, units_2, arrows_1, arrows_2, sounds, banners):
    """обновление экрана"""
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    base.output()
    health_base.output(f'Health {base.health}')
    gold_1.output(f'Gold:{base.gold}')
    base_2.output()
    health_base_2.output(f'Health {base_2.health}')
    gold_2.output(f'Gold:{base_2.gold}')
    for unit in units_1.sprites():
        unit.output()
        unit.move()
    for unit in units_2.sprites():
        unit.output()
        unit.move()
    for arrow in arrows_1.sprites():
        arrow.draw()
    for arrow2 in arrows_2.sprites():
        arrow2.draw()
    arrow_collide(units_1, units_2, arrows_1, arrows_2, sounds)
    for unit in units_1:
        health_bar = Text2(screen, f'{unit.health}', unit)
        health_bar.output()
    for unit in units_2:
        health_bar = Text2(screen, f'{unit.health}', unit)
        health_bar.output()
    for banner in banners.sprites():
        banner.output()


if __name__ == "__main__":
    start()