import pygame
import random
import sys

pygame.init()

# board
ROWS = 3
COLUMNS = 3
BORDER = 40
SQUARESIZE = 100
WIDTH = 5

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)
D_GRAY = (80, 80, 80)
WHITE = (255, 255, 255)


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


def start_game():
    grid = [["", "", ""], 
            ["", "", ""], 
            ["", "", ""]]

    curr_turn = 1

    tie = False

    pygame.draw.rect(screen, BLACK, (0, 0, COLUMNS * SQUARESIZE + (BORDER * 2), BORDER))
    pygame.draw.rect(screen, GRAY, (BORDER, BORDER, COLUMNS * SQUARESIZE, ROWS * SQUARESIZE))
    
    text, x2, y2 = message(18, "PLAYER 1 - X", RED)
    x1 = (SQUARESIZE + BORDER - x2) / 2
    y1 = (BORDER + WIDTH- y2) / 2
    screen.blit(text, (x1, ROWS * SQUARESIZE + BORDER + y1, BORDER + SQUARESIZE, BORDER))
    
    text, x2, y2 = message(18, "PLAYER 2 - O", RED)
    x1 = (SQUARESIZE + BORDER - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2
    screen.blit(text, (SQUARESIZE * 2 + BORDER + x1, ROWS * SQUARESIZE + BORDER + y1, BORDER + SQUARESIZE, BORDER))

    for r in range(ROWS):
        for c in range(COLUMNS):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE + BORDER, r * SQUARESIZE + BORDER, SQUARESIZE, SQUARESIZE), WIDTH)

    pygame.draw.rect(screen, D_GRAY, (SQUARESIZE * .5 + BORDER, SQUARESIZE * .5 + BORDER, SQUARESIZE * 2, SQUARESIZE * 2))
    player_1 = pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER + WIDTH, SQUARESIZE * 1 + BORDER + WIDTH, SQUARESIZE * 2 - (WIDTH * 2), SQUARESIZE / 2 - (WIDTH * 2)))
    player_2 = pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER + WIDTH, SQUARESIZE * 1.5 + BORDER + WIDTH, SQUARESIZE * 2 - (WIDTH * 2), SQUARESIZE / 2 - (WIDTH * 2)))
    player_random = pygame.draw.rect(screen, BLACK, (SQUARESIZE * .5 + BORDER + WIDTH, SQUARESIZE * 2 + BORDER + WIDTH, SQUARESIZE * 2 - (WIDTH * 2), SQUARESIZE / 2 - (WIDTH * 2)))

    text, x2, y2 = message(24, "CHOOSE PLAYER", RED)
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE * .5 + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    text, x2, y2 = message(22, "PLAYER 1 - X", RED)
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    text, x2, y2 = message(22, "PLAYER 2 - O", RED)
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE * 1.5 + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    text, x2, y2 = message(22, "RANDOM", RED)
    x1 = (SQUARESIZE * 2 - x2) / 2
    y1 = (SQUARESIZE / 2 - y2) / 2
    screen.blit(text, (SQUARESIZE * .5 + BORDER + x1, SQUARESIZE * 2 + BORDER + y1, SQUARESIZE * 2, SQUARESIZE))

    pygame.display.update()

    player_icon, ai_icon = choose_turn(player_1, player_2, player_random)

    if ai_icon == "X":
        ai_order = 1
        player_order = 2
    else:
        ai_order = 2
        player_order = 1

    draw_board(grid)

    return grid, curr_turn, tie, player_icon, player_order, ai_icon, ai_order


