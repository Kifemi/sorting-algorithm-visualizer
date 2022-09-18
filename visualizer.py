import pygame
import random
import math
from settings import Settings
from sorting_algorithms import bubble_sort, insertion_sort, quick_sort, \
    merge_sort, shell_sort, heap_sort


class Visualizer:
    def __init__(self):
        pygame.init()

        # Initialize basic settings
        self.run = True
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.width = self.settings.WINDOW_WIDTH
        self.height = self.settings.WINDOW_HEIGHT
        self.initialize_list()

        # Initialize sorting algorithm
        self.current_algorithm = bubble_sort
        self.current_algorithm_name = "Bubble Sort"
        self.current_algorithm_generator = None
        self.ascending = True
        self.sorting = False

        # Initialize pygame display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualization")

    def initialize_list(self):
        # Generate a random list and initialize the basic properties of the list
        self.lst = self.generate_random_list(self.settings.LIST_LENGTH,
                                             self.settings.MIN_VALUE,
                                             self.settings.MAX_VALUE)
        self.min_value = min(self.lst)
        self.max_value = max(self.lst)

        self.start_x = self.settings.SIDE_PADDING // 2
        self.bar_width = round((self.width - self.settings.SIDE_PADDING) / len(self.lst))
        if self.min_value < self.max_value:
            self.bar_height_unit = math.floor((self.height - self.settings.TOP_PADDING) /
                                              (self.max_value - self.min_value))
        else:
            # If all the values are same, use half of the available space
            self.bar_height_unit = math.floor((self.height - self.settings.TOP_PADDING) / 2)

    @staticmethod
    def generate_random_list(n: int, min_value: int, max_value: int) -> list:
        return [random.randint(min_value, max_value) for _ in range(n)]

    def draw(self, sorting_algorithm: object, ascending: bool) -> None:
        # Reset the screen by filling it with the background color
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        # Draw text
        controls1 = self.settings.FONT.render("Controls: ", 1, self.settings.BLUE)
        controls2 = self.settings.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | "
                                              "D - Descending | P - Pause",
                                              1, self.settings.BLACK)
        sorting1 = self.settings.FONT.render("Sorting algorithms: ", 1, self.settings.BLUE)
        sorting2 = self.settings.FONT.render("I - Insertion | B - Bubble | Q - Quick | M - Merge "
                                             "| S - Shell | H - Heap",
                                             1, self.settings.BLACK)
        info = self.settings.LARGE_FONT.render(f"{sorting_algorithm} - {'Ascending' if ascending else 'Descending'}",
                                               1, self.settings.BLUE)
        self.screen.blit(controls1, ((self.width - (controls2.get_width() + controls1.get_width())) / 2, 5))
        self.screen.blit(controls2, ((self.width - (controls2.get_width() - controls1.get_width())) / 2, 5))
        self.screen.blit(sorting1, ((self.width - (sorting2.get_width() + sorting1.get_width())) / 2, 45))
        self.screen.blit(sorting2, ((self.width - (sorting2.get_width() - sorting1.get_width())) / 2, 45))
        self.screen.blit(info, ((self.width - info.get_width()) / 2, 75))

        # Draw the bars
        self.draw_list()

    def draw_list(self, color_positions={}, clear_bg=False) -> None:
        if clear_bg:
            clear_area = (self.settings.SIDE_PADDING // 2, self.settings.TOP_PADDING,
                          self.width - self.settings.SIDE_PADDING,
                          self.height - self.settings.TOP_PADDING)
            pygame.draw.rect(self.screen, self.settings.BACKGROUND_COLOR, clear_area)

        for i, value in enumerate(self.lst):
            x = self.start_x + i * self.bar_width
            if self.min_value < self.max_value:
                y = self.height - (value - self.min_value) * self.bar_height_unit - 5
            else:
                # If all the values are same, use half of the available space
                y = self.height - self.bar_height_unit
            color = self.settings.BLUES[i % 3]

            if i in color_positions:
                color = color_positions[i]

            pygame.draw.rect(self.screen, color, (x, y, self.bar_width, self.height))

        if clear_bg:
            pygame.display.update()

    def get_next_iteration(self):
        if self.sorting:
            try:
                next(self.current_algorithm_generator)
            except StopIteration:
                self.sorting = False
        else:
            self.draw(self.current_algorithm_name, self.ascending)

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                # Reset
                self.initialize_list()
                self.sorting = False
            elif event.key == pygame.K_p:
                # Pause
                self.sorting = False
            elif event.key == pygame.K_SPACE and not self.sorting:
                # Start sorting
                self.sorting = True
                self.current_algorithm_generator = self.current_algorithm(self, self.ascending)
            elif event.key == pygame.K_a and not self.sorting:
                self.ascending = True
            elif event.key == pygame.K_d and not self.sorting:
                self.ascending = False
            elif event.key == pygame.K_b and not self.sorting:
                self.current_algorithm = bubble_sort
                self.current_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and not self.sorting:
                self.current_algorithm = insertion_sort
                self.current_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_q and not self.sorting:
                self.current_algorithm = quick_sort
                self.current_algorithm_name = "Quick Sort"
            elif event.key == pygame.K_m and not self.sorting:
                self.current_algorithm = merge_sort
                self.current_algorithm_name = "Merge Sort"
            elif event.key == pygame.K_s and not self.sorting:
                self.current_algorithm = shell_sort
                self.current_algorithm_name = "Shell Sort"
            elif event.key == pygame.K_h and not self.sorting:
                self.current_algorithm = heap_sort
                self.current_algorithm_name = "Heap Sort"

    def main_loop(self) -> None:
        while self.run:
            self.clock.tick(self.settings.CLOCK_TICK)
            self.get_next_iteration()
            self.check_pygame_events()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.main_loop()
