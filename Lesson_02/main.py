import pygame, settings, sprites

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tile Game Tutorial - Lesson 01')
        self.sprite_group = pygame.sprite.Group()
        self.player = sprites.Player(self, 10, 10) 
        
    def gameloop(self):
        keymap = {'up': False, 'down': False, 'left': False, 'right': False}
        while self.running:
            self.clock.tick(30)
            ### Process event list ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event, keymap)
                    
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event, keymap)
            
            ### Move Player ###
            self.handle_movement(keymap)
            
            self.screen.fill(settings.BLACK)
            self.show_tile_grid()
            # call sprite update methods
            self.sprite_group.update()
            # draw sprites to screen
            self.sprite_group.draw(self.screen)
            pygame.display.flip()
    
    def handle_movement(self, keymap):
        if keymap['left']:
            self.player.move(dx = -1)
        if keymap['right']:
            self.player.move(dx = 1)
        if keymap['up']:
            self.player.move(dy = -1)
        if keymap['down']:
            self.player.move(dy = 1)
    
    def handle_keydown(self, event, keymap):
        if event.key == pygame.K_UP:
            keymap['up'] = True
        elif event.key == pygame.K_DOWN:
            keymap['down'] = True
        elif event.key == pygame.K_LEFT:
            keymap['left'] = True
        elif event.key == pygame.K_RIGHT:
            keymap['right'] = True
            
    def handle_keyup(self, event, keymap):
        if event.key == pygame.K_UP:
            keymap['up'] = False
        elif event.key == pygame.K_DOWN:
            keymap['down'] = False
        elif event.key == pygame.K_LEFT:
            keymap['left'] = False
        elif event.key == pygame.K_RIGHT:
            keymap['right'] = False
            
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