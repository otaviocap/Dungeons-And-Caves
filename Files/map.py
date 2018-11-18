import pytmx as px
import pygame

class tiledMap:

    def __init__(self, file):
        tm = px.load_pygame(file, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmdata = tm

    def render(self, surface):
        ti = self.tmdata.get_tile_image_by_gid
        for layers in self.tmdata.visible_layers:
            if isinstance(layers, px.TiledTileLayer):
                for x, y, gid in layers:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmdata.tilewidth, y * self.tmdata.tileheight))

    def makeMap(self):
        tempSurface = pygame.Surface((self.width, self.height))
        self.render(tempSurface)
        return tempSurface

    def getProportions(self):
        return (self.height, self.width)

class wall(pygame.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        super().__init__(self, self.groups)
        self.groups = game.walls
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

