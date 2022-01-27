import pygame

pygame.init()


# TODO: implement checks
class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.selected = None
        self.legal_moves = []

    def play(self, x, y):
        sq = self.board.get_square(x, y)
        print(sq)
        print(self.legal_moves)
        if self.selected is not None:
            if sq in self.legal_moves:
                self.selected.move(sq)

            self.selected = None
            for square in self.legal_moves:
                square.highlighted = False
            self.legal_moves = []
        else:
            # TODO: make sure that the piece that's selected is the same as player color
            self.selected = sq.piece
            if self.selected is not None:
                self.legal_moves = self.selected.possible_moves()
