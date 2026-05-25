import pygame
import sys
import math
import random
import os
import json

# 1. 基础配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40  
MAP_SIZE = 30   # 30x30 大空间

# 颜色定义
COLOR_GRASS = (34, 139, 34)
COLOR_TILLED = (139, 69, 19)     
COLOR_WATERED = (92, 51, 23)      
COLOR_PIT = (105, 105, 105)       
COLOR_WATER_PIT = (0, 191, 255)   
COLOR_ROCK = (128, 128, 128)
COLOR_SEED = (144, 238, 144)
COLOR_RIPE = (255, 215, 0)
COLOR_BIN = (30, 144, 255)
COLOR_CRAFTING = (34, 139, 100)   
COLOR_BG = (40, 40, 40)          
COLOR_TEXT = (255, 255, 255)     
COLOR_ENERGY = (0, 255, 127)     
COLOR_HEALTH = (255, 0, 50)      
COLOR_FLOOR = (210, 180, 140)    
COLOR_DUNGEON = (70, 70, 70)     
COLOR_CHEST = (218, 165, 32)     
COLOR_PORTAL = (139, 0, 0)       
COLOR_ENDLESS_PORTAL = (0, 191, 255) 
COLOR_STAIRS = (50, 205, 50)     

# 怪物颜色
COLOR_MONSTER_NORMAL = (255, 0, 0)     
COLOR_MONSTER_ELITE = (139, 0, 255)    
COLOR_MONSTER_BOSS = (0, 0, 0)         

# 建筑大门颜色
COLOR_DOOR_SHOP = (148, 0, 211)   
COLOR_DOOR_HOSP = (220, 20, 60)   
COLOR_DOOR_GUILD = (218, 165, 32) 
COLOR_DOOR_REST = (255, 127, 80)  
COLOR_DOOR_CLOTH = (75, 0, 130)   

# 全局双语文本字典
LANG_DATA = {
    "zh": {
        "loc": "当前位置", "tool": "当前工具", "lvl": "角色等级", "xp": "当前经验",
        "hp": "生命值", "energy": "体力值", "gold": "我的金币", "seeds": "芜菁种子",
        "turnip": "收割芜菁", "bread": "充饥面包", "ore": "铁矿材料", "bin": "出货箱暂存",
        "hoe": "锄头 (开垦/采矿)", "shovel": "铲子 (草地挖坑)", "water_can": "水壶 (土地灌溉)", "move_tool": "搬运模式 (拿起/放下)",
        "farm": "我的私人农场", "village": "丰收小镇村庄", "dungeon": "未知深渊地牢",
        "interior_shop": "杂货种子商店", "interior_hosp": "小镇爱心诊所",
        "interior_guild": "冒险者公会大厅", "interior_rest": "美味风味餐馆", "interior_cloth": "精致潮流服装店",
        "guide_title": "--- 🎮 快捷键操作指南 ---", "guide_1": "[1/2/3/4] 切换工具  [E] 吃面包",
        "guide_2": "[空格] 睡觉 (跨天并清算出货箱)", "guide_3": "[ESC] 呼出/关闭快捷系统菜单",
        "craft_title": "--- 🛠️ 简易合成台菜单 ---", "craft_1": "[F1] 烘焙面包 <- 2个芜菁",
        "craft_2": "[F2] 自制种子 <- 10金币+1铁矿", "craft_3": "[F3] 升级铁矿镐 <- 50G+5铁矿",
        "menu_title": "=== 系统快捷菜单 ===", "menu_save": "保存游戏进度", "menu_lang": "切换语言 (ZH/EN)",
        "menu_resume": "返回游戏 (或再按ESC)", "dungeon_info": "地牢层数", "story": "主线剧情", "endless": "无尽挑战",
        "label_bin": "出货", "label_portal": "地牢", "label_endless_portal": "无尽", "label_crafting_table": "合成",
        "label_door_shop": "商店", "label_door_hosp": "医院", "label_door_guild": "工会", "label_door_rest": "餐馆", "label_door_cloth": "服装",
        "label_npc_shop": "商人", "label_npc_hosp": "医生", "label_npc_guild": "团长", "label_npc_rest": "厨师", "label_npc_cloth": "裁缝",
        "label_exit": "出口", "label_dungeon_exit": "回城", "label_dungeon_to_endless": "无尽", "label_stairs": "下层", "label_chest": "宝箱",
        "holding": "手中搬运", "holding_none": "无",
        "cust_title": "=== 🎭 形象自定义捏脸中心 ===", "cust_gender": "[G] 切换性别: ", "cust_style": "[H] 切换发型: ",
        "cust_color": "[C] 切换发色: ", "cust_enter": "【 按 ENTER 回车键 开启大冒险 】", "male": "汉子 (蓝色校服)", "female": "妹子 (粉色裙子)",
        "hair_1": "利落寸头", "hair_2": "双马尾长发", "hair_3": "杀马特爆炸头"
    },
    "en": {
        "loc": "Location", "tool": "Active Tool", "lvl": "Level", "xp": "XP",
        "hp": "HP", "energy": "Energy", "gold": "Gold", "seeds": "Seeds",
        "turnip": "Turnip", "bread": "Bread", "ore": "Iron Ore", "bin": "In Bin",
        "hoe": "Hoe (Till/Mine)", "shovel": "Shovel (Dig Pit)", "water_can": "Water Can (Irrigate)", "move_tool": "Move Mode (Pick/Place)",
        "farm": "MY PRIVATE FARM", "village": "HARVEST VILLAGE", "dungeon": "UNKNOWN DUNGEON",
        "interior_shop": "SEED GENERAL SHOP", "interior_hosp": "VILLAGE CLINIC",
        "interior_guild": "ADVENTURER GUILD", "interior_rest": "TASTY RESTAURANT", "interior_cloth": "CLOTHES BOUTIQUE",
        "guide_title": "--- 🎮 CONTROLS GUIDE ---", "guide_1": "[1/2/3/4] Switch Tools  [E] Eat Bread",
        "guide_2": "[SPACE] Sleep (Next Day & Sell)", "guide_3": "[ESC] Open/Close System Menu",
        "craft_title": "--- 🛠️ CRAFTING BLUEPRINTS ---", "craft_1": "[F1] Bake Bread <- 2 Turnips",
        "craft_2": "[F2] Make Seed <- 10G + 1 Ore", "craft_3": "[F3] Iron Pickaxe <- 50G + 5 Ore",
        "menu_title": "=== SYSTEM MENU ===", "menu_save": "Save Progress", "menu_lang": "Switch Language",
        "menu_resume": "Resume Game (or ESC)", "dungeon_info": "Dungeon", "story": "Story", "endless": "Endless",
        "label_bin": "Bin", "label_portal": "Portal", "label_endless_portal": "Endls", "label_crafting_table": "Craft",
        "label_door_shop": "Shop", "label_door_hosp": "Hosp", "label_door_guild": "Guild", "label_door_rest": "Rest", "label_door_cloth": "Cloth",
        "label_npc_shop": "Shop", "label_npc_hosp": "Doc", "label_npc_guild": "Guild", "label_npc_rest": "Chef", "label_npc_cloth": "Tailor",
        "label_exit": "Exit", "label_dungeon_exit": "Home", "label_dungeon_to_endless": "Endls", "label_stairs": "Next", "label_chest": "Chest",
        "holding": "Holding", "holding_none": "None",
        "cust_title": "=== 🎭 CHARACTER CREATOR ===", "cust_gender": "[G] Gender: ", "cust_style": "[H] Hair Style: ",
        "cust_color": "[C] Hair Color: ", "cust_enter": "[ Press ENTER to Start Adventure ]", "male": "Male (Blue Uniform)", "female": "Female (Pink Skirt)",
        "hair_1": "Buzzcut", "hair_2": "Twin-Tails", "hair_3": "Punk Spiky"
    }
}

