import pygame

pygame.font.init()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text(msg, x, y, size, screen, color):
        font = pygame.font.Font("OpenSans.ttf",size)
        textSurf, textRect = text_objects(msg, font, color)
        textRect.center = x, y
        screen.blit(textSurf, textRect)
