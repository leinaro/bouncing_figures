import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(world: esper.World, delta_time:float) -> None:
    components = world.get_components(CTransform, CVelocity)
    for entity, (transform, velocity) in components:
        transform.pos.x += velocity.vel.x * delta_time
        transform.pos.y += velocity.vel.y * delta_time