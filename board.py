from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import pygame

pygame.init()


class Square:
    white = (250, 215, 180)
    black = (105, 58, 12)
    highlight = (120, 223, 245)
    home_piece = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self, board, row, column, color, x, y, length):
        self.board = board
        self.column = column
        self.row = row
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.piece = self.get_home_piece()
        self.highlighted = False

    def __repr__(self):
        return f'{self.get_name()}'  # -> {self.piece}'

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def get_name(self):
        return f"{chr(ord('a') + self.column - 1)}{self.row}"

    def get_home_piece(self):
        if self.row == 1:
            return self.home_piece[self.column - 1](self.board, 'White', self)
        elif self.row == 8:
            return self.home_piece[self.column - 1](self.board, 'Black', self)
        elif self.row == 2:
            return Pawn(self.board, 'White', self)
        elif self.row == 7:
            return Pawn(self.board, 'Black', self)

    # TODO: change highlighting
    # TODO: add highlighting for checks
    def draw(self, win):
        if self.highlighted:
            pygame.draw.rect(win, self.highlight, (self.x, self.y, self.length, self.length))
        else:
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
        self.square_length = self.length // 8
        self.squares = self.make_squares()
        self.kings = {'White': self.get_square(1, 5).piece,
                      'Black': self.get_square(8, 5).piece}
        # print(self.squares)

    def get_square(self, row, column):
        if row <= 0 or column <= 0 or row > 8 or column > 8:
            return None
        return self.squares[8 - row][column - 1]

    def make_squares(self):
        """
        This method creates the board representation matrix
        :return:  8*8 matrix of "Square" objects
        """
        squares = []
        x, y = self.x, self.y

        for j in range(8, 0, -1):
            color = Square.white if j % 2 == 0 else Square.black
            row = []
            for i in range(8):
                if i != 0:
                    color = Square.white if color == Square.black else Square.black
                square = Square(self, j, i + 1, color, x, y, self.square_length)
                row.append(square)
                x += self.square_length
            squares.append(row)
            x = self.x
            y += self.square_length

        return squares

    def draw(self, win):
        """
        This method draws the board on the window
        :param win: the window on which the board will be drawn
        """
        for row in self.squares:
            for square in row:
                square.draw(win)

    # FIXME: clicks outside board errors out
    def get_clicked_square(self, x, y):
        """
        This method will take the coordinates and return what square the coordinate is on
        :param x: x-coordinate
        :param y: y-coordinate
        :return: "Square" object
        """
        i = (x - self.x) // self.square_length
        j = (y - self.y) // self.square_length
        return self.squares[j][i]
