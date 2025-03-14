import numpy as np
from pathlib import Path


PIECE_LOCATIONS = {
    "wP" : 0,
    "wF" : 1,
    "wC" : 2,
    "wN" : 3,
    "wB" : 4,
    "wR" : 5,
    "wQ" : 6,
    "wZ" : 7,
    "wK" : 8,
    "bP" : 9,
    "bF" : 10,
    "bC" : 11,
    "bN" : 12,
    "bB" : 13,
    "bR" : 14,
    "bQ" : 15,
    "bZ" : 16,
    "bK" : 17,
}

ZOBRIST_FILE = "zinfo.txt"

def init_zobrist():
    
    my_file = Path(ZOBRIST_FILE)
    if not my_file.is_file():
        rng = np.random.default_rng()
        values = rng.integers(0, (2**63), size=(8, 8, 18))
        blackTurn = rng.integers(0, (2**63))
        return values, blackTurn, {}
    
    with open(ZOBRIST_FILE, "r") as file:
        allLines = file.readlines()
        valuesStr = "np." + "".join(allLines[:391])
        tableStr = "".join(allLines[392:])
        
        values = eval(valuesStr)
        blackTurn = int(allLines[391].strip())
        table = eval(tableStr)
        
        return values, blackTurn, table
        
        
        # loc = allLines.rindex("]]]")+1
        # zValues = exec(allLines[:loc])
        # zTurn = int(allLines[loc:loc+1])
        
        
def output_zobrist(zValues, zTurn, zTable):
    with open(ZOBRIST_FILE, "w") as output:
        with np.printoptions(threshold=np.inf):
            print(repr(zValues), file = output)
        
        print(zTurn, file = output)
        print(zTable, file = output)

 
def computeHash(board, turn, zTable, zTurn):
    h = 0
    for l, v in board.items():
        h ^= zTable[l[0]][l[1]][PIECE_LOCATIONS[v]]
        
    if turn == "b":
        h ^= zTurn
        
    return h

def updateHash(hash, edit, turn, zTable, zTurn):
    for pair in edit:
        hash ^= zTable[pair[0][0]][pair[0][1]][PIECE_LOCATIONS[pair[1]]]
        
    if turn == "b":
        hash ^= zTurn
        
    return hash
        
 
# testBoard = {
#   (5,3): 'wK',
#   (3,4): 'wP',
#   (4,5): 'bP',
# }

# resultBoard = {
#   (5,3): 'wK',
#   (3,4): 'bP',
# }
 
# edit_set = set(testBoard.items()) ^ set(resultBoard.items())  
 
# zTable = init_zobrist()
# hash = computeHash(testBoard, zTable)
# print(hash)
# edit = updateHash(hash, edit_set, zTable)
# print(edit)
# edit = updateHash(edit, edit_set, zTable)
# print(edit)
