import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import *
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
import GUI
import ClientHandler
ClientHandler = ClientHandler.ClientHandler
Notepad = GUI.Notepad


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.container = container
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def add_frame(self, host, doc):
        host_gui = Notepad(self.container, self, host)
        host.connect_doc(doc)
        host_gui.grid(row=0, column=0, sticky="nsew")
        host_gui.tkraise()
        host_gui.run()

    def pass_reference(self, host):
        frame = self.frames['PageTwo']
        frame.set_host(host)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the SolaceIDE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        text_field = Text(self, height=1, width=20)

        def event():
            controller.show_frame("PageTwo")
            name = text_field.get(1.0, END)
            host = ClientHandler(name)
            host.is_host = True
            host.attempt_connection()
            controller.pass_reference(host)

        button2 = tk.Button(self, text="ConfirmUsername",
                            command=event)
        text_field.pack()
        button2.pack()


class PageTwo(tk.Frame):

    host: ClientHandler

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter a document code",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.text_field = Text(self, height=1, width=20)
        button = tk.Button(self, text="Host Doc",
                           command=self.host_file)
        button2 = tk.Button(self, text="Join Doc",
                           command=self.join_file)
        self.text_field.pack()
        button.pack()
        button2.pack()

    def set_host(self, host):
        self.host = host

    def host_file(self):
        self.host.is_host = True
        doc_name = self.text_field.get(1.0, END)
        self.controller.add_frame(self.host, doc_name)

    def join_file(self):
        self.host.is_host = False
        doc_name = self.text_field.get(1.0, END)
        self.controller.add_frame(self.host, doc_name)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
