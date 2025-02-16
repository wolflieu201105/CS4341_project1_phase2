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

def main():
    print(moveToIndex("a1"))
    print(moveToIndex("b2"))
    print(moveToIndex("c3"))
    print(moveToIndex("d5"))
    print(moveToIndex("e4"))
    print(moveToIndex("f6"))
    print(moveToIndex("g7"))
    print(moveToIndex("a4"))

    print(indexToMove(6,0))
    print(indexToMove(5,0))
    print(indexToMove(4,0))
    print(indexToMove(2,1))
    print(indexToMove(3,3))
    print(indexToMove(1,2))
    print(indexToMove(0,2))
    print(indexToMove(3,0))
    return
    # board = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    # blue = True
    # myTurn = False
    # turns = 0
    # game_input = input().strip()
    # if game_input == "blue":
    #     myTurn = True
    # elif game_input == "orange":
    #     myTurn = False
    #     blue = False
    # else:
    #     print("Invalid input")
    #     sys.exit(1)
    # while True:
    #     try:
    #         if (myTurn):
    #             if (blue):
    #                 print("h1 a4 r0", flush=True)
    #             else:
    #                 print("h2 b4 r0", flush=True)
    #             myTurn = False
    #             turns += 1
            
    #         else:
    #             move = input().strip()
    #             # modify the board
    #             myTurn = True
    #             turns += 1

    #     except EOFError:
    #         break

if __name__ == "__main__":
    main()