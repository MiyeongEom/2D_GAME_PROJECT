from pico2d import*

GAME_X = 1300
GAME_Y = 600

class StageOne:
    def __init__(self):
        self.stage1 = load_image('Resource/stage1_background.png')

    def draw(self):
        self.stage1.draw(GAME_X//2, GAME_Y//2)

    def update(self):
        pass
