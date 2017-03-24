'''EXAMPLE MAIN'''
from concretegame import ConcreteGame
import boids
import pygame


def main():
    """Main execution func."""
    game = ConcreteGame("Concrete Game")
    for iterator in range(12):
        game.addtobatch(boids.Agent((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())))
    # game.addtobatch(boids.Agent(pygame.display.get_surface()))
    # make gameobjects to participate in game
    game.run()


if __name__ == "__main__":

    main()
