import pygame, settings, sprites, os, tilemap

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tile Game Tutorial - Lesson 10 Vector Rotation and Movement, No Collisions')
        # a group of all the sprites in this game
        self.sprite_group = pygame.sprite.Group()
        # a group of all the wall sprites in this game
        self.wall_group = pygame.sprite.Group()
        self.load_game()
        
    
    def load_game(self):
        map_file = os.path.join(os.path.dirname(__file__), 'map2.txt')
        self.images_folder = os.path.join(os.path.dirname(__file__), 'images')
        self.player_image_file = os.path.join(self.images_folder, settings.PLAYER_IMG_FILE)
        self.map = tilemap.Map(map_file)
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        for y, row in enumerate(self.map.tiles):
            for x, tile in enumerate(row):
                if tile == '1':
                    sprites.Wall(self, x, y)
                # position player in location from map.txt
                elif tile == 'P':
                    self.player = sprites.Player(self, x, y)
            
    def gameloop(self):
        while self.running:
            # get the time in milliseconds since last update to adjust movement
            self.dt = self.clock.tick(60) / 1000
            self.event_update()
            self.game_update()
            self.game_draw()
    
    def game_draw(self):
        self.screen.fill(settings.BLACK)
        self.show_tile_grid()
        # draw sprites to screen
        for sprite in self.sprite_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # draw a rectangle for debugging and viewing purposes
        pygame.draw.rect(self.screen, settings.WHITE, self.camera.apply(self.player), width = 1)
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