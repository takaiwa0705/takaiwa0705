from tkinter import *
from random import randint
import math
from time import sleep , time 
from math import sqrt

HEGHT = 600
WIDTH = 520
window = Tk()
window.title("STG")
BUB_CHANCE = 75

c = Canvas(window, width=WIDTH, height=HEGHT, bg="darkblue")
c.pack()
ship_id = c.create_oval(0, 0, 6, 6, fill="red")
SHIP_R = 3
MID_X = WIDTH / 2
MID_Y = HEGHT / 1.1
c.move(ship_id, MID_X, MID_Y)
SHIP_SPD = 6
LOW_SPEED = 2  # 低速移動時の速度

# 押されているキーを追跡する辞書
keys_pressed = set()

# キーが押されたときに呼び出される関数
def key_press(event):
    keys_pressed.add(event.keysym)

# キーが離されたときに呼び出される関数
def key_release(event):
    keys_pressed.discard(event.keysym)

# 移動処理を更新する関数
def move_ship():
    dx, dy = 0, 0
    current_speed = LOW_SPEED if "Shift_L" in keys_pressed or "Shift_R" in keys_pressed else SHIP_SPD

    if "Up" in keys_pressed:
        dy -= current_speed
    if "Down" in keys_pressed:
        dy += current_speed
    if "Left" in keys_pressed:
        dx -= current_speed
    if "Right" in keys_pressed:
        dx += current_speed

    # 斜め移動時の速度を調整
    if dx != 0 and dy != 0:
        norm = math.sqrt(dx**2 + dy**2)  # ベクトルの長さを計算
        dx = (dx / norm) * current_speed
        dy = (dy / norm) * current_speed

    # 現在の座標を取得
    x1, y1, x2, y2 = c.coords(ship_id)

    # 移動後の座標を計算
    new_x1 = x1 + dx
    new_y1 = y1 + dy
    new_x2 = x2 + dx
    new_y2 = y2 + dy

    # 画面端の制限
    if new_x1 < 10:  # 左端
        dx = 10 -x1
    if new_y1 < 10:  # 上端
        dy = 10 -y1
    if new_x2 > WIDTH - 10:  # 右端
        dx = WIDTH - 10 - x2
    if new_y2 > HEGHT - 10:  # 下端
        dy = HEGHT - 10 - y2
    
    c.move(ship_id, dx, dy)
    window.after(20, move_ship)  # 20ミリ秒ごとに更新

# 無敵状態を管理するフラグ
is_invincible = False

def set_invincible(duration):
    global is_invincible
    if is_invincible:
        return  # 既に無敵状態の場合は何もしない
    is_invincible = True
    window.after(duration, disable_invincible)  # 指定時間後に無敵状態を解除
    print("無敵状態が設定されました")  # デバッグ用メッセージ

def disable_invincible():
    global is_invincible
    is_invincible = False
    print("無敵状態が解除されました")  # デバッグ用メッセージ

def reset_ship_position():
    c.coords(ship_id, MID_X - SHIP_R, MID_Y - SHIP_R, MID_X + SHIP_R, MID_Y + SHIP_R)

MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 15
GAP = 100

# 敵弾（右から左）のリスト
bub_id_left = []
bub_r_left = []
bub_speed_left = []

# 敵弾（上から下）のリスト
bub_id_down = []
bub_r_down = []
bub_speed_down = []

# 敵弾（円形）のリスト
bub_id_circle = []
bub_r_circle = []
bub_speed_circle = []
bub_angle_circle = []
bub_current_speed_circle = []

# 自機狙いの敵弾のリスト
bub_id_targeted = []
bub_r_targeted = []
bub_speed_targeted = []
bub_dx_targeted = []
bub_dy_targeted = []

# 円を描く敵弾のリスト
bub_id_orbit = []
bub_r_orbit = []
bub_center_orbit = []
bub_angle_orbit = []
bub_radius_orbit = []
bub_speed_orbit = []

# 敵弾（円が広がる）のリスト
bub_id_expanding_orbit = []
bub_r_expanding_orbit = []
bub_center_expanding_orbit = []
bub_angle_expanding_orbit = []
bub_radius_expanding_orbit = []
bub_speed_expanding_orbit = []

# 敵弾（円が逆回転で広がる）のリスト
bub_id_expanding_orbit_2 = []
bub_r_expanding_orbit_2 = []
bub_center_expanding_orbit_2 = []
bub_angle_expanding_orbit_2 = []
bub_radius_expanding_orbit_2 = []
bub_speed_expanding_orbit_2 = []

# ショットガンの敵弾のリスト
bub_id_shotgun = []
bub_dx_shotgun = []
bub_dy_shotgun = []
bub_r_shotgun = []
bub_speed_shotgun = [] 

# 敵弾（螺旋）のリスト
bub_id_spiral = []
bub_r_spiral = []
bub_speed_spiral = []
bub_angle_spiral = []

# レーザー弾のリスト
laser_id = []
laser_active = []

# 自機の敵弾のリスト
player_bullets = []
player_bullet_speed = 20  # 自機の弾の速度

