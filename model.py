import random
import time
from settings import *

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, speed):
        self.rect.x -= speed

class Player(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.velocity_y = 0
        self.jump_count = 0

    def jump(self, max_jumps):
        if self.jump_count < max_jumps:
            self.velocity_y = JUMP_VELOCITY_START
            self.jump_count += 1

    def update_physics(self, platforms):
        self.rect.y += self.velocity_y
        
        if self.velocity_y < 0:
            for plat in platforms:
                if self.rect.colliderect(plat.rect):
                    self.rect.top = plat.rect.bottom
                    self.velocity_y = 0
                    break

        self.velocity_y += GRAVITY
        current_floor = GROUND_Y
        
        for plat in platforms:
            if self.rect.right > plat.rect.left and self.rect.left < plat.rect.right:
                if self.rect.bottom - self.velocity_y - GRAVITY <= plat.rect.top + 15:
                    current_floor = plat.rect.top
                    break

        if self.rect.bottom >= current_floor:
            self.rect.bottom = current_floor
            self.velocity_y = 0
            self.jump_count = 0

        if self.rect.y < 0:
            self.rect.y = 0
            if self.velocity_y < 0:
                self.velocity_y = 0

class Obstacle(GameObject): pass
class Platform(GameObject): pass
class Pit(GameObject): pass
class HealItem(GameObject): pass
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

    def init_words(self, diff_idx):
        bank = WORDS_BANK[diff_idx]
        self.words = [random.choice(bank) for _ in range(WORDS_IN_ROW_COUNT)]
        self.current_idx = 0
        self.char_colors = [GRAY] * len(self.words[0])

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

    def _spawn_random_zone(self, model, start_x, width, base_y, diff_idx, chance=0.75):
        if random.random() > chance or width < ZONE_WIDTH + 20:
            return
            
        zx = start_x + random.randint(10, width - ZONE_WIDTH - 10)
        zy = base_y - ZONE_HEIGHT 
        
        z_type = "yellow"
        if diff_idx in (2, 3):
            z_type = random.choices(["yellow", "blue"], weights=[50, 50])[0]
            
        model.zones.append(Zone(zx, zy, ZONE_WIDTH, ZONE_HEIGHT, z_type))

    def generate_chunk(self, model, speed, diff_idx):
        self.distance_since_last += speed
        if self.distance_since_last < self.next_dist:
            return

        jump_frames = (2 * abs(JUMP_VELOCITY_START)) / GRAVITY
        max_jump_dist = jump_frames * speed
        
        chunk_types = ["ground_rush", "random_platforms", "pit"]
        weights = [45, 35, 20] if diff_idx == 0 else [30, 50, 20]
        selected = random.choices(chunk_types, weights=weights)[0]
        chunk_width = 0

        x_start = WIDTH + SPAWN_OFFSET_X
        
        if selected == "ground_rush":
            length = random.randint(400, 1000)
            chunk_width = length
            
            if diff_idx != 0:
                obs_count = random.randint(1, max(1, length // 250))
                for _ in range(obs_count):
                    ox = x_start + random.randint(50, length - OBSTACLE_SIZE - 50)
                    model.obstacles.append(Obstacle(ox, GROUND_Y - OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE))
            
            for _ in range(random.randint(1, 2)):
                self._spawn_random_zone(model, x_start, length, GROUND_Y, diff_idx, chance=0.8)

        elif selected == "random_platforms":
            num_plats = random.randint(1, 3)
            current_x = x_start
            
            for _ in range(num_plats):
                plat_w = random.randint(200, 600)
                plat_y = GROUND_Y - random.randint(60, 150) 
                
                model.platforms.append(Platform(current_x, plat_y, plat_w, 20))
                
                if diff_idx != 0 and plat_w > 300 and random.random() < 0.35:
                    ox = current_x + random.randint(50, plat_w - OBSTACLE_SIZE - 50)
                    model.obstacles.append(Obstacle(ox, plat_y - OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE))
                
                self._spawn_random_zone(model, current_x, plat_w, plat_y, diff_idx, chance=0.85)
                
                gap = random.randint(50, int(max_jump_dist * 0.6))
                current_x += plat_w + gap
            
            chunk_width = current_x - x_start

        elif selected == "pit":
            pit_w = random.randint(100, int(max_jump_dist * 0.8))
            model.pits.append(Pit(x_start, GROUND_Y, pit_w, 40))
            chunk_width = pit_w

        self.distance_since_last = -chunk_width
        min_d, max_d = OBSTACLE_DISTANCE_RANGES[diff_idx]
        self.next_dist = random.randint(max(int(max_jump_dist) + 40, min_d), max_d)

class GameModel:
    def __init__(self):
        self.diff_idx = 1
        self.yellow_gold = 10
        self.blue_gold = 10
        self.char_dmg = 0.2
        self.obs_dmg = 0.5
        self.heal_amt = 1.0
        self.rhythm_mode = False

        self.player = Player(200, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
        self.word_manager = WordManager()
        self.generator = LevelGenerator()
        
        self.reset_state()

    def reset_state(self):
        self.hp = 10.0
        self.gold = 0
        self.game_over = False
        self.is_victory = False
        self.start_time = time.time()
        self.total_time = 0
        
        self.platforms = []
        self.obstacles = []
        self.pits = []
        self.zones = []
        self.heals = []
        
        self.player = Player(200, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE)
        self.word_manager = WordManager()
        self.word_manager.init_words(self.diff_idx)
        self.generator.reset(self.diff_idx)

    def update(self):
        if self.game_over: return

        progression = 1.0 + ((self.gold / TARGET_GOLD) * 1.5)
        diff_factor = DIFFICULTY_MULTIPLIERS[self.diff_idx] * progression
        speed = min(int(12 * diff_factor), 35)

        self.player.update_physics(self.platforms)
        self.generator.generate_chunk(self, speed, self.diff_idx)
        
        self._move_objects(speed)
        self._check_collisions()
        self._check_game_over()

    def _move_objects(self, speed):
        for obj_list in [self.platforms, self.pits, self.obstacles, self.heals, self.zones]:
            for obj in obj_list[:]:
                obj.move(speed)
                if obj.rect.right < 0:
                    obj_list.remove(obj)

    def _check_collisions(self):
        for pit in self.pits:
            if pit.rect.left + 12 < self.player.rect.centerx < pit.rect.right - 12:
                if self.player.rect.bottom >= GROUND_Y: self.hp = 0

        for obs in self.obstacles[:]:
            if self.player.rect.colliderect(obs.rect):
                if self.diff_idx == 3: self.hp = 0
                elif self.diff_idx != 0: self.hp -= self.obs_dmg
                self.obstacles.remove(obs)

        for heal in self.heals[:]:
            if self.player.rect.colliderect(heal.rect):
                self.hp = min(10.0, self.hp + self.heal_amt)
                self.heals.remove(heal)

        for zone in self.zones[:]:
            if self.player.rect.colliderect(zone.rect):
                self.gold += self.yellow_gold if zone.zone_type == "yellow" else -self.blue_gold
                self.gold = max(0, min(TARGET_GOLD, self.gold))
                self.zones.remove(zone)

    def _check_game_over(self):
        if self.hp <= 0 or self.gold >= TARGET_GOLD:
            self.game_over = True
            self.is_victory = (self.gold >= TARGET_GOLD)
            self.total_time = time.time() - self.start_time
