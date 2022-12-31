import time,random,math
from tkinter import *
import matplotlib.pyplot as plt

root = Tk()

root.title('Animation')
root.geometry('800x600')
cv= Canvas(root, width=600, height=600,background="linen")
cv.place(x=0,y=0, width=600, height=600)
cv_=0
L_grass=Label(root,text="grass:")
L_grass.place(x=610,y=10)
E_grass = Entry(root, bd =3)
E_grass.place(x=680,y=10, width=50, height=30)

L_cow=Label(root,text="cow:")
L_cow.place(x=610,y=50)
E_cow = Entry(root, bd =3)
E_cow.place(x=680,y=50, width=50, height=30)

L_tiger=Label(root,text="tiger:")
L_tiger.place(x=610,y=90)
E_tiger = Entry(root, bd =3)
E_tiger.place(x=680,y=90, width=50, height=30)

L1=Label(root,text="current number:")
L1.place(x=610,y=190)
L2=Label(root,text="grass:")
L2.place(x=610,y=230)
L2_=Label(root,text="")
L2_.place(x=680,y=230)

L3=Label(root,text="cow:")
L3.place(x=610,y=270)
L3_=Label(root,text="")
L3_.place(x=680,y=270)

L4=Label(root,text="tiger:")
L4.place(x=610,y=310)
L4_=Label(root,text="")
L4_.place(x=680,y=310)
#以上是关于界面的设计


class grass:#被吃的时间都是随能量剩余值线性变化


    def __init__(self,pos):
        self.eat_energy_per_time=18 #每个单位被吃的能量
        self.energy=50#初始能量
        self.generate_energy=100#繁衍所需能量
        self.life_span=30#寿命
        self.position=pos#当前位置
        self.be_eaten=False
        self.be_find=False
        self.age=0#初始化年龄
        self.gain=4#每个时间点获得能量

    def generate_next(self):#判断是否繁衍
        if self.energy>=self.generate_energy:
            newgrass=grass([random.randint(0,598),random.randint(0,598)])
            self.energy-=50
            return newgrass


    def die(self):#判断是否死亡
        rand_span=random.choice([self.life_span-3,self.life_span+3,
                                 self.life_span-2,self.life_span+2,self.life_span-2,self.life_span+2,
                                 self.life_span-1,self.life_span+1,self.life_span-1,self.life_span+1,self.life_span-1,self.life_span+1,
                                 self.life_span,self.life_span,self.life_span,self.life_span])
        if self.age>=rand_span or self.energy<=0:
            return True
        return False

    def gain_energy(self):#获得能量的步骤
        if len(lists[0])<4500:
            self.energy+=random.choice([0,self.gain,self.gain,2*self.gain])

        else:
            self.energy+=math.floor(4500*self.gain/len(lists[0]))


    def loss_energy(self):#被吃时能量的损失
        if self.energy - self.eat_energy_per_time >= 0:
            self.energy -= self.eat_energy_per_time
            return self.eat_energy_per_time
        else:
            temp=self.energy
            self.energy = 0
            return temp






