import pygame
pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
FPS = 60

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
PLAYER_SIZE = 60
OBSTACLE_SIZE = 60
HEAL_SIZE = 40
ZONE_HEIGHT = 15
ZONE_WIDTH = 120
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
