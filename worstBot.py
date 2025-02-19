import sys

def moveToIndex(str):
    if (str == "h1" or str == "r0"):
        return [-1, -1]
    col = ord(str[0]) - 97
    row = 7 - int(str[1])
    if (row != 3):
        if (col < 3):
            col = 0
        elif (col > 3):
            col = 2
        else:
            col = 1
    else:
        if col > 3:
            col -= 1
    return [row, col]

def indexToMove(row, col):
    if (row == 3):
        if (col < 3):
            return chr(col + 97) + "4"
        else:
            return chr(col + 97 + 1) + "4"
    if (col == 1):
        return "d" + str(7 - row)
    if (col < 1):
        return chr(100 - abs(3 - row)) + str(7 - row)
    else:
        return chr(100 + abs(3 - row)) + str(7 - row)

def printBoard(board):
    for i in range(7):
        if (abs(3 - i) == 3):
            print("\t" + str(board[i][0]) + "\t" + "\t" + "\t" + str(board[i][1]) + "\t" + "\t" + "\t" + str(board[i][2]))
        elif (abs(3 - i) == 2):
            print("\t" + "\t" + str(board[i][0]) + "\t" + "\t" + str(board[i][1]) + "\t" + "\t" + str(board[i][2]) + "\t")
        elif (abs(3 - i) == 1):
            print("\t" + "\t" + "\t" + str(board[i][0]) + "\t" + str(board[i][1]) + "\t" + str(board[i][2]) + "\t" + "\t")
        else:
            print("\t" + str(board[i][0]) + "\t" +  str(board[i][1]) + "\t" +  str(board[i][2]) + "\t" + "\t" +  str(board[i][3]) + "\t" +  str(board[i][4]) + "\t" +  str(board[i][5]))

def main():
    board = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    printBoard(board)
    blue = True
    myTurn = False
    turns = 0
    game_input = input().strip()
    if game_input == "blue":
        myTurn = True
    elif game_input == "orange":
        myTurn = False
        blue = False
    else:
        print("Invalid input")
        sys.exit(1)
    while True:
        try:
            if (myTurn):
                if (blue):
                    print("h1 a4 r0", flush=True)
                else:
                    print("h2 b4 r0", flush=True)
                myTurn = False
                turns += 1
            
            else:
                move = input().strip()
                # modify the board
                myTurn = True
                turns += 1

        except EOFError:
            break

if __name__ == "__main__":
    main()