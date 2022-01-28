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

    def possible_moves(self):
        """
        This methods finds the legal moves for a piece
        :return:
        """
        pass

    def is_legal_move(self, moves, move):
        flag = True
        if move is None:
            return False
        if move.piece is None:
            moves.append(move)
        elif move.piece.color != self.color:
            moves.append(move)
            flag = False
        else:
            flag = False

        return flag


# TODO: implement en passant and promotion
class Pawn(Piece):
    # home_row = {'White': 2, 'Black': 7}

    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Pawn'][Piece.colors[color]]

    # def move(self):
    #     pass
    #
    def possible_moves(self):
        moves = []
        i, j = self.square.row, self.square.column
        front_square = left_diagonal = right_diagonal = extra_square = None

        if self.color == 'White':
            front_square = self.board.get_square(i + 1, j)
            left_diagonal = self.board.get_square(i + 1, j - 1)
            right_diagonal = self.board.get_square(i + 1, j + 1)
            if i == 2:
                extra_square = self.board.get_square(i + 2, j)
        elif self.color == 'Black':
            front_square = self.board.get_square(i - 1, j)
            left_diagonal = self.board.get_square(i - 1, j + 1)
            right_diagonal = self.board.get_square(i - 1, j - 1)
            if i == 7:
                extra_square = self.board.get_square(i - 2, j)

        if front_square is not None and front_square.piece is None:
            moves.append(front_square)
        if left_diagonal is not None and left_diagonal.piece is not None:
            if left_diagonal.piece.color != self.color:
                moves.append(left_diagonal)
        if right_diagonal is not None and right_diagonal.piece is not None:
            if right_diagonal.piece.color != self.color:
                moves.append(right_diagonal)
        if extra_square is not None and extra_square.piece is None:
            moves.append(extra_square)

        return moves


class Knight(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Knight'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def possible_moves(self):
        moves = []

        i, j = self.square.row, self.square.column

        squares = [(i - 2, j - 1), (i - 2, j + 1), (i + 2, j + 1), (i + 2, j - 1), (i + 1, j + 2), (i - 1, j + 2),
                   (i + 1, j - 2), (i - 1, j - 2)]

        for r, c in squares:
            move = self.board.get_square(r, c)
            self.is_legal_move(moves, move)

        return moves


class Bishop(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Bishop'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def possible_moves(self):
        moves = []

        # right-up diagonal
        i, j = self.square.row + 1, self.square.column + 1
        while i <= 8 and j <= 8:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            i += 1
            j += 1

        # left-down diagonal
        i, j = self.square.row - 1, self.square.column - 1
        while i >= 1 and j >= 1:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            i -= 1
            j -= 1

        # left-up diagonal
        i, j = self.square.row + 1, self.square.column - 1
        while i <= 8 and j >= 1:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            i += 1
            j -= 1

        # right-down diagonal
        i, j = self.square.row - 1, self.square.column + 1
        while i >= 1 and j <= 8:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            i -= 1
            j += 1

        return moves


class Rook(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Rook'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def possible_moves(self):
        moves = []

        # up
        i, j = self.square.row + 1, self.square.column
        while i <= 8:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            i += 1

        # down
        i, j = self.square.row - 1, self.square.column
        while i >= 0:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            i -= 1

        # left
        i, j = self.square.row, self.square.column - 1
        while i >= 1:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            j -= 1

        # right
        i, j = self.square.row, self.square.column + 1
        while i <= 8:
            move = self.board.get_square(i, j)

            if not self.is_legal_move(moves, move):
                break

            j += 1

        return moves


class Queen(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Queen'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def possible_moves(self):
        dummy_bishop = Bishop(self.board, self.color, self.square)
        dummy_rook = Rook(self.board, self.color, self.square)

        return dummy_bishop.possible_moves() + dummy_rook.possible_moves()


# TODO: add pin restrictions
class King(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['King'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def checked_by(self, square, piece):
        dummy = piece(self.board, self.color, square)
        moves = dummy.possible_moves()
        for move in moves:
            if isinstance(move.piece, piece) and move.piece.color != self.color:
                return True

        return False

    def opposition(self, square):
        i, j = square.row, square.column
        squares = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
                   (i, j - 1)]

        for r, c in squares:
            move = self.board.get_square(r, c)
            if move is None:
                continue
            if isinstance(move.piece, King) and move.piece.color != self.color:
                return True

        return False

    def in_check(self, square):
        flag = False
        if self.checked_by(square, Knight):
            return True

        if self.checked_by(square, Bishop):
            return True

        if self.checked_by(square, Rook):
            return True

        if self.checked_by(square, Queen):
            return True

        right = left = None

        if self.color == 'White':
            right = self.board.get_square(square.row + 1, square.column + 1)
            left = self.board.get_square(square.row + 1, square.column - 1)
        elif self.color == 'Black':
            right = self.board.get_square(square.row - 1, square.column + 1)
            left = self.board.get_square(square.row - 1, square.column - 1)

        if right is not None and isinstance(right.piece, Pawn):
            print(right.piece)
            if right.piece.color != self.color:
                flag = True
        if left is not None and isinstance(left.piece, Pawn):
            if left.piece.color != self.color:
                flag = True

        return flag

    def is_legal_move(self, moves, move):
        if move is None:
            return
        if move.piece is None or move.piece.color != self.color:
            if not self.in_check(move) and not self.opposition(move):
                moves.append(move)

    def possible_moves(self):
        moves = []

        i, j = self.square.row, self.square.column

        squares = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
                   (i, j - 1)]

        for r, c in squares:
            move = self.board.get_square(r, c)
            self.is_legal_move(moves, move)

        # print(moves)
        return moves
