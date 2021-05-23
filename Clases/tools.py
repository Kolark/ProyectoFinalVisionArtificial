import cv2
import numpy as np
print("UTILS IMPORTED")
class Characteristics:
    @staticmethod
    def findCentroid(segmentedImage):
        height,width = segmentedImage.shape
        returnImage = np.zeros((height,width))
        returnImage += segmentedImage
        ret,thresh = cv2.threshold(segmentedImage,127,255,0)
        M = cv2.moments(thresh)
        cX = 0
        cY = 0
        message = ""
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            message = "Centroid"
        except:
            cX = width/2
            cY = height/2
            message = "Centroid Not Found"

        cv2.circle(returnImage, (int(cX), int(cY)), 5, (255, 255, 255), -1)
        cv2.putText(returnImage, message, (int(cX) - 25, int(cY) - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return cX,cY,message


class Quality:
    @staticmethod
    def makebetter(img):
        b,g,r = cv2.split(img)
        bMin,bDelta = Quality.Encontrar(b)
        gMin,gDelta = Quality.Encontrar(g)
        rMin,rDelta = Quality.Encontrar(r)

        b = cv2.subtract(b,bMin)
        g = cv2.subtract(g,gMin)
        r = cv2.subtract(r,rMin)

        salida = cv2.merge((b,g,r))
        return salida
    @staticmethod
    def Encontrar(imagen):
        minimo,maximo, ret, ret = cv2.minMaxLoc(imagen)
        delta = 255/(maximo-minimo)
        return minimo,delta