import pygame
import sys
from units import Units_1, Units_2, Arrows, Arrows2, Banner
import random

unit_path = ["pictures/l_knigth.png",
             "pictures/l_melee.png",
             "pictures/l_archer.png",
             "pictures/r_melee.png",
             "pictures/r_killer.png",
             "pictures/r_archer.png"]


def restart(base_1, base_2, units_1, units_2, banners):
    base_1.gold, base_2.gold, base_1.health, base_2.health = 0, 0, 500, 500
    units_1.empty()
    units_2.empty()
    banners.empty()


def events(screen, units_1, units_2, base_1, base_2, sounds, arrows_1, arrows_2, banners):
    """events control"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:  # Spawn
            if event.key == pygame.K_1:
                if base_1.gold >= 10:
                    sounds.a_spawn_1[random.randint(0, 2)].play()
                    unit = Units_1(screen, unit_path[0], 100, 1, 7, 5)
                    units_1.add(unit)
                    base_1.gold -= 10
            elif event.key == pygame.K_2:  # Spawn
                if base_1.gold >= 10:
                    sounds.a_spawn_2[random.randint(0, 2)].play()
                    unit = Units_1(screen, unit_path[1], 50, 1.5, 15, 0)
                    units_1.add(unit)
                    base_1.gold -= 10
            elif event.key == pygame.K_3:  # Spawn
                if base_1.gold >= 10:
                    sounds.a_spawn_3[random.randint(0, 2)].play()
                    unit = Units_1(screen, unit_path[2], 30, 0.7, 10, 0)
                    units_1.add(unit)
                    base_1.gold -= 10
            elif event.key == pygame.K_UP:  # Spawn
                if base_2.gold >= 10:
                    sounds.u_spawn_1[random.randint(0, 2)].play()
                    unit = Units_2(screen, unit_path[3], 100, 1, 7, 5)
                    units_2.add(unit)
                    base_2.gold -= 10
            elif event.key == pygame.K_DOWN:  # Spawn
                if base_2.gold >= 10:
                    sounds.u_spawn_2[random.randint(0, 2)].play()
                    unit = Units_2(screen, unit_path[4], 50, 1.5, 15, 0)
                    units_2.add(unit)
                    base_2.gold -= 10
            elif event.key == pygame.K_RIGHT:  # Spawn
                if base_2.gold >= 10:
                    sounds.u_spawn_3[random.randint(0, 2)].play()
                    unit = Units_2(screen, unit_path[5], 30, 0.7, 10, 0)
                    units_2.add(unit)
                    base_2.gold -= 10
        elif event.type == pygame.USEREVENT:
            """"timer generation"""
            base_1.timer += 1
            print(base_1.timer)

            if base_1.timer % 3 == 0:
                """gold generating"""
                base_1.gold += random.randint(1, 5)
                base_2.gold += random.randint(1, 5)
                for banner in banners:
                    if banner.banner_type == "pictures/dark_banner.png":
                        base_2.gold += random.randint(0, 2)
                    elif banner.banner_type == "pictures/light_banner.png":
                        base_1.gold += random.randint(0, 2)

            if base_1.timer % 2 == 0:
                """right side shooting"""
                for unit1 in units_1:
                    if unit1.unit_type == unit_path[2]:
                        sounds.a_archer_shoot.play()
                        new_arrow = Arrows(screen, unit1, (0, 0, 20, 4), (0, 0, 150))
                        arrows_1.add(new_arrow)
            if base_1.timer % 2 == 0:
                """left side shooting"""
                for unit2 in units_2:
                    if unit2.unit_type == unit_path[5]:
                        sounds.u_mage_shoot.play()
                        new_arrow = Arrows2(screen, unit2, (0, 0, 8, 8), (150, 0, 0))
                        arrows_2.add(new_arrow)

    for unit1 in units_1:
        """melee fight"""
        for unit2 in units_2:
            if pygame.sprite.collide_rect(unit1, unit2):
                sounds.damage[random.randint(0, 5)].play()
                unit1.x -= 30
                unit2.x += 30
                unit1.health = unit1.health - (unit2.attack + random.randint(-5, 10) - unit1.armor)
                unit2.health = unit2.health - (unit1.attack + random.randint(-5, 10) - unit2.armor)

    """Check fot base_1 taking damage"""
    for unit2 in units_2:
        if pygame.sprite.collide_rect(unit2, base_1):
            sounds.damage_base_1.play()
            unit2.x += 50
            base_1.health -= (unit2.attack + random.randint(1, 5))
            unit2.health -= (unit2.attack + random.randint(1, 5))

    """Check fot base_2 taking damage"""
    for unit1 in units_1:
        if pygame.sprite.collide_rect(unit1, base_2):
            sounds.damage_base_2.play()
            unit1.x -= 50
            base_2.health -= (unit1.attack + random.randint(1, 5))
            unit1.health -= (unit1.attack + random.randint(1, 5))


