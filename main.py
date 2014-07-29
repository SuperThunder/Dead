__author__ = 'Patrick'
import pygame
import tmx

class Game(object):
    def main(self, screen):

        clock = pygame.time.Clock()     # Game clock

        self.tilemap = tmx.load('data/maps/intro.tmx', screen.get_size())

        ## Main game loop
        while True:

            clock.tick(30)      # Slows the while loop to 30 FPS
            ## Get single keypress events (opposed to holding a key down)
            for event in pygame.event.get():
                ## If the player tries to quit the game, exit
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN and \
                        pygame.key.get_mods() & pygame.KMOD_CTRL and event.key == pygame.K_q:
                    return

            pygame.display.flip()   # Loads the image from memory
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    Game().main(screen)