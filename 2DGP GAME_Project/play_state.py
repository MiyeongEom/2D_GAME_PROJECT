from pico2d import*
import game_framework
import title_state
import logo_state

# 화면 크기
GAME_X = 1300
GAME_Y = 600

class Stage_ONE:
    def __init__(self):
        self.stage1 = load_image('stage1_background.png')

    def draw(self):
        self.stage1.draw(GAME_X//2, GAME_Y//2)

class Hero:
    frame = 0
    ground = True
    dir = 0
    dir2 = 1
    plus_move = 1
    action = 0

    def __init__(self):
        self.x = 100
        self.y = 75
        self.stand_image = load_image('MC_Idle.png')
        self.walking_image = load_image('MC_Walking.PNG')
        self.Attack01_image = load_image('MC_Attack01.png')
        # 592 102

    def update(self):
        self.left = self.x - 30
        self.right = self.x + 30
        self.top = self.y - 30
        self.bottom = self.y + 30
        self.frame = (self.frame + 1) % 6

        if self.dir == 1:
            self.x += 20
        elif self.dir == -1:
            self.x -= 20

        if self.dir != 0 and self.plus_move < 15:
            self.plus_move += 1
            if self.plus_move > 15:
                self.plus_move = 15

        elif self.dir == 0 and self.plus_move > 0:
            self.plus_move -= 2
            if self.plus_move < 0:
                self.plus_move = 0

        if self.dir != 0 and self.dir != self.dir2:
            self.plus_move = 0

        if self.x > 1260 and self.dir != -1:
            self.x = 1260

        elif self.x < 30 and self.dir != 1:
            self.x = 30

    def draw(self):
      # self.stand_image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y, 100, 100)
      # delay(0.15)

        if self.dir == 1:  # 오른쪽
            self.walking_image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y, 100, 100)

        elif self.dir == -1:  # 왼쪽
            self.walking_image.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', self.x, self.y, 100, 100)

        elif self.dir == 0 and self.dir2 == 1:
            self.stand_image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y, 100, 100)

        elif self.dir == 0 and self.dir2 == -1:
            self.stand_image.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', self.x, self.y, 100, 100)
        delay(0.15)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.change_state(title_state)
                case pico2d.SDLK_RIGHT:
                    main_hero.plus_move = 0
                    main_hero.dir2 = 1
                    main_hero.dir += 1

                case pico2d.SDLK_LEFT:
                    main_hero.plus_move = 0
                    main_hero.dir2 = -1
                    main_hero.dir -= 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:  # 오른쪽
                main_hero.dir -= 1
            elif event.key == SDLK_LEFT:  # 왼쪽
                main_hero.dir += 1
            elif event.key == SDLK_a:
                main_hero.action = 0


main_hero = None
stage1 = None
running = None

def enter():
    global stage1, running, main_hero
    stage1 = Stage_ONE()
    main_hero = Hero()
    running = True

# 게임 종료 - 객체 소멸
def exit():
    global stage1, main_hero
    del stage1
    del main_hero

#게임 객체 업데이트 - 게임 로직
def update():
    main_hero.update()
    pass

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def draw_world():
    stage1.draw()
    main_hero.draw()

def pause():
    pass

def resume():
    pass

def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas(GAME_X, GAME_Y)
    game_framework.run(this_module)
    pico2d.close_canvas()

if __name__ == '__main__': # 만약 단독 실행 상태이면,
    test_self()
