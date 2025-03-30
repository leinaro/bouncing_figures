import pygame

class CEnemySpawner:
    def __init__(self, enemy_spawn_events:list):
        self.enemy_spawn_events = enemy_spawn_events
        self.time = 0.0
        self.spawned_events = set()
