import ast

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
            num_agents=int(self.fagents.readline().split()[-1])  ##extract ... upto 25 --> 25
            # self.fagents.readlines()[:num_agents]
            tmp=self.fagents.readlines()
            for i in tmp[:num_agents]:
                tempt=i.strip('\n')
                tempt=[i for i in tempt.split(' ') if i[0]=="(" and i[-1]==")" and len(i)>4]
                tempt=list(map(lambda x:(int(x[0])+1,int(x[1])+1),list(map(lambda x:x.strip('()').split(','),tempt))))
                self.agents.append(tempt)
            self.max_agents_length=len(max(self.agents, key=len))

            tempt=tmp[num_agents].strip('\n')
            tempt=[i for i in tempt.split(' ') if len(i)>12]
            # print([ast.literal_eval(i)[0] for i in tempt])
            cons_loc1=list(map(lambda x:(x[0]+1,x[1]+1),[ast.literal_eval(i)[0] for i in tempt]))
            # print(self.cons_loc1)
            cons_loc2=list(map(lambda x:(x[0]+1,x[1]+1),[ast.literal_eval(i)[1] for i in tempt]))
            # print(self.cons_loc2)
            cons_time=[ast.literal_eval(i)[2] for i in tempt]
            # print(self.cons_time)

            loc_zip = [list(z) for z in zip(cons_loc1, cons_loc2)]
            zip_iterator = zip(cons_time, loc_zip)
            self.constraint_dict = dict(zip_iterator)
            # print(self.constraint_dict)
            # for i in range(len(self.agents)):
            #     if len(self.agents[i])>109:
            #         print(i)
            #         print(self.agents[i][107])
            #         print("!")
            # print(self.agents)
        def draw_map(self,canvas):
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
            frame.text.insert("end","Timestep: 0"+"\n",'current')
            for i in range(len(self.agents)):
                self.image.append(canvas.create_oval(self.x0 + self.agents[i][0][1] * self.a, self.y0 + self.agents[i][0][0] * self.a,
                                                self.x0 + (self.agents[i][0][1] + 1) * self.a, self.y0 + (self.agents[i][0][0] + 1) * self.a,
                                                fill='#B45B3E'))


                frame.text.insert("end", "Agent "+str(i) + ": "+"("+str(self.agents[i][0][0]-1)+","+str(self.agents[i][0][1]-1)+")"+"\n")
        def move_agents(self,t,canvas,frame):
            tt=1
            frame.text.insert("end","\nTimestep: "+str(t)+"\n",'current')

            if (t in self.constraint_dict.keys()):
                canvas.itemconfig(self.GridMap[self.constraint_dict[t][0][0]][self.constraint_dict[t][0][1]], fill='#0000FF')
                #add text description to the frame
                frame.text.insert("end", "Constraint time "+str(t) + ":\n"+"("+str(self.constraint_dict[t][0][0]-1)+","+str(self.constraint_dict[t][0][1]-1)+")"+"\n",'constraint')
                frame.text.see("end")
                if (self.constraint_dict[t][1][0],self.constraint_dict[t][1][1]) != (0,-1):
                    canvas.itemconfig(self.GridMap[self.constraint_dict[t][1][0]][self.constraint_dict[t][1][1]], fill='#0000FF')

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
