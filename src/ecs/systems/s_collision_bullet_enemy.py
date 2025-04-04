import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(world: esper.World):
    bullets = world.get_components(CTransform, CSurface, CTagBullet)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)

    for bullet_entity, (bullet_transform, bullet_surface, _) in bullets:
        bullet_rect = bullet_surface.surf.get_rect(topleft=bullet_transform.pos)

        for enemy_entity, (enemy_transform, enemy_surface, _) in enemies:
            enemy_rect = enemy_surface.surf.get_rect(topleft=enemy_transform.pos)

            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
                break 
