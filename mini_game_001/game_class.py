import pygame


class Game:
    def __init__(self, location):
        self.canvas = pygame.Surface((900, 900))
        self.canvas.fill('Blue')
        self.button = pygame.Rect(100, 100, 150, 200)
        pygame.draw.rect(self.canvas, 'Green', self.button)
        self.done = False
        self.location = location

    def draw(self):
        return self.canvas

    def update(self):
        pass

    def handle_mouse_event(self, mouse_event):
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            mouse_position = self.location.mini_game_mouse_pos()
            if mouse_position is None:
                return
            if not self.button.collidepoint(*mouse_position):
                return

            # Clicked the button
            pygame.draw.rect(self.canvas, 'Red', self.button)
            self.done = True

    def handle_key_event(self):
        pass
