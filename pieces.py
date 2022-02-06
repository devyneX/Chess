import pygame

pygame.init()


class Check:
    def __init__(self, king, pieces):
        self.king = king
        self.pieces = pieces

    def double_check(self):
        return len(self.pieces) == 2

    @classmethod
    def in_path(cls, king_square, piece_square, move):
        if move == king_square:
            return False
        if king_square.row == piece_square.row:
            # horizontal
            if move.row == king_square.row:
                return max(king_square.column, piece_square.column) >= move.column >= min(king_square.column,
                                                                                          piece_square.column)
        elif king_square.column == piece_square.column:
            # vertical
            if move.column == king_square.column:
                return max(king_square.row, piece_square.row) >= move.row >= min(king_square.row, piece_square.row)
        else:
            # diagonal
            m = (king_square.row - piece_square.row) // (king_square.column - piece_square.column)
            c = - m * king_square.column + king_square.row
            if move.row == m * move.column + c:
                h_row, l_row = max(king_square.row, piece_square.row), min(king_square.row, piece_square.row)
                h_col, l_col = max(king_square.column, piece_square.column), min(king_square.column,
                                                                                 piece_square.column)
                return h_row >= move.row >= l_row and h_col >= move.column >= l_col
            else:
                return False

    def restricted(self, move):
        if isinstance(self.pieces[0], Knight):
            if move == self.pieces[0].square:
                return False
            else:
                return True
        if move == self.pieces[0].square:
            return False
        return not self.in_path(self.king.square, self.pieces[0].square, move)


