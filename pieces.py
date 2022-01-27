import pygame

pygame.init()


class Piece:
    images = {
        'Pawn': [pygame.image.load(r'chess_pieces/pawnb.png'), pygame.image.load(r'chess_pieces/pawnw.png')],
        'Knight': [pygame.image.load(r'chess_pieces/knightb.png'), pygame.image.load(r'chess_pieces/knightw.png')],
        'Bishop': [pygame.image.load(r'chess_pieces/bishopb.png'), pygame.image.load(r'chess_pieces/bishopw.png')],
        'Rook': [pygame.image.load(r'chess_pieces/rookb.png'), pygame.image.load(r'chess_pieces/rookw.png')],
        'Queen': [pygame.image.load(r'chess_pieces/queenb.png'), pygame.image.load(r'chess_pieces/queenw.png')],
        'King': [pygame.image.load(r'chess_pieces/kingb.png'), pygame.image.load(r'chess_pieces/kingw.png')]
    }
    colors = {'Black': 0, 'White': 1}

    def __init__(self, board, color, square):
        self.board = board
        self.color = color
        self.square = square
        self.img = None

    def __repr__(self):
        return f'{self.__class__} {self.color}'

    def move(self, square):
        self.square.piece = None
        self.square = square
        square.piece = self


class Pawn(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = Piece.images['Pawn'][Piece.colors[color]]

    # def move(self):
    #     pass
    #
    # def possible_moves(self):
    #     pass


class Knight(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = Piece.images['Knight'][Piece.colors[color]]

        # def move(self):
        #     pass
        #
        # def possible_moves(self):
        #     pass


class Bishop(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = Piece.images['Bishop'][Piece.colors[color]]

        # def move(self):
        #     pass
        #
        # def possible_moves(self):
        #     pass


class Rook(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = Piece.images['Rook'][Piece.colors[color]]

        # def move(self):
        #     pass
        #
        # def possible_moves(self):
        #     pass


class Queen(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = Piece.images['Queen'][Piece.colors[color]]

        # def move(self):
        #     pass
        #
        # def possible_moves(self):
        #     pass


class King(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = Piece.images['King'][Piece.colors[color]]

        # def move(self):
        #     pass
        #
        # def possible_moves(self):
        #     pass

