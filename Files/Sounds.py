import pygame
from Interpreter import Interpreter

class Sound():

    def __init__(self):
        self.musics = [pygame.mixer.Sound('../Assets/Sounds/dungeon.ogg'), pygame.mixer.Sound('../Assets/Sounds/dungeon2.ogg')]
        self.bossMusics = [pygame.mixer.Sound('../Assets/Sounds/bossMain.ogg'), pygame.mixer.Sound('../Assets/Sounds/bossFinal.ogg')]
        self.effects = [pygame.mixer.Sound('../Assets/Sounds/click.ogg'), pygame.mixer.Sound('../Assets/Sounds/magic.ogg')]
        self.musicVolume = Interpreter().getParameter('music')
        self.sfxVolume = Interpreter().getParameter('sfx')
        self.musicChannel = pygame.mixer.Channel(0)
        self.sfxChannel = pygame.mixer.Channel(1)
        self.musicChannel.set_volume(self.musicVolume)
        self.sfxChannel.set_volume(self.sfxVolume)
        # self.musicChannel.set_endevent('')

    def playMusic(self, lane, music):
        pygame.mixer.fadeout(500)
        if lane == 0:
            self.musicChannel.queue(self.musics[music])
        elif lane == 1:
            self.musicChannel.queue(self.musics[music])

    def playSfx(self, sfx):
        self.sfxChannel.queue(self.effects[sfx])

