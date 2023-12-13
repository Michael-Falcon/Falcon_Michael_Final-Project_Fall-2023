#This file was created by Michael Falcon 
#Sources: 
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

# content from kids can code: http://kidscancode.org/blog/
# content from classmates: Miguel, 
#GamdeDesign:
#Goals: achieve a score of 50, eliminate all the mobs, avoid 
#Rules: Jump, move both directions, 
#Feedback: score at top, sound effects, 

#Feature Goals 
#make the mobs 
# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
from math import floor
import math

# a;skjdfj;sakdf

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_raindrops = pg.sprite.Group()
        
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        
        '''for m in MONSTER_LIST:
            mob = Mob(*m)
            self.all_sprites.add(mob)
            self.all_mobs.add(mob)
        
        self.run()'''

        for m in range(0,12):
            m = Mob(randint(0,WIDTH), randint(0,HEIGHT - 150), 25, 25, "move")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        for r in range(0, 15): 
            r = Rain(randint(0,WIDTH), randint(0,HEIGHT), 5, 40, "acid")
            self.all_sprites.add(r)
            self.all_raindrops.add(r)

        self.run()
        
       
        
        '''for m in range(0,5):
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()'''

        

        
        
        

        
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
    


        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top:
                    self.player.rect.top = hits[0].rect.bottom
        elif self.player.vel.y <= 0: 
            mhits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if mhits:
                self.player.acc = 5
                self.player.vel.y = 0
                self.score += 1 
                if self.player.rect.bottom >= hits[0].rect.top + 1:
                    self.player.rect.top = hits[0].rect.bottom
                    

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()

