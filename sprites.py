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
        self.direction = 1 # 0 - left, 1 - right, 2 - up, 3 - down
        
    def jump(self):
        if not self.in_air:
            self.vel.y = -20
    
    def shoot(self, direction):
        if len(self.game.bullets) < 3:
            b = Bullet(self.rect.x, self.rect. y, direction)
            self.game.bullets.add(b)
            self.game.all_sprites.add(b)
        
    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.direction = 0
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.direction = 1
        if keys[pg.K_UP]:
            self.direction = 2
        if keys[pg.K_DOWN]:
            self.direction = 3
        if keys[pg.K_LSHIFT]:
            self.shoot(self.direction)
        
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
            
class Enemies(pg.sprite.Sprite):
    
    """
    Class that handles the enemies for the reward section.
    """

    def __init__(self, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
        self.direction = direction # 0 - left, 1 - right
        
    def update(self):
        if self.direction == 0:
            self.rect.x -= 5
        else:
            self.rect.x += 5
            
        if self.rect.x > WIDTH:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = WIDTH
            
class Bullet(pg.sprite.Sprite):
        
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        size = self.size_choice(direction)
        self.image = pg.Surface(size)
        self.image.fill(TEAL_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction # 0 - left, 1 - right
    
    def size_choice(self, direction):
        if direction == 2 or direction == 3:
            size = (10, 20)
            return size
        else:
            size = (20, 10)
            return size
    
    def update(self):
        
        if self.direction == 0:
            self.rect.x -= 10
        elif self.direction == 1:
            self.rect.x += 10
        elif self.direction == 2:
            self.rect.y -= 10
        elif self.direction == 3:
            self.rect.y += 10
        
        if self.rect.x > WIDTH:
            self.kill()
        elif self.rect.x < 0:
            self.kill()
            
        if self.rect.y < 0:
            self.kill()
        elif self.rect.y > HEIGHT:
            self.kill()
                
            
        