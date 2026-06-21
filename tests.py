import pygame
pygame.init()

from model import WordManager, Player, Platform, GameModel, Obstacle, HealItem, Pit, Zone, GameObject, LevelGenerator
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
    TEST_YELLOW_GOLD_START,
    DEF_DIF, DEF_YELLOW_GOLD, DEF_BLUE_GOLD, DEF_CHAR_DAMAGE, DEF_OBSTACLE_DAMAGE,
    DEF_HEAL_AMOUNT, DEF_RHYTHM_MODE,
    BASE_SPEED, MAX_SPEED, DIFFICULTY_MULTIPLIERS, PROGRESSION_SCALE,
    INSTANT_DEATH_IDX, NO_DAMAGE_IDX,
    MIN_YELLOW_GOLD, MIN_BLUE_GOLD, MIN_CHAR_DAMAGE, MIN_OBSTACLE_DAMAGE, MIN_HEAL_AMOUNT,
    CHAR_DAMAGE_STEP, OBSTACLE_DAMAGE_STEP, HEAL_AMOUNT_STEP,
    RUSSIAN_ALPHABET,
    TEST_OBJ_SIZE, TEST_OBJ_SIZE_SMALL, TEST_MOVE_SPEED, TEST_MOVE_SPEED_SMALL,
    TEST_ZERO_SPEED, TEST_PLAYER_POS_X, TEST_PLAYER_POS_Y, TEST_JUMP_COUNT,
    TEST_GRAVITY_FRAMES, TEST_LARGE_DISTANCE, TEST_PIT_OFFSET_LARGE, TEST_HP_OFFSET,
    TEST_WAIT_TIME, TEST_GOLD_AMOUNT, TEST_GOLD_AMOUNT_BLUE, TEST_GOLD_AMOUNT_PLUS,
    TEST_DAMAGE_BASE, TEST_DAMAGE_MINUS, TEST_DAMAGE_PLUS, TEST_TIME_TOTAL,
    TEST_TIME_TOTAL_SMALL, TEST_RECT_EDGE, TEST_RECT_OUTSIDE, TEST_BUTTON_ACTION,
    TEST_BUTTON_TEXT, TEST_BUTTON_TEXT_DEFAULT, TEST_ZONE_TYPE_YELLOW, TEST_ZONE_TYPE_BLUE,
    TEST_ACTION_DIFF_MINUS, TEST_ACTION_Y_GOLD_MINUS, TEST_ACTION_B_GOLD_MINUS,
    TEST_ACTION_C_DMG_MINUS, TEST_ACTION_O_DMG_MINUS, TEST_ACTION_HEAL_MINUS,
    TEST_CHAR_WRONG, TEST_CHAR_NON_RUSSIAN, TEST_OVERLAY_TITLE, TEST_OVERLAY_SUBTITLE,
    TEST_OVERLAY_COLOR, TEST_WORDS_BANK_0, TEST_WORDS_BANK_1
)


def test_correct_input_colors_green():
    wm = WordManager()
    wm.init_words(TEST_ZERO_SPEED)
    first_char = wm.words[TEST_ZERO_SPEED][TEST_ZERO_SPEED].lower()
    wm.process_input(first_char, TEST_ZERO_SPEED)
    assert wm.char_colors[TEST_ZERO_SPEED] == GREEN


def test_wrong_input_colors_red():
    wm = WordManager()
    wm.init_words(TEST_ZERO_SPEED)
    wm.process_input(TEST_CHAR_WRONG, TEST_ZERO_SPEED)
    assert wm.char_colors[TEST_ZERO_SPEED] == RED


def test_wrong_input_returns_damage():
    wm = WordManager()
    wm.init_words(TEST_ZERO_SPEED)
    result = wm.process_input(TEST_CHAR_WRONG, TEST_ZERO_SPEED)
    assert result is True


def test_complete_word_returns_true():
    wm = WordManager()
    wm.init_words(TEST_ZERO_SPEED)
    word = wm.words[TEST_ZERO_SPEED]
    for ch in word:
        wm.process_input(ch.lower(), TEST_ZERO_SPEED)
    completed = wm.check_word_completion(TEST_ZERO_SPEED)
    assert completed is True


def test_non_russian_ignored():
    wm = WordManager()
    wm.init_words(TEST_ZERO_SPEED)
    result = wm.process_input(TEST_CHAR_NON_RUSSIAN, TEST_ZERO_SPEED)
    assert result is False


