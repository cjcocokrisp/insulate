from types import DynamicClassAttribute
import pygame as pg
import pygame as pg
from pygame import mouse
from pygame.constants import K_BACKSPACE, K_LCTRL, K_v
from game import Game
from settings import *
from sprites import *
import json
import dexcom_integration as dex_int
import clipboard
from datetime import datetime
from advice import *
import random

# This file contains the class of the main application.

class App():

    "Class that handles the main application for Insulate."
    
    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # WIDTH and HEIGHT are used in various places of the program see settings.py for the value.
        pg.display.set_caption('Insulate Development Build')
        self.clock = pg.time.Clock()
        self.state = 'menu-main' # Changes the behavior of appliction based on the value. 
        self.manual_bs_input = ''
        self.manual_bs_data = []
        self.auth_code = ''
        self.bearer_token = ''
        self.app_settings = self.load_settings() # Loads settings from data/settings.json to use throughout the program. 
        self.current_date = self.get_date_time() # Used to see if the user has used the program today.
        self.average = 0
        self.plays_remaining = 0
        game = Game()
        self.game_stats = game.load_stats() # Loads stats to be viewed on the stats screen.
        self.todays_advice = []
        
    def run(self):
        
        "Runs the main loop."
        
        self.events()
        self.update()
        self.draw()

    def new(self):
        
        "Creates the elements that are viewed on screen. Varies based on the value of self.state."
        # The if statements control which elements are drawn based on the state of the program.
        self.all_sprites = pg.sprite.Group()
        if self.state == 'menu-main': # Displays the main menu which allows you to choose what you want to do, check, track, settings, or quit.
            self.logo = Image('./assets/img/logo.png', 0, 35)
            self.check = Image('./assets/img/menu-main/check.png', WIDTH / 2 - 93.5, 240)
            self.track = Image('./assets/img/menu-main/track.png', WIDTH / 2 - 98, 300)
            self.settings = Image('./assets/img/menu-main/settings.png', WIDTH / 2 - 133.5, 360)
            self.quit = Image('./assets/img/menu-main/quit.png', WIDTH / 2 - 69, 420)
            self.help = Image('./assets/img/menu-main/help.png', WIDTH - 56, HEIGHT - 56)
            self.all_sprites.add(self.logo, self.check, self.track, self.settings, self.quit, self.help)
        if self.state == 'menu-track': # Displays the track menu where you can choose which data collection method to use.
            self.header = Image('./assets/img/menu-track/header.png', 0, 0)
            self.manual = Image('./assets/img/menu-track/manual.png', WIDTH / 2 - 90.5 , 220)
            self.dexcom = Image('assets/img/menu-track/dexcom.png', WIDTH / 2 - 160.5, 340)
            self.all_sprites.add(self.header, self.manual, self.dexcom)
        if self.state == 'track-manual': # Displays menu where blood sugars can be manually input. 
            self.header = Image('./assets/img/manual-input/header-' + str(self.app_settings['collection_range']) + '.png', 0, 0) # Changes input prompt based on the collection range setting.
            self.input_box = Surface(WIDTH / 2 - 135, HEIGHT / 2 - 50 , 270, 120, CHARLESTON_GREEN)
            self.enter = Image('./assets/img/manual-input/enter.png', HEIGHT / 2 - 73.5, HEIGHT / 2 + 110)
            self.all_sprites.add(self.header, self.enter, self.input_box)
        if self.state == 'track-dexcom': # Displays menu where blood sugars can be retrieved from the Dexcom API.
            self.header = Image('./assets/img/dexcom-integration/header.png', 0, 25)
            self.sign_in = Image('./assets/img/dexcom-integration/open.png', WIDTH / 2 - 144, 150)
            self.get_data = Image('./assets/img/dexcom-integration/get.png', WIDTH /2 - 108, 375)
            self.input_box = Surface(10, 230, WIDTH - 20, 120, CHARLESTON_GREEN)
            self.paste = Image('./assets/img/dexcom-integration/paste.png', WIDTH - 120, HEIGHT - 37)
            self.all_sprites.add(self.header, self.sign_in, self.get_data, self.input_box, self.paste)
        if self.state == 'menu-check': # Displays the check menu where you can do one of the following, play and check, view your stats, and learn the controls.
            self.header = Image('./assets/img/menu-check/header.png', 0, 20)
            self.start_check = Image('./assets/img/menu-check/check_and_play.png', WIDTH / 2 - 162.5, 200)
            self.stats = Image('./assets/img/menu-check/stats.png', WIDTH / 2 - 173, 280)
            self.how_to = Image('./assets/img/menu-check/how_to_play.png', WIDTH / 2 - 135, 360)
            if self.current_date[0:10] == self.app_settings['last_check']: # Used to display text based on if you have checked today or not.
                self.check_status = Image('./assets/img/menu-check/yes.png', WIDTH - 277, HEIGHT - 30)
            else:
                self.check_status = Image('./assets/img/menu-check/no.png', WIDTH - 328, HEIGHT - 30)
            self.all_sprites.add(self.header, self.start_check, self.stats, self.how_to, self.check_status)
        if self.state == 'check': # Displays the check and play menu which has two options, play and advice.
            self.header = Image('./assets/img/check/header.png', 0, 0)
            self.play = Image('./assets/img/check/play.png', WIDTH / 2 - 55, 240)
            self.advice = Image('./assets/img/check/advice.png', WIDTH / 2 - 77.5, 290)
            self.remaining = Image('./assets/img/check/remaining.png', WIDTH - 304, HEIGHT - 35)
            self.all_sprites.add(self.header, self.play, self.advice, self.remaining)
        if self.state == 'stats': # Displays all things for the stats page.
            self.header = Image('./assets/img/stats/header.png', 0, 0)
            self.back = Image('./assets/img/back.png', WIDTH / 2 - 28, HEIGHT - 56)
            self.all_sprites.add(self.header, self.back)
        if self.state == 'how_to_play': # Displays the controls of the game.
            self.image = Image('./assets/img/how_to_play.png', 0, 0)
            self.back = Image('./assets/img/back.png', WIDTH / 2 - 28, HEIGHT - 56)
            self.all_sprites.add(self.image, self.back)
        if self.state == 'advice': # Displays the advice screen.
            self.header = Image('./assets/img/advice/header.png', 0, 0)
            self.text_box = Surface(20, 100, WIDTH - 40, 330, CHARLESTON_GREEN)
            self.back = Image('./assets/img/back.png', WIDTH / 2 - 28, HEIGHT - 56)
            self.all_sprites.add(self.header, self.text_box, self.back)
        if self.state == 'settings': # Displays the settings page and button options to change them.
            # h stands for high, l stands for low, c stands for collection range.
            self.header = Image('./assets/img/settings/header.png', 0, 50)
            self.high = Image('./assets/img/settings/high.png', 45, 150)
            self.low = Image('./assets/img/settings/low.png', 45, 200)
            self.collect = Image('./assets/img/settings/collection.png', 45, 250)
            self.left_arrow_h = Image('./assets/img/settings/left-arrow.png', 325, 150)
            self.option_box_h = Surface(355, 150, 65, 40, CHARLESTON_GREEN)
            self.right_arrow_h = Image('./assets/img/settings/right-arrow.png', 430, 150)
            self.left_arrow_l = Image('./assets/img/settings/left-arrow.png', 325, 200)
            self.option_box_l = Surface(355, 200, 65, 40, CHARLESTON_GREEN)
            self.right_arrow_l = Image('./assets/img/settings/right-arrow.png', 430, 200)
            self.left_arrow_c = Image('./assets/img/settings/left-arrow.png', 325, 250)
            self.option_box_c = Surface(355, 250, 65, 40, CHARLESTON_GREEN)
            self.right_arrow_c = Image('./assets/img/settings/right-arrow.png', 430, 250)
            self.save = Image('./assets/img/settings/save.png', WIDTH / 2 - 93.5, 350)
            self.all_sprites.add(self.header, self.high, self.low, self.collect, self.left_arrow_h, self.option_box_h, self.right_arrow_h, self.left_arrow_l, self.option_box_l, self.right_arrow_l, self.left_arrow_c, self.option_box_c, self.right_arrow_c, self.save)
        if self.state != 'menu-main' and self.state != 'advice' and self.state != 'how_to_play' and self.state != 'stats': # Displays a back button on the botton left corner of the screen on every screen except on the main menu, advice screen, and stats screen. 
            self.back = Image('./assets/img/back.png', 0, HEIGHT - 56)
            self.all_sprites.add(self.back)
        self.run() # Runs the rest of the loop after creating the screen elements is complete.

    def events(self):
        
        "Handles the various events that may happen in each state of the program."
        
        for event in pg.event.get():
            if event.type == pg.QUIT: # Checks to see if the X on the window title bar is clicked and closes the app if clicked.
                self.running = False
            elif event.type == pg.KEYDOWN: # Same as the other one except it deals with the escape key.
                if event.key == pg.K_ESCAPE:
                    self.running = False
            # The code below deals with typing on the manual screen for manual blood sugar input and typing on the Dexcom screen to input your authcode.
            if self.state == 'track-manual' and event.type == pg.KEYDOWN and event.unicode in DIGITS and len(self.manual_bs_input) < 3: # Checks to see if the keyboard input was a number and no more then 3 digits. 
                self.manual_bs_input += event.unicode # event.unicode is what is typed on the keyboard. 
            if self.state == 'track-dexcom' and event.type == pg.KEYDOWN and len(self.auth_code) < 32: # Same as before but instead allows letters and the max length is 32 characters because that is the authcode length.
                self.auth_code += event.unicode
            if self.state == 'track-dexcom' and event.type == pg.KEYDOWN and event.key == K_BACKSPACE: # Resets the input. 
                self.auth_code = ''
            if self.state == 'track-manual' and event.type == pg.KEYDOWN and event.key == K_BACKSPACE: # Resets the input.
                self.manual_bs_input = ''
            # The code below deals with the user pressing the play button on the check screen.
            # It is here instead of update because update is for things that don't linger in one spot. 
            # If this was in update it would press the button multiple times and play right after you lost if plays remain. 
            if self.state == 'check':
                mouse_pos = pg.mouse.get_pos()
                if event.type == pg.MOUSEBUTTONUP and self.play.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.plays_remaining > 0:
                    game = Game() # See game.py for how the Game class works.
                    while game.running:
                        game.new()
                    self.game_stats = game.load_stats() # Updates loaded game stats when a game is complete. 
                    self.plays_remaining -= 1 # See update for more information on how plays are distributed.
            # The code below deals with the buttons on the setting screen.
            if event.type == pg.MOUSEBUTTONUP and self.state == 'settings': 
                # mouse_pos is here for the same reason as the previous logic block.
                mouse_pos = pg.mouse.get_pos()
                # Allows user to adjust high setting. The lowest it can go is 120 and the highest is 400.
                if self.left_arrow_h.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['high_setting'] > 120:
                    self.app_settings['high_setting'] -= 5
                elif self.right_arrow_h.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['high_setting'] < 400:
                    self.app_settings['high_setting'] += 5
                # Allows user to adjust low settings. The lowest it can go is 60 and the highest it can go is 100. 
                if self.left_arrow_l.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['low_setting'] > 60:
                    self.app_settings['low_setting'] -= 5
                elif self.right_arrow_l.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.app_settings['low_setting'] < 100:
                    self.app_settings['low_setting'] += 5
                # Both of the mins and maxs for the high and low setting are based on the mins and maxs of the Dexcom.
                # Below deals with updating the collection range of the Dexcom API data that is recieved. 
                # The three options are 12, 24, and 48.
                if self.left_arrow_c.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.app_settings['collection_range'] == 24: self.app_settings['collection_range'] = 12
                    elif self.app_settings['collection_range'] == 48: self.app_settings['collection_range'] = 24
                elif self.right_arrow_c.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.app_settings['collection_range'] == 12: self.app_settings['collection_range'] = 24
                    elif self.app_settings['collection_range'] == 24: self.app_settings['collection_range'] = 48

    def update(self):
        
        "Updates the program based on the elements and state of the program."
        
        self.all_sprites.update() 
        mouse_pos = pg.mouse.get_pos()
        if self.state == 'menu-main': # Deals with the clickable elements on the main menu. 
            if pg.mouse.get_pressed()[0] and self.quit.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.running = False # Closes application. 
            
            if pg.mouse.get_pressed()[0] and self.check.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-check') # Brings you to the check menu.

            if pg.mouse.get_pressed()[0] and self.track.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-track') # Brings you to the track menu. 

            if pg.mouse.get_pressed()[0] and self.settings.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('settings') # Brings you to the settings menu.

        if self.state == 'menu-track': # Deals with the elements on the track menu.
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main') # Brings you back to the main menu.
            
            if pg.mouse.get_pressed()[0] and self.manual.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('track-manual') # Brings you to the manual input screen. 

            if pg.mouse.get_pressed()[0] and self.dexcom.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('track-dexcom') # Brings you to the Dexcom collection screen. 
        
        if self.state == 'track-dexcom': # Deals with the elements on the Dexcom track screen. 
            # This screen uses the Dexcom API for more information on how the code.
            # For more information on the functions that use the API see dexcom_integration.py.
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main') # Brings you back to the main menu.

            if pg.mouse.get_pressed()[0] and self.sign_in.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                dex_int.prompt_login() 
            
            if pg.mouse.get_pressed()[0] and self.get_data.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                try: # Uses the auth code inputted to get the data from the API. 
                    bearer = dex_int.get_bearer(self.auth_code)
                    end_date = self.get_date_time()
                    start_date = self.calc_start_date_time(end_date)
                    data = dex_int.get_egvs(bearer['access_token'], start_date, end_date)
                    with open('data/full_cgm_data.json', 'w') as f: # Saves the data retrieved to be filtered. 
                        json.dump(data, f, indent=4)
                        f.close()
                    self.filter_cgm_data() # There is more data that the API provides that is not needed. This function filters it to what is needed.
                    self.auth_code = 'DATA WAS SUCCESSFULLY OBTAINED!'
                except:
                    self.auth_code = 'AN ERROR HAS OCCURRED!' # Returns an error if something goes wrong. 
                    # Things that can go wrong include, inputing expired or wrong auth code and not being connected to the internet. 

            if pg.mouse.get_pressed()[0] and self.paste.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.auth_code = clipboard.paste() # Pastes the user's system clipboard into the auth code variable.

        if self.state == 'track-manual': # Deals with the elements on the manual track screen. 
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main') # Returns user to main menu.
                if self.manual_bs_data: 
                    i = 0
                    while i < len(self.manual_bs_data):
                        self.manual_bs_data[i] = int(self.manual_bs_data[i]) # Because the event.unicode is a string it converts all of the values that were added to te list to a integer.
                        i += 1
                with open('data/gv_data.json', 'w') as f: # Saves the list of integers to data/gv_data.json.
                    json.dump(self.manual_bs_data, f)
                    f.close()

            if pg.mouse.get_pressed()[0] and self.enter.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.manual_bs_data.append(self.manual_bs_input) # Appends input to the list of manually input values. 
                self.manual_bs_input = '' # Resets the inputed value to a blank string.
                while '' in self.manual_bs_data:
                    self.manual_bs_data.remove('') # When the user clicks the enter button it will sometimes input blank strings. This removes those from the list.
        
        if self.state == 'menu-check': # Deals with the elements on the check menu screen.
            
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main') # Brings the user back to the main menu.

            if pg.mouse.get_pressed()[0] and self.start_check.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if self.app_settings['last_check'] != self.current_date[0:10]: # If the date in self.app_settings['last_check'] is the same as todays date then you can not check because there is a limit of once per day.
                    self.state_change('check') # Brings you to the check and play screen. 
                    data = self.load_bs_data() # Loads the saved values of blood sugars. 
                    if not data: # If the list is empty makes the average none and makes a note of that there was no data. This will make it so the last check date will not update so the user can go back when data is collected.
                        self.average = "NONE"
                        self.no_data = True
                    else:
                        self.average = self.average_data(data) # Gets the average of the blood sugars. 
                        if self.average >= self.app_settings['high_setting'] or self.average <= self.app_settings['low_setting']: # If the average is high or low the user will get one play at the reward game. 
                            self.plays_remaining = 1
                        else: # If the blood sugar is in range the user will get three plays at the reward game. 
                            self.plays_remaining = 3
                        self.get_advice() # Picks the advice for the day. 
                        self.no_data = False
                            
            if pg.mouse.get_pressed()[0] and self.stats.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('stats') # Brings you to the stats page. 
                
            if pg.mouse.get_pressed()[0] and self.how_to.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('how_to_play') # Brings you to the how to play screen. 
                
        if self.state == 'check': # Deals with elements on the check and play screen.
            
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main') # Brings you back to the main menu.
                if not self.no_data: # Only updates the last check data if there is data. 
                    self.app_settings['last_check'] = self.current_date[0:10]
                    self.save_settings()
                # If the user comes to this screen before inputting data there is nothing to do here. Advice will not be viewable too. 
            if pg.mouse.get_pressed()[0] and self.advice.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.no_data == False:
                self.state_change('advice') # Brings you to the advice screen. 
                
        if self.state == 'stats': # Deals with elements on the stats screen. 
            
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-check') # Brings you back to the check menu.
                
        if self.state == 'how_to_play': # Deals with elements on the how to play screen. 

            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-check') # Brings you back to the check menu. 

        if self.state == 'advice': # Deals with elements on the advice screen. 
            
            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('check') # Brings you back to the check and play screen. 
                                                          
        if self.state == 'settings': # Deals with elements on the settings page.

            if pg.mouse.get_pressed()[0] and self.back.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state_change('menu-main') # Brings you back to the main menu.
                
            if pg.mouse.get_pressed()[0] and self.save.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.save_settings() # Saves your settings when the save button is pressed. 

    def draw(self):
        
        "Draws elements and text to the screen."
        
        self.screen.fill(ASH_GRAY) # Background color throughout the app. 
        self.all_sprites.draw(self.screen) # Draws every sprite to the screen.
        if self.state == 'check' and self.average != 'NONE': # Draws the text for the blood sugar average and plays remaining on the check and play screne.
            self.draw_text(str(round(self.average, 2)), 64, CHARLESTON_GREEN, 370, 80) # Rounds the average to two decimal places.
            self.draw_text(str(self.plays_remaining), 39, CHARLESTON_GREEN, WIDTH - 28, HEIGHT - 32)
        elif self.state == 'check': # Displays none instead of an average if no data is displayed. 
            self.draw_text("NONE", 64, CHARLESTON_GREEN, 370, 68)
            self.draw_text('0', 39, CHARLESTON_GREEN, WIDTH - 28, HEIGHT - 36)
        if self.state == 'track-manual': # Displays keyboard inputs on the manual screen.
            self.draw_text(self.manual_bs_input, 110, BEIGE, WIDTH / 2, HEIGHT / 2 - 25)
        if self.state == 'track-dexcom': # Displays keyboard inputs on the dexcom screen.
            self.draw_text(self.auth_code, 32, BEIGE, WIDTH / 2, 272)
        if self.state == 'stats': # Displays game stats on the statistics page.
            self.draw_text("High Score: " + str(self.game_stats['high_score']), 55, CHARLESTON_GREEN, WIDTH / 2, 120)
            self.draw_text("Total Score: " + str(self.game_stats['total_score']), 55, CHARLESTON_GREEN, WIDTH / 2, 170)
            self.draw_text("Coins Collected: " + str(self.game_stats['total_coins_collected']), 50, CHARLESTON_GREEN, WIDTH / 2, 220)
            self.draw_text("Enemies Defeated: " + str(self.game_stats['total_enemies_defeated']), 50, CHARLESTON_GREEN, WIDTH / 2, 270)
            self.draw_text("Games Played: " + str(self.game_stats['games_played']), 55, CHARLESTON_GREEN, WIDTH / 2, 320)
        if self.state == 'settings': # Displays the current settings on the settings screen.
            self.draw_text(str(self.app_settings['high_setting']), 32, ASH_GRAY, 387, 152)
            self.draw_text(str(self.app_settings['low_setting']), 32, ASH_GRAY, 387, 202)
            self.draw_text(str(self.app_settings['collection_range']), 32, ASH_GRAY, 387, 252)
        if self.state == 'advice': # Displays the advice from the todays_advice list. For how this works see advice.py. 
            self.draw_text(self.todays_advice[0], 32, BEIGE, WIDTH / 2, 110)
            self.draw_text(self.todays_advice[1], 32, BEIGE, WIDTH / 2, 140)
            self.draw_text(self.todays_advice[2], 32, BEIGE, WIDTH / 2, 170)
            self.draw_text(self.todays_advice[3], 32, BEIGE, WIDTH / 2, 200)
            self.draw_text(self.todays_advice[4], 32, BEIGE, WIDTH / 2, 230)
            self.draw_text(self.todays_advice[5], 32, BEIGE, WIDTH / 2, 260)
            self.draw_text(self.todays_advice[6], 32, BEIGE, WIDTH / 2, 290)
            self.draw_text(self.todays_advice[7], 32, BEIGE, WIDTH / 2, 320)
            self.draw_text(self.todays_advice[8], 32, BEIGE, WIDTH / 2, 350)
            self.draw_text(self.todays_advice[9], 32, BEIGE, WIDTH / 2, 380)
        pg.display.flip() # Displays everything on the screen.

    def draw_text(self, text, size, color, x, y):
        
        "Draws the text to the screen." 
       
        font = pg.font.Font('./assets/font/font.otf', size) # Gets the font data from the otf file.
        text_surface = font.render(text, True, color) # Renders the text with the color that was selected. 
        text_rect = text_surface.get_rect() 
        text_rect.midtop = (x, y) # Sets the texts position. 
        self.screen.blit(text_surface, text_rect)

    def state_change(self, new_state: str):

        "Changes the state that the app is on."

        self.state = new_state
        self.new() # Resets the main loop so that the new elements can be drawn to the screen.

    def average_data(self, data: list):

        "Calculates the average of a list of integers or floats."

        return sum(data) / len(data) # Averages the data by doing sum of the data divided by the number of the items in the data.

    def get_date_time(self):

        "Gets the current date and time of the system."

        now = datetime.now() 
        current_time = now.strftime("%Y-%m-%dT%H:%M:%S") # Formats the date to the same as the Dexcom APIs date inputs
        return current_time

    def calc_start_date_time(self, date: str):

        "Calculate a date and time based on the apps collection range settings from the format that the Dexcom API uses."
        
        # Singles out the hours, day, month, year, minutes, and seconds. 
        hours = int(date[11] + date[12])
        day = int(date[8] + date[9])
        month = int(date[5] + date[6])
        year = int(date[0] + date[1] + date[2] + date[3])
        minutes = date[14] + date [15]
        seconds = date [17] + date[18]
        hours = hours - self.app_settings['collection_range'] # Calculates the new hour based on the collection range.
        
        if hours < 0: # Changes the date if hours is less then 0. 
            if self.app_settings['collection_range'] == 48:
                day -= 2
            else:
                day -= 1
                if int(day) < 10:
                    day = '0' + str(day)

            if self.app_settings['collection_range'] == 12:
                hours += 24 # Makes the hour correct if collection range is 12 hours. For example if you get at 8 AM when 12 is subtracted you will get -4 adding 24 will give you 20 which is 8 PM in 24 hour time. 

        if int(day) <= 0: # Changes the month if the day is less then 0. 
            month -= 1
            if month == 2: # If the month is changed to Feburary calculates the new day for the month based on if it is a leap year or not. 
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
            elif month == 0: # If the month is changed to 0 then subtracts the year by 1 and sets month to 12.
                year -= 1
                month = 12
                if self.app_settings['collection_range'] == 48:
                    day = 30
                else:
                    day = 31

            else:
                day = DAYS_IN_MONTHS[month-1] # Because every month that isn't Feburary has a static number of days uses a list of days in a month to change the date. 
                if self.app_settings['collection_range'] == 48:
                    day = int(day) - 1
                if month < 10: # Adds a 0 in front of the month if it is less then 10 because the API needs a 0 in front of a single digit month. 
                    month = '0' + str(month)
        else:
            month = date[5] + date[6] # If the day is not 0 uses the same month as what it started with. 

        if self.app_settings['collection_range'] == 24 or self.app_settings['collection_range'] == 48:
            hours = date[11] + date[12] # If the collection range is the 24 or 48 uses the same time as what is input. 
        elif self.app_settings['collection_range'] == 12: # Adds 0s in front of the hour and days if the collection range is 12.
            if hours < 10:
                hours = '0' + str(hours) 
            if day < 10:
                day = '0' + str(day)
            
        if self.app_settings['collection_range'] == 48: # Adds a 0 in front of the hour if the collection range is 48. 
            day = '0' + str(day)

        start_date = "{}-{}-{}T{}:{}:{}".format(year, month, day, hours, minutes, seconds) # Formats the new date. 
        return start_date
 
    def filter_cgm_data(self):
        
        "Filters data from the data retrieved based on the Dexcom API."
        
        filtered_data = [] 
        with open('data/full_cgm_data.json', 'r') as f: # Opens the data that was retrieved from the CGM to make sure it exists. 
            cgm_data = json.load(f) 

        for egv in cgm_data['egvs']: # Takes all the egvs values from the dictionary and appends it to the filtered_data list. 
            filtered_data.append(egv['value'])

        f.close()
        
        with open('data/gv_data.json', 'w') as f: # Saves the filtered data. 
            json.dump(filtered_data, f)

        f.close()

    def load_bs_data(self):
        
        "Load blood sugars from 'gv_data.json.'"
        
        with open('./data/gv_data.json', 'r') as f: # Loads the saved blood sugar data. 
            data = json.load(f)
        
        f.close()
        return data

    def load_settings(self):

        "Loads settings from './data/settings.json.'"

        with open('./data/settings.json', 'r') as f: # Loads the saved settings. 
            settings = json.load(f)

        f.close()
        return settings

    def save_settings(self):

        "Save settings when altered."

        with open('./data/settings.json', 'w') as f: # Saves the settings. 
            json.dump(self.app_settings, f, indent=4)
            f.close()
            
    def get_advice(self):
        
        "Gets random advice depending on blood sugars average. See advice.py for all of the advice that is viewable."
        
        # Checks what list that the program needs to use based on the blood sugar average. 
        if self.average >= self.app_settings['high_setting']: 
            result = HIGH
        elif self.average <= self.app_settings['low_setting']:
            result = LOW
        else:
            result = IN_RANGE
        
        for x in result[random.randint(0, len(result) - 1)]: # Appends each line of the advice into the todays advice list based on a randomly generated number.
            self.todays_advice.append(x)