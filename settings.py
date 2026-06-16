import pygame
pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
FPS = 60

START_Y = 130
MENU_START_Y = 130
MENU_SPASING_Y = 65
MENU_LABEL_OFFSET_X = 380
MENU_VERTICAL_OFFSET = 5
SETTINGS_HORIZONTAL_OFFSET = 220
RYTM_CORD = 40, 40

GROUND_LINE_SIZE = 5
FONT_SIZE = 40
LARGE_FONT_SIZE = 65
ACTIVE_FONT_SIZE = 90
MENU_FONT_SIZE = 32
BUTTON_BORDER_RADIUS = 5
MENU_Y = 40

THORN_WIDTH = 20
THORN_HEIGHT = 25
THORN_DEEP = 15

PLATFORM_BORDER_RADIUS = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)
GREEN = (34, 177, 76)
RED = (237, 28, 36)
PLAYER_BLUE = (0, 80, 239)
YELLOW = (255, 201, 14)
CYAN_ZONE = (0, 162, 232)
PURPLE = (148, 0, 211)
PROPORTIONAL_COEFFICIENT = 4/3
PLAYER_SIZE = 60
OBSTACLE_SIZE = 60
HEAL_SIZE = 40
ZONE_HEIGHT = 90
ZONE_WIDTH = 90
GROUND_Y = HEIGHT - 200
SPAWN_OFFSET_X = 50
BRIDGE_HEIGHT_1 = 130
BRIDGE_HEIGHT_2 = 100
BRIDGE_HEIGHT_3 = 230
DANGER_PLATFORM_HEIGHT = 120
JUMP_VELOCITY_START = -22.5
GRAVITY = 1.5
DIFFICULTY_NAMES = ["Легкий", "Средний", "Сложный", "Веселый"]
DIFFICULTY_MULTIPLIERS = [0.8, 1.0, 1.35, 1.75]
OBSTACLE_DISTANCE_RANGES = [
    (800, 1300), (715, 1235), (525, 975), (500, 1000)
]

WORDS_BANK = [
    ["вода", "небо", "луна", "стол", "стул", "рука", "нога", "глаз", "день", "ночь"],
    ["книга", "дверь", "дождь", "город", "рынок", "ведро", "птица", "актер", "океан", "трава"],
    ["солнце", "дерево", "дорога", "яблоко", "золото", "корова", "собака", "молоко", "ворона", "работа"],
    ["планета", "человек", "корабль", "телефон", "самолет", "капуста", "свобода", "красота", "природа", "картина"]
]

RUSSIAN_ALPHABET = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
WORDS_IN_ROW_COUNT = 4
TARGET_GOLD = 200

IMAGE_DIR = "images"
TEX_PLAYER = f"{IMAGE_DIR}/Typing_dinO.png"
TEX_OBSTACLE = f"{IMAGE_DIR}/zaborchik_KRIVOY.png"
TEX_ZONE_YELLOW = f"{IMAGE_DIR}/monetka_yellow.png"
TEX_ZONE_BLUE = f"{IMAGE_DIR}/monetka_blue.png"
TEX_BG = f"{IMAGE_DIR}/45908.png"