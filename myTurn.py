from chezz import *
from values import *
from zobrist import *

SEARCH_DEPTH = 3
TURN_FLIPPER = { "w" : "b", "b" : "w" }
MAX_TABLE_SIZE = 10000
# ZVALUES, ZTURN, ZTABLE = init_zobrist()

# things to try
# - piece tables
# - transposition tables
#


def pieceValueHeuristic( board, turn ):
    value = 0
    for l, v in board.items():
        # print(l, v, (PIECE_VALUES[v[1]]), (PIECE_TABLES[v[1]][v[0]][l[1]][l[0]]), (1 if v[0] == turn else -1))
        value += PIECE_VALUES[v[1]] * (1 if v[0] == turn else -1)
        
    return value

def pieceValueAndSquaresHeuristic( board, turn, verbose = False ):
    value = 0
    for l, v in board.items():
        # if verbose: print(l, v, (PIECE_VALUES[v[1]]), (PIECE_TABLES[v][l[1]][l[0]]), (1 if v[0] == turn else -1))
        value += (PIECE_VALUES[v[1]] + PIECE_TABLES[v][l[1]][l[0]]) * (1 if v[0] == turn else -1)
        
    return value

def heuristic( currentState, turn, depth = 0 ):
    return pieceValueAndSquaresHeuristic(currentState, turn) * (depth + 1)/10
    
    # return pieceValueHeuristic(currentState, turn)


# def minimax():
#     board, turn, i1, i2, i3 = readBoard()
#     # printBoard(board)
#     bestScore, bestMove, path = max_score(board, turn, SEARCH_DEPTH)
    
#     # for n in path:
#     #     printBoard(n)
#     #     print(" ")
    
    
#     printBoard(bestMove)
#     print("score:", bestScore)
    
#     outputBoard(bestMove, "turn.txt", turn, "0", "0", "0")

def minimax(verbose = False):
    board, turn, i1, i2, i3 = readBoard()
    
    # printBoard(board)
    bestScore = -999999999999999
    bestMove = {}
    path = []
    
    bestScore, bestMove, path = max_score(board, turn, SEARCH_DEPTH)
    
    # bestScore, bestMove, path = negamax_wrapper(board, turn)
    # if turn == "w":  
        # global ZVALUES, ZTURN, ZTABLE
        # ZVALUES, ZTURN, ZTABLE = init_zobrist()    
    #     bestScore, bestMove, path = negamax_wrapper(board, turn)
    # else:
    #     bestScore, bestMove, path = max_score(board, turn, SEARCH_DEPTH)
    
    if verbose:
        print("---------------")
        pathTurn = turn
        for n in path:
            pathTurn = TURN_FLIPPER[pathTurn]
            print("TURN:", pathTurn)
            printBoard(n)
            print("Score:", pieceValueAndSquaresHeuristic(n, pathTurn, True))
            print(" ")
            
        printBoard(bestMove)
        print("score:", bestScore)
    
    outputBoard_print(bestMove, turn, "0", "0", "0")    
    # outputBoard(bestMove, "turn.txt", turn, "0", "0", "0")

    

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





EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

def negamax_wrapper(currentState, turn):
    successors = getNextMoves((currentState, turn))
    bestMove = {}
    bestScore = -100000000000
    bestPath = []
    
    for move in successors:
        score, path = negamax(move, TURN_FLIPPER[turn], SEARCH_DEPTH-1)
        score = -score
        
        if score > bestScore:
            bestMove = move
            bestScore = score
            bestPath = path
        
    return bestScore, bestMove, bestPath



def negamax(currentState, turn, depth, alpha=-100000000000, beta=100000000000):    
    if depth == 0:
        return heuristic( currentState, turn ), []
    
    value = -100000000000
    successors = getNextMoves((currentState, turn))
    path = []
    
    if len(successors) == 0:
        return heuristic( currentState, turn ), []
    
    # remove_set = set(successors[0].items()) - set(currentState.items()) 
    # add_set = set(currentState.items()) - set(successors[0].items())
    # print("remove:", remove_set) 
    # print("add:", add_set) 
    
    for nextState in successors:
        score, oldPath = negamax(nextState, TURN_FLIPPER[turn], depth-1, -beta, -alpha)
        score = -score
        
        if score > value:
            value = score
            path = oldPath + [nextState]
            
        alpha = max(alpha, value)
        
        if alpha >= beta:
            break
            
    # print("--------------RESULT OF MINS--------------")
    # printBoard(bestMove)
    # print("^^Score:", bestScore)
    return value, path



def negamax_tt(currentState, turn, depth, alpha=-100000000000, beta=100000000000):
    alphaOrig = alpha
    
    hash = computeHash(currentState, turn, ZVALUES, ZTURN)
    ttEntry = ZTABLE.get(hash, None)
    if ttEntry != None and ttEntry["depth"] >= depth:
        if ttEntry["flag"] == EXACT:
            return ttEntry["value"], []
        elif ttEntry["flag"] == LOWERBOUND:
            alpha = max(alpha, ttEntry["value"])
        elif ttEntry["flag"] == UPPERBOUND:
            beta = min(beta, ttEntry["value"])
    
        if alpha >= beta:
            return ttEntry["value"], []
    
    elif ttEntry == None:
        ttEntry = {"value" : 0, "flag" : -1, "depth" : 0}
        
    
    if depth == 0:
        return heuristic( currentState, turn ), []
    
    value = -100000000000
    successors = getNextMoves((currentState, turn))
    path = []
    
    if len(successors) == 0:
        return heuristic( currentState, turn ), []
    
    # remove_set = set(successors[0].items()) - set(currentState.items()) 
    # add_set = set(currentState.items()) - set(successors[0].items())
    # print("remove:", remove_set) 
    # print("add:", add_set) 
    
    for nextState in successors:
        score, oldPath = negamax(nextState, TURN_FLIPPER[turn], depth-1, -beta, -alpha)
        score = -score
        
        if score > value:
            value = score
            path = oldPath + [nextState]
            
        alpha = max(alpha, value)
        
        if alpha >= beta:
            break
        
    ttEntry["value"] = value
    if value <= alphaOrig:
        ttEntry["flag"] = UPPERBOUND
    elif value >= beta:
        ttEntry["flag"] = LOWERBOUND
    else:
        ttEntry["flag"] = EXACT
        
    ttEntry["depth"] = depth
    ZTABLE[hash] = ttEntry
            
    # print("--------------RESULT OF MINS--------------")
    # printBoard(bestMove)
    # print("^^Score:", bestScore)
    return value, path



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