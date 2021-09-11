import sys

from tkinter import *
from Map import info
import time

def simulation_canvas  (parent,**config):
    global the_canvas
    the_canvas = Canvas(parent,**config)
    return the_canvas

def repeater(root):
    global Info,the_canvas,the_frame,t,backward,forward
    t=1
    while True:
        if backward and t>1:
            t-=1
            Info.move_agents(t,the_canvas,the_frame,True)

        elif forward and t>=1:
            tt=Info.move_agents(t,the_canvas,the_frame,False)
            if tt:
                break
            t+=1

        elif continuePlay:
            tt=Info.move_agents(t,the_canvas,the_frame,False)
            if tt:
                break
            t+=1

        forward=False
        backward=False

        root.update()
        time.sleep(0.4)


class myFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.text = Text(self, height=6, width=20)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.tag_config('constraint', background="#DCE2F1", foreground="black")
        self.text.tag_config('current', background="#EBEBE4", foreground="black")
        self.button = Button(self, text='Play',width=5,height=2, bg='green', fg='black', command=self.play_visualizer)
        self.button.pack(side=TOP, padx=5, pady=5)

        self.button1 = Button(self, text='<<',width=5,height=2, bg='#EBEBE4', fg='black', command=self.backward)
        self.button1.pack(side=BOTTOM, padx=5, pady=5)

        self.button2 = Button(self, text='>>',width=5,height=2, bg='#EBEBE4', fg='black', command=self.forward)
        self.button2.pack(side=BOTTOM, padx=5, pady=5)


    def play_visualizer(self):
        global continuePlay,Paused
        if self.button["text"] == "Play":
            self.button["text"] = "Pause"
            self.button["bg"] = "red"
            continuePlay=False

        else:
            self.button["text"] = "Play"
            self.button["bg"] = "green"
            continuePlay= True

    def backward(self):
        global continuePlay,t,backward,forward
        self.button["text"] = "Pause"
        self.button["bg"] = "red"
        backward=True
        forward=False
        continuePlay=False

    def forward(self):
        global continuePlay,t,forward,backward
        self.button["text"] = "Pause"
        self.button["bg"] = "red"
        forward=True
        backward=False
        continuePlay=False



if __name__=="__main__":
    try:
        agents_file=sys.argv[1]
        map_file=sys.argv[2]
        addagen,addmap=agents_file,map_file
    except IndexError:
        addagen,addmap="test_25.txt","warehouse-10-20-10-2-1.map.ecbs"


    global Info,the_canvas,the_frame,continuePlay,t,backward,forward


    Info=info(addagen,addmap)

    # Construct a simple root window
    the_canvas   = None
    root = Tk()

    continuePlay,backward,forward = True,False,False

    root.title("Simulation")
    # root.protocol("WM_DELETE_WINDOW",exit)

    the_frame = myFrame(root)
    the_frame.pack(side="right",fill="both", expand=True)

    simulation_canvas(root,width=1630,height=720,bg="#d1d1d1").pack(side=LEFT,expand=True,fill=BOTH)


    Info.draw_map(the_canvas)
    Info.draw_agents(the_canvas,the_frame)
    repeater(root)

    root.mainloop()



    
    
    
