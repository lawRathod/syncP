import threading
import os
import socket
import inspect
from syncP.player import player


class sock:
    def __init__(self, port, host):
        self.port = int(port)
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
            raise e
        conn.close()
        print("App Closed!")
    except Exception as e:
        raise e

if __name__ == "__main__":
    run()

