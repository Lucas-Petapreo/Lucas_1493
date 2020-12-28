"""
    chat room
    client
"""
from socket import *
import os, sys

ADDR = ('127.0.0.1', 12345)


def send_msg(sockfd, name):
    while True:
        try:
            text = input('Speak: ')
        except KeyboardInterrupt:
            text = 'quit'
        if text == 'quit':
            msg = 'Q' + name
            sockfd.sendto(msg.encode(), ADDR)
            sys.exit('Exit Chat Room')
        msg = 'C %s %s' % (name, text)
        sockfd.sendto(msg.encode(), ADDR)


def recive_msg(sockfd):
    while True:
        msg, addr = sockfd.recvfrom(2048)
        # 服务端发送EXIT让客户端退出
        if msg.decode() == 'EXIT':
            sys.exit()
        print(msg.decode())


def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("Name: ")
        msg = 'L ' + name
        sockfd.sendto(msg.encode(), ADDR)
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == 'OK':
            print('You have already in the Chat Room')
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit('Error')
    elif pid == 0:
        send_msg(sockfd, name)
    else:
        recive_msg(sockfd)


if __name__ == '__main__':
    main()
