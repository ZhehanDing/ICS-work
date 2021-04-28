from chat_utils import *
import json
import pygame
from Window import *

class ClientSM :
    def __init__ (self, s) :
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s  # socket for the current client
        self.matrix_for_game2 = []
        self.color = (0, 0, 0)
        self.turn = 'my turn'
        self.round = 0
        self.win = ''
        self.one_more = ''

    def set_state (self, state) :
        self.state = state

    def get_state (self) :
        return self.state

    def set_myname (self, name) :
        self.me = name

    def get_myname (self) :
        return self.me

    def connect_to (self, peer) :
        msg = json.dumps ({"action" : "connect", "target" : peer})
        mysend (self.s, msg)
        response = json.loads (myrecv (self.s))
        if response["status"] == "success" :
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response["status"] == "busy" :
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self" :
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else :
            self.out_msg += 'User is not online, try again later\n'
        return (False)

    def disconnect (self) :
        msg = json.dumps ({"action" : "disconnect"})
        mysend (self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc (self, my_msg, peer_msg) :
        """
        :param my_msg:
        :param peer_msg:
        :return: self.out_msg: which will be displayed on the client side
        """
        self.out_msg = ''
        # ==============================================================================
        # Once logged in, do a few things: get peer listing, connect, search
        # And, of course, if you are so bored, just go
        # This is event handling instate "S_LOGGEDIN"
        # ==============================================================================
        if self.state == S_LOGGEDIN :
            # todo: can't deal with multiple lines yet
            if len (my_msg) > 0 :

                if my_msg == 'q' :
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time' :
                    mysend (self.s, json.dumps ({"action" : "time"}))
                    time_in = json.loads (myrecv (self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who' :
                    mysend (self.s, json.dumps ({"action" : "list"}))
                    logged_in = json.loads (myrecv (self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c' :
                    peer = my_msg[1 :]
                    peer = peer.strip ()
                    if self.connect_to (peer) == True :
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else :
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?' :
                    term = my_msg[1 :].strip ()
                    mysend (self.s, json.dumps ({"action" : "search", "target" : term}))
                    search_rslt = json.loads (myrecv (self.s))["results"].strip ()
                    if (len (search_rslt)) > 0 :
                        self.out_msg += search_rslt + '\n\n'
                    else :
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1 :].isdigit () :
                    poem_idx = my_msg[1 :].strip ()
                    mysend (self.s, json.dumps ({"action" : "poem", "target" : poem_idx}))
                    poem = json.loads (myrecv (self.s))["results"]
                    if (len (poem) > 0) :
                        self.out_msg += poem + '\n\n'
                    else :
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                elif my_msg[0 :5] == 'game2' :
                    peer = my_msg[5 :]
                    peer = peer.strip ()
                    self.color = (0, 0, 0)
                    self.state = S_GAMING2
                    self.turn = 'my turn'
                    mysend (self.s, json.dumps (
                        {"action" : "game2", "from" : self.me, 'with' : peer}))
                    if self.connect_to (peer) :
                        self.out_msg += 'You can play game2 with' + self.peer + 'now'
                    else :
                        self.out_msg += 'Connection unsuccessful\n'
                elif my_msg == 'game1' :
                    main()
                    self.out_msg += menu

                else :
                    self.out_msg += menu

            if len (peer_msg) > 0 :
                try :
                    peer_msg = json.loads (peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str (err)
                    return self.out_msg

                if peer_msg["action"] == "connect" :
                    # ----------your code here------#
                    print (peer_msg)
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

                if peer_msg['action'] == 'game2' :
                    print (peer_msg)
                    self.peer = peer_msg['from']
                    self.out_msg += 'Game2 request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer + '\nNow, you can play game2 with' + self.peer
                    self.state = S_GAMING2
                    self.color = (255, 255, 255)
                    self.turn = 'not my turn'
                    # ----------end of your code----#

        # ==============================================================================
        # Start chatting, 'bye' for quit
        # This is event handling instate "S_CHATTING"
        # ==============================================================================
        elif self.state == S_CHATTING :
            if len (my_msg) > 0 :  # my stuff going out
                mysend (self.s, json.dumps ({"action" : "exchange", "from" : "[" + self.me + "]", "message" : my_msg}))
                if my_msg == 'bye' :
                    self.disconnect ()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len (peer_msg) > 0 :  # peer's stuff, coming in
                # ----------your code here------#
                peer_msg = json.loads (peer_msg)
                if peer_msg["action"] == "connect" :
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect" :
                    self.out_msg += peer_msg["message"]
                    self.state = S_LOGGEDIN
                else :
                    self.out_msg += peer_msg["from"] + peer_msg["message"]
                # ----------end of your code----#
            if self.state == S_LOGGEDIN :
                # Display the menu again
                self.out_msg += menu

        # gaming: exchange the position through server
        elif self.state == S_GAMING2 :
            # whole code of game2
            pygame.init ()

            # screen, caption, and icon
            screen = pygame.display.set_mode ((720, 720))
            icon = pygame.image.load ('Doraemon.png')
            pygame.display.set_icon (icon)
            if self.color == (0, 0, 0) :
                pygame.display.set_caption ('Gobang （Black)')
            else :
                pygame.display.set_caption ('Gobang （White)')
            running = True
            black = (0, 0, 0)
            white = (255, 255, 255)
            orange = (255, 97, 0)

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
                    matrix_white[i].append ([0 , 0])
                    matrix_black[i].append ([0 , 0])

            def record_the_pos (pos, color) :
                """

                :param color: color of the grid
                :type pos: list
                """
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
                        matrix_black[times2][times1][0] = grid_x
                        matrix_black[times2][times1][1] = grid_y
                        color_matrix[times2][times1] = -1
                    if color == white :
                        matrix_white[times2][times1][0] = grid_x
                        matrix_white[times2][times1][1] = grid_y
                        color_matrix[times2][times1] = 1

            def add_coin () :
                for i in range(len(matrix_white)):
                    for j in matrix_white[i]:
                        if j[0] != 0 and j[1] != 0:
                            pygame.draw.circle(screen , white , (j[0] , j[1]) , 15)
                for i in range(len(matrix_black)):
                    for j in matrix_black[i]:
                        if j[0] != 0 and j[1] != 0:
                            pygame.draw.circle(screen , black , (j[0] , j[1]) , 15)

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

            def one_more_or_over () :
                font = pygame.font.Font (None, 70)
                choice_text1 = font.render (self.win ,  1, white)
                choice_text2 = font.render('Press LEFT to leave' , 1 , white)
                choice_text3 = font.render('Press RIGHT to play again' , 1 , white)
                screen.blit (choice_text1, (36, 36))
                screen.blit (choice_text2, (36, 136))
                screen.blit (choice_text3, (36, 236))
            while running :
                screen.fill (orange)
                font = pygame.font.Font (None, 30)
                text = font.render (self.turn + ' Press SPACE to refresh', 1, white)
                screen.blit (text, (0, 0))

                for event in pygame.event.get () :
                    if event.type == pygame.QUIT :
                        running = False
                        self.state = S_LOGGEDIN
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if self.turn == 'my turn' :
                            pos = list (event.pos)
                            self.turn = 'not my turn'
                            record_the_pos (pos, self.color)
                            if game_over (pos, self.color) :
                                self.turn = 'over'
                                self.win = 'you win'
                                mysend (self.s, json.dumps (
                                    {'action' : 'move', 'from' : self.me, 'position' : event.pos,
                                     'with' : self.peer, 'color' : self.color, 'state' : 'over' , 'one more' : self.one_more}))
                            else :
                                mysend (self.s, json.dumps (
                                    {'action' : 'move', 'from' : self.me, 'position' : event.pos,
                                     'with' : self.peer, 'color' : self.color, 'state' : 'not over' , 'one more' : self.one_more}))
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_SPACE :
                            if self.turn == 'not my turn' :
                                mysend (self.s, json.dumps ({'action' : 'refresh'}))
                                response = json.loads (myrecv (self.s))
                                if response['state'] == 'over' :
                                    self.win = 'you lose'
                                    self.turn = 'over'
                                else :
                                    if color_matrix != response['color'] :
                                        self.turn = 'my turn'
                                        matrix_white = response['white']
                                        matrix_black = response['black']
                                        color_matrix = response['color']
                            elif self.turn == 'over' :
                                mysend (self.s, json.dumps ({'action' : 'refresh'}))
                                response = json.loads (myrecv (self.s))
                                if self.one_more != '' and response['player1'] != '' and response['player2'] != '':
                                    if self.color == (0, 0, 0) :
                                        if self.one_more != response['player2'] :
                                            running = False
                                            self.state = S_LOGGEDIN
                                        else:
                                            if self.one_more == 'yes':
                                                matrix_white = response['white']
                                                matrix_black = response['black']
                                                color_matrix = response['color']
                                                if self.win == 'you win' :
                                                    self.turn = 'not my turn'
                                                else :
                                                    self.turn = 'my turn'
                                            elif self.one_more == 'no' :
                                                running = False
                                                self.state = S_LOGGEDIN
                                    else :
                                        if self.one_more != response['player1'] :
                                            running = False
                                            self.state = S_LOGGEDIN
                                        elif self.one_more == 'yes' :
                                            matrix_white = response['white']
                                            matrix_black = response['black']
                                            color_matrix = response['color']
                                            if self.win == 'you win' :
                                                self.turn = 'not my turn'
                                            else :
                                                self.turn = 'my turn'
                                        elif self.one_more == 'no' :
                                            running = False
                                            self.state = S_LOGGEDIN
                        elif event.key == pygame.K_LEFT and self.turn == 'over' :
                            self.one_more = 'no'
                            mysend (self.s, json.dumps (
                                {'action' : 'move', 'from' : self.me, 'position' : '',
                                 'with' : self.peer, 'color' : self.color, 'state' : 'over',
                                 'one more' : self.one_more}))
                        elif event.key == pygame.K_RIGHT and self.turn == 'over' :
                            self.one_more = 'yes'
                            mysend (self.s, json.dumps (
                                {'action' : 'move', 'from' : self.me, 'position' : '',
                                 'with' : self.peer, 'color' : self.color, 'state' : 'over',
                                 'one more' : self.one_more}))
                draw_the_board ()

                add_coin ()
                # limit the fps
                fps = pygame.time.Clock ()
                fps.tick (40)
                # display over message
                if self.turn == 'over' :
                    one_more_or_over ()
                pygame.display.update ()




        # ==============================================================================
        # invalid state
        # ==============================================================================
        else :
            self.out_msg += 'How did you wind up here??\n'
            print_state (self.state)
        return self.out_msg
