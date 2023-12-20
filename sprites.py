
import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *
from sprites import *
import math


# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'porsche .png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, 800)
        self.vel = vec(0,0)
        self.acc = vec(1,2)
        self.score = 0
    #all the keys that allow me to contrl how fast car is goign foward, back, sideways
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -8
        if keys[pg.K_d]:
            self.acc.x = 8
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_w]:
            self.acc.y = -.15
        if keys[pg.K_s]:
            self.acc.y = .5
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
        
    def update(self):
         #CHECKING FOR COLLISION WITH MOBS HERE>>>>>
        #mhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        #if mhits: 
            #self.score += 1
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms
#i left this class the same as before 
class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 10
        
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
 #Mobs 
#i did the same thing with this class  
class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'purple-car.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.speed = 0
        if self.kind == "move":
            self.speed = 16
        
    def update(self):
        if self.kind == "move":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
 #Acid Rain 
#one of the things I changed from this class i made was that I disabled the rain droplets from moving left to right
class Rain(Sprite):
    def __init__(self, x, y, w, h, type):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.x = x
        self.rect.y = y
        speed = 0 
        if self.type == "acid":
            self.speed = 8
    
    def update(self):
        if self.type == "acid":
            self.rect.y += self.speed
            #self.rect.x += self.speed / 3
            if self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0:
                self.speed = -self.speed
            #if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                #self.speed = -self.speed 


#self.pos = vec(WIDTH/2, HEIGHT/2)

    #def update(self):
       # pass 

    
   


