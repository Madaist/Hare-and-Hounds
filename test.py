import numpy as np

board = [['0' for x in range(5)] for y in range(3)]

""" Set hound position with value 1"""
board[0][1] = 'c1'
board[1][0] = 'c2'
board[2][1] = 'c3'

""" Set hare position with value 2 """
board[1][4] = 'i'

pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(board) if 'i' in row]
pozitie_c1 = [(index, row.index('c1')) for index, row in enumerate(board) if 'c1' in row]
pozitie_c2 = [(index, row.index('c2')) for index, row in enumerate(board) if 'c2' in row]
pozitie_c3 = [(index, row.index('c3')) for index, row in enumerate(board) if 'c3' in row]
print("iepure ", pozitie_iepure)
print(pozitie_c2)

ls = [1] * 9
print("ls ", ls)


def print_invalid():
    print('Invalid Move !')


def print_game_state(board):
    """
    print board
    with X for hounds
    with 0 for hare
    """
    print('\t0\t1\t2\t3\t4')
    print('  ----------------------')
    illegal_moves = [(0, 0), (2, 0), (0, 4), (2, 4)]
    for i in range(len(board)):
        buffer = ''
        buffer += str(i) + '|\t'
        for j in range(len(board[i])):
            if board[i][j] == 1:
                buffer += 'c\t'
            elif board[i][j] == 2:
                buffer += 'i\t'
            elif (i, j) in illegal_moves:
                buffer += ' \t'
            else:
                buffer += '-\t'
        print(buffer)
    print('-' * 30)


print_game_state(board)

