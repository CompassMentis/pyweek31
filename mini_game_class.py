import pygame


class MiniGame:
    def __init__(self, location):
        self.canvas = pygame.Surface((900, 900))
        self.done = False
        self.location = location

    def draw(self):
        pass

    def update(self):
        pass

    def handle_mouse_event(self, mouse_event):
        pass

    def handle_key_event(self, key_event):
        pass
