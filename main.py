__author__ = 'Patrick'
import pygame

class Game(object):
    def main(self, screen):

        clock = pygame.time.Clock()     ## Game clock

        while True:

            clock.tick(30)

            for event in pygame.event.get():
                ## If the playe tries to quit the game, exit
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    return

            pygame.display.flip() ## Flips the display
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    Game().main(screen)