import pygame as pg
from pygame.constants import KEYDOWN, K_z
from settings import *
from sprites import *
import random
from time import sleep
import json

class Game():
    
    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Insulate Development Build")
        self.clock = pg.time.Clock()
        self.score = 0
        self.coin_count = 0
        self.enemies_defeated = 0
        self.enemy_limit = 0
        self.stats = self.load_stats()
        self.new_high_score = False
    
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
                self.enemies_defeated += 1
                self.score += 5
                
        enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            self.game_over()
                        
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
            p = Surface(random.randint(30, WIDTH - 30), random.randint(-30, 0), random.randint(100, 200), 20, GREEN_SHEEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
            
        if len(self.coins) < 3:
            c = Surface(random.randint(0, WIDTH), random.randint(-90, 0), 20, 20, GOLD)
            self.coins.add(c)
            self.all_sprites.add(c)
            
        if len(self.enemies) < self.enemy_limit:
            e = Enemies(random.randint(-500, 0), random.randint(0, 1))
            self.enemies.add(e)
            self.all_sprites.add(e)
            
        self.change_difficulty()
            
        if self.player.pos.y > 1000:
            self.game_over()
            
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
        
    def change_difficulty(self):
        if self.score > 2250:
            self.enemy_limit = 10
        elif self.score > 2000:
            self.enemy_limit = 9
        elif self.score > 1750:
            self.enemy_limit = 8
        elif self.score > 1500:
            self.enemy_limit = 7
        elif self.score > 1250:
            self.enemy_limit = 6
        elif self.score > 1000:
            self.enemy_limit = 5
        elif self.score > 750:
            self.enemy_limit = 4
        elif self.score > 500:
            self.enemy_limit = 3
        elif self.score > 250:
            self.enemy_limit = 2
        elif self.score > 100:
            self.enemy_limit = 1
            
    def game_over(self):
        self.playing = False
        self.draw_text('GAME OVER', 64, RED, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        sleep(2)
        self.results_screen()
        self.running = False
        
    def results_screen(self):
        self.update_stats()
        self.screen.fill(ASH_GRAY)
        self.draw_text('Results:', 64, CHARLESTON_GREEN, WIDTH / 2, 20)
        self.draw_text('Score: ' + str(self.score), 64, CHARLESTON_GREEN, WIDTH / 2, 100)
        self.draw_text('Coins Collected: ' + str(self.coin_count), 55, CHARLESTON_GREEN, WIDTH / 2, 180)
        self.draw_text('Enemies Defeated: ' + str(self.enemies_defeated), 58, CHARLESTON_GREEN, WIDTH / 2, 260)
        if self.new_high_score:
            self.draw_text('NEW HIGH SCORE!!!', 64, TEAL_BLUE, WIDTH / 2, 340)
        self.draw_text('-Press any key to continue-', 40, CHARLESTON_GREEN, WIDTH / 2, 420)
        pg.display.flip()
        self.wait_for_input()
        self.save_stats()
        
    
    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen."
        
        font = pg.font.Font('./assets/font/font.otf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def update_stats(self):
        
        "Updates the user stats after a game."
        
        if self.score > self.stats['high_score']:
            self.stats['high_score'] = self.score
            self.new_high_score = True
        
        self.stats['total_score'] += self.score
        self.stats['total_coins_collected'] += self.coin_count
        self.stats['total_enemies_defeated'] += self.enemies_defeated
        self.stats['games_played'] += 1
    
    def load_stats(self):
        
        "Loads the games statistics from data/game_stats.json."
        
        with open('data/game_stats.json', 'r') as f:
            stats = json.load(f)
        
        f.close()
        return stats
    
    def save_stats(self):
        
        "Saves the game statstics to data/game_stats.json."
        
        with open('data/game_stats.json', 'w') as f:
            json.dump(self.stats, f)
            
        f.close()
        
    def wait_for_input(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                        waiting = False

