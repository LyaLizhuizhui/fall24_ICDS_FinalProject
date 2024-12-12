#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
#implementation
from tkinter import messagebox
from chat_utils import *
import json
import logic

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300,
                             bg = "#FFFFFF")
        # create a Label
        self.pls = Label(self.login,
                       bg = "#FFFFFF", 
                       fg = "#000000",
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Bahnschrift 14 bold")
          
        self.pls.place(relheight = 0.13,
                       relx = 0.2, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               bg = "#FFFFFF", 
                               fg = "#000000",
                               text = "Name: ",
                               font = "Bahnschrift 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             bg = "#b3cde0",
                             fg = "#011f4b",
                             font = "Bahnschrift 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Bahnschrift 14 bold", 
                         bg = "#196ba0",
                         fg = '#FFFFFF',
                         command = lambda: self.goAhead(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
  
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title(name+"'s Chatroom")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#FFFFFF")
        self.labelHead = Label(self.Window,
                               bg = "#03396c", 
                               fg = "#FFFFFF",
                               text = self.name ,
                               font = "Bahnschrift 14 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#196ba0")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#FFFFFF",
                             fg = "#000000",
                             font = "Bahnschrift 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.8,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#03396c",
                                 height = 75)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#b3cde0",
                              fg = "#011f4b",
                              font = "Bahnschrift 12")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.73,
                            relheight = 0.03,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "SEND",
                                font = "Bahnschrift 12 bold", 
                                width = 20,
                                bg = "#19A092",
                                fg = "#FFFFFF",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.03, 
                             relwidth = 0.22)
        
        ##################### implementation: game button ###################
        self.buttonGame = Button(self.labelBottom, 
                                  text='Game',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#e8bb23",
                                  fg = "#FFFFFF",
                                  # command = lambda : self.sendButton("game")
                                  command = self.game
                                  )
        
        self.buttonGame.place(relx = 0.01,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### game button end ###################

        ##################### implementation: time button ###################
        self.buttonTime = Button(self.labelBottom, 
                                  text='Time',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#196ba0",
                                  fg = "#FFFFFF",
                                  command = lambda : self.sendButton("time")
                                  #command = self.time
                                  )
        
        self.buttonTime.place(relx = 0.135,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### time button end ###################

        ##################### implementation: contacts button ###################
        self.buttonContacts = Button(self.labelBottom, 
                                  text='Contact',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#196ba0",
                                  fg = "#FFFFFF",
                                  command = lambda : self.sendButton("who")
                                  #command = self.contacts
                                  )
        
        self.buttonContacts.place(relx = 0.26,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### contacts button end ###################

        ##################### implementation: connect button ###################
        self.buttonConnect = Button(self.labelBottom, 
                                  text='Connect',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#196ba0",
                                  fg = "#FFFFFF",
                                  command = self.connect)
        
        self.buttonConnect.place(relx = 0.385,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### connect button end ###################

        ##################### implementation: history button ###################
        self.buttonHistory = Button(self.labelBottom, 
                                  text='History',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#196ba0",
                                  fg = "#FFFFFF",
                                  command = self.history)
        
        self.buttonHistory.place(relx = 0.51,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### history button end ###################

        ##################### implementation: sonnet button ###################
        self.buttonSonnet = Button(self.labelBottom, 
                                  text='Sonnet',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#196ba0",
                                  fg = "#FFFFFF",
                                  command= self.sonnet)
        
        self.buttonSonnet.place(relx = 0.635,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### sonnet button end ###################

        ##################### implementation: quit button ###################
        self.buttonQ = Button(self.labelBottom, 
                                  text='QUIT',
                                  font = "Bahnschrift 12 bold", 
                                  width = 20,
                                  bg = "#eb6841",
                                  fg = "#FFFFFF",
                                  command=self.Window.destroy)
        
        self.buttonQ.place(relx = 0.77,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.22)
        ##################### quit button end ###################

        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
    #################implementation: display window #################
    def time(self):
        msg = json.dumps({"action":"time"})
        self.send(msg)
        time_in = json.loads(self.recv())["results"]
        messagebox.showinfo('Time', \
                            "Time is: " + time_in)
        
    def contacts(self):
        msg = json.dumps({"action":"list"})
        self.send(msg)
        logged_in = json.loads(self.recv())["results"]
        messagebox.showinfo('Contacts', \
                            "Here are all the users in the system:\n" + logged_in)
    
    #######################end implementation#######################

    #################implementation: connect window #################
    def connect(self):
        self.connect_window = Tk()
        self.connect_window.title("Connect")
        self.connect_window.resizable(width = False, 
                            height = False)
        self.connect_window.configure(width = 400,
                            height = 300,
                            bg = "#FFFFFF")

        self.top_frame = Frame(self.connect_window)
        self.bottom_frame = Frame(self.connect_window)

        self.prompt_label = Label(self.top_frame,
                                text='Connect to:',
                                bg = "#FFFFFF", 
                                fg = "#000000",
                                font = "Bahnschrift 12")
        self.entry = Entry(self.top_frame,
                           bg = '#b3cde0',
                           fg = "#011f4b",
                           width=10)

        self.prompt_label.pack(side='left')
        self.entry.pack(side='left')

        self.connect_button = Button(self.bottom_frame,
                                text='Connect',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                #command = lambda : self.sendButton("c "+self.entry.get()))
                                command = self.connect_with)
                                #command = lambda : [self.sendButton("c "+self.entry.get()),
                                #    self.connect_window.destroy])
        self.quit_button = Button(self.bottom_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.connect_window.destroy)

        self.connect_button.pack(side='left')
        self.quit_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()

        #kinter.connectloop()

    def connect_with(self):
        self.sendButton("c "+self.entry.get())
        self.connect_window.withdraw()
    #######################end implementation#######################

    #################implementation: history window #################
    def history(self):
        self.history_window = Tk()
        self.history_window.title("Chat History")
        self.history_window.resizable(width = False, 
                            height = False)
        self.history_window.configure(width = 400,
                            height = 300,
                            bg = "#FFFFFF")

        self.top_frame = Frame(self.history_window)
        self.bottom_frame = Frame(self.history_window)

        self.prompt_label = Label(self.top_frame,
                                text='Who said this:',
                                bg = "#FFFFFF", 
                                fg = "#000000",
                                font = "Bahnschrift 12")
        self.entry = Entry(self.top_frame,
                           bg = '#b3cde0',
                           fg = "#011f4b",
                           width=10)

        self.prompt_label.pack(side='left')
        self.entry.pack(side='left')

        self.history_button = Button(self.bottom_frame,
                                text='Search',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                #command = lambda : self.sendButton("? "+self.entry.get()))
                                command = self.search_history)
                                #command = lambda : [self.sendButton("? "+self.entry.get()),
                                #    self.history_window.destroy])
        self.quit_button = Button(self.bottom_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.history_window.destroy)

        self.history_button.pack(side='left')
        self.quit_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()

        #kinter.historyloop()

    def search_history(self):
        self.sendButton("? "+self.entry.get())
        self.history_window.withdraw()
    #######################end implementation#######################

    #################implementation: sonnet window #################
    def sonnet(self):
        self.sonnet_window = Tk()
        self.sonnet_window.title("Sonnet")
        self.sonnet_window.resizable(width = False, 
                            height = False)
        self.sonnet_window.configure(width = 400,
                            height = 300,
                            bg = "#FFFFFF")

        self.top_frame = Frame(self.sonnet_window)
        self.bottom_frame = Frame(self.sonnet_window)

        self.prompt_label = Label(self.top_frame,
                                text='Sonnet #:',
                                bg = "#FFFFFF", 
                                fg = "#000000",
                                font = "Bahnschrift 12")
        self.entry = Entry(self.top_frame,
                           bg = '#b3cde0',
                           fg = "#011f4b",
                           width=10)

        self.prompt_label.pack(side='left')
        self.entry.pack(side='left')

        self.sonnet_button = Button(self.bottom_frame,
                                text='Get',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                #command = lambda : self.sendButton("p"+self.entry.get()))
                                command = self.get_sonnet)
                                #command = lambda : [self.sendButton("p"+self.entry.get()),
                                #    self.sonnet_window.destroy])
        self.quit_button = Button(self.bottom_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.sonnet_window.destroy)

        self.sonnet_button.pack(side='left')
        self.quit_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()
        #kinter.sonnetloop()

    def get_sonnet(self):
        self.sendButton("p"+self.entry.get())
        self.sonnet_window.withdraw()
    #######################end implementation#######################

    ##################### implementation: 2048 game window ###################
    def game(self):   
        self.game_window = Tk()
        self.game_window.title("2048 GAME")
        self.game_window.resizable(width = False, 
                            height = False)
        self.game_window.configure(width = 600,
                            height = 800,
                            bg = "#FFFFFF")
        self.top_frame = Frame(self.game_window) # top
        self.mid_frame = Frame(self.game_window) # mid: canvas
        self.bottom_frame = Frame(self.game_window) # bottom

        # Text
        self.text_label = Label(self.top_frame,
                                text='2048            ',
                                bg = "#FFFFFF", 
                                fg = "#000000",
                                font = "Bahnschrift 24 bold")
        self.text_label.pack(side='left')

        # Quit Button
        self.quit_button = Button(self.top_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.game_window.destroy)
        self.quit_button.pack(side='right')

        # Canvas
        self.canvas = Canvas(self.mid_frame,
                            bg = '#cce6ff',
                            width = 400,
                            height = 400,
                            )
        self.canvas.pack()
        self.draw_grid()

        # Description / rule
        self.rule_label = Label(self.bottom_frame,
                                text='Combine matching tiles on a grid by sliding them \nto create larger numbers, aiming to reach 2048.',
                                bg = "#FFFFFF", 
                                fg = "#000000",
                                font = "Bahnschrift 12")
        self.rule_label.pack(side='left')

        # Up Button
        self.up_button = Button(self.bottom_frame,
                            text='↑',
                            font = "Bahnschrift 12 bold", 
                            width = 3,
                            bg = "#196ba0",
                            fg = "#FFFFFF",
                            command = self.up
                        )

        self.up_button.place(relx = 0.7, 
                       rely = 0.2)

        # Down Button
        self.down_button = Button(self.bottom_frame,
                            text='↓',
                            font = "Bahnschrift 12 bold", 
                            width = 3,
                            bg = "#196ba0",
                            fg = "#FFFFFF",
                            command = self.down
                        )
        self.up_button.place(relx = 0.7, 
                       rely = 0.8)

        # Left Button
        self.left_button = Button(self.bottom_frame,
                            text='←',
                            font = "Bahnschrift 12 bold", 
                            width = 3,
                            bg = "#196ba0",
                            fg = "#FFFFFF",
                            command= self.left
                        )
        self.up_button.place(relx = 0.6, 
                       rely = 0.5)
        # Right Button
        self.right_button = Button(self.bottom_frame,
                            text='→',
                            font = "Bahnschrift 12 bold", 
                            width = 3,
                            bg = "#196ba0",
                            fg = "#FFFFFF",
                            command = self.right
                        )
        self.up_button.place(relx = 0.8, 
                       rely = 0.5)

        self.up_button.pack(side = "top",padx=1,pady=2)
        self.down_button.pack(side = "bottom",padx=1,pady=2)
        self.left_button.pack(side = "left",padx=3,pady=2)
        self.right_button.pack(side = "right",padx=3,pady=2)

        self.top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()

    def up(self):
        # call the move_up function
        mat, flag = logic.move_up(mat)

        # get the current state and print it
        status = logic.get_current_state(mat)
        print(status)

        # if game not over then continue
        # and add a new two
        if flag:
            if(status == 'GAME NOT OVER'):
                logic.add_new_2(mat)

        # else break the loop 
            else:
                break
        #else
        else:
            print("Invalid move, no tiles moved. Try again.")


    def down(self):
        mat, flag = logic.move_down(mat)
        status = logic.get_current_state(mat)
        print(status)
        if flag:
            if(status == 'GAME NOT OVER'):
                logic.add_new_2(mat)
            else:
                break
        else:
            print("Invalid move, no tiles moved. Try again.")

    
    def left(self):
        mat, flag = logic.move_left(mat)
        status = logic.get_current_state(mat)
        print(status)
        if flag:
            if(status == 'GAME NOT OVER'):
                logic.add_new_2(mat)
            else:
                break
        else:
            print("Invalid move, no tiles moved. Try again.")

    def right(self):
        mat, flag = logic.move_right(mat)
        status = logic.get_current_state(mat)
        print(status)
        if flag:
            if(status == 'GAME NOT OVER'):
                logic.add_new_2(mat)
            else:
                break
        else:
            print("Invalid move, no tiles moved. Try again.")

        ##################### 2048 game window end ###################

    def draw_grid(self):
        # Vertical lines
        for i in range(5):
            self.canvas.create_line(i * 100, 0, i * 100, 400, fill="#3399ff")
        # Horizontal lines
        for i in range(5):
            self.canvas.create_line(0, i * 100, 400, i * 100, fill="#3399ff")
        

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()
