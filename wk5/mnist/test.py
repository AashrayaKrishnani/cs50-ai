from re import L
from more_itertools import all_equal
import pygame
import sys
import time
import tensorflow as tf
from train import train

# Getting the model.
if len(sys.argv)==2:
    print('\n[!] Trying to load model: \''+str(sys.argv[1]) + '\'\n')
    model = tf.keras.models.load_model(sys.argv[1])
else:
    print('\n[!] Training Fresh model\n')
    model = train()

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180,180,180)

# Screen
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# Grid
grid = [
    [   
        [0] for i in range(28)
    ] for i in range(28)
]

# Grid Dimensions
grid_padding = 20
grid_height = min(height, width) - 2*grid_padding
grid_width = min(height, width) - 2*grid_padding
cell_size =  grid_height/(28.0)
origin = (grid_padding, grid_padding)

# Fonts
OPENS_SANS = "assets/fonts/OpenSans-Regular.ttf"
small_font = pygame.font.Font(OPENS_SANS, 20)
med_font = pygame.font.Font(OPENS_SANS, 28)
lrg_font = pygame.font.Font(OPENS_SANS, 38)


# Brush Width
brush_radius = 1
resultText = None

# UI Rendering Loop
while True:

    # If quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    # Else Render UI
    screen.fill(BLACK)


    # Adding ColorChange button.
    colorButton = pygame.Rect(width-30, 10, 20, 20)
    color = med_font.render("!", True, BLACK)
    colorRect = color.get_rect()
    colorRect.center = colorButton.center

    pygame.draw.rect(screen, WHITE, colorButton)
    screen.blit(color, colorRect)

    # Handling Click on it
    cl, _, _ = pygame.mouse.get_pressed()
    if cl:
        if colorButton.collidepoint(pygame.mouse.get_pos()):
            temp = BLACK
            BLACK = WHITE
            WHITE = temp    
            time.sleep(0.2) 

    # Rendering Board
    cells = []
    for i in range(28):
        row = []
        for j in range(28):
            # The cell rectangle
            cell = pygame.Rect(
                origin[0] + j*cell_size,
                origin[1] + i*cell_size,
                cell_size, cell_size)

            if grid[i][j][0] == 1:
                pygame.draw.rect(screen, BLACK, cell)
            else:
                pygame.draw.rect(screen, GRAY, cell)
            
            pygame.draw.rect(screen, WHITE, cell, 3)

            row.append(cell)
        cells.append(row)

    # clear Button
    clearButton = pygame.Rect( grid_width + grid_padding + 80, height-80, 80, 50)
    clearText = med_font.render('Clear', True, BLACK)
    clearRect = clearText.get_rect()
    clearRect.center = clearButton.center

    pygame.draw.rect(screen, WHITE, clearButton)
    screen.blit(clearText, clearRect)

    # ai Button
    aiButton = pygame.Rect( grid_width + grid_padding + 80, 150, 80, 50)
    aiText = med_font.render('AI', True, BLACK)
    aiRect = aiText.get_rect()
    aiRect.center = aiButton.center

    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(aiText, aiRect)

    # result Text
    if resultText is not None:
        text = lrg_font.render(resultText, True, WHITE)
        textRect = text.get_rect()
        textRect.center = (grid_width + grid_padding + 90, 300)

        screen.blit(text, textRect)

    # Handling Click
    cl,_,_ = pygame.mouse.get_pressed()

    if cl:
        cur = pygame.mouse.get_pos()

        if clearRect.collidepoint(cur):
            # Clear the Grid
            grid = [
                    [   
                        [0] for i in range(28)
                    ] for i in range(28)
                ]
            resultText = None
        elif aiRect.collidepoint(cur):
            # If AI Button is pressed.

            if all_equal(grid) and not grid[0][0][0]:
                resultText= 'DRAW ;p'
            else:
                # Showing Prediction
                prediction = list( model.predict([grid])[0] )
                index = 0 
                max = prediction[index]
                for i in range(1, len(prediction)):
                    if prediction[i]>max:
                        max=prediction[i]
                        index = i
                resultText = str(index)

        else:
            for i in range(28):
                for j in range(28):
                    if cells[i][j].collidepoint(cur):
                        for p in range(i-brush_radius, i+1+brush_radius):
                            for q in range(j-brush_radius, j+1+brush_radius):
                                if 0<=p<28 and 0<=q<28:
                                    grid[p][q][0] = 1      
                        time.sleep(0.03)
                        break

    
    pygame.display.flip()