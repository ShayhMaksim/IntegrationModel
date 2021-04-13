from typing import List
from Model import Model
from Door import Door
from Wall import Wall
from Room import Room
from QrCode import QrCode
from PyQt5.QtGui import QPen
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QWidget,QApplication,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPainter, QColor, QPen,QBrush
from PyQt5.QtCore import QRectF
import sys

app = QApplication(sys.argv)
scene = QGraphicsScene()
graphicsView = QGraphicsView(scene)
graphicsView.setWindowTitle("Комплексирование информационных приборов")
graphicsView.show()
graphicsView.resize(800,600)

room=Room(0,0,400,scene)

wall1=Wall(100,200,200,300,scene)
wall2=Wall(100,150,300,100,scene)
wall3=Wall(300,150,250,300,scene)

wall4=Wall(100,150,200,230,scene)
#wall5=Wall(200,350,150,250,scene)

wall6=Wall(260,150,300,250,scene)

door=Door(400,100,scene)

walls=[wall1,wall2,wall3,wall4,wall6]

QrCode1=QrCode(0,50,-np.pi*3./2.,scene)
QrCode2=QrCode(50,0,-0,scene)

QrCode3=QrCode(50,400,-np.pi,scene)
QrCode4=QrCode(0,400-50,-np.pi*3./2.,scene)

QrCode5=QrCode(400,50,-np.pi*0.5,scene)
QrCode6=QrCode(400-50,0,-0,scene)

QrCode7=QrCode(400,400-50,-np.pi*0.5,scene)
QrCode8=QrCode(400-50,400,-np.pi,scene)

qrList=[QrCode1,QrCode2,QrCode3,QrCode4,QrCode5,QrCode6,QrCode7,QrCode8]
model=Model(50,300,scene,room,door)
model.AddQrCode(qrList)
model.AddWalls(walls)
model.Simulate(0.1)
model.FilterKalman(0.1)
graphicsView.show()


import matplotlib.pyplot as plt

t=[]
a=[]
for j in model.RealData:
    t.append(j[0])
    a.append(j[3])

ai=[]
for j in model.Y:
    ai.append(j[2][2])

afk=[]
for j in model.Result:
    afk.append(j[3])

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции угла курса") # заголовок
plt.xlabel("t, сек.") # ось абсцисс
plt.ylabel("Угол курса, рад.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, a,'r',label="Реальное значение угла курса")  # построение графика
plt.plot(t, afk,'b',label="Значение угла курса - ФК")  # построение графика
plt.plot(t, ai,'g',label="Измерение угла курса")  # построение графика
plt.legend(loc=0)
plt.savefig('Эволюция компоненты Курса')


t=[]
x=[]
y=[]
rx=[]
ry=[]
kx=[]
ky=[]

for j in model.RealData:
    t.append(j[0])
    x.append(j[1])
    y.append(j[2])
    rx.append(j[4])
    ry.append(j[5])
    kx.append(10)
    ky.append(10)

xi=[]
yi=[]
rxi=[]
for j in model.Y:
    xi.append(j[2][0])
    yi.append(j[2][1])
    #rxi.append(j[3][3])

xfk=[]
yfk=[]
rxfk=[]
ryfk=[]
kxfk=[]
kyfk=[]
qrxfk=[]
qryfk=[]
for j in model.Result:
    xfk.append(j[1])
    yfk.append(j[2])
    rxfk.append(j[4])
    ryfk.append(j[5])
    qrxfk.append(j[6])
    qryfk.append(j[7])
    kxfk.append(j[8])
    kyfk.append(j[9])

p_x=[]
p_y=[]
p_a=[]
p_rx=[]
p_ry=[]
p_kx=[]
p_ky=[]
p_qrx=[]
p_qry=[]
for p in model.P:
    p_x.append(p[1])
    p_y.append(p[2])
    p_a.append(p[3])
    p_rx.append(p[4])   
    p_ry.append(p[5])
    p_qrx.append(p[6])
    p_qry.append(p[7])
    p_kx.append(p[8])   
    p_ky.append(p[9])    

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("y, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, ry,'r',label="Реальное значение траектории")  # построение графика
plt.plot(t, ryfk,'b',label="Результат - ФК")  # построение графика
plt.plot(t, y,'g',label="БИНС")  # построение графика
#plt.plot(t, yi,'g',label="Результат измерения- ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('Траектория движения Y')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, rx,'r',label="Реальное значение траектории")  # построение графика
plt.plot(t, rxfk,'b',label="Результат - ФК")  # построение графика
plt.plot(t, x,'g',label="БИНС")  # построение графика
#plt.plot(t, xi,'g',label="Результат измерения- ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('Траектория движения X')



plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка для компоненты X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(x)-np.asarray(xfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_x)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_x))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка X')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка для компоненты Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("y, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(y)-np.asarray(yfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_y)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_y))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка Y')


plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка для угла курса") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("Угол курса, рад.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(a)-np.asarray(afk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_a)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_a))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка угла курса')


plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка для компоненты X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(rx)-np.asarray(rxfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_rx)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_rx))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка положения робота X')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка для компоненты Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("y, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(ry)-np.asarray(ryfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_ry)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_ry))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка положения робота Y')


plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции K1") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("k1") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, kx,'r',label="Реальное значение K1")  # построение графика
plt.plot(t, kxfk,'b',label="Результат K1 - ФК")  # построение графика
#plt.plot(t, yi,'g',label="Результат измерения- ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('K1')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции K2") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("k2") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, ky,'r',label="Реальное значение K2")  # построение графика
plt.plot(t, kyfk,'b',label="Значение K2 - ФК")  # построение графика
#plt.plot(t, yi,'g',label="Результат измерения- ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('K2')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка K1") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("K1") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(kx)-np.asarray(kxfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_kx)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_kx))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка K1')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка K2") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("K2") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(ky)-np.asarray(kyfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_ky)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_ky))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка K2')



plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка Qr X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(rx)-np.asarray(qrxfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_qrx)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_qrx))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка Qr X')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка Qr Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("y, см") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(ry)-np.asarray(qryfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_qry)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_qry))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка Qr Y')


sys.exit(app.exec())