class Crop:
    def __init__(self, current_age=0, is_ripe=False):
        self.growth_time = 3  
        self.current_age = current_age
        self.is_ripe = is_ripe

    def grow(self):
        if not self.is_ripe:
            self.current_age += 1
            if self.current_age >= self.growth_time:
                self.is_ripe = True

class Tile:
    def __init__(self, tile_type="grass"):
        self.type = tile_type  
        self.crop = None 

    def dig_with_shovel(self, player_inventory):
        if self.type == "grass":
            if player_inventory["energy"] >= 5:
                self.type = "pit"
                player_inventory["energy"] -= 5
                return True
        return False

    def use_watering_can(self, player_inventory):
        if player_inventory["energy"] < 3: return False
        if self.type == "tilled":
            self.type = "watered"
            player_inventory["energy"] -= 3
            return True
        elif self.type == "pit":
            self.type = "water_pit"
            player_inventory["energy"] -= 3
            return True
        return False

    def dig(self, unlocked_tools, player_inventory):
        if self.type == "grass":
            if player_inventory["energy"] >= 5:
                self.type = "tilled"
                player_inventory["energy"] -= 5
                return "dig_ground"
        elif self.type == "rock":
            if unlocked_tools["iron_pickaxe"]:
                if player_inventory["energy"] >= 10:
                    self.type = "grass"
                    player_inventory["energy"] -= 10
                    return "iron_ore"
        return None

    def plant(self, player_inventory):
        if self.type in ["tilled", "watered"] and self.crop is None:
            if player_inventory["seeds"] > 0:
                player_inventory["seeds"] -= 1
                self.crop = Crop()

class Player:
    def __init__(self):
        self.x = 400  
        self.y = 300
        self.speed = 5
        self.size = 30  
        self.gender = "male"       
        self.hair_style = 1        
        self.hair_color_index = 0  
        self.color_palette = [
            (50,50,50), (218,165,32), (139,0,0), (30,144,255), (50,205,50), (148,0,211)
        ]

    def get_center(self):
        return self.x + self.size // 2, self.y + self.size // 2

    def move(self, keys, current_map_name):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.y += self.speed

        world_max = MAP_SIZE * TILE_SIZE
        if current_map_name == "farm":
            self.x = max(0, self.x)
            self.y = max(0, min(self.y, world_max - self.size))
            if self.x > world_max - self.size:
                self.x = 5  
                return "GO_TO_VILLAGE"

        elif current_map_name == "village":
            self.x = min(self.x, world_max - self.size)
            self.y = max(0, min(self.y, world_max - self.size))
            if self.x < 0:
                self.x = world_max - self.size - 5  
                return "GO_TO_FARM"
                
        elif current_map_name.startswith("interior_") or current_map_name == "dungeon":
            self.x = max(0, min(self.x, world_max - self.size))
            self.y = max(0, min(self.y, world_max - self.size))
        return None

    def draw_model(self, screen, rx, ry, scale_size):
        body_color = (65, 105, 225) if self.gender == "male" else (255, 182, 193)
        pygame.draw.rect(screen, body_color, (rx, ry, scale_size, scale_size))
        pygame.draw.rect(screen, (255, 222, 173), (rx + int(scale_size*0.1), ry + int(scale_size*0.1), int(scale_size*0.8), int(scale_size*0.4)))

        h_color = self.color_palette[self.hair_color_index]
        if self.hair_style == 1:
            pygame.draw.rect(screen, h_color, (rx, ry, scale_size, int(scale_size * 0.15)))
        elif self.hair_style == 2:
            pygame.draw.rect(screen, h_color, (rx, ry, scale_size, int(scale_size * 0.15)))
            pygame.draw.rect(screen, h_color, (rx, ry, int(scale_size * 0.15), int(scale_size * 0.7)))
            pygame.draw.rect(screen, h_color, (rx + int(scale_size * 0.85), ry, int(scale_size * 0.15), int(scale_size * 0.7)))
        elif self.hair_style == 3:
            pygame.draw.rect(screen, h_color, (rx + int(scale_size*0.1), ry - int(scale_size*0.15), int(scale_size * 0.8), int(scale_size * 0.2)))
            pygame.draw.rect(screen, h_color, (rx + int(scale_size*0.3), ry - int(scale_size*0.3), int(scale_size * 0.4), int(scale_size * 0.2)))

    def draw(self, screen, cam_x, cam_y):
        self.draw_model(screen, self.x - cam_x, self.y - cam_y, self.size)

