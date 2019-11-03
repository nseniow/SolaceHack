import tkinter
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from output import OutputNotepad
import subprocess
import time


class Notepad(tkinter.Frame):
    # variables
    __root: Tk

    # default window width and height
    __thisWidth = 400
    __thisHeight = 400
    __file = None
    __cursors : int

    __client_handler: None
    parent: str

    def __init__(self, parent, root, client_handler, **kwargs):
        # initialization
        tkinter.Frame.__init__(self, parent)
        # set window size (the default is 300x300)
        self.__root = root
        self.parent = parent
        self.__thisTextArea = Text(self.__root)
        self.__thisMenuBar = Menu(self.__root)
        self.__thisFileMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisScrollBar = Scrollbar(self.__thisTextArea)

        self.__client_handler = client_handler
        self.__client_handler.gui = self
        print(self.__client_handler.gui)
        self.__cursors = {}

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # set the window text
        self.__root.title("Untitled - Notepad")

        # center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        self.__root.geometry(
            '%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        # to make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self.__thisTextArea.pack(fill=BOTH, expand=1)

        # add controls (widget)

        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)
        self.__thisRunMenu = Menu(self.__thisMenuBar, tearoff=0)

        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        self.__thisEditMenu.add_command(label="Update code", command=self.menu_request_update)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        self.__thisRunMenu.add_command(label="Run", command=self.__run)
        self.__thisMenuBar.add_cascade(label="Run", menu=self.__thisRunMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

        self.__thisTextArea.bind("<Key>", self.key)

    def menu_request_update(self):
        print("Button been pressed")
        try:
            self.__client_handler.request_update()
        except:
            print("Didn't work")

    def __run(self):
        #self.__saveFile()
        file = (self.__saveFile())
        #file = "C:\\Users\\Nicho\\PycharmProjects\\Hackathon\\fina\\Untitled.java"

        import os
        def compile_java(java_file):
            java_file = java_file.split("/")[-1]
            print(java_file)
            cmd = 'javac ' + java_file
            cmd2 = 'java ' + java_file.split(".")[0]
            print('java ' + java_file.split(".")[0])
            proc = subprocess.Popen(cmd, shell=True)
            # proc2 = subprocess.Popen(cmd2, shell=True, stdout=PIPE)
            # proc2.wait(50000)
            os.system(cmd)
            time.sleep(5)
            apple = os.popen(cmd2).read()
            self.insert_text("15.0", apple)
            #outWindow = OutputNotepad(self.__root, self.parent, apple)

            # outWindow.grid(row=0, column=0, sticky="nsew")
            # outWindow.tkraise()
            # print(apple)

        compile_java(file)

    def key(self, event):
        kp = repr(event.char)[1:-1]
        if kp == '\\x08':
            try:
                self.__client_handler.send(
                    {'name': self.__client_handler.nickname,
                     'target': 'delete',
                     'p1': self.__thisTextArea.index(tkinter.SEL_FIRST),
                     'p2': self.__thisTextArea.index(tkinter.SEL_LAST)})
            except:
                secondPart = self.__thisTextArea.index(tkinter.INSERT).split(".")[1]
                secondPart = str(int(secondPart)-1)
                wholething = self.__thisTextArea.index(tkinter.INSERT).split(".")[0]+"."+secondPart
                self.__client_handler.send({'name': self.__client_handler.nickname,
                                            'target':'delete',
                                        'p1': wholething,'p2': self.__thisTextArea.index(tkinter.INSERT)})
        else:
            if kp == '\\\\':
                kp = '\\'
            if kp == "\\r":
                kp = "\n"
            self.__client_handler.send({'name': self.__client_handler.nickname,
                                            'target':'insert',
                                        'position': self.__thisTextArea.index(tkinter.INSERT),'text':kp})

    def __quitApplication(self):
        self.__root.destroy()
        # exit()

    def __openFile(self):

        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])

        if self.__file == "":
            # no file to open
            self.__file = None
        else:
            # try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisTextArea.insert(1.0, file.read())

            file.close()

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):

        if self.__file == None:
            # save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"), (
                                            "Text Documents", "*.txt")])

            if self.__file == "":
                self.__file = None
            else:
                # try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                print([(x, y) for x, y in zip(self.__thisTextArea.get(1.0, END),
                                              range(len(
                                                  self.__thisTextArea.get(1.0,
                                                                          END))))])
                file.close()
                # change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            print([(x,y) for x, y in zip(self.__thisTextArea.get(1.0, END), range(len(self.__thisTextArea.get(1.0, END))))])
            file.close()
        return self.__file

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

    def check_existing_editors(self, name: str):
        if name in self.__cursors:
            return
        else:
            self.__cursors[name] = 1.0

    def update_cursors(self, name, msg):
        pass

    def get_text(self):
        return self.__thisTextArea.get(1.0, END)

    def set_text(self, text: str):
        self.__thisTextArea.delete(1.0, END)
        self.__thisTextArea.insert(1.0, text)

    def insert_text(self, position, text):
        self.__thisTextArea.insert(position, text)

    def delete_text(self, p1, p2):
        self.__thisTextArea.delete(p1, p2)

# run main application
# notepad = Notepad(None, width=600, height=400)
# notepad.run()