# 敵のリスト
enemies = []
enemy_health = []  # 各敵の体力を管理
enemy_targets = []  # 各敵の移動先を管理

# 敵の状態を管理するリスト
enemy_states = []  # 各敵の状態を管理（例: "normal", "moving_up")

def create_enemy(x=None, y=None, target_x=None, target_y=None, health=3):
    # 初期位置を指定（デフォルトはランダム）
    if x is None:
        x = randint(50, WIDTH - 50)
    if y is None:
        y = -50  # 画面外上部
    
    # 移動先を指定（デフォルトは画面中央付近）
    if target_x is None:
        target_x = randint(50, WIDTH - 50)
    if target_y is None:
        target_y = HEGHT // 2
    
    r = 30  # 敵の半径
    
    # 敵を生成
    enemy_id = c.create_oval(x - r, y - r, x + r, y + r, fill="green", outline="white")
    enemies.append(enemy_id)
    enemy_health.append(health)
    enemy_targets.append((target_x, target_y))  # 移動先を保存
    enemy_states.append("normal")  # 初期状態を「normal」に設定

# 敵の状態を変更する関数
def set_enemy_to_move_up(index):
    if index < len(enemy_states):
        enemy_states[index] = "moving_up"  # 状態を「上に移動する」に変更

def move_enemies():
    for i in range(len(enemies) - 1, -1, -1):
        x1, y1, x2, y2 = c.coords(enemies[i])
        enemy_x = (x1 + x2) / 2
        enemy_y = (y1 + y2) / 2

        if enemy_states[i] == "normal":
            # 移動先を取得
            target_x, target_y = enemy_targets[i]

            # 移動方向を計算
            dx = target_x - enemy_x
            dy = target_y - enemy_y
            distance = math.sqrt(dx**2 + dy**2)

            # 移動速度を設定
            speed = 3
            if distance > 0:
                dx = (dx / distance) * speed
                dy = (dy / distance) * speed

            # 敵を移動
            c.move(enemies[i], dx, dy)

            # 移動先に到達したら停止
            if distance < speed:
                enemy_targets[i] = (enemy_x, enemy_y)  # 到達後はその場に留まる
                create_bub_circle(enemy_x, enemy_y, 1, 8, 5, 8, 120, 0)
                window.after(1500, set_enemy_to_move_up, i)  # 3秒後に上に移動する状態に変更

        elif enemy_states[i] == "moving_up":
                # 上方向に移動
                c.move(enemies[i], 0, -2)  # 上方向に移動
                # 画面外に出たら削除
                if enemy_y < -50:
                    c.delete(enemies[i])
                    del enemies[i]
                    del enemy_health[i]
                    del enemy_targets[i]
                    del enemy_states[i]

    # 50ミリ秒ごとに再実行
    window.after(50, move_enemies)

def check_enemy_collision():
    for i in range(len(enemies) - 1, -1, -1):
        for bullet in player_bullets[:]:
            if distance(enemies[i], bullet) < 30:  # 衝突判定（敵の半径と弾の位置）
                # 敵の体力を減らす
                enemy_health[i] -= 1

                # 弾を削除
                c.delete(bullet)
                player_bullets.remove(bullet)

                # 体力が0になったら敵を削除
                if enemy_health[i] <= 0:
                    c.delete(enemies[i])
                    del enemies[i]
                    del enemy_health[i]
                    del enemy_targets[i]
                    del enemy_states[i]
                    break

    # 50ミリ秒ごとに再実行
    window.after(50, check_enemy_collision)

def fire_enemy_bullets(bullet_type):
    for i in range(len(enemies)):
        # 敵の体力を確認
        if enemy_health[i] <= 0:
            continue  # 体力が0以下の敵はスキップ

        # 敵の移動先（enemy_targets）を基準に弾を発射
        target_x, target_y = enemy_targets[i]
        print(int(target_x), int(target_y))

        if bullet_type == 1:  # 円形の敵弾
            create_bub_circle(target_x, target_y, 1, 8, 5, 8, 120, 0)
        elif bullet_type == 2:  # 自機狙いの敵弾
            create_bub_targeted(target_x, target_y, 1, 8, 5, 0)
        elif bullet_type == 3:  # ショットガンの敵弾
            create_shotgun_bullets(target_x, target_y, 1, 8, 5, 5, 120, 0)

def enemy_fire_loop():
    fire_enemy_bullets(2)  # 敵弾を発射
    window.after(2000, enemy_fire_loop)  # 2秒ごとに再実行

#生成回数を管理するカウンター
circle_count = 0
targeted_count = 0
orbit_count = 0
expanding_orbit_count = 0
expanding_orbit_2_count = 0
shotgun_count = 0
spiral_count  = 0
laser_count = 0

# 弾を発射中かどうかを管理するフラグ
is_firing = False

# 自機の敵弾を発射する関数
def fire_player_bullet():
    # 自機の現在位置を取得
    ship_x, ship_y = get_coords(ship_id)

    # 弾を生成
    bullet_id = c.create_oval(ship_x - 3, ship_y - 10, ship_x + 3, ship_y - 5, fill="white")
    player_bullets.append(bullet_id)

