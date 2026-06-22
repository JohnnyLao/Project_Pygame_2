import pygame
import sys
from controls import (
    events, update_arrows, health_control, arrow_collide,
    banner_spawn, ai_spawn, restart,
    COSTS_L, COSTS_R, UPGRADE_COSTS, MAX_UPGRADE, SPAWN_COOLDOWN, MINER_COST,
)
from units import Base_L, Base_R, Text, Banner, MINER_TYPE_L, MINER_TYPE_R
from pygame.sprite import Group
from sounds import Sounds

FPS = 60
W, H = 1920, 1000
clock = pygame.time.Clock()

_BTN_W, _BTN_H, _BTN_GAP = 205, 72, 8

_UNITS_L = [
    {"key": "1", "name": "Рыцарь", "hp": 160, "atk": 9,  "arm": 8, "cost": COSTS_L[0], "color": (50, 90, 160)},
    {"key": "2", "name": "Мечник", "hp": 65,  "atk": 20, "arm": 0, "cost": COSTS_L[1], "color": (50, 130, 70)},
    {"key": "3", "name": "Лучник", "hp": 35,  "atk": 5,  "arm": 0, "cost": COSTS_L[2], "color": (150, 110, 30)},
]
_UNITS_R = [
    {"key": "↑", "name": "Воин",   "hp": 160, "atk": 9,  "arm": 8, "cost": COSTS_R[0], "color": (150, 30, 30)},
    {"key": "↓", "name": "Убийца", "hp": 65,  "atk": 20, "arm": 0, "cost": COSTS_R[1], "color": (110, 30, 150)},
    {"key": "→", "name": "Маг",    "hp": 35,  "atk": 5,  "arm": 0, "cost": COSTS_R[2], "color": (30, 90, 150)},
]

# ─── Вспомогательные функции рисования ───────────────────────────────────────

def _draw_button(screen, x, y, info, gold, cooldowns_i, fonts):
    now = pygame.time.get_ticks()
    cd_ratio = max(0.0, 1.0 - (now - cooldowns_i) / SPAWN_COOLDOWN)
    can_afford = gold >= info["cost"] and cd_ratio == 0.0

    col = info["color"] if can_afford else tuple(max(0, c - 70) for c in info["color"])
    panel = pygame.Surface((_BTN_W, _BTN_H), pygame.SRCALPHA)
    panel.fill((*col, 200))
    screen.blit(panel, (x, y))
    border = (255, 240, 140) if can_afford else (70, 70, 70)
    pygame.draw.rect(screen, border, (x, y, _BTN_W, _BTN_H), 2)

    txt = (255, 255, 255) if can_afford else (140, 140, 140)
    screen.blit(fonts["btn"].render(f"[{info['key']}] {info['name']}", True, txt), (x + 8, y + 6))
    screen.blit(fonts["small"].render(f"HP:{info['hp']}  Атк:{info['atk']}  Бр:{info['arm']}", True, txt), (x + 8, y + 30))
    cost_col = (255, 220, 60) if can_afford else (100, 100, 100)
    screen.blit(fonts["small"].render(f"Цена: {info['cost']}g", True, cost_col), (x + 8, y + 50))

    if cd_ratio > 0:
        cd_w = int(_BTN_W * cd_ratio)
        pygame.draw.rect(screen, (200, 120, 0), (x, y + _BTN_H - 5, cd_w, 5))


def _draw_miner_btn(screen, x, y, key, gold, is_alive, fonts):
    if is_alive:
        col, border = (30, 100, 80), (100, 255, 200)
        label, cost_txt = f"[{key}] Шахтёр", "АКТИВЕН"
        cost_col = (100, 255, 200)
    else:
        can = gold >= MINER_COST
        col = (100, 70, 20) if can else (60, 40, 10)
        border = (255, 210, 80) if can else (70, 70, 70)
        label = f"[{key}] Шахтёр"
        cost_txt = f"Цена: {MINER_COST}g"
        cost_col = (255, 210, 60) if can else (100, 100, 100)
    panel = pygame.Surface((_BTN_W, _BTN_H), pygame.SRCALPHA)
    panel.fill((*col, 200))
    screen.blit(panel, (x, y))
    pygame.draw.rect(screen, border, (x, y, _BTN_W, _BTN_H), 2)
    txt = (255, 255, 255) if (is_alive or gold >= MINER_COST) else (140, 140, 140)
    screen.blit(fonts["btn"].render(label, True, txt), (x + 8, y + 6))
    screen.blit(fonts["small"].render("HP:40  +1g каждые 3с", True, txt), (x + 8, y + 30))
    screen.blit(fonts["small"].render(cost_txt, True, cost_col), (x + 8, y + 50))


