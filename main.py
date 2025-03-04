import pygame
from constants import *
from player import Player
pygame.init
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    player = Player(x,y)
    while True:
        #dt
        dt = clock.tick(60) / 1000
        #Exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #Update
        updatable.update(dt)
        #Drawing
        pygame.Surface.fill(screen, (0,0,0))
        for drawing in drawable:
            drawing.draw(screen)
        #Flip
        pygame.display.flip()


if __name__ == "__main__":
    main()

