import os
from json import load, dumps

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(BASE_DIR, "config.json")

config = {}


def save_config(kp, sp):
    with open(config_path, 'w') as config_file:
        config_file.write(dumps(
            {
                "keyword_pause": kp,
                "ste_pause": sp
            }
        ))
    load_config()


def load_config():
    with open(config_path) as config_file:
        config.update(load(config_file))


def get_config_value(name):
    return config[name]


if not os.path.isfile(config_path):
    save_config(20, 1)

load_config()
