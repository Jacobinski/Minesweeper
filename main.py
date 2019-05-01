import curses
from game import Minesweeper 


NUM_ROWS = 20
NUM_COLS = 40
NUM_MINES = 150
STR_COVERED = 'x'
STR_MINE = '*'

PAIR_MINE = 10
PAIR_FLAG = 11

def isValidCoordinate(x, y):
    return ( x >= 0 ) and ( y >= 0 ) and ( x < NUM_COLS ) and ( y < NUM_ROWS ) 

def revealTile(x, y, win, game):
    if not isValidCoordinate(x, y) or win.inch(y,x) == ord(' '):
        return
    
    val = game.getValue(y, x)
    if val == 0:
        win.addstr(' ')
        win.refresh()       
 
        # Recurse on all surrounding tiles
        for xi in [x-1, x, x+1]:
            for yi in [y-1, y, y+1]:
                revealTile(xi, yi, win, game)
    
    elif game.containsMine(y, x):
        win.addstr(STR_MINE, curses.color_pair(PAIR_MINE))
    else:
        win.addstr(str(val), curses.color_pair(val))
    
    win.refresh()

def main(stdscr):
    # Clear the screen
    stdscr.clear()
    
    # Initialize the display
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            stdscr.addstr(y, x, STR_COVERED)
    stdscr.move(0,0)
    stdscr.refresh()

    # Initialize colors
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

    # Initialize the Minesweeper game
    minesweeper = Minesweeper(NUM_ROWS, NUM_COLS, NUM_MINES)

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
            revealTile(x, y, stdscr, minesweeper)
            
            # Avoid moving the cursor. There's probably a nicer way to do this
            stdscr.move(y, x)
            stdscr.refresh()
        elif c == ord('f'):
            stdscr.addstr('f', curses.color_pair(PAIR_FLAG))

            # Avoid moving the cursor.
            stdscr.move(y, x)
            stdscr.refresh()

if __name__ == "__main__":
    # Invoke wrapper, which initializes and cleans up curses
    curses.wrapper(main)
