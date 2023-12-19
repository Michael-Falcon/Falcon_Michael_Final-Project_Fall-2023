
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

    
   


'''import pygame as pg
import math
from pygame.math import Vector2 as vec
from utils import  blit_rotate_center
import os

from pygame.sprite import Sprite

import os
from settings import *
from sprites import *
import math
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Your Game Title")
pg.init()


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')



# Assuming the 'img_folder' variable is defined somewhere in your code


class AbstractCar:
    def __init__(self, max_vel, rotation_vel, game ):
        self.img = img_folder
        Sprite.__init__(self)
        self.game = game
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pg.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class Player(AbstractCar):
    img_folder = pg.image.load(os.path.join(img_folder, 'mitsubishi2.png')).convert()

    START_POS = (180, 200)

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("I can jump")
            self.vel.y = -PLAYER_JUMP

    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rotate(left=True)
        if keys[pg.K_d]:
            self.rotate(right=True)
        if keys[pg.K_w]:
            self.move_forward()
        if keys[pg.K_s]:
            self.move_backward()

    def update(self):
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if mhits:
            self.score = 1
        self.acc = vec(0, PLAYER_GRAV)
        self.controls()
        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


class Mob(AbstractCar):
    img_folder = pg.image.load(os.path.join(img_folder, 'purple-car.png')).convert()
    START_POS = (150, 200)

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
            self.rect.x += self.speed / 3
            if self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0:
                self.speed = -self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed 

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
'''
