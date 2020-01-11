import numpy as np
import copy

board = [[0 for x in range(5)] for y in range(3)]
m = copy.deepcopy(board)
m[0][0] = 2
print(board)




board = [['0' for x in range(5)] for y in range(3)]


board = [['0' for x in range(5)] for y in range(3)]

""" Set hound position with value 1"""
board[0][1] = 'c'
board[1][0] = 'c'
board[2][1] = 'c'

""" Set hare position with value 2 """
board[1][4] = 'i'

pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(board) if 'i' in row]
pozitii_caini = [(index, row.index('c')) for index, row in enumerate(board) if 'c' in row]
linie1, col1 = pozitii_caini[2]
print("linie ", linie1)
print("coloana ", col1)
print(pozitii_caini)

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

