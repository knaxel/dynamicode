from codigram.modules.modules import Module

MODULE_ID = "python_11"
NEXT_MODULE_ID = None

MODULE_DATA = {
    "title": "Project 1: Tic-Tac-Toe Game",
    "author": "Codigram",
    "author_uuid": "3473989f-0e1f-4488-9e98-847da1969d41",
    "sandbox_uuid": "b9a39b5a-d652-4ff2-aaaa-cd6abcd0142d",
    "date_created": "Aug 02, 2021 09:44 PM",
    "blocks": [
        {
            "name": "Project Explanation",
            "text": "In this project, you will be making a tic-tac-toe game for two human players. In the code window, you will see that you have been given some variables and empty functions that you should complete. Do not modify the parameters of the functions. Here are some test cases that your project should be able to complete exactly in order to complete this module. Not all possible test cases are listed - some are hidden but must still be passed to complete this project.\n***\n`printBoard()` function: This function should print the state of the board when it is called. A board may look like this:    \n    X O -    \n    O X -    \n    - - O    \nUnused squares are represented by dashes. Player 1 should use X’s and player 2 should use O’s. There is a space between each square. This function should not return anything.\n***\n`assignSquare()` function: This function takes in two arguments - the player number and the square chosen - and assigns a value to a square assuming the space has not yet been filled. This function should not return anything. Remember that a player can only choose one of the nine squares, and the board is stored as a list with items indexed 0 through 8.    \n***\nInput: (1,1)    \nOutput (if first square is square 1):    \n    X - -    \n    - - -    \n    - - -    \nAlternative Output (if first square is square 0):    \n    - X -    \n    - - -    \n    - - -   \n***\nInput: (3,1)    \nOutput: Error, player number not valid   \n***   \nInput: (1,20)    \nOutput: Error, square does not exist    \n***\n`winDetection()` function: This function takes in one argument - the board list - and returns a true or false value depending on if the player that has most recently taken their turn has made a winning move. In order to win, a player must have three X’s or three O’s either in a horizontal, vertical, or diagonal line. Do not worry about determining if it is player 1 or player 2’s win - this is handled by the main function.   \n***\nInput:     \n    O X -  \n    - X O  \n    - X -  \nOutput: True\n***\n`main()` function: This function handles actually running the game. All function calls are made from the `main()` function. Take a look at it to understand the gameplay and how the functions you need to complete are being used.",
            "type": "TextBlock"
        },
        {
            "name": "Tic-Tac-Toe Project",
            "code": "board = [\"-\",\"-\",\"-\",\"-\",\"-\",\"-\",\"-\",\"-\",\"-\"]\n\n# Outputs the current board state. Complete this function.\n# Sample output: \n# X O -\n# O X -\n# - - O\ndef printBoard():  \n\tpass\n\n# Changes an open square based on player input. The function takes a player ID and chosen square as input. Complete this function.\ndef assignSquare(player, square): \n\tpass\n\n# Detects if a player has won following their turn. The function takes a board state as input. Complete this function.\ndef winDetection(inputBoard): \n\tpass\n\n# Main function. This code will manage starting and running a game between two human players.\ndef main(): \n  print(\"Starting new game\")\n  gameOver = False\n  movesMade = 0\n  winner = 0\n  # All code in this loop will run as long as no player has won or tied\n  while(not gameOver):\n\n    print(\"Player 1's turn\")\n    square = input(\"Choose a square: \") # Player inputs a value 1 - 9 to choose a square\n    assignSquare(1,int(square)-1) # Assign X or O to square\n    movesMade+=1\n    if(winDetection(board) or movesMade==9):\n      gameOver = True\n      winner = 1 # Set winner to player 1\n      break # Exit loop\n\n    printBoard() # Print updated board state\n\n    print(\"Player 2's turn: \")\n    square = input(\"Choose a square: \")\n    assignSquare(2,int(square)-1)\n    movesMade+=1\n    if(winDetection(board)):\n      gameOver = True\n      winner = 2\n      break\n\n    printBoard() # Print updated board state\n\n  print(\"Game over!\")\n  if(movesMade==9):\n    print(\"Tie!\")\n  else:\n    print(\"Winner: Player \" + winner)\n  print()\n\nif __name__ == \"__main__\":\n    main()",
            "type": "CodeBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
