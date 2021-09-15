import pygame, settings, math

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        # keep refernce to our main.Applicaiton
        self.game = game
        
        # load player image
        self.non_rotated_image = pygame.image.load(game.player_image_file).convert_alpha()
        self.image = self.non_rotated_image
        
        # scale image to our tile size (optional)
        # self.image = pygame.transform.scale(self.image, (settings.TILE_SIZE, settings.TILE_SIZE))
        
        # create rect object for movement/collisions, set position
        self.rect = self.image.get_rect()
        
        # use a vector for position and velocity
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y) * settings.TILE_SIZE
        
        # use angle for rotation
        self.angle = 0
        self.rotation_speed = 0
        
        # add to the sprite group main.Application
        self.game.sprite_group.add(self)
    
    def check_keys(self):
        # assume no pressed
        self.vel.x, self.vel.y = 0, 0
        self.rotation_amt = 0
        # get a boolean list of all key states, index is key code
        # True indicates key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = pygame.math.Vector2(settings.PLAYER_SPEED, 0).rotate(self.angle)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = pygame.math.Vector2(-settings.PLAYER_SPEED / 2, 0).rotate(self.angle)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation_amt -= settings.PLAYER_ROTATION_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation_amt += settings.PLAYER_ROTATION_SPEED

    
   
    def update(self):
        #print(self.pos, self.vel, self.angle)
        # we rework the update and movement from the ground up
        # check for key presses
        self.check_keys()
        
        # rotate image and reassign rect
        self.angle += self.rotation_amt * self.game.dt
        self.angle %= 360
        self.image = pygame.transform.rotate(self.non_rotated_image, -self.angle)
        self.rect = self.image.get_rect()
        
        # change the player position vector based on velocity, adjusted for delta time
        self.pos += self.vel * self.game.dt
        
        # move the player's x position
        self.rect.x = self.pos.x
        
        # check for player's collisions in x direction
        #self.check_for_collisions('x')
        
        # reassign x posiion again, since check_for_collisions may have moved pos.x
        self.rect.x = self.pos.x
        
        # move player's y position
        self.rect.y = self.pos.y
        
        # check player's collisions in y direction
        #self.check_for_collisions('y')
        
        # reassign y position again
        self.rect.y = self.pos.y
        
        
        
    def check_for_collisions(self, direction):
        # we build this up again from ground up
        # check for x direction
        if direction == 'x':
            # get a list of colliding walls
            wall = pygame.sprite.spritecollide(self, self.game.wall_group, False)
            # if there is at least one wall collision, choose first wall in list
            if len(wall) != 0:
                if self.vel.x > 0: # moving right pos.x is left side of player
                    # set pos.x to left side minus width of player rect
                    self.pos.x = wall[0].rect.left - self.rect.width 
                if self.vel.x < 0: # moving left
                    # set pos.x to right side of wall
                    self.pos.x = wall[0].rect.right
                # if a collision occured, stop velocity in x direciton
                self.vel.x = 0
        
        # check for y direction in same manner
        elif direction == 'y':
            wall = pygame.sprite.spritecollide(self, self.game.wall_group, False)
            if len(wall) != 0:
                if self.vel.y > 0: # moving down pos.y is top of player
                    # set pos.y to top of wall minus player rect height
                    self.pos.y = wall[0].rect.top - self.rect.height
                if self.vel.y < 0: # moving up
                    # set pos.y to bottom of wall
                    self.pos.y = wall[0].rect.bottom
                self.vel.y = 0
        

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
        