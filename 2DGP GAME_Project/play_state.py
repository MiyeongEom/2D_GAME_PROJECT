import random
import json
import os

from pico2d import*

import StageOne
import game_framework
import game_world

from StageOne import *
from Hero import Hero
from StageOne_Monster import *
import server


running = None
hero_position = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            server.main_hero.handle_event(event)

def enter():
    global running, hero_position

    running = True
    server.first_stage = StageOne()
    server.main_hero = Hero()
    hero_position = HeroPosition()
    #소개굴
    frog1 = Frog(580, 70)
    frog2 = Frog(40, 465)
    frog3 = Frog(1962, 70)
    frog4 = Frog(2050, 70)
    frog5 = Frog(2178, 70)
    frog6 = Frog(2356, 70)
    server.adj_monster = [frog1, frog2, frog3, frog4, frog5, frog6]

    #대개굴
    king_frog1= King_Frog(90, 315)
    king_frog2 = King_Frog(860, 80)
    king_frog3 = King_Frog(1900, 490)

    server.King_monster = [king_frog1, king_frog2, king_frog3]

    #큰몹
    monster1 =  Monster(1150, 470)
    monster2 = Monster(2220, 300)

    server.Mon_Monster = [monster1, monster2]

    #기본 블럭
    block01 = Block1(130, 250)
    block02 = Block1(310, 140)
    block03 = Block1(850, 300)
    block04 = Block1(1170, 400)
    block05 = Block1(1022, 180)
    block06 = Block1(1912, 420)
    block07 = Block1(1965, 160)
    block08 = Block1(2200, 230)

    server.blocks_basic = [block01, block02, block03, block04, block05, block06, block07, block08]

    #나무큐브
    block20 = Block2(350, 330)
    block21 = Block2(480, 330)
    block22 = Block2(610, 300)

    block23 = Block2(140, 400)
    block24 = Block2(85, 400)
    block25 = Block2(30, 400)

    block26 = Block2(690, 450)
    block27 = Block2(1347, 330)

    block19 = Block2(1800, 90)
    block18 = Block2(2390, 250)
    block17 = Block2(2290, 400)

    #계단
    block28 = Block2(1470, 70)

    block29 = Block2(1525, 70)
    block33 = Block2(1525, 124)

    block30 = Block2(1580, 70)
    block34 = Block2(1580, 124)
    block35 = Block2(1580, 178)

    block31 = Block2(1635, 70)
    block36 = Block2(1635, 124)
    block37 = Block2(1635, 178)
    block38 = Block2(1635, 232)

    block32 = Block2(1690, 70)
    block39 = Block2(1690, 124)
    block40 = Block2(1690, 178)
    block41 = Block2(1690, 232)
    block42 = Block2(1690, 286)



    server.tree_cube = [block17, block18 ,block19, block20, block21, block22, block23, block24, block25, block26, block27\
                        ,block28, block29, block30, block31, block32, block33, block34, block35\
                        ,block36, block37, block38, block39, block40, block41 ,block42]

    #벽돌
    block40 = Block3(690, 60)
    server.stone = [block40]


    spirit01 = Spirit(370, 220)
    spirit02 = Spirit(776, 90)
    spirit03 = Spirit(690, 530)
    spirit04 = Spirit(1230, 480)
    spirit05 = Spirit(30, 480)
    spirit06 = Spirit(1347, 410)
    spirit07 = Spirit(1985, 500)
    spirit08 = Spirit(1892, 90)
    spirit09 = Spirit(2390, 330)
    spirit10 = Spirit(2297, 480)


    server.spirit = [spirit01, spirit02, spirit03, spirit04, spirit05, spirit06, spirit07, spirit08, spirit09, spirit10]

########################################

    game_world.add_object(server.first_stage, 0)
    game_world.add_object(hero_position, 0)
    game_world.add_object(server.main_hero, 2)

    game_world.add_objects(server.adj_monster, 2)
    game_world.add_objects(server.King_monster, 2)
    game_world.add_objects(server.Mon_Monster, 2)

    game_world.add_objects(server.spirit, 1)
    game_world.add_objects(server.blocks_basic, 1)
    game_world.add_objects(server.tree_cube, 1)
    game_world.add_objects(server.stone, 1)


########################################

    # 블럭(배경장애물)과 주인공 충돌그룹
    game_world.add_collision_group(server.blocks_basic, server.main_hero, 'blocks_basic:main_hero')
    game_world.add_collision_group(server.tree_cube, server.main_hero, 'tree_node:main_hero')
    game_world.add_collision_group(server.stone, server.main_hero, 'stone:main_hero')

    # 블럭과 스틸 충돌 시 스킬 삭제
    game_world.add_collision_group(None, server.blocks_basic, 'skill:blocks_basic')
    game_world.add_collision_group(None, server.tree_cube, 'skill:tree_node')
    game_world.add_collision_group(None, server.stone, 'skill:stone')

    # 스킬과 몬스터 충돌
    game_world.add_collision_group(None, server.Mon_Monster, 'skill:Mon_Monster')
    game_world.add_collision_group(None, server.adj_monster, 'skill:adj_monster')
    game_world.add_collision_group(None, server.King_monster, 'skill:King_monster')

    # 영혼과 주인공 충돌
    game_world.add_collision_group(server.spirit, server.main_hero, 'spirit:main_hero')

    # 주인공과 몬스터 충돌
    game_world.add_collision_group(server.main_hero, server.adj_monster, 'main_hero:adj_monster')

    # 블럭과 몬스터 충돌
    game_world.add_collision_group(server.blocks_basic, server.adj_monster, 'blocks_basic:adj_monster')
    game_world.add_collision_group(server.tree_cube, server.adj_monster, 'tree_node:adj_monster')
    game_world.add_collision_group(server.stone, server.adj_monster, 'stone:adj_monster')

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

    pico2d.open_canvas(1200, 650)
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
