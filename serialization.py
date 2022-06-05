import json
from os.path import exists, join

FILE_NAME = "data.json"

def set_initial_data():
    data = {
        "max_stage": 0,
        "sound_volume": 100,
        "music_volume": 100,
    }

    save_data(data)

    return data


def get_data():
    if exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    
    else:
        return set_initial_data()


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)