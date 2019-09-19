import pygame
import random
import sys

# board
ROWS = 3
COLUMNS = 3
BORDER = 40
SQUARESIZE = 100
WIDTH = 5

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)
D_GRAY = (80, 80, 80)

pygame.init()

# creates display of game board
screen_size = (COLUMNS * SQUARESIZE + (2 * BORDER), ROWS * SQUARESIZE + (2 * BORDER))
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("TIC-TAC-TOE")

# takes size, text, color of new message to be displayed
# returns configured text block and width,height dimensions
# dimensions so text block can be centered in desired location of the screen
def message(size, word, color):
    # sets font with hard coded font type and passed in size 
    set_font = pygame.font.SysFont("Courier New", size, True)

    # creates text block with passed in message and color
    set_color = set_font.render(word, True, color)

    # gets dimension of text block in form [left,top,width,height]
    get_dimension = set_color.get_rect()

    return set_color, get_dimension[2], get_dimension[3]


# displays start game menu for user to choose move order
# resets variables from previous games
def start_game():
    # represents game board
    grid = [["", "", ""], 
            ["", "", ""], 
            ["", "", ""]]

    # move number 
    curr_turn = 1

    # whether the board is filled without a three in a row
    tie = False

    # covers win message from previous game 
    pygame.draw.rect(screen, BLACK, (0, 0, COLUMNS * SQUARESIZE + (BORDER * 2), BORDER))
    
    # colors in game board square
    pygame.draw.rect(screen, GRAY, (BORDER, BORDER, COLUMNS * SQUARESIZE, ROWS * SQUARESIZE))
   

    # covers user and ai icons from previous game
    pygame.draw.rect(screen, BLACK, (0, ROWS * SQUARESIZE + BORDER, COLUMNS * SQUARESIZE + (BORDER * 2), BORDER))
    
    
   # draws lines to divide board into 3x3 grid
    for r in range(ROWS):
        for c in range(COLUMNS):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE + BORDER, r * SQUARESIZE + BORDER, SQUARESIZE, SQUARESIZE), WIDTH)

    # draws start menu to display move choices for user
    pygame.draw.rect(screen, D_GRAY, (SQUARESIZE * .5 + BORDER, SQUARESIZE * .5 + BORDER, SQUARESIZE * 2, SQUARESIZE * 2))
    
    # draws the buttons for the three move choices 
    move_1 = pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER + WIDTH, SQUARESIZE * 1 + BORDER + WIDTH, SQUARESIZE * 2 - (WIDTH * 2), SQUARESIZE / 2 - (WIDTH * 2)))
    move_2 = pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER + WIDTH, SQUARESIZE * 1.5 + BORDER + WIDTH, SQUARESIZE * 2 - (WIDTH * 2), SQUARESIZE / 2 - (WIDTH * 2)))
    move_random = pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER + WIDTH, SQUARESIZE * 2 + BORDER + WIDTH, SQUARESIZE * 2 - (WIDTH * 2), SQUARESIZE / 2 - (WIDTH * 2)))

    # creates text block asking user to choose a move order
    text, x2, y2 = message(24, "CHOOSE MOVE", RED)

    # used to find center of upper fourth of the start menu
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2

    # places and centers text block on start menu 
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE * .5 + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    # creates text block for first move choice
    text, x2, y2 = message(22, "MOVE 1 - X", RED)

    # used to find center of second fourth from the top of start menu
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2

    # places and centers text block on start menu
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    # creates text block for the second move choice
    text, x2, y2 = message(22, "MOVE 2 - O", RED)

    # used to find center of third fourth from the top of start menu
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2

    # places and centers text block on start menu
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE * 1.5 + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    # creates text block for when user desires a random move order
    text, x2, y2 = message(22, "RANDOM", RED)

    # used to find center of bottom fourth on start menu
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2

    # places and centers text block on start menu
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE * 2 + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    # simply updates changes to the display screen 
    pygame.display.update()

    # gets the respective icons("X" or "O") for the user and the AI 
    # based off the users choice by mouse click
    player_icon, ai_icon = choose_turn(move_1, move_2, move_random)

    # when ai icon is X means user goes second
    # player order is the users move order
    if ai_icon == "X":
        player_order = 2
    else:
        player_order = 1

    # draws game board
    draw_board(grid, player_icon, ai_icon)

    # returns all starting variables needed to begin game 
    return grid, curr_turn, tie, player_icon, player_order, ai_icon


