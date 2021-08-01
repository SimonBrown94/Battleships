import numpy as np


class Board:
    """Create a game board"""

    def __init__(self, size):
        self.size = size
        self.board = np.array([['-' for i in range(size)] for j in range(size)])

    def coord_value(self, xval, yval):
        if xval > (self.size - 1) or yval > (self.size - 1):
            return 'Invalid board coordinate'
        else:
            return self.board[yval, xval]

    def coord_update(self, xval, yval, value):
        if xval > (self.size - 1) or yval > (self.size - 1):
            return 'Invalid board coordinate'
        else:
            self.board[yval, xval] = value

    def print_board(self):
        for line in self.board:
            print(*line, sep=" ")

