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
    p_x = SCREEN_WIDTH / 2
    p_y = SCREEN_HEIGHT / 2
    #Fps
    clock = pygame.time.Clock()
    dt = 0
    #Drawing text on screen
    def draw_text(text, font, text_col, x, y, centered=True):
        img = font.render(text, True, text_col)
        if centered:
            text_rect = img.get_rect()
            text_rect.center = (x, y)
            screen.blit(img, text_rect)
        else:
            screen.blit(img, (x, y))
    text_font = pygame.font.SysFont(None, 30)
    #Score
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
    player = Player(p_x,p_y)
    asteroidfield = AsteroidField()
    #Start menu
    start = 1
    #Status
    game_state = "START"
    #Game Loop
    while True:
        #dt
        dt = clock.tick(60) / 1000
        #Exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_state == "START" and event.type == pygame.KEYDOWN:
                game_state = "PLAYING"
            # Clear remaining events
                pygame.event.clear()
        #Screen
        pygame.Surface.fill(screen, (0,0,0))
        # Gamestate Logic
        if game_state == "START":
            draw_text(f"Asteroids", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.30, centered=True)
            draw_text(f"Version: {GAME_VERSION}", text_font, (255,255,255), 3, SCREEN_HEIGHT - 20, centered=False)
            draw_text("Press any keys to continue", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, centered=True)
        elif game_state == "PLAYING":
            #Update
            for updating in updatable:
                if updating == player:
                    updating.cooldown -= dt
                updating.update(dt)
            #Drawing
            for drawing in drawable:
                drawing.draw(screen)
            #Score
            draw_text(f"Score: {score}", text_font, (255,255,255), 20, 20, centered=False)
            draw_text(f"High Score:{current_high_score}", text_font, (255,255,255), 20, 40, centered=False)
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