# scores each possible position for ai after ai placed a piece 
# favors three in a row, two in a row, corners 
# takes in icons to check where user has placed pieces 
def get_score(temp_grid, curr_turn, player_icon, ai_icon):
    # value of square starts at zero
    total = 0

    # there is a three in a row 
    if check_win(temp_grid):
        total += 1000

    # when moving second must take the center 
    # all other moves are losing
    if curr_turn == 2 and temp_grid[1][1] == ai_icon:
        total += 1000

    # stores pieces in columns
    c1 = []
    c2 = []
    c3 = []

    # stores pieces in diagonals
    d1 = []
    d2 = []

    # array of possible three in a rows 
    grid_array = [c1, c2, c3, d1, d2]

    # loops through grid to store values in row column and diagonal lists
    for r in range(ROWS):
        # stores the values on the diagonal in diagonal lists
        d1.append(temp_grid[r][r])
        d2.append(temp_grid[r][COLUMNS - r - 1])

        # there are 2 user icons in a row with no ai icon 
        # score of position is -100 because ai will lose on next move
        if temp_grid[r].count(player_icon) == 2 and temp_grid[r].count(ai_icon) == 0:
            total -= 100

        # there is 1 user icons in a row with no ai icon
        # score of position is -2 so ai would favor a corner position
        elif temp_grid[r].count(player_icon) == 1 and temp_grid[r].count(ai_icon) == 0:
            total -= 2

        # there are 2 ai icons in a row with no user icon
        # score of position is +30 because this position forces a move by the user 
        elif temp_grid[r].count(player_icon) == 0 and temp_grid[r].count(ai_icon) == 2:
            total += 30

        # iterates over columns to add values to column lists
        for c in range(COLUMNS):

            # column 1
            if c == 0:
                c1.append(temp_grid[r][c])

                # ai favors a corner position +10 to maximize winning opportunities 
                if (r == 0 or r == ROWS - 1) and temp_grid[r][c] == ai_icon:
                    total += 10

            # column 2
            elif c == 1:
                c2.append(temp_grid[r][c])

            # column 3
            elif c == 2:
                c3.append(temp_grid[r][c])

                # ai favors a corner position +10 to maximize winning opportunities 
                if (r == 0 or r == ROWS - 1) and temp_grid[r][c] == ai_icon:
                    total += 10
    
    # iterates through grid array to calculate scores of each 
    for i in range(len(grid_array)):

        # there are 2 user icons in a row with no ai icon 
        # score of position is -100 because ai will lose on next move
        if grid_array[i].count(player_icon) == 2 and grid_array[i].count(ai_icon) == 0:
            total -= 100

        # there is 1 user icons in a row with no ai icon
        # score of position is -2 so ai would favor a corner position
        elif grid_array[i].count(player_icon) == 1 and grid_array[i].count(ai_icon) == 0:
            total -= 2

        # separates scores of columns vs diagonals 
        # columns favored due to user being able to block a diagonal with a corner position
        # corners being a superior position to edges as they open opportunities for double winning moves  
        if i < COLUMNS:

            # there are 2 ai icons in a column with no user icon
            # score of position is +30 because this position forces a move by the user 
            if grid_array[i].count(player_icon) == 0 and grid_array[i].count(ai_icon) == 2:
                total += 30

        # there are 2 ai icons in a diagonal with no user icon
        # score of position is +16 because this position forces a move by the user 
        # not as valuable of column because can be blocked with a corner position
        elif grid_array[i].count(player_icon) == 0 and grid_array[i].count(ai_icon) == 2:
            total += 16

    return total


# performs move by ai
# checks all possible moves then makes a calculated decision 
def ai_move(grid, curr_turn, player_icon, ai_icon):
    # holds highest score of a position 
    # initialized to -1000 so that first checked position gets set to best
    best_score = -1000

    # holds position of highest score
    best_row = -1
    best_column = -1

    # goes through grid looking for possible moves
    for r in range(ROWS):
        for c in range(COLUMNS):

            # this is a possible move
            if grid[r][c] == "":

                # ai makes this move
                grid[r][c] = ai_icon

                # then evaluates the score of the position 
                score = get_score(grid, curr_turn, player_icon, ai_icon)

                # there is a new best score 
                if score > best_score:
                    
                    # sets best score and position
                    best_row = r
                    best_column = c
                    best_score = score
                
                # undos ai move to evaluate the next position
                grid[r][c] = ""

    # ai chooses the best position after scoring all available options
    grid[best_row][best_column] = ai_icon

    return grid
    

