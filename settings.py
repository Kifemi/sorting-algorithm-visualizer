import pygame


class Settings:
    def __init__(self):
        # COLOR SETTINGS
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (160, 15, 160)
        self.BACKGROUND_COLOR = (150, 200, 255)
        self.BLUES = [
            (0, 130, 255),
            (0, 90, 255),
            (0, 50, 255)
        ]

        # WINDOW SETTINGS
        self.WINDOW_HEIGHT = 800
        self.WINDOW_WIDTH = 900
        self.SIDE_PADDING = 100
        self.TOP_PADDING = 150

        # FONT SETTINGS
        self.FONT = pygame.font.SysFont('arial', 20)
        self.LARGE_FONT = pygame.font.SysFont('arial', 30)

        # LIST SETTINGS
        self.LIST_LENGTH = 100
        self.MIN_VALUE = 0
        self.MAX_VALUE = 100

        # CLOCK SETTINGS
        self.CLOCK_TICK = 60
