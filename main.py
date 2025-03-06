#Imports
import pygame
from constants import *
from player import Player,Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
import highscore
#activating virtual: source venv/bin/activate
pygame.init()
#Game Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    #Console
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    #Position for player
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    #Fps
    clock = pygame.time.Clock()
    dt = 0
    #Score
    def draw_score(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    text_font = pygame.font.SysFont(None, 30)

    score = 0
    current_high_score = highscore.load_high_score()
    #Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    #Containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = updatable
    #Objects
    player = Player(x,y)
    asteroidfield = AsteroidField()
    #Game Loop
    while True:
        #dt
        dt = clock.tick(60) / 1000
        #Exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #Update
        for updating in updatable:
            if updating == player:
                updating.cooldown -= dt
            updating.update(dt)

        #Drawing
        pygame.Surface.fill(screen, (0,0,0))
        for drawing in drawable:
            drawing.draw(screen)
        draw_score(f"Score: {score}", text_font, (255,255,255), 20, 20)
        #Collision check
        for steroid in asteroids:
            if True == steroid.collision_check(player):
                print("Game over!")
                print(f"Current score: {score}")
                if score > current_high_score:
                    print(f"Congratulations you managed to beat you highest score of {current_high_score}!!!")
                    highscore.save_high_score(score)
                    current_high_score = score
                print(f"Highest score: {current_high_score}")
                exit()
            for bullet in shots:
                if True == steroid.collision_check(bullet):
                    if steroid.radius == ASTEROID_MIN_RADIUS:  # Small asteroid
                        if "big" in steroid.origin_chain:  # From big to medium to small
                            score += 30
                        elif "medium" in steroid.origin_chain:  # From medium to small
                            score += 25
                        else:  # Base small asteroid
                            score += 20
                    elif steroid.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:  # Medium asteroid
                        if "big" in steroid.origin_chain:  # From big to medium
                            score += 20
                        else:  # Base medium asteroid
                            score += 15
                    elif steroid.radius == ASTEROID_MAX_RADIUS:  # Big asteroid
                        score += 10
                    steroid.split()
                    pygame.sprite.Sprite.kill(bullet)
        #Flip       
        pygame.display.flip()


if __name__ == "__main__":
    main()

