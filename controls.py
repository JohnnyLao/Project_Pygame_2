import pygame
import sys
from units import Units_1, Units_2, Arrows, Arrows2, Banner, Miner_L, Miner_R, MINER_TYPE_L, MINER_TYPE_R
import random

unit_path = [
    "pictures/l_knigth.png",
    "pictures/l_melee.png",
    "pictures/l_archer.png",
    "pictures/r_melee.png",
    "pictures/r_killer.png",
    "pictures/r_archer.png",
]

SPAWN_COOLDOWN = 1500   # мс между спавнами одного слота
COSTS_L = [20, 15, 10]  # Рыцарь, Мечник, Лучник
COSTS_R = [20, 15, 10]  # Воин, Убийца, Маг
UPGRADE_COSTS = [30, 60, 90]  # цена каждого уровня прокачки золота
MAX_UPGRADE = 3
MINER_COST = 15
START_GOLD = 10


def restart(base_1, base_2, units_1, units_2, banners, arrows_1, arrows_2, screen):
    base_1.gold, base_2.gold = START_GOLD, START_GOLD
    base_1.health, base_2.health = 500, 500
    base_1.timer = 0
    base_1.cooldowns = [0, 0, 0]
    base_2.cooldowns = [0, 0, 0]
    base_1.gold_upgrade = 0
    base_2.gold_upgrade = 0
    units_1.empty()
    units_2.empty()
    banners.empty()
    arrows_1.empty()
    arrows_2.empty()
    units_1.add(Miner_L(screen, base_1))
    units_2.add(Miner_R(screen, base_2))


