import pygame
from constants import PLAYER_RADIUS ,PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN
from circleshape import CircleShape

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self, Shot):
        if self.cooldown > 0:
            return False
        if self.cooldown < 0:
            self.cooldown = 0
            
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        new_shot = Shot(self.position, velocity)
        self.cooldown += PLAYER_SHOOT_COOLDOWN

    def update(self, dt):
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
            self.shoot(Shot)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen,(255,255,255),self.triangle(),2)    
    
class Shot(CircleShape):
    def __init__(self, position, velocity):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.velocity = pygame.math.Vector2(velocity)
        self.position = pygame.math.Vector2(position)

    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255),self.position,self.radius,2)      

    def update(self, dt):
        self.position += (self.velocity * dt) 

