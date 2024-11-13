import random
from counter import increment

winList = [
    [[0,0], [0,1], [0,2]],
    [[1,0], [1,1], [1,2]],
    [[2,0], [2,1], [2,2]],
    [[0,0], [1,0], [2,0]],
    [[0,1], [1,1], [2,1]],
    [[0,2], [1,2], [2,2]],
    [[0,0], [1,1], [2,2]],
    [[2,0], [1,1], [0,2]],
]

def empty_cells(grid):
    return [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == " "]

def check_lose(grid):
    increment()
    return any(all(grid[x][y] == "O" for x, y in win) for win in winList)

def check_win(grid):
    increment()
    return any(all(grid[x][y] == "X" for x, y in win) for win in winList)

def winning_moves(grid):
    ret = []
    for row, col in empty_cells(grid):
        grid[row][col] = "X"
        if check_win(grid):
            ret.append([row, col])
        grid[row][col] = " "
    return ret

def opp_winning_moves(grid):
    ret = []
    for row, col in empty_cells(grid):
        grid[row][col] = "O"
        if check_lose(grid):
            ret.append([row, col])
        grid[row][col] = " "
    return ret

def random_move(grid):
    if empty_cell := random.choice(empty_cells(grid)):
        grid[empty_cell[0]][empty_cell[1]] = "X"

def priority_squares(grid):
    # take center square or corner squares whenever possible    
    if grid[1][1] == " ":
        grid[1][1] = "X"
        return
    corner_squares = [[0,0], [0,2], [2,0], [2,2]]
    empty_corner_squares = [square for square in corner_squares if grid[square[0]][square[1]] == " "]
    if empty_corner_squares:
        square = random.choice(empty_corner_squares)
        grid[square[0]][square[1]] = "X"
    else:
        random_move(grid)

def value(grid):
    if check_win(grid):
        return 1
    elif check_lose(grid):
        return -1
    elif not empty_cells(grid):
        return 0
    else:
        return None
    
def player(grid):
    return "X" if len(empty_cells(grid)) % 2 == 0 else "O"

def minimax_recursive(grid):
    if (val := value(grid)) is not None:
        return val

    if player(grid) == "X":
        max_val = -1
        for row, col in empty_cells(grid):
            grid[row][col] = "X"
            max_val = max(max_val, minimax_recursive(grid))
            grid[row][col] = " "
        return max_val
    
    elif player(grid) == "O":
        min_val = 1
        for row, col in empty_cells(grid):
            grid[row][col] = "O"
            min_val = min(min_val, minimax_recursive(grid))
            grid[row][col] = " "
        return min_val

def abp_minimax_recursive(grid, alpha=-1, beta=1):
    if (val := value(grid)) is not None:
        return val

    if player(grid) == "X":
        max_val = -1
        for row, col in empty_cells(grid):
            grid[row][col] = "X"
            max_val = max(max_val, abp_minimax_recursive(grid, alpha, beta))
            grid[row][col] = " "
            alpha = max(alpha, max_val)
            if beta <= alpha:
                break
        return max_val
    
    elif player(grid) == "O":
        min_val = 1
        for row, col in empty_cells(grid):
            grid[row][col] = "O"
            min_val = min(min_val, abp_minimax_recursive(grid, alpha, beta))
            grid[row][col] = " "
            beta = min(beta, min_val)
            if beta <= alpha:
                break
        return min_val
