import pygame
import sys
from settings import *

class Button:
    def __init__(self, x, y, w, h, text, action_name, bg_color=LIGHT_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action_name
        self.bg_color = bg_color
        self.text_color = text_color

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.state = "MENU"
        self.setup_menu_buttons()

    def setup_menu_buttons(self):
        self.buttons = []
        start_y = START_Y
        
        actions = ["diff", "y_gold", "b_gold", "c_dmg", "o_dmg", "heal", "rhythm"]
        for i, act in enumerate(actions):
            y = start_y + i * MENU_SPASING_Y
            self.buttons.append(Button(WIDTH // 2 + MENU_MINUS_OFFSET_X, y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "-", f"{act}_minus"))
            self.buttons.append(Button(WIDTH // 2 + MENU_PLUS_OFFSET_X, y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "+", f"{act}_plus"))

        self.buttons.append(Button(WIDTH // 2 - QUITSTART_OFFSET, start_y + MENU_START_Y_OFFSET, MENU_ACTION_WIDTH, MENU_ACTION_HEIGHT, MENU_START_TEXT, "start", GREEN, WHITE))
        self.buttons.append(Button(WIDTH // 2 - QUITSTART_OFFSET, start_y + MENU_START_Y_OFFSET + MENU_BUTTON_GAP_Y, MENU_ACTION_WIDTH, MENU_ACTION_HEIGHT, MENU_QUIT_TEXT, "quit", RED, WHITE))

    def handle_menu_click(self, action):
        m = self.model
        if action == "diff_minus": m.diff_idx = (m.diff_idx - 1) % 4
        elif action == "diff_plus": m.diff_idx = (m.diff_idx + 1) % 4
        elif action == "y_gold_minus": m.yellow_gold = max(1, m.yellow_gold - 1)
        elif action == "y_gold_plus": m.yellow_gold += 1
        elif action == "b_gold_minus": m.blue_gold = max(0, m.blue_gold - 1)
        elif action == "b_gold_plus": m.blue_gold += 1
        elif action == "c_dmg_minus": m.char_dmg = max(0.0, m.char_dmg - 0.1)
        elif action == "c_dmg_plus": m.char_dmg += 0.1
        elif action == "o_dmg_minus": m.obs_dmg = max(0.0, m.obs_dmg - 0.1)
        elif action == "o_dmg_plus": m.obs_dmg += 0.1
        elif action == "heal_minus": m.heal_amt = max(0.1, m.heal_amt - 0.1)
        elif action == "heal_plus": m.heal_amt += 0.1
        elif action == "rhythm_minus" or action == "rhythm_plus": m.rhythm_mode = not m.rhythm_mode
        elif action == "start": 
            m.reset_state()
            self.state = "START_WAIT"
        elif action == "quit":
            pygame.quit()
            sys.exit()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        if btn.is_clicked(event.pos):
                            self.handle_menu_click(btn.action)

            elif self.state == "START_WAIT":
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self.state = "PLAYING"

            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    elif event.key == pygame.K_SPACE and self.model.rhythm_mode:
                        self.model.player.jump(3)
                    elif event.unicode:
                        took_dmg = self.model.word_manager.process_input(event.unicode.lower(), self.model.diff_idx)
                        if took_dmg and self.model.diff_idx != 0:
                            self.model.hp -= self.model.char_dmg
                        
                        if self.model.word_manager.check_word_completion(self.model.diff_idx):
                            if not self.model.rhythm_mode:
                                self.model.player.jump(3)

            elif self.state == "GAME_OVER":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_r):
                    self.model.reset_state()
                    self.state = "START_WAIT"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

    def update(self):
        self.process_events()
        if self.state == "PLAYING":
            self.model.update()
            if self.model.game_over:
                self.state = "GAME_OVER"

    def render(self):
        if self.state == "MENU":
            self.view.draw_menu(self.buttons, self.model)
        else:
            self.view.draw_game(self.model)
            if self.state == "START_WAIT":
                self.view.draw_overlay("Готов?", "Нажмите любую кнопку", BLACK)
            elif self.state == "GAME_OVER":
                self.view.draw_game_over(self.model)
        
        pygame.display.flip()