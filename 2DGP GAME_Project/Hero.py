from pico2d import*
import game_framework
import game_world

RD, LD, RU, LU, DD, DQ, DW, DE = range(8)
event_name =  ['RD', 'LD', 'RU', 'LU', 'DD', 'DQ', 'DW', 'DE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT) : RD,
    (SDL_KEYDOWN, SDLK_LEFT) : LD,
    (SDL_KEYUP, SDLK_RIGHT) : RU,
    (SDL_KEYUP, SDLK_LEFT) : LU,

    (SDL_KEYDOWN, SDLK_DOWN) : DD, #구르기

    (SDL_KEYDOWN, SDLK_q) : DQ,
    (SDL_KEYDOWN, SDLK_w) : DW,
    (SDL_KEYDOWN, SDLK_e) : DE,

}

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 0.9 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5
VELOCITY = 135
MASS = 0.005

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
        print('ENTER IDLE')
        self.dir = 0
        pass

    @staticmethod
    def exit(self, event):
        print('EXIT RUN')
        pass

    @staticmethod
    def do(self): #움직일 수 있도록 프레임 증가
        self.frame = (self.frame + 2.5 * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.jump()
        pass

    @staticmethod
    def draw(self):
        if self.face_dir == 1: #오른쪽을 바라보고 있는 상태
            self.Idle_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, self.x, self.y, 150, 150)
        else: #왼쪽
            self.Idle_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 150, 150)
        pass

class RUN:
    def enter(self, event):
        Set_Speed(0.5, 6)
        print('ENTER RUN')

        if event == RD: self.dir += 1
        elif event == LD: self.dir -= 1
        elif event == RU: self.dir -= 1
        elif event == LU: self.dir += 1

    def exit(self, event):
        print('EXIT EXIT')
        self.face_dir = self.dir

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(40, self.x, 1260) #x값을 0과 800사이로 제한
        self.jump()

    def draw(self):  #int(boy.frame)
         if self.dir == 1:
            self.RUN_image.clip_draw(int(self.frame) % 5 * 100, 0, 100, 100, self.x, self.y, 150, 150)
         elif self.dir == -1:
            self.RUN_image.clip_composite_draw(int(self.frame) % 5 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 150, 150)


class Roll:
    def enter(self, event):
        Set_Speed(1.5, 6)
        print('ENTER Roll')
        # self.dir을 결정해야 함.
        # 왜? : 아이들에서 런 상태가 되었을 때 아이들에서 나올 떄 왼쪽키를 눌렀는지 혹은 오른쪽 키를 눌렀는지에 의해 판단됨
        # 따라서 셀프 뿐만 아니라 이벤트도 같이 전달되어야 함, 이것을 아이들도 맞춰줘야함

    def exit(self, event):
        print('EXIT Roll')
        # run을 나가서 idle로 갈 때 run의 방향을 알려줄 필요가 있다.
        self.face_dir = self.dir

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(40, self.x, 1260) #x값을 0과 800사이로 제한

    def draw(self):  #int(boy.frame)
         if self.dir == 1:
            self.Roll_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, self.x, self.y, 190, 190)
         elif self.dir == -1:
            self.Roll_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 190, 190)

class Attack:
    def enter(self, event):
        Set_Speed(0.5, 6)
        print('ENTER Attack')
        if event == DQ :
            self.skill = 1
        elif event == DW :
            self.skill = 2
        elif event == DE :
            self.skill = 3

    def exit(self, event):
        print('EXIT Attack')
        self.face_dir = self.dir

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        self.x = clamp(40, self.x, 1260) #x값을 0과 800사이로 제한

    def draw(self):  #int(boy.frame)
         if self.dir == 1:
            self.AttackQ_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, self.x, self.y, 190, 190)
         elif self.dir == -1:
            self.AttackQ_image.clip_composite_draw(int(self.frame) % 6 * 100, 0, 100, 100, 0, 'h', self.x, self.y, 190, 190)


next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, DD: IDLE, DQ: Attack},
    RUN: {RU: IDLE, LU: IDLE, LD: IDLE, RD: IDLE, DD: Roll, DQ: Attack},
    Roll: {RU: IDLE, LU: IDLE, LD: IDLE, RD: IDLE, DD: Roll, DQ: Roll},
    Attack: {RU: IDLE, LU: IDLE, LD: IDLE, RD: IDLE, DD: Roll, DQ: Attack}
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
        self.x, self.y = 40, 83
        self.v, self.m = VELOCITY, MASS
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.isJump = 0
        self.skill  = 0   # 1 : q , 2: w, 3: e
        self.damage = 0
        self.skill_time = 0
        self.jump_high = 90

        self.Idle_image = load_image('Resource/MC/MC_Idle.png')
        self.RUN_image = load_image('Resource/MC/MC_Run.png')
        self.Roll_image = load_image('resource/MC/MC_Roll.png')
        self.Jump_image = load_image('resource/MC/MC_JUMP.png')
        self.AttackQ_image = load_image('resource/MC/MC_AttackQ.png')

        self.q = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None) # 맨처음에는 이벤트가 없었기에

    def update(self):
        self.cur_state.do(self)
        if self.q : #q에 뭔가 들어있다면,
            event = self.q.pop() # 이벤트를 가져오고
            self.cur_state.exit(self, event) #현재 상태를 나가고, self에 대한 정보는 전달해주고 ^^
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__} Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())


    def jump(self):
        if self.isJump == 1:
            if self.v > 0:
                F = ((RUN_SPEED_PPS * game_framework.frame_time / 20) * self.m * (self.v ** 2))
            else:
                F = -((RUN_SPEED_PPS * game_framework.frame_time / 40) * self.m * (self.v ** 2))

            self.y += round(F)
            self.v -= 1

            if self.y < self.jump_high:
                self.y = self.jump_high
                self.v = VELOCITY
                self.isJump = 0


    def handle_event(self, event):  # 주인공이 스스로 이벤트를 처리할 수 있게
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)  # 변환된 내부 이벤트를 큐에 추가
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.isJump == 0:
                self.cur_state.exit(self, event)
                self.isJump = 1

    def Stop(self):
        if self.face_dir == 1:
            self.dir -= 1
        elif self.face_dir == -1:
            self.dir += 1

    def get_bb(self):
        if self.cur_state == RUN:
            if self.dir == 1:
                return self.x - 45, self.y - 50, self.x + 35, self.y + 43
            elif self.dir == -1:
                return self.x - 35, self.y - 50, self.x + 45, self.y + 43

        elif self.cur_state == Roll:
            if self.dir == 1:
                return self.x - 40, self.y - 60, self.x + 30, self.y + 15
            elif self.dir == -1:
                return self.x - 35, self.y - 60, self.x + 40, self.y + 15

        else:
            if self.face_dir == 1:
                return self.x - 36, self.y - 53, self.x + 25, self.y + 37
            elif self.face_dir == -1:
                return self.x - 25, self.y - 53, self.x + 36, self.y + 37

    def handle_collision(self, other, group):
        if group == 'block_basic:main_hero':
            Hero.Stop(self)
            pass