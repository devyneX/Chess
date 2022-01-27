from board import Board
from player import Player
import pygame

pygame.init()

bg_color = (0, 0, 0)
screen_width = 500  # 660
screen_height = 480  # 640
size = (screen_width, screen_height)

# TODO: add clocks and background (improvement)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
# pygame.display.set_icon('icon.png')
game_board = Board()
player1 = Player(game_board, None)
# TODO: implement turns


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
            player1.play(x, y)

    redraw()

pygame.quit()
