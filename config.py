import os
from json import load, dumps


config_path = "config.json"

config = {
    "keyword_pause": 20,
    "ste_pause": 10
}


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
