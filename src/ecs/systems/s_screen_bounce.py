import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_screen_bounce(world: esper.World, screen: pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    
    for entity, (transform, velocity, surface, tag_enemy) in components:
        cuad_rect = surface.surf.get_rect(topleft=transform.pos)

        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            velocity.vel.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            transform.pos.x = cuad_rect.x

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            velocity.vel.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            transform.pos.y = cuad_rect.y
