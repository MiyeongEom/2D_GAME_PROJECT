from pico2d import *
import game_world

class Attackq:
    image = None

    def __init__(self):
        if Attackq.image == None:
            Attackq.image = load_image('resource/MC_AttackQ.png')
        self.x, self.y = 40, 90

    def draw(self):
        self.Attackq_image.clip_draw(int(self.frame) % 6 * 100, 0, 100, 100, self.x, self.y, 150, 150)

    def update(self):
        pass