class Monster:
    def __init__(self, x_tile, y_tile, m_type, dungeon_lvl):
        self.x = x_tile * TILE_SIZE + 5
        self.y = y_tile * TILE_SIZE + 5
        self.type = m_type 
        stat_multiplier = 1.0 + (dungeon_lvl * 0.08)
        speed_bonus = dungeon_lvl * 0.03

        if m_type == "normal":
            self.size = 28
            self.max_hp = int(15 * stat_multiplier)
            self.speed = 1.2 + speed_bonus
            self.attack = 1.5 * stat_multiplier  
            self.color = COLOR_MONSTER_NORMAL
        elif m_type == "elite":
            self.size = 34
            self.max_hp = int(50 * stat_multiplier)
            self.speed = 1.8 + speed_bonus
            self.attack = 4.0 * stat_multiplier  
            self.color = COLOR_MONSTER_ELITE
        elif m_type == "boss":
            self.size = 45 
            self.max_hp = int(180 * stat_multiplier)
            self.speed = 0.9 + (dungeon_lvl * 0.01)
            self.attack = 12.0 * stat_multiplier 
            self.color = COLOR_MONSTER_BOSS
        self.hp = self.max_hp

    def update(self, player_obj, player_inventory):
        mx, my = self.x + self.size//2, self.y + self.size//2
        px, py = player_obj.get_center()
        dx, dy = px - mx, py - my
        dist = math.hypot(dx, dy)
        if dist > 5:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        player_rect = pygame.Rect(player_obj.x, player_obj.y, player_obj.size, player_obj.size)
        monster_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        if player_rect.colliderect(monster_rect):
            player_inventory["hp"] -= self.attack / 60.0
            if player_inventory["hp"] < 0: player_inventory["hp"] = 0

    def draw(self, screen, cam_x, cam_y):
        rx, ry = self.x - cam_x, self.y - cam_y
        pygame.draw.rect(screen, self.color, (rx, ry, self.size, self.size))
        pygame.draw.rect(screen, (100, 0, 0), (rx, ry - 8, self.size, 4))
        pygame.draw.rect(screen, (0, 255, 0), (rx, ry - 8, int(self.size * (self.hp / self.max_hp)), 4))

class TimeManager:
    def __init__(self):
        self.day = 1
        self.hour = 6
        self.minute = 30
        self.timer = 0.0

    def update(self, dt, world_maps, player_inventory):
        self.timer += (dt / 1000.0) * 1.75
        if self.timer >= 1.0:
            self.minute += int(self.timer)
            self.timer -= int(self.timer)
            if self.minute >= 60:
                self.hour += self.minute // 60
                self.minute = self.minute % 60
            if self.hour >= 24:
                self.trigger_next_day(world_maps, player_inventory)

    def trigger_next_day(self, world_maps, player_inventory):
        self.day += 1
        self.hour = 6
        self.minute = 30
        self.timer = 0.0
        player_inventory["energy"] = 100
        player_inventory["hp"] = 100 
        if player_inventory["shipping_bin"] > 0:
            player_inventory["gold"] += player_inventory["shipping_bin"] * 20
            player_inventory["shipping_bin"] = 0 

        farm_grid = world_maps["farm"]
        watered_by_pits = set()
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                if farm_grid[y][x].type == "water_pit":
                    for dy in range(-2, 3): 
                        for dx in range(-2, 3):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < MAP_SIZE and 0 <= nx < MAP_SIZE: watered_by_pits.add((ny, nx))

        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile = farm_grid[y][x]
                if (y, x) in watered_by_pits and tile.type == "tilled": tile.type = "watered"
                if hasattr(tile, 'crop') and tile.crop:
                    if tile.type == "watered": tile.crop.grow()
                if tile.type == "watered" and (y, x) not in watered_by_pits: tile.type = "tilled"

    def get_time_string(self, lang):
        day_str = "第" if lang == "zh" else "Day"
        t_str = "天" if lang == "zh" else ""
        return f"{day_str} {self.day} {t_str}  {self.hour:02d}:{self.minute:02d}"

