import threading
from datetime import datetime
from socket import *

sent_msg = []


class Client:
    def __init__(self, server_name, server_port):
        self.server_name = server_name
        self.server_port = server_port

    def connecting_to_server(self):
        self._client_socket = socket(AF_INET, SOCK_STREAM)
        self._client_socket.connect((SERVER_NAME, SERVER_PORT))
        print(f"connected to {SERVER_NAME}:{SERVER_PORT}")

    def send(self, message: str):
        self._client_socket.send(str(message).encode())

    def log(self, message: str):
        now = datetime.now()
        log = message + "\n\t" + now.strftime("%H:%M:%S")
        sent_msg.append(log)

    def receive_and_print(self):
        for message in iter(lambda: self._client_socket.recv(1024).decode(), ""):
            # inbox.append(message)
            print(":", message)
            print("")

    def disconnect(self):
        self._client_socket.close()


if __name__ == "__main__":
    SERVER_NAME = "127.0.0.1"
    SERVER_PORT = 21000

    client = Client(SERVER_NAME, SERVER_PORT)

    client.connecting_to_server()

    # message protocol
    print(
        """1.Hello <user_name>\n2.Please send the list of attendees.\n3.Public message, length=<message_len>:
    <message_body>\n4.Private message, length=<message_len> to <user_name1>,<user_name2>,<user_name3>,<user_name4>:
    <message_body>\n5.Bye."""
    )

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

        client.send(body)
