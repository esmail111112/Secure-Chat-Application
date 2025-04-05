import socket
import threading

class SignalingServer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"[SERVER] Listening on {self.host}:{self.port}")

        while len(self.clients) < 2:
            client_socket, addr = self.server_socket.accept()
            print(f"[SERVER] Connected by {addr}")
            self.clients.append((client_socket, addr))

        self.exchange_info()

    def exchange_info(self):
        addr1 = self.clients[0][1]
        addr2 = self.clients[1][1]

        # أرسل عنوان العميل الأول للثاني
        self.clients[1][0].send(f"{addr1[0]}:6000".encode())
        # أرسل عنوان العميل الثاني للأول
        self.clients[0][0].send(f"{addr2[0]}:6001".encode())

        for client, _ in self.clients:
            client.close()

if __name__ == "__main__":
    server = SignalingServer()
    server.start()
