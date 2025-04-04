import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_player_enemy(
        world: esper.World, 
        player_entity: int,
        level_cfg: dict
):
    components = world.get_components(CTransform, CSurface, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = player_surface.surf.get_rect(topleft=player_transform.pos)

    for enemy_entity, (transform, surface, tag_enemy) in components:
        if enemy_entity == player_entity:
            continue
        enemy_rect = surface.surf.get_rect(topleft=transform.pos)
        if player_rect.colliderect(enemy_rect):
            print("Collision detected between player and enemy!")
            world.delete_entity(enemy_entity)
            player_transform.pos.x = level_cfg["player_spawn"]["position"]["x"] - player_surface.surf.get_width() / 2
            player_transform.pos.y = level_cfg["player_spawn"]["position"]["y"] - player_surface.surf.get_height() / 2