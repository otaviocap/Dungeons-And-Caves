import pygame
from Sounds import Sound

class menuButton:

    def __init__(self, menu, x, y, text='', key='', group=''):
        self.menu = menu
        self.key = key
        self.group = group
        exec('self.menu.'+group+'.append(self)')
        self.text = text
        self.images = [self.menu.images[7], self.menu.images[9]]
        self.renderImage = self.images[0]
        self.x = x
        self.y = y
        self.w = self.images[0].get_rect().size[0]
        self.h = self.images[0].get_rect().size[1]
        self.rect = self.images[0].get_rect()
        self.clicked = False
        self.selected = False
        self.cooldown = 0
        self.helper = False

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x + self.w > self.mouse[0] > self.x and self.y + self.h > self.mouse[1] > self.y:
            self.setSelected(True)
            if self.cooldown <= 0:
                if self.isClicked():
                    self.menu.sound.playSfx(0)
                    self.disarmOthers()
                    self.clicked = not self.clicked
                    exec('self.menu.'+self.key+'Page()')
                    self.cooldown = 10
                    print('self.menu.'+self.key+'Page()')
                    self.helper = True
        else:
            self.setSelected(False)
            if self.key == 'options' and self.helper:
                print('sad')
                self.menu.data.updateParameter('difficulty', self.menu.difficulty('return'))
                self.helper = False

        if self.selected or self.clicked:
            self.renderImage = self.images[1]
        else:
            self.renderImage = self.images[0]
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

    def setSelected(self, bool):
        if bool:
            self.selected = bool
        else:
            self.selected = bool

    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def disarmOthers(self):
        for key in self.menu.menuPage.keys():
            if key != self.key:
                self.menu.menuPage[key] = False
        if self.group == 'menuButtons':
            for button in self.menu.menuButtons:
                if button != self:
                 button.clicked = False
        else:
            for button in self.menu.buttons:
                if button != self:
                 button.clicked = False

    def draw(self):
        self.menu.screen.blit(self.renderImage, (self.x, self.y))
        self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text)*7.5, self.rect.center[1] - 25))


class Slider:

    def __init__(self, menu, x, y, max, min, keyForPos=None):
        self.menu = menu
        self.max = max
        self.min = min
        self.x = x
        self.y = y
        self.images = [self.menu.images[12], self.menu.images[13]]
        self.rectBall = self.images[1].get_rect()
        self.rectSlide = self.images[0].get_rect()
        self.rectBall.x = self.x
        self.rectBall.y = self.y
        self.rectSlide.x = self.x
        self.rectSlide.y = self.y
        self.spawnX = x
        self.spawnY = y
        self.dragging = False
        self.menu.sliders.append(self)
        self.mouse = pygame.Rect(pygame.mouse.get_pos(), (30, 50))

    def update(self):
        self.mouse.x = pygame.mouse.get_pos()[0]
        self.mouse.y = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed()[0] and pygame.Rect.colliderect(self.rectBall, self.mouse):
            self.dragging = True
        else:
            self.dragging = False
        if self.dragging:
            if self.mouse[0] - self.spawnX >= -2 and self.mouse[0] - self.spawnX <= 255:
                self.rectBall.x = self.mouse[0]

    def getValue(self):
        return self.mapping(self.rectBall.x-self.spawnX, -2, 255, 0.0, 1.0)

    def draw(self):
        self.menu.screen.blit(self.images[0], (self.x, self.y))
        self.menu.screen.blit(self.images[1], (self.rectBall.x, self.rectBall.y - 5))
        # pygame.draw.rect(self.menu.screen, (255,255,255), (self.rectSlide.x, self.rectSlide.y, self.rectSlide.width, self.rectSlide.height))

    def mapping(self, x, inMin, inMax, outMin=None, outMax=None):
        if outMin == None and outMax == None:
            outMin, outMax = self.max, self.min
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin


class bigButton:

    def __init__(self, menu, x, y, images, text=''):
        self.menu = menu
        self.text = text
        self.images = [self.menu.images[2], self.menu.images[3]]
        self.menu.bigButtons.append(self)
        self.renderImage = self.images[0]
        self.addImage = []
        for i in images:
            a = pygame.image.load(i)
            a = pygame.transform.scale(a, (a.get_rect().width * 3, a.get_rect().height * 3))
            self.addImage.append(a)
        self.x = x
        self.y = y
        self.w = self.images[0].get_rect().size[0]
        self.h = self.images[0].get_rect().size[1]
        self.rect = self.images[0].get_rect()
        self.clicked = False
        self.selected = False
        self.cooldown = 0

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x + self.w > self.mouse[0] > self.x and self.y + self.h > self.mouse[1] > self.y:
            self.setSelected(True)
            if self.cooldown <= 0:
                if self.isClicked():
                    self.menu.sound.playSfx(0)
                    self.disarmOthers()
                    self.clicked = not self.clicked
                    self.cooldown = 10
        else:
            self.setSelected(False)

        if self.selected or self.clicked:
            self.renderImage = self.images[1]
        else:
            self.renderImage = self.images[0]
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

    def setSelected(self, bool):
        if bool:
            self.selected = bool
        else:
            self.selected = bool

    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def disarmOthers(self):
        for button in self.menu.bigButtons:
            if button != self:
                button.clicked = False

    def draw(self):
        self.menu.screen.blit(self.renderImage, (self.x, self.y))
        if len(self.addImage) == 2:
            self.menu.screen.blit(self.addImage[0], (self.x+25, self.y+40))
            self.menu.screen.blit(self.addImage[1], (self.x+75, self.y+40))
        elif len(self.addImage) == 1:
            self.menu.screen.blit(self.addImage[0], (self.x+45, self.y+40))
        self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text) * 7.5, self.rect.center[1] + 60))


class Button:

    def __init__(self, menu, x, y, action='', image=None, text=None, selectable=False):
        self.menu = menu
        self.action = action
        self.menu.buttons.append(self)
        self.text = text
        self.selectable = selectable
        if image == None:
            self.images = [self.menu.images[7], self.menu.images[9]]
        else:
            self.images = image
        self.renderImage = self.images[0]
        self.x = x
        self.y = y
        self.w = self.images[0].get_rect().size[0]
        self.h = self.images[0].get_rect().size[1]
        self.rect = self.images[0].get_rect()
        self.clicked = False
        self.selected = False
        self.cooldown = 0

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x + self.w > self.mouse[0] > self.x and self.y + self.h > self.mouse[1] > self.y:
            self.setSelected(True)
            if self.cooldown <= 0:
                if self.isClicked():
                    self.menu.sound.playSfx(0)
                    if self.selectable:
                        self.disarmOthers()
                        self.clicked = not self.clicked
                    exec(self.action)
                    self.cooldown = 10
        else:
            self.setSelected(False)

        if self.selected or self.clicked:
            self.renderImage = self.images[1]
        else:
            self.renderImage = self.images[0]
        if self.cooldown <= 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

    def setSelected(self, bool):
        if bool:
            self.selected = bool
        else:
            self.selected = bool

    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def disarmOthers(self):
        for button in self.menu.buttons:
            if button != self:
                button.clicked = False

    def draw(self):
        self.menu.screen.blit(self.renderImage, (self.x, self.y))
        if self.text != None:
            self.menu.screen.blit(self.menu.textGui.text(self.text, color=(28, 17, 23)), (self.rect.center[0] - len(self.text) * 7.5, self.rect.center[1] - 25))

