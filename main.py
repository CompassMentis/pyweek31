import yaml
import flatten_dict

from game_class import Game


def load_settings():
    with open('settings.yml') as input_file:
        settings = yaml.load(input_file, Loader=yaml.Loader)

    try:
        with open('local_settings.yml') as input_file:
            local_settings = yaml.load(input_file, Loader=yaml.Loader)
    except FileNotFoundError:
        local_settings = {}

    if local_settings:
        settings = flatten_dict.flatten(settings)
        local_settings = flatten_dict.flatten(local_settings)
        settings.update(local_settings)
        settings = flatten_dict.unflatten(settings)
    return settings


settings = load_settings()
game = Game(settings)
game.run()
