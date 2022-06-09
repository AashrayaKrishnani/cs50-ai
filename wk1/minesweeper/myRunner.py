import pygame
import sys
import time

from minesweeper import MinesweeperAI, Minesweeper


# Game Variables
HEIGHT = 8 
WIDTH = 8
MINES = 8

shown = set()
flagged = set()
lost = False

# Game
pygame.init()
size = width, height = 600,400
screen = pygame.display.set_mode(size)

# Calculating Board Dimensions
BOARD_PADDING = 20
board_width = (2/3)*width - (2*BOARD_PADDING)
board_height = height - (2*BOARD_PADDING)
cell_size = min(board_width/WIDTH, board_height/HEIGHT)
origin = (BOARD_PADDING, BOARD_PADDING)

if HEIGHT<WIDTH:
    origin = (BOARD_PADDING, BOARD_PADDING + (board_height - HEIGHT*cell_size)/2)
elif WIDTH<HEIGHT:
    origin = (BOARD_PADDING + (board_width - WIDTH*cell_size)/2, BOARD_PADDING )

# Game Agents
board = Minesweeper(HEIGHT, WIDTH, MINES)
ai = MinesweeperAI(HEIGHT, WIDTH)

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180,180,180)

# Fonts
OPENS_SANS = "assets/fonts/OpenSans-Regular.ttf"
small_font = pygame.font.Font(OPENS_SANS, 20)
med_font = pygame.font.Font(OPENS_SANS, 28)
lrg_font = pygame.font.Font(OPENS_SANS, 38)

# Images
flag = pygame.image.load("assets/images/flag.png")
mine = pygame.image.load("assets/images/mine.png")

flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Beginning Text
initialText = True

# The UI Rendering loop :)
while True:

    # If quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Else Render UI

    screen.fill(BLACK)

    # Adding ColorChange button.
    colorButton = pygame.Rect(width-30, 10, 20, 20)
    color = med_font.render("!", True, BLACK)
    colorRect = color.get_rect()
    colorRect.center = colorButton.center

    pygame.draw.rect(screen, WHITE, colorButton)
    screen.blit(color, colorRect)

    # Handling Click
    cl, _, _ = pygame.mouse.get_pressed()
    if cl:
        if colorButton.collidepoint(pygame.mouse.get_pos()):
            temp = BLACK
            BLACK = WHITE
            WHITE = temp    
            time.sleep(0.2)        

    # Beginning Text
    if(initialText):

        # Main Title 
        title = lrg_font.render('Play !MineCraft ;p', True, WHITE)
        titleBox = title.get_rect()
        titleBox.center = (width/2), 50
        screen.blit(title, titleBox)

        instructs = [
            '1. Hidden mines! Your sole purpose, find them!',
            '2. Numbers tell how many mines surround.',
            '3. It\'s not that hard, but if it gets!',
            'Then my AI is there to help ;D'
        ]

        for i, instruct in enumerate(instructs):
            line = small_font.render(instruct, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = width/2, 150 + 30*i
            screen.blit(line, lineRect)
        
        # The Let's Play! Button
        buttonRect = pygame.Rect(width/4, (3/4)*height, width/2, 50)
        playButton = med_font.render('Let\'s Play!', True, BLACK)
        playButtonRect = playButton.get_rect()
        playButtonRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(playButton, playButtonRect)

        # Handle Click on PlayButton
        click, _, _ = pygame.mouse.get_pressed()
        if click:
            cur = pygame.mouse.get_pos()
            if buttonRect.collidepoint(cur):
                initialText = False
                time.sleep(1)
        pygame.display.flip()
        continue

    # If in Game, Draw board.
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # The cell rectangle
            cell = pygame.Rect(
                origin[0] + j*cell_size,
                origin[1] + i*cell_size,
                cell_size, cell_size)

            pygame.draw.rect(screen, GRAY, cell)
            pygame.draw.rect(screen, WHITE, cell, 3)

            # If Cell is Revealed then show required info:
            if board.is_mine((i,j)) and lost:
                screen.blit(mine, cell)
            elif (i, j) in flagged:
                screen.blit(flag, cell)
            elif (i, j) in shown:
                cellNum = small_font.render(
                    str(board.nearby_mines((i,j))), True, BLACK
                )
                cellNumRect = cellNum.get_rect()
                cellNumRect.center = cell.center
                screen.blit(cellNum, cellNumRect)

            row.append(cell)
        cells.append(row)


    # AI Move BUtton
    aiMoveButton = pygame.Rect(
        (2/3)*width + BOARD_PADDING, (1/3)*height-50, (1/3)*width - 2*BOARD_PADDING, 50 
        )
    aiMoveText = med_font.render('AI Power!', True, BLACK)
    aiMoveRect = aiMoveText.get_rect()
    aiMoveRect.center = aiMoveButton.center

    pygame.draw.rect(screen, WHITE, aiMoveButton)
    screen.blit(aiMoveText, aiMoveRect)

    # Restart Button
    restartButton = pygame.Rect(
        (2/3)*width + BOARD_PADDING, (1/3)*height+20, (1/3)*width - 2*BOARD_PADDING, 50 
    )
    restartText = med_font.render('Try Again!', True, BLACK)
    restarRect = restartText.get_rect()
    restarRect.center = restartButton.center

    pygame.draw.rect(screen, WHITE, restartButton)
    screen.blit(restartText, restarRect)

    # Game Result Text
    text = 'Lost! **' if lost else 'Won! ^^' if board.mines == flagged else ''
    text = med_font.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = (5*width/6, 2*height/3)

    screen.blit(text, textRect)

    # Handling move
    move = None

    l, _, r = pygame.mouse.get_pressed()

    # Right Click means toggle flag!
    if r:
        cur = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(cur):
                    if (i,j) in flagged:
                        flagged.remove((i,j))
                    else:
                        flagged.add((i,j))
                    time.sleep(0.5)
    elif l: # Player moved either on board, or pressed a button.
        cur = pygame.mouse.get_pos()

        # If they clicked reset
        if restartButton.collidepoint(cur):
            board= Minesweeper(HEIGHT, WIDTH, MINES)
            ai = MinesweeperAI(HEIGHT, WIDTH)
            shown = set()
            flagged = set()
            lost = False

            continue
        # If they clicked AI button.
        elif aiMoveButton.collidepoint(cur) and not lost:
            move = ai.make_safe_move()
            if move == None:
                move = ai.make_random_move()
                if move == None: # We won :D
                    flagged = board.mines.copy()
                    print('Look! You won ;p XD')
                else:                     
                    print('*-* AI Confused *-* Guessing now ;p')

            else:
                print('AI knows well what its doing! ^-^')

            time.sleep(0.3)
        # User made a move
        else:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(cur) and (i,j) not in flagged and (i,j) not in shown:
                        move = (i,j)

    # Make the Move
    if move is not None:
        if board.is_mine(move):
            lost=True
        else:
            ai.add_knowledge(move, board.nearby_mines(move))
            shown.add(move)

    pygame.display.flip()