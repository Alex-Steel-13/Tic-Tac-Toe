import random
import os
import time
clear = lambda: os.system('clear')

class Grid:
  def __init__(self):
    #This grid has 3 3lements in the list which are the rows
    self.grid = [[" "," "," ",], [" "," "," ",], [" "," "," ",]]
    self.cross_turn = False
    self.naught_turn = True
  def win_checker(self):
    #first for loop checks whether there is a horizontal line of 3. 0 means naught wins, 1 means crosses wins
    for i in range(3):
      if self.grid[i] == ["X", "X", "X"]:
        return 1
      elif self.grid[i] == ["O", "O", "O"]:
        return 0
    #Checks for the 3 in a row in the columns. i is the column number, and x is the row number
    for i in range(3):
      column_score = 0
      for x in range(3):
        if self.grid[x][i] == ["X"]:
          column_score +=1
        elif self.grid[x][i] == ["O"]:
          column_score +=2
        else:
          column_score += 100
      #If there are 3 crosses, then column_score is 3, and if there are 3 naughts, then it is 6, and if nothing is in a square, it adds 100 so that it won't be any of those
      if column_score == 3:
        return 1
      elif column_score == 6:
        return 0
    #diagonal checker, couldn't think of a way to do it with for loops so just hard programmed it
    if self.grid[0][0] == "X" and self.grid[1][1] == "X" and self.grid[2][2] == "X":
      return 1
    elif self.grid[0][0] == "O" and self.grid[1][1] == "O" and self.grid[2][2] == "O":  
      return 0
    elif self.grid[0][2] == "O" and self.grid[1][1] == "O" and self.grid[2][0] == "O":  
      return 0
    elif self.grid[0][2] == "X" and self.grid[1][1] == "X" and self.grid[2][0] == "X":
      return 1
  
  def print_grid(self):
    for i in range(3):
      if i != 2:
        print(*self.grid[i], sep='|')
        print('-+-+-')
      else:
        print(*self.grid[i], sep='|') 
  #input from number in main.py and decides who goes first
  def first_turn(self, cross):
    if cross == True:
      self.cross_turn = True
    else:
      self.naught_turn = True
  def end_turn(self):
    if self.cross_turn:
      self.cross_turn = False
      self.naught_turn = True
    else:
      self.cross_turn = True
      self.naught_turn = False

class Player:
  def __init__(self, type, name):
    #if type = True, then the player is a cross
    self.crosses = type
    self.name = name
  def move(self, grid):
    #loops if move is invalid
     while True: 
      #Get the user to select the square they are changing
      row = int(input("Choose which row you are entering in\n"))
      while row != 1 and row != 2 and row != 3:
        row = int(input("Now choose the row you are entering, 1 for the first row, 2 for the second row, 3 for the 3rd row\n"))
      column = int(input("Choose which column you are entering in\n"))
      while column != 1 and column != 2 and column != 3:
        column = int(input("Now choose the column you are entering, 1 for the first column, 2 for the second column, 3 for the 3rd column\n"))
      if grid[row-1][column-1] != "X" and grid[row-1][column-1] != "O":
        if self.crosses == True:
          grid[row-1][column-1] = "X"
          break
        else:
          grid[row-1][column-1] = "O"
          break
#creates the grid
grid = Grid()
#creates the 2 players
naught = Player(False, input("Enter the name of the person playing as naughts"))
cross = Player(True, input("Enter the name of the person playing as crosses"))
#If number is 1, then crosses go first, and pass through True into the first turn method in grid
turn = 0
number = random.randint(1,3)
if number == 1:
  first = True
else:
  first = False
while True:
  turn+=1
  if turn == 10:
    print("It was a draw")
    break
  time.sleep(1)
  clear()
  #checks which turn
  if grid.naught_turn:
    print(f"It is {naught.name}'s turn")
    grid.print_grid()
    naught.move(grid.grid)
    grid.end_turn()
  else:
    print(f"It is {cross.name}'s turn")
    grid.print_grid()
    cross.move(grid.grid)
    grid.end_turn()
  win = grid.win_checker()
  if win == 1:
    print("crosses won")
    grid.print_grid()
    break
  elif win == 0:
    print("naughts won")
    grid.print_grid()
    break
  grid.print_grid()