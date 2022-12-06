import game_framework
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import math
import random
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
        self.Idle_image = load_image('Resource/MON/Frog/Idle.png')
        self.Attack_image = load_image('Resource/MON/Frog/Attack.png')
        self.Death_image = load_image('Resource/MON/Frog/Death.png')
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0

        self.attack = 0
        self.hp = 120
        self.hit = 0
        self.dead = 0

        self.build_behavior_tree()
        self.face_dir = 1
        self.speed = 0
        self.timer = 0

        self.dead_sound = load_wav('Monster_dead.mp3')
        self.dead_sound.set_volume(40)

    def update(self):
        if self.speed == 0:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.face_dir)
        self.y += round(-2)

        if self.y <= 80:
            self.y = 80

        if self.hit == 1:
            print(self.hp)
            self.hp -= 1.2
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 1
            else:
                self.x += 1

        if self.hit == 2:
            print(self.hp)
            self.hp -= 1.0
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 1
            else:
                self.x += 1

        if self.hit == 3:
            print(self.hp)
            self.hp -= 0.6
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 0.3
            else:
                self.x += 0.3

        if self.hp <= 0:
            self.dead_sound.play()
            self.dead = 1
            self.timer += 1
            self.speed = 0
            server.main_hero.hit = 0
            game_world.remove_object(self)

        if self.hp > 0 :
            self.dead = 0

        if server.main_hero.skill == 1:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                # draw_rectangle(self.x, self.y - 56, self.x + 85, self.y + 46)
                # la > rb, ra < lb, ta < bb, ba > tb a가 몬스터 b스킬
                if self.get_bb()[0] < server.main_hero.x + 65 - server.first_stage.window_left < self.get_bb()[2] :
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom < self.get_bb()[3] :
                        self.hit = 1
            else:
                if self.get_bb()[0] < server.main_hero.x - 65 - server.first_stage.window_left < self.get_bb()[2] :
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom< self.get_bb()[3]:
                        self.hit = 1

        elif server.main_hero.skill == 2:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                # draw_rectangle(self.x - 40, self.y - 37, self.x + 75, self.y + 8)
                if self.get_bb()[0] < server.main_hero.x + 55 - server.first_stage.window_left < self.get_bb()[2]:
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom < self.get_bb()[3]:
                        self.hit = 2
            else:
                if self.get_bb()[0] < server.main_hero.x - 55 - server.first_stage.window_left< self.get_bb()[2]:
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom< self.get_bb()[3]:
                        self.hit = 2


        distance2 = (server.main_hero.x - self.x) ** 2 + (server.main_hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 3) ** 2:
            self.attack = 1
            self.speed = 0

        else: self.attack = 0

        self.bt.run()


    def draw(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom

        if self.attack == 1:
            if math.cos(self.face_dir) < 0:
                self.Attack_image.clip_draw(int(self.frame) % 4 * 170, 0, 170, 100, sx, sy, 200,120)

            else:
                self.Attack_image.clip_composite_draw(int(self.frame) % 4 * 170, 0, 170, 100, 0, 'h', sx, sy, 200,
                                                   120)

        elif self.dead == 1:
            if math.cos(self.face_dir) < 0:
                self.Death_image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, sx, sy, 120,120)

            else:
                self.Death_image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                                   120)

        else:
            if math.cos(self.face_dir) < 0:  # 오른쪽을 바라보고 있는 상태
                if self.speed == 0:
                    self.Idle_image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, sx, sy, 120,120)
                else:
                    self.image.clip_draw(int(self.frame) % 5 * 100, 0, 100, 100, sx, sy, 120, 120)
            else:
                if self.speed == 0:
                    self.Idle_image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                                        120)
                else:
                    self.image.clip_composite_draw(int(self.frame) % 5 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                                   120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if self.attack == 1:
            if math.cos(self.face_dir) < 0:
                return sx - 88, sy - 40, sx + 47, sy + 30
            else:
                return sx - 47, sy - 40, sx + 88, sy + 30
        else:
            if math.cos(self.face_dir) < 0:
                return sx - 38, sy - 40, sx + 47, sy + 30
            else:
                return sx - 47, sy - 40, sx + 38, sy + 30


    def handle_collision(self, other, group):
        if group == 'skill:adj_monster':
            self.hit = 3

        if group == 'main_hero:adj_monster':
            pass

        if group == 'blocks_basic:adj_monster':
            self.y += round(2)

        if group== 'tree_node:adj_monster':
            self.y += round(2)

        if group== 'stone:adj_monster':
            self.y += round(2)

    def find_player(self):
        distance = (server.main_hero.x - self.x) ** 2 + (server.main_hero.y - self.y) ** 2
        if distance <= (PIXEL_PER_METER * 4) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = 0.5
        self.face_dir = math.atan2(server.main_hero.y - self.y, server.main_hero.x - self.x)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # fill here
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        self.bt = BehaviorTree(chase_node)


class King_Frog:
    image = None

    def __init__(self, x, y):
        if King_Frog.image == None:
            King_Frog.image = load_image('Resource/MON/King_Frog/King_Walk.png')
        self.Idle_image = load_image('Resource/MON/King_Frog/King_Idle.png')
        self.Attack_image = load_image('Resource/MON/King_Frog/King_Attack.png')
        self.Death_image = load_image('Resource/MON/King_Frog/King_Death.png')

        self.dead_sound = load_wav('Monster_dead.mp3')
        self.dead_sound.set_volume(40)
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0
        self.attack_frame = 0
        self.hp = 250
        self.attack = 0

        self.hit = 0
        self.dead = 0

        self.build_behavior_tree()
        self.face_dir = 1
        self.speed = 0

        self.timer = 2

    def update(self):
        if self.speed == 0:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.attack_frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.face_dir)
        self.y += round(-1.5)

        if self.y <= 80:
            self.y = 80

        if self.hit == 1:
            self.hp -= 2
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 1
            else:
                self.x += 1

        if self.hit == 2:
            self.hp -= 2
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 1
            else:
                self.x += 1

        if self.hit == 3:
            self.hp -= 1
            self.hit = 0

            if server.main_hero.face_dir == -1:
                self.x -= 0.3
            else:
                self.x += 0.3

        if self.hp <= 0:
            self.dead_sound.play()
            self.dead = 1
            self.timer += 1
            self.speed = 0
            server.main_hero.hit = 0

            if self.timer == 150:
                game_world.remove_object(self)
                self.timer = 0

        if self.hp > 0 :
            self.dead = 0

        if server.main_hero.skill == 1:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                if self.get_bb()[0] < server.main_hero.x + 65 - server.first_stage.window_left < self.get_bb()[2] :
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom < self.get_bb()[3] :
                        self.hit = 1
            else:
                if self.get_bb()[0] < server.main_hero.x - 65 - server.first_stage.window_left < self.get_bb()[2] :
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom< self.get_bb()[3]:
                        self.hit = 1

        elif server.main_hero.skill == 2:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                # draw_rectangle(self.x - 40, self.y - 37, self.x + 75, self.y + 8)
                if self.get_bb()[0] < server.main_hero.x + 55 - server.first_stage.window_left < self.get_bb()[2]:
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom < self.get_bb()[3]:
                        self.hit = 2
            else:
                if self.get_bb()[0] < server.main_hero.x - 55 - server.first_stage.window_left< self.get_bb()[2]:
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom< self.get_bb()[3]:
                        self.hit = 2

        distance2 = (server.main_hero.x - self.x) ** 2 + (server.main_hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 4) ** 2:
            self.attack = 1
            self.speed = 0
        else:
            self.attack = 0

        self.bt.run()


    def draw(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom

        if self.attack == 1:
            if math.cos(self.face_dir) < 0:
                self.Attack_image.clip_draw(int(self.attack_frame) % 4 * 150, 0, 150, 100, sx, sy, 200, 120)

            else:
                self.Attack_image.clip_composite_draw(int(self.attack_frame) % 4 * 150, 0, 150, 100, 0, 'h', sx, sy, 200, 120)

        elif self.dead == 1:
            if math.cos(self.face_dir) < 0:
                self.Death_image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, sx, sy, 120, 120)

            else:
                self.Death_image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                                         120)
        else:
            if math.cos(self.face_dir) < 0:  # 오른쪽을 바라보고 있는 상태
                if self.speed == 0:
                    self.Idle_image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, sx, sy, 120,120)
                else:
                    self.image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 120, 120)
            else:
                if self.speed == 0:
                    self.Idle_image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                                        120)
                else:
                    self.image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                                   120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if self.attack == 1:
            if math.cos(self.face_dir) < 0:
                return sx - 85, sy - 45, sx + 35, sy + 50
            else:
                return sx - 45, sy - 45, sx + 85, sy + 50
        else:
            if math.cos(self.face_dir) < 0:
                return sx - 45, sy - 45, sx + 35, sy + 50
            else:
                return sx - 45, sy - 45, sx + 35, sy + 50

    def handle_collision(self, other, group):
        if group == 'skill:King_monster':
            self.hit = 3

        if group == 'main_hero:King_monster':
            pass

        if group == 'blocks_basic:King_monster':
            self.y += round(2)

        if group == 'tree_node:King_monster':
            self.y += round(2)

        if group == 'stone:King_monster':
            self.y += round(2)

    def find_player(self):
        distance = (server.main_hero.x - self.x) ** 2 + (server.main_hero.y - self.y) ** 2
        if distance <= (PIXEL_PER_METER * 5) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = 0.3
        self.face_dir = math.atan2(server.main_hero.y - self.y, server.main_hero.x - self.x)
        return BehaviorTree.SUCCESS  # 일단 소년 쪽으로 움직이기만 해도 성공으로 간주

    def build_behavior_tree(self):

        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        self.bt = BehaviorTree(chase_node)


