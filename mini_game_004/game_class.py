import pygame
from PIL import Image

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
        self.image_path += f'{self.size}x{self.size}/'
        self.background = pygame.image.load(self.image_path + 'background.png')
        self.grid_lines = self.load_grid_lines()
        self.grid = self.grid_from_starting_position()
        self.solution = [int(number) for number in self.settings['target_code'].split()]
        self.font = pygame.font.SysFont('Courier New', 70, bold=True)
        self.buttons = None

    def grid_from_starting_position(self):
        result = []
        for row in range(self.size):
            result.append([])
            line = self.settings['starting_position'][row]
            for part in line.split():
                result[row].append('' if part == '.' else int(part))
        return result

    def load_grid_lines(self):
        result = dict(y=dict(), x=dict())
        for i in range(self.size):
            image = Image.open(f'{self.image_path}h{i + 1}.png')
            bbox = image.getbbox()
            result['y'][i] = bbox[1], bbox[3]

            image = Image.open(f'{self.image_path}v{i + 1}.png')
            bbox = image.getbbox()
            result['x'][i] = bbox[0], bbox[2]

        return result

    def draw(self):
        self.canvas.blit(self.background, (0, 0))
        if self.done:
            return self.canvas

        for row in range(self.size):
            for column in range(self.size):
                x1, x2 = self.grid_lines['x'][column]
                for row in range(self.size):
                    y1, y2 = self.grid_lines['y'][row]
                    font_image = self.font.render(str(self.grid[row][column]), True, 'Black')
                    x = x1 // 2 + x2 // 2 - font_image.get_width() // 2
                    self.canvas.blit(font_image, (x, y1 + 5))

        self.buttons = self.create_buttons()

        return self.canvas

    def create_buttons(self):
        buttons = []
        for row in range(self.size):
            for column in range(self.size):
                x1, x2 = self.grid_lines['x'][column]
                for row in range(self.size):
                    y1, y2 = self.grid_lines['y'][row]

                    if self.grid[row][column] == '':
                        continue

                    buttons.append(Button(
                        click_area=pygame.Rect(x1, y1, x2 - x1, y2 - y1),
                        row=row,
                        column=column
                    ))
        return buttons

    def find_empty_spot(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.grid[row][column] == '':
                    return row, column

    def check_completion(self):
        for row in self.grid:
            if row == self.solution:
                self.game_completion()

    def move_number(self, row, column):
        empty_row, empty_column = self.find_empty_spot()
        number = self.grid[row][column]
        self.grid[row][column] = ''
        self.grid[empty_row][empty_column] = number
        for offset_row, offset_column in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            r = empty_row + offset_row
            c = empty_column + offset_column
            if r < 0 or c < 0 or r >= self.size or c >= self.size:
                continue
            if self.grid[r][c] == '':
                continue
            self.grid[r][c] += number

        self.check_completion()

    def handle_mouse_event(self, mouse_event):
        if self.done:
            return
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            mouse_position = self.location.mini_game_mouse_pos()
            for button in self.buttons:
                if button.was_clicked(mouse_position):
                    self.move_number(row=button.row, column=button.column)
                    return

            # if mouse_position is None:
            #     return
            # if not self.button.collidepoint(*mouse_position):
            #     return
            #
            # # Clicked the button
            # pygame.draw.rect(self.canvas, 'Red', self.button)
            # self.game_completion()
