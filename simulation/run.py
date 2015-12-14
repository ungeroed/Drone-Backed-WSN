from gui import NodeGUI, DroneGUI, FloorGUI
from actor import NodeActor, DroneActor, FloorActor
from world import World

# Application entry point
if __name__ == '__main__':
    world_definition = [
        {
            "name": "floor",
            "position": [0, 0, 0, 0],
            "gui_constructor": FloorGUI,
            "actor_constructor": FloorActor,
        },
        {
            "name": "node1",
            "position": [0, 0, 0, 0],
            "gui_constructor": NodeGUI,
            "actor_constructor": NodeActor,
        },
        {
            "name": "drone",
            "position": [100, 100, 100, 0],
            "gui_constructor": DroneGUI,
            "actor_constructor": DroneActor,
        },
    ]
    w = World(world_definition)
    w.start()
