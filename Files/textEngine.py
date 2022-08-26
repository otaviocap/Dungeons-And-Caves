import pygame
from glob import glob

class textGui():

    def __init__(self):
        if not pygame.font.get_init():
            pygame.font.init()
        self.extraFonts = []
        for font in glob('../Fonts/*.*'):
            self.extraFonts.append(pygame.font.Font(font, 50))

    def text(self, text, color=(255,255,255), antialias=True, useFont=None, background=None):
        return pygame.font.Font.render(self.extraFonts[0], text, antialias, color, background)

    def size(self, text):
        try:
            return pygame.font.Font.size(self.extraFonts[0], text)
        except IndexError as exc:
            print("Error in {path}: {error}".format(path=__file__, error=str(exc)))
            raise IndexError
