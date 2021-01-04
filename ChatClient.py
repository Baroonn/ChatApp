import threading
from socket import *

HOST = '192.168.43.115'
PORT = 22334
BUFSIZ = 1024
ADDR = (HOST, PORT)

def send_message():
    while True:
        message = input()
        chat_client.send(message.encode('utf-8'))

def recv_message():
    while True:
        message = chat_client.recv(BUFSIZ).decode('utf-8')
        print (message)

chat_client = socket(AF_INET, SOCK_STREAM)
chat_client.connect(ADDR)

while True:
    incoming = chat_client.recv(BUFSIZ).decode('utf-8')
    print (incoming)
    if incoming == 'welcome':
        break
    outgoing = input()
    chat_client.send(outgoing.encode('utf-8'))

send_thread = threading.Thread(target = send_message)
recv_thread = threading.Thread(target = recv_message)

send_thread.start()
recv_thread.start()
