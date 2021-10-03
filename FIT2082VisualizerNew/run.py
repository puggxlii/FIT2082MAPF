import sys
#from lazycbs import init

from tkinter import *
from Map import info
import time

class MyCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)

class myFrame2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.playButton = Button(self, text='Pause',width=10,height=3, bg='red', fg='black', command=self.play_visualizer)
        self.playButton.grid(row=0, column=0,columnspan=2,pady=(0,10))
        self.backButton = Button(self, text='<<',width=5,height=3, bg='white', fg='black', command=self.backward)
        self.backButton.grid(row=3, column=0,pady=10)
        self.forwardButton = Button(self, text='>>',width=5,height=3, bg='white', fg='black', command=self.forward)
        self.forwardButton.grid(row=3, column=1,pady=10)
        self.speedUpButton=Button(self, text='<<<',width=5,height=3, bg='white', fg='black', command=lambda:self.speedChange(0.05))
        self.speedUpButton.grid(row=4, column=0,pady=10)
        self.speedDownButton=Button(self, text='>>>',width=5,height=3, bg='white', fg='black', command=lambda:self.speedChange(-0.05))
        self.speedDownButton.grid(row=4, column=1,pady=10)
    """speed up or down"""
    def speedChange(self,change):
        global speedup
        speedup=max(0.001,speedup+change)
    """"""
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

class myFrame(Frame):
    def __init__(self, master,canvas):
        Frame.__init__(self, master)

        """enable user to drag the scene"""
        self.canvas = canvas
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,4000,2000))

        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)
        """"""

        """add menu to root"""
        self.master = master
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Agent Detail",command=self.openNewWindow)
        menu.add_cascade(label="More", menu=fileMenu)
        """"""

        """setup text box, button in main frame"""
        self.text = Text(self, width=20)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_config('constraint', background="#DCE2F1", foreground="black")
        self.text.tag_config('current', background="#EBEBE4", foreground="black")

        # self.playButton = Button(self, text='Pause',width=10,height=3, bg='red', fg='black', command=self.play_visualizer)
        # self.playButton.pack(fill=X,pady=10)
        #
        # self.backButton = Button(self, text='<<',width=5,height=2, bg='#EBEBE4', fg='black', command=self.backward)
        # self.backButton.pack(side=BOTTOM,pady=10)
        # self.forwardButton = Button(self, text='>>',width=5,height=2, bg='#EBEBE4', fg='black', command=self.forward)
        # self.forwardButton.pack(side=BOTTOM,pady=10)
        #
        # self.speedUpButton=Button(self, text='<<<',width=8,height=2, bg='#EBEBE4', fg='black', command=lambda:self.speedChange(0.05))
        # self.speedUpButton.pack(side=BOTTOM, pady=5)
        # self.speedDownButton=Button(self, text='>>>',width=8,height=2, bg='#EBEBE4', fg='black', command=lambda:self.speedChange(-0.05))
        # self.speedDownButton.pack(side=BOTTOM, pady=5)
        """"""

    # """speed up or down"""
    # def speedChange(self,change):
    #     global speedup
    #     speedup=max(0.001,speedup+change)
    # """"""
    """drag function"""
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerP(self,event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self,event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    """"""

    # def play_visualizer(self):
    #     global continuePlay,Paused
    #     if self.playButton["text"] == "Pause":
    #         self.playButton["text"] = "Play"
    #         self.playButton["bg"] = "green"
    #         continuePlay=False
    #
    #     else:
    #         self.playButton["text"] = "Pause"
    #         self.playButton["bg"] = "red"
    #         continuePlay= True
    #
    # def backward(self):
    #     global continuePlay,t,backward,forward
    #     self.playButton["text"] = "Play"
    #     self.playButton["bg"] = "green"
    #     backward=True
    #     forward=False
    #     continuePlay=False
    #
    # def forward(self):
    #     global continuePlay,t,forward,backward
    #     self.playButton["text"] = "Play"
    #     self.playButton["bg"] = "green"
    #     forward=True
    #     backward=False
    #     continuePlay=False

    """open new window to display the Agent Detail"""
    def openNewWindow(self):
        self.newWindow = Toplevel(root)
        self.newWindow.title("Inspect AI")
        self.newWindow.geometry("400x700")

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
                 command = lambda: Info.printInput(the_canvas,self.inputtxt,self.inputtxt1,self.t))
        self.printButton.pack()
    """"""

def repeater(root):
    global backward,forward,speedup
    t=1
    notMovingFlag=False      #True when no agent is moving
    while True:
        if backward and t>1:
            t-=1
            Info.move_agents(t,the_canvas,the_frame,True)
            notMovingFlag=False
        elif notMovingFlag==True:
            pass
        elif forward and t>=1:
            tt=Info.move_agents(t,the_canvas,the_frame,False)
            t+=1
            if tt:
                notMovingFlag=True

        elif continuePlay:
            tt=Info.move_agents(t,the_canvas,the_frame,False)
            t+=1
            if tt:
                notMovingFlag=True


        forward=False
        backward=False

        root.update()
        time.sleep(speedup)


if __name__=="__main__":
    #in windows: python run.py test_2.txt debug-6-6.map.ecbs 2
    #in linux: python3 run.py test_2.txt debug-6-6.map.ecbs 2
    try:
        addagen=sys.argv[1]
        addmap=sys.argv[2]
        numAgent=int(sys.argv[3])
    except IndexError:
        addagen,addmap,numAgent="test_25.txt","warehouse-10-20-10-2-1.map.ecbs",25
        # addagen,addmap,numAgent="test_2.txt","debug-6-6.map.ecbs",2

    # addagen=init("../maps/debug-6-6.map.ecbs", "../scenarios/debug-6-6-2-2.scen", 2, [(0, ((-1, -2), (-1, -2)), -2, -100)])
    # with open("agentPath.txt","w") as text_file:
    #     text_file.write(addagen)
    # text_file.close()

    global Info,the_canvas,the_frame,continuePlay,t,backward,forward,newWindow,speedup


    Info=info(addagen,addmap,numAgent)

    # Construct a simple root window
    root = Tk()

    continuePlay,backward,forward,speedup = True,False,False,0.2

    root.title("Lazycbs Visualizer")
    # root.protocol("WM_DELETE_WINDOW",exit)

    the_canvas= MyCanvas(root,width=1630,height=720,bg="#d1d1d1")
    the_canvas.pack(side=LEFT,expand=True,fill=BOTH)

    the_frame2 = myFrame2(root)
    the_frame2.pack(side=RIGHT,expand=True,fill=BOTH)

    the_frame = myFrame(root,the_canvas)
    the_frame.pack(side=RIGHT,expand=True,fill=BOTH)

    """cross platform"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    the_frame.config(width=screen_width, height=screen_height)

    Info.draw_map(the_canvas)
    Info.draw_agents(the_canvas,the_frame,the_frame2)

    repeater(root)

    root.mainloop()

    
