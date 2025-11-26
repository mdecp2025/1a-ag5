from robot_lib import World as BaseWorld, AnimatedRobot as BaseRobot, timer, CELL_SIZE

# --- 1. 定義世界（加入細格） ---
class MyWorld(BaseWorld):
    def __init__(self, width=10, height=10, sub_cell=5):
        super().__init__(width, height)
        self.sub_cell = sub_cell
        self.sub_size = CELL_SIZE // sub_cell
        self._draw_fine_grid()

    def _draw_fine_grid(self):
        ctx = self.layers["grid"].getContext("2d")
        ctx.strokeStyle = "#e0e0e0"
        ctx.lineWidth = 0.5
        # 畫垂直細線
        for i in range(self.width * self.sub_cell + 1):
            x = i * self.sub_size
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, self.height * CELL_SIZE); ctx.stroke()
        # 畫水平細線
        for j in range(self.height * self.sub_cell + 1):
            y = j * self.sub_size
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(self.width * CELL_SIZE, y); ctx.stroke()

    # 細格座標轉換為像素座標
    def sub_to_px(self, sub_x, sub_y):
        big_x = sub_x // self.sub_cell
        big_y = sub_y // self.sub_cell
        # 細格內的 X 偏移量
        offset_x = (sub_x % self.sub_cell) * self.sub_size
        
        # *** 此處 Y 軸細格內偏移的反轉是正確的 ***
        offset_y = (self.sub_cell - 1 - (sub_y % self.sub_cell)) * self.sub_size

        px = big_x * CELL_SIZE + offset_x + self.sub_size // 2
        py = (self.height - 1 - big_y) * CELL_SIZE + offset_y + self.sub_size // 2
        return px, py

    # 在細格座標上畫線 (保持不變)
    def draw_line(self, x1, y1, x2, y2):
        ctx = self.layers["objects"].getContext("2d")
        ctx.strokeStyle = "#d33"
        ctx.lineWidth = 9
        ctx.lineCap = "round"
        ctx.beginPath()
        ctx.moveTo(*self.sub_to_px(x1, y1))
        ctx.lineTo(*self.sub_to_px(x2, y2))
        ctx.stroke()

