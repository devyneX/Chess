from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
import pygame

pygame.init()


class Square:
    white = (250, 215, 180)
    black = (105, 58, 12)
    highlight = (120, 223, 245)
    check_highlight = (255, 0, 0)
    home_piece = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    # home_piece = [None, Knight, Bishop, None, King, None, None, None]

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
        self.selected_highlighted = False
        self.check_highlighted = False

    def __repr__(self):
        return f'{self.get_name()} -> {self.piece}'

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

    def draw(self, win):
        if self.highlighted:
            if self.piece is not None:
                pygame.draw.rect(win, self.highlight, (self.x, self.y, self.length, self.length))
            else:
                pygame.draw.circle(win, self.highlight, (self.x + self.length // 2, self.y + self.length // 2),
                                   self.length // 6)
        elif self.check_highlighted:
            pygame.draw.rect(win, self.check_highlight, (self.x, self.y, self.length, self.length))
        elif self.selected_highlighted:
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
        self.x = 0
        self.y = 0
        self.square_length = self.length // 8
        self.squares = self.make_squares()
        self.kings = {'White': self.get_square(1, 5).piece,
                      'Black': self.get_square(8, 5).piece}
        self.promoting_pawn = None

    def get_square(self, row, column):
        """
        This method finds the square given a row and a column
        :param row: Row of the square
        :param column: Column of the square
        :return: A Square Object
        """
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

    def draw_promotion_screen(self, win):
        """
        This method draws the promotion options on the window
        :param win: window on which the promotion pieces will be drawn
        """
        length = self.square_length
        x = self.promoting_pawn.square.x
        y = self.promoting_pawn.square.y
        if self.promoting_pawn.color == 'White':
            pygame.draw.rect(win, (73, 81, 111), (x, y, length, 4 * length))
            win.blit(Piece.images['Queen'][1], (x, y))
            win.blit(Piece.images['Rook'][1], (x, y + length))
            win.blit(Piece.images['Bishop'][1], (x, y + 2 * length))
            win.blit(Piece.images['Knight'][1], (x, y + 3 * length))

        else:
            pygame.draw.rect(win, (98, 121, 184), (x, y - 3 * length, length, 4 * length))
            win.blit(Piece.images['Queen'][0], (x, y))
            win.blit(Piece.images['Rook'][0], (x, y - length))
            win.blit(Piece.images['Bishop'][0], (x, y - 2 * length))
            win.blit(Piece.images['Knight'][0], (x, y - 3 * length))

    def draw(self, win):
        """
        This method draws the board on the window
        :param win: the window on which the board will be drawn
        """
        for row in self.squares:
            for square in row:
                square.draw(win)

        if self.promoting_pawn is not None:
            self.draw_promotion_screen(win)

    def get_clicked_square(self, x, y):
        """
        This method will take the coordinates and return what square the coordinate is on
        :param x: x-coordinate
        :param y: y-coordinate
        :return: "Square" object
        """
        if x < self.x or y < self.y or x >= self.x + self.length or y >= self.y + self.length:
            return None
        i = (x - self.x) // self.square_length
        j = (y - self.y) // self.square_length
        return self.squares[j][i]
