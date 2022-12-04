from pico2d import *
import game_framework
import game_world
import server

#W
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30
TIME_PER_ACTION = 0.125
ACTION_PER_TIME = 2.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class SkillE:
    image = None

    def __init__(self, x = 80, y = 100, velocity = 1):
        if  SkillE.image == None:
            SkillE.image = load_image('Resource/Effect/E_Effect01.png')
        self.x, self.y = x, y
        self.frame = 0
        self.velocity = velocity

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.velocity
        if self.x < server.main_hero.x - 150 or self.x > server.main_hero.x + 150:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(int(self.frame) % 8 * 100, 0, 100, 100, self.x , self.y, 40, 40)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 15

    def handle_collision(self, other, group):
        if group == 'skill:blocks_basic':
            game_world.remove_object(self)

        if group == 'skill:tree_node':
            game_world.remove_object(self)

        if group == 'skill:stone':
            game_world.remove_object(self)