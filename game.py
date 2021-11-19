import pygame as pg
from pygame.constants import KEYDOWN
from settings import *
from sprites import *
import random

class Game():
    
    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Insulate Development Build")
        self.clock = pg.time.Clock()
        self.score = 0
        self.coins = 0
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.platforms = pg.sprite.Group()
        ground = Surface(0, HEIGHT - 60, WIDTH, 60, CHARLESTON_GREEN)
        start_plat1 = Surface(20, 280, 110, 20, CHARLESTON_GREEN)
        start_plat2 = Surface(WIDTH - 130, 280, 110, 20, CHARLESTON_GREEN)
        start_plat3 = Surface(WIDTH / 2 - 55, 100, 110, 20, CHARLESTON_GREEN)
        self.platforms.add(ground, start_plat1, start_plat2, start_plat3)
        self.all_sprites.add(self.player, ground, start_plat1, start_plat2, start_plat3)
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
            
        if self.player.rect.top <= 120: 
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.top += max(abs(self.player.vel.y),2)
                if plat.rect.y >= 500:
                    plat.kill()
                    self.score += 10
                    print(self.score)

        if len(self.platforms) <= 5:
            p = Surface(random.randint(0, WIDTH), random.randint(-180, 0), random.randint(100, 200), 20, CHARLESTON_GREEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
            
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
