from chezz import *

SEARCH_DEPTH = 2
TURN_FLIPPER = { "w" : "b", "b" : "w" }

PIECE_VALUES = { "P" : 1, "F" : 8, "C" : 8, "N" : 3, "B" : 3, "R" : 5, "Q" : 9, "Z" : 20, "K" : 10000 }


def pieceValueHeuristic( board, turn ):
    value = 0
    for _, v in board.items():
        value += PIECE_VALUES[v[1]] * (1 if v[0] == turn else -1)
        
    return value

def heuristic( currentState, turn ):
    return pieceValueHeuristic(currentState, turn)

def minimax():
    board, turn, i1, i2, i3 = readBoard()
    printBoard(board)
    bestScore, bestMove = max_score(board, turn, SEARCH_DEPTH)
    print("best score:", bestScore)
    printBoard(bestMove)

def max_score(currentState, turn, depth, alpha=-1000000000, beta=1000000000):
    if depth == 0:
        return heuristic( currentState, turn ), None
    
    bestScore = -1000000000
    bestMove = {}
    successors = getNextMoves((currentState, turn))
    
    print("--------------MAX--------------")
    for nextState in successors:
        score, _ = min_score(nextState, turn, depth-1, alpha, beta)
        printBoard(nextState)
        print("^^Score:", score)
        
        if score > bestScore:
            bestScore = score
            bestMove = nextState
            
        alpha = max(alpha, bestScore)
        
        if beta <= alpha:
            break
        
            
    return bestScore, bestMove


def min_score(currentState, turn, depth, alpha, beta):
    if depth == 0:
        return heuristic( currentState, turn ), None
    
    worstScore = 1000000000
    worstMove = {}
    successors = getNextMoves((currentState, TURN_FLIPPER[turn]))
    print(len(successors), turn)
    
    print("--------------MIN--------------")
    for nextState in successors:
        score, _ = max_score(nextState, turn, depth-1, alpha, beta)
        printBoard(nextState)
        print("^^Score:", score)
        
        if score < worstScore:
            worstScore = score
            worstMove = nextState
            
        beta = min(beta, score)
        
        if beta <= alpha:
            break
        
        
    return worstScore, worstMove

minimax()


# def max_score(currentState, depth):
#     if depth == 0:
#         return heuristic(currentState), None
    
#     bestScore = -1000000000
#     bestMove = ""
#     successors = getNextMoves()
    
#     for nextState in successors:
#         score = min_score(nextState, depth-1)
#         if score > bestScore:
#             bestScore = score
#             bestMove = nextState
            
#     return bestScore, bestMove


# def min_score(currentState, depth):
#     if depth == 0:
#         return heuristic(currentState), None
    
#     worstScore = 1000000000
#     worstMove = ""
#     successors = getNextMoves()
    
#     for nextState in successors:
#         score = max_score(nextState, depth-1)
#         if score < worstScore:
#             worstScore = score
#             worstMove = nextState
            
#     return worstScore, worstMove