import re
import threading
from datetime import datetime
from socket import *

from pip._vendor.distlib.compat import raw_input

# this is server port and  server address
server_name = "127.0.0.1"
server_port = 21000
print("connecting to server")
# creating a tcp socket
client_socket = socket(AF_INET, SOCK_STREAM)
# connecting to defined server
client_socket.connect((server_name, server_port))
print(f'connected to {server_name}:{server_port}')
# print a defined format to users
print('''1.Hello <user_name>\n2.Please send the list of attendees.\n3.Public message, length=<message_len>:
<message_body>\n4.Private message, length=<message_len> to <user_name1>,<user_name2>,<user_name3>,<user_name4>:
<message_body>\n5.Bye.''')


# a function to receive message and  save inbox  and print it
def receive_and_print():
    for message in iter(lambda: client_socket.recv(1024).decode(), ''):
        inbox.append(message)
        print(":", message)
        print("")


# this thread form getting message from server every second
# creating
background_thread = threading.Thread(target=receive_and_print)
background_thread.daemon = True
# start thread
background_thread.start()
message = ''
inbox = []  # for saving messages
send_msg = []  # for saving commands
while message != "Bye":
    # getting input from std
    message = raw_input()
    now = datetime.now()
    # adding a time to commands
    log = message + "\n\t" + now.strftime("%H:%M:%S")
    send_msg.append(log)
    # append  log to  commands
    if message[0:6] == "Private" or message[0:5] == "Public":
        # send message
        client_socket.send(message.encode())
        # get another input
        especial_msg = raw_input()
        # finding length with regex
        length = int(re.findall(message, r"\d+")[0])
        # checking length
        if len(especial_msg) == length:
            client_socket.send(message.encode())
        else:
            # print error
            print("try again")
    else:
        # sending message
        client_socket.send(message.encode())
