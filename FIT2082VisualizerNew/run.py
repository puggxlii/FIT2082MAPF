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
    t=0
    while 1:
        if continuePlay:
            tt=Info.move_agents(t,the_canvas,the_frame)
            if tt:
                break
            t+=1
        root.update()
        time.sleep(0.5)


class Example(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.text = Text(self, height=6, width=40)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.tag_config('current', background="yellow", foreground="red")

        self.button = Button(self, text='Play', width=20,height=8, bg='green', fg='black', command=self.play_agents)
        self.button.pack()


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
    # Construct a simple root window
    global Info,the_canvas,the_frame,continuePlay
    the_canvas   = None
    root = Tk()

    continuePlay = True

    root.title("Simulation")
    # root.protocol("WM_DELETE_WINDOW",exit)

    the_frame = Example(root)
    the_frame.pack(side="right",fill="both", expand=True)
    simulation_canvas(root,width=1280,height=720,bg="#d1d1d1").pack(side=BOTTOM,expand=True,fill=BOTH)

    addagen,addmap="test_5.txt","warehouse-10-20-10-2-1.map.ecbs"
    Info=info(addagen,addmap)
    Info.draw_map(the_canvas)
    Info.draw_agents(the_canvas,the_frame)
    repeater(root)

    root.mainloop()



    
    
    