def events(screen, units_1, units_2, base_1, base_2, sounds, arrows_1, arrows_2, banners, gold_anims):
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # ── Левая сторона: спавн ──
            if event.key == pygame.K_1:
                if base_1.gold >= COSTS_L[0] and now - base_1.cooldowns[0] >= SPAWN_COOLDOWN:
                    sounds.a_spawn_1[random.randint(0, 2)].play()
                    units_1.add(Units_1(screen, unit_path[0], 160, 0.8, 9, 8))
                    base_1.gold -= COSTS_L[0]
                    base_1.cooldowns[0] = now
            elif event.key == pygame.K_2:
                if base_1.gold >= COSTS_L[1] and now - base_1.cooldowns[1] >= SPAWN_COOLDOWN:
                    sounds.a_spawn_2[random.randint(0, 2)].play()
                    units_1.add(Units_1(screen, unit_path[1], 65, 1.5, 20, 0))
                    base_1.gold -= COSTS_L[1]
                    base_1.cooldowns[1] = now
            elif event.key == pygame.K_3:
                if base_1.gold >= COSTS_L[2] and now - base_1.cooldowns[2] >= SPAWN_COOLDOWN:
                    sounds.a_spawn_3[random.randint(0, 2)].play()
                    units_1.add(Units_1(screen, unit_path[2], 35, 0.6, 5, 0))
                    base_1.gold -= COSTS_L[2]
                    base_1.cooldowns[2] = now
            # ── Левая сторона: шахтёр (4) ──
            elif event.key == pygame.K_4:
                has_miner = any(u.unit_type == MINER_TYPE_L and not u.is_dying for u in units_1)
                if not has_miner and base_1.gold >= MINER_COST:
                    units_1.add(Miner_L(screen, base_1))
                    base_1.gold -= MINER_COST
            # ── Левая сторона: апгрейд золота (Q) ──
            elif event.key == pygame.K_q:
                lvl = base_1.gold_upgrade
                if lvl < MAX_UPGRADE and base_1.gold >= UPGRADE_COSTS[lvl]:
                    base_1.gold -= UPGRADE_COSTS[lvl]
                    base_1.gold_upgrade += 1

            # ── Правая сторона: спавн ──
            elif event.key == pygame.K_UP:
                if base_2.gold >= COSTS_R[0] and now - base_2.cooldowns[0] >= SPAWN_COOLDOWN:
                    sounds.u_spawn_1[random.randint(0, 2)].play()
                    units_2.add(Units_2(screen, unit_path[3], 160, 0.8, 9, 8))
                    base_2.gold -= COSTS_R[0]
                    base_2.cooldowns[0] = now
            elif event.key == pygame.K_DOWN:
                if base_2.gold >= COSTS_R[1] and now - base_2.cooldowns[1] >= SPAWN_COOLDOWN:
                    sounds.u_spawn_2[random.randint(0, 2)].play()
                    units_2.add(Units_2(screen, unit_path[4], 65, 1.5, 20, 0))
                    base_2.gold -= COSTS_R[1]
                    base_2.cooldowns[1] = now
            elif event.key == pygame.K_RIGHT:
                if base_2.gold >= COSTS_R[2] and now - base_2.cooldowns[2] >= SPAWN_COOLDOWN:
                    sounds.u_spawn_3[random.randint(0, 2)].play()
                    units_2.add(Units_2(screen, unit_path[5], 35, 0.6, 5, 0))
                    base_2.gold -= COSTS_R[2]
                    base_2.cooldowns[2] = now
            # ── Правая сторона: шахтёр (Ctrl) ──
            elif event.key == pygame.K_RCTRL:
                has_miner = any(u.unit_type == MINER_TYPE_R and not u.is_dying for u in units_2)
                if not has_miner and base_2.gold >= MINER_COST:
                    units_2.add(Miner_R(screen, base_2))
                    base_2.gold -= MINER_COST
            # ── Правая сторона: апгрейд золота (←) ──
            elif event.key == pygame.K_LEFT:
                lvl = base_2.gold_upgrade
                if lvl < MAX_UPGRADE and base_2.gold >= UPGRADE_COSTS[lvl]:
                    base_2.gold -= UPGRADE_COSTS[lvl]
                    base_2.gold_upgrade += 1

        elif event.type == pygame.USEREVENT:
            base_1.timer += 1
            if base_1.timer % 3 == 0:
                earn_1 = 1 + base_1.gold_upgrade
                earn_2 = 1 + base_2.gold_upgrade
                base_1.gold += earn_1
                base_2.gold += earn_2
                gold_anims.append({"cx": 120, "y": 658.0, "timer": 55, "text": f"+{earn_1}g", "color": (255, 210, 40)})
                gold_anims.append({"cx": 1800, "y": 658.0, "timer": 55, "text": f"+{earn_2}g", "color": (255, 210, 40)})
                if any(u.unit_type == MINER_TYPE_L and not u.is_dying for u in units_1):
                    base_1.gold += 1
                    gold_anims.append({"cx": 120, "y": 648.0, "timer": 55, "text": "+1g (шахт.)", "color": (180, 255, 255)})
                if any(u.unit_type == MINER_TYPE_R and not u.is_dying for u in units_2):
                    base_2.gold += 1
                    gold_anims.append({"cx": 1800, "y": 648.0, "timer": 55, "text": "+1g (шахт.)", "color": (180, 255, 255)})
                for banner in banners:
                    if banner.banner_type == "pictures/dark_banner.png":
                        base_2.gold += 1
                        gold_anims.append({"cx": 1800, "y": 638.0, "timer": 55, "text": "+1g (флаг)", "color": (160, 255, 160)})
                    elif banner.banner_type == "pictures/light_banner.png":
                        base_1.gold += 1
                        gold_anims.append({"cx": 120, "y": 638.0, "timer": 55, "text": "+1g (флаг)", "color": (160, 255, 160)})

            if base_1.timer % 2 == 0:
                for unit1 in units_1:
                    if not unit1.is_dying and unit1.unit_type == unit_path[2]:
                        sounds.a_archer_shoot.play()
                        arrows_1.add(Arrows(screen, unit1, (0, 0, 20, 4), (0, 0, 150)))
                        unit1.attack_timer = 10
                for unit2 in units_2:
                    if not unit2.is_dying and unit2.unit_type == unit_path[5]:
                        sounds.u_mage_shoot.play()
                        arrows_2.add(Arrows2(screen, unit2, (0, 0, 8, 8), (150, 0, 0)))
                        unit2.attack_timer = 10

    # ── Рукопашный бой ──
    for unit1 in units_1:
        if unit1.is_dying:
            continue
        for unit2 in units_2:
            if unit2.is_dying:
                continue
            if pygame.sprite.collide_rect(unit1, unit2):
                sounds.damage[random.randint(0, 5)].play()
                unit1.x -= 30
                unit2.x += 30
                if not getattr(unit2, 'is_passive', False):
                    unit1.health -= unit2.attack + random.randint(-3, 3) - unit1.armor
                if not getattr(unit1, 'is_passive', False):
                    unit2.health -= unit1.attack + random.randint(-3, 3) - unit2.armor
                unit1.hit_timer = 10
                unit2.hit_timer = 10
                unit1.attack_timer = 8
                unit2.attack_timer = 8

    # ── Урон по базе 1 ──
    for unit2 in units_2:
        if unit2.is_dying or getattr(unit2, 'is_passive', False):
            continue
        if pygame.sprite.collide_rect(unit2, base_1):
            sounds.damage_base_1.play()
            unit2.x += 50
            base_1.health -= unit2.attack + random.randint(1, 3)
            unit2.health -= unit2.attack + random.randint(1, 3)
            unit2.hit_timer = 10
            unit2.attack_timer = 8

    # ── Урон по базе 2 ──
    for unit1 in units_1:
        if unit1.is_dying or getattr(unit1, 'is_passive', False):
            continue
        if pygame.sprite.collide_rect(unit1, base_2):
            sounds.damage_base_2.play()
            unit1.x -= 50
            base_2.health -= unit1.attack + random.randint(1, 3)
            unit1.health -= unit1.attack + random.randint(1, 3)
            unit1.hit_timer = 10
            unit1.attack_timer = 8


