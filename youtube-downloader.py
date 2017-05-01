from tkinter import *
from tkinter.ttk import *
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

        filemenu.add_command(label="Exit", command=self.do_exit)

        menubar.add_cascade(label="File",menu=filemenu)

        input_label = Label(self,text="YouTube Video Url:").pack()
        self.input_box = Entry(self,width=100)
        self.input_box.bind('<Return>',self.startFetch)
        self.input_box.pack()
        self.input_box.focus_set()

        self.inp_btn = Button(self,text="Fetch",command = self.startFetch)
        self.inp_btn.pack()

        self.inp_btn.bind('<Return>',self.startFetch)
        self.video_title=Label(self)
        self.randomLabel=Label(self)
        self.video_duration=Label(self)
        self.downloadStatus = Label( self )
        self.progbar = Progressbar(self)
        self.buttons=[]

    def clearButtons(self):
        for button in self.buttons:
            button.destroy()

    def startFetch(self,*args):
        self.inp_btn["text"] = "Fetching...Please Wait"
        root.update()
        self.clearButtons()
        self.progbar.destroy()
        self.downloadStatus["text"]=""
        self.url = self.input_box.get()
        video = pafy.new(self.url)
        self.video_title ["text"]="Title-"+video.title
        self.video_title.pack()
        self.video_duration["text"]="Duration-"+video.duration
        self.video_duration.pack()
        self.randomLabel["text"]="Downloads:"
        self.randomLabel.pack()
        self.buttons = []
        self.progbar = Progressbar(self,orient="horizontal",mode="determinate")
        self.downloadStatus.pack()
        self.progbar.pack()

        streams = video.streams

        for stream in streams:
            size = str(stream.get_filesize()/10**6).split(".")[0]+"."+str(stream.get_filesize()/10**6).split(".")[1][:2]
            self.buttons.append(Button(self,width=40,text=stream.resolution+" "+stream.extension+" "+size+"MB",command=lambda stream=stream:self.downloadfrom(stream)))
        for button in self.buttons:
            button.pack()

        self.inp_btn["text"] = "Fetch"
        root.update()

    def downloadfrom(self,stream):
        self.downloadStatus["text"] = "Downloading - "
        videoname = stream.title+"."+stream.extension
        if not "Downloads" in os.listdir():
            os.mkdir("Downloads")
        if not videoname in os.listdir('./Downloads'):
            stream.download(filepath="Downloads/",quiet=False,callback=self.mycb)
        os.startfile(os.getcwd()+"/Downloads")
        self.downloadStatus["text"]="Download Completed"

    def mycb(self,total, recvd, ratio, rate, eta):
        kbps = str(rate*0.125).split(".")
        speed = kbps[0]+"."+kbps[1][:2]
        raw_time_min = int(eta/60)
        raw_time_sec = int(eta%60)
        str_time = str(raw_time_min)+"min:"+str(raw_time_sec)+"sec"
        self.downloadStatus["text"]="Downloading -"+str(ratio*100)[:4]+"% "+speed+" kB/s "+str_time
        self.progbar["value"]=ratio*100
        root.update()
        
    def do_exit(self):
        exit()

root = Tk()
root.geometry("500x500")
mainFrame = MainFrame(root)
root.mainloop()
