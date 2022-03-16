import pygame

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (175, 55, 0)

FPS = 120

WIDTH, HEIGHT = 560, 600

ROWS = COLS = 28

TOOLBAR_HEIGHT = HEIGHT - WIDTH


def get_font(size):
    return pygame.font.SysFont("Times New Roman", size)
