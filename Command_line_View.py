"""
The command line file which sees what the user inputs then parses that information which will lead to a specific method that will do what
the user wants to do. hello
"""
from ActionsForTest import *
from collections import namedtuple

import threading

#SND
class commandline():

    controller = None
    backgroundLogger = None
    currentlyThreading = False


    def __init__(self, controller):
        self.controller = controller

    def printMsg(self, msg):
        print(msg)
    def idle(self):

        while 1:
            print("Welcome to CAN tester type help to see a list of commands")
            request = input(">")
            #self.actions.send(request)
            direction = request.split(" ")
            if direction[0] == "SND":
                if(len(direction) == 3):
                    if direction[1] == "-m":
                        #print("Gonna send mult")
                        self.controller.send_mult(direction[2])
                        # self.actions.send_Mult(direction[2])
                    elif len(direction[2]) == 16:
                        self.controller.send(direction[1] + " " + direction[2])
                        # self.actions.send(request)
                    else:
                        print("Not valid message. Try again")
                else:
                    print("Not valid message. Try again")
            elif direction[0] == "GET":
                if(len(direction) == 2):
                    if direction[1] == "-b":
                        if not self.currentlyThreading:
                            self.controller.get_background()
                    elif direction[1] == "-c":
                        self.controller.cancel_log()
                        #self.actions.idle()
                    else:
                        self.controller.getN(direction[1])
                        #self.actions.get(direction[1])
                else:
                    print("Not valid, please specify how many you would like")
            elif direction[0] == "LOG":
                self.controller.log()
            elif direction[0] == "IDLE":
                self.controller.idle()
            elif direction[0] == "help":
                print("SND [ID] [MSG] will send a message over the CAN bus")
                print("SND -m [filename] will send a list of commands located in a specific file")
                print("GET [N] will log the next N received messages on the screen and output to a text file")
                print("GET -b will log all messages to a text file in the background")
                print("GET -c will cancel a background log")
                print("LOG will continuously log messages. Not recommended because you cant leave this mode")

    def handle_print(self):
        print("Nothing")

    def run(self):
        self.idle()