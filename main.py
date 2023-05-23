import random
import sys
import time

import pygame as pg

white = (255,255,255)
black = (0,0,0)
green = (0,150,0)
red = (255,0,0)
blue = (0,0,255)
light_blue = (147,251,253)
width = 1600
height = 900
goalheight = 50

def check_bound(area: pg.Rect, obj: pg.Rect) -> tuple[bool, bool]:
    """
    ホッケーの玉の移動範囲を指定
    """
    
    yoko, tate = True, True
    if obj.left < area.left or area.right < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < area.top or area.bottom < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


def check_bound_hockey(scr_rect: pg.Rect, obj_rect: pg.Rect):
    """
    ホッケーの動く範囲を指定
    """
    yoko, tate = True, True
    if obj_rect.center <  scr_rect.center:
        if obj_rect.left < scr_rect.left or scr_rect.centerx < obj_rect.right:
            yoko = False
    if obj_rect.center >  scr_rect.center:
        if obj_rect.left < scr_rect.centerx or scr_rect.right < obj_rect.right:
            yoko = False
    if obj_rect.top < scr_rect.top or scr_rect.bottom < obj_rect.bottom:
        tate = False
    return yoko, tate

class playerlect_1:

    _delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }
    

    def __init__(self, xy: tuple[int,int]): 
        self._img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/redpad.png"),0, 2.0)
        self._rct = self._img.get_rect()
        self._rct.center = xy


    def update(self,key_lst: list[bool], screen: pg.Surface):
        for k,mv in __class__._delta.items():
            if key_lst[k]:
                self._rct.move_ip(mv)
        if check_bound_hockey(screen.get_rect(), self._rct) != (True, True):
            for k, mv in __class__._delta.items():
                if key_lst[k]:
                    self._rct.move_ip(-mv[0], -mv[1])
        screen.blit(self._img,self._rct)

class ball:
    _dires = [-1, 0, +1]
    def __init__(self):
        self._img = pg.image.load(f"ex05/fig/disc.png")
        self._rct = self._img.get_rect()
        self._rct.center = width/2,height/2
        self._vx, self._vy = random.choice(ball._dires),random.choice(ball._dires)
        
    def update(self,screen: pg.Surface):
        yoko,tate = check_bound(screen.get_rect(), self._rct)
        if not yoko:
            self._vx *= -1
        if not tate:
            self._vy *= -1
        self._rct.move_ip(self._vx, self._vy)
        screen.blit(self._img,self._rct)



def main():
    pg.display.set_caption("Air-hockey")
    screen = pg.display.set_mode((1600,900))
    pl1 = playerlect_1((width-300,height/2))
    disc = ball()
    clock = pg.time.Clock()


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        screen.fill((0,0,0))  # フィールドについて
        pg.draw.line(screen, blue,(0,0), (screen.get_width()/2 - 5,0) ,20)  # フィールドについて
        pg.draw.line(screen, blue,(0,screen.get_height()), (screen.get_width()/2 - 5,screen.get_height()) ,20)  # フィールドについて
        pg.draw.line(screen, red, (screen.get_width()/2+5,0), (screen.get_width() ,0) ,20)  # フィールドについて
        pg.draw.line(screen, red, (screen.get_width()/2 + 5,screen.get_height()) , (screen.get_width(),screen.get_height()) ,20)  # フィールドについて
        pg.draw.line(screen,white,(width/2,0),(width/2,height),5)  # フィールドについて
        pg.draw.line(screen, (0, 0, 255), (0,0), (0,screen.get_height()/2-goalheight) ,20)  # フィールドについて
        pg.draw.line(screen, (0, 0, 255), (0,screen.get_height()/2 + goalheight), (0,screen.get_height()) ,20)  # フィールドについて
        pg.draw.line(screen, (255, 0, 0), (screen.get_width(),0), (screen.get_width(),screen.get_height()/2-goalheight) ,20)  # フィールドについて
        pg.draw.line(screen, (255, 0, 0), (screen.get_width(),screen.get_height()/2 + goalheight), (screen.get_width(),screen.get_height()) ,20)  # フィールドについて

        key_lst = pg.key.get_pressed()
        pl1.update(key_lst,screen)
        disc.update(screen)

        pg.display.update()
        clock.tick(1000)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()