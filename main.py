import pygame
from core.field import GameField
from core.draw_utils import draw_cell
from config import CELLS_R, WIDTH, HEIGHT, BG_COLOR, FONT_FACE, FONT_SIZE, HELP_TEXT_COLOR, HELP_FONT_SIZE

pygame.init()
window_size = (WIDTH, HEIGHT)
pygame.display.set_caption("2048 hexagon")
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
running = True

field = GameField(CELLS_R, screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                field.global_move("ne")
            elif event.key == pygame.K_j:
                field.global_move("e")
            elif event.key == pygame.K_n:
                field.global_move("se")
            elif event.key == pygame.K_b:
                field.global_move("sw")
            elif event.key == pygame.K_g:
                field.global_move("w")
            elif event.key == pygame.K_y:
                field.global_move("nw")
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_z:
                field.undo_last_move()

    screen.fill(BG_COLOR)

    font = pygame.font.Font(FONT_FACE, HELP_FONT_SIZE)
    text = font.render("Keys:", True, HELP_TEXT_COLOR)
    screen.blit(text, (WIDTH - 150, 30))

    ac_keys = ["U: Up right", "J: Right", "N: Down right", "B: Down left", "G: Left", "Y: Up Left", "Q: Quit"]

    for i in range(0, len(ac_keys)):
        text = font.render(ac_keys[i], True, HELP_TEXT_COLOR)
        screen.blit(text, (WIDTH - 150, 60 + i * 20))

    if field.prev_state is not None:
        text = font.render("Z: Undo last move", True, HELP_TEXT_COLOR)
        screen.blit(text, (WIDTH - 150, HEIGHT - 200))

    for index in field.cells.keys():
        draw_cell(screen, index[0], index[1], field.cells[index]['value'])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
