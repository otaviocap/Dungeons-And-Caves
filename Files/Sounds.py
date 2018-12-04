import pygame
from Interpreter import Interpreter

class Sound():

    def __init__(self):
        self.musics = [pygame.mixer.Sound('../Assets/Sounds/dungeon.ogg'), pygame.mixer.Sound('../Assets/Sounds/dungeon2.ogg'),
                       pygame.mixer.Sound('../Assets/Sounds/menu.ogg')]
        self.bossMusics = [pygame.mixer.Sound('../Assets/Sounds/bossMain.ogg'),
                           pygame.mixer.Sound('../Assets/Sounds/bossFinal.ogg')]
        self.effects = [pygame.mixer.Sound('../Assets/Sounds/click.ogg'),
                        pygame.mixer.Sound('../Assets/Sounds/magic.ogg'),
                        pygame.mixer.Sound('../Assets/Sounds/youDied.ogg'),
                        pygame.mixer.Sound('../Assets/Sounds/spike.ogg'),
                        pygame.mixer.Sound('../Assets/Sounds/openingChest.ogg'),
                        pygame.mixer.Sound('../Assets/Sounds/death.ogg')]
        self.musicChannel = pygame.mixer.Channel(0)
        self.sfxChannel = pygame.mixer.Channel(1)
        self.sfx2Channel = pygame.mixer.Channel(2)
        self.musicChannel.set_volume(Interpreter().getParameter('music'))
        self.sfxChannel.set_volume(Interpreter().getParameter('sfx'))
        self.sfx2Channel.set_volume(Interpreter().getParameter('sfx'))
        self.lastMusic = self.musics[0]
        self.equalization()

    def update(self):
        if not self.musicChannel.get_busy():
            self.musicChannel.queue(self.lastMusic)
        a = Interpreter().getParameter('music')
        b = Interpreter().getParameter('sfx')
        self.musicChannel.queue(self.lastMusic)
        self.musicChannel.set_volume(a)
        self.sfxChannel.set_volume(b)
        self.sfx2Channel.set_volume(b)

    def playMusic(self, lane, music):
        pygame.mixer.fadeout(500)
        if lane == 0:
            self.musicChannel.queue(self.musics[music])
            self.lastMusic = self.musics[music]
        elif lane == 1:
            self.musicChannel.queue(self.bossMusics[music])
            self.lastMusic = self.bossMusics[music]

    def playSfx(self, sfx):
        if not self.sfxChannel.get_busy():
            self.sfxChannel.queue(self.effects[sfx])
        else:
            self.sfx2Channel.queue(self.effects[sfx])

    def equalization(self):
        self.effects[1].set_volume(0.2)
        self.effects[2].set_volume(1)
        self.effects[3].set_volume(0.3)
        self.effects[5].set_volume(0.5)

