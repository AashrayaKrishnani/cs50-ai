"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return O if sum(row.count(X) - row.count(O) for row in board) else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('Invalid Action Attempted: ' + str(action))

    # Manual Deep Copy
    copy = initial_state()
    crnt_player = player(board)
    
    for i in range(3):
        for j in range(3):
            if (i,j) == action:
                copy[i][j] = crnt_player    # Executing action.
            else:
                copy[i][j] = board[i][j]

    return copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking rows
    for row in board:
        player = row[0]
        winner = True
        for j in range(3):
            if row[j] != player or player==EMPTY:
                winner = False
                break
        if winner:
            return player

    # Checking columns
    for i in range(3):
        player = board[0][i]
        winner = True
        for j in range(3):
            if board[j][i] != player or player==EMPTY:
                winner = False
                break
        if winner:
            return player 

    # Checking Diagonals

    player = board[1][1]
    winner = False

    if player != EMPTY:
        if (board[0][0] == player and board[2][2] == player) or (board[0][2] == player and board[2][0] == player):
            winner = True
     
    return player if winner else None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) else (not sum(row.count(EMPTY) for row in board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    hasWon = winner(board)

    if hasWon == X:
        return 1
    elif hasWon == O:
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        isPlaying = player(board)
        canDo = actions(board)
        record = []

        for action in canDo:
            # Direct winning
            if winner(result(board, action)) == player:
                return action
            # Calculating best value for each case
            else:
                value = _poweredUpHelper(result(board, action))
                if value==1 and isPlaying==X:
                    return action
                elif value==-1 and isPlaying==O:
                    return action
                else:
                    record.append({"value": value, "action":action})

        # Choosing action leading to state with best value for the current player.
        handle = min if isPlaying==O else max
        best_val = record[0]["value"]
        best_action = record[0]["action"]
        for entry in record:
            if handle(best_val, entry["value"]) != best_val:
                best_val = entry["value"]
                best_action = entry["action"]

        return best_action
                    

def _helper(board):
    if terminal(board):
        return utility(board)
    else: 
        isPlaying = player(board)
        values = set()
        for action in actions(board):
            value = _helper(result(board,action))
            if (value==1 and isPlaying==X) or (value==-1 and isPlaying==O): # Tiny optimization.
                return value
            else:
                values.add(value)

        return min(value for value in values) if isPlaying==O else max(value for value in values)

# AlphaBeta Pruning enabled!
def _poweredUpHelper(board, alpha=None):
    if terminal(board):
        return utility(board)
    else: 
        beta = None
        isPlaying = player(board)
        handle = min if isPlaying==O else max
        handle_for_prev_player = max if isPlaying==O else min
        ans = handle(-1,1) * (-1)   # Worst case value initialization

        for action in actions(board):

            value = _poweredUpHelper(result(board,action), beta)
            ans = handle(ans, value)            
            
            if (value==1 and isPlaying==X) or (value==-1 and isPlaying==O): # Tiny optimization.
                return value
            elif alpha is not None and handle_for_prev_player(alpha, value)==alpha:        # The Alpha-Beta Pruning, 
                return value         # When we can't obtain better results from a subtree

            if beta is None:   # First sub node Checking and initializing Alpha-Value
                beta = value

        return ans
