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