# 弾を発射し続ける関数
def continuous_fire():
    if is_firing:  # `Z`キーが押されている場合のみ発射
        fire_player_bullet()
        window.after(100, continuous_fire)  # 100ミリ秒ごとに弾を発射

# 自機の敵弾を移動させる関数
def move_player_bullets():
    for bullet in player_bullets[:]:
        # 弾を上方向に移動
        c.move(bullet, 0, -player_bullet_speed)

        # 弾の現在位置を取得
        x1, y1, x2, y2 = c.coords(bullet)

        # 画面外に出たら削除
        if y2 < 0:
            c.delete(bullet)
            player_bullets.remove(bullet)

    # 50ミリ秒ごとに再実行
    window.after(10, move_player_bullets)

# キーが押されたときに呼び出される関数
def key_press(event):
    global is_firing
    keys_pressed.add(event.keysym)
    if event.keysym == "z" or event.keysym == "Z":  # Zキーが押された場合
        if not is_firing:  # 既に発射中でなければ発射を開始
            is_firing = True
            continuous_fire()


# キーが離されたときに呼び出される関数
def key_release(event):
    global is_firing
    keys_pressed.discard(event.keysym)
    if event.keysym == "z" or event.keysym == "Z":  # Zキーが離された場合
        is_firing = False

# 敵弾（右から左）を生成する関数
def create_bub_left():
    if randint(1, GAP) <= BUB_CHANCE:  # 一定確率で敵弾を生成
        x = WIDTH + GAP
        y = randint(0, HEGHT)
        r = randint(MIN_BUB_R, MAX_BUB_R)
        id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
        bub_id_left.append(id1)
        bub_r_left.append(r)
        bub_speed_left.append(randint(1, MAX_BUB_SPD))
    window.after(100, create_bub_left)  # 100ミリ秒ごとに再実行

# 敵弾（上から下）を生成する関数
def create_bub_down():
    if randint(1, GAP) <= BUB_CHANCE:  # 一定確率で敵弾を生成
        x = randint(0, WIDTH)
        y = -GAP
        r = randint(MIN_BUB_R, MAX_BUB_R)
        id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
        bub_id_down.append(id1)
        bub_r_down.append(r)
        bub_speed_down.append(randint(1, MAX_BUB_SPD))
    window.after(100, create_bub_down)  # 100ミリ秒ごとに再実行

# 円形の敵弾を生成する関数
def create_bub_circle(x, y, circle_limit, r, speed, num_bullets, spread_angle, rest):
        global circle_count
        if circle_count >= circle_limit:
            return  # 生成回数が上限に達したら停止
        
        center_x = x  # 円の中心を画面の中央に設定
        center_y = y
        angle_step = spread_angle / (num_bullets - 1)  # 各弾の間隔の角度

        # 自機の位置を取得
        ship_x, ship_y = get_coords(ship_id)

        # 自機への基準角度を計算
        base_angle = math.degrees(math.atan2(ship_y - center_y, ship_x - center_x))# 自機の位置を取得

        for i in range(num_bullets):
            # 各弾の角度を計算（広がる角度を考慮）
            angle = base_angle - (spread_angle / 2) + (i * angle_step)
            angle_rad = math.radians(angle)

            # 弾の初期位置を計算
            x = center_x + r * math.cos(angle_rad)
            y = center_y + r * math.sin(angle_rad)
            id1 = c.create_oval(center_x - r, center_y - r, center_x + r, center_y + r, outline="white", fill="yellow")
            bub_id_circle.append(id1)
            bub_r_circle.append(r)
            bub_speed_circle.append(speed)  # 弾の速度
            bub_angle_circle.append(angle)  # 各弾の角度を保存
            bub_current_speed_circle.append(speed * 2)

        circle_count += 1  # カウンターを増加
        window.after(int(rest*1000), lambda: create_bub_circle(center_x, center_y, circle_limit, r, speed, num_bullets, spread_angle, rest))  # 1秒ごとに再実行

# 自機狙いの敵弾を生成する関数
def create_bub_targeted(x, y, tergeted_limit, r, speed, rest):
    global targeted_count
    if targeted_count >= tergeted_limit:
        return
    
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline="red", fill="orange")
    bub_id_targeted.append(id1)
    bub_r_targeted.append(r)
    bub_speed_targeted.append(speed)

    # 自機の位置を取得
    ship_x, ship_y = get_coords(ship_id)

    # 敵弾の初期位置を取得
    bub_x, bub_y = get_coords(id1)

    # 初期速度の設定
    initial_speed = speed * 2  # 初期速度は設定速度の4倍

    # 自機への移動方向を計算
    dx = ship_x - bub_x    
    dy = ship_y - bub_y
    norm = math.sqrt(dx**2 + dy**2)
    bub_dx_targeted.append((dx / norm) * initial_speed)
    bub_dy_targeted.append((dy / norm) * initial_speed)
    targeted_count += 1  # カウンターを増加
    window.after(int(rest*1000), lambda: create_bub_targeted(x, y, tergeted_limit, r, speed, rest))

