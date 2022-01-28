import pygame

pygame.init()


# TODO: implement checks
class Player:

    turn = 0

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.selected = None
        self.legal_moves = []

    def highlight_legal_moves(self):
        for move in self.legal_moves:
            move.highlighted = not move.highlighted

    def play(self, x, y):
        sq = self.board.get_clicked_square(x, y)
        # print(sq)
        # print(self.legal_moves)
        if self.selected is not None:
            if sq in self.legal_moves:
                self.selected.move(sq)
                Player.turn ^= 1

            self.selected = None
            self.highlight_legal_moves()
            self.legal_moves = []
        else:
            self.selected = sq.piece
            # print(sq)
            if self.selected is not None and self.selected.color != self.color:
                self.selected = None
            if self.selected is not None:
                self.legal_moves = self.selected.possible_moves()
                self.highlight_legal_moves()
