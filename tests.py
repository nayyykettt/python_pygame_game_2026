import pygame
pygame.init()

from model import WordManager, Player, Platform, GameModel, Obstacle, HealItem, Pit, Zone
from controller import GameController, Button
from view import GameView
from settings import (
    GREEN, RED, GRAY, WORDS_IN_ROW_COUNT,
    GROUND_Y, PLAYER_SIZE, JUMP_VELOCITY_START, GRAVITY, JUMP,
    MAX_HP, START_GOLD, TARGET_GOLD,
    OBSTACLE_SIZE, HEAL_SIZE, ZONE_WIDTH, ZONE_HEIGHT, PIT_HEIGHT,
    WIDTH, HEIGHT,
    TEST_PLAYER_X, TEST_PLAYER_Y,
    TEST_PLATFORM_X, TEST_PLATFORM_Y, TEST_PLATFORM_WIDTH, TEST_PLATFORM_HEIGHT,
    TEST_GOLD_START, TEST_HP_LOW,
    TEST_PIT_WIDTH, TEST_PIT_HEIGHT, TEST_PIT_OFFSET,
    TEST_BUTTON_X, TEST_BUTTON_Y, TEST_BUTTON_WIDTH, TEST_BUTTON_HEIGHT,
    TEST_YELLOW_GOLD_START
)


def test_init_words_creates_words():
    wm = WordManager()
    wm.init_words(0)
    assert len(wm.words) == WORDS_IN_ROW_COUNT


def test_correct_input_colors_green():
    wm = WordManager()
    wm.init_words(0)
    first_char = wm.words[0][0].lower()
    wm.process_input(first_char, 0)
    assert wm.char_colors[0] == GREEN


def test_wrong_input_colors_red():
    wm = WordManager()
    wm.init_words(0)
    wm.process_input("ы", 0)
    assert wm.char_colors[0] == RED


def test_wrong_input_returns_damage():
    wm = WordManager()
    wm.init_words(0)
    result = wm.process_input("ы", 0)
    assert result is True


def test_complete_word_returns_true():
    wm = WordManager()
    wm.init_words(0)
    word = wm.words[0]
    for ch in word:
        wm.process_input(ch.lower(), 0)
    completed = wm.check_word_completion(0)
    assert completed is True


def test_complete_word_adds_new():
    wm = WordManager()
    wm.init_words(0)
    word = wm.words[0]
    for ch in word:
        wm.process_input(ch.lower(), 0)
    wm.check_word_completion(0)
    assert len(wm.words) == WORDS_IN_ROW_COUNT


def test_non_russian_ignored():
    wm = WordManager()
    wm.init_words(0)
    result = wm.process_input("a", 0)
    assert result is False


