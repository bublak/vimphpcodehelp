import threading

from Tkinter import *

class BasicGui(threading.Thread):
    title = ''
    ttext = ''
    fileName = ''
    window = None

    def __init__(self, title, ttext, fileName):
        threading.Thread.__init__(self)

        self.title = title
        self.ttext = ttext
        self.fileName = fileName

    def run(self):
        self.window = Tk()
        self.window.title(self.title)
        self.window.geometry('700x400')

        lblClassName = Label(self.window, text=self.fileName, anchor=NW, justify=LEFT, pady=20)
        lblClassName.pack()

        #w = Text(self.window, anchor=W, justify=LEFT)

        txtFunctionAnotation = Text(self.window)
        txtFunctionAnotation.insert(END, ''.join(self.ttext))
        txtFunctionAnotation.pack()

        #lblFunctionAnotation = Label(self.window, text=''.join(self.ttext), anchor=NW, justify=LEFT)
        #lblFunctionAnotation.pack()
        btn = Button(self.window, text='Exit ', command=self.closeWindow)
        btn.pack(expand=NO)

        #btnText = Button(win, text=self.ttext, command=self.closeWindow)
        #btnText.pack(expand=YES, fill=BOTH)

        mainloop()

    def closeWindow(self):
        self.window.destroy()
        
        
