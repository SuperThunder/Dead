__author__ = 'Patrick'
import pygame
import tmx

class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/bullet.png')

    def __init__(self, location, (x, y), *groups):

        super(Bullet, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())     # Setup rect
        x, y = float(x), float(y)
        self.dx = float(x/y)
        self.dy = -1   # Bullet Direction
        self.lifespan = 1


    def update(self, dtim, game):
        def dt(val):
            return (dtim * val)/1000

        self.lifespan -= dt(1)
        if self.lifespan < 0:
            self.kill()
            return

        self.rect.x += self.dx * dt(100)
        self.rect.y += self.dy * float(dt(100))

       # if pygame.sprite.spritecollide(self, game.enemies, True):
       #     self.kill

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)

        self.image = pygame.image.load('data/upc.png')

        self.rect = pygame.rect.Rect(location, self.image.get_size())

        ## Variables for gravity
        self.resting = False    # If the player is on the ground or not
        self.dy = 0

        self.direction = 0

        self.is_dead = False

        self.gun_cooldown = 0       # Gun cooldown

    def update(self, dtim, game):
        ## Return the distance between ticks divided by 1000 multiplied by a variable,
        ## For movement to be standardized
        def dt(val):
            return (dtim * val)/1000

        dx = 200    # Delta X

        old_r = self.rect.copy()     # Get the rectangle before any changes are made (For collision detection)

        key = pygame.key.get_pressed()      # Get keys that are continually being pressed
        if key[pygame.K_LEFT]:
            self.rect.x -= dt(dx)

        if key[pygame.K_RIGHT]:
            self.rect.x += dt(dx)

        if self.resting and key[pygame.K_UP]:
            self.dy = -600
            self.resting = False

        if key[pygame.K_SPACE] and not self.gun_cooldown:
            game.gun_sound.play()
            Bullet(self.rect.midleft, pygame.mouse.get_pos(), game.sprites)
            self.gun_cooldown = 10
        self.gun_cooldown = max(0, self.gun_cooldown - 1)

        self.dy = min(400, self.dy + 60)    # Gravity
        self.rect.y += dt(self.dy)      # Apply the delta-y to the player

        new_r = self.rect   # Get the new rectangle after changes of distance are made (For collision detection)

        ## From map file find tiles /w name 'blockers'
        ## If 't' in value blockers move block to old_r.bottom
        ## Same for rest of 'tlrb' (top,left,right,bottom)
        for cell in game.tilemap.layers['triggers'].collide(new_r, 'blockers'):
            blockers = cell['blockers']
            if 'l' in blockers and old_r.right <= cell.left < new_r.right:
                new_r.right = cell.left
            if 'r' in blockers and old_r.left >= cell.right > new_r.left:
                new_r.left = cell.right
            if 't' in blockers and old_r.bottom <= cell.top < new_r.bottom:
                self.resting = True
                new_r.bottom = cell.top
                self.dy = 0
            if 'b' in blockers and old_r.top >= cell.bottom > new_r.top:
                new_r.top = cell.bottom
                self.dy = 0

        game.tilemap.set_focus(self.rect.x, self.rect.y)

class Game(object):
    def main(self, screen):

        clock = pygame.time.Clock()     # Game clock

        bg = pygame.image.load('data/images/bg.png')    # Load image file

        self.tilemap = tmx.load('data/maps/intro.tmx', screen.get_size())   # Load TMX file

        ## Load the UPC
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)

        ## Sounds
        self.gun_sound = pygame.mixer.Sound('data/sounds/shot.wav')

        ## Main game loop
        while True:

            dt = clock.tick(30)      # Slows the while loop to 30 FPS
            ## Get single keypress events (opposed to holding a key down)
            for event in pygame.event.get():
                ## If the player tries to quit the game, exit
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN and \
                        pygame.key.get_mods() & pygame.KMOD_CTRL and event.key == pygame.K_q:
                    return

            if self.player.rect.y > self.tilemap.height * 32:
                self.player.is_dead = True

            if self.player.is_dead:
                return

            screen.blit(bg, (0, 0))     # Shows the background image
            self.tilemap.update(dt, self)
            self.tilemap.draw(screen)


            pygame.display.flip()   # Loads the image from memory

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    Game().main(screen)