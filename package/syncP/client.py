import threading
import os
import sys
import time
import socket
import inspect
from syncP.player import player
from syncP.host import node, list

# socket class to instantiate socket connection and start accepting new connections to the socker
class sock:

    # Specifying the host url and port input at runtime or from file
    # Params: Port, host
    def __init__(self, port, host):
        self.port = int(port)
        self.host = host

    # Connecting to a socket using the host url and port 
    # Params: None
    def start(self):
        try:
            s = socket.socket()
            print("socket created")
            s.connect((self.host, self.port))
            payload = s.recv(1024).decode()
            s.send("veryVeryverySecretString".encode())
            return (s, payload)
        except Exception as e:
            print(e)

# Playing is spawned in a new thread to listen for incoming messages from host
# Params: player object, connection
def playing(p, conn):
    print("thread created successfullyy")
    while 1:
        data = conn.recv(1024).decode()
        if data=="toggle":
            p.toggle()
        elif data=="pause":
            p.pause()
        elif data.find("sync: ") == 0:
            p.player.seek(data[6:],reference="absolute")
        elif data=="" or data=="quit":
            p.quit()
            break

    print("\nPlayer Close!")


def keep_alive(conn):
    while True:
        conn.send("KeepAlive".encode())
        time.sleep(200)


# Config method to get host and port for connection at runtime of prev stored file
# The host and port are written to a file everytime a input is used
def config():
    own_path=inspect.getfile(player)[:-9]
    config_path = os.path.join(own_path, 'config')
    if "config" in os.listdir(own_path):
        host = None
        port = None
        temp = None
        with open(config_path, 'r') as f:
                temp = f.read().split("~")
                print("\nLast Config Stored: ")
                print("Host: "+temp[0])
                print("Port: "+temp[1])
        print("\n\nUse last entered config? [Y/n]")
        s = input()
        s = s.lower()
        if s=="" or s=="y":
            host, port = temp[0], temp[1]
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Enter host url: ")
            host = input()
            print("Enter Port: ")
            port = int(input())

            with open(config_path, 'w') as f:
                f.write(host+"~"+str(port))
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Enter host url: ")
        host = input()
        print("Enter Port: ")
        port = int(input())

        with open(config_path, 'w') as f:
            f.write(host+"~"+str(port))


    return (host, port)

# Run methos is called by the entry method to orchestrate the entire client script
def run():
    host, port = config()
    try:
        p = player()
        s = sock(port, host)
        conns_list = list()
        conn, payload = s.start()
        if conn==None:
            raise EOFError

        temp = node(conn)
        conns_list.append(temp)

        t = threading.Thread(target=playing, args=(p, conn,))
        ka = threading.Thread(target=keep_alive, args=(conn,))

        try:
            t.start()
            ka.start()
            p.start(conns_list, payload)
        except Exception as e:
            print(e)

        conns_list.head.conn.close()
        sys.exit()
        print("App Closed!")
    except Exception as e:
        print(e)

# Entry point if the script is called separately
if __name__ == "__main__":
    run()

