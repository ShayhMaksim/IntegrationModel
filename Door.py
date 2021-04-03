
from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsScene


class Door:
    """Дверь, в которую должен войти робот"""
    def __init__(self,x0,y0,scene:QGraphicsScene):
        self.__item=scene.addRect(QRectF(x0-20,y0-20,40,40),QColor(0,0,255))
        self.__x=x0
        self.__y=y0

    
    @property
    def position(self):
        return self.__x,self.__y

    @property
    def item(self):
        return self.__item