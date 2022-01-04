from multiprocessing import Process
import socket, select
import time

class User:
    def __init__(self, ipadrr):
        self.ipadrr = ipadrr

class Server():
    def run(self):
        self.CONNECTION_LIST = []
        self.RECV_BUFFER = 4096
        self.PORT = 5000
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.PORT))
        self.server_socket.listen(10)

        self.CONNECTION_LIST.append(self.server_socket)
        while 1:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST,[],[])
            for i, sock in enumerate(read_sockets):
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)

                else:
                    data = sock.recv(self.RECV_BUFFER).decode("utf-8")
                    if data:
                        self.parse_msg(data, addr, sock)
        self.server_socket.close()

    def parse_msg(self, data, addr, sock):
        command = data.replace('\n', '').split('|')
        if command[0] == 'connected': 
            self.broadcast_data(sock, "salope va".encode())

    def broadcast_data (self, sock, message):
        for socket in self.CONNECTION_LIST:
            if socket != self.server_socket:
                socket.send(message)

if __name__ == "__main__":
    host = 'localhost'
    port = 1234

    s = Server()
    s.run()
