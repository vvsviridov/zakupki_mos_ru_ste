import os
from json import load, dumps


config_path = "config.json"

config = {}


def save_config(sp, sd, ed, bf, bt):
    with open(config_path, 'w') as config_file:
        config_file.write(dumps(
            {
                # "keyword_pause": kp,
                "ste_pause": sp,
                "start": sd,
                "end": ed,
                "bet_from": bf,
                "bet_to": bt,
            }
        ))
    load_config()


def load_config():
    with open(config_path) as config_file:
        config.update(load(config_file))


def get_config_value(name):
    return config[name]


if not os.path.isfile(config_path):
    save_config(1, "22.05.2021", "23.05.2021", "", "")

load_config()
