import select
import socket
import struct
import sys
import threading
import msvcrt
import time
from multiprocessing import Process
import keyboard

BUFFER_SIZE=2048
PORT = 13117

class Client:

    #open client socket
    def __init__(self,group_name):
        self.group_name=group_name
        client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Client started, listening for offer requests...")
        client_udp_socket.bind(("", PORT))
    #looking for a server
        while True:
            try:
                pack, address = client_udp_socket.recvfrom(BUFFER_SIZE)#buffer_size
                print("Received offer from " + address[0]+", attempting to connect..")
                message = struct.unpack(">IbH",pack)
                self.connect_server_tcp(('127.0.0.1',message[2]))
            except Exception as e:
                print(e)


    def connect_server_tcp(self,address):
        self.client_tcp_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_tcp_socket.connect((address[0],address[1]))
        self.client_tcp_socket.send(bytes(self.group_name+"\n", "utf-8"))
        #equation message
        message = self.client_tcp_socket.recv(BUFFER_SIZE).decode("utf-8")
        print(message)
        ###
        t= threading.Thread(target=self.get_messages).start()
        t2=threading.Thread(target=self.send_messages).start()
        time.sleep(10)
        return
        # my_answer = input()
        # self.client_tcp_socket.send(bytes(my_answer + "\n", "utf-8"))
        # i, o, e = select.select([sys.stdin], [], [], 10)
        #
        # if (i):
        #     my_answer = sys.stdin.readline()[0]
        #     self.client_tcp_socket.send(bytes(my_answer + "\n", "utf-8"))
        # else:
        #     return
        ###
        # t = threading.Thread(target=self.send_messages())
        # t.start()
        # time.sleep(10)
        # while True:

        # message = self.client_tcp_socket.recv(BUFFER_SIZE).decode("utf-8")
        # print(message)
        # #     time.sleep(10)
        # t.kill()
        #game over message
        # ready = select.select([self.client_tcp_socket], [], [], 10)
        # if ready[0]:
        #     message = self.client_tcp_socket.recv(BUFFER_SIZE).decode("utf-8")
        #     print(message)
        # while True:
        #     message = self.client_tcp_socket.recv(BUFFER_SIZE)
        #     print(message.decode('utf-8'))


    def get_messages(self):
        while True:
            try:
                message = self.client_tcp_socket.recv(BUFFER_SIZE).decode('utf-8')
                if message!="":
                    print(message)
            except:
                pass

    def send_messages(self):
        my_answer = input()
        self.client_tcp_socket.send(bytes(my_answer + "\n", "utf-8"))
        ####

        # time.sleep(10)
        # my_answer = input()
        # self.client_tcp_socket.send(bytes(my_answer + "\n", "utf-8"))
        # ready = select.select([self.client_tcp_socket], [], [], 10)
        # if ready[0]:
        #     message = self.client_tcp_socket.recv(BUFFER_SIZE).decode("utf-8")
        #     print(message)
        # else:
        #     return



Client("noni3")