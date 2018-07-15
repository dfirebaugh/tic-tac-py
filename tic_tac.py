import os

# loop through the board and run a function
# using optional keyword arguments for optionally 
# doing something at the start or end of line
def fn_board(brd,fn,start=None,ending=None):
    new_brd = brd
    i = 0
    while i < len(new_brd):
        n = 0
        if start:
            start() # do something at beginning of line
        # if lines[0]:
        while n < len(new_brd[i]):
            fn(new_brd[i][n],i,n)
            n += 1
        if ending:
            ending() # do something at the end of line
        i += 1

    return new_brd

def init_board():
    board = [
        ['-','-','-'],
        ['-','-','-'],
        ['-','-','-']
        ]
    return board

board = init_board()
player_char = ''
computer_char = ''

def draw_board(brd):
    print('  ')
    def draw(*arg):
        if arg[0]:
            print(arg[0], end=' |  ')

    def draw_space():
        print('  ', end ="")
    def draw_line_end():
         print('\n')

    fn_board(
        brd,
        draw,
        start=draw_space,
        ending=draw_line_end
        )

def logger(msg):
    # cross-platform clears stdout
    os.system('cls' if os.name == 'nt' else 'clear')
    draw_board(board)
    print(msg)

def handle_error(msg):
    logger(msg)

def on_board(num):
    return 2 >= num >= 0

def set_player_char():
    global player_char
    while True:
        player_char = input('Choose [X] or [O]: ')
        if len(player_char) == 0:
            handle_error('You must input [X] or [O]')
            continue
        else:
            player_char = player_char[0].upper()
            if player_char != 'X' and player_char != 'O':
                handle_error('You must choose [X] or [O]')
                continue
            else:
                print('playerChar is:  ', player_char)
                break

def exec_turn():
    if player_char == '':
        set_player_char()

    while True:
        try:
            a, b = [int(x) for x in input('Enter a position (i.e. 2 numbers separated by spaces):  ').split()]
        except ValueError:
            handle_error('Error: please input 2 numbers separated by *SPACES')
            continue

        if on_board(a) and on_board(b):
            place_player([b,a], player_char)
            break
        else:
            handle_error('input not on the board (input numbers between 0 and 2')
            continue

def place_player(arr, char):
    if board[arr[0]][arr[1]] == '-':
        board[arr[0]][arr[1]] = char
        logger('placed')
    else:
        handle_error('invalid placement -- something already exists in this spot')
        print(board[arr[0]][arr[1]] , ' is already in that spot')
        exec_turn()
    return

def place_computer():
    global computer_char
    computer_char = "O" if player_char == 'X'  else "X"
    best_placement(board)

# returns coords of empty positions
def empty_spots(brd):
    arr = []
    def empty(*arg):
        if arg[0] == '-':
            arr.append([arg[1],arg[2]])

    fn_board(brd, empty)
    # print('empty spots: ', arr)
    
    return arr

def minimax(brd,player):
    # avail_spots will be evaluated as potential positions
    # if placing player_char in that position results in the player winning, 
    # decrease score of that spot
    # if placing computer_char in that position results in the computer winning,
    # increase score of spot
    new_brd = brd

    if check_win(new_brd,player_char):
        return -1
    elif check_win(new_brd,computer_char):
        return 1
    else:
        return 0

def best_placement(brd):
    # determine best place to move
    # currently the computer places in the first available empty square
    empties = empty_spots(brd)

    def evaluate_spots(n):
        if n < len(empty_spots(brd)):
            evaluate_spots(n+1);
        else:
            return
        temp = brd
        temp[empties[n][0]][empties[n][1]] = computer_char

        print("win? ", minimax(temp,computer_char))

    if not len(empty_spots(brd)) == 0:
        place_player(empty_spots(brd)[0],computer_char)
        # evaluate_spots(0)


def check_win(brd, player):
    win_conditions = [
        [[0,0],[0,1],[0,2]],
        [[1,0],[1,1],[1,2]],
        [[2,0],[2,1],[2,2]],
        
        [[0,0],[1,0],[2,0]],
        [[0,1],[1,1],[2,1]],
        [[0,2],[1,2],[2,2]],
        
        [[0,0],[1,1],[2,2]],
        [[2,0],[1,1],[0,2]]
    ]

    for cond in win_conditions:
        x = 0
        for i in cond:
            if brd[i[0]][i[1]] == player:
                x += 1
        if x == 3:
            return True
    return False

def game_over():
    if check_win(board,player_char): 
        return 'player'
    elif check_win(board,computer_char):
        return 'computer'

def game_loop():
    if game_over() == 'player': 
        logger('YOU WON THE GAME!!!')
        return
    elif game_over() == 'computer':
        logger('You lost')
        return
    else:
        if len(empty_spots(board)) == 0:
            logger('tied')
            return
        else:
            exec_turn()
            place_computer()
            game_loop()

game_loop()