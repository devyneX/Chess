import pygame
from pieces import Queen, Rook, Pawn, King, Bishop, Knight

pygame.init()


class Player:
    turn = 0

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.selected = None
        self.king = self.board.kings[self.color]
        self.opponent = None
        self.legal_moves = {}
        self.promoting_pawn = None

        self.set_legal_moves()
        self.get_legal_moves(None)

    def set_opponent(self, other):
        """
        sets the opponent of the player
        :param other: A Player Object
        """
        self.opponent = other

    def get_status(self, check):
        """
        Finds out whether the game should continue or end. If ended, finds the result.
        :param check: Check Object
        :return: A string containing current status of the game
        """
        flag = True
        insufficient = False
        self.get_legal_moves(check)

        if len(self.legal_moves) == 1:
            if len(self.opponent.legal_moves) == 1:
                insufficient = True
            elif len(self.opponent.legal_moves) == 2:
                insufficient = True
                for piece in self.opponent.legal_moves:
                    if isinstance(piece, Queen) or isinstance(piece, Rook) or isinstance(piece, Pawn):
                        insufficient = False
        elif len(self.legal_moves) == 2:
            insufficient = True
            remaining = None
            for piece in self.legal_moves:
                if isinstance(piece, Queen) or isinstance(piece, Rook) or isinstance(piece, Pawn):
                    insufficient = False
                elif not isinstance(piece, King):
                    remaining = piece
            if insufficient:
                if len(self.opponent.legal_moves) == 2:
                    if not isinstance(remaining, Bishop):
                        insufficient = False
                    else:
                        opponent_remaining = None
                        for piece in self.opponent.legal_moves:
                            if isinstance(piece, Queen) or isinstance(piece, Rook) or isinstance(piece, Pawn):
                                insufficient = False
                            elif not isinstance(piece, King):
                                opponent_remaining = piece
                        if isinstance(opponent_remaining, Bishop):
                            if remaining.square.color != opponent_remaining.square.color:
                                insufficient = False
                        else:
                            insufficient = False
                elif len(self.opponent.legal_moves) > 2:
                    insufficient = False

        for piece in self.legal_moves:
            if len(self.legal_moves[piece]) != 0:
                flag = False

        if check is not None:
            if flag:
                return 'Checkmate'
            elif insufficient:
                return 'Draw by insufficient material'
            else:
                return 'Continue'
        elif flag:
            return 'Stalemate'
        elif insufficient:
            return 'Draw by insufficient material'
        else:
            return 'Continue'

    def set_legal_moves(self):
        """
        Sets player pieces at object creation
        """
        limit = (1, 3) if self.color == 'White' else (7, 9)
        for i in range(limit[0], limit[1]):
            for j in range(1, 9):
                self.legal_moves[self.board.get_square(i, j).piece] = []

    def get_legal_moves(self, check):
        """
        Calculates the legal move for all pieces currently on the board
        :param check: A Check object
        """
        if check is not None and check.double_check():
            self.legal_moves[self.king] = self.king.possible_moves(check)
            return
        captured = []
        for piece in self.legal_moves:
            if piece.square is None:
                captured.append(piece)
                continue
            self.legal_moves[piece] = piece.possible_moves(check)

        for piece in captured:
            del self.legal_moves[piece]

    def clear_legal_moves(self):
        """
        Clears all the previous legal moves
        """
        for piece in self.legal_moves:
            self.legal_moves[piece] = []
            if isinstance(piece, Pawn):
                piece.en_passant = 0

    def highlight_legal_moves(self, piece):
        """
        Highlights the legal move of a selected piece
        :param piece: A Piece Object
        """
        for move in self.legal_moves[piece]:
            move.highlighted = not move.highlighted

    def select(self, piece):
        """
        Selected the piece clicked
        :param piece: A Piece Object
        """
        self.selected = piece
        if self.selected is not None and self.selected.color != self.color:
            self.selected = None
        if self.selected is not None:
            # print(self.selected)
            self.highlight_legal_moves(self.selected)
            piece.square.selected_highlighted = True

    def unselect(self):
        """
        Removes the current selected piece
        """
        self.selected.square.selected_highlighted = False
        self.highlight_legal_moves(self.selected)
        self.selected = None

    def end_turn(self):
        """
        Ends the turn for the current player
        :return: returns the current status of the game
        """
        Player.turn ^= 1
        check = self.opponent.king.in_check(self.opponent.king.square)
        if check is not None:
            self.opponent.king.square.check_highlighted = True
        status = self.opponent.get_status(check)
        return status

    def promotion(self, sq):
        """
        Handles pawn promotion
        :param sq: A Square Object
        :return: returns status of the game after promotion
        """
        if sq.column == self.promoting_pawn.square.column:
            if self.color == 'White':
                # promoted_piece = None
                if sq.row == 8:
                    promoted_piece = self.promoting_pawn.promote(Queen)
                elif sq.row == 7:
                    promoted_piece = self.promoting_pawn.promote(Rook)
                elif sq.row == 6:
                    promoted_piece = self.promoting_pawn.promote(Bishop)
                elif sq.row == 5:
                    promoted_piece = self.promoting_pawn.promote(Knight)
                else:
                    return 'Continue'

                if promoted_piece is not None:
                    del self.legal_moves[self.promoting_pawn]
                    self.legal_moves[promoted_piece] = []
                    self.promoting_pawn = None
                    self.board.promoting_pawn = None
                    return self.end_turn()

            else:
                # promoted_piece = None
                if sq.row == 1:
                    promoted_piece = self.promoting_pawn.promote(Queen)
                elif sq.row == 2:
                    promoted_piece = self.promoting_pawn.promote(Rook)
                elif sq.row == 3:
                    promoted_piece = self.promoting_pawn.promote(Bishop)
                elif sq.row == 4:
                    promoted_piece = self.promoting_pawn.promote(Knight)
                else:
                    return 'Continue'

                if promoted_piece is not None:
                    del self.legal_moves[self.promoting_pawn]
                    self.legal_moves[promoted_piece] = []
                    self.promoting_pawn = None
                    self.board.promoting_pawn = None
                    return self.end_turn()
        else:
            return 'Continue'

    def play(self, x, y):
        """
        Handling the players play
        :param x: x-coordinate of click
        :param y: y-coordinate of click
        :return: the current status of the game
        """
        sq = self.board.get_clicked_square(x, y)
        if sq is None:
            return 'Continue'

        if self.promoting_pawn is not None:
            return self.promotion(sq)

        elif self.selected is not None:
            if sq in self.legal_moves[self.selected]:
                if self.king.square.check_highlighted:
                    self.king.square.check_highlighted = False
                self.selected.square.selected_highlighted = False

                self.promoting_pawn = self.selected.move(sq)

                self.unselect()
                self.clear_legal_moves()

                if self.promoting_pawn is None:
                    return self.end_turn()
                else:
                    self.board.promoting_pawn = self.promoting_pawn
                    return 'Continue'

            elif sq.piece is not None:
                if sq.piece == self.selected:
                    self.unselect()
                elif sq.piece.color == self.color:
                    self.unselect()
                    self.select(sq.piece)
                else:
                    self.unselect()
            else:
                self.unselect()
        else:
            self.select(sq.piece)

        return 'Continue'
