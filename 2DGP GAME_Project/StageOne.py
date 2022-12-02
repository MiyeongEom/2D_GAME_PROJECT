from pico2d import*
import random
import game_framework
import game_world

GAME_X = 1300
GAME_Y = 600

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11

class StageOne:
    def __init__(self):
        self.stage1 = load_image('Resource/StageOne/stage1_background.png')

    def draw(self):
        self.stage1.draw(GAME_X//2, GAME_Y//2)

    def update(self):
        pass


# (130, 240), (410, 140), (900, 300)
class Block1:
    image = None
    def __init__(self, x, y):
        if Block1.image == None:
            Block1.image = load_image('Resource/StageOne/Block1.png')

        self.x = x
        self.y = y
        self.w  = 194.4
        self.h = 48

    def draw(self):
        # 200 240 194.4 48
        self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 97.2, self.y - 24, self.x + 97.2, self.y + 24

    def handle_collision(self, other, group):
        if group == 'blocks_basic:main_hero':

            pass


#(410, 330), (540, 330), (670, 300)
class Block2:
    image = None
    def __init__(self, x, y):
        if Block2.image == None:
            Block2.image = load_image('Resource/StageOne/Block2.png')
        self.x, self.y = x, y
        self.w, self.h = 55, 54

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())


    def update(self):
        pass

    def get_bb(self):
        return self.x - 28, self.y - 27, self.x + 26, self.y + 25

    def handle_collision(self, other, group):
        if group == 'tree_node:main_hero':
            pass


#(750, 60), (750, 100), (750, 140), (750, 180), (750, 220)
class Block3:
    image = None

    def __init__(self, x, y):
        if Block3.image == None:
            Block3.image = load_image('Resource/StageOne/Block3.png')
        self.x, self.y = x, y
        self.w, self.h = 40, 40

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())


    def update(self):
        pass

    def get_bb(self):
        return self.x - 21, self.y - 21, self.x + 21, self.y + 21

    def handle_collision(self, other, group):
        if group == 'block3:main_hero':
            pass


class Spirit:
    image = None

    def __init__(self, x, y):
        if Spirit.image == None:
            Spirit.image = load_image('Resource/StageOne/Spirit.png')
        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        self.image.clip_draw(int(self.frame) % 11 * 100, 0, 100, 100, self.x, self.y, 140, 140)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 55, self.x + 15, self.y + 10

    def handle_collision(self, other, group):
        if group == 'spirit:main_hero':
            game_world.remove_object(self)
            pass

