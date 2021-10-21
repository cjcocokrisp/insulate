import pygame as pg
from settings import *

class Image(pg.sprite.Sprite):
    """
    Class that allows for drawing an image to the screen.
    The exact file path must be inputted.
    """
    def __init__(self, file_path, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Surface(pg.sprite.Sprite):
    """
    Class that draws rectangles to the screen.
    """
    def __init__(self, x, y, width, height, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
