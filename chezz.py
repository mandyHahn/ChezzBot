from pieceMovement import *
import sys, os


a8=(0,7); b8=(1,7); c8=(2,7); d8=(3,7); e8=(4,7); f8=(5,7); g8=(6,7); h8=(7,7);
a7=(0,6); b7=(1,6); c7=(2,6); d7=(3,6); e7=(4,6); f7=(5,6); g7=(6,6); h7=(7,6);
a6=(0,5); b6=(1,5); c6=(2,5); d6=(3,5); e6=(4,5); f6=(5,5); g6=(6,5); h6=(7,5);
a5=(0,4); b5=(1,4); c5=(2,4); d5=(3,4); e5=(4,4); f5=(5,4); g5=(6,4); h5=(7,4);
a4=(0,3); b4=(1,3); c4=(2,3); d4=(3,3); e4=(4,3); f4=(5,3); g4=(6,3); h4=(7,3);
a3=(0,2); b3=(1,2); c3=(2,2); d3=(3,2); e3=(4,2); f3=(5,2); g3=(6,2); h3=(7,2);
a2=(0,1); b2=(1,1); c2=(2,1); d2=(3,1); e2=(4,1); f2=(5,1); g2=(6,1); h2=(7,1);
a1=(0,0); b1=(1,0); c1=(2,0); d1=(3,0); e1=(4,0); f1=(5,0); g1=(6,0); h1=(7,0);

POS_TO_COORD = {
    (0,7) : "a8", (1,7) : "b8", (2,7) : "c8", (3,7) : "d8", (4,7) : "e8", (5,7) : "f8", (6,7) : "g8", (7,7) : "h8",
    (0,6) : "a7", (1,6) : "b7", (2,6) : "c7", (3,6) : "d7", (4,6) : "e7", (5,6) : "f7", (6,6) : "g7", (7,6) : "h7",
    (0,5) : "a6", (1,5) : "b6", (2,5) : "c6", (3,5) : "d6", (4,5) : "e6", (5,5) : "f6", (6,5) : "g6", (7,5) : "h6",
    (0,4) : "a5", (1,4) : "b5", (2,4) : "c5", (3,4) : "d5", (4,4) : "e5", (5,4) : "f5", (6,4) : "g5", (7,4) : "h5",
    (0,3) : "a4", (1,3) : "b4", (2,3) : "c4", (3,3) : "d4", (4,3) : "e4", (5,3) : "f4", (6,3) : "g4", (7,3) : "h4",
    (0,2) : "a3", (1,2) : "b3", (2,2) : "c3", (3,2) : "d3", (4,2) : "e3", (5,2) : "f3", (6,2) : "g3", (7,2) : "h3",
    (0,1) : "a2", (1,1) : "b2", (2,1) : "c2", (3,1) : "d2", (4,1) : "e2", (5,1) : "f2", (6,1) : "g2", (7,1) : "h2",
    (0,0) : "a1", (1,0) : "b1", (2,0) : "c1", (3,0) : "d1", (4,0) : "e1", (5,0) : "f1", (6,0) : "g1", (7,0) : "h1",    
}

PIECE_MOVES = {"P" : movePeon, "F" : moveFlinger, "N" : moveKnight, "C" : moveCannon, 
               "Q" : moveQueen, "K" : moveKing, "Z" : moveZombie, "B" : moveBishop, "R" : moveRook}

OUTPUT_DIR = "out/"
BOARD_SIZE = 8
EMPTY_SQUARE = '  '
COLUMN_LABELS = "     a    b    c    d    e    f    g    h"

def printBoard(boardContents):
    board = [[EMPTY_SQUARE]*(BOARD_SIZE+1) for _ in range(BOARD_SIZE)]
    
    for i in range(BOARD_SIZE):
        board[i][0] = str(BOARD_SIZE - i) + " "
            
    for k, v in boardContents.items():
        board[BOARD_SIZE - k[1] -1][k[0]+1] = v
        
    boardStr = '\n   +----+----+----+----+----+----+----+----\n'.join(map(lambda x: " | ".join(x), board))
    
    print(COLUMN_LABELS)
    print("   +----+----+----+----+----+----+----+----")
    print(boardStr)


def outputBoard(board, file, turn, i1, i2, i3):
    nextTurn = "w" if turn == "b" else "b"
    with open(file, "w") as f:
        f.write(f"{nextTurn} {i1} {i2} {i3}\n")
        f.write("{\n")
        for k, v in board.items():
            f.write(f"  {POS_TO_COORD[k]}: '{v}',\n")
            
        f.write("}\n")
        f.write("0 0 0\n")

def outputBoard_print(board, turn, i1, i2, i3):
    nextTurn = "w" if turn == "b" else "b"
    print(f"{nextTurn} {i1} {i2} {i3}")
    print("{")
    for k, v in board.items():
        print(f"  {POS_TO_COORD[k]}: '{v}',")
        
    print("}")
    
def readBoard():
    turn, i1, i2, i3 = sys.stdin.readline().split()
    contents = "".join(sys.stdin.readlines())
    contents = contents[:(contents.rindex("}")+1)]
    board = eval( contents )
    
    return board, turn, i1, i2, i3


def outputNextMoves(outputDir, verbose = False):
    board, turn, i1, i2, i3 = readBoard()
    
    if verbose:
        print("Starting state")
        printBoard(boardContents=board)
        print("\n")
    
    resultingBoards = []
    
    # loop through pieces on the board
    for loc, piece in board.items():
        if piece[0] == turn:
            resultingBoards += PIECE_MOVES[piece[1]](piece, loc, board)

    n = 0
    for move in resultingBoards:
        postMoveActions(move, turn)
        
        fileName = "board." + "{:03d}".format(n)
        outputBoard(move, outputDir + fileName, turn, i1, i2, i3)
        
        n += 1
        if verbose:
            print("Solution", n)
            printBoard(move)
            print('\n')
            
def getNextMoves(turnInfo, verbose = False):
    board = turnInfo[0]
    turn = turnInfo[1]
    
    if verbose:
        print("Starting state")
        printBoard(boardContents=board)
        print("\n")
    
    resultingBoards = []
    kingAlive = False
    
    # loop through pieces on the board
    for loc, piece in board.items():
        if piece[0] == turn:
            resultingBoards += PIECE_MOVES[piece[1]](piece, loc, board)
            
            if piece[1] == "K": kingAlive = True

    if not kingAlive:
        return []
    
    n = 0
    for move in resultingBoards:
        postMoveActions(move, turn)
        
        n += 1
        if verbose:
            print("Solution", n)
            printBoard(move)
            print('\n')
            
    return resultingBoards
  
          
# outputDir = OUTPUT_DIR if len(sys.argv) < 2 else sys.argv[1]

# if not os.path.exists(outputDir):
#     os.mkdir(outputDir)

# outputNextMoves(outputDir, True)

# outputNextMoves("", False)