import pygame
### Screen Constants
TILE_SIZE = 64
SCREEN_WIDTH = TILE_SIZE * 16
SCREEN_HEIGHT = TILE_SIZE * 10


### Color Constants
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (20, 20, 20)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BROWN = (160, 100, 60)

### IMAGE FILE NAMES ocated in /images
WALL_IMG_FILENAME = 'tile_11.png'
ZOMBIE_IMG_FILENAME = 'zombie1_hold.png'
PLAYER_IMG_FILENAME = 'manBlue_gun.png'
BULLET_IMG_FILENAME = 'circle_bullet.png'

### PLAYER SETTINGS
PLAYER_SPEED = 250 # pixels per second
PLAYER_ROTATION_SPEED = 200 # degrees per second
GUN_BARREL_OFFSET = pygame.math.Vector2(28, 10)  # a vector to offset the bullets from center of player
PLAYER_HEALTH = 100

### BULLET SETTINGS
BULLET_SPEED = 500
BULLET_LIFE = 1000
FIRE_RATE = 200 # delay in fire
BULLET_SIZE = 10
BULLET_KICKBACK = 50
BULLET_SPREAD = 5
BULLET_DAMAGE = 10
BULLET_KNOCKBACK = 50

### ZOMBIE SETTINGS
ZOMBIE_ACCELERATION = 100 # pixels per second per second
ZOMBIE_HIT_BOX_SIZE = 30 # pixels by pixels
ZOMBIE_FRICTION = 0.4
ZOMBIE_HEALTH = 100
ZOMBIE_DAMAGE = 10
ZOMBIE_KNOCKBACK = 50
