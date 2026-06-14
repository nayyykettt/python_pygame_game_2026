import pygame
import sys
from settings import *


def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error as e:
        print(f"[WARNING] Не удалось загрузить {path}: {e}")
        return None


class GameView:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.SysFont("arial", 40)
            self.large_font = pygame.font.SysFont("arial", 65)
            self.active_font = pygame.font.SysFont("arial", 90, bold=True)
            self.menu_font = pygame.font.SysFont("arial", 32)
        except:
            self.font, self.large_font, self.active_font, self.menu_font = [pygame.font.Font(None, s) for s in (40, 65, 90, 32)]
        self.tex_player = load_image(TEX_PLAYER, (PLAYER_SIZE*PROPORTIONAL_COEFFICIENT, PLAYER_SIZE*PROPORTIONAL_COEFFICIENT))
        self.tex_obstacle = load_image(TEX_OBSTACLE, (OBSTACLE_SIZE*PROPORTIONAL_COEFFICIENT, OBSTACLE_SIZE*PROPORTIONAL_COEFFICIENT))
        self.tex_zone_yellow = load_image(TEX_ZONE_YELLOW, (ZONE_WIDTH, ZONE_HEIGHT))
        self.tex_zone_blue = load_image(TEX_ZONE_BLUE, (ZONE_WIDTH, ZONE_HEIGHT))
        self.tex_bg = load_image(TEX_BG, (WIDTH, HEIGHT))
        

    def draw_button(self, btn):
        pygame.draw.rect(self.screen, btn.bg_color, btn.rect, border_radius=5)
        txt = self.menu_font.render(btn.text, True, btn.text_color)
        self.screen.blit(txt, (btn.rect.x + (btn.rect.width - txt.get_width()) // 2, btn.rect.y + (btn.rect.height - txt.get_height()) // 2))

    def draw_menu(self, buttons, model):
        self.screen.fill(WHITE)
        title = self.large_font.render("НАСТРОЙКИ БАЛАНСА", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        labels = [
            ("Уровень сложности:", DIFFICULTY_NAMES[model.diff_idx]),
            ("Золото за желтую зону:", f"+{model.yellow_gold}"),
            ("Штраф за синюю зону:", f"-{model.blue_gold}"),
            ("Урон за символ:", f"{model.char_dmg:.1f}"),
            ("Урон за куб:", f"{model.obs_dmg:.1f}"),
            ("Лечение:", f"+{model.heal_amt:.1f}"),
            ("Ритм режим:", "ВКЛ" if model.rhythm_mode else "ВЫКЛ")
        ]

        start_y = 130
        for i, (lbl_txt, val_txt) in enumerate(labels):
            y = start_y + i * 65
            lbl = self.menu_font.render(lbl_txt, True, BLACK)
            val = self.menu_font.render(val_txt, True, PLAYER_BLUE)
            
            self.screen.blit(lbl, (WIDTH // 2 - 380, y + 5))
            
            center_x = WIDTH // 2 + 220
            self.screen.blit(val, (center_x - val.get_width() // 2, y + 5))

        for btn in buttons:
            self.draw_button(btn)

    def draw_game(self, model):
        if self.tex_bg:
            self.screen.blit(self.tex_bg, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        if model.rhythm_mode:
            rhythm_txt = self.font.render("РИТМ-РЕЖИМ", True, PLAYER_BLUE)
            self.screen.blit(rhythm_txt, (40, 40))
        
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 5)

        for pit in model.pits:
            pygame.draw.rect(self.screen, PURPLE, (pit.rect.left, GROUND_Y - 5, pit.rect.width, 10))
            for i in range(pit.rect.width // 20):
                px = pit.rect.left + i * 20
                pygame.draw.polygon(self.screen, PURPLE, [(px, GROUND_Y + 40), (px + 10, GROUND_Y + 15), (px + 20, GROUND_Y + 40)])
        
        for p in model.platforms:
            pygame.draw.rect(self.screen, LIGHT_GRAY, p.rect, border_radius=20)
        
        for z in model.zones:
            tex = self.tex_zone_yellow if z.zone_type == "yellow" else self.tex_zone_blue
            if tex:
                self.screen.blit(tex, z.rect)
            else:
                color = YELLOW if z.zone_type == "yellow" else CYAN_ZONE
                pygame.draw.rect(self.screen, color, z.rect)
        
        for o in model.obstacles:
            if self.tex_obstacle:
                self.screen.blit(self.tex_obstacle, o.rect)
            else:
                pygame.draw.rect(self.screen, RED, o.rect)
        
        for h in model.heals:
            pygame.draw.rect(self.screen, GREEN, h.rect)
        
        if self.tex_player:
            self.screen.blit(self.tex_player, model.player.rect)
        else:
            pygame.draw.rect(self.screen, PLAYER_BLUE, model.player.rect)

        hp_txt = self.font.render(f"Здоровье: {max(0, model.hp):.1f}", True, BLACK)
        g_txt = self.font.render(f"Золото: {model.gold}/{TARGET_GOLD}", True, YELLOW)
        self.screen.blit(hp_txt, (40, HEIGHT - 175))
        self.screen.blit(g_txt, (40 + hp_txt.get_width() + 40, HEIGHT - 175))

        wm = model.word_manager
        words_y = HEIGHT - 110
        current_x = WIDTH // 2 - sum([self.large_font.size(w)[0] + 20 for w in wm.words]) // 2
        
        for i, word in enumerate(wm.words):
            if i == 0:
                for j, char in enumerate(word):
                    font = self.active_font if j == wm.current_idx else self.large_font
                    color = wm.char_colors[j]
                    surf = font.render(char, True, color)
                    self.screen.blit(surf, (current_x, words_y - (20 if j == wm.current_idx else 0)))
                    current_x += font.size(char)[0]
            else:
                surf = self.large_font.render(word, True, GRAY)
                self.screen.blit(surf, (current_x, words_y))
                current_x += self.large_font.size(word)[0]
            current_x += 20

    def draw_overlay(self, msg, sub_msg, color):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        t1 = self.large_font.render(msg, True, color)
        t2 = self.font.render(sub_msg, True, BLACK)
        self.screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 50))

    def draw_game_over(self, model):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        msg = "ПОБЕДА!" if model.is_victory else "ПОРАЖЕНИЕ"
        color = GREEN if model.is_victory else RED
        
        t1 = self.large_font.render(msg, True, color)
        self.screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 180))
        
        total_time_sec = int(model.total_time)
        wrong_chars = model.word_manager.wrong_chars
        correct_chars = max(0, model.word_manager.total_chars - wrong_chars)
        time_minutes = model.total_time / 60.0
        cpm = int(correct_chars / time_minutes) if time_minutes > 0 else 0
        
        stats_lines = [
            f"Время в игре: {total_time_sec} сек.",
            f"Скорость ввода: {cpm} симв/мин.",
            f"Количество ошибок: {wrong_chars}"
        ]
        
        for i, line in enumerate(stats_lines):
            stat_surf = self.font.render(line, True, BLACK)
            self.screen.blit(stat_surf, (WIDTH // 2 - stat_surf.get_width() // 2, HEIGHT // 2 - 40 + i * 45))
            
        sub_txt = self.menu_font.render("Нажмите R / ENTER для рестарта | ESC для меню", True, DARK_GRAY)
        self.screen.blit(sub_txt, (WIDTH // 2 - sub_txt.get_width() // 2, HEIGHT // 2 + 130))