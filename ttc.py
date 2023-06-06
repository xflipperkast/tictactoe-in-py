import random

def print_board(board):
    print('     0       1       2')
    for i, row in enumerate(board):
        print(f'{i} ', end='')
        for item in row:
            if item == 0:
                print('[ _ ]', end='   ')
            elif item == 1:
                print('[ X ]', end='   ')
            else:
                print('[ O ]', end='   ')
        print('\n')

def check_win(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != 0:
            return True

    for col in range(len(board)):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != 0:
            return True

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return True

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return True

    return False

def check_draw(board):
    for row in board:
        if 0 in row:
            return False
    return True

def get_best_move(board, computer, player):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = computer
                if check_win(board):
                    return (i, j)
                board[i][j] = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player
                if check_win(board):
                    return (i, j)
                board[i][j] = 0

    if board[1][1] == 0:
        return (1, 1)

    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)
    for corner in corners:
        if board[corner[0]][corner[1]] == 0:
            return corner

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return (i, j)

def tictactoe(mode):
    board = [[0, 0, 0] for _ in range(3)]
    player, computer = 1, 2
    while True:
        print_board(board)
        while True:
            try:
                move = input("Your move (row, col): ")
                move = list(map(int, move.split(',')))
                if move[0] not in [0, 1, 2] or move[1] not in [0, 1, 2]:
                    print("Invalid move. Please enter numbers between 0 and 2 separated by a comma.")
                    continue
                if board[move[0]][move[1]] != 0:
                    print("This position is already filled. Please enter a valid move.")
                    continue
                board[move[0]][move[1]] = player
                break
            except Exception as e:
                print("Invalid input. Please enter numbers separated by a comma.")

        if check_win(board):
            print_board(board)
            print("Player wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw.")
            break

        if mode == 'easy':
            move = (random.randint(0, 2), random.randint(0, 2))
            while board[move[0]][move[1]] != 0:
                move = (random.randint(0, 2), random.randint(0, 2))
        else:
            move = get_best_move(board, computer, player)

        board[move[0]][move[1]] = computer
        if check_win(board):
            print_board(board)
            print("Computer wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw.")
            break

def get_mode():
    print("Gamemodes:")
    print("- 1: easy")
    print("- 2: normal")
    print("- 3: hard")
    print("- 4: impossible")
    mode = input("Choose your game mode (1-4): ")
    if mode == '1':
        return 'easy'
    elif mode == '2':
        return 'normal'
    elif mode == '3':
        return 'hard'
    elif mode == '4':
        return 'impossible'
    else:
        print("Invalid choice. Please choose a number from 1-4.")
        return get_mode()

while True:
    mode = get_mode()
    tictactoe(mode)
    play_again = input("Would you like to play again? (yes/no): ")
    if play_again.lower() != 'yes':
        break
