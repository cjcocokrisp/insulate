import pygame as pg
from pygame.constants import KEYDOWN
from settings import *
from sprites import *

class Game():
    
    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Insulate Development Build")
        self.clock = pg.time.Clock()
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.platforms = pg.sprite.Group()
        p = Surface(0, HEIGHT - 60, WIDTH, 60, CHARLESTON_GREEN)
        self.platforms.add(p)
        self.all_sprites.add(p)
        self.all_sprites.add(self.player)
        self.run()
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        self.all_sprites.update()
        
        plat_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if plat_hits:
            self.player.pos.y = plat_hits[0].rect.top
            self.player.vel.y = 0
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            if event.type == KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.playing = False
                if event.key == pg.K_SPACE:
                    self.player.jump()                
        
    def draw(self):
        self.screen.fill(ASH_GRAY)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen."
        
        font = pg.font.Font('./assets/font/font.otf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
