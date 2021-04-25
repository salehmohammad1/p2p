from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import emoji
from emoji import emojize

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(msg.encode("utf-8"))
    #client_socket.send(msg.emoji.emojize('python is :thumbs_up:'))
    #print("Python is " + emojize(":thumbs_up:"))
    if msg == "bye(*)":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("bye(*)")
    send()

top = tkinter.Tk()
top.title("chat room")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, bg="cyan")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width=43)
entry_field.bind("<Return>", send)
entry_field.pack(side=tkinter.LEFT)
send_button = tkinter.Button(top, text="send", command=send)
send_button.pack(side=tkinter.LEFT)

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = "127.0.0.1"
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()