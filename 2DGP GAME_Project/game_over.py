import game_framework
from pico2d import *
import play_state
import title_state
import game_world

image = None


def enter():
    global image, font, font3
    image = load_image('Resource/Logo&Title/game_over.png')


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                #종료
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
                #시작화면
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
                #다시하기
                game_framework.change_state(play_state)
    pass

def exit():
    global image
    del image


def draw():
    clear_canvas()
    image.draw(650, 325)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass


class Music:
    def __init__(self):
        self.bgm = load_music('title.mp3')
        self.bgm.set_volume(40)
        self.bgm.repeat_play()

    def draw(self):
        pass

    def update(self):
        pass
