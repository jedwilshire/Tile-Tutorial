import pygame, settings, math

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
        # adjust for frame rate independent move speed
        self.vx *= self.game.dt
        self.vy *= self.game.dt
        # adjust for the diagonal problem
        if self.vx != 0 and self.vy != 0:
            self.vx /= math.sqrt(2)
            self.vy /= math.sqrt(2)
        
    
    # this method called once per frame
    def update(self):
        self.check_keys()
        # check for collisions before moving
        self.check_for_collisions_and_move('x')
        self.check_for_collisions_and_move('y')

    def check_for_collisions_and_move(self, direction):
        if direction == 'x':
            self.rect.x += self.vx
            wall = pygame.sprite.spritecollide(self, self.game.wall_group, False)
            if len(wall) != 0:
                if self.vx > 0:
                    self.rect.x = wall[0].rect.left - self.rect.width
                    self.vx = 0
                if self.vx < 0:
                    self.rect.x = wall[0].rect.right
                    self.vx = 0
        elif direction == 'y':
            self.rect.y += self.vy
            wall = pygame.sprite.spritecollide(self, self.game.wall_group, False)
            if len(wall) != 0:
                if self.vy > 0:
                    self.rect.y = wall[0].rect.top - self.rect.height
                    self.vy = 0
                if self.vy < 0:
                    self.rect.y = wall[0].rect.bottom
                    self.vy = 0
    

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
        