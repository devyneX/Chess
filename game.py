from board import Board
import pygame

pygame.init()

bg_color = (0, 0, 0)
screen_width = 500  # 660
screen_height = 480  # 640
size = (screen_width, screen_height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
# pygame.display.set_icon('icon.png')
game_board = Board()


def redraw():
    game_board.draw(screen)
    pygame.display.update()


run = True
selected = None
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            sq = game_board.get_square(x, y)
            print(sq)
            if selected is not None:
                selected.move(sq)
                selected = None
            else:
                selected = sq.piece

    redraw()

pygame.quit()
