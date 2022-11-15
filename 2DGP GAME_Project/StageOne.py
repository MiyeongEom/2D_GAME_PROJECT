from pico2d import*

GAME_X = 1300
GAME_Y = 600

class StageOne:
    def __init__(self):
        self.stage1 = load_image('Resource/StageOne/stage1_background.png')

    def draw(self):
        self.stage1.draw(GAME_X//2, GAME_Y//2)

    def update(self):
        pass

class Block:
    def __init__(self):
        self.block = load_image('Resource/StageOne/Block1.png')

    def draw(self):
        self.block.draw(200, 230, 194.4, 48)
        self.block.draw(420, 140, 194.4, 48)
        self.block.draw(900, 300, 194.4, 48)


    def update(self):
        pass


class Block2:
    def __init__(self):
        self.block = load_image('Resource/StageOne/Block2.png')

    def draw(self):
        self.block.draw(410, 330, 55, 54)
        self.block.draw(540, 330, 55, 54)
        self.block.draw(670, 330, 55, 54)

    def update(self):
        pass


class Block3:
    def __init__(self):
        self.block = load_image('Resource/StageOne/Block3.png')

    def draw(self):

        for i in [0, 1, 2, 3, 4]:
            self.block.draw(750, 60 + 40 * i, 40, 40)


    def update(self):
        pass