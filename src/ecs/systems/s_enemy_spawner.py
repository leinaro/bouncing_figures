import random
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.create.prefab_creator import create_cuadrado, create_enemy_square


def system_enemy_spawner(world: esper.World, delta_time:float, enemy_config:dict):
    for entity, spawner in world.get_component(CEnemySpawner):
         spawner.time += delta_time

         for i, event in enumerate(spawner.enemy_spawn_events):

            if event["time"] <= spawner.time and i not in spawner.spawned_events:
                enemy_type = event["enemy_type"]
                enemy_data = enemy_config[enemy_type]
                
                create_enemy_square(
                    world,
                    enemy_config=enemy_data,
                    enemy_spawn=event
                )

                spawner.spawned_events.add(i)