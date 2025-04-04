import json
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_fire_bullet import CFireBullet
from src.ecs.create.prefab_creator import create_bullet, create_input_player, create_player_square, create_spawner
from src.ecs.json.json_interpreter import read_enemies, read_level, read_window
from src.ecs.systems.s_bullet_screen_limits import system_bullet_screen_limits
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_fire_bullet import system_fire_bullet
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_limits import system_screen_limits


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()

        self._setup_screen()

        self.ecs_world = esper.World()

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.screen_config = json.load(window_file)
        with open("assets/cfg/enemies.json") as enemy_file:
            self.enemy_config = json.load(enemy_file)
        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_config = json.load(level_01_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_config = json.load(player_file)
        with open("assets/cfg/bullet.json") as bullet_file:
            self.bullet_config = json.load(bullet_file)
        

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
        self._player_entity = create_player_square(self.ecs_world, self.player_config, self.level_config['player_spawn'])
        self._player_c_vel = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_surface = self.ecs_world.component_for_entity(self._player_entity, CSurface)

        create_spawner(self.ecs_world, self.level_config['enemy_spawn_events'])
        create_input_player(self.ecs_world)


    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)        
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemy_config)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_config)
        system_screen_limits(self.ecs_world, self.screen)
        system_fire_bullet(self.ecs_world, self.bullet_config, self.level_config["player_spawn"]["max_bullets"])
        system_bullet_screen_limits(self.ecs_world, self.screen)
        system_collision_bullet_enemy(self.ecs_world)

        self.ecs_world._clear_dead_entities()
       
    def _draw(self):
        self.screen.fill(
            (self.screen_config["bg_color"]["r"],
            self.screen_config["bg_color"]["g"],
            self.screen_config["bg_color"]["b"])
        )

        system_rendering(self.ecs_world, self.screen)
        
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
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

    def _do_action(self, c_input: CInputCommand):
        if c_input.phase == c_input.phase.START:
            if c_input.name == "PLAYER_LEFT":
                self._player_c_vel.vel.x = -self.player_config["input_velocity"]
            elif c_input.name == "PLAYER_RIGHT":
                self._player_c_vel.vel.x = self.player_config["input_velocity"]
            elif c_input.name == "PLAYER_UP":
                self._player_c_vel.vel.y = -self.player_config["input_velocity"]
            elif c_input.name == "PLAYER_DOWN":
                self._player_c_vel.vel.y = self.player_config["input_velocity"]
            elif c_input.name == "PLAYER_FIRE":
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                self.ecs_world.add_component(self._player_entity, CFireBullet(mouse_pos))

        elif c_input.phase == c_input.phase.END:
            if c_input.name in ["PLAYER_LEFT", "PLAYER_RIGHT"]:
                self._player_c_vel.vel.x = 0
            elif c_input.name in ["PLAYER_UP", "PLAYER_DOWN"]:
                self._player_c_vel.vel.y = 0
            elif c_input.name == "PLAYER_FIRE":
                print("...Shooting...")
        