# Command Line Minesweeper

This repository contains a command line implementation of Minesweeper. This implementation follows the standard [rules](http://www.freeminesweeper.org/help/minehelpinstructions.html) of Minesweeper. 

The user navigates the board with their arrow keys. Tiles are checked with the 'c' key and are flagged with the 'f' key. Checking a tile which has already been revealed and has an approriate number of adjacant tiles flagged will reveal all surrounding tiles.
![Game](https://raw.githubusercontent.com/jacobinski/Minesweeper/assets/GameScreen.png)

## Requirements
The user must have **Python 3.x** installed on their computer. To start the game, simply run *main.py* using Python:

    python main.py

The following screen should be seen.
![Start](https://raw.githubusercontent.com/jacobinski/Minesweeper/assets/StartScreen.png)

## Future features
The following features will be implemented in the future
- Game over screen for losing the game
- Victory screen for winning the game
- Better icons for mines and flags
- Center the screen