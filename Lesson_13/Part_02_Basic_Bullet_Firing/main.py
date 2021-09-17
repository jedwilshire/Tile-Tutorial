import pygame, settings, sprites, os, tilemap

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tile Game Tutorial - Lesson 13 Shooting Zombies')
        
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
        map_file = os.path.join(os.path.dirname(__file__), 'map5_gauntlet.txt')
        self.map = tilemap.Map(map_file)
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        for y, row in enumerate(self.map.tiles):
            for x, tile in enumerate(row):
                if tile == '1':
                    sprites.Wall(self, x, y)
                # position player in location from map.txt
                elif tile == 'P':
                    self.player = sprites.Player(self, x, y)
                
                # position zombie from map.txt
                elif tile == 'Z':
                    sprites.Zombie(self, x, y)
    
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
        self.screen.fill(settings.BROWN)
        # self.show_tile_grid()
        # draw sprites to screen
        for sprite in self.sprite_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # set our screen's caption to include game fps - for development purposes only
        pygame.display.set_caption("'Tile Game Tutorial - Lesson 13 Shooting Zombies // FPS = {:.2f}".format(self.clock.get_fps()))
        
        # draw a player hit box rectangle for debugging and viewing purposes
        # pygame.draw.rect(self.screen, settings.WHITE, self.camera.apply_to_rect(self.player.hit_box_rect), width = 1)
        
        # draw hit box for zombies
        #for sprite in self.zombie_group:
            #pygame.draw.rect(self.screen, settings.WHITE, self.camera.apply_to_rect(sprite.hit_box_rect), width = 1)
        
        # flip display
        pygame.display.flip()
    
    def event_update(self):
        ### Process event list ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def game_update(self):
        self.sprite_group.update()
        self.camera.update(self.player)
        
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