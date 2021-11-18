import pygame as pg
from settings import *

vec = pg.math.Vector2

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

class Player(pg.sprite.Sprite):
    """
    Class that handles the player for the reward section.
    """
    
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(TEAL_BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(250, 250)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.in_air = False
        
    def jump(self):
        if not self.in_air:
            self.vel.y = -20
        
    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x < 0:
            self.pos.x = WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x = 0 
            
        self.rect.midbottom = self.pos
        
        if self.vel.y < 0.81 and self.vel.y > 0:
            self.in_air = False
        else:
            self.in_air = True
