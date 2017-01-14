import threading as th

import tkinter as tk

class BasicGui(th.Thread):
#class BasicGui():
    title = ''
    ttext = ''
    fileName = ''
    window = None

    def __init__(self, title, ttext, fileName):
        th.Thread.__init__(self)

        self.title = title
        self.ttext = ttext
        self.fileName = fileName

    def run(self):
        self.window = tk.Tk()
        self.window.title(self.title)
        self.window.geometry('800x500')

        lblClassName = tk.Label(self.window, text=self.fileName, anchor=tk.NW, justify=tk.LEFT, pady=20)
        lblClassName.pack()

        #w = Text(self.window, anchor=W, justify=LEFT)

        txtFunctionAnotation = tk.Text(self.window)
        txtFunctionAnotation.insert(tk.END, ''.join(self.ttext))
        txtFunctionAnotation.pack(expand=True, fill='both')

        #lblFunctionAnotation = Label(self.window, text=''.join(self.ttext), anchor=NW, justify=LEFT)
        #lblFunctionAnotation.pack()
        btn = tk.Button(self.window, text='Exit ', command=self.closeWindow)
        btn.pack(expand=tk.NO)

        #btnText = Button(win, text=self.ttext, command=self.closeWindow)
        #btnText.pack(expand=YES, fill=BOTH)

        self.window.mainloop()

    def closeWindow(self):
        self.window.destroy()
        
        