def get_score(temp_grid, player_icon, ai_icon):
    total = 0
    if check_win(temp_grid):
        total += 100

    c1_count = []
    c2_count = []
    c3_count = []
    d1_count = []
    d2_count = []
    for r in range(ROWS):
        d1_count.append(temp_grid[r][r])
        d2_count.append(temp_grid[r][COLUMNS - r - 1])
        if temp_grid[r].count(player_icon) == 2 and temp_grid[r].count(ai_icon) < 1:
            total -= 50
        for c in range(COLUMNS):
            if c == 0:
                c1_count.append(temp_grid[r][c])
            elif c == 1:
                c2_count.append(temp_grid[r][c])
            elif c == 2:
                c3_count.append(temp_grid[r][c])
            
    if c1_count.count(player_icon) == 2 and c1_count.count(ai_icon) < 1:
        total -= 50
    if c1_count.count(player_icon) == 0 and c1_count.count(ai_icon) == 2:
        total += 10

    if c2_count.count(player_icon) == 2 and c2_count.count(ai_icon) < 1:
        total -= 50
    if c2_count.count(player_icon) == 0 and c2_count.count(ai_icon) == 2:
        total += 10

    if c3_count.count(player_icon) == 2 and c3_count.count(ai_icon) < 1:
        total -= 50
    if c3_count.count(player_icon) == 0 and c3_count.count(ai_icon) == 2:
        total += 10

    if d1_count.count(player_icon) == 2 and d1_count.count(ai_icon) < 1:
        total -= 50
    if d1_count.count(player_icon) == 0 and d1_count.count(ai_icon) == 2:
        total += 8

    if d2_count.count(player_icon) == 2 and d2_count.count(ai_icon) < 1:
        total -= 50
    if d2_count.count(player_icon) == 0 and d2_count.count(ai_icon) == 2:
        total += 8

    if ai_icon == "O" and temp_grid[1][1] == "":
        total -= 5
    return total


def ai_move(grid, player_icon, ai_icon):
    best_score = -100
    best_row = -1
    best_column = -1
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] == "":
                grid[r][c] = ai_icon
                score = get_score(grid, player_icon, ai_icon)
                if score > best_score:
                    best_row = r
                    best_column = c
                    best_score = score
                grid[r][c] = ""
    grid[best_row][best_column] = ai_icon
    return grid
    

def choose_turn(X, O, rand):
    player_choice = 0
    while player_choice == 0:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:
                choice = event2.pos
                if X.collidepoint(choice):
                    player_choice = 1
                if O.collidepoint(choice):
                    player_choice = 2
                if rand.collidepoint(choice):
                    player_choice = random.randint(1,2)
        
    if player_choice == 1:
        return "X", "O"
    else:
        return "O", "X"


