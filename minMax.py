from copy import deepcopy

# Evaluates if the given player has won.
# Returns [(bool) X, (bool) Y]
# X denotes if the player has won.
# Y denotes if the game is over (no more empty spaces)
def evaluate(brd, player):

    for row in brd:
        if row[0] == player and len(set(row)) == 1:
            return [True, True]

    for i in range(3):
        col = [brd[n][i] for n in range(3)]
        if col[0] == player and len(set(col)) == 1:
            return [True, True]

    if brd[0][0] == player and brd[1][1] == player and brd[2][2] == player:
        return [True, True]

    if brd[0][2] == player and brd[1][1] == player and brd[2][0] == player:
        return [True, True]

    if sum([ row.count("-") for row in brd ]) == 0:
        return [False, True]
    
    return [False, False]
    

# Generator function to collect empty spaces
def getEmpty(board):
    for y in range(3):
        for x in range(3):
            if board[y][x] == "-":
                yield [x,y]


# Recursive minMax algorithm.
def minMax(board, char, player = 1, depth = 0):

    scores = []
    oponents_char = "X" if (char == "O") else "O"

    for pos in getEmpty(board):

        new_board = deepcopy(board)

        if player == 1:
            new_board[pos[1]][pos[0]] = char
        else:
            new_board[pos[1]][pos[0]] = oponents_char

        score = 0    
        e = evaluate(new_board, char)

        if e[0]:
            scores.append((100-depth, pos))
        else:
            e = evaluate(new_board, oponents_char)
            if e[0]:
                scores.append((depth-100, pos))
            elif e[1]:
                scores.append((0, pos))
            else:
                scores.append(minMax(new_board, char, player*-1, depth-1))
            
    if player == 1:
        return min(scores)

    return max(scores)
