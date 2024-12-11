#!/usr/bin/env python3
# -*- coding: utf-8 -*-
####################### time method: line 288####################
####################### proc: line 347 ##########################
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
        
        ##################### implementation: time button ###################
        self.buttonGame = Button(self.labelBottom, 
                                  text='Game',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#e8bb23",
                                  fg = "#FFFFFF",
                                  command = lambda : self.sendButton("game")
                                  #command = self.game
                                  )
        
        self.buttonGame.place(relx = 0.01,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.11)
        ##################### time button end ###################

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
    
    #################implementation: connect window #################
    def connect(self):
        self.input_window = Tk()
        self.input_window.title("Connect")
        self.input_window.resizable(width = False, 
                            height = False)
        self.input_window.configure(width = 400,
                            height = 300,
                            bg = "#FFFFFF")

        self.top_frame = Frame(self.input_window)
        self.bottom_frame = Frame(self.input_window)

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

        self.input_button = Button(self.bottom_frame,
                                text='Connect',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = lambda : self.sendButton("c "+self.entry.get()))
                                #command = self.connect_with)
                                #command = lambda : [self.sendButton("c "+self.entry.get()),
                                #    self.input_window.destroy])
        self.quit_button = Button(self.bottom_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.input_window.destroy)

        self.input_button.pack(side='left')
        self.quit_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()

        #kinter.inputloop()

    def connect_with(self):
        lambda : self.sendButton("c "+self.entry.get())
        self.input_window.destroy
    #######################end implementation#######################

    #################implementation: history window #################
    def history(self):
        self.input_window = Tk()
        self.input_window.title("Chat History")
        self.input_window.resizable(width = False, 
                            height = False)
        self.input_window.configure(width = 400,
                            height = 300,
                            bg = "#FFFFFF")

        self.top_frame = Frame(self.input_window)
        self.bottom_frame = Frame(self.input_window)

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

        self.input_button = Button(self.bottom_frame,
                                text='Search',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = lambda : self.sendButton("? "+self.entry.get()))
                                #command = self.search_history)
                                #command = lambda : [self.sendButton("? "+self.entry.get()),
                                #    self.input_window.destroy])
        self.quit_button = Button(self.bottom_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.input_window.destroy)

        self.input_button.pack(side='left')
        self.quit_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()

        #kinter.inputloop()

    def search_history(self):
        lambda : self.sendButton("? "+self.entry.get())
        self.input_window.destroy
    #######################end implementation#######################

    #################implementation: sonnet window #################
    def sonnet(self):
        self.input_window = Tk()
        self.input_window.title("Sonnet")
        self.input_window.resizable(width = False, 
                            height = False)
        self.input_window.configure(width = 400,
                            height = 300,
                            bg = "#FFFFFF")

        self.top_frame = Frame(self.input_window)
        self.bottom_frame = Frame(self.input_window)

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

        self.input_button = Button(self.bottom_frame,
                                text='Get',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = lambda : self.sendButton("p"+self.entry.get()))
                                #command = self.get_sonnet)
                                #command = lambda : [self.sendButton("p"+self.entry.get()),
                                #    self.input_window.destroy])
        self.quit_button = Button(self.bottom_frame,
                                text='Quit',
                                font = "Bahnschrift 12 bold", 
                                width = 10,
                                bg = "#196ba0",
                                fg = "#FFFFFF",
                                command = self.input_window.destroy)

        self.input_button.pack(side='left')
        self.quit_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()

        #kinter.inputloop()

    def get_sonnet(self):
        lambda : self.sendButton("p"+self.entry.get())
        self.input_window.destroy
    
    #######################end implementation#######################

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
            #json_msg = json.loads(peer_msg)
            #if json_msg["action"] == "time":
            #     continue
            if self.socket in read:
                peer_msg = self.recv()
            if self.my_msg == 'time' and self.my_msg == 'who':
                continue
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
            # if (len(self.my_msg) > 0 or len(peer_msg) > 0) and self.my_msg != 'time' and self.my_msg != 'who':
            #     # print(self.system_msg)
            #     self.system_msg += self.sm.proc(self.my_msg, peer_msg)
            #     self.my_msg = ""
            #     self.textCons.config(state = NORMAL)
            #     self.textCons.insert(END, self.system_msg +"\n\n")      
            #     self.textCons.config(state = DISABLED)
            #     self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()
