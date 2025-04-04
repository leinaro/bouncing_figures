import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_fire_bullet import CFireBullet
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.create.prefab_creator import create_bullet


def system_fire_bullet(world: esper.World, bullet_config: dict, max_bullets: int):
    active_bullets = len(world.get_component(CTagBullet))

    if active_bullets >= max_bullets:
        return

    components = world.get_components(CTransform, CSurface, CFireBullet)

    for entity, (transform, surface, fire_bullet) in components:
        player_rect = surface.surf.get_rect(topleft=transform.pos)
        player_center_pos = pygame.Vector2(player_rect.center)

        direction = fire_bullet.pos - player_center_pos
        if direction.length() != 0:
            direction = direction.normalize()

        create_bullet(world, bullet_config, player_center_pos, direction)

        world.remove_component(entity, CFireBullet)