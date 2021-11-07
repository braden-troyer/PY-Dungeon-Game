import pygame

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
#Images
slime = pygame.image.load('resources/Slime_Sprite.png')


# North, East, South, West
direction = {False, False, False, False}


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                direction[0] = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                direction[1] = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                direction[2] = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                direction[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                direction[0] = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                direction[1] = False
            if event.key == pygame.K_UP or event.key == ord('w'):
                direction[2] = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                direction[3] = False
            
        if event.type == pygame.QUIT:
            done = True

    # Set the velocity vector
    velocity = Vector(0, 0)

    if direction[0]:
        velocity.y -= 1
    if direction[1]:
        velocity.y += 1
    if direction[2]:
        velocity.y += 1
    if direction[3]:
        velocity.x -= 1


    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    screen.blit(slime, (10,10))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()