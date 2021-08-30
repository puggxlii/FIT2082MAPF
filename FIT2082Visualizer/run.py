from tkinter import *
from Map import info
import time
# Place canvas in the space below
def simulation_canvas  (parent,**config):
    global the_canvas
    the_canvas = Canvas(parent,**config)
    #the_canvas.bind("<ButtonRelease>", lambda event : model.mouse_click(event.x,event.y))
    return the_canvas

def repeater(root):
    #model.update_all()
    global Info,the_canvas
    t=0
    while 1:
        time.sleep(0.001)
        for o in the_canvas.find_all():
            the_canvas.delete(o)
        Info.draw_map(the_canvas)
        tt=Info.draw_agents(t,the_canvas)
        if tt:
            break
        root.update()
        t+=1
    
if __name__=="__main__":
    # Construct a simple root window
    global Info,the_canvas
    the_canvas   = None
    root = Tk()
    sb = Scrollbar(root)  
    sb.pack(side = RIGHT, fill = Y)  
    root.title("Simulation")
    root.protocol("WM_DELETE_WINDOW",quit)
    frame = Frame(root)
    simulation_canvas(root,width=1920,height=1080,bg="#d1d1d1").pack(side=BOTTOM,expand=True,fill=BOTH)
    addagen,addmap="location.txt","warehouse-10-20-10-2-1.map.ecbs"
    Info=info(addagen,addmap)
    #loop
    repeater(root)
    root.mainloop()
    
    
    
