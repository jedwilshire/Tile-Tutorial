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
FLASH_IMGS = ['flash00.png', 'flash01.png', 'flash02.png', 'flash03.png', 'flash04.png', 'flash05.png', 'flash06.png', 'flash07.png']
ITEM_IMGS = {'health' : 'health_pack.png'}
ZOMBIE_SPLAT_IMAGE = 'splat_green.png'

### PLAYER SETTINGS
PLAYER_SPEED = 250 # pixels per second
PLAYER_ROTATION_SPEED = 200 # degrees per second
GUN_BARREL_OFFSET = pygame.math.Vector2(28, 10)  # a vector to offset the bullets from center of player
PLAYER_HEALTH = 100

### BULLET SETTINGS
BULLET_SPEED = 500
BULLET_LIFE = 1000
FIRE_RATE = 200 # delay in fire
BULLET_SIZE = 6
BULLET_KICKBACK = 50
BULLET_SPREAD = 5
BULLET_DAMAGE = 10
BULLET_KNOCKBACK = 50

### ZOMBIE SETTINGS
ZOMBIE_ACCELERATION = [80, 90, 100, 110, 120] # pixels per second per second
ZOMBIE_HIT_BOX_SIZE = 30 # pixels by pixels
ZOMBIE_FRICTION = 1.0
ZOMBIE_HEALTH = 100
ZOMBIE_DAMAGE = 10
ZOMBIE_KNOCKBACK = 30
AVOID_RADIUS = 50
ZOMBIE_DETECT_RADIUS = 400

### SPECIAL EFFECTS
FLASH_TIME = 100
FLASH_SIZE = 20

### LAYERS
WALL_LAYER = 1
ITEMS_LAYER = 2
PLAYER_LAYER = 3
ZOMBIE_LAYER = 4
BULLET_LAYER = 5
EFFECTS_LAYER = 6

### ITEMS
HEALTH_PACK_AMT = 20
ITEM_BOB_RANGE = 15
ITEM_BOB_RATE = .4
 
# SOUND AND MUSIC SETTINGS
BG_MUSIC = 'espionage.ogg'
LEVEL_START_SOUND = 'level_start.wav'
WEAPON_SOUNDS = {'gun' : 'pistol.wav', 'shotgun' : 'shotgun.wav'}
ZOMBIE_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav', 'zombie-roar-3.wav', 'zombie-roar-4.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav', 'zombie-roar-8.wav']
ITEM_SOUNDS = {'health' : 'health_pack.wav'}
ZOMBIE_SPLAT_SOUND = 'splat-15.wav'
PLAYER_HURT_SOUNDS = ['player-hurt-1.wav', 'player-hurt-2.wav', 'player-hurt-3.wav', 'player-hurt-4.wav', 'player-hurt-5.wav', 'player-hurt-6.wav', 'player-hurt-7.wav']

# FONTS
PAUSE_FONT = 'zombie_font.ttf'