import tkinter as tk
from tkinter import *
import GUI
import ClientHandler
ClientHandler = ClientHandler.ClientHandler
Notepad = GUI.Notepad

text_field = None
client = None
page1 = None
page2 = None

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

def connection_event():
    global client
    name = text_field.get(1.0, END)
    client = ClientHandler("name")
    client.is_host = False
    page1.lift().pack()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       global page1
       page1 = self
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Welcome to the SolaceIDE. Please enter your user name to login.")
       label.pack(fill="both", expand=True)
       label.place(x = 40, y = 80)
       global text_field
       text_field = Text(self, height = 1, width=20)
       text_field.pack(pady=150, padx=5, expand=False)
       b1 = tk.Button(self, text="Confirm", command=connection_event())
       b1.pack(pady=0, padx = 10)
       b1.place(x = 170, y = 180 )

class Page2(Page):
   def __init__(self, *args, **kwargs):
        global page2
        page2 = self
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


        #b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        #b2.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x370")
    root.title("SolaceIDE - Prototype")
    root.mainloop()
