import re
import threading
from socket import *
from typing import List
from dataclasses import dataclass
import json
import ast


@dataclass
class User:
    username: str
    addr: str


users = []
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
        self._server_socket = None

    def binding_port(self):
        """binding port for server to listen to clients"""
        self._server_socket = socket(AF_INET, SOCK_STREAM)
        self._server_socket.bind((self.server_name, self.server_port))

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

    def accept(self):
        connection_socket, addr = self._server_socket.accept()
        return connection_socket, addr

    def add_user(self, user: User) -> bool:
        if user in users:
            return False
        users.append(user)
        return True

    def broadcast(self, m: str) -> bool:
        for client in clients.values():
            client.send(m)
        return True

    def greet(self, username: str, clientSocket):
        welcome_str = "Hi " + username + ", welcome to the chat room."
        print(welcome_str)
        clientSocket.send(welcome_str.encode())

    def get_all_users(self):
        response = ""
        for user in users:
            response += user.username + ","
        return response

    def send_private_msg(self, msg, receivers: str):
        for user in users:
            if user.username in receivers:
                clients[user.username].send(msg)

    def reply(self, clientSocket, addr):
        while True:
            request = clientSocket.recv(1024)
            request.decode()
            print(request)
            request_dict = ast.literal_eval(request.decode("utf-8"))

            code = int(request_dict["code"])
            if code == 1:
                user = User(username=request_dict["username"], addr=addr)
                if self.add_user(user):
                    self.greet(user.username, clientSocket)
                    notification_str = user.username + " join the chat room."
                    self.broadcast(notification_str.encode())
                    print(notification_str)
                    clients[user.username] = clientSocket
                else:
                    er_str = b"username  is exist please try again!"

                    clientSocket.send(er_str)
            elif code == 2:
                response_str = "Here is the list of attendees:\n" + self.get_all_users()

                clientSocket.send(response_str.encode())
            elif code == 3:
                msg = request_dict["message"]
                self.broadcast(msg.encode())
            elif code == 4:
                pr_msg = "Private message from " + User.username
                msg = request["message"]
                pr_response = str(pr_msg) + "\r\n" + msg
                pr_response_bytes = pr_response.encode()
                receivers = request_dict["receivers"]
                self.send_private_msg(pr_response_bytes, receivers)
            elif code == 5:
                msg = user.username + " left the chat room."
                print(msg)
                self.broadcast(msg.encode())
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
