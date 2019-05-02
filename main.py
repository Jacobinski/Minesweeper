import curses
from game import Minesweeper 


# Window Constants
WIN_HEIGHT_OFFSET = 5

# Board Constants
NUM_ROWS = 20
NUM_COLS = 40
NUM_MINES = 100

# Display Constants
STR_COVERED = 'x'
STR_MINE = '*'
STR_FLAG = '!'

# Curses Color Pair Constants
PAIR_MINE = 10
PAIR_FLAG = 11

# Splash Screen
LOGO = r"""
        _                                                   
  /\/\ (_)_ __   ___  _____      _____  ___ _ __   ___ _ __ 
 /    \| | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
/ /\/\ \ | | | |  __/\__ \\ V  V /  __/  __/ |_) |  __/ |   
\/    \/_|_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|   
                                           |_|              
    
                  Created by: Jacob Budzis
                  Updated:    May 2, 2019

                  Controls
                   f: Flag a location as a mine
                   c: Check the covered location
                   e: Exit the game

                  PRESS ANY KEY TO CONTINUE

"""

def debug_str( string, win ):
    win.addstr( 25, 25, "                                                      ")
    win.refresh()

    win.addstr( 25, 25, string ) 
    win.refresh()

def isValidCoordinate(x, y):
    return ( x >= 0 ) and ( y >= 0 ) and ( x < NUM_COLS ) and ( y < NUM_ROWS ) 

def countSurroundingFlags(x, y, win):
    count = 0

    for xi in [x-1, x, x+1]:
        for yi in [y-1, y, y+1]:
            if (xi == x and yi == y) or not isValidCoordinate(xi, yi):
                continue
            if chr(win.inch(yi,xi) & 0xff) == STR_FLAG:
                count += 1

    return count

def revealSurrounding(x, y, win, game):
    for xi in [x-1, x, x+1]:
        for yi in [y-1, y, y+1]:
            c = chr(win.inch(yi, xi) & 0xff)   
            if c != STR_FLAG:
                revealTile(xi, yi, win, game)

def revealTile(x, y, win, game):
    if not isValidCoordinate(x, y) or (win.inch(y,x) & 0xff) == ord(' '):
        return
    
    val = game.getValue(y, x)

    # CASE: No mines surrounding tile. Flood reveal the board
    if val == 0:
        win.addstr(' ')
 
        # Recurse on all surrounding tiles
        for xi in [x-1, x, x+1]:
            for yi in [y-1, y, y+1]:
                revealTile(xi, yi, win, game)
    
    # CASE: Tile contains mine
    elif game.containsMine(y, x):
        win.addstr(STR_MINE, curses.color_pair(PAIR_MINE))
    
    else:
        win.addstr(str(val), curses.color_pair(val))
    
    win.refresh()

def initialize_color_pairs():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(PAIR_MINE, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(PAIR_FLAG, curses.COLOR_BLACK, curses.COLOR_GREEN)

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Display the logo and wait for user input
    stdscr.addstr(LOGO)
    stdscr.refresh()
    stdscr.getch()
    
    # Initialize the game grid display
    stdscr.clear()
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            stdscr.addstr(y, x, STR_COVERED)
    stdscr.move(0,0)
    stdscr.refresh()

    # Initialize colors
    initialize_color_pairs()

    # Initialize the Minesweeper game
    minesweeper = Minesweeper(NUM_ROWS, NUM_COLS, NUM_MINES)

    # Run the game logic
    while True:
        c = stdscr.getch()
        (y, x) = stdscr.getyx()        

        # This is a good place for a switch statement!!!

        if c == ord('e'):
            break
        elif c == curses.KEY_LEFT:
            stdscr.move(y, max(x-1,0))
        elif c == curses.KEY_RIGHT:
            stdscr.move(y, min(x+1, NUM_COLS-1))
        elif c == curses.KEY_UP:
            stdscr.move(max(y-1,0), x)
        elif c == curses.KEY_DOWN:
            stdscr.move(min(y+1, NUM_ROWS-1), x)           
        elif c == ord('c'):
            # Check for double click on revealed tile which has proper number
            # of marked flags
            if ord('1') <= (stdscr.inch(y,x) & 0xff) <= ord('8') and str(countSurroundingFlags(x,y,stdscr)) == chr(stdscr.inch(y,x) & 0xff):
                revealSurrounding(x, y, stdscr, minesweeper)
            else:  
                revealTile(x, y, stdscr, minesweeper)
            
            # Avoid moving the cursor. There's probably a nicer way to do this
            stdscr.move(y, x)
            stdscr.refresh()
        elif c == ord('f'):
            stdscr.addstr(STR_FLAG, curses.color_pair(PAIR_FLAG))

            # Avoid moving the cursor.
            stdscr.move(y, x)
            stdscr.refresh()

if __name__ == "__main__":
    # Invoke wrapper, which initializes and cleans up curses
    curses.wrapper(main)