class Piece:
    images = {
        'Pawn': [pygame.image.load(r'chess_pieces/black_pawn.png'), pygame.image.load(r'chess_pieces/white_pawn.png')],
        'Knight': [pygame.image.load(r'chess_pieces/black_knight.png'), pygame.image.load(
            r'chess_pieces/white_knight.png')],
        'Bishop': [pygame.image.load(r'chess_pieces/black_bishop.png'), pygame.image.load(
            r'chess_pieces/white_bishop.png')],
        'Rook': [pygame.image.load(r'chess_pieces/black_rook.png'), pygame.image.load(r'chess_pieces/white_rook.png')],
        'Queen': [pygame.image.load(r'chess_pieces/black_queen.png'), pygame.image.load(
            r'chess_pieces/white_queen.png')],
        'King': [pygame.image.load(r'chess_pieces/black_king.png'), pygame.image.load(r'chess_pieces/white_king.png')]
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
        if square.piece is not None:
            square.piece.square = None
        square.piece = self

    def pinned(self):
        """
        This method will determine whether a piece is pinned and find the path of the pin
        Path {}
        :return: The path on which the piece is restricted
        """

        def check_pin(generator, square_func, piece):
            for x in generator:
                sq = square_func(x)
                if sq is None:
                    return None
                elif isinstance(sq.piece, piece) or isinstance(sq.piece, Queen):
                    if sq.piece.color != self.color:
                        return Check(king, [sq.piece])
                    else:
                        return None
                elif sq.piece is not None:
                    return None

        king = self.board.kings[self.color]
        if king.square.row == self.square.row:
            # horizontal
            if king.square.column > self.square.column:
                for i in range(self.square.column + 1, king.square.column):
                    square = self.board.get_square(self.square.row, i)
                    if square.piece is not None:
                        return None

                return check_pin(range(self.square.column - 1, 0, -1),
                                 lambda x: self.board.get_square(self.square.row, x), Rook)

            else:
                for i in range(king.square.column + 1, self.square.column):
                    square = self.board.get_square(self.square.row, i)
                    if square.piece is not None:
                        return None

                return check_pin(range(self.square.column + 1, 9),
                                 lambda x: self.board.get_square(self.square.row, x), Rook)

        elif king.square.column == self.square.column:
            # vertical
            if king.square.row > self.square.row:
                for i in range(self.square.row + 1, king.square.row):
                    square = self.board.get_square(i, self.square.column)
                    if square.piece is not None:
                        return None

                return check_pin(range(self.square.row - 1, 0, -1),
                                 lambda x: self.board.get_square(x, self.square.column), Rook)

            else:
                for i in range(king.square.row + 1, self.square.row):
                    square = self.board.get_square(i, self.square.column)
                    if square.piece is not None:
                        return None

                return check_pin(range(self.square.row + 1, 9),
                                 lambda x: self.board.get_square(x, self.square.column), Rook)

        else:
            m = (king.square.row - self.square.row) // (king.square.column - self.square.column)
            c = - m * king.square.column + king.square.row
            if m == 1 or m == -1:
                # diagonal
                if king.square.column > self.square.column:
                    for i in range(self.square.column + 1, king.square.column):
                        square = self.board.get_square(m * i + c, i)
                        if square is not None and square.piece is not None:
                            return None

                    return check_pin(range(self.square.column - 1, 0, -1),
                                     lambda x: self.board.get_square(m * x + c, x), Bishop)

                else:
                    for i in range(king.square.column + 1, self.square.column):
                        square = self.board.get_square(m * i + c, i)
                        if square is not None and square.piece is not None:
                            return None

                    return check_pin(range(self.square.column + 1, 9),
                                     lambda x: self.board.get_square(m * x + c, x), Bishop)

            else:
                return None

    def possible_moves(self, check):
        """
        This methods finds the legal moves for a piece
        :param check:
        :return: a list of legal moves
        """
        return []

    def add_if_legal(self, moves, move, check, pin):
        if move is None:
            return False

        flag = True
        append = False
        if move.piece is None:
            append = True
        elif move.piece.color != self.color:
            append = True
            flag = False
        else:
            flag = False

        if append:
            if check is not None and check.restricted(move):
                append = False
            if pin is not None and pin.restricted(move):
                append = False

        if append:
            moves.append(move)

        return flag


class Pawn(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.en_passant = 0
        self.img = self.images['Pawn'][Piece.colors[color]]

    def en_passant_available(self, left, right):
        if left is not None:
            if isinstance(left.piece, Pawn) and left.piece.color != self.color:
                left.piece.en_passant = -1
        if right is not None:
            if isinstance(right.piece, Pawn) and right.piece.color != self.color:
                right.piece.en_passant = 1

    def play_en_passant(self, square, side):
        print(side)
        super().move(square)
        side.piece.square = None
        side.piece = None

    def is_en_passant(self, square, col_inc, row_inc):
        sq = self.board.get_square(self.square.row + row_inc, self.square.column + col_inc)
        if square is sq:
            side = self.board.get_square(self.square.row, self.square.column + col_inc)
            if side is not None and side.piece is not None:
                self.play_en_passant(square, side)
                return True
            else:
                return False
        return False

    def promote(self, piece):
        promoted = piece(self.board, self.color, self.square)
        self.square.piece = promoted
        self.square = None
        return promoted

    def move(self, square):
        if self.color == 'White':
            if square.row == 4:
                if self.square.row == 2:
                    left = self.board.get_square(square.row, self.square.column - 1)
                    right = self.board.get_square(square.row, self.square.column + 1)
                    self.en_passant_available(left, right)
            elif self.en_passant:
                if self.is_en_passant(square, self.en_passant, 1):
                    return None

        elif self.color == 'Black':
            if square.row == 5:
                if self.square.row == 7:
                    left = self.board.get_square(square.row, self.square.column + 1)
                    right = self.board.get_square(square.row, self.square.column - 1)
                    self.en_passant_available(left, right)
            elif self.en_passant:
                if self.is_en_passant(square, -self.en_passant, -1):
                    return None

        super().move(square)
        if self.color == 'White' and square.row == 8:
            return self
        elif self.color == 'Black' and square.row == 1:
            return self

    def possible_moves(self, check):
        pin = self.pinned()

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
            if check is None or not check.restricted(front_square):
                if pin is None or not pin.restricted(front_square):
                    moves.append(front_square)
                    if extra_square is not None and extra_square.piece is None:
                        if check is None or not check.restricted(extra_square):
                            if pin is None or not pin.restricted(extra_square):
                                moves.append(extra_square)
        if left_diagonal is not None:
            if left_diagonal.piece is not None:
                if left_diagonal.piece.color != self.color:
                    if check is None or not check.restricted(left_diagonal):
                        if pin is None or not pin.restricted(left_diagonal):
                            moves.append(left_diagonal)
            elif self.en_passant == -1:
                if check is None or not check.restricted(left_diagonal):
                    if pin is None or not pin.restricted(left_diagonal):
                        moves.append(left_diagonal)
        if right_diagonal is not None:
            if right_diagonal.piece is not None:
                if right_diagonal.piece.color != self.color:
                    if check is None or not check.restricted(right_diagonal):
                        if pin is None or not pin.restricted(right_diagonal):
                            moves.append(right_diagonal)
            elif self.en_passant == 1:
                if check is None or not check.restricted(right_diagonal):
                    if pin is None or not pin.restricted(right_diagonal):
                        moves.append(right_diagonal)

        return moves


class Knight(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Knight'][Piece.colors[color]]

    def possible_moves(self, check):
        pin = self.pinned()

        moves = []

        i, j = self.square.row, self.square.column

        squares = [(i - 2, j - 1), (i - 2, j + 1), (i + 2, j + 1), (i + 2, j - 1), (i + 1, j + 2), (i - 1, j + 2),
                   (i + 1, j - 2), (i - 1, j - 2)]

        for r, c in squares:
            move = self.board.get_square(r, c)
            self.add_if_legal(moves, move, check, pin)

        return moves


class Bishop(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Bishop'][Piece.colors[color]]

    def possible_moves(self, check):
        pin = self.pinned()

        moves = []

        # right-up diagonal
        i, j = self.square.row + 1, self.square.column + 1
        while i <= 8 and j <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            i += 1
            j += 1

        # left-down diagonal
        i, j = self.square.row - 1, self.square.column - 1
        while i >= 1 and j >= 1:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            i -= 1
            j -= 1

        # left-up diagonal
        i, j = self.square.row + 1, self.square.column - 1
        while i <= 8 and j >= 1:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            i += 1
            j -= 1

        # right-down diagonal
        i, j = self.square.row - 1, self.square.column + 1
        while i >= 1 and j <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            i -= 1
            j += 1

        return moves


class Rook(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Rook'][Piece.colors[color]]
        self.moved = False

    def move(self, square):
        super().move(square)
        if not self.moved:
            self.moved = True

    def possible_moves(self, check):
        pin = self.pinned()

        moves = []

        # up
        i, j = self.square.row + 1, self.square.column
        while i <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            i += 1

        # down
        i, j = self.square.row - 1, self.square.column
        while i >= 0:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            i -= 1

        # left
        i, j = self.square.row, self.square.column - 1
        while i >= 1:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            j -= 1

        # right
        i, j = self.square.row, self.square.column + 1
        while i <= 8:
            move = self.board.get_square(i, j)

            if not self.add_if_legal(moves, move, check, pin):
                break

            j += 1

        return moves


class Queen(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['Queen'][Piece.colors[color]]

    def possible_moves(self, check):
        dummy_bishop = Bishop(self.board, self.color, self.square)
        dummy_rook = Rook(self.board, self.color, self.square)

        return dummy_bishop.possible_moves(check) + dummy_rook.possible_moves(check)


class Dummy(Knight, Bishop, Rook, Queen):
    def __init__(self, board, color, square, piece, king):
        super().__init__(board, color, square)
        self.type = piece
        self.king = king

    def add_if_legal(self, moves, move, check, pin):
        if move is None:
            return False

        if move.piece is None:
            return True
        elif move.piece.color != self.color:
            moves.append(move)
            return False
        elif move.piece == self.king:
            return True
        else:
            return False

    def possible_moves(self, check):
        if self.type == Queen:
            dummy_bishop = Dummy(self.board, self.color, self.square, Bishop, self.king)
            dummy_rook = Dummy(self.board, self.color, self.square, Rook, self.king)
            return dummy_bishop.possible_moves(check) + dummy_rook.possible_moves(check)
        return self.type.possible_moves(self, check)


class King(Piece):
    def __init__(self, board, color, square):
        super().__init__(board, color, square)
        self.img = self.images['King'][Piece.colors[color]]
        self.moved = False

    def move(self, square):
        if self.color == 'White':
            if self.square.row == 1 and self.square.column == 5:
                if square.row == 1:
                    if square.column == 7:
                        rook = self.board.get_square(1, 8).piece
                        rook.move(self.board.get_square(1, 6))
                    elif square.column == 3:
                        rook = self.board.get_square(1, 1).piece
                        rook.move(self.board.get_square(1, 4))
        elif self.color == 'Black':
            if self.square.row == 8 and self.square.column == 5:
                if square.row == 8:
                    if square.column == 7:
                        rook = self.board.get_square(8, 8).piece
                        rook.move(self.board.get_square(8, 6))
                    elif square.column == 3:
                        rook = self.board.get_square(8, 1).piece
                        rook.move(self.board.get_square(8, 4))

        super().move(square)
        if not self.moved:
            self.moved = True

    def checked_by(self, square, piece):
        dummy = Dummy(self.board, self.color, square, piece, self)
        moves = dummy.possible_moves(None)
        for move in moves:
            if isinstance(move.piece, piece) and move.piece.color != self.color:
                return move.piece

        return None

    @staticmethod
    def adjacent_squares(i, j):
        return [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
                (i, j - 1)]

    def opposition(self, square):
        squares = self.adjacent_squares(square.row, square.column)

        for r, c in squares:
            move = self.board.get_square(r, c)
            if move is None:
                continue
            if isinstance(move.piece, King) and move.piece.color != self.color:
                return True

        return False

    def in_check(self, square):
        checking_pieces = []
        for piece in [Knight, Bishop, Rook, Queen]:
            checking_piece = self.checked_by(square, piece)
            if checking_piece is not None:
                checking_pieces.append(checking_piece)

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

        return None if len(checking_pieces) == 0 else Check(self, checking_pieces)

    def add_if_legal(self, moves, move, check, pin):
        if move is None:
            return
        if move.piece is None or move.piece.color != self.color:
            if self.in_check(move) is None and not self.opposition(move):
                moves.append(move)

    def castle_available(self, moves):
        if self.moved:
            return

        if self.color == 'White':
            short_rook = self.board.get_square(1, 8).piece
            middle_square1 = self.board.get_square(1, 6)
            middle_square2 = self.board.get_square(1, 7)
            if isinstance(short_rook, Rook) and not short_rook.moved:
                if middle_square1.piece is None and middle_square2.piece is None:
                    if self.in_check(middle_square1) is None and self.in_check(middle_square2) is None:
                        moves.append(self.board.get_square(1, 7))

            long_rook = self.board.get_square(1, 1).piece
            middle_square1 = self.board.get_square(1, 2)
            middle_square2 = self.board.get_square(1, 3)
            middle_square3 = self.board.get_square(1, 4)
            if isinstance(long_rook, Rook) and not long_rook.moved:
                if middle_square1.piece is None and middle_square2.piece is None:
                    if middle_square3.piece is None:
                        if self.in_check(middle_square2) is None and self.in_check(middle_square3) is None:
                            moves.append(self.board.get_square(1, 3))

        elif self.color == 'Black':
            short_rook = self.board.get_square(8, 8).piece
            middle_square1 = self.board.get_square(8, 6)
            middle_square2 = self.board.get_square(8, 7)
            if isinstance(short_rook, Rook) and not short_rook.moved:
                if middle_square1.piece is None and middle_square2.piece is None:
                    if self.in_check(middle_square1) is None and self.in_check(middle_square2) is None:
                        moves.append(self.board.get_square(8, 7))

            long_rook = self.board.get_square(8, 1).piece
            middle_square1 = self.board.get_square(8, 2)
            middle_square2 = self.board.get_square(8, 3)
            middle_square3 = self.board.get_square(8, 4)
            if isinstance(long_rook, Rook) and not long_rook.moved:
                if middle_square1.piece is None and middle_square2.piece is None:
                    if middle_square3.piece is None:
                        if self.in_check(middle_square2) is None and self.in_check(middle_square3) is None:
                            moves.append(self.board.get_square(8, 3))

    def possible_moves(self, check):
        moves = []

        squares = self.adjacent_squares(self.square.row, self.square.column)

        for r, c in squares:
            move = self.board.get_square(r, c)
            self.add_if_legal(moves, move, check, None)

        self.castle_available(moves)

        return moves