def _draw_upgrade_btn(screen, x, y, key, base, fonts):
    lvl = base.gold_upgrade
    maxed = lvl >= MAX_UPGRADE
    cost = UPGRADE_COSTS[lvl] if not maxed else 0
    can = not maxed and base.gold >= cost

    col = (60, 160, 60) if can else (40, 80, 40) if not maxed else (80, 60, 20)
    panel = pygame.Surface((_BTN_W, 60), pygame.SRCALPHA)
    panel.fill((*col, 200))
    screen.blit(panel, (x, y))
    pygame.draw.rect(screen, (200, 255, 200) if can else (70, 70, 70), (x, y, _BTN_W, 60), 2)

    txt = (255, 255, 255) if can else (140, 140, 140)
    label = "МАКС" if maxed else f"[{key}] Золото+"
    screen.blit(fonts["btn"].render(label, True, txt), (x + 8, y + 6))
    lvl_str = f"Уровень: {lvl}/{MAX_UPGRADE}"
    cost_str = "" if maxed else f"  Цена: {cost}g"
    screen.blit(fonts["small"].render(lvl_str + cost_str, True, txt), (x + 8, y + 34))


def _draw_ui(screen, fonts, base_l, base_r, units_1, units_2):
    step = _BTN_H + _BTN_GAP
    for i, info in enumerate(_UNITS_L):
        _draw_button(screen, 5, 140 + i * step, info, base_l.gold, base_l.cooldowns[i], fonts)
    miner_y = 140 + 3 * step
    has_miner_l = any(u.unit_type == MINER_TYPE_L and not u.is_dying for u in units_1)
    _draw_miner_btn(screen, 5, miner_y, "4", base_l.gold, has_miner_l, fonts)
    _draw_upgrade_btn(screen, 5, miner_y + step, "Q", base_l, fonts)

    for i, info in enumerate(_UNITS_R):
        _draw_button(screen, W - _BTN_W - 5, 140 + i * step, info, base_r.gold, base_r.cooldowns[i], fonts)
    has_miner_r = any(u.unit_type == MINER_TYPE_R and not u.is_dying for u in units_2)
    _draw_miner_btn(screen, W - _BTN_W - 5, miner_y, "Ctrl", base_r.gold, has_miner_r, fonts)
    _draw_upgrade_btn(screen, W - _BTN_W - 5, miner_y + step, "←", base_r, fonts)


def _update_gold_anims(screen, gold_anims, font):
    alive = []
    for a in gold_anims:
        a["y"] -= 0.9
        a["timer"] -= 1
        if a["timer"] > 0:
            surf = font.render(a["text"], True, a["color"])
            surf.set_alpha(int(255 * a["timer"] / 55))
            screen.blit(surf, surf.get_rect(centerx=a["cx"], y=int(a["y"])))
            alive.append(a)
    gold_anims[:] = alive


def _draw_hp_bar(screen, unit):
    bar_w = unit.rect.width
    x, y = unit.rect.left, unit.rect.top - 10
    ratio = max(0.0, unit.health / unit.max_health)
    bar_color = (0, 200, 0) if ratio > 0.5 else (220, 200, 0) if ratio > 0.25 else (200, 30, 30)
    pygame.draw.rect(screen, (60, 0, 0), (x, y, bar_w, 6))
    pygame.draw.rect(screen, bar_color, (x, y, int(bar_w * ratio), 6))


# ─── Экран меню ──────────────────────────────────────────────────────────────

_MENU_BTN_W, _MENU_BTN_H = 340, 65

def _menu_btn_rect(i):
    x = W // 2 - _MENU_BTN_W // 2
    y = 380 + i * (_MENU_BTN_H + 20)
    return pygame.Rect(x, y, _MENU_BTN_W, _MENU_BTN_H)


