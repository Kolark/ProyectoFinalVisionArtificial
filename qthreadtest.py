from PyQt5.QtCore import QObject, QThread, pyqtSignal
# Snip...
import time
class MyThread(QThread):
    # Create a counter thread
    def run(self):
        cnt = 0
        while cnt < 40:
            cnt+=1
            print("Holaa")
            time.sleep(0.1)


def setProgressVal(hola):
    print("holaa")

    

if __name__ == "__main__":
    thread = MyThread()
    thread.start()
    thread.run()
    print("THREAD ENDED")