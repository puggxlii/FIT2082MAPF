class info:
    def __init__(self,addagen,addmap):
        self.fagents=open(addagen,'r')
        self.fmap=open(addmap,'r')
        self.a=10
        self.x0,self.y0=10,10
        self.Arrmap=[]
        self.readmap()
        self.agents=[]
        self.read_agent()

    def readmap(self):
        #a,b=(map(int,self.fmap.readline().split(',')))
        #Arrmap=[[]]
        self.fmap.readline()
        for i in self.fmap:  #iterate each line in fmap
            self.Arrmap.append(list(map(int,i.split(','))))
            # print(i)
        # print(len(self.Arrmap),len(self.Arrmap[0]))
        
    def read_agent(self):
        for i in self.fagents:
            tempt=i.strip('\n')
            tempt=[i for i in tempt.split(' ') if i[0]=="(" and i[-1]==")" and len(i)>4]
            tempt=list(map(lambda x:(int(x[0])+1,int(x[1])+1),list(map(lambda x:x.strip('()').split(','),tempt))))
            #print(tempt)
            self.agents.append(tempt)
        # print(self.agents)
            
    def draw_agents(self,t,canvas):
        tt=1
        for i in self.agents:
            if t<len(i): #still moving
                canvas.create_oval(self.x0 + i[t][1] * self.a, self.y0 + i[t][0] * self.a,
                                            self.x0 + (i[t][1] + 1) * self.a, self.y0 + (i[t][0] + 1) * self.a,
                                            fill='#FF0000')
                tt=0
            else:       #stop
                canvas.create_oval(self.x0 + i[-1][1] * self.a, self.y0 + i[-1][0] * self.a,
                                            self.x0 + (i[-1][1] + 1) * self.a, self.y0 + (i[-1][0] + 1) * self.a,
                                            fill='#00FF00')
        return tt       #return 1 if no agent is moving
            
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

# if __name__=="__main__":
#     temp=info("location.txt","warehouse-10-20-10-2-1.map.ecbs")
