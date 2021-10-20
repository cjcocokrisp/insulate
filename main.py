import pygame as pg
import pygame as pg
from settings import *
from sprites import *

class App():

    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Insulate Development Build')
        self.clock = pg.time.Clock()
        self.state = 'menu-main'

    def run(self):
        self.events()
        self.update()
        self.draw()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        if self.state == 'menu-main':
            self.check = Image('./assets/img/menu-main/check.png', WIDTH / 2 - 93.5, 240)
            self.all_sprites.add(self.check)
            self.track = Image('./assets/img/menu-main/track.png', WIDTH / 2 - 98, 300)
            self.all_sprites.add(self.track)
            self.settings = Image('./assets/img/menu-main/settings.png', WIDTH / 2 - 133.5, 360)
            self.all_sprites.add(self.settings)
            self.quit = Image('./assets/img/menu-main/quit.png', WIDTH / 2 - 69, 420)
            self.all_sprites.add(self.quit)
            self.help = Image('./assets/img/menu-main/help.png', WIDTH - 56, HEIGHT - 56)
            self.all_sprites.add(self.help)
        if self.state == 'menu-track':
            self.header = Image('./assets/img/menu-track/header.png', 0, 0)
            self.all_sprites.add(self.header)
            self.manual = Image('./assets/img/menu-track/manual.png', WIDTH / 2 - 90.5 , 220)
            self.all_sprites.add(self.manual)
            self.dexcom = Image('assets/img/menu-track/dexcom.png', WIDTH / 2 - 160.5, 280)
            self.all_sprites.add(self.dexcom)
            self.back = Image('./assets/img/back.png', 0, HEIGHT - 56)
            self.all_sprites.add(self.back)
        self.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        mouse_pos = pg.mouse.get_pos()
        if self.state == 'menu-main':
            if pg.mouse.get_pressed()[0] and self.quit.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.running = False
            
            if pg.mouse.get_pressed()[0] and self.track.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-track')

        if self.state == 'menu-track':
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main')
            
    
    def draw(self):
        self.screen.fill(ASH_GRAY)
        self.all_sprites.draw(self.screen)
        if self.state == 'menu-main':
            self.draw_text('LOGO WILL BE ABOVE WHEN IT IS FINISHED...', 32, RED, 250, 0)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen." 
       
        font = pg.font.Font('./assets/font/font.otf', size) # Checks to see if the font is part of Pygame's font library. 
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def state_change(self, newState):

        "Changes the state that the app is on."

        self.state = newState
        self.new()


