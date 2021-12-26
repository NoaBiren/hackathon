import socket
import struct

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
        try:
            pack, address = client_udp_socket.recvfrom(BUFFER_SIZE)#buffer_size
            print("Received offer from " + address[0]+", attempting to connect..")
            message = struct.unpack(">IbH",pack)
            self.connect_server_tcp(('127.0.0.1',message[2]))
        except:
            pass


    def connect_server_tcp(self,address):
        print("here")
        client_tcp_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp_socket.connect((address[0],address[1]))
        while True:

            client_tcp_socket.send(bytes(self.group_name+"\n", "utf-8"))



Client("noni")