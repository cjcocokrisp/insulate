import pygame as pg
from pygame.constants import KEYDOWN, K_z
from settings import *
from sprites import *
import random
from time import sleep
import json

class Game():
    
    def __init__(self):
        
        "Initaliezes the program's variables."
        
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # See settings.py for the WIDTH and HEIGHT values.
        pg.display.set_caption("Insulate Development Build")
        self.clock = pg.time.Clock()
        self.score = 0
        self.coin_count = 0
        self.enemies_defeated = 0
        self.enemy_limit = 0
        self.stats = self.load_stats() # Loads stats from data/game_stats.json
        self.new_high_score = False
    
    def new(self):
        
        "Sets up sprite groups and creates the player."
        
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        ground = Surface(0, HEIGHT - 60, WIDTH, 60, GREEN_SHEEN)
        # Makes three starting platforms for the player. 
        start_plat1 = Surface(20, 280, 110, 20, GREEN_SHEEN)
        start_plat2 = Surface(WIDTH - 130, 280, 110, 20, GREEN_SHEEN)
        start_plat3 = Surface(WIDTH / 2 - 55, 100, 110, 20, GREEN_SHEEN)
        self.platforms.add(ground, start_plat1, start_plat2, start_plat3)
        self.all_sprites.add(self.player, ground, start_plat1, start_plat2, start_plat3)
        self.run()
        
    def run(self):
        
        "Runs the main loop."
        
        self.playing = True
        while self.playing:
            # Main Game Loop
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        
        "Updates the sprite groups."
        
        self.all_sprites.update()
        
        if self.player.vel.y > 0: # Platform Collision
            plat_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if plat_hits:
                self.player.pos.y = plat_hits[0].rect.top 
                self.player.vel.y = 0
            
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, False) # Coin Collision
        if coin_hits:
            self.coin_count += 1
            self.score += 1
            coin_hits[0].kill()

        bullet_hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, False) # Bullet Collision
        if bullet_hits:
            for hit in bullet_hits:
                hit.kill()
                self.enemies_defeated += 1
                self.score += 5
                
        enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False) # Enemy Collision
        if enemy_hits:
            self.game_over()
                        
        if self.player.rect.top <= 200: # Camera scroll based on player position. 
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.top += max(abs(self.player.vel.y), 2)
                if plat.rect.y >= 500:
                    plat.kill() # Removes platforms from the screen once they go off screen. 
                    self.score += 10
            for coin in self.coins:
                coin.rect.top += max(abs(self.player.vel.y), 2)
                if coin.rect.y >= 500:
                    coin.kill() # Removes uncollected coins from the screen once they go off screen.
            for enemy in self.enemies:
                enemy.rect.top += max(abs(self.player.vel.y), 2)
                if enemy.rect.y >= 500:
                    enemy.kill() # Removes unkilled enemies once they go off screen. 

        # For the next three logic statements the elements are spawn off screen from the top 
        if len(self.platforms) < 5: # Generates random platforms if there are less then five on the screen. 
            p = Surface(random.randint(30, WIDTH - 30), random.randint(-30, 0), random.randint(100, 200), 20, GREEN_SHEEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
            
        if len(self.coins) < 3: # Generates coins if there are less then 3 on the screen. 
            c = Surface(random.randint(0, WIDTH), random.randint(-90, 0), 20, 20, GOLD)
            self.coins.add(c)
            self.all_sprites.add(c)
            
        if len(self.enemies) < self.enemy_limit: # Generates enemies based on the enemy limit which is determined by how high your score is. 
            e = Enemies(random.randint(-500, 0), random.randint(0, 1))
            self.enemies.add(e)
            self.all_sprites.add(e)
            
        self.change_difficulty() # Checks to see if the difficulty should be higher. 
            
        if self.player.pos.y > 1000: # If the player falls causes a game over. 
            self.game_over()
            
    def events(self):
        
        "Handles the various events that can happen while using the program."
        
        for event in pg.event.get():
            if event.type == pg.QUIT: # If the X on the window bar is clicked closes application. 
                self.running = False
                self.playing = False
            if event.type == KEYDOWN: 
                if event.key == pg.K_ESCAPE: # If escape is pressed closes application. 
                    self.running = False
                    self.playing = False
                if event.key == pg.K_SPACE: # If space is clicked causes the player to jump.
                    self.player.jump()              
        
    def draw(self):
        
        "Draws elements and text to the screen."
        
        self.screen.fill(ASH_GRAY) # Sets background color.
        self.all_sprites.draw(self.screen) # Draws all sprites.
        self.draw_text("Score: " + str(self.score), 64, CHARLESTON_GREEN, WIDTH / 2, 20) # Writes the score on the top of the screen.
        pg.display.flip()
        
    def change_difficulty(self):
        
        "Changes the difficulty based on the score."
        
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
        
        "Displays game over screen."
        
        self.playing = False
        self.draw_text('GAME OVER', 64, RED, WIDTH / 2, HEIGHT / 2) # Writes game over over what is going on screen.
        pg.display.flip()
        sleep(2)
        self.results_screen()
        self.running = False
        
    def results_screen(self):
        
        "Displalys the results screen."
        
        self.update_stats()
        self.screen.fill(ASH_GRAY)
        self.draw_text('Results:', 64, CHARLESTON_GREEN, WIDTH / 2, 20)
        self.draw_text('Score: ' + str(self.score), 64, CHARLESTON_GREEN, WIDTH / 2, 100)
        self.draw_text('Coins Collected: ' + str(self.coin_count), 55, CHARLESTON_GREEN, WIDTH / 2, 180)
        self.draw_text('Enemies Defeated: ' + str(self.enemies_defeated), 58, CHARLESTON_GREEN, WIDTH / 2, 260)
        if self.new_high_score: # If the score is higher then the one in the stats file displays that you got a new high score.
            self.draw_text('NEW HIGH SCORE!!!', 64, TEAL_BLUE, WIDTH / 2, 340)
        self.draw_text('-Press space to continue-', 40, CHARLESTON_GREEN, WIDTH / 2, 420)
        pg.display.flip()
        self.wait_for_input()
        self.save_stats()
        
    
    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen."
        
        font = pg.font.Font('./assets/font/font.otf', size) # Loads the font. 
        text_surface = font.render(text, True, color) # Renders text with the selected color.
        text_rect = text_surface.get_rect() 
        text_rect.midtop = (x, y) # Sets the texts position. 
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
        
        with open('data/game_stats.json', 'r') as f: # Loads the stats from data/game_stats.json.
            stats = json.load(f)
        
        f.close()
        return stats
    
    def save_stats(self):
        
        "Saves the game statstics to data/game_stats.json."
        
        with open('data/game_stats.json', 'w') as f: # Saves the stats that were updated. 
            json.dump(self.stats, f)
            
        f.close()
        
    def wait_for_input(self):
        
        "Waits for the user to input the space bar to continue."
        
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP and event.key == pg.K_SPACE: # Stops waiting if the space bar is pressed.
                        waiting = False

