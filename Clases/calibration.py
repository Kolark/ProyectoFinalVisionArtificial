# import cv2
# import numpy as np
# fotograma = cv2.imread("testimage2.png")
# # captura = cv2.VideoCapture(0)

# while(True):
#     # disponible, fotograma = captura.read()
#     height,width,channels = fotograma.shape
#     # if disponible == True:
#     if True:   
#         # cv2.rectangle(fotograma,(0,0),(height,width),(0,255,0),20)
#         # r = cv2.selectROI(im)

        
#         cut = fotograma[0:500,0:500]
#         hsv = cv2.cvtColor (cut, cv2.COLOR_BGR2HSV)
#         h, s, v = cv2.split (hsv)
#         mean1 = h.mean()
#         mean2 = s.mean()
#         mean3 = v.mean()
#         stdevm1 = np.std(h)
#         print("h " + str(mean1) + " - stdev: " + str(stdevm1))
#         print("s" + str(mean2))
#         print("v " + str(mean3))
#         cv2.imshow("Segmentado",cut)
#         cv2.imshow("Segmentado3",fotograma)
#     ch = 0xFF & cv2.waitKey(1)
#     if ch == ord('q'):
#         break

# cv2.destroyAllWindows()
import cv2
import numpy as np
class CalibrationClass:

    @staticmethod
    def Calibrate(ROI):
        hsv = cv2.cvtColor (ROI, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split (hsv)
        HueMean = h.mean()
        SatMean = s.mean()
        ValMean = v.mean()
        HueSTD = np.std(h)
        SatSTD = np.std(s)
        ValSTD = np.std(v)

        HueMIN = (HueMean-HueSTD*3) % 179
        SatMIN = np.clip(SatMean-SatSTD*5,0,255)
        ValMIN = np.clip(ValMean-ValSTD*5,0,255)
        HueMAX = (HueMean+HueSTD*3) % 179
        SatMAX = np.clip(SatMean+SatSTD*5,0,255)
        ValMAX = np.clip(ValMean+ValSTD*5,0,255)

        return np.array((HueMIN,SatMIN,ValMIN)),np.array((HueMAX,SatMAX,ValMAX))
        