# sets the move order by users mouse click on the start menu for every game
# X O and rand are the buttons representing the options 
def choose_turn(X, O, rand):
    # represents the move the user chose
    player_choice = 0

    # runs until user picks a move order
    while player_choice == 0:

        # gets users input
        for event2 in pygame.event.get():

            # code terminates if user exits the window
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:

                # stores the position of the user mouse click 
                choice = event2.pos

                # user clicked inside the X block
                if X.collidepoint(choice):
                    player_choice = 1

                # user clicked inside the O block
                if O.collidepoint(choice):
                    player_choice = 2

                # user clicked inside the random block
                if rand.collidepoint(choice):

                    # generates a random int either 1 or 2 to be players move order
                    player_choice = random.randint(1,2)
        
    # sets icons for user, ai based off move order
    if player_choice == 1:
        return "X", "O"
    else:
        return "O", "X"


# updates board with each move 
# draws Xs and Os on board
def update_board(grid):
    # iterates through grid to find where the pieces have been placed
    for r in range(ROWS):
        for c in range(COLUMNS):

            # draws lines to separate board into 3x3 grid
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE + BORDER, r * SQUARESIZE + BORDER, SQUARESIZE, SQUARESIZE), WIDTH)
            if grid[r][c] != "":

                # letter is the icon to be placed on the game display
                letter = ""
                if grid[r][c] == "X":
                    letter = "X"
                else:
                    letter = "O"

                # creates text block on the icon
                text, x2, y2 = message(88, letter, BLACK)

                # used to center icon in its location on the grid
                x1 = (SQUARESIZE - x2) / 2
                y1 = (SQUARESIZE - y2) / 2

                # places the icon text block on the displayed board
                screen.blit(text, (c * SQUARESIZE + BORDER + x1, r * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))

    # simply updates the display of the board  
    pygame.display.update()


