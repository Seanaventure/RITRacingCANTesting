from tkinter import *
from tkinter import ttk


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
"""
The preceding lines create the three main widgets in our program: the entry where we type the number of feet in, a 
label where we put the resulting number of meters, and the calculate button that we press to perform the calculation.

For each of the three widgets, we need to do two things: create the widget itself, and then place it onscreen. 
All three widgets, which are 'children' of our content window are created as instances of one of Tk's themed widget 
classes. At the same time as we create them, we give them certain options, such as how wide the entry is, the text to 
put inside the Button, etc. The entry and label each are assigned a mysterious "textvariable"; we'll see what that does 
shortly.

If the widgets are just created, they won't automatically show up on screen, because Tk doesn't know how you want them 
to be placed relative to other widgets. That's what the "grid" part does. Remembering the layout grid for our 
application, we place each widget in the appropriate column (1, 2 or 3), and row (also 1, 2 or 3). The "sticky" option 
says how the widget would line up within the grid cell, using compass directions. So "w" (west) means anchor the widget 
to the left side of the cell, "we" (west-east) means anchor it to both the left and right sides, and so on.
"""
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()