# 円を描く敵弾を生成する関数
def create_bub_orbit(center_x, center_y, orbit_limit, r, speed, num_bullets, rest):
    global orbit_count
    if orbit_count >= orbit_limit:
        return

    radius = randint(75, 100)  # 円の半径
    angle = randint(0, 360)  # 初期角度
    angle_step = 360 / num_bullets  # 各弾の間隔の角度

    for i in range(num_bullets):
        angle = i * angle_step  # 各弾の初期角度
        # 弾の初期位置を計算
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        id1 = c.create_oval(x - r, y - r, x + r, y + r, outline="green", fill="lime")
        bub_id_orbit.append(id1)
        bub_r_orbit.append(r)
        bub_center_orbit.append((center_x, center_y))
        bub_angle_orbit.append(angle)
        bub_radius_orbit.append(radius)
        bub_speed_orbit.append(speed)  # 回転速度
        # 3秒後に敵弾を削除
        window.after(4000, lambda id1=id1: delete_bub_orbit(id1))
    orbit_count += 1  # カウンターを増加 
    window.after(int(rest*1000), lambda: create_bub_orbit(center_x, center_y, orbit_limit, r, speed, num_bullets, rest))  # 1秒ごとに再実行  

# 円を描く敵弾を削除する関数
def delete_bub_orbit(bub_id):
    if bub_id in bub_id_orbit:
        index = bub_id_orbit.index(bub_id)
        c.delete(bub_id_orbit[index])
        del bub_id_orbit[index]
        del bub_r_orbit[index]
        del bub_center_orbit[index]
        del bub_angle_orbit[index]
        del bub_radius_orbit[index]
        del bub_speed_orbit[index]

# 円が広がりながら描かれる敵弾を生成する関数
def create_expanding_bub_orbit(center_x, center_y, expanding_orbit_limit, r, speed, num_bullets, rest):
    
        global expanding_orbit_count
        if expanding_orbit_count >= expanding_orbit_limit:
            return
        
        initial_radius = 50  # 初期の半径
        angle_step = 360 / num_bullets  # 各弾の間隔の角度
        r = 8  # 弾の半径

        for i in range(num_bullets):
                angle = i * angle_step  # 各弾の初期角度
                # 弾の初期位置を計算
                x = center_x + initial_radius * math.cos(math.radians(angle))
                y = center_y + initial_radius * math.sin(math.radians(angle))
                id1 = c.create_oval(x - r, y - r, x + r, y + r, outline="blue", fill="cyan")
                bub_id_expanding_orbit.append(id1)
                bub_r_expanding_orbit.append(r)
                bub_center_expanding_orbit.append((center_x, center_y))
                bub_angle_expanding_orbit.append(angle)
                bub_radius_expanding_orbit.append(initial_radius)
                bub_speed_expanding_orbit.append(speed)  # 半径が広がる速度
        expanding_orbit_count += 1  # カウンターを増加    
        window.after(int(rest*1000), lambda: create_expanding_bub_orbit(center_x, center_y, expanding_orbit_limit, r, speed, num_bullets, rest))  # 2秒ごとに再実行

# 円が逆回転で広がりながら描かれる敵弾を生成する関数
def create_expanding_bub_orbit_2(center_x, center_y, expanding_orbit_2_limit, r, speed, num_bullets, rest):
    
        global expanding_orbit_2_count
        if expanding_orbit_2_count >= expanding_orbit_2_limit:
            return
        
        initial_radius = 50  # 初期の半径
        angle_step = 360 / num_bullets  # 各弾の間隔の角度

        for i in range(num_bullets):
                angle = i * angle_step  # 各弾の初期角度
                # 弾の初期位置を計算
                x = center_x + initial_radius * math.cos(math.radians(angle))
                y = center_y + initial_radius * math.sin(math.radians(angle))
                id1 = c.create_oval(x - r, y - r, x + r, y + r, outline="orange", fill="white")
                bub_id_expanding_orbit_2.append(id1)
                bub_r_expanding_orbit_2.append(r)
                bub_center_expanding_orbit_2.append((center_x, center_y))
                bub_angle_expanding_orbit_2.append(angle)
                bub_radius_expanding_orbit_2.append(initial_radius)
                bub_speed_expanding_orbit_2.append(speed)  # 半径が広がる速度

        expanding_orbit_2_count += 1  # カウンターを増加
        window.after(int(rest*1000), lambda:create_expanding_bub_orbit_2(center_x, center_y, expanding_orbit_2_limit, r, speed, num_bullets, rest))  # 2秒ごとに再実行