class cow:#被吃时能量都是线性变化
    def __init__(self,pos):
        self.pace_=1#慢速
        self.speed=3#快速
        self.eat_energy_per_time=180#每个单位被吃能量
        self.energy = 500 #初始化能量
        self.generate_energy = 900 #繁衍所需能量
        self.life_span =300 #寿命
        self.position=pos
        self.age=0 #初始化年龄
        self.behurt=False #被伤了
        self.is_eating=False #正在吃
        self.find_grass=False #搜索发现了草
        self.find_tiger=False #搜索发现老虎
        self.be_find=False #被发现

    def generate_next(self):
        if self.energy >= self.generate_energy:
            pos_0=self.position[0]+random.choice([-2,-1,1,2])
            pos_1=self.position[1]+random.choice([-2,-1,1,2])
            if 0<=pos_0<=598 and 0<=pos_1<=598:
                newcow = cow([pos_0,pos_1])
            else:
                newcow=cow(self.position)
            self.energy -= 500
            return newcow


    def die(self):
        if self.age>=self.life_span or self.energy<=0:
            return True
        return False


    def search(self):#搜索 距离优先 先搜索老虎 再搜索草
        range_=[[max(round(self.position[0]-30),0),max(round(self.position[1]-30),0)],[min(round(self.position[0]+30),598),min(round(self.position[1]+30),598)]]
        dist_=float("inf")
        near_position=0
        near_index=None
        for i in range(range_[0][0],range_[1][0]):
            for j in range(range_[0][1],range_[1][1]):
                for k in pos_dict[2][(i,j)]:
                    dist=math.sqrt((lists[2][k].position[0]-self.position[0])**2+(lists[2][k].position[1]-self.position[1])**2)
                    if dist<dist_:
                        dist_=dist
                        near_position = lists[2][k].position
                        near_index=k

        if not near_position == 0:#初始化，意味着没搜索到
            self.find_tiger=True

        if near_position==0 and not self.is_eating:
           for i in range(range_[0][0], range_[1][0]):
                for j in range(range_[0][1], range_[1][1]):
                    for k in pos_dict[0][(i, j)]:
                        if not lists[0][k].be_eaten:
                            dist = math.sqrt((lists[0][k].position[0] - self.position[0]) ** 2 + (
                                    lists[0][k].position[1] - self.position[1]) ** 2)
                            if dist < dist_:
                                dist_ = dist
                                near_position = lists[0][k].position
                                near_index=k

           if not near_position == 0:
               self.find_grass=True


        if near_position!=0:
            return near_position,near_index

        self.find_grass=False
        self.find_tiger=False


    def pace(self): #慢速走，随机漫步
        x1=0;y1=0
        while 1:
            x1=round(random.uniform(-self.pace_,self.pace_),2)
            y_temp=round(math.sqrt(1-math.pow(x1,2)),2)
            y1=random.choice([-y_temp,y_temp])
            if 0 <= self.position[0] + x1 <= 598 and 0 <= self.position[1] + y1 <= 598:
                break

        self.position=[self.position[0] +x1, self.position[1]+y1]
        self.energy-=self.pace_*2

        return x1,y1

    def goto_grass(self,pos):#发现了草，就往草走
        factor = [0, 0]




        if pos[0] - self.position[0] >= 0:
            factor[0] = 1
        else:
            factor[0] = -1

        if pos[1] - self.position[1] >= 0:
            factor[1] = 1
        else:
            factor[1] = -1

        if 2<math.sqrt((pos[1]-self.position[1])**2+(pos[0]-self.position[0])**2)<=3:
            temp_x=pos[0]-self.position[0];temp_y=pos[1]-self.position[1]
            self.position[0]=pos[0]
            self.position[1] = pos[1]
            self.energy -= self.pace_*2

            return temp_x,temp_y

        else:
            if pos[0] - self.position[0] != 0:
                k = (pos[1] - self.position[1]) / (pos[0] - self.position[0])

                x1 = round(self.pace_ / math.sqrt(1 + k ** 2) * factor[0], 2)
                y1 = round(x1 * k, 2)


            else:x1=0;y1=self.pace_*factor[1]
            self.position = [self.position[0] + x1, self.position[1] + y1]
            self.energy -= self.pace_*2
            return x1,y1


    def rush(self,pos):#发现老虎，就跑
        factor = [0, 0]


        if pos[0] - self.position[0] >= 0:
            factor[0] = 1
        else:
            factor[0] = -1

        if pos[1] - self.position[1] >= 0:
            factor[1] = 1
        else:
            factor[1] = -1

        if     (pos[0] - self.position[0]) !=0:
            k = (pos[1] - self.position[1]) / (pos[0] - self.position[0])
            x1 = round(self.speed/ math.sqrt(1 + k ** 2) * factor[0], 2)
            y1 = round(x1 * k, 2)

        else: x1=0;y1=self.speed*factor[1]




        if 0 <= self.position[0] - x1 <= 598 and 0 <= self.position[1] - y1 <= 598:#
            self.position = [self.position[0] - x1, self.position[1] - y1]

            self.energy -= self.speed*4

            return -x1,-y1

        return 0,0

    def loss_energy(self):#被吃时能量变化
        if self.energy - self.eat_energy_per_time >= 0:
            self.energy -= self.eat_energy_per_time
            return self.eat_energy_per_time
        else:
            temp=self.energy
            self.energy = 0
            return temp



