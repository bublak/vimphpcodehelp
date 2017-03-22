import threading as th

import tkinter as tk

class BasicGui(th.Thread):
#class BasicGui():
    title = ''
    ttext = ''
    fileName = ''
    window = None
    ent=None
    txtFunctionAnotation=None
    hintsData=None
    

    def __init__(self, title, ttext, fileName, hintsData=None):
        th.Thread.__init__(self)

        self.title = title
        self.ttext = ttext
        self.fileName = fileName
        self.hintsData = hintsData

    # fetch/filter lines according to searched text in Entry field
    def fetch(self):
        searchText = self.ent.get()

        text=[]
        for hh in self.hintsData:
            text.append('\n= = = = = = = = = =\n')
            text.append(hh + ': \n')
            item = self.hintsData.get(hh)

            content = item.getAllPrintable('\n      ')

            newContent=[]

            for line in content:
                if line.lower().find(searchText.lower()) > -1:
                    newContent.append(line)

            text.extend(newContent)

        self.txtFunctionAnotation.delete('1.0', tk.END)
        self.txtFunctionAnotation.insert(tk.END, ''.join(text))

    def cleanText(self):
        self.ent.delete(0, tk.END)

        self.fetch()

    def run(self):
        self.window = tk.Tk()
        self.window.title(self.title)
        self.window.geometry('800x500')

        lblClassName = tk.Label(self.window, text=self.fileName, anchor=tk.NW, justify=tk.LEFT, pady=20)
        lblClassName.pack()

        if self.hintsData:
            lblEntry = tk.Label(self.window, text='search: ', anchor=tk.NE, justify=tk.LEFT, pady=20)
            lblEntry.pack()

            ent = tk.Entry(self.window)
            #ent.insert(0, '')
            ent.pack(side=tk.TOP, fill=tk.X)
            ent.focus()

            ent.bind('<KeyPress>', (lambda event: self.fetch()))
            ent.bind('<Return>', (lambda event: self.cleanText()))
            self.ent = ent

        #w = Text(self.window, anchor=W, justify=LEFT)

        txtFunctionAnotation = tk.Text(self.window)
        txtFunctionAnotation.insert(tk.END, ''.join(self.ttext))
        txtFunctionAnotation.pack(expand=True, fill='both')

        self.txtFunctionAnotation = txtFunctionAnotation

        #lblFunctionAnotation = Label(self.window, text=''.join(self.ttext), anchor=NW, justify=LEFT)
        #lblFunctionAnotation.pack()
        btn = tk.Button(self.window, text='Exit ', command=self.closeWindow)
        btn.pack(expand=tk.NO)

        #btnText = Button(win, text=self.ttext, command=self.closeWindow)
        #btnText.pack(expand=YES, fill=BOTH)

        self.window.mainloop()

    def closeWindow(self):
        self.window.destroy()
        
        
