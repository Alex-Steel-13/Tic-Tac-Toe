#This code uses bitboards to represent the grid, which means the grid is stored as a decimal number.
#Python converts the number into binary, which represents the grid. The first element is for crosses
#the second is for noughts
bitboards = [0,0]
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
    bitboards[turn] ^= (1<<move)
    #Krentz's method, take compliment of move left shifted by the square
    #bitboards[turn] & ~(1<<move)

def get_bit(bitboard, square):
    #returns the bit if there is one there
    return bitboard & (1 << square)

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
        return False
    return True

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

turn = 0
while True:
    if turn:
        print("It is nought's turn")
        player_move = (int(input("What square?"))-1)
        bitboards = move(bitboards, player_move, turn)
        turn = 0
    else:
        print("It is cross' turn")
        player_move = (int(input("What square?"))-1)
        bitboards = move(bitboards, player_move, turn)
        turn = 1
    score = evaluate(bitboards)
    print_board(bitboards)
    if score == 10:
        print("Crosses won")
        break
    elif score == -10:
        print("Noughts won")
        break
    elif not empty_squares(bitboards):
        print("Draw")
        break