class tiger:
    def __init__(self,pos):
        self.pace_=1
        self.speed=5
        self.energy =800
        self.generate_energy = 1600
        self.life_span =450
        self.position=pos
        self.age=0
        self.find=False
        self.is_eating=False

    def generate_next(self):
        if self.energy >= self.generate_energy:
            pos_0 = self.position[0] + random.choice([-2, -1, 1, 2])
            pos_1 = self.position[1] + random.choice([-2, -1, 1, 2])
            if 0 <= pos_0 <= 598 and 0 <= pos_1 <= 598:
                newtiger = tiger([pos_0, pos_1])
            else:
                newtiger = tiger(self.position)
            self.energy -= 800
            return newtiger

    def die(self):
        if self.age >= self.life_span or self.energy <= 0:
            return True
        return False

    def pace(self):#随机漫步
        x1=0;y1=0
        while 1:
            x1=round(random.uniform(-self.pace_,self.pace_),2)
            y_temp=round(math.sqrt(1-math.pow(x1,2)),2)
            y1=random.choice([-y_temp,y_temp])
            if 0 <= self.position[0] + x1 <= 598 and 0 <= self.position[1] + y1 <= 598:
                break

        self.position=[self.position[0] +x1, self.position[1]+y1]
        self.energy-=self.pace_*2

        return x1,y1

    def search(self):#搜索牛
        range_ = [[max(round(self.position[0] - 50), 0), max(round(self.position[1] - 50), 0)],
                  [min(round(self.position[0] + 50), 598), min(round(self.position[1] + 50), 598)]]

        dist_=float("inf")
        near_position = 0
        near_index=None
        for i in range(range_[0][0],range_[1][0]):
            for j in range(range_[0][1],range_[1][1]):
                for k in pos_dict[1][(i,j)]:
                    dist=math.sqrt((lists[1][k].position[0]-self.position[0])**2+(lists[1][k].position[1]-self.position[1])**2)
                    if dist<dist_:
                        dist_=dist
                        near_position=lists[1][k].position
                        near_index=k

        if not near_position == 0:
            self.find=True
            return near_position,near_index

        self.find=False



    def rush(self,pos):#找到牛就追
        factor = [0, 0]


        if pos[0] - self.position[0] >= 0:
            factor[0] = 1
        else:
            factor[0] = -1

        if pos[1] - self.position[1] >= 0:
            factor[1] = 1
        else:
            factor[1] = -1

        if pos[0] - self.position[0]!=0:
            k = (pos[1] - self.position[1]) / (pos[0] - self.position[0])
            x1 = round(self.speed / math.sqrt(1 + k ** 2) * factor[0], 2)
            y1 = round(x1 * k, 2)

        else:x1=0;y1=self.speed*factor[1]

        if 0 <= self.position[0] + x1 <= 598 and 0 <= self.position[1] + y1 <= 598:
            self.position = [self.position[0] + x1, self.position[1] + y1]

        self.energy -= self.speed*1.5
        return x1,y1


lists=[[], [], []]#三个子列表储存所有生物


points=[[], [], []]#用于对应UI上的位置
color_=["lime","blue","red"]
pos_dict=[{},{},{}]#用于搜索


def show():#所有点在地图上初始化
    global points
    points=[[], [], []]

    for i in range(3):
        for j in range(len(lists[i])):
            points[i].append(cv.create_rectangle(lists[i][j].position[0], lists[i][j].position[1], lists[i][j].position[0] + 2, lists[i][j].position[1] + 2, fill=color_[i], width=0))
    cv.update()

def pos_map():#所有点对应到不同的位置区间上
    global pos_dict
    for type_ in range(3):
        for i in range(599):
            for j in range(599):
                pos_dict[type_][(i, j)] = []
        for i in range(len(lists[type_])):
            pos_dict[type_][(math.floor(lists[type_][i].position[0]), math.floor(lists[type_][i].position[1]))].append(
                i)

    return pos_dict

timestp=[]#统计物种数量随时间变化



def click():
    global timestp
    timestp=[]

    global lists,points
    lists=[[], [], []]
    for i in points:
        for j in i:
            cv.delete(j)
    points = [[], [], []]

    cv.update()


    try:#输入获得初始化
        grass_num=int(E_grass.get())
        cow_num=int(E_cow.get())
        tiger_num =int(E_tiger.get())

    except:

        warn_label = Label(text="invalid input")
        warn_label.place(x=630,y=150, width=100, height=40)
        root.update()
        time.sleep(2)
        warn_label.place_forget()
        return 0

    if grass_num==0 and cow_num==0 and tiger_num==0:
        warn_label = Label(text="invalid input")
        warn_label.place(x=630, y=150, width=100, height=40)
        root.update()
        time.sleep(2)
        warn_label.place_forget()
        return 0


    ##########################################################



    for i in range(grass_num):#初始化所有物种
        lists[0].append(grass([random.randint(0, 598), random.randint(0, 598)]))

    for i in range(cow_num):
        lists[1].append(cow([random.randint(0, 598), random.randint(0, 598)]))

    for i in range(tiger_num):
        lists[2].append(tiger([random.randint(0, 598), random.randint(0, 598)]))


    end_pro=False
    show()

    def pace_point(type_,index):#漫步对应的ui动作
        global lists,points
        a=lists[type_][index].pace()
        cv.move(points[type_][index], a[0], a[1])
        cv.update()

    def add_(type_, obj):#生成新生物对应的ui动作
        lists[type_].append(obj)
        points[type_].append(
            cv.create_rectangle(obj.position[0], obj.position[1], obj.position[0] + 2, obj.position[1] + 2,
                                fill=color_[type_], width=0))
        cv.update()

    def del_(type_, index):#死亡对应的ui动作
        del lists[type_][index]

        cv.delete(points[type_][index])
        cv.update()
        del points[type_][index]




    while not end_pro: #没达到退出条件（主代码）
        pos_map()


