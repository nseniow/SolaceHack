import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class OutputNotepad(tkinter.Frame):
    # variables

    # default window width and height
    __thisWidth = 300
    __thisHeight = 300

    __root: str

    def __init__(self, root, parent, contents="Failed compilation", **kwargs):
        # initialization
        Frame.__init__(parent)
        self.__root = root

        # set window size (the default is 300x300)

        self.__thisTextArea = Text(self.__root)
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # center the window
        # screenWidth = parent.winfo_screenwidth()
        # screenHeight = parent.winfo_screenheight()
        #
        # left = (screenWidth / 2) - (self.__thisWidth / 2)
        # top = (screenHeight / 2) - (self.__thisHeight / 2)
        #
        # self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        # to make the textarea auto resizable
        # self.__root.grid_rowconfigure(0, weight=1)
        # self.__root.grid_columnconfigure(0, weight=1)

        # add controls (widget)

        self.__thisTextArea.pack(fill=BOTH, expand = 1)
        self.__thisTextArea.insert("1.0", contents)

