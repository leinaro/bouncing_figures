import json


def read_window():
    # Open and read the JSON file
    with open('src/ecs/json/configuracion/window.json', 'r') as file:
        data = json.load(file)
        title = data['title']
        size = data['size']
        bg_color = data['bg_color']
        frame_rate = data['framerate']


    # Print the data
    print(data)
    return data


def read_enemies():
    # Open and read the JSON file
    with open('src/ecs/json/configuracion/enemies.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data)
    return data


def read_level():
    # Open and read the JSON file
    with open('src/ecs/json/configuracion/level_01.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data)
    return data