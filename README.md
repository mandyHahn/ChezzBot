# Chezz Bot: RRBCZB
Created by: Amanda Hahn

## Introduction
RRBCZB is a "chezz" bot created for Assignmenet 4 of my Introduction to Intelligent Systems course at the University of Guelph (CIS\*3700). RRBCZB is the top performing bot of the Winter 2025 CIS\*3700 class. 

## What is Chezz?
Chezz is a custom variant of Chess created by Professor Kremer for his Intro to Intelligent Systems course. Chezz adds three new pieces to the classic game of Chess:
- The Flinger (a.k.a. catapult) (F) – Moves like a king but cannot capture. Instead, it can fling an adjacent friendly piece in a straight line over itself, continuing in that direction any distance. The flung piece can land on an empty square or capture an enemy piece (but is destroyed in the process).
- The Cannon (C) - Moves like a one-step Rook, but cannot capture. Instead, it can fire a cannonball one of the four diagonal directions, capturing all pieces along that diagonal (friend and foe alike)
- The Zombie (Z) - Moves like a one-step Rook, it can capture. At the end of the current player's turn, any enemy pieces orthogonally adjacent to the zombie turn into player zombies (change colour)

And a few additional rules:
- Pieces "flung" by the flinger cannot capture a King
- The Cannon cannot fire a cannonball that doesn't hit any pieces
- Enemy Zombies and The King cannot be converted into Zombies
- En passant and castling do not exist in Chezz
- "Checkmate" occurs when the opposing King is captured
- A player loses the game if they make an illegal move
- A player loses the game if they run out of time

## How it works
RRBCZB makes decisions on what the best next move is using the [minimax algorithm](https://en.wikipedia.org/wiki/Minimax) with a search depth of three. A custom heuristic has been written which takes into account piece values and locations in order to determine the "strength" of each board state. Each round, an input file is given via STDIN to the bot specifying the current player, time left, and board state. RRBCZB then generates the next board after applying it's best move, outputting it to STDOUT.  

To prevent infinite loops (where two bots continually make the same moves over and over without ever progressing the game), a check is performed using a Zobrist hash. Then, if the same board state has been seen twice before while searching for the next move it is skipped.

## Performance
RRBCZB came first in all three iterations of the class-wide tournament, with a >97% win rate over 350+ individual "Chezz" games.  