class Monster:
    image = None

    def __init__(self, x, y):
        if Monster.image == None:
            Monster.image = load_image('Resource/MON/Monster/Monster_Idle.png')
        self.Walk_image = load_image('Resource/MON/Monster/Monster_Walk.png')
        self.dead_sound = load_wav('Monster_dead.mp3')
        self.dead_sound.set_volume(40)
        self.x, self.y = x, y
        self.ax, self.ay = x, y
        self.frame = 0
        self.hp = 320

        self.build_behavior_tree()
        self.face_dir = 1
        self.speed = 0

        self.hit = 0
        self.dead = 0
        self.timer = 0

    def update(self):
        if self.speed == 0:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.face_dir)
        self.y += round(-1.5)

        if self.y <= 80:
            self.y = 80

        if self.y <= 80:
            self.y = 80

        if self.hit == 1:
            self.hp -= 3
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 1
            else:
                self.x += 1

        if self.hit == 2:
            self.hp -= 3
            self.hit = 0
            if server.main_hero.face_dir == -1:
                self.x -= 1
            else:
                self.x += 1

        if self.hit == 3:
            self.hp -= 0.8
            self.hit = 0

            if server.main_hero.face_dir == -1:
                self.x -= 0.1
            else:
                self.x += 0.1

        if self.hp <= 0:
            self.dead_sound.play()
            self.dead = 1
            self.timer += 1
            self.speed = 0
            server.main_hero.hit = 0
            game_world.remove_object(self)

        if server.main_hero.skill == 1:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                if self.get_bb()[0] < server.main_hero.x + 65 - server.first_stage.window_left < self.get_bb()[2] :
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom < self.get_bb()[3] :
                        game_world.remove_object(self)
            else:
                if self.get_bb()[0] < server.main_hero.x - 65 - server.first_stage.window_left < self.get_bb()[2] :
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom< self.get_bb()[3]:
                        game_world.remove_object(self)

        elif server.main_hero.skill == 2:
            if server.main_hero.face_dir == 1 or server.main_hero.dir == 1:
                # draw_rectangle(self.x - 40, self.y - 37, self.x + 75, self.y + 8)
                if self.get_bb()[0] < server.main_hero.x + 55 - server.first_stage.window_left < self.get_bb()[2]:
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom < self.get_bb()[3]:
                        game_world.remove_object(self)
            else:
                if self.get_bb()[0] < server.main_hero.x - 55 - server.first_stage.window_left< self.get_bb()[2]:
                    if self.get_bb()[1] < server.main_hero.y - 20 - server.first_stage.window_bottom< self.get_bb()[3]:
                        game_world.remove_object(self)
        self.bt.run()


    def draw(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if math.cos(self.face_dir) < 0:  # 오른쪽을 바라보고 있는 상태
            if self.speed == 0:
                self.image.clip_draw(int(self.frame) % 4 * 100, 0, 100, 100, sx, sy, 120,120)
            else:
                self.Walk_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 120,120)

        else:
            if self.speed == 0:
                self.image.clip_composite_draw(int(self.frame) % 4 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                               120)
            else:
                self.Walk_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 120,
                                               120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if math.cos(self.face_dir) < 0:
            return sx - 35, sy - 47, sx + 39, sy + 50
        else:
            return sx - 35, sy - 47, sx + 39, sy + 50

    def handle_collision(self, other, group):
        if group == 'skill:Mon_Monster':
            self.hit = 3

        if group == 'main_hero:Mon_Monster':
            pass

        if group == 'blocks_basic:Mon_Monster':
            self.y += round(2)

        if group == 'tree_node:Mon_Monster':
            self.y += round(2)

        if group == 'stone:Mon_Monster':
            self.y += round(2)

    def find_player(self):
        distance = (server.main_hero.x - self.x) ** 2 + (server.main_hero.y - self.y) ** 2
        if distance <= (PIXEL_PER_METER * 3) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = 0.2
        self.face_dir = math.atan2(server.main_hero.y - self.y, server.main_hero.x - self.x)
        return BehaviorTree.SUCCESS  # 일단 소년 쪽으로 움직이기만 해도 성공으로 간주

    def build_behavior_tree(self):

        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        self.bt = BehaviorTree(chase_node)
