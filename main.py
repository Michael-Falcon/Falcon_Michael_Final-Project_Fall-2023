#This file was created by Michael Falcon 
#Sources: chatgpt, (kids can code), 
#Overview: explain what you want to create What is something you're passionate about or interested in?  How can you apply python and its many libraries towards that interest in your final project?

#Include a main.py file with comments including project title and goals.
'''
project title: Death Race(I want to create a game similr to mario cart but with mroe realistic options such as the 
user losign health. The point of the game is to win the race but also not to die 
#I am amakeing a change 
more specfic gaols: 
    need to make cars powerslide and drift 
    allow cars to ineract with other classes (in this case certain classes can be picked up or thrown )
    create healthabr for user
    add a class for extra boost 
    allow for realistic feedback(like if two cars were to crash into each other then they would explode)
    create npc's that will partake in race and not only hurt the user but other npcs 
    allow for backgroudn to move with user 
    
'''
#Second push test 
#fragnraio

# content from kids can code: http://kidscancode.org/blog/; youtube vids: https://www.youtube.com/watch?v=GiUGVOqqCKg
#Github links:https://github.com/clickclackcode/python-car-game/blob/main/car_game.py, https://github.com/randhir408/sourceofcargame/blob/main/game.py, https://github.com/techwithtim/Pygame-Car-Racer/blob/main/tutorial4-code/main.py, 
# content from classmates: Miguel, 
#GamdeDesign:
#Goals: achieve a score of 50, eliminate all the mobs, avoid 
#Rules: Jump, move both directions, 
#Feedback: score at top, sound effects, 

#Feature Goals 
#make the mobs 
# import libraries and modules
'''


'''




from turtle import speed
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
from math import floor
import math

vec = pg.math.Vector2

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Scrolling background")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.score = 0 
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.background = pg.image.load(os.path.join(img_folder, 'Road Png-Resize.png')).convert()
        self.all_raindrops = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        #make the mobs appear
        for m in range(0, 30):
            m = Mob(randint(0, WIDTH), randint(0, HEIGHT - 150), 25, 25, "move")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        #make the rain appear
        for r in range(0, 20):
            r = Rain(randint(400, 1250), randint(0, HEIGHT), 5, 40, "acid")
            self.all_sprites.add(r)
            self.all_raindrops.add(r)

        self.run()

    def run(self):
        self.playing = True
        #where the background starts
        bg_scroll = -500
        #rate at which background goes up
        scroll_speed = 6

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw(bg_scroll)
            bg_scroll += scroll_speed
            #saying that if the background reaches more than 50 then it must reset to -600
            if bg_scroll > 50:
                bg_scroll = -600

    def update(self):
        self.all_sprites.update()
        #makes the cars disappear
        mhits = pg.sprite.spritecollide(self.player, self.all_mobs, True)
        if mhits:
                self.player.acc = 1
                self.player.vel.y = 0
                self.score += 2.5 
        #makes the score drop if you hit an acid raindrop 
        rhits = pg.sprite.spritecollide(self.player, self.all_raindrops, False)
        if rhits:
                self.player.acc = .5
                self.player.vel.y = 0 
                self.score -= .25
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed * 1

        # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.acc.y = 1
                self.player.vel.y = 0
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top:
                    self.player.rect.top = hits[0].rect.bottom
        #elif self.player.vel.y <= 0:
            
                
                #if self.player.rect.bottom >= hits[0].rect.top + 1:
                    #self.player.rect.top = hits[0].rect.bottom

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    #making the backgorund screen display 
    def draw(self, bg_scroll):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, -bg_scroll))

        self.all_sprites.draw(self.screen)
        #adding the score that will show
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 10)

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

# Instantiate and run the game
g = Game()
while g.running:
    g.new()

pg.quit()
