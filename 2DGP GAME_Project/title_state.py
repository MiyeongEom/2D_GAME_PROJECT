import game_framework
from pico2d import *

import game_world
import play_state

image = None
music = None

def enter():
    global image, music
    image = load_image('Resource/Logo&Title/title.png')
    music = load_music('title.mp3')
    music.set_volume(53)
    music.repeat_play()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(play_state)
    pass

def exit():
    global image, music
    del image
    pass

def draw():
    clear_canvas()
    image.draw(600, 325)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass



