from pico2d import*
import game_framework
from Skill import SkillE
import game_world
import server
import game_over

RD, LD, RU, LU, DD = range(5)
event_name =  ['RD', 'LD', 'RU', 'LU', 'DD']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT) : RD,
    (SDL_KEYDOWN, SDLK_LEFT) : LD,
    (SDL_KEYUP, SDLK_RIGHT) : RU,
    (SDL_KEYUP, SDLK_LEFT) : LU,

    (SDL_KEYDOWN, SDLK_DOWN) : DD, #구르기
}

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 0.9 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5
VELOCITY = 150
MASS = 0.005

PIXEL_PER_METER = (10.0 / 0.4)
RUN_SPEED_KMPH = 1.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ATTACK = 0.3
ATTACK_PER_TIME = 0.6 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 6

TIME_PER_DEFEND = 2
DEFEND_PER_TIME = 2 / TIME_PER_DEFEND
FRAMES_PER_DEFEND = 1

TIME_PER_ANIMATION = 0.3
ANIMATION_PER_TIME = 0.6 / TIME_PER_ANIMATION
FRAMES_PER_ANIMATION = 9

TIME_PER_ANIMATION2 = 0.5
ANIMATION2_PER_TIME = 1.0 / TIME_PER_ANIMATION2
FRAMES_PER_ANIMATION2 = 8

TIME_PER_ANIMATION3 = 10.0
ANIMATION3_PER_TIME = 8.0 / TIME_PER_ANIMATION3
FRAMES_PER_ANIMATION3 = 8


def Set_Speed(time_per_action, frames_per_action):
    global FRAMES_PER_ACTION
    global TIME_PER_ACTION
    global ACTION_PER_TIME
    TIME_PER_ACTION = time_per_action
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = frames_per_action


class IDLE:
    @staticmethod
    def enter(self, event):
        Set_Speed(1, 6)
        self.dir = 0
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self): #움직일 수 있도록 프레임 증가
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.jump()
        self.attackq()
        self.attackw()
        self.attacke()
        self.defend()

        self.y = clamp(90, self.y, server.first_stage.h - 1 - 45)
        if self.isJump == 0 :
            self.y += round(-2)
            if self.y < self.jump_high :
                self.y = self.jump_high

        pass

    @staticmethod
    def draw(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if self.face_dir == 1: #오른쪽을 바라보고 있는 상태
            self.Idle_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 150, 150)
        else: #왼쪽
            self.Idle_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 150, 150)
        pass

class RUN:
    def enter(self, event):
        Set_Speed(0.5, 6)

        if event == RD: self.dir += 1
        elif event == LD: self.dir -= 1
        elif event == RU: self.dir -= 1
        elif event == LU: self.dir += 1
        if self.dir != 0:
            self.face_dir = self.dir

    def exit(self, event):
        pass


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(40, self.x, 2470)
        self.y = clamp(90, self.y, server.first_stage.h - 1 - 45)

        self.jump()
        self.attackq()
        self.attackw()
        self.attacke()
        self.defend()

    def draw(self):  #int(boy.frame)
         sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
         if self.dir == 1:
            self.RUN_image.clip_draw(int(self.frame) % 5 * 100, 0, 100, 100, sx, sy, 150, 150)
         elif self.dir == -1:
            self.RUN_image.clip_composite_draw(int(self.frame) % 5 * 100, 0, 100, 100, 0, 'h', sx, sy, 150, 150)

class Roll:
    def enter(self, event):
        Set_Speed(1.5, 6)
        # self.dir을 결정해야 함.
        # 왜? : 아이들에서 런 상태가 되었을 때 아이들에서 나올 떄 왼쪽키를 눌렀는지 혹은 오른쪽 키를 눌렀는지에 의해 판단됨
        # 따라서 셀프 뿐만 아니라 이벤트도 같이 전달되어야 함, 이것을 아이들도 맞춰줘야함

    def exit(self, event):
        pass


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(40, self.x, 2470)
        self.y = clamp(90, self.y, server.first_stage.h - 1 - 45)

    def draw(self):  #int(boy.frame)
         sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
         if self.dir == 1:
            self.Roll_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
         elif self.dir == -1:
            self.Roll_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 190, 190)


next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, DD: IDLE},
    RUN: {RU: IDLE, LU: IDLE, LD: IDLE, RD: IDLE, DD: Roll},
    Roll: {RU: IDLE, LU: IDLE, LD: IDLE, RD: IDLE, DD: Roll}
}

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KPH = 30
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Hero:
    def add_event(self, event):
        self.q.insert(0, event)

    def __init__(self):
        # 원래 40 90
        self.x = 40
        self.y = 90
        self.v, self.m = VELOCITY, MASS
        self.frame = 0
        self.aniframe = 0
        self.dir, self.face_dir = 0, 1
        self.collision = 0
        self.score = 0

        self.hp = 200
        self.dead = 0
        self.timer = 0
        self.hit = 0

        self.isJump = 0
        self.jump_high = 90
        self.jump_value = 0

        self.attacking = False
        self.skill  = 0   # 1 : q, 2: w, 3: e
        self.damage = 0
        self.skill_time = 0
        self.skill_q = 3

        self.Idle_image = load_image('Resource/MC/MC_Idle.png')
        self.RUN_image = load_image('Resource/MC/MC_Run.png')
        self.Roll_image = load_image('Resource/MC/MC_Roll.png')
        self.Jump_image = load_image('Resource/MC/MC_JUMP.png')
        self.AttackQ_image = load_image('Resource/MC/MC_AttackQ.png')
        self.AttackW_image = load_image('Resource/MC/MC_AttackW.png')
        self.AttackE_image = load_image('Resource/MC/MC_FUN.png')
        self.Defend_image = load_image('Resource/MC/MC_Defend.png')
        self.Dead_image = load_image('Resource/MC/MC_Death.png')

        #################################################################

        self.QEffect_image = load_image('Resource/Effect/Q_Effect01.png')
        self.WEffect_image = load_image('Resource/Effect/W_Effect01.png')
        self.EEffect02_image = load_image('Resource/Effect/E_Effect02.png')

        self.DEffect_image = load_image('Resource/Effect/D_Effect.png')

        self.font = load_font('Font/Galmuri11-Bold.ttf', 28)
        self.font2 = load_font('Font/Galmuri7.ttf', 20)
        self.font3 = load_font('Font/Galmuri11-Bold.ttf', 100)

        self.q = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None) # 맨처음에는 이벤트가 없었기에

    def update(self):
        self.cur_state.do(self)
        self.x = clamp(40, self.x, server.first_stage.w - 1 - 40)
        self.y = clamp(90, self.y, server.first_stage.h - 1 - 45)
        if self.q : #q에 뭔가 들어있다면,
            event = self.q.pop() # 이벤트를 가져오고
            self.cur_state.exit(self, event) #현재 상태를 나가고, self에 대한 정보는 전달해주고 ^^
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__} Event {event_name[event]}')
            self.cur_state.enter(self, event)

        #print(self.hp)

        if self.hit == 1:
            self.hp -= 0.2
            self.hit = 0

        if self.hit == 2:
            self.hp -= 0.4
            self.hit = 0

        if self.hit == 3:
            self.hp -= 0.6
            self.hit = 0

        if self.hp > 0 :
            self.dead = 0

        if self.hp <= 0:
            self.dead = 1
            self.timer += 1
            if self.timer == 75:
                delay(2)
                game_framework.change_state(game_over)

        if self.dead == 1:
            self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 6

        else :
            if self.skill == 1:
                self.frame =  (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 6
                self.aniframe = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 5

            elif self.skill == 2:
                self.frame =  (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 6
                self.aniframe = (self.frame + FRAMES_PER_ANIMATION * ANIMATION_PER_TIME * game_framework.frame_time) % 9

            elif self.skill == 3:
                self.frame =  (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 6
                self.aniframe = (self.frame + FRAMES_PER_ANIMATION2 * ANIMATION2_PER_TIME * game_framework.frame_time) % 8

            elif self.skill == 4:
                self.frame =  (self.frame + FRAMES_PER_DEFEND * DEFEND_PER_TIME * 2) % 12
                self.aniframe = (self.frame + FRAMES_PER_ANIMATION3 * ANIMATION3_PER_TIME * game_framework.frame_time) % 8

    def draw(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if self.skill == 1:
            if self.dir == 1:
                self.AttackQ_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.QEffect_image.clip_composite_draw(int(self.aniframe) % 5 * 100, 0, 100, 100, 0, 'h', sx + 25, sy, 150,150)
                draw_rectangle(sx, sy - 56, sx + 65, sy + 46)

            elif self.dir == -1:
                self.AttackQ_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 190,190)
                self.QEffect_image.clip_draw(int(self.aniframe) % 5 * 100, 0, 100, 100, sx - 25, sy, 150, 150)
                draw_rectangle(sx - 65, sy - 56, sx, sy + 46)

            elif self.face_dir == 1:
                self.AttackQ_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.QEffect_image.clip_composite_draw(int(self.aniframe) % 5 * 100, 0, 100, 100, 0, 'h', sx, sy , 150,150)
                draw_rectangle(sx, sy - 56, sx + 65, sy + 46)

            elif self.face_dir == -1:
                self.AttackQ_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 190, 190)
                self.QEffect_image.clip_draw(int(self.aniframe) % 5 * 100, 0, 100, 100, sx - 25, sy, 150, 150)
                draw_rectangle(sx - 65, sy - 56, sx, sy + 46)

        elif self.skill == 2:
            if self.dir == 1:
                self.AttackW_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.WEffect_image.clip_draw(int(self.aniframe) % 9 * 100, 0, 100, 100, sx + 5, sy+30, 150, 150)
                draw_rectangle(sx - 40, sy - 37, sx + 55, sy + 8)

            elif self.dir == -1:
                self.AttackW_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 190,
                                                    190)
                self.WEffect_image.clip_composite_draw(int(self.aniframe) % 9 * 100, 0, 100, 100, 0, 'h', sx -5, sy+30, 150, 150)
                draw_rectangle(sx - 55, sy - 37, sx + 40, sy + 8)

            elif self.face_dir == 1:
                self.AttackW_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.WEffect_image.clip_draw(int(self.aniframe) % 9 * 100, 0, 100, 100, sx + 5, sy + 30, 160, 160)
                draw_rectangle(sx - 40, sy - 37, sx + 55, sy + 8)

            elif self.face_dir == -1:
                self.AttackW_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h',sx, sy, 190,
                                                    190)
                self.WEffect_image.clip_composite_draw(int(self.aniframe) % 9 * 100, 0, 100, 100, 0, 'h', sx -5,
                                                       sy+30, 150, 150)
                draw_rectangle(sx - 55, sy - 37, sx + 40, sy + 8)

        elif self.skill == 3:
            if self.dir == 1:
                self.AttackE_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.EEffect02_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy , 200,
                                             200)

            elif self.dir == -1:
                self.AttackE_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy,
                                                       190,190)
                self.EEffect02_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy , 200,
                                              200)

            elif self.face_dir == 1:
                self.AttackE_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.EEffect02_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy, 200,
                                               200)

            elif self.face_dir == -1:
                self.AttackE_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy,
                                                       190,190)
                self.EEffect02_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy , 200,
                                               200)

        elif self.skill == 4:
            if self.dir == 1:
                self.Defend_image.clip_draw(int(self.frame) % 12 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.DEffect_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy-15, 100,
                                               100)
            elif self.dir == -1:
                self.Defend_image.clip_composite_draw(int(self.frame) % 12 * 100, 0, 100, 100, 0, 'h', sx, sy,
                                                       190, 190)
                self.DEffect_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy-15, 100,
                                             100)

            elif self.face_dir == 1:
                self.Defend_image.clip_draw(int(self.frame) % 12 * 100, 0, 100, 100, sx, sy, 190, 190)
                self.DEffect_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy-15, 100,
                                               100)

            elif self.face_dir == -1:
                self.Defend_image.clip_composite_draw(int(self.frame) % 12 * 100, 0, 100, 100, 0, 'h', sx, sy,
                                                       190,190)
                self.DEffect_image.clip_draw(int(self.aniframe) % 8 * 100, 0, 100, 100, sx, sy-15, 100,
                                             100)

        elif self.skill == 0 and self.dead == 0:
            self.cur_state.draw(self)

        if self.dead == 1:
            self.font3.draw(330, 325, 'GAME OVER', (255, 0, 0))
            if self.face_dir == 1:  # 오른쪽을 바라보고 있는 상태
                self.Dead_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, sx, sy, 150, 150)
            else:  # 왼쪽
                self.Dead_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', sx, sy, 150, 150)

        draw_rectangle(*self.get_bb())
        self.font.draw(980, 625, 'score : ', (255, 255, 200))
        self.font.draw(1100, 625, '%d / 10' % (self.score), (255, 255, 255))
        self.font2.draw(sx - 40, sy + 40, '(%d, %d)' % (self.x, self.y), (255, 255, 0))

    def jump(self):
        jump_value = 0.00349923324584
        if self.isJump == 1:
            if self.v > 0:
                F = ((RUN_SPEED_PPS * 0.00349923324584 / 40) * self.m * (self.v ** 2))
                self.y += round(F)
                self.v -= 1
            else:
                self.fall()

    def fall(self):
        if self.isJump == 1:
            F = -((RUN_SPEED_PPS * 0.00349923324584 / 40) * self.m * (self.v ** 2))
            self.y += round(F)
            self.v -= 1

            if self.y < self.jump_high:
                self.y = self.jump_high
                self.v = VELOCITY
                self.m = MASS
                self.isJump = 0

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.isJump == 0:
                self.cur_state.exit(self, event)
                self.skill = 0
                self.isJump = 1

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            if self.skill == 0:
                self.cur_state.exit(self, event)
                self.skill = 1

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            if self.skill == 0:
                self.cur_state.exit(self, event)
                self.skill = 2

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_e):
            if self.skill == 0:
                self.cur_state.exit(self, event)
                self.skill = 3

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            if self.skill == 0:
                self.cur_state.exit(self, event)
                self.skill = 4

    def attackq(self):
        if self.skill == 1:
            self.attacking = True
            self.skill_time += 1

            if self.skill_time == 120:
                self.attacking = False
                self.skill = 0
                self.skill_time = 0

    def attackw(self):
        if self.skill == 2:
            self.attacking = True
            self.skill_time += 1

            if self.skill_time == 140:
                self.attacking = False
                self.skill = 0
                self.skill_time = 0

    def attacke(self):
        if self.skill == 3:
            self.attacking = True
            self.skill_time += 1
            self.e_skill()

            if self.skill_time == 100:
                self.attacking = False
                self.skill = 0
                self.skill_time = 0

    def e_skill(self):
        if self.face_dir == 1 or self.dir == 1:
            skille = SkillE(self.x + 35, self.y, self.face_dir * 2)
        else:
            skille = SkillE(self.x - 35, self.y, self.face_dir * 2)
        game_world.add_object(skille, 1)
        game_world.add_collision_group(skille, None, 'skill:adj_monster')
        game_world.add_collision_group(skille, None, 'skill:King_monster')
        game_world.add_collision_group(skille, None, 'skill:Mon_Monster')
        game_world.add_collision_group(skille, None, 'skill:blocks_basic')
        game_world.add_collision_group(skille, None, 'skill:tree_node')
        game_world.add_collision_group(skille, None, 'skill:stone')

    def defend(self):
        if self.skill == 4:
            self.attacking = True
            self.skill_time += 1

            if self.skill_time == 150:  #1초
                self.attacking = False
                self.skill = 0
                self.skill_time = 0

    def get_bb(self):
        sx, sy = self.x - server.first_stage.window_left, self.y - server.first_stage.window_bottom
        if self.cur_state == RUN:
            if self.dir == 1:
                return sx - 27, sy - 46, sx + 28, sy + 40
            elif self.dir == -1:
                return sx - 28, sy - 46, sx + 27, sy + 40

        elif self.cur_state == Roll:
            if self.dir == 1:
                return sx - 27, sy - 46, sx + 28, sy + 10
            elif self.dir == -1:
                return sx - 25, sy - 46, sx + 27, sy + 10

        else:
            if self.face_dir == 1:
                return sx - 27, sy - 48, sx + 28, sy + 40
            elif self.face_dir == -1:
                return sx - 28, sy - 48, sx + 27, sy + 40
            return sx - 28, sy - 50, sx + 28, sy + 40

    def handle_collision(self, other, group): #other.get_bb()[1]
        if group == 'blocks_basic:main_hero':
            if self.get_bb()[1] < other.get_bb()[3] or self.get_bb()[3] < other.get_bb()[1]: #좌우
                if self.get_bb()[2] > other.get_bb()[0]:
                    self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
                elif self.get_bb()[0] > other.get_bb()[2]:
                    self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

            if other.get_bb()[3]+1 > self.get_bb()[3] > other.get_bb()[1]-1:
                self.fall()

            elif self.get_bb()[1] < other.get_bb()[3]:
                if other.get_bb()[0] < self.get_bb()[0] + 50 and self.get_bb()[2] - 50 < other.get_bb()[2]:
                    self.y += 2
                    self.v = VELOCITY
                    self.m = MASS
                    self.isJump = 0

        if group == 'tree_node:main_hero':
            if self.get_bb()[1] < other.get_bb()[3] or self.get_bb()[3] < other.get_bb()[1]: #좌우
                if self.get_bb()[2] > other.get_bb()[0]:
                    self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
                elif self.get_bb()[0] > other.get_bb()[2]:
                    self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

            if other.get_bb()[3]+1 > self.get_bb()[3] > other.get_bb()[1]-1:
                self.fall()

            elif self.get_bb()[1] < other.get_bb()[3]:
                if other.get_bb()[0] < self.get_bb()[0] + 50 and self.get_bb()[2] - 50 < other.get_bb()[2]:
                     self.y += 2
                     self.v = VELOCITY
                     self.m = MASS
                     self.isJump = 0

        if group == 'stone:main_hero':
            if self.get_bb()[1] < other.get_bb()[3] or self.get_bb()[3] < other.get_bb()[1]: #좌우
                if self.get_bb()[2] > other.get_bb()[0]:
                    self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
                elif self.get_bb()[0] > other.get_bb()[2]:
                    self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

            if other.get_bb()[3]+1 > self.get_bb()[3] > other.get_bb()[1]-1:
                self.fall()

            elif self.get_bb()[1] < other.get_bb()[3]:
                if other.get_bb()[0] < self.get_bb()[0] + 50 and self.get_bb()[2] - 50 < other.get_bb()[2]:
                    self.y += 2
                    self.v = VELOCITY
                    self.m = MASS
                    self.isJump = 0

        if group == 'spirit:main_hero':
            self.score += 1
            self.hp += 5

        if group == 'main_hero:adj_monster':
            self.hit = 1

        if group == 'main_hero:King_monster':
            self.hit = 2

        if group == 'main_hero:Mon_monster':
            self.hit = 3

        else:
            self.hp += 0




