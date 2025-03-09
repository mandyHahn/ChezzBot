import copy

#################################
#       PIECE DEFINITIONS       #
#################################

def movePeon(piece, loc, board):
    # print("movePeon", loc)
    moves = []
    dir = 1 if piece[0] == "w" else -1
    
    newLoc = list(copy.copy(loc))
    newLoc[1] += dir 	# TODO: make sure no issues with copy	
    
    # can't move at all if on an edge
    if not (0 <= newLoc[1] <= 7):
        return []
 
    # if nothing ahead of Peon, moving forward is valid
    moves += tryMovePiece(piece, loc, board, 0, dir, False)
        
    # try to capture ahead to the left
    if newLoc[0] > 0:
        newLoc[0] -= 1
        tNL = tuple(newLoc)
        if tNL in board and board.get(tNL)[0] != piece[0]:
            moves.append(movePiece(piece, loc, newLoc, board))
            
        newLoc[0] += 1 # undo the operation

    # try to capture ahead to the left
    # TODO: hardcoding board size
    if newLoc[0] < 7:
        newLoc[0] += 1
        tNL = tuple(newLoc)
        if tNL in board and board.get(tNL)[0] != piece[0]:
            moves.append(movePiece(piece, loc, newLoc, board))

    return moves


def moveFlinger(piece, loc, board):
    # print("moveFlinger", loc)
    moves = []
    looper = range(8)
    
    for dir in [[0, 1], (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
        flingedPos = (loc[0] + dir[0], loc[1] + dir[1])
        if flingedPos not in board or board[flingedPos][0] != piece[0]:
            continue
        
        flingedPiece = board[flingedPos]
        
        x = loc[0]
        y = loc[1]
        
        for _ in looper:
            # subtract to get the opposite direction
            x -= dir[0] 
            y -= dir[1]
            targetLoc = (x, y)

            if not ((0 <= x <= 7) and (0 <= y <= 7)):
                break

            if targetLoc in board:
                if (board[targetLoc][0] == flingedPiece[0] or board[targetLoc][1] == "K"):
                    continue
                
                newBoard = copy.copy(board)
                del newBoard[flingedPos]
                del newBoard[targetLoc]
                moves += [newBoard]
            else:   
                moves += [movePiece(flingedPiece, flingedPos, targetLoc, board)]

    moves += simpleMove(piece, loc, board, False, True)
    return moves

def moveKnight(piece, loc, board):
    # print("moveKnight", loc)
    moves = []

    moves += tryMovePiece(piece, loc, board, 1, 2, True) 
    moves += tryMovePiece(piece, loc, board, -1, 2, True) 

    moves += tryMovePiece(piece, loc, board, 2, 1, True) 
    moves += tryMovePiece(piece, loc, board, 2, -1, True) 

    moves += tryMovePiece(piece, loc, board, 1, -2, True) 
    moves += tryMovePiece(piece, loc, board, -1, -2, True) 

    moves += tryMovePiece(piece, loc, board, -2, 1, True) 
    moves += tryMovePiece(piece, loc, board, -2, -1, True) 

    return moves

def moveCannon(piece, loc, board): 
    # print("moveCannon", loc)
    moves = []
    looper = range(1, 8)
    
    # -x, -y
    validMove = False
    newBoard = copy.copy(board)
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] - i
        y = loc[1] - i

        if (x < 0) or (y < 0):
            break

        if (x, y) in board:
            validMove = True
            del newBoard[(x, y)]
            
    if validMove:
        moves += [newBoard]
        newBoard = copy.copy(board)
    
    # -x, +y
    validMove = False
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] - i
        y = loc[1] + i

        if (x < 0) or (y > 7):
            break

        if (x, y) in board:
            validMove = True
            del newBoard[(x, y)]
            
    if validMove:
        moves += [newBoard]
        newBoard = copy.copy(board)
        
    # +x, +y
    validMove = False
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] + i
        y = loc[1] + i

        if (x > 7) or (y > 7):
            break

        if (x, y) in board:
            validMove = True
            del newBoard[(x, y)]
            
    if validMove:
        moves += [newBoard]
        newBoard = copy.copy(board)
        
    # +x, -y
    validMove = False
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] + i
        y = loc[1] - i

        if (x > 7) or (y < 0):
            break

        if (x, y) in board:
            validMove = True
            del newBoard[(x, y)]

    if validMove:
        moves += [newBoard]

    moves += simpleMove(piece, loc, board, False)
    return moves

def moveQueen(piece, loc, board):
    # print("moveQueen", loc)
    return moveDiagonals(piece, loc, board) + moveOrtho(piece, loc, board)

def moveKing(piece, loc, board):
    # print("moveKing", loc)    
    return simpleMove(piece, loc, board, diagonals = True)

def moveZombie(piece, loc, board):
    # print("moveZombie", loc)
    return simpleMove(piece, loc, board)

def moveBishop(piece, loc, board):
    # print("moveBishop", loc)
    return moveDiagonals(piece, loc, board)

