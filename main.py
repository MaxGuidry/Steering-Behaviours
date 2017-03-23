"""Main file."""
import pygame
import boids
import random


random.seed()
pygame.init()
CLOCK = pygame.time.Clock()
if __name__ == "__main__":
    
    pygame.display.set_mode((1080, 720))
    SCREEN = pygame.display.get_surface()
    BOIDS = []
    TARGETBOID = boids.Boid((SCREEN.get_width(), SCREEN.get_height()))
    TARGETBOID.position = (SCREEN.get_width() / 2, SCREEN.get_height() / 2)
    for itera in range(10):
        BOIDS.append(boids.Boid((SCREEN.get_width(), SCREEN.get_height())))
        BOIDS[itera].position = (random.randrange(0, SCREEN.get_width() + 1),
                                 random.randrange(0, SCREEN.get_height() + 1))
        BOIDS[itera].target = TARGETBOID
    RUNNING = True
    while RUNNING:
        CLOCK.tick(60)
        DELTATIME = float(CLOCK.get_time()) / float(1000)
        EVENTS = pygame.event.get()
        pygame.display.set_mode((1080, 720))
        for event in EVENTS:    
            if event.type == pygame.QUIT:
                RUNNING = False
        for boid in BOIDS:
            boid.seek(DELTATIME)
            pygame.draw.circle(SCREEN, (255, 0, 0),
                               (int(round(boid.position[0])),
                                int(round(boid.position[1]))), 10, 0)
        pygame.draw.circle(SCREEN, (255, 255, 255),
                           (int(round(TARGETBOID.position[0])),
                            int(round(TARGETBOID.position[1]))), 10, 0)
        TARGETBOID.position = pygame.mouse.get_pos()
        pygame.display.flip()
