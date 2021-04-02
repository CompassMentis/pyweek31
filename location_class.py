import yaml

import pygame
from PIL import Image


class Location:
    def __init__(self, id, game):
        self.id = id
        self.game = game
        self.path = f'locations/location_{id:03}/'
        self.image_path = f'{self.path}/images/'
        # TODO: Lazy image loading
        self.background = pygame.image.load(self.image_path + 'background.png')
        self.map_image = pygame.transform.scale(pygame.image.load(self.image_path + 'map.png'), (1920, 1080))

        # TODO: Convert PIL image to PyGame or vice versa
        # .. or pre-calculate room boundaries
        self.map_button_area = self.get_button_area()

        self.unlocked = False
        self.next_locations = []
        self.first_visit = True
        self.show_intro_text = True
        self.intro_text_image = pygame.image.load(self.image_path + 'intro_text.png')

        with open(f'{self.path}settings.yml') as input_file:
            self.settings = yaml.load(input_file, Loader=yaml.Loader)

        game_area_image = Image.open(self.image_path + 'mini_game_area.png')
        self.settings['game_location'] = game_area_image.getbbox()[0:2]
        self.settings['game_size'] = (
            game_area_image.getbbox()[2] - game_area_image.getbbox()[0],
            game_area_image.getbbox()[3] - game_area_image.getbbox()[1]
        )
        mini_game_id = self.settings.get('mini_game_id')
        if mini_game_id is not None:
            assert isinstance(mini_game_id, int)
            game_name = f'mini_game_{mini_game_id:03}'
            exec('import ' + game_name)
            self.mini_game = locals()[game_name].Game(self)

    def get_button_area(self):
        map_image = Image.open(self.image_path + 'map.png').resize((1920, 1080))
        bbox = map_image.getbbox()
        margin = 10
        x, y, width, height = bbox[0] + margin, \
                              bbox[1] + margin, \
                              bbox[2] - bbox[0] - margin * 2, \
                              bbox[3] - bbox[1] - margin * 2
        return pygame.Rect(x, y, width, height)

    def map_button_size(self):
        return self.map_button_area[2] * self.map_button_area[3]

    def mouse_in_area(self, mouse_position):
        return self.map_button_area.collidepoint(*mouse_position)

    def set_next_locations(self):
        self.next_locations = [
            self.game.location_for_id(id)
            for id in self.game.settings['location_tree'].get(self.id, [])
        ]

    def handle_key_event(self, key):
        if self.mini_game:
            self.mini_game.handle_key_event(key)

    def handle_mouse_event(self, event):
        if self.mini_game:
            self.mini_game.handle_mouse_event(event)

    def mini_game_mouse_pos(self):
        if not self.mini_game:
            return None

        x, y = pygame.mouse.get_pos()

        # scale to the window size
        x = x / self.game.size[0] * 1920
        y = y / self.game.size[1] * 1080

        # make relative to top left hand corner of game area
        x -= self.settings['game_location'][0]
        y -= self.settings['game_location'][1]

        # Scale size
        x = int(x / self.settings['game_size'][0] * 900)
        y = int(y / self.settings['game_size'][1] * 900)
        return x, y

    def draw(self):
        result = self.background.copy()

        if self.show_intro_text:
            result.blit(self.intro_text_image, (0, 0))

        if self.mini_game:
            game_image = self.mini_game.draw()
            game_image = pygame.transform.scale(game_image, self.settings['game_size'])
            result.blit(game_image, self.settings['game_location'])

        return result
