import pygame
from interpreter import interpreter

class Camera():

    def __init__(self, height, width):
        self.camera = pygame.Rect(0,0, width, height)
        self.width = width
        self.height = height
        self.data = interpreter()

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.data.getParameter('screenSize')[0] / 2)
        y = -target.rect.y + int(self.data.getParameter('screenSize')[1] / 2)
