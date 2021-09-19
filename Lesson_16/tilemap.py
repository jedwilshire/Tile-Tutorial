import settings, os, pygame, pytmx

# class for loading basic .txt map files
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

# class for loading tiled map files *.tmx files using PyTMX package added to Thonny
class TiledMap:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
    
    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    
    def make_map(self):
        surface = pygame.Surface((self.width, self.height))
        self.render(surface)
        return surface

class Camera:
    def __init__(self, map_width, map_height):
        self.camera_rect = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.map_width = map_width
        self.map_height = map_height
    
    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)
    
    # for moving a rectangle not a sprite
    def apply_to_rect(self, rect):
        return rect.move(self.camera_rect.topleft)
        
    def update(self, target):
        x = -target.rect.centerx + int(settings.SCREEN_WIDTH / 2) # use centerx
        y = -target.rect.centery + int(settings.SCREEN_HEIGHT / 2) # use centery
        x = min(0, x) # restrict left
        x = max(x, -(self.map_width - self.camera_rect.width))  # restrict right
        y = min(0, y) # restrict up
        y = max(y, -(self.map_height - self.camera_rect.height)) # restrict down
        self.camera_rect.x = x
        self.camera_rect.y = y