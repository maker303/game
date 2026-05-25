import pygame
import sys

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
COLOR_BG = (50, 50, 50)          # 背景暗灰
COLOR_PLAYER = (255, 105, 180)   # 玩家小方块-粉色
COLOR_TEXT = (255, 255, 255)     # 文字-白色

# 2. 核心类设计
class Crop:
    def __init__(self):
        self.growth_time = 3  # 3天成熟
        self.current_age = 0
        self.is_ripe = False

    def grow(self):
        if not self.is_ripe:
            self.current_age += 1
            if self.current_age >= self.growth_time:
                self.is_ripe = True

class Tile:
    def __init__(self, tile_type="grass"):
        self.type = tile_type  
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
                print("⛏️ 这个矿石太硬了！升级铁矿镐(按U)再来吧。")
        return None

    def plant(self):
        if self.type == "tilled" and self.crop is None:
            self.crop = Crop()
            print("🌱 种下了芜菁种子！")

class Player:
    def __init__(self):
        # 初始位置（像素坐标）
        self.x = 200
        self.y = 200
        self.speed = 4
        self.size = 30  # 比格子略小，看起来更舒服

    def move(self, keys):
        """根据按键移动角色，并限制在屏幕内"""
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed

        # 边界碰撞限制
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
        self.is_night_ended = False

    def update(self, dt, game_map):
        """根据帧率时间差(dt)更新游戏时间"""
        if self.is_night_ended:
            return

        # 现实1秒钟 = 游戏内1.75分钟
        # dt 是毫秒，所以除以 1000 换算成秒
        self.timer += (dt / 1000.0) * 1.75
        
        if self.timer >= 1.0:
            self.minute += int(self.timer)
            self.timer -= int(self.timer)

            if self.minute >= 60:
                self.hour += self.minute // 60
                self.minute = self.minute % 60

            # 到了晚上 12:00 (24:00)，强制熬夜昏倒/睡觉
            if self.hour >= 24:
                self.hour = 24
                self.minute = 0
                self.trigger_next_day(game_map)

    def trigger_next_day(self, game_map):
        """进入下一天"""
        self.day += 1
        self.hour = 6
        self.minute = 30
        self.timer = 0.0
        # 让所有作物生长
        for row in game_map:
            for tile in row:
                if tile.crop:
                    tile.crop.grow()
        print(f"\n☀️ 新的一天！第 {self.day} 天开始。")

    def get_time_string(self):
        return f"Day {self.day}  {self.hour:02d}:{self.minute:02d}"

# 3. 游戏主程序
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyFarm - Character & Time System")
    clock = pygame.time.Clock()
    
    # 初始化字体
    font = pygame.font.SysFont("SimHei", 20) # 尽量使用支持中文的系统字体，若无则显示英文

    # 游戏数据
    player = Player()
    time_manager = TimeManager()
    player_inventory = {"gold": 100, "iron_ore": 0, "turnip": 0} # 砍掉了自动售出，变成存入 turnip
    unlocked_tools = {"iron_pickaxe": False}

    # 初始化地图
    game_map = [[Tile("grass") for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    game_map[2][3].type = "rock"
    game_map[5][6].type = "rock"

    # 主循环
    while True:
        # 计算两帧之间的时间差（毫秒）
        dt = clock.tick(60) 

        # 处理时间流逝
        time_manager.update(dt, game_map)

        # 输入事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 鼠标点击（基于鼠标在网格的位置）
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                tile_x = mouse_x // TILE_SIZE
                tile_y = mouse_y // TILE_SIZE

                if 0 <= tile_x < MAP_SIZE and 0 <= tile_y < MAP_SIZE:
                    target_tile = game_map[tile_y][tile_x]

                    # 左键：收割（入背包）/ 锄地 / 采矿
                    if event.button == 1:
                        if target_tile.crop and target_tile.crop.is_ripe:
                            target_tile.crop = None
                            target_tile.type = "grass"
                            player_inventory["turnip"] += 1  # 变为直接收入背包！
                            print(f"🧺 成功收割芜菁！当前背包拥有: {player_inventory['turnip']} 个。")
                        else:
                            result = target_tile.dig(unlocked_tools)
                            if result == "iron_ore":
                                player_inventory["iron_ore"] += 1

                    # 右键：播种
                    elif event.button == 3:
                        target_tile.plant()

            # 键盘单次按下事件
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u: # 解锁铁矿镐
                    if not unlocked_tools["iron_pickaxe"] and player_inventory["gold"] >= 50:
                        player_inventory["gold"] -= 50
                        unlocked_tools["iron_pickaxe"] = True
                        print("🎉 解锁铁矿镐！")

        # 实时键盘长按处理（控制角色移动）
        keys = pygame.key.get_pressed()
        player.move(keys)

        # 4. 画面渲染
        screen.fill(COLOR_BG)

        # 绘制网格地图
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile = game_map[y][x]
                if tile.type == "grass": color = COLOR_GRASS
                elif tile.type == "tilled": color = COLOR_TILLED
                elif tile.type == "rock": color = COLOR_ROCK

                if tile.crop:
                    color = COLOR_RIPE if tile.crop.is_ripe else COLOR_SEED

                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))

        # 绘制玩家
        player.draw(screen)

        # 绘制右侧 UI 栏（背景和文字信息）
        ui_left_margin = MAP_SIZE * TILE_SIZE + 20
        
        # 显示时间
        time_text = font.render(time_manager.get_time_string(), True, COLOR_TEXT)
        screen.blit(time_text, (ui_left_margin, 20))
        
        # 显示背包状态
        gold_text = font.render(f"Gold: {player_inventory['gold']}", True, COLOR_TEXT)
        ore_text = font.render(f"Iron Ore: {player_inventory['iron_ore']}", True, COLOR_TEXT)
        turnip_text = font.render(f"Turnip (Inventory): {player_inventory['turnip']}", True, COLOR_TEXT)
        
        screen.blit(gold_text, (ui_left_margin, 60))
        screen.blit(ore_text, (ui_left_margin, 90))
        screen.blit(turnip_text, (ui_left_margin, 120))
        
        # 补充操作提示
        tip_text = font.render("[W/A/S/D]: Move", True, (200,200,200))
        screen.blit(tip_text, (ui_left_margin, 200))

        pygame.display.flip()

if __name__ == "__main__":
    main()