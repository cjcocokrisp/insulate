import pygame as pg
from settings import *

class App():

    def __init__(self):
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Insulate Development Build')
        self.clock = pg.time.Clock()

    def run(self):
        self.new()

    def new(self):
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(GREY)
        pg.display.flip()

