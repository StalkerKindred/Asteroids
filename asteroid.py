import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS,ASTEROID_MAX_RADIUS
class Asteroid(CircleShape):
    def __init__(self, x, y, radius, origin_chain=None):
        super().__init__(x,y,radius)
        self.alive = True
        self.radius = radius
        self.origin_chain = origin_chain or []

    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255),self.position,self.radius,2)      

    def update(self, dt):
        self.position += (self.velocity * dt) 
    
    def split(self):
        if not self.alive:
            return
        self.alive = False
        pygame.sprite.Sprite.kill(self)
        if self.radius == ASTEROID_MIN_RADIUS:
            return
        else:
            new_origin_chain = self.origin_chain.copy()
            if self.radius == ASTEROID_MAX_RADIUS:
                new_origin_chain.append("big")
            elif self.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:
                new_origin_chain.append("medium")
            
            angle = random.uniform(20,50)
            A1 = Asteroid(self.position.x, self.position.y, (self.radius - ASTEROID_MIN_RADIUS ),  origin_chain=new_origin_chain)
            A2 = Asteroid(self.position.x, self.position.y, (self.radius - ASTEROID_MIN_RADIUS ),  origin_chain=new_origin_chain)
            A1.velocity = pygame.math.Vector2.rotate(self.velocity, angle) * 1.2
            A2.velocity = pygame.math.Vector2.rotate(self.velocity, -angle) * 1.2