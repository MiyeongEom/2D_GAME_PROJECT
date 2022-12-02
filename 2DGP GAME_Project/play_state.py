import random
import json
import os

from pico2d import*
import game_framework
import game_world

from StageOne import *
from Hero import Hero
from StageOne_Monster import *


main_hero = None
first_stage = None
running = None
adj_monster, King_monster,  Mon_Monster  = None, None, None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            main_hero.handle_event(event)

def enter():
    global main_hero, adj_monster, running

    running = True
    first_stage = StageOne()
    main_hero = Hero()
    adj_monster = Frog(570, 80)
    King_monster = King_Frog(90, 305)
    Mon_Monster = Monster(1150, 370)

# (130, 240), (410, 140), (900, 300)
    block01 = Block1(130, 240)
    block02 = Block1(310, 140)
    block03 = Block1(850, 200)
    block04 = Block1(1100, 300)

    blocks_basic = [block01, block02, block03, block04]

# (410, 330), (540, 330), (670, 300)
    block20 = Block2(350, 330)
    block21 = Block2(480, 330)
    block22 = Block2(610, 300)

    tree_cube = [block20, block21, block22]

# (750, 60), (750, 100), (750, 140), (750, 180), (750, 220)

    block40 = Block3(690, 60)
    block41 = Block3(690, 100)
    block42 = Block3(690, 140)
    block43 = Block3(690, 180)
    block44 = Block3(690, 220)

    stone = [block40, block41, block42, block43, block44]


    spirit01 = Spirit(370, 220)
    spirit02 = Spirit(610, 382)

    spirit = [spirit01, spirit02]

########################################

    game_world.add_object(first_stage, 0)
    game_world.add_object(main_hero, 2)
    game_world.add_object(adj_monster, 2)
    game_world.add_object(King_monster, 2)
    game_world.add_object(Mon_Monster, 2)

    game_world.add_objects(spirit, 1)
    game_world.add_objects(blocks_basic, 1)
    game_world.add_objects(tree_cube, 1)
    game_world.add_objects(stone, 1)

########################################

    game_world.add_collision_group(blocks_basic, None, 'blocks_basic:main_hero')
    game_world.add_collision_group(None, main_hero, 'blocks_basic:main_hero')
    game_world.add_collision_group(tree_cube, main_hero, 'tree_node:main_hero')
    game_world.add_collision_group(stone, main_hero, 'stone:main_hero')
    game_world.add_collision_group(spirit, main_hero, 'spirit:main_hero')


# 게임 종료 - 객체 소멸
def exit():
    game_world.clear()

#게임 객체 업데이트 - 게임 로직
def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            #print('COLLISION by', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)



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

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb : return False
    if ra < lb : return False
    if ta < bb : return False
    if ba > tb : return False

    return True

def test_self():
    import play_state

    pico2d.open_canvas(1200, 600)
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
