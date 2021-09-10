class info:
    def __init__(self,addagen,addmap):
        self.fagents=open(addagen,'r')
        self.fmap=open(addmap,'r')
        self.a=10
        self.x0,self.y0=10,10
        self.Arrmap=[]
        self.readmap()
        self.agents=[]
        self.image=[]
        # self.constraints=[]
        # self.barriers=[]
        # self.max_agents_length=-1
        self.read_agent()
    def readmap(self):
        self.fmap.readline()
        # self.width=self.fmap.readline().strip('\n').split(',')[1]
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
        print(self.max_agents_length)
        # tempt=tmp[num_agents].strip('\n')
        # self.constraints.append(tmp[num_agents])
        # self.barriers.append(tmp[num_agents+1])
        # print(self.constraints)
        # print(self.barriers)
    def draw_map(self,canvas):
        for x in range(len(self.Arrmap[0])):  #165
                for y in range(len(self.Arrmap)):   #63
                    if self.Arrmap[y][x]:
                        canvas.create_rectangle(self.x0 + x * self.a, self.y0 + y * self.a,
                                            self.x0 + (x + 1) * self.a, self.y0 + (y + 1) * self.a,
                                            fill='#000000')
                    else:
                        canvas.create_rectangle(self.x0 + x * self.a, self.y0 + y * self.a,
                                            self.x0 + (x + 1) * self.a, self.y0 + (y + 1) * self.a,
                                            fill='#FFFFFF')

    def draw_agents(self,canvas,frame):
        frame.text.insert("end","Timestep: 0"+"\n",'current')
        for i in range(len(self.agents)):
            self.image.append(canvas.create_oval(self.x0 + self.agents[i][0][1] * self.a, self.y0 + self.agents[i][0][0] * self.a,
                                            self.x0 + (self.agents[i][0][1] + 1) * self.a, self.y0 + (self.agents[i][0][0] + 1) * self.a,
                                            fill='#FF0000'))

            # print(i[0][1])
            frame.text.insert("end", "Agent "+str(i) + ": "+"("+str(self.agents[i][0][0]-1)+","+str(self.agents[i][0][1]-1)+")"+"\n",'current')
    def move_agents(self,t,canvas,frame):
        tt=1
        frame.text.insert("end","\nTimestep: "+str(t+1)+"\n",'current')
        for i in range(len(self.agents)):
            if t<len(self.agents[i])-1: #still moving
                canvas.move(self.image[i],(self.agents[i][t+1][1]-self.agents[i][t][1])*self.a,(self.agents[i][t+1][0]-self.agents[i][t][0])* self.a)

                frame.text.insert("end", "Agent "+str(i) + ": "+"("+str(self.agents[i][t+1][0]-1)+","+str(self.agents[i][t+1][1]-1)+")"+"\n",'current')
                frame.text.see("end")
                # frame.text
                tt=0
            elif t==len(self.agents[i])-1:
                canvas.itemconfig(self.image[i], fill='#00FF00')
            elif t>len(self.agents[i])-1 and t<=self.max_agents_length:       #stop
                canvas.move(self.image[i],0,0)

        return tt       #return 1 if no agent is moving

if __name__=="__main__":
    temp=info("test_25.txt","warehouse-10-20-10-2-1.map.ecbs")
