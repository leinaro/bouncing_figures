import json


def read_window():
    # Open and read the JSON file
    with open('assets/cfg/window.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data)
    return data


def read_enemies():
    # Open and read the JSON file
    with open('assets/cfg/enemies.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data)
    return data


def read_level():
    # Open and read the JSON file
    with open('assets/cfg/level_01.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data)
    return data