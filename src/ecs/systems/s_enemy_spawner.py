import random
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.create.prefab_creator import create_cuadrado


def system_enemy_spawner(world: esper.World, delta_time:float, enemy_config:dict):
    for entity, spawner in world.get_component(CEnemySpawner):
         spawner.time += delta_time

         for i, event in enumerate(spawner.enemy_spawn_events):

            print(f"spawner time: {spawner.time}")


            if event["time"] <= spawner.time and i not in spawner.spawned_events:
                enemy_type = event["enemy_type"]
                position = pygame.Vector2(event["position"]["x"], event["position"]["y"])
                enemy_data = enemy_config[enemy_type]
                
                size = pygame.Vector2(enemy_data["size"]["x"], enemy_data["size"]["y"])
                color = pygame.Color(enemy_data["color"]["r"], enemy_data["color"]["g"], enemy_data["color"]["b"])
                velocity_value = random.uniform(enemy_data["velocity_min"], enemy_data["velocity_max"])
                velocity = pygame.Vector2(velocity_value, velocity_value)



                create_cuadrado(
                    world,
                    pos=position,
                    size=size,
                    color=color,
                    velocity=velocity
                )
                spawner.spawned_events.add(i)