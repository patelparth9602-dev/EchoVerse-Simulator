import pygame
import numpy as np
import random
import math

WIDTH, HEIGHT = 1280, 720
FPS = 60
POPULATION_LIMIT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tissue_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()

class Organism:
    def __init__(self, x, y, dna=None):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.dna = dna if dna else [random.random(), 0.05, 500]
        self.health = self.dna[2]
        self.color = [int(self.dna[0]*255), 100, 255]

    def think_and_move(self, target):
        
        diff = target - self.pos
        dist = np.linalg.norm(diff)
        
        self.health -= 0.5
        
      
        if dist < 400:
            strength = self.dna[0] * 2.0
            steering = (diff / (dist + 1)) * strength
            self.vel += steering + np.random.normal(0, 0.1, 2)
            
       
        speed = np.linalg.norm(self.vel)
        if speed > 6: self.vel = (self.vel / speed) * 6
        
        self.pos += self.vel
       
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

    def reproduce(self):
       
        if self.health > 200 and random.random() > 0.98:
            new_dna = [
                np.clip(self.dna[0] + random.uniform(-0.1, 0.1), 0.1, 1.0),
                self.dna[1],
                500
            ]
            self.health -= 250
            return Organism(self.pos[0], self.pos[1], new_dna)
        return None

    def draw(self, surf):
        alpha = int(np.clip(self.health, 0, 255))   
        pygame.draw.circle(surf, self.color + [alpha], (int(self.pos[0]), int(self.pos[1])), 2)
        pygame.draw.line(surf, (0, 255, 255, alpha//2), self.pos, self.pos - self.vel*3, 1)

organisms = [Organism(WIDTH/2, HEIGHT/2) for _ in range(50)]
running = True

while running:
    screen.fill((2, 5, 15))
    tissue_surface.fill((0, 0, 0, 12)) 
    
    target_pos = np.array(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    next_gen = []
    for o in organisms:
        o.think_and_move(target_pos)
        
       
        if np.linalg.norm(o.pos - target_pos) < 30:
            o.health += 10
            
        child = o.reproduce()
        if child and len(organisms) < POPULATION_LIMIT:
            next_gen.append(child)
            
        if o.health > 0:
            next_gen.append(o)
            o.draw(tissue_surface)

    organisms = next_gen
    screen.blit(tissue_surface, (0, 0))

    if random.random() > 0.95:
        font = pygame.font.SysFont("monospace", 14)
        msg = f"COGNITION_LEVEL: {int(len(organisms)/4)}% | HEART_RATE: {60 + len(organisms)//5} BPM"
        text = font.render(msg, True, (0, 255, 100))
        screen.blit(text, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


