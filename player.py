import pygame

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

        self.set_legal_moves()
        self.get_legal_moves(None)

    def set_opponent(self, other):
        self.opponent = other

    def checkmate(self, check):
        self.get_legal_moves(check)
        for piece in self.legal_moves:
            if len(self.legal_moves[piece]) != 0:
                return False
        return True

    def set_legal_moves(self):
        limit = (1, 3) if self.color == 'White' else (7, 9)
        for i in range(limit[0], limit[1]):
            for j in range(1, 9):
                print(self.board.get_square(i, j).piece)
                self.legal_moves[self.board.get_square(i, j).piece] = []

    def get_legal_moves(self, check):
        if check is not None and check.double_check():
            self.legal_moves[self.king] = self.king.possible_moves(check)
            return
        for piece in self.legal_moves:
            self.legal_moves[piece] = piece.possible_moves(check)

    def clear_legal_moves(self):
        for piece in self.legal_moves:
            self.legal_moves[piece] = []

    def highlight_legal_moves(self, piece):
        for move in self.legal_moves[piece]:
            move.highlighted = not move.highlighted

    def select(self, piece):
        self.selected = piece
        # print(sq)
        if self.selected is not None and self.selected.color != self.color:
            self.selected = None
        if self.selected is not None:
            # self.legal_moves = self.selected.possible_moves()
            self.highlight_legal_moves(self.selected)

    def unselect(self):
        self.highlight_legal_moves(self.selected)
        self.selected = None

    def play(self, x, y):

        # if self.king.in_check():
        #     if king in double check
        #         calculate king moves
        #         if no king moves
        #             checkmate
        #         if king moves
        #             add king moves
        #     if not in double check
        #         find moves for all pieces
        #         if no moves
        #             checkmate
        #         if moves:
        #             add moves
        # if not in check
        #     calculate moves and add

        sq = self.board.get_clicked_square(x, y)
        # print(sq)
        # print(self.legal_moves)
        if self.selected is not None:
            if sq in self.legal_moves[self.selected]:
                self.selected.move(sq)
                Player.turn ^= 1
                self.unselect()
                self.clear_legal_moves()
                check = self.opponent.king.in_check(self.opponent.king.square)
                if self.opponent.checkmate(check):
                    print('Game over')
            elif sq.piece is not None:
                if sq.piece == self.selected:
                    self.unselect()
                elif sq.piece.color == self.color:
                    self.unselect()
                    self.select(sq.piece)
            else:
                self.unselect()
        else:
            self.select(sq.piece)
