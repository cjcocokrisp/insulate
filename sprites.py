import pygame as pg
from settings import *

class Image(pg.sprite.Sprite):
    """
    Class that allows for drawing an image to the screen.
    The exact file path must be inputted.
    A type is assignable to allow you to use images as buttons.
    """
    def __init__(self, file_path, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
