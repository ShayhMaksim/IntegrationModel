

from math import atan, pi
from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsScene


class QrCode:
    """Дверь, в которую должен войти робот"""
    def __init__(self,x0,y0,scene:QGraphicsScene):
        self.__item=scene.addRect(QRectF(x0-20,y0-20,40,40),QColor(0,255,0))
        self.__x=x0
        self.__y=y0
        self.__detected=0

    
    @property
    def position(self):
        return self.__x,self.__y

    @property
    def item(self):
        return self.__item


    def GetQrCoordinate(self,alpha,b,alphaK1,bK1,alphaK2,bK2,x,y):
        # if (self.__y<self.__x*alpha+b):
        if (self.__y<alphaK1*self.__x+bK1) and (self.__y>alphaK2*self.__x+bK2):
            if (((x-self.__x)**2+(y-self.__y)**2)**0.5<200):              
                self.__detected+=1
                if self.__detected==1:
                    self.__item.setPen(QColor(255,0,0))
                if self.__detected>1:
                    self.__item.setPen(QColor(255,0,255))
                if self.__detected>=10:
                    self.__item.setPen(QColor(255,255,0))    
                return self.__x,self.__y
        # else:
        #     if (self.__y<alphaK1*self.__x+bK1) and (self.__y>alphaK2*self.__x+bK2):
        #         if (((x-self.__x)**2+(y-self.__y)**2)**0.5<200):
        #             self.__item.setPen(QColor(255,0,0))
        #             return self.__x,self.__y
        return -1.,-1.