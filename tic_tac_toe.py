from functions_tic_tac_toe import *

board, turn, draw, player, player_turn, ai, ai_turn = start_game()

draw_board(board)

play_again = True
while play_again:
    if turn % 2 == ai_turn % 2:
        board = ai_move(board, player, ai)
        turn += 1
        draw_board(board)
        if check_win(board) or turn > 9:
            if not check_win(board):
                draw = True
            play_again = game_over(draw, turn)
            if play_again:
                board, turn, draw, player, player_turn, ai, ai_turn = start_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                selected_x, selected_y = get_cell(posx, posy)
                if valid_move(selected_x, selected_y, board):
                    board[selected_x][selected_y] = player
                    turn += 1
                draw_board(board)
                if check_win(board) or turn > 9:
                    if not check_win(board):
                        draw = True
                    play_again = game_over(draw, turn)
                    if play_again:
                        board, turn, draw, player, player_turn, ai, ai_turn = start_game()
                  
