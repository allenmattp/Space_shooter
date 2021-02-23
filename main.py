"""
 Show how to fire bullets.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/PpdJjaiLX6A
"""
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# --- Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("block.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0

        # Instance variables for our current speed and direction
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right > self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("bullet.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3


# --- Create the window

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

# Background impage
background_image = pygame.image.load("background.jpg").convert()

# Sound
click_sound = pygame.mixer.Sound("laser.ogg")

# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites

for i in range(50):
    # This represents a block
    block = Block()

    # Set a random location for the block
    block.rect.x = random.randrange(25, screen_width - 25)
    block.rect.y = random.randrange(screen_height - 150)

    block.change_x = random.randrange(-3, 4)
    block.change_y = random.randrange(-3, 4)
    block.left_boundary = 0
    block.top_boundary = 0
    block.right_boundary = screen_width
    block.bottom_boundary = screen_height

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block
player = Player()
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide mouse cursor
pygame.mouse.set_visible(0)

score = 0
player.rect.y = screen_height - 100

# Stars
star_list = []
for i in range(2000):
    x = random.randrange(0, screen_width)
    y = random.randrange(0, screen_height + 25)
    star_list.append([x, y])

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x + 42
            bullet.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)


    # --- Game logic

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            score_text = int(score)
            print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # --- Draw a frame

    # Clear the screen
    screen.blit(background_image, [0, 0])

    # Draw all the spites
    if score == 50:
        font = pygame.font.SysFont("serif", 50)
        text = font.render("CONGRATULATIONS YOU WIN", True, WHITE)
        center_x = (screen_width // 2) - (text.get_width() // 2)
        center_y = (screen_height // 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

    else:
        all_sprites_list.draw(screen)

    # Starfield
    for i in range(len(star_list)):
        pygame.draw.circle(screen, WHITE, star_list[i], 1)
        star_list[i][1] -= 1
        if star_list[i][1] < 0:
            y = random.randrange(screen_height + 10, screen_height + 50)
            star_list[i][1] = y
            x = random.randrange(0, screen_width)
            star_list[i][0] = x

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()