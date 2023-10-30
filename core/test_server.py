import pytest
from .server import Server,User


@pytest.fixture
def server_instance():
    SERVER_NAME = ""
    SERVER_PORT = 21001
    server = Server(SERVER_NAME, SERVER_PORT)

    yield server
    if server._server_socket:
        server._server_socket.close()


def test_binding_port(server_instance):
    server_instance.binding_port()
    assert server_instance._server_socket is not None


def test_add_user(server_instance):
    user = User("testuser", ("127.0.0.1", 12345))
    result = server_instance.add_user(user)
    assert result is True


def test_add_same_user(server_instance):
    user1 = User("testuser", ("127.0.0.1", 12345))
    result1 = server_instance.add_user(user1)
    user2 = User("testuser", ("127.0.0.1", 12345))
    result2 = server_instance.add_user(user2)
    assert result2 is False


from .client import Client



@pytest.fixture
def  client_instance():
    SERVER_NAME = "127.0.0.1"
    SERVER_PORT = 21001
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


def test_send_msg(client_instance,server_instance):
    body = {}
    test_username = 'test_user'
    test_message = f"Hello {test_username}"
    body["username"] = test_username
    body["code"]=1
    body["message"] = test_message
    
    client_instance.send(body)
    client_instance.receive_and_print()
    assert test_message in client_instance.inbox 

