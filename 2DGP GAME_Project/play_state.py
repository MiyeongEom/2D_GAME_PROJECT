from pico2d import*
import game_framework
import game_world

from Stage_One import StageOne
from Hero import Hero

main_hero = None
first_stage = None
running = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            main_hero.handle_event(event)

def enter():
    global main_hero, running
    running = True
    first_stage = StageOne()
    main_hero = Hero()

    game_world.add_object(first_stage, 0)
    game_world.add_object(main_hero, 1)

# 게임 종료 - 객체 소멸
def exit():
    game_world.clear()

#게임 객체 업데이트 - 게임 로직
def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

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
