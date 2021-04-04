from QrCode import QrCode
from typing import List
from Door import Door
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QColorDialog, QGraphicsScene
import numpy as np
from Wall import Wall
from Room import Room
from math import*

class Model:
    """
        Спереди модели установлена камера и дальномер\n
        Справа от модели установлен еще один дальномер\n
        Мера измерения - 1 см - 1 пиксель\n
        Дальномер не имеет ограничений на измерения (2 дальномера)
    """
    def __init__(self,x0,y0,scene:QGraphicsScene,room: Room,door:Door,walls:List[Wall]):
        self.__item=scene.addEllipse(x0-10,y0-10,20,20,QPen(QColor(100,100,100)),QBrush(QColor(255,50,50)))
        self.__scene=scene
        self.__initX=x0
        self.__initY=y0
        self.__x=x0
        self.__y=y0
        self.__wz=0
        self.__door=door
        self.__walls=walls
        self.__room=room
        self.__qr=None

        self.dw=90.*np.pi/180.
    
    def DrawTrajectory(self,oldX,oldY,newX,newY):
        self.__scene.addLine(oldX,oldY,newX,newY)

    def Move(self,dt,c,dwz):
        oldX=self.__x
        oldY=self.__y
        self.__x=self.__x+c*cos(self.__wz+dwz)*dt
        self.__y=self.__y+c*sin(self.__wz+dwz)*dt
        self.__wz=self.__wz+dwz
        self.DrawTrajectory(oldX,oldY,self.__x,self.__y)
        
    def AddQrCode(self,qrCode:List[QrCode]):
        self.__qr=qrCode

    def Control(self,dt,d1,d2,d3):
        """Управляющие элементы"""
        position=self.__door.position

        currentT=0
        #если преграды нет, то движемся прямо к двери
        if (d1>=20) and (d3>=20):
            alpha=tan(atan2((position[1]-self.__y),(position[0]-self.__x)))
            dwz=alpha-self.__wz
            currentT=dt
            c=10

        #если преграды нет, то есть ограничения, то сохряняем угол траектории
        if (d1>=20) and ((d2<=20) or (d3<=20)):
            dwz=0
            currentT=dt
            c=10
            
        #если справо свободно, то поворачиваем направо
        
        if (d1<20) and (d3>20):
            dwz=0
            while (self.dw>self.dw*currentT):
                dwz+=self.dw*dt
                currentT+=dt
            c=0
             
        #если справо занято, и слево свободно, то налево
        elif (d1<20) and (d3<20) and (d2>20):
            dwz=0
            while (self.dw>self.dw*currentT):
                dwz-=self.dw*dt
                currentT+=dt
            c=0


        #если занято с обоих сторон, то поворачиваем направо
        elif (d1<20) and (d3<20) and (d2<20) :
            dwz=0
            while (self.dw>self.dw*currentT):
                dwz+=self.dw*dt
                currentT+=dt
            c=0

        return c,dwz,currentT

    def BeginEnd(self,x0,x1):
        if x0<=x1:
            return x0,x1
        if x0>=x1:
            return x1,x0

    def Simulate(self,dt):
        """моделирование ситуации"""
        t0=0
        position=self.__door.position
        alpha=tan(atan2((position[1]-self.__y),(position[0]-self.__x)))
        self.__wz=alpha


        while(True):
            
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
            for wall in self.__walls:
                #дальномер, который спереди
                x,y=wall.getWallCoordinate(self.__wz,b)
                if (x==-1) and (y==-1): continue

                if (y<(alpha90*x+b_90)):
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
            resultXY=self.__room.getRoomCoordinate(self.__wz,b)
            for xy in resultXY:
                if (xy[1]<(alpha90*xy[0]+b_90)):
                    x=xy[0]
                    y=xy[1]
                    d=((x-self.__x)**2+(y-self.__y)**2)**0.5
                    rangefinder1.append(d)
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
            resultD3=min(rangefinder3)
            
            c,dwz,newDt=self.Control(dt,resultD1,resultD2,resultD3)


            qrlist=[]
            if self.__qr!=None:
                #обзор камеры справа
                _alpha90=tan(self.__wz+np.pi*30./180)
                _b_90=self.__y-_alpha90*self.__x
            
                _alpha_90=tan(self.__wz-np.pi*30./180)
                _b_minus90=self.__y-_alpha_90*self.__x
                for qr in self.__qr:
                    x,y=qr.GetQrCoordinate(alpha90,b_90,_alpha90,_b_90,_alpha_90,_b_minus90,self.__x,self.__y)
                    if (x!=-1) and (y!=-1):
                        qrlist.append([x,y])

            self.Move(dt,c,dwz)

            t0=t0+newDt
            if t0==100: break

            if ((position[1]-self.__y)**2+(position[0]-self.__x)**2)**0.5<40:
                break
