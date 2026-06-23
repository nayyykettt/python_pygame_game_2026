import random
import time
from settings import *

#Базовый класс для объектов в игре.
class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, speed):
        self.rect.x -= speed

#класс Игрока.(наследование)
class Player(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.velocity_y = 0
        self.jump_count = 0

    def jump(self, max_jumps):
        if self.jump_count < max_jumps:
            self.velocity_y = JUMP_VELOCITY_START
            self.jump_count += 1

    #Алгоритм
    def update_physics(self, platforms):
        self.rect.y += self.velocity_y

        #столкновение с платформой
        if self.velocity_y < 0:
            for plat in platforms:
                if self.rect.colliderect(plat.rect):
                    self.rect.top = plat.rect.bottom
                    self.velocity_y = 0
                    break
                
        self.velocity_y += GRAVITY
        current_floor = GROUND_Y
        #определяем находится ли игрок над платформой. Делаем её полом.
        for plat in platforms:
            if self.rect.right > plat.rect.left and self.rect.left < plat.rect.right:
                if self.rect.bottom - self.velocity_y - GRAVITY <= plat.rect.top + PLATFORM_EXT_SIZE:
                    current_floor = plat.rect.top
                    break
#Столкновение снизу
        if self.rect.bottom >= current_floor:
            self.rect.bottom = current_floor
            self.velocity_y = 0
            self.jump_count = 0

        if self.rect.y < 0:
            self.rect.y = 0
            if self.velocity_y < 0:
                self.velocity_y = 0

#наследуются без изменений
class Obstacle(GameObject):
    pass
class Platform(GameObject):
    pass
class Pit(GameObject):
    pass
class HealItem(GameObject):
    pass
class Zone(GameObject):
    def __init__(self, x, y, width, height, zone_type):
        super().__init__(x, y, width, height)
        self.zone_type = zone_type

class WordManager:
    def __init__(self):
        self.words = []
        self.char_colors = []
        self.current_idx = 0
        self.words_typed = 0
        self.wrong_chars = 0
        self.total_chars = 0

#Алгоритм вывод ряда
    def init_words(self, diff_idx):
        bank = WORDS_BANK[diff_idx]
        self.words = [random.choice(bank) for _ in range(WORDS_IN_ROW_COUNT)]
        self.current_idx = 0
        self.char_colors = [GRAY] * len(self.words[0])

#Алгоритм писанины
    def process_input(self, char_typed, diff_idx) -> bool:
        if char_typed not in RUSSIAN_ALPHABET:
            return False

        self.total_chars += 1
        target = self.words[0][self.current_idx].lower()
        damage_taken = False

        if char_typed == target:
            self.char_colors[self.current_idx] = GREEN
        else:
            self.char_colors[self.current_idx] = RED
            self.wrong_chars += 1
            damage_taken = True

        self.current_idx += 1
        return damage_taken

    #Алгоритм конца слова
    def check_word_completion(self, diff_idx) -> bool:
        if self.current_idx >= len(self.words[0]):
            self.words_typed += 1
            self.words.pop(0)
            self.words.append(random.choice(WORDS_BANK[diff_idx]))
            self.current_idx = 0
            self.char_colors = [GRAY] * len(self.words[0])
            return True
        return False

class LevelGenerator:
    def __init__(self):
        self.distance_since_last = 0
        self.next_dist = 0

    def reset(self, diff_idx):
        self.distance_since_last = 0
        self.next_dist = random.randint(*OBSTACLE_DISTANCE_RANGES[diff_idx])

    #Алгоритм 
    def _spawn_random_zone(self, model, start_x, width, base_y, diff_idx, chance=ZONE_CHANCE_EASY):
        if random.random() > chance or width < ZONE_WIDTH + ZONE_WIDTH_SPAWN:
            return

        zx = start_x + random.randint(ZONE_MIN_PADDING_X, width - ZONE_WIDTH - ZONE_MIN_PADDING_X)
        zy = base_y - ZONE_HEIGHT 

        z_type = "yellow"
        if diff_idx == 2:
            z_type = random.choices(["yellow", "blue"], weights=[ZONE_WEIGHT_YELLOW, ZONE_WEIGHT_BLUE])[0]

        if diff_idx == 3:
            z_type = random.choices(["yellow", "blue"], weights=[ZONE_WEIGHT_YELLOW_FUN, ZONE_WEIGHT_BLUE_FUN])[0]

        model.zones.append(Zone(zx, zy, ZONE_WIDTH, ZONE_HEIGHT, z_type))

    #Алгоритм
    def _spawn_heal(self, model, start_x, width, base_y):
        if random.random() > HEAL_CHANCE or width < HEAL_SIZE + HEAL_MIN_PADDING_X * 2:
            return

        hx = start_x + random.randint(HEAL_MIN_PADDING_X, width - HEAL_SIZE - HEAL_MIN_PADDING_X)
        hy = base_y - HEAL_SIZE - random.randint(0, HEAL_SPAWN_HEIGHT_VARIATION)
        model.heals.append(HealItem(hx, hy, HEAL_SIZE, HEAL_SIZE))

    #Алгоритм
    def generate_chunk(self, model, speed, diff_idx):
        self.distance_since_last += speed
        if self.distance_since_last < self.next_dist:
            return

        #расстояние за прыжок
        jump_frames = (2 * abs(JUMP_VELOCITY_START)) / GRAVITY
        max_jump_dist = jump_frames * speed

        #Случайная генерация
        chunk_types = ["ground_rush", "random_platforms", "pit"]
        weights = CHUNK_WEIGHTS_EASY if diff_idx == 0 else CHUNK_WEIGHTS_HARD
        selected = random.choices(chunk_types, weights=weights)[0]
        chunk_width = 0

        x_start = WIDTH + SPAWN_OFFSET_X

#генерация по типам
        if selected == "ground_rush":
            length = random.randint(GROUND_MIN_LENGTH, GROUND_MAX_LENGTH)
            chunk_width = length
            #заборы
            if diff_idx != 0:
                obs_count = random.randint(1, max(1, length // GROUND_OBSTACLE_DENSITY))
                for _ in range(obs_count):
                    ox = x_start + random.randint(OBS_SPAWN_MIN_OFFSET, length - OBSTACLE_SIZE - OBS_PADDING_GROUND)
                    model.obstacles.append(Obstacle(ox, GROUND_Y - OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE))

            for _ in range(random.randint(1, 2)):
                self._spawn_random_zone(model, x_start, length, GROUND_Y, diff_idx, chance=ZONE_CHANCE_RUSH)

            self._spawn_heal(model, x_start, length, GROUND_Y)

        elif selected == "random_platforms":
            num_plats = random.randint(PLAT_MIN_COUNT, PLAT_MAX_COUNT)
            current_x = x_start

            for _ in range(num_plats):
                plat_w = random.randint(PLAT_MIN_WIDTH, PLAT_MAX_WIDTH)
                plat_y = GROUND_Y - random.randint(PLAT_MIN_HEIGHT, PLAT_MAX_HEIGHT)

                model.platforms.append(Platform(current_x, plat_y, plat_w, PLAT_THICKNESS))

                if diff_idx != 0 and plat_w > PLAT_MIN_OBSTACLE and random.random() < PLAT_OBSTACLE_CHANCE:
                    ox = current_x + random.randint(PLAT_OBSTACLE_PADDING, plat_w - OBSTACLE_SIZE - PLAT_OBSTACLE_PADDING)
                    model.obstacles.append(Obstacle(ox, plat_y - OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE))

                self._spawn_random_zone(model, current_x, plat_w, plat_y, diff_idx, chance=ZONE_CHANCE_PLAT)
                self._spawn_heal(model, current_x, plat_w, plat_y)

                gap = random.randint(GAP_MIN, int(max_jump_dist * GAP_MAX_FACTOR))
                current_x += plat_w + gap

            chunk_width = current_x - x_start

        elif selected == "pit":
            pit_w = random.randint(PIT_MIN_WIDTH, int(max_jump_dist * PIT_MAX_FACTOR))
            model.pits.append(Pit(x_start, GROUND_Y, pit_w, PIT_HEIGHT))
            chunk_width = pit_w
        #сброс счетчика
        self.distance_since_last = -chunk_width
        min_d, max_d = OBSTACLE_DISTANCE_RANGES[diff_idx]
        lower_bound = max(int(max_jump_dist) + SPAWN_RESET_OFFSET, min_d)

        #дистанция до след чанка
        if lower_bound >= max_d:
            self.next_dist = lower_bound
        else:
            self.next_dist = random.randint(lower_bound, max_d)

class GameModel:
    def __init__(self):
        self.diff_idx = DEF_DIF
        self.yellow_gold = DEF_YELLOW_GOLD
        self.blue_gold = DEF_BLUE_GOLD
        self.char_dmg = DEF_CHAR_DAMAGE
        self.obs_dmg = DEF_OBSTACLE_DAMAGE
        self.heal_amt = DEF_HEAL_AMOUNT
        self.rhythm_mode = DEF_RHYTHM_MODE

        self.player = Player(PLAYER_START_X, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
        self.word_manager = WordManager()
        self.generator = LevelGenerator()

        self.reset_state()

    #Алгоритм сброса харк
    def reset_state(self):
        self.hp = MAX_HP
        self.gold = START_GOLD
        self.game_over = False
        self.is_victory = False
        self.start_time = time.time()
        self.total_time = 0
        self.coin_collected = False
        self.obstacle_hit = False

        self.platforms = []
        self.obstacles = []
        self.pits = []
        self.zones = []
        self.heals = []

        self.player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_SIZE)
        self.word_manager = WordManager()
        self.word_manager.init_words(self.diff_idx)
        self.generator.reset(self.diff_idx)

    #Алгоритм обновление скорости, физики, колизий и прочего.
    def update(self):
        if self.game_over:
            return

        progression = 1.0 + ((self.gold / TARGET_GOLD) * PROGRESSION_SCALE)
        diff_factor = DIFFICULTY_MULTIPLIERS[self.diff_idx] * progression
        speed = min(int(BASE_SPEED * diff_factor), MAX_SPEED)

        self.player.update_physics(self.platforms)
        self.generator.generate_chunk(self, speed, self.diff_idx)

        self._move_objects(speed)
        self._check_collisions()
        self._check_game_over()

    #Алгоритм псведо движения
    def _move_objects(self, speed):
        for obj_list in [self.platforms, self.pits, self.obstacles, self.heals, self.zones]:
            for obj in obj_list[:]:
                obj.move(speed)
                if obj.rect.right < 0:
                    obj_list.remove(obj)

    #Алгоритм коллизий
    def _check_collisions(self):
        for pit in self.pits:
            if pit.rect.left + PIT_COLLISION_MARGIN < self.player.rect.centerx < pit.rect.right - PIT_COLLISION_MARGIN:
                if self.player.rect.bottom >= GROUND_Y: 
                    self.hp = 0

        for obs in self.obstacles[:]:
            if self.player.rect.colliderect(obs.rect):
                if self.diff_idx == INSTANT_DEATH_IDX:
                    self.hp = 0
                elif self.diff_idx != NO_DAMAGE_IDX: 
                    self.hp -= self.obs_dmg
                self.obstacle_hit = True
                self.obstacles.remove(obs)

        for heal in self.heals[:]:
            if self.player.rect.colliderect(heal.rect):
                self.hp = min(MAX_HP, self.hp + self.heal_amt)
                self.heals.remove(heal)

        for zone in self.zones[:]:
            if self.player.rect.colliderect(zone.rect):
                self.gold += self.yellow_gold if zone.zone_type == "yellow" else -self.blue_gold
                self.gold = max(0, min(TARGET_GOLD, self.gold))
                if zone.zone_type == "yellow":
                    self.coin_collected = True
                self.zones.remove(zone)

    #Алгоритм конца
    def _check_game_over(self):
        if self.hp <= 0 or self.gold >= TARGET_GOLD:
            self.game_over = True
            self.is_victory = (self.gold >= TARGET_GOLD)
            self.total_time = time.time() - self.start_time