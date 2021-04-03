
from Door import Door
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QColorDialog
import numpy as np

class Model:
    """
        Спереди модели установлена камера и дальномер
        Справа от модели установлен еще один дальномер
        Мера измерения - 1 см - 1 пиксель
    """
    def __init__(self,scene,x0,y0,dt,door:Door):
        self.__item=scene.addEllipse(x0-10,y0-10,20,20,QPen(QColorDialog(100,100,100)),QBrush(QColor(255,50,50)))
        self.__initX=x0
        self.__initY=y0
        self.__x=x0
        self.__y=y0
        self.__dt=dt
        self.__wz=0
        self.__door=door

        self.dw=10.*np.pi/180.
    
    def Move(self,Vx,Vy,wz):
        self.__x=self.__x+Vx*self.__dt
        self.__y=self.__y+Vy*self.__dt
        self.__wz=wz
        
    
    def Control(self,d1,d2):
        """Управляющие элементы"""
        if (d1>400):
            position=self.__door.position()
            Vx=(position[0]-self.__x)/((position[0]-self.__x)**2+(position[1]-self.__y)**2)
            Vy=(position[1]-self.__y)/((position[0]-self.__x)**2+(position[1]-self.__y)**2)
            return Vx,Vy,self.__wz

        if (d1<400) and (d2<400):
            Vx=0
            Vy=0
            w=self.__wz+self.dw*self.__dt
            return Vx,Vy,w
        
        if (d1<400) and (d2>400):
            Vx=0
            Vy=0
            w=self.__wz-self.dw*self.__dt
            return Vx,Vy,w


    def Simulate(self,dt):
        t0=0
        while(True):


            t0=t0+dt
