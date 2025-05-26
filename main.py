#Imports
import pygame
from constants import *
from player import Player,Shot,bullet_border_check,Melta_Gun,Machine_Gun,Rail_Gun,GrenadeLauncher, check_max_range
from asteroid import Asteroid
from asteroidfield import AsteroidField
import button
import highscore
from timer import display
#activating virtual: source venv/bin/activate
pygame.init()
#Game Screen
pygame.display.set_caption("Asteroids")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    #Console
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    #Position for player
    p_x = SCREEN_WIDTH / 2
    p_y = SCREEN_HEIGHT / 2
    #Fps #Currently only 60
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
    #Buttons
    mch_gun_button = button.Button((10,10,10),SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.30,200,50,text="Machine Gun",text_color=(255,255,255))
    railgun_button = button.Button((10,10,10),SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.30,200,50,text="Rail Gun",text_color=(255,255,255))
    melta_gun_button = button.Button((10,10,10),SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.30,200,50,text="Melta Gun",text_color=(255,255,255))
    granade_gun_button = button.Button((10,10,10),SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.60,200,50,text="Granade Gun",text_color=(255,255,255))
    #Weapons
    mch_gun = Machine_Gun("Machine Gun",0,MCH_GUN_SPEED, MCH_GUN_COOLDOWN)
    railgun = Rail_Gun("Rail Gun",0,RAILGUN_SPEED, RAILGUN_COOLDOWN)
    melta_gun =  Melta_Gun("Melta Gun",0,MELTA_SPEED, MELTA_COOLDOWN)
    granade_gun = GrenadeLauncher("Granade Gun",0,G_LAUNCHER_SPEED, G_LAUNCHER_COOLDOWN)
    #Weapon buttons
    weapon_buttons = {
        mch_gun_button: mch_gun,
        railgun_button: railgun,
        melta_gun_button: melta_gun,
        granade_gun_button: granade_gun
    }
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
    #Timer
    Countdown = 0
    Timer = 0
    Seconder = 0
    Minuter = 0
    Hourer = 0
    #Keys
    keys = pygame.key.get_pressed()
    #Game Loop
    while True:
        #dt
        dt = clock.tick(60) / 1000
        #Timer
        #Exiting and logic switching
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            #Check button clicks based on game state
                if game_state == "EQUIPMENT_SELECTION":
                    if mch_gun_button.isOver(pos):
                        player.equip_weapon(mch_gun)
                        game_state = "PLAYING"

                    elif railgun_button.isOver(pos):
                        player.equip_weapon(railgun)
                        game_state = "PLAYING"

                    elif melta_gun_button.isOver(pos):
                        player.equip_weapon(melta_gun)
                        game_state = "PLAYING"

                    elif granade_gun_button.isOver(pos):
                        player.equip_weapon(granade_gun)
                        game_state = "PLAYING"

            #KeyDown logic
            elif event.type == pygame.KEYDOWN:
                #Tutorial
                if game_state == "START" and (event.key == pygame.K_t):
                    game_state = "TUTORIAL"

                elif game_state == "TUTORIAL" and (event.key == pygame.K_t or pygame.K_ESCAPE):
                    game_state = "START"

                #Start
                elif game_state == "START":
                    game_state = "EQUIPMENT_SELECTION"
                    
                #Deadscreen
                elif game_state == "DEATHSCREEN":
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_ESCAPE:
                        exit()
                #Pause
                elif game_state == "PLAYING" and (event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB):
                    game_state = "PAUSE"

                elif game_state == "PAUSE" and (event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB):
                    game_state = "PLAYING"

                elif game_state == "PAUSE" and (event.key == pygame.K_r):
                    main()
        #Screen
        pygame.Surface.fill(screen, (0,0,0))
        #Version
        draw_text(f"Version: {GAME_VERSION}", text_font, (255,255,255), 3, SCREEN_HEIGHT - 20, centered=False)
        #Gamestate Logic
            #Start
        if game_state == "START":
            draw_text(f"Asteroids", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.30, centered=True)
            draw_text("Press Any Keys to Continue", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, centered=True)
            draw_text("Press T for Tutorial", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 20 , centered=True)
            #Tutorial Drawing
        elif game_state == "TUTORIAL":
            draw_text("Welcome to the tutorial screen:", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.10, centered=False)
            draw_text("Press W to move forward and S to move backwards", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.20, centered=False)
            draw_text("Press A to rotate left and D to rotate right", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.30, centered=False)
            draw_text("Press Space to shoot bullets", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.40, centered=False)
            draw_text("Shoot bullets at asteroids to increase your score", text_font, (255,255,255), SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.50, centered=False)
            #DeathScreen
        elif game_state == "DEATHSCREEN":
            draw_text(f"Your High Score:{current_high_score}", text_font, (255,255,255), 20, 45, centered=False)
            draw_text(f"Your Score: {score}", text_font, (255,255,255), 20, 20, centered=False)
            draw_text("Press R to restart", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2), centered=True)
            draw_text("Or ESC to quit", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 20, centered=True)
            #Equip
        elif game_state == "EQUIPMENT_SELECTION":
            #buttons
            mch_gun_button.draw(screen)
            railgun_button.draw(screen)
            melta_gun_button.draw(screen)
            granade_gun_button.draw(screen)
            #text
            draw_text("Weapons:", text_font, (255,255,255), SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.15, centered=True)
            draw_text("A fast firing weapon", text_font, (255,255,255), SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.30 + 40, centered=True)
            draw_text("A slow yet fast with high penetration", text_font, (255,255,255), SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.30 + 40, centered=True)
            draw_text("A bane of asteroids", text_font, (255,255,255), SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.30 + 40, centered=True)
            draw_text("Mans happiness", text_font, (255,255,255), SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.60 + 40, centered=True)
        #Game
        elif game_state == "PLAYING" or game_state == "PAUSE":
            if game_state == "PAUSE":
                draw_text("Game is paused", text_font, (255,255,255), SCREEN_WIDTH * 0.50, SCREEN_HEIGHT / 2, centered=True)
                draw_text("Press R to restart", text_font, (255,255,255), SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.5 + 20, centered=True)
            elif game_state == "PLAYING":
                #Timer logic
                Timer += dt
                #Sekundy
                if Timer >= 1:
                    Timer -= 1
                    Seconder += 1
                #Minuty
                if Seconder >= 60:
                    Seconder -= 60
                    Minuter += 1
                #Hodiny
                if Minuter >= 60:
                    Hourer += 1
                    Minuter -= 60
                #Update
                for updating in updatable:
                    if isinstance(updating, Player) and updating.equipped_weapon:  # Player with a weapon
                        if updating.equipped_weapon.cooldown > 0:  # Reduce weapon cooldown
                            updating.equipped_weapon.cooldown -= dt
                    updating.update(dt)

                #Collision check
                for steroid in asteroids:
                    if True == steroid.collision_check(player):
                        if score > current_high_score:
                            highscore.save_high_score(score)
                            if game_state == "DEATHSCREEN":
                                draw_text(f"Congratulations you managed to beat you highest score of {current_high_score}!!!", text_font, (255,255,255), SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 40, centered=True)
                            current_high_score = score
                        game_state = "DEATHSCREEN"

                    #Bullet logic checker
                    for bullet in shots:
                        #Melta Life time
                        if player.equipped_weapon == melta_gun or player.equipped_weapon == granade_gun:
                            if (check_max_range(bullet, player.equipped_weapon) == True) and bullet.living_bomb == 0:
                                pygame.sprite.Sprite.kill(bullet)
                            elif bullet.time_to_die() == True:
                                pygame.sprite.Sprite.kill(bullet)

                        if True == steroid.collision_check(bullet):
                            #Railgun and granade launcher Invincible bullet
                            if player.equipped_weapon == granade_gun:
                                bullet.change()

                            if (player.equipped_weapon != railgun) and (player.equipped_weapon != granade_gun):
                                pygame.sprite.Sprite.kill(bullet)

                            #Steroid score logic
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
                                
                        elif (True == bullet_border_check(bullet)) and (player.equipped_weapon != granade_gun):
                            pygame.sprite.Sprite.kill(bullet)
            #Drawing
            for drawing in drawable:
                drawing.draw(screen)
            #Ammo counter for granade launcher
            if player.equipped_weapon == granade_gun:
                if player.equipped_weapon.current_ammo == 5 and player.equipped_weapon.cooldown > 0:
                    draw_text(f"Reloading",text_font, (255,255,255), 3, SCREEN_HEIGHT - 40, centered=False)
                else:
                    draw_text(f"Ammo: {player.equipped_weapon.current_ammo}",text_font, (255,255,255), 3, SCREEN_HEIGHT - 40, centered=False)
            #Score
            draw_text(f"Score: {score}", text_font, (255,255,255), 20, 20, centered=False)
            draw_text(f"High Score:{current_high_score}", text_font, (255,255,255), 20, 45, centered=False)
            #Timer
            draw_text(f"Timer: {display(Seconder,Minuter,Hourer)}", text_font, (255,255,255), SCREEN_WIDTH - 140, 20 , centered=False)
        #Flip       
        pygame.display.flip()


if __name__ == "__main__":
    main()