class MapGenerator:
    @staticmethod
    def generate_farm(unlocked_endless=False):
        grid = [[Tile("grass") for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        grid[5][5].type = "bin"              
        grid[28][2].type = "portal"          
        grid[5][15].type = "crafting_table"   
        if unlocked_endless: grid[28][3].type = "endless_portal"
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                if grid[y][x].type == "grass" and random.random() < 0.07: grid[y][x].type = "rock"
        return grid

    @staticmethod
    def generate_village():
        grid = [[Tile("grass") for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        grid[6][6].type = "door_shop"   
        grid[6][22].type = "door_hosp"   
        grid[15][15].type = "door_guild"  
        grid[24][6].type = "door_rest"   
        grid[24][22].type = "door_cloth"  
        return grid

    @staticmethod
    def generate_interior(npc_type):
        grid = [[Tile("floor") for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        grid[12][15].type = npc_type  
        grid[28][15].type = "exit"    
        return grid

    @staticmethod
    def generate_dungeon(level):
        grid = [[Tile("dungeon") for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        for _ in range(random.randint(3, 5)): grid[random.randint(4,24)][random.randint(4,24)].type = "chest"
        return grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python像素农场RPG - 极致防残影完美版 v2.0")
    clock = pygame.time.Clock()
    
    win_font_path = "C:\\Windows\\Fonts\\msyh.ttc" 
    if os.path.exists(win_font_path):
        font = pygame.font.Font(win_font_path, 15)
        font_label = pygame.font.Font(win_font_path, 13)
        font_menu = pygame.font.Font(win_font_path, 18)
        font_large = pygame.font.Font(win_font_path, 24)
    else:
        font = pygame.font.Font(None, 18)
        font_label = pygame.font.Font(None, 14)
        font_menu = pygame.font.Font(None, 22)
        font_large = pygame.font.Font(None, 28)

    player = Player()
    time_manager = TimeManager()
    
    player_inventory = {"gold": 100, "iron_ore": 0, "turnip": 0, "seeds": 5, "shipping_bin": 0, "energy": 100, "bread": 1, "xp": 0, "level": 1, "hp": 100.0, "current_tool": "hoe", "held_item": None} 
    unlocked_tools = {"iron_pickaxe": False}
    dungeon_state = {"current_level": 1, "is_endless_mode": False, "unlocked_endless": False, "stairs_spawned": False, "near_crafting": False}
    
    current_lang = "zh"       
    game_state = "PLAY"       
    SAVE_FILE = "savegame.json"

    world_maps = {}
    monsters = []
    current_map_name = "farm" 
    saved_village_pos = (200, 200) 

    # 载入游戏
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f: save_data = json.load(f)
            player_inventory.update(save_data["player_inventory"])
            unlocked_tools.update(save_data["unlocked_tools"])
            dungeon_state.update(save_data["dungeon_state"])
            current_lang = save_data.get("current_lang", "zh")
            time_manager.day, time_manager.hour, time_manager.minute = save_data["time"]["day"], save_data["time"]["hour"], save_data["time"]["minute"]
            
            player.gender = save_data["player_avatar"]["gender"]
            player.hair_style = save_data["player_avatar"]["hair_style"]
            player.hair_color_index = save_data["player_avatar"]["hair_color_index"]
            
            world_maps["village"] = MapGenerator.generate_village()
            world_maps["interior_shop"] = MapGenerator.generate_interior("npc_shop")
            world_maps["interior_hosp"] = MapGenerator.generate_interior("npc_hosp")
            world_maps["interior_guild"] = MapGenerator.generate_interior("npc_guild")
            world_maps["interior_rest"] = MapGenerator.generate_interior("npc_rest")
            world_maps["interior_cloth"] = MapGenerator.generate_interior("npc_cloth")
            world_maps["dungeon"] = MapGenerator.generate_dungeon(1)
            
            farm_grid = []
            for r_data in save_data["farm_map"]:
                row = []
                for t_data in r_data:
                    tile = Tile(t_data["type"])
                    if t_data["crop"]: tile.crop = Crop(t_data["crop"]["current_age"], t_data["crop"]["is_ripe"])
                    row.append(tile)
                farm_grid.append(row)
            world_maps["farm"] = farm_grid
            game_state = "PLAY"
            print("💾 [载入] 进度加载成功。")
        except:
            if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
            game_state = "CUSTOMIZE"
    else:
        game_state = "CUSTOMIZE"

    if "farm" not in world_maps:
        world_maps["farm"] = MapGenerator.generate_farm(dungeon_state["unlocked_endless"])
        world_maps["village"] = MapGenerator.generate_village()
        world_maps["interior_shop"] = MapGenerator.generate_interior("npc_shop")
        world_maps["interior_hosp"] = MapGenerator.generate_interior("npc_hosp")
        world_maps["interior_guild"] = MapGenerator.generate_interior("npc_guild")
        world_maps["interior_rest"] = MapGenerator.generate_interior("npc_rest")
        world_maps["interior_cloth"] = MapGenerator.generate_interior("npc_cloth")
        world_maps["dungeon"] = MapGenerator.generate_dungeon(1)

    def save_game_logic():
        try:
            farm_save_data = []
            for row in world_maps["farm"]:
                row_data = []
                for tile in row:
                    row_data.append({"type": tile.type, "crop": {"current_age": tile.crop.current_age, "is_ripe": tile.crop.is_ripe} if tile.crop else None})
                farm_save_data.append(row_data)
            
            full_json_data = {
                "player_inventory": player_inventory, "unlocked_tools": unlocked_tools, "dungeon_state": dungeon_state, "current_lang": current_lang,
                "time": {"day": time_manager.day, "hour": time_manager.hour, "minute": time_manager.minute}, "farm_map": farm_save_data,
                "player_avatar": {"gender": player.gender, "hair_style": player.hair_style, "hair_color_index": player.hair_color_index}
            }
            with open(SAVE_FILE, "w", encoding="utf-8") as f: json.dump(full_json_data, f, ensure_ascii=False, indent=4)
            print("💾 [存档] 数据已保存。")
            return True
        except: return False

    def spawn_dungeon_monsters(lvl):
        dungeon_state["stairs_spawned"] = False
        m_list = []
        if lvl % 10 == 0: m_list.append(Monster(15, 12, "boss", lvl))
        elif lvl % 5 == 0:
            m_list.append(Monster(15, 12, "elite", lvl))
            for _ in range(min(5, 2 + (lvl // 15))): m_list.append(Monster(random.randint(5,25), random.randint(5,25), "normal", lvl))
        else:
            for _ in range(random.randint(3 + (lvl // 10), min(9, 4 + (lvl // 8)))): m_list.append(Monster(random.randint(5,25), random.randint(5,25), "normal", lvl))
        return m_list

    while True:
        dt = clock.tick(60) 
        L = LANG_DATA[current_lang] 
        active_grid = world_maps[current_map_name]

        cam_x = max(0, min(player.x - 240, MAP_SIZE * TILE_SIZE - 480))
        cam_y = max(0, min(player.y - 300, MAP_SIZE * TILE_SIZE - 600))

        if game_state == "PLAY":
            time_manager.update(dt, world_maps, player_inventory)
            if player_inventory["hp"] <= 0:
                current_map_name = "farm"
                player.x, player.y = 400, 300  
                monsters.clear()
                player_inventory["gold"] -= player_inventory["gold"] // 2
                player_inventory["hp"], player_inventory["energy"] = 40.0, 40 

            dungeon_state["near_crafting"] = False
            if current_map_name == "farm":
                for y in range(MAP_SIZE):
                    for x in range(MAP_SIZE):
                        if active_grid[y][x].type == "crafting_table":
                            if math.hypot((x*TILE_SIZE+20) - player.get_center()[0], (y*TILE_SIZE+20) - player.get_center()[1]) <= 75:
                                dungeon_state["near_crafting"] = True

            pt_x, pt_y = int(player.get_center()[0] // TILE_SIZE), int(player.get_center()[1] // TILE_SIZE)
            if 0 <= pt_x < MAP_SIZE and 0 <= pt_y < MAP_SIZE:
                current_tile = active_grid[pt_y][pt_x]
                if current_map_name == "farm" and current_tile.type == "portal":
                    current_map_name = "dungeon"
                    dungeon_state["current_level"], dungeon_state["is_endless_mode"] = 1, False
                    player.x, player.y = 600, 1000
                    monsters = spawn_dungeon_monsters(1)
                elif current_map_name == "farm" and current_tile.type == "endless_portal":
                    current_map_name = "dungeon"
                    dungeon_state["current_level"], dungeon_state["is_endless_mode"] = 51, True
                    player.x, player.y = 600, 1000
                    monsters = spawn_dungeon_monsters(51)
                elif current_map_name == "dungeon" and current_tile.type == "stairs":
                    dungeon_state["current_level"] += 1
                    player.x, player.y = 600, 1000
                    world_maps["dungeon"] = MapGenerator.generate_dungeon(dungeon_state["current_level"])
                    monsters = spawn_dungeon_monsters(dungeon_state["current_level"])
                elif current_map_name == "dungeon" and current_tile.type == "dungeon_exit":
                    current_map_name = "farm"
                    player.x, player.y = 400, 300
                    monsters.clear()
                elif current_map_name == "dungeon" and current_tile.type == "dungeon_to_endless":
                    dungeon_state["current_level"], dungeon_state["is_endless_mode"] = 51, True
                    player.x, player.y = 600, 1000
                    world_maps["dungeon"] = MapGenerator.generate_dungeon(51)
                    monsters = spawn_dungeon_monsters(51)
                elif current_map_name == "village" and current_tile.type.startswith("door_"):
                    saved_village_pos = (player.x, player.y + 40) 
                    current_map_name = current_tile.type.replace("door_", "interior_")
                    player.x, player.y = 600, 1000
                elif current_map_name.startswith("interior_") and current_tile.type == "exit":
                    current_map_name = "village"
                    player.x, player.y = saved_village_pos

            if current_map_name == "dungeon":
                for monster in monsters: monster.update(player, player_inventory) 
                if len(monsters) == 0 and not dungeon_state["stairs_spawned"]:
                    dungeon_state["stairs_spawned"] = True
                    if dungeon_state["current_level"] < 50 or dungeon_state["is_endless_mode"]: active_grid[15][15].type = "stairs"
                    elif dungeon_state["current_level"] == 50 and not dungeon_state["is_endless_mode"]:
                        dungeon_state["unlocked_endless"] = True
                        world_maps["farm"] = MapGenerator.generate_farm(True)
                        active_grid[15][14].type = "dungeon_exit"        
                        active_grid[15][16].type = "dungeon_to_endless"  

        # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif game_state == "CUSTOMIZE" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g: player.gender = "female" if player.gender == "male" else "male"
                elif event.key == pygame.K_h: player.hair_style = player.hair_style + 1 if player.hair_style < 3 else 1
                elif event.key == pygame.K_c: player.hair_color_index = (player.hair_color_index + 1) % len(player.color_palette)
                elif event.key == pygame.K_RETURN:
                    game_state = "PLAY"
                    save_game_logic()
                continue

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_state == "MENU":
                    if event.button == 1: 
                        if 240 <= mouse_x <= 440 and 210 <= mouse_y <= 250:
                            if current_map_name != "dungeon": save_game_logic()
                        elif 240 <= mouse_x <= 440 and 270 <= mouse_y <= 310: current_lang = "en" if current_lang == "zh" else "zh"
                        elif 240 <= mouse_x <= 440 and 330 <= mouse_y <= 370: game_state = "PLAY"
                    continue 

                world_click_x = mouse_x + cam_x
                world_click_y = mouse_y + cam_y
                tile_x, tile_y = int(world_click_x // TILE_SIZE), int(world_click_y // TILE_SIZE)
                
                if 0 <= tile_x < MAP_SIZE and 0 <= tile_y < MAP_SIZE:
                    t_cx, t_cy = tile_x * TILE_SIZE + TILE_SIZE // 2, tile_y * TILE_SIZE + TILE_SIZE // 2
                    if math.hypot(t_cx - player.get_center()[0], t_cy - player.get_center()[1]) > 70: continue  
                    target_tile = active_grid[tile_y][tile_x]

                    if event.button == 1: 
                        if current_map_name == "dungeon":
                            hit_any = False
                            for monster in monsters[:]:
                                m_cx, m_cy = monster.x + monster.size//2, monster.y + monster.size//2
                                if math.hypot(world_click_x - m_cx, world_click_y - m_cy) < 50:
                                    monster.hp -= 10
                                    hit_any = True
                                    if monster.hp <= 0:
                                        monsters.remove(monster)
                                        player_inventory["xp"] += 15 if monster.type == "normal" else (40 if monster.type == "elite" else 150)
                                        if player_inventory["xp"] >= player_inventory["level"] * 50: player_inventory["level"] += 1
                                        if monster.type == "boss": player_inventory["iron_ore"] += 3; player_inventory["gold"] += 100
                                        else:
                                            if random.random() < 0.5: player_inventory["iron_ore"] += 1
                            if target_tile.type == "chest": target_tile.type = "dungeon"; player_inventory["gold"] += 40; player_inventory["bread"] += 1
                            if hit_any: continue
                        
                        if current_map_name == "farm" and player_inventory["current_tool"] == "move":
                            movable_types = ["bin", "portal", "endless_portal", "crafting_table", "water_pit"]
                            if player_inventory["held_item"] is None:
                                if target_tile.type in movable_types:
                                    player_inventory["held_item"] = target_tile.type
                                    target_tile.type = "grass"
                            else:
                                if target_tile.type == "grass" and target_tile.crop is None:
                                    target_tile.type = player_inventory["held_item"]
                                    player_inventory["held_item"] = None 
                            continue 

                        if target_tile.type == "bin" and current_map_name == "farm":
                            if player_inventory["turnip"] > 0: player_inventory["shipping_bin"] += player_inventory["turnip"]; player_inventory["turnip"] = 0
                        elif target_tile.type == "npc_shop":
                            if player_inventory["turnip"] > 0: player_inventory["gold"] += player_inventory["turnip"] * 12; player_inventory["turnip"] = 0
                        elif hasattr(target_tile, 'crop') and target_tile.crop and target_tile.crop.is_ripe:
                            target_tile.crop, target_tile.type = None, "grass"
                            player_inventory["turnip"] += 1  
                        elif current_map_name == "farm":
                            if player_inventory["current_tool"] == "hoe":
                                result = target_tile.dig(unlocked_tools, player_inventory)
                                if result == "iron_ore": player_inventory["iron_ore"] += 1
                            elif player_inventory["current_tool"] == "shovel": target_tile.dig_with_shovel(player_inventory)
                            elif player_inventory["current_tool"] == "water_can": target_tile.use_watering_can(player_inventory)

                    elif event.button == 3: 
                        try:
                            if target_tile.type == "npc_shop":
                                if player_inventory["gold"] >= 5: player_inventory["gold"] -= 5; player_inventory["seeds"] += 1
                            elif current_map_name == "farm" and hasattr(target_tile, 'plant'): target_tile.plant(player_inventory)
                        except: pass

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "MENU" if game_state == "PLAY" else "PLAY"
                    continue
                if game_state == "PLAY":
                    if event.key == pygame.K_SPACE: time_manager.trigger_next_day(world_maps, player_inventory)
                    elif event.key == pygame.K_e:
                        if player_inventory["bread"] > 0 and (player_inventory["energy"] < 100 or player_inventory["hp"] < 100):
                            player_inventory["bread"] -= 1
                            player_inventory["energy"] = min(100, player_inventory["energy"] + 30)
                            player_inventory["hp"] = min(100.0, player_inventory["hp"] + 30.0)
                    elif event.key == pygame.K_b and current_map_name == "interior_rest":
                        if player_inventory["gold"] >= 15: player_inventory["gold"] -= 15; player_inventory["bread"] += 1
                    
                    elif event.key == pygame.K_1: player_inventory["current_tool"] = "hoe"
                    elif event.key == pygame.K_2: player_inventory["current_tool"] = "shovel"
                    elif event.key == pygame.K_3: player_inventory["current_tool"] = "water_can"
                    elif event.key == pygame.K_4: player_inventory["current_tool"] = "move" 
                    
                    elif dungeon_state["near_crafting"]:
                        if event.key == pygame.K_F1 and player_inventory["turnip"] >= 2: player_inventory["turnip"] -= 2; player_inventory["bread"] += 1
                        elif event.key == pygame.K_F2 and player_inventory["gold"] >= 10 and player_inventory["iron_ore"] >= 1: player_inventory["gold"] -= 10; player_inventory["iron_ore"] -= 1; player_inventory["seeds"] += 1
                        elif event.key == pygame.K_F3 and not unlocked_tools["iron_pickaxe"] and player_inventory["gold"] >= 50 and player_inventory["iron_ore"] >= 5:
                            player_inventory["gold"] -= 50; player_inventory["iron_ore"] -= 5; unlocked_tools["iron_pickaxe"] = True

        # 纸娃娃捏脸场景渲染
        if game_state == "CUSTOMIZE":
            screen.fill((25, 25, 35)) 
            player.draw_model(screen, 350, 150, 100)
            pygame.draw.rect(screen, (255,215,0), (340, 135, 120, 130), 2) 
            
            title_s = font_large.render(L["cust_title"], True, (0, 255, 255))
            screen.blit(title_s, (SCREEN_WIDTH // 2 - title_s.get_width() // 2, 40))
            
            gender_txt = L["male"] if player.gender == "male" else L["female"]
            hair_txt = L[f"hair_{player.hair_style}"]
            
            screen.blit(font_menu.render(f"{L['cust_gender']}{gender_txt}", True, COLOR_TEXT), (260, 320))
            screen.blit(font.render(f"{L['cust_style']}{hair_txt}", True, COLOR_TEXT), (260, 360))
            screen.blit(font.render(f"{L['cust_color']}Color ID: #{player.hair_color_index}", True, COLOR_TEXT), (260, 400))
            
            enter_s = font_large.render(L["cust_enter"], True, (50, 255, 127))
            screen.blit(enter_s, (SCREEN_WIDTH // 2 - enter_s.get_width() // 2, 500))
            
            pygame.display.flip()
            continue 

        if game_state == "PLAY":
            keys = pygame.key.get_pressed()
            move_result = player.move(keys, current_map_name)
            if move_result == "GO_TO_VILLAGE": current_map_name = "village"
            elif move_result == "GO_TO_FARM": current_map_name = "farm"

        # 4. 渲染世界地图层（防残影高级缓冲区重构 ⭐）
        screen.fill(COLOR_BG)
        
        # 让起始点强行往左上挪 1 格，结束点强行往右下挪 2 格，完全盖过视野边缘物理断层
        start_tile_x = max(0, int(cam_x // TILE_SIZE) - 1)
        start_tile_y = max(0, int(cam_y // TILE_SIZE) - 1)
        end_tile_x = min(MAP_SIZE, start_tile_x + 15)
        end_tile_y = min(MAP_SIZE, start_tile_y + 18)

        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                tile = active_grid[y][x]
                if tile.type == "floor": color = COLOR_FLOOR
                elif tile.type == "dungeon": color = COLOR_DUNGEON
                elif tile.type == "bin": color = COLOR_BIN
                elif tile.type == "rock": color = COLOR_ROCK
                elif tile.type == "tilled": color = COLOR_TILLED        
                elif tile.type == "watered": color = COLOR_WATERED      
                elif tile.type == "pit": color = COLOR_PIT              
                elif tile.type == "water_pit": color = COLOR_WATER_PIT  
                elif tile.type == "portal": color = COLOR_PORTAL
                elif tile.type == "endless_portal": color = COLOR_ENDLESS_PORTAL
                elif tile.type == "stairs": color = COLOR_STAIRS
                elif tile.type == "chest": color = COLOR_CHEST
                elif tile.type in ["exit", "dungeon_exit"]: color = (0,0,0) 
                elif tile.type == "dungeon_to_endless": color = COLOR_ENDLESS_PORTAL
                elif tile.type in ["door_shop", "npc_shop"]: color = COLOR_DOOR_SHOP
                elif tile.type in ["door_hosp", "npc_hosp"]: color = COLOR_DOOR_HOSP
                elif tile.type in ["door_guild", "npc_guild"]: color = COLOR_DOOR_GUILD
                elif tile.type in ["door_rest", "npc_rest"]: color = COLOR_DOOR_REST
                elif tile.type in ["door_cloth", "npc_cloth"]: color = COLOR_DOOR_CLOTH
                elif tile.type == "crafting_table": color = COLOR_CRAFTING
                else: color = COLOR_GRASS 

                if hasattr(tile, 'crop') and tile.crop: color = COLOR_RIPE if tile.crop.is_ripe else COLOR_SEED
                rx, ry = x * TILE_SIZE - cam_x, y * TILE_SIZE - cam_y
                pygame.draw.rect(screen, color, (rx, ry, TILE_SIZE - 2, TILE_SIZE - 2))
                if tile.type == "crafting_table": pygame.draw.rect(screen, (255, 215, 0), (rx, ry, TILE_SIZE - 2, TILE_SIZE - 2), 2)

                if os.path.exists(win_font_path) and f"label_{tile.type}" in L and not tile.crop:
                    lbl_s = font_label.render(L[f"label_{tile.type}"], True, (255,255,255))
                    screen.blit(lbl_s, (rx + (TILE_SIZE - lbl_s.get_width()) // 2, ry + (TILE_SIZE - lbl_s.get_height()) // 2))

        if current_map_name == "dungeon":
            for monster in monsters: monster.draw(screen, cam_x, cam_y)
        player.draw(screen, cam_x, cam_y)

        # 小地图雷达绘制
        MINIMAP_GRID_SIZE, MINIMAP_X, MINIMAP_Y = 4, 15, 15
        pygame.draw.rect(screen, (20, 20, 20), (MINIMAP_X - 3, MINIMAP_Y - 3, MAP_SIZE * MINIMAP_GRID_SIZE + 6, MAP_SIZE * MINIMAP_GRID_SIZE + 6))
        pygame.draw.rect(screen, (255, 215, 0), (MINIMAP_X - 3, MINIMAP_Y - 3, MAP_SIZE * MINIMAP_GRID_SIZE + 6, MAP_SIZE * MINIMAP_GRID_SIZE + 6), 2)
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                t = active_grid[y][x]
                if t.type == "dungeon": mc = COLOR_DUNGEON
                elif t.type == "floor": mc = COLOR_FLOOR
                elif t.type in ["bin", "crafting_table", "water_pit"]: mc = (0, 191, 255)
                elif t.type == "rock": mc = COLOR_ROCK
                elif t.type.startswith("door_"): mc = (200,200,200)
                else: mc = (20, 100, 20)
                if hasattr(t, 'crop') and t.crop: mc = COLOR_RIPE if t.crop.is_ripe else COLOR_SEED
                pygame.draw.rect(screen, mc, (MINIMAP_X + x * MINIMAP_GRID_SIZE, MINIMAP_Y + y * MINIMAP_GRID_SIZE, MINIMAP_GRID_SIZE, MINIMAP_GRID_SIZE))
        
        if current_map_name == "dungeon":
            for monster in monsters:
                ms_x, ms_y = int((monster.x + 15) // TILE_SIZE), int((monster.y + 15) // TILE_SIZE)
                if 0 <= ms_x < MAP_SIZE and 0 <= ms_y < MAP_SIZE: pygame.draw.rect(screen, (255, 0, 0), (MINIMAP_X + ms_x * MINIMAP_GRID_SIZE, MINIMAP_Y + ms_y * MINIMAP_GRID_SIZE, MINIMAP_GRID_SIZE, MINIMAP_GRID_SIZE))
        p_grid_x, p_grid_y = int(player.get_center()[0] // TILE_SIZE), int(player.get_center()[1] // TILE_SIZE)
        if 0 <= p_grid_x < MAP_SIZE and 0 <= p_grid_y < MAP_SIZE: pygame.draw.circle(screen, (255, 20, 147), (MINIMAP_X + p_grid_x * MINIMAP_GRID_SIZE + 2, MINIMAP_Y + p_grid_y * MINIMAP_GRID_SIZE + 2), 3)

        # 右侧 UI 面板绘制
        ui_left_margin = 500
        pygame.draw.line(screen, (100,100,100), (480, 0), (480, 600), 2)
        pygame.draw.rect(screen, (30,30,30), (482, 0, 320, 600)) 

        if os.path.exists(win_font_path):
            screen.blit(font.render(f"{L['loc']}: {L.get(current_map_name, current_map_name.upper())}", True, (255,255,0)), (ui_left_margin, 15))
            if current_map_name == "dungeon":
                mode_label = L['endless'] if dungeon_state["is_endless_mode"] else L['story']
                screen.blit(font.render(f"{L['dungeon_info']}: B{dungeon_state['current_level']} ({mode_label})", True, (255,50,50)), (ui_left_margin, 40))
            else:
                screen.blit(font.render(time_manager.get_time_string(current_lang), True, COLOR_TEXT), (ui_left_margin, 40))
            
            screen.blit(font.render(f"{L['tool']}: {L.get(player_inventory['current_tool'], 'ERROR')}", True, (0,255,255)), (ui_left_margin, 65))
            held_display = L[f"label_{player_inventory['held_item']}"] if player_inventory["held_item"] else L["holding_none"]
            screen.blit(font.render(f"{L['holding']}: {held_display}", True, (255,105,180)), (ui_left_margin, 90))
            screen.blit(font.render(f"{L['lvl']}: LV.{player_inventory['level']} ({L['xp']}: {player_inventory['xp']})", True, (255,165,0)), (ui_left_margin, 115))
            
            screen.blit(font.render(f"{L['hp']}: {int(player_inventory['hp'])}", True, COLOR_HEALTH), (ui_left_margin, 140))
            pygame.draw.rect(screen, (100,100,100), (ui_left_margin + 90, 145, 100, 8))
            pygame.draw.rect(screen, COLOR_HEALTH, (ui_left_margin + 90, 145, int(100 * (player_inventory['hp']/100)), 8))
            screen.blit(font.render(f"{L['energy']}: {player_inventory['energy']}", True, COLOR_ENERGY), (ui_left_margin, 165))
            pygame.draw.rect(screen, (100,100,100), (ui_left_margin + 90, 170, 100, 8))
            pygame.draw.rect(screen, COLOR_ENERGY, (ui_left_margin + 90, 170, int(100 * (player_inventory['energy']/100)), 8))

            screen.blit(font.render(f"{L['gold']}: {player_inventory['gold']} G", True, COLOR_TEXT), (ui_left_margin, 195))
            screen.blit(font.render(f"{L['seeds']}: {player_inventory['seeds']}", True, COLOR_TEXT), (ui_left_margin, 220))
            screen.blit(font.render(f"{L['turnip']}: {player_inventory['turnip']}", True, COLOR_TEXT), (ui_left_margin, 245))
            screen.blit(font.render(f"{L['bread']}: {player_inventory['bread']}", True, COLOR_TEXT), (ui_left_margin, 270))
            screen.blit(font.render(f"{L['ore']}: {player_inventory['iron_ore']}", True, COLOR_TEXT), (ui_left_margin, 295))
            screen.blit(font.render(f"{L['bin']}: {player_inventory['shipping_bin']}", True, COLOR_TEXT), (ui_left_margin, 320))
            
            if dungeon_state["near_crafting"]:
                screen.blit(font.render(L["craft_title"], True, (255, 215, 0)), (ui_left_margin, 350))
                screen.blit(font.render(L["craft_1"], True, (100,255,100)), (ui_left_margin, 375))
                screen.blit(font.render(L["craft_2"], True, (100,255,100)), (ui_left_margin, 400))
                screen.blit(font.render(L["craft_3"] if not unlocked_tools["iron_pickaxe"] else "Pickaxe MAXED", True, (100,255,100)), (ui_left_margin, 425))
            else:
                screen.blit(font.render(L["guide_title"], True, (255, 215, 0)), (ui_left_margin, 350))
                screen.blit(font.render(L["guide_1"], True, (200,200,200)), (ui_left_margin, 375))
                screen.blit(font.render(L["guide_2"], True, (200,200,200)), (ui_left_margin, 400))
                screen.blit(font.render(L["guide_3"], True, (100,255,255)), (ui_left_margin, 425))

        # ESC 菜单面板
        if game_state == "MENU":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (30,30,30), (220, 150, 240, 250))
            pygame.draw.rect(screen, (255, 215, 0), (220, 150, 240, 250), 2) 
            title_s = font_menu.render(L["menu_title"], True, (255,215,0))
            screen.blit(title_s, (340 - title_s.get_width()//2, 170))
            
            pygame.draw.rect(screen, (60,60,60), (240, 210, 200, 40))
            pygame.draw.rect(screen, (200,200,200), (240, 210, 200, 40), 1)
            btn_a_s = font.render(L["menu_save"], True, COLOR_TEXT)
            screen.blit(btn_a_s, (340 - btn_a_s.get_width()//2, 222))
            
            pygame.draw.rect(screen, (60,60,60), (240, 270, 200, 40))
            pygame.draw.rect(screen, (200,200,200), (240, 270, 200, 40), 1)
            btn_b_s = font.render(f"{L['menu_lang']} ({current_lang.upper()})", True, COLOR_TEXT)
            screen.blit(btn_b_s, (340 - btn_b_s.get_width()//2, 282))
            
            pygame.draw.rect(screen, (80,40,40), (240, 330, 200, 40))
            pygame.draw.rect(screen, (255,100,100), (240, 330, 200, 40), 1)
            btn_c_s = font.render(L["menu_resume"], True, (255,200,200))
            screen.blit(btn_c_s, (340 - btn_c_s.get_width()//2, 342))

        pygame.display.flip()

if __name__ == "__main__":
    main()
