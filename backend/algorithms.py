import random
from helpers import abp_minimax_recursive, empty_cells, minimax_recursive, winning_moves, opp_winning_moves, priority_squares

def random_move(grid):
    if empty_cell := random.choice(empty_cells(grid)):
        grid[empty_cell[0]][empty_cell[1]] = "X"
        
def heuristic(grid):
    if winning_moves_list := winning_moves(grid):
        winning_move = random.choice(winning_moves_list)
        grid[winning_move[0]][winning_move[1]] = "X"
    elif block_win_list := opp_winning_moves(grid):
        block_win = random.choice(block_win_list)
        grid[block_win[0]][block_win[1]] = "X"
    else:
        priority_squares(grid)
        
def minimax(grid):
    max_squares = []
    ecs = empty_cells(grid)
    
    for row, col in ecs:
        grid[row][col] = "X"
        score, depth = minimax_recursive(grid)
        if score == 1:
            max_squares.append([row, col, depth])
        grid[row][col] = " "
        
    if max_squares:
        max_squares.sort(key=lambda x: x[2])
        row, col, _ = max_squares[0]
        grid[row][col] = "X"
    else:
        heuristic(grid)


def abp_minimax(grid):
    max_squares = []
    for row, col in empty_cells(grid):
        grid[row][col] = "X"
        val, depth = abp_minimax_recursive(grid)
        if val == 1:
            max_squares.append([row, col, depth])
        grid[row][col] = " "
        
    if max_squares:
        max_squares.sort(key=lambda x: x[2])
        row, col, _ = max_squares[0]
        grid[row][col] = "X"
    else:
        heuristic(grid)
