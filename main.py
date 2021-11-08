from types import DynamicClassAttribute
import pygame as pg
import pygame as pg
from pygame import mouse
from pygame.constants import K_BACKSPACE, K_LCTRL, K_v
from settings import *
from sprites import *
import json
import dexcom_integration as dex_int
import clipboard
from datetime import datetime


class App():

    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Insulate Development Build')
        self.clock = pg.time.Clock()
        self.state = 'menu-main'
        self.manual_bs_input = ''
        self.manual_bs_data = []
        self.auth_code = ''
        self.bearer_token = ''
        self.app_settings = self.load_settings()

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
            self.header = Image('./assets/img/manual-input/header-' + str(self.app_settings['collection_range']) + '.png', 0, 0)
            self.all_sprites.add(self.header)
            self.input_box = Surface(WIDTH / 2 - 135, HEIGHT / 2 - 50 , 270, 120, CHARLESTON_GREEN)
            self.all_sprites.add(self.input_box)
            self.enter = Image('./assets/img/manual-input/enter.png', HEIGHT / 2 - 73.5, HEIGHT / 2 + 85)
            self.all_sprites.add(self.enter)
        if self.state == 'track-dexcom':
            self.header = Image('./assets/img/dexcom-integration/header.png', 0, 25)
            self.all_sprites.add(self.header)
            self.sign_in = Image('./assets/img/dexcom-integration/open.png', 0, 150)
            self.all_sprites.add(self.sign_in)
            self.get_data = Image('./assets/img/dexcom-integration/get.png', 0, 375)
            self.all_sprites.add(self.get_data)
            self.input_box = Surface(10, 230, WIDTH - 20, 120, CHARLESTON_GREEN)
            self.all_sprites.add(self.input_box)
            self.paste = Image('./assets/img/dexcom-integration/paste.png', WIDTH - 120, HEIGHT - 37)
            self.all_sprites.add(self.paste)
        if self.state == 'settings':
            self.header = Image('./assets/img/settings/header.png', 0, 50)
            self.all_sprites.add(self.header)
            self.high = Image('./assets/img/settings/high.png', 45, 150)
            self.all_sprites.add(self.high)
            self.low = Image('./assets/img/settings/low.png', 45, 200)
            self.all_sprites.add(self.low)
            self.collect = Image('./assets/img/settings/collection.png', 45, 250)
            self.all_sprites.add(self.collect)
            self.left_arrow_h = Image('./assets/img/settings/left-arrow.png', 325, 150)
            self.all_sprites.add(self.left_arrow_h)
            self.option_box_l = Surface(355, 150, 65, 40, CHARLESTON_GREEN)
            self.all_sprites.add(self.option_box_l)
            self.right_arrow_h = Image('./assets/img/settings/right-arrow.png', 430, 150)
            self.all_sprites.add(self.right_arrow_h)
            self.left_arrow_l = Image('./assets/img/settings/left-arrow.png', 325, 200)
            self.all_sprites.add(self.left_arrow_l)
            self.option_box_l = Surface(355, 200, 65, 40, CHARLESTON_GREEN)
            self.all_sprites.add(self.option_box_l)
            self.right_arrow_l = Image('./assets/img/settings/right-arrow.png', 430, 200)
            self.all_sprites.add(self.right_arrow_l)
            self.left_arrow_c = Image('./assets/img/settings/left-arrow.png', 325, 250)
            self.all_sprites.add(self.left_arrow_c)
            self.option_box_c = Surface(355, 250, 65, 40, CHARLESTON_GREEN)
            self.all_sprites.add(self.option_box_c)
            self.right_arrow_c = Image('./assets/img/settings/right-arrow.png', 430, 250)
            self.all_sprites.add(self.right_arrow_c)
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
            if self.state == 'track-manual' and event.type == pg.KEYDOWN and event.unicode in DIGITS and len(self.manual_bs_input) <= 2:
                self.manual_bs_input += event.unicode
            if self.state == 'track-dexcom' and event.type == pg.KEYDOWN and len(self.auth_code) < 32:
                self.auth_code += event.unicode
            if self.state == 'track-dexcom' and event.type == pg.KEYDOWN and event.key == K_BACKSPACE:
                self.auth_code = ''
            if self.state == 'track-manual' and event.type == pg.KEYDOWN and event.key == K_BACKSPACE:
                self.manual_bs_input = ''
            if event.type == pg.MOUSEBUTTONUP and self.state == 'settings': 
                mouse_pos = pg.mouse.get_pos()
                if self.left_arrow_h.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['high_setting'] > 120:
                    self.app_settings['high_setting'] -= 5
                elif self.right_arrow_h.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['high_setting'] < 400:
                    self.app_settings['high_setting'] += 5
                
                if self.left_arrow_l.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['low_setting'] > 60:
                    self.app_settings['low_setting'] -= 5
                elif self.right_arrow_l.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['low_setting'] < 100:
                    self.app_settings['low_setting'] += 5

                if self.left_arrow_c.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.app_settings['collection_range'] == 24: self.app_settings['collection_range'] = 12
                    elif self.app_settings['collection_range'] == 48: self.app_settings['collection_range'] = 24
                elif self.right_arrow_c.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.app_settings['collection_range'] == 12: self.app_settings['collection_range'] = 24
                    elif self.app_settings['collection_range'] == 24: self.app_settings['collection_range'] = 48

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

            if pg.mouse.get_pressed()[0] and self.dexcom.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('track-dexcom')
        
        if self.state == 'track-dexcom':
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main')

            if pg.mouse.get_pressed()[0] and self.sign_in.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                dex_int.prompt_login()
            
            if pg.mouse.get_pressed()[0] and self.get_data.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                try:
                    bearer = dex_int.get_bearer(self.auth_code)
                    end_date = self.get_date_time()
                    start_date = self.calc_start_date_time(end_date)
                    data = dex_int.get_egvs(bearer['access_token'], start_date, end_date)
                    with open('data/full_cgm_data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        f.close()
                    self.analyze_cgm_data()
                    self.auth_code = 'DATA WAS SUCCESSFULLY OBTAINED!'
                except:
                    self.auth_code = 'AN ERROR HAS OCCURRED!'

            if pg.mouse.get_pressed()[0] and self.paste.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.auth_code = clipboard.paste()

        if self.state == 'track-manual':
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main')
                if self.manual_bs_data:
                    i = 0
                    while i < len(self.manual_bs_data):
                        self.manual_bs_data[i] = int(self.manual_bs_data[i])
                        i += 1
                with open('data/gv_data.json', 'w') as f:
                    json.dump(self.manual_bs_data, f)
                    f.close()

            if pg.mouse.get_pressed()[0] and self.enter.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.manual_bs_data.append(self.manual_bs_input)
                self.manual_bs_input = ''
                while '' in self.manual_bs_data:
                    self.manual_bs_data.remove('')
        
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
            self.draw_text(self.manual_bs_input, 110, BEIGE, WIDTH / 2, HEIGHT / 2 - 45)
        if self.state == 'track-dexcom':
            self.draw_text(self.auth_code, 32, BEIGE, WIDTH / 2, 272)
        if self.state == 'settings':
            self.draw_text(str(self.app_settings['high_setting']), 32, ASH_GRAY, 387, 152)
            self.draw_text(str(self.app_settings['low_setting']), 32, ASH_GRAY, 387, 202)
            self.draw_text(str(self.app_settings['collection_range']), 32, ASH_GRAY, 387, 252)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen." 
       
        font = pg.font.Font('./assets/font/font.otf', size) # Checks to see if the font is part of Pygame's font library. 
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def state_change(self, new_state: str):

        "Changes the state that the app is on."

        self.state = new_state
        self.new()

    def average_data(data: list):

        "Calculates the average of a list of integers or floats."

        return sum(data) / len(data)

    def get_date_time(self):

        "Gets the current date and time of the system."

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%dT%H:%M:%S")
        return current_time

    def calc_start_date_time(self, date: str):

        "Calculate a date and time based on the apps collection range settings."
        
        hours = int(date[11] + date[12])
        day = int(date[8] + date[9])
        month = int(date[5] + date[6])
        year = int(date[0] + date[1] + date[2] + date[3])
        minutes = date[14] + date [15]
        seconds = date [17] + date[18]
        hours = hours - self.app_settings['collection_range']
        
        if hours < 0:
            if self.app_settings['collection_range'] == 48:
                day -= 2

            else:
                day -= 1
                if int(day) < 10:
                    day = '0' + str(day)

            if self.app_settings['collection_range'] == 12:
                hours += 24

        if int(day) <= 0:
            month -= 1
            if month == 2:
                if year % 400 == 0:
                    if self.app_settings['collection_range'] == 48:
                        month = '0' + str(month)
                        day = 28
                    else:
                        month = '0' + str(month)
                        day = 29
                else:
                    if self.app_settings['collection_range'] == 48:
                        month = '0' + str(month)
                        day = 27
                    else:
                        month = '0' + str(month) 
                        day = 28
            elif month == 0:
                year -= 1
                month = 12
                if self.app_settings['collection_range'] == 48:
                    day = 30
                else:
                    day = 31

            else:
                day = DAYS_IN_MONTHS[month-1]
                if self.app_settings['collection_range'] == 48:
                    day = int(day) - 1
                if month < 10:
                    month = '0' + str(month)
        else:
            month = date[5] + date[6]

        if self.app_settings['collection_range'] == 24 or self.app_settings['collection_range'] == 48:
            hours = date[11] + date[12]
        elif self.app_settings['collection_range'] == 12:
            if hours < 10:
                hours = '0' + str(hours)
            if day < 10:
                day = '0' + str(day)
            
        if self.app_settings['collection_range'] == 48:
            day = '0' + str(day)

        start_date = "{}-{}-{}T{}:{}:{}".format(year, month, day, hours, minutes, seconds)
        return start_date
 
    def analyze_cgm_data(self):
        filtered_data = []
        with open('data/full_cgm_data.json', 'r') as f:
            cgm_data = json.load(f)

        for egv in cgm_data['egvs']:
            filtered_data.append(egv['value'])

        f.close()
        
        with open('data/gv_data.json', 'w') as f:
            json.dump(filtered_data, f)

        f.close()


        

    def load_settings(self):

        "Loads settings from './data/settings.json.'"

        with open('./data/settings.json', 'r') as f:
            settings = json.load(f)

        f.close()
        return settings

    def save_settings(self):

        "Save settings when altered."

        with open('./data/settings.json', 'w') as f:
            json.dump(self.app_settings, f)
            f.close()