# ショットガンの敵弾を生成する関数
def create_shotgun_bullets(center_x, center_y, shotgun_limit, r, speed, num_bullets, spread_angle, rest):
    global shotgun_count
    if shotgun_count >= shotgun_limit:
        return
        
    # 自機の位置を取得
    ship_x, ship_y = get_coords(ship_id)

    # 自機への基準角度を計算
    base_angle = math.degrees(math.atan2(ship_y - center_y, ship_x - center_x))# 自機の位置を取得

    # 自機への基準角度を計算
    base_angle = math.degrees(math.atan2(ship_y - center_y, ship_x - center_x))

    for i in range(num_bullets):
            # 各弾の角度をランダムに決定
            angle = base_angle + randint(-spread_angle // 2, spread_angle // 2)
            initial_speed = speed * 2  # 初期速度は設定速度の4倍

            # 弾の初期位置を計算
            dx = initial_speed * math.cos(math.radians(angle))
            dy = initial_speed * math.sin(math.radians(angle))
            id1 = c.create_oval(center_x - r, center_y - r, center_x + r, center_y + r, outline="orange", fill="yellow")
            bub_id_shotgun.append(id1)
            bub_dx_shotgun.append(dx)
            bub_dy_shotgun.append(dy)
            bub_r_shotgun.append(r)
            bub_speed_shotgun.append(speed)

    shotgun_count += 1  # カウンターを増加
    window.after(int(rest*1000), lambda: create_shotgun_bullets(center_x, center_y, shotgun_limit, r, speed, num_bullets, spread_angle, rest))  # 1秒ごとに再実行

# 螺旋階段状の敵弾を生成する関数
spiral_angle = 0  # グローバル変数で角度を管理

def create_spiral_bullets(center_x, center_y, spiral_limit, r, speed, num_bullets, rest):
    global spiral_count
    if spiral_count >= spiral_limit:
        return
    
    global spiral_angle
    radius = 50  # 弾の初期半径

    for i in range(num_bullets):
        # 各弾の角度を計算
        angle = spiral_angle + (360 / num_bullets) * i
        angle_rad = math.radians(angle)

        # 弾の初期位置を計算
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)

        # 弾を生成
        id1 = c.create_oval(x - r, y - r, x + r, y + r, outline="purple", fill="violet")
        bub_id_spiral.append(id1)
        bub_r_spiral.append(r)
        bub_speed_spiral.append(speed)
        bub_angle_spiral.append(angle)  # 各弾の角度を保存

    # 次の発射のために角度を更新
    spiral_angle += 10  # 角度を少しずつ増加させる
    spiral_angle %= 360  # 角度を0～360度に制限

    spiral_count += 1  # カウンターを増加
    # 一定間隔で再実行
    window.after(int(rest*200), lambda: create_spiral_bullets(center_x, center_y, spiral_limit, r, speed, num_bullets, rest))  # 200ミリ秒ごとに再実行

# レーザーを生成する関数
def create_laser(x1, y1, x2, y2, laser_limit, width1, width2 , rest):
    global laser_count
    if laser_count >= laser_limit:
        return  # 生成回数が上限に達したら停止
    
    # 予告線を描画（破線）
    warning_line = c.create_line(x1, y1, x2, y2, fill="white", width = width1,)
    
    # 2秒後にレーザーを発射
    def fire_laser():
        # 予告線を削除
        c.delete(warning_line)
        
        # レーザーを描画（実線）
        laser = c.create_line(x1, y1, x2, y2, fill="yellow", width = width2)
        laser_id.append(laser)
        laser_active.append(True)

        # 1秒後にレーザーを削除
        window.after(1000, lambda: delete_laser(laser))
    
    window.after(2000, fire_laser)  # 2秒後にレーザーを発射
    laser_count += 1  # カウンターを増加
    window.after(int(rest*1000), lambda: create_laser(x1, y1, x2, y2, laser_limit, width1, width2 , rest))  # 200ミリ秒ごとに再実行

def delete_laser(laser):
    if laser in laser_id:
        index = laser_id.index(laser)
        c.delete(laser_id[index])
        del laser_id[index]
        del laser_active[index]

# 敵弾（右から左）を移動させる関数
def move_bubbles_left():
    for i in range(len(bub_id_left) - 1, -1, -1):  # 逆順でループ
        c.move(bub_id_left[i], -bub_speed_left[i], 0)  # 左方向に移動
        x1, y1, x2, y2 = c.coords(bub_id_left[i])
        if x2 < 0:  # 画面外に出たら削除
            c.delete(bub_id_left[i])
            del bub_id_left[i]
            del bub_r_left[i]
            del bub_speed_left[i]
    window.after(50, move_bubbles_left)  # 50ミリ秒ごとに再実行

# 敵弾（上から下）を移動させる関数
def move_bubbles_down():
    for i in range(len(bub_id_down) - 1, -1, -1):  # 逆順でループ
        c.move(bub_id_down[i], 0, bub_speed_down[i])  # 下方向に移動
        x1, y1, x2, y2 = c.coords(bub_id_down[i])
        if y1 > HEGHT:  # 画面外に出たら削除
            c.delete(bub_id_down[i])
            del bub_id_down[i]
            del bub_r_down[i]
            del bub_speed_down[i]
    window.after(50, move_bubbles_down)  # 50ミリ秒ごとに再実行

