import os
clear = lambda: os.system('cls')
import time

nodes = 0

def evaluate(board):
	#checking if there are 3 in a row for each row on all 3 depth, but not across depths
	for depth in range(3):
		for row in range(3):
			if board[depth][row][0] == board[depth][row][1] and board[depth][row][2] == board[depth][row][1]:
					if board[depth][row][0] == "X":
						return 10
					elif board[depth][row][0] == "O":
						return -10
	#now checking if there are 3 in a row for each column on all 3 depths
	for depth in range(3):
		for column in range(3):
			if board[depth][0][column] == board[depth][1][column] and board[depth][1][column] == board[depth][2][column]:
					if board[depth][0][column] == "X":
						return 10
					elif board[depth][0][column] == "O":
						return -10
	#now checking for 3 in a row going across depths
	for row in range(3):
		for column in range(3):
			if board[0][row][column] == board[1][row][column] and board[1][row][column] == board[2][row][column]:
				if board[0][row][column] == "X":
					return 10
				elif board[0][row][column] == "O":
					return 10
	#now checking for 3 in a diagonal not across depths
	for depth in range(3):
		if board[depth][0][0] == "X" and board[depth][1][1] == "X" and board[depth][2][2] == "X":
			return 10
		elif board[depth][0][0] == "O" and board[depth][1][1] == "O" and board[depth][2][2] == "O":
			return -10
		elif board[depth][2][0] == "X" and board[depth][1][1] == "X" and board[depth][0][2] == "X":
			return 10
		elif board[depth][2][0] == "O" and board[depth][1][1] == "O" and board[depth][0][2] == "O":
			return -10
	#now checking for 3 in a diagonal across depth, but not going diagonally through centre
	for column in range(3):
			if board[0][0][column] == "X" and board[1][1][column] == "X" and board[2][2][column] == "X":
				return 10
			elif board[0][0][column] == "O" and board[1][1][column] == "O" and board[2][2][column] == "O":
				return -10
			if board[0][2][column] == "X" and board[1][1][column] == "X" and board[2][0][column] == "X":
				return 10
			elif board[0][2][column] == "O" and board[1][1][column] == "O" and board[2][0][column] == "O":
				return -10
	#now checking for 3 in a row through the diagonal through centre diagonal
	if board[0][0][0] == "X" and board[1][1][1] == "X" and board[2][2][2] == "X":
		return 10
	elif board[0][0][0] == "O" and board[1][1][1] == "O" and board[2][2][2] == "O":
		return -10
	
	elif board[0][2][2] == "X" and board[1][1][1] == "X" and board[2][0][0] == "X":
		return 10
	elif board[0][2][2] == "O" and board[1][1][1] == "O" and board[2][0][0] == "O":
		return -10
	
	elif board[0][0][2] == "X" and board[1][1][1] == "X" and board[2][2][0] == "X":
		return 10
	elif board[0][0][2] == "O" and board[1][1][1] == "O" and board[2][2][0] == "O":
		return -10

	elif board[0][2][0] == "X" and board[1][1][1] == "X" and board[2][0][2] == "X":
		return 10
	elif board[0][2][2] == "O" and board[1][1][1] == "O" and board[2][0][2] == "O":
		return -10
	return 0

def square_converter(board, b):
	while True:
		square = int(input("Enter the square you want, from 1 - 9"))
		#if the remainder of the randomnumber /3 is 0, it is the 3rd column
		if square%3 == 0:
			column = 2
			row = int((square/3) - 1)
		#if we go back one, then we can find if it is divisible by 3 then we know it is the first column
		elif (square-1)%3 == 0:
			column = 0
			row = int((square-1)/3)
		elif (square-2)%3 == 0:
			column = 1
			row = int((square-2)/3)
		if board[b][row][column] == " ":
			return (row,column)

def make_move(board, computer_turn):
	while True:
		if computer_turn:
			move = best_move(board)
			print_board(board)
			print(move)
			board[move[0]][move[1]][move[2]] = computer
			break
		elif not computer_turn:
			b = int(input("Enter which board you are playing from, 1, 2, or 3"))
			b -= 1
			square = square_converter(board, b)
			if board[b][square[0]][square[1]] == " ":
				board[b][square[0]][square[1]] = "O"
				break

def print_board(board):
	#clear()
	print("Board 1")
	for b in range(3):
		for i in range(3):
			if i!=2:
				print(*board[b][i], sep = "|")
				print('-+-+-')
			else:
				print(*board[b][i], sep = "|")
		if b !=2:
			print(f"\nBoard {b+2}")

def empty_square(board):
	for b in range(3):
		for row in range(3):
			for column in range(3):
				if board[b][row][column] == " ":
					return False
	return True

def count_empty_squares(board):
	count = 0
	for b in range(3):
		for row in range(3):
			for column in range(3):
				if board[b][row][column] == " ":
					count+=1
	return count

def minimax(board, depth, isMax, alpha, beta):

	global nodes

	score = evaluate(board)
	if empty_square(board) or depth == 0:
		return score
	elif score == 10:
		return score + count_empty_squares(board)
	elif score == -10:
		return score - count_empty_squares(board)
	
	if isMax:
		best = -1000
		for b in range(3):
			for row in range(3):
				for column in range(3):
					if board[b][row][column] == " ":
						board[b][row][column] = computer
						nodes += 1
						score_board = minimax(board, depth-1, not isMax, alpha, beta)
						best = max(best, score_board)
						board[b][row][column] = " "
						alpha = max(alpha, score_board)
						if alpha <= beta:
								break
	
	else:
		best = 1000
		for b in range(3):
			for row in range(3):
				for column in range(3):
					if board[b][row][column] == " ":
						board[b][row][column] = player
						nodes += 1
						score_board = minimax(board, depth-1, not isMax, alpha, beta)
						best = min(best, score_board)
						board[b][row][column] = " "
						beta = min(beta, score_board)
						if beta <= alpha:
								break
	return best

def best_move(board):
	#accessing nodes variable in multiple function
	global nodes
	nodes = 0
	best_val = -1000
	best_move = (-1,-1)
	start = time.time()
	for b in range(3):
		for row in range(3):
			for column in range(3):
				if board[b][row][column] == " ":
					#current nodes, subtract nodes from current nodes
					cur_nodes = nodes
					cur_time = time.time()
					board[b][row][column] = computer
					#depth = 5, as you can't search  
					move_val = minimax(board, 4, False, -100000, 100000)
					print(f"Board {b} | Move: {row}, {column} | Time Taken: {(time.time() - cur_time):.4f} | Nodes searched: {nodes - cur_nodes}")
					board[b][row][column] = " "
					if move_val > best_val:
						best_val = move_val
						best_move = (b, row, column)
	print(f"Time Taken: {time.time() - start} | Nodes searched: {nodes}")
	return best_move


computer, player = "X", "O"

grid = [[
[" ", " ", " "],
[" ", " ", " "],
[" ", " ", " "]
],
[[" ", " ", " "],
[" ", " ", " "],
[" ", " ", " "]
],
[[" ", " ", " "],
[" ", " ", " "],
[" ", " ", " "]
]]
computer_turn = False
print_board(grid)
while True:
	if computer_turn:
		make_move(grid, computer_turn)
		score = evaluate(grid)
		print_board(grid)
		computer_turn = False
	else:
		make_move(grid, computer_turn)
		score = evaluate(grid)
		print_board(grid)
		computer_turn = True
	if score == 10:
		print("Crosses won")
		break
	elif score == -10:
		print("Noughts won")
		break
	elif count_empty_squares(grid) == 0:
		print("Draw")
		break
