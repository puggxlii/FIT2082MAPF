import sys
#from lazycbs import init

from tkinter import *
from Map import info
import time

class MyCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)


class myFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.text = Text(self, width=20)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_config('constraint', background="#DCE2F1", foreground="black")
        self.text.tag_config('current', background="#EBEBE4", foreground="black")

        self.playButton = Button(self, text='Pause',width=10,height=3, bg='red', fg='black', command=self.play_visualizer)
        self.playButton.pack(side=TOP)

        self.backButton = Button(self, text='<<',width=8,height=2, bg='#EBEBE4', fg='black', command=self.backward)
        self.backButton.pack(side=BOTTOM, padx=5, pady=5)

        self.forwardButton = Button(self, text='>>',width=8,height=2, bg='#EBEBE4', fg='black', command=self.forward)
        self.forwardButton.pack(side=BOTTOM, padx=5, pady=5)

        self.btn = Button(self,text ="inspect AI",command = self.openNewWindow)
        self.btn.pack(pady = 5)

        self.newWindow=None

    def play_visualizer(self):
        global continuePlay,Paused
        if self.playButton["text"] == "Pause":
            self.playButton["text"] = "Play"
            self.playButton["bg"] = "green"
            continuePlay=False

        else:
            self.playButton["text"] = "Pause"
            self.playButton["bg"] = "red"
            continuePlay= True

    def backward(self):
        global continuePlay,t,backward,forward
        self.playButton["text"] = "Play"
        self.playButton["bg"] = "green"
        backward=True
        forward=False
        continuePlay=False

    def forward(self):
        global continuePlay,t,forward,backward
        self.playButton["text"] = "Play"
        self.playButton["bg"] = "green"
        forward=True
        backward=False
        continuePlay=False

    def openNewWindow(self):
        self.newWindow = Toplevel(root)
        self.newWindow.title("Inspect AI")
        self.newWindow.geometry("400x700")
        # Label(self.newWindow,text ="This is a new window").pack()

        self.newframe = Frame(self.newWindow)
        self.newframe.place(x=10, y=20)

        self.t = Text(self.newframe, width=20)
        self.scrollbar = Scrollbar(self.newframe,orient="vertical", command=self.t.yview)
        self.t.configure(yscrollcommand=self.vsb.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.t.pack(side="left")

        self.inputtxt = Entry(self.newWindow,width=5)
        self.inputtxt.pack()

        self.inputtxt1 = Entry(self.newWindow,width=5)
        self.inputtxt1.pack()

        """ print out comparison """
        self.printButton = Button(self.newWindow,text = "see",
                 command = lambda: Info.printInput(self.newframe,the_canvas,self.inputtxt,self.inputtxt1,self.t))
        self.printButton.pack()

def repeater(root):
    global Info,the_canvas,the_frame,t,backward,forward
    t=1
    backwardFlag=False
    while True:

        if backward and t>1:
            t-=1
            Info.move_agents(t,the_canvas,the_frame,True)
            backwardFlag=False
        elif backwardFlag==True:
            pass
        elif forward and t>=1:
            tt=Info.move_agents(t,the_canvas,the_frame,False)
            t+=1
            if tt:
                backwardFlag=True

        elif continuePlay:
            tt=Info.move_agents(t,the_canvas,the_frame,False)
            t+=1
            if tt:
                backwardFlag=True


        forward=False
        backward=False

        root.update()
        time.sleep(0.2)


if __name__=="__main__":
    try:
        addagen=sys.argv[1]
        addmap=sys.argv[2]
        numAgent=int(sys.argv[3])
    except IndexError:
        addagen,addmap,numAgent="test_25.txt","warehouse-10-20-10-2-1.map.ecbs",25
        # addagen,addmap,numAgent="test_2.txt","debug-6-6.map.ecbs",2
    #python run.py test_2.txt debug-6-6.map.ecbs 2

    # addagen=init("../maps/debug-6-6.map.ecbs", "../scenarios/debug-6-6-2-2.scen", 2, [(0, ((-1, -2), (-1, -2)), -2, -100)])
    # with open("agentPath.txt","w") as text_file:
    #     text_file.write(addagen)
    # text_file.close()

    global Info,the_canvas,the_frame,continuePlay,t,backward,forward,newWindow


    Info=info(addagen,addmap,numAgent)

    # Construct a simple root window
    the_canvas   = None
    root = Tk()

    continuePlay,backward,forward = True,False,False

    root.title("Simulation")
    # root.protocol("WM_DELETE_WINDOW",exit)

    the_frame = myFrame(root)
    the_frame.pack(side="right",fill="both")

    the_canvas= MyCanvas(root,width=1630,height=720,bg="#d1d1d1")
    the_canvas.pack(side=LEFT,expand=True,fill=BOTH)



    """a little big, cross platform"""
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # the_canvas.config(width=screen_width, height=screen_height)

    Info.draw_map(the_canvas)
    Info.draw_agents(the_canvas,the_frame)

    repeater(root)

    root.mainloop()

    
