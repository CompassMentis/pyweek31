import pygame


class MiniGame:
    def __init__(self, location):
        self.canvas = pygame.Surface((900, 900))
        self.done = False
        self.location = location
        self.settings = location.settings
        self.id = self.settings['mini_game_id']
        self.path = f'mini_game_{self.id:03}/'
        self.image_path = self.path + 'images/'

    def draw(self):
        pass

    def update(self):
        pass

    def handle_mouse_event(self, mouse_event):
        pass

    def handle_key_event(self, key_event):
        pass

    def game_completion(self):
        self.done = True
        for location in self.location.next_locations:
            location.unlocked = True
