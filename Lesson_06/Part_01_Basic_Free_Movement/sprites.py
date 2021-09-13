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
        self.vx = 0
        self.vy = 0
        # add to the sprite group main.Application
        self.game.sprite_group.add(self)
    
    def check_keys(self):
        # assume no pressed
        self.vx, self.vy = 0, 0
        # get a boolean list of all key states, index is key code
        # True indicates key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -settings.PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = settings.PLAYER_SPEED
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = settings.PLAYER_SPEED
    
    def update(self):
        # called once per frame
        self.check_keys()
        self.rect.x += self.vx
        self.rect.y += self.vy
    
    

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
        