# 敵弾（円形）を移動させる関数
def move_bubbles_circle():
    for i in range(len(bub_id_circle) - 1, -1, -1):
            angle = bub_angle_circle[i]
            target_speed = bub_speed_circle[i]
            current_speed = bub_current_speed_circle[i]

            # 減速処理
            if current_speed > target_speed:
                current_speed -= 1.2  # 減速率
                if current_speed < target_speed:
                    current_speed = target_speed  # 目標速度に達したら停止
                bub_current_speed_circle[i] = current_speed

            # 移動量を計算
            dx = current_speed * math.cos(math.radians(angle))
            dy = current_speed * math.sin(math.radians(angle))

            # 敵弾を移動
            c.move(bub_id_circle[i], dx, dy)

            # 現在の座標を取得
            x1, y1, x2, y2 = c.coords(bub_id_circle[i])
            if x2 < 0 or x1 > WIDTH or y2 < 0 or y1 > HEGHT:  # 画面外に出たら削除
                c.delete(bub_id_circle[i])
                del bub_id_circle[i]
                del bub_r_circle[i]
                del bub_speed_circle[i]
                del bub_angle_circle[i]
                del bub_current_speed_circle[i]
    window.after(50, move_bubbles_circle)  # 50ミリ秒ごとに再実行

# 自機狙いの敵弾を移動させる関数
def move_bubbles_targeted():
    for i in range(len(bub_id_targeted) - 1, -1, -1):
        # 現在の速度を取得
        dx = bub_dx_targeted[i]
        dy = bub_dy_targeted[i]
        target_speed = bub_speed_targeted[i]

        # 現在の速度を計算
        current_speed = math.sqrt(dx**2 + dy**2)

        # 減速処理
        if current_speed > target_speed:
            scale = (current_speed - 1.2) / current_speed  # 減速率
            dx *= scale
            dy *= scale
            bub_dx_targeted[i] = dx
            bub_dy_targeted[i] = dy

        # 敵弾を移動
        c.move(bub_id_targeted[i], dx, dy)

        # 現在の座標を取得
        x1, y1, x2, y2 = c.coords(bub_id_targeted[i])
        if x2 < 0 or x1 > WIDTH or y2 < 0 or y1 > HEGHT:  # 画面外に出たら削除
            c.delete(bub_id_targeted[i])
            del bub_id_targeted[i]
            del bub_r_targeted[i]
            del bub_speed_targeted[i]
            del bub_dx_targeted[i]
            del bub_dy_targeted[i]
    window.after(50, move_bubbles_targeted)  # 50ミリ秒ごとに再実行

# 円を描く敵弾を移動させる関数
def move_bubbles_orbit():
    for i in range(len(bub_id_orbit) - 1, -1, -1):
        # 現在の角度を更新
        bub_angle_orbit[i] += bub_speed_orbit[i]
        bub_angle_orbit[i] %= 360  # 角度を0～360度に制限

        # 新しい座標を計算
        center_x, center_y = bub_center_orbit[i]
        radius = bub_radius_orbit[i]
        angle_rad = math.radians(bub_angle_orbit[i])
        new_x = center_x + radius * math.cos(angle_rad)
        new_y = center_y + radius * math.sin(angle_rad)

        # 敵弾を移動
        x1, y1, x2, y2 = c.coords(bub_id_orbit[i])
        dx = new_x - (x1 + x2) / 2
        dy = new_y - (y1 + y2) / 2
        c.move(bub_id_orbit[i], dx, dy)

        # 画面外に出たら削除
        if new_x < 0 or new_x > WIDTH or new_y < 0 or new_y > HEGHT:
            c.delete(bub_id_orbit[i])
            del bub_id_orbit[i]
            del bub_r_orbit[i]
            del bub_center_orbit[i]
            del bub_angle_orbit[i]
            del bub_radius_orbit[i]
            del bub_speed_orbit[i]
    window.after(50, move_bubbles_orbit)  # 50ミリ秒ごとに再実行

# 円が広がりながら描かれる敵弾を移動させる関数
def move_expanding_bubbles_orbit():
    for i in range(len(bub_id_expanding_orbit) - 1, -1, -1):
        # 半径を広げる
        bub_radius_expanding_orbit[i] += bub_speed_expanding_orbit[i]

        # 角度を回転させる
        bub_angle_expanding_orbit[i] += 0.8  # 回転速度（角度を増加）
        bub_angle_expanding_orbit[i] %= 360  # 角度を0～360度に制限

        # 新しい座標を計算
        center_x, center_y = bub_center_expanding_orbit[i]
        radius = bub_radius_expanding_orbit[i]
        angle_rad = math.radians(bub_angle_expanding_orbit[i])
        new_x = center_x + radius * math.cos(angle_rad)
        new_y = center_y + radius * math.sin(angle_rad)

        # 敵弾を移動
        x1, y1, x2, y2 = c.coords(bub_id_expanding_orbit[i])
        dx = new_x - (x1 + x2) / 2
        dy = new_y - (y1 + y2) / 2
        c.move(bub_id_expanding_orbit[i], dx, dy)

        # 完全に画面外に出たら削除
        max_radius = math.sqrt(WIDTH**2 + HEGHT**2)  # 画面の対角線の長さ
        if radius > max_radius:
            c.delete(bub_id_expanding_orbit[i])
            del bub_id_expanding_orbit[i]
            del bub_r_expanding_orbit[i]
            del bub_center_expanding_orbit[i]
            del bub_angle_expanding_orbit[i]
            del bub_radius_expanding_orbit[i]
            del bub_speed_expanding_orbit[i]
    window.after(50, move_expanding_bubbles_orbit)  # 50ミリ秒ごとに再実行

