import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.json.json_interpreter import read_enemies, read_level, read_window
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce


class GameEngine:
    screen_config = read_window()
    enemy_config = read_enemies()
    level_config = read_level()


    def __init__(self) -> None:
        pygame.init()
        
        self._setup_screen()

        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        spawner_entity = self.ecs_world.create_entity()
        enemy_spawn_events = self.level_config['enemy_spawn_events']
        self.ecs_world.add_component(
            spawner_entity,
            CEnemySpawner(enemy_spawn_events)
        )


    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)        
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemy_config)
        pass

       
    def _draw(self):
        self.screen.fill(
            (self.screen_config["bg_color"]["r"],
            self.screen_config["bg_color"]["g"],
            self.screen_config["bg_color"]["b"])
        )

        system_rendering(self.ecs_world, self.screen)
        
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def _setup_screen(self):
        w = self.screen_config["size"]["w"]
        h = self.screen_config["size"]["h"]
        title = self.screen_config["title"]

        self.screen = pygame.display.set_mode((w, h), pygame.SCALED)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = self.screen_config.get("framerate", 60)
        self.delta_time = 0