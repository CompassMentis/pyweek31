import pygame
import random

from mini_game_class import MiniGame


class Button:
    def __init__(self, click_area, row, column):
        self.click_area = click_area
        self.row = row
        self.column = column

    def was_clicked(self, mouse_position):
        return self.click_area.collidepoint(*mouse_position)


class Game(MiniGame):
    def __init__(self, location):
        super().__init__(location)
        self.size = self.settings['size']
        self.tile_size = 900 // self.size
        self.tiles = self.load_tiles()
        self.grid = self.create_grid()
        self.shuffle_tiles(5)
        self.buttons = None

    def create_grid(self):
        grid = []
        coordinates = []
        for row in range(self.size):
            grid.append([])
            for column in range(self.size):
                grid[row].append(row * self.size + column)
                coordinates.append((row, column))

        grid[1][1] = None

        return grid

    def load_tiles(self):
        image = pygame.image.load(f'{self.location.image_path}puzzle.png')
        result = []
        for row in range(self.size):
            for column in range(self.size):
                x = column * self.tile_size
                y = row * self.tile_size
                tile = image.subsurface([x, y, self.tile_size, self.tile_size])
                result.append(tile)

        return result

    def get_empty_cell(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.grid[row][column] is None:
                    return row, column

    def create_buttons(self):
        buttons = []
        row, column = self.get_empty_cell()
        for row_offset, column_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r = row + row_offset
            c = column + column_offset
            if r < 0 or c < 0 or r >= self.size or c >= self.size:
                continue
            buttons.append(Button(
                pygame.Rect(c * self.tile_size, r * self.tile_size, self.tile_size, self.tile_size),
                r,
                c
            ))
        return buttons

    def draw(self):
        self.canvas.fill('Black')
        for row in range(self.size):
            for column in range(self.size):
                tile_number = self.grid[row][column]
                if tile_number is None:
                    continue
                tile = self.tiles[tile_number]
                self.canvas.blit(tile, (column * self.tile_size, row * self.tile_size))
        if not self.done:
            self.buttons = self.create_buttons()

        return self.canvas

    def swap_tiles(self, row, column):
        empty_row, empty_column = self.get_empty_cell()
        self.grid[empty_row][empty_column] = self.grid[row][column]
        self.grid[row][column] = None

    def check_completion(self):
        for row in range(self.size):
            for column in range(self.size):
                cell = self.grid[row][column]
                if cell is not None and cell != row * self.size + column:
                    return

        empty_row, empty_column = self.get_empty_cell()
        self.grid[empty_row][empty_column] = empty_row * self.size + empty_column
        self.game_completion()

    def handle_mouse_event(self, mouse_event):
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            mouse_position = self.location.mini_game_mouse_pos()
            for button in self.buttons:
                if button.was_clicked(mouse_position):
                    self.swap_tiles(button.row, button.column)
                    self.check_completion()
                    return

    def swap_random(self):
        empty_row, empty_column = self.get_empty_cell()
        while True:
            row_offset, column_offset= random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            r = empty_row + row_offset
            c = empty_column + column_offset
            if r < 0 or c < 0 or r >= self.size or c >= self.size:
                continue
            self.swap_tiles(r, c)
            break

    def shuffle_tiles(self, times):
        for _ in range(times):
            self.swap_random()
