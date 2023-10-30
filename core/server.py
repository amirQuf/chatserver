import threading
from socket import *
from dataclasses import dataclass
import ast


@dataclass
class User:
    """Represents a user in the chat room."""
    username: str
    addr: str


users = []
threads = []  # list of threads
clients = {}  # clients[str]= socket


class ServerException(Exception):
    """Custom exception class for server-related exceptions."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


from dataclasses import dataclass


class Server:
    def __init__(self, server_name: str, server_port: int) -> None:
        """
        Initialize a Server instance.

        Args:
            server_name (str): The server's hostname or IP address.
            server_port (int): The port on which the server listens for connections.
        """
        self.server_name = server_name
        self.server_port = server_port
        self._server_socket = None

    def binding_port(self):
        """Bind the server to a specific host and port for listening."""
        self._server_socket = socket(AF_INET, SOCK_STREAM)
        self._server_socket.bind((self.server_name, self.server_port))

        print("Server started!")
        print("Waiting for clients...")
        print("Got connection from", self.server_name, self.server_port)
        self._server_socket.listen(100)

    def listen_to_clients(self):
        """Listen for incoming client connections and create threads to handle them."""
        while 1:
            connection_socket, addr = self._server_socket.accept()
            clients[connection_socket.fileno()] = connection_socket

            t = threading.Thread(target=self.reply, args=(connection_socket, addr))

            t.start()

            self._server_socket.close()

    def accept(self):
        """Accept a client connection and return the client socket and address."""
        connection_socket, addr = self._server_socket.accept()
        return connection_socket, addr

    def add_user(self, user: User) -> bool:
        """
        Add a user to the list of users.

        Args:
            user (User): The user object to add.

        Returns:
            bool: True if the user is successfully added, False if the user already exists.
        """
        if user in users:
            return False
        users.append(user)
        return True

    def broadcast(self, m: str) -> bool:
        """
        Broadcast a message to all connected clients.

        Args:
            m (str): The message to broadcast.

        Returns:
            bool: True if the message is successfully broadcasted.
        """
        for client in clients.values():
            client.send(m)
        return True

    def greet(self, username: str, clientSocket):
        """Send a welcome message to a client."""
        welcome_str = "Hi " + username + ", welcome to the chat room."
        print(welcome_str)
        clientSocket.send(welcome_str.encode())

    def get_all_users(self):
        """Get a list of all connected users."""
        response = ""
        for user in users:
            response += user.username + ","
        return response

    def send_private_msg(self, msg, receivers: str):
        """
        Send a private message to specific users.

        Args:
            msg (str): The private message.
            receivers (str): A comma-separated list of usernames who should receive the message.
        """
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
                pr_msg = "Private message from " + user.username
                msg = request_dict["message"]
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
    SERVER_PORT = 21001

    server = Server(SERVER_NAME, SERVER_PORT)

    try:
        server.binding_port()
    except ServerException as e:
        raise ServerException(f"{SERVER_NAME}:{SERVER_PORT} :{str(e)}")

    while 1:
        connection_socket, addr = server._server_socket.accept()
        clients[connection_socket.fileno()] = connection_socket

        t = threading.Thread(target=server.reply, args=(connection_socket, addr))

        t.start()

    server._server_socket.close()

    # server.listen_to_clients()
