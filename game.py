import pygame
from pygame import display
import move

#Vector
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
background = WHITE
 
#Window
pygame.init()
size = (700, 500) # Set the width and height of the screen [width, height]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock() # Used to manage how fast the screen updates
 
#Loop
done = False


#Images
slime_img = pygame.image.load('resources/Slime_Sprite.png')
player_img = pygame.image.load('resources/Player_Sprite.png')

#Handeling Events
direction = Vector(0,0) #Input Vector
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
    def __init__(self, image, initial_vector = Vector(0,0), hp=5):
        entities.append(self)
        image = pygame.transform.scale(image, (70, 70))
        self.image = image
        self.x = initial_vector.x
        self.y = initial_vector.y
        self.hp = hp
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        display_number(round(self.hp), (self.x, self.y))
    def take_damage(self, dealt_dammage):
        self.hp -= dealt_dammage

#Get Mobs
#def get_mobs():
    #return(filter())

##Player
player_entity = Entity(player_img, Vector(50,50))
def updatePlayer():
    player_entity.x += direction.x
    player_entity.y -= direction.y
player_entity.update = updatePlayer


##Monsters
monster_entity = Entity(slime_img)
def updateMonster():
    #get direction to player
    dir_to_player_x = -0.5 if monster_entity.x < player_entity.x else 0.5
    dir_to_player_y = -0.5 if monster_entity.y < player_entity.y else 0.5

    #move towards player
    monster_entity.x -= dir_to_player_x
    monster_entity.y -= dir_to_player_y

    #if slime is within range of the player, hit the player
    global background
    background = WHITE
    if within(monster_entity, player_entity, 10):
        background = RED
        monster_entity.x += 40*dir_to_player_x
        monster_entity.y += 40*dir_to_player_y
        player_entity.take_damage(1)

monster_entity.update = updateMonster





# -------- Main Program Loop -----------
while not done:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        update_dir_vector(event)
        
    #handle game events
    #move.handle_events(player_entity, direction)

    #Updating Entities
    for e in entities:
        e.update()

    #Drawing Entities
    screen.fill(background)    #Background
    for e in entities:  #Draw Sprites
        e.draw()
    pygame.display.flip() #Update

    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()