from PyQt5.QtWidgets import QGraphicsScale, QGraphicsScene, QGraphicsView

#пусть комната будет квадратной
class Room:
    def __init__(self,x0,y0,size,scene:QGraphicsScene):
        """Конструктор"""
        scene.addLine(x0,y0,x0,y0+size)
        scene.addLine(x0,y0,x0+size,y0)
        scene.addLine(x0+size,y0,x0+size,y0+size)
        scene.addLine(x0,y0+size,x0+size,y0+size)
        self.__x0=x0
        self.__y0=y0
        self.__size=size

   
    def getRoomCoordinate(self,alpha,B):
        """ 
            Метод расчета координаты комнаты при использовании дальномера
        """
        x=self.__x0
        y=alpha*x+B
        if (y>=self.__y0) and (y<=(self.__y0+self.__size)):
            return x,y

        x=self.__x0+self.__size
        y=alpha*x+B
        if (y>=self.__y0) and (y<=(self.__y0+self.__size)):
            return x,y

        y=self.__y0
        x=(y-B)/alpha
        if (x>=self.__x0) and (x<=(self.__x0+self.__size)):
            return x,y

        y=self.__y0+self.__size
        x=(y-B)/alpha
        if (x>=self.__x0) and (x<=(self.__x0+self.__size)):
            return x,y

    
      