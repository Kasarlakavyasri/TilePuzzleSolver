#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
import numpy as np
import copy
import heapq
import math
ROWS=5
COLS=5
def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


def move_right(board, row):
  """Move the given row to one position right"""
  board[row] = board[row][-1:] + board[row][:-1]
  return board

def move_left(board, row):
  """Move the given row to one position left"""
  board[row] = board[row][1:] + board[row][:1]
  return board



def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    """Move the outer ring clockwise"""
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_cclockwise(board):
    """Move the outer ring counter-clockwise"""
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def extract_inner_mat(board):
    rows, cols = 3,3
    inner_matrix = [([0]*cols) for i in range(rows)]
    for i in range(0,3):
        for j in range(0,3):
            inner_matrix[i][j]=board[i+1][j+1]
    return inner_matrix

def rotate_inner_clock(board):
    inner_mat=extract_inner_mat(copy.deepcopy(board))
    inner_mat=move_clockwise(copy.deepcopy(inner_mat))
    replace_inner_mat(inner_mat,board)
    return board

def rotate_inner_cclock(board):
    inner_mat=extract_inner_mat(copy.deepcopy(board))
    inner_mat=move_cclockwise(copy.deepcopy(inner_mat))
    replace_inner_mat(inner_mat,board)
    return board

def replace_inner_mat(inner_matrix,board):
    for i in range(1,4):
        for j in range(1,4):
            board[i][j]=inner_matrix[i-1][j-1]
    return board

def transpose_board(board):
  """Transpose the board --> change row to column"""
  return [list(col) for col in zip(*board)]

# return a list of possible successor states
def successors(state):
        #print(instance)
        states=[]
        for r in range(ROWS):
            states.append((move_right(copy.deepcopy(state), r), "R"+str(r+1)))
        for r in range(ROWS):
            states.append((move_left(copy.deepcopy(state), r),"L"+str(r+1)))
        col_mat=copy.deepcopy(state)
        col_mat=transpose_board(col_mat)
        for r in range(ROWS):
            states.append((transpose_board(move_right(copy.deepcopy(col_mat), r)),"D"+str(r+1)))
            #print(transpose_board(move_right(copy.deepcopy(col_mat), r)))
        for r in range(ROWS):
            states.append((transpose_board(move_left(copy.deepcopy(col_mat), r)),"U"+str(r+1)))
            #print(transpose_board(move_left(copy.deepcopy(col_mat), r)))
        
        states.append((move_clockwise(copy.deepcopy(state)),"Oc"))
        states.append((move_cclockwise(copy.deepcopy(state)),"Occ"))
        states.append((rotate_inner_clock(copy.deepcopy(state)),"Ic"))
        states.append((rotate_inner_cclock(copy.deepcopy(state)),"Icc"))
        return states
        


# check if we've reached the goal
def is_goal(state):
    state=flatten(state)
    goal=list(range(1, 26))
    for i,j in zip(state,goal):
        if i!=j:
            return False
    return True



def original_dist(val):
    x1 = 999
    y1 = 999
    goal = []
    dataList=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    for i in range(ROWS):
        rowList = []
        for j in range(COLS):
            rowList.append(dataList[ROWS * i + j])
        goal.append(rowList)
    distance=0
    for i in range(ROWS):
        for j in range(COLS):
            if goal[i][j]==val:
                x1 = i
                y1 = j
                break
    return x1, y1


     
def h(initial_state):
    inits = initial_state.copy()
    x1 = y1 = x2 = y2 = 999
    total_h = 0
    
    for i in range(ROWS):
        for j in range(COLS):
            x1, y1 = original_dist(inits[i][j])
            x2, y2 = i, j
            total_h += math.sqrt(abs(x1-x2)**2+abs(y1-y2)**2)
    return total_h

def flatten(state):
    flat = np.array(state).flatten()
    return flat

def convert_to_2d(state):
    list_of_lists = []
    i=0
    for row in range(0,5):
        inner_list = []
        for col in range(0,5):
            inner_list.append(state[i])
            i+=1
        list_of_lists.append(inner_list)
    return list_of_lists



def  solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    initial_board=convert_to_2d(initial_board)
    initial_cost=h(initial_board)
    fringe=[(initial_cost,initial_board,[])]
    visited=[]
    fringe_1d=[tuple(flatten(initial_board))]
    
    heapq.heapify(fringe)
    path=[]
    
    while fringe:
        (curr_dist,curr_state ,path)=heapq.heappop(fringe)
        flat_curr_state=flatten(curr_state)
        if is_goal(curr_state):
            return curr_state,path
        if tuple(flat_curr_state) in visited:
            continue
        else: 
            visited.append(tuple(flat_curr_state))
            for next_state,next_step in successors(curr_state):
                cost=h(next_state)
                if(cost<initial_cost):
                    heapq.heappush(fringe,(cost,next_state,path+[next_step]))
                
    
                            



# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))
 
    print("Solving...")
    route = solve(tuple(start_state))
    #print(h(start_state))


    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
