import random
import math


class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        self.num_mines = num_mines
        self.rows = rows
        self.cols = cols
        self.board = [[0 for c in range(cols)] for r in range(rows)]

        # Determine the location of the mines
        mine_locations = random.sample(range(rows*cols), num_mines)
        for loc in mine_locations:
            # Determine the row by figuring out how many sets of columns we have
            # past using integer division. Take the minimum in case loc = rows*cols,
            # in which case loc // cols = rows which overflows.
            r = min(loc // cols, rows-1) 
            c = loc % cols
            self.board[r][c] = float("inf")

            # Increment the count of the items around the block
            allowed_rows = [r]
            allowed_cols = [c] 

            if r+1 < rows:
                allowed_rows.append(r+1)
            if r-1 >= 0:
                allowed_rows.append(r-1)
            if c+1 < cols:
                allowed_cols.append(c+1)
            if c-1 >= 0:
                allowed_cols.append(c-1)

            # Note: This will increment self.board[r][c] which is ok since it is
            #       set to inf
            for ri in allowed_rows:
                for ci in allowed_cols:
                    self.board[ri][ci] += 1

    def containsMine(self, row, col):
        return math.isinf(self.board[row][col]) 

    def getValue(self, row, col):
        return self.board[row][col]

    def board_iterator(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield self.board[r][c]         
