##https://github.com/NoaBiren/hackathon.git
import select
import socket
import struct
import threading
import time
import colorama
import random
from scapy.arch import get_if_addr

# IP=socket.gethostbyname(socket.gethostname())
BUFFER_SIZE = 2048
DEST_PORT = 13117
HOST_IP = get_if_addr("eth1")
PORT = 2111


class Server:

    def __init__(self, IP, tcp_port):
        self.best = 0
        self.tcp_port = tcp_port
        self.IP = IP
        self.clients = {}
        self.num = 0
        self.game_over = False
        print(f"{colorama.Fore.GREEN}Server started, listening on IP address " + self.IP)
        threading.Thread(target=self.udp_handler).start()
        self.num_clients_lock = threading.Lock()
        self.second_client_event = threading.Event()
        self.create_tcp_connection()
        self.game_over_message = ''

    def udp_handler(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Enable broadcasting mode
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.bind((self.IP, DEST_PORT))
        pack = struct.pack(">IbH", 0xabcddbca, 0x2, self.tcp_port)

        while True:
            # print("here")
            server.sendto(pack, ('.'.join(HOST_IP.split(".")[:2]) + ".255.255", DEST_PORT))
            time.sleep(1)
            # self.udp_evenet_caller.wait() ## thread waits to other thread wake him up
            # self.udp_evenet_caller.set()  ## another thread wakes up the wait thread
            # self.udp_evenet_caller.clear() ## thread reset the event

    def create_tcp_connection(self):
        self.server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_tcp_socket.bind((self.IP, self.tcp_port))
        self.server_tcp_socket.listen()
        while True:
            while len(self.clients) < 2:
                # print("before accept")
                client, ip = self.server_tcp_socket.accept()
                print("accepted Client")
                self.clients[client] = ""
                threading.Thread(target=self.new_client_socket_handler, args=(client, ip)).start()
            self.Flag = False
            while (len(self.clients) == 2 and self.Flag == False):
                # print("before")
                self.num_clients_lock.acquire()
                if (self.num == 2):
                    # print("after")
                    self.Flag = True
                    self.game_over = False
                    if self.num == 2:
                        self.num = 0

                    self.num_clients_lock.release()
                    for cli in self.clients.keys():
                        try:
                            cli.send(bytes(self.game_over_message, 'utf-8'))
                            time.sleep(0.1)
                            cli.shutdown(socket.SHUT_RDWR)
                            cli.close()
                        except Exception as e:
                            pass
                        # cli.close()
                    self.clients = {}
                    print(f"{colorama.Fore.GREEN}Game Over")
                else:
                    self.num_clients_lock.release()
                time.sleep(0.1)

    def new_client_socket_handler(self, client, ip):
        # while True:
        try:
            name = client.recv(BUFFER_SIZE).decode("utf-8")
            self.clients[client] = name
            if (len(self.clients) != 2):
                self.second_client_event.wait()
                self.equation = self.formulate_equation()
            else:
                self.second_client_event.set()
            self.game_mode(client)
        except Exception as e:
            pass

    def game_mode(self, client):
        try:
            print("Game Started")
            time.sleep(2)  # TODO change to 10
            group_names = list(self.clients.values())
            message = "Welcome to Quick Maths!\nPlayer 1: " + group_names[0] + "\nPlayer 2: " + group_names[
                1] + "\nPlease answer the following question as fast as you can:\nHow much is " + self.equation[
                          1] + "?\nanswer: "
            client.send(bytes(message, 'utf-8'))
            t = time.time() + 10
            while (t - time.time() > 0 and self.game_over == False):
                ready = select.select([client], [], [], 0.2)
                if ready[0]:
                    answer = client.recv(BUFFER_SIZE).decode("utf-8")
                    self.num_clients_lock.acquire()
                    self.num += 1
                    if self.num == 1:
                        self.first_answered = self.clients[client]
                        for cli in self.clients.keys():
                            if cli != client:
                                self.not_first_answered = self.clients[cli]
                    # elif self.num == 2:
                    #     self.not_first_answered = self.clients[client]
                    #     self.num_clients_lock.release()
                    # else:
                    # self.num = 0
                    # self.num_clients_lock.release()
                    if answer == str(self.equation[0]):  # correct answer
                        self.game_over_message = "Game over!\nThe correct answer was " + str(
                            self.equation[0]) + "!\nCongratulations to the winner: " + self.first_answered + ""

                    else:
                        self.game_over_message = "Game over!\nThe correct answer was " + str(
                            self.equation[0]) + "!\nCongratulations to the winner: " + self.not_first_answered + ""
                    self.num_clients_lock.release()
                    self.game_over = True
                    return
                else:
                    if self.game_over:
                        self.num_clients_lock.acquire()
                        self.num = 2
                        self.num_clients_lock.release()

            self.game_over = True
            self.num_clients_lock.acquire()
            if t - time.time() > 10:
                self.num = 2
            self.num_clients_lock.release()
            self.game_over_message = "Game over!\nThe correct answer was " + str(self.equation[0])
            return
        except Exception as e:
            pass

    def formulate_equation(self):
        add_or_sub = random.randrange(0, 2)
        if add_or_sub == 0:
            first = random.randrange(0, 1000)
            second = random.randrange(first, first + 10)
            if first < second:
                answer = second - first
                string = "" + str(second) + "-" + str(first)
                return (answer, string)
            else:
                answer = first - second
                string = "" + str(first) + "-" + str(second)
                return (answer, string)
        else:
            first = random.randrange(0, 10)
            second = random.randrange(0, 10 - first)
            answer = first + second
            string = "" + str(first) + "+" + str(second)
            return (answer, string)


s = Server(HOST_IP, PORT)

