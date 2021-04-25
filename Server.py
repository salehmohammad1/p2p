from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import emoji
from emoji import emojize

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s connected" % client_address)
        client.send("Enter your name and click send".encode("utf-8"))
        #client.send(print("Python is " + emojize(":thumbs_up:")))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = """Welcome %s! For the exit he sent "Bye(*)“ """ % name
    client.send(welcome.encode("utf-8"))
    msg = "%s joined!" % name
    print(emoji.emojize(":grinning_face_with_big_eyes:"))
    broadcast(msg.encode("utf-8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != "bye(*)".encode("utf-8"):
            broadcast(msg, name + ": ")
        else:
            client.close()
            del clients[client]
            broadcast("%s leave the room" % name.encode("utf-8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(prefix.encode("utf-8") + msg)


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("the server is up!")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()