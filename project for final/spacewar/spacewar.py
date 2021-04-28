import sys, pygame
import random
from pygame import mixer


def main () :
    # initialize
    pygame.init ()

    # set up the screen
    size = width, length = 600, 600
    screen = pygame.display.set_mode (size)

    running = True

    color = R, G, B = 0, 0, 0

    # set the caption
    pygame.display.set_caption ("Space War")
    icon = pygame.image.load ("Doraemon.png")
    pygame.display.set_icon (icon)

    # background
    background = pygame.image.load ("background.jpg")
    # music
    mixer.music.load ('Cornfield Chase - Hans Zimmer.mp3')
    mixer.music.play (-1)

    # record and show the score
    score_value = 0
    font = pygame.font.Font ('freesansbold.ttf', 32)

    # player
    playerimg = pygame.image.load ("spaceship.png")
    p_x, p_y = 284, 568
    p_x_change = 0

    def player (x, y) :
        screen.blit (playerimg, (x, y))

    # monster
    monsterimg = []
    m_x = []
    m_y = []
    m_x_change = []
    m_y_change = []
    num_of_monsters = 8
    for i in range (num_of_monsters) :
        monsterimg.append (pygame.image.load ('monster.png'))
        m_x.append (random.randint (0, 568))
        m_y.append (random.randint (50, 250))
        m_x_change.append (0.2)
        m_y_change.append (40)

    def monster (x, y, i) :
        screen.blit (monsterimg[i], (x, y))

    # meteor
    meteors = []
    t_x = []
    t_y = []
    t_y_change = []
    num_of_meteor = 2
    for i in range (num_of_meteor) :
        meteors.append (pygame.image.load ('asteroid.png'))
        t_x.append (random.randint (100, 500))
        t_y.append (50)
        t_y_change.append (0.2)

    def meteor (x, y, i) :
        screen.blit (meteors[i], (x, y))

    # bullet
    class bullet :
        def __init__ (self) :
            self.state = ''

    bulletimg = pygame.image.load ("bullet.png")
    b_x = 0
    b_y = 568
    b_x_change = 0
    b_y_change = 0.4
    b_state = bullet()
    b_state.state = 'ready'

    def fire_bullet (x, y) :
        b_state.state = 'fire'
        screen.blit (bulletimg, (x + 8, y))

    # detect a collision
    def is_collision (x1, y1, x2, y2) :
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        if distance <= 27 :
            return True
        else :
            return False

    def display_score () :
        score = font.render ('Score:' + str (score_value), True, (255, 255, 255))
        screen.blit (score, (10, 10))

    # game over
    font2 = pygame.font.Font ('freesansbold.ttf', 64)

    def game_over () :
        over = font2.render ("Game over!!!", True, (255, 0, 0))
        screen.blit (over, (100, 268))

    # game loop
    while running :
        screen.fill (color)
        screen.blit (background, (-200, -200))
        for event in pygame.event.get () :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT :
                    p_x_change = 0.5
                if event.key == pygame.K_LEFT :
                    p_x_change = -0.5
                if event.key == pygame.K_SPACE :
                    if b_state.state == 'ready' :
                        b_x = p_x
                        fire_bullet (b_x, b_y)
                        bullet_sound = mixer.Sound ('bullet2.mp3')
                        bullet_sound.set_volume (0.2)
                        bullet_sound.play ()
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT :
                    p_x_change = 0

        # movement of the player
        p_x += p_x_change
        if p_x <= 0 or p_x >= 568 :
            p_x -= p_x_change
        player (p_x, p_y)

        # movement of the monster
        for i in range (num_of_monsters) :
            if m_y[i] > 536 :
                for j in range (num_of_monsters) :
                    m_y[j] = 2000
                game_over ()
                mixer.music.stop ()
                break
            else :
                m_x[i] += m_x_change[i]
                if m_x[i] <= 0 :
                    m_x_change[i] = m_x_change[i] * (-1)
                    m_y[i] += m_y_change[i]
                if m_x[i] >= 568 :
                    m_x_change[i] = m_x_change[i] * (-1)
                    m_y[i] += m_y_change[i]
                monster (m_x[i], m_y[i], i)
        # movement of the meteor
        if score_value >= 10 :
            for i in range (num_of_meteor) :
                if is_collision (t_x[i], t_y[i], p_x, p_y) :
                    game_over ()
                    for j in range (num_of_monsters) :
                        m_y[j] = 2000
                    for j in range (num_of_meteor) :
                        t_y_change[j] = 0
                        t_x[j] = 2000
                    boomsound = mixer.Sound ('boom.mp3')
                    boomsound.set_volume (0.2)
                    boomsound.play ()
                    mixer.music.stop ()
                    break
                else :
                    t_y[i] += t_y_change[i]
                    if t_y[i] >= 580 :
                        t_x[i] = random.randint (100, 500)
                        t_y[i] = random.randint (50, 100)
                        score_value += 1
                    else :
                        meteor (t_x[i], t_y[i], i)

        # movement of the bullet
        if b_state.state == "fire" :
            fire_bullet (b_x, b_y)
            b_y -= b_y_change
            if b_y <= 0 :
                b_y = 568
                b_state.state = 'ready'

        # detect the collision between monster and the bullet
        for i in range (num_of_monsters) :
            if is_collision (m_x[i], m_y[i], b_x, b_y) :
                boomsound = mixer.Sound ('boom.mp3')
                boomsound.set_volume (0.2)
                boomsound.play ()
                b_x = 0
                b_y = p_y
                b_state.state = 'ready'
                m_x[i] = random.randint (0, 568)
                m_y[i] = random.randint (50, 200)
                m_x_change[i] += 0.02
                score_value += 1
        display_score ()
        pygame.display.update ()