def moveRook(piece, loc, board):
    # print("moveRook", loc)
    return moveOrtho(piece, loc, board)

####################################
#       POST MOVE OPERATIONS       #
####################################
IMMUNE_PIECES = ["K", "Z"]

def postMoveActions(board, colour):
    # perform contaigen
    newBoard = copy.copy(board)
    for k, v in newBoard.items():
        if v[1] != 'Z' or v[0] != colour:
            continue

        up = (k[0], k[1]+1)
        if up in newBoard and newBoard[up][0] != colour and newBoard[up][1] not in IMMUNE_PIECES:
            board[up] = colour + "Z"

        right = (k[0]+1, k[1])
        if right in newBoard and newBoard[right][0] != colour and newBoard[right][1] not in IMMUNE_PIECES:
            board[right] = colour + "Z"

        down = (k[0], k[1]-1)
        if down in newBoard and newBoard[down][0] != colour and newBoard[down][1] not in IMMUNE_PIECES:
            board[down] = colour + "Z"

        left = (k[0]-1, k[1])
        if left in newBoard and newBoard[left][0] != colour and newBoard[left][1] not in IMMUNE_PIECES:
            board[left] = colour + "Z"

    # perform promotions
    farSide = 7 if colour == "w" else 0
    for i in range(8):
        piece = board.get((i, farSide), None)
        if piece == None or piece[1] != 'P' or piece[0] != colour:
            continue

        board[(i, farSide)] = colour + "Z"


###############################
#       GENERIC HELPERS       #
###############################

def movePiece(piece, loc, newLoc, board): 
    newBoard = copy.copy(board) # TODO: make sure safe
    del newBoard[loc]
    newBoard[tuple(newLoc)] = piece
    return newBoard

# TODO: speed up by passing in newLoc
def tryMovePiece(piece, loc, board, x, y, canCapture):
    newLoc = list(copy.copy(loc))
    newLoc[1] += y
    newLoc[0] += x

    # TODO: make more efficient by reducing checks
    if (0 <= newLoc[0] <= 7) and (0 <= newLoc[1] <= 7):
        tNL = tuple(newLoc)
        if tNL not in board or (canCapture and board[tNL][0] != piece[0]):
            return [movePiece(piece, loc, newLoc, board)]
        
    return []


def simpleMove(piece, loc, board, canCapture = True, diagonals = False):
    moves = []

    moves += tryMovePiece(piece, loc, board, 0, 1, canCapture)
    moves += tryMovePiece(piece, loc, board, 0, -1, canCapture)
    moves += tryMovePiece(piece, loc, board, 1, 0, canCapture)
    moves += tryMovePiece(piece, loc, board, -1, 0, canCapture)

    if diagonals:
        moves += tryMovePiece(piece, loc, board, -1, 1, canCapture)
        moves += tryMovePiece(piece, loc, board, 1, 1, canCapture)
        moves += tryMovePiece(piece, loc, board, -1, -1, canCapture)
        moves += tryMovePiece(piece, loc, board, 1, -1, canCapture)

    return moves

def moveDiagonals(piece, loc, board):
    moves = []
    looper = range(1, 8)
    
    # -x, -y
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] - i
        y = loc[1] - i

        if (x < 0) or (y < 0):
            break

        moves += tryMovePiece(piece, loc, board, -i, -i, True)

        if (x, y) in board:
            break
    
    # -x, +y
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] - i
        y = loc[1] + i

        if (x < 0) or (y > 7):
            break

        moves += tryMovePiece(piece, loc, board, -i, +i, True)

        if (x, y) in board:
            break
    
    # +x, +y
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] + i
        y = loc[1] + i

        if (x > 7) or (y > 7):
            break

        moves += tryMovePiece(piece, loc, board, +i, +i, True)

        if (x, y) in board:
            break
    
    # +x, -y
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] + i
        y = loc[1] - i

        if (x > 7) or (y < 0):
            break

        moves += tryMovePiece(piece, loc, board, +i, -i, True)

        if (x, y) in board:
            break

    return moves


def moveOrtho(piece, loc, board):
    moves = []
    looper = range(1, 8)
    
    # -x
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] - i

        if (x < 0):
            break

        moves += tryMovePiece(piece, loc, board, -i, 0, True)

        if (x, loc[1]) in board:
            break
    
    # +y
    # TODO: Hardcoded
    for i in looper:
        y = loc[1] + i

        if (y > 7):
            break

        moves += tryMovePiece(piece, loc, board, 0, +i, True)

        if (loc[0], y) in board:
            break
    
    # +x
    # TODO: Hardcoded
    for i in looper:
        x = loc[0] + i

        if (x > 7):
            break

        moves += tryMovePiece(piece, loc, board, +i, 0, True)

        if (x, loc[1]) in board:
            break
    
    # -y
    # TODO: Hardcoded
    for i in looper:
        y = loc[1] - i

        if (y < 0):
            break

        moves += tryMovePiece(piece, loc, board, 0, -i, True)

        if (loc[0], y) in board:
            break

    return moves