#########一下对每一个生物进行状态更新

        for i in range(len(lists[0])):

            lists[0][i].gain_energy()

            lists[0][i].age+=1


        for i in range(len(lists[1])):
            lists[1][i].age += 1
            if lists[1][i].behurt:

                pass

            else:
                cow_search=lists[1][i].search()
                if lists[1][i].find_tiger:
                    cow_rush=lists[1][i].rush(cow_search[0])
                    cv.move(points[1][i],*cow_rush)
                    cv.update()

                elif lists[1][i].find_grass:
                    if math.sqrt((lists[1][i].position[1]-cow_search[0][1])**2+(lists[1][i].position[0]-cow_search[0][0])**2)>2:
                        cow_gotograss=lists[1][i].goto_grass(cow_search[0])
                        cv.move(points[1][i], *cow_gotograss)
                        cv.update()

                    if math.sqrt((lists[1][i].position[1]-cow_search[0][1])**2+(lists[1][i].position[0]-cow_search[0][0])**2)<=2:

                        en = lists[0][cow_search[1]].loss_energy()
                        lists[1][i].energy += en

                else: pace_point(1,i)


            #最后再进行清算

        for i in range(len(lists[2])):
            lists[2][i].age += 1
            tiger_search=lists[2][i].search()
            if lists[2][i].find:
                if math.sqrt((lists[2][i].position[1] - tiger_search[0][1]) ** 2 + (
                        lists[2][i].position[0] - tiger_search[0][0]) ** 2) >4:
                    tiger_rush=lists[2][i].rush(tiger_search[0])
                    cv.move(points[2][i], *tiger_rush)
                    cv.update()

                if math.sqrt((lists[2][i].position[1] - tiger_search[0][1]) ** 2 + (
                        lists[2][i].position[0] - tiger_search[0][0]) ** 2) <=4:

                    lists[1][tiger_search[1]].behurt=True
                    en=lists[1][tiger_search[1]].loss_energy()
                    lists[2][i].energy+=en

            else:pace_point(2,i)



        for j in range(3):
            i=0
            while i<len(lists[j]):
                gn=lists[j][i].generate_next()
                if gn:
                    add_(j,gn)
                if lists[j][i].die():

                    del_(j,i)
                    continue
                i+=1

            #########更新结束
            '''
            以上代码逻辑
            每一次循环：
            对于每一个草：
            更新能量
            
            对于每一个牛：
            如果没被伤，就搜索
            如果找到老虎就跑，找到草就去吃，如果进入一定范围就可以开始吃，不然随机漫步，在这期间更新能量（吃获得的能量，移动减少的能量）
            
            对于每一个老虎
            搜索附近的牛，如果找到就追，进入一定范围就伤并且开始吃，并更新两者能量，不然随机漫步
            
            更新状态：是否出生新的或者死亡，更新lists,points
            
            
            '''
            ###############以下开始统计

        #print(len(lists[0]),len(lists[1]),len(lists[2]))
        L2_["text"]=str(len(lists[0]))
        L3_["text"]=str(len(lists[1]))
        L4_["text"] = str(len(lists[2]))

        timestp.append([len(lists[0]),len(lists[1]),len(lists[2])])


        time.sleep(0.01)

        if len(lists[0])==0 and len(lists[1])==0 or len(lists[0])==0 and len(lists[2])==0 or len(lists[1])==0 and len(lists[2])==0:
            break


def click1():
    if len(timestp)!=0:


        x = [i for i in range(len(timestp))]
        y0 = [timestp[i][0]/10 for i in range(len(timestp))]
        y1 = [timestp[i][1] for i in range(len(timestp))]
        y2 = [timestp[i][2] for i in range(len(timestp))]



        plt.plot(x,y0,'g')
        plt.plot(x, y1,'b')
        plt.plot(x, y2,'r')
        plt.title('the number of each specy')  # 折线图标题
        plt.xlabel('time')  # x轴标题
        plt.ylabel('number')  # y轴标题
        plt.legend(['grass*10', 'cow',"tiger"])

        plt.show()



bt1=Button(text="start",command=click)
bt1.place(x=630,y=130, width=80, height=20)



bt1=Button(text="figure",command=click1)
bt1.place(x=630,y=350, width=80, height=20)


root.mainloop()

