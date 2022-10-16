import os
import tkinter as tk
from tkinter import filedialog
import fitz
import io
from PIL import ImageTk, Image
from functools import partial

class Reader:
    window = tk.Tk()
    frame = tk.Frame(window)
    window.title("Reader")
    window.state('zoomed')
    window.configure(bg="#718085")


    dataFolder = ""
    folders = []
    settings = []
    series = {}
    selected = ""
    indexToBook = {}
    theme = ""

    def readSettings(self):
        try:
            with open('settings') as f:
                self.settings = f.readlines()
                if len(self.settings[0].split(">")) == 2:
                    self.dataFolder = self.settings[0].split(">")[1]
        except:
            try:
                f = open('settings', 'x')
                f.close()
            except:
                pass
            with open('settings', 'w') as f:
                f.write("datapath>\n")

    def updateSettings(self):
        map(lambda x: x + "\n", self.settings)
        with open('settings', 'w') as f:
            f.writelines(self.settings)

    def getFolders(self):
        self.folders = []
        self.series = {}
        try:
            self.folders = os.listdir(self.dataFolder)

        except:
            print("No Library Folder Found")
            return
        for i in self.folders:
            self.series[i] = os.listdir(self.dataFolder + "/" + i)
            for j in self.series[i]:
                Reader.convertBook(r, self.dataFolder + "/" + i, j)
        Reader.displaySeries(r)

    def convertBook(self, path, book):

        src = path + "/src"
        if not os.path.exists(src):
            os.mkdir(path + "/src")
        try:
            os.mkdir(src+"/"+book[:-4])
        except:
            pass
        volPath = src+"/"+book[:-4]

        pdffile = path+"/"+book


        try:
            with fitz.open(pdffile) as doc:
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)

                count = len(doc)

                if len(os.listdir(volPath)) != count:
                    print(f"\t <Converting Book: {book}>")
                    for i in range(count):
                        val = f"{volPath}/image_{i + 1}.png"
                        page = doc.load_page(i)
                        pix = page.get_pixmap(matrix=mat)
                        pix.save(val)
        except:
            pass



    def getDir(self):
        self.dataFolder = filedialog.askdirectory(initialdir=self.dataFolder)
        print("Updated Data Folder: " + self.dataFolder)
        if len(self.settings) == 0:
            self.settings = [""]
        self.settings[0] = "datapath>" + self.dataFolder
        Reader.updateSettings(r)
        Reader.getFolders(r)

    def selectBook(self, i, j):

        b, s = self.indexToBook.get((i, j))
        print("Selected: " + b)
        bookPath = self.dataFolder + "/" + s + "/" + b
        Reader.loadBook(r, bookPath)

    def loadBook(self, book):
        for i in self.window.pack_slaves():
            try:
                i.pack_forget()
            except:
                pass
        backB = tk.Button(self.window, text="<<BACK", command=lambda: Reader.goBack(r), bg="#9cc9db")
        backB.pack()
        print(book)

        #pageL = tk.Label(image=test)
        #pageL.pack()

    def turnPage(self, i):
        pass

    def goBack(self):
        for i in self.window.pack_slaves():
            try:
                i.destroy()
            except:
                pass
        self.selected = ""
        Reader.start(r)

    def displaySeries(self):
        for c in self.frame.grid_slaves():
            try:
                c.grid_forget()
            except:
                pass
        i = 1
        for series in self.series.keys():
            j = 1
            sB = tk.Label(self.frame, text=" " + series + " ", font=("Segoe UI", 15), bg="#718085", fg="#EEEEEE")
            sB.grid(row=0, column=i)
            for book in self.series[series]:
                if book.endswith(".pdf"):
                    self.indexToBook[(i, j)] = (book, series)
                    bB = tk.Button(self.frame, text=j, height=1, width=5, command=partial(Reader.selectBook, r, i, j))
                    bB.grid(row=j, column=i)
                    j += 1
            i += 1

    def start(self):

        Reader.readSettings(r)
        Reader.getFolders(r)

        print("Started with Data Folder: " + self.dataFolder)

        Reader.displaySeries(r)

        dirB = tk.Button(self.window, text="Change Library Directory >", command=lambda: Reader.getDir(r), bg="#9cc9db")
        dirB.pack()

        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.configure(bg="#718085")

        self.window.mainloop()


if __name__ == '__main__':
    r = Reader()
    r.start()