# 円が逆回転で広がりながら描かれる敵弾を移動させる関数
def move_expanding_bubbles_orbit_2():
    for i in range(len(bub_id_expanding_orbit_2) - 1, -1, -1):
        # 半径を広げる
        bub_radius_expanding_orbit_2[i] += bub_speed_expanding_orbit_2[i]

        # 角度を回転させる
        bub_angle_expanding_orbit_2[i] -= 0.8  # 回転速度（角度を増加）
        bub_angle_expanding_orbit_2[i] %= 360  # 角度を0～360度に制限

        # 新しい座標を計算
        center_x, center_y = bub_center_expanding_orbit_2[i]
        radius = bub_radius_expanding_orbit_2[i]
        angle_rad = math.radians(bub_angle_expanding_orbit_2[i])
        new_x = center_x + radius * math.cos(angle_rad)
        new_y = center_y + radius * math.sin(angle_rad)

        # 敵弾を移動
        x1, y1, x2, y2 = c.coords(bub_id_expanding_orbit_2[i])
        dx = new_x - (x1 + x2) / 2
        dy = new_y - (y1 + y2) / 2
        c.move(bub_id_expanding_orbit_2[i], dx, dy)

        # 完全に画面外に出たら削除
        max_radius = math.sqrt(WIDTH**2 + HEGHT**2)  # 画面の対角線の長さ
        if radius > max_radius:
            c.delete(bub_id_expanding_orbit_2[i])
            del bub_id_expanding_orbit_2[i]
            del bub_r_expanding_orbit_2[i]
            del bub_center_expanding_orbit_2[i]
            del bub_angle_expanding_orbit_2[i]
            del bub_radius_expanding_orbit_2[i]
            del bub_speed_expanding_orbit_2[i]
    window.after(50, move_expanding_bubbles_orbit_2)  # 50ミリ秒ごとに再実行


# ショットガンの敵弾を移動させる関数
def move_shotgun_bullets():
    for i in range(len(bub_id_shotgun) - 1, -1, -1):  # 逆順でループ
        # 現在の速度を取得
        dx = bub_dx_shotgun[i]
        dy = bub_dy_shotgun[i]
        target_speed = bub_speed_shotgun[i]

        # 現在の速度を計算
        current_speed = math.sqrt(dx**2 + dy**2)

        # 減速処理
        if current_speed > target_speed:
            scale = (current_speed - 1.2) / current_speed  # 減速率
            dx *= scale
            dy *= scale
            bub_dx_shotgun[i] = dx
            bub_dy_shotgun[i] = dy

        # 敵弾を移動
        c.move(bub_id_shotgun[i], dx, dy)

        # 現在の座標を取得
        x1, y1, x2, y2 = c.coords(bub_id_shotgun[i])
        if x2 < 0 or x1 > WIDTH or y2 < 0 or y1 > HEGHT:  # 画面外に出たら削除
            c.delete(bub_id_shotgun[i])
            del bub_id_shotgun[i]
            del bub_dx_shotgun[i]
            del bub_dy_shotgun[i]
            del bub_r_shotgun[i]
            del bub_speed_shotgun[i]

    window.after(50, move_shotgun_bullets)  # 50ミリ秒ごとに再実行

# 敵弾（螺旋）を移動させる関数
def move_bubbles_spiral():
    for i in range(len(bub_id_spiral) - 1, -1, -1):
            angle = bub_angle_spiral[i]
            speed = bub_speed_spiral[i]

            # 移動量を計算
            dx = speed * math.cos(math.radians(angle))
            dy = speed * math.sin(math.radians(angle))

            # 敵弾を移動
            c.move(bub_id_spiral[i], dx, dy)

            # 現在の座標を取得
            x1, y1, x2, y2 = c.coords(bub_id_spiral[i])
            if x2 < 0 or x1 > WIDTH or y2 < 0 or y1 > HEGHT:  # 画面外に出たら削除
                c.delete(bub_id_spiral[i])
                del bub_id_spiral[i]
                del bub_r_spiral[i]
                del bub_speed_spiral[i]
                del bub_angle_spiral[i]
    window.after(50, move_bubbles_spiral)  # 50ミリ秒ごとに再実行

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return (x, y)