def test_player_starts_on_ground():
    p = Player(0, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
    assert p.rect.bottom == GROUND_Y


def test_jump_sets_velocity():
    p = Player(0, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
    p.jump(JUMP)
    assert p.velocity_y == JUMP_VELOCITY_START


def test_double_jump_allowed():
    p = Player(0, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
    p.jump(JUMP)
    p.jump(JUMP)
    assert p.jump_count == 2


def test_gravity_pulls_down():
    p = Player(0, TEST_PLAYER_Y, PLAYER_SIZE)
    p.velocity_y = 0
    p.update_physics([])
    assert p.velocity_y == GRAVITY


def test_player_lands_on_platform():
    p = Player(TEST_PLAYER_X, TEST_PLAYER_Y, PLAYER_SIZE)
    p.velocity_y = GRAVITY * 2
    plat = Platform(TEST_PLATFORM_X, TEST_PLATFORM_Y, TEST_PLATFORM_WIDTH, TEST_PLATFORM_HEIGHT)
    p.update_physics([plat])
    assert p.rect.bottom == plat.rect.top


def test_player_stops_at_ground():
    p = Player(0, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
    p.velocity_y = GRAVITY * 2
    p.update_physics([])
    assert p.rect.bottom == GROUND_Y
    assert p.velocity_y == 0


def test_model_starts_with_full_hp():
    model = GameModel()
    assert model.hp == MAX_HP


def test_model_starts_with_zero_gold():
    model = GameModel()
    assert model.gold == START_GOLD


def test_reset_sets_full_hp():
    model = GameModel()
    model.hp = TEST_HP_LOW
    model.reset_state()
    assert model.hp == MAX_HP


def test_reset_clears_gold():
    model = GameModel()
    model.gold = TEST_GOLD_START
    model.reset_state()
    assert model.gold == START_GOLD


def test_obstacle_deals_damage():
    model = GameModel()
    model.diff_idx = 1
    start_hp = model.hp
    obs = Obstacle(model.player.rect.x, model.player.rect.y, OBSTACLE_SIZE, OBSTACLE_SIZE)
    model.obstacles = [obs]
    model._check_collisions()
    assert model.hp < start_hp


def test_easy_no_damage():
    model = GameModel()
    model.diff_idx = 0
    start_hp = model.hp
    obs = Obstacle(model.player.rect.x, model.player.rect.y, OBSTACLE_SIZE, OBSTACLE_SIZE)
    model.obstacles = [obs]
    model._check_collisions()
    assert model.hp == start_hp


def test_heal_increases_hp():
    model = GameModel()
    model.hp = TEST_HP_LOW
    heal = HealItem(model.player.rect.x, model.player.rect.y, HEAL_SIZE, HEAL_SIZE)
    model.heals = [heal]
    model._check_collisions()
    assert model.hp > TEST_HP_LOW


def test_yellow_zone_adds_gold():
    model = GameModel()
    model.gold = TEST_GOLD_START
    zone = Zone(model.player.rect.x, model.player.rect.y, ZONE_WIDTH, ZONE_HEIGHT, "yellow")
    model.zones = [zone]
    model._check_collisions()
    assert model.gold > TEST_GOLD_START


def test_blue_zone_removes_gold():
    model = GameModel()
    model.gold = TEST_GOLD_START
    zone = Zone(model.player.rect.x, model.player.rect.y, ZONE_WIDTH, ZONE_HEIGHT, "blue")
    model.zones = [zone]
    model._check_collisions()
    assert model.gold < TEST_GOLD_START


def test_pit_kills():
    model = GameModel()
    model.player.rect.bottom = GROUND_Y
    pit = Pit(model.player.rect.centerx - TEST_PIT_OFFSET, GROUND_Y, TEST_PIT_WIDTH, PIT_HEIGHT)
    model.pits = [pit]
    model._check_collisions()
    assert model.hp == 0


def test_zero_hp_game_over():
    model = GameModel()
    model.hp = 0
    model._check_game_over()
    assert model.game_over is True


def test_target_gold_victory():
    model = GameModel()
    model.gold = TARGET_GOLD
    model._check_game_over()
    assert model.game_over is True
    assert model.is_victory is True


def test_button_click_inside():
    btn = Button(TEST_BUTTON_X, TEST_BUTTON_Y, TEST_BUTTON_WIDTH, TEST_BUTTON_HEIGHT, "Test", "test")
    assert btn.is_clicked((TEST_BUTTON_X + 1, TEST_BUTTON_Y + 1)) is True


def test_button_click_outside():
    btn = Button(TEST_BUTTON_X, TEST_BUTTON_Y, TEST_BUTTON_WIDTH, TEST_BUTTON_HEIGHT, "Test", "test")
    assert btn.is_clicked((0, 0)) is False


def test_controller_starts_in_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    assert controller.state == "MENU"


def test_diff_minus_changes_difficulty():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    start = model.diff_idx
    controller.handle_menu_click("diff_minus")
    assert model.diff_idx != start


def test_start_changes_state():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    controller.handle_menu_click("start")
    assert controller.state == "START_WAIT"


def test_y_gold_minus_decreases():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    model.yellow_gold = TEST_YELLOW_GOLD_START
    controller.handle_menu_click("y_gold_minus")
    assert model.yellow_gold == TEST_YELLOW_GOLD_START - 1


def test_rhythm_toggles():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    start = model.rhythm_mode
    controller.handle_menu_click("rhythm_minus")
    assert model.rhythm_mode != start