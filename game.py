from board import Board
from player import Player
import pygame

pygame.init()

bg_color = (0, 0, 0)
screen_width = 480  # 660
screen_height = 480  # 640
size = (screen_width, screen_height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
# pygame.display.set_icon('icon.png')
game_board = Board()
white_player = Player(game_board, 'White')
black_player = Player(game_board, 'Black')
white_player.set_opponent(black_player)
black_player.set_opponent(white_player)
ended = False


def reset():
    global game_board, white_player, black_player, ended, result
    game_board = Board()
    white_player = Player(game_board, 'White')
    black_player = Player(game_board, 'Black')
    white_player.set_opponent(black_player)
    black_player.set_opponent(white_player)
    ended = False
    result = 'Continue'
    Player.turn = 0


def show_game_end(res):
    text_size = 30
    font = pygame.font.SysFont('SansSerif', text_size)
    winner = f"{'White' if Player.turn == 1 else 'Black'} wins!!" if res == 'Checkmate' else None
    restart = 'Press Space to restart'

    end_screen_color = (142, 164, 210)
    end_screen_width = 300
    end_screen_height = 150
    end_screen_x = screen_width // 2 - end_screen_width // 2
    end_screen_y = screen_height // 2 - end_screen_height // 2
    pygame.draw.rect(screen, end_screen_color, (end_screen_x, end_screen_y, end_screen_width, end_screen_height))

    pos = (end_screen_x + end_screen_width // 2, end_screen_y + end_screen_height // 2)

    message = font.render(res, True, (0, 0, 0))
    rect = message.get_rect()
    rect.center = (pos[0], pos[1] - text_size)
    screen.blit(message, rect)

    if winner is not None:
        message = font.render(winner, True, (0, 0, 0))
        rect = message.get_rect()
        rect.center = pos
        screen.blit(message, rect)

    message = font.render(restart, True, (0, 0, 0))
    rect = message.get_rect()
    rect.center = (pos[0], pos[1] + text_size)
    screen.blit(message, rect)


def redraw(res):
    global ended
    game_board.draw(screen)
    if res != 'Continue':
        ended = True
        show_game_end(res)

    pygame.display.update()


run = True
selected = None
result = 'Continue'
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if ended:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset()

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if Player.turn == 0:
                    result = white_player.play(x, y)
                else:
                    result = black_player.play(x, y)

    redraw(result)

pygame.quit()
