bitboards = [0,0]

# 0 1 2
# 3 4 5
# 6 7 8

# 9 10 11
# 12 13 14
# 15 16 17

# 18 19 20
# 21 22 23
# 24 25 26
nodes = 0
move_nodes = 0
def move(bitboards, move, turn):
    #turn 0 =  X's turn, turn 1 = O's turn
    #Chekcs if there is a marker there already, then adds the move on 
    move = int(move)
    if has_marker(bitboards, move):
        temp_board = bitboards
        temp_board[turn] = bitboards[turn] | (1<<move)
        turn ^= 1
        return temp_board

def has_marker(bitboards, square):
    #returns false if there is a marker, return true if no marker
    occupied = bitboards[0] | bitboards[1]
    if occupied & (1<<square) == (1<<square):
        return False
    return True

def take_back(bitboards, move, turn):
    #use to take back move in minimax
    turn ^= 1
    bitboards[turn] = bitboards[turn] & ~(1<<move)
    return bitboards

def get_bit(bitboard, square):
    #returns the bit if there is one there
    return bitboard & (1 << square)

def evaluate(bitboards):
    # list of all possible wins
    win_table = [
    # rows (per board)
    [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26],
    # columns (per board)
    [0, 3, 6], [1, 4, 7], [2, 5, 8], [9, 12, 15], [10, 13, 16], [11, 14, 17], [18, 21, 24], [19, 22, 25], [20, 23, 26],
    # diagonals (per board)
    [0, 4, 8], [2, 4, 6], [9, 13, 17], [11, 13, 15], [18, 22, 26], [20, 22, 24],
    # stacks (between boards)
    [0, 9, 18], [1, 10, 19], [2, 11, 20], [3, 12, 21], [4, 13, 22], [5, 14, 23], [6, 15, 24], [7, 16, 25], [8, 17, 26],
    # diagonals (between board)
    [0, 12, 24], [1, 13, 25], [2, 14, 26], [6, 12, 18], [7, 13, 19], [8, 14, 20], [0, 10, 20], [3, 13, 23], [6, 16, 26],
    [2, 10, 18], [5, 13, 21], [8, 16, 24], [0, 13, 26], [2, 13, 24], [6, 13, 20], [8, 13, 18]
    ]
    # for loop for the two bitboards
    for p in range(2):
        # for loop for every list in the win table
        for i in range(len(win_table)):
            counter = 0
            #iterate through each element of the list
            for j in range(3):
                if get_bit(bitboards[p], win_table[i][j]):
                    counter+=1
            # if counter is 3, then someone has won
            if counter == 3:
                if p:
                    return -10
                else:
                    return 10

def empty_squares(bitboards):
    temp_board = bitboards[0] | bitboards[1]
    if temp_board == 134217727:
        #511 in binary = 111 111 111
        return True
    return False

def minimax(bitboards, depth, isMax, alpha, beta):
    
    global move_nodes
    
    score = evaluate(bitboards)
    if score == 10:
        #print(score + depth)
        return score + depth
    elif score == -10:
        #print(score - depth)
        return score - depth
    elif depth == 0:
        return 0
    
    if isMax:
        best = -10000
        for i in range(27):
            move_nodes +=1
            if has_marker(bitboards, i):
                bitboards = move(bitboards, i, 0)
                score_board = minimax(bitboards, depth - 1, not isMax, alpha, beta)
                best = max(best, score_board)
                bitboards = take_back(bitboards, i, 1)
                alpha = max(alpha, score_board)
                if beta <= alpha:
                    break
    
    else:
        best = 10000
        for i in range(27):
            move_nodes +=1
            if has_marker(bitboards, i):
                bitboards = move(bitboards, i, 0)
                score_board = minimax(bitboards, depth - 1, not isMax, alpha, beta)
                best = min(best, score_board)
                bitboards = take_back(bitboards, i, 1)
                beta = min(beta, score_board)
                if beta <= alpha:
                    break
    return best

def best_move(bitboards):
    
    global nodes
    global move_nodes

    best_val = -1000
    best_move = -1
    for i in range(27):
        if has_marker(bitboards, i):
            move_nodes = 0
            bitboards = move(bitboards, i, 0)
            move_val = minimax(bitboards, 5, False, -1000000, 1000000)
            bitboards = take_back(bitboards, i, 1)
            if move_val > best_val:
                best_val = move_val
                best_move = i
                print(best_move)
            print(move_nodes)
    return best_move

def print_board(bitboards):
    board = []
    for i in range(27):
        if get_bit(bitboards[0],i):
            board.append("X")
        elif get_bit(bitboards[1],i):
            board.append("O")
        else:
            board.append(" ")
    print("Board 1")
    print(*board[0], board[1], board[2], sep = "|")
    print("-+-+-")
    print(*board[3], board[4], board[5], sep = "|")
    print("-+-+-")
    print(*board[6], board[7], board[8], sep = "|")

    print("Board 2")
    print(*board[9], board[10], board[11], sep = "|")
    print("-+-+-")
    print(*board[12], board[13], board[14], sep = "|")
    print("-+-+-")
    print(*board[15], board[16], board[17], sep = "|")

    print("Board 3")
    print(*board[18], board[19], board[20], sep = "|")
    print("-+-+-")
    print(*board[21], board[22], board[23], sep = "|")
    print("-+-+-")
    print(*board[24], board[25], board[26], sep = "|")
turn = 1
while True:
    print(bitboards)
    if turn:
        print("It is nought's turn")
        player_move = (int(input("What square?"))-1)
        bitboards = move(bitboards, player_move, turn)
        turn = 0
    else:
        print("Its the computers turn")
        computer_move = int(best_move(bitboards))
        bitboards = move(bitboards, computer_move, turn)
        turn = 1
    print_board(bitboards)
    score = evaluate(bitboards)
    if score == 10:
        print("Crosses won")
        break
    elif score == -10:
        print("Noughts won")
        break
    elif empty_squares(bitboards):
        print("Draw")
        break