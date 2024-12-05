import pygame
import random

width = 700
height = 700
cellSize = 100

turn = 0

run = True
selectedPiece = None

board = [
    [1,0,0,0,0,0,2],
    [0,0,0,0,0,0,0],
    [1,0,0,0,0,0,2],
    [0,0,0,0,0,0,0],
    [2,0,0,0,0,0,1],
    [0,0,0,0,0,0,0],
    [2,0,0,0,0,0,1]
    ]

def drawBoard():
    for i in range(0,7):
        for j in range(0,7):
            pygame.draw.rect(backSurface, 'black', pygame.Rect(j * cellSize, i * cellSize, cellSize, cellSize), 1)


def drawPieces():
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 1):
                pygame.draw.polygon(backSurface, 'red', ((j * cellSize + 50, i * cellSize + 25), (j * cellSize + 25, i * cellSize + 75), (j * cellSize + 75, i * cellSize + 75)))
            if(val == 2):
                pygame.draw.circle(backSurface, 'red', (j * cellSize + 50, i * cellSize + 50), 25)


def findPossibleMoves(selectedPiece):
    row, column = selectedPiece[0], selectedPiece[1]
    possibleMoves = []
    
    if 7 > row + 1 >= 0 and board[row+1][column] != 1 and board[row+1][column] != 2:
        possibleMoves.append((row+1, column))
    if 0 <= row - 1 < 7 and board[row-1][column] != 1 and board[row-1][column] != 2:
        possibleMoves.append((row-1, column))
    if 7 > column + 1 >= 0 and board[row][column+1] != 1 and board[row][column+1] != 2:
        possibleMoves.append((row, column+1))
    if 0 <= column - 1 < 7 and board[row][column-1] != 1 and board[row][column-1] != 2:
        possibleMoves.append((row, column-1))

    for row, column in possibleMoves:
        board[row][column] = 3


def drawPossibleMoves():
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 3):
                pygame.draw.circle(backSurface, 'gray', (j * cellSize + 50, i * cellSize + 50), 5)


def MoveSelectedPiece(selectedPiece, mouseX, mouseY):
    row, column = selectedPiece
    board[row][column] = 0
    board[mouseY][mouseX] = 2

    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 3):
                board[i][j] = 0


