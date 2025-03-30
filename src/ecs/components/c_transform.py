import pygame


class CTransform:
    def __init__(self, pos:pygame.Vector2):
        self.pos = pos

    def __repr__(self):
        return f"CTransform(position={self.position}, rotation={self.rotation}, scale={self.scale})"