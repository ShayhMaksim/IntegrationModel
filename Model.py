from numpy import random
from QrCode import QrCode
from typing import List
from Door import Door
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QColorDialog, QGraphicsScene
import numpy as np
from Wall import Wall
from Room import Room
from math import*
import numpy as np
from numpy import linalg as LA

class Model:
    """
        Спереди модели установлена камера и дальномер\n
        Справа от модели установлен еще один дальномер\n
        Мера измерения - 1 см - 1 пиксель\n
        Дальномер не имеет ограничений на измерения (2 дальномера)
    """
    def __init__(self,x0,y0,scene:QGraphicsScene,room: Room,door:Door):
        self.__item=scene.addEllipse(x0-10,y0-10,20,20,QPen(QColor(100,100,100)),QBrush(QColor(255,50,50)))
        self.__scene=scene
        self.__initX=x0
        self.__initY=y0
        self.__x=x0
        self.__y=y0
        self.__wz=0
        self.__door=door
        self.__walls=None
        self.__room=room
        self.__qr=None

        self.dw=90.*np.pi/180.

        #под задачу фильтрации
        self.__p_p=np.zeros((9,9))
        self.__p_c=np.zeros((9,9))
        self.__x_c=np.zeros(9)
        self.__x_p=np.zeros(9)
        self.__cT=0.

        #ошибки измерений
        self.__Dn=np.asarray([
            [0.01,0,0.],
            [0,0.01,0.],
            [0,0,0.0049],
        ])

        # self.__Dn2=np.asarray([
        #     [0.01,0,0,0,0],
        #     [0,0.01,0,0,0],
        #     [0,0,0.0049,0,0],
        #     [0,0,0.,9.,0],
        #     [0.,0.,0.,0.,9.]
        # ])

        #матрица наблюдения
        self.__H=np.asarray([
            [1.,0,0,0,0,0,0,0,0],
            [0,1.,0,0,0,0,0,0,0],
            [0,0,1.,0,0,0,0,0,0],
        ])
        self.__H2=np.asarray([
            [1.,0,0,0,0,0,0,0,0],
            [0,1.,0,0,0,0,0,0,0],
            [0,0,1.,0,0,0,0,0,0],
            [0,0,0.,0,0,1,0,0,0],
            [0,0,0.,0,0,0,1,0,0],
        ])

        self.Y=[]
        self.Result=[]
        self.RealData=[]
        self.P=[]
        
    
    def DrawTrajectory(self,oldX,oldY,newX,newY):
        self.__scene.addLine(oldX,oldY,newX,newY)

    def Move(self,dt,c,dwz):
        oldX=self.__x
        oldY=self.__y
        self.__x=self.__x+c*cos(self.__wz)*dt
        self.__y=self.__y+c*sin(self.__wz)*dt
        self.__wz=self.__wz+dwz
        self.DrawTrajectory(oldX,oldY,self.__x,self.__y)
        
    def AddQrCode(self,qrCode:List[QrCode]):
        self.__qr=qrCode

    def AddWalls(self,walls:List[Wall]):
        self.__walls=walls

    

    def Control(self,dt,d1,d2,d3,__x,__y,__wz):
        """Управляющие элементы"""
        position=self.__door.position

        currentT=0
        #если преграды нет, то движемся прямо к двери
        if (d1>=30) and (d3>=30) and (d2>=30):
            alpha=atan2((position[1]-__y),(position[0]-__x))
            dwz1=alpha-__wz
            if dwz1>self.dw*dt:
                dwz=self.dw*dt
            if dwz1<self.dw*dt:
                dwz=-self.dw*dt
            currentT=dt
            c=30

        #если преграды нет, то есть ограничения, то сохряняем угол траектории
        if (d1>30) and ((d2<30) or (d3<30)):
            dwz=0
            currentT=dt
            c=30
            
        #если справо свободно, то поворачиваем направо
        
        if (d1<30) and (d3>30):
            dwz=0
            #while (self.dw>self.dw*currentT):
            dwz+=self.dw*dt
                #currentT+=dt
            currentT=dt
            c=0
             
        #если справо занято, и слево свободно, то налево
        elif (d1<30) and (d3<30) and (d2>30):
            dwz=0
            #while (self.dw>self.dw*currentT):
            dwz-=self.dw*dt
            currentT=dt
                #currentT+=dt
            c=0


        #если занято с обоих сторон, то поворачиваем направо
        elif (d1<30) and (d3<30) and (d2<30) :
            dwz=0
            #while (self.dw>self.dw*currentT):
            dwz+=self.dw*dt
            currentT=dt
                #currentT+=dt
            c=0

        return c,dwz,currentT


    def Simulate(self,dt):
        """
            моделирование ситуации

            модель ошибок БИНСа для координат - значения линейно уходит с k=3/c\n
            модель ошибок координат по Qr коду - 9 cм\n
            модель ошибок угловых координат по БИНСу - дисперсия линейно растет с интесивностью 0.1 градус^2/c\n
            модель ошибок угловых координат по Qr коду - 3 градусов
        """
        t0=0
        position=self.__door.position
        alpha=atan2((position[1]-self.__y),(position[0]-self.__x))
        self.__wz=alpha

        qrlist=[]

        #список измерений
        
        
        while(True):
            currentY=[]

            b=self.__y-self.__wz*self.__x

            #камера справа
            alpha90=tan(self.__wz+np.pi*0.5)
            b_90=self.__y-alpha90*self.__x
            
            #камера слева
            alpha_90=tan(self.__wz-np.pi*0.5)
            b_minus90=self.__y-alpha_90*self.__x

            rangefinder1=[]
            rangefinder2=[]
            rangefinder3=[]

            #решающее правило для дальномеров
            alphaR=tan(self.__wz)
            bR=self.__y-alphaR*self.__x

            if self.__walls!=None:
                for wall in self.__walls:
                #дальномер, который спереди
                    x,y=wall.getWallCoordinate(self.__wz,b)
                    if (x==-1) and (y==-1): continue

                    if alpha90>0:
                        if (y<(alpha90*x+b_90)):
                            d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                            rangefinder1.append(d)
                    elif alpha90<=0:
                        if (y>(alpha90*x+b_90)):
                            d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                            rangefinder1.append(d)
            
                for wall in self.__walls:
                #дальномер, который сбоку
                    x,y=wall.getWallCoordinate(alpha90,b_90)
                    if (x==-1) and (y==-1): continue       
                    if ((alphaR*x+bR)>=y):
                        d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                        rangefinder2.append(d)

            
                for wall in self.__walls:
                #дальномер, который сбоку
                    x,y=wall.getWallCoordinate(alpha_90,b_minus90)
                    if (x==-1) and (y==-1): continue
                    if ((alphaR*x+bR)<y):
                        d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                        rangefinder3.append(d)

            #главный дальномер
            room=[]
            resultXY=self.__room.getRoomCoordinate(self.__wz,b)
            for xy in resultXY:
                if alpha90>0:
                    if (xy[1]<(alpha90*xy[0]+b_90)):
                        x=xy[0]
                        y=xy[1]
                        d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                        rangefinder1.append(d)
                        room.append(x)
                        room.append(y)
                        room.append(d)
                elif alpha90<=0:
                    if (xy[1]>=(alpha90*xy[0]+b_90)):
                        x=xy[0]
                        y=xy[1]
                        d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                        rangefinder1.append(d)
                        room.append(x)
                        room.append(y)
                        room.append(d)         
            resultD1=min(rangefinder1)


            #боковой справа
            resultXYL=self.__room.getRoomCoordinate(alpha90,b_90)
            for xy in resultXYL:
                if (xy[1]<=(alphaR*xy[0]+bR)):
                    x=xy[0]
                    y=xy[1]
                    d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                    rangefinder2.append(d)
            resultD2=min(rangefinder2)

            #боковой слева
            resultXYL2=self.__room.getRoomCoordinate(alpha_90,b_minus90)
            for xy in resultXYL2:
                if (xy[1]>(alphaR*xy[0]+bR)):
                    x=xy[0]
                    y=xy[1]
                    d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                    rangefinder3.append(d)
            if len(rangefinder3)==0: break   
            resultD3=min(rangefinder3)
            

            Detected=[]
            if self.__qr!=None:
                #обзор камеры справа
                _alpha90=tan(self.__wz+np.pi*30./180)
                _b_90=self.__y-_alpha90*self.__x
            
                _alpha_90=tan(self.__wz-np.pi*30./180)
                _b_minus90=self.__y-_alpha_90*self.__x
                for qr in self.__qr:
                    x,y=qr.GetQrCoordinate(np.pi*30./180,self.__x,self.__y,room[0],room[1],room[2])
                    if (x!=-1) and (y!=-1):
                        dQr,angle,qrw=qr.GetLocalCoordinate(self.__x,self.__y)
                        print(abs(cos(angle)/sin(angle)))
                        dX=np.random.normal(0,abs(cos(angle)/sin(angle))*(2**(dQr**(1./3)))**0.5)
                        dY=np.random.normal(0,abs(cos(angle)/sin(angle))*(2**(dQr**(1./3)))**0.5)
                        __X=(dQr*cos(angle)+dX)*cos(qrw)+(dQr*sin(angle)+dY)*sin(qrw)+x
                        __Y=-(dQr*cos(angle)+dX)*sin(qrw)+(dQr*sin(angle)+dY)*cos(qrw)+y

                
                        # if (round(__X,3)==round(self.__x,3)) and (round(__Y,3)==round(self.__y,3)): 
                        #     print("YES!")

                        Detected.append([__X,__Y,dQr,angle])

  
            c,dwz,newDt=self.Control(dt,resultD1,resultD2,resultD3,self.__x,self.__y,self.__wz)
            self.Move(dt,c,dwz)


            __qrx=0
            __qry=0
            metka=""
            if len(Detected)!=0:
                metka="qr"
            else:
                metka="bins"

            __x=self.__x+t0*10+np.random.normal(0,0.1)
            __y=self.__y+t0*10+np.random.normal(0,0.1)
                    
            __wz=self.__wz+np.random.normal(0,0.07)
            __d1=resultD1
            __d2=resultD2
            __d3=resultD3

            if metka=="qr":
                currentY=np.asarray([__x,__y,__wz])
                Data=np.asarray([__d1,__d2,__d3,Detected])                  
                self.Y.append([t0,metka,currentY,Data])
            else:
                currentY=np.asarray([__x,__y,__wz])
                Data=np.asarray([__d1,__d2,__d3,0])
                self.Y.append([t0,metka,currentY,Data])

            self.RealData.append([t0,__x,__y,self.__wz,self.__x,self.__y,])
            
             
            t0=t0+newDt
            self.__cT+=newDt
            if t0>=10000: break

            if abs(((position[1]-self.__y)**2+(position[0]-self.__x)**2)**0.5)<=30:
                break


    def Prediction(self,U,dt,t,metka):

        F=np.asarray([
                [1.,0.,0, 0., 0.,0.,0, 0., 0.],
                [0.,1.,0, 0.,0.,0.,0, 0., 0.],
                [0.,0.,1.,0.,0.,0.,0, 0., 0.],
            
                [1.,0.,0.,0.,0.,0.,0, -t, 0.],
                [0.,1.,0.,0.,0.,0.,0, 0., -t],
            
                [0.,0.,0.,0.,1.,0.,0, 0., 0],
                [0.,0.,0.,0.,0.,1.,0, 0., 0],

                [0.5/t,0,0.,0.,-0.5/t,0.,0, 0.5, 0],
                [0.,0.5/t,0.,0.,0.,-0.5/t,0, 0., 0.5],
                ],dtype=float)

    
        De=np.asarray([
            [0.15,0,0,0,0,0,0,0,0],
            [0,0.15,0,0,0,0,0,0,0],
            [0,0,(0.5*np.pi*dt)**2,0,0,0,0,0,0],
            [0,0,0,(10*dt)**2,0,0,0,0,0],
            [0,0,0,0,(10*dt)**2,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
        ])

 
        self.__x_p[0]=self.__x_c[0]+U[0]*cos(self.__x_c[2])*dt
        self.__x_p[1]=self.__x_c[1]+U[0]*sin(self.__x_c[2])*dt
        self.__x_p[2]=self.__x_c[2]+U[1]

        self.__x_p[3]=self.__x_c[0]-self.__x_c[7]*t+U[0]*cos(self.__x_c[2])*dt
        self.__x_p[4]=self.__x_c[1]-self.__x_c[8]*t+U[0]*sin(self.__x_c[2])*dt

        self.__x_p[5]=self.__x_c[5]+U[0]*cos(self.__x_c[2])*dt
        self.__x_p[6]=self.__x_c[6]+U[0]*sin(self.__x_c[2])*dt

        
        self.__x_p[7]=(self.__x_c[7]+(self.__x_c[0]-self.__x_c[5])/t)/2.
        self.__x_p[8]=(self.__x_c[8]+(self.__x_c[1]-self.__x_c[6])/t)/2.



        self.__p_p=np.dot(np.dot(F,self.__p_c),np.transpose(F))+De


    def Correction(self,Y,metka,D):


        if metka=="bins":
            __H=self.__H
            invDe=LA.inv(self.__Dn)
            H_t=np.transpose(self.__H)
        elif metka=="qr":
            self.__Dn2=np.asarray([
            [0.01,0,0,0,0],
            [0,0.01,0,0,0],
            [0,0,0.0049,0,0],
            [0,0,0.,D,0],
            [0.,0.,0.,0.,D]
            ])
            __H=self.__H2
            invDe=LA.inv(self.__Dn2)
            H_t=np.transpose(self.__H2)
                  
        self.__p_c=LA.inv(LA.inv(self.__p_p)+np.dot(np.dot(H_t,invDe),__H))
    
        mult=np.dot(np.dot(self.__p_c,H_t),invDe)
    
        subl=Y-np.dot(__H,self.__x_p)
    
        self.__x_c=(self.__x_p+np.dot(mult,subl))



    def FilterKalman(self,dt):
        t0=0
        position=self.__door.position
        alpha=atan2((position[1]-self.__initY),(position[0]-self.__initX))
        self.__wz=alpha

        self.__x_p[0]=self.__initX
        self.__x_p[1]=self.__initY
        self.__x_p[2]=self.__wz
        self.__x_p[3]=self.__x_p[0]
        self.__x_p[4]=self.__x_p[1]
        self.__x_p[5]=self.__x_p[0]
        self.__x_p[6]=self.__x_p[1]
        self.__x_p[7]=0
        self.__x_p[8]=0
     

        self.__p_p[0][0]=5
        self.__p_p[1][1]=5
        self.__p_p[2][2]=1
        self.__p_p[3][3]=5
        self.__p_p[4][4]=5
        self.__p_p[5][5]=5
        self.__p_p[6][6]=5
        self.__p_p[7][7]=50
        self.__p_p[8][8]=50
   
        
        index=0
        self.__cT=0


        while(True):

            Data=self.Y[index]

            y=Data[2]
            otherY=Data[3]           
            D_=0
            if otherY[3]!=0:
                __qrx=0
                __qry=0
                D=[]
                if len(otherY[3])!=0:
                    for qr in otherY[3]:
                        __qrx+=qr[0]
                        __qry+=qr[1]
                        d_=(qr[0]**2+qr[1]**2)**0.5
                        al_=atan2(qr[1],qr[0])
                        an=cos(al_)**2/sin(al_)**2
                        D_l=an*(2**(d_**(1./3)))
                        D.append(D_l)
                    __qrx=__qrx/len(otherY[3])
                    __qry=__qry/len(otherY[3])
                    y=np.resize(y,5)
                    y[3]=(__qrx)
                    y[4]=(__qry)
                    D_=min(D)

            self.Correction(y,Data[1],D_)
            self.Result.append([Data[0],self.__x_c[0],self.__x_c[1],self.__x_c[2],self.__x_c[3],self.__x_c[4],self.__x_c[5],self.__x_c[6],self.__x_c[7],self.__x_c[8]])
            self.P.append([Data[0],self.__p_c[0][0],self.__p_c[1][1],self.__p_c[2][2],self.__p_c[3][3],self.__p_c[4][4],self.__p_c[5][5],self.__p_c[6][6],self.__p_c[7][7],self.__p_c[8][8]])         

            c,dwz,newDt=self.Control(dt,otherY[0],otherY[1],otherY[2],self.__x_c[3],self.__x_c[4],self.__x_c[2])
            U=np.asarray([c,dwz])
            self.Prediction(U,newDt,Data[0]+dt,Data[1])
            
            
            
            self.__cT+=newDt
            index+=1
            
            if index>=len(self.Y): 
                break


      

