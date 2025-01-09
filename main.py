import pygame
import math
import time

width = 700
height = 700
cellSize = 100

turnToPlay = "Computer"
turn = 0

playerSelectedPieceArr = []

run = True
selectedPiece = None

bestMove = None

board = [                 #1's are AI's pieces and 2s are Player's
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


def findPossibleMoves(selectedPiece):   #Finds the possible moves for selected piece
    row, column = selectedPiece[0], selectedPiece[1]
    possibleMoves = findAllPossibleMoves("Player")

    for piece, row, column in possibleMoves:
        if piece == selectedPiece:
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

    selectedPieceNewPos = mouseY, mouseX

    playerSelectedPieceArr.append(selectedPieceNewPos)
    
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 3):
                board[i][j] = 0


def checkCapture(): #Checks all four directions of the pieces

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
                        deletedPieces.append((newPositionRow, k, 1))

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
                        deletedPieces.append((newPositionRow, k, 1))

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
                        deletedPieces.append((k, newPositionColumn, 1))
                count = 0

                #Checking bottom of the piece
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
                        deletedPieces.append((k, newPositionColumn, 1))

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
                        deletedPieces.append((newPositionRow, k, 2))

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
                        deletedPieces.append((newPositionRow, k, 2))

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
                        deletedPieces.append((k, newPositionColumn, 2))
                count = 0

                #Checking bottom of the piece
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
                        deletedPieces.append((k, newPositionColumn, 2))

                count = 0



    for row, column, deletedPiece in deletedPieces:   #Deleting the captured pieces
        board[row][column] = 0


    return deletedPieces


def undoCapture(deletedPieces):

    for row, column,deletedPiece in deletedPieces:
        board[row][column] = deletedPiece


def findAllPossibleMoves(player):

    possibleMoves = []
    pieces = []

    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 1 and player == "Computer":
                pieces.append((i, j))
            elif val == 2 and player == "Player":
                pieces.append((i, j))


    for piece in pieces:
        row, column = piece
    
        if 7 > row + 1 >= 0 and board[row+1][column] != 1 and board[row+1][column] != 2:
            possibleMoves.append((piece, row+1, column))
        if 0 <= row - 1 < 7 and board[row-1][column] != 1 and board[row-1][column] != 2:
            possibleMoves.append((piece, row-1, column))
        if 7 > column + 1 >= 0 and board[row][column+1] != 1 and board[row][column+1] != 2:
            possibleMoves.append((piece, row, column+1))
        if 0 <= column - 1 < 7 and board[row][column-1] != 1 and board[row][column-1] != 2:
            possibleMoves.append((piece, row, column-1))


    return possibleMoves


def makeMove(piece, move, player):
    row, column = piece
    targetRow, targetColumn = move

    if player == "Computer":
        board[targetRow][targetColumn] = 1
    elif player == "Player":
        board[targetRow][targetColumn] = 2
    else:
        print("Error")

    board[row][column] = 0

    return piece


def undoMove(piece, move, player):
    row, column = piece
    playedRow, playedColumn = move

    if player == "Computer":
        board[row][column] = 1
    elif player == "Player":
        board[row][column] = 2

    board[playedRow][playedColumn] = 0
    

def checkWinner():

    computerPieces = 0
    playerPieces = 0

    for row in board:
        for val in row:
            if val == 1:
                computerPieces += 1
            elif val == 2:
                playerPieces += 1

    if computerPieces == 0:
        return "Player"
    
    if playerPieces == 0:
        return "Computer"

    if turn >= 50:
        if computerPieces == playerPieces:
            return "Draw"
        elif computerPieces > playerPieces:
            return "Computer"
        elif computerPieces < playerPieces:
            return "Player"

    return False

def evaluateBoard():
    eval = 0

    for i, row in enumerate(board):
        for j, val in enumerate(row):

            if i == 0:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if i == 6:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if j == 0:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if j == 6:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if val == 1:
                eval += 3
            elif val == 2:
                eval -= 3


    return eval


def minimax(depth, isMaximizingPlayer, alpha, beta, treeDepth = 0):  # Maximizing player is ai

    if depth == 0 or checkWinner() != False:
        return evaluateBoard()

    if isMaximizingPlayer:
        maxEval = -math.inf
        possibleMoves = findAllPossibleMoves("Computer")

        for piece, row, column in possibleMoves:

            makeMove(piece, (row,column), "Computer")
            deletedPieces = checkCapture()

            eval = minimax(depth - 1, False, alpha, beta, treeDepth + 1)

            undoCapture(deletedPieces)
            undoMove(piece, (row,column), "Computer")

            if treeDepth == 0 and eval > maxEval:
                maxEval = eval
                global bestMove
                bestMove = (piece, row, column)

            elif eval > maxEval:
                maxEval = eval


            alpha = max(alpha, maxEval)

            if beta <= alpha:
                break

        return maxEval
    
    else:
        minEval = math.inf
        possibleMoves = findAllPossibleMoves("Player")

        for piece, row, column in possibleMoves:
            
            makeMove(piece, (row,column), "Player")
            deletedPieces = checkCapture()

            eval = minimax(depth - 1, True, alpha, beta, treeDepth + 1)

            undoCapture(deletedPieces)
            undoMove(piece, (row,column), "Player")
            minEval = min(minEval, eval)
            beta = min(minEval, beta)

            if beta <= alpha:
                break

        return minEval


def computerMove():
    
    global bestMove

    start = time.process_time()

    minimax(5, True, -math.inf, math.inf)

    print("Time it took to calculate: ", time.process_time() - start)

    if bestMove:    
        makeMove(bestMove[0], (bestMove[1], bestMove[2]), "Computer")
    else:
        print("No valid move")


    bestMove = None



pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

backSurface = pygame.Surface((width, height))


while turn <= 50:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn != 0:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseX = mouseX // 100
            mouseY = mouseY // 100
            if board[mouseY][mouseX] == 2:

                if len(playerSelectedPieceArr) != 0:
                    for piece in playerSelectedPieceArr:
                        if piece != (mouseY, mouseX):
                            selectedPiece = mouseY, mouseX
                else:
                    selectedPiece = mouseY, mouseX
                    
                for i, row in enumerate(board):
                    for j, val in enumerate(row):
                        if(val == 3):
                            board[i][j] = 0

            elif board[mouseY][mouseX] == 3:

                MoveSelectedPiece(selectedPiece, mouseX, mouseY)
                checkCapture()

                turn += 1
                turnToPlay = "Computer"
                playerSelectedPieceArr.clear()
                
                
                if turnToPlay == "Computer":
                    computerMove()
                    checkCapture()
                    turn += 1
                    computerTurnCounter = 0
                    turnToPlay = "Player"


                selectedPiece = None

        elif event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            computerMove()
            checkCapture()
            turn += 1
            turnToPlay = "Player"

           

    backSurface.fill('white')            

    drawBoard()
    drawPieces()

    if selectedPiece:
        findPossibleMoves(selectedPiece)
        drawPossibleMoves()

    screen.blit(backSurface, (0,0))
    pygame.display.update()


print("Game over ", turn)

winner = checkWinner()

if winner != "Draw":
    print("Winner of the game is", winner)
else:
    print("Draw")