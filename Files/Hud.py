import pygame


class Hud:

    def __init__(self, game):
        self.game = game
        self.heartImg = pygame.image.load('../Assets/heart.png')
        self.getStates()

    def getStates(self):
        self.heartStages = []
        self.heartStages.append(self.heartImg.subsurface((0, 0, 13, 12)))
        self.heartStages.append(self.heartImg.subsurface((16, 0, 13, 12)))
        self.heartStages.append(self.heartImg.subsurface((32, 0, 13, 12)))
        for i in range(3):
            self.heartStages[i] = pygame.transform.scale(self.heartStages[i], (26, 24))

    def draw(self):
        self.life = self.game.player.life
        self.fullHearts, self.halfHearts, self.emptyHearts, space = 0, 0, 0, 0
        for i in range(int(self.game.player.maxLife/2)):
            if self.life >= 2:
                self.fullHearts += 1
                self.life -= 2
            elif self.life >= 1:
                self.halfHearts += 1
                self.life -= 1
            else:
                self.emptyHearts += 1

        for _ in range(self.fullHearts):
            self.game.screen.blit(self.heartStages[0], (space, 0))
            space += 30
        for _ in range(self.halfHearts):
            self.game.screen.blit(self.heartStages[1], (space, 0))
            space += 30
        for _ in range(self.emptyHearts):
            self.game.screen.blit(self.heartStages[2], (space, 0))
            space += 30




