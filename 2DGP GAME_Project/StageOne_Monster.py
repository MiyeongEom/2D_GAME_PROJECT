import random
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import math
import server

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30

#개굴
Frog_SPEED_KMPH = 10.0  # Km / Hour
Frog_SPEED_MPM = (Frog_SPEED_KMPH * 1000.0 / 60.0)
Frog_SPEED_MPS = (Frog_SPEED_MPM / 60.0)
Frog_SPEED_PPS = (Frog_SPEED_MPS * PIXEL_PER_METER)

#킹
KING_SPEED_KMPH = 10.0  # Km / Hour
KING_SPEED_MPM = (KING_SPEED_KMPH * 1000.0 / 60.0)
KING_SPEED_MPS = (KING_SPEED_MPM / 60.0)
KING_SPEED_PPS = (KING_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

Monster_SPEED_KMPH = 10.0  # Km / Hour
Monster_SPEED_MPM = (KING_SPEED_KMPH * 1000.0 / 60.0)
Monster_SPEED_MPS = (KING_SPEED_MPM / 60.0)
Monster_SPEED_PPS = (KING_SPEED_MPS * PIXEL_PER_METER)

class Frog:
    image = None

    def __init__(self, x, y):
        if Frog.image == None:
            Frog.image = load_image('Resource/MON/Frog/Idle.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0

        self.dir = 0
        self.face_dir = -1

        self.speed = 0
        self.timer = 2

    def update(self):
        self.speed = Frog_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # self.x += self.speed * game_framework.frame_time
        # if self.x < self.ax + 50 :  #초기값보다 이동값이 더 클 때
        #     self.x += self.speed * game_framework.frame_time
        # elif self.x >= self.ax - 50:
        #     self.x -= self.speed * game_framework.frame_time
        pass


    def draw(self):
        if self.face_dir == 1:  # 오른쪽을 바라보고 있는 상태
            self.image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 120,
                                                120)
        else:  # 왼쪽
            self.image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, self.x, self.y, 120,120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 50, self.y - 40, self.x + 40, self.y + 20
        elif self.face_dir == -1:
            return self.x - 45, self.y - 40, self.x + 45, self.y + 20

    def handle_collision(self, other, group):
        if group == 'block2:main_hero':
            print('hi hero')


class King_Frog:
    image = None

    def __init__(self, x, y):
        if King_Frog.image == None:
            King_Frog.image = load_image('Resource/MON/King_Frog/King_Idle.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0

        self.dir = 0
        self.face_dir = 1

        self.speed = 0
        self.timer = 2

    def update(self):
        self.speed = KING_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # self.x += self.speed * game_framework.frame_time
        # if self.x < self.ax + 50 :  #초기값보다 이동값이 더 클 때
        #     self.x += self.speed * game_framework.frame_time
        # elif self.x >= self.ax - 50:
        #     self.x -= self.speed * game_framework.frame_time
        pass


    def draw(self):
        if self.face_dir == 1:  # 오른쪽을 바라보고 있는 상태
            self.image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 120,
                                                120)
        else:  # 왼쪽
            self.image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, self.x, self.y, 120,120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 45, self.y - 40, self.x + 35, self.y + 50

    def handle_collision(self, other, group):
        if group == 'block2:main_hero':
            print('hi hero')


class Monster:
    image = None

    def __init__(self, x, y):
        if Monster.image == None:
            Monster.image = load_image('Resource/MON/Monster/Monster_Idle.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0

        self.dir = 0
        self.face_dir = -1

        self.speed = 0
        self.timer = 2

    def update(self):
        self.speed = Monster_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # self.x += self.speed * game_framework.frame_time
        # if self.x < self.ax + 50 :  #초기값보다 이동값이 더 클 때
        #     self.x += self.speed * game_framework.frame_time
        # elif self.x >= self.ax - 50:
        #     self.x -= self.speed * game_framework.frame_time
        pass


    def draw(self):
        if self.face_dir == 1:  # 오른쪽을 바라보고 있는 상태
            self.image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 120,
                                                120)
        else:  # 왼쪽
            self.image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, self.x, self.y, 120,120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 35, self.y - 47, self.x + 39, self.y + 50

    def handle_collision(self, other, group):
        if group == 'block2:main_hero':
            print('hi hero')