import pygame
import sys
import time

import tictactoe as t

pygame.init()
size = (width,height) = (600, 400)

# Colors
black =(0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

medFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
lrgFont = pygame.font.Font("OpenSans-Regular.ttf", 45)
playFont = pygame.font.Font("OpenSans-Regular.ttf", 70)

firstTime = True
user = None
board = t.initial_state()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill(black)

    # Adding ColorChange button.
    colorButton = pygame.Rect(width-30, 10, 20, 20)
    color = medFont.render("!", True, black)
    colorRect = color.get_rect()
    colorRect.center = colorButton.center
    pygame.draw.rect(screen, white, colorButton)
    screen.blit(color, colorRect)

    # Handling color button pressed
    clicked, something, something = pygame.mouse.get_pressed()
    if clicked:
        cursor_pos = pygame.mouse.get_pos()
        if colorButton.collidepoint(cursor_pos):
            # Swapping colors ;p
            temp = black
            black = white
            white = temp

    if user is None:

        # Title
        title = lrgFont.render("Ticky-Tacky-Toe! ;p" if not firstTime else "Tic-Tac-Toe :D", True, white) 
        titleRect = title.get_rect()
        titleRect.center = (width/2, 100)
        screen.blit(title, titleRect)

        # Play as 'X' or 'O'
        xButton = pygame.Rect(width/8, height/1.8, width/4, 50)
        x = medFont.render(" Play as X ", True, black)
        xButtonRect = x.get_rect()
        xButtonRect.center = xButton.center
        pygame.draw.rect(screen, white, xButton)
        screen.blit(x, xButtonRect)

        oButton = pygame.Rect(5*width/8, height/1.8, width/4, 50)
        o = medFont.render(" Play as O ", True, black)
        oButtonRect = o.get_rect()
        oButtonRect.center = oButton.center
        pygame.draw.rect(screen, white, oButton)
        screen.blit(o, oButtonRect)

        # Handling Button click
        clicked, something, something = pygame.mouse.get_pressed()
        if clicked:
            cursor_pos = pygame.mouse.get_pos()
            if xButton.collidepoint(cursor_pos):
                time.sleep(.5)
                user = t.X
                firstTime=False
            elif oButton.collidepoint(cursor_pos):
                time.sleep(.5)
                user = t.O
                firstTime=False

    else:
        # GameBoard: t=tile
        size = 80
        origin = (width/2 -1.5 * size, height/2 -1.5 * size)        # Top-Left corner coordinates.

        tiles = []

        for i in range(3):
            row = []
            for j in range(3):          
                tile = pygame.Rect(origin[0] + i*size, origin[1] + j*size, size, size)   #(x, y, width, height)
                pygame.draw.rect(screen, white, tile, 3)

                # Fill the tile
                if board[i][j] != t.EMPTY:
                    move = playFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = tile.center
                    screen.blit(move, moveRect)
                row.append(tile)
            tiles.append(row)
        
        player = t.player(board)
        game_over = t.terminal(board)

        # Showing Big Title
        if game_over:
            winner = t.winner(board)
            if winner is None:
                title = "Tie *-*"
            elif winner == user:
                title = "You win! ^^"
            else:
                title = "AI won! ;p"

            # Displaying Play Again
            againButton = pygame.Rect(width/3, height-55, width/3, 45)
            again = medFont.render("Play Again", True, black)
            againButtonRect = again.get_rect()
            againButtonRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againButtonRect)

            # Handling PlayAgain button
            clicked, something, something = pygame.mouse.get_pressed()
            if clicked:
                cursor_pos = pygame.mouse.get_pos()
                if againButton.collidepoint(cursor_pos):
                    time.sleep(0.2)
                    user = None
                    board = t.initial_state()

        elif player==user:
            title = "Play as: " + player
        else:
            title = "AI calculating..."

        title = lrgFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = (width/2, 40)
        screen.blit(title, titleRect)

        # Checking for AI turn        
        if user!=player and not game_over:
            time.sleep(0.5)
            move = t.minimax(board)
            board = t.result(board, move)
            player = t.player(board)
        
        # Checking for User's turne
        if user==player and not game_over:
            clicked, something, something = pygame.mouse.get_pressed()
            if clicked:
                cursor_pos = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if tiles[i][j].collidepoint(cursor_pos) and board[i][j] == t.EMPTY:
                            board = t.result(board, (i, j))
                            player = t.player(board)
        

        # Handling playAgain Pressed

        




    # Actully what updates the screen XD
    pygame.display.flip()
