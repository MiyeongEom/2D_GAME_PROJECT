from pico2d import*
import game_framework
import title_state
import logo_state

from Stage_One import Stage_One
from Hero import Hero

main_hero = None
stage1 = None
running = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            main_hero.handle_event(event)

def enter():
    global stage1, main_hero, running
    stage1 = Stage_One()
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

def draw_world():
    stage1.draw()
    main_hero.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def test_self():
    import play_state

    pico2d.open_canvas(1300, 600)
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