def draw_board(grid, player_icon, ai_icon):
    # colors in game board 
    pygame.draw.rect(screen, GRAY, (BORDER, BORDER, COLUMNS * SQUARESIZE, ROWS * SQUARESIZE))
    
    # creates text block to show the icon of the user 
    text, x2, y2 = message(26, "YOU - {}".format(player_icon), RED)

    # used to center the text block on the left bottom corner of the game window 
    x1 = (SQUARESIZE + BORDER - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2

    # places the text block on the window
    screen.blit(text, (x1, ROWS * SQUARESIZE + BORDER + y1, BORDER + SQUARESIZE, BORDER))
    
    # creates a text block to show the ai icon
    text, x2, y2 = message(26, "AI - {}".format(ai_icon), RED)

    # used to center the text block on the right bottom corner of the game window
    x1 = (SQUARESIZE + BORDER - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2

    # places the tedt block on the window
    screen.blit(text, (SQUARESIZE * 2 + BORDER + x1, ROWS * SQUARESIZE + BORDER + y1, BORDER + SQUARESIZE, BORDER))

    # draws the Xs and Os on the board
    update_board(grid)


# converts the pixel x,y mouse click to row and column on the game board
def get_cell(x, y):
    # checks if click is on the board
    if BORDER + WIDTH < x < COLUMNS * SQUARESIZE + BORDER - (2 * WIDTH) and BORDER + WIDTH < y < ROWS * SQUARESIZE + BORDER - (2 * WIDTH):
        
        # return y,x becasue pygame display is flipped as 0,0 it top left corner
        return int((y - BORDER) / SQUARESIZE), int((x - BORDER) / SQUARESIZE)

    # outside the board
    else:
        return -1, -1


# checks intended placement is empty 
def valid_move(x, y, grid):
    # only invalid move is when intended cell is not empty
    if grid[x][y] == "":
        return True
    return False


# runs at the end of a game 
# prompts user to play again
def game_over(tie, curr_turn, player_icon):
    # holds win message
    winner = ""

    # uses passed in tie as bool that represents no winner when true
    if not tie:

        # remainder of the current turn and player move order divided by 2 should be equal 
        # when game ends on player turn meaning ai made last move 
        if curr_turn % 2 == player_icon % 2:
            winner = "AI WINS"
        else:
            winner = "YOU WIN"
    else:
        winner = "DRAW"

    # creates text block for win message
    text, x2, y2 = message(30, winner, RED)

    # used to center text block on the upper border of the game display
    x1 = (SQUARESIZE - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2

    # places the win message on the display
    screen.blit(text, (SQUARESIZE + BORDER + x1, y1, SQUARESIZE, BORDER))

    # simply updates the display of the board
    pygame.display.update()

    # pauses for 1 second before showing play again prompt
    pygame.time.wait(1000)

    # colors in play again menu to display options
    pygame.draw.rect(screen, D_GRAY, (SQUARESIZE * .5 + BORDER, SQUARESIZE * .5 + BORDER, SQUARESIZE * 2, SQUARESIZE * 1))
    pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER, SQUARESIZE * 1.5 + BORDER, SQUARESIZE * 2, SQUARESIZE * 1))
    
    # creates play again text block
    text, x2, y2 = message(28, "PLAY AGAIN?", BLACK)

    # used to center play again text block on the upper portion of the play again menu
    x1 = (2 * SQUARESIZE - x2) / 2
    y1 = (SQUARESIZE - y2) / 2

    # places the text block on the display 
    screen.blit(text, (.5 * SQUARESIZE + BORDER + x1, .5 * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
        
    # creates yes text block
    text, x2, y2 = message(30, "YES", BLACK)

    # used to center yes block on the bottom right of the menu
    x1 = (SQUARESIZE - x2) / 2
    y1 = (SQUARESIZE - y2) / 2
    
    # creates yes option button 
    yes_block = pygame.draw.rect(screen, GREEN, (1.5 * SQUARESIZE + BORDER + x1 - (2 * WIDTH), 1.5 * SQUARESIZE + BORDER + y1 - (2 * WIDTH), 4 * WIDTH + x2, 4 * WIDTH + y2))
    
    # creates no option button
    # uses x1,y1 centering variables from yes block so that buttons are the same size
    no_block = pygame.draw.rect(screen, RED, (.5 * SQUARESIZE + BORDER + x1 - (2 * WIDTH), 1.5 * SQUARESIZE + BORDER + y1 - (2 * WIDTH), 4 * WIDTH + x2, 4 * WIDTH + y2))

    # places yes text block on its button on the display
    screen.blit(text, (1.5 * SQUARESIZE + BORDER + x1, 1.5 * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))

    # creates no option text block
    text, x2, y2 = message(30, "NO", BLACK)

    # used to center the text on the bottom left of the menu
    x1 = (SQUARESIZE - x2) / 2
    y1 = (SQUARESIZE - y2) / 2

    # places the no text on its button on the display
    screen.blit(text, (.5 * SQUARESIZE + BORDER + x1, 1.5 * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
   
   # simply updates the display 
    pygame.display.update()

    # repeat represents users choice to play again
    repeat = None
    while True:

        # gets users inputs
        for event2 in pygame.event.get():

            # if user exits the window code is terminated
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:

                # stores position in pixels of user mouse click 
                choice = event2.pos

                # user clicked the yes button
                if yes_block.collidepoint(choice):
                    repeat = True

                # user clicked the no button
                if no_block.collidepoint(choice):
                    repeat = False

        # breaks loop only when user selects an option
        if repeat is not None:
            break

    return repeat


# checks if there is a three in a row
def check_win(grid):
    # iterates through the grid checking the 8 possible three in a rows
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] != "":

                # row 1 6 possible three in a rows
                if r == 0: 
                    
                    # row 1 column 1 3 possible three in a rows
                    # vertical horizontal and negative diagonal wins
                    if c == 0:
                        if grid[r][c] == grid[r + 1][c] and grid[r][c] == grid[r + 2][c]:
                            return True
                        if grid[r][c] == grid[r][c + 1] and grid[r][c] == grid[r][c + 2]:
                            return True
                        if grid[r][c] == grid[r + 1][c + 1] and grid[r][c] == grid[r + 2][c + 2]:
                            return True
                    
                    # row 1 column 2 1 possible three in a row
                    # vertical win
                    if c == 1:
                        if grid[r][c] == grid[r + 1][c] and grid[r][c] == grid[r + 2][c]:
                            return True

                    # row 1 column 3 2 possible three in a rows
                    # vertical and positive diagonal win
                    if c == 2:
                        if grid[r][c] == grid[r + 1][c] and grid[r][c] == grid[r + 2][c]:
                            return True
                        if grid[r][c] == grid[r + 1][c - 1] and grid[r][c] == grid[r + 2][c - 2]:
                            return True

                # row 2 column 1 1 possible three in a row
                # horizontal win
                if r == 1 and c == 0:
                    if grid[r][c] == grid[r][c + 1] and grid[r][c] == grid[r][c + 2]:
                        return True

                # row 3 column 1 1 possible three in a row
                # horizontal win
                if r == 2 and c == 0:
                    if grid[r][c] == grid[r][c + 1] and grid[r][c] == grid[r][c + 2]:
                        return True

    # no three in a row found returns false
    return False
