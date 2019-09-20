from functions_tic_tac_toe import *

# sets all starting variables to begin game with start menu
board, turn, draw, player, player_turn, ai = start_game()

# draws game board
draw_board(board, player, ai)

# runs until user decides to quit game 
play_again = True
while play_again:

    # ai turn to move 
    # based off user choice of move order
    if turn % 2 != player_turn % 2:

        # ai makes a move
        board = ai_move(board, turn, player, ai)

        # counts moves made by both players
        turn += 1

        # waits to display ai move on board so not instantly after player
        pygame.time.wait(300)

        # displays move on game display of board
        update_board(board)

        # checks win or if the board is filled
        if check_win(board) or turn > 9:

            # no winner means the board is full meaning draw
            if not check_win(board):
                draw = True

            # prompts a menu for user to play again or not
            play_again = game_over(draw, turn, player_turn)

            # user wants to play again
            # reset all variables to start game with start menu
            if play_again:
                board, turn, draw, player, player_turn, ai = start_game()
    
    # user turn to move
    else:

        # gets users inputs 
        for event in pygame.event.get():

            # terminates code is user exits the game window
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # stores pixel location of user mouse click
                posx = event.pos[0]
                posy = event.pos[1]

                # converts pixels and stores row and column of click on board
                selected_x, selected_y = get_cell(posx, posy)

                # the click was on an empty square on the board
                if valid_move(selected_x, selected_y, board) and selected_x != -1:

                    # places users piece on selected square
                    board[selected_x][selected_y] = player

                    # now its ai turn to move
                    turn += 1

                    # draws the updated board on the display
                    update_board(board)

                    # checks if there is a three in a row 
                    # and if there is another empty square
                    if check_win(board) or turn > 9:

                        # if ai is perfect checkwin should never be true after a user move
                        if not check_win(board):
                            
                            # board filled without a winner means draw
                            draw = True

                        # asks user to play again 
                        play_again = game_over(draw, turn, player_turn)

                        # resets to starting variables  
                        if play_again:
                            board, turn, draw, player, player_turn, ai = start_game()
                 