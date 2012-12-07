class Cell(object):
    def __init__(self,row,col,state):
        self.row = row
        self.col = col
        self.neighbours = {}
        self.state = state
        self.marked = False
    def set_neighbour(self,c):
        neighbour = self.neighbours.get((c.row,c.col),None)
        if not neighbour :
            self.neighbours[(c.row,c.col)] = c
    def live_neighbours(self):
        live = 0
        for cell in self.neighbours.values() :
            if cell.state :
                live += 1
        return live

    def cycle(self):
        live = self.live_neighbours()
        if self.state :
            if live < 2 : self.marked = False
            elif live > 3 : self.marked = False
            else : self.marked = True
        elif live == 3 :
            self.marked = True
        else :
            self.marked = False

    def switch(self):
        self.state = self.marked

class Board(object):
    def __init__(self,rows,cols,live):
        self.cells = []
        self.rows = rows
        self.cols = cols
        for row_nbr in range(rows) :
            row = []
            self.cells.append(row)
            for col_nbr in range(cols) :
                if (row_nbr,col_nbr) in live :
                    row.append(Cell(row_nbr,col_nbr,True))
                else :
                    row.append(Cell(row_nbr,col_nbr,False))
        for row_nbr in range(rows) :
            for col_nbr in range(cols) :
                for row_offset in (-1,0,1) :
                    for col_offset in (-1,0,1) :
                        self.set_neighbours(
                            row_nbr,col_nbr,
                            row_offset,col_offset)
    def set_neighbours(self,row_nbr,col_nbr,
                       row_offset,col_offset):
        n_row = row_nbr + row_offset
        n_col = col_nbr + col_offset
        if 0 <= n_row < self.rows :
            if 0 <= n_col < self.cols :
                if (n_row != row_nbr) or \
                    (n_col != col_nbr) :
                    self.cells[row_nbr][col_nbr]\
                        .set_neighbour(
                            self.cells[n_row][n_col])

    def show(self):
        buffer = []
        for row in range(self.rows) :
            row_buffer = []
            for col in range(self.cols) :
                if self.cells[row][col].state == True :
                    row_buffer.append('*')
                else :
                    row_buffer.append('_')
            buffer.append("".join(row_buffer))
        return "\n".join(buffer)

    def cycle(self):
        for row in range(self.rows) :
            for col in range(self.cols) :
                self.cells[row][col].cycle()
        for row in range(self.rows) :
            for col in range(self.cols) :
                self.cells[row][col].switch()

import time
if __name__ == "__main__" :
#    print board.show()
    start = time.time()
    board = Board(5,5,((2,1),(2,2),(2,3)))
    for i in range(100000) :
        board.cycle()
        #print board.show()
    stop = time.time()
    print "Time:", stop - start