def checkCapture():

    deletedPieces = []

    count = 0
    i = 0

    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == 2: # Iterating for all the circles

                newPositionColumn = y
                newPositionRow = x

                #Checking right of the piece
                for i in range(newPositionColumn + 1, 8):
                    if i != 7:
                        if board[newPositionRow][i] == 2:
                            for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 1:
                                    count += 1


                if (i - newPositionColumn) - 1 == count:
                    for k in range(newPositionColumn + 1, i):
                        #board[newPositionRow][k] = 0
                        deletedPieces.append((newPositionRow, k))

                count = 0

                #Checking left of the piece
                for i in range(newPositionColumn - 1, -2, -1):
                    if i != -1:
                        if board[newPositionRow][i] == 2:
                            for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 1:
                                    count += 1


                if (newPositionColumn - i) - 1 == count:
                    for k in range(newPositionColumn - 1, i, -1):
                        deletedPieces.append((newPositionRow, k))

                count = 0

                #Checking up of the piece
                for i in range(newPositionRow - 1, -2, -1):
                    if i != -1:
                        if board[i][newPositionColumn] == 2:
                            for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 1:
                                    count += 1

                if (newPositionRow - i) - 1 == count:
                    for k in range(newPositionRow - 1, i, -1):
                        #board[k][newPositionColumn] = 0
                        deletedPieces.append((k, newPositionColumn))
                count = 0

                #Checking down of the piece
                for i in range(newPositionRow + 1, 8):
                    if i != 7:
                        if board[i][newPositionColumn] == 2:
                            for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 1:
                                    count += 1

                if (i - newPositionRow) - 1 == count:
                    for k in range(newPositionRow + 1, i):
                        deletedPieces.append((k, newPositionColumn))

                count = 0

            elif value == 1:  # Iterating for all the triangles

                newPositionColumn = y
                newPositionRow = x

                #Checking right of the piece
                for i in range(newPositionColumn + 1, 8):
                    if i != 7:
                        if board[newPositionRow][i] == 1:
                            for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 2:
                                    count += 1


                if (i - newPositionColumn) - 1 == count:
                    for k in range(newPositionColumn + 1, i):
                        deletedPieces.append((newPositionRow, k))

                count = 0

                #Checking left of the piece
                for i in range(newPositionColumn - 1, -2, -1):
                    if i != -1:
                        if board[newPositionRow][i] == 1:
                            for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 2:
                                    count += 1


                if (newPositionColumn - i) - 1 == count:
                    for k in range(newPositionColumn - 1, i, -1):
                        deletedPieces.append((newPositionRow, k))

                count = 0

                #Checking up of the piece
                for i in range(newPositionRow - 1, -2, -1):
                    if i != -1:
                        if board[i][newPositionColumn] == 1:
                            for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 2:
                                    count += 1

                if (newPositionRow - i) - 1 == count:
                    for k in range(newPositionRow - 1, i, -1):
                        deletedPieces.append((k, newPositionColumn))
                count = 0

                #Checking down of the piece
                for i in range(newPositionRow + 1, 8):
                    if i != 7:
                        if board[i][newPositionColumn] == 1:
                            for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 2:
                                    count += 1

                if (i - newPositionRow) - 1 == count:
                    for k in range(newPositionRow + 1, i):
                        deletedPieces.append((k, newPositionColumn))

                count = 0



    for row, column in deletedPieces:
        board[row][column] = 0


def computerMove():

    pieces = []
    possibleMoves = []

    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if board[i][j] == 1:
                pieces.append((i,j))

    selectedPiece = random.choice(pieces)

    row, column = selectedPiece

    if 7 > row + 1 >= 0 and board[row+1][column] != 1 and board[row+1][column] != 1 and board[row+1][column] != 2:
        possibleMoves.append((row+1, column))
    if 0 <= row - 1 < 7 and board[row-1][column] != 1 and board[row-1][column] != 1 and board[row-1][column] != 2:
        possibleMoves.append((row-1, column))
    if 7 > column + 1 >= 0 and board[row][column+1] != 1 and board[row][column+1] != 1 and board[row][column+1] != 2:
        possibleMoves.append((row, column+1))
    if 0 <= column - 1 < 7 and board[row][column-1] != 1 and board[row][column-1] != 1 and board[row][column-1] != 2:
        possibleMoves.append((row, column-1))


    while not possibleMoves:
        selectedPiece = random.choice(pieces)

    selectedMove = random.choice(possibleMoves)

    board[selectedPiece[0]][selectedPiece[1]] = 0
    board[selectedMove[0]][selectedMove[1]] = 1

    print(f"Played the move {selectedMove}")


pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

backSurface = pygame.Surface((width, height))


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn != 0:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseX = mouseX // 100
            mouseY = mouseY // 100
            if board[mouseY][mouseX] == 2:
                selectedPiece = mouseY, mouseX

                for i, row in enumerate(board):
                    for j, val in enumerate(row):
                        if(val == 3):
                            board[i][j] = 0

            elif board[mouseY][mouseX] == 3:

                MoveSelectedPiece(selectedPiece, mouseX, mouseY)
                checkCapture()
                turn += 1
                
                computerMove()
                checkCapture()
                turn += 1

                selectedPiece = None

        elif event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            computerMove()
            checkCapture()
            turn += 1

           

    backSurface.fill('white')            

    drawBoard()
    drawPieces()

    if selectedPiece:
        findPossibleMoves(selectedPiece)
        drawPossibleMoves()

    screen.blit(backSurface, (0,0))
    pygame.display.update()