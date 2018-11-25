import pygame

class Chest(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.game = game
        self.game.chests.add(self)
        self.getStates()

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.players, False):
            pass

    def openChest(self):
        pass

    def getStates(self):
        self.chestStates = []
        pos =[-16,0]
        for i in range(6):
            if i % 2 == 0:
                pos[1] += 16
            else:
                pos[0] += 16
            self.chestStates.append(self.heartImg.subsurface(pos, (16, 16)))



