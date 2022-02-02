def in_path(king_square, piece_square, move):
    if move == king_square:
        return False
    if king_square.row == piece_square.row:
        # horizontal
        if move.row == king_square.row:
            return max(king_square.column, piece_square.column) >= move.column >= min(king_square.column, piece_square.column)
    elif king_square.column == piece_square.column:
        # vertical
        if move.column == king_square.column:
            return max(king_square.row, piece_square.row) >= move.row >= min(king_square.row, piece_square.row)
    else:
        # diagonal
        print('here')
        m = (king_square.row - piece_square.row) // (king_square.column - piece_square.column)
        c = - m * king_square.column + king_square.row
        print(m, c)
        if move.row == m * move.column + c:
            h_row, l_row = max(king_square.row, piece_square.row), min(king_square.row, piece_square.row)
            h_col, l_col = max(king_square.column, piece_square.column), min(king_square.column, piece_square.column)
            return h_row >= move.row >= l_row and h_col >= move.column >= l_col
        else:
            return False

    # if move == king_square:
    #     return False
    # h_row, l_row = max(king_square.row, piece_square.row), min(king_square.row, piece_square.row)
    # h_col, l_col = max(king_square.column, piece_square.column), min(king_square.column, piece_square.column)
    # return h_row >= move.row >= l_row and h_col >= move.column >= l_col


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
