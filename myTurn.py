from chezz import *
from values import *

SEARCH_DEPTH = 3
TURN_FLIPPER = { "w" : "b", "b" : "w" }

def pieceValueHeuristic( board, turn ):
    value = 0
    for l, v in board.items():
        value += PIECE_VALUES[v[1]] * (1 if v[0] == turn else -1)
        
    return value

def pieceValueAndSquaresHeuristic( board, turn ):
    value = 0
    for l, v in board.items():
        value += (PIECE_VALUES[v[1]] + PIECE_TABLES[v][l[1]][l[0]]) * (1 if v[0] == turn else -1)
        
    return value

def heuristic( currentState, turn, depth = 0 ):
    return pieceValueAndSquaresHeuristic(currentState, turn) * (depth + 1)/10    

def minimax():
    board, turn, i1, i2, i3 = readBoard()
    
    # printBoard(board)
    bestScore = -999999999999999
    bestMove = {}
    path = []
    
    bestScore, bestMove, path = max_score(board, turn, SEARCH_DEPTH)

    # print("---------------")
    # pathTurn = turn
    # for n in path:
    #     print("TURN:", pathTurn)
    #     printBoard(n)
    #     print("Score:", heuristic(n, pathTurn, 2))
    #     print(" ")
    #     pathTurn = TURN_FLIPPER[pathTurn]
        
    # printBoard(bestMove)
    # print("score:", bestScore)
    
    # outputBoard(bestMove, "turn.txt", turn, "0", "0", "0")
    outputBoard_print(bestMove, turn, "0", "0", "0")    


def max_score(currentState, turn, depth, alpha=-1000000000, beta=1000000000):
    if depth == 0:
        return heuristic( currentState, turn, depth ), None, []
    
    bestScore = -1000000000
    bestMove = {}
    successors = getNextMoves((currentState, turn))
    bestPath = []
    
    if len(successors) == 0:
        return heuristic( currentState, turn, depth ), None, []

    for nextState in successors:
        score, _, path = min_score(nextState, turn, depth-1, alpha, beta)
        
        if score > bestScore:
            bestScore = score
            bestMove = nextState
            bestPath = path + [bestMove]
            
        alpha = max(alpha, bestScore)
        
        if bestScore >= beta:
            break
        
    return bestScore, bestMove, bestPath


def min_score(currentState, turn, depth, alpha, beta):
    if depth == 0:
        return heuristic( currentState, turn, depth ), None, []
    
    worstScore = 1000000000
    worstMove = {}
    successors = getNextMoves((currentState, TURN_FLIPPER[turn]))
    worstPath = []
    
    if len(successors) == 0:
        return heuristic( currentState, turn, depth ), None, []
    
    for nextState in successors:
        score, _, path = max_score(nextState, turn, depth-1, alpha, beta)
        
        if score < worstScore:
            worstScore = score
            worstMove = nextState
            worstPath = path + [worstMove]
            
        beta = min(beta, score)
        
        if worstScore <= alpha:
            break
        
    return worstScore, worstMove, worstPath


minimax()
