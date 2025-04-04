import random
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def create_player_square(
    ecs_world: esper.World, 
    player_config: dict, 
    player_spawn: dict
) -> int:
    size = pygame.Vector2(player_config['size']['x'], player_config['size']['y'])
    pos = pygame.Vector2(player_spawn['position']['x'] - size.x/2, player_spawn['position']['y'] - size.y/2)
    color = pygame.Color(player_config['color']['r'], player_config['color']['g'], player_config['color']['b'])
    velocity = pygame.Vector2(0, 0)
    

    player = create_cuadrado(ecs_world, pos, size, color, velocity)

    ecs_world.add_component(
        player, 
        CTagPlayer()
    )

    return player

def create_enemy_square(
    ecs_world: esper.World, 
    enemy_config: dict, 
    enemy_spawn: dict
) -> int:
    size = pygame.Vector2(enemy_config['size']['x'], enemy_config['size']['y'])
    pos = pygame.Vector2(enemy_spawn['position']['x'] - size.x/2, enemy_spawn['position']['y'] - size.y/2)
    color = pygame.Color(enemy_config['color']['r'], enemy_config['color']['g'], enemy_config['color']['b'])            
    velocity_value = random.uniform(enemy_config["velocity_min"], enemy_config["velocity_max"])
    velocity = pygame.Vector2(velocity_value, velocity_value)

    enemy = create_cuadrado(ecs_world, pos, size, color, velocity)

    ecs_world.add_component(
        enemy, 
        CTagEnemy()
    )

    return enemy

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

def create_input_player(ecs_world: esper.World):
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_up = ecs_world.create_entity()
    input_down = ecs_world.create_entity()
    input_fire = ecs_world.create_entity()

    ecs_world.add_component(
        input_left,
        CInputCommand("PLAYER_LEFT", pygame.K_LEFT)
    )
    ecs_world.add_component(
        input_right,
        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT)
    )
    ecs_world.add_component(
        input_up,
        CInputCommand("PLAYER_UP", pygame.K_UP)
    )
    ecs_world.add_component(
        input_down,
        CInputCommand("PLAYER_DOWN", pygame.K_DOWN)
    )
    
    ecs_world.add_component(
        input_fire,
        CInputCommand("PLAYER_FIRE", pygame.MOUSEBUTTONDOWN)
    )

def create_bullet(
    ecs_world: esper.World, 
    bullet_config: dict, 
    player_pos: pygame.Vector2, 
    direction: pygame.Vector2
) -> int:
    size = pygame.Vector2(bullet_config['size']['x'], bullet_config['size']['y'])
    color = pygame.Color(bullet_config['color']['r'], bullet_config['color']['g'], bullet_config['color']['b'])            
    velocity = direction*bullet_config["velocity"]
    pos = pygame.Vector2(player_pos.x-(size.x/2), player_pos.y-(size.y/2))

    bullet = create_cuadrado(ecs_world, pos, size, color, velocity)

    ecs_world.add_component(
        bullet, 
        CTagBullet()
    )


    return bullet