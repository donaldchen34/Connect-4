import sys, pygame
import numpy as np
from random import *

# Global Settings
SQUARE_SIZE = 100
ROW_COUNT = 6
COL_COUNT = 7
BOARD_DIMENSIONS = COL_COUNT * SQUARE_SIZE, (ROW_COUNT + 1) * SQUARE_SIZE
screen = pygame.display.set_mode(BOARD_DIMENSIONS)

#add new game/ End screen GUI
#Computer AI 


def start():
    pygame.init()
    gui()
    playGame()
    #endGame()

def gui():
    drawBoard(screen)

def playGame():
    playing = True

    turn = randint(1, 2)  # 1 is Player, 2 is Computer

    board = createBoard()

    while playing:
        for event in pygame.event.get():
            #Close game
            if event.type == pygame.QUIT:
                playing = False
                sys.exit()

            #Piece on top of screen
            if event.type == pygame.MOUSEMOTION:
                BLACK = (0,0,0)
                YELLOW = (255, 255, 0)
                RED = (255, 0, 0)

                width = COL_COUNT * SQUARE_SIZE
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))

                pos = pygame.mouse.get_pos()
                if turn == 1:
                    pygame.draw.circle(screen,RED,(pos[0],int(SQUARE_SIZE/2)),int(SQUARE_SIZE/2 - 5))
                else:
                    pygame.draw.circle(screen,YELLOW,(pos[0],int(SQUARE_SIZE/2)),int(SQUARE_SIZE/2 - 5))

            pygame.display.update()


            #Put down piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = int(pos[0] / SQUARE_SIZE)

                if validMove(x, board):
                    playPiece(x, turn, board,screen)

                    if gameFinished(board):
                        playerWon(turn,screen)
                        print("Player", turn, "won!")


                        playing = False

                    elif boardFull(board):
                        RED = (255,0,0)
                        font = pygame.SysFont("Arial", 75, bold = True)
                        pygame.draw.rect(screen, (0,0,0), (0, 0, COL_COUNT * SQUARE_SIZE, SQUARE_SIZE))
                        
                        text = font.render("Tie: Board is Full", 1 , RED)
                        screen.blit(text, (40,10))

                        pygame.display.update()
                        playing = False


                if (turn == 1): #Players Turn
                        turn += 1
                else: #"Computers" Turn
                        turn -= 1

    pygame.time.wait(3000)



def playerWon(turn,screen):
    RED = (255,0,0)
    BLACK = (0,0,0)

    pygame.draw.rect(screen, BLACK, (0, 0, COL_COUNT * SQUARE_SIZE, SQUARE_SIZE))
    font = pygame.font.SysFont("Arial",75, bold = True)
    if (turn == 1):
        text = font.render("Player 1 Won", 1, RED)
        screen.blit(text, (40,10))
    else:
        text = font.render("Player 2 Won", 1, RED)
        screen.blit(text, (40,10))

    pygame.display.update()

#Gui : Play again? YES/ NO
def endgame():
    pass

def boardFull(board):
    for row in range(ROW_COUNT):
        if (not validMove(row,board)):
            return False

def drawBoard(screen):
    BLACK = (0,0,0)
    BLUE = (0, 0, 255)

    for col in range(COL_COUNT):
        for row in range(ROW_COUNT + 1):
            pygame.draw.rect(screen, BLUE, (row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            CENTER = (int((row * SQUARE_SIZE) + SQUARE_SIZE / 2), int(((col + 1) * SQUARE_SIZE) + SQUARE_SIZE / 2))
            RADIUS = int(SQUARE_SIZE/2 - 5)
            pygame.draw.circle(screen, BLACK, CENTER, RADIUS)

    pygame.display.update()

def validMove(x, board):
    return  board[0][x] == 0

#1 is Red, 2 is Yellow
def playPiece(x, turn, board,screen):
    #Update Internal Board
    temp = ROW_COUNT
    for row in range(ROW_COUNT):
        if board[row][x] == 0:
            temp = row

    board[temp][x] = turn

    #Put Piece on Screen
    YELLOW = (255,255,0)
    RED = (255,0,0)

    CENTER = (int((x * SQUARE_SIZE) + SQUARE_SIZE / 2), int(((temp+1) * SQUARE_SIZE) + SQUARE_SIZE / 2))
    RADIUS = int(SQUARE_SIZE / 2 - 5)

    if (turn == 1):
        pygame.draw.circle(screen,RED,CENTER,RADIUS)
    else:
        pygame.draw.circle(screen,YELLOW,CENTER,RADIUS)

    pygame.display.update()

def gameFinished(board):
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            #Horizontal Win
            if (row <= ROW_COUNT - 4):
                if (board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1 and board[row +3][col] == 1) or\
                        (board[row][col] == 2 and board[row + 1][col] == 2 and board[row + 2][col] == 2 and board[row +3][col] == 2):
                    return True

            #Vertical Win
            if (col <= COL_COUNT - 4):
                if (board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1 and board[row][col + 3] == 1) or\
                        (board[row][col] == 2 and board[row][col + 1] == 2 and board[row][col + 2] == 2 and board[row][col + 3] == 2):
                    return True

            #Down-Right/Up-Left Diagnol Win
            if (col <= COL_COUNT -4 and row <= ROW_COUNT -4):
                if (board[row][col] == 1 and board[row + 1][col + 1] == 1 and board[row + 2][col + 2] == 1 and board[row + 3][col + 3]  == 1) or\
                        (board[row][col] == 2 and board[row + 1][col + 1] == 2 and board[row + 2][col + 2] == 2 and board[row + 3][col + 3] == 2):
                    return True

            #Down-Left/Up-Right Diagnol Win
            if (col >= 3 and col < COL_COUNT and row < ROW_COUNT - 3):
                if (board[row][col] == 1 and board[row + 1][col - 1] == 1 and board[row + 2][col - 2] == 1 and board[row + 3][col - 3] == 1 or\
                        (board[row][col] == 2 and board[row + 1][col - 1] == 2 and board[row + 2][col - 2] == 2 and board[row + 3][col - 3] == 2)):
                    return True

def createBoard():
    newBoard = np.zeros((ROW_COUNT,COL_COUNT))
    return newBoard

def printBoard(board):
    print(board)