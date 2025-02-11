import random
import os

SIZE = 4

def clear_screen():
    os.system('cls')  # Windows 清屏

def init_board():
    board = [[0]*SIZE for _ in range(SIZE)]
    add_new_number(board)
    add_new_number(board)
    return board

def add_new_number(board):
    empty_cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empty_cells:
        return
    r, c = random.choice(empty_cells)
    board[r][c] = 4 if random.random() > 0.9 else 2

def compress(row):
    new_row = [num for num in row if num != 0]
    new_row += [0]*(SIZE - len(new_row))
    return new_row

def merge(row):
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(board):
    new_board = []
    for row in board:
        compressed = compress(row)
        merged = merge(compressed)
        new_board.append(compress(merged))
    return new_board

def rotate(board):
    return list(map(list, zip(*board[::-1])))

def move_right(board):
    return [row[::-1] for row in move_left([row[::-1] for row in board])]

def move_down(board):
    rotated = rotate(board)
    moved = move_left(rotated)
    for _ in range(3):
        moved = rotate(moved)
    return moved

def move_up(board):
    for _ in range(3):
        board = rotate(board)
    board = move_left(board)
    board = rotate(board)
    return board

def print_board(board):
    clear_screen()
    for row in board:
        print("\t".join(str(num) if num else "." for num in row))
    print()

def check_win(board):
    return any(2048 in row for row in board)

def check_game_over(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return False
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return False
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return False
    return True

def main():
    board = init_board()
    while True:
        print_board(board)
        if check_win(board):
            print("恭喜，达成 2048！")
            break
        if check_game_over(board):
            print("游戏结束，没有可移动的方块。")
            break

        move = input("方向 (W 上, S 下, A 左, D 右, Q 退出): ").lower()
        if move == 'q':
            break
        elif move == 'w':
            board = move_up(board)
        elif move == 's':
            board = move_down(board)
        elif move == 'a':
            board = move_left(board)
        elif move == 'd':
            board = move_right(board)
        add_new_number(board)

if __name__ == "__main__":
    main()