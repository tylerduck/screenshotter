import random
from tkinter import Tk, Label, Button, Entry, IntVar, StringVar, DISABLED, NORMAL, END, W, E, Radiobutton
from tkinter import filedialog
from six.moves.urllib.request import urlopen
from screenshotter import collect_png

class ScreenshotGUI:
    def __init__(self, master):
        self.master = master
        master.title("URL Screenshotter")

        self.message = "Please enter a url and select a folder to save the screenshots"
        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(master, textvariable=self.label_text)
        self.folder = None

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master)

        self.select_folder = Button(master, text="Select Folder", command=self.get_filename)
        self.enter_button = Button(master, text="Run", command=self.run, state=NORMAL)

        self.label.grid(row=0, column=0, columnspan=2, sticky=W+E)
        self.entry.grid(row=1, column=0, columnspan=2, sticky=W+E)
        
        self.selector = IntVar()
        self.button0 = Radiobutton(master, text="All Pages", variable=self.selector, value=0)
        self.button1 = Radiobutton(master, text="Main Pages", variable=self.selector, value=1)
        self.button2 = Radiobutton(master, text="Just this page", variable=self.selector, value=2)
        self.button0.grid(row=2, column=0)
        self.button1.grid(row=2, column=1)
        self.button2.grid(row=2, column=2)

        self.select_folder.grid(row=3, column=0)
        self.enter_button.grid(row=3, column=1)

    def get_filename(self):
        self.folder = filedialog.askdirectory()

    def validate(self, new_text):
        return True

    def run(self):
        self.url = str(self.entry.get())
        try:
            urlopen(self.url)
        except Exception as e:
            self.message = "Please enter a valid url\nFull Error:\n" + e
            self.label_text.set(self.message)
            return

        if not self.folder:
            self.message = "Please select a save folder"
            self.label_text.set(self.message)
            return

        self.select_folder.configure(state=DISABLED)
        self.enter_button.configure(state=DISABLED)
        while True:
            try:
                collect_png(self.url, self.folder, self.selector.get())
                break
            except:
                pass

root = Tk()
my_gui = ScreenshotGUI(root)
root.mainloop()