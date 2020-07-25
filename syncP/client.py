import threading
import os
import socket
from player import player


class sock:
    def __init__(self, port, host):
        self.port = port
        self.host = host

    def start(self):
        try:
            s = socket.socket()
            print("socket created")
            s.connect((self.host, self.port))
            print(s.recv(1024).decode())
            return s
        except Exception as e:
            print(e)

def playing(p, conn):
    print("thread created successfullyy")
    while 1:
        data = conn.recv(1024).decode()
        if data=="toggle":
            p.toggle()
        elif data=="":
            p.quit()
            break
        elif data.find("sync: ") == 0:
            p.player.seek(data[6:],reference="absolute")

    print("thread completed")

def config():
    # os.system('cls' if os.name == 'nt' else 'clear')
    if "config" in os.listdir():
        print("Use last entered config? [Y/n]")
        host = None
        port = None
        s = input()
        s = s.lower()
        if s=="\n" or s=="y":
            with open("config", 'r') as f:
                temp = f.read().split("~")
                host, port = temp[0], temp[1]
        else:
            print("Enter host url: ")
            host = input()
            print("Enter Port: ")
            port = int(input())

            with open("config", 'w') as f:
                f.write(host+"~"+str(port))
    else:
        print("Enter host url: ")
        host = input()
        print("Enter Port: ")
        port = int(input())

        with open("config", 'w') as f:
            f.write(host+"~"+str(port))


    return (host, port)


def run():
    host, port = config()
    try:
        p = player()
        s = sock(port, host)
        conn = s.start()
        if conn==None:
            raise EOFError
        t = threading.Thread(target=playing, args=(p, conn,))
        try:
            t.start()
            p.start(conn)
        except Exception as e:
            print(e)
        conn.close()
        print("App Closed!")
    except Exception as e:
        print(e)

