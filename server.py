import re
import threading
from socket import *

clients = {}  # client information
users = {}  # client sockets for broadcast
threads = [] # list of threads
usernames = [] # list of usernames


# broadcast function
def broadcast(m):
    # iterate Clients and sending message for everyone
    for client in clients.values():
        client.send(m)


# this function is for receiving message and answer to them
def client_send(clientSocket, addr):
    request = b''
    while request != b"Bye.":
        # receiving messages from clients
        request = clientSocket.recv(1024)
        # decode message
        request.decode()
        if request[0:5] == b'Hello':
            # print('hello')
            # finding username
            username = request[6:]
            # checking username  to other usernames
            if not username in users:
                usernames.append(username)
                # welcome message
                welcome_str = b"Hi " + username + b", welcome to the chat room."
                print(welcome_str)
                # send welcome message to user
                clientSocket.send(welcome_str)
                # send noftication message for other users
                notification_str = username + b" join the chat room."
                print(notification_str)
                broadcast(notification_str)
                # save socket for sending broadcast and Private message
                users[username] = clientSocket
            else:
                # sending error message to user because username was taken
                er_str = b'''username  is exist please try again!'''
                print(er_str)
                clientSocket.send(er_str)
        elif request == b'Bye':
            # print('bye')
            # sending a message  for other users  that this user left chat room
            msg = username + b" left the chat room."
            print(msg)
            broadcast(msg)
            # remove username from list
            usernames.remove(username)
            break;
        elif request == b'Please send the list of attendees.':
            # print('list')
            # sending list of attendees
            response = b'Here is the list of attendees:\n'
            # iterate all usernames and make the string and send to user
            for user in usernames:
                response = response + user + b','
            print(response[:-1])
            clientSocket.send(response)
        elif request[0:6] == b'Public':
            # print('public')
            # getting information about public message
            public_str = request[:13] + b' from ' + username + request[13:]
            # finding and return length in message with regex and concat it to int
            length = int(re.findall(r'\d+', str(request))[0])
            # receiving  message body
            public_msg = clientSocket.recv(length)
            # print the message
            print(username, ":", public_msg.decode())
            # creating message response  to broadcast
            public_response = str(public_str) + "\r\n" + str(public_msg)
            print(username, ":", public_response)
            broadcast(public_response.encode())
        elif request[0:7] == b'Private':

            # print('private')
            pr_msg = b'''Private message from ''' + username

            print(pr_msg)
            # getting information about public message
            # finding length with regex and concat to int
            length = int(re.findall(r'\d+', str(request))[0])
            # receive message body and decode it
            private_msg = clientSocket.recv(length).decode()
            pr_response = str(pr_msg) + "\r\n" + private_msg
            # encode message for sending
            pr_response_bytes = pr_response.encode()
            # iterate users
            for u in users:
                # finding names in information message
                if u in request:
                    # send them message
                    users[u].send(pr_response_bytes)
        else:
            # SENDING AND PRINTING ERROR FOR UNAVAILABLE MESSAGE
            er_strr = 'undefined command'
            print(er_strr)
            clientSocket.send(er_strr.encode())
        # print("done")


server_name = ""  # server name(local host)
server_port = 21000  # server port

# creating and binding Tcp socket for server
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_name, server_port))
print('Server started!')
print('Waiting for clients...')
print('Got connection from', server_name, server_port)
# listening  to  users
server_socket.listen(100)

while 1:
    # a client connect  to  server and we should accept them for the rest
    connection_Socket, addr = server_socket.accept()
    # saving connection Socket
    clients[connection_Socket.fileno()] = connection_Socket
    # creating thread for answering to multiple clients
    t = threading.Thread(target=client_send, args=(connection_Socket, addr))
    # start the thread
    t.start()
# closing the sever socket
server_socket.close()




#end  of file 

