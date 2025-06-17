import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {  #練習1移動量辞書
    pg.K_UP:    (0, -5),
    pg.K_DOWN:  (0, +5),
    pg.K_LEFT:  (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:#練習3場外定義
    x_ok = 0 <= obj_rct.left and obj_rct.right <= WIDTH
    y_ok = 0 <= obj_rct.top and obj_rct.bottom <= HEIGHT
    return x_ok, y_ok


def game_over(screen: pg.Surface) -> None:#演習1がめおべら
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


def make_bomb_assets():#演習2爆弾変化
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    print(bb_accs)
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs,bb_accs = make_bomb_assets()

#練習2爆弾定義
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

        old_rct = kk_rct.copy()#練習3場外壁
        kk_rct.move_ip(sum_mv)
        x_ok, y_ok = check_bound(kk_rct)
        if not x_ok or not y_ok:
            kk_rct = old_rct

        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        acc = bb_accs[idx]
        avx, avy = vx * acc, vy * acc

        bb_rct.move_ip(avx, avy)#練習2爆弾移動
        if bb_rct.left < 0 or bb_rct.right > WIDTH:
            vx *= -1
        if bb_rct.top < 0 or bb_rct.bottom > HEIGHT:
            vy *= -1

        bb_rct = bb_img.get_rect(center=bb_rct.center)

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        if kk_rct.colliderect(bb_rct):  #練習4衝突判定
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
