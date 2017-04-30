from tkinter import *
from tkinter import ttk
import pafy
import os

class MainFrame(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.createWindow()

    def createWindow(self):
        self.master.title("Youtube Downloader")
        self.pack(fill=BOTH,expand=1)

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = Menu(menubar)
        aboutmenu = Menu(menubar)

        filemenu.add_command(label="New")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save As")
        filemenu.add_command(label="Edit")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.do_exit)

        aboutmenu.add_command(label="About Us")
        aboutmenu.add_command(label="Help",command =self.newFrame)

        menubar.add_cascade(label="File",menu=filemenu)
        menubar.add_cascade(label="About", menu=aboutmenu)

        input_label = Label(self,text="YouTube Video Url:").pack()
        self.input_box = Entry(self,width=100)
        self.input_box.bind('<Return>',self.startFetch)
        self.input_box.pack()
        self.inp_btn = Button(self,text="Fetch",command = self.startFetch)
        self.inp_btn.pack()
        self.inp_btn.bind('<Return>',self.startFetch)
        self.firsttime = True
        self.video_title=Label(self)
        self.randomLabel=Label(self)
        self.video_duration=Label(self)
        self.buttons=[]
    def newFrame(self):
        frm = Frame(self)
        frm.pack(fill=BOTH,expand=1)
    def clearButtons(self):
        for button in self.buttons:
            button.destroy()

    def startFetch(self,*args):
        self.clearButtons()
        self.url = self.input_box.get()
        video = pafy.new(self.url)
        self.video_title ["text"]="Title-"+video.title
        self.video_title.pack()
        self.video_duration["text"]="Duration-"+video.duration
        self.video_duration.pack()
        self.randomLabel["text"]="Downloads:"
        self.randomLabel.pack()
        self.buttons = []
        streams = video.streams

        for stream in streams:
            size = str(stream.get_filesize()/10**6).split(".")[0]+"."+str(stream.get_filesize()/10**6).split(".")[1][:2]
            self.buttons.append(Button(self,width=20,text=stream.resolution+" "+stream.extension+" "+size+"MB",command=lambda stream=stream:self.downloadfrom(stream)))
        for button in self.buttons:
            button.pack()

    def downloadfrom(self,stream):
        videoname = stream.title+"."+stream.extension
        if not "Downloads" in os.listdir():
            os.mkdir("Downloads")
        if not videoname in os.listdir('./Downloads'):
            stream.download(filepath="Downloads/")
        os.startfile(os.getcwd()+"/Downloads")


    def do_exit(self):
        exit()

root = Tk()
root.geometry("500x500")
mainFrame = MainFrame(root)
root.mainloop()
