import pygame, settings, sprites, os

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tile Game Tutorial - Lesson 05 One Tile Movement at a Time')
        # a group of all the sprites in this game
        self.sprite_group = pygame.sprite.Group()
        # a group of all the wall sprites in this game
        self.wall_group = pygame.sprite.Group() 
        self.load_walls()
    
    def load_walls(self):
        wall_text = []
        with open(os.path.join(os.path.dirname(__file__), 'map.txt'), 'r') as f:
            for line in f:
                wall_text.append(line.strip())
        for y, row in enumerate(wall_text):
            for x, tile in enumerate(row):
                if tile == '1':
                    sprites.Wall(self, x, y)
                # position player in location from map.txt
                elif tile == 'P':
                    self.player = sprites.Player(self, x, y)
            
    def gameloop(self):
        keymap = {'up': False, 'down': False, 'left': False, 'right': False}
        while self.running:
            self.clock.tick(30)
            ### Process event list ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.move(dy = -1)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(dy = 1)
                    elif event.key == pygame.K_LEFT:
                        self.player.move(dx = -1)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(dx = 1)                        
            
            self.screen.fill(settings.BLACK)
            self.show_tile_grid()
            # call sprite update methods
            self.sprite_group.update()
            # draw sprites to screen
            self.sprite_group.draw(self.screen)
            pygame.display.flip()
    
            
    def show_tile_grid(self):
        for x in range(0, settings.SCREEN_WIDTH, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.GREY, (x, 0), (x, settings.SCREEN_HEIGHT))
        for y in range(0, settings.SCREEN_HEIGHT, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.GREY, (0, y), (settings.SCREEN_WIDTH, y))

def main():
    app = Application()
    app.gameloop()
    pygame.quit()

if __name__ == '__main__':
    main()