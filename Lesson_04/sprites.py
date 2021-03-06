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
        if not self.check_for_collision(dx, dy):
            self.x += dx * settings.PLAYER_SPEED
            self.y += dy * settings.PLAYER_SPEED
    
    def check_for_collision(self, dx, dy):
        for wall in self.game.wall_group:
            if ((self.x + dx * settings.PLAYER_SPEED) * settings.TILE_SIZE >= wall.rect.left and
                (self.x + dx * settings.PLAYER_SPEED) * settings.TILE_SIZE <= wall.rect.right and
                (self.y + dy * settings.PLAYER_SPEED) * settings.TILE_SIZE >= wall.rect.top and
                (self.y + dy * settings.PLAYER_SPEED) * settings.TILE_SIZE <= wall.rect.bottom):
                return True
        return False
    
    def update(self):
        # positions this sprite inside nearest grid space
        self.rect.x = int(self.x) * settings.TILE_SIZE
        self.rect.y = int(self.y) * settings.TILE_SIZE

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE
        self.game.wall_group.add(self)
        self.game.sprite_group.add(self)
        