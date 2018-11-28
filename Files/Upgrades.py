import pygame
from textEngine import textGui
from random import randrange

class Upgrade(pygame.sprite.Sprite):

    def __init__(self, game, x, y, justImg=False):
        super().__init__()
        self.x = x
        self.y = y
        self.game = game
        self.spawnX = x
        self.spawnY = y
        self.image = pygame.image.load('../Assets/Items.png')
        self.getItems()
        self.itemType = 0#randrange(0, 26, 5)
        self.itemStrenght = randrange(0, 4, 1)
        self.itemImg = self.items[self.itemType + self.itemStrenght]
        self.rect = self.itemImg.get_rect()
        self.textGui = textGui()
        self.game.allUpgrades.add(self)
        self.makeText()
        self.rect.x = self.x
        self.rect.y = self.y
        self.actionDone = False
        self.justImg = justImg

    def getItems(self):
        self.items = []
        pos = [-16, 0]
        for i in range(35):
            if pos[0] == 64:
                pos[0] = 0
                pos[1] += 16
            else:
                pos[0] += 16
            self.items.append(self.image.subsurface(pos, (16, 16)))

    def makeText(self):
        if self.itemType == 0:
            self.text = 'New Magic:\n'
            if self.itemStrenght == 0:
                self.text += 'Wind Force\nYou can fly for 2 seconds\nCooldown: 10s'
            elif self.itemStrenght == 1:
                self.text += 'Burning Fire from Hell\nDamage is multiplied by 2 for 5 seconds\nCooldown: 30s'
            elif self.itemStrenght == 2:
                self.text += 'Drop of deep water\nInverse Knockback\nActivable'
            elif self.itemStrenght == 3:
                self.text += 'Light from Heaven\nEnemies life is reduced by 3\nCooldown: 45s'
            elif self.itemStrenght == 4:
                self.text += 'Darkest dark magic\nYour consume 1 heart to get +2 damage for 10 seconds\nCooldown: 30s'

        if self.itemType == 5:
            self.text = 'Defense UP:\n'
            if self.itemStrenght == 0:
                self.text += '+1'
            elif self.itemStrenght == 1:
                self.text += '+2'
            elif self.itemStrenght == 2:
                self.text += '+3'
            elif self.itemStrenght == 3:
                self.text += '+4'
            elif self.itemStrenght == 4:
                self.text += '+5'

        if self.itemType == 10:
            self.text = 'Total Life UP:\n'
            if self.itemStrenght == 0:
                self.text += '+1'
            elif self.itemStrenght == 1:
                self.text += '+2'
            elif self.itemStrenght == 2:
                self.text += '+3'
            elif self.itemStrenght == 3:
                self.text += '+4'
            elif self.itemStrenght == 4:
                self.text += '+5'

        if self.itemType == 15:
            self.text = 'DPS UP:\n'
            if self.itemStrenght == 0:
                self.text += '+1'
            elif self.itemStrenght == 1:
                self.text += '+2'
            elif self.itemStrenght == 2:
                self.text += '+3'
            elif self.itemStrenght == 3:
                self.text += '+4'
            elif self.itemStrenght == 4:
                self.text += '+5'

        if self.itemType == 20:
            self.text = 'Damage UP:\n'
            if self.itemStrenght == 0:
                self.text += '+1'
            elif self.itemStrenght == 1:
                self.text += '+2'
            elif self.itemStrenght == 2:
                self.text += '+3'
            elif self.itemStrenght == 3:
                self.text += '+4'
            elif self.itemStrenght == 4:
                self.text += '+5'

        if self.itemType == 25:
            self.text = 'Life:\n'
            if self.itemStrenght == 0:
                self.text += 'MAXED'
            elif self.itemStrenght == 1:
                self.text += '+1'
            elif self.itemStrenght == 2:
                self.text += '+2'
            elif self.itemStrenght == 3:
                self.text += '+3'
            elif self.itemStrenght == 4:
                self.text += '+4'

    def update(self):
        if not self.justImg:
            text = ''
            nText = 0
            textPos = 10
            for character in self.text:
                if character == "\n":
                    self.game.texts['Upgrade' + str(nText)] = (text, (self.x, self.y + textPos))
                    text = ''
                    nText += 1
                    textPos += 10
                else:
                    text += character
            self.game.texts['Upgrade'] = (text, (self.x, self.y+textPos))
            self.rect.y = self.y
            if self.y - self.spawnY > -50:
                self.y -= .5
            else:
                for i in range(nText):
                    self.game.texts.pop('Upgrade' + str(i))
                self.game.texts.pop('Upgrade')
                self.kill()
            if not self.justImg:
                self.itemAction()
        else:
            pass

    def itemAction(self):
        if not self.actionDone:
            self.actionDone = True
            item = self.itemType + self.itemStrenght
            if item == 0:
                for player in self.game.players.sprites():
                    player.setMagic(1)

            elif item == 1:
                for player in self.game.players.sprites():
                    player.setMagic(2)

            elif item == 2:
                for player in self.game.players.sprites():
                    player.setMagic(3)

            elif item == 3:
                for player in self.game.players.sprites():
                    player.setMagic(4)

            elif item == 4:
                for player in self.game.players.sprites():
                    player.setMagic(5)

            elif item == 5:
                for player in self.game.players.sprites():
                    player.defense += 1

            elif item == 6:
                for player in self.game.players.sprites():
                    player.defense += 2

            elif item == 7:
                for player in self.game.players.sprites():
                    player.defense += 3

            elif item == 8:
                for player in self.game.players.sprites():
                    player.defense += 4

            elif item == 9:
                for player in self.game.players.sprites():
                    player.defense += 5

            elif item == 10:
                for player in self.game.players.sprites():
                    player.maxLife += 1

            elif item == 11:
                for player in self.game.players.sprites():
                    player.maxLife += 2

            elif item == 12:
                for player in self.game.players.sprites():
                    player.maxLife += 3

            elif item == 13:
                for player in self.game.players.sprites():
                    player.maxLife += 4

            elif item == 14:
                for player in self.game.players.sprites():
                    player.maxLife += 5

            elif item == 15:
                for player in self.game.players.sprites():
                    player.hab1cooldown -= 1

            elif item == 16:
                for player in self.game.players.sprites():
                    player.hab1cooldown -= 2

            elif item == 17:
                for player in self.game.players.sprites():
                    player.hab1cooldown -= 3

            elif item == 18:
                for player in self.game.players.sprites():
                    player.hab1cooldown -= 4

            elif item == 19:
                for player in self.game.players.sprites():
                    player.hab1cooldown -= 5

            elif item == 20:
                for player in self.game.players.sprites():
                    player.damage += 1

            elif item == 21:
                for player in self.game.players.sprites():
                    player.damage += 2

            elif item == 22:
                for player in self.game.players.sprites():
                    player.damage += 3

            elif item == 23:
                for player in self.game.players.sprites():
                    player.damage += 4

            elif item == 24:
                for player in self.game.players.sprites():
                    player.damage += 5

            elif item == 25:
                for player in self.game.players.sprites():
                    player.life = player.maxLife

            elif item == 26:
                for player in self.game.players.sprites():
                    player.life += 1

            elif item == 27:
                for player in self.game.players.sprites():
                    player.life += 2

            elif item == 28:
                for player in self.game.players.sprites():
                    player.life += 3

            elif item == 29:
                for player in self.game.players.sprites():
                    player.life += 4