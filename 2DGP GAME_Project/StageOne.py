from pico2d import*
import Hero
import game_framework
import game_world

GAME_X = 1300
GAME_Y = 600

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
        return self.x - 97, self.y - 27, self.x + 95, self.y + 23

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
        if group == 'block2:main_hero':
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