# --- 2. 定義機器人（以細格移動） --- (保持不變)
class MyRobot(BaseRobot):
    def __init__(self, world, start_big_x=1, start_big_y=1):
        super().__init__(world, start_big_x, start_big_y)
        # 初始位置轉換為細格中心
        self.sub_x = start_big_x * world.sub_cell + world.sub_cell // 2
        self.sub_y = start_big_y * world.sub_cell + world.sub_cell // 2
        self.robot_size = world.sub_size * 1.8

    # 重新繪製機器人（使用細格座標） (保持不變)
    def _draw_robot(self):
        self.robot_ctx.clearRect(0, 0, self.world.width * CELL_SIZE, self.world.height * CELL_SIZE)
        img = self.images[self.facing]
        px, py = self.world.sub_to_px(self.sub_x, self.sub_y)
        s = self.robot_size
        if img.complete:
            self.robot_ctx.drawImage(img, px - s//2, py - s//2, s, s)

    # 瞬間移動（不畫線） (保持不變)
    def teleport_to(self, tx, ty):
        def action(done):
            self.sub_x, self.sub_y = tx, ty
            self._draw_robot()
            timer.set_timeout(done, 10)
        self.queue.append(action)
        self._run_queue()

    # 移動 + 畫線（最核心）
    def move_to(self, tx, ty, draw_trace=True):
        def action(done):
            def step():
                if self.sub_x == tx and self.sub_y == ty:
                    done(); return
                prev_x, prev_y = self.sub_x, self.sub_y

                # 計算方向並轉向
                dx = tx - self.sub_x
                dy = ty - self.sub_y
                
                target = self.facing
                if abs(dx) > abs(dy):
                    target = "E" if dx > 0 else "W"
                elif abs(dy) > abs(dx):
                    # dy > 0 表示 sub_y 增大，這是我們定義的「向下」
                    target = "S" if dy > 0 else "N" 

                # 同步轉向（安全版）
                while self.facing != target:
                    idx = self.facing_order.index(self.facing)
                    self.facing = self.facing_order[(idx + 1) % 4]

                # 移動一步
                self.sub_x += 1 if dx > 0 else (-1 if dx < 0 else 0)
                self.sub_y += 1 if dy > 0 else (-1 if dy < 0 else 0)

                if draw_trace:
                    self.world.draw_line(prev_x, prev_y, self.sub_x, self.sub_y)
                self._draw_robot()
                # 調整速度，讓線條更平滑
                timer.set_timeout(step, 40)
            step()
        self.queue.append(action)
        self._run_queue()

# --- 3. 七段顯示器定義 --- (保持不變)
SEGMENTS = {
    0:[1,1,1,1,1,1,0], 1:[0,1,1,0,0,0,0], 2:[1,1,0,1,1,0,1],
    3:[1,1,1,1,0,0,1], 4:[0,1,1,0,0,1,1], 5:[1,0,1,1,0,1,1],
    6:[1,0,1,1,1,1,1], 7:[1,1,1,0,0,0,0], 8:[1,1,1,1,1,1,1],
    9:[1,1,1,1,0,1,1]
}

# 每個線段的細格座標路徑（相對座標）
# Y=0 為頂部，Y=6 為底部 
PATHS = [
    [(0,0),(1,0),(2,0),(3,0)],             # A 上
    [(3,0),(3,1),(3,2),(3,3)],             # B 右上
    [(3,3),(3,4),(3,5),(3,6)],             # C 右下
    [(3,6),(2,6),(1,6),(0,6)],             # D 下
    [(0,6),(0,5),(0,4),(0,3)],             # E 左下
    [(0,3),(0,2),(0,1),(0,0)],             # F 左上
    [(0,3),(1,3),(2,3),(3,3)]              # G 中
]

def draw_digit(robot, digit, ox, oy):
    # 七段顯示器的 Y 座標範圍是 0 到 6
    DIGIT_HEIGHT = 6 
    
    if digit not in SEGMENTS: return
    for i, on in enumerate(SEGMENTS[digit]):
        if not on: continue
        path = PATHS[i]
        
        # *** 關鍵修正：整體 Y 軸方向反轉 ***
        # 由於數字仍然上下顛倒，我們對 PATHS 提供的 Y 座標進行反轉：
        # Y_new = oy + (DIGIT_HEIGHT - Y_original)
        
        # 起點
        original_start_y = path[0][1]
        start_x = ox + path[0][0]
        # 反轉 Y 座標：Y=0 (頂部) 變成 oy+6，Y=6 (底部) 變成 oy+0
        start_y = oy + (DIGIT_HEIGHT - original_start_y) 
        
        robot.teleport_to(start_x, start_y)
        
        for j in range(1, len(path)):
            original_ty = path[j][1]
            tx = ox + path[j][0]
            # 反轉 Y 座標
            ty = oy + (DIGIT_HEIGHT - original_ty)
            robot.move_to(tx, ty, draw_trace=True)

# ==================== 主程式：畫 0123456789 ====================
world = MyWorld(65, 10, sub_cell=5) 
robot = MyRobot(world, 0, 0) 

# Y 軸偏移量 oy：
# 由於我們已經在 draw_digit 內反轉了 Y 軸， oy=1 會讓數字頂部 (原 Y=6) 位於世界 Y=1 的位置。
START_Y_SUB_CELL = 30

for i in range(10):
    start_x_offset = 1 + i * 6 
    draw_digit(robot, i, start_x_offset, START_Y_SUB_CELL)

print("機器人正在寫字：0123456789 (已修正 draw_digit 中的整體 Y 軸方向)")