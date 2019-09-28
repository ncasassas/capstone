import json

def dict_rendimientos(path):
    with open(path, 'r') as file:
        dict = json.load(file)
        return dict