def test_check_word_completion_resets_current_idx():
    wm = WordManager()
    wm.init_words(TEST_ZERO_SPEED)
    word = wm.words[TEST_ZERO_SPEED]
    for ch in word:
        wm.process_input(ch.lower(), TEST_ZERO_SPEED)
    wm.check_word_completion(TEST_ZERO_SPEED)
    assert wm.current_idx == TEST_ZERO_SPEED


def test_jump_sets_velocity():
    p = Player(TEST_ZERO_SPEED, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
    p.jump(JUMP)
    assert p.velocity_y == JUMP_VELOCITY_START


def test_gravity_pulls_down():
    p = Player(TEST_ZERO_SPEED, TEST_PLAYER_Y, PLAYER_SIZE)
    p.velocity_y = TEST_ZERO_SPEED
    p.update_physics([])
    assert p.velocity_y == GRAVITY


def test_player_lands_on_platform():
    p = Player(TEST_PLAYER_X, TEST_PLAYER_Y, PLAYER_SIZE)
    p.velocity_y = GRAVITY * TEST_GRAVITY_FRAMES
    plat = Platform(TEST_PLATFORM_X, TEST_PLATFORM_Y, TEST_PLATFORM_WIDTH, TEST_PLATFORM_HEIGHT)
    p.update_physics([plat])
    assert p.rect.bottom == plat.rect.top


def test_player_stops_at_ground():
    p = Player(TEST_ZERO_SPEED, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
    p.velocity_y = GRAVITY * TEST_GRAVITY_FRAMES
    p.update_physics([])
    assert p.rect.bottom == GROUND_Y
    assert p.velocity_y == TEST_ZERO_SPEED


def test_player_falls_due_to_gravity():
    p = Player(TEST_PLAYER_POS_X, TEST_PLAYER_POS_Y, PLAYER_SIZE)
    p.velocity_y = TEST_ZERO_SPEED
    p.update_physics([])
    assert p.velocity_y == GRAVITY


def test_player_ceiling_collision():
    p = Player(TEST_ZERO_SPEED, TEST_ZERO_SPEED, PLAYER_SIZE)
    p.velocity_y = -TEST_MOVE_SPEED
    p.update_physics([])
    assert p.rect.y == TEST_ZERO_SPEED
    assert p.velocity_y == TEST_ZERO_SPEED


def test_gameobject_move():
    obj = GameObject(TEST_PLAYER_POS_X, TEST_PLAYER_POS_Y, TEST_OBJ_SIZE, TEST_OBJ_SIZE)
    obj.move(TEST_MOVE_SPEED)
    assert obj.rect.x == TEST_PLAYER_POS_X - TEST_MOVE_SPEED


def test_obstacle_is_gameobject():
    obs = Obstacle(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE)
    assert isinstance(obs, GameObject)


def test_zone_is_gameobject():
    zone = Zone(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE, TEST_ZONE_TYPE_YELLOW)
    assert isinstance(zone, GameObject)


def test_zone_has_zone_type():
    zone = Zone(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE, TEST_ZONE_TYPE_BLUE)
    assert zone.zone_type == TEST_ZONE_TYPE_BLUE


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
    model.diff_idx = TEST_GOLD_AMOUNT
    start_hp = model.hp
    obs = Obstacle(model.player.rect.x, model.player.rect.y, OBSTACLE_SIZE, OBSTACLE_SIZE)
    model.obstacles = [obs]
    model._check_collisions()
    assert model.hp < start_hp


def test_easy_no_damage():
    model = GameModel()
    model.diff_idx = TEST_ZERO_SPEED
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


def test_heal_caps_at_max_hp():
    model = GameModel()
    model.hp = MAX_HP - TEST_HP_OFFSET
    heal = HealItem(model.player.rect.x, model.player.rect.y, HEAL_SIZE, HEAL_SIZE)
    model.heals = [heal]
    model._check_collisions()
    assert model.hp == MAX_HP


def test_yellow_zone_adds_gold():
    model = GameModel()
    model.gold = TEST_GOLD_START
    zone = Zone(model.player.rect.x, model.player.rect.y, ZONE_WIDTH, ZONE_HEIGHT, TEST_ZONE_TYPE_YELLOW)
    model.zones = [zone]
    model._check_collisions()
    assert model.gold > TEST_GOLD_START


def test_blue_zone_removes_gold():
    model = GameModel()
    model.gold = TEST_GOLD_START
    zone = Zone(model.player.rect.x, model.player.rect.y, ZONE_WIDTH, ZONE_HEIGHT, TEST_ZONE_TYPE_BLUE)
    model.zones = [zone]
    model._check_collisions()
    assert model.gold < TEST_GOLD_START


def test_gold_never_negative():
    model = GameModel()
    model.gold = TEST_ZERO_SPEED
    zone = Zone(model.player.rect.x, model.player.rect.y, ZONE_WIDTH, ZONE_HEIGHT, TEST_ZONE_TYPE_BLUE)
    model.zones = [zone]
    model._check_collisions()
    assert model.gold == TEST_ZERO_SPEED


def test_gold_capped_at_target():
    model = GameModel()
    model.gold = TARGET_GOLD - TEST_GOLD_AMOUNT
    model.yellow_gold = TEST_MOVE_SPEED
    zone = Zone(model.player.rect.x, model.player.rect.y, ZONE_WIDTH, ZONE_HEIGHT, TEST_ZONE_TYPE_YELLOW)
    model.zones = [zone]
    model._check_collisions()
    assert model.gold <= TARGET_GOLD


def test_pit_kills():
    model = GameModel()
    model.player.rect.bottom = GROUND_Y
    pit = Pit(model.player.rect.centerx - TEST_PIT_OFFSET, GROUND_Y, TEST_PIT_WIDTH, TEST_PIT_HEIGHT)
    model.pits = [pit]
    model._check_collisions()
    assert model.hp == TEST_ZERO_SPEED


def test_zero_hp_game_over():
    model = GameModel()
    model.hp = TEST_ZERO_SPEED
    model._check_game_over()
    assert model.game_over is True


def test_target_gold_victory():
    model = GameModel()
    model.gold = TARGET_GOLD
    model._check_game_over()
    assert model.game_over is True
    assert model.is_victory is True


def test_model_default_difficulty():
    model = GameModel()
    assert model.diff_idx == DEF_DIF


def test_reset_clears_platforms():
    model = GameModel()
    model.platforms = [Platform(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE)]
    model.reset_state()
    assert len(model.platforms) == TEST_ZERO_SPEED


def test_reset_clears_obstacles():
    model = GameModel()
    model.obstacles = [Obstacle(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE)]
    model.reset_state()
    assert len(model.obstacles) == TEST_ZERO_SPEED


def test_reset_clears_zones():
    model = GameModel()
    model.zones = [Zone(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE, TEST_ZONE_TYPE_YELLOW)]
    model.reset_state()
    assert len(model.zones) == TEST_ZERO_SPEED


def test_game_over_no_update():
    model = GameModel()
    model.game_over = True
    start_gold = model.gold
    model.update()
    assert model.gold == start_gold


def test_move_objects_removes_offscreen():
    model = GameModel()
    model.obstacles = [Obstacle(-TEST_PLAYER_POS_X, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE)]
    model._move_objects(TEST_MOVE_SPEED)
    assert len(model.obstacles) == TEST_ZERO_SPEED


def test_move_objects_moves_left():
    model = GameModel()
    obs = Obstacle(TEST_PLAYER_POS_X, TEST_ZERO_SPEED, TEST_OBJ_SIZE, TEST_OBJ_SIZE)
    model.obstacles = [obs]
    model._move_objects(TEST_MOVE_SPEED_SMALL)
    assert obs.rect.x == TEST_PLAYER_POS_X - TEST_MOVE_SPEED_SMALL


def test_instant_death_obstacle():
    model = GameModel()
    model.diff_idx = INSTANT_DEATH_IDX
    obs = Obstacle(model.player.rect.x, model.player.rect.y, OBSTACLE_SIZE, OBSTACLE_SIZE)
    model.obstacles = [obs]
    model._check_collisions()
    assert model.hp == TEST_ZERO_SPEED


def test_is_victory_false_on_death():
    model = GameModel()
    model.hp = TEST_ZERO_SPEED
    model._check_game_over()
    assert model.is_victory is False


def test_level_generator_reset():
    lg = LevelGenerator()
    lg.reset(TEST_ZERO_SPEED)
    assert lg.distance_since_last == TEST_ZERO_SPEED
    assert lg.next_dist > TEST_ZERO_SPEED


def test_generate_chunk_increments_distance():
    lg = LevelGenerator()
    lg.reset(TEST_ZERO_SPEED)
    lg.distance_since_last = TEST_ZERO_SPEED
    lg.next_dist = TEST_LARGE_DISTANCE
    model = GameModel()
    lg.generate_chunk(model, TEST_MOVE_SPEED, TEST_ZERO_SPEED)
    assert lg.distance_since_last == TEST_MOVE_SPEED


def test_button_click_inside():
    btn = Button(TEST_BUTTON_X, TEST_BUTTON_Y, TEST_BUTTON_WIDTH, TEST_BUTTON_HEIGHT, TEST_BUTTON_TEXT_DEFAULT, TEST_BUTTON_TEXT_DEFAULT)
    assert btn.is_clicked((TEST_BUTTON_X + TEST_GOLD_AMOUNT, TEST_BUTTON_Y + TEST_GOLD_AMOUNT)) is True


def test_button_click_outside():
    btn = Button(TEST_BUTTON_X, TEST_BUTTON_Y, TEST_BUTTON_WIDTH, TEST_BUTTON_HEIGHT, TEST_BUTTON_TEXT_DEFAULT, TEST_BUTTON_TEXT_DEFAULT)
    assert btn.is_clicked((TEST_ZERO_SPEED, TEST_ZERO_SPEED)) is False


def test_button_stores_action():
    btn = Button(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_RECT_EDGE, TEST_RECT_EDGE, TEST_BUTTON_TEXT_DEFAULT, TEST_BUTTON_ACTION)
    assert btn.action == TEST_BUTTON_ACTION


def test_button_stores_text():
    btn = Button(TEST_ZERO_SPEED, TEST_ZERO_SPEED, TEST_RECT_EDGE, TEST_RECT_EDGE, TEST_BUTTON_TEXT, TEST_BUTTON_TEXT_DEFAULT)
    assert btn.text == TEST_BUTTON_TEXT


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
    controller.handle_menu_click(TEST_ACTION_DIFF_MINUS)
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
    controller.handle_menu_click(TEST_ACTION_Y_GOLD_MINUS)
    assert model.yellow_gold == TEST_YELLOW_GOLD_START - TEST_GOLD_AMOUNT


def test_y_gold_minus_capped_at_min():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    model.yellow_gold = MIN_YELLOW_GOLD
    controller.handle_menu_click(TEST_ACTION_Y_GOLD_MINUS)
    assert model.yellow_gold == MIN_YELLOW_GOLD


def test_c_dmg_minus_decreases():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    model.char_dmg = TEST_DAMAGE_BASE
    controller.handle_menu_click(TEST_ACTION_C_DMG_MINUS)
    assert model.char_dmg == TEST_DAMAGE_MINUS


def test_c_dmg_minus_capped_at_min():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    model.char_dmg = MIN_CHAR_DAMAGE
    controller.handle_menu_click(TEST_ACTION_C_DMG_MINUS)
    assert model.char_dmg == MIN_CHAR_DAMAGE


def test_rhythm_toggles():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    start = model.rhythm_mode
    controller.handle_menu_click("rhythm_minus")
    assert model.rhythm_mode != start


def test_setup_menu_buttons_creates_buttons():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    assert len(controller.buttons) > TEST_ZERO_SPEED


def test_view_has_sound_manager():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    view = GameView(screen)
    assert view.sound_manager is not None


def test_sound_manager_toggle():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    view = GameView(screen)
    start = view.sound_manager.enabled
    view.sound_manager.toggle()
    assert view.sound_manager.enabled != start


def test_sound_manager_play_when_disabled():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    view = GameView(screen)
    view.sound_manager.enabled = False
    view.sound_manager.play("jump")
    assert True


def test_draw_menu_does_not_crash():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)
    view.draw_menu(controller.buttons, model)
    assert True


def test_draw_game_does_not_crash():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    model = GameModel()
    view = GameView(screen)
    view.draw_game(model)
    assert True


def test_draw_overlay_does_not_crash():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    view = GameView(screen)
    view.draw_overlay(TEST_OVERLAY_TITLE, TEST_OVERLAY_SUBTITLE, TEST_OVERLAY_COLOR)
    assert True