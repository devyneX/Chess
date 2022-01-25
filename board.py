from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
import pygame

pygame.init()


class Board:
    def __init__(self):
        self.width = 480
        self.height = 480
        self.x = 10
        self.y = 0
        self.pieces = [[]]

    def draw_pieces(self, win, color, x, y, w_inc):
        if x == self.x or x == self.width - w_inc + self.x:
            # rooks
            rook = Rook(self, color, None, x, y)
            win.blit(rook.img, (rook.x, rook.y))
        elif x == self.x + w_inc or x == self.width - 2 * w_inc + self.x:
            # knights
            knight = Knight(self, color, None, x, y)
            win.blit(knight.img, (knight.x, knight.y))
        elif x == self.x + 2 * w_inc or x == self.width - 3 * w_inc + self.x:
            # bishops
            bishop = Bishop(self, color, None, x, y)
            win.blit(bishop.img, (bishop.x, bishop.y))
        elif x == self.x + 3 * w_inc:
            # queen
            queen = Queen(self, color, None, x, y)
            win.blit(queen.img, (queen.x, queen.y))
        elif x == self.width - 4 * w_inc + self.x:
            # king
            king = King(self, color, None, x, y)
            win.blit(king.img, (king.x, king.y))

    def draw(self, win):
        # white = (255, 255, 255)
        # size_pos = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(win, white, size_pos)
        w_inc = self.width // 8
        h_inc = self.height // 8
        white_square = (250, 215, 180)
        black_square = (105, 58, 12)
        i = 1
        for x in range(self.x, self.x + self.width, w_inc):
            i -= 1
            for y in range(self.y, self.y + self.height, h_inc):
                if i % 2 == 0:
                    color = black_square
                else:
                    color = white_square
                pygame.draw.rect(win, color, (x, y, w_inc, h_inc))
                i += 1
                if y == 0:
                    # black
                    self.draw_pieces(win, 'Black', x, y, w_inc)

                elif y == h_inc:
                    pawn = Pawn(self, 'Black', None, x, y)
                    win.blit(pawn.img, (pawn.x, pawn.y))
                elif y == self.height - 2 * h_inc:
                    pawn = Pawn(self, 'White', None, x, y)
                    win.blit(pawn.img, (pawn.x, pawn.y))
                elif y == self.height - h_inc:
                    # white
                    self.draw_pieces(win, 'White', x, y, w_inc)
