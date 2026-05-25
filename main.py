import pygame
import sys
import math

# 1. 基础配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40  # 每个网格 40x40 像素
MAP_SIZE = 12   # 12x12 的地图

# 颜色定义 (RGB)
COLOR_GRASS = (34, 139, 34)      # 草地-绿色
COLOR_TILLED = (139, 69, 19)     # 耕地-棕色
COLOR_ROCK = (128, 128, 128)     # 铁矿石-灰色
COLOR_SEED = (144, 238, 144)     # 种子-淡绿色
COLOR_RIPE = (255, 215, 0)       # 成熟作物-金色
COLOR_BIN = (30, 144, 255)       # 【新】出货箱-道奇蓝
COLOR_NPC = (148, 0, 211)        # 【新】商店NPC-深紫色
COLOR_BG = (50, 50, 50)          # 背景暗灰
COLOR_PLAYER = (255, 105, 180)   # 玩家小方块-粉色
COLOR_TEXT = (255, 255, 255)     # 文字-白色

# 2. 核心类设计
class Crop:
    def __init__(self):
        self.growth_time = 3  
        self.current_age = 0
        self.is_ripe = False

    def grow(self):
        if not self.is_ripe:
            self.current_age += 1
            if self.current_age >= self.growth_time:
                self.is_ripe = True

class Tile:
    def __init__(self, tile_type="grass"):
        self.type = tile_type  # grass, tilled, rock, bin, npc
        self.crop = None       

    def dig(self, unlocked_tools):
        if self.type == "grass":
            self.type = "tilled"
            return "dig_ground"
        elif self.type == "rock":
            if unlocked_tools["iron_pickaxe"]:
                self.type = "grass"
                return "iron_ore"
            else:
                print("⛏️ This rock is too hard! Press 'U' to upgrade your pickaxe first.")
        return None

    def plant(self, player_inventory):
        """修改：播种时需要消耗背包里的种子"""
        if self.type == "tilled" and self.crop is None:
            if player_inventory["seeds"] > 0:
                player_inventory["seeds"] -= 1
                self.crop = Crop()
                print(f"🌱 Planted a Turnip seed! Seeds left: {player_inventory['seeds']}")
            else:
                print("❌ No seeds left! Go buy some from the NPC (Purple tile).")

class Player:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.speed = 4
        self.size = 30  

    def get_center(self):
        return self.x + self.size // 2, self.y + self.size // 2

    def move(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_PLAYER, (self.x, self.y, self.size, self.size))

class TimeManager:
    def __init__(self):
        self.day = 1
        self.hour = 6
        self.minute = 30
        self.timer = 0.0

    def update(self, dt, game_map, player_inventory):
        self.timer += (dt / 1000.0) * 1.75
        if self.timer >= 1.0:
            self.minute += int(self.timer)
            self.timer -= int(self.timer)
            if self.minute >= 60:
                self.hour += self.minute // 60
                self.minute = self.minute % 60
            if self.hour >= 24:
                self.trigger_next_day(game_map, player_inventory)

    def trigger_next_day(self, game_map, player_inventory):
        """进入下一天，并结算出货箱金额"""
        self.day += 1
        self.hour = 6
        self.minute = 30
        self.timer = 0.0
        
        # 1. 结算出货箱（100% 价格：每个 20 金币）
        if player_inventory["shipping_bin"] > 0:
            earnings = player_inventory["shipping_bin"] * 20
            player_inventory["gold"] += earnings
            print(f"📦 Overnight Shipping Bin Income: +{earnings} Gold for {player_inventory['shipping_bin']} Turnips!")
            player_inventory["shipping_bin"] = 0 # 清空出货箱
        
        # 2. 作物生长
        for row in game_map:
            for tile in row:
                if tile.crop:
                    tile.crop.grow()
        print(f"☀️ Good morning! Day {self.day} started.")

    def get_time_string(self):
        return f"Day {self.day}  {self.hour:02d}:{self.minute:02d}"

