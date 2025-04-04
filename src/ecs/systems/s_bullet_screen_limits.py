import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullet_screen_limits(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    bullet_components = world.get_components(CTransform, CSurface, CTagBullet)

    for bullet_entity, (c_transform, c_surface, _) in bullet_components:
        bullet_rect = c_surface.surf.get_rect(topleft=c_transform.pos)

        #if not screen_rect.colliderect(bullet_rect):
        #    world.delete_entity(bullet_entity)
    
        if bullet_rect.left < screen_rect.left:
            bullet_rect.left = screen_rect.left
            world.delete_entity(bullet_entity)
        elif bullet_rect.right > screen_rect.right:
            bullet_rect.right = screen_rect.right
            world.delete_entity(bullet_entity)

        if bullet_rect.top < screen_rect.top:
            bullet_rect.top = screen_rect.top
            world.delete_entity(bullet_entity)
        elif bullet_rect.bottom > screen_rect.bottom:
            bullet_rect.bottom = screen_rect.bottom
            world.delete_entity(bullet_entity)
