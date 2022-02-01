def in_path(square1, square2, move):
    if square1.row == square2.row:
        # horizontal
        return move.row == square1.row
    elif square1.column == square2.column:
        # vertical
        return move.column == square1.column
    else:
        # diagonal
        # TODO: implement straight line equation
        pass


class Check:
    def __init__(self, king, pieces):
        self.king = king
        self.pieces = pieces

    def double_check(self):
        return len(self.pieces) == 2

    def is_restricted(self, move):
        if move is self.pieces[0].square:
            return False
        return not in_path(self.king.square, self.pieces[0].square, move)


class Pin:
    pass
