from board import Board
from player import Player
import pygame

pygame.init()

bg_color = (0, 0, 0)
screen_width = 500  # 660
screen_height = 480  # 640
size = (screen_width, screen_height)

# TODO: add clocks and background and probably sound effects (improvement)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
# pygame.display.set_icon('icon.png')
game_board = Board()
white_player = Player(game_board, 'White')
black_player = Player(game_board, 'Black')


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
            # print(Player.turn)
            if Player.turn == 0:
                white_player.play(x, y)
            else:
                black_player.play(x, y)

    redraw()

pygame.quit()
