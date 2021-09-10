import sys

from tkinter import *
from Map import info
import time
from tkinter import ttk
def simulation_canvas  (parent,**config):
    global the_canvas
    the_canvas = Canvas(parent,**config)
    return the_canvas

def repeater(root):
    global Info,the_canvas,the_frame
    t=1
    while 1:
        if continuePlay:
            tt=Info.move_agents(t,the_canvas,the_frame)
            if tt:
                break
            t+=1
        root.update()
        time.sleep(0.4)


class Example(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.text = Text(self, height=6, width=20)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.tag_config('constraint', background="#DCE2F1", foreground="black")
        self.text.tag_config('current', background="#EBEBE4", foreground="black")
        self.button = Button(self, text='Play',width=5,height=2, bg='green', fg='black', command=self.play_agents)
        self.button.pack(side=TOP, padx=5, pady=5)


    def play_agents(self):
        global continuePlay
        if self.button["text"] == "Play":
            self.button["text"] = "Pause"
            self.button["bg"] = "red"
            continuePlay=False
        else:
            self.button["text"] = "Play"
            self.button["bg"] = "green"
            continuePlay= True



if __name__=="__main__":
    # agents_file=sys.argv[1]
    # map_file=sys.argv[2]
    global Info,the_canvas,the_frame,continuePlay
    addagen,addmap="test_25.txt","warehouse-10-20-10-2-1.map.ecbs"

    # addagen,addmap=agents_file,map_file

    Info=info(addagen,addmap)

    # Construct a simple root window
    the_canvas   = None
    root = Tk()

    continuePlay = True

    root.title("Simulation")
    # root.protocol("WM_DELETE_WINDOW",exit)

    the_frame = Example(root)
    the_frame.pack(side="right",fill="both", expand=True)

    simulation_canvas(root,width=1630,height=720,bg="#d1d1d1").pack(side=LEFT,expand=True,fill=BOTH)



    Info.draw_map(the_canvas)
    Info.draw_agents(the_canvas,the_frame)
    repeater(root)

    root.mainloop()



    
    
    
