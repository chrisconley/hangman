def generate_board(n_row, n_col, live):
    return tuple(tuple(
        ((row,col) in live, neighbours(row,col,n_row,n_col))
        for col in range(n_col)) for row in range(n_row) )

def neighbours(row, col, n_row,n_col):
    return tuple((r,c)
        for r in range(max(0,row-1),min(n_row-1,row+1)+1)
            for c in range(max(0,col-1),min(n_col-1,col+1)+1)
                if (r != row) or (c != col))

def next_state(row, board):
    for state,nbrs in row :
        live = sum(1 for r, c in nbrs if board[r][c][0])
        yield state,2<=live<= 3 if state else live == 3,nbrs

def cycle(board):
    return tuple(tuple(
        (new,nns) for _, new, nns in row)
            for row in tuple(tuple(next_state(row,board))
                for row in board))

def render(board):
    return "\n".join(("".join('*' if col else '_'
                        for col,_ in row)) for row in board)

import time
start = time.time()
board = generate_board(5,5,((2,1),(2,2),(2,3)))
for i in range(100000) :
    board = cycle(board)
    #print render(board)
stop = time.time()
print "Time:", stop - start
