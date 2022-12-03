from pico2d import *
import game_framework
import game_world


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class SkillQ:
    image = None

    def __init__(self):
        if SkillQ.image == None:
            SkillQ.image = load_image('Resource/Effect/Q_Effect01.png')
        self.x, self.y = 40, 90
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        self.image.clip_draw(int(self.frame) % 5 * 100, 0, 100, 100, self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 55, self.x + 15, self.y + 10

    def handle_collision(self, other, group):
        pass