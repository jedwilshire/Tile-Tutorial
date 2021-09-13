import pygame, settings

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        # keep refernce to our main.Applicaiton
        self.game = game
        # create an image surface of tile size, fill with red
        self.image = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.RED)
        # create rect object for movement/collisions, set position
        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE
        self.x = x
        self.y = y
        # add to the sprite group main.Application
        self.game.sprite_group.add(self)
    
    def move(self, dx = 0, dy = 0):
        # moves without grid parameters
        if not ( (self.rect.left <= 0 and dx < 0) or (self.rect.right >= settings.SCREEN_WIDTH and dx > 0)):
            self.x += dx * settings.PLAYER_SPEED
        if not ( (self.rect.top <= 0 and dy < 0) or (self.rect.bottom >= settings.SCREEN_HEIGHT and dy > 0)):
            self.y += dy * settings.PLAYER_SPEED
    
    def update(self):
        # positions this sprite inside nearest grid space
        self.rect.x = int(self.x) * settings.TILE_SIZE
        self.rect.y = int(self.y) * settings.TILE_SIZE