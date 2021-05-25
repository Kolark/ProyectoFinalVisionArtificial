import socket

UDP_IP = "127.0.0.1"

UDP_PORT = 5065

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


def SendToUnity(message):
    sock.sendto(message.encode(),(UDP_IP,UDP_PORT))
