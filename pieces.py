from restrictions import Check
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
        return f'{self.color} {self.__class__} {self.square}'

    def pinned(self):
        """
        This function will determine whether a piece is pinned and find the path of the pin
        Path {}
        :return: The path on which the piece is restricted
        """
        pass

    def move(self, square):
        self.square.piece = None
        self.square = square
        square.piece = self

    def possible_moves(self, check):
        """
        This methods finds the legal moves for a piece
        :return:
        """
        pass

    def add_if_legal(self, moves, move, check):
        if move is None:
            return False
        if check is not None and check.is_restricted(move):
            return True

        flag = True
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
    def possible_moves(self, check):
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
            if check is None or not check.is_restricted(front_square):
                moves.append(front_square)
        if left_diagonal is not None and left_diagonal.piece is not None:
            if left_diagonal.piece.color != self.color:
                if check is None or not check.is_restricted(left_diagonal):
                    moves.append(left_diagonal)
        if right_diagonal is not None and right_diagonal.piece is not None:
            if right_diagonal.piece.color != self.color:
                if check is None or not check.is_restricted(right_diagonal):
                    moves.append(right_diagonal)
        if extra_square is not None and extra_square.piece is None:
            if check is None or not check.is_restricted(extra_square):
                moves.append(extra_square)

        return moves


class Knight(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Knight'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def possible_moves(self, check):
        moves = []

        i, j = self.square.row, self.square.column

        squares = [(i - 2, j - 1), (i - 2, j + 1), (i + 2, j + 1), (i + 2, j - 1), (i + 1, j + 2), (i - 1, j + 2),
                   (i + 1, j - 2), (i - 1, j - 2)]

        for r, c in squares:
            move = self.board.get_square(r, c)
            self.add_if_legal(moves, move, check)

        return moves


class Bishop(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Bishop'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    def possible_moves(self, check):
        moves = []

        # right-up diagonal
        i, j = self.square.row + 1, self.square.column + 1
        while i <= 8 and j <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
                break

            i += 1
            j += 1

        # left-down diagonal
        i, j = self.square.row - 1, self.square.column - 1
        while i >= 1 and j >= 1:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
                break

            i -= 1
            j -= 1

        # left-up diagonal
        i, j = self.square.row + 1, self.square.column - 1
        while i <= 8 and j >= 1:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
                break

            i += 1
            j -= 1

        # right-down diagonal
        i, j = self.square.row - 1, self.square.column + 1
        while i >= 1 and j <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
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

    def possible_moves(self, check):
        moves = []

        # up
        i, j = self.square.row + 1, self.square.column
        while i <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
                break

            i += 1

        # down
        i, j = self.square.row - 1, self.square.column
        while i >= 0:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
                break

            i -= 1

        # left
        i, j = self.square.row, self.square.column - 1
        while i >= 1:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
                break

            j -= 1

        # right
        i, j = self.square.row, self.square.column + 1
        while i <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check):
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

    def possible_moves(self, check):
        dummy_bishop = Bishop(self.board, self.color, self.square)
        dummy_rook = Rook(self.board, self.color, self.square)

        return dummy_bishop.possible_moves(check) + dummy_rook.possible_moves(check)


class Dummy(Knight, Bishop, Rook, Queen):
    def __init__(self, board, color, square, piece, king):
        super().__init__(board, color, square)
        self.type = piece
        self.king = king

    def add_if_legal(self, moves, move, check):
        # print('called dummy')
        if move is None:
            return False

        if move.piece is None:
            return True
        elif move.piece.color != self.color:
            moves.append(move)
            return False
        elif move.piece == self.king:
            # print('here')
            return True
        else:
            return False

    def possible_moves(self, check):
        if self.type == Queen:
            dummy_bishop = Dummy(self.board, self.color, self.square, Bishop, self.king)
            dummy_rook = Dummy(self.board, self.color, self.square, Rook, self.king)
            return dummy_bishop.possible_moves(check) + dummy_rook.possible_moves(check)
        return self.type.possible_moves(self, check)


# TODO: add pin restrictions
# TODO: add castling
class King(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['King'][Piece.colors[color]]

        # def move(self):
        #     pass
        #

    # def checked_by_knight(self, square):
    #     dummy = Knight(self.board, self.color, square)
    #     moves = dummy.possible_moves(None)
    #     for move in moves:
    #         if isinstance(move.piece, Knight) and move.piece.color != self.color:
    #             return move.piece
    #
    #     return None
    #
    # def checked_by_bishop(self, square):
    #     pass

    def checked_by(self, square, piece):
        # dummy = piece(self.board, self.color, square)
        dummy = Dummy(self.board, self.color, square, piece, self)
        moves = dummy.possible_moves(None)
        for move in moves:
            if isinstance(move.piece, piece) and move.piece.color != self.color:
                # print('found', move.piece)
                return move.piece

        return None

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
        print(square)
        checking_pieces = []
        for piece in [Knight, Bishop, Rook, Queen]:
            checking_piece = self.checked_by(square, piece)
            if checking_piece is not None:
                checking_pieces.append(checking_piece)

        # if self.checked_by(square, Knight):
        #     return True
        #
        # if self.checked_by(square, Bishop):
        #     return True
        #
        # if self.checked_by(square, Rook):
        #     return True
        #
        # if self.checked_by(square, Queen):
        #     return True

        right = left = None

        if self.color == 'White':
            right = self.board.get_square(square.row + 1, square.column + 1)
            left = self.board.get_square(square.row + 1, square.column - 1)
        elif self.color == 'Black':
            right = self.board.get_square(square.row - 1, square.column + 1)
            left = self.board.get_square(square.row - 1, square.column - 1)

        if right is not None and isinstance(right.piece, Pawn):
            if right.piece.color != self.color:
                checking_pieces.append(right.piece)
        if left is not None and isinstance(left.piece, Pawn):
            if left.piece.color != self.color:
                checking_pieces.append(left.piece)

        print(checking_pieces)

        return None if len(checking_pieces) == 0 else Check(self, checking_pieces)

    def add_if_legal(self, moves, move, check):
        if move is None:
            return
        if move.piece is None or move.piece.color != self.color:
            if self.in_check(move) is None and not self.opposition(move):
                moves.append(move)

    def possible_moves(self, check):
        moves = []

        i, j = self.square.row, self.square.column

        squares = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
                   (i, j - 1)]

        for r, c in squares:
            move = self.board.get_square(r, c)
            self.add_if_legal(moves, move, check)

        return moves
