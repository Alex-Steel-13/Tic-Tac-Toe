#This code uses bitboards to represent the grid, which means the grid is stored as a decimal number.
#Python converts the number into binary, which represents the grid. The first element is for crosses
#the second is for noughts
import time
import random
bitboards = [0,0]
nodes = 0
total_nodes = nodes
turn_nodes = 0
def move(bitboards, move, turn):
    #turn 0 =  X's turn, turn 1 = O's turn
    #Chekcs if there is a marker there already, then adds the move on 
    if has_marker(bitboards, move):
        temp_board = bitboards
        temp_board[turn] = bitboards[turn] | (1<<move)
        turn ^= 1
        return temp_board
# 0 1 2
# 3 4 5
# 6 7 8

def has_marker(bitboards, square):
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

def randomised_move(bitboards):
    while True:
        move = random.randint(0,8)
        if has_marker(bitboards, move):
            return move

def evaluate(bitboards):
    #checking for 3 in a row
    for i in range(3):
        for j in range(2):
            #iterates 3 times as there are 3 possible 3 in a row, and iterates twice, once for each bitboard
            if (get_bit(bitboards[j], i*3)) and (get_bit(bitboards[j], i*3+1)) and (get_bit(bitboards[j], i*3+2)):
                if j:
                    return -10
                elif not j:
                    return 10
    
    #checking for 3 in a column
    for i in range(3):
        for j in range(2):
            #column go up in differences of 3, see board above
            if (get_bit(bitboards[j], i)) and (get_bit(bitboards[j], i +3)) and (get_bit(bitboards[j], i+6)):
                if j:
                    return -10
                elif not j:
                    return 10
    
    #checking for diagonal
    for j in range(2):
        if get_bit(bitboards[j], 0) and get_bit(bitboards[j], 4) and get_bit(bitboards[j], 8):
            if j:
                return -10
            elif not j:
                return 10
    for j in range(2):
        if get_bit(bitboards[j], 6) and get_bit(bitboards[j], 4) and get_bit(bitboards[j], 2):
            if j:
                return -10
            elif not j:
                return 10
    return 0

def empty_squares(bitboards):
    temp_board = bitboards[0] | bitboards[1]
    if temp_board == 511:
        #511 in binary = 111 111 111
        return True
    return False



def print_board(bitboards):
    board = []
    for i in range(9):
        if get_bit(bitboards[0],i):
            board.append("X")
        elif get_bit(bitboards[1],i):
            board.append("O")
        else:
            board.append(" ")
    print(*board[0], board[1], board[2], sep = "|")
    print("-+-+-")
    print(*board[3], board[4], board[5], sep = "|")
    print("-+-+-")
    print(*board[6], board[7], board[8], sep = "|")

def minimax(bitboards, depth, isMax, alpha, beta):
    
    global nodes

    score = evaluate(bitboards)
    if score == 10:
        return score + depth
    elif score == -10:
        return score - depth
    if empty_squares(bitboards) or depth == 0:
        return 0
    if isMax:
        best = -1000
        for i in range(9):
            if has_marker(bitboards, i):
                nodes +=1
                bitboards = move(bitboards, i, 0)
                score_board = minimax(bitboards, depth - 1, not isMax, alpha, beta)
                best = max(best, score_board)
                bitboards = take_back(bitboards, i, 1)
                alpha = max(alpha, score_board)
                if beta <= alpha:
                    break
    else:
        best = 1000
        for i in range(9):
            if has_marker(bitboards, i):
                nodes += 1
                bitboards = move(bitboards, i, 1)
                score_board = minimax(bitboards, depth - 1, not isMax, alpha, beta)
                best = min(best, score_board)
                bitboards = take_back(bitboards, i, 0)
                beta = min(beta, score_board)
                if beta <= alpha:
                    break
    return best

def best_move(bitboards):
    
    global nodes
    global total_nodes

    total_nodes += nodes
    best_val = -1000
    best_move = -1
    start_time = time.time()
    for i in range(9):
        if has_marker(bitboards, i):
            cur_nodes = nodes
            cur_time= time.time()
            bitboards = move(bitboards, i, 0)
            move_val = minimax(bitboards, 10, False, -1000000, 1000000)
            bitboards = take_back(bitboards, i, 1)
            if move_val > best_val:
                best_val = move_val
                best_move = i
    end_time = time.time()
    return best_move



total_time = 0
turn = 1
wins = 0
draws = 0
losses = 0
games = 0
start = time.time()
while games != 1000:
    if turn:
        bitboards = move(bitboards, randomised_move(bitboards), turn)
        turn = 0
    else:
        computer_move = int(best_move(bitboards))
        bitboards = move(bitboards, computer_move, turn)
        turn = 1
    score = evaluate(bitboards)
    if score == 10:
        print("Crosses won")
        wins+=1
        print(f"Wins: {wins}\nLosses: {losses}\nDraws: {draws}\n Percentage won: {(wins/(wins+losses+draws))*100}")
        bitboards = [0,0]
        games+=1
    elif score == -10:
        print("Noughts won")
        losses +=1
        print(f"Wins: {wins}\nLosses: {losses}\nDraws: {draws}\n Percentage won: {(wins/(wins+losses+draws))*100}")
        bitboards = [0,0]
        games+=1
    elif empty_squares(bitboards):
        bitboards = [0,0]
        draws += 1
        games+=1
        print(f"Wins: {wins}\nLosses: {losses}\nDraws: {draws}\nPercentage won: {(wins/(wins+losses+draws))*100}")
        print("Draw")
end = time.time()
print(end-start)
print(f"Number of nodes searched: {nodes}")