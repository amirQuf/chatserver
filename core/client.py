import threading
from datetime import datetime
from socket import *
from dataclasses import dataclass



@dataclass
class Message:
    """Represents a message with a message body and timestamp."""
    message: str
    date: datetime


class Client:
    def __init__(self, server_name, server_port):
        """
        Initialize a Client instance.

        Args:
            server_name (str): The server's hostname or IP address.
            server_port (int): The port to connect to on the server.
        """
        self.server_name = server_name
        self.server_port = server_port
        self.sent_msg = []
        self.inbox = []
        self.logs = []


    def connecting_to_server(self):
        """
        Connect to the server.
        """
        self._client_socket = socket(AF_INET, SOCK_STREAM)
        self._client_socket.connect((self.server_name, self.server_port))
        print(f"connected to {self.server_name}:{self.server_port}")

    def send(self, message: str):
        """
        Send a message to the server.

        Args:
            message (str): The message to send to the server.
        """
        self._client_socket.send(str(message).encode())

    def log(self, message: str):
        """
        Log a message with a timestamp.

        Args:
            message (str): The message to log.
        """
        now = datetime.now()
        log = message + "\n\t"
        message = Message(message=log, date=now)
        self.logs.append(message)

    def receive_and_print(self):
        """
        Receive and print messages from the server.
        """
        for message in iter(lambda: self._client_socket.recv(1024).decode(), ""):
            self.inbox.append(message)
            print("SERVER>>", message)
            print("")

    def disconnect(self):
        """
        Disconnect from the server.
        """
        self._client_socket.close()


if __name__ == "__main__":
    SERVER_NAME = "127.0.0.1"
    SERVER_PORT = 21001

    help = """1.Hello <user_name>\n2.Please send the list of attendees.\n3.Public message, length=<message_len>:
    <message_body>\n4.Private message, length=<message_len> to <user_name1>,<user_name2>,<user_name3>,<user_name4>:
    <message_body>\n5.Bye."""
    client = Client(SERVER_NAME, SERVER_PORT)

    client.connecting_to_server()

    # message protocol
    print(help)

    background_thread = threading.Thread(target=client.receive_and_print)
    background_thread.daemon = True
    # start thread
    background_thread.start()
    while 1:
        print("Instruction code:")
        code = int(input())

        body = {
            "code": code,
        }
        if code == 1:
            username = input("username:")
            message = f"Hello {username}"
            body["username"] = username

        elif code == 2:
            message = "Please send the list of attendees."

        elif code == 3:
            message = input("message:")
            body["type"] = "Public"
        elif code == 4:
            message = input("message:")
            receivers = input("receivers:")
            body["receivers"] = receivers
            body["type"] = "Private"
            # encrypt message

        elif code == 5:
            # Bye
            message = "Bye."
            client.disconnect()
        else:
            print("Invalid code")

        body["message"] = message
        client.sent_msg.append(message)
        client.send(body)
