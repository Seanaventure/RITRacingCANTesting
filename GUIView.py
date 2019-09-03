from tkinter import *
from tkinter import ttk
from tkinter import messagebox


from queue import Queue
doLog = False

class GUI_View:

    print_Queue = Queue() #Queue that contains commands
    logger = None
    controller = None
    root = None

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.title("RIT Formula CAN tester")
        root.iconbitmap('rit2.ico')
        log_frame = ttk.Frame(root, padding="0 0 40 40")
        log_frame.grid(column=1, row=2, rowspan=12, columnspan=1)

        filter_frame = ttk.Frame(root).grid(column=4, row=2, rowspan=12, columnspan=1)
        ttk.Label(root, text="Log").grid(column=1, row=1, sticky=(W, E))
        ttk.Label(root, text="Actions").grid(column=2, row=1, columnspan=2)
        ttk.Label(root, text="Filters").grid(column=3, row=1, columnspan=2)

        ttk.Button(root, text="Log data", command=self.logData).grid(column=2, row=2, columnspan=2, pady=0)
        ttk.Button(root, text="Stop logging", command=self.stopLog).grid(column=2, row=3, columnspan=2, pady=0)

        id = StringVar()
        msg = StringVar()
        self.logger = Text(log_frame, height=20, width=40)
        self.logger.grid(column=1, row=2, rowspan=6)
        self.logger.config(state=DISABLED)

        radio_button_input = IntVar()
        filter_val = StringVar()
        id_rb = Radiobutton(filter_frame, text="ID", variable=radio_button_input, value=1)
        id_rb.grid(column=4, row=7, rowspan=1, columnspan=1)
        msg_rb = Radiobutton(filter_frame, text="Message", variable=radio_button_input, value=2)
        msg_rb.grid(column=4, row=8, rowspan=1, columnspan=1)
        filter_entry = ttk.Entry(filter_frame, width=3, textvariable=filter_val)
        ttk.Button(filter_frame, text="Apply Filter", command= lambda: self.add_filter(filter_val, filters, radio_button_input)).grid(column=4, row=10, columnspan=2)
        ttk.Button(filter_frame, text="Delete Filter", command= lambda: self.remove_filter(filters)).grid(column=4, row=11, columnspan=2)
        check_value = IntVar()
        Checkbutton(filter_frame, text="Filters Active", variable=check_value, command=self.toggle_filters).grid(column=4, row=12, rowspan=1, columnspan=1)
        filter_entry.grid(column=4, row=9, stick=(W, E))

        filters = Listbox(filter_frame)
        filters.grid(column=4, row=2, rowspan=5, columnspan=1)

        scrollbar = Scrollbar(log_frame)
        self.logger.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.logger.yview)
        scrollbar.grid(ipady=140, column=2, row=2, rowspan=2, columnspan=6)

        ttk.Label(root, text="ID(Hex):").grid(column=2, row=4, sticky=(W + E), pady=0)
        id_entry = ttk.Entry(root, width=3, textvariable=id)
        id_entry.grid(column=2, row=5, stick=(W, E), pady=0)
        id_entry.focus()

        ttk.Label(root, text="MSG(Hex)/Filename:").grid(column=2, row=6, sticky=(W, E))
        msg_entry = ttk.Entry(root, width=16, textvariable=msg)
        msg_entry.grid(column=2, row=7, stick=(W, E))
        ttk.Button(root, text="Send data", command= lambda: self.sendData(id, msg)).grid(column=2, row=8, columnspan=1)
        ttk.Button(root, text="Send Multiple", command= lambda: self.send_mult(msg)).grid(column=2, row=9, columnspan=1)
        ttk.Button(root, text="Execute Tests", command= lambda: self.exec_tests(msg)).grid(column=2, row=10, columnspan=1)
        ttk.Button(root, text="End Sending", command= lambda: self.stop_send()).grid(column=2, row=11, columnspan=1)

        for child in root.winfo_children(): child.grid_configure(padx=20, pady=5)

    def logData(self):
        self.controller.log()
        print("Gonna log stuff")

    def exec_tests(self, filename):
        self.controller.exec_tests(filename.get())

    def sendData(self, id, msg):
        snd_msg = id.get() + " " + msg.get().strip()
        self.controller.send(snd_msg)

    def toggle_filters(self):
        self.controller.toggle_filters()

    def add_filter(self, item, filters, type):
        filters.insert(END, item.get())
        self.controller.new_filter(item.get(), type.get())

    def stopLog(self):
        self.controller.cancel_log()

    def stop_send(self):
        self.controller.end_send()

    def send_mult(self, msg):
        self.controller.send_mult(msg.get())

    def remove_filter(self, filters):
        item = filters.get(ANCHOR)
        self.controller.remove_filter(item)
        filters.delete(ANCHOR)

    def handle_print(self):
        while self.print_Queue.qsize():
            try:
                msg = self.print_Queue.get()
                self.logger.config(state=NORMAL)
                self.logger.insert(END, msg)
                self.logger.see(END)
                self.logger.config(state=DISABLED)
            except Queue.empty():
                pass

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.end()
            self.root.destroy()

    def printMsg(self, msg):
        self.print_Queue.put(msg)