
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsScene


class Wall:

    def __init__(self,x0,y0,x1,y1,scene:QGraphicsScene):
        self.__item=scene.addLine(x0,y0,x1,y1,QPen(QColor(255,0,0)))
        self.__x0=x0
        self.__y0=y0
        self.__x1=x1
        self.__y1=y1


        self.__alpha=(y1-y0)/(x1-x0)
        self.__B=y0-x0*(y1-y0)/(x1-x0)

    @property
    def item(self):
        return self.__item

    def getRoomCoordinate(self,alpha,B):
        y=(alpha*self.__B-self.__alpha*B)/(alpha-self.__alpha)
        x=(y-B)/alpha

        if self.__x0<=self.__x1:
            minX=self.__x0
            maxX=self.__x1
        else:
            minX=self.__x1
            maxX=self.__x0
        
        if self.__y0<=self.__y1:
            minY=self.__y0
            maxY=self.__y1
        else:
            minY=self.__y1
            maxY=self.__y0
         
        if x>=minX and x<=maxX and y>=minY and y<=maxY:
            return x,y

        
        