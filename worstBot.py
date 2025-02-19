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

def changeBoardWithIndex(board, row, col, type):
    board[row][col] = type
    return board

# Check for mill based on the row and column used
def checkForMill(board, row, col, type):
    if (row != 3):
        for i in range(3):
            if (board[row][i] != type):
                break
            if (i == 2):
                return True
        if col == 0:
            if (board[6-row][col] == type and board[3][3 - abs(3-row)] == type):
                return True
        elif col == 2:
            if (board[6-row][col] == type and board[3][2 + abs(3-row)] == type):
                return True
        else:
            if row < 3:
                if (board[0][1] == type and board[1][1] == type and board[2][1] == type):
                    return True
            else:
                if (board[4][1] == type and board[5][1] == type and board[6][1] == type):
                    return True
    else:
        if col < 3:
            for i in range(3):
                if (board[3][i] != type):
                    break
                if (i == 2):
                    return True
            if (board[col][0] == type and board[6 - col][0] == type):
                return True
        else:
            for i in range(3):
                if (board[3][i + 3] != type):
                    break
                if (i == 2):
                    return True
            if (board[col][2] == type and board[6 - col][2] == type):
                return True
    return False

def checkWinByNumber(board, type, phase):
    type = -type
    if phase != 3:
        return 0
    count = 0
    for i in range(7):
        for j in range(3):
            if (board[i][j] == type):
                count += 1
    for i in range (3):
        if (board[3][i] == type):
            count += 1
    if type == 2:
        return True
    return False

def checkEmptySpaces(board):
    possibleMoves = []
    for i in range(7):
        for j in range(3):
            if (board[i][j] == 0):
                possibleMoves.append([i, j])
    for i in range(3):
        if (board[3][i] == 0):
            possibleMoves.append([3, i])
    return possibleMoves

def checkPossibleMoves(board, row, col):
    possibleMoves = []
    if row != 3:
        if col == 0:
            if (board[3][3 - abs(3-row)] == 0):
                possibleMoves.append([3, 3 - abs(3-row)])
            if (board[row][1] == 0):
                possibleMoves.append([row, 1])
        elif col == 2:
            if (board[3][2 + abs(3-row)] == 0):
                possibleMoves.append([3, 2 + abs(3-row)])
            if (board[row][1] == 0):
                possibleMoves.append([row, 1])
        else:
            if (board[row][0] == 0):
                possibleMoves.append([row, 0])
            if (board[row][2] == 0):
                possibleMoves.append([row, 2])
            if row < 3:
                if row < 2:
                    if (board[row+1][1] == 0):
                        possibleMoves.append([row+1, 1])
                if row > 0:
                    if (board[row-1][1] == 0):
                        possibleMoves.append([row-1, 1])
            if row > 3:
                if row < 6:
                    if (board[row+1][1] == 0):
                        possibleMoves.append([row+1, 1])
                if row > 4:
                    if (board[row-1][1] == 0):
                        possibleMoves.append([row-1, 1])
    else:
        if col < 3:
            if (board[col][0] == 0):
                possibleMoves.append([col, 0])
            if (board[6-col][0] == 0):
                possibleMoves.append([6-col, 0])
            if col < 2:
                if (board[3][col + 1] == 0):
                    possibleMoves.append([3, col + 1])
            elif col > 0:
                if (board[3][col - 1] == 0):
                    possibleMoves.append([3, col - 1])
        else:
            if (board[col][2] == 0):
                possibleMoves.append([col, 2])
            if (board[6-col][2] == 0):
                possibleMoves.append([6-col, 2])
            if col > 4:
                if (board[3][col - 1] == 0):
                    possibleMoves.append([3, col - 1])
            elif col < 6:
                if (board[3][col + 1] == 0):
                    possibleMoves.append([3, col + 1])
    return possibleMoves

def evaluate(board, type, phase):
    return 0
    
def maxPruning(board, depth, alpha, beta, type, phase, turn, lastChanged):
    if (checkWinByNumber(board, -1, phase)):
        return -1000
    if (depth == 0):
        return evaluate(board, type, phase)

def minPruning(board, depth, alpha, beta, type, phase, turn, lastChanged):
    if (checkWinByNumber(board, 1, phase)):
        return 1000
    if (depth == 0):
        return evaluate(board, type, phase)

def makeMove(board, type, phase, turn, lastChanged):
    return

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