import os

import pygame

import location_class


class Game:
    def __init__(self, settings):
        self.fullscreen = settings['screen'].get('fullscreen', False)
        self.size = None if self.fullscreen else (settings['screen']['width'], settings['screen']['height'])

        self.locations = []
        for name in os.listdir('locations'):
            if name.startswith('location_'):
                id = int(name.split('_')[1])
                self.locations.append(location_class.Location(id, self))
        self.active_location = next(location for location in self.locations if location.id == settings['initial_location_id'])
        self.done = False
        self.last_size = None
        self.screen = None
        self.initialise_screen(self.size)
        self.game_active = True

    def toggle_full_screen(self):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            self.last_size = self.size
            self.initialise_screen()

        else:
            self.initialise_screen(self.last_size)

    def initialise_screen(self, screen_size=None):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
        self.size = self.screen.get_size()

    def draw(self):
        screen_image = self.active_location.draw()
        screen_image = pygame.transform.scale(screen_image, self.size)
        self.screen.blit(screen_image, (0, 0))
        pygame.display.flip()

    def handle_key_event(self, key):
        if self.game_active:
            self.active_location.handle_key_event(key)

    def handle_mouse_event(self, event):
        if self.game_active:
            self.active_location.handle_mouse_event(event)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.done = True
                else:
                    self.handle_key_event(event.key)
                # TODO: Get full screen mode working
                # elif event.key == pygame.K_f:
                #     self.toggle_full_screen()
            elif event.type == pygame.VIDEORESIZE:
                self.size = event.dict['size']

            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self.handle_mouse_event(event)

    def run(self):
        clock = pygame.time.Clock()
        while not self.done:
            self.update()
            self.draw()
            clock.tick(15)
