#Import libraries
import sys,re
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import Clases
import cv2
import numpy as np
import queue
from collections import deque
chars = Clases.tools.Characteristics()

#.ui file path
uiFile = "./ui/MainUI.ui"
#Load ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)
#Capture video
captura = cv2.VideoCapture(0)


class UIWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btnCalibrar.clicked.connect(self.Calibrar)
        self.timer = QTimer()
        self.btnEmpezar.clicked.connect(self.controlTimer)
        self.timer.timeout.connect(self.viewCam)
        self.hasCalibrated = False
        self.ftgmas = deque()
        self.inputStatesclass = Clases.mousepos.inputStates()
    def printxd(self):
        print("calibrado")
    
    def Calibrar(self):
        # print("Tamaño: "  + str(len(self.ftgmas)))
        
        # sumatoria = np.zeros(self.ftgmas[0].size)
        # for i in range(5):
        #     sumatoria = cv2.add(sumatoria,np.array(self.ftgmas[i]))
        # sumatoria = cv2.multiply(sumatoria,0.2)
        self.HSVMIN,self.HSVMAX = Clases.calibration.CalibrationClass.Calibrate(self.ROI)
        self.labelhuemin.setText(str(self.HSVMIN[0]))
        self.labelhuemax.setText(str(self.HSVMAX[0]))
        self.labelsatmin.setText(str(self.HSVMIN[1]))
        self.labelsatmax.setText(str(self.HSVMAX[1]))
        self.labelvalmin.setText(str(self.HSVMIN[2]))
        self.labelvalmax.setText(str(self.HSVMAX[2]))
        self.labelcolormin.setStyleSheet(f"background-color: hsv({self.HSVMIN[0]*2},{self.HSVMIN[1]},{self.HSVMIN[2]})") 
        self.labelcolormax.setStyleSheet(f"background-color: hsv({self.HSVMAX[0]*2},{self.HSVMAX[1]},{self.HSVMAX[2]})")
        self.hasCalibrated = True
        self.segment = Clases.segmentation.Segmentation(*self.HSVMIN,*self.HSVMAX)
        # self.segment = Clases.segmentation.Segmentation(45,50,50,75,200,200)
    def Ejecutar(self):
        print("ah")
    
    def viewCam(self):
    # read imageS in BGR format
        disponible, fotograma = captura.read()
        fotograma = cv2.flip(fotograma,1)
        

        self.upPos  = self.upSlider.value()
        self.downPos  = self.downSlider.value()
        self.leftPos  = self.leftSlider.value()
        self.rightPos  = self.rightSlider.value()
        # fotograma = Clases.tools.Quality.makebetter(fotograma)

        h, w, channel = fotograma.shape    
        self.ROI = np.array(fotograma[h//2-60:h//2+60,w//2-60:w//2+60])


        if len(self.ftgmas) < 5:
            self.ftgmas.append(self.ROI)
            
        else:
            self.ftgmas.popleft()
            self.ftgmas.append(self.ROI)

        
    # convert image to RGB format
        fotogramaRGB = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        if self.hasCalibrated:
            self.segmentedIMG = self.segment.segmentate(fotograma)
            self.posX,self.posY,self.message = Clases.tools.Characteristics.findCentroid(self.segmentedIMG)
            
            if self.message != "Centroid Not Found":
                # print("posx : " + str(self.posX))
                # Clases.mousepos.MoveMouse(self.posX,w,self.posY,h)
                self.inputStatesclass.EvalInputs(self.posX,w,self.posY,h,self.upPos,self.downPos,self.leftPos,self.rightPos,125)
                # Clases.mousepos.MoveMouse(w//2,w,h//2,h)
            
            cv2.circle(fotogramaRGB, (int(self.posX), int(self.posY)), 5, (255, 255, 255), -1)
            cv2.putText(fotogramaRGB, self.message, (int(self.posX) - 25, int(self.posY) - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
       
        cv2.rectangle(fotogramaRGB,(w//2-60,h//2-60),(w//2+60,h//2+60),(0,255,0),5)
        
        cv2.rectangle(fotogramaRGB,(0,0),(w,self.upPos),(255,0,0),1)
        cv2.rectangle(fotogramaRGB,(0,h-self.downPos),(w,h),(255,0,0),1)
        cv2.rectangle(fotogramaRGB,(0,0),(self.leftPos,h),(255,0,0),1)
        cv2.rectangle(fotogramaRGB,(w-self.rightPos,0),(w,h),(255,0,0),1)
        # cv2.circle(fotogramaRGB, (w//2,h//2),125,(0,0,255),1)


        ROIRGB = cv2.cvtColor(self.ROI, cv2.COLOR_BGR2RGB)
        self.SetImages(fotogramaRGB,self.qlabel)
        self.SetImages(ROIRGB,self.labelCalibration)



    def SetImages(self,IMG,label):
        h, w, channel = IMG.shape        
        step = channel * w
        
        qImg = QImage(IMG.data, w, h, step, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qImg))


        

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(16)
            # update control_bt text
            self.btnEmpezar.setText("Parar")
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.btnEmpezar.setText("Empezar")

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = UIWindow()
    window.show()
    sys.exit(app.exec_())