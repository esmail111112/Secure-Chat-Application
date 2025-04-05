
import socket
import threading
from secure_chat import SecureChat

class P2PClient:
    def __init__(self, name, is_host, listen_port, signaling_host="127.0.0.1", signaling_port=5000):
        self.name = name
        self.is_host = is_host
        self.listen_port = listen_port
        self.signaling_host = signaling_host
        self.signaling_port = signaling_port
        self.peer_socket = None
        self.secure = None

    def connect_to_signaling(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.signaling_host, self.signaling_port))
        peer_info = sock.recv(1024).decode()
        sock.close()
        return peer_info.split(":")

    def listen_for_peer(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", self.listen_port))
        server.listen(1)
        print("[CLIENT] Waiting for peer to connect...")
        self.peer_socket, _ = server.accept()
        print("[CLIENT] Peer connected.")

    def connect_to_peer(self, peer_ip, peer_port):
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.connect((peer_ip, int(peer_port)))
        print("[CLIENT] Connected to peer.")

    def exchange_keys(self):
        if self.is_host:
            key = SecureChat().key
            self.peer_socket.send(key)
            self.secure = SecureChat(key)
        else:
            key = self.peer_socket.recv(1024)
            self.secure = SecureChat(key)

    def send_messages(self):
        while True:
            msg = input(f"[{self.name}]: ")
            if msg.lower() == "end":
                break
            self.peer_socket.send(self.secure.encrypt(msg))

    def receive_messages(self):
        while True:
            try:
                data = self.peer_socket.recv(1024)
                if not data:
                    break
                print(f"[Peer]: {self.secure.decrypt(data)}")
            except:
                break

    def start(self):
        peer_ip, peer_port = self.connect_to_signaling()
        if self.is_host:
            self.listen_for_peer()
        else:
            self.connect_to_peer(peer_ip, peer_port)

        self.exchange_keys()

        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.send_messages()
        self.peer_socket.close()

if __name__ == "__main__":
    client = P2PClient(name="Esmail", is_host=True, listen_port=6000)
    client.start()
