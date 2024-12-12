from chat_utils import *
from game import TicTacToe
import json

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nYou are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nUser is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nCannot talk to yourself (sick)\n'
        else:
            self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nUser is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nYou are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSee you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nTime is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nHere are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nConnect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' + search_rslt + '\n\n'
                    else:
                        self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' + poem + '\n\n'
                    else:
                        self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSonnet ' + poem_idx + ' not found\n\n'
                
                elif my_msg == "game":
                    mysend(self.s, json.dumps({"action": "game"}))
                    self.out_msg += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEntering game mode :)"
                    self.state = S_GAMING
                
                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nRequest from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)

                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"

                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN

                elif peer_msg["action"] == "game":
                    role = peer_msg["role"]
                    opponent = peer_msg["opponent"]
                    self.role = role
                    self.out_msg += f"Starting game as {self.role} against {opponent}.\n"
                    self.state = S_GAMING
                
                elif peer_msg["action"] == "error":
                    self.out_msg += peer_msg["msg"] + "\n"
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"] + '\n'

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        elif self.state == S_GAMING:
            game = TicTacToe(role = self.role)
            # assign roles
            # if self.role == "X":
            #     game.player_turn = player_x 
            # else:
            #     game.player_turn = player_O
            game.run()
            self.state = S_LOGGEDIN
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
