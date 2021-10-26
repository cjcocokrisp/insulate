from types import DynamicClassAttribute
import pygame as pg
import pygame as pg
from pygame import mouse
from pygame.constants import K_BACKSPACE
from settings import *
from sprites import *
import json

class App():

    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Insulate Development Build')
        self.clock = pg.time.Clock()
        self.state = 'menu-main'
        self.manualBSInput = ''
        self.manualBSData = []
        self.appSettings = self.load_settings()

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
        if self.state == 'track-manual':
            self.header = Image('./assets/img/manual-input/header-' + str(self.appSettings['collection_range']) + '.png', 0, 0)
            self.all_sprites.add(self.header)
            self.inputBox = Surface(WIDTH / 2 - 135, HEIGHT / 2 - 50 , 270, 120, CHARLESTON_GREEN)
            self.all_sprites.add(self.inputBox)
            self.enter = Image('./assets/img/manual-input/enter.png', HEIGHT / 2 - 73.5, HEIGHT / 2 + 85)
            self.all_sprites.add(self.enter)
        if self.state == 'settings':
            self.header = Image('./assets/img/settings/header.png', 0, 50)
            self.all_sprites.add(self.header)
            self.high = Image('./assets/img/settings/high.png', 45, 150)
            self.all_sprites.add(self.high)
            self.low = Image('./assets/img/settings/low.png', 45, 200)
            self.all_sprites.add(self.low)
            self.collect = Image('./assets/img/settings/collection.png', 45, 250)
            self.all_sprites.add(self.collect)
            self.leftArrowH = Image('./assets/img/settings/left-arrow.png', 325, 150)
            self.all_sprites.add(self.leftArrowH)
            self.optionBoxH = Surface(355, 150, 65, 40, CHARLESTON_GREEN)
            self.all_sprites.add(self.optionBoxH)
            self.rightArrowH = Image('./assets/img/settings/right-arrow.png', 430, 150)
            self.all_sprites.add(self.rightArrowH)
            self.leftArrowL = Image('./assets/img/settings/left-arrow.png', 325, 200)
            self.all_sprites.add(self.leftArrowL)
            self.optionBoxL = Surface(355, 200, 65, 40, CHARLESTON_GREEN)
            self.all_sprites.add(self.optionBoxL)
            self.rightArrowL = Image('./assets/img/settings/right-arrow.png', 430, 200)
            self.all_sprites.add(self.rightArrowL)
            self.leftArrowC = Image('./assets/img/settings/left-arrow.png', 325, 250)
            self.all_sprites.add(self.leftArrowC)
            self.optionBoxC = Surface(355, 250, 65, 40, CHARLESTON_GREEN)
            self.all_sprites.add(self.optionBoxC)
            self.rightArrowC = Image('./assets/img/settings/right-arrow.png', 430, 250)
            self.all_sprites.add(self.rightArrowC)
            self.save = Image('./assets/img/settings/save.png', WIDTH / 2 - 93.5, 350)
            self.all_sprites.add(self.save)
        if self.state != 'menu-main':
            self.back = Image('./assets/img/back.png', 0, HEIGHT - 56)
            self.all_sprites.add(self.back)
        self.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if self.state == 'track-manual' and event.type == pg.KEYDOWN and event.unicode in DIGITS and len(self.manualBSInput) <= 2:
                self.manualBSInput += event.unicode
            if self.state == 'track-manual' and event.type == pg.KEYDOWN and event.key == K_BACKSPACE:
                self.manualBSInput = ''
            if event.type == pg.MOUSEBUTTONUP and self.state == 'settings': 
                mouse_pos = pg.mouse.get_pos()
                if self.leftArrowH.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.appSettings['high_setting'] > 120:
                    self.appSettings['high_setting'] -= 5
                elif self.rightArrowH.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.appSettings['high_setting'] < 400:
                    self.appSettings['high_setting'] += 5
                
                if self.leftArrowL.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.appSettings['low_setting'] > 60:
                    self.appSettings['low_setting'] -= 5
                elif self.rightArrowL.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.appSettings['low_setting'] < 100:
                    self.appSettings['low_setting'] += 5

                if self.leftArrowC.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.appSettings['collection_range'] == 24: self.appSettings['collection_range'] = 12
                    elif self.appSettings['collection_range'] == 48: self.appSettings['collection_range'] = 24
                elif self.rightArrowC.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.appSettings['collection_range'] == 12: self.appSettings['collection_range'] = 24
                    elif self.appSettings['collection_range'] == 24: self.appSettings['collection_range'] = 48

    def update(self):
        self.all_sprites.update()
        mouse_pos = pg.mouse.get_pos()
        if self.state == 'menu-main':
            if pg.mouse.get_pressed()[0] and self.quit.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.running = False
            
            if pg.mouse.get_pressed()[0] and self.track.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-track')

            if pg.mouse.get_pressed()[0] and self.settings.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('settings')

        if self.state == 'menu-track':
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main')
            
            if pg.mouse.get_pressed()[0] and self.manual.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('track-manual')
        
        if self.state == 'track-manual':
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main')
                if self.manualBSData:
                    i = 0
                    while i < len(self.manualBSData):
                        self.manualBSData[i] = int(self.manualBSData[i])
                        i += 1
                with open('data/manual_data.json', 'w') as f:
                    json.dump(self.manualBSData, f)
                    f.close()

            if pg.mouse.get_pressed()[0] and self.enter.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.manualBSData.append(self.manualBSInput)
                self.manualBSInput = ''
                while '' in self.manualBSData:
                    self.manualBSData.remove('')
        
        if self.state == 'settings':

            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main')
                
            if pg.mouse.get_pressed()[0] and self.save.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.save_settings()

            
    
    def draw(self):
        self.screen.fill(ASH_GRAY)
        self.all_sprites.draw(self.screen)
        if self.state == 'menu-main':
            self.draw_text('LOGO WILL BE ABOVE WHEN IT IS FINISHED...', 32, RED, 250, 0)
        if self.state == 'track-manual':
            self.draw_text(self.manualBSInput, 110, BEIGE, WIDTH / 2, HEIGHT / 2 - 45)
        if self.state == 'settings':
            self.draw_text(str(self.appSettings['high_setting']), 32, ASH_GRAY, 387, 152)
            self.draw_text(str(self.appSettings['low_setting']), 32, ASH_GRAY, 387, 202)
            self.draw_text(str(self.appSettings['collection_range']), 32, ASH_GRAY, 387, 252)
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

    def average_data(data: list):

        "Calculates the average of a list of integers or floats."

        return sum(data) / len(data)

    def load_settings(self):

        "Loads settings from './data/settings.json'"

        with open('./data/settings.json', 'r') as f:
            settings = json.load(f)

        f.close()
        return settings

    def save_settings(self):

        "Save settings when altered."

        with open('./data/settings.json', 'w') as f:
            json.dump(self.appSettings, f)

        f.close()