# 3. 游戏主程序
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyFarm - Economy System v0.5")
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 24) 

    player = Player()
    time_manager = TimeManager()
    
    # 增加：种子数量、出货箱暂存数量
    player_inventory = {"gold": 100, "iron_ore": 0, "turnip": 0, "seeds": 3, "shipping_bin": 0} 
    unlocked_tools = {"iron_pickaxe": False}

    # 初始化 12x12 地图
    game_map = [[Tile("grass") for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    
    # 放置固定设施
    game_map[0][0].type = "bin"  # 左上角放置【出货箱】(蓝色)
    game_map[0][2].type = "npc"  # 旁边放置【商店NPC】(紫色)
    
    # 放置矿石
    game_map[2][3].type = "rock"
    game_map[5][6].type = "rock"
    game_map[8][2].type = "rock"

    print("Game Started with Economy System!")
    print("Blue tile = Shipping Bin (100% value next day) | Purple tile = NPC Shop (60% value instant)")

    while True:
        dt = clock.tick(60) 
        time_manager.update(dt, game_map, player_inventory)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                tile_x = mouse_x // TILE_SIZE
                tile_y = mouse_y // TILE_SIZE

                if 0 <= tile_x < MAP_SIZE and 0 <= tile_y < MAP_SIZE:
                    
                    # 距离检测（最大 70 像素限制）
                    tile_center_x = tile_x * TILE_SIZE + TILE_SIZE // 2
                    tile_center_y = tile_y * TILE_SIZE + TILE_SIZE // 2
                    player_center_x, player_center_y = player.get_center()
                    distance = math.hypot(tile_center_x - player_center_x, tile_center_y - player_center_y)
                    
                    if distance > 70:
                        print("❌ Too far away!")
                        continue  

                    target_tile = game_map[tile_y][tile_x]

                    # ─── 鼠标左键点击 ───
                    if event.button == 1:
                        # 情况 A: 点击了出货箱 (蓝色)
                        if target_tile.type == "bin":
                            if player_inventory["turnip"] > 0:
                                count = player_inventory["turnip"]
                                player_inventory["shipping_bin"] += count
                                player_inventory["turnip"] = 0
                                print(f"📦 Deposited {count} Turnips into the shipping bin. Will sell tonight!")
                            else:
                                print("📦 Shipping bin is empty. Collect harvested turnips first.")
                        
                        # 情况 B: 点击了商店 NPC (紫色) -> 卖出背包的所有物品 (获得 60% 价格 = 12 Gold/个)
                        elif target_tile.type == "npc":
                            if player_inventory["turnip"] > 0:
                                count = player_inventory["turnip"]
                                money_gained = count * 12  # 20 * 0.6 = 12
                                player_inventory["gold"] += money_gained
                                player_inventory["turnip"] = 0
                                print(f"💰 Sold {count} Turnips to NPC instantly! Gained {money_gained} Gold.")
                            else:
                                print("🧙‍♂️ NPC: You don't have any Turnips to sell me!")

                        # 情况 C: 点击了成熟作物 -> 收割
                        elif target_tile.crop and target_tile.crop.is_ripe:
                            target_tile.crop = None
                            target_tile.type = "grass"
                            player_inventory["turnip"] += 1  
                            print(f"🧺 Harvested a Turnip! Total: {player_inventory['turnip']}")
                        
                        # 情况 D: 普通锄地或采矿
                        else:
                            result = target_tile.dig(unlocked_tools)
                            if result == "iron_ore":
                                player_inventory["iron_ore"] += 1

                    # ─── 鼠标右键点击 ───
                    elif event.button == 3:
                        # 如果右键点击 NPC (紫色) -> 购买种子 (消耗 5金币，获得 1种子)
                        if target_tile.type == "npc":
                            if player_inventory["gold"] >= 5:
                                player_inventory["gold"] -= 5
                                player_inventory["seeds"] += 1
                                print(f"🛒 Bought 1 Seed! Gained 1 Turnip seed (Total: {player_inventory['seeds']})")
                            else:
                                print("❌ NPC: You don't have enough gold! (Needs 5 Gold)")
                        else:
                            # 正常的播种
                            target_tile.plant(player_inventory)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time_manager.trigger_next_day(game_map, player_inventory)
                elif event.key == pygame.K_u: 
                    if not unlocked_tools["iron_pickaxe"]:
                        if player_inventory["gold"] >= 50:
                            player_inventory["gold"] -= 50
                            unlocked_tools["iron_pickaxe"] = True
                            print("🎉 Unlocked Iron Pickaxe!")
                        else:
                            print("❌ Need 50 Gold!")

        keys = pygame.key.get_pressed()
        player.move(keys)

        # 4. 渲染画面
        screen.fill(COLOR_BG)

        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile = game_map[y][x]
                if tile.type == "grass": color = COLOR_GRASS
                elif tile.type == "tilled": color = COLOR_TILLED
                elif tile.type == "rock": color = COLOR_ROCK
                elif tile.type == "bin": color = COLOR_BIN
                elif tile.type == "npc": color = COLOR_NPC

                if tile.crop:
                    color = COLOR_RIPE if tile.crop.is_ripe else COLOR_SEED

                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))

        player.draw(screen)

        # 5. UI 面板渲染
        ui_left_margin = MAP_SIZE * TILE_SIZE + 20
        time_text = font.render(time_manager.get_time_string(), True, COLOR_TEXT)
        screen.blit(time_text, (ui_left_margin, 20))
        
        gold_text = font.render(f"Gold: {player_inventory['gold']}", True, COLOR_TEXT)
        seed_text = font.render(f"Seeds: {player_inventory['seeds']}", True, COLOR_TEXT)
        turnip_text = font.render(f"Turnip (Inv): {player_inventory['turnip']}", True, COLOR_TEXT)
        bin_text = font.render(f"In Bin: {player_inventory['shipping_bin']}", True, COLOR_TEXT)
        ore_text = font.render(f"Iron Ore: {player_inventory['iron_ore']}", True, COLOR_TEXT)
        
        screen.blit(gold_text, (ui_left_margin, 60))
        screen.blit(seed_text, (ui_left_margin, 90))
        screen.blit(turnip_text, (ui_left_margin, 120))
        screen.blit(bin_text, (ui_left_margin, 150))
        screen.blit(ore_text, (ui_left_margin, 180))
        
        # 键位与玩法说明
        tip_title = font.render("--- HOW TO PLAY ---", True, (255, 215, 0))
        tip_move = font.render("[W/A/S/D] : Move Around", True, (200, 200, 200))
        tip_bin = font.render("[Left Click Blue] : Put into Bin", True, (200, 200, 200))
        tip_npc_buy = font.render("[Right Click Purple] : Buy Seed (5G)", True, (200, 200, 200))
        tip_npc_sell = font.render("[Left Click Purple] : Quick Sell (12G)", True, (200, 200, 200))
        tip_sleep = font.render("[SPACE] : Go to Sleep", True, (200, 200, 200))
        
        screen.blit(tip_title, (ui_left_margin, 240))
        screen.blit(tip_move, (ui_left_margin, 270))
        screen.blit(tip_bin, (ui_left_margin, 300))
        screen.blit(tip_npc_buy, (ui_left_margin, 330))
        screen.blit(tip_npc_sell, (ui_left_margin, 360))
        screen.blit(tip_sleep, (ui_left_margin, 390))

        pygame.display.flip()

if __name__ == "__main__":
    main()
