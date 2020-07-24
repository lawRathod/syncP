import threading
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
        print(data)
        if data=="toggle":
            p.toggle()
        elif data=="quit":
            p.quit()
        elif data=="":
            break

    print("thread completed")


if __name__ == "__main__":
    print("Enter host url: ")
    host = input()

    print("Enter Port: ")
    port = int(input())


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

