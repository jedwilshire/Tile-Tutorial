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
        if not self.check_for_collision(dx, dy):
            self.rect.x += dx * settings.TILE_SIZE
            self.rect.y += dy * settings.TILE_SIZE
    
    def check_for_collision(self, dx, dy):
        for wall in self.game.wall_group:
            if (self.rect.x + self.rect.width + dx * settings.TILE_SIZE > wall.rect.left and
                self.rect.x + dx * settings.TILE_SIZE < wall.rect.right and
                self.rect.y + self.rect.height + dy  * settings.TILE_SIZE > wall.rect.top and
                self.rect.y + dy * settings.TILE_SIZE < wall.rect.bottom):
                return True
        return False

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
        