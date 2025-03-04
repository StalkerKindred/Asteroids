import pygame
from constants import *
pygame.init

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
i = 1

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while i == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen, (0,0,0))
        pygame.display.flip()


if __name__ == "__main__":
    main()

