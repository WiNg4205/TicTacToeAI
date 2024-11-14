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

center = [1,1]
corner_squares = [[0,0], [0,2], [2,0], [2,2]]
side_squares = [[0,1], [1,0], [1,2], [2,1]]


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

def minimax_recursive(grid, depth=0):
    if (val := value(grid)) is not None:
        return val, depth

    if player(grid) == "X":
        max_val = -1
        best_depth = float('inf')
        for row, col in empty_cells(grid):
            grid[row][col] = "X"
            score, child_depth = minimax_recursive(grid, depth + 1)
            grid[row][col] = " "
            if score > max_val or (score == max_val and child_depth < best_depth):
                max_val = score
                best_depth = child_depth
        return max_val, best_depth
    
    elif player(grid) == "O":
        min_val = 1
        best_depth = float('inf')
        for row, col in empty_cells(grid):
            grid[row][col] = "O"
            score, child_depth = minimax_recursive(grid, depth + 1)
            grid[row][col] = " "
            if score < min_val or (score == min_val and child_depth < best_depth):
                min_val = score
                best_depth = child_depth
        return min_val, best_depth


def abp_minimax_recursive(grid, alpha=-1, beta=1, depth=0):
    if (val := value(grid)) is not None:
        return val, depth

    if player(grid) == "X":
        max_val = -1
        best_depth = float('inf')
        for row, col in empty_cells(grid):
            grid[row][col] = "X"
            score, child_depth = abp_minimax_recursive(grid, alpha, beta, depth + 1)
            grid[row][col] = " "
            if score > max_val or (score == max_val and child_depth < best_depth):
                max_val = score
                best_depth = child_depth
            alpha = max(alpha, max_val)
            if beta <= alpha:
                break
        return max_val, best_depth

    elif player(grid) == "O":
        min_val = 1
        best_depth = float('inf')
        for row, col in empty_cells(grid):
            grid[row][col] = "O"
            score, child_depth = abp_minimax_recursive(grid, alpha, beta, depth + 1)
            grid[row][col] = " "
            if score < min_val or (score == min_val and child_depth < best_depth):
                min_val = score
                best_depth = child_depth
            beta = min(beta, min_val)
            if beta <= alpha:
                break
        return min_val, best_depth
