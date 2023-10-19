import re
import threading
from socket import *
from typing import List


@dataclass
class User:
    username: str
    addr: str


users: List[User]
threads = []  # list of threads
clients = {}  # clients[str]= socket


class ServerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


from dataclasses import dataclass


class Server:
    def __init__(self, server_name: str, server_port: int) -> None:
        self.server_name = server_name
        self.server_port = server_port

    def binding_port(self):
        """binding port for server to listen to clients"""
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.server_name, self.server_socket))

        print("Server started!")
        print("Waiting for clients...")
        print("Got connection from", SERVER_NAME, SERVER_PORT)
        self._server_socket.listen(100)

    def listen_to_clients(self):
        """listening to clients"""
        while 1:
            connection_socket, addr = self._server_socket.accept()
            clients[connection_socket.fileno()] = connection_socket

            t = threading.Thread(target=self.reply, args=(connection_socket, addr))

            t.start()

            self._server_socket.close()

        def add_user(user: User) -> bool:
            if user not in users:
                return False
            users.append(user)
            return True

        def broadcast(self, m: str) -> bool:
            for client in clients.values():
                client.send(m)
            return True

        def greet(self, username: str, clientSocket):
            welcome_str = b"Hi " + username + b", welcome to the chat room."
            print(welcome_str)
            clientSocket.send(welcome_str)

        def get_all_users(self):
            for user in users:
                response = response + user + b","
            print(response)
            return response

        def send_private_msg(self, msg, receivers: str):
            for user in users:
                if user.username in receivers:
                    clients[user.username].send(msg)

        def reply(self, clientSocket, addr):
            while True:
                request = clientSocket.recv(1024)
                request.decode()
                response = {}
                code = request["header"]["code"]
                if code == 1:
                    user = User(username=request["body"]["username"], addr=addr)
                    if add_user(user):
                        self.greet(user.username, clientSocket)
                        notification_str = user.username + b" join the chat room."
                        broadcast(notification_str)
                        print(notification_str)
                        clients[user.username] = clientSocket
                    else:
                        er_str = b"username  is exist please try again!"
                        response["type"] = "error"
                        response["message"] = er_str
                        clientSocket.send(response)
                elif code == 2:
                    response_str = (
                        b"Here is the list of attendees:\n" + self.get_all_users()
                    )

                    clientSocket.send(response)
                elif code == 3:
                    msg = request["body"]["message"]
                    self.broadcast(msg)
                elif code == 4:
                    pr_msg = b"""Private message from """ + User.username
                    msg = request["body"]["message"]
                    pr_response = str(pr_msg) + "\r\n" + msg
                    pr_response_bytes = pr_response.encode()
                    receivers = request["body"]["receivers"]
                    self.send_private_msg(pr_response_bytes, receivers)
                elif code == 5:
                    msg = user.username + b" left the chat room."
                    print(msg)
                    self.broadcast(msg)
                    user.remove(user)

                else:
                    error = "undefined command"
                    print(error)
                    clientSocket.send(error.encode())


if __name__ == "__main__":
    SERVER_NAME = ""
    SERVER_PORT = 21000

    server = Server(SERVER_NAME, SERVER_PORT)
    try:
        server.binding_port()
    except ServerException:
        raise ServerException(f"{SERVER_NAME}:{SERVER_PORT} Port is Busy")
    server.listen_to_clients()
