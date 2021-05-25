import socket
from PyQt5.QtCore import QObject, QThread, pyqtSignal
# Snip...
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


class MyThread(QThread):
    # Create a counter thread
    def run(self):
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print(data.decode('utf-8'))
            # time.sleep(0.1)


    

if __name__ == "__main__":
    thread = MyThread()
    thread.start()
    thread.run()
    print("THREAD ENDED")