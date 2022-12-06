from pico2d import*
import random
import server
import game_framework
import game_world
import os

GAME_X = 1300
GAME_Y = 600

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11


class StageOne:
    def __init__(self):
        self.stage1 = load_image('Resource/StageOne/stage1_background.png')
        self.bar = load_image('Resource/UI/Basic.png')
        self.distance = load_image('Resource/UI/Distance.png')

        self.font = load_font('Font/Galmuri11-Bold.ttf', 20)
        self.font2 = load_font('Font/Galmuri11-Bold.ttf', 25)
        self.font3 = load_font('Font/Galmuri11-Bold.ttf', 28)

        self.canvas_width = GAME_X
        self.canvas_height = GAME_Y
        self.w = self.stage1.w
        self.h = self.stage1.h

    def draw(self):
        self.stage1.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height,
            0, 0
        )

        self.bar.draw(650, 600, 1300, 100)
        self.distance.draw(230, 595, 200, 100)
        self.font3.draw(615, 575, '60.0', (255, 255, 255))
        self.font2.draw(35, 625, 'n o w', (255, 255, 200))
        self.font.draw(565, 625, 'S T A G E - 0 1', (255, 255, 200))

    def update(self):
        self.window_left = clamp(0, int(server.main_hero.x) - self.canvas_width // 2, self.w - self.canvas_width - 1)
        self.window_bottom = clamp(0, int(server.main_hero.y) - self.canvas_height // 2, self.h - self.canvas_height - 1)
        pass

class HeroPosition:
    def __init__(self):
        self.image = load_image('Resource/UI/Position.png')
        self.x, self.y = 133, 628

    def draw(self):
        self.image.draw(self.x, self.y, 14, 14)

    def update(self):
        if 40 <= server.main_hero.x < 587:
            self.x = 133
        if 1215 <= server.main_hero.x < 1842:
            self.x = 230
        if 2470 <= server.main_hero.x:
            self.x = 333
        if 587 <= server.main_hero.x < 1215:
            self.x = 183
        if 1842 <= server.main_hero.x < 2470:
            self.x = 283

class HpLife:
    def __init__(self):
        self.image = load_image('Resource/UI/Life.png')
        self.x, self.y = 40, 565

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

    def update(self):
        pass

class HpBar:
    def __init__(self):
        self.image1 = load_image('Resource/UI/Bar1.png')
        self.image2 = load_image('Resource/UI/Bar2.png')
        self.image3 = load_image('Resource/UI/Bar3.png')
        self.image4 = load_image('Resource/UI/Bar4.png')
        self.image5 = load_image('Resource/UI/Bar5.png')
        self.image6 = load_image('Resource/UI/Bar6.png')
        self.image7 = load_image('Resource/UI/Bar7.png')
        self.hp_sound = load_wav('hp_sound.mp3')
        self.hp_sound.set_volume(40)
        self.x, self.y = 190, 567
        self.bar = 1

    def draw(self):
        if self.bar == 1:
            self.image1.draw(self.x, self.y, 247, 32)

        elif self.bar == 2:
            self.image2.draw(self.x, self.y, 247, 32)

        elif self.bar == 3:
            self.image3.draw(self.x, self.y, 247, 32)

        elif self.bar == 4:
            self.image4.draw(self.x, self.y, 247, 32)

        elif self.bar == 5:
            self.image5.draw(self.x, self.y, 247, 32)

        elif self.bar == 6:
            self.image6.draw(self.x, self.y, 247, 32)

        elif self.bar == 7:
            self.image7.draw(self.x, self.y, 247, 32)

    def update(self):
        if 0 <= server.main_hero.hp < 30:
            self.bar = 7
        elif 30 <= server.main_hero.hp < 60:
            self.bar = 6
        elif 60 <= server.main_hero.hp < 90:
            self.bar = 5
        elif 90 <= server.main_hero.hp < 120:
            self.bar = 4
        elif 120 <= server.main_hero.hp < 150:
            self.bar = 3
        elif 150 <= server.main_hero.hp < 180:
            self.bar = 2
        elif 180 <= server.main_hero.hp :
            self.bar = 1


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
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        self.image.draw(sx, sy, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        return sx - 97.2, sy - 24, sx + 97.2, sy + 24

    def handle_collision(self, other, group):
        if group == 'blocks_basic:main_hero':
            pass

        if group == 'skill:blocks_basic':
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
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        self.image.draw(sx, sy, self.w, self.h)
        draw_rectangle(*self.get_bb())


    def update(self):
        pass

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        return sx - 28, sy - 27, sx + 26, sy + 25

    def handle_collision(self, other, group):
        if group == 'tree_node:main_hero':
            pass

        if group == 'skill:tree_node':
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
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        self.image.draw(sx, sy, self.w, self.h)
        self.image.draw(sx, sy + 40, self.w, self.h)
        self.image.draw(sx, sy + 80, self.w, self.h)
        self.image.draw(sx, sy + 120 , self.w, self.h)
        self.image.draw(sx, sy + 160 , self.w, self.h)
        draw_rectangle(*self.get_bb())


    def update(self):
        pass

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        return sx - 21, sy - 21, sx + 21, sy + 180

    def handle_collision(self, other, group):
        if group == 'stone:main_hero':
            pass

        if group == 'skill:stone':
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
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        self.image.clip_draw(int(self.frame) % 11 * 100, 0, 100, 100, sx, sy, 140, 140)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        return sx - 15, sy - 55, sx + 15, sy + 10

    def handle_collision(self, other, group):
        if group == 'spirit:main_hero':
            game_world.remove_object(self)
            pass

