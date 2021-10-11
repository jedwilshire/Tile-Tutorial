import pygame, sprites, os, tilemap, random
from settings import *


## HUD ##
def make_HUD(surface, player):
    # make health bar
    health_bar_width = 100
    health_bar_height = 25
    outer_rect = pygame.Rect(0, 0, health_bar_width, health_bar_height)
    health_pct = player.health / PLAYER_HEALTH
    inner_rect_width = int(health_pct * health_bar_width)
    inner_rect = pygame.Rect(0, 0, inner_rect_width, health_bar_height)
    pygame.draw.rect(surface, BLACK, outer_rect, width = 2)
    if health_pct > .60:
        color = GREEN
    elif health_pct > .30:
        color = YELLOW
    else:
        color = RED
    pygame.draw.rect(surface, color, inner_rect)
        
class Application:
    def __init__(self):
        pygame.init() # needed for sounds / music
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        # make a reference to game folder - director        
        self.game_folder = os.path.dirname(__file__)
        
        pygame.display.set_caption('Tile Game Tutorial - Lesson 22 Adding a Pause Screen')
        
        # a group of all the sprites in this game
        self.sprite_group = pygame.sprite.LayeredUpdates()
        
        # a group of all the wall sprites in this game
        self.wall_group = pygame.sprite.Group()
        
        # a group of zombie hunters
        self.zombie_group = pygame.sprite.Group()
        
        # a group of bullets
        self.bullet_group = pygame.sprite.Group()
        
        # a group of items
        self.item_group = pygame.sprite.Group()
        
        
        # load all game images
        self.load_images()
        
        # load all game sounds and music
        self.load_sounds()
        
        # load game using tile map
        self.load_game()

        # press 'p' key to pause game
        self.paused = False
        
    def load_game(self):
        self.map_folder = os.path.join(self.game_folder, 'maps')
        map_file = os.path.join(self.map_folder, 'map1.tmx')
        self.map = tilemap.TiledMap(map_file)
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        for item in self.map.tmxdata.objects:
            item_centerx = item.x + item.width / 2
            item_centery = item.y + item.height / 2
            if item.name == 'obstacle':
                sprites.Wall(self, item.x, item.y, item.width, item.height)
            elif item.name == 'player':
                self.player = sprites.Player(self, item_centerx, item_centery)
            elif item.name == 'zombie':
                sprites.Zombie(self, item_centerx, item_centery)
            elif item.name in ITEM_IMGS.keys():
                sprites.Item(self, item.name, item_centerx, item_centery)
        self.camera = tilemap.Camera(self.map.width, self.map.height) 
    
    def load_images(self):
        # changed name of settings for file name as well
        self.images_folder = os.path.join(self.game_folder, 'images')
        
        player_image_file = os.path.join(self.images_folder, PLAYER_IMG_FILENAME)
        self.player_image = pygame.image.load(player_image_file).convert_alpha()
        
        # wall_image_file = os.path.join(self.images_folder, WALL_IMG_FILENAME)
        # self.wall_image = pygame.image.load(wall_image_file).convert_alpha()
        # self.wall_image = pygame.transform.scale(self.wall_image, (TILE_SIZE, TILE_SIZE))

        zombie_image_file = os.path.join(self.images_folder, ZOMBIE_IMG_FILENAME)
        self.zombie_image = pygame.image.load(zombie_image_file)
        
        bullet_image_file = os.path.join(self.images_folder, BULLET_IMG_FILENAME)
        original_bullet_image = pygame.image.load(bullet_image_file).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['pistol'] = pygame.transform.scale(original_bullet_image,
                                                             (WEAPONS['pistol']['bullet_size'], WEAPONS['pistol']['bullet_size']))
        self.bullet_images['shotgun'] = pygame.transform.scale(original_bullet_image,
                                                             (WEAPONS['shotgun']['bullet_size'], WEAPONS['shotgun']['bullet_size']))
        
        self.flash_images = []
        for img in FLASH_IMGS:
            f_img = pygame.image.load(os.path.join(self.images_folder, img)).convert_alpha()
            f_img = pygame.transform.scale(f_img, (FLASH_SIZE, FLASH_SIZE))
            self.flash_images.append(f_img)
            
        self.item_images = {}
        for item in ITEM_IMGS.keys():
            img_file = os.path.join(self.images_folder, ITEM_IMGS[item])
            self.item_images[item] = pygame.image.load(img_file)
        
        splat_file = os.path.join(self.images_folder, ZOMBIE_SPLAT_IMAGE)
        self.zombie_splat_image = pygame.image.load(splat_file).convert_alpha()
        self.zombie_splat_image = pygame.transform.scale(self.zombie_splat_image, (64, 64))
        
        # a surface that dims screen
        self.dim_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 100)) # Black with alpha = 100
        
        # A font for pause menu
        self.pause_font = os.path.join(self.images_folder, PAUSE_FONT)
        
    def load_sounds(self):
        self.sounds_folder = os.path.join(self.game_folder, 'sounds')
        self.music_folder = os.path.join(self.game_folder, 'music')
        # load background music
        music_file = os.path.join(self.music_folder, BG_MUSIC)
        pygame.mixer.music.load(music_file)
        
        # load level start sound
        lvl_start_snd = os.path.join(self.sounds_folder, LEVEL_START_SOUND)
        self.level_start_sound = pygame.mixer.Sound(lvl_start_snd)
        
        # load weapon sounds
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS.keys():
            self.weapon_sounds[weapon] = []
            for sound in WEAPON_SOUNDS[weapon]:
                snd_file = os.path.join(self.sounds_folder, sound)
                self.weapon_sounds[weapon].append(pygame.mixer.Sound(snd_file))
        
        # load zombie sounds
        self.zombie_sounds = []
        for sound in ZOMBIE_SOUNDS:
            snd_file = os.path.join(self.sounds_folder, sound)
            self.zombie_sounds.append(pygame.mixer.Sound(snd_file))
        
        # load zombie splat sound
        splat_snd_file = os.path.join(self.sounds_folder, ZOMBIE_SPLAT_SOUND)
        self.zombie_splat_sound = pygame.mixer.Sound(splat_snd_file)
        # load item sound effects
        self.item_sound = {}
        for sound in ITEM_SOUNDS.keys():
            snd_file = os.path.join(self.sounds_folder, ITEM_SOUNDS[sound])
            self.item_sound[sound] = pygame.mixer.Sound(snd_file)
        
        # load player hurt sounds
        self.player_hurt_sounds = []
        for sound in PLAYER_HURT_SOUNDS:
            snd_file = os.path.join(self.sounds_folder, sound)
            self.player_hurt_sounds.append(pygame.mixer.Sound(snd_file))

    def gameloop(self):
        pygame.mixer.music.play(loops = -1)
        self.level_start_sound.play()
        while self.running:
            # get the time in milliseconds since last update to adjust movement
            self.dt = self.clock.tick(60) / 1000
            self.event_update()
            if not self.paused:
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
        pygame.display.set_caption("Tile Game Tutorial - Lesson 22 Adding a Pause Screen - FPS = {:.2f}".format(self.clock.get_fps()))
        
        # draw a player hit box rectangle for debugging and viewing purposes
        # pygame.draw.rect(self.screen, WHITE, self.camera.apply_to_rect(self.player.hit_box_rect), width = 1)
        
        # draw hit box for zombies
        #for sprite in self.zombie_group:
            #pygame.draw.rect(self.screen, WHITE, self.camera.apply_to_rect(sprite.hit_box_rect), width = 1)
        
        # Add/update HUD
        make_HUD(self.screen, self.player)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('PAUSED', self.pause_font, 64, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # flip display    
        pygame.display.flip()
    
    def event_update(self):
        ### Process event list ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
    def game_update(self):
        # update all sprites
        self.sprite_group.update()
        
        # update the camera
        self.camera.update(self.player)
        
        # handle bullets colliding with zombies
        # all group1 hits                        # group 1          # group 2        # kill1?  #kill2?
        zombie_hits = pygame.sprite.groupcollide(self.zombie_group, self.bullet_group, False, True)
        for hit in zombie_hits:
            for bullet in zombie_hits[hit]:
                hit.health -= WEAPONS[self.player.weapon]['damage']
                hit.vel = pygame.math.Vector2(0, 0)
        
        # handle zombies colliding with player
        # NEED FIX SHOTGUT HIT
        player_hits = pygame.sprite.spritecollide(self.player, self.zombie_group, False, sprites.hit_box_to_hit_box_collide)
        for hit in player_hits:
            self.player.health -= ZOMBIE_DAMAGE
            self.player.pos += pygame.math.Vector2(ZOMBIE_KNOCKBACK, 0).rotate(hit.angle)
            hit.vel = pygame.math.Vector2(-ZOMBIE_KNOCKBACK, 0).rotate(hit.angle)
            random.choice(self.player_hurt_sounds).play()
            if self.player.health <= 0:
                self.running = False
        
        item_hits = pygame.sprite.spritecollide(self.player, self.item_group, False)
        for item in item_hits:
            if item.item_type == 'health' and self.player.health < PLAYER_HEALTH:
                self.player.use_health_pack(HEALTH_PACK_AMT)
                self.item_sound['health'].play()
                item.kill()
                
    def show_tile_grid(self):
        for x in range(0, self.map.width, TILE_SIZE):
            pygame.draw.line(self.screen, GREY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, self.map.height, TILE_SIZE):
            pygame.draw.line(self.screen, GREY, (0, y), (SCREEN_WIDTH, y))

    def draw_text(self, text, font_name, size, color, x, y, align = 'center'):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'center':
            text_rect.center = (x, y)
        elif align == 'left':
            text_rect.left = x
            text_rect.centery = y
        self.screen.blit(text_surface, text_rect)    

def main():
    app = Application()
    app.gameloop()
    pygame.quit()

if __name__ == '__main__':
    main()