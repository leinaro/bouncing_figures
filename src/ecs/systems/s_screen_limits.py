import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_screen_limits(world: esper.World, screen: pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    player_components = world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)
    
    for entity, (transform, velocity, surface, tag_player) in player_components:
        cuad_rect = surface.surf.get_rect(topleft=transform.pos)

        if cuad_rect.left < screen_rect.left:
            cuad_rect.left = screen_rect.left
            velocity.vel.x = 0
        elif cuad_rect.right > screen_rect.right:
            cuad_rect.right = screen_rect.right
            velocity.vel.x = 0

        if cuad_rect.top < screen_rect.top:
            cuad_rect.top = screen_rect.top
            velocity.vel.y = 0
        elif cuad_rect.bottom > screen_rect.bottom:
            cuad_rect.bottom = screen_rect.bottom
            velocity.vel.y = 0
