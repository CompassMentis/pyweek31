import collections

import pygame

from mini_game_class import MiniGame


class Button:
    """
    Mouse click area
    tile name (a, b, c, etc)
    New tile positions - list of (x, y)
    """
    def __init__(self, game, tile_name, click_area, new_tile_position):
        self.game = game
        self.tile_name = tile_name
        self.click_area = pygame.Rect(click_area)
        self.new_tile_position = new_tile_position
        self.clicked = False

    def was_clicked(self, mouse_position):
        if self.clicked:
            return False
        return self.click_area.collidepoint(*mouse_position)

    def execute(self):
        grid = self.game.grid
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == self.tile_name:
                    grid[y][x] = ''
        for x, y in self.new_tile_position:
            grid[y][x] = self.tile_name
        self.clicked = True


class Game(MiniGame):
    def __init__(self, location):
        super().__init__(location)
        self.grid = self.grid_from_settings(self.settings['grid_start'])
        self.row_count = len(self.grid)
        self.column_count = len(self.grid[0])
        self.cell_width = 900 // self.column_count
        self.cell_height = 900 // self.row_count
        self.images = self.load_images()
        self.buttons = self.create_buttons()
        # TODO, maybe: add a background image

    def can_move_to(self, name, positions):
        for x, y in positions:
            if x < 0 or x > self.column_count - 1:
                return False
            if y < 0 or y > self.row_count - 1:
                return False
            if self.grid[y][x] not in [name, '']:
                return False
        return True

    def click_area_for_square(self, position, direction):
        offset = {
            'left': (-1, 1),
            'right': (3, 1),
            'up': (1, -1),
            'down': (1, 3)
        }[direction]

        x, y = position

        return (
            (x + offset[0] / 3) * self.cell_width,
            (y + offset[1] / 3) * self.cell_height,
            self.cell_width // 3,
            self.cell_height // 3
        )

    def get_buttons_for_tile(self, name, positions):
        top_left = min(positions)
        bottom_right = max(positions)
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        if width == height:
            direction = 'both'
        elif width > height:
            direction = 'horizontal'
        else:
            direction = 'vertical'

        result = []

        if direction in ['both', 'horizontal']:
            left_positions = [(x - 1, y) for (x, y) in positions]
            if self.can_move_to(name, left_positions):
                click_area = self.click_area_for_square(positions[0], 'left')
                result.append(Button(self, name, click_area, left_positions))

            right_positions = [(x + 1, y) for (x, y) in positions]
            if self.can_move_to(name, right_positions):
                click_area = self.click_area_for_square(positions[-1], 'right')
                result.append(Button(self, name, click_area, right_positions))

        if direction in ['both', 'vertical']:
            up_positions = [(x, y - 1) for (x, y) in positions]
            if self.can_move_to(name, up_positions):
                click_area = self.click_area_for_square(positions[0], 'up')
                result.append(Button(self, name, click_area, up_positions))

            down_positions = [(x, y + 1) for (x, y) in positions]
            if self.can_move_to(name, down_positions):
                click_area = self.click_area_for_square(positions[-1], 'down')
                result.append(Button(self, name, click_area, down_positions))

        return result

    def create_buttons(self):
        """
        Square tiles can move in any direction
        Rectangular tiles can only move along their longest axis
        Cannot move off the board
        Cannot move so it overlaps with another tile
        """
        if self.done:
            return []

        result = []

        block_positions = self.get_block_positions()
        for name, position in block_positions.items():
            result += self.get_buttons_for_tile(name, position)

        return result

    def load_images(self):
        # TODO: rotate images once loaded - see the board
        return {
            name: pygame.image.load(f'{self.image_path}{image_name}.png')
            for name, image_name in self.settings['tile_images'].items()
        }

    @staticmethod
    def grid_from_settings(raw_grid):
        return [
            [char.replace('.', '') for char in line.split()]
            for line in raw_grid
        ]

    def get_block_positions(self):
        block_positions = collections.defaultdict(list)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                block_positions[cell].append((x, y))
        return block_positions

    def game_finished(self):
        block_positions = self.get_block_positions()
        return list(block_positions['x'][0]) == list(self.settings['finish_position'])

    def draw(self):
        if self.done:
            self.canvas.fill('Blue')
        else:
            self.canvas.fill('White')
        block_positions = self.get_block_positions()

        for name, positions in block_positions.items():
            top_left = min(positions)
            bottom_right = max(positions)
            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]
            image = self.images[name]
            if height > width:
                image = image.copy()
                image = pygame.transform.rotate(image, 90)

            x = top_left[0] * self.cell_width
            y = top_left[1] * self.cell_height
            self.canvas.blit(image, (x, y))

        for button in self.buttons:
            # Todo: replace squares with arrows
            pygame.draw.rect(self.canvas, 'Green', button.click_area)

        return self.canvas

    # TODO: Replace clicking squares with drag and drop
    def handle_mouse_event(self, mouse_event):
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            mouse_position = self.location.mini_game_mouse_pos()
            if mouse_position is None:
                return

            for button in self.buttons:
                if button.was_clicked(mouse_position):
                    button.execute()
                    if self.game_finished():
                        self.done = True
                    self.buttons = self.create_buttons()
                    return
