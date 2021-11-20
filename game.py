import pygame as pg
from pygame.constants import KEYDOWN, K_z
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
        self.coin_count = 0
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        ground = Surface(0, HEIGHT - 60, WIDTH, 60, GREEN_SHEEN)
        start_plat1 = Surface(20, 280, 110, 20, GREEN_SHEEN)
        start_plat2 = Surface(WIDTH - 130, 280, 110, 20, GREEN_SHEEN)
        start_plat3 = Surface(WIDTH / 2 - 55, 100, 110, 20, GREEN_SHEEN)
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
        
        if self.player.vel.y > 0:
            plat_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if plat_hits:
                self.player.pos.y = plat_hits[0].rect.top 
                self.player.vel.y = 0
            
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, False)
        if coin_hits:
            self.coin_count += 1
            self.score += 1
            coin_hits[0].kill()

        bullet_hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, False)
        if bullet_hits:
            for hit in bullet_hits:
                hit.kill()
                self.score += 5
                
        enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            self.running = False
            self.playing = False
            
        if self.player.rect.top <= 200: 
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.top += max(abs(self.player.vel.y), 2)
                if plat.rect.y >= 500:
                    plat.kill()
                    self.score += 10
            for coin in self.coins:
                coin.rect.top += max(abs(self.player.vel.y), 2)
                if coin.rect.y >= 500:
                    coin.kill()
            for enemy in self.enemies:
                enemy.rect.top += max(abs(self.player.vel.y), 2)
                if enemy.rect.y >= 500:
                    enemy.kill()

        if len(self.platforms) < 5:
            p = Surface(random.randint(0, WIDTH), random.randint(-90, 0), random.randint(100, 200), 20, GREEN_SHEEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
            
        if len(self.coins) < 3:
            c = Surface(random.randint(0, WIDTH), random.randint(-90, 0), 20, 20, GOLD)
            self.coins.add(c)
            self.all_sprites.add(c)
            
        if len(self.enemies) < 1:
            e = Enemies(random.randint(-90, 0), random.randint(0, 1))
            self.enemies.add(e)
            self.all_sprites.add(e)
            
        if self.player.pos.y > 1000:
            self.playing = False
            self.running = False
            
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
                if event.key == pg.K_LEFT and event.key == K_z:
                    self.player.jump()             
        
    def draw(self):
        self.screen.fill(ASH_GRAY)
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 64, CHARLESTON_GREEN, WIDTH / 2, 20)
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen."
        
        font = pg.font.Font('./assets/font/font.otf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
