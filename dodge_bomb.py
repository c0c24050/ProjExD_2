import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 練習1移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    pg.K_w: (0, -5),
    pg.K_s: (0, +5),
    pg.K_a: (-5, 0),
    pg.K_d: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:  # 練習3場外定義
    """オブジェクトが画面内にあるかチェック"""
    x_ok = 0 <= obj_rct.left and obj_rct.right <= WIDTH
    y_ok = 0 <= obj_rct.top and obj_rct.bottom <= HEIGHT
    return x_ok, y_ok


def game_over(screen: pg.Surface) -> None:  # 演習1ゲームオーバー
    """ゲームオーバー画面を表示"""
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(150)
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))

    sad_img = pg.image.load("fig/8.png")
    sad_img = pg.transform.rotozoom(sad_img, 0, 0.9)
    sad_rct1 = sad_img.get_rect(center=(WIDTH//2 + 180, HEIGHT//2))
    sad_rct2 = sad_img.get_rect(center=(WIDTH//2 - 180, HEIGHT//2))
    screen.blit(sad_img, sad_rct1)
    screen.blit(sad_img, sad_rct2)

    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pg.display.update()
    time.sleep(5)


def make_bomb_assets():  # 演習爆弾変化
    """爆弾の画像と加速度のリストを作成"""
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def load_images():  # 演習3鳥方向転換
    """こうかとんの方向別画像を読み込み"""
    kk_img0 = pg.image.load("fig/3.png")
    kk_imgs = {}
    directions = {
        (0, 0): 0,
        (5, 0): 0,
        (-5, 0): 0,
        (0, -5): -90,
        (0, 5): 90,
        (5, -5): -45,
        (-5, -5): -45,
        (5, 5): 45,
        (-5, 5): 45
    }
    for mv, angle in directions.items():
        img = pg.transform.rotozoom(kk_img0, angle, 0.9)
        # 左方向のときだけ左右反転
        if mv[0] > 0:
            img = pg.transform.flip(img, True, False)
        kk_imgs[mv] = img
    return kk_imgs


def get_movement_direction(sum_mv: list[int]) -> tuple[int, int]:
    """移動量から方向を決定"""
    dx = -5 if sum_mv[0] < 0 else 5 if sum_mv[0] > 0 else 0
    dy = -5 if sum_mv[1] < 0 else 5 if sum_mv[1] > 0 else 0
    return (dx, dy)


def chase_velocity(bb_rct: pg.Rect, kk_rct: pg.Rect, vx: float, vy: float) -> tuple[float, float]:  # 演習4追尾爆弾
    """爆弾がこうかとんを追いかけるように移動方向を決定する"""
    dx = kk_rct.centerx - bb_rct.centerx
    dy = kk_rct.centery - bb_rct.centery
    dist2 = dx**2 + dy**2

    if dist2 < 300**2:
        return vx, vy

    norm = (dx**2 + dy**2) ** 0.5
    if norm == 0:
        return 0, 0
    scale = (50 ** 0.5) / norm
    return dx * scale, dy * scale


def main():
    """メイン関数"""
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_imgs = load_images()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()

    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = make_bomb_assets()

    # 練習2爆弾定義
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        old_rct = kk_rct.copy()  # 練習3場外壁
        kk_rct.move_ip(sum_mv)
        x_ok, y_ok = check_bound(kk_rct)
        if not x_ok or not y_ok:
            kk_rct = old_rct

        mv_dir = get_movement_direction(sum_mv)
        kk_img = kk_imgs.get(mv_dir, kk_imgs[(0, 0)])

        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        acc = bb_accs[idx]
        vx, vy = chase_velocity(bb_rct, kk_rct, vx, vy)
        avx, avy = vx * acc, vy * acc

        bb_rct.move_ip(avx, avy)  # 練習2爆弾移動
        if bb_rct.left < 0 or bb_rct.right > WIDTH:
            vx *= -1
        if bb_rct.top < 0 or bb_rct.bottom > HEIGHT:
            vy *= -1

        bb_rct = bb_img.get_rect(center=bb_rct.center)

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        if kk_rct.colliderect(bb_rct):  # 練習4衝突判定
            game_over(screen)
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()