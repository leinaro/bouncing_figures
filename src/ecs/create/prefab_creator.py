import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_spawner(
        ecs_world: esper.World,
        enemy_spawn_events: list
) -> int:
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(
        spawner_entity,
        CEnemySpawner(enemy_spawn_events)
    )
    return spawner_entity

def create_cuadrado(
    ecs_world: esper.World, 
    pos: pygame.Vector2, 
    size: pygame.Vector2, 
    color: pygame.Color, 
    velocity: pygame.Vector2
) -> int:
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(
        cuad_entity, 
        CSurface(size, color)
    )

    ecs_world.add_component(
        cuad_entity, 
        CTransform(pos)
    )

    ecs_world.add_component(
        cuad_entity, 
        CVelocity(velocity)
    )
    return cuad_entity    