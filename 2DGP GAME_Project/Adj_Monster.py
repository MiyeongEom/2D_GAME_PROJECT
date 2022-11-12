from pico2d import *
import game_framework
import game_world

class Admon:

    def add_event(self, event):
        self.q.insert(0, event)

    def handle_event(self, event):
        pass

    def __init__(self):
        self.x, self.y = 200, 230
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.mon_image = load_image('MON_Frog.png')


    def update(self):
        self.frame = (self.frame + 1) % 6
        self.x += self.dir
        if (self.x >= self.x - 50):
            self.dir = -1
        elif (self.x <= self.x + 50):
            self.dir = 1

    def draw(self):

        if self.dir == 1:  # 오른쪽을 바라보고 있는 상태
            self.mon_image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y, 150, 150)
        elif self.dir == -1:
            self.mon_image.clip_composite_draw(self.frame * 100, 0, 100, 100, 0, 'h', self.x, self.y, 150,
                                                150)
