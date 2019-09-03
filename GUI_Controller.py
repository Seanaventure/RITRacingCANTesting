from ActionsForTest import *
from tkinter import *
from GUIView import GUI_View
from Command_line_View import commandline
import sys
import threading
import time


class GUI_Controller:
    actions = None
    GUI_view = None

    def __init__(self, root):
        if sys.argv[1] == "gui":
            self.GUI_view = GUI_View(root, self)
        else:
            self.GUI_view = commandline(self)

        self.actions = arduino_actions(sys.argv[2], sys.argv[3], self.GUI_view)
        readThread = threading.Thread(target=self.actions.run)
        readThread.start()
        if sys.argv[1] == "cmd":
            self.GUI_view.run()

        if sys.argv[1] == "gui":
            self.periodic_call()
        print("Set up")

    def exec_tests(self, filename):
        self.actions.commandQueue.put(self.actions.command("execTests", [filename]))

    def send_mult(self, filename):
        self.actions.commandQueue.put(self.actions.command("sendMult", [filename]))

    def end(self):
        self.actions.threadActive = False

    def send(self, msg):
        split_msg = msg.split()
        if len(split_msg[0]) == 3:
            if len(split_msg[1]) == 16:
                self.actions.commandQueue.put(self.actions.command("send", ["SND " + msg.upper()]))
            else:
                self.GUI_view.printMsg("MSG is invalid, must be 16 hex chars")
        else:
            self.GUI_view.printMsg("ID is invalid, must be 3 hex characters")


    def cancel_log(self):
        self.actions.commandQueue.put(self.actions.command("getCancel", []))

    def get_background(self):
        self.actions.commandQueue.put(self.actions.command("getBackground", [False]))

    def getN(self, n):
        inputCommand = self.actions.command("getN", [n])
        self.actions.commandQueue.put(inputCommand)

    def log(self):
        self.actions.commandQueue.put(self.actions.command("getBackground", [True]))

    def idle(self):
        self.actions.idle()

    def end_send(self):
        self.actions.doSend=False
        print(self.actions.doSend)

    def remove_filter(self, item):
        self.actions.remove_filter(item)

    def toggle_filters(self):
        self.actions.toggle_filters()

    def new_filter(self, msg, type):
        if type == 1:
            if len(msg) == 3:
                self.actions.add_filter(msg, "id")
            else:
                self.GUI_view.printMsg("Filter ID invalid, must be 3 hex chars.")
        elif type == 2:
            if len(msg) == 16:
                self.actions.add_filter(msg, "msg")
            else:
                self.GUI_view.printMsg("Filter MSG invalid, must be 16 hex chars.")

    def periodic_call(self):
        self.GUI_view.handle_print()
        self.GUI_view.root.after(200, self.periodic_call)

root = Tk()
controller = GUI_Controller(root)
if sys.argv[1] == "gui":
    root.mainloop()
