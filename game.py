import pygame
from pygame import display
import random
from threading import Timer
import sys
import random

#Vector
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

windowv = Vector(736, 640)

class Spritesheet(object):
    def __init__(self, filename, sprite_height = 32, sprite_width = 32):
        self.sheet = pygame.image.load(filename).convert()
        self.imgRect = pygame.Rect(0, 0, sprite_width, sprite_height)
        self.img_list = []
        self.rows = self.sheet.get_height() // sprite_height
        self.columns = self.sheet.get_width() // sprite_width

        for i in range(self.columns):
            self.img_list.append([])
            for j in range(self.rows):
                self.imgRect.x = 32 * j
                self.img_list[i].append(self.sheet.subsurface(self.imgRect))
            self.imgRect.y += 32
        




                



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
background = WHITE
 
#Window
pygame.init()
size = (windowv.x, windowv.y) # Set the width and height of the screen [width, height]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock() # Used to manage how fast the screen updates
 
#Loop
done = False


#Images
slime_img = pygame.image.load('resources/Slime_Sprite.png')
player_img = pygame.image.load('resources/Player_Sprite.png')

#Sound
def hit_sound():
    pygame.mixer.music.load('resources/Hit.wav')
    pygame.mixer.music.play(1)

#Handeling Events
direction = Vector(0,0) #Input Vector
attack = False
def update_dir_vector(event):
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            direction.x -= 1
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            direction.x += 1
        if event.key == pygame.K_UP or event.key == ord('w'):
            direction.y += 1
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            direction.y -= 1
        if event.key == pygame.K_RETURN:
            global attack
            attack = True


    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            direction.x = 0
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            direction.x = 0
        if event.key == pygame.K_UP or event.key == ord('w'):
            direction.y = 0
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            direction.y = 0

def within(v1,v2,r):
    return((v1.x-v2.x)**2 + (v1.y-v2.y)**2 < r**2)

def display_number(value, position):
        '''Displays a number on that tile'''
        font = pygame.font.SysFont('arial', 30)
        text = font.render(str(value), True, (0, 0, 0))
        screen.blit(text, position)

#Entities
entities = []
class Entity():
    def __init__(self, image, initial_vector = Vector(size[0]/2,size[1]/2), stats={"speed": 3, "hp": 9}):
        entities.append(self)
        image = pygame.transform.scale(image, (70, 70))
        self.image = image
        self.x = initial_vector.x
        self.y = initial_vector.y
        self.hp = stats["hp"]
        self.speed = stats["speed"]
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        display_number(round(self.hp), (self.x, self.y))
    def take_damage(self, dealt_dammage):
        #Take away the hp
        self.hp -= dealt_dammage
        #Check dead
        if(self.hp<=0):
            entities.remove(self)
            self.die()
        hit_sound()
    def move(self, vector):
        self.x += vector.x * self.speed
        self.y -= vector.y * self.speed

##Player
player_entity = None
player_damage=5
player_range =30
def updatePlayer():
    #Move Player
    player_entity.move(direction)

    #If the attack flag is triggered damage entities around it
    global attack
    if(attack):
        attack = False
        for e in entities:
            if e==player_entity:
                continue
            if within(e,player_entity,player_range):
                e.take_damage(3)

def player_die():
    global done
    done=True

def revive():
    global player_entity
    player_entity = Entity(player_img)
    player_entity.update = updatePlayer
    player_entity.die = player_die
revive()

##Monsters
class Slime:
    def __init__(self, initial_vector = Vector(0,0)):
        self.monster_entity = Entity(pygame.image.load('resources/Slime_Sprite.png'), initial_vector, {"hp": 1, "speed": 0.5+random.random()})
        self.monster_entity.update = self.updateMonster
        self.monster_entity.die = lambda: None
    def updateMonster(self):
        #get direction to player
        dir_to_player_x = 0 if abs(self.monster_entity.x - player_entity.x) < 2 else (-1 if self.monster_entity.x < player_entity.x else 1)
        dir_to_player_y = 0 if abs(self.monster_entity.y - player_entity.y) < 2 else (-1 if self.monster_entity.y < player_entity.y else 1)

        #move towards player
        self.monster_entity.move(Vector(-dir_to_player_x, dir_to_player_y))

        #if slime is within range of the player, hit the player
        global background
        background = WHITE
        if within(self.monster_entity, player_entity, 10):
            background = RED
            self.monster_entity.x += 40*dir_to_player_x
            self.monster_entity.y += 40*dir_to_player_y
            player_entity.take_damage(1)


def spawn_slime():
    vec = Vector(random.random()*size[0], random.random()*size[1])
    if(random.random()>0.5):
        vec.x=0
    
    Slime(vec)
    t = Timer(0.5, spawn_slime)
    t.start()
spawn_slime()



class Background:
    def __init__(self):
        self.sp = Spritesheet("resources/Wall_Floor_Spritesheet.png")
        self.bg = []
    def newBackground(self):
        for i in range(0, 20):
            list = []
            for j in range(0, 23):
                num = random.randrange(0, 16)
                if num < 10:
                    list.append(self.sp.img_list[2][2])
                elif num < 13:
                    list.append(self.sp.img_list[1][random.randrange(0, 2)])
                elif num < 15:
                    list.append(self.sp.img_list[2][random.randrange(0, 2)])
                elif num == 15:
                    list.append(self.sp.img_list[0][random.randrange(0, 2)])            
            self.bg.append(list)
    def renderBackground(self):
        for i in range(0, 20):
            for j in range(0, 23):
                screen.blit(self.bg[i][j], (j * 32, i * 32))

bg = Background()
bg.newBackground()
# -------- Main Program Loop -----------
while not done:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        update_dir_vector(event)
    
    #Updating Entities
    for e in entities:
        e.update()

    #Drawing Entities
#    screen.fill(background)    #Background
    bg.renderBackground()
    
    for e in entities:  #Draw Sprites
        e.draw()
    pygame.display.flip() #Update

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.

pygame.quit()
sys.exit()