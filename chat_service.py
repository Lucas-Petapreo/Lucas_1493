"""
    chat room
    env: python
    socket fork Exercise
"""
from socket import *
import os, sys

# 服务器地址
ADDR = ('0.0.0.0', 12345)
# 存储用户信息
user = {}


def do_quit(sockfd, name):
    msg = '%s left the room' % name
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])
        else:
            sockfd.sendto(b'EXIT', user[name])
    del user[name]


def do_chat(sockfd, name, text):
    msg = '%s says: %s' % (name, text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])


def do_login(sockfd, name, addr):
    if name in user:
        sockfd.sendto(b'User already exists.', addr)
        return
    sockfd.sendto(b'OK', addr)
    # 通知其他人
    msg = '%s enter the chat room' % name
    for name in user:
        sockfd.sendto(msg.encode(), user[name])
    # 将用户加入
    user[name] = addr


def accept_request(sockfd):
    while True:
        data, addr = sockfd.recvfrom(1024)
        msg = data.decode().split(' ')
        if msg[0] == 'L':
            do_login(sockfd, msg[1], addr)
        elif msg[0] == 'C':
            do_chat(sockfd, msg[1], ' '.join(msg[2:]))
        elif msg[0] == 'Q':
            do_quit(sockfd, msg[1])


# 创建网络连接
def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.bind(ADDR)

    # 接受请求, 处理客户请求
    accept_request(sockfd)


if __name__ == '__main__':
    main()
