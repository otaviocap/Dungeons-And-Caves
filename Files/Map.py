import pytmx as px
import pygame

class tiledMap:

    def __init__(self, file):
        tm = px.load_pygame(file, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmdata = tm


    def render(self, surface, game):
        ti = self.tmdata.get_tile_image_by_gid
        tempSurface3 = pygame.Surface(surface.get_size())
        tempSurface2 = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        for layers in self.tmdata.visible_layers:
            if layers.name == 'UpperCharacter':
                if isinstance(layers, px.TiledTileLayer):
                    for x, y, gid in layers:
                        tile = ti(gid)
                        if tile:
                            if gid == 0:
                                pass
                            else:
                                tempSurface2.blit(tile, (x * self.tmdata.tilewidth, y * self.tmdata.tileheight))
                    self.upperLayer = tempSurface2
            elif isinstance(layers, px.TiledTileLayer):
                for x, y, gid in layers:
                    tile = ti(gid)
                    if tile:
                        tempSurface3.blit(tile, (x * self.tmdata.tilewidth, y * self.tmdata.tileheight))
                self.underLayer = tempSurface3


    def makeMap(self, game):
        tempSurface = pygame.Surface((self.width, self.height))
        self.render(tempSurface, game)
        return tempSurface

    def getProportions(self):
        return (self.height, self.width)



class Wall(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__()
        game.walls.add(self)
        self.game = game
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)

