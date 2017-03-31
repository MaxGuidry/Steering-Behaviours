"""EXAMPLE MAIN."""
from concretegame import ConcreteGame
import boids
import pygame


def main():
    """Main execution func."""
    game = ConcreteGame("Concrete Game")
    for _ in range(1):
        game.addtobatch(boids.Agent((pygame.display.get_surface(
        ).get_width(), pygame.display.get_surface().get_height()), 75, 50))
    game.run()


if __name__ == "__main__":

    main()