AI_RESERVE = 15   # ИИ всегда держит этот запас и не тратит ниже него
# Веса выбора: Воин=4, Убийца=3, Маг=1 — чтобы не спамил только дешёвых
_AI_WEIGHTS = [4, 3, 1]


def ai_spawn(units_2, base_2, sounds, screen, next_time):
    """ИИ для режима 1 игрок — спавнит юниты за правую сторону."""
    now = pygame.time.get_ticks()
    if now < next_time:
        return next_time

    spendable = base_2.gold - AI_RESERVE
    options = [i for i, cost in enumerate(COSTS_R) if spendable >= cost]
    if not options:
        return now + random.randint(800, 1500)

    weights = [_AI_WEIGHTS[i] for i in options]
    choice = random.choices(options, weights=weights, k=1)[0]

    if choice == 0:
        sounds.u_spawn_1[random.randint(0, 2)].play()
        units_2.add(Units_2(screen, unit_path[3], 160, 0.8, 9, 8))
        base_2.gold -= COSTS_R[0]
    elif choice == 1:
        sounds.u_spawn_2[random.randint(0, 2)].play()
        units_2.add(Units_2(screen, unit_path[4], 65, 1.5, 20, 0))
        base_2.gold -= COSTS_R[1]
    else:
        sounds.u_spawn_3[random.randint(0, 2)].play()
        units_2.add(Units_2(screen, unit_path[5], 35, 0.6, 5, 0))
        base_2.gold -= COSTS_R[2]

    return now + random.randint(2000, 4000)


