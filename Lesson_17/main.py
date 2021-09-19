import pygame, settings, sprites, os, tilemap


## HUD ##
def make_HUD(surface, player):
    # make health bar
    health_bar_width = 100
    health_bar_height = 25
    outer_rect = pygame.Rect(0, 0, health_bar_width, health_bar_height)
    health_pct = player.health / settings.PLAYER_HEALTH
    inner_rect_width = int(health_pct * health_bar_width)
    inner_rect = pygame.Rect(0, 0, inner_rect_width, health_bar_height)
    pygame.draw.rect(surface, settings.BLACK, outer_rect, width = 2)
    if health_pct > .60:
        color = settings.GREEN
    elif health_pct > .30:
        color = settings.YELLOW
    else:
        color = settings.RED
    pygame.draw.rect(surface, color, inner_rect)
        
class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tile Game Tutorial - Lesson 14 Zombie and Player Health Bars')
        
        # a group of all the sprites in this game
        self.sprite_group = pygame.sprite.Group()
        
        # a group of all the wall sprites in this game
        self.wall_group = pygame.sprite.Group()
        
        # a group of zombie hunters
        self.zombie_group = pygame.sprite.Group()
        
        # a group of bullets
        self.bullet_group = pygame.sprite.Group()
        
        # load all game images
        self.load_images()
        
        # load game using tile map
        self.load_game()

    def load_game(self):
        game_folder = os.path.dirname(__file__)
        self.map_folder = os.path.join(game_folder, 'maps')
        map_file = os.path.join(self.map_folder, 'map1.tmx')
        self.map = tilemap.TiledMap(map_file)
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        for item in self.map.tmxdata.objects:
            if item.name == 'obstacle':
                sprites.Wall(self, item.x, item.y, item.width, item.height)
            elif item.name == 'player':
                self.player = sprites.Player(self, item.x, item.y)
            elif item.name == 'zombie':
                sprites.Zombie(self, item.x, item.y)
        self.camera = tilemap.Camera(self.map.width, self.map.height) 
    
    def load_images(self):
        # changed name of settings for file name as well
        self.images_folder = os.path.join(os.path.dirname(__file__), 'images')
        
        player_image_file = os.path.join(self.images_folder, settings.PLAYER_IMG_FILENAME)
        self.player_image = pygame.image.load(player_image_file).convert_alpha()
        
        wall_image_file = os.path.join(self.images_folder, settings.WALL_IMG_FILENAME)
        self.wall_image = pygame.image.load(wall_image_file).convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (settings.TILE_SIZE, settings.TILE_SIZE))

        zombie_image_file = os.path.join(self.images_folder, settings.ZOMBIE_IMG_FILENAME)
        self.zombie_image = pygame.image.load(zombie_image_file)
        
        bullet_image_file = os.path.join(self.images_folder, settings.BULLET_IMG_FILENAME)
        self.bullet_image = pygame.image.load(bullet_image_file).convert_alpha()
        self.bullet_image = pygame.transform.scale(self.bullet_image, (settings.BULLET_SIZE, settings.BULLET_SIZE))
        
        
        
                                         
    def gameloop(self):
        while self.running:
            # get the time in milliseconds since last update to adjust movement
            self.dt = self.clock.tick(60) / 1000
            self.event_update()
            self.game_update()
            self.game_draw()
    
    def game_draw(self):
        # draw game map
        self.screen.blit(self.map_image, self.camera.apply_to_rect(self.map_rect))
        
        # self.show_tile_grid()
        # draw sprites to screen
        for sprite in self.sprite_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # set our screen's caption to include game fps - for development purposes only
        pygame.display.set_caption("'Tile Game Tutorial - Lesson 14 Zombie and Player Health Bar - FPS = {:.2f}".format(self.clock.get_fps()))
        
        # draw a player hit box rectangle for debugging and viewing purposes
        # pygame.draw.rect(self.screen, settings.WHITE, self.camera.apply_to_rect(self.player.hit_box_rect), width = 1)
        
        # draw hit box for zombies
        #for sprite in self.zombie_group:
            #pygame.draw.rect(self.screen, settings.WHITE, self.camera.apply_to_rect(sprite.hit_box_rect), width = 1)
        
        # Add/update HUD
        make_HUD(self.screen, self.player)
        # flip display    
        pygame.display.flip()
    
    def event_update(self):
        ### Process event list ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def game_update(self):
        # update all sprites
        self.sprite_group.update()
        
        # update the camera
        self.camera.update(self.player)
        
        # handle bullets colliding with zombies
        # all group1 hits                        # group 1          # group 2        # kill1?  #kill2?
        zombie_hits = pygame.sprite.groupcollide(self.zombie_group, self.bullet_group, False, True)
        for hit in zombie_hits:
            hit.health -= settings.BULLET_DAMAGE
            hit.vel = pygame.math.Vector2(0, 0)
        
        # handle zombies colliding with player
        player_hits = pygame.sprite.spritecollide(self.player, self.zombie_group, False, sprites.hit_box_to_hit_box_collide)
        for hit in player_hits:
            self.player.health -= settings.ZOMBIE_DAMAGE
            self.player.pos += pygame.math.Vector2(settings.ZOMBIE_KNOCKBACK, 0).rotate(hit.angle)
            hit.vel = pygame.math.Vector2(-settings.ZOMBIE_KNOCKBACK, 0).rotate(hit.angle)
            if self.player.health <= 0:
                self.running = False
        
    def show_tile_grid(self):
        for x in range(0, self.map.width, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.GREY, (x, 0), (x, settings.SCREEN_HEIGHT))
        for y in range(0, self.map.height, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.GREY, (0, y), (settings.SCREEN_WIDTH, y))

def main():
    app = Application()
    app.gameloop()
    pygame.quit()

if __name__ == '__main__':
    main()