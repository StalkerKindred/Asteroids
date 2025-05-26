import pygame
import random
import math
from constants import *
from circleshape import CircleShape
class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y, PLAYER_RADIUS)
        self.rotation = 0
        self.equipped_weapon = None

    def equip_weapon(self, weapon):
        self.equipped_weapon = weapon

    def check_weapon(self):
        return self.equipped_weapon

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.equipped_weapon and self.equipped_weapon.can_shoot():
            self.equipped_weapon.rotation = self.rotation
            velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            return self.equipped_weapon.shoot(self.position, velocity)
        else:
            if self.equipped_weapon == None:
                print("no weapon")
            return False            

    def update(self, dt):
        if self.equipped_weapon and self.equipped_weapon.cooldown > 0:
            self.equipped_weapon.cooldown -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen,(255,255,255),self.triangle(),2)  

#Drawable Shot Object
class Shot(CircleShape):
    def __init__(self, position, velocity):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.velocity = pygame.math.Vector2(velocity)
        self.position = pygame.math.Vector2(position)
        self.initial_position = pygame.math.Vector2(position)
        self.living_bomb = 0
        self.lifetime = G_LAUNCHER_LIFETIME

    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255),self.position,self.radius,2)      

    def update(self, dt):
        self.position += (self.velocity * dt)
        if self.living_bomb == 1:
            self.lifetime -= dt
        
    def change(self):
        self.living_bomb = 1
        self.radius = float(G_LAUNCHER_AOE)
        self.velocity = pygame.math.Vector2(0,0)

    def time_to_die(self):
        if self.lifetime <= 0:
            return True
        else:
            return False

#Weapon Equipment
    #Weapon class for logic 
class Weapon:
    def __init__(self, name, rotation, shoot_speed, cooldown):
        self.name = name
        self.rotation = rotation
        self.shoot_speed = shoot_speed
        self.cooldown = cooldown

    def can_shoot(self):
        return self.cooldown <= 0

    def shoot(self, position, velocity):
        raise NotImplementedError("This method should be implemented by subclasses")

class Rail_Gun(Weapon):
    def shoot(self, position, velocity):
            if self.can_shoot():
                self.cooldown = RAILGUN_COOLDOWN
                velocity = pygame.Vector2(0, 1).rotate(self.rotation) * RAILGUN_SPEED
                return Shot(position, velocity)

class Machine_Gun(Weapon):
    def shoot(self, position, velocity):
            if self.can_shoot():
                self.cooldown = MCH_GUN_COOLDOWN
                velocity = pygame.Vector2(0, 1).rotate(self.rotation) * MCH_GUN_SPEED
                return Shot(position, velocity)

class GrenadeLauncher(Weapon):
    max_range = MAX_G_LAUNCHER_RANGE
    current_ammo = G_LAUNCHER_AMMO
    max_ammo = G_LAUNCHER_AMMO

    def re_loading(self):
        self.cooldown += G_LAUNCHER_RELOAD
        self.current_ammo += G_LAUNCHER_AMMO
        
    def can_shoot(self):
        return self.cooldown <= 0 and self.current_ammo >= 1

    def shoot(self, position, velocity):
            if self.can_shoot():
                self.cooldown = G_LAUNCHER_COOLDOWN
                velocity = pygame.Vector2(0, 1).rotate(self.rotation) * G_LAUNCHER_SPEED
                self.current_ammo -= 1
                if self.current_ammo == 0:
                    self.re_loading()
                return Shot(position, velocity)

class Melta_Gun(Weapon):
    max_range = MELTA_MAX_RANGE
    def shoot(self, position, velocity):
        if self.can_shoot():
            #Gen 7 shots
            shots = []
            angles = [random.uniform(-31,31) for _ in range(7)]
            for angle in angles:
                velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle) * MELTA_SPEED
                shots.append(Shot(position, velocity))   
            self.cooldown = MELTA_COOLDOWN
            return shots

        
def bullet_border_check(bullet):
    if bullet.position.x > SCREEN_WIDTH + 10 or bullet.position.x < 0 - 10 or bullet.position.y > SCREEN_HEIGHT + 10 or bullet.position.y < 0 - 10:
        return True
    else:
        return False

def check_max_range(bullet, weapon):
    if (abs(bullet.position.x - bullet.initial_position.x) > weapon.max_range or abs(bullet.position.y - bullet.initial_position.y) > weapon.max_range) == True:
        return True