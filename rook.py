import pygame

pygame.init()


class Rook:
    def __init__(self, board, color, square, x, y):
        self.board = board
        self.color = color
        self.img = None
        if self.color == 'Black':
            self.img = pygame.image.load('rookb.png')
        elif self.color == 'White':
            self.img = pygame.image.load('rookw.png')
        self.x = x
        self.y = y