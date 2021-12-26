##https://github.com/NoaBiren/hackathon.git

import socket
import struct
import threading
import time
import random

# IP=socket.gethostbyname(socket.gethostname())
BUFFER_SIZE=2048
DEST_PORT=13117
class Server:


    def __init__(self,IP,tcp_port):
        self.tcp_port=tcp_port
        self.IP=IP
        self.clients=[]
        threading.Thread(target=self.udp_handler).start()
        print("Server started, listening on IP address " + self.IP)
        self.create_tcp_connection()



    def udp_handler(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Enable broadcasting mode
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.bind(("",DEST_PORT))
        pack = struct.pack(">IbH", 0xabcddbca, 0x2, self.tcp_port)
        while True:
            print(formulate_equation())
            server.sendto(pack, ('<broadcast>', DEST_PORT))
            time.sleep(1)
            # self.udp_evenet_caller.wait() ## thread waits to other thread wake him up
            # self.udp_evenet_caller.set()  ## another thread wakes up the wait thread
            # self.udp_evenet_caller.clear() ## thread reset the event


    def create_tcp_connection(self):
        server_tcp_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp_socket.bind((self.IP,self.tcp_port))
        server_tcp_socket.listen(2)
        while len(self.clients)<2:
            client,ip=server_tcp_socket.accept()
            print("tcp success")
            self.clients.append(client)
            threading.Thread(target=self.new_client_socket_handler,args=(client,ip)).start()



    def new_client_socket_handler(self,client,ip):
        #print("gal haben zona")
        while True:
            try:
                message = client.recv(BUFFER_SIZE).decode("utf-8")
                if (clients_counter == 2):
                    time.sleep(10)
                    self.game_mode()
            except:
                pass


    #def game_mode(self):

def formulate_equation():
    add_or_sub=random.randrange(0,2)
    if add_or_sub==0:
        first = random.randrange(0,1000)
        second = random.randrange(first,first+10)
        if first<second:
            return "" + str(second) + "-" + str(first)
        return "" + str(first) + "-" + str(second)
    else:
        first = random.randrange(0,10)
        second = random.randrange(0,10-first)
        return "" + str(first) + "+" + str(second)
Server('127.0.0.1',2512)
