import numpy as np
import cv2 as cv
import mouse
import win32api,win32con
import keyboard
# win32api.SetCursorPos((x,y))
#SCREEN SIZE
# ix,iy = 640,480

# mouse callback function
def click_mouse(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        posX,posY = normMousePos(x,y)
        print("x: " + str(posX))
        print("y: " + str(posY))
        
def MoveMouse(posX,width,posY,height):
    px,py = normMousePos(posX,width,posY,height)
    px=px-0.5
    py=py-0.5
    py*=-1
    # print(f"px:{px},py:{py}")
    nx = px*1920*(int(65535*2)/win32api.GetSystemMetrics(0))#+ int(65535/2)
    ny = py*1080*(int(65535*2)/win32api.GetSystemMetrics(1))#+ int(65535/2)

    # print(f"x:{nx},y:{ny}")
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,int(nx),int(ny))
    # win32api.SetCursorPos((int(px*1920),int(py*1080)))
    # mouse.move(px*1920,py*1080)

class inputStates:
    def __init__(self):
        self.canSendInput = False
        self.currentInput = ""
        self.upb = False
        self.downb = False
        self.leftb= False
        self.rightb = False
    def EvalInputs(self,posX,width,posY,height,up,down,left,right,radius):

        # isInDeadZone = self.CheckIfDeadZone(posX,posY,width,height,radius)
        

        vertical = self.CheckVertical(posY,height,up,down)
        horizontal = self.CheckHorizontal(posX,width,left,right)
            
        if vertical > 0:
            if True:
                print("UP")
                keyboard.press('up')
                self.currentInput='up'     
                self.canSendInput = False
                self.upb = True
                return
        else:
            self.upb = False
        if vertical < 0:
            if True:
                print("DOWN")
                keyboard.press('down')
                self.currentInput='down'
                self.canSendInput = False
                self.downb = True
                return
        else:
            self.downb = False
            
        if horizontal > 0:
            if True:
                print("RIGHT")
                keyboard.press('right')
                self.currentInput='right'
                self.canSendInput = False
                self.rightb = True
                return
        else:
            self.rightb = False
            

        if horizontal<0:
            if True:
                print("LEFT")
                keyboard.press('left')
                self.currentInput='left'
                self.canSendInput = False
                self.leftb = True
                return
        else:
            self.leftb = False
                
        if (not self.upb) and (not self.downb) and (not self.leftb) and (not self.rightb):
            if self.currentInput is not "":
                keyboard.release(self.currentInput) 
                print("Released " + self.currentInput)
                self.currentInput = ""
            self.canSendInput = True
            

    def CheckIfDeadZone(self,posX,posY,width,height,radius):
        cx = width//2
        cy = height//2
        distance = np.sqrt((posX-cx)**2 + (posY-cy)**2)
        if distance < radius:
            return True
        else:
            return False

    def CheckVertical(self,posY,height,up,down):
        if posY < up:
            return 1
        elif posY > (height-down):
            return -1
        else:
            return 0


    def CheckHorizontal(self,posX,width,left,right):
        if posX < left:
            return -1
        elif posX > (width-right):
            return 1
        else:
            return 0



def normMousePos(x,width,y,height):
    # return x/width,y/height
    return x/width,y/height
