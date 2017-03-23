"""Main file."""
import pygame
import boids
import random
import vectoroperations as vec

random.seed()
pygame.init()
CLOCK = pygame.time.Clock()
if __name__ == "__main__":

    pygame.display.set_mode((1080, 720))
    SCREEN = pygame.display.get_surface()
    BOIDS = []
    TARGETBOID = boids.Boid((SCREEN.get_width(), SCREEN.get_height()))
    TARGETBOID.position = (SCREEN.get_width() / 2, SCREEN.get_height() / 2)
    for itera in range(200):
        BOIDS.append(boids.Boid((SCREEN.get_width(), SCREEN.get_height())))
        BOIDS[itera].position = (random.randrange(0, SCREEN.get_width() + 1),
                                 random.randrange(0, SCREEN.get_height() + 1))
        BOIDS[itera].target = TARGETBOID
    RUNNING = True
    TIMECOUNT = 0
    RAGE = False
    RAGETIMER = 0
    FORCEVECTOR = (0, 0)
    while RUNNING:
        CLOCK.tick(60)

        DELTATIME = float(CLOCK.get_time()) / float(1000)
        TIMECOUNT += DELTATIME
        EVENTS = pygame.event.get()
        pygame.display.set_mode((1080, 720))
        TARGETBOID.position = pygame.mouse.get_pos()
        pygame.draw.circle(SCREEN, (255, 255, 255),
                           (int(round(TARGETBOID.position[0])),
                            int(round(TARGETBOID.position[1]))), 10, 0)
        for event in EVENTS:
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    RAGE = True
        if RAGE:
            RAGETIMER += DELTATIME
        for boid in BOIDS:
            if RAGE:
                boid.wandertimer = 1
                boid.target = TARGETBOID
                boid.maxvelo = 10
                boid.flee(DELTATIME)
                if RAGETIMER > 3:
                    RAGE = False
                    RAGETIMER = 0
            elif vec.get_magnitude(vec.get_dist(boid.position, TARGETBOID.position)) > 200:
                boid.maxvelo = 5
                #boid.centerofmass(BOIDS)
                boid.wander(DELTATIME)
                
            else:
                boid.wandertimer = 1
                boid.target = TARGETBOID
                boid.maxvelo = 10
                boid.seek(DELTATIME)
            pygame.draw.circle(SCREEN, (0, random.randrange(100, 256), random.randrange(0, 150)),
                               (int(round(boid.position[0])),
                               int(round(boid.position[1]))), 10, 0)

        
        
        pygame.display.flip()
