from board import Board
import pygame

pygame.init()

bg_color = (0, 0, 0)
screen_width = 500
screen_height = 480
size = (screen_width, screen_height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
# pygame.display.set_icon('icon.png')
game_board = Board()


def redraw():
    pass


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    game_board.draw(screen)
    pygame.display.update()
pygame.quit()
