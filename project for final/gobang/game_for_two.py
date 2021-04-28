import pygame
from pygame import mixer

pygame.init ()

# screen, caption, and icon
screen = pygame.display.set_mode ((720, 720))
icon = pygame.image.load ('Doraemon.png')
pygame.display.set_icon (icon)
pygame.display.set_caption ('Gobang')
running = True
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 97, 0)
player1, player2 = black, white
player = player1


# draw the board out
def draw_the_board () :
    grid_width = 36
    a = 36
    b = 684
    pygame.draw.line (screen, black, (a, a), (b, a), 2)
    pygame.draw.line (screen, black, (a, a), (a, b), 2)
    pygame.draw.line (screen, black, (b, b), (b, a), 2)
    pygame.draw.line (screen, black, (b, b), (a, b), 2)
    for i in range (1, 18) :
        pygame.draw.line (screen, black, (a, a + i * grid_width), (b, a + i * grid_width), 2)
        pygame.draw.line (screen, black, (a + i * grid_width, a), (a + i * grid_width, b), 2)
    pygame.draw.circle (screen, black, (a + 3 * grid_width, a + 3 * grid_width), 5)
    pygame.draw.circle (screen, black, (a + 3 * grid_width, b - 3 * grid_width), 5)
    pygame.draw.circle (screen, black, (b - 3 * grid_width, b - 3 * grid_width), 5)
    pygame.draw.circle (screen, black, (b - 3 * grid_width, a + 3 * grid_width), 5)
    pygame.draw.circle (screen, black, (a + 9 * grid_width, a + 9 * grid_width), 5)


# record the click and draw the coin
matrix_white = []
matrix_black = []
color_matrix = [[0] * 19 for i in range (19)]
for i in range (19) :
    matrix_white.append ([])
    matrix_black.append ([])
    for j in range (19) :
        matrix_white[i].append ((0, 0))
        matrix_black[i].append ((0, 0))


def record_the_pos (pos, color=black) :
    within_the_board = True
    for i in pos :
        if not 36 <= i <= 684 :
            within_the_board = False
    if within_the_board :
        times1 = round ((pos[0] - 36) / 36)
        times2 = round ((pos[1] - 36) / 36)
        grid_x = int (times1) * 36 + 36
        grid_y = int (times2) * 36 + 36
        if color == black :
            matrix_black[times2][times1] = (grid_x, grid_y)
            color_matrix[times2][times1] = -1
        if color == white :
            matrix_white[times2][times1] = (grid_x, grid_y)
            color_matrix[times2][times1] = 1
        print (matrix_black)
        print (matrix_white)
        print (color_matrix)


def add_coin () :
    for i in range (len (matrix_white)) :
        for j in matrix_white[i] :
            if j != (0, 0) :
                pygame.draw.circle (screen, white, j, 15)
    for i in range (len (matrix_black)) :
        for j in matrix_black[i] :
            if j != (0, 0) :
                pygame.draw.circle (screen, black, j, 15)


# game is over?
def game_over (pos, player=black) :
    x = round ((pos[0] - 36) / 36)
    y = round ((pos[1] - 36) / 36)
    bool = True
    if player is black :
        # check horizontal
        for i in range (5) :
            check = 0
            if 0 <= x - i <= 13 :
                for j in range (5) :
                    check += color_matrix[y][x - i + j]
                if check == -5 :
                    bool = True
                    return bool
                else :
                    check = 0
                    bool = False
        # check vertical
        for i in range (5) :
            check = 0
            if 0 <= y - i <= 13 :
                for j in range (5) :
                    check += color_matrix[y - i + j][x]
                if check == -5 :
                    bool = True
                    return bool
                else :
                    check = 0
                    bool = False
        # check for dialogue 1
        for i in range (5) :
            check = 0
            if 0 <= x - i <= 13 and 0 <= y - i <= 13 :
                for j in range (5) :
                    check += color_matrix[y - i + j][x - i + j]
                if check == -5 :
                    bool = True
                    return bool
                else :
                    bool = False
        # check for dialogue 2
        for i in range (5) :
            check = 0
            if 0 <= x - i <= 13 and 5 <= y + i <= 13 :
                for j in range (5) :
                    check += color_matrix[y + i - j][x - i + j]
                if check == -5 :
                    bool = True
                    return bool
                else :
                    bool = False

    if player is white :
        # check horizontal
        for i in range (5) :
            check = 0
            if 0 <= x - i <= 13 :
                for j in range (5) :
                    check += color_matrix[y][x - i + j]
                if check == 5 :
                    bool = True
                    return bool
                else :
                    check = 0
                    bool = False
        # check vertical
        for i in range (5) :
            check = 0
            if 0 <= y - i <= 13 :
                for j in range (5) :
                    check += color_matrix[y - i + j][x]
                if check == 5 :
                    bool = True
                    return bool
                else :
                    check = 0
                    bool = False
        # check for dialogue 1
        for i in range (5) :
            check = 0
            if 0 <= x - i <= 13 and 0 <= y - i <= 13 :
                for j in range (5) :
                    check += color_matrix[y - i + j][x - i + j]
                if check == 5 :
                    bool = True
                    return bool
                else :
                    bool = False
        # check for dialogue 2
        for i in range (5) :
            check = 0
            if 0 <= x - i <= 13 and 5 <= y + i <= 13 :
                for j in range (5) :
                    check += color_matrix[y + i - j][x - i + j]
                if check == 5 :
                    bool = True
                    return bool
                else :
                    bool = False
    return bool


def start_game () :
    global running
    running = True


# game loop
while running :
    screen.fill (orange)

    for event in pygame.event.get () :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :
            record_the_pos (event.pos)
            if game_over (event.pos, player) :
                running = False

    draw_the_board ()
    add_coin ()

    # limit the fps
    fps = pygame.time.Clock ()
    fps.tick (40)

    pygame.display.update ()