def health_control(units_1, units_2, base_1, base_2, sounds, banners):
    """checking if health is 0, then kill unit"""
    for unit1 in units_1:
        if unit1.health <= 0:
            if unit1.unit_type == unit_path[0]:
                sounds.a_death_1[random.randint(0, 2)].play()
            elif unit1.unit_type == unit_path[1]:
                sounds.a_death_2[random.randint(0, 2)].play()
            elif unit1.unit_type == unit_path[2]:
                sounds.a_death_3[random.randint(0, 2)].play()
            units_1.remove(unit1)
            base_2.gold += 5
    for unit2 in units_2:
        if unit2.health <= 0:
            if unit2.unit_type == unit_path[3]:
                sounds.u_death_1[random.randint(0, 1)].play()
            elif unit2.unit_type == unit_path[4]:
                sounds.u_death_2[random.randint(0, 2)].play()
            elif unit2.unit_type == unit_path[5]:
                sounds.u_death_3[random.randint(0, 2)].play()
            units_2.remove(unit2)
            base_1.gold += 5
    if base_1.health <= 0:
        sounds.u_win[random.randint(0, 2)].play()
        restart(base_1, base_2, units_1, units_2, banners)
    elif base_2.health <= 0:
        restart(base_1, base_2, units_1, units_2, banners)
        sounds.a_win[random.randint(0, 2)].play()


def update_arrows(arrows_1, arrows_2):
    """arrows position update"""
    shoot_distance = 500
    arrows_1.update()
    for arrow in arrows_1.copy():
        if arrow.unit.rect.centerx - arrow.x <= -shoot_distance:
            arrows_1.remove(arrow)
    arrows_2.update()
    for arrow in arrows_2.copy():
        if arrow.unit.rect.centerx - arrow.x >= shoot_distance:
            arrows_2.remove(arrow)


def arrow_collide(units_1, units_2, arrows_1, arrows_2, sounds):
    """check if arrows collide with both"""
    for unit2 in units_2:
        if pygame.sprite.spritecollide(unit2, arrows_1, True):
            if unit2.unit_type == unit_path[3]:
                sounds.damage_melee_4.play()
                unit2.x += 20
                unit2.health = unit2.health - (20 + random.randint(-5, 5) - unit2.armor)
            else:
                sounds.damage_melee_4.play()
                unit2.x += 20
                unit2.health = unit2.health - (10 + random.randint(-5, 5) - unit2.armor)
    for unit1 in units_1:
        if pygame.sprite.spritecollide(unit1, arrows_2, True):
            if unit1.unit_type == unit_path[0]:
                sounds.damage_melee_4.play()
                unit1.x -= 20
                unit1.health = unit1.health - (20 + random.randint(-5, 5) - unit1.armor)
            else:
                sounds.damage_melee_4.play()
                unit1.x -= 20
                unit1.health = unit1.health - (10 + random.randint(-5, 5) - unit1.armor)


def banner_spawn(units_1, units_2, banners, sounds, screen):
    for unit2 in units_2:
        if unit2.x <= 1920 // 2:
            if len(banners) == 0:
                banner = Banner(screen, "pictures/dark_banner.png")
                banners.add(banner)
            else:
                for banner in banners:
                    if banner.banner_type == "pictures/light_banner.png":
                        banners.empty()
                        banner = Banner(screen, "pictures/dark_banner.png")
                        banners.add(banner)
                        if unit2.unit_type == unit_path[3]:
                            sounds.u_ban_1_1.play()
                        elif unit2.unit_type == unit_path[4]:
                            sounds.u_ban_2_1.play()
                        elif unit2.unit_type == unit_path[5]:
                            sounds.u_ban_3_1.play()
    for unit1 in units_1:
        if unit1.x >= 1920 // 2:
            if len(banners) == 0:
                banner = Banner(screen, "pictures/light_banner.png")
                banners.add(banner)
            else:
                for banner in banners:
                    if banner.banner_type == "pictures/dark_banner.png":
                        banners.empty()
                        banner = Banner(screen, "pictures/light_banner.png")
                        banners.add(banner)
                        if unit1.unit_type == unit_path[0]:
                            sounds.a_ban_1_1.play()
                        elif unit1.unit_type == unit_path[1]:
                            sounds.a_ban_2_1.play()
                        elif unit1.unit_type == unit_path[2]:
                            sounds.a_ban_3_1.play()

