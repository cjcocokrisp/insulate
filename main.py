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
            self.quit = Image('./assets/img/menu-main/quit.png', 20, 20)
            self.all_sprites.add(self.quit)
        self.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        mouse_pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0] and self.quit.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.running = False
    
    def draw(self):
        self.screen.fill(ASH_GRAY)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen." 
       
        font = pg.font.Font('./assets/font/font.otf', size) # Checks to see if the font is part of Pygame's font library. 
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

