from socket import *
import threading
from time import ctime

HOST = '192.168.43.115'
PORT = 22334
BUFSIZ = 1024
ADDR = (HOST, PORT)
users = []
USERS = []

class User(object):
    def __init__(self, n, c):
        self.name = n
        self.conn = c

def handle_client(conn, addr):
    try:
        conn.send(b'Enter desired username: ')
        while True:  
            new_name = conn.recv(BUFSIZ).decode('utf-8')
            if new_name in users:
                conn.send(b'Username exists. Try Again. ')
            else:
                users.append(new_name)
                conn.send(b'welcome')
                break
        new_user = User(new_name, conn)
        USERS.append(new_user)
        print ('NEW CONNECTION BOSS...', new_name)

        connected = True

        while connected:
            message = conn.recv(BUFSIZ).decode('utf-8')
            if not message:
                break
            new_message = '[%s] %s:%s' %(ctime(), new_name, message)
            print (new_message)
            for i in USERS:
                if i.name != new_name:
                    i.conn.send(new_message.encode('utf-8'))

    except:
        USERS.remove(new_user)
        users.remove(new_name)

    conn.close()

chat_server = socket(AF_INET, SOCK_STREAM)
chat_server.bind(ADDR)
chat_server.listen(5)
print ('SERVER IS LISTENING ON...', HOST)

while True:
    conn, addr = chat_server.accept()
    thread = threading.Thread(target = handle_client, args = [conn, addr])
    thread.start()

chat_server.close()
