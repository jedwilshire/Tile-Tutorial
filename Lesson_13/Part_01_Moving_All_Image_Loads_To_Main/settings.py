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

### ZOMBIE SETTINGS
ZOMBIE_ACCELERATION = 100 # pixels per second per second
ZOMBIE_HIT_BOX_SIZE = 30 # pixels by pixels
ZOMBIE_FRICTION = 0.4