def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def collision():
    global is_invincible
    if is_invincible:
        window.after(20, collision)
        return  # 無敵状態の場合は衝突判定をスキップ

    # 右から左の敵弾との衝突判定
    for bub in range(len(bub_id_left) - 1, -1, -1):
        if distance(ship_id, bub_id_left[bub]) < (SHIP_R + bub_r_left[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする

    # 上から下の敵弾との衝突判定
    for bub in range(len(bub_id_down) - 1, -1, -1):
        if distance(ship_id, bub_id_down[bub]) < (SHIP_R + bub_r_down[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    # 円形の敵弾との衝突判定
    for bub in range(len(bub_id_circle) - 1, -1, -1):
        if distance(ship_id, bub_id_circle[bub]) < (SHIP_R + bub_r_circle[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする

    # 自機狙いの敵弾との衝突判定
    for bub in range(len(bub_id_targeted) - 1, -1, -1):
        if distance(ship_id, bub_id_targeted[bub]) < (SHIP_R + bub_r_targeted[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    # 円を描く敵弾との衝突判定
    for bub in range(len(bub_id_orbit) - 1, -1, -1):
        if distance(ship_id, bub_id_orbit[bub]) < (SHIP_R + bub_r_orbit[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    # 円を描く敵弾（広がる）との衝突判定
    for bub in range(len(bub_id_expanding_orbit) - 1, -1, -1):
        if distance(ship_id, bub_id_expanding_orbit[bub]) < (SHIP_R + bub_r_expanding_orbit[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    # 円を描く敵弾（逆回転で広がる）との衝突判定
    for bub in range(len(bub_id_expanding_orbit_2) - 1, -1, -1):
        if distance(ship_id, bub_id_expanding_orbit_2[bub]) < (SHIP_R + bub_r_expanding_orbit_2[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    # 螺旋階段状の敵弾との衝突判定
    for bub in range(len(bub_id_spiral) - 1, -1, -1):
        if distance(ship_id, bub_id_spiral[bub]) < (SHIP_R + bub_r_spiral[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    # ショットガンの敵弾との衝突判定
    for bub in range(len(bub_id_shotgun) - 1, -1, -1):
        if distance(ship_id, bub_id_shotgun[bub]) < (SHIP_R + bub_r_shotgun[bub]) // 4 * 3:
            reset_ship_position()  # 自機を初期位置に戻す
            set_invincible(3000)  # 3秒間無敵状態にする
        
    for i in range(len(laser_id) - 1, -1, -1):
        if laser_active[i]:  # レーザーがアクティブな場合のみ判定
            # 自機の座標を取得
            x1, y1, x2, y2 = c.coords(ship_id)
            ship_center_x = (x1 + x2) / 2
            ship_center_y = (y1 + y2) / 2
            
            # レーザーの座標を取得
            laser_coords = c.coords(laser_id[i])
            lx1, ly1, lx2, ly2 = laser_coords
            
            # 自機がレーザーの線上にあるか判定
            # レーザーの幅を考慮した判定
            laser_width = 5  # レーザーの当たり判定の幅
            if (min(lx1, lx2) - laser_width <= ship_center_x <= max(lx1, lx2) + laser_width and
                min(ly1, ly2) - laser_width <= ship_center_y <= max(ly1, ly2) + laser_width):
                # 衝突時の処理（例: ゲームオーバー）
                reset_ship_position()  # 自機を初期位置に戻す
                set_invincible(3000)  # 3秒間無敵状態にする
    window.after(20, collision)

def reset_counters():
    global circle_count, expanding_orbit_count, spiral_count, shotgun_count, laser_count, targeted_count, orbit_count
    circle_count = 0
    expanding_orbit_count = 0
    spiral_count = 0
    shotgun_count = 0
    laser_count = 0
    targeted_count = 0
    orbit_count = 0


# 最初の敵弾を発射する関数
def start_first_enemy():
    reset_counters()  # カウンターをリセット
    create_enemy(WIDTH // 2, -50, WIDTH // 2, HEGHT // 8)  # 敵の生成を開始
    # 5秒後に次の敵弾を発射
    window.after(1000, start_second_enemy)

# 次の敵弾を発射する関数
def start_second_enemy():
    reset_counters()  # カウンターをリセット
    create_enemy(WIDTH // 4, -50, WIDTH // 4, HEGHT // 8)  # 敵の生成を開始
    window.after(1000, start_third_enemy)  # 1秒後に次の敵弾を発射

def start_third_enemy():
    reset_counters()  # カウンターをリセット
    create_enemy(WIDTH // 4 * 3, -50, WIDTH // 4 * 3, HEGHT // 8)  # 敵の生成を開始
rest = 4000
# 最初の敵弾を発射
for i in range(5):
    window.after(int(rest), start_first_enemy)
    rest += 4000
    
move_shotgun_bullets()  # 敵弾の移動を開始
move_bubbles_circle()
move_bubbles_targeted()
# 自機の弾の移動を開始
move_player_bullets()
check_enemy_collision()  # 敵と弾の衝突判定を開始
move_enemies()  # 敵を移動させる
collision()

# イベントバインド
c.bind_all("<KeyPress>", key_press)
c.bind_all("<KeyRelease>", key_release)

# 移動処理を開始
move_ship()

window.mainloop()