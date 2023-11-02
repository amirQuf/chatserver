
from .client import Client
import pytest
from .server import  Server
import threading

clients =[]

@pytest.fixture
def server_setup():
    SERVER_NAME = ""
    SERVER_PORT = 21003
    server = Server(SERVER_NAME, SERVER_PORT)
    while 1:
        connection_socket, addr = server._server_socket.accept()
        clients[connection_socket.fileno()] = connection_socket

        t = threading.Thread(target=server.reply, args=(connection_socket, addr))

        t.start()

    server._server_socket.close()

    yield server
    if server._server_socket:
        server._server_socket.close()




@pytest.fixture
def  client_instance():
    SERVER_NAME = "127.0.0.1"
    SERVER_PORT = 21003
    client = Client(SERVER_NAME, SERVER_PORT)
    client.connecting_to_server()
    yield client
    client.disconnect()


test_msgs = [    
{   "code": 1,
    "username":'test_user',
    "message" : "Hello test_user"

},{
    "code": 2,
    "message": "Please send the list of attendees."
},{
    "code":3,
    "message":"Test message",
    "type" : "Public"
},{
    "code":4,
    "message":"Test message",
    "type" : "Private"

},{
    "code": 5,
    "message":"Bye."
}
]

@pytest.fixture(params=test_msgs)
def generate_test_msg(request):
    return request.params


    

def test_send_msg(client_instance,server_setup):
      
    body = {}
    test_username = 'test_user'
    test_message = f"Hello {test_username}"
    body["username"] = test_username
    body["code"]=1
    body["message"] = test_message
    client_instance.send(body)
    
    client_instance.receive_and_print()
    assert test_message in client_instance.inbox 

