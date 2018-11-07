import pygame
from Player import Player
from Bullet import Bullet
from interpreter import interpreter


class game():

    def __init__(self):
        pygame.init()
        self.configs = interpreter('configs')
        self.hab1cooldown = 10
        self.speedB = 5
        self.velocity = 1
        self.ammo = 45
        self.magCapacity = 10
        self.screenSize = self.configs.getParameter('screenSize')
        self.fps = self.configs.getParameter('fps')
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("My Game")

        self.clock = pygame.time.Clock()
        self.done = False
        self.bullets = pygame.sprite.Group()
        self.player = Player(0, 0)
        self.mag = 10

    def gameRun(self):
        while not self.done:
            self.events()
            self.update()

        pygame.quit()


    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.done = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.done = True
        key = pygame.key.get_pressed()

        if key[pygame.K_LSHIFT]:
            self.velocity = 3
        elif key[pygame.K_LCTRL]:
            self.velocity = 1
        if key[pygame.K_a]:
            self.player.move(-self.velocity, 0)
        if key[pygame.K_d]:
            self.player.move(self.velocity, 0)
        if key[pygame.K_w]:
            self.player.move(0, -self.velocity)
        if key[pygame.K_s]:
            self.player.move(0, self.velocity)


        if self.player.checkCooldown():
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
                if self.mag == 0:
                    if not self.ammo == 0:
                        self.ammo -= self.magCapacity
                        self.mag = self.magCapacity
                        self.player.setCooldown(50)
                    else:
                        pass
                else:
                    self.mag -= 1
                    if key[pygame.K_LEFT]:
                        bullet = Bullet('left', self.speedB, self.screenSize)
                        self.player.setDirection('left')
                        bullet.rect.x = self.player.rect.x - 35
                        bullet.rect.y = self.player.rect.y + 25
                        self.bullets.add(bullet)
                        self.player.setCooldown(self.hab1cooldown)

                    elif key[pygame.K_RIGHT]:
                        bullet = Bullet('right', self.speedB, self.screenSize)
                        self.player.setDirection('right')
                        bullet.rect.x = self.player.rect.x + 40
                        bullet.rect.y = self.player.rect.y + 27
                        self.bullets.add(bullet)
                        self.player.setCooldown(self.hab1cooldown)

                    elif key[pygame.K_UP]:
                        bullet = Bullet('up', self.speedB, self.screenSize)
                        self.player.setDirection('up')
                        bullet.rect.x = self.player.rect.x + 26
                        bullet.rect.y = self.player.rect.y - 40
                        self.bullets.add(bullet)
                        self.player.setCooldown(self.hab1cooldown)

                    elif key[pygame.K_DOWN]:
                        bullet = Bullet('down', self.speedB, self.screenSize)
                        self.player.setDirection('down')
                        bullet.rect.x = self.player.rect.x - 25
                        bullet.rect.y = self.player.rect.y + 30
                        self.bullets.add(bullet)
                        self.player.setCooldown(self.hab1cooldown)

    def update(self):
        self.clock.tick(self.fps)
        self.velocity = 2
        self.screen.fill((0, 0, 0))
        for i in self.bullets.sprites():
            i.go()
            # pygame.draw.rect(screen, i.getColor(), i.rect)
            self.screen.blit(i.getImg(), (i.getPos()[0] - i.getImg().get_rect().center[0], i.getPos()[1] - i.getImg().get_rect().center[1]))
            if i.rect.x >= self.screenSize[0] or i.rect.y >= self.screenSize[1] or i.rect.x <= 0 or i.rect.y <= 0:
                self.bullets.remove(i)
        # pygame.draw.rect(screen, (97,49,108), player.rect)
        self.player.goCooldown()
        self.screen.blit(self.player.getImg(), (self.player.getPos()[0] - self.player.getImg().get_rect().center[0], self.player.getPos()[1] - self.player.getImg().get_rect().center[1]))
        pygame.display.flip()
        pygame.display.set_caption(str(self.ammo) + '/' + str(self.mag) + str(self.bullets) + 'FPS = ' + str(self.clock.get_fps()))
        print(self.ammo, '/', self.mag)

if __name__ == '__main__':
    a = game()
    a.gameRun()
