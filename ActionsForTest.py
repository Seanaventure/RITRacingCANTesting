"""
this is the actions class which completes the actions from the command line.
"""
import serial
import time
import xlwt
import datetime
from collections import namedtuple

from queue import Queue


class arduino_actions():

    msg_line = 1
    arduinoData = None
    doInfiniteLog = False
    doSend=False
    threadActive = False
    commandQueue = Queue() #Queue that contains commands
    command = namedtuple('command', 'cmd args')
    arduino_com = None
    baudrate = None
    view = None
    filter_active = False
    #test = namedtuple('test', 'test_name test_send test_timeout test_check')
    test = namedtuple('test', 'test_name test_op test_data test_timeout')

    filter_item = namedtuple('Filter', ['item', 'type'])
    filters = []

    def __init__(self, arudino_com, baudrate, view):
        self.arduino_com = arudino_com
        self.baudrate = baudrate
        self.view = view

    def send(self, msg):
        self.view.printMsg("Sent: " + msg + "\n")
        self.write_arduino((msg.strip('\n')).encode('utf-8'))

    def write_arduino(self, msg):
        self.arduinoData.write(msg)

    def send_multiple(self, filename):
        with open(filename) as file:
            self.send_Mult(file.readlines())

    def send_Mult(self, msgs):
        #if self.doSend:
        for msg in msgs:
            if self.doSend:
                if msg[0:5] == "delay":
                    delay_time = float(msg[6:])
                    time.sleep(delay_time)
                else:
                    self.send(msg)
                    time.sleep(0.003)

    def get(self, msgNum):
        self.arduinoData.write('LOG'.encode('utf-8'))
        f = open("results.txt", "w+")
        for i in range(int(msgNum)):
            get_msg = self.formattedRead(True)
            if get_msg != "":
                self.view.printMsg(get_msg.strip('\n'))
                f.write(get_msg)
        self.arduinoData.write('IDL'.encode('utf-8'))
        f.close()

    def infiniteLog(self, doPrint):
        self.doInfiniteLog = True
        file = open("results.txt", "a")
        self.arduinoData.write('LOG'.encode('utf-8'))
        while self.doInfiniteLog:
            get_msg = self.formattedRead(True)
            if get_msg != "":
                file.write(get_msg)
                if doPrint:
                    self.view.printMsg(get_msg)
            self.handleCommands()
        file.close()
        #self.arduinoData.write('IDL'.encode('utf-8'))


    def formattedRead(self, timeStamp):
        get_msg = self.arduinoData.readline()
        msg_txt = (get_msg.decode("utf-8")).strip(' \t\n\r')
        if self.filter_active and not self.filter_text(msg_txt):
            return ""
        if msg_txt != "":
            msg_txt = "0" + msg_txt.upper()
            if timeStamp:
                msg_txt = msg_txt + "   " + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f') + "\n"
        return msg_txt

    def filter_text(self, msg):
        if msg != "":
            for val in self.filters:
                split = msg.split()
                if val.type == "id":
                    if split[0] == val.item:
                        return True
                elif val.type == "msg":
                    if split[1] == val.item:
                        return True
        return False

    def remove_filter(self, to_remove):
        for val in self.filters:
            if val.item == to_remove:
                self.filters.remove(val)

    def exec_tests(self, filename):
        print("Doing tests")
        self.view.printMsg("-------------Test------------\n")
        test_list = self.read_test_file(filename)
        if test_list == "fnf":
            return
        for test in test_list:
            if self.doSend:
                print(self.doSend)
                curr_test_name = test.test_name
                if test.test_op == "send":
                    self.send_Mult(test.test_data)
                elif test.test_op == "check":
                    result = self.check_responses(test.test_data, test.test_timeout)
                    if result != "success":
                        self.view.printMsg("Failed test: " + curr_test_name + "\n failed on: " + result + "\n")
                    else:
                        self.view.printMsg("Test: " + curr_test_name + " succeeded \n")

    def check_responses(self, response_list, timeout):
        got_all_messages = False
        start_time = time.time()
        while not got_all_messages and (time.time()-start_time) <= timeout:
            received_msg = self.formattedRead(False).strip('|')
            msg_to_remove = []
            # To compare each message we need to split the ID and message into their respective
            # hex values
            if received_msg != "":
                id = received_msg.split(' ')[0]
                msg = received_msg.split(' ')[1]
                self.view.printMsg("received: " + received_msg + "\n")
                for i in range(len(response_list)):
                    check_id = response_list[i].split(' ')[0]
                    check_msg = response_list[i].split(' ')[1]
                    msg_match = True
                    if check_id == id:
                        for j in range(len(msg)):
                            if check_msg[j] != "X":
                                if check_msg[j] != msg[j]:
                                    msg_match = False
                        if msg_match:
                            msg_to_remove.append(response_list[i])
                for i in msg_to_remove:
                    response_list.remove(i)
                # This line will remove a response from a list if it is in the response list
                # response_list[:] = [checkMsg for checkMsg in response_list if not (int(checkMsg.split(' ')[0], 16) == idVal
                #                                                                    and int(checkMsg.split(' ')[1], 16) == msgVal)]
        if len(response_list) == 0:
            return "success"
        else:
            return response_list[0]


    def read_test_file(self, filename):
        tests = []
        try:
            with open(filename) as test_line:
                in_test = False
                in_sending = False
                in_checking = False
                msg_to_send = []
                msg_to_check = []
                test_name = ""
                timeout = 1
                for line in test_line.readlines():
                    split = line.strip().split(',')
                    if len(split) > 0:
                        if split[0][0:2] != "//":
                            if in_test:
                                if in_sending:
                                    if split[0][1:len(split[0]) - 1] != "/send":
                                        if split[0][0:3] == "SND" or split[0][0:3] == "del":
                                            msg_to_send.append(split[0][0:24].strip())
                                    else:
                                        tests.append(self.test(test_name=test_name, test_op="send", test_data=msg_to_send, test_timeout=0))
                                        msg_to_send = []
                                        in_sending = False
                                elif in_checking:
                                    if split[0][1:len(split[0]) - 1] != "/check":
                                        check = split[0][0:20]
                                        msg_to_check.append(check)
                                    else:
                                        tests.append(self.test(test_name=test_name, test_op="check", test_data=msg_to_check, test_timeout=timeout))
                                        in_checking = False
                                        msg_to_check = []
                                elif split[0][1:len(split[0]) - 1] == "send":
                                    in_sending = True
                                elif split[0][1:] == "check":
                                    in_checking = True
                                    timeout = float(split[1][8:len(split[1]) - 1])
                                elif split[0][1:len(split[0]) - 1] == "/test":
                                    in_test = False
                                    msg_to_send = []
                                    msg_to_check =[]
                            else:
                                if split[0][1:] == "test":
                                    test_name = split[1][10:len(split[1]) - 2]
                                    in_test = True
            return tests
        except:
            self.view.printMsg("File not found \n")
            return "fnf"



    def idle(self):
        self.view.printMsg("Idle\n")
        self.arduinoData.write('IDL'.encode('utf-8'))

    def log_loop(self):
        self.write_arduino('LOG'.encode())
        with open("results.txt", "w+") as file:
            while True:
                msg = self.formattedRead(True)
                file.write(msg)
                self.view.printMsg(msg.strip('\n'))

    def add_filter(self, filter_item, filter_type):
        self.filters.append(self.filter_item(item=filter_item, type=filter_type))

    def toggle_filters(self):
        if self.filter_active:
            self.filter_active = False
        else:
            self.filter_active = True

    def handleCommands(self):
        if not self.commandQueue.empty():
            sent_command = self.commandQueue.get()
            if sent_command.cmd == "getN":
                self.get(sent_command.args[0])
            elif sent_command.cmd == "send":
                self.send(sent_command.args[0])
            elif sent_command.cmd == "sendMult":
                self.doSend = True
                self.send_multiple(sent_command.args[0])
            elif sent_command.cmd == "getCancel":
                self.doInfiniteLog = False
            elif sent_command.cmd == "getAll":
                self.get(-1)
            elif sent_command.cmd == "getBackground":
                if not self.doInfiniteLog:
                    self.infiniteLog(sent_command.args[0])
            elif sent_command.cmd == "execTests":
                self.doSend= True
                self.exec_tests(sent_command.args[0])
            elif sent_command.cmd == "cancelSend":
                self.doSend=False
            return True
        else:
            return False

    def run(self):
        self.arduinoData = serial.Serial(self.arduino_com, self.baudrate, timeout=0.5)
        self.threadActive = True
        while self.threadActive:
            self.handleCommands()
