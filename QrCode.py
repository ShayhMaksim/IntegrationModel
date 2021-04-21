

from math import atan, pi
import math
from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsScene


class QrCode:
    """Дверь, в которую должен войти робот"""
    def __init__(self,x0,y0,w,scene:QGraphicsScene):
        self.__item=scene.addRect(QRectF(x0-20,y0-20,40,40),QColor(0,255,0))
        self.__x=x0
        self.__y=y0
        self.__w=w
        self.__detected=0

    
    @property
    def position(self):
        return self.__x,self.__y

    @property
    def item(self):
        return self.__item


    def GetQrCoordinate(self,alpha,xM,yM,xroom,yroom,d):
        if (((xM-self.__x)**2+(yM-self.__y)**2)**0.5<200):
            if (d*math.sin(alpha)>((xroom-self.__x)**2+(yroom-self.__y)**2)**0.5):
                self.__detected+=1
                if self.__detected==1:
                    self.__item.setPen(QColor(255,0,0))
                if self.__detected>1:
                    self.__item.setPen(QColor(255,0,255))
                if self.__detected>=10:
                    self.__item.setPen(QColor(255,255,0))    
                return self.__x,self.__y 
        return -1.,-1.

    def GetLocalCoordinate(self,x,y):
        if abs(self.__w)==math.pi or abs(self.__w)==0:
            x0=(x-self.__x)/math.cos(self.__w)
            y0=(y-self.__y)/math.cos(self.__w)

            return x0,y0,self.__w
        elif abs(self.__w)==math.pi*0.5 or abs(self.__w)==math.pi*1.5:
            y0=(x-self.__x)/math.sin(self.__w)
            x0=(y-self.__y)/(-math.sin(self.__w))

            return x0,y0,self.__w
        else:
            y0=(y-self.__y)+math.tan(self.__w)*(x-self.__x)
            x0=((x-self.__x)-y0*math.sin(self.__w))/math.cos(self.__w)

            return x0,y0,self.__w