def draw_board(grid):
    pygame.draw.rect(screen, GRAY, (BORDER, BORDER, COLUMNS * SQUARESIZE, ROWS * SQUARESIZE))
    
    text, x2, y2 = message(18, "PLAYER 1 - X", RED)
    x1 = (SQUARESIZE + BORDER - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2
    screen.blit(text, (x1, ROWS * SQUARESIZE + BORDER + y1, BORDER + SQUARESIZE, BORDER))
    
    text, x2, y2 = message(18, "PLAYER 2 - O", RED)
    x1 = (SQUARESIZE + BORDER - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2
    screen.blit(text, (SQUARESIZE * 2 + BORDER + x1, ROWS * SQUARESIZE + BORDER + y1, BORDER + SQUARESIZE, BORDER))

    for r in range(ROWS):
        for c in range(COLUMNS):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE + BORDER, r * SQUARESIZE + BORDER, SQUARESIZE, SQUARESIZE), WIDTH)
            if grid[r][c] != "":
                letter = ""
                if grid[r][c] == "X":
                    letter = "X"
                else:
                    letter = "O"
                text, x2, y2 = message(88, letter, BLACK)
                x1 = (SQUARESIZE - x2) / 2
                y1 = (SQUARESIZE - y2) / 2
                screen.blit(text, (c * SQUARESIZE + BORDER + x1, r * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
        
        pygame.display.update()


def get_cell(x, y):
    if BORDER + WIDTH < x < COLUMNS * SQUARESIZE + BORDER - WIDTH and BORDER + WIDTH < y < ROWS * SQUARESIZE + BORDER - WIDTH:
        return int((y - BORDER) / SQUARESIZE), int((x - BORDER) / SQUARESIZE)
    else:
        return -1, -1


def valid_move(x, y, grid):
    if grid[x][y] == "":
        return True
    return False


def game_over(tie, curr_turn):
    winner = ""
    if not tie:
        if curr_turn % 2 != 0:
            winner = "PLAYER 2 WINS"
        else:
            winner = "PLAYER 1 WINS"
    else:
        winner = "DRAW"

    text, x2, y2 = message(30, winner, RED)
    x1 = (SQUARESIZE - x2) / 2
    y1 = (BORDER + WIDTH - y2) / 2
    screen.blit(text, (SQUARESIZE + BORDER + x1, y1, SQUARESIZE, BORDER))

    pygame.display.update()

    pygame.time.wait(1500)
    pygame.draw.rect(screen, D_GRAY, (SQUARESIZE * .5 + BORDER, SQUARESIZE * .5 + BORDER, SQUARESIZE * 2, SQUARESIZE * 1))
    no_block = pygame.draw.rect(screen, RED, (SQUARESIZE * .5 + BORDER, SQUARESIZE * 1.5 + BORDER, SQUARESIZE * 1, SQUARESIZE * 1))
    yes_block = pygame.draw.rect(screen, GREEN, (SQUARESIZE * 1.5 + BORDER, SQUARESIZE * 1.5 + BORDER, SQUARESIZE * 1, SQUARESIZE * 1))
    
        
    text, x2, y2 = message(24, "PLAY AGAIN?", BLACK)
    x1 = (2 * SQUARESIZE - x2) / 2
    y1 = (SQUARESIZE - y2) / 2
    screen.blit(text, (.5 * SQUARESIZE + BORDER + x1, .5 * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
        
    text, x2, y2 = message(26, "NO", BLACK)
    x1 = (SQUARESIZE - x2) / 2
    y1 = (SQUARESIZE - y2) / 2
    screen.blit(text, (.5 * SQUARESIZE + BORDER + x1, 1.5 * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
        
    text, x2, y2 = message(26, "YES", BLACK)
    x1 = (SQUARESIZE - x2) / 2
    y1 = (SQUARESIZE - y2) / 2
    screen.blit(text, (1.5 * SQUARESIZE + BORDER + x1, 1.5 * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
   
    pygame.display.update()

    repeat = None
    while True:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:
                choice = event2.pos
                if yes_block.collidepoint(choice):
                    repeat = True
                if no_block.collidepoint(choice):
                    repeat = False
        if repeat is not None:
            break
    return repeat


def check_win(grid):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] != "":
                if r == 0: 
                    if c == 0:
                        if grid[r][c] == grid[r + 1][c] and grid[r][c] == grid[r + 2][c]:
                            return True
                        if grid[r][c] == grid[r][c + 1] and grid[r][c] == grid[r][c + 2]:
                            return True
                        if grid[r][c] == grid[r + 1][c + 1] and grid[r][c] == grid[r + 2][c + 2]:
                            return True
                        
                    if c == 1:
                        if grid[r][c] == grid[r + 1][c] and grid[r][c] == grid[r + 2][c]:
                            return True
                        
                    if c == 2:
                        if grid[r][c] == grid[r + 1][c] and grid[r][c] == grid[r + 2][c]:
                            return True
                        if grid[r][c] == grid[r + 1][c - 1] and grid[r][c] == grid[r + 2][c - 2]:
                            return True

                if r == 1 and c == 0:
                    if grid[r][c] == grid[r][c + 1] and grid[r][c] == grid[r][c + 2]:
                        return True

                if r == 2 and c == 0:
                    if grid[r][c] == grid[r][c + 1] and grid[r][c] == grid[r][c + 2]:
                        return True

    return False
