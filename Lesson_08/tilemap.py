import settings, os, pygame
class Map:
    def __init__(self, filename):
        self.tiles = []
        with open(filename, 'r') as f:
            for line in f:
                self.tiles.append(line.strip())
                
        ### Properties of the tile map ###
        self.tiles_width = len(self.tiles[0])
        self.tiles_height = len(self.tiles)
        self.width = self.tiles_width * settings.TILE_SIZE
        self.height = self.tiles_height * settings.TILE_SIZE

class Camera:
    def __init__(self, map_width, map_height):
        self.camera_rect = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.map_width = map_width
        self.map_height = map_height
    
    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(settings.SCREEN_WIDTH / 2)
        y = -target.rect.y + int(settings.SCREEN_HEIGHT / 2)
        x = min(0, x) # restrict left
        x = max(x, -(self.map_width - self.camera_rect.width))  # restrict right
        y = min(0, y) # restrict up
        y = max(y, -(self.map_height - self.camera_rect.height)) # restrict down
        self.camera_rect.x = x
        self.camera_rect.y = y