import pygame, settings, math, os, random, pytweening


# To use Tiled Objects layer, we remove all multiply by tilesize

def hit_box_collide(player, sprite):
    return player.hit_box_rect.colliderect(sprite.rect)

def hit_box_to_hit_box_collide(sprite1, sprite2):
    return sprite1.hit_box_rect.colliderect(sprite2.hit_box_rect)

def check_for_collisions(sprite, sprite_group, direction):
    # check for x direction
    if direction == 'x':
        # get a list of colliding walls
        collisions = pygame.sprite.spritecollide(sprite, sprite_group, False, hit_box_collide)
        # if there is at least one wall collision, choose first wall in list
        if len(collisions) != 0:
            #print(wall[0])
            if sprite.hit_box_rect.centerx < collisions[0].rect.centerx: # moving right pos.x is left side of player
                # set pos.x to left side minus half width of player rect
                sprite.pos.x = collisions[0].rect.left - sprite.hit_box_rect.width / 2.0
            if sprite.hit_box_rect.centerx > collisions[0].rect.centerx: # moving left
                # set pos.x to right side of wall plus have player width
                sprite.pos.x = collisions[0].rect.right + sprite.hit_box_rect.width / 2.0
            # if a collision occured, stop velocity in x direciton
            sprite.vel.x = 0
        
        # check for y direction in same manner
    elif direction == 'y':
        collisions = pygame.sprite.spritecollide(sprite, sprite_group, False, hit_box_collide)
        if len(collisions) != 0:
            if sprite.hit_box_rect.centery < collisions[0].rect.centery: # moving down pos.y is top of player
                # set pos.y to top of wall minus half player rect height
                sprite.pos.y = collisions[0].rect.top - sprite.hit_box_rect.height / 2.0
            if sprite.hit_box_rect.centery > collisions[0].rect.centery: # moving up
                # set pos.y to bottom of wall plus have player height
                sprite.pos.y = collisions[0].rect.bottom + sprite.hit_box_rect.height / 2.0
            sprite.vel.y = 0
            
            
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self._layer = settings.PLAYER_LAYER
        # keep refernce to our main.Applicaiton
        self.game = game
        
        # assign player image
        self.image = self.game.player_image
        
        # scale image to our tile size (optional)
        # self.image = pygame.transform.scale(self.image, (settings.TILE_SIZE, settings.TILE_SIZE))
        
        # create rect object for movement/collisions, set position
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # create a hit box rectangle that does not change in size with rotation
        self.hit_box_rect = pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE)
        self.hit_box_rect.center = self.rect.center
        
        # use a vector for position and velocity
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        
        # use angle for rotation
        self.angle = 0
        self.rotation_speed = 0
        
        # add to the sprite group main.Application
        self.game.sprite_group.add(self)
        
        # last time gun fired
        self.last_fire_time = 0
        
        self.health = settings.PLAYER_HEALTH
    
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
    
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_fire_time > settings.FIRE_RATE:
                self.last_fire_time = current_time
                spread = random.uniform(-settings.BULLET_SPREAD, settings.BULLET_SPREAD)
                off_pos = self.pos + settings.GUN_BARREL_OFFSET.rotate(self.angle)
                Bullet(self.game, off_pos, self.angle + spread)
                self.vel += pygame.math.Vector2(-settings.BULLET_KICKBACK, 0).rotate(self.angle)
                ExplosionEffect(self.game, off_pos)
    def update(self):
        #print(self.pos, self.vel, self.angle)
        # we rework the update and movement from the ground up
        # check for key presses
        self.check_keys()
        
        # rotate image and reassign rect
        self.angle += self.rotation_amt * self.game.dt
        self.angle %= 360
        self.image = pygame.transform.rotate(self.game.player_image, -self.angle)
        self.rect = self.image.get_rect()
        
        # change the player position vector based on velocity, adjusted for delta time
        self.pos += self.vel * self.game.dt
        
        # move the player's hit box x position
        self.hit_box_rect.centerx = self.pos.x
        
        # check for player's collisions in x direction
        check_for_collisions(self, self.game.wall_group, 'x')
        
        # reassign x posiion of hit box again, since check_for_collisions may have moved pos.x
        self.hit_box_rect.centerx = self.pos.x
        
        # move player's y position
        self.hit_box_rect.centery = self.pos.y
        
        # check player's collisions in y direction
        check_for_collisions(self, self.game.wall_group, 'y')
        
        # reassign hit box y position again
        self.hit_box_rect.centery = self.pos.y
        
        # move player rect to hit box rect
        self.rect.center = self.hit_box_rect.center
        
    def use_health_pack(self, amt):
        self.health += amt
        self.health = min(self.health, settings.PLAYER_HEALTH)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, angle):
        super().__init__()
        self._layer = settings.BULLET_LAYER
        self.game = game
        game.sprite_group.add(self)
        game.bullet_group.add(self)
        self.image = game.bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = angle
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(settings.BULLET_SPEED, 0).rotate(self.angle)
        self.spawn_time = pygame.time.get_ticks()
                                       
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > settings.BULLET_LIFE:
            self.kill()
        
        if pygame.sprite.spritecollideany(self, self.game.wall_group):
            self.kill()
        
        
        

        

class Zombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self._layer = settings.ZOMBIE_LAYER
        self.game = game
        
        self.image = game.zombie_image.copy()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = self.pos
        
        # create a hit box for the zombie, center on rect
        self.hit_box_rect = pygame.Rect(0, 0, settings.ZOMBIE_HIT_BOX_SIZE, settings.ZOMBIE_HIT_BOX_SIZE)
        self.hit_box_rect.center = self.rect.center
        
        # vectors to control zombie motion      
        self.acceleration_rate = random.choice(settings.ZOMBIE_ACCELERATION)
        self.acc = pygame.math.Vector2(self.acceleration_rate, 0)
        self.vel = pygame.math.Vector2(0, 0)
        
        # angle of rotatoin
        self.angle = 0
        self.game.sprite_group.add(self)
        self.game.zombie_group.add(self)
        
        self.health = settings.ZOMBIE_HEALTH
    
    def adjust_acc_for_avoidance(self, acc):
        for zombie in self.game.zombie_group:
            if zombie != self:
                dist = self.pos - zombie.pos
                if 0 < dist.length() < settings.AVOID_RADIUS:
                    acc += dist.normalize()
        return acc
        
    def update(self):
        self.angle = (self.game.player.pos - self.pos).angle_to(pygame.math.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.game.zombie_image, self.angle)
        # recenter image
        self.rect = self.image.get_rect()
        
        # rotate acceleraion vector to match angle of rotation
        self.acc = pygame.math.Vector2(self.acceleration_rate, 0).rotate(-self.angle)
        self.acc = self.acc.normalize()
        self.acc = self.adjust_acc_for_avoidance(self.acc)
        self.acc.scale_to_length(self.acceleration_rate)
        self.acc -= self.vel * settings.ZOMBIE_FRICTION
        
        # set new velocity vector
        self.vel += self.acc * self.game.dt
        
        # move position by velocity
        self.pos += self.vel * self.game.dt + 1.0/2.0 * self.acc * self.game.dt ** 2
        
        # move and check each direction
        self.hit_box_rect.centerx = self.pos.x
        check_for_collisions(self, self.game.wall_group, 'x')
        self.hit_box_rect.centerx = self.pos.x
        
        self.hit_box_rect.centery = self.pos.y
        check_for_collisions(self, self.game.wall_group, 'y')
        self.hit_box_rect.centery = self.pos.y
        
        self.rect.center = self.hit_box_rect.center
        
        if self.health < settings.ZOMBIE_HEALTH:
            self.draw_health_bar()
            
        if self.health <= 0:
            self.kill()
            
    def draw_health_bar(self):
        pct = self.health / settings.ZOMBIE_HEALTH
        if pct > .6:
            color = settings.GREEN
        elif pct > .3:
            color = settings.YELLOW
        else:
            color = settings.RED
        rect = pygame.Rect(0, 0, int(self.image.get_width() * pct), 7)
        pygame.draw.rect(self.image, color, rect)
        
            
            
class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self._layer = settings.EFFECTS_LAYER
        self.game = game
        self.game.sprite_group.add(self)
        self.image = random.choice(self.game.flash_images)
        self.spawn_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > settings.FLASH_TIME:
            self.kill()
        

class Item(pygame.sprite.Sprite):
    def __init__(self, game, item_type, x, y):
        super().__init__()
        self._layer = settings.ITEMS_LAYER
        self.game = game
        self.item_type = item_type
        self.image = game.item_images[item_type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = pygame.math.Vector2(x, y)
        self.game.item_group.add(self)
        self.game.sprite_group.add(self)
        self.tween_step = 0
        self.tween_dir = 1
    
    def update(self):
        rng = settings.ITEM_BOB_RANGE
        offset = rng * (pytweening.easeInOutSine(self.tween_step / rng) - 0.5)
        self.rect.centery = self.pos.y + offset * self.tween_dir
        self.tween_step += settings.ITEM_BOB_RATE
        if self.tween_step > rng:
            self.tween_step = 0
            self.tween_dir *= -1
        

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        super().__init__()
        self._layer = settings.WALL_LAYER
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x 
        self.rect.y = y
        self.game.wall_group.add(self)
        