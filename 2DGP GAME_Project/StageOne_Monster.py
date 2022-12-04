import game_framework
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import math
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


#개굴
Frog_SPEED_KMPH = 1.0  # Km / Hour
Frog_SPEED_MPM = (Frog_SPEED_KMPH * 1000.0 / 60.0)
Frog_SPEED_MPS = (Frog_SPEED_MPM / 60.0)
Frog_SPEED_PPS = (Frog_SPEED_MPS * PIXEL_PER_METER)

#킹
KING_SPEED_KMPH = 5.0  # Km / Hour
KING_SPEED_MPM = (KING_SPEED_KMPH * 1000.0 / 60.0)
KING_SPEED_MPS = (KING_SPEED_MPM / 60.0)
KING_SPEED_PPS = (KING_SPEED_MPS * PIXEL_PER_METER)

#monster
Monster_SPEED_KMPH = 4.0  # Km / Hour
Monster_SPEED_MPM = (Monster_SPEED_KMPH * 1000.0 / 60.0)
Monster_SPEED_MPS = (Monster_SPEED_MPM / 60.0)
Monster_SPEED_PPS = (Monster_SPEED_MPS * PIXEL_PER_METER)

class Frog:
    image = None

    def __init__(self, x, y):
        if Frog.image == None:
            Frog.image = load_image('Resource/MON/Frog/Walk.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0
        self.wandering = False

        self.dir = 0.2
        self.face_dir = 1

        self.speed = 0
        self.timer = 2

    def update(self):
        self.speed = Frog_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x += self.dir
        if self.x >= self.ax + 60 :  #초기값보다 이동값이 더 클 때
            self.dir -= 0.2
            self.face_dir = -1
        elif self.x <= self.ax - 60:
            self.dir += 0.2
            self.face_dir = 1

        if server.main_hero.skill == 1:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                # draw_rectangle(self.x, self.y - 56, self.x + 85, self.y + 46)
                # la > rb, ra < lb, ta < bb, ba > tb a가 몬스터 b스킬
                if server.adj_monster.get_bb()[0] < server.main_hero.x + 85 < server.adj_monster.get_bb()[2] :
                    game_world.remove_object(server.adj_monster)
            else:
                if server.adj_monster.get_bb()[0] < server.main_hero.x - 85 < server.adj_monster.get_bb()[2] :
                    game_world.remove_object(server.adj_monster)

        if server.main_hero.skill == 2:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                # draw_rectangle(self.x - 40, self.y - 37, self.x + 75, self.y + 8)
                if server.adj_monster.get_bb()[0] < server.main_hero.x + 55 < server.adj_monster.get_bb()[2]:
                    game_world.remove_object(server.adj_monster)
            else:
                if server.adj_monster.get_bb()[0] < server.main_hero.x - 55 < server.adj_monster.get_bb()[2]:
                    game_world.remove_object(server.adj_monster)
        pass


    def draw(self):
        if self.face_dir == 1:  # 오른쪽을 바라보고 있는 상태
            self.image.clip_composite_draw(int(self.frame) % 5 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 120,
                                                120)
        elif self.face_dir == -1:  # 왼쪽
            self.image.clip_draw(int(self.frame) % 5 * 100, 0, 100, 100, self.x, self.y, 110,110)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 40, self.y - 40, self.x + 38, self.y + 30
        elif self.face_dir == -1:
            return self.x - 40, self.y - 40, self.x + 38, self.y + 30

    def handle_collision(self, other, group):
        if group == 'skill:adj_monster':
            game_world.remove_object(self)

        if group == 'main_hero:adj_monster':
            pass


class King_Frog:
    image = None

    def __init__(self, x, y):
        if King_Frog.image == None:
            King_Frog.image = load_image('Resource/MON/King_Frog/King_Walk.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0

        self.dir = 0.1
        self.face_dir = 1

        self.speed = 0
        self.timer = 2

    def update(self):
        self.speed = KING_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x += self.dir
        if self.x >= self.ax + 30:  # 초기값보다 이동값이 더 클 때
            self.dir -= 0.1
            self.face_dir = -1
        elif self.x <= self.ax - 25:
            self.dir += 0.1
            self.face_dir = 1

        if server.main_hero.skill == 1:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                if server.King_monster.get_bb()[0] < server.main_hero.x + 85 < server.King_monster.get_bb()[2] :
                    game_world.remove_object(server.King_monster)
            else:
                if server.King_monster.get_bb()[0] < server.main_hero.x - 85 < server.King_monster.get_bb()[2] :
                    game_world.remove_object(server.King_monster)

        if server.main_hero.skill == 2:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                if server.King_monster.get_bb()[0] < server.main_hero.x + 55 < server.King_monster.get_bb()[2] :
                    game_world.remove_object(server.King_monster)
            else:
                if server.King_monster.get_bb()[0] < server.main_hero.x - 55 < server.King_monster.get_bb()[2] :
                    game_world.remove_object(server.King_monster)

        pass


    def draw(self):
        if self.face_dir == 1:  # 오른쪽을 바라보고 있는 상태
            self.image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 120,
                                                120)
        else:  # 왼쪽
            self.image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, self.x, self.y, 120,120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 45, self.y - 45, self.x + 35, self.y + 50

    def handle_collision(self, other, group):
        if group == 'skill:King_monster':
            game_world.remove_object(self)
        pass


class Monster:
    image = None

    def __init__(self, x, y):
        if Monster.image == None:
            Monster.image = load_image('Resource/MON/Monster/Monster_Idle.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0

        self.dir = 0.05
        self.face_dir = -1

        self.speed = 0
        self.timer = 2

    def update(self):
        self.speed = Monster_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x -= self.dir
        if self.x <= self.ax - 10:
            self.dir -= 0.05
            self.face_dir = 1

        elif self.x >= self.ax + 10:  # 초기값보다 이동값이 더 클 때
            self.dir += 0.05
            self.face_dir = -1

        if server.main_hero.skill == 1:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                if server.Mon_Monster.get_bb()[0] < server.main_hero.x + 85 < server.Mon_Monster.get_bb()[2]:
                    game_world.remove_object(server.Mon_Monster)

            else:
                if server.Mon_Monster.get_bb()[0] < server.main_hero.x - 85 < server.Mon_Monster.get_bb()[2] :
                    game_world.remove_object(server.Mon_Monster)

        if server.main_hero.skill == 2:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                if server.Mon_Monster.get_bb()[0] < server.main_hero.x + 55 < server.Mon_Monster.get_bb()[2]:
                    game_world.remove_object(server.Mon_Monster)

            else:
                if server.Mon_Monster.get_bb()[0] < server.main_hero.x - 55 < server.Mon_Monster.get_bb()[2] :
                    game_world.remove_object(server.Mon_Monster)

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
        if group == 'skill:Mon_Monster':
            game_world.remove_object(self)