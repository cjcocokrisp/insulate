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
    Class that draws a quadrilateral to the screen.
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
        self.game = game # Gets the game class to interact with it for its logic.
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
        
        "Causes the player to jump."
        
        if not self.in_air: # Only jumps if the player is not in the air.
            self.vel.y = -20
    
    def shoot(self, direction):
        
        "Allows the player to shoot a bullet."
        
        if len(self.game.bullets) < 5: # Allows up to 5 bullets to be shot.
            b = Bullet(self.rect.x + 15, self.rect.y + 15, direction) # Creates a bullet and adds it to the game's bullet group.
            self.game.bullets.add(b)
            self.game.all_sprites.add(b)
        
    def update(self):
        
        "Updates the player every frame."
        
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: # Moves left and sets direction to left.
            self.acc.x = -PLAYER_ACC
            self.direction = 0
        if keys[pg.K_RIGHT]: # Moves right and sets direction to right. 
            self.acc.x = PLAYER_ACC
            self.direction = 1
        if keys[pg.K_UP]: # Sets player direction to up. 
            self.direction = 2
        if keys[pg.K_DOWN]: # Sets player direction to down. 
            self.direction = 3
        if keys[pg.K_LSHIFT]:
            self.shoot(self.direction)
        
        self.acc.x += self.vel.x * PLAYER_FRICTION # Stops player when movement is stopped.
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # If the player goes all the way to the left or right swaps their side.
        if self.pos.x < 0:
            self.pos.x = WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x = 0 
            
        self.rect.midbottom = self.pos
        
        if self.vel.y < 0.81 and self.vel.y > 0: # Checks to see if the player is on the ground. 
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
        self.speed = 5
        
    def update(self):
        
        "Updates the enemy every frame."
        
        if self.direction == 0: # Moves the enemy left or right. 
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
        if self.rect.x > WIDTH: # If the enemy goes all the way to the left or right moves them to the other side.
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
        self.direction = direction # 0 - left, 1 - right, 2 - up, 3 - down.
    
    def size_choice(self, direction):
        
        "Changes the bullet size based on what direction it is shot in."
        
        if direction == 2 or direction == 3:
            size = (10, 20)
            return size
        else:
            size = (20, 10)
            return size
    
    def update(self):
        
        if self.direction == 0: # Moves bullet left. 
            self.rect.x -= BULLET_SPEED
        elif self.direction == 1: # Moves bullet right.
            self.rect.x += BULLET_SPEED
        elif self.direction == 2: # Moves bullet up.
            self.rect.y -= BULLET_SPEED
        elif self.direction == 3: # Moves bullet down. 
            self.rect.y += BULLET_SPEED
        
        # The rest deals with the despawning the bullet once it goes off screen.
        if self.rect.x > WIDTH + 100: 
            self.kill()
        elif self.rect.x < -100:
            self.kill()
            
        if self.rect.y < -100:
            self.kill()
        elif self.rect.y > HEIGHT + 100:
            self.kill()
                
            
        