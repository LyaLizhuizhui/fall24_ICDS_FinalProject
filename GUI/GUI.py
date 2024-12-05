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
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Bahnschrift 14 bold")
          
        self.pls.place(relheight = 0.13,
                       relx = 0.2, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Bahnschrift 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
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
            #######################implementation: name not valid#######################
            else:
                self.login.destroy()
                self.login
            #######################end implementation#######################
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
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                               bg = "#B9DDCF", 
                               fg = "#252C29",
                               text = self.name ,
                               font = "Bahnschrift 14 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#A8B9D5")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#F1F8F5",
                             fg = "#252C29",
                             font = "Bahnschrift 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.8,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#A8B9D5",
                                 height = 75)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#F1F8F5",
                              fg = "#252C29",
                              font = "Bahnschrift 13")
          
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
                                bg = "#A8B9D5",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.03, 
                             relwidth = 0.22)
        
        ##################### implementation: time button ###################
        self.buttonTime = Button(self.labelBottom, 
                                  text='Time',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#A8B9D5",
                                  #command = lambda : self.sendButton("time")
                                  command = self.time
                                  )
        
        self.buttonTime.place(relx = 0.01,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.13)
        ##################### time button end ###################

        ##################### implementation: contacts button ###################
        self.buttonContacts = Button(self.labelBottom, 
                                  text='Contacts',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#A8B9D5",
                                  #command = lambda : self.sendButton("who")
                                  command = self.contacts
                                  )
        
        self.buttonContacts.place(relx = 0.16,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.13)
        ##################### contacts button end ###################

        ##################### implementation: connect button ###################
        self.buttonConnect = Button(self.labelBottom, 
                                  text='Connect',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#A8B9D5",
                                  command=self.Window.destroy)
        
        self.buttonConnect.place(relx = 0.31,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.13)
        ##################### connect button end ###################

        ##################### implementation: history button ###################
        self.buttonHistory = Button(self.labelBottom, 
                                  text='History',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#A8B9D5",
                                  command=self.Window.destroy)
        
        self.buttonHistory.place(relx = 0.46,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.13)
        ##################### history button end ###################

        ##################### implementation: sonnet button ###################
        self.buttonSonnet = Button(self.labelBottom, 
                                  text='Sonnet',
                                  font = "Bahnschrift 10", 
                                  width = 20,
                                  bg = "#A8B9D5",
                                  command=self.Window.destroy)
        
        self.buttonSonnet.place(relx = 0.61,
                            rely = 0.038,
                            relheight = 0.03, 
                            relwidth = 0.13)
        ##################### sonnet button end ###################

        ##################### implementation: quit button ###################
        self.buttonQ = Button(self.labelBottom, 
                                  text='QUIT',
                                  font = "Bahnschrift 12 bold", 
                                  width = 20,
                                  bg = "#A8B9D5",
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
    
    #################implementation: entry window #################
    
    
    #######################end implementation#######################

    #################implementation: select window #################
    
    
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
            #print(self.my_msg)
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
