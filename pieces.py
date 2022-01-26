import pygame

pygame.init()


class Piece:
    images = {
        'Pawn': [pygame.image.load('pawnb.png'), pygame.image.load('pawnw.png')],
        'Knight': [pygame.image.load('knightb.png'), pygame.image.load('knightw.png')],
        'Bishop': [pygame.image.load('bishopb.png'), pygame.image.load('bishopw.png')],
        'Rook': [pygame.image.load('rookb.png'), pygame.image.load('rookw.png')],
        'Queen': [pygame.image.load('queenb.png'), pygame.image.load('queenw.png')],
        'King': [pygame.image.load('kingb.png'), pygame.image.load('kingw.png')]
    }
    colors = {'Black': 0, 'White': 1}

    def __init__(self, board, color, square, x, y):
        self.board = board
        self.color = color
        self.img = None
        self.square = square
        self.x = x
        self.y = y


class Pawn(Piece):
    def __init__(self, board, color, square, x, y):
        super().__init__(board, color, square, x, y)
        self.img = Piece.images['Pawn'][Piece.colors[color]]

    def move(self):
        pass

    def possible_moves(self):
        pass


class Knight(Piece):
    def __init__(self, board, color, square, x, y):
        super().__init__(board, color, square, x, y)
        self.img = Piece.images['Knight'][Piece.colors[color]]

        def move(self):
            pass

        def possible_moves(self):
            pass


class Bishop(Piece):
    def __init__(self, board, color, square, x, y):
        super().__init__(board, color, square, x, y)
        self.img = Piece.images['Bishop'][Piece.colors[color]]

        def move(self):
            pass

        def possible_moves(self):
            pass


class Rook(Piece):
    def __init__(self, board, color, square, x, y):
        super().__init__(board, color, square, x, y)
        self.img = Piece.images['Rook'][Piece.colors[color]]

        def move(self):
            pass

        def possible_moves(self):
            pass


class Queen(Piece):
    def __init__(self, board, color, square, x, y):
        super().__init__(board, color, square, x, y)
        self.img = Piece.images['Queen'][Piece.colors[color]]

        def move(self):
            pass

        def possible_moves(self):
            pass


class King(Piece):
    def __init__(self, board, color, square, x, y):
        super().__init__(board, color, square, x, y)
        self.img = Piece.images['King'][Piece.colors[color]]

        def move(self):
            pass

        def possible_moves(self):
            pass

