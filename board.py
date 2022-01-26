from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import pygame

pygame.init()


class Square:
    white = (250, 215, 180)
    black = (105, 58, 12)
    home_piece = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self, board, name, color, x, y, length):
        self.board = board
        self.name = name
        self.color = color
        self.piece = None
        self.x = x
        self.y = y
        self.length = length
        self.piece = self.set_home_piece()
        self.highlighted = False

    def set_home_piece(self):
        if self.name[1] == '1':
            return Square.home_piece[ord(self.name[0]) - ord('a')](self.board, 'White', self)
        elif self.name[1] == '8':
            return Square.home_piece[ord(self.name[0]) - ord('a')](self.board, 'Black', self)
        elif self.name[1] == '2':
            return Pawn(self.board, 'White', self)
        elif self.name[1] == '7':
            return Pawn(self.board, 'Black', self)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.length, self.length))
        self.draw_piece(win)

    def draw_piece(self, win):
        if self.piece is None:
            return
        win.blit(self.piece.img, (self.x, self.y))


class Board:
    def __init__(self):
        self.length = 480
        self.x = 10
        self.y = 0
        self.squares = self.make_squares()

    def make_squares(self):
        squares = []
        length = self.length // 8
        x, y = self.x, self.y

        for i in range(8):
            color = Square.white if i % 2 == 0 else Square.black
            column = []
            for j in range(8, 0, -1):
                if j != 8:
                    color = Square.white if color == Square.black else Square.black
                name = f"{chr(ord('a') + i)}{j}"
                square = Square(self, name, color, x, y, length)
                column.append(square)
                y += length
            squares.append(column)
            y = self.y
            x += length

        return squares

    def draw(self, win):
        for row in self.squares:
            for square in row:
                square.draw(win)