def draw_menu(screen, bg, score_l, score_r, fonts):
    screen.blit(bg, (0, 0))
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    title = fonts["title"].render("KINGDOM BATTLE", True, (255, 220, 60))
    screen.blit(title, title.get_rect(center=(W // 2, 200)))

    score_txt = fonts["big"].render(f"Альянс  {score_l} : {score_r}  Нежить", True, (200, 200, 200))
    screen.blit(score_txt, score_txt.get_rect(center=(W // 2, 300)))

    mx, my = pygame.mouse.get_pos()
    labels = ["1 Игрок  (vs ИИ)", "2 Игрока", "Выход"]
    for i, label in enumerate(labels):
        rect = _menu_btn_rect(i)
        hovered = rect.collidepoint(mx, my)
        col = (90, 140, 220) if i == 0 else (60, 180, 80) if i == 1 else (180, 50, 50)
        bright = tuple(min(255, c + 40) for c in col) if hovered else col
        pygame.draw.rect(screen, bright, rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
        txt = fonts["big"].render(label, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=rect.center))


def handle_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if _menu_btn_rect(0).collidepoint(mx, my):
                return "1p"
            if _menu_btn_rect(1).collidepoint(mx, my):
                return "2p"
            if _menu_btn_rect(2).collidepoint(mx, my):
                sys.exit()
    return None


# ─── Экран победы ────────────────────────────────────────────────────────────

def draw_victory(screen, side, score_l, score_r, fonts, elapsed_ms):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    name = "Альянс" if side == "left" else "Нежить"
    col  = (100, 160, 255) if side == "left" else (180, 60, 60)
    win_txt = fonts["title"].render(f"ПОБЕДА — {name}!", True, col)
    screen.blit(win_txt, win_txt.get_rect(center=(W // 2, H // 2 - 80)))

    score_txt = fonts["big"].render(f"Альянс  {score_l} : {score_r}  Нежить", True, (220, 220, 220))
    screen.blit(score_txt, score_txt.get_rect(center=(W // 2, H // 2)))

    secs_left = max(0, 3 - elapsed_ms // 1000)
    cd_txt = fonts["btn"].render(f"Новая игра через {secs_left}...", True, (180, 180, 180))
    screen.blit(cd_txt, cd_txt.get_rect(center=(W // 2, H // 2 + 80)))


def handle_quit_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


# ─── Игровой кадр ────────────────────────────────────────────────────────────

def update(screen, bg, fonts, base, base_2, health_base, health_base_2, gold_1, gold_2,
           units_1, units_2, arrows_1, arrows_2, sounds, banners, gold_anims):
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    base.output()
    health_base.output(f'HP: {base.health}')
    gold_1.output(f'Gold: {base.gold}')
    base_2.output()
    health_base_2.output(f'HP: {base_2.health}')
    gold_2.output(f'Gold: {base_2.gold}')
    for unit in units_1.sprites():
        unit.output()
        unit.move()
    for unit in units_2.sprites():
        unit.output()
        unit.move()
    for arrow in arrows_1.sprites():
        arrow.draw()
    for arrow in arrows_2.sprites():
        arrow.draw()
    arrow_collide(units_1, units_2, arrows_1, arrows_2, sounds)
    for unit in units_1:
        _draw_hp_bar(screen, unit)
    for unit in units_2:
        _draw_hp_bar(screen, unit)
    for banner in banners.sprites():
        banner.output()
    _update_gold_anims(screen, gold_anims, fonts["small"])
    _draw_ui(screen, fonts, base, base_2, units_1, units_2)


# ─── Запуск ──────────────────────────────────────────────────────────────────

def start():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    bg = pygame.image.load("pictures/fon_1980.png")
    fonts = {
        "title": pygame.font.SysFont("Times New Roman", 64, bold=True),
        "big":   pygame.font.SysFont("Times New Roman", 36),
        "btn":   pygame.font.SysFont("Times New Roman", 22),
        "small": pygame.font.SysFont("Times New Roman", 16),
    }

    pygame.mixer.music.load("sounds/Fon track_1.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    sounds = Sounds()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Kingdom Battle")

    units_1, units_2, arrows_1, arrows_2, banners = Group(), Group(), Group(), Group(), Group()

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    base   = Base_L(screen, 500)
    base_2 = Base_R(screen, 500)
    health_base   = Text(screen, "HP: 500",   100,  710, "Times New Roman", 30)
    health_base_2 = Text(screen, "HP: 500",  1820,  710, "Times New Roman", 30)
    gold_1        = Text(screen, "Gold: 0",   100,  670, "Times New Roman", 30)
    gold_2        = Text(screen, "Gold: 0",  1820,  670, "Times New Roman", 30)
    gold_anims = []

    state = "menu"
    mode = "2p"
    score_l = 0
    score_r = 0
    victory_timer = 0
    victory_side = ""
    ai_next_spawn = 0

    sounds.game_start.play()

    while True:
        if state == "menu":
            draw_menu(screen, bg, score_l, score_r, fonts)
            result = handle_menu_events()
            if result:
                mode = result
                restart(base, base_2, units_1, units_2, banners, arrows_1, arrows_2, screen)
                ai_next_spawn = pygame.time.get_ticks() + 3000
                state = "playing"

        elif state == "playing":
            events(screen, units_1, units_2, base, base_2, sounds, arrows_1, arrows_2, banners, gold_anims)
            if mode == "1p":
                ai_next_spawn = ai_spawn(units_2, base_2, sounds, screen, ai_next_spawn)
            update(screen, bg, fonts, base, base_2, health_base, health_base_2, gold_1, gold_2,
                   units_1, units_2, arrows_1, arrows_2, sounds, banners, gold_anims)
            update_arrows(arrows_1, arrows_2)
            winner = health_control(units_1, units_2, base, base_2, sounds, banners)
            if winner:
                if winner == "left":
                    score_l += 1
                else:
                    score_r += 1
                victory_timer = pygame.time.get_ticks()
                victory_side = winner
                state = "victory"
            banner_spawn(units_1, units_2, banners, sounds, screen)

        elif state == "victory":
            handle_quit_events()
            update(screen, bg, fonts, base, base_2, health_base, health_base_2, gold_1, gold_2,
                   units_1, units_2, arrows_1, arrows_2, sounds, banners, gold_anims)
            elapsed = pygame.time.get_ticks() - victory_timer
            draw_victory(screen, victory_side, score_l, score_r, fonts, elapsed)
            if elapsed >= 3000:
                restart(base, base_2, units_1, units_2, banners, arrows_1, arrows_2, screen)
                ai_next_spawn = pygame.time.get_ticks() + 3000
                state = "playing"

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    start()
