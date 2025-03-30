import pygame

class CVelocity:
    def __init__(self, vel: pygame.Vector2):
        """
        Initialize the CVelocity component with a given velocity vector.

        :param vel: A pygame.Vector2 representing the velocity of the entity.
        """
        self.vel = vel

    