def health_control(units_1, units_2, base_1, base_2, sounds, banners):
    """Возвращает 'left', 'right' при победе, иначе None."""
    for unit1 in list(units_1):
        if unit1.health <= 0 and not unit1.is_dying:
            unit1.is_dying = True
            unit1.dying_timer = 25
            if unit1.unit_type == unit_path[0]:
                sounds.a_death_1[random.randint(0, 2)].play()
            elif unit1.unit_type == unit_path[1]:
                sounds.a_death_2[random.randint(0, 2)].play()
            elif unit1.unit_type == unit_path[2]:
                sounds.a_death_3[random.randint(0, 2)].play()
        if unit1.is_dying:
            unit1.dying_timer -= 1
            if unit1.dying_timer <= 0:
                units_1.remove(unit1)
                base_2.gold += 5

    for unit2 in list(units_2):
        if unit2.health <= 0 and not unit2.is_dying:
            unit2.is_dying = True
            unit2.dying_timer = 25
            if unit2.unit_type == unit_path[3]:
                sounds.u_death_1[random.randint(0, 1)].play()
            elif unit2.unit_type == unit_path[4]:
                sounds.u_death_2[random.randint(0, 2)].play()
            elif unit2.unit_type == unit_path[5]:
                sounds.u_death_3[random.randint(0, 2)].play()
        if unit2.is_dying:
            unit2.dying_timer -= 1
            if unit2.dying_timer <= 0:
                units_2.remove(unit2)
                base_1.gold += 5

    if base_1.health <= 0:
        sounds.u_win[random.randint(0, 2)].play()
        return "right"
    if base_2.health <= 0:
        sounds.a_win[random.randint(0, 2)].play()
        return "left"
    return None


def update_arrows(arrows_1, arrows_2):
    shoot_distance = 500
    arrows_1.update()
    for arrow in list(arrows_1):
        if arrow.unit.rect.centerx - arrow.x <= -shoot_distance:
            arrows_1.remove(arrow)
    arrows_2.update()
    for arrow in list(arrows_2):
        if arrow.unit.rect.centerx - arrow.x >= shoot_distance:
            arrows_2.remove(arrow)


def arrow_collide(units_1, units_2, arrows_1, arrows_2, sounds):
    for unit2 in units_2:
        if unit2.is_dying:
            continue
        if pygame.sprite.spritecollide(unit2, arrows_1, True):
            sounds.damage_melee_4.play()
            unit2.x += 20
            unit2.health -= 18 + random.randint(-3, 3) - unit2.armor
            unit2.hit_timer = 10
    for unit1 in units_1:
        if unit1.is_dying:
            continue
        if pygame.sprite.spritecollide(unit1, arrows_2, True):
            sounds.damage_melee_4.play()
            unit1.x -= 20
            unit1.health -= 18 + random.randint(-3, 3) - unit1.armor
            unit1.hit_timer = 10


def banner_spawn(units_1, units_2, banners, sounds, screen):
    for unit2 in units_2:
        if unit2.is_dying:
            continue
        if unit2.x <= 1920 // 2:
            if len(banners) == 0:
                banners.add(Banner(screen, "pictures/dark_banner.png"))
            else:
                for banner in list(banners):
                    if banner.banner_type == "pictures/light_banner.png":
                        banners.empty()
                        banners.add(Banner(screen, "pictures/dark_banner.png"))
                        if unit2.unit_type == unit_path[3]:
                            sounds.u_ban_1_1.play()
                        elif unit2.unit_type == unit_path[4]:
                            sounds.u_ban_2_1.play()
                        elif unit2.unit_type == unit_path[5]:
                            sounds.u_ban_3_1.play()
    for unit1 in units_1:
        if unit1.is_dying:
            continue
        if unit1.x >= 1920 // 2:
            if len(banners) == 0:
                banners.add(Banner(screen, "pictures/light_banner.png"))
            else:
                for banner in list(banners):
                    if banner.banner_type == "pictures/dark_banner.png":
                        banners.empty()
                        banners.add(Banner(screen, "pictures/light_banner.png"))
                        if unit1.unit_type == unit_path[0]:
                            sounds.a_ban_1_1.play()
                        elif unit1.unit_type == unit_path[1]:
                            sounds.a_ban_2_1.play()
                        elif unit1.unit_type == unit_path[2]:
                            sounds.a_ban_3_1.play()
