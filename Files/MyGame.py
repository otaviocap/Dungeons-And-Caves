import pygame
from Player import Player
from Bullet import Bullet
from interpreter import interpreter


configs = interpreter('configs')
hab1cooldown = 10
speedB = 5
velocity = 1
ammo = 45
magCapacity = 10
screenSize = configs.getParameter('screenSize')
fps = configs.getParameter('fps')

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

done = False
bullets = pygame.sprite.Group()

player = Player(0, 0)

mag = 10

while not done:
    clock.tick(fps)
    velocity = 2
    screen.fill((0,0,0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            done = True
    key = pygame.key.get_pressed()

    if key[pygame.K_LSHIFT]:
        velocity = 3
    elif key[pygame.K_LCTRL]:
        velocity = 1
    if key[pygame.K_a]:
        player.move(-velocity, 0)
    if key[pygame.K_d]:
        player.move(velocity, 0)
    if key[pygame.K_w]:
        player.move(0, -velocity)
    if key[pygame.K_s]:
        player.move(0, velocity)


    if player.checkCooldown():
        if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
            if mag == 0:
                if not ammo == 0:
                    ammo -= magCapacity
                    mag = magCapacity
                    player.setCooldown(50)
                else:
                    pass
            else:
                mag -= 1
                if key[pygame.K_LEFT]:
                    bullet = Bullet('left', speedB, screenSize)
                    player.setDirection('left')
                    bullet.rect.x = player.rect.x - 35
                    bullet.rect.y = player.rect.y + 25
                    bullets.add(bullet)
                    player.setCooldown(hab1cooldown)

                elif key[pygame.K_RIGHT]:
                    bullet = Bullet('right', speedB, screenSize)
                    player.setDirection('right')
                    bullet.rect.x = player.rect.x + 40
                    bullet.rect.y = player.rect.y + 27
                    bullets.add(bullet)
                    player.setCooldown(hab1cooldown)

                elif key[pygame.K_UP]:
                    bullet = Bullet('up', speedB, screenSize)
                    player.setDirection('up')
                    bullet.rect.x = player.rect.x + 26
                    bullet.rect.y = player.rect.y - 40
                    bullets.add(bullet)
                    player.setCooldown(hab1cooldown)

                elif key[pygame.K_DOWN]:
                    bullet = Bullet('down', speedB, screenSize)
                    player.setDirection('down')
                    bullet.rect.x = player.rect.x - 25
                    bullet.rect.y = player.rect.y + 30
                    bullets.add(bullet)
                    player.setCooldown(hab1cooldown)

    for i in bullets.sprites():
        i.go()
        # pygame.draw.rect(screen, i.getColor(), i.rect)
        screen.blit(i.getImg(), (i.getPos()[0] - i.getImg().get_rect().center[0], i.getPos()[1] - i.getImg().get_rect().center[1]))
        if i.rect.x >= screenSize[0] or i.rect.y >= screenSize[1] or i.rect.x <= 0 or i.rect.y <= 0:
            bullets.remove(i)
    # pygame.draw.rect(screen, (97,49,108), player.rect)
    player.goCooldown()
    screen.blit(player.getImg(), (player.getPos()[0] - player.getImg().get_rect().center[0], player.getPos()[1] - player.getImg().get_rect().center[1]))
    pygame.display.flip()
    pygame.display.set_caption(str(ammo) + '/' + str(mag) + str(bullets) + 'FPS = ' + str(clock.get_fps()))
    print(ammo, '/', mag)

pygame.quit()
