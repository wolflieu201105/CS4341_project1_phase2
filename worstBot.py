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

def changeBoard(board, move, type):
    move = move.split(" ")
    if (move[0] != "h1" and move[0] != "h2"):
        moveUsed = moveToIndex(move[0])
        board[moveUsed[0]][moveUsed[1]] = 0
    moveUsed = moveToIndex(move[1])
    board[moveUsed[0]][moveUsed[1]] = type
    if (move[2] != "r0"):
        moveUsed = moveToIndex(move[2])
        board[moveUsed[0]][moveUsed[1]] = 0
    return board

# Check for mill based on the row and column used
def checkForMill(board, row, col, type):
    if (row == 0):
        if (col == 0):
            if (board[0][1] == type and board[0][2] == type):
                return True
            if (board[3][0] == type and board[6][0] == type):
                return True
        if (col == 1):
            if (board[0][0] == type and board[0][2] == type):
                return True
            if (board[1][1] == type and board[2][1] == type):
                return True
        if (col == 2):
            if (board[0][0] == type and board[0][1] == type):
                return True
            if (board[3][5] == type and board[6][2] == type):
                return True
    if (row == 1):
        if (col == 0):
            if (board[1][1] == type and board[2][1] == type):
                return True
            if (board[3][1] == type and board[5][1] == type):
                return True
        if (col == 1):
            if (board[0][1] == type and board[2][1] == type):
                return True
            if (board[1][0] == type and board[1][2] == type):
                return True
        if (col == 2):
            if (board[0][2] == type and board[1][2] == type):
                return True
            if (board[3][4] == type and board[5][2] == type):
                return True
    if (row == 2):
        if (col == 0):
            if (board[2][1] == type and board[2][2] == type):
                return True
            if (board[3][0] == type and board[4][0] == type):
                return True
        if (col == 1):
            if (board[1][1] == type and board[0][1] == type):
                return True
            if (board[2][0] == type and board[2][2] == type):
                return True
        if (col == 2):
            if (board[2][0] == type and board[2][1] == type):
                return True
            if (board[3][3] == type and board[4][2] == type):
                return True
    if (row == 3):
        if (col == 0):
            if (board[3][1] == type and board[3][2] == type):
                return True
            if (board[0][0] == type and board[6][0] == type):
                return True
        if (col == 1):
            if (board[3][0] == type and board[3][2] == type):
                return True
            if (board[1][0] == type and board[5][0] == type):
                return True
        if (col == 2):
            if (board[3][0] == type and board[3][1] == type):
                return True
            if (board[2][0] == type and board[4][0] == type):
                return True
        if (col == 3):
            if (board[3][4] == type and board[3][5] == type):
                return True
            if (board[2][2] == type and board[4][2] == type):
                return True
        if (col == 4):
            if (board[3][3] == type and board[3][5] == type):
                return True
            if (board[1][2] == type and board[5][2] == type):
                return True
        if (col == 5):
            if (board[3][3] == type and board[3][4] == type):
                return True
            if (board[0][2] == type and board[6][2] == type):
                return True
    if (row == 4):
        if (col == 0):
            if (board[4][1] == type and board[4][2] == type):
                return True
            if (board[2][0] == type and board[3][2] == type):
                return True
        if (col == 1):
            if (board[4][0] == type and board[4][2] == type):
                return True
            if (board[5][1] == type and board[6][1] == type):
                return True
        if (col == 2):
            if (board[4][0] == type and board[4][1] == type):
                return True
            if (board[3][3] == type and board[2][2] == type):
                return True
    if (row == 5):
        if (col == 0):
            if (board[5][1] == type and board[5][2] == type):
                return True
            if (board[3][1] == type and board[1][0] == type):
                return True
        if (col == 1):
            if (board[5][0] == type and board[5][2] == type):
                return True
            if (board[4][1] == type and board[6][1] == type):
                return True
        if (col == 2):
            if (board[5][0] == type and board[5][1] == type):
                return True
            if (board[3][4] == type and board[1][2] == type):
                return True
    if (row == 6):
        if (col == 0):
            if (board[6][1] == type and board[6][2] == type):
                return True
            if (board[3][0] == type and board[0][0] == type):
                return True
        if (col == 1):
            if (board[6][0] == type and board[6][2] == type):
                return True
            if (board[5][1] == type and board[4][1] == type):
                return True
        if (col == 2):
            if (board[6][0] == type and board[6][1] == type):
                return True
            if (board[3][5] == type and board[0][2] == type):
                return True
    return False

def checkWinByNumber(board, phase):
    if phase != 3:
        return 0
    blue = 0
    orange = 0
    for i in range(7):
        for j in range(3):
            if (board[i][j] == 1):
                blue += 1
            elif (board[i][j] == -1):
                orange += 1
    for i in range (3):
        if (board[3][i] == 1):
            blue += 1
        elif (board[3][i] == -1):
            orange += 1
    if blue == 2:
        return -1
    if orange == 2:
        return 1
    return 0
    
def main():
    board = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    printBoard(board)
    blue = True
    myTurn = False
    turns = 0
    phase = 0
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