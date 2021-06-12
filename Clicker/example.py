from game import *
from tkinter import * 
from numberNaming import *
from asyncio import get_event_loop, sleep


result = ""
okay = True
buttons = []

def money_update(self):
    prettyMoney.set("Money: "+nameNumber(self.money))
    for i, button in enumerate(buttons):
        button.configure(state="disabled" if self.money < self.workerList[i].price else "normal")

def levelUp(i):
    instance.buy(i)
    w = instance.workerList[i]
    tkinterVars[i].set(f"{i} | Name: {w.name} | Efficiency: {nameNumber(w.eff)}\n"+
                    f"Level: {nameNumber(w.level)}| Price: {nameNumber(w.price)}")
    print("levelup end")

instance = game(money_update_callback=money_update)

# idk how it works, just copy-pasted frame with scroll
class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

class MainFrame(Frame):
    def __init__(self, root):
        global tkinterVars
        global prettyMoney
        global instance
        global buttons

        Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
    
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        
        Button(self.scrollFrame.viewPort, textvariable=prettyMoney, command=instance.click).grid(row=0, column=0)

        for i, _ in enumerate(tkinterVars):
            buttons.append(Button(self.scrollFrame.viewPort, textvariable=tkinterVars[i], command=lambda i=i: levelUp(i)))
            buttons[i].grid(row=i+1, column=0)

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
    
    def printMsg(self, msg):
        print(msg)

root=Tk()

prettyMoney = StringVar()
prettyMoney.set("Money: 0")

tkinterVars = []

for i, w in enumerate(instance.workerList):
    tkinterVars.append(StringVar())
    if i == 0:
        tkinterVars[i].set(f"{i} | Name: {w.name} | Efficiency: {nameNumber(w.eff)}\n"+
                    f"Level: {nameNumber(w.level)}| Price: {nameNumber(w.price)}")
    else:
        tkinterVars[i].set(f"{i} | Name: {w.name} | Not yet bought\n"+
                    f" Base Efficiency: {nameNumber(w.eff)} | Price: {nameNumber(w.price)} ")

MainFrame(root).pack(side="top", fill="both", expand=True)

root.title("Clicker")

def exiting():
    okay = False
    root.destroy()
    root.quit()

root.protocol("WM_DELETE_WINDOW", exiting)

async def gameloop():
    while okay:
        await sleep(1)
        instance.update()
    loop.stop()

async def mainloop():
    while okay:
        root.update()
        root.update_idletasks()
        await sleep(0.01)
    loop.stop()

loop = get_event_loop()
loop.create_task(gameloop())
loop.create_task(mainloop())
loop.run_forever()
