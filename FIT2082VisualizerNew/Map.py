from tkinter import *
import ast
import time
from collections import defaultdict

class info:
        def __init__(self,addagen,addmap):
            self.fagents=open(addagen,'r')
            self.fmap=open(addmap,'r')
            self.a=10
            self.x0,self.y0=10,10
            self.Arrmap=[]
            self.GridMap=[]
            self.readmap()
            self.agents=[]
            self.image=[]
            self.read_agent()
        def readmap(self):
            self.fmap.readline()
            for i in self.fmap:  #iterate each line in fmap
                self.Arrmap.append(list(map(int,i.split(','))))

        def read_agent(self):
            for _ in range(15):
                next(self.fagents)
            cond=False
            while (cond==False):
            	time.sleep(1)
            	try:
            		num_agents=int(self.fagents.readline().split()[-1])  ##extract ... upto 25 --> 25
            		cond=True
            	except:
            		continue
            tmp=self.fagents.readlines()
            for i in tmp[:num_agents]:
                tempt=i.strip('\n')
                tempt=[i for i in tempt.split(' ') if i[0]=="(" and i[-1]==")" and len(i)>4]
                # +1 to x and y value otherwise don't match
                tempt=list(map(lambda x:(int(x[0])+1,int(x[1])+1),list(map(lambda x:x.strip('()').split(','),tempt))))
                self.agents.append(tempt)
            self.max_agents_length=len(max(self.agents, key=len))
            # print(self.agents)
            tempt=tmp[num_agents].strip('\n')
            tempt=[i for i in tempt.split(' ') if len(i)>12]
            # print([ast.literal_eval(i)[0] for i in tempt])
            cons_loc1=list(map(lambda x:(x[0]+1,x[1]+1),[ast.literal_eval(i)[0] for i in tempt]))
            # print(cons_loc1)
            cons_loc2=list(map(lambda x:(x[0]+1,x[1]+1),[ast.literal_eval(i)[1] for i in tempt]))
            # print(cons_loc2)
            cons_time=[ast.literal_eval(i)[2] for i in tempt]
            # print(cons_time)
            loc_zip = [list(z) for z in zip(cons_loc1, cons_loc2)]
            self.constraint_dict = defaultdict(list)
            for i in range(len(cons_time)):
                self.constraint_dict[cons_time[i]].append(loc_zip[i])
            # print(self.constraint_dict)
            # for value in self.constraint_dict[108]:
            #     print(value[0])

            self.agentsPath=[None]*len(self.agents)

        def draw_map(self,canvas):
            """
            Function to draw the map on canvas
            """
            self.GridMap=self.Arrmap
            for x in range(len(self.Arrmap[0])):  #165
                    for y in range(len(self.Arrmap)):   #63
                        if self.Arrmap[y][x]:
                            self.GridMap[y][x]=(
                                canvas.create_rectangle(self.x0 + x * self.a, self.y0 + y * self.a,
                                                self.x0 + (x + 1) * self.a, self.y0 + (y + 1) * self.a,
                                                fill='#8080C0')
                            )
                        else:
                            self.GridMap[y][x]=(
                                canvas.create_rectangle(self.x0 + x * self.a, self.y0 + y * self.a,
                                                self.x0 + (x + 1) * self.a, self.y0 + (y + 1) * self.a,
                                                fill='#FBFBEA')
                            )

        def draw_agents(self,canvas,frame):
            """
            Function that draws agent on map.
            Bind tags to the agent object:
                self.w Label is with the Frame. Will display the AI number when user hover on it
                when user click on the agent, display its path. Click again to remove its path.
            """
            self.w = Label(frame, text="AI : ")
            self.w.place(x=0, y=0, anchor="nw")
            self.w.pack()

            frame.text.insert("end","Timestep: 0"+"\n",'current')
            for i in range(len(self.agents)):
                self.image.append(canvas.create_oval(self.x0 + self.agents[i][0][1] * self.a, self.y0 + self.agents[i][0][0] * self.a,
                                                self.x0 + (self.agents[i][0][1] + 1) * self.a, self.y0 + (self.agents[i][0][0] + 1) * self.a,
                                                fill='#B45B3E'))

                canvas.tag_bind(self.image[-1], '<Button-1>', lambda event,i=i : self.onObjectClick(i,canvas))
                canvas.tag_bind(self.image[-1], '<Enter>', lambda event,i=i : self.on_enter(i))


                frame.text.insert("end", "Agent "+str(i) + ": "+"("+str(self.agents[i][0][0]-1)+","+str(self.agents[i][0][1]-1)+")"+"\n")

        def on_enter(self,i):
            """
            Function to update the AI number when user hover on the agent
            """
            temp="AI : "+str(i)
            self.w.config(text=temp)


        def linemaker(self,screen_points):
            """
            Function to take list of points and make them into lines
            """
            is_first = True
            # Set up some variables to hold x,y coods
            x1 = y1 = 0
            # Grab each pair of points from the input list
            for (y,x) in screen_points:
                # If its the first point in a set, set x0,y0 to the values
                x=x*self.a + self.x0 + 0.5*self.a
                y=y*self.a + self.y0 + 0.5*self.a

                if is_first:
                    x1 = x
                    y1 = y
                    is_first = False
                else:
                    # If its not the fist point yeild previous pair and current pair
                    yield x1,y1,x,y
                    # Set current x,y to start coords of next line
                    x1,y1 = x,y

        def onObjectClick(self, index, canvas):
            """
            Function that when user click on the object, display or remove its path.
            """
            list_of_screen_coods = self.agents[index]
            # print(list_of_screen_coods)
            if self.agentsPath[index] == None:
                self.agentsPath[index]=[]
                for (x1,y1,x2,y2) in self.linemaker(list_of_screen_coods):
                    # print(str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2)+" ")
                    self.agentsPath[index].append(canvas.create_line(x1,y1,x2,y2, width=1.5,fill="red"))
                # self.agentsClicked[index] = canvas

            else:
                for obj in self.agentsPath[index]:
                    canvas.delete(obj)
                self.agentsPath[index] = None


        def move_agents(self,t,canvas,frame,doBackward):
            """
            Funciton that move each agents in one timestamp.
            """
            if doBackward:
                for i in range(len(self.agents)):
                    #if still moving.
                    if 0<t<len(self.agents[i]):
                        canvas.move(self.image[i],(self.agents[i][t-1][1]-self.agents[i][t][1])*self.a,(self.agents[i][t-1][0]-self.agents[i][t][0])* self.a)
                    elif t==len(self.agents[i]):
                        canvas.itemconfig(self.image[i], fill='#B45B3E')
                        #reduce the oval's size once it reaches the destination
                        #because cosntraint might later appear on the same spot
                        x0, y0, x1, y1 = canvas.coords(self.image[i])
                        x0 = x0 - 2
                        x1 = x1 + 2
                        y0 = y0 - 2
                        y1 = y1 + 2
                        canvas.coords(self.image[i], x0, y0, x1, y1)
                    #t=0,do nothing
            else:
                tt=1
                frame.text.insert("end","\n")
                frame.text.insert("end","Timestep: "+str(t)+"\n",'current')

                if (t in self.constraint_dict.keys()):
                    for value in self.constraint_dict[t]:
                        canvas.itemconfig(self.GridMap[value[0][0]][value[0][1]], fill='#0000FF')
                        #add text description to the frame
                        frame.text.insert("end", "Constraint time "+str(t) + ":\n"+"("+str(value[0][0]-1)+","+str(value[0][1]-1)+")"+"\n",'constraint')
                        frame.text.see("end")
                        if (value[1][0],value[1][1]) != (0,-1):
                            canvas.itemconfig(self.GridMap[value[1][0]][value[1][1]], fill='#0000FF')

                for i in range(len(self.agents)):
                    #if still moving.
                    if t<len(self.agents[i]):
                        canvas.move(self.image[i],(self.agents[i][t][1]-self.agents[i][t-1][1])*self.a,(self.agents[i][t][0]-self.agents[i][t-1][0])* self.a)
                        #add text description to the frame
                        frame.text.insert("end", "Agent "+str(i) + ": "+"("+str(self.agents[i][t][0]-1)+","+str(self.agents[i][t][1]-1)+")"+"\n")
                        frame.text.see("end")
                        #an agent is still moving, so repeater continues
                        tt=0
                    #elif the agent stops, change its color to green
                    elif t==len(self.agents[i]):
                        canvas.itemconfig(self.image[i], fill='#00FF00')
                        #reduce the oval's size once it reaches the destination
                        #because cosntraint might later generate on it
                        x0, y0, x1, y1 = canvas.coords(self.image[i])
                        x0 = x0 + 2
                        x1 = x1 - 2
                        y0 = y0 + 2
                        y1 = y1 - 2
                        canvas.coords(self.image[i], x0, y0, x1, y1)
                    #elif the agent have stopped, move (0,0) so speed don't accelerate
                    elif t>len(self.agents[i]) and t<=self.max_agents_length:
                        canvas.move(self.image[i],0,0)
                    else:
                        print("error?")
                #return True if no agent is moving
                return tt

if __name__=="__main__":
    temp=info("test_25.txt","warehouse-10-20-10-2-1.map.ecbs")
