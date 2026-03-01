import pygame
from math import sin, cos, pi
from config import BG_COLOR, CX, CY, HEXAGON_R, BORDER_COLOR, TEXT_COLOR, BORDER_WIDTH, FONT_FACE, FONT_SIZE, NUM_COLORS


def draw_hexagon(surface, x, y, color = BG_COLOR):
    pygame.draw.polygon(surface, color, [(x + HEXAGON_R * sin(2 * pi * i / 6), y + HEXAGON_R * cos(2 * pi * i / 6)) for i in range(6)],0)  # Вначале закрашиваем
    pygame.draw.polygon(surface, BORDER_COLOR, [(x + HEXAGON_R * sin(2 * pi * i / 6), y + HEXAGON_R * cos(2 * pi * i / 6)) for i in range(6)], BORDER_WIDTH) # Потом рисуем границу

def draw_text(surface, x, y, text):
    if str(text) != '0':
        font = pygame.font.Font(FONT_FACE, FONT_SIZE)
        text = font.render(str(text), True, TEXT_COLOR)
        rect = text.get_rect(center=(x, y))
        surface.blit(text, rect)

def draw_cell(surface, x, y, text=0):
    # x, y передаём в координатах поля и уже здесь преобразуем в экранные, z передавать не надо
    draw_x = CX + (y - cos(pi / 3) * x) * HEXAGON_R * 2
    draw_y = CY - (x * sin(pi / 3)) * HEXAGON_R * 2

    color = BG_COLOR
    text = int(text)
    if text > 65536:
        text = 65536
    if text in NUM_COLORS.keys():
        color = NUM_COLORS[text]

    draw_hexagon(surface, draw_x, draw_y, color)
    draw_text(surface, draw_x, draw_y, text)
