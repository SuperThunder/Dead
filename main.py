__author__ = 'Patrick'
import pygame
import tmx

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)

        self.image = pygame.image.load('data/upc.png')

        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def update(self, dtim, game):

        def dt(val):
            return (dtim * val)/1000

        key = pygame.key.get_pressed()

        dx = 200    # Delta X

        if key[pygame.K_LEFT]:
            self.rect.x -= dt(dx)

        if key[pygame.K_RIGHT]:
            self.rect.x += dt(dx)

class Game(object):
    def main(self, screen):

        clock = pygame.time.Clock()     # Game clock

        bg = pygame.image.load('data/images/bg.png')    # Load image file

        self.tilemap = tmx.load('data/maps/intro.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)


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
            self.tilemap.update(dt, self)
            screen.blit(bg, (0, 0))     # Shows the background image
            self.tilemap.draw(screen)
            pygame.display.flip()   # Loads the image from memory

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